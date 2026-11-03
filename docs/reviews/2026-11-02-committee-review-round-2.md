# Committee review, round 2 (2026-11-02)

Round 2 judged the rebuilt UI against the agreed mockups (docs/superpowers/designs 02, 03, 05) and the
round 1 findings. Reviewers: principal product designer and head of research tools (separate agents,
given the mockups as the yardstick this time, which round 1 had lacked). The chair checked every claim
against the code before acting.

## Verdicts
- Designer: no longer ugly; reads as one product; colour semantics are the strongest part. Not yet polished.
- Research tools: better than round 1 and worth opening, but not yet something a researcher would paste from
  blindly, and there is still no fix list to work through.

## Fixed after round 2 (verified with tests and a screenshot review)
- Intro rewrite no longer invents a reward: it leaves "[Say what members get for finishing.]" for the researcher.
- A strength can no longer be listed next to a finding in the same area (rubric tolerance of one 9.2 issue
  had made "content standards" a strength beside an ALL CAPS finding).
- The CLI now says what the screen says (score on checked points, pending launch checks, headline, now/fix).
- The ring shows earned / lost / not-checked-yet separately; unchecked points can never look earned. Caption
  reads "of 46 checked". Earned is always green, lost always red.
- The header names the pending launch checks ("54 points and 3 launch checks wait on the AI step").
- Rail rows for unflagged screens say "Nothing flagged yet", not "No issues found".
- Mobile: phone starts near y=365 and opens scrolled to issue 1; one-line top-issue bar above the phone;
  compact header; short disclaimer; no device switcher on a phone.
- Suggestions mark only the words that change (struck-through original, highlighted replacement).
- Flattened the nested "which version" box; one selection signal per card; deeper phone bezel.
- Overflow bug on mobile (native select) and an accessibility bug (pins inside role=img) were found by tests
  and fixed. 0 axe violations across 10 scans.

## Chair's judgement on claims that were not acted on
- "1 to 4 / 5 to 10 leaves a gap for 4.5 years": this is the owner-approved rubric's own example (4.2), kept.
  Worth revisiting for continuous measures.
- "Q4 appears twice": two different problems (emoji, ALL CAPS), correctly separate.
- "Scroll trap in the phone frame": the phone body scrolling is the point of a phone preview; the frame now
  fits the viewport and the region is keyboard focusable.

## Deferred, in value order (needs the owner's call or a backend)
1. Copyable fix list (grouped, copy all, done checkboxes saved in the browser). Mockup 03, section 3.
2. A "hurts data" tier (overlapping ranges, unbalanced scales, leading wording) above "worth improving".
   Both rounds asked for it; the mockups have two tiers. Changes the severity model and the rubric. Owner decision.
3. "Keep on purpose" with a reason (mockup 05), so a 0 to 10 recommend scale is not nagged forever.
4. B7 must say whether the image is broken in RedJade or our crawler failed to fetch it (needs the crawler).
5. Projected score "with fixes" (mockup 03: "91, was 78"): needs the engine re-run on the fixed snapshot.
6. Coverage gaps: title-case survey titles, imperative-as-question, "How much do you agree?" rewrite.
7. Re-check, version diff, sign-off packet, Play as a member, reading moment: all need Plans 3 to 5.
