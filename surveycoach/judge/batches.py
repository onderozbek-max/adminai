"""The AI-judged part of the rubric, split into three calls that run in parallel.

Image criteria 7.1 and 7.4 are not here: they need real image files from the crawler (Plan 5), so they stay
'unchecked' rather than being guessed.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Batch:
    id: str
    title: str
    criteria: tuple[str, ...]
    blockers: tuple[str, ...]
    focus: str


WORDING = Batch(
    "wording", "Wording and answer choices",
    criteria=("3.1", "3.4", "3.5", "4.1", "4.3", "5.1", "5.2", "5.3"), blockers=("B1", "B2", "B6"),
    focus=("Read every question, answer choice and instruction as a member on a phone would. Look for words that lead or "
           "load the answer, questions that ask two things, jargon, members who would have no valid answer, and typos or "
           "grammar errors (for grammar and spelling, put the corrected sentence in suggested_text). "
           "Also decide the blockers: a leading question on the main research topic, a question where some members "
           "have no valid answer, and a request for personal details."))

STORY = Batch(
    "story", "Intro, voice and thank-you",
    criteria=("1.1", "1.2", "1.3", "9.1", "10.1", "10.3"), blockers=(),
    focus=("Judge the survey as a conversation: the title, the intro (what we are exploring, why this member was asked, "
           "a co-creator tone), the warmth of the voice, the thank-you, and whether members are told what happens "
           "with their answers."))

FLOW = Batch(
    "flow", "Order and relevance",
    criteria=("2.3", "2.5", "8.1", "8.3", "8.4", "8.5"), blockers=(),
    focus=("Judge the order and relevance: nothing we already know about the member, no repeated questions, an easy "
           "on-topic opener, a moment that makes the member feel like an insider, only relevant questions, and a good "
           "energy curve from start to finish."))

BATCHES = (WORDING, STORY, FLOW)
