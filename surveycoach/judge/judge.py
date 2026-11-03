"""Run the AI judge: batches in parallel, cached, grounded, and honest about anything it could not check."""
from __future__ import annotations

from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel, Field

from surveycoach.findings import CheckResult, Finding
from surveycoach.judge.batches import BATCHES, Batch
from surveycoach.judge.cache import JudgeCache
from surveycoach.judge.dedupe import dedupe
from surveycoach.judge.grounding import ground
from surveycoach.judge.prompts import survey_block, system_prompt
from surveycoach.judge.schemas import BatchOutput
from surveycoach.llm import ASSESSMENT_MODEL, LlmError, LlmProvider
from surveycoach.rubric import Rubric
from surveycoach.snapshot import SurveySnapshot


class AiRunInfo(BaseModel):
    """What the AI step did, so the screen can say it plainly instead of implying everything was checked."""

    model: str
    checked: list[str] = Field(default_factory=list)          # batch ids that produced an answer
    failed: dict[str, str] = Field(default_factory=dict)      # batch id -> why it could not check
    dropped: list[str] = Field(default_factory=list)          # claims refused because the survey did not back them up
    from_cache: list[str] = Field(default_factory=list)
    merged: list[str] = Field(default_factory=list)           # overlaps removed so each text has one rewrite


def _answer(batch: Batch, snapshot: SurveySnapshot, rubric: Rubric, provider: LlmProvider,
            cache: JudgeCache | None, known: Sequence[Finding]) -> tuple[BatchOutput | None, bool, str]:
    """(output, came_from_cache, failure reason). Failures are returned, never raised: one batch must not sink the rest."""
    key = cache.key(snapshot, rubric, batch, known) if cache else None
    if cache and (hit := cache.get(key)) is not None:
        return hit, True, ""
    try:
        output = provider.complete_json(system_prompt(batch, rubric), survey_block(snapshot, known), BatchOutput)
    except LlmError as error:
        return None, False, str(error)
    if cache:
        cache.put(key, output)
    return output, False, ""


def run_judge(snapshot: SurveySnapshot, rubric: Rubric, provider: LlmProvider, cache: JudgeCache | None = None,
              workers: int = 3, known: Sequence[Finding] = ()) -> tuple[dict[str, CheckResult], AiRunInfo]:
    """`known` are the problems code already found: the judge is told to skip them."""
    info = AiRunInfo(model=ASSESSMENT_MODEL)
    results: dict[str, CheckResult] = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [(batch, pool.submit(_answer, batch, snapshot, rubric, provider, cache, known)) for batch in BATCHES]
        for batch, future in futures:                      # collected in rubric order, so output is deterministic
            output, cached, failure = future.result()
            if output is None:
                info.failed[batch.id] = failure
                continue
            info.checked.append(batch.id)
            if cached:
                info.from_cache.append(batch.id)
            grounded = ground(output, batch, snapshot, rubric)
            results.update(grounded.results)
            info.dropped += [f"{batch.id}: {note}" for note in grounded.dropped]
    results, info.merged = dedupe(results, rubric)
    return results, info
