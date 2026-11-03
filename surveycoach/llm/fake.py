"""A deterministic stand-in for tests and offline use. It never pretends to be a model in the product."""
from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

from pydantic import BaseModel

from surveycoach.llm.base import LlmError

Canned = BaseModel | Callable[[str, str], BaseModel]


class FakeProvider:
    """`responses` maps a schema class name to a canned model, or to a function of (system, data)."""

    def __init__(self, responses: Mapping[str, Canned]):
        self.responses = dict(responses)
        self.calls: list[tuple[str, str, str]] = []

    def complete_json(self, system: str, data: str, schema: type, images: Sequence[Path] = ()):
        self.calls.append((system, data, schema.__name__))
        answer = self.responses.get(schema.__name__)
        if answer is None:
            raise LlmError(f"FakeProvider has no answer for {schema.__name__}")
        return answer(system, data) if callable(answer) else answer
