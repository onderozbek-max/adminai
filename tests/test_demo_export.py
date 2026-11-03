import json
from pathlib import Path

from surveycoach.demo_export import SITE_DATA, build_demo_data, render_data_js

ROOT = Path(__file__).parent.parent


def parsed() -> dict:
    prefix = "window.SURVEYCOACH_DEMO = "
    text = render_data_js(build_demo_data())
    assert text.startswith(prefix) and text.rstrip().endswith(";")
    return json.loads(text[len(prefix):].rstrip().rstrip(";"))


def test_committed_site_data_is_not_stale():
    assert SITE_DATA.read_text() == render_data_js(build_demo_data()), \
        "Run: .venv/bin/python -m surveycoach.demo_export"


def test_data_js_is_pure_ascii_so_no_literal_emoji_in_any_file():
    assert render_data_js(build_demo_data()).isascii()


def test_both_samples_with_reviews_and_snapshots():
    data = parsed()
    assert [s["id"] for s in data["surveys"]] == ["boxer-briefs", "coffee-pods"]
    boxer = data["surveys"][0]
    assert boxer["review"]["scorecard"]["readiness"] == "needs_work"
    assert boxer["review"]["findings"][0]["severity"] == "must_fix"
    assert boxer["snapshot"]["pages"][0]["kind"] == "intro"


def test_criteria_lookup_covers_every_finding_so_the_page_can_name_them():
    data = parsed()
    cited = {f["criterion_id"] for s in data["surveys"] for f in s["review"]["findings"]}
    assert cited <= set(data["criteria"])
    assert data["criteria"]["6.3"]["title"]


def test_demo_says_it_is_sample_data_that_changes_nothing_in_redjade():
    disclaimer = parsed()["disclaimer"].lower()
    assert "sample" in disclaimer and "redjade" in disclaimer
