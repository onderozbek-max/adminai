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
    lines = [f"SurveyCoach review: {review.survey_title}", ""]
    lines.append(f"Readiness: {READINESS_LABEL[card.readiness]}    Score: {card.score:.1f} / 100")
    if card.provisional:
        lines.append(f"  Provisional: {card.unchecked_points} points are judged by the AI step, which has not run yet,"
                     " so they count as full credit for now.")
    if card.pending_blockers:
        lines.append(f"  Pending: blockers {', '.join(card.pending_blockers)} need the AI step, so this cannot be called"
                     " Ready to launch yet.")
    promise = f" (the intro promises {review.promised_minutes:g})" if review.promised_minutes else ""
    lines.append(f"Members will need about {review.est_minutes:g} minutes{promise}. This is an estimate.")
    for title, severity in (("MUST FIX", "must_fix"), ("WORTH IMPROVING", "worth_improving")):
        items = [f for f in review.findings if f.severity == severity]
        lines += ["", f"{title} ({len(items)})"]
        for f in items:
            where = f" [{f.question_id}]" if f.question_id else ""
            lines += [f"  {f.criterion_id}{where}  {f.evidence}", f"      Fix: {f.explanation}"]
    lines += ["", "WHAT'S WORKING"] + [f"  {s}" for s in card.strengths or ["Nothing stands out yet."]]
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
