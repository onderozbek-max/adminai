import re
from pathlib import Path

import pytest
import yaml

from surveycoach.rubric import Rubric, RubricError, load_rubric

MARKDOWN = Path(__file__).parent.parent / "docs/rubric/mmc-survey-rubric-v2.md"
ROW = re.compile(r"^\| (\d+\.\d+) \|.*\| (\d+) \| \[([^\]]+)\] \|\s*$")
BLOCKER = re.compile(r"^\| (B\d) \|")


def raw_rubric() -> dict:
    return yaml.safe_load((Path(__file__).parent.parent / "surveycoach/data/rubric-v2.yaml").read_text())


def test_loads_with_expected_shape():
    rubric = load_rubric()
    assert len(rubric.dimensions) == 10
    assert len(rubric.criteria) == 46
    assert len(rubric.blockers) == 7
    assert rubric.active_points == 100


def test_inactive_criteria_are_worth_zero():
    rubric = load_rubric()
    assert {c.id for c in rubric.criteria if not c.active} == {"10.2", "10.4", "10.5"}


def test_yaml_matches_the_approved_markdown():
    rows = [m.groups() for line in MARKDOWN.read_text().splitlines() if (m := ROW.match(line))]
    expected = {rid: (int(points), check) for rid, points, check in rows}
    rubric = load_rubric()
    assert {c.id: (c.points, c.check) for c in rubric.criteria} == expected
    blockers = [m.group(1) for line in MARKDOWN.read_text().splitlines() if (m := BLOCKER.match(line))]
    assert [b.id for b in rubric.blockers] == blockers


def test_fails_when_active_points_do_not_sum_to_100():
    data = raw_rubric()
    data["criteria"][0]["points"] += 1
    with pytest.raises(RubricError, match="100"):
        Rubric.model_validate(data)


def test_fails_when_a_dimension_total_mismatches():
    data = raw_rubric()
    data["criteria"][0]["points"] -= 1   # D1 loses a point
    data["criteria"][4]["points"] += 1   # D2 gains it: the grand total stays 100
    with pytest.raises(RubricError, match="dimension"):
        Rubric.model_validate(data)


def test_fails_on_duplicate_ids():
    data = raw_rubric()
    data["criteria"][1]["id"] = data["criteria"][0]["id"]
    with pytest.raises(RubricError, match="duplicate"):
        Rubric.model_validate(data)


def test_fails_on_unknown_dimension():
    data = raw_rubric()
    data["criteria"][0]["dimension"] = "D99"
    with pytest.raises(RubricError, match="unknown dimension"):
        Rubric.model_validate(data)
