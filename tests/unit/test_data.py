"""Tests for explicit errors in data-driven test inputs."""

from pathlib import Path

import pytest

from automation_framework.data import load_cases, load_json


@pytest.mark.unit
def test_load_cases_returns_named_case_list(tmp_path: Path) -> None:
    source = tmp_path / "cases.json"
    source.write_text('{"invalid": [{"id": "one"}]}', encoding="utf-8")

    assert load_cases(source, "invalid") == [{"id": "one"}]


@pytest.mark.unit
def test_load_json_explains_invalid_input(tmp_path: Path) -> None:
    source = tmp_path / "broken.json"
    source.write_text("{not-json", encoding="utf-8")

    with pytest.raises(ValueError, match=r"Invalid JSON in .*broken.json"):
        load_json(source)


@pytest.mark.unit
@pytest.mark.parametrize("payload", ['{"cases": {}}', '{"cases": ["wrong"]}'])
def test_load_cases_requires_a_list_of_objects(tmp_path: Path, payload: str) -> None:
    source = tmp_path / "cases.json"
    source.write_text(payload, encoding="utf-8")

    with pytest.raises(ValueError, match="cases"):
        load_cases(source, "cases")
