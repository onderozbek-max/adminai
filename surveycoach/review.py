"""The review pipeline: snapshot in, scored review out. Pure and deterministic."""
from __future__ import annotations

from pydantic import BaseModel

from surveycoach.checks import run_all
from surveycoach.checks.registry import ReviewContext
from surveycoach.findings import CheckResult, Finding
from surveycoach.rubric import Rubric, load_rubric
from surveycoach.scoring import ScoreCard, score
from surveycoach.snapshot import SurveySnapshot
from surveycoach.timing import Timing


class Review(BaseModel):
    survey_title: str
    content_hash: str
    rubric_version: str
    scorecard: ScoreCard
    findings: list[Finding]
    unchecked: list[str]            # titles of active criteria no check could judge yet
    est_minutes: float
    promised_minutes: float | None
    timing: Timing
    results: dict[str, CheckResult]


def _merge(results: dict[str, CheckResult], rubric: Rubric) -> list[Finding]:
    """De-duplicate by fingerprint; must-fix first, then rubric order."""
    order = {cid: i for i, cid in enumerate([b.id for b in rubric.blockers] + [c.id for c in rubric.criteria])}
    unique: dict[str, Finding] = {}
    for result in results.values():
        for f in result.findings:
            unique.setdefault(f.fingerprint, f)
    return sorted(unique.values(), key=lambda f: (f.severity != "must_fix", order.get(f.criterion_id, 999)))


def run_review(snapshot: SurveySnapshot, rubric: Rubric | None = None,
               kept_blockers: frozenset[str] = frozenset()) -> Review:
    rubric = rubric or load_rubric()
    context = ReviewContext.build(snapshot, rubric)
    results = run_all(context)
    unchecked = [c.title for c in rubric.criteria if c.active
                 and ((r := results.get(c.id)) is None or (r.applies and r.fraction is None))]
    return Review(
        survey_title=snapshot.title, content_hash=snapshot.content_hash, rubric_version=rubric.version,
        scorecard=score(rubric, results, kept_blockers), findings=_merge(results, rubric), unchecked=unchecked,
        est_minutes=context.timing.minutes, promised_minutes=context.promised_minutes,
        timing=context.timing, results=results)
