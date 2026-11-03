"""Built for the phone: one screen, tappable answers, small grids, thumb-friendly, stays put (6.1 to 6.5)."""
from __future__ import annotations

import re

from surveycoach.checks.registry import ReviewContext, check, clip, finding, result, share_fraction
from surveycoach.findings import CheckResult, Finding
from surveycoach.snapshot import Question

MAX_QUESTION_WORDS = 25
MAX_LABEL_CHARS = 60
MAX_CHOICES = 8
MAX_DROPDOWN_BUTTONS = 7   # lists this short should be buttons, not a dropdown
MAX_GRID_ROWS = 5
MAX_GRID_COLUMNS = 5
MAX_SCALE_POINTS = 7
DESKTOP_WORDS = re.compile(r"\b(click(?:ing)?|double-click|right-click|hover|drag(?:ging)?|on the (?:left|right)|"
                           r"(?:left|right)[- ]hand side)\b", re.I)
CHOICE_KINDS = {"single_choice", "multi_choice", "dropdown", "image_choice"}
GRID_KINDS = {"grid_single", "grid_multi"}
TRUNCATED = re.compile(r"(\.\.\.|\u2026)\s*$")


def _questions(ctx: ReviewContext) -> list[Question]:
    return [q for q in ctx.snapshot.all_questions() if q.kind != "info"]


def _phone_finding(criterion: str, q: Question, evidence: str, fix: str, impact: str) -> Finding:
    return finding(criterion, "worth_improving", evidence, fix, impact, question_id=q.id)


def _screen_problems(page, q_findings) -> list[Finding]:
    problems = list(q_findings)
    if len([q for q in page.questions if not q.conditional]) > 1:
        problems.append(finding("6.1", "worth_improving", f"{len(page.questions)} questions on one screen.",
                                "Show one question per screen.", "Crowded screens need a lot of scrolling on a phone.",
                                page_id=page.id))
    return problems


def _question_fit_findings(q: Question) -> list[Finding]:
    found = []
    words = len(q.text.split())
    if words > MAX_QUESTION_WORDS:
        found.append(_phone_finding("6.1", q, f"{words} words: {clip(q.text, 90)}",
                                    f"Shorten the question to about {MAX_QUESTION_WORDS} words or fewer.",
                                    "Long questions push the answers off the first screen."))
    if q.options_below_fold or q.fits_one_screen is False:
        found.append(_phone_finding("6.1", q, f"{q.options_below_fold} answer(s) are below the fold on a phone.",
                                    "Trim or group the answers so the question and its first answers show without scrolling.",
                                    "Members may never see the answers they'd have picked."))
    return found


@check("6.1")
def fits_one_screen(ctx: ReviewContext) -> CheckResult:
    """Judged per screen: a screen fails if it holds several questions or any question doesn't fit."""
    screens = [p for p in ctx.snapshot.pages if any(q.kind != "info" for q in p.questions)]
    findings, failing = [], 0
    for page in screens:
        problems = _screen_problems(page, [f for q in page.questions if q.kind != "info"
                                           for f in _question_fit_findings(q)])
        failing += bool(problems)
        findings += problems
    return result("6.1", share_fraction(failing, len(screens)), *findings)


@check("6.2")
def tappable_answers(ctx: ReviewContext) -> CheckResult:
    findings, failing, total = [], 0, 0
    for q in _questions(ctx):
        if q.kind not in CHOICE_KINDS or not q.options:
            continue
        total += 1
        problems = []
        long_labels = [o.label for o in q.options if len(o.label) > MAX_LABEL_CHARS]
        if long_labels:
            problems.append((clip(long_labels[0], 90), f"Keep each answer to about {MAX_LABEL_CHARS} characters (2 lines)."))
        if len(q.options) > MAX_CHOICES:
            problems.append((f"{len(q.options)} answer choices.", f"Group, alphabetize, or trim to {MAX_CHOICES} or fewer."))
        if q.kind == "dropdown" and len(q.options) <= MAX_DROPDOWN_BUTTONS:
            problems.append((f"A dropdown with only {len(q.options)} choices.", "Use buttons instead; they take one tap, not two."))
        failing += bool(problems)
        findings += [_phone_finding("6.2", q, ev, fix, "Long or crowded answers are hard to read and tap on a phone.")
                     for ev, fix in problems]
    return result("6.2", share_fraction(failing, total), *findings)


@check("6.3")
def small_grids(ctx: ReviewContext) -> CheckResult:
    findings, failing, total = [], 0, 0
    for q in _questions(ctx):
        columns = q.scale.points if q.scale else len(q.options)
        problems = []
        if q.kind in GRID_KINDS:
            total += 1
            if len(q.rows) > MAX_GRID_ROWS:
                problems.append((f"A grid with {len(q.rows)} rows.", f"Split it into separate questions of {MAX_GRID_ROWS} rows or fewer."))
            if columns > MAX_GRID_COLUMNS:
                problems.append((f"A grid with {columns} columns.", f"Use {MAX_GRID_COLUMNS} columns or fewer."))
        elif q.scale and q.kind in {"rating", "slider"}:
            total += 1
            if q.scale.points > MAX_SCALE_POINTS:
                problems.append((f"A {q.scale.points}-point scale.", f"Use {MAX_SCALE_POINTS} points or fewer; a 0 to 10 scale is hard to tap."))
        failing += bool(problems)
        findings += [_phone_finding("6.3", q, ev, fix, "Wide grids and long scales force sideways scrolling and mis-taps.")
                     for ev, fix in problems]
    return result("6.3", share_fraction(failing, total), *findings)


@check("6.4")
def thumb_friendly(ctx: ReviewContext) -> CheckResult:
    findings, failing = [], 0
    for q in _questions(ctx):
        texts = [q.text, q.help_text, *[o.label for o in q.options]]
        problems = []
        if match := next((m for t in texts if (m := DESKTOP_WORDS.search(t))), None):
            problems.append((f'"{match.group(0)}" is a desktop word.', 'Say "tap" and avoid "left" or "right".'))
        if q.kind in {"ranking", "slider"}:
            problems.append((f"A {q.kind} question.", "Offer a tap alternative: drag-and-drop and precision sliders are hard with a thumb."))
        failing += bool(problems)
        findings += [_phone_finding("6.4", q, ev, fix, "Members on a phone can't click, hover, or drag.") for ev, fix in problems]
    return result("6.4", share_fraction(failing, len(_questions(ctx))), *findings)


@check("6.5")
def stays_put(ctx: ReviewContext) -> CheckResult:
    findings, failing = [], 0
    for page in ctx.snapshot.pages:
        if page.links_out:
            failing += 1
            findings.append(finding("6.5", "worth_improving", f"Links away from the survey: {', '.join(page.links_out[:2])}",
                                    "Remove the link, or open it in a way that keeps the member's progress.",
                                    "Leaving the survey can lose all progress.", page_id=page.id))
    for q in _questions(ctx):
        if TRUNCATED.search(q.text):
            failing += 1
            findings.append(_phone_finding("6.5", q, q.text[-60:], "Show the full question text.",
                                           "Cut-off text leaves members guessing what is being asked."))
    total = len(ctx.snapshot.pages) + len(_questions(ctx))
    return result("6.5", share_fraction(failing, total), *findings)
