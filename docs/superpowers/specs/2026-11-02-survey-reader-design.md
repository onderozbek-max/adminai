# SurveyCoach: Reading RedJade Surveys (Reader Design v2, Generic Crawler)

- **Date:** 2026-11-02
- **Parent spec:** `2026-11-02-survey-coach-design.md` (this document replaces its section 8.2)
- **Evidence:** `docs/spikes/r1-redjade-findings.md`, `docs/spikes/r1b-previewer-findings.md`
- **Decision (Onder, 2026-11-02):** read surveys with a **generic crawler on the public
  survey link**. No RedJade accounts, no project sharing, no admin roles. The live-data
  impact is accepted and contained (section 10). The previewer approach is rejected (section 14).

---

## 1. What the reader must do

| # | Requirement |
|---|---|
| RQ-1 | Work from the **public survey link alone**, for anyone, with no RedJade account. |
| RQ-2 | **Progress through every page generically**: press a button; pick an option and continue; pick in every row of a matrix; pick several options; type a required text or number; slide, rate, rank, or any other interaction a question needs. New question types are added without touching the crawler core. |
| RQ-3 | Recognize **nested structure**: several questionnaires in one survey (intro, per sample), repeated loops (same questions per sample), matrix rows and sub-questions (Q1.1, Q1.2), questions revealed on the same page. |
| RQ-4 | **Crawl images** of every kind (`<img>`, responsive sources, CSS backgrounds, SVG, video posters) with original files and rendered size, for evaluation. |
| RQ-5 | Capture **how each page looks on a phone** for the mobile viewer. |
| RQ-6 | **Contain the live-data impact**: one tagged participant per read, never a completed response (section 10). |
| RQ-7 | Be **re-runnable**: improving extraction never requires crawling again. |
| RQ-8 | Be honest about **coverage**: what was read, how confidently, what wasn't reached. |

## 2. Architecture

Two stages: **crawl and capture** (touches RedJade once per read), then **interpret**
(pure functions over saved files, re-runnable at will).

```
Survey link
  -> Resolve: GET event_meta (public, read-only): title, project, event, locales, theme, live status
  -> CrawlSession (Playwright Chromium, phone emulation, fresh context)
       per page:  OBSERVE -> PLAN -> ACT -> VERIFY      (section 4)
                  strategy registry (section 5), vision fallback (5.6)
       passive recorder: questionnaire JSON if RedJade sends it (3.3)
  -> CaptureBundle on disk (per page: screenshots, tagged DOM, a11y tree, geometry, images)
  -> Interpret (pure):
       extractor chain  -> SurveySnapshot (structure, nesting, confidence)   (section 8)
       ReplicaBuilder   -> sanitized per-page HTML for the phone viewer      (section 9)
       CoverageReport                                                       (section 11)
```

`SurveyReader` remains the seam. `CrawlReader` is v1, `FixtureReader` serves tests and
samples. When the official RedJade API arrives it becomes the **structure** source
(merged by question ID); the crawl keeps providing **appearance**.

## 3. Crawl session

### 3.1 Browser setup

- Playwright Chromium, headless, **fresh context per read**. Proxy from the system PAC
  file (`proxy-intlho.wal-mart.com:8080` on the Walmart network).
- Phone emulation: iPhone 16 (393 x 852 CSS px, DPR 3, touch, iOS Safari user agent).
- Locale `en-US`, reduced motion, analytics and tracker requests blocked.
- Limits: 200 pages, 30 s per page, 15 minutes per read, 300 MB per bundle, 15 MB per image.

### 3.2 Per-page capture (OBSERVE)

| Artifact | Notes |
|---|---|
| Viewport screenshot | What a member sees without scrolling. |
| Full-content screenshot | RedJade scrolls **inside an inner container** (spike R1b), so the capturer finds the scrolling element, scrolls it in steps, and stitches. `full_page` alone is wrong. |
| Tagged DOM | Every question container, prompt, option, input, image, and button gets a stable `data-sc-id` before saving. Findings, pins, and "With fixes" patches use the same IDs. |
| Accessibility tree | `aria_snapshot()`: roles and names of every control. |
| Geometry | Bounding boxes, inner-scroller height vs. viewport (true "fits on one screen"), text overflow, computed fonts, image natural vs. rendered size. |
| Images | Section 7. |
| Console errors, failed requests | Broken images (B7), rendering issues (6.5). |
| Action log | What was observed, planned, done, and verified (section 4), with timings. |

Each page is streamed to the UI as soon as it's captured (`page_captured` event), so the
reading moment shows real pages arriving on the phone.

### 3.3 Passive definition recording

RedJade's participant app must download the questionnaire to draw it. The recorder keeps
every JSON response from `/api/v1/` (secrets redacted). If it contains the questionnaire
definition (the previewer used `questionnaires/<id>` with `page_groups -> pages ->
questions`, `answers`, `triggers`), the extractor chain uses it as the **highest-confidence
source, including branches the walk never visited**. If RedJade doesn't send it, nothing
breaks: the page-based extractors carry the read. First real crawl confirms which.

## 4. The page loop: OBSERVE, PLAN, ACT, VERIFY

```
for each page (until end, stop rule, or budget):
    observe  -> PageObservation (DOM, a11y, screenshot, geometry, page kind)
    classify -> intro | question | sample_code | info | screen_out | end | error
    plan     -> for each ResponseGroup: pick the best Strategy, produce Actions
    act      -> run Actions; after each one re-observe for revealed questions (4.3)
    advance  -> press the advance control (4.4), unless the stop rule says no (10)
    verify   -> new page? done. Same page + validation error? repair (4.5). Stuck? vision (5.6)
```

### 4.1 Response groups (generic detection)

A **response group** is one thing a member must answer. Detection is platform-neutral,
in this order, each signal adding confidence:

1. ARIA: `radiogroup`, `group`, `listbox`, `slider`, `spinbutton`, `grid`, `table` with inputs.
2. Native forms: inputs sharing a `name`, `fieldset`/`legend`, `select`, `textarea`, `input[type=*]`.
3. **Button-style options** (RedJade renders answers as buttons, spike R1b): sibling
   clickable elements with similar size and style under one prompt, toggled by
   `aria-pressed`, `aria-checked`, or a class change on click.
4. Layout: a repeated row structure under a header row = matrix; each row is a child group.
5. RedJade rules file (`readers/redjade_rules.yaml`): selectors learned from captures,
   kept as data so markup changes mean editing YAML, not code.

### 4.2 Plan

Each group goes to the strategy registry (section 5); the highest-confidence strategy
produces a list of typed **Actions**: `click(id)`, `select(id, value)`, `type(id, text)`,
`set_range(id, value)`, `drag(id, to_id)`, `scroll(id)`, `press(key)`. Actions only target
tagged elements on the current page. Nothing else is allowed.

### 4.3 Same-page reveals

After every action the page is re-observed. New groups that appear (follow-up questions,
"Other, please specify" boxes) are captured as **conditional**, linked to the option that
revealed them, and planned in turn.

### 4.4 Advance control

Found by role and accessible name (`Next`, `Continue`, `Begin`, `Start`, `Submit`,
`Finish`, `Done`, arrow icons with an aria-label), position (bottom, sticky footer), and
the rules file. Its label also feeds the stop rule (`Submit`, `Finish`, `Done` on a
non-intro page = likely final submission; section 10).

### 4.5 Verify and repair

- **Page fingerprint** = hash of visible prompt text, option labels, and URL. Changed = advanced.
- Unchanged plus visible error text: parse it with repair rules, re-plan, retry up to 3 times.

| Error pattern (examples) | Repair |
|---|---|
| "required", "please answer", "select an answer" | Fill groups that were skipped or misdetected |
| "select at least N" / "at most N" / "exactly N" | Adjust the number of selections |
| "between X and Y", "must be a number" | Re-enter a number within range |
| "must total 100" | Rebalance constant-sum inputs |
| "N characters" | Type a longer or shorter text |
| "rank all items" | Complete the ranking |

- Still stuck: vision fallback (5.6). Still stuck: stop with coverage "blocked at page N",
  keep everything captured so far.

## 5. Strategy registry (how any question type gets answered)

### 5.1 Contract

```python
class InteractionStrategy(Protocol):
    kind: str                                           # e.g. "single_choice"
    def detect(self, group: ResponseGroup) -> float: ...   # confidence 0..1
    def plan(self, group: ResponseGroup, policy: AnswerPolicy) -> list[Action]: ...
```

Strategies are registered in a list; the crawler core never knows question types.
**Adding a type = adding one strategy class plus a Survey Zoo page** (open/closed).

### 5.2 Built-in strategies

| Strategy | Detects | Plans |
|---|---|---|
| `AdvanceOnly` | Info, intro, and instruction pages with no groups | Nothing; just advance |
| `SingleChoice` | Radio groups, button-style options with single selection | Click one option |
| `MultiChoice` | Checkbox groups, multi-toggle buttons | Click one (or the minimum required) |
| `Dropdown` | `select`, `listbox`, custom combobox | Open, pick first real option |
| `ShortText` / `LongText` | `input[type=text]`, `textarea`, contenteditable | Type `SurveyCoach test` (padded if a minimum length applies) |
| `Numeric` | `input[type=number]`, `spinbutton`, numeric patterns | Midpoint of min/max, else 1 |
| `Date` | `input[type=date]`, date pickers | Today or midpoint of the allowed range |
| `Rating` | Star rows, numbered scales, NPS 0 to 10 | Middle value |
| `Slider` | `input[type=range]`, `role=slider`, line scales | Keyboard arrows to the midpoint; drag as fallback |
| `MatrixSingle` / `MatrixMulti` | Rows of radios or checkboxes under a column header | Middle column in **every row** |
| `MatrixText` | Rows of text or number inputs | Fill every cell |
| `Ranking` | Draggable lists, rank-by-click, rank dropdowns | Keep the shown order: click in order or assign 1..N |
| `BestWorst` | Paired best/worst columns per item set | First item best, last item worst |
| `ConstantSum` | Numeric inputs with a total | Split evenly, remainder to the first |
| `ImageChoice` | Options that are images (or image plus label) | Treated as single or multi choice |
| `SampleCode` | Prompts asking for a sample or blinding code | Use a code shown on the page if present; else stop with "needs a sample code" |
| `Consent` | Single checkbox plus agreement text | Check it |
| `VisionAssisted` | Anything with confidence below 0.5 | Section 5.6 |

### 5.3 Answer policy

- **Deterministic** (seeded): the same survey gets the same answers on every re-check,
  so version diffs compare the same path.
- Avoid exclusive answers ("None of these", "Prefer not to say") unless required.
- **Screeners:** if the next page is a screen-out, capture it, then (budget permitting)
  start a fresh session and pick a different option on the last screener question.
  Budget: 3 sessions per read (each is one tagged participant; section 10).

### 5.4 Answer text is a marker

Every typed text is `SurveyCoach test`, and numbers are plausible but not extreme, so
stray partial responses are easy to spot.

### 5.5 Page kind classification

`screen_out` (no inputs, no advance, termination wording), `end` (thank-you wording, no
advance), `error` (RedJade error states seen in its code: `completed_survey`,
`test_complete`, `no_event_scheduled`, `invalid_code`), `sample_code`, `info`, `question`.

### 5.6 Vision fallback (screenshot to actions)

Used only when deterministic strategies fail or have low confidence. It's the
"screenshot to image and text" path, made safe:

1. Draw numbered marks on every tagged interactive element (set-of-marks screenshot).
2. Send the screenshot, the mark list (id, role, name), and the visible error text to the
   AI judge with a fixed instruction: return JSON `{questions: [...], actions: [...]}`.
3. Validate with Pydantic: actions must use the allowed action types and existing mark
   IDs. Anything else is rejected. Survey text is untrusted input.
4. Execute, verify, and log. At most 2 vision attempts per page.
5. Questions it reports are recorded with `source: vision` and shown as "read by AI".

## 6. Nested structure, loops, and reveals

| Structure | How it's recognized | How it's recorded |
|---|---|---|
| Several questionnaires in one survey (intro plus product sections) | Questionnaire boundary: progress bar resets, header changes (for example "Sample 578"), title change, or definition JSON `questionnaire_id` | `Section` nodes grouping pages |
| **Loops** (same questions per sample) | Page fingerprints repeat with a different header or sample code | First instance captured fully; later instances recorded as **repeats** (count, sample labels). Counts drive the time estimate and fatigue. |
| Matrix rows | Row structure under a column header | Parent question with row children sharing the scale |
| Sub-questions (Q1.1, Q1.2) | Numbering patterns, fieldset nesting, heading hierarchy, definition JSON | Parent with children |
| Same-page reveals | New groups after an action (4.3) | `conditional_on: {question, option}` |
| Branches not walked | Definition JSON `triggers` (if captured) | Present in the snapshot as `reached: false`; checked on text, not shown on the phone |

## 7. Images

### 7.1 Discovery (per page, after lazy content loads)

- Scroll the **inner scroller** to the bottom in steps so lazy images load.
- Collect: `<img>` (using `currentSrc`, so the responsive source actually chosen),
  `<picture>`, CSS `background-image` on any element, inline `<svg>`, `<canvas>` (snapshot),
  video `poster`, and images inside option buttons (image choice).

### 7.2 Capture

| Field | Source |
|---|---|
| Original bytes | Downloaded through the same browser context (same cookies), stored by content hash |
| Format, file size | Response headers and bytes |
| Natural size | `naturalWidth/Height` or decoded file |
| Rendered size and position | Bounding box at the phone viewport |
| Crop | `object-fit`, `object-position`, background-size; the visible region is computed |
| Sharpness check | Natural width vs. rendered width x DPR (upscaled = blurry) |
| Alt text and nearby label | DOM |
| Rendered crop | Element screenshot exactly as the member sees it |
| Role | Question illustration, option image, logo or decoration (by position and size) |

### 7.3 Evaluation hand-off

Deterministic checks (D7 rubric): resolution vs. rendered size, upscaling, aspect ratio
and crop loss, file weight, missing alt text, failed loads (B7). AI checks: relevance to
the question, clarity, legibility of text inside the image, and whether the product is
recognizable at phone size.

## 8. Interpretation: extractor chain and SurveySnapshot

### 8.1 Extractor chain

Runs over a saved bundle (no RedJade access). For each element ID, the highest-confidence
result wins.

| Order | Extractor | Source |
|---|---|---|
| 1 | Definition | Questionnaire JSON captured passively (3.3): exact text, IDs, types, answers, values, triggers |
| 2 | RedJade rules | `readers/redjade_rules.yaml` selectors over the tagged DOM |
| 3 | Generic | Response groups and strategy kinds from the crawl (4.1, 5.2), accessibility tree, labels |
| 4 | Vision | Questions reported by the vision fallback (5.6) |

The crawl already knows each group's kind (it had to answer it), so extraction mostly
**names and links** what the crawl did, rather than guessing from scratch.

### 8.2 SurveySnapshot

```
SurveySnapshot
  survey_title, source_url, event_id, project_id, captured_at, reader_version, content_hash
  theme (from event_meta)    sections: [Section]    coverage: CoverageReport

Section:   id, title, kind (intro | product | screener | other), pages: [Page], repeats: [str]
Page:      id, position, kind (question | info | intro | sample_code | screen_out | end)
           viewport_png, full_png, replica_path, scroller_height, viewport_height
           questions: [Question], reached: bool
Question:  id (RedJade id if known, else stable hash), label ("Q1.2" if shown), text, help_text
           kind (strategy kind or "unknown"), required, options: [Option], rows: [Question]
           children: [Question], scale, validation, conditional_on, media: [Media]
           element_id, bbox, flags (piped, randomized), source, confidence, reached
Option:    id, label, value, element_id, media, is_other_with_text, is_exclusive
Media:     kind, asset_hash, alt, natural_wh, rendered_wh, visible_crop, bytes, format,
           role, element_id
```

- `content_hash` uses canonical (sorted) option order, so randomized surveys don't create
  false new versions. Option order is randomized if the definition says so, or if it
  differs across sessions.
- Piped text (containing the crawler's own answers, such as `SurveyCoach test`) is
  flagged so checks don't treat it as a typo.

## 9. Mobile viewer

- **Current:** a replica of the captured page (scripts removed, assets local, sandboxed
  iframe, strict CSP), checked against the real screenshot at capture time. Below 98%
  pixel similarity, that page falls back to the screenshot.
- **With fixes:** text patches by `data-sc-id`, image swaps for suggested crops, screen
  reordering. Structural fixes (splitting a grid) are described in the coach, labeled
  "not previewed".
- **Devices and Large text:** resize the iframe and scale text; pins follow live element boxes.
- **Dark mode:** shown only if RedJade's theme supports it (event_meta shows a single
  light theme so far).
- **Play as a member:** steps through captured pages with loops expanded by repeat count.

## 10. Live-data containment (accepted trade-off)

Spike R1 confirmed: pressing Begin **creates a participant**, and progress is **saved per
page**. A crawler can't avoid that, so it's contained:

| Rule | Detail |
|---|---|
| One participant per read | Re-checks are new reads. Screener backtracking adds at most 2 more (budget 3). |
| **Tagged participants** | If RedJade accepts an `external_id` link parameter (its sign-in code sends one), every read uses `external_id=SURVEYCOACH-TEST-<read id>`, so researchers can filter or delete these participants. Verified on the first crawl; if unsupported, the marker text (5.4) is the fallback. |
| **Never complete a response** | Stop before the final submission: an advance button labeled Submit, Finish, or Done on a non-intro page, a progress bar at 100%, or the last page of the definition JSON. The thank-you page is therefore not captured; coverage says so and D10 checks use the definition text when available. |
| Never retake | Fresh context per read; no participant reuse. |
| Visible to researchers | The paste box says: "Reading this survey adds one test participant, tagged SurveyCoach, to RedJade. Exclude it from results." The sign-off packet lists each read's tag. |
| Prefer pre-launch reads | Guidance: check surveys before the link goes to members. |
| Rate limits | One read at a time per survey; no read more than once a minute. |
| No member identifiers | Never add real member IDs or `enc` tokens. |

## 11. Coverage report

Shown in the reading moment, review header, and packet: pages captured; questions by kind
and source (definition, rules, generic, AI) with confidence; sections and loop repeats;
reveals found; screen-outs found; branches known but not walked; stop reason (end
reached, final-submit stop, blocked at page N, budget, error); participants created with
their tags; replica fallbacks.

## 12. Errors

| Situation | Behavior |
|---|---|
| RedJade error state (`completed_survey`, `no_event_scheduled`, `invalid_code`) | Stop, explain in plain words (for example "This survey is closed") |
| Bot challenge or CAPTCHA | Stop. Never attempt to bypass. |
| Sample code required and not shown | Stop at that page: "This survey needs a sample code to continue." |
| Blocked by validation after repair and vision | Stop at that page, review what was read |
| Embedded video or third-party content | Captured as an image region; "video not analyzed" |
| Timeout or budget reached | Keep what was read, coverage partial, offer retry |
| RedJade markup changes | Generic detection and vision take over; rules YAML updated from saved bundles |

## 13. Testing

- **Survey Zoo** (local fixture site, offline): one page per strategy in 5.2, in both
  native-input and **button-style** variants; inner scroll container; matrix with 8 rows;
  same-page reveal; validation errors for each repair rule; screener with screen-out;
  intro plus two product sections with a per-sample loop; sample-code page; lazy,
  responsive, background, SVG, and oversized images; a final Submit page (must stop before it).
- **Strategy unit tests:** detect and plan on saved observations.
- **Loop tests:** the full crawl of the Zoo produces the expected sections, repeats,
  reveals, images, and stop reason.
- **Vision fallback:** FakeProvider returns valid, invalid, and malicious action JSON;
  only valid actions run.
- **Golden bundles:** each real RedJade read is saved and replayed through the extractors
  without network access.
- **Live crawl:** opt-in only, on a link Onder approves, one tagged participant.

## 14. Assumptions and decision history

**Assumptions the crawler depends on** (deliberately few):

1. The public link opens without login (confirmed for the three examples).
2. No bot challenge (none seen in RedJade's code path).

**Nice to have, verified on the first crawl, not required:** questionnaire JSON visible
in network traffic (3.3); `external_id` tagging (10).

**Rejected: reading through RedJade's previewer** (spike R1b). It worked technically and
saved nothing, but needed a RedJade account, per-project sharing, and possibly an admin
role, which ruled out managers, designers, and engineers without RedJade. Kept as an
option if RedJade ever offers a service account or API.
