from surveycoach.checks.registry import clip


def test_short_text_is_untouched():
    assert clip("Which flavor?", 90) == "Which flavor?"


def test_long_text_is_cut_at_a_word_boundary_with_an_ellipsis():
    text = "Please indicate your level of agreement with each of the following statements about the aforementioned boxer briefs."
    clipped = clip(text, 90)
    assert clipped.endswith("...")
    assert len(clipped) <= 93
    assert clipped[:-3] in text and not clipped[:-3].endswith(" ")
    assert text[len(clipped[:-3])] == " "          # cut landed on a space, never mid-word


def test_one_giant_word_still_gets_clipped():
    assert clip("x" * 200, 50) == "x" * 50 + "..."
