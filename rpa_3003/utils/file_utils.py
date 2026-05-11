"""Shared file utilities for RPA projects."""

from __future__ import annotations

import shutil
from pathlib import Path

from rpa_3003.core.exceptions import FileOperationError


def create_directory(path: str) -> str:
    """Create a directory and any missing parent directories."""
    target = Path(path)

    try:
        target.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise FileOperationError(f"Unable to create directory '{target}': {exc}") from exc

    return str(target)


def delete_file(path: str) -> bool:
    """Delete a file if it exists and return whether it was removed."""
    target = Path(path)

    if not target.exists():
        return False

    try:
        target.unlink()
    except OSError as exc:
        raise FileOperationError(f"Unable to delete file '{target}': {exc}") from exc

    return True


def copy_file(src: str, dst: str) -> str:
    """Copy a file and return the destination path."""
    source = Path(src)
    target = Path(dst)
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(source, target)
    except OSError as exc:
        raise FileOperationError(
            f"Unable to copy file from '{source}' to '{target}': {exc}"
        ) from exc

    return str(target)


def move_file(src: str, dst: str) -> str:
    """Move a file and return the destination path."""
    source = Path(src)
    target = Path(dst)
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(source), str(target))
    except OSError as exc:
        raise FileOperationError(
            f"Unable to move file from '{source}' to '{target}': {exc}"
        ) from exc

    return str(target)


def list_files(directory: str, extension: str = "*") -> list[str]:
    """List files in a directory, optionally filtered by extension."""
    base_dir = Path(directory)

    if not base_dir.exists():
        return []

    if extension in {"", "*"}:
        pattern = "*"
    else:
        normalized_extension = extension if extension.startswith(".") else f".{extension}"
        pattern = f"*{normalized_extension}"

    return [str(path) for path in sorted(base_dir.glob(pattern)) if path.is_file()]


def file_exists(path: str) -> bool:
    """Return whether a file exists."""
    return Path(path).exists()


def get_file_size(path: str) -> int:
    """Return the file size in bytes."""
    target = Path(path)

    try:
        return target.stat().st_size
    except OSError as exc:
        raise FileOperationError(f"Unable to read file size for '{target}': {exc}") from exc


def read_file(path: str, encoding: str = "utf-8") -> str:
    """Read a text file and return its content."""
    target = Path(path)

    try:
        return target.read_text(encoding=encoding)
    except OSError as exc:
        raise FileOperationError(f"Unable to read file '{target}': {exc}") from exc


def write_file(path: str, content: str, encoding: str = "utf-8") -> None:
    """Write text content to a file, creating parent directories if needed."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        target.write_text(content, encoding=encoding)
    except OSError as exc:
        raise FileOperationError(f"Unable to write file '{target}': {exc}") from exc