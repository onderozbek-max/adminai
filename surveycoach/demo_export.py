"""Precompute the demo site's data from the real engine, so the page only displays results.

Run: .venv/bin/python -m surveycoach.demo_export
"""
from __future__ import annotations

import json
from pathlib import Path

from surveycoach.review import run_review
from surveycoach.rubric import load_rubric
from surveycoach.snapshot import SurveySnapshot

ROOT = Path(__file__).parent.parent
SITE_DATA = ROOT / "site" / "data.js"
DISCLAIMER = ("Sample data: two made-up surveys. SurveyCoach never reads or changes anything in RedJade; "
              "you copy the fixes and apply them yourself.")
DISCLAIMER_SHORT = "Sample data. SurveyCoach never reads or edits RedJade; you copy fixes yourself."
SAMPLES = [
    ("boxer-briefs", "A deliberately flawed sample. Shows what a review catches and how it explains each fix."),
    ("coffee-pods", "A clean sample. It still cannot be called Ready to launch, because the AI step has not run."),
]


def _survey(sample_id: str, blurb: str) -> dict:
    snapshot = SurveySnapshot.model_validate_json((ROOT / "fixtures" / f"{sample_id}.json").read_text())
    review = run_review(snapshot)
    return {
        "id": sample_id, "title": snapshot.title, "blurb": blurb,
        "review": review.model_dump(mode="json", exclude={"results", "timing"}),
        "timeline": [{"page_id": p.page_id, "seconds": round(p.cumulative_seconds)} for p in review.timing.pages],
        "total_seconds": round(review.timing.total_seconds),
        "snapshot": snapshot.model_dump(mode="json", exclude_defaults=True),
    }


def build_demo_data() -> dict:
    rubric = load_rubric()
    return {
        "disclaimer": DISCLAIMER, "disclaimer_short": DISCLAIMER_SHORT,
        "surveys": [_survey(sample_id, blurb) for sample_id, blurb in SAMPLES],
        "dimensions": {d.id: d.name for d in rubric.dimensions},
        "criteria": {**{c.id: {"title": c.title, "dimension": c.dimension, "points": c.points} for c in rubric.criteria},
                     **{b.id: {"title": b.title, "dimension": "blocker", "points": 0} for b in rubric.blockers}},
    }


def render_data_js(data: dict) -> str:
    """ASCII-only (emoji and accents become escapes), stable output."""
    return "window.SURVEYCOACH_DEMO = " + json.dumps(data, indent=1, ensure_ascii=True) + ";\n"


def main() -> None:
    SITE_DATA.parent.mkdir(exist_ok=True)
    SITE_DATA.write_text(render_data_js(build_demo_data()))
    print(f"wrote {SITE_DATA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
