# Spikes R1c and R2: generic crawl of a live RedJade survey, and Wibey vision (2026-11-02)

**Approved by Onder** for testing on `https://app.redjade.net/surveys/samc/posthalloween26/`
("Insights Post-Halloween Survey", project P300057, event 501637, live anonymous link).
Prototype: `spikes/r1c/crawl.py` and `definition.py` (git-ignored with raw artifacts).
Up to five test participants were created, all tagged `SURVEYCOACH-TEST-001` to `-003`.
This survey skips the start screen (`skipParticipantStart`), so **merely loading the link
signs in a participant**, including in runs that crashed early. Runs 1 and 2 submitted a
response; run 3 stopped before submitting.

## R1c: crawl findings

| # | Finding | Evidence | Design consequence |
|---|---|---|---|
| 1 | **The full questionnaire definition arrives passively.** `POST /api/v1/surveys/in_progress_check_events` returns `questionnaire.data.pages[]` with every page, question, answer, and trigger, including pages the walk never visits. | 53 KB response; 7 pages vs. 3 walked in run 1 | Extractor 1 (definition) is real. Shape differs from the previewer (`data.pages` vs. `data.page_groups[].pages`); the parser accepts both. |
| 2 | **`external_id` tagging works.** `?external_id=SURVEYCOACH-TEST-001` on the link is sent with the sign-in. | Sign-in post data | Containment rule confirmed. |
| 3 | RedJade saves each answer (`PUT answer_submit_events/<id>`) and each page start; completion is `POST questionnaire_submit_events`, then sign-out. | Network log | A read always leaves a partial response; only completion is avoidable. |
| 4 | **The last page's button is labeled "Next"**, not Submit. Label-based final-submit detection failed (runs 1 and 2 submitted). | Runs 1 and 2 | Final-submit detection must use the definition (no later page reachable given answers). Implemented in run 3: stopped correctly. |
| 5 | **Branching is explicit**: page triggers with `condition: any` or `equal`, a `parent_cid`, and answer IDs. p6 shows only for "I didn't do anything" (`equal`). | Definition | Coverage-first answer policy, plus a multi-session path planner for mutually exclusive branches. |
| 6 | Pick-the-middle answers took the **shortest path** (3 of 7 pages); option order is randomized (`randomize: unseeded`). | Run 1 | Choose answers from triggers: run 3 reached **6 of 7 pages** (the maximum for one path). |
| 7 | Answers are **buttons, each in its own wrapper**. "Same parent" grouping produced 13 groups of 1. | Run 2 | Group = nearest ancestor holding at least 2 answer controls (works for lists and matrix rows). |
| 8 | Many hidden controls in the DOM (`I'm Finished`, a hidden previous button, event pickers). | Wait timeout | Visibility filter on every query; wait for a *visible* control. |
| 9 | The page never reaches network idle. | goto timeout | Wait for a visible control plus a settle delay. |
| 10 | RedJade doesn't use a scrolling container for overflow here, so scroller measurement said "fits" while 13 options overflowed. | p01 screenshot | Fold = answer control bottoms vs. top of the advance button (platform-neutral). Reported "1 below fold". |
| 11 | Question types seen: `page_text` (intro), `checkbox`, `radio`, `media` (image page); an "Other (tell us)" option; emoji in prompts; HTML prompts. | Definition | Strategy and extractor coverage for these is mandatory in v1. |
| 12 | The intro page appeared in run 3 but not run 1. | Runs 1 and 3 | Investigate timing (possible auto-advance or a late render). |

### Mobile observations (for the review engine)

- The "celebrate" question renders 13 tall buttons; "Something else" is cut off and the
  opt-out answer sits below the fold on iPhone 16. Real D6 findings exist in real surveys.
- Images: a portrait 1025 x 1534 rendered at 349 x 522, and the thank-you image 842 x 595 at 280 x 198.

## R2: Wibey vision

| Mode | Result |
|---|---|
| `wibey -f prompt.txt -m gpt-6.1-sol`, JSON on stdout | Correct content, but **underscores stripped from keys and values** (`questiontext`, `singlechoice`) by Markdown rendering, plus terminal escape codes. 9.7 s. |
| Same, prompt says "write the JSON to <path>" | **Exact JSON**, correct question, all 9 options, selected answer detected. 12.7 s. |

Consequence: `WibeyProvider` always uses file output and validates it with Pydantic.

## Spec changes made

- Reader design: definition capture confirmed (3.3), grouping rule (4.1), fold geometry
  (3.2), definition-based final-submit stop (4.4, 10), coverage-first policy and path
  planner (5.3), assumptions updated (14).
- Main spec: `WibeyProvider` file output; R2 resolved.
