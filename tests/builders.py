"""Small builders so each test states only what it cares about."""
from surveycoach.checks.registry import ReviewContext
from surveycoach.rubric import load_rubric
from surveycoach.snapshot import Media, Option, Page, Question, Scale, SurveySnapshot

INTRO_TEXT = "Thanks for helping shape our products! This takes about 5 minutes and you'll earn points."


def question(qid="q1", text="Which flavor do you like best?", kind="single_choice",
             options=("Vanilla", "Chocolate", "Mint"), required=True, **extra) -> Question:
    opts = [Option(id=f"{qid}-o{i}", label=label) for i, label in enumerate(options)]
    return Question(id=qid, text=text, kind=kind, options=opts, required=required, **extra)


def page(position: int, *questions: Question, kind="question", text="", intro_text="", links_out=()) -> Page:
    return Page(id=f"p{position}", position=position, kind=kind, questions=list(questions),
                text=text, intro_text=intro_text, links_out=list(links_out))


def intro(text: str = INTRO_TEXT) -> Page:
    return page(0, kind="intro", intro_text=text)


def thank_you(text="Thanks! Your feedback will help shape Member's Mark products.", position=99) -> Page:
    return page(position, kind="thank_you", text=text)


def survey(*pages: Page, survey_type="non_ihut_product", title="Help pick our next flavor") -> SurveySnapshot:
    return SurveySnapshot(title=title, survey_type=survey_type, pages=list(pages))


def one_question_survey(q: Question, with_intro=True) -> SurveySnapshot:
    pages = ([intro()] if with_intro else []) + [page(1, q), thank_you()]
    return survey(*pages)


def context(snapshot: SurveySnapshot) -> ReviewContext:
    return ReviewContext.build(snapshot, load_rubric())


def image(natural=(1200, 1200), rendered=(349, 349), **extra) -> Media:
    return Media(natural_w=natural[0], natural_h=natural[1], rendered_w=rendered[0],
                 rendered_h=rendered[1], bytes=extra.pop("bytes", 120_000), alt=extra.pop("alt", "A product"), **extra)


def scale(points=5, low="Not at all", high="Extremely", labels=()) -> Scale:
    return Scale(points=points, low_label=low, high_label=high, labels=list(labels))
