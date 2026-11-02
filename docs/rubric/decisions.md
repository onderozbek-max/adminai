# MMC Survey Rubric: Decision Log

Decisions that shape `mmc-survey-rubric-v2.md`. The rubric holds the rules; this log
holds the why. Newest first. Revisit a decision by adding a new entry, not by editing
an old one.

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

### Consequence: scoring over active criteria

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
