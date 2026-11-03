"""The LLM seam. The product depends on this Protocol, never on a particular model runner."""
from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Protocol, TypeVar

from pydantic import BaseModel

# Decided by Onder (2026-11-02): one judge for every researcher, so scores stay comparable between reviews.
# It is stored on every AI result and is part of the cache key: changing it re-runs the AI steps on purpose.
ASSESSMENT_MODEL = "gpt-6.1-sol"

T = TypeVar("T", bound=BaseModel)


class LlmError(Exception):
    """The model could not give a usable answer. The caller shows 'couldn't check', never a guess."""


class LlmUnavailable(LlmError):
    """The model runner is not installed or not signed in. Deterministic checks still work."""


class LlmProvider(Protocol):
    def complete_json(self, system: str, data: str, schema: type[T], images: Sequence[Path] = ()) -> T:
        """`system` holds the instructions, `data` the untrusted survey content. The answer matches `schema`."""
