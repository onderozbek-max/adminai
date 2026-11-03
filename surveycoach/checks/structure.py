"""Structure and length checks: intro, time promise, screeners, typing load, variety (B3 B4 B5 1.4 2.1 2.2 2.4 8.2 8.6)."""
from __future__ import annotations

import re

from surveycoach.checks.registry import (ReviewContext, blocker_ok, check, finding, not_applicable, passed,
                                         clip, result)
from surveycoach.findings import CheckResult
from surveycoach.snapshot import Page

SCREEN_OUT_EFFORT_SECONDS = 120
OPEN_TEXT = {"text_short", "text_long"}
REWARD_WORDS = re.compile(r"\b(points?|rewards?|earn(?:ed|ing)?|gift ?cards?|\$\d+)\b", re.I)
THANKS = re.compile(r"\bthank", re.I)
FORMAT_FAMILY = {
    "single_choice": "single choice", "dropdown": "single choice", "multi_choice": "multiple choice",
    "rating": "rating", "text_short": "open text", "text_long": "open text", "image_choice": "image choice",
    "ranking": "ranking", "best_worst": "ranking", "grid_single": "grid", "grid_multi": "grid", "slider": "slider",
}


def _question_pages(ctx: ReviewContext) -> list[Page]:
    return [p for p in ctx.snapshot.pages if p.questions]


def _real_questions(ctx: ReviewContext):
    return [q for q in ctx.snapshot.all_questions() if q.kind != "info"]


@check("B4")
def no_intro(ctx: ReviewContext) -> CheckResult:
    pages = ctx.snapshot.pages
    if pages and pages[0].kind == "intro":
        return blocker_ok("B4")
    return result("B4", None, finding(
        "B4", "must_fix", "The survey opens straight into questions.",
        "Add a short welcome page before the first question: why we're asking, how long it takes, and the reward.",
        "Members don't know why they're here or what they get, so more of them leave."))


@check("B5")
def broken_time_promise(ctx: ReviewContext) -> CheckResult:
    promised, estimated = ctx.promised_minutes, ctx.timing.minutes
    if promised is None or not (estimated > promised * 1.5 and estimated - promised > 3):
        return blocker_ok("B5")
    return result("B5", None, finding(
        "B5", "must_fix", f"The intro promises {promised:g} minutes; we estimate about {estimated:g}.",
        f"Either shorten the survey to about {promised:g} minutes or update the intro to say about {estimated:.0f} minutes.",
        "Members promised a short survey who get a long one stop trusting every future promise."))


def _screen_out_pages(ctx: ReviewContext) -> list[tuple[int, Page]]:
    return [(i, p) for i, p in enumerate(ctx.snapshot.pages) if p.kind == "screen_out"]


@check("B3")
def late_screen_out(ctx: ReviewContext) -> CheckResult:
    findings = []
    for index, page in _screen_out_pages(ctx):
        effort = ctx.timing.pages[index - 1].cumulative_seconds if index > 0 else 0
        if effort > SCREEN_OUT_EFFORT_SECONDS:
            findings.append(finding(
                "B3", "must_fix", f"Members can be screened out after about {effort / 60:.0f} minutes of effort.",
                "Move the qualifying questions to the start so unqualified members find out in under 2 minutes.",
                "Spending minutes and then being told you don't qualify is the fastest way to lose a member.",
                page_id=page.id))
        if not THANKS.search(page.text or page.intro_text):
            findings.append(finding(
                "B3", "must_fix", clip(page.text) or "The screen-out page has no thank-you.",
                "Thank members warmly on the screen-out page, for example: Thanks for your time! "
                "This one isn't a match, but we'd love your help on the next one.",
                "Members who don't qualify still decide whether to come back.", page_id=page.id))
    return result("B3", None, *findings) if findings else blocker_ok("B3")


@check("1.4")
def time_and_reward(ctx: ReviewContext) -> CheckResult:
    intro = ctx.snapshot.intro_text
    has_time, has_reward = ctx.promised_minutes is not None, bool(REWARD_WORDS.search(intro))
    findings = []
    if not has_time:
        findings.append(finding("1.4", "worth_improving", "The intro doesn't say how long the survey takes.",
                                f"Add the time, for example: This takes about {max(1, round(ctx.timing.minutes))} minutes.",
                                "Members decide whether to start based on the time it asks of them."))
    if not has_reward:
        findings.append(finding("1.4", "worth_improving", "The intro doesn't mention the reward.",
                                "Say what members get, for example: You'll earn points for finishing.",
                                "A clear reward makes starting feel worth it."))
    return result("1.4", (has_time + has_reward) / 2, *findings)


@check("2.1")
def length_fits_type(ctx: ReviewContext) -> CheckResult:
    full, partial = ctx.rubric.length_targets_minutes[ctx.snapshot.survey_type]
    minutes, count = ctx.timing.minutes, len(_real_questions(ctx))
    if minutes <= full:
        return passed("2.1")
    fraction = 0.6 if minutes <= partial else 0.0
    return result("2.1", fraction, finding(
        "2.1", "worth_improving", f"About {minutes:g} minutes across {count} questions; the target is up to {full:g}.",
        f"Cut to about {full:g} minutes by removing or merging questions that don't drive a decision.",
        "Every extra minute on a phone costs completions and goodwill."))


@check("2.2")
def screeners_first(ctx: ReviewContext) -> CheckResult:
    if not _screen_out_pages(ctx):
        return not_applicable("2.2")   # no screen-out was observed, so there is nothing to place
    late = []
    for index, page in _screen_out_pages(ctx):
        answered = sum(len(p.questions) for p in ctx.snapshot.pages[:index])
        if answered > 3:
            late.append(finding(
                "2.2", "worth_improving", f"A screen-out comes after {answered} questions.",
                "Put every qualifying question in the first 3 screens.",
                "Late screening wastes the time of members who never qualified.", page_id=page.id))
    return result("2.2", 0.0 if late else 1.0, *late)


@check("2.4")
def typing_load(ctx: ReviewContext) -> CheckResult:
    required = [q for q in ctx.snapshot.all_questions() if q.kind in OPEN_TEXT and q.required]
    fraction = 1.0 if len(required) <= 2 else 0.5 if len(required) == 3 else 0.0
    findings = [finding("2.4", "worth_improving", clip(q.text),
                        "Make this answer optional, or replace it with answer choices.",
                        "Typing on a phone is work, and required typing makes members quit.", question_id=q.id)
                for q in required[2:]]
    return result("2.4", fraction, *findings)


@check("8.2")
def format_variety(ctx: ReviewContext) -> CheckResult:
    questions = _real_questions(ctx)
    if not questions:
        return result("8.2", None)
    formats = {FORMAT_FAMILY[q.kind] for q in questions if q.kind in FORMAT_FAMILY}
    needed = 2 if len(questions) <= 8 else 3
    if len(formats) >= needed:
        return passed("8.2")
    fraction = 0.5 if len(questions) > 8 and len(formats) == 2 else 0.0
    return result("8.2", fraction, finding(
        "8.2", "worth_improving", f"{len(questions)} questions use {len(formats)} format(s): {', '.join(sorted(formats))}.",
        f"Mix in at least {needed} formats, such as a rating, an image choice, or a short optional comment.",
        "The same question shape again and again feels like a chore."))


@check("8.6")
def room_to_speak(ctx: ReviewContext) -> CheckResult:
    tail = [q for p in _question_pages(ctx)[-2:] for q in p.questions]
    if any(q.kind in OPEN_TEXT and not q.required for q in tail):
        return passed("8.6")
    return result("8.6", 0.0, finding(
        "8.6", "worth_improving", "No optional comment box near the end.",
        "Add one optional question: Anything else you'd like the product team to know?",
        "Members who have something to say feel heard when they get the chance."))
