# MMC Survey Quality Rubric (v1 draft, Onder, 2026-11-02)

Saved verbatim from Onder's draft for history. Superseded by `mmc-survey-rubric-v2.md`.
(Emoji markers from the original were stripped by the project's emoji filter.)

---

MMC is Sam's Club's co-creation community (150,000+ members). Survey quality directly affects completion rates and member trust.

## Plain language rule

Write reports for Product Managers and Community Managers. Never use research jargon.

- MaxDiff / paired ranking -> "1 of 6 rounds comparison question"
- Acquiescence bias -> members defaulting to "agree"
- Double-barreled -> two questions packed into one
- Mutually exclusive options -> answer choices that don't overlap
- Exhaustive options -> choices that cover every possible response

## Survey types

Identify type before scoring. Affects D1, D2, D4 requirements. Default to Non-IHUT Product if unstated.

- IHUT: Member tested a free product at home. Longer surveys OK. Product image + co-creator language required.
- Non-IHUT Product: Member evaluating a product/category without receiving it. Shorter surveys required. Co-creator language required.
- Services / Concept: Service, concept, or market research topic. No physical product. Image/co-creator requirements adjusted.
- Market Research: Brand tracking, ad testing, pricing, general insights. Adjusted requirements apply.

## Auto-fail conditions

Check these FIRST. Any present = survey cannot be sent regardless of score. Flag immediately and stop scoring.

1. Leading Question on Primary Objective: any question that steers respondents toward a specific answer on the core research topic.
2. Impossible Answer Set: a required question where no valid answer exists for a meaningful portion of the member base.
3. Screener That Eliminates the Audience: a screener so narrow it disqualifies the majority of MMC members, making data unusable.
4. No Introductory Page: survey begins directly with questions with no member-facing context, purpose statement, or reward mention.

## The 11-dimension quality rubric (106 points total)

### D1 Purpose & Value Clarity (12 pts)
Survey must communicate upfront AND at close why member input matters and what they receive. Half score if messages appear on only one page.
- IHUT / Non-IHUT Product (all 3 required for full score): intro states what product/topic is being evaluated (4); intro includes co-creator language, responses shape real Member's Mark products (4); value exchange stated: points earned, brand contribution, or both (4).
- Services / Concept / Market Research (all 3 required): intro states the topic being explored (4); intro explains why member input matters (4); value exchange stated: points or explicit acknowledgment of member's time (4).

### D2 Length & Pacing (10 pts)
Counting rules: standard questions = 1 each; MaxDiff block = 1; matrix table = 1; multiple questions per page count separately.

| Type | Full | Partial | Low |
|---|---|---|---|
| IHUT | <= 20 | 21-25 | 26+ |
| Non-IHUT (any) | <= 8 | 9-12 | 13+ |
| Services / Market Research | <= 10 | 11-15 | 16+ |

### D3 Plain Language & Grammar (15 pts)
- Clarity (5): one idea per question, no double-barreled; no ambiguous pronouns; select-one / select-all instructions stated explicitly; scales labeled at both ends; flag questions about services/features where availability context is missing (existing, coming soon, or hypothetical).
- Plain Language (5): no jargon (sensory profile, organoleptic, viscosity, incremental lift, net promoter, ROI, construct); approachable reading level (aim grade 8); no overly formal phrasing.
- Grammar & Spelling (5): 0 errors = 5; 1-2 minor errors = 3; 3+ errors OR any error in a question stem = 0. Flag exact text with suggested correction.

### D4 Visual Context (10 pts)
- IHUT / Non-IHUT Product: product image present on intro page (5); image shows the specific product, not generic branding (5). Flag images < 200px wide.
- Services / Concept / Market Research: relevant visual establishes survey topic (5); image is clearly on-topic, not generic or decorative (5).
- No images present: award 3/10. Flag images with missing or unhelpful alt text.

### D5 Community Tone (10 pts)
Language must feel warm, direct, and human: co-creation community, not a corporate panel.
- 10: Conversational throughout. Feels like a person wrote it.
- 7: Mostly warm with occasional formal phrases.
- 4: Predominantly formal. Overall feeling is corporate.
- 0: Entirely clinical. No personality.
One emoji or light humor in the intro is acceptable and encouraged. Emoji in question stems or answer options: flag. Flag clinical phrases and suggest warm rewrites.

### D6 Closing Moment (10 pts)
Final page must include all three: genuine thank-you, not just "Survey complete" (4); points confirmation, "you've earned [X] points" or equivalent (3), waived if platform shows it automatically; co-creator/impact reminder, "your feedback helps shape Member's Mark products" (3).

### D7 Question Variety (8 pts)
- <= 8 questions: 2+ question types = 8; 1 type = 0.
- 9+ questions: 3+ types = 8; 2 types = 4; 1 type = 0.
- Types: single-select, multi-select, rating scale, open-ended, image selection, MaxDiff/ranking, matrix, slider.

### D8 Answer Option Completeness (10 pts)
- Exhaustive options (4): no plausible answer missing.
- Mutually exclusive options (3): no overlap; ranges must not share endpoints (fail: "1-5 years" and "5-10 years").
- Escape options present where needed (3): "Other" / "None of these".
- Additional checks: scale questions label both anchor points; multi-select needs "select all that apply"; single-select needs "select one"; if members could genuinely not know, "Not sure" / "I don't know" is required; do not recommend "Other" on closed-list preference questions without a text field.

### D9 Mobile & Technical Suitability (6 pts)
- Matrix > 6 rows: flag as mobile problem, suggest breaking into separate questions (2).
- Drag-and-drop ranking or fine-motor sliders: flag (2).
- Rendering issues (truncated text, missing content, iframe problems): flag (2).

### D10 Response Bias Check (5 pts)
5 = none present; 3 = 1 instance; 0 = 2+. Always quote the specific question text.
- Acquiescence bias: too many agree/disagree scales back-to-back.
- Social desirability framing: language implying a "correct" answer.
- Anchoring: number or benchmark presented before asking for an estimate.
- Double-barreled: two questions in one.

### D11 Member Experience Framing (10 pts)
- Intro page (7): clear statement of survey purpose (2); co-creator framing (3); reward points mentioned + realistic time estimate (2).
- Outro page (3): genuine thank-you referencing what feedback will be used for (1); reward points confirmation (1); next steps or timeline communicated (1).
- Score 0 if no intro page exists.

## Scoring thresholds
- 80-100: Good to go, approved for sending.
- 60-79: Needs minor fixes, revise before sending.
- Below 60: Needs major revision, must be revised and re-reviewed.
- Any auto-fail: Cannot send, critical issue must be resolved regardless of score.

## Report format (as drafted)
Survey URL, review date, survey type; auto-fail check (4 items) and status; dimension scores listed as: Survey Objective Clarity /12, Question Quality & Clarity /10, Answer Set Completeness /15, Survey Flow & Logic /10, Audience Alignment /10, Length & Respondent Experience /10, Scale & Measurement Consistency /8, Bias & Neutrality /10, Technical & Formatting Quality /6, Actionability of Insights /5, Member Experience Framing /10; total /106 with READY / NEEDS WORK / NOT READY; 2-3 sentences of feedback per dimension; top 3 strengths; top 3 issues with fixes; suggested rewrites (page, current, suggested); plain language note.

## MMC content standards (as drafted)
Do not change the score unless referenced by the rubric. Flag violations and suggest concise rewrites in the MMC voice. (Voice & tone section to be added.)

- Survey titles: sentence case. Flag "How Do You Make Coffee At Home?" Recommend "How do you make coffee at home?"
- Question titles: sentence case, no capitalization for emphasis. Flag "Which Coffee Products Do You Buy Most Often?" Recommend "Which coffee products do you buy most often?"
- Answer options: sentence case, consistent capitalization, grammatically parallel. (Flag/recommend to be added.)
- Emphasis & punctuation: no ALL CAPS for emphasis; avoid repeated ellipses; avoid excessive bold, italics, punctuation. Flag "What do you ACTUALLY reach for?" Recommend "What do you usually reach for?"
- Writing style: avoid first-person narration by an unnamed narrator (Flag "Personally, I...", "My favorite...", "If you ask me...", "I always..."), unless the speaker is identified. (More to come.)
- Answer choice standards: consistent terminology ("single-serve pods" should not drift to "pods", "K-cups", "capsules").
- Images: support the topic, reinforce understanding, don't replace instructions unless fully visible. Flag decorative or unrelated imagery.
- Transitions: use transition screens only when introducing a new topic. (Flag line duplicated from Images in draft.)
- Rewrite guidelines: preserve the research objective; smallest possible wording change; simplify rather than add concepts; keep the MMC voice (warm, conversational, clear, member-focused); don't rewrite purely for style when already clear; when several options exist, recommend the shortest that preserves meaning.
