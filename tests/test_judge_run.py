"""The judge runner: three batches in parallel, cached, honest about what it could not check."""
import threading

from surveycoach.judge.batches import BATCHES
from surveycoach.judge.cache import JudgeCache
from surveycoach.judge.judge import run_judge
from surveycoach.judge.prompts import survey_block
from surveycoach.judge.schemas import AiFinding, BatchOutput, BlockerCall, Verdict
from surveycoach.llm import ASSESSMENT_MODEL, FakeProvider, LlmError, LlmUnavailable
from surveycoach.rubric import load_rubric
from tests.builders import intro, page, question, survey, thank_you

RUBRIC = load_rubric()


def snapshot():
    return survey(intro("Welcome! This takes about 3 minutes."),
                  page(1, question("q1", "How much did you LOVE the amazing softness?")), thank_you())


def batch_of(system: str):
    return next(b for b in BATCHES if f"Your job in this call: {b.title}" in system)


def all_clear(system: str, data: str) -> BatchOutput:
    batch = batch_of(system)
    return BatchOutput(verdicts=[Verdict(criterion_id=c, fraction=1.0) for c in batch.criteria],
                       blockers=[BlockerCall(blocker_id=b, triggered=False) for b in batch.blockers])


def provider(answer=all_clear) -> FakeProvider:
    return FakeProvider({"BatchOutput": answer})


def everything() -> set[str]:
    return {x for b in BATCHES for x in (*b.criteria, *b.blockers)}


def test_every_batch_is_called_once_with_its_own_prompt_and_the_survey_block():
    fake = provider()
    results, info = run_judge(snapshot(), RUBRIC, fake)
    assert set(results) == everything() and info.checked == ["wording", "story", "flow"] and info.failed == {}
    assert info.model == ASSESSMENT_MODEL and len(fake.calls) == 3
    assert {data for _, data, _ in fake.calls} == {survey_block(snapshot())}
    assert sorted(batch_of(system).id for system, _, _ in fake.calls) == ["flow", "story", "wording"]


def test_the_three_calls_really_run_at_the_same_time():
    barrier = threading.Barrier(3, timeout=5)        # releases only when all three calls are in flight together

    def waits_for_the_others(system: str, data: str) -> BatchOutput:
        barrier.wait()
        return all_clear(system, data)

    results, info = run_judge(snapshot(), RUBRIC, provider(waits_for_the_others))
    assert info.failed == {} and set(results) == everything()


def test_a_second_run_with_the_same_cache_makes_no_calls(tmp_path):
    cache = JudgeCache(tmp_path)
    run_judge(snapshot(), RUBRIC, provider(), cache)
    fake = provider()
    _, info = run_judge(snapshot(), RUBRIC, fake, cache)
    assert fake.calls == [] and info.from_cache == ["wording", "story", "flow"] and info.checked == ["wording", "story", "flow"]


def test_the_cache_key_changes_with_the_model_the_prompt_the_rubric_and_the_survey(tmp_path, monkeypatch):
    cache, batch = JudgeCache(tmp_path), BATCHES[0]
    base = cache.key(snapshot(), RUBRIC, batch)
    monkeypatch.setattr("surveycoach.judge.cache.ASSESSMENT_MODEL", "some-other-model")
    assert cache.key(snapshot(), RUBRIC, batch) != base
    monkeypatch.undo()
    monkeypatch.setattr("surveycoach.judge.cache.PROMPT_VERSION", "999")
    assert cache.key(snapshot(), RUBRIC, batch) != base
    monkeypatch.undo()
    other = survey(intro(), page(1, question("q1", "A different question?")), thank_you())
    assert cache.key(other, RUBRIC, batch) != base and cache.key(snapshot(), RUBRIC, BATCHES[1]) != base


def test_a_failed_batch_is_isolated_named_and_never_cached(tmp_path):
    def story_fails(system: str, data: str) -> BatchOutput:
        if batch_of(system).id == "story":
            raise LlmError("Wibey timed out after 180 s")
        return all_clear(system, data)

    cache = JudgeCache(tmp_path)
    results, info = run_judge(snapshot(), RUBRIC, provider(story_fails), cache)
    assert not set(BATCHES[1].criteria) & set(results) and set(BATCHES[0].criteria) <= set(results)
    assert info.failed == {"story": "Wibey timed out after 180 s"} and info.checked == ["wording", "flow"]
    retry = provider()
    _, info2 = run_judge(snapshot(), RUBRIC, retry, cache)
    assert [batch_of(s).id for s, _, _ in retry.calls] == ["story"] and info2.failed == {}   # only the failed batch re-runs


def test_an_unavailable_model_never_raises_it_just_checks_nothing():
    def down(system: str, data: str):
        raise LlmUnavailable("Wibey is not installed")

    results, info = run_judge(snapshot(), RUBRIC, provider(down))
    assert results == {} and set(info.failed) == {"wording", "story", "flow"} and info.checked == []


def test_findings_that_cannot_be_backed_up_are_reported_as_dropped_with_their_batch(tmp_path):
    invented = AiFinding(criterion_id="5.1", page_id="p1", question_id="q1", headline="h", evidence="never said this",
                         explanation="x", member_impact="m")

    def invents(system: str, data: str) -> BatchOutput:
        out = all_clear(system, data)
        return out.model_copy(update={"findings": [invented]}) if batch_of(system).id == "wording" else out

    cache = JudgeCache(tmp_path)
    results, info = run_judge(snapshot(), RUBRIC, provider(invents), cache)
    assert results["5.1"].findings == [] and info.dropped and info.dropped[0].startswith("wording: 5.1")
    replay_results, replay = run_judge(snapshot(), RUBRIC, provider(), cache)             # grounding re-runs on cached answers
    assert replay_results["5.1"].findings == [] and replay.dropped == info.dropped


def test_without_a_cache_nothing_is_written_to_disk(tmp_path, monkeypatch):
    monkeypatch.setenv("SURVEYCOACH_HOME", str(tmp_path))
    run_judge(snapshot(), RUBRIC, provider())
    assert list(tmp_path.iterdir()) == []


def test_a_corrupt_cache_file_is_a_miss_not_a_crash(tmp_path):
    cache = JudgeCache(tmp_path)
    (tmp_path / f"{cache.key(snapshot(), RUBRIC, BATCHES[0])}.json").write_text("{not json")
    fake = provider()
    _, info = run_judge(snapshot(), RUBRIC, fake, cache)
    assert info.failed == {} and len(fake.calls) == 3


def test_the_default_cache_folder_follows_surveycoach_home(tmp_path, monkeypatch):
    monkeypatch.setenv("SURVEYCOACH_HOME", str(tmp_path))
    assert JudgeCache().root == tmp_path / "cache"
