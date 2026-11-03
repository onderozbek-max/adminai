# MMC Survey Rubric: Decision Log

Decisions that shape `mmc-survey-rubric-v2.md`. The rubric holds the rules; this log
holds the why. Newest first. Revisit a decision by adding a new entry, not by editing
an old one.

---

## 2026-11-02: Weighted sum to exactly 100 (Onder Ozbek)

**Supersedes** the "scoring over active criteria" normalization below. Onder's call:
the score must be a plain sum that adds up to 100, not a formula.

### D-8: The six freed points go to the most critical criteria (+1 each)

Inactive 10.2 (1), 10.4 (3), and 10.5 (2) are now worth 0. Their 6 points went to the
criteria with the most leverage on the goal: members enjoy the survey, trust MMC,
and come back.

| Criterion | Was | Now | Why it earned the extra point |
|---|---|---|---|
| 1.3 Co-creator framing | 3 | 4 | MMC's known value-prop gap: members don't yet believe "Sam's Club hears me, products improve". This intro line is the first place we make that case. |
| 8.3 Insider moment | 3 | 4 | Access ranks second in MMC's value hierarchy, and IHUTs complete about 15x more often than surveys. Getting something new is what makes members show up. |
| 6.1 Fits on one screen | 2 | 3 | Surveys are phone-only. Scrolling to find the answers is the friction members feel on every single screen. |
| 7.2 Phone-friendly image shape | 2 | 3 | Onder's most common real-world defect: wide images that look awkward on phones. |
| 10.1 Genuine thank-you | 3 | 4 | With reward confirmation and "what happens next" impossible in RedJade today, the thank-you is the main closing lever left. |
| 10.3 Impact reminder | 2 | 3 | Same reason: the only other way to make the loop visible at the end of a survey today. |

Result: active criteria sum to exactly **100**. Dimension totals: D1 11, D2 13, D3 10,
D4 9, D5 7, D6 11, D7 13, D8 13, D9 6, D10 7.

### D-9: Pre-agreed rebalance when 10.4 switches on (Q4 2026 rewards launch)

10.4 "What happens next" becomes worth **3**. To stay at 100, three boosts revert,
chosen because 10.4 itself does the job they were covering for:

- 1.3 Co-creator framing: 4 back to 3
- 10.1 Genuine thank-you: 4 back to 3
- 10.3 Impact reminder: 3 back to 2

D10 becomes 3 + 2 + 3 = 8, D1 becomes 10, and the total stays 100. Any future
activation (10.2, 10.5) needs its own rebalance entry here.

---

## 2026-11-02: Rubric v2 open questions resolved (Onder Ozbek)

| # | Question | Decision | Effect on the rubric |
|---|---|---|---|
| D-1 | Are the length targets in 2.1 right? | **Yes, locked as starting targets.** Proposed by Onder after brainstorming with Wibey and Code Puppy. Not yet formally validated by research leadership. | 2.1 table marked locked. Recalibrate against real completion times once performance data exists. |
| D-2 | Should B5 (broken time promise), B6 (unneeded personal details), and B7 (members can't see what they're judging) block launch? | **Yes.** Keep-with-reason remains available and shows in the sign-off packet. | No change; blockers stand as written. |
| D-3 | Can surveys confirm the reward on the final page (10.2)? | **Not possible today.** RedJade, which renders the final page, can't show earned points. | 10.2 **inactive**. |
| D-4 | Can surveys tell members what happens next (10.4)? | **Not yet.** Becomes possible after the rewards program launches in Q4 2026. | 10.4 **inactive until the Q4 rewards launch**, then switch on. |
| D-5 | Can every survey end with a "How was this survey?" rating (10.5)? | **Not possible.** RedJade lacks the capability. | 10.5 **inactive**. SurveyCoach's learning loop uses completion, drop-off, and timing instead (see spec section 9). |
| D-6 | Voice and tone starter (section 4)? | **Confirmed** as the MMC voice for SurveyCoach. | Marked confirmed. |
| D-7 | RedJade mobile image rendering (width, height cap, dark mode)? | **Agreed:** measure in the crawler spike. | Thresholds in D6 and D7 may be adjusted after the spike, logged here as a new entry. |

### Consequence: scoring over active criteria (superseded by D-8)

With 10.2, 10.4, and 10.5 inactive, 94 of 100 points are active. Rather than
re-weighting every dimension now and again in Q4, the score is **normalized over
active criteria**:

`score = round(points earned on active criteria / active points x 100)`

- Readiness thresholds (80 / 60) stay meaningful.
- When 10.4 switches on after the rewards launch, no re-weighting is needed.
- Trade-off accepted: Closing the loop carries less weight today (5 of 94 active
  points) because most of it can't be done inside RedJade yet.

### Follow-up idea (not a rubric item)

"How was this survey?" can't live inside RedJade, but it could live in the
**MMC app itself**: a one-tap rating when a member returns from a completed activity.
That would restore the cleanest ground truth for both MMC and SurveyCoach. It's an MMC
roadmap candidate for Onder, not a SurveyCoach feature.

## 2026-11-02: Visual direction is the dark Studio design, not Living Design

The first static demo ignored the aligned mockups (docs/superpowers/designs 02, 03, 05) and
shipped a generic light report page. A committee review missed it because the reviewers were
not given the mockups. Decision (Onder): build the UI to the mockups' dark Studio look in
custom CSS. Living Design has no dark theme, so this overrides the "compose from LD" rule.
Any future design review must be given the mockups and spec as its yardstick.
