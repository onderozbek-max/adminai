# MMC Survey Quality Rubric v2

- **Date:** 2026-11-02 (revised same day: images and phone pass)
- **Author:** Onder Ozbek (v1 draft), revised by the researcher review committee
- **Status:** Approved 2026-11-02. Replaces `mmc-survey-rubric-v1-draft.md`.
  Decisions and their reasons: `decisions.md`.
- **Goal of this rubric:** surveys that Member's Mark Community members enjoy, finish,
  trust, and come back for, while still producing clean data for the business.
- **Context that shapes everything below:** MMC surveys are taken **only on phones**.

---

## 0. How to read this rubric

- **Blockers** are checked first. Any open blocker means the survey isn't ready,
  whatever the score. In SurveyCoach, blockers appear as **Must fix**.
- **Ten dimensions** add up to **100 points**. Everything that costs points appears
  in SurveyCoach as **Worth improving**.
- Every criterion has an ID (for example `7.2`) that findings cite.
- **Check type:** `[Auto]` is a rule the app checks with code (instant, always
  consistent). `[AI]` needs judgment from the model. `[Auto+AI]` uses both.
- Dimensions follow the member's journey: first impression, time, clarity, answers,
  fairness, the phone, images, engagement, voice, and the close.
- Each criterion is counted **once**. If an issue fits two criteria, it belongs to
  the one listed here (no double penalties).
- "Phone width" means a small modern phone (about 375 points wide, high-density
  screen). SurveyCoach previews iPhone SE, iPhone 16, and Android XL.

### Readiness

| Readiness | Rule |
|---|---|
| Ready to launch | No open blockers and 80+ points |
| Almost ready | No open blockers and 60 to 79 points |
| Needs work | Any open blocker, or below 60 points |

A blocker the researcher deliberately keeps (with a reason) no longer counts as
open, but it is always shown in the sign-off packet.

### Active and inactive criteria

Some criteria depend on capabilities RedJade or MMC don't have yet. They stay in the
rubric, marked **Inactive**, and are worth **0 points** until the capability exists.
**Active criteria always add up to exactly 100.** When an inactive criterion switches
on, a pre-agreed rebalance keeps the total at 100 (see `decisions.md`, D-8 and D-9).

**Currently inactive:** 10.2, 10.4 (until the Q4 2026 rewards launch), 10.5.
Their 6 points went to the six criteria most critical to members coming back,
marked **+1** below (D-8).

### Survey types

Identify the type first. It changes the length targets (2.1), first-impression
framing (1.3), and image requirements (7.1). If unclear, use **Non-IHUT Product** and say so.

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
| B5 | **Broken time promise.** The estimated time is more than 50% *and* more than 3 minutes over what the intro promises. | Members promised 5 minutes who get 12 stop trusting every future promise. | [Auto] |
| B6 | **Asks for personal details it doesn't need.** Name, email, phone, address, membership number, health conditions, or similar, without a clear reason. | Sam's Club already knows who they are. Asking feels careless and risky. | [AI] |
| B7 | **Members can't see what they're asked to judge.** A question depends on an image or video that is missing, broken, or too small or blurry on a phone to judge. | Members guess, get frustrated, and the answers are meaningless. | [Auto+AI] |

> **Moved, not deleted:** v1's "screener that eliminates the audience" is no longer a
> blocker, because the app can't see the activity's audience targeting. It's now a
> **note under 2.2** asking the researcher to confirm targeting in the admin portal.

---

## 2. The ten dimensions (100 points)

| # | Dimension | Pts |
|---|---|---|
| D1 | First impression | 11 |
| D2 | Respect for members' time | 13 |
| D3 | Clear questions | 10 |
| D4 | Fair and complete answers | 9 |
| D5 | Neutral questions | 7 |
| D6 | Built for the phone | 11 |
| D7 | Images that work on a phone | 13 |
| D8 | Engaging experience | 13 |
| D9 | Community voice and tone | 6 |
| D10 | Closing the loop | 7 |

### D1. First impression (11)

The title and intro decide whether members start, and how they feel while answering.
(The intro image is scored under 7.1.)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 1.1 | **Inviting, specific title** in sentence case. "Help pick our next coffee pod flavor" beats "Coffee survey Q3". | 2 | [Auto+AI] |
| 1.2 | **What we're exploring, and why this member was asked** ("Because you tried our new boxer briefs..."). | 3 | [AI] |
| 1.3 | **+1** **Co-creator framing.** Product types: responses shape real Member's Mark products. Services, concept, market research: why their input matters and what it will change. | 4 | [AI] |
| 1.4 | **Honest time estimate and the reward** are both stated. | 2 | [Auto] |

### D2. Respect for members' time (13)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 2.1 | **Length fits the survey type** (estimated minutes, table below). Full points in the first band, 3 in the second, 0 in the third. | 5 | [Auto] |
| 2.2 | **Qualifying questions come first.** All screening happens within the first 3 screens, and the screen-out page thanks the member warmly. *Note:* if the screener looks likely to exclude most members, ask the researcher to confirm audience targeting in the admin portal (no points). | 3 | [Auto+AI] |
| 2.3 | **Don't ask what we already know.** Avoid questions about membership type, club, region, or past purchases that Sam's Club already has, unless the survey says why. | 2 | [AI] |
| 2.4 | **Light typing load.** Typing on a phone is work: at most 2 required open-ended questions, the rest optional. | 2 | [Auto] |
| 2.5 | **No repeats, smooth flow.** Nothing is asked twice in different words. Related questions are grouped, and transition screens only appear when the topic changes. | 1 | [AI] |

**Length targets (estimated minutes).** Locked starting targets (decision D-1),
recalibrated against real
completion times once performance data comes in.

| Type | Full (5) | Partial (3) | Too long (0) |
|---|---|---|---|
| IHUT | up to 10 | 10 to 15 | over 15 |
| Non-IHUT Product | up to 5 | 5 to 8 | over 8 |
| Services / Concept | up to 6 | 6 to 10 | over 10 |
| Market Research | up to 6 | 6 to 10 | over 10 |

Question counts are shown as context. For counting, a grid counts as one question
per 3 rows, because every row is a separate judgment for the member.

### D3. Clear questions (10)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 3.1 | **One idea per question.** No "How was the fit and comfort?" | 3 | [AI] |
| 3.2 | **Plain words.** Grade 8 reading level or lower. No jargon (sensory profile, organoleptic, viscosity, incremental lift, net promoter, ROI, construct). No stiff, formal phrasing. | 2 | [Auto+AI] |
| 3.3 | **Clear instructions and context.** "Select one" or "Select all that apply" is stated. No ambiguous pronouns. Questions about services or features say whether they exist, are coming soon, or are hypothetical. | 2 | [Auto+AI] |
| 3.4 | **Grammar and spelling.** 0 errors = 2. 1 or 2 minor errors = 1. 3+ errors, or any error in a question = 0. Quote each error with a correction. | 2 | [Auto+AI] |
| 3.5 | **Consistent terms.** "Single-serve pods" doesn't drift into "pods", "K-cups", or "capsules" unless those are different products. | 1 | [AI] |

### D4. Fair and complete answers (9)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 4.1 | **Every member can find their answer.** No plausible answer is missing. | 3 | [AI] |
| 4.2 | **No overlapping choices.** Ranges don't share endpoints ("1 to 5 years" and "5 to 10 years" overlap). | 2 | [Auto] |
| 4.3 | **A way out when needed.** "Other (please specify)" with a text box, "None of these", "Not sure" where members genuinely might not know, "Prefer not to say" on personal questions. Don't add "Other" to closed preference lists without a text box. | 2 | [AI] |
| 4.4 | **Honest scales.** Both ends labeled, as many positive as negative points, and the same direction throughout (5 always means best). | 2 | [Auto] |

### D5. Neutral questions (7)

Members should never sense a "right" answer. Quote the exact question text in every
finding. (A leading question on the *main* topic is blocker B1. Unequal image choices
are scored under 7.5.)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 5.1 | **No leading or loaded words** ("How much did you love...", "Our improved formula..."). | 3 | [AI] |
| 5.2 | **No "right answer" framing.** No wording that makes one answer sound more socially acceptable. | 2 | [AI] |
| 5.3 | **No anchoring.** Don't show a number or benchmark before asking for the member's own estimate. | 1 | [AI] |
| 5.4 | **Not a wall of agree/disagree.** At most 3 agree/disagree scales in a row. Prefer direct questions ("How soft was it?"). | 1 | [Auto] |

### D6. Built for the phone (11)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 6.1 | **+1** **Fits on one screen.** One question per screen. Question text is short (about 25 words or fewer), and the question plus its first answers are visible on an iPhone SE without scrolling. | 3 | [Auto] |
| 6.2 | **Short, tappable answer choices.** Each choice fits in 2 lines (about 60 characters). More than 8 choices are grouped, alphabetized, or trimmed. Short lists (7 or fewer) use buttons, not dropdowns. | 2 | [Auto] |
| 6.3 | **Small grids, short scales.** Grids up to 5 rows and 5 columns, otherwise split into separate questions. Scales of 7 points or fewer. A 0 to 10 scale is avoided or shown vertically. | 2 | [Auto] |
| 6.4 | **Thumb-friendly.** No drag-and-drop ranking or precision sliders without a tap alternative. No desktop words: "click", "hover", "drag", "on the left / right". Say "tap". | 2 | [Auto] |
| 6.5 | **Stays put and renders cleanly.** No links that leave the survey and lose progress. No truncated text, missing content, or broken embeds. Nothing relies on color alone. | 2 | [Auto] |

### D7. Images that work on a phone (13)

Every MMC survey is seen on a phone, so images are judged at phone size, not on a
researcher's monitor. SurveyCoach pins each image finding on the phone preview and
offers a **suggested crop** where shape is the problem.

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 7.1 | **The right image is there.** Product surveys show the specific product (correct flavor, size, variant) on the intro. Services, concept, and market research use an on-topic visual, with no penalty if the topic genuinely doesn't need one. No generic branding, stock-photo filler, placeholders, or watermarks. | 2 | [Auto+AI] |
| 7.2 | **+1** **Phone-friendly shape.** Square to portrait 4:5 (width divided by height between 0.8 and 1.0) = 3. Mild landscape up to 4:3, or taller than 4:5 = 1. Wider than 4:3 (for example 16:9) = 0, because at phone width the product shrinks to a strip and looks awkward. Scored on the worst image. | 3 | [Auto] |
| 7.3 | **Sharp and high resolution.** Full-width images are at least 750 px wide (phones have high-density screens). No visible blur, pixelation, heavy compression, or upscaling. Never stretched or squashed. | 2 | [Auto+AI] |
| 7.4 | **The product is the hero.** The subject fills most of the frame and is cropped tightly with nothing cut off. Clean, uncluttered background, good lighting, true-to-life color (members judge food and fabric by how they look). | 2 | [AI] |
| 7.5 | **Fair image choices.** When members compare images (concepts, packaging, flavors), every option shares the same size, shape, background, lighting, scale, and level of polish, and no option has branding cues the others lack. Each has a short label. At most 6 options, laid out 2 per row. Unequal images bias the result: the prettiest photo wins, not the best product. | 2 | [Auto+AI] |
| 7.6 | **Readable, light, and accessible.** No text baked into images (put it in the question), or if unavoidable it's readable at phone width. Each image under about 500 KB and the whole survey under about 5 MB, since members are often on cellular. Helpful alt text. Transparent images stay visible on dark backgrounds. Any video is 30 seconds or shorter, captioned, and doesn't autoplay with sound. | 2 | [Auto+AI] |

### D8. Engaging experience (13)

This is the dimension that most directly drives "I'd do another one of these."

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 8.1 | **Easy, on-topic opener.** The first question is quick and about the product or topic, not demographics. | 2 | [Auto+AI] |
| 8.2 | **Format variety that fits the content.** Up to 8 questions: 2+ formats. 9 or more: 3+ formats (2 formats = 1 point). Formats: single choice, multiple choice, rating, open text, image choice, ranking or best/worst, grid, slider. | 2 | [Auto] |
| 8.3 | **+1** **An insider moment.** At least one question lets members react to something new or not yet public: a concept, flavor, package, prototype, or sneak peek. For market research, any genuinely fresh angle counts. | 4 | [AI] |
| 8.4 | **Only relevant questions.** Branching skips questions that don't apply, and earlier answers are referenced where natural ("You said you drink coffee daily..."). | 2 | [AI] |
| 8.5 | **A good energy curve.** Effortful questions sit in the middle. Demographics and sensitive questions come last and are optional. The survey ends on a light note. | 2 | [AI] |
| 8.6 | **Room to speak freely.** One optional "Anything else you'd like the product team to know?" | 1 | [Auto] |

### D9. Community voice and tone (6)

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 9.1 | **Warm and human.** 4 = conversational throughout, sounds like a person. 3 = mostly warm with some formal phrases. 1 = mostly corporate. 0 = clinical. Light humor in the intro is welcome. Emoji: at most one, intro only, never in questions or answer choices. | 4 | [AI] |
| 9.2 | **Follows the content standards** (section 4). 0 to 1 issues = 2, 2 to 4 issues = 1, 5 or more = 0. | 2 | [Auto+AI] |

### D10. Closing the loop (7)

Members come back when they believe they were heard.

| ID | Criterion | Pts | Check |
|---|---|---|---|
| 10.1 | **+1** **A genuine thank-you** that names what their feedback will be used for. "Survey complete" doesn't count. | 4 | [AI] |
| 10.2 | **Inactive (RedJade can't show earned points).** **Reward confirmed** ("You've earned 50 points"). | 0 | [Auto] |
| 10.3 | **+1** **Impact reminder.** Their feedback helps shape Member's Mark products. | 3 | [AI] |
| 10.4 | **Inactive until the Q4 2026 rewards launch, then worth 3 (D-9).** **What happens next.** When and where members will hear what we learned ("We'll share results in the Community in about 6 weeks"). | 0 | [AI] |
| 10.5 | **Inactive (RedJade can't add it).** **"How was this survey?"** A one-tap rating (1 to 5) at the end. | 0 | [Auto] |

---

## 3. Plain-language rule

Findings and reports are written for product managers, community managers, and
researchers in plain English. Translate research terms:

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
| Aspect ratio | the image's shape (wide, square, or tall) |

Every review also shows **what's working**: SurveyCoach lists the top 3 strengths in
the review and the sign-off packet, because a coach that only criticizes gets ignored.

---

## 4. MMC content standards

These standards only cost points through 9.2. Image standards live in D7. Every
violation is flagged with a short rewrite in the MMC voice.

| Standard | Flag | Recommend |
|---|---|---|
| Survey titles in sentence case | "How Do You Make Coffee At Home?" | "How do you make coffee at home?" |
| Question text in sentence case | "Which Coffee Products Do You Buy Most Often?" | "Which coffee products do you buy most often?" |
| Answer choices in consistent sentence case | "Very Satisfied / somewhat satisfied" | "Very satisfied / Somewhat satisfied" |
| Answer choices grammatically parallel | "Taste / It was too expensive / Packaging" | "The taste / The price / The packaging" |
| No ALL CAPS, repeated ellipses, or heavy bold/italics/punctuation for emphasis | "What do you ACTUALLY reach for?" | "What do you usually reach for?" |
| No unnamed first-person narrator | "Personally, I always...", "My favorite..." | Second person or neutral voice, unless the speaker is named (for example, a named product developer) |
| Consistent terminology | "single-serve pods" then "K-cups" | Keep "single-serve pods" throughout |
| Transitions only when the topic changes | "Great! Let's keep going!" between related questions | Remove, or use only when a new topic starts |

### Voice and tone (confirmed 2026-11-02, decision D-6)

MMC sounds **warm, clear, member-first, and honest**: a friendly product team talking
to people it respects, not a panel company talking to "respondents".

| Instead of | Say |
|---|---|
| respondents, customers, participants | members |
| Please indicate your level of agreement | How much do you agree? |
| Thank you for your participation | Thanks for helping shape Member's Mark |
| Survey complete | That's it, thank you! |
| Coffee study Q3 | Help us pick our next coffee flavor |
| This survey will take approximately 10 minutes | This takes about 10 minutes |
| Click the image you prefer | Tap the one you like best |

### Rewrite guidelines (applies to every suggestion SurveyCoach makes)

1. Preserve the research objective.
2. Make the smallest wording change that fixes the issue.
3. Simplify existing copy rather than introducing new concepts.
4. Keep the MMC voice: warm, conversational, clear, member-focused.
5. Don't rewrite purely for style when the copy is already clear and effective.
6. When several options exist, put the shortest one that preserves meaning first.
7. For images, suggest a concrete fix (crop to 4:5, use the original high-resolution
   file, match backgrounds across options). Never "improve" an image by upscaling.

---

## 5. What changed from v1, and why

| Change | Why |
|---|---|
| Reorganized into 10 dimensions in the order a member experiences them | Maps onto SurveyCoach's question rail and phone preview. Easier to explain. |
| Total is now 100, not 106 | Thresholds (80/60) were written for 100. |
| Removed double counting: v1's D1, D6, and D11 all scored the intro and outro; D3, D8, and D10 overlapped on scales and double-barreled questions | Each issue now costs points once. |
| New **Engaging experience** (12) and stronger **Closing the loop** (11) | The goal is members coming back. v1 spent most points on correctness, few on enjoyment. |
| New **Images that work on a phone** (12) and rebuilt **Built for the phone** (10) | Surveys are mobile-only. v1 had one image floor (200 px) and three mobile checks. New: image shape, sharpness at phone density, product as hero, fair image choices, image weight, dark backgrounds, video, one-screen fit, answer length, desktop words, scale width, links that leave the survey. |
| New blocker **B7**: members can't see what they're asked to judge | An image question with a broken or unreadable image produces meaningless answers. |
| Length measured in **estimated minutes**, not question counts | A 20-row grid counted as 1 question in v1. Members feel minutes. |
| New time and engagement checks: screener placement, don't ask what we know, typing load, insider moment, energy curve, what happens next, "How was this survey?" | Biggest drivers of satisfaction and repeat participation. |
| Blockers: added B3 late screen-out, B5 broken time promise, B6 unneeded personal details. "Audience-eliminating screener" moved to a note | Late screen-outs and broken promises do the most damage to trust. The app can't see audience targeting. |
| v1's report template replaced by SurveyCoach's review screen and sign-off packet | v1's template listed dimensions that didn't match the rubric and used different points. |
| Draft gaps filled: answer choice examples, transitions (v1 repeated the images line), voice and tone starter | Completes the content standards. |
| Every criterion has an ID and a check type | Findings cite the ID. `[Auto]` rules run instantly and consistently without the model. |

## 6. Decisions

All open questions were resolved on 2026-11-02. See `decisions.md`. The only pending
item: D6 and D7 thresholds may be adjusted after the crawler spike measures RedJade's
mobile image rendering (D-7).
