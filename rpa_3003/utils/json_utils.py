"""Shared JSON utilities for RPA projects."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from rpa_3003.core.exceptions import FileOperationError


def read_json(path: str, encoding: str = "utf-8") -> dict | list:
    """Read a JSON file and return its parsed content."""
    source = Path(path)

    try:
        with source.open("r", encoding=encoding) as file_obj:
            return json.load(file_obj)
    except OSError as exc:
        raise FileOperationError(f"Unable to read JSON file '{source}': {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON content in '{source}': {exc}") from exc


def write_json(
    path: str,
    data: dict | list,
    indent: int = 4,
    encoding: str = "utf-8",
) -> None:
    """Write Python data to a JSON file."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        with target.open("w", encoding=encoding) as file_obj:
            json.dump(data, file_obj, indent=indent, ensure_ascii=False)
    except OSError as exc:
        raise FileOperationError(f"Unable to write JSON file '{target}': {exc}") from exc
    except TypeError as exc:
        raise ValueError(f"Data is not JSON serializable: {exc}") from exc


def merge_json(file1: str, file2: str, output: str | None = None) -> dict:
    """Deep-merge two JSON object files and optionally persist the result."""
    data1 = read_json(file1)
    data2 = read_json(file2)

    if not isinstance(data1, dict) or not isinstance(data2, dict):
        raise ValueError("merge_json expects both files to contain JSON objects.")

    merged = _deep_merge_dicts(data1, data2)

    if output is not None:
        write_json(output, merged)

    return merged


def json_to_dict(json_string: str) -> dict | list:
    """Convert a JSON string into Python data."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON string: {exc}") from exc


def dict_to_json(data: dict | list, indent: int = 4) -> str:
    """Convert Python data into a JSON string."""
    try:
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except TypeError as exc:
        raise ValueError(f"Data is not JSON serializable: {exc}") from exc


def validate_json(path_or_string: str) -> bool:
    """Validate whether the input is a JSON file path or JSON string."""
    candidate_path = Path(path_or_string)

    try:
        if candidate_path.exists() and candidate_path.is_file():
            read_json(path_or_string)
        else:
            json_to_dict(path_or_string)
    except (FileOperationError, OSError, ValueError):
        return False

    return True


def _deep_merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = dict(base)

    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge_dicts(merged[key], value)
        else:
            merged[key] = value

    return merged