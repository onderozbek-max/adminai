"""Words and tone: plain language, instructions, emoji, and the MMC content standards (3.2 3.3 9.1 9.2)."""
from __future__ import annotations

import re

from surveycoach.checks.registry import ReviewContext, check, clip, finding, result, share_fraction
from surveycoach.checks.text import WORD, emoji_count, reading_grade, title_case_signature
from surveycoach.findings import CheckResult, Finding
from surveycoach.snapshot import Question

MAX_GRADE = 8.0
MIN_WORDS_FOR_GRADE = 8   # shorter fragments give unreliable grade levels
JARGON = re.compile(r"\b(sensory profile|organoleptic|viscosity|incremental lift|net promoter|roi|construct|"
                    r"aforementioned|utili[sz]e|demographics?|psychographic)\b", re.I)
ALL_THAT_APPLY = re.compile(r"all that apply|select all|check all|choose all|pick all", re.I)
BANNED_TERMS = re.compile(r"\b(respondents?|participants?|customers?(?! service))\b", re.I)
UNNAMED_NARRATOR = re.compile(r"\b(personally|i always|i love|i think|i believe|my favou?rite)\b", re.I)
HEAVY_PUNCTUATION = re.compile(r"!{2,}|\?{2,}|[!?]{2,}|(?:\.{3,}|\u2026).+(?:\.{3,}|\u2026)")
ALL_CAPS_WORD = re.compile(r"\b[A-Z]{4,}\b")
KNOWN_ACRONYMS = {"IHUT", "USDA", "NASA"}
CAPS_RUN = re.compile(r"\b[A-Z]{2,}(?:\s+[A-Z]{2,})+\b")


def _questions(ctx: ReviewContext) -> list[Question]:
    return [q for q in ctx.snapshot.all_questions() if q.kind != "info"]


@check("3.2")
def plain_words(ctx: ReviewContext) -> CheckResult:
    findings, failing = [], 0
    questions = _questions(ctx)
    for q in questions:
        words = len(WORD.findall(q.text))
        grade = reading_grade(q.text) if words >= MIN_WORDS_FOR_GRADE else 0.0
        jargon = JARGON.search(q.text)
        if jargon:
            findings.append(finding("3.2", "worth_improving", f'"{jargon.group(0)}" in: {clip(q.text, 90)}',
                                    "Use everyday words a member would use at the kitchen table.",
                                    "Jargon makes members guess or skip.", question_id=q.id))
        elif grade > MAX_GRADE:
            findings.append(finding("3.2", "worth_improving", f"Reads at about grade {grade:.0f}: {clip(q.text, 90)}",
                                    f"Use shorter sentences and simpler words (aim for grade {MAX_GRADE:.0f} or lower).",
                                    "Dense wording slows members down and invites misreading.", question_id=q.id))
        failing += bool(jargon) or grade > MAX_GRADE
    return result("3.2", share_fraction(failing, len(questions)), *findings)


@check("3.3")
def clear_instructions(ctx: ReviewContext) -> CheckResult:
    multi = [q for q in _questions(ctx) if q.kind == "multi_choice"]
    missing = [q for q in multi if not ALL_THAT_APPLY.search(f"{q.text} {q.help_text}")]
    findings = [finding("3.3", "worth_improving", clip(q.text), 'Add "Select all that apply" to the question.',
                        "Members can't tell whether they may pick more than one answer.", question_id=q.id)
                for q in missing]
    return result("3.3", share_fraction(len(missing), len(multi)), *findings)


@check("9.1")
def emoji_rule(ctx: ReviewContext) -> CheckResult:
    """Only the emoji rule of 9.1. Tone is the AI judge's call, so the criterion stays unchecked (fraction None)."""
    findings: list[Finding] = []
    if emoji_count(ctx.snapshot.intro_text) > 1:
        findings.append(finding("9.1", "worth_improving", clip(ctx.snapshot.intro_text),
                                "Use at most one emoji, in the intro only.", "Heavy emoji use reads as less trustworthy."))
    for q in _questions(ctx):
        in_question = emoji_count(q.text) + emoji_count(q.help_text)
        in_options = [o.label for o in q.options if emoji_count(o.label)]
        if in_question:
            findings.append(finding("9.1", "worth_improving", clip(q.text), "Remove emoji from questions.",
                                    "Emoji belong in the intro only.", question_id=q.id))
        for label in in_options:
            findings.append(finding("9.1", "worth_improving", clip(label), "Remove emoji from answer choices.",
                                    "Emoji in answers can read differently across phones.", question_id=q.id))
    return result("9.1", None, *findings)


def _standards_findings(ctx: ReviewContext) -> list[Finding]:
    found: list[Finding] = []

    def add(evidence: str, explanation: str, q: Question | None = None) -> None:
        found.append(finding("9.2", "worth_improving", clip(evidence), explanation,
                             "Consistent, friendly wording builds trust in every survey.",
                             question_id=q.id if q else None))

    if title_case_signature(ctx.snapshot.title):
        add(ctx.snapshot.title, "Write the title in sentence case: only the first word and names are capitalized.")
    for text in [p.intro_text or p.text for p in ctx.snapshot.pages if p.kind in {"intro", "thank_you"}]:
        if banned := BANNED_TERMS.search(text):
            add(text, f'Say "members" instead of "{banned.group(0)}".')
    for q in _questions(ctx):
        if title_case_signature(q.text):
            add(q.text, "Write the question in sentence case: only the first word and names are capitalized.", q)
        shouting = [w for w in ALL_CAPS_WORD.findall(q.text) if w not in KNOWN_ACRONYMS]
        if shouting or CAPS_RUN.search(q.text):
            add(q.text, "Write it in normal capitalization; avoid ALL CAPS for emphasis.", q)
        if HEAVY_PUNCTUATION.search(q.text):
            add(q.text, "Use one calm punctuation mark; avoid repeated !, ?, or ellipses.", q)
        if UNNAMED_NARRATOR.search(q.text):
            add(q.text, "Speak to the member (you), not as an unnamed 'I'.", q)
        if banned := BANNED_TERMS.search(q.text):
            add(q.text, f'Say "members" instead of "{banned.group(0)}".', q)
        labels = [o.label for o in q.options if o.label]
        lettered = [l for l in labels if l[0].isalpha()]   # '1 to 5 years' has no case to compare
        if len(lettered) >= 3 and len({l[0].isupper() for l in lettered}) > 1:
            add(" / ".join(labels[:4]), "Start every answer choice the same way: sentence case throughout.", q)
        elif any(title_case_signature(l) for l in labels):
            add(" / ".join(labels[:4]), "Write answer choices in sentence case.", q)
    return found


@check("9.2")
def content_standards(ctx: ReviewContext) -> CheckResult:
    issues = _standards_findings(ctx)
    fraction = 1.0 if len(issues) <= 1 else 0.5 if len(issues) <= 4 else 0.0
    return result("9.2", fraction, *issues[:8])
