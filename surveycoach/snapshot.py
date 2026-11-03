"""Reader-independent survey model. Every reader (crawler, API, fixture) produces this."""
from __future__ import annotations

import hashlib
import json
from typing import Literal

from pydantic import BaseModel, Field

SurveyType = Literal["ihut", "non_ihut_product", "services_concept", "market_research"]
PageKind = Literal["intro", "question", "info", "screen_out", "thank_you", "end"]
QuestionKind = Literal[
    "single_choice", "multi_choice", "dropdown", "text_short", "text_long", "numeric",
    "date", "rating", "slider", "grid_single", "grid_multi", "ranking", "best_worst",
    "image_choice", "constant_sum", "info", "unknown",
]


class Media(BaseModel):
    kind: Literal["image", "video", "embed"] = "image"
    element_id: str = ""
    role: Literal["intro", "question", "option", "decoration"] = "question"
    alt: str | None = None
    natural_w: int | None = None
    natural_h: int | None = None
    rendered_w: int | None = None
    rendered_h: int | None = None
    bytes: int | None = None
    format: str | None = None
    has_alpha: bool = False
    loaded: bool = True
    asset_path: str | None = None


class Option(BaseModel):
    id: str
    label: str
    media: Media | None = None
    is_other_with_text: bool = False
    is_exclusive: bool = False


class Scale(BaseModel):
    points: int
    low_label: str | None = None
    high_label: str | None = None
    labels: list[str] = Field(default_factory=list)


class Question(BaseModel):
    id: str
    text: str
    kind: QuestionKind
    label: str | None = None
    help_text: str = ""
    required: bool = True
    options: list[Option] = Field(default_factory=list)
    rows: list[str] = Field(default_factory=list)
    scale: Scale | None = None
    media: list[Media] = Field(default_factory=list)
    conditional: bool = False
    options_below_fold: int = 0
    fits_one_screen: bool | None = None


class Page(BaseModel):
    id: str
    position: int
    kind: PageKind
    intro_text: str = ""
    questions: list[Question] = Field(default_factory=list)
    links_out: list[str] = Field(default_factory=list)
    text: str = ""


class SurveySnapshot(BaseModel):
    title: str
    source_url: str = ""
    survey_type: SurveyType = "non_ihut_product"
    pages: list[Page]

    def all_questions(self) -> list[Question]:
        return [q for page in self.pages for q in page.questions]

    @property
    def intro_text(self) -> str:
        return next((p.intro_text or p.text for p in self.pages if p.kind == "intro"), "")

    @property
    def content_hash(self) -> str:
        """Stable across option reordering, so randomized surveys do not create new versions."""
        canonical = [
            [page.kind, page.intro_text, page.text,
             [[q.text, q.kind, sorted(o.label for o in q.options), sorted(q.rows)] for q in page.questions]]
            for page in self.pages
        ]
        payload = json.dumps([self.title, canonical], sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()
