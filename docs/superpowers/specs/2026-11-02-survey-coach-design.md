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
  member rating from a "How was this survey?" closing question.
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

### 7.2 Reading moment

- Phone on the left fills with questions as they are read. Steps on the right:
  "Reading Q9", "Checking against 24 MMC guidelines", "Previewing on 3 phones".
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
  **Large text**, **Dark mode**.
- **Play as a member**: auto-advances through the survey at estimated member pace.
  A timeline under the phone shows elapsed time and fatigue zones (Fresh, Fatigue
  builds, High), and marks screen-out points with timestamps. Labeled as an estimate.
- The preview is a faithful approximation of RedJade's mobile rendering, not a
  pixel-perfect clone. The UI says so once, unobtrusively.

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
- Ships with a **draft MMC rubric**, clearly labeled draft, until the real criteria are provided.
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

```python
class SurveyReader(Protocol):
    def read(self, url: str, on_progress: ProgressFn) -> SurveySnapshot: ...
```

- `CrawlReader` (v1): opens the public RedJade URL, extracts each screen's question
  text, type, options, scale labels, images (downloaded), required flags, and a
  screenshot; advances by choosing a valid answer; detects screen-out and end pages.
  Records **path coverage** ("linear path, 15 screens, 1 screen-out detected").
- `FixtureReader`: loads saved snapshots (sample survey, tests).
- `ApiReader` (future): same output from the RedJade API. Selected by config.

**SurveySnapshot** (canonical, reader-independent): survey title, intro, ordered
screens, each with `id`, `position`, `kind` (intro, single_choice, multi_choice,
scale, grid, open_text, image_choice, info, thank_you, screen_out), `text`, `options`,
`grid_rows`, `images` (path, dimensions, bytes), `required`, plus `content_hash`
computed over normalized content.

### 8.3 Review pipeline

```
SurveySnapshot
  -> deterministic checks (pure functions)      -> findings
  -> AI judge (batched, structured JSON)        -> findings + suggestions
  -> merge + de-duplicate by fingerprint
  -> scoring (pure function)                    -> score, readiness, minutes
  -> persist Review + Findings
```

**Deterministic checks (v1).** Each is a small, independently tested function:
estimated minutes vs. promised minutes, question count, grid size on small screens,
screener position (screen-out after N seconds), scale direction consistency, missing
negative side on scales, answer option overlap, missing "Other / None" where options
look non-exhaustive (heuristic), reading level (grade above 8), brand glossary,
image byte size, image text legibility proxy (image width vs. phone width), intro
explains purpose, thank-you closes the loop.

**AI judge (v1).** Handles judgment calls: leading or loaded wording, double-barreled
questions, ambiguity and jargon, brand voice, community-guideline tone, image
relevance and legibility (vision), and writes suggestions (Neutral, Shorter,
Friendlier). Rules:

- Survey content is **untrusted input**, passed inside a delimited data block.
  Instructions come only from the system prompt. Output must match a JSON schema
  keyed to screen IDs and guideline IDs. Validated with Pydantic; one retry on
  invalid output, then the criterion is marked "couldn't check".
- Low temperature. Results cached by `(content_hash, rubric_version, model)`.
- Each finding carries: screen ID, guideline ID, severity, evidence quote,
  explanation, member impact, suggestions.

**Scoring.** Member Experience Score 0 to 100. Start at 100 and subtract weighted
penalties per open finding (must-fix weighs more than worth-improving; weights live
on the guideline). Floors at 0. Readiness:

| Readiness | Rule |
|---|---|
| Needs work | Any open must-fix |
| Almost ready | Zero open must-fix, score below 85 |
| Ready to launch | Zero open must-fix, score 85 or above |

"Kept on purpose" must-fix findings don't count as open, but stay visible in the
packet. **Projected score** recomputes the same function with chosen suggestions
treated as resolved. Thresholds and weights are config, recalibrated in v1.5.

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

A review is a background job. Progress events (`screen_read`, `check_started`,
`check_done`, `review_ready`, `error`) stream to the browser over SSE. One job per
survey at a time.

### 8.6 Data model

| Table | Key fields |
|---|---|
| Survey | id, url, title, researcher, status, launched_at, created_at |
| Version | id, survey_id, number, content_hash, snapshot_json, reader, coverage, read_at |
| Review | id, version_id, rubric_version, model, score, readiness, est_minutes, created_at |
| Finding | id, review_id, screen_id, guideline_id, severity, evidence, explanation, member_impact, suggestions_json, fingerprint |
| Choice | id, finding_id, picked (original, neutral, shorter, friendlier, custom), reason_code, reason_text, picked_at |
| Guideline | id, rubric_version, category, title, rule, why, good_example, bad_example, severity, weight, check_type, enabled |
| GlossaryTerm | id, rubric_version, avoid, use |
| Performance (v1.5) | id, version_id, completion_rate, median_minutes, dropoff_json, member_rating, responses |

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
| Predicted score vs. member rating, completion, drop-off (v1.5) | CSV import | Whether the score predicts real member experience. |

Rules for honesty:

- Compare only within the same activity type (IHUT, survey, screener, and so on).
- Show "Need 20+ launched surveys" instead of correlations below that threshold.
- The app **proposes** weight or rule changes. A guidelines admin approves them,
  which creates a new rubric version.
- Recommended business process (not product): add a one-question
  "How was this survey?" (1 to 5) to the end of every MMC survey. It's the cleanest
  ground truth for the score.

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
- **The crawler must not submit real responses** (see Risks, section 12).
- Everything stays local in v1: SQLite file and images on the researcher's machine.
- No credentials in the browser. LLM access happens server-side through Wibey.

## 12. Risks and open questions

| # | Item | Impact | Proposed resolution |
|---|---|---|---|
| R1 | **Crawling a live survey may record a fake response in RedJade**, polluting research data and quotas. | High | Spike first. Prefer RedJade's preview or test link. Never submit the final page. If neither works, mark crawl sessions as test responses or require a preview link. Confirm with the RedJade owner. |
| R2 | Wibey headless image support for vision checks is unverified. | Medium | Spike first. Fallback: text-only image checks (size, dimensions, alt text) until the gateway is available. |
| R3 | Crawler picks answers to advance, so it may follow one branch only. | Medium | Show coverage honestly. Prefer options that continue. Branching handled properly by the future API reader. |
| R4 | Real MMC rubric not yet provided. | Medium | Ship draft rubric labeled draft. Guidelines are data, so swapping needs no code change. |
| R5 | Researchers may distrust AI findings. | High | Evidence on every finding, consistent results, and a golden-set check (section 14) before rollout. |
| Q1 | Who owns guidelines edits (admin role)? | Low | v1: anyone can edit, every edit versioned. Revisit when hosted. |
| Q2 | Sign-off skip policy (for example "90+ and no must-fix skips director review"). | Business | Decision for Onder with Morgan and Sue. Product only enables it. |
| Q3 | Can the "How was this survey?" closing question be added to all surveys? | Business | Raise with research leadership. |

## 13. Future extension points

- `ApiReader` replaces `CrawlReader` (config switch).
- "Apply to RedJade" replaces Copy once a write API exists. No interface built now (YAGNI).
- `GatewayProvider` replaces `WibeyProvider` when hosted on AI Launchpad, enabling
  share links, SSO, and live sign-off.
- Admin-portal connector for audience-level fatigue.

## 14. Testing

- **Unit (pytest):** every deterministic check, scoring, timing model, diffing,
  fingerprinting, snapshot normalization. Fixture-driven.
- **Judge:** schema validation, retry path, caching, injection resistance (survey text
  that contains instructions must not change behavior), all against `FakeProvider`.
- **Reader:** `CrawlReader` against saved RedJade HTML served locally. One opt-in live smoke test.
- **API:** httpx tests per route, including SSE event order.
- **E2E (Playwright), isolated per feature:** paste and read, review navigation,
  version choice and preview, copy, re-check diff, packet export, guidelines edit,
  first-run sample.
- **Accessibility:** axe on every screen in both themes, keyboard-only pass.
- **Golden set (pre-rollout gate):** 20 to 30 past surveys graded by senior directors.
  Measure agreement on must-fix findings. Rollout proceeds when agreement is
  acceptable to research leadership.

## 15. Build order

1. Spikes: R1 (crawl without polluting responses) and R2 (Wibey vision). Results may adjust section 8.
2. Snapshot model, FixtureReader, sample survey, deterministic checks, scoring, timing.
3. FastAPI, SQLite, jobs, SSE. Home and Reading moment.
4. Review workspace: rail, phone (devices, toggles), coach with choices and copy.
5. AI judge with WibeyProvider, caching, suggestions, Ask the coach.
6. CrawlReader.
7. Re-check and versions, then sign-off packet export.
8. Guidelines library and glossary.
9. Play as a member and polish (motion, empty states, a11y pass).
10. v1.5: performance import and predicted vs. actual.
