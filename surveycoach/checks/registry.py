"""Check registry. A check is a pure function of ReviewContext, registered by rubric ID."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import NamedTuple

from surveycoach.findings import CheckResult, Finding, Severity
from surveycoach.rubric import Rubric
from surveycoach.snapshot import SurveySnapshot
from surveycoach.timing import Timing, estimate, parse_promised_minutes


@dataclass(frozen=True)
class ReviewContext:
    snapshot: SurveySnapshot
    rubric: Rubric
    timing: Timing
    promised_minutes: float | None

    @classmethod
    def build(cls, snapshot: SurveySnapshot, rubric: Rubric) -> "ReviewContext":
        return cls(snapshot, rubric, estimate(snapshot), parse_promised_minutes(snapshot.intro_text))


CheckFn = Callable[[ReviewContext], CheckResult]
REGISTRY: dict[str, CheckFn] = {}


def check(criterion_id: str) -> Callable[[CheckFn], CheckFn]:
    def register(fn: CheckFn) -> CheckFn:
        if criterion_id in REGISTRY:
            raise ValueError(f"check {criterion_id} registered twice")
        REGISTRY[criterion_id] = fn
        return fn
    return register


def finding(criterion_id: str, severity: Severity, headline: str, evidence: str, explanation: str,
            member_impact: str, **where_and_text: str | None) -> Finding:
    """Keyword extras: page_id, question_id, element_id, current_text, suggested_text, highlight."""
    return Finding(criterion_id=criterion_id, severity=severity, headline=headline, evidence=evidence,
                   explanation=explanation, member_impact=member_impact, **where_and_text)


class Problem(NamedTuple):
    """What a check found wrong with one thing, before it is tied to a rubric criterion and a place."""
    headline: str
    evidence: str
    fix: str
    current: str | None = None
    suggested: str | None = None
    highlight: str | None = None


def problem_finding(criterion_id: str, problem: Problem, impact: str, severity: Severity = "worth_improving",
                    **where: str | None) -> Finding:
    return finding(criterion_id, severity, problem.headline, problem.evidence, problem.fix, impact,
                   current_text=problem.current, suggested_text=problem.suggested, highlight=problem.highlight, **where)


def result(criterion_id: str, fraction: float | None, *findings: Finding) -> CheckResult:
    return CheckResult(criterion_id=criterion_id, fraction=fraction, findings=list(findings))


def passed(criterion_id: str) -> CheckResult:
    return result(criterion_id, 1.0)


def not_applicable(criterion_id: str) -> CheckResult:
    return CheckResult(criterion_id=criterion_id, applies=False)


def blocker_ok(blocker_id: str) -> CheckResult:
    return CheckResult(criterion_id=blocker_id)


def clip(text: str, limit: int = 120) -> str:
    """Shorten evidence at a word boundary, with an ellipsis, so it never ends mid-word."""
    if len(text) <= limit:
        return text
    cut = text[:limit]
    space = cut.rfind(" ")
    return (cut[:space] if space > 0 else cut).rstrip(" ,;:") + "..."


def share_fraction(failing: int, total: int) -> float:
    """Proportional credit: the share of items that pass (full credit when there is nothing to judge)."""
    return 1.0 if total == 0 else round(max(0.0, 1 - failing / total), 2)
