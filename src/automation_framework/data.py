"""Small, typed helpers for data-driven tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    """Read JSON and add the source path to decoding errors."""

    source = Path(path)
    try:
        with source.open(encoding="utf-8") as data_file:
            return json.load(data_file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {source}: {error.msg}") from error


def load_cases(path: str | Path, key: str) -> list[dict[str, Any]]:
    """Load a named list of test cases from a JSON object."""

    payload = load_json(path)
    if not isinstance(payload, dict) or not isinstance(payload.get(key), list):
        raise ValueError(f"Expected '{key}' to be a list in {Path(path)}")
    cases = payload[key]
    if not all(isinstance(case, dict) for case in cases):
        raise ValueError(f"Every '{key}' entry in {Path(path)} must be an object")
    return cases
