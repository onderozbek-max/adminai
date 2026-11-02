# SurveyCoach: Reading RedJade Surveys (Reader Design)

- **Date:** 2026-11-02
- **Parent spec:** `2026-11-02-survey-coach-design.md` (this document replaces its section 8.2)
- **Status:** Draft for review. Section 12 lists the spike that confirms the RedJade-specific parts.

---

## 1. What the reader must do

| # | Requirement |
|---|---|
| RQ-1 | Read **every question type**, including ones we haven't anticipated: single and multiple choice, open text, numeric, dropdowns, grids and matrices, sliders, rankings, best/worst rounds, image choices, nested sub-questions (Q1.1, Q1.2), questions revealed on the same page, info screens, screen-outs, thank-you pages. Unknown widgets must degrade gracefully, never silently disappear. |
| RQ-2 | Retrieve **question text, answer options, and images** (original files, plus their rendered size on a phone). |
| RQ-3 | Capture **how each page looks on a phone**, so the mobile viewer is faithful and supports Current / With fixes, device sizes, and Large text. |
| RQ-4 | **Never pollute research data**: no fake responses counted in results or quotas (section 9). |
| RQ-5 | Survive RedJade's page markup changing, without code changes where possible. |
| RQ-6 | Switch to the RedJade API later by replacing one part, not the whole reader. |
| RQ-7 | Be **re-runnable**: improving the extraction must not require visiting RedJade again. |
| RQ-8 | Be honest about **coverage**: what was read, how confidently, and what wasn't reached. |

## 2. The core idea: capture once, interpret many times

Reading is split into two independent stages:

1. **Capture.** A headless phone browser walks the survey and saves everything about each
   page into a **capture bundle** on disk: screenshots, the rendered page markup, the
   accessibility tree, element positions, images, and network traffic. It makes no
   decisions about what a "question" is.
2. **Interpret.** Pure functions turn a capture bundle into three outputs:
   - **Structure:** the `SurveySnapshot` (screens, questions, options, media) for the checks.
   - **Appearance:** a **replica** of each page for the mobile viewer.
   - **Coverage:** an honest report of what was read and how.

Why this split:

- Extraction bugs are fixed by re-interpreting saved bundles, with no new RedJade
  sessions (RQ-7, and fewer chances to pollute data).
- Every real capture becomes a regression test fixture.
- When the API arrives, it replaces the *structure* source. Appearance still comes from
  a capture, because an API returns data, not how the page looks on a phone (RQ-6).

```
RedJade URL
  -> CaptureSession (Playwright, phone emulation)
       Navigator  <->  PageCapturer
       -> CaptureBundle (disk)
            -> Extractor chain  -> SurveySnapshot (+ confidence per question)
            -> ReplicaBuilder   -> sanitized per-screen HTML + assets
            -> CoverageReport
                 -> review pipeline, phone viewer, reading moment

Later:  RedJade API (StructureSource) --merge by question ID--> SurveySnapshot
        CaptureSession (AppearanceSource) -----------------------> replica + screenshots
```

## 3. Capture session

### 3.1 Browser setup

- Playwright Chromium, headless, a **fresh browser context per session** (no cookies,
  storage, or cache carried between sessions or surveys).
- **Phone emulation:** iPhone-class viewport (390 x 844 CSS px, device scale factor 3,
  touch, mobile user agent). The exact user agent mirrors how the MMC app opens RedJade
  (in-app web view or browser), confirmed in the spike.
- Locale `en-US`, timezone `America/Chicago`, reduced motion on (stable screenshots).
- Network recording on (HAR). Third-party analytics and trackers are blocked, so pages
  load faster and nothing is reported to analytics.
- Hard limits: 150 screens per session, 30 s per page load, 10 minutes per session,
  200 MB per bundle, 15 MB per asset.

### 3.2 What is captured for every screen

| Artifact | How | Used for |
|---|---|---|
| Viewport screenshot (what's visible without scrolling) | `page.screenshot()` | "Fits on one screen" (6.1), pins, packet thumbnails |
| Full-page screenshot | `page.screenshot(full_page=True)` | Ground truth for the viewer, replica fidelity check |
| Rendered markup with element tags | `page.content()` after tagging (3.3) | Replica, generic extractor |
| Accessibility tree | `page.locator("body").aria_snapshot()` | Generic extractor: roles and names of every control |
| Element geometry | One `page.evaluate` pass: bounding boxes, rendered vs. natural image size, text overflow (`scrollWidth > clientWidth`), computed font size, CSS background images | Phone checks (D6, D7), pins, stretched-image check |
| Assets | Images, fonts, and stylesheets from network responses, stored once by content hash | Image checks, replica |
| Console errors and failed requests | Playwright events | Broken images (B7), rendering issues (6.5) |
| Navigation log | What the navigator did (answers chosen, retries, timings) | Coverage, debugging, determinism |

### 3.3 Element tagging

Before saving the markup, the capturer stamps every meaningful element with a stable
`data-sc-id` (question container, question text, option, input, image, button). The same
ID is used in the snapshot, in findings, in phone pins, and in "With fixes" patches.
One ID scheme ties reading, checking, and previewing together.

### 3.4 Progressive streaming

Each captured screen is emitted immediately (`screen_captured` event with its viewport
screenshot), so the reading moment shows the **real pages** arriving on the phone
while the walk continues.

## 4. Navigator: getting from page to page

To see page 2, page 1 must be answered. The navigator answers like a careful tester.

### 4.1 Answer policy (deterministic)

| Control | Answer |
|---|---|
| Radio group / single choice | First option that isn't an exclusive "none" or "prefer not to say" (screeners: see 4.3) |
| Checkboxes / multiple choice | One option, same rule |
| Dropdown | First real option (skip placeholders like "Select...") |
| Short or long text | `SurveyCoach test` (an obvious test marker) |
| Numeric | Midpoint of min/max attributes, else 1; retry with validation hints |
| Date | Today, or the midpoint of the allowed range |
| Slider | Midpoint |
| Grid / matrix | Middle column in every row |
| Ranking (drag or select) | Leave default order; if required, tap items in order |
| Best/worst rounds | First item best, last item worst |
| Constant sum | Split evenly, remainder to the first item |
| Unknown widget | Click the first focusable control inside it, then try Next |

A fixed seed keeps choices **identical across re-checks**, so the same path is walked
each time and version diffs compare like with like.

### 4.2 Page loop

1. Wait for the page to settle (network idle plus no layout change for 500 ms).
2. Capture (section 3.2).
3. Answer controls in visual order. **After each answer, re-scan the page**: newly
   revealed questions (show-if logic on the same page) are captured as conditional
   questions with their trigger recorded.
4. Find the advance control (button whose accessible name matches Next, Continue,
   Submit, an arrow, or the RedJade-specific selector from the adapter).
5. Click and wait. If the page didn't change and error text appeared, read the error,
   adjust the answer (for example, a different number or more selections), and retry
   up to 3 times. Then stop with coverage "blocked at screen N".
6. Detect the page type of the result: **question**, **screen-out** (termination text,
   no inputs, no Next), **end / thank-you**, **loop** (same content hash 3 times, stop).

### 4.3 Screeners and screen-outs

- A screen-out page is captured (it's checked for B3 and the warm thank-you) along
  with the elapsed estimated time at which it occurred.
- Then the navigator **backtracks**: a new session replays the same path and picks a
  different option on the most recent screener question, until it qualifies or the budget
  (5 sessions per survey) runs out.
- The qualifying path is the **primary path** that all checks and the viewer use.
  Screen-out pages found along the way are attached to the screens that triggered them.

### 4.4 Never-submit rule

The navigator never clicks the advance control on the **last question page** (the
page whose next result would be the end page), unless the session is in confirmed
test mode (section 9). The thank-you page is then not captured in live mode; the
coverage report says so, and checks D10 run only in test mode.

## 5. Extractor chain: turning pages into questions

Extractors run in priority order. Each returns questions with a **confidence** (0 to 1)
and a **source**. For every element ID, the highest-confidence result wins.

| Order | Extractor | How it works | Strength |
|---|---|---|---|
| 1 | **Network definition** | If RedJade's page loads the survey definition as JSON, parse it directly. | Exact text, IDs, types, maybe even branching. Confirmed or ruled out by the spike. |
| 2 | **RedJade adapter** | Selector rules for RedJade's markup (question container, numbering, option list, Next button), stored as **data** in `readers/redjade_rules.yaml`. | Precise. Markup changes mean editing a YAML file, not code (RQ-5). |
| 3 | **Generic accessible-form extractor** | Uses the accessibility tree and form semantics that any survey platform must expose: radio groups, checkboxes, text boxes, tables of radios, sliders, labels, fieldsets, headings. Platform-independent. | Works on any reasonable survey page, including widgets the adapter doesn't know. |
| 4 | **Vision fallback** | For anything still unknown or low confidence: the AI judge receives the screenshot crop plus simplified markup and returns structured questions (validated JSON). | Handles custom widgets (card sorts, heat maps). Marked "read by AI". |

### 5.1 Question kinds

`intro`, `info`, `single_choice`, `multi_choice`, `dropdown`, `open_text_short`,
`open_text_long`, `numeric`, `date`, `rating` (stars, numbered scale), `slider`,
`grid_single`, `grid_multi`, `grid_text`, `ranking`, `best_worst`, `image_choice`,
`constant_sum`, `card_sort`, `click_map`, `file_upload`, `video`, `screen_out`,
`thank_you`, `unknown`.

`unknown` questions keep their text, screenshot, and geometry. Text-only checks
(clarity, tone, bias, grammar) still run on them; type-specific checks skip them, and
coverage lists them so the researcher can glance at them.

### 5.2 Nested and grouped questions

- A question may have **children** (Q1 with Q1.1, Q1.2, Q1.3). Nesting comes from, in
  order: the network definition, RedJade numbering patterns in the adapter, then
  fieldset and heading hierarchy in the generic extractor.
- Grids are one question with rows (each row a child question sharing the column scale),
  so both views work: "a grid with 6 rows" (6.3) and per-row text checks (3.1).
- A screen can hold several questions. Checks know both the screen and the question.

### 5.3 Piping and randomization

- **Piping:** text containing values the navigator entered (for example, "You said
  SurveyCoach test...") or an option it chose is marked as **piped** so checks don't
  flag our own test answers as typos.
- **Randomization:** when backtracking produces a second session, option and question
  order are compared. Differences mark the question as **randomized**. Content hashes
  and version diffs use a canonical order (sorted), while checks use the displayed
  order. Without a second session, randomization is unknown, and the snapshot says so.

## 6. SurveySnapshot (reader output)

Replaces the snapshot outline in the parent spec, section 8.2.

```
SurveySnapshot
  survey_title, source_url, captured_at, reader_version, content_hash
  screens: [Screen]
  coverage: CoverageReport

Screen
  id, position, kind (question_page | intro | info | screen_out | thank_you)
  viewport_png, full_png, replica_path, est_scroll_height
  questions: [Question]
  screen_out_of: question id that led here (screen-out pages only)

Question
  id (RedJade ID if known, else stable hash of position and text)
  label ("Q1.2" if shown), text, help_text, kind, required
  options: [Option]    rows: [Question]    scale: Scale | None
  children: [Question] conditional_on: {question_id, option_id} | None
  validation: {min, max, max_length, min_select, max_select}
  media: [Media]       element_id (data-sc-id)   bbox
  flags: piped, randomized
  source: network | redjade | generic | vision     confidence: 0..1

Option:  id, label, element_id, media, is_other_with_text, is_exclusive
Scale:   points, low_label, high_label, has_midpoint, direction
Media:   kind (image | background_image | video | embed), asset_hash, alt,
         natural_w, natural_h, rendered_w, rendered_h, bytes, element_id
```

## 7. The mobile viewer: replica first, screenshot as truth

Three ways to show a page were considered:

| Option | Faithful | Supports With fixes, devices, Large text | Verdict |
|---|---|---|---|
| Screenshots only | Exact | No: a picture can't be edited or reflowed | Ground truth and fallback |
| Re-draw from the snapshot in our own components | Approximate | Yes | Not faithful enough to trust; also a second renderer to maintain |
| **Replica: the captured page markup, made safe, shown in a phone frame** | Near exact | **Yes** | **Chosen** |

### 7.1 Building the replica

- Start from the tagged markup (3.3). **Remove all scripts**, event handlers, forms'
  submit targets, iframes to third parties, and external links.
- Rewrite stylesheets, fonts, and images to locally stored assets. Inline CSS
  background images as local URLs.
- Freeze the state the page had at capture (inputs unselected, the way a member first sees it).
- Serve each replica from a dedicated path inside a **sandboxed iframe with no script
  permission** and a strict content security policy (no network access outside our
  asset path). Survey content is untrusted.

### 7.2 Fidelity check

At capture time, the replica is rendered headlessly at the same viewport and compared
with the real screenshot (pixel difference). Above 98% similarity, the replica is used.
Below that, the viewer falls back to the **screenshot** for that screen and shows a small
"Exact snapshot" label; Large text and text-level With fixes previews are then shown
in the coach panel instead of on the phone.

### 7.3 What each viewer feature does

| Feature | How |
|---|---|
| Current | Replica (or screenshot fallback) |
| With fixes, text | Patch text nodes by `data-sc-id` using the picked suggestion |
| With fixes, images | Swap the image source for the suggested crop |
| With fixes, screen order (for example, screener moved earlier) | Reorder screens in the rail and Play sequence |
| With fixes, structural changes (split a grid, add a question) | Not drawn on the phone. The coach shows the suggested structure. Labeled "not previewed". |
| Devices (iPhone SE, iPhone 16, Android XL) | Resize the iframe; RedJade's responsive CSS reflows. Pins re-position using live element boxes. |
| Large text | Scale text in the replica (130% and 200%) |
| Dark mode | Only shown if the spike finds RedJade supports dark mode. If RedJade is always light, the toggle is removed, and transparent-image checks (7.6) still run. |
| Play as a member | Steps through primary-path screens with the timing model |
| Pins | Positioned from element geometry, so they stay attached as layouts reflow |

## 8. Coverage report

Shown in the reading moment, the review header, and the packet:

- Screens captured, and whether the end page was reached.
- Questions by kind, and how they were read (adapter, generic, or AI) with confidence.
- Unknown widgets and low-confidence questions ("Please glance at Q7, read by AI").
- Screen-outs found and when; sessions used for backtracking.
- Randomization detected or unknown; piped text detected.
- Fidelity fallbacks ("2 screens shown as exact snapshots").
- Blocked or partial reads, with the reason.

A review on partial coverage is still useful, but it's never presented as complete.

## 9. Response safety (no fake data in RedJade)

Each crawl is a survey session. Many platforms **save answers page by page**, so even an
unfinished walk can create a partial response, use up a quota spot, or **use up a
single-use link**. Rules:

1. **Test mode (required default):** SurveyCoach reads RedJade **test or preview links**.
   If RedJade has a test-response flag or a link parameter that excludes responses
   from data and quotas, the reader always sets it.
2. **Live links are refused by default.** If a researcher pastes a link that the spike
   shows to be live, SurveyCoach explains why and asks for the test link. An admin
   setting can allow live links only after RedJade's owner confirms partial responses
   are excluded.
3. Every text answer is `SurveyCoach test`, so any stray response is easy to find and
   delete.
4. Session budget per review is capped (5), and re-checks reuse the same deterministic path.
5. No member identifiers are ever added to the URL.

## 10. Errors

| Situation | Behavior |
|---|---|
| Bot challenge or CAPTCHA | Stop. "RedJade asked to verify a human. Try the test link or retry later." |
| Navigator blocked by validation it can't satisfy | Stop at that screen, review what was read, coverage "blocked at Q9". |
| Embedded video or third-party content | Captured as a screenshot region; checks note "video not analyzed". |
| Asset too large or failed to load | Recorded as a finding (6.5, 7.6, or B7). |
| Session or page timeout | Keep what was read, coverage partial, offer retry. |
| RedJade markup changed (adapter matches nothing) | Generic extractor and vision fallback take over automatically; coverage shows lower confidence. Adapter rules get updated from the saved bundle. |

## 11. Testing

- **Survey Zoo:** a local static fixture site that mimics a multi-page survey with every
  question kind in 5.1, nested questions, same-page reveal logic, validation errors,
  a screener with a screen-out, piping, randomized options, wide and blurry images,
  and a thank-you page. All navigator and extractor tests run against it, offline.
- **Golden captures:** once the spike has a RedJade test link, real capture bundles are
  saved as fixtures (no member data exists in test sessions). Extractor and replica
  changes are tested against them without visiting RedJade.
- **Unit tests:** each extractor on saved bundles; merge rules; piping and randomization
  detection; replica sanitizer (scripts and external requests removed, injection
  attempts neutralized); fidelity comparison.
- **Live smoke test:** opt-in only, test links only.

## 12. Spike R1: what it must answer

Run against a RedJade **test or preview link** first.

1. Does a test or preview link exist? Are test responses excluded from data and quotas?
   Are answers saved per page? Are links single-use?
2. Does the page load the survey definition as JSON (extractor 1)?
3. Are controls native, labeled form elements (generic extractor quality)?
4. Navigation: Next button naming, validation behavior, URL per page or one-page app,
   back button, progress bar.
5. Mobile rendering: image width and height caps, viewport settings, fonts, and
   whether dark mode is supported.
6. Bot protection or rate limits.
7. How the MMC app opens RedJade (in-app web view or browser, user agent, URL
   parameters it adds).

The spike's findings update section 3.1 (user agent), section 5 (adapter rules, network
extractor), section 7.3 (dark mode), section 9 (test mode mechanics), and the rubric's
D6 and D7 thresholds (decision D-7).

## 13. Gap review

A review of this design against the parent spec, the rubric, and how survey platforms
behave in practice found these gaps. Each is resolved above or listed as an open question.

| # | Gap | Resolution |
|---|---|---|
| G-1 | Parent spec said the API reader would *replace* the crawler, but an API returns data, not appearance. The phone viewer would have gone blank. | Split into structure and appearance sources (section 2). |
| G-2 | Never clicking the final submit doesn't prevent pollution if answers save per page, use up quotas, or burn single-use links. | Test links required by default, live links refused (section 9). |
| G-3 | Randomized option order would make content hashes and version diffs unstable. | Canonical order for hashing and diffing (5.3). |
| G-4 | Piped text would contain our test answers and trigger false typo findings. | Piping detection (5.3). |
| G-5 | Questions revealed on the same page by an answer would be missed. | Re-scan after every answer (4.2). |
| G-6 | Screen-outs would end the walk early and hide most of the survey. | Backtracking to a qualifying primary path (4.3). |
| G-7 | Images set as CSS backgrounds, not `<img>`, would escape image checks. | Geometry pass collects computed background images (3.2). |
| G-8 | "With fixes" previews need suggestions addressed to specific elements, not prose. | Suggestions carry `element_id` and replacement text (parent spec 8.3 updated). |
| G-9 | The Dark mode toggle may simulate something members never see. | Shown only if RedJade supports dark mode (7.3). |
| G-10 | A replica that drifts from reality would mislead researchers. | Automatic fidelity check with screenshot fallback (7.2). |
| G-11 | Untrusted survey markup inside our app is a security risk. | Scripts stripped, sandboxed iframe, strict CSP (7.1). |
| G-12 | Re-checks walking different answers would produce noisy diffs. | Deterministic seeded navigator (4.1). |
| G-13 | Thank-you page (D10 checks) can't be captured without submitting in live mode. | Captured in test mode only; coverage states it otherwise (4.4). |
| G-14 | The sign-off packet and accessibility: the replica iframe is visual only. | Iframe has a title and is inert; all findings and text are available in the rail and coach for keyboard and screen-reader users. |

### Open questions for Onder (answers needed before or during the spike)

1. **Does RedJade have test or preview links, and are test responses excluded from data
   and quotas?** This is the gating question for the whole reader.
2. **Does SurveyCoach's automated access fit our contract with RedJade?** Worth a quick
   check with whoever owns the vendor relationship.
3. **How does the MMC app open RedJade surveys** (in-app web view or browser)? An
   engineer on Manuj's iOS team can answer in a minute.
4. **Spanish or other language versions:** do MMC surveys have them? If yes, v1 reads
   the default language and flags that others exist; reading all languages is v2.
