"""Command line: python -m surveycoach review <snapshot.json>"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from surveycoach.review import Review, run_review
from surveycoach.snapshot import SurveySnapshot

READINESS_LABEL = {"ready": "Ready to launch", "almost_ready": "Almost ready", "needs_work": "Needs work"}


def render(review: Review) -> str:
    card = review.scorecard
    checked = 100 - card.unchecked_points
    earned = card.score - card.unchecked_points
    lines = [f"SurveyCoach review: {review.survey_title}", "", f"Readiness: {READINESS_LABEL[card.readiness]}"]
    lines.append(f"  Score on the {checked} points checked so far: {earned:.1f} of {checked} ({earned / checked:.0%})."
                 if checked else "  Nothing has been checked yet.")
    if card.provisional:
        lines.append(f"  {card.unchecked_points} more points wait on the AI step, which has not run yet.")
    if card.pending_blockers:
        lines.append(f"  {len(card.pending_blockers)} launch checks ({', '.join(card.pending_blockers)}) also wait on the AI step,"
                     " so this cannot be called Ready to launch yet.")
    promise = f" (the intro promises {review.promised_minutes:g})" if review.promised_minutes else ""
    lines.append(f"Members will need about {review.est_minutes:g} minutes{promise}. This is an estimate.")
    for title, severity in (("MUST FIX", "must_fix"), ("WORTH IMPROVING", "worth_improving")):
        items = [f for f in review.findings if f.severity == severity]
        lines += ["", f"{title} ({len(items)})"]
        for f in items:
            where = f" [{f.question_id or f.page_id}]" if f.question_id or f.page_id else ""
            lines += [f"  {f.criterion_id}{where}  {f.headline}", f"      Why: {f.explanation}"]
            if f.suggested_text:
                lines += [f"      Now:  {f.current_text or '(nothing)'}", f"      Fix:  {f.suggested_text}"]
    lines += ["", "WHAT'S WORKING"] + [f"  {s}" for s in card.strengths or ["Nothing confirmed yet."]]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="surveycoach")
    commands = parser.add_subparsers(dest="command", required=True)
    review = commands.add_parser("review", help="Score a survey snapshot against the MMC rubric")
    review.add_argument("snapshot", type=Path)
    args = parser.parse_args(argv)
    snapshot = SurveySnapshot.model_validate_json(args.snapshot.read_text())
    print(render(run_review(snapshot)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
