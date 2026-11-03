import json

from surveycoach.snapshot import Option, Page, Question, SurveySnapshot


def make_snapshot(option_labels=("A", "B", "C"), text="How was it?") -> SurveySnapshot:
    question = Question(
        id="q1",
        text=text,
        kind="single_choice",
        options=[Option(id=f"o{i}", label=label) for i, label in enumerate(option_labels)],
    )
    return SurveySnapshot(
        title="Help pick our next flavor",
        source_url="https://example.test/s",
        pages=[
            Page(id="p0", position=0, kind="intro", intro_text="Thanks for helping."),
            Page(id="p1", position=1, kind="question", questions=[question]),
        ],
    )


def test_round_trips_through_json():
    snapshot = make_snapshot()
    restored = SurveySnapshot.model_validate(json.loads(snapshot.model_dump_json()))
    assert restored == snapshot


def test_hash_ignores_option_order():
    assert make_snapshot(("A", "B", "C")).content_hash == make_snapshot(("C", "A", "B")).content_hash


def test_hash_changes_with_text():
    assert make_snapshot(text="One").content_hash != make_snapshot(text="Two").content_hash


def test_all_questions_flattens_pages():
    assert [q.id for q in make_snapshot().all_questions()] == ["q1"]


def test_intro_text_comes_from_the_intro_page():
    assert make_snapshot().intro_text == "Thanks for helping."
