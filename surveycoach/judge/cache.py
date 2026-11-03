"""A tiny file cache for validated AI answers, so re-reviewing an unchanged survey costs nothing."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

from pydantic import ValidationError

from surveycoach.judge.batches import Batch
from surveycoach.judge.prompts import PROMPT_VERSION
from surveycoach.judge.schemas import BatchOutput
from surveycoach.llm.base import ASSESSMENT_MODEL
from surveycoach.rubric import Rubric
from surveycoach.snapshot import SurveySnapshot


class JudgeCache:
    """One JSON file per (survey content, rubric, model, batch, prompt version).

    The model is part of the key on purpose: changing it is a recorded decision that re-runs the AI steps.
    """

    def __init__(self, root: Path | None = None):
        home = Path(os.environ.get("SURVEYCOACH_HOME") or Path.home() / ".surveycoach")
        self.root = Path(root) if root else home / "cache"

    def key(self, snapshot: SurveySnapshot, rubric: Rubric, batch: Batch) -> str:
        raw = "|".join([snapshot.content_hash, rubric.version, ASSESSMENT_MODEL, batch.id, PROMPT_VERSION])
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    def get(self, key: str) -> BatchOutput | None:
        try:
            return BatchOutput.model_validate_json((self.root / f"{key}.json").read_text())
        except (FileNotFoundError, ValidationError, ValueError):
            return None                      # a missing or corrupt entry is just a miss

    def put(self, key: str, output: BatchOutput) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / f"{key}.json").write_text(output.model_dump_json(indent=1))
