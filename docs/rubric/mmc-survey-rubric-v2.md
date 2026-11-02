# MMC Survey Quality Rubric v2

- **Date:** 2026-11-02
- **Author:** Onder Ozbek (v1 draft), revised by the researcher review committee
- **Status:** Proposed. Replaces `mmc-survey-rubric-v1-draft.md` once approved.
- **Goal of this rubric:** surveys that Member's Mark Community members enjoy, finish,
  trust, and come back for, while still producing clean data for the business.

---

## 0. How to read this rubric

- **Blockers** are checked first. Any open blocker means the survey isn't ready,
  whatever the score. In SurveyCoach, blockers appear as **Must fix**.
- **Nine dimensions** add up to **100 points**. Everything that costs points appears
  in SurveyCoach as **Worth improving**.
- Every criterion has an ID (for example `2.2`) that findings cite.
- **Check type:** `[Auto]` is a rule the app checks with code (instant, always
  consistent). `[AI]` needs judgment from the model. `[Auto+AI]` uses both.
- Dimensions follow the member's journey through a survey: first impression,
  time, clarity, answers, fairness, phone comfort, engagement, voice, and the close.
- Each criterion is counted **once**. If an issue fits two criteria, it belongs to
  the one listed here (no double penalties).

### Readiness

| Readiness | Rule |
|---|---|
| Ready to launch | No open blockers and 80+ points |
| Almost ready | No open blockers and 60 to 79 points |
| Needs work | Any open blocker, or below 60 points |

A blocker the researcher deliberately keeps (with a reason) no longer counts as
open, but it is always shown in the sign-off packet.

### Survey types

Identify the type first. It changes the length targets (2.1) and the first-impression
requirements (1.3, 1.5). If it's unclear, use **Non-IHUT Product** and say so.

| Type | What it is |
|---|---|
| IHUT | Member tested a free product at home. Longer surveys are acceptable. |
| Non-IHUT Product | Member evaluates a product or category they didn't receive. |
| Services / Concept | A service, idea, or concept. No physical product. |
| Market Research | Brand tracking, ad testing, pricing, general insights. |

---

## 1. Blockers (Must fix)

| ID | Blocker | Why it matters to members | Check |
|---|---|---|---|
| B1 | **Leading question on the main research topic.** Wording or answer choices steer members toward an answer on the thing the survey exists to measure. | Members feel manipulated, and the business gets data it can't trust. | [AI] |
| B2 | **No valid answer.** A required question has no honest option for a meaningful share of members. | Members are forced to lie or quit. | [Auto+AI] |
| B3 | **Late screen-out.** Members can be screened out after more than about 2 minutes of effort, or the screen-out page doesn't thank them. | Spending 5 minutes and then being told "you don't qualify" is the fastest way to lose a member for good. | [Auto] |
| B4 | **No intro page.** The survey starts straight into questions with no context. | Members don't know why they're here or what they get. | [Auto] |
| B5 | **Broken time promise.** The estimated time is more than 50% *and* more than 3 minutes over what the intro promises. | Members who were promised 5 minutes and get 12 stop trusting every future promise. | [Auto] |
| B6 | **Asks for personal details it doesn't need.** Name, email, phone, address, membership number, health conditions, or similar, without a clear reason. | Sam's Club already knows who they are. Asking feels careless and risky. | [AI] |

> **Moved, not deleted:** v1's "screener that eliminates the audience" is no longer a
> blocker, because the app can't see the activity's audience targeting. It's now a
> **note under 2.2** that asks the researcher to confirm the audience is targeted in
> the admin portal.

---

## 2. The nine dimensions (100 points)

### D1. First impression (12)

The intro and title decide whether members start, and how they feel while they answer.

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 1.1 | **Inviting, specific title**, in sentence case. "Help pick our next coffee pod flavor" beats "Coffee survey Q3". | 2 | [Auto+AI] |
| 1.2 | **What we're exploring, and why this member was asked** ("Because you tried our new boxer briefs..."). | 3 | [AI] |
| 1.3 | **Co-creator framing.** Product types: responses shape real Member's Mark products. Services, concept, and market research: why their input matters and what it will change. | 3 | [AI] |
| 1.4 | **Honest time estimate and the reward** are both stated. | 2 | [Auto] |
| 1.5 | **A visual that sets the scene.** Product types: an image of the specific product, not generic branding. Other types: an on-topic visual, or no penalty if the topic genuinely doesn't need one. Flag images narrower than 400 px. | 2 | [Auto+AI] |

### D2. Respect for members' time (15)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 2.1 | **Length fits the survey type** (estimated minutes, table below). Full points in the first band, 3 in the second, 0 in the third. | 5 | [Auto] |
| 2.2 | **Qualifying questions come first.** All screening happens within the first 3 screens, and the screen-out page thanks the member warmly. *Note:* if the screener looks likely to exclude most members, ask the researcher to confirm audience targeting in the admin portal (no points). | 3 | [Auto+AI] |
| 2.3 | **Don't ask what we already know.** Avoid questions about membership type, club, region, or past purchases that Sam's Club already has, unless the survey says why it's needed. | 2 | [AI] |
| 2.4 | **Light writing load.** At most 2 required open-ended questions. The rest are optional. | 2 | [Auto] |
| 2.5 | **No repeats.** The same thing isn't asked twice in different words. | 2 | [AI] |
| 2.6 | **Smooth flow.** Related questions are grouped. Transition screens only appear when the topic changes. | 1 | [AI] |

**Length targets (estimated minutes).** These are starting points, and they'll be
recalibrated against real completion times once performance data comes in.

| Type | Full (5) | Partial (3) | Too long (0) |
|---|---|---|---|
| IHUT | up to 10 | 10 to 15 | over 15 |
| Non-IHUT Product | up to 5 | 5 to 8 | over 8 |
| Services / Concept | up to 6 | 6 to 10 | over 10 |
| Market Research | up to 6 | 6 to 10 | over 10 |

Question counts are still shown as context. For counting, a grid counts as one
question per 3 rows, because every row is a separate judgment for the member.

### D3. Clear questions (12)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 3.1 | **One idea per question.** No "How was the fit and comfort?" | 3 | [AI] |
| 3.2 | **Plain words.** Grade 8 reading level or lower. No jargon (sensory profile, organoleptic, viscosity, incremental lift, net promoter, ROI, construct). No stiff, formal phrasing. | 3 | [Auto+AI] |
| 3.3 | **Clear instructions and context.** "Select one" or "Select all that apply" is stated. No ambiguous pronouns. Questions about services or features say whether they exist, are coming soon, or are hypothetical. | 2 | [Auto+AI] |
| 3.4 | **Grammar and spelling.** 0 errors = 2. 1 or 2 minor errors = 1. 3+ errors, or any error in a question = 0. Quote each error with a correction. | 2 | [Auto+AI] |
| 3.5 | **Consistent terms.** "Single-serve pods" doesn't drift into "pods", "K-cups", or "capsules" unless those are different products. | 2 | [AI] |

### D4. Fair and complete answers (10)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 4.1 | **Every member can find their answer.** No plausible answer is missing. | 3 | [AI] |
| 4.2 | **No overlapping choices.** Ranges don't share endpoints ("1 to 5 years" and "5 to 10 years" overlap). | 2 | [Auto] |
| 4.3 | **A way out when needed.** "Other (please specify)" with a text box, "None of these", "Not sure" where members genuinely might not know, and "Prefer not to say" on personal questions. Don't add "Other" to closed preference lists without a text box. | 3 | [AI] |
| 4.4 | **Honest scales.** Both ends are labeled, there are as many positive as negative points, and the direction stays the same throughout (5 always means best). | 2 | [Auto] |

### D5. Neutral questions (8)

Members should never sense a "right" answer. Quote the exact question text in every finding.
(A leading question on the *main* topic is a blocker, B1. This dimension covers everything else.)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 5.1 | **No leading or loaded words** ("How much did you love...", "Our improved formula..."). | 3 | [AI] |
| 5.2 | **No "right answer" framing.** Avoid wording that makes one answer sound more socially acceptable. | 2 | [AI] |
| 5.3 | **No anchoring.** Don't show a number or benchmark before asking members for their own estimate. | 1 | [AI] |
| 5.4 | **Not a wall of agree/disagree.** At most 3 agree/disagree scales in a row. Prefer direct questions ("How soft was it?") over "Do you agree it was soft?" | 2 | [Auto] |

### D6. Comfortable on a phone (8)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 6.1 | **Small grids only.** Up to 5 rows and 5 columns. Anything bigger should be split into separate questions. | 2 | [Auto] |
| 6.2 | **No fiddly controls.** No drag-and-drop ranking or precision sliders unless there's a tap alternative. | 1 | [Auto] |
| 6.3 | **Images work on a phone.** Text inside images is readable at phone width, and images load quickly (under about 500 KB). | 2 | [Auto+AI] |
| 6.4 | **Short option lists.** More than 8 options should be grouped, alphabetized, or trimmed. | 1 | [Auto] |
| 6.5 | **Accessible.** Meaningful images have helpful alt text, and nothing relies on color alone. | 1 | [Auto+AI] |
| 6.6 | **Renders cleanly.** No truncated text, missing content, or broken embeds. | 1 | [Auto] |

### D7. Engaging experience (15)

This is the dimension that most directly drives "I'd do another one of these."

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 7.1 | **Easy, on-topic opener.** The first question is quick and about the product or topic, not demographics. | 2 | [Auto+AI] |
| 7.2 | **Format variety that fits the content.** Up to 8 questions: 2+ formats. 9 or more: 3+ formats (2 formats = 1 point). Formats: single choice, multiple choice, rating, open text, image choice, ranking or best/worst, grid, slider. | 3 | [Auto] |
| 7.3 | **An insider moment.** At least one question lets members react to something new or not yet public: a concept, flavor, package, prototype, or sneak peek. For market research, any genuinely fresh angle counts. | 3 | [AI] |
| 7.4 | **Only relevant questions.** Branching skips questions that don't apply, and earlier answers are referenced where it's natural ("You said you drink coffee daily..."). | 2 | [AI] |
| 7.5 | **Visuals that help members imagine.** Image choices, concept boards, or packaging shots where they aid judgment, not decoration. | 2 | [AI] |
| 7.6 | **A good energy curve.** Effortful questions sit in the middle. Demographics and sensitive questions come last and are optional. The survey ends on a light note. | 2 | [AI] |
| 7.7 | **Room to speak freely.** One optional "Anything else you'd like the product team to know?" | 1 | [Auto] |

### D8. Community voice and tone (8)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 8.1 | **Warm and human.** 5 = conversational throughout, sounds like a person. 3 = mostly warm with some formal phrases. 1 = mostly corporate. 0 = clinical. Light humor in the intro is welcome. Emoji: at most one, intro only. Never in questions or answer choices. | 5 | [AI] |
| 8.2 | **Follows the content standards** (section 4): sentence case, no ALL CAPS for emphasis, no unnamed first-person narrator, parallel answer choices. Full points for 0 to 1 issues, 1 point for 2 to 4 issues, 0 for 5 or more. | 3 | [Auto+AI] |

### D9. Closing the loop (12)

Members come back when they believe they were heard.

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 9.1 | **A genuine thank-you** that names what their feedback will be used for. "Survey complete" doesn't count. | 3 | [AI] |
| 9.2 | **Reward confirmed** ("You've earned 50 points"). Full points if the platform shows it automatically. | 2 | [Auto] |
| 9.3 | **Impact reminder.** Their feedback helps shape Member's Mark products. | 2 | [AI] |
| 9.4 | **What happens next.** When and where members will hear what we learned ("We'll share results in the Community in about 6 weeks"). | 3 | [AI] |
| 9.5 | **"How was this survey?"** A one-tap rating (1 to 5) at the end. This is also how SurveyCoach learns whether its scores are right. | 2 | [Auto] |

---

## 3. Plain-language rule

Findings and reports are written for product managers, community managers, and
researchers in plain English. Translate research terms like these:

| Research term | Say instead |
|---|---|
| MaxDiff / paired ranking | "pick-the-best-and-worst question (1 of 6 rounds)" |
| Acquiescence bias | members defaulting to "agree" |
| Double-barreled | two questions packed into one |
| Mutually exclusive options | answer choices that don't overlap |
| Exhaustive options | choices that cover every possible answer |
| Monadic | each member sees only one version |
| Screener / quota | qualifying questions / spots for each group |
| Piping | using an earlier answer in a later question |

Every finding also includes **what's working**. SurveyCoach shows the top 3 strengths
in the review and in the sign-off packet, because a coach that only criticizes gets ignored.

---

## 4. MMC content standards

These standards only cost points through 8.2. Every violation is flagged with a short
rewrite in the MMC voice.

| Standard | Flag | Recommend |
|---|---|---|
| Survey titles in sentence case | "How Do You Make Coffee At Home?" | "How do you make coffee at home?" |
| Question text in sentence case | "Which Coffee Products Do You Buy Most Often?" | "Which coffee products do you buy most often?" |
| Answer choices in consistent sentence case | "Very Satisfied / somewhat satisfied" | "Very satisfied / Somewhat satisfied" |
| Answer choices grammatically parallel | "Taste / It was too expensive / Packaging" | "The taste / The price / The packaging" |
| No ALL CAPS, repeated ellipses, or heavy bold/italics/punctuation for emphasis | "What do you ACTUALLY reach for?" | "What do you usually reach for?" |
| No unnamed first-person narrator | "Personally, I always...", "My favorite..." | Second person or neutral voice, unless the speaker is named (for example, a named product developer) |
| Consistent terminology | "single-serve pods" then "K-cups" | Keep "single-serve pods" throughout |
| Images support understanding and don't hide instructions | Decorative stock photo | On-topic product or concept image |
| Transitions only when the topic changes | "Great! Let's keep going!" between related questions | Remove, or use it only when a new topic starts |

### Voice and tone (proposed starter, needs Onder's confirmation)

MMC sounds **warm, clear, member-first, and honest**: a friendly product team
talking to people it respects, not a panel company talking to "respondents".

| Instead of | Say |
|---|---|
| respondents, customers, participants | members |
| Please indicate your level of agreement | How much do you agree? |
| Thank you for your participation | Thanks for helping shape Member's Mark |
| Survey complete | That's it, thank you! |
| Coffee study Q3 | Help us pick our next coffee flavor |
| This survey will take approximately 10 minutes | This takes about 10 minutes |

### Rewrite guidelines (applies to every suggestion SurveyCoach makes)

1. Preserve the research objective.
2. Make the smallest wording change that fixes the issue.
3. Simplify existing copy rather than introducing new concepts.
4. Keep the MMC voice: warm, conversational, clear, member-focused.
5. Don't rewrite purely for style when the copy is already clear and effective.
6. When several options exist, put the shortest one that preserves meaning first.

---

## 5. What changed from v1, and why

| Change | Why |
|---|---|
| Reorganized into 9 dimensions in the order a member experiences them | Maps directly onto the question rail and phone preview in SurveyCoach. Easier to explain. |
| Total is now 100, not 106 | Thresholds (80/60) were written for 100. |
| Removed double counting: v1's D1, D6, and D11 all scored the intro and outro; D3, D8, and D10 overlapped on scales and double-barreled questions | Each issue now costs points once, so scores are fairer and easier to explain. |
| New **Engaging experience** dimension (15) and stronger **Closing the loop** (12) | The goal is members coming back. v1 spent most of its points on correctness and very few on enjoyment. |
| Length measured in **estimated minutes**, not question counts | A 20-row grid counted as 1 question in v1. Members feel minutes, not counts. |
| New checks: screener placement, don't ask what we know, open-text load, repeats, insider moment, energy curve, what happens next, "How was this survey?" | Industry experience: these are the biggest drivers of satisfaction and repeat participation. |
| Blockers: added B3 late screen-out, B5 broken time promise, B6 unneeded personal details. "Audience-eliminating screener" moved to a note. | Late screen-outs and broken promises do the most damage to trust. The app can't see audience targeting, so it can't judge screener narrowness fairly. |
| The v1 report template is replaced by SurveyCoach's review screen and sign-off packet | v1's template listed dimensions that didn't match the rubric (for example "Audience Alignment", "Actionability of Insights") and used different point values. |
| Images: v1 gave 3/10 for no images, even on product surveys that require one | Product surveys without an image now score 0 on 1.5. Other types aren't penalized if a visual isn't needed. Minimum width raised from 200 to 400 px for today's phone screens. |
| Draft gaps filled: answer choice examples, transitions (v1 repeated the images line), voice and tone starter | Completes the content standards. |
| Every criterion has an ID and a check type | SurveyCoach findings cite the ID, and `[Auto]` rules run instantly and consistently without the model. |

## 6. Open questions for Onder

1. **Length targets (2.1)** are proposed starting points. Do they match what research leadership expects?
2. **B5 and B6 as blockers:** comfortable making a broken time promise and unneeded
   personal details launch-blocking (keep-with-reason still available)?
3. **9.4 "What happens next":** is there a real mechanism to share results back with
   members (Community home module, notifications)? If not, this criterion should
   wait, because promising updates that never arrive is worse than not promising.
4. **9.5 "How was this survey?"** needs research leadership to agree to add it to every survey.
5. **Voice and tone starter:** confirm, edit, or replace with the official MMC voice guide.
