# Plan 1: Review Engine Implementation Plan

> **For agentic workers:** use subagent-driven-development or executing-plans. Steps use
> checkboxes. TDD: failing test, see it fail, minimal code, see it pass, commit.

**Goal:** `python -m surveycoach review fixtures/boxer-briefs.json` prints a scored,
rubric-cited review of a survey snapshot, with no network, browser, or AI.

**Architecture:** A reader-independent `SurveySnapshot` (Pydantic) goes through pure
deterministic checks registered by rubric ID. Each check returns a `CheckResult`
(a score *fraction* 0..1 plus findings). The rubric YAML is the single source of truth
for points; scoring is a plain weighted sum over active criteria totaling exactly 100.

**Tech Stack:** Python 3.14 (`.venv` via uv), Pydantic v2, PyYAML, Pillow, pytest.

## Global Constraints

- Rubric v2 (`docs/rubric/mmc-survey-rubric-v2.md`) is authoritative: 10 dimensions,
  46 criteria, 7 blockers, active points sum to exactly 100. Inactive: 10.2, 10.4, 10.5 (0 pts).
- Rubric points live only in `surveycoach/data/rubric-v2.yaml`. Checks return fractions.
- Readiness: any open blocker or score < 60 = needs_work; 60-79 = almost_ready; 80+ = ready.
- Unchecked criteria (AI-only, not built yet) are reported as `unchecked`; the score is
  then flagged `provisional` and gives them full credit (never silently penalizes).
- Findings are plain English, member-first, no emojis in code, files, or output.
- Files stay under 600 lines. DRY, YAGNI. Survey text is untrusted data.
- Python install: `uv pip install --python .venv/bin/python --index-url
  https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple
  --allow-insecure-host pypi.ci.artifacts.walmart.com <pkg>`.

## File Structure

```
pyproject.toml
surveycoach/__init__.py  __main__.py  cli.py
surveycoach/snapshot.py      # SurveySnapshot, Page, Question, Option, Media, Scale; content_hash
surveycoach/rubric.py        # Rubric model, load_rubric(), validation
surveycoach/data/rubric-v2.yaml
surveycoach/findings.py      # Finding, CheckResult, Severity, fingerprint
surveycoach/scoring.py       # score(), readiness, strengths
surveycoach/timing.py        # estimate_minutes(), fatigue zones, promised-minutes parser
surveycoach/checks/__init__.py   # registry: @check("2.1"), run_all()
surveycoach/checks/structure.py  # B3 B4 B5 1.4 2.1 2.2 2.4 8.2 8.6
surveycoach/checks/answers.py    # 4.2 4.4 5.4
surveycoach/checks/phone.py      # 6.1 6.2 6.3 6.4 6.5
surveycoach/checks/content.py    # 3.2 3.3 9.1(emoji) 9.2 plus helpers
surveycoach/checks/images.py     # 7.2 7.3 7.5 7.6 B7
surveycoach/review.py        # run_review(snapshot, rubric) -> Review
fixtures/boxer-briefs.json   # realistic sample survey with deliberate problems
tests/...                    # one test module per source module
```

## Tasks

### Task 1: Scaffold
Create `pyproject.toml` (package `surveycoach`, deps pydantic pyyaml pillow, dev pytest),
package files, `tests/test_smoke.py` asserting import. Install deps. Commit.

### Task 2: Snapshot model
**Produces:** `SurveySnapshot(title, source_url, survey_type, pages)`, `Page(id, position, kind, questions, links_out)`,
`Question(id, label, text, help_text, kind, required, options, rows, scale, media, conditional, options_below_fold, fits_one_screen)`,
`Option(id, label, media, is_other_with_text, is_exclusive)`, `Media(...)`, `Scale(points, low_label, high_label, labels)`,
`SurveySnapshot.content_hash` (sha256 over canonical text, options sorted), `intro_text`, `all_questions()`.
Tests: round trip JSON; hash stable when option order changes; hash changes when text changes.

### Task 3: Rubric data and loader
`rubric-v2.yaml` transcribes every criterion and blocker. `load_rubric()` fails on:
active points != 100, dimension total mismatch, duplicate IDs, unknown dimension.
Test also parses the approved markdown and asserts IDs, points, and active flags match the YAML (G-17).

### Task 4: Findings, scoring, readiness
`CheckResult(criterion_id, fraction | None, findings)`; `score(rubric, results) -> ScoreCard(score, provisional, unchecked_points, by_dimension, open_blockers, readiness, strengths)`.
Tests: all full = 100; inactive contribute 0; open blocker forces needs_work even at 95; 79.9 vs 80 boundary; kept-on-purpose blockers not open.

### Task 5: Timing model
`estimate(snapshot) -> Timing(total_seconds, per_page, fatigue_zone_per_page)`; `parse_promised_minutes(text)`.
Constants in one dataclass. Tests: reading speed, per-kind costs, grid per row, promised minutes parser ("about 5 minutes", "10-12 minutes", "under 3 minutes").

### Task 6: Check registry and structure checks
`@check("B4")` registry; `run_all(ctx)`. Structure checks per rubric: B3 late screen-out (screen-out page after > 120 s cumulative or lacking thanks), B4 no intro, B5 broken time promise (> 50% and > 3 min over), 1.4 time and reward stated, 2.1 length bands per survey type (1 / 0.6 / 0), 2.2 screeners within first 3 pages, 2.4 at most 2 required open text, 8.2 format variety, 8.6 optional open "anything else".

### Task 7: Answer checks
4.2 overlapping numeric ranges, 4.4 scale labeled both ends/balanced/direction, 5.4 more than 3 consecutive agree/disagree scales.

### Task 8: Phone checks
6.1 text <= 25 words and options fit above fold, 6.2 choice <= 60 chars, > 8 choices flagged, dropdown with <= 7, 6.3 grid <= 5x5 and scales <= 7, 6.4 desktop words and drag ranking, 6.5 outbound links.

### Task 9: Content checks
3.2 reading grade (Flesch-Kincaid <= 8) plus jargon list, 3.3 select-one/all-that-apply instruction on choice questions, 9.1 emoji limit (max one, intro only), 9.2 content standards (sentence case, ALL CAPS, repeated ellipses, unnamed first person, banned terms respondents/customers/participants).

### Task 10: Image checks
7.2 worst-image aspect ratio (1 / 1/3 / 0), 7.3 width < 750 or upscaled or stretched, 7.5 option image consistency and count, 7.6 per-image 500 KB and total 5 MB and alt text, B7 missing or broken media. Pillow helper `analyze_image(path)` for dimensions, alpha, blur score.

### Task 11: Pipeline, fixture, CLI
`run_review(snapshot, rubric) -> Review`; `fixtures/boxer-briefs.json`; `python -m surveycoach review <file>` prints readiness, score (provisional flag), must-fix, worth-improving, strengths, minutes. CLI test via subprocess.

### Task 12: Wrap up
Update roadmap, save a memory note, commit.
