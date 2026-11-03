"""The review pipeline: snapshot in, scored review out. Pure and deterministic."""
from __future__ import annotations

from pydantic import BaseModel

from surveycoach.checks import run_all
from surveycoach.checks.registry import ReviewContext
from surveycoach.findings import CheckResult, Finding
from surveycoach.judge import AiRunInfo, JudgeCache, run_judge
from surveycoach.judge.grounding import CREDIT_CAP_WITH_FINDING
from surveycoach.llm import LlmProvider
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
    ai: AiRunInfo | None = None     # None means the AI step did not run at all


def _merge(results: dict[str, CheckResult], rubric: Rubric) -> list[Finding]:
    """De-duplicate by fingerprint; must-fix first, then rubric order."""
    order = {cid: i for i, cid in enumerate([b.id for b in rubric.blockers] + [c.id for c in rubric.criteria])}
    unique: dict[str, Finding] = {}
    for result in results.values():
        for f in result.findings:
            unique.setdefault(f.fingerprint, f)
    return sorted(unique.values(), key=lambda f: (f.severity != "must_fix", order.get(f.criterion_id, 999)))


def _with_ai(code: dict[str, CheckResult], ai: dict[str, CheckResult]) -> dict[str, CheckResult]:
    """Code wins wherever it judged. Where code left a criterion open (fraction None, for example 9.1 where code only
    checks emoji), the AI supplies the verdict and the code's own findings are kept next to the AI's."""
    merged = dict(code)
    for cid, theirs in ai.items():
        mine = code.get(cid)
        if mine is None:
            merged[cid] = theirs
        elif mine.fraction is None and theirs.fraction is not None:
            findings = [*mine.findings, *theirs.findings]
            fraction = min(theirs.fraction, CREDIT_CAP_WITH_FINDING) if findings else theirs.fraction
            merged[cid] = CheckResult(criterion_id=cid, fraction=fraction, applies=mine.applies, findings=findings)
    return merged


def run_review(snapshot: SurveySnapshot, rubric: Rubric | None = None, kept_blockers: frozenset[str] = frozenset(),
               provider: LlmProvider | None = None, cache: JudgeCache | None = None) -> Review:
    rubric = rubric or load_rubric()
    context = ReviewContext.build(snapshot, rubric)
    results = run_all(context)
    ai: AiRunInfo | None = None
    if provider is not None:
        known = [f for r in results.values() for f in r.findings]
        ai_results, ai = run_judge(snapshot, rubric, provider, cache, known=known)
        results = _with_ai(results, ai_results)
    unchecked = [c.title for c in rubric.criteria if c.active
                 and ((r := results.get(c.id)) is None or (r.applies and r.fraction is None))]
    return Review(
        survey_title=snapshot.title, content_hash=snapshot.content_hash, rubric_version=rubric.version,
        scorecard=score(rubric, results, kept_blockers), findings=_merge(results, rubric), unchecked=unchecked,
        est_minutes=context.timing.minutes, promised_minutes=context.promised_minutes,
        timing=context.timing, results=results, ai=ai)
