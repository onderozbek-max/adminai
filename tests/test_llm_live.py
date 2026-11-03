"""Talks to the real Wibey. Opt in with SURVEYCOACH_LIVE=1; CI never runs this."""
import os

import pytest
from pydantic import BaseModel

from surveycoach.llm import WibeyProvider

pytestmark = [pytest.mark.live, pytest.mark.skipif(os.environ.get("SURVEYCOACH_LIVE") != "1", reason="set SURVEYCOACH_LIVE=1")]


class Echo(BaseModel):
    word_with_underscore: str
    sum: int


def test_real_wibey_round_trips_a_schema_and_keeps_underscores():
    got = WibeyProvider().complete_json(
        "Return the word 'snake_case' in word_with_underscore and the sum of the numbers in the data in sum.",
        "numbers: 2 and 5", Echo)
    assert got.word_with_underscore == "snake_case" and got.sum == 7
