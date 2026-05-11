"""Focused tests for shared JSON utilities."""

import json

import pytest

from rpa_3003.core import FileOperationError
from rpa_3003.utils import (
    dict_to_json,
    json_to_dict,
    merge_json,
    read_json,
    validate_json,
    write_json,
)


def test_write_and_read_json_round_trip(tmp_path) -> None:
    target = tmp_path / "config.json"
    data = {"engine": "playwright", "options": {"headless": True}}

    write_json(str(target), data)

    assert read_json(str(target)) == data


def test_json_string_conversion_round_trip() -> None:
    data = {"browser": "edge", "timeout": 30}

    json_string = dict_to_json(data)

    assert json_to_dict(json_string) == data


def test_merge_json_deep_merges_nested_objects(tmp_path) -> None:
    file1 = tmp_path / "first.json"
    file2 = tmp_path / "second.json"
    output = tmp_path / "merged.json"

    file1.write_text(
        json.dumps({"browser": "chrome", "options": {"headless": False, "timeout": 10}}),
        encoding="utf-8",
    )
    file2.write_text(
        json.dumps({"options": {"timeout": 20}, "engine": "playwright"}),
        encoding="utf-8",
    )

    merged = merge_json(str(file1), str(file2), str(output))

    assert merged == {
        "browser": "chrome",
        "options": {"headless": False, "timeout": 20},
        "engine": "playwright",
    }
    assert read_json(str(output)) == merged


def test_read_json_raises_for_invalid_content(tmp_path) -> None:
    target = tmp_path / "broken.json"
    target.write_text("invalid", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON content"):
        read_json(str(target))


def test_write_json_raises_for_non_serializable_data(tmp_path) -> None:
    target = tmp_path / "broken.json"

    with pytest.raises(ValueError, match="not JSON serializable"):
        write_json(str(target), {"data": {1, 2, 3}})


def test_validate_json_accepts_strings_and_files(tmp_path) -> None:
    target = tmp_path / "valid.json"
    target.write_text(json.dumps({"ok": True}), encoding="utf-8")

    assert validate_json(str(target)) is True
    assert validate_json('{"ok": true}') is True
    assert validate_json("not json") is False


def test_read_json_raises_framework_error_for_missing_file(tmp_path) -> None:
    missing = tmp_path / "missing.json"

    with pytest.raises(FileOperationError, match="Unable to read JSON file"):
        read_json(str(missing))