"""Scoring: a plain weighted sum over active criteria (exactly 100 points), plus readiness."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from surveycoach.findings import CheckResult
from surveycoach.rubric import Rubric

Readiness = Literal["ready", "almost_ready", "needs_work"]


class DimensionScore(BaseModel):
    name: str
    earned: float
    possible: int


class ScoreCard(BaseModel):
    score: float
    provisional: bool
    unchecked_points: int
    by_dimension: dict[str, DimensionScore]
    open_blockers: list[str]
    kept_blockers: list[str]
    readiness: Readiness
    strengths: list[str]


def score(rubric: Rubric, results: dict[str, CheckResult], kept_blockers: frozenset[str] = frozenset()) -> ScoreCard:
    """Unchecked criteria get full credit but flag the score as provisional (never a silent penalty)."""
    earned: dict[str, float] = {}
    unchecked = 0
    for criterion in rubric.criteria:
        if not criterion.active:
            continue
        result = results.get(criterion.id)
        if result is None or result.fraction is None:
            unchecked += criterion.points
            earned[criterion.id] = float(criterion.points)
        else:
            earned[criterion.id] = criterion.points * result.fraction

    by_dimension = {
        d.id: DimensionScore(
            name=d.name,
            earned=sum(earned[c.id] for c in rubric.criteria if c.dimension == d.id and c.active),
            possible=d.points,
        )
        for d in rubric.dimensions
    }
    total = sum(earned.values())
    flagged = [b.id for b in rubric.blockers if _is_failed(results.get(b.id))]
    open_blockers = [b for b in flagged if b not in kept_blockers]
    kept = [b for b in flagged if b in kept_blockers]

    return ScoreCard(
        score=total,
        provisional=unchecked > 0,
        unchecked_points=unchecked,
        by_dimension=by_dimension,
        open_blockers=open_blockers,
        kept_blockers=kept,
        readiness=_readiness(rubric, total, bool(open_blockers)),
        strengths=_strengths(rubric, results),
    )


def _is_failed(result: CheckResult | None) -> bool:
    return bool(result) and any(f.severity == "must_fix" for f in result.findings)


def _readiness(rubric: Rubric, total: float, has_open_blocker: bool) -> Readiness:
    if has_open_blocker or total < rubric.readiness.almost_min:
        return "needs_work"
    return "ready" if total >= rubric.readiness.ready_min else "almost_ready"


def _strengths(rubric: Rubric, results: dict[str, CheckResult]) -> list[str]:
    """Top 3 criteria that were actually checked and earned full credit, heaviest first."""
    full = [
        c for c in rubric.criteria
        if c.active and (r := results.get(c.id)) is not None and r.fraction == 1.0
    ]
    full.sort(key=lambda c: (-c.points, c.id))
    return [c.title for c in full[:3]]
