"""Focused tests for shared CSV utilities."""

import pytest

from rpa_3003.core import FileOperationError
from rpa_3003.utils import append_to_csv, filter_csv, read_csv, write_csv


def test_write_and_read_csv_round_trip(tmp_path) -> None:
    target = tmp_path / "rows.csv"
    data = [
        {"name": "alpha", "status": "ok"},
        {"name": "beta", "status": "pending"},
    ]

    write_csv(str(target), data)

    assert read_csv(str(target)) == data


def test_append_to_csv_creates_file_and_preserves_headers(tmp_path) -> None:
    target = tmp_path / "append.csv"

    append_to_csv(str(target), {"name": "alpha", "status": "ok"})
    append_to_csv(str(target), {"name": "beta", "status": "pending"})

    assert read_csv(str(target)) == [
        {"name": "alpha", "status": "ok"},
        {"name": "beta", "status": "pending"},
    ]


def test_filter_csv_returns_exact_column_matches(tmp_path) -> None:
    target = tmp_path / "filter.csv"
    write_csv(
        str(target),
        [
            {"name": "alpha", "status": "ok"},
            {"name": "beta", "status": "pending"},
            {"name": "gamma", "status": "ok"},
        ],
    )

    assert filter_csv(str(target), "status", "ok") == [
        {"name": "alpha", "status": "ok"},
        {"name": "gamma", "status": "ok"},
    ]


def test_read_csv_raises_framework_error_for_missing_file(tmp_path) -> None:
    missing = tmp_path / "missing.csv"

    with pytest.raises(FileOperationError, match="Unable to read CSV file"):
        read_csv(str(missing))