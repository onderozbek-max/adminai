"""After grounding, the AI's findings are de-duplicated across criteria and batches: one problem, one rewrite per text."""
from surveycoach.findings import CheckResult, Finding, RewriteOption
from surveycoach.judge.dedupe import dedupe
from surveycoach.rubric import load_rubric

RUBRIC = load_rubric()
LOUD = "How much did you LOVE the fit?"


def finding(cid, headline="h", question_id="q4", evidence="LOVE the fit", current=LOUD, options=("Neutral rewrite",), **kw):
    return Finding(criterion_id=cid, severity="must_fix" if cid.startswith("B") else "worth_improving", headline=headline,
                   evidence=evidence, explanation="x", member_impact="m", question_id=question_id, page_id="p4",
                   current_text=current, suggested_text=options[0] if options else None,
                   options=[RewriteOption(label="Neutral", text=t) for t in options], source="ai", **kw)


def results(*findings, fraction=0.5):
    out: dict[str, CheckResult] = {}
    for f in findings:
        mine = out.setdefault(f.criterion_id, CheckResult(criterion_id=f.criterion_id, fraction=None if f.criterion_id.startswith("B") else fraction))
        mine.findings.append(f)
    return out


def kept(out, cid):
    return out[cid].findings


def test_a_finding_that_repeats_a_blocker_on_the_same_question_and_quote_is_dropped_once():
    out, notes = dedupe(results(finding("B1"), finding("5.1")), RUBRIC)
    assert len(kept(out, "B1")) == 1 and kept(out, "5.1") == []
    assert notes == ["5.1: repeats B1 on q4"]


def test_the_criterion_keeps_its_points_decision_when_its_finding_is_dropped_as_a_repeat():
    out, _ = dedupe(results(finding("B1"), finding("5.1"), fraction=0.5), RUBRIC)
    assert out["5.1"].fraction == 0.5                      # the blocker is the visible reason, so the verdict stands


def test_different_questions_or_different_quotes_are_not_repeats():
    other_question = finding("5.1", question_id="q5", current="Where do you usually shop?")
    other_quote = finding("5.2", evidence="something else", current="Another stem entirely")
    out, notes = dedupe(results(finding("B1"), other_question, other_quote), RUBRIC)
    assert kept(out, "5.1") and kept(out, "5.2") and notes == []


def test_two_findings_rewriting_the_same_text_keep_only_the_first_rewrite_but_both_stay_as_problems():
    intro = "Welcome to the Boxer Briefs Survey!"
    a = finding("1.2", question_id=None, evidence=intro, current=intro, options=("Intro rewrite A",))
    b = finding("1.3", question_id=None, evidence=intro, current=intro, options=("Intro rewrite B",))
    c = finding("8.3", question_id=None, evidence=intro, current=intro, options=("Intro rewrite C",))
    out, notes = dedupe(results(c, b, a), RUBRIC)           # fed in a scrambled order: rubric order decides, not arrival
    assert kept(out, "1.2")[0].suggested_text == "Intro rewrite A"
    for cid in ("1.3", "8.3"):
        loser = kept(out, cid)[0]
        assert loser.suggested_text is None and loser.options == [] and loser.current_text is None and loser.structural is False
        assert loser.headline == "h" and loser.explanation == "x"       # the problem and advice survive, only the rewrite goes
    assert notes == ["1.3: its rewrite of this text was dropped, 1.2 already rewrites it",
                     "8.3: its rewrite of this text was dropped, 1.2 already rewrites it"]


def test_findings_without_rewrites_never_claim_a_text():
    a = finding("1.2", options=(), current=None)
    b = finding("1.3", options=("Real rewrite",), current=LOUD)
    out, notes = dedupe(results(a, b), RUBRIC)
    assert kept(out, "1.3")[0].suggested_text == "Real rewrite" and notes == []


def test_blockers_are_judged_before_criteria_so_the_blocker_always_wins_a_shared_text():
    out, _ = dedupe(results(finding("5.1", options=("criterion rewrite",)), finding("B1", evidence="x", options=("blocker rewrite",))), RUBRIC)
    assert kept(out, "B1")[0].suggested_text == "blocker rewrite" and kept(out, "5.1")[0].suggested_text is None


def test_nothing_is_dropped_when_nothing_repeats():
    original = results(finding("5.1"), finding("4.3", question_id="q6", evidence="Which of these", current="Which of these matter?"))
    out, notes = dedupe(original, RUBRIC)
    assert notes == [] and {c: len(r.findings) for c, r in out.items()} == {"5.1": 1, "4.3": 1}
