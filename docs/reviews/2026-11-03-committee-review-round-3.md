# Committee review, round 3 (2026-11-03)

Two independent reviewers (Head of Research Tools, Principal Product Designer) saw the AI judge and its screens.
The chair (the assistant) checked each claim against the data before acting. Nothing below was taken on trust.

## Verdicts
- Research: "Yes, show it to a researcher, but not unsupervised." Better than round 2 because no rewrite invents a reward
  and structural rewrites are fenced off. Still drowned good findings in duplicates and wrote rewrites that were not
  pasteable.
- Design: strong fidelity to mockup 05 (three rewrites, small-caps labels, word-level highlights), but provenance was too
  quiet, density too high, and the preview state contradicted itself on overridden fixes.

## Verified and fixed in this pass
| Claim | Evidence | Fix |
|---|---|---|
| B1 and 5.1 on Q4 were the same finding twice | identical quote and rewrites | `judge/dedupe.py` drops a finding that repeats a blocker on the same place and quote; prompt v4 says report once |
| 1.2, 1.3, 8.3 gave three competing rewrites of one sentence | cache dump | one rewrite per text, first in rubric order wins, losers keep their advice only; prompt asks for one merged rewrite |
| "You've tried these boxer briefs" contradicted the non-buyer finding | cache dump | prompt v4: unknowable facts go in `[square brackets]` |
| Rewrites changed question type or dropped images | cache dump | prompt v4: wording only, keep every existing choice |
| B2 explanation talked about other questions | cache dump | prompt v4: only talk about the place the finding points to |
| "Same model, so scores stay comparable" is false comfort | reasoning: true only for identical text via cache | wording replaced with what actually happens (saved, human-reviewed answers) |
| Ring caption and header disagreed on what was checked | screenshot | caption "of 96 points checked"; header names the unchecked checks; kept on mobile |
| "Nothing flagged yet" after the AI ran | screenshot | "Nothing flagged" when the AI ran |
| AI chip second and small | screenshot | first, solid, 12px, 4.5:1 contrast; rewrites labeled "AI-written. Check it before you use it." |
| Radio said "previewed" while the note said otherwise | screenshot | amber "Not shown in preview" chip; title shows "Not previewed" (it is on no phone screen) |
| Time promise on the intro stayed false with fixes on | screenshot | code-made fixes apply before AI fixes |

## Found while fixing (not raised by the committee)
- Multi-line quotes were being dropped even when every line was real survey text. Now each line must be verbatim
  (our own `option:` labels are ignored; an invented line sinks the whole quote). This recovered a real finding.
- A bundle was only marked copy-only when the model's "before" text was one line. Now any multi-line rewrite is a bundle.
- The "Fixed in preview" badge could say yes while the phone did not change. The badge and the preview now come from
  one function, and a browser test checks the invariant on every screen.

## Deferred, with reasons
- Placeholder rows as a launch blocker (needs a rubric decision; the AI now files it as B2 anyway).
- NPS exception for 0 to 10 scales (rubric decision).
- Severity tiers and splitting the 27 "worth improving" (owner decision, backlog item 2).
- Merged rewrite when a code fix and an AI fix overlap (feature).
- Designer polish: conflict note position, per-row copy for bundles, one-line "How to fix", pin gutter.

## Honest limits the reviewers raised that remain true
- The quote rule is mechanical: for "absence" findings the quote is only the stem or greeting.
- Failed-batch behavior is covered by tests but has not occurred in the committed demo data.
- No fixture contains a prompt injection; that defense is tested with unit tests, not demonstrated in the demo.
