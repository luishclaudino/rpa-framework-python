"""Focused tests for shared file utilities."""

from pathlib import Path

import pytest

from rpa_3003.core import FileOperationError
from rpa_3003.utils import (
    copy_file,
    create_directory,
    delete_file,
    file_exists,
    get_file_size,
    list_files,
    move_file,
    read_file,
    write_file,
)


def test_create_write_read_and_delete_file(tmp_path) -> None:
    target_dir = tmp_path / "nested" / "logs"
    target_file = target_dir / "output.txt"

    created = create_directory(str(target_dir))
    write_file(str(target_file), "conteudo")

    assert Path(created).exists()
    assert file_exists(str(target_file)) is True
    assert read_file(str(target_file)) == "conteudo"
    assert get_file_size(str(target_file)) == len("conteudo")
    assert delete_file(str(target_file)) is True
    assert delete_file(str(target_file)) is False


def test_copy_and_move_file(tmp_path) -> None:
    source = tmp_path / "source.txt"
    source.write_text("data", encoding="utf-8")

    copied = tmp_path / "copied" / "copy.txt"
    moved = tmp_path / "moved" / "moved.txt"

    assert copy_file(str(source), str(copied)) == str(copied)
    assert copied.read_text(encoding="utf-8") == "data"

    assert move_file(str(copied), str(moved)) == str(moved)
    assert moved.read_text(encoding="utf-8") == "data"
    assert not copied.exists()


def test_list_files_can_filter_by_extension(tmp_path) -> None:
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.csv").write_text("b", encoding="utf-8")
    (tmp_path / "c.txt").write_text("c", encoding="utf-8")

    listed_all = list_files(str(tmp_path))
    listed_txt = list_files(str(tmp_path), ".txt")
    listed_csv = list_files(str(tmp_path), "csv")

    assert [Path(path).name for path in listed_all] == ["a.txt", "b.csv", "c.txt"]
    assert [Path(path).name for path in listed_txt] == ["a.txt", "c.txt"]
    assert [Path(path).name for path in listed_csv] == ["b.csv"]


def test_read_file_raises_framework_error_for_missing_path(tmp_path) -> None:
    missing = tmp_path / "missing.txt"

    with pytest.raises(FileOperationError, match="Unable to read file"):
        read_file(str(missing))