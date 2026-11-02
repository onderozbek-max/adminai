# Spike R1b: RedJade previewer and mobile rendering (findings, 2026-11-02)

**Method:** Onder signed into RedJade himself in a SurveyCoach-controlled Chrome window
(dedicated profile, git-ignored). SurveyCoach never handled the password. All actions
were read-only: page loads and the PREVIEW button. Raw captures are in `spikes/r1b/`
(git-ignored: they contain internal survey content).

## Hypothesis: SurveyCoach can read a full survey and its phone rendering through the previewer

**Confirmed** on Sensory_ChocolateCoveredCashews_October2026 (project 299615, event 500801).

| Finding | Evidence |
|---|---|
| PREVIEW opens `/previewer/questionnaire` in a new tab | Recorded navigation |
| The previewer loads `GET /api/v1/survey_previewer/servings?event_id=<id>` and then `GET /api/v1/questionnaires/<id>` for each questionnaire | Network log |
| **Preview saves nothing**: 14 API calls while stepping through 5 pages, **0 non-GET calls** | Network log |
| Phone emulation (iPhone 16, 393 x 852, DPR 3, touch, iOS user agent) gives RedJade's true mobile layout | Screenshots: full-width answer buttons, Lato question text, sticky pill Next button |
| Demo mode **auto-selects a random answer** on each page, so Next always works | Screenshots |
| Captured screens match the definition one-to-one (page 4 = "Overall Liking") | Screenshot vs. JSON |
| RedJade scrolls **inside an inner container**, not the document | `document.scrollHeight` always equals the viewport; a visible inner scrollbar. "Fits on one screen" (6.1) must measure the inner scroller. |

## Questionnaire definition shape

```
questionnaire: id, title, questionnaire_type (single_sample | single_non_sample | ...),
               enhanced_mode, is_launched, approved, locales, media_tier
  data.config: question_font_size, response_font_size, question_spacing, disable_previous_button
  data.theme_overrides.elements: header, responses, stars, line_scales, buttons, tables...
  data.page_groups[]: id, name
    pages[]: id, index, config, triggers[], validations[], errors[]
      questions[]: id, cid, question_type, display_name, text{locale: html},
                   answers[] {id, text{locale}, value, config.media}, config,
                   triggers[] {type, condition: any|all, parent_cid, answers[]}, validations[]
```

- Cashews has 2 questionnaires: "Intro - Local Panel" (1 page) and "Dark Chocolate Covered
  Cashews Acceptance" (17 pages: 14 `radio`, 2 `text`, 2 `page_text`).
- Branching is explicit: a "Below Expectations" open-ended question is shown when specific
  answers to its parent are chosen.
- Question text is HTML per locale (for example `<b>APPEARANCE</b>`).
- A survey link's public `event_meta` returns the `event_id`, which is what the previewer is keyed on.

## Access: Onder's doubt was right

- Onder's account has broad permissions (`view_questionnaires`, `manage_projects`, ...),
  but **projects are shared individually**. `GET /api/v1/projects/300489` (Cakeballs)
  returned **404** for his account.
- The login is RedJade username and password (`company_saml_subdomain: null`), not Walmart SSO.
- **Not proven:** whether the previewer API serves an unshared event. Two indirect probes
  were inconclusive (the previewer needs state set by the dashboard). We stopped there
  rather than probe RedJade internals further. The 404 on the project strongly
  suggests sharing is enforced.
- Not tested: an unlaunched draft. Cashews is launched.

## Implication for "anyone can test SurveyCoach"

Any login, personal or service, only sees projects shared with it. Options:

1. **SurveyCoach service account plus a sharing step:** the researcher adds the
   SurveyCoach account in the project's SHARING dialog once (like sharing a doc with a
   colleague). Then anyone, with or without RedJade, can review it in SurveyCoach.
2. **SurveyCoach service account with company-wide visibility** (if RedJade offers such
   a role): no sharing step. Needs a RedJade admin decision.
3. In both cases, people who **view** a review (a manager, a designer) never need RedJade.
   Only the first read of a survey needs access.
