"""Shared CSV utilities for RPA projects."""

from __future__ import annotations

import csv
from pathlib import Path

from rpa_3003.core.exceptions import FileOperationError


def read_csv(path: str, delimiter: str = ",", encoding: str = "utf-8") -> list[dict]:
    """Read a CSV file into a list of dictionaries."""
    source = Path(path)

    try:
        with source.open("r", encoding=encoding, newline="") as file_obj:
            reader = csv.DictReader(file_obj, delimiter=delimiter)
            return list(reader)
    except OSError as exc:
        raise FileOperationError(f"Unable to read CSV file '{source}': {exc}") from exc
    except csv.Error as exc:
        raise FileOperationError(f"Invalid CSV content in '{source}': {exc}") from exc


def write_csv(
    path: str,
    data: list[dict],
    headers: list[str] | None = None,
    delimiter: str = ",",
    encoding: str = "utf-8",
) -> None:
    """Write a list of dictionaries to a CSV file."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = headers or _infer_headers(data)
    if not fieldnames:
        target.write_text("", encoding=encoding)
        return

    try:
        with target.open("w", encoding=encoding, newline="") as file_obj:
            writer = csv.DictWriter(file_obj, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)
    except OSError as exc:
        raise FileOperationError(f"Unable to write CSV file '{target}': {exc}") from exc
    except (csv.Error, ValueError) as exc:
        raise FileOperationError(f"Unable to serialize CSV file '{target}': {exc}") from exc


def append_to_csv(path: str, row: dict, encoding: str = "utf-8") -> None:
    """Append a row to a CSV file, creating it with inferred headers if needed."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and target.stat().st_size > 0:
        fieldnames = _read_headers(target, encoding)
        write_header = False
    else:
        fieldnames = list(row.keys())
        write_header = True

    try:
        with target.open("a", encoding=encoding, newline="") as file_obj:
            writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow(row)
    except OSError as exc:
        raise FileOperationError(f"Unable to append to CSV file '{target}': {exc}") from exc
    except (csv.Error, ValueError) as exc:
        raise FileOperationError(f"Unable to append CSV row to '{target}': {exc}") from exc


def filter_csv(path: str, column: str, value: str) -> list[dict]:
    """Return CSV rows whose column value matches exactly."""
    return [row for row in read_csv(path) if row.get(column) == value]


def _infer_headers(data: list[dict]) -> list[str]:
    if not data:
        return []

    headers: list[str] = []
    for row in data:
        for key in row.keys():
            if key not in headers:
                headers.append(key)
    return headers


def _read_headers(path: Path, encoding: str) -> list[str]:
    try:
        with path.open("r", encoding=encoding, newline="") as file_obj:
            reader = csv.reader(file_obj)
            return next(reader)
    except StopIteration:
        return []
    except OSError as exc:
        raise FileOperationError(f"Unable to read CSV headers from '{path}': {exc}") from exc
    except csv.Error as exc:
        raise FileOperationError(f"Invalid CSV header in '{path}': {exc}") from exc