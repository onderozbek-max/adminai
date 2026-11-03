from builders import context, intro, one_question_survey, page, question, survey, thank_you

from surveycoach.checks import content
from surveycoach.checks.text import has_emoji, reading_grade, title_case_signature


def run(fn, snapshot):
    return fn(context(snapshot))


def single(q):
    return one_question_survey(q)


# helpers
def test_reading_grade_orders_simple_below_dense():
    simple = reading_grade("Which flavor do you like best?")
    dense = reading_grade("Please indicate the extent to which you concur with the aforementioned characteristics.")
    assert simple < 6 < 12 < dense


def test_has_emoji():
    assert has_emoji("Happy Halloween \U0001F383")
    assert not has_emoji("Happy Halloween")


def test_title_case_signature_needs_a_capitalized_function_word():
    assert title_case_signature("How Do You Make Coffee At Home?")
    assert title_case_signature("Which Coffee Products Do You Buy Most Often?")
    assert not title_case_signature("What do you think of Member's Mark Boxer Briefs?")
    assert not title_case_signature("How do you make coffee at home?")
    assert not title_case_signature("Thanks. You helped. Now tell us more.")   # capitals after a full stop are fine


# 3.2 plain words
def test_3_2_flags_jargon_and_dense_sentences():
    jargon = question(text="Rate the organoleptic viscosity of this sample.")
    assert run(content.plain_words, single(jargon)).fraction < 1.0
    dense = question(text="Please indicate the extent to which you concur with the aforementioned characteristics of the product.")
    assert run(content.plain_words, single(dense)).fraction < 1.0


def test_3_2_passes_plain_language():
    assert run(content.plain_words, single(question())).fraction == 1.0


# 3.3 instructions
def test_3_3_multi_select_must_say_all_that_apply():
    bad = question(kind="multi_choice", text="Which flavors do you like?")
    good = question(kind="multi_choice", text="Which flavors do you like? Select all that apply.")
    assert run(content.clear_instructions, single(bad)).fraction == 0.0
    assert run(content.clear_instructions, single(good)).fraction == 1.0
    helped = question(kind="multi_choice", text="Which flavors?", help_text="Choose all that apply")
    assert run(content.clear_instructions, single(helped)).fraction == 1.0


# 9.1 emoji (rule only: tone stays with the AI judge, so the criterion stays unchecked)
def test_9_1_emoji_in_questions_and_options_are_flagged_without_scoring():
    q = question(text="What did you buy candy for? \U0001F36B", options=("Trick-or-treaters \U0001F383", "Me"))
    result = run(content.emoji_rule, single(q))
    assert result.fraction is None
    assert len(result.findings) == 2


def test_9_1_allows_one_emoji_in_the_intro_only():
    snapshot = single(question())
    snapshot.pages[0].intro_text = "Happy Halloween \U0001F383 This takes about 5 minutes."
    assert run(content.emoji_rule, snapshot).findings == []
    snapshot.pages[0].intro_text = "Hi \U0001F383\U0001F383 This takes about 5 minutes."
    assert len(run(content.emoji_rule, snapshot).findings) == 1


# 9.2 content standards
def test_9_2_flags_title_case_all_caps_and_banned_words():
    q = question(text="What Do You ACTUALLY reach for?")
    snapshot = single(q)
    result = run(content.content_standards, snapshot)
    explanations = " ".join(f.explanation for f in result.findings).lower()
    assert "sentence case" in explanations
    assert "capital" in explanations


def test_9_2_flags_respondents_but_not_customer_service():
    bad = question(text="How satisfied were respondents with the package?")
    ok = question(text="How was our customer service?")
    assert run(content.content_standards, single(bad)).findings
    assert run(content.content_standards, single(ok)).findings == []


def test_9_2_flags_unnamed_narrator_and_heavy_punctuation():
    q = question(text="Personally, I always pick the red one!! Do you?")
    assert len(run(content.content_standards, single(q)).findings) >= 2


def test_9_2_flags_mixed_answer_case():
    q = question(options=("Very Satisfied", "somewhat satisfied", "Not satisfied"))
    assert run(content.content_standards, single(q)).findings


def test_9_2_banding_by_issue_count():
    clean = run(content.content_standards, single(question()))
    assert clean.fraction == 1.0
    issues = lambda n: survey(intro(), *[page(i + 1, question(f"q{i}", "How Do You Make Coffee At Home?")) for i in range(n)],
                              thank_you())
    assert run(content.content_standards, issues(3)).fraction == 0.5
    assert run(content.content_standards, issues(6)).fraction == 0.0


def test_9_2_numeric_answers_do_not_count_as_lowercase():
    q = question(options=("Under 1 year", "1 to 5 years", "5 to 10 years", "Over 10 years"))
    assert run(content.content_standards, single(q)).findings == []


def test_9_2_catches_four_letter_shouting_but_not_known_acronyms():
    assert run(content.content_standards, single(question(text="How much did you LOVE the fit?"))).findings
    assert run(content.content_standards, single(question(text="Did you take part in an IHUT test?"))).findings == []
