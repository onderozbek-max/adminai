# Committee review of the demo UI (2026-11-02)

Three independent reviewers (separate agents, no shared context) reviewed `screen1.png` to
`screen3.png` of the static demo. Personas: product lead (AI writing and workflow products),
principal product designer (mobile-first, design systems), head of research tools (survey
platforms; speaks for the daily researcher). The chair (the agent that built the demo) checked
their claims against the code before synthesizing.

## Chair's corrections to the reviews

- "Click the one you like best" WAS flagged (rubric 6.4); it was below the screenshot's fold.
- The "400 x 400 placeholder above Image failed to load" is two different images on screen 8, not a
  contradiction. The confusion is still valid: each image needs its own label and issue.
- "Two severity levels is right" is one member's view; the other two want a data-quality tier.

## Unanimous

1. **The score display is dishonest in effect.** 84.2 next to "Needs work", and full green bars on
   areas nobody checked (Neutral questions 7/7, Community voice 6/6, Closing the loop 7/7). Real
   checked result: 30.2 of 46 points (66%). Fix: lead with the verdict, show "checked points",
   draw unchecked areas grey "Not checked yet", color bars by ratio, no false-precision decimals.
2. **Finding titles read as passes.** "Light typing load", "Plain words", "Honest scales" are rubric
   criterion names. Several bodies only quote the question. Fix: problem-first headline
   ("Scale has no labeled ends"); rubric name and ID become small metadata.
3. **Fixes are not paste-ready.** "Fix or replace the image..." restates the problem, and the primary
   button "Copy suggestion" copies it. Fix: current text and suggested replacement; hide Copy when
   there is nothing to paste; for images show file name or URL and the error.
4. **The phone preview is underused.** Opens on the Welcome screen (nothing flagged); "Coach flagged
   this question (3)" never says which three. Fix: open on the first flagged screen; numbered pins
   on the exact elements; list each flag.

## Majority (2 of 3)

5. **Severity needs a data-quality tier**: overlapping ranges (4.2) and unbalanced scales (4.4)
   corrupt data; a 4-option dropdown (6.2) is friction. Sort by damage. (Designer dissents.)
6. **The core loop is missing**: no per-finding status (fixed / won't fix), no re-check, no
   version diff ("4 resolved, 1 new, 15 remaining").
7. **Noise and jargon**: rubric codes on every card, "B1, B2, B6", "WORTH IMPROVING" repeated 19
   times, the detail panel repeats the card, "Show on phone" duplicates selection, a 16-bullet
   "Waiting on the AI step" wall, "2 answer(s)".

## Tension to resolve

- Product lead: the left column becomes a fix checklist (Linear-style triage).
- Designer: the screen is the organizing unit; phone in the center with a filmstrip of screens.
- Research tools: sort by damage to data quality.
- Chair's proposal: one list, tiered by damage (must fix / hurts data / member friction), grouped
  by screen within each tier; the phone follows the selection with pins. Triage first, then fix
  page by page, which matches how researchers edit RedJade.

## Engine gaps the review exposed (not just UI)

- Findings need a problem-first `headline` and, where deterministic, `current_text` and
  `suggested_text` (overlap ranges, "Select all that apply", "Click" to "Tap", dropdown to buttons,
  scale end labels).
- A time overrun below the blocker threshold (4.3 vs 3 minutes) should still be its own finding.
- Spelling (3.4) can be checked without AI.
- B7 must distinguish "broken in RedJade" from "our crawler could not fetch it" (re-fetch to verify).
- Strengths must not contradict findings ("Stays put and renders cleanly" next to a render failure).

## Full reviews

The verbatim reviews are in the session log; key points are captured above.
