# SurveyCoach: Design Spec

- **Date:** 2026-11-02
- **Owner:** Onder Ozbek (Staff PM, Member's Mark Community)
- **Status:** Draft for review
- **Working name:** SurveyCoach
- **Design mockups:** `docs/superpowers/designs/` (HTML fragments from the brainstorming session)

---

## 1. Summary

SurveyCoach is a standalone web app where an MMC researcher pastes a RedJade survey
link and, within about a minute, sees the survey on a member's phone with a friendly
coach pointing out what members would trip on, why it matters, and better wording.
Researchers edit RedJade themselves, re-check the same link, and the app shows what
got resolved. A one-page sign-off packet replaces hours of senior-director review.

## 2. Goals

1. Help researchers raise survey quality **before** an activity launches.
2. Give members who take surveys a clearly better experience on their phones.
3. Cut the human QA burden, especially senior directors, to a 2-minute sign-off.
4. Learn over time whether the coach's predictions and suggestions are actually good.

### Non-goals (v1)

- Editing or publishing anything in RedJade (no write API exists yet).
- Acting as a launch gate. The coach is advisory. Sign-off policy is a business decision.
- Activity creation, audience building, or scheduling (the admin portal owns these).
- Team analytics dashboards.
- Multi-user hosting, SSO, shareable links (see section 13, Future).

## 3. Users

| User | Role in the product | What they need |
|---|---|---|
| **Researcher** (primary) | Writes surveys in RedJade, pastes link, iterates | Fast, friendly, non-technical, beautiful. Never feels graded. Stays the author. |
| **Member** (ultimate beneficiary) | Takes the survey on a phone | Short, clear, neutral, readable, no late screen-outs, feels heard. |
| **Senior director** (approver) | Signs off before launch | A 2-minute verdict: score, time, what changed, what was kept on purpose. |
| **Guidelines admin** | Owns the rubric and brand glossary | Edit rules in plain English. See which rules the coach gets right. |

## 4. Design principles

1. **The member's phone is the center.** Every finding is shown where it happens on the phone.
2. **Coach, not cop.** Warm, plain-language, encouraging. No points or gamification for researchers.
3. **No fake commits.** Nothing pretends to change RedJade. We suggest, the researcher copies, re-check verifies.
4. **The researcher stays the author.** Choices, not approvals. Their original is always an option.
5. **Same survey, same answer.** Results are cached by content hash and rubric version.
6. **Every finding shows its evidence.** Quoted text, cited guideline, member impact.
7. **Honest numbers.** Estimates are labeled as estimates. No correlations before there is enough data.

## 5. Scope

### v1

- Home ("My surveys"): paste box, pipeline, first-run sample survey.
- Reading moment (live progress while the survey is read and checked).
- Review workspace: question rail, phone stage, coach panel.
- "Which version is better?" choice per finding, with Copy and optional reason.
- Re-check: same URL, new version, automatic resolved / still open / new.
- Versions history.
- Sign-off packet (exported self-contained HTML, printable to PDF).
- Guidelines library (editable rules, examples, brand glossary, draft MMC rubric).
- Settings (researcher name, model choice, theme).

### v1.5

- Performance import (CSV): completion rate, median time, drop-off by question,
  and time since launch. (A member rating isn't possible inside RedJade, decision D-5.)
- Predicted vs. actual on the survey's Performance tab and on Home "Learned" cards.
- Coach accuracy panel inside Guidelines (admin only).

### v2 and parked

| Item | Why parked |
|---|---|
| RedJade API reader | API arrives in a few months. One adapter swap (section 8.2). |
| "Apply to RedJade" | Needs a write API. Button goes where Copy is today. |
| Branching / logic map | Crawler walks one path, so a map would mislead. Needs the API. |
| Cross-survey fatigue ("audience got 4 surveys in 10 days") | Needs admin-portal audience data. |
| Synthetic AI member walkthroughs | Slow, costly, unproven. "Play as a member" covers most of the value. |
| Hosting, SSO, share links, WMT LLM gateway | Needs AI Launchpad hosting. Provider swap (section 8.4). |
| Team insights dashboard | Cut. No user need until 50+ launched surveys. |

## 6. Information architecture

```
Nav (dark)
  My surveys          <- home, paste box is the front door
  Library
    Guidelines        <- rules, examples, glossary, (v1.5) coach accuracy
  Settings

Survey workspace (opened from Home or after paste)
  Review              <- default: rail | phone | coach
  Versions            <- v1 61 -> v2 78 -> v3 89, what changed
  Sign-off packet     <- preview + export
  Performance (v1.5)  <- predicted vs. actual
```

The core object is the **Survey**. A survey has many **Versions** (one per distinct
RedJade content read). Each version has one **Review** per rubric version.

### Pipeline statuses on Home

| Status | Meaning | How it's set |
|---|---|---|
| In progress | Reviewed, open must-fix findings exist | Automatic |
| Ready to launch | Zero open must-fix (resolved, or original kept with intent) | Automatic |
| Live | Researcher marked it launched (with date) | Manual in v1 |
| Learned | Performance data imported | Automatic on import (v1.5) |

## 7. Screens and interactions

### 7.1 Home: My surveys

- Greeting plus paste box: "Paste a RedJade link. You'll see it on a member's phone in about a minute."
- Pipeline columns: In progress, Ready to launch, Live, Learned. Cards show title,
  score chip, one plain-language status line ("2 must-fix", "Day 3, 41% completing").
- First run: empty state offers **Try a sample survey** (bundled fixture), so the first
  critique a researcher sees is not of their own work.
- Pasting a URL that already exists opens that survey and starts a re-check.
- Pasting a new URL asks one quick question while reading starts: **"Is this a new
  survey or a new version of one you've checked?"** (RedJade copies and new test links
  get new URLs, and versions must still line up.)
- **Survey type** (IHUT, Non-IHUT Product, Services / Concept, Market Research) drives
  length targets and image rules. The AI proposes a type from the intro, and the
  researcher confirms or changes it with one tap. The type is set in the admin portal
  today, not in RedJade, so it can't be read reliably.

### 7.2 Reading moment

- The phone on the left fills with the **real captured pages** as they're read. Steps on
  the right: "Reading screen 9", "Checking 46 rubric criteria", "Previewing on 3 phones".
- Deterministic findings appear within seconds of capture finishing; AI findings stream
  in after (performance budget in section 8.5).
- Streams over Server-Sent Events. Respects `prefers-reduced-motion`.
- Partial failure shows what was read and what wasn't (section 10).

### 7.3 Review workspace

**Hero bar.** Score ring, encouraging one-liner, plain numbers: "2 must fix",
"3 worth improving", "9 min for members (goal 7)", and **Share for sign-off**.
When "With fixes" is on, the ring animates to the projected score ("91, was 78")
and time updates. The minutes **goal** is the time promised in the survey intro when
detected ("takes about 5 minutes"), otherwise a configured default per activity type.

**Question rail (left).** Every screen of the survey (Intro, Q1..Qn, Thank you)
with a status dot (red must-fix, amber worth improving, green fine) and a short
plain-language label. Keyboard: up/down to move, Enter to focus coach.

**Phone stage (center).**

- Renders the selected screen as a member sees it. Numbered pins mark each finding.
- Toggles: **Current / With fixes**, device (**iPhone SE / iPhone 16 / Android XL**),
  **Large text**, and **Dark mode** (only if the spike shows RedJade supports dark mode).
- **Play as a member**: auto-advances through the survey at estimated member pace.
  A timeline under the phone shows elapsed time and fatigue zones (Fresh, Fatigue
  builds, High), and marks screen-out points with timestamps. Labeled as an estimate.
- The phone shows a **replica** of RedJade's captured page (sandboxed, scripts removed),
  verified against a real screenshot, with automatic fallback to the screenshot when
  the replica isn't faithful (reader design, section 7).

**Coach panel (right).** For the selected finding:

- Severity chip (Must fix / Worth improving) and cited guideline ("Criteria 2.1").
- What's off, and why it matters to members, in plain language.
- **Which version is better?** Radio list: **Your original**, plus up to three
  suggestions (Neutral, Shorter, Friendlier). Selection drives the "With fixes"
  preview and is recorded as a learning signal. Each suggestion has **Copy**.
  Nothing is pre-selected. Until the researcher picks, "With fixes" previews the first
  suggestion, and no Choice is recorded (only explicit picks count as signal).
- If **Your original** is chosen on a must-fix: optional one-tap reason chips
  (Needed for comparability, Suggestion changes meaning, Required wording, Other).
  The finding is then "kept on purpose", shows in the packet, and doesn't block Ready.
- **Ask the coach**: free-text tweak ("mention the waistband") that generates one
  more suggestion, added to the list.
- **Copy all suggestions**: copies a per-question change list, ready to apply in
  RedJade. Uses the picked suggestion where one exists, otherwise the first; skips
  findings where the researcher picked their original.
- **Suggested crop** (image shape findings, rubric 7.2): the coach shows the image
  cropped to 4:5 around the product (subject box from the AI judge, center crop as
  fallback). "With fixes" previews it on the phone, and **Download cropped image**
  saves a file the researcher can upload to RedJade. This is a real fix, not a fake
  commit. Never upscales: low-resolution findings ask for the original file instead.

Findings that aren't tied to one question (for example, "Members Mark" in two
places, or total length) appear under an **All copy** / **Whole survey** rail item.

### 7.4 Re-check

- Button in the hero: **I've updated RedJade, re-check**. Also triggered by
  re-pasting the same URL on Home.
- If content hash is unchanged: "No changes found in RedJade yet." No new version.
- Otherwise a new version is created and reviewed. A banner summarizes:
  **resolved / still open / new**, plus the score change. Each row links to the question.
- If the researcher chose a suggestion and the new version contains it (fuzzy match),
  the finding is marked **Resolved with suggestion**. If resolved differently, it's
  **Resolved your way**. Both count as resolved; they differ as learning signals.

### 7.5 Versions

A simple timeline: version number, read time, score, readiness, and a "what changed"
summary (questions added, removed, edited, reordered). Clicking a version opens it
read-only in the review workspace.

### 7.6 Sign-off packet

- Light theme, printable. Contents: title, version, researcher, Member Experience Score,
  minutes for members, open must-fix count, what changed since v1, **kept on purpose**
  (with reasons), and thumbnails of every screen with pins.
- v1 exports a **self-contained HTML file** (images inlined) that opens offline and
  prints cleanly to PDF. Approve / Request changes happen in Teams or email in v1.

### 7.7 Guidelines library

- Categories: **Brand voice**, **Community guidelines**, **Survey criteria**,
  **Mobile experience**, **Brand glossary**.
- Each rule: ID, title, plain-English rule, why it matters to members, good example,
  bad example, default severity, check type (deterministic or AI), enabled toggle.
- Ships with **MMC Survey Quality Rubric v2** (`docs/rubric/`), loaded as data.
- Edits create a new rubric version. Reviews record the rubric version they used.
- Brand glossary: simple "say this, not that" pairs (for example "Members Mark" to
  "Member's Mark", "customer" to "member").

### 7.8 Visual design

- Dark chrome (navigation, rails, panels) with Sam's Club blue accent. Light theme toggle.
- Phone preview always renders as the member would see it (light, or dark when the
  Dark mode toggle is on), independent of app theme.
- Built with Living Design components and Sam's Club theming. WCAG 2.2 AA in both themes.
- Motion is purposeful: reading moment, ring animation, Play as a member. All respect
  reduced motion.
- No emojis in UI copy.

## 8. Architecture

### 8.1 Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | React + Vite + Living Design (Sam's Club theme) | Walmart UI standard, multi-theme, a11y tooling |
| Backend | Python + FastAPI | Async jobs, SSE, Playwright and LLM orchestration |
| Storage | SQLite (SQLModel) + local files for images and packets | Local single-user v1, zero ops |
| Crawler | Playwright (Python, headless Chromium) | Real rendering, images, screenshots |
| LLM | `LlmProvider` interface, Wibey CLI adapter first (`gpt-6.1-sol`) | Available on this machine today |
| Tests | pytest, curl/httpx API tests, Playwright E2E, axe | Per-feature isolation |

### 8.2 Survey readers

Full design: **`2026-11-02-survey-reader-design.md`** (v2, generic crawler). Summary:

```python
class SurveyReader(Protocol):
    def read(self, url: str, on_progress: ProgressFn) -> ReadResult: ...
    # ReadResult = SurveySnapshot + replica paths + CoverageReport
```

- **Crawl once, interpret many times.** `CrawlReader` (v1) opens the public survey link in
  a headless phone browser and walks it with an OBSERVE, PLAN, ACT, VERIFY loop. A
  strategy registry answers any question type (choice, matrix, text, slider, ranking,
  and more), with an AI vision fallback for unknown widgets. Each page is saved as a
  capture bundle (screenshots, tagged markup, accessibility tree, geometry, images).
- Pure extractors turn bundles into the `SurveySnapshot` (sections, loops, nested
  questions, images), the replica, and coverage. No RedJade account is needed by anyone.
- Each read creates **one tagged test participant** in RedJade and never completes a
  response (reader design, section 10). Onder accepted this trade-off.
- `FixtureReader`: loads saved snapshots and bundles (sample survey, Survey Zoo, tests).
- Future: the RedJade API becomes the **structure** source, merged by question ID;
  appearance still comes from a capture.
- The `SurveySnapshot` model (sections, pages, nested questions, options, scales, media,
  element IDs, confidence) is defined in the reader design, section 6. Its
  `content_hash` uses canonical option order so randomization doesn't create versions.

### 8.3 Review pipeline

```
SurveySnapshot
  -> deterministic checks (pure functions)      -> findings
  -> AI judge (batched, structured JSON)        -> findings + suggestions
  -> merge + de-duplicate by fingerprint
  -> scoring (pure function)                    -> score, readiness, minutes
  -> persist Review + Findings
```

**Deterministic checks (v1).** Each is a small, independently tested function, cited
by rubric ID: estimated minutes vs. promised minutes, question count, screener
position, typing load, grid size and scale length, scale direction and balance,
overlapping ranges, reading level, glossary and content standards (sentence case,
ALL CAPS, desktop words like "click"), answer-choice length, one-screen fit on
iPhone SE, links that leave the survey, intro and thank-you presence.

**Image checks (v1, rubric D7 and B7).** Measured on the downloaded file plus the
crawler's rendered size: aspect ratio (shape), pixel width vs. phone density,
blur score (edge variance with Pillow and NumPy), stretched or squashed (rendered vs.
natural ratio), file size and total survey weight, transparency on dark backgrounds,
and size/shape consistency across image-choice options. The AI judge adds what code
can't see: correct product, product as hero, background and lighting, polish parity
between options, and text baked into images.

**AI judge (v1).** Handles judgment calls: leading or loaded wording, double-barreled
questions, ambiguity and jargon, brand voice, community-guideline tone, image
relevance and legibility (vision), and writes suggestions (Neutral, Shorter,
Friendlier). Rules:

- Survey content is **untrusted input**, passed inside a delimited data block.
  Instructions come only from the system prompt. Output must match a JSON schema
  keyed to screen IDs and guideline IDs. Validated with Pydantic; one retry on
  invalid output, then the criterion is marked "couldn't check".
- Low temperature. Results cached by `(content_hash, rubric_version, model)`.
- Each finding carries: screen ID, question ID, element ID, guideline ID, severity,
  evidence quote, explanation, member impact, suggestions.
- Each suggestion is **element-addressable**: a list of `{element_id, new_text}`
  patches (question text, option labels) plus a display string, so "With fixes" can
  patch the replica. Structural suggestions (split a grid, move a screen) carry a
  `structural` type and are described in the coach, not drawn on the phone.

**Scoring.** Member Experience Score 0 to 100, defined by the rubric
(`docs/rubric/mmc-survey-rubric-v2.md`): nine dimensions, each criterion worth fixed
points. Rubric **blockers** surface as **Must fix**; criteria that cost points surface
as **Worth improving**. Readiness (thresholds are rubric data, not code):

| Readiness | Rule |
|---|---|
| Needs work | Any open blocker, or score below 60 |
| Almost ready | No open blockers, score 60 to 79 |
| Ready to launch | No open blockers, score 80 or above |

"Kept on purpose" blockers don't count as open, but stay visible in the
packet. **Projected score** recomputes the same function with chosen suggestions
treated as resolved. The review hero and the packet also show the **top 3 strengths**.

**Time and fatigue model (deterministic, labeled as an estimate).** Reading time at a
mobile reading speed plus per-kind interaction time (for example, single choice a
few seconds plus options, grid per row, open text substantially longer, images a few
seconds). Constants live in config and are calibrated against real median times once
performance data exists. Fatigue zones come from cumulative time and question count.
Play as a member uses the same model.

**Version diff.** Screens are matched across versions by normalized text similarity
plus position. A finding is resolved when its fingerprint (guideline ID + matched
screen) is absent in the new review. Suggestion adoption is detected by fuzzy
matching the chosen suggestion against the new screen text.

### 8.4 LLM provider

```python
class LlmProvider(Protocol):
    def complete_json(self, system: str, data: str, schema: type[BaseModel],
                      images: list[Path] = ()) -> BaseModel: ...
```

- `WibeyProvider` (v1): writes the prompt to a temp file and runs
  `wibey -f <file> -m gpt-6.1-sol` headlessly; parses JSON from stdout. Model is
  configurable in Settings.
- `FakeProvider`: deterministic canned responses for tests and offline demos.
- `GatewayProvider` (future): WMT LLM Gateway when hosted on AI Launchpad.

### 8.5 Jobs and streaming

A review is a background job. Progress events (`screen_captured`, `capture_done`,
`check_started`, `check_done`, `review_ready`, `error`) stream to the browser over SSE.
One job per survey at a time.

**Performance budget** (15-screen survey, measured on the pilot machine):

| Stage | Target |
|---|---|
| First real page on the phone | under 10 s |
| Capture complete | under 60 s |
| Deterministic findings and score shown | under 5 s after capture |
| AI findings complete | under 90 s after capture (dimension-batched calls run in parallel) |

If AI findings are slower, the review is usable as soon as deterministic findings
appear; AI findings arrive progressively, and the score updates with a gentle animation.

### 8.6 Data model

| Table | Key fields |
|---|---|
| Survey | id, url, title, researcher, status, launched_at, created_at |
| Version | id, survey_id, number, content_hash, snapshot_json, bundle_path, reader, coverage_json, read_at |
| Review | id, version_id, rubric_version, model, score, readiness, est_minutes, created_at |
| Finding | id, review_id, screen_id, guideline_id, severity, evidence, explanation, member_impact, suggestions_json, fingerprint |
| Choice | id, finding_id, picked (original, neutral, shorter, friendlier, custom), reason_code, reason_text, picked_at |
| Guideline | id, rubric_version, category, title, rule, why, good_example, bad_example, severity, weight, check_type, enabled |
| GlossaryTerm | id, rubric_version, avoid, use |
| Performance (v1.5) | id, version_id, completion_rate, median_minutes, dropoff_json, responses |

### 8.7 Suggested layout

```
survey-coach/
  backend/app/
    readers/      crawl.py, fixture.py, base.py
    checks/       one module per check family
    judge/        prompts, schemas, judge.py
    llm/          base.py, wibey.py, fake.py
    scoring.py    diffing.py    timing.py
    packet/       exporter + template
    api/          routes, sse
    models.py     db.py
  frontend/src/
    pages/        Home, Reading, Review, Versions, Packet, Guidelines, Settings
    components/   Phone, QuestionRail, CoachPanel, ScoreRing, PlayTimeline, ...
  fixtures/       sample survey snapshot + saved HTML
  docs/
```

Every file stays under 600 lines.

## 9. Learning loop

| Signal | Source | What it tells us |
|---|---|---|
| Choice: original vs. suggestion, and which style | "Which version is better?" | Acceptance rate per guideline and per style. Low-acceptance rules get flagged for review. |
| Resolved with suggestion vs. resolved your way | Re-check | Whether suggestions are good enough to use verbatim. |
| Keep-original reasons | Reason chips | Where rules are too strict or miss context (for example, tracker comparability). |
| Predicted score vs. completion, drop-off, and actual vs. estimated time (v1.5) | CSV import | Whether the score predicts real member behavior. |

Rules for honesty:

- Compare only within the same activity type (IHUT, survey, screener, and so on).
- Show "Need 20+ launched surveys" instead of correlations below that threshold.
- The app **proposes** weight or rule changes. A guidelines admin approves them,
  which creates a new rubric version.
- Active rubric criteria always sum to exactly 100. Inactive ones (for example 10.4
  until the Q4 rewards launch) are worth 0 and switch on with a pre-agreed rebalance
  (`docs/rubric/decisions.md`, D-8 and D-9).
- A member satisfaction rating can't be added inside RedJade (D-5). A one-tap rating
  in the MMC app after a completed activity would be the cleanest ground truth; that's
  an MMC roadmap candidate, outside SurveyCoach.

## 10. Error handling

| Situation | Behavior |
|---|---|
| Not a valid or reachable URL | Inline message on the paste box with an example of a valid link. |
| Page loads but isn't a RedJade survey | "This doesn't look like a RedJade survey." |
| Crawl stalls or times out mid-survey | Keep what was read, mark coverage "partial", review what we have, offer retry. |
| Screen-out reached early | Record it as a finding (late or early screen-out), note coverage. |
| Wibey not installed or not authenticated | Settings shows a setup card with the exact command. Deterministic checks still run. |
| LLM returns invalid JSON | One retry, then that criterion shows "couldn't check" with retry. |
| Unchanged content on re-check | "No changes found in RedJade yet." |

The researcher always sees something useful. Deterministic findings never wait on the LLM.

## 11. Trust, safety, data

- Advisory only. The app never blocks or launches anything.
- Survey definitions only. No member responses or PII are read or stored.
- **The reader contains its RedJade footprint**: one tagged test participant per read,
  never a completed response (reader design, section 10).
- Surveys often show **unreleased products and concepts**. They're treated as
  confidential: stored only locally, sent only to the Walmart-approved LLM path, and
  the sign-off packet is stamped "Confidential, internal use only".
- Everything stays local in v1: SQLite file and images on the researcher's machine.
- No credentials in the browser. LLM access happens server-side through Wibey.

## 12. Risks and open questions

| # | Item | Impact | Proposed resolution |
|---|---|---|---|
| R1 | **Each crawl creates a participant and saves partial progress in live data** (confirmed in spike R1). | High | Accepted by Onder. Contained: one tagged participant per read, stop before final submit, visible notice to researchers (reader design, section 10). |
| R2 | Wibey headless image support for vision checks is unverified. | Medium | Spike first. Fallback: text-only image checks (size, dimensions, alt text) until the gateway is available. |
| R3 | The navigator walks one qualifying path, so other branches may be unseen. | Medium | Backtracking past screen-outs, honest coverage report. Full branching comes from the future API structure source. |
| R4 | Rubric thresholds in D6 and D7 may shift after the spike measures RedJade rendering (D-7). | Low | Rubric is data; changes go in the rubric and decision log. |
| R6 | **Non-technical researchers can't install and run a local Python, Node, and Wibey app.** | High | Open question O-1 (section 16). |
| R7 | Wibey CLI start-up per call may break the "about a minute" promise. | Medium | Batch AI checks by dimension, run calls in parallel, show deterministic findings first (8.5). Measured in spike R2. |
| R8 | Automated access to RedJade may need vendor approval. | Medium | Ask the RedJade vendor owner before the first live crawl. |
| R5 | Researchers may distrust AI findings. | High | Evidence on every finding, consistent results, and a golden-set check (section 14) before rollout. |
| Q1 | Who owns guidelines edits (admin role)? | Low | v1: anyone can edit, every edit versioned. Revisit when hosted. |
| Q2 | Sign-off skip policy (for example "90+ and no must-fix skips director review"). | Business | Decision for Onder with Morgan and Sue. Product only enables it. |
| Q3 | Member rating at the end of surveys? | Resolved | Not possible in RedJade (D-5). MMC-app rating is a separate roadmap idea. |

## 13. Future extension points

- The RedJade API becomes the structure source (merged by question ID); captures keep
  supplying appearance.
- "Apply to RedJade" replaces Copy once a write API exists. No interface built now (YAGNI).
- `GatewayProvider` replaces `WibeyProvider` when hosted on AI Launchpad, enabling
  share links, SSO, and live sign-off.
- Admin-portal connector for audience-level fatigue.

## 14. Testing

- **Unit (pytest):** every deterministic check, scoring, timing model, diffing,
  fingerprinting, snapshot normalization. Fixture-driven.
- **Rubric validation:** loading the rubric fails unless active criteria sum to exactly
  100, every dimension total matches its criteria, and IDs are unique.
- **Judge:** schema validation, retry path, caching, injection resistance (survey text
  that contains instructions must not change behavior), all against `FakeProvider`.
- **Reader:** Survey Zoo fixture site (every question kind, nesting, reveal logic,
  screen-outs, piping, randomization, bad images) plus golden RedJade capture bundles.
  Live smoke test is opt-in and uses test links only.
- **API:** httpx tests per route, including SSE event order.
- **E2E (Playwright), isolated per feature:** paste and read, review navigation,
  version choice and preview, copy, re-check diff, packet export, guidelines edit,
  first-run sample.
- **Accessibility:** axe on every screen in both themes, keyboard-only pass.
- **Golden set (pre-rollout gate):** 20 to 30 past surveys graded by senior directors.
  Measure agreement on must-fix findings. Rollout proceeds when agreement is
  acceptable to research leadership.

## 15. Build order

The build is sequenced in `docs/superpowers/plans/2026-11-02-roadmap.md` (one
detailed plan per stage), so the order lives in one place.

## 16. Spec review: gaps found and resolved (2026-11-02)

| # | Gap | Resolution |
|---|---|---|
| G-15 | The rubric needs the survey type, but RedJade doesn't hold it. | AI proposes, researcher confirms with one tap (7.1). |
| G-16 | A new RedJade test link or survey copy gets a new URL, breaking version history. | "New survey or new version?" on paste (7.1). |
| G-17 | The rubric existed only as a document; the app needs data, and the two could drift. | `docs/rubric/mmc-survey-rubric-v2.yaml` is the app's source of truth. A test asserts it matches the approved markdown (IDs, points, active flags). Guidelines edits create new rubric versions in the database. |
| G-18 | "About a minute" had no budget behind it. | Section 8.5 budget. |
| G-19 | Unreleased products in surveys are confidential. | Section 11. |
| G-20 | Reader gaps (API vs. appearance, pollution, randomization, piping, reveal logic, screen-outs, CSS images, element-addressable fixes, replica fidelity and safety). | Reader design, section 13 (G-1 to G-14). |
| G-21 | The golden set needs past surveys, but closed RedJade links may no longer open. | Open question O-2. |

### Open questions for Onder

| # | Question | Why it matters |
|---|---|---|
| O-1 | **Who runs v1, and where?** Options: (a) a pilot on Onder's machine with researchers alongside, then hosting on AI Launchpad with the WMT LLM gateway for self-serve; (b) host from the start, which moves the gateway provider and sign-in into v1. | Researchers can't install a local developer stack. This decides whether hosting is v1 or v1.1. |
| O-2 | Can we get 20 to 30 past surveys as RedJade test links or exports, with senior-director grades? | Needed for the pre-rollout golden-set check (section 14). |
| O-3 | Vendor approval for automated access; how researchers should exclude SurveyCoach test participants from results. | Needed before live crawls become routine. |
