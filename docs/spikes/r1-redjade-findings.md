# Spike R1: How RedJade serves surveys (findings, 2026-11-02)

**Method:** read-only. Fetched the three example survey links' HTML, RedJade's public
JavaScript bundles, and the public `event_meta` endpoint (the same call a member's
browser makes when the link opens). **No sign-in, no answers, no participants created.**
Raw artifacts are in `spikes/r1/` (git-ignored: RedJade's code and internal project data).

Examples: `CakeballsDeepDive`, `PrivateReserveWhiteWine`, `posthalloween26` under
`https://app.redjade.net/surveys/samc/`.

## Network

- `app.redjade.net` doesn't resolve on the Walmart network directly. It works through
  the PAC-selected proxy `proxy-intlho.wal-mart.com:8080` (Kerberos, no extra login).
  `sysproxy.wal-mart.com:8080` returns 407. The reader must use the system PAC proxy.

## How a RedJade survey link works

1. The link returns a 4 KB **app shell** (AngularJS plus Svelte). No survey content is in the HTML.
2. The app calls **`GET /api/v1/surveys/event_meta?static_url=<name>&company_token=samc`**
   (public, read-only). It returns 45 KB of metadata, including:
   - `display_name` ("Insights Cakeball & CakePop Deep Dive: Acceptance Test (P300489)"),
     `project_id`, `event_id`, `project_name`
   - `event_online_type: "anonymous_link"`, `is_online_event_active: true`
   - `locales` (1 = English only), screen texts, variables
   - **`theme`**: font (Lato), root and question font size (18 px), colors, button style
     (pill), progress bar settings, page width, per-element style overrides
   - **No questions.**
3. Pressing Begin calls **`POST /api/v1/surveys/online_sign_in_events`**, which **creates a
   participant** and returns an auth token. It accepts `external_id` and `enc` (likely how
   the MMC app identifies members) and optional challenges (code, email, date of birth).
4. Answering posts **`page_start_events`** and **`in_progress_check_events`** with the
   in-progress questionnaire: **progress is saved page by page.**
   `questionnaire_submit_events` completes it.

## Consequences

- **Walking a live link is never safe.** These are active anonymous-link surveys: any
  walk past Begin creates a participant and saves partial responses in live data.
- The questions can't be read without signing in through the public link.

## The better path RedJade already has: the previewer

RedJade's own code contains a **`/previewer`** route:

- Runs in **demo mode** (`"preview-only"`): questions render and navigate, but responses
  aren't processed.
- Has a **built-in mobile preview** with device sizes.
- Loads the **full questionnaire** from the authenticated `/api/v1/questionnaires`
  resource (pages, elements, theme, randomization settings, media).
- It needs a **RedJade user login**, which researchers have because they build the surveys.

This gives complete structure (every page and branch, not one walked path), RedJade's
own mobile rendering, and zero risk to live data.

## Still unknown (needs one session with a RedJade login)

1. The exact previewer URL for a given questionnaire, and how a static link's
   `project_id` / `event_id` maps to a `questionnaire_id`.
2. The questionnaire JSON shape (element types, nesting, logic, media URLs).
3. Login method (SSO or password) and session lifetime.
4. Whether the previewer can jump to any page directly, and whether it validates required answers.
5. Whether automating a researcher's own session fits the RedJade contract.
