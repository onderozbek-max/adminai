"""Rubric as validated data. Points live only here (in the YAML); checks return fractions."""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError, model_validator

RUBRIC_PATH = Path(__file__).parent / "data" / "rubric-v2.yaml"
TOTAL_POINTS = 100


class RubricError(Exception):
    """Raised when the rubric data is inconsistent. The app refuses to start on it.

    Deliberately not a ValueError: pydantic would wrap that inside its own ValidationError.
    """


class Strict(BaseModel):
    """Unknown keys are errors, so a typo or bad YAML quoting cannot silently drop data."""

    model_config = ConfigDict(extra="forbid")


class Dimension(Strict):
    id: str
    name: str
    points: int


class Criterion(Strict):
    id: str
    dimension: str
    points: int
    check: str
    title: str

    @property
    def active(self) -> bool:
        return self.points > 0


class Blocker(Strict):
    id: str
    title: str
    check: str


class Readiness(Strict):
    ready_min: int
    almost_min: int


class Rubric(Strict):
    version: str
    readiness: Readiness
    length_targets_minutes: dict[str, tuple[float, float]]
    dimensions: list[Dimension]
    blockers: list[Blocker]
    criteria: list[Criterion]

    @model_validator(mode="after")
    def _consistent(self) -> "Rubric":
        ids = [c.id for c in self.criteria] + [b.id for b in self.blockers] + [d.id for d in self.dimensions]
        duplicates = [i for i, n in Counter(ids).items() if n > 1]
        if duplicates:
            raise RubricError(f"duplicate IDs: {duplicates}")
        known = {d.id for d in self.dimensions}
        for criterion in self.criteria:
            if criterion.dimension not in known:
                raise RubricError(f"criterion {criterion.id}: unknown dimension {criterion.dimension}")
        if self.active_points != TOTAL_POINTS:
            raise RubricError(f"active points must total {TOTAL_POINTS}, got {self.active_points}")
        for dimension in self.dimensions:
            total = sum(c.points for c in self.criteria if c.dimension == dimension.id)
            if total != dimension.points:
                raise RubricError(f"dimension {dimension.id} declares {dimension.points} but criteria total {total}")
        return self

    @property
    def active_points(self) -> int:
        return sum(c.points for c in self.criteria if c.active)

    def criterion(self, criterion_id: str) -> Criterion:
        return next(c for c in self.criteria if c.id == criterion_id)


@lru_cache(maxsize=1)
def load_rubric(path: Path = RUBRIC_PATH) -> Rubric:
    try:
        return Rubric.model_validate(yaml.safe_load(path.read_text()))
    except ValidationError as exc:  # pydantic wraps validator errors; surface ours plainly
        raise RubricError(str(exc)) from exc
