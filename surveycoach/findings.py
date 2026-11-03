"""Findings and check results. Plain English, member-first."""
from __future__ import annotations

import hashlib
import re
from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["must_fix", "worth_improving"]


class Finding(BaseModel):
    criterion_id: str
    severity: Severity
    evidence: str
    explanation: str
    member_impact: str
    page_id: str | None = None
    question_id: str | None = None
    element_id: str | None = None
    source: Literal["auto", "ai"] = "auto"

    @property
    def fingerprint(self) -> str:
        """Identifies the same issue across re-checks: rubric ID, location, normalized evidence."""
        evidence = re.sub(r"\s+", " ", self.evidence).strip().lower()
        raw = f"{self.criterion_id}|{self.page_id}|{self.question_id}|{evidence}"
        return hashlib.sha1(raw.encode()).hexdigest()[:12]


class CheckResult(BaseModel):
    """One rubric criterion or blocker. `fraction` is 0..1 of the rubric points earned.

    None means the check could not judge (it stays unchecked). Blockers use findings only.
    `applies=False` means there was nothing to judge (for example, no images): full credit, no
    provisional flag, and never listed as a strength.
    """

    criterion_id: str
    fraction: float | None = Field(default=None, ge=0.0, le=1.0)
    applies: bool = True
    findings: list[Finding] = Field(default_factory=list)
