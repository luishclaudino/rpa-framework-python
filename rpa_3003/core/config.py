"""Configuration management for the RPA framework."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from rpa_3003.core.exceptions import ConfigError


class Config:
    """Manage framework and project configuration values."""

    DEFAULT_CONFIG: dict[str, Any] = {
        "engine": "selenium",
        "browser": "chrome",
        "headless": False,
        "timeout": 10,
        "log_level": "INFO",
        "log_max_bytes": 10_485_760,
        "log_backup_count": 5,
    }

    def __init__(self, config_path: str | None = None) -> None:
        self._config: dict[str, Any] = dict(self.DEFAULT_CONFIG)

        if config_path is not None:
            self.load(config_path)

    def get(self, key: str, default: Any = None) -> Any:
        """Return a configuration value or the provided default."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value

    def save(self, path: str) -> None:
        """Persist the current configuration to a JSON file."""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)

        try:
            with target.open("w", encoding="utf-8") as file_obj:
                json.dump(self._config, file_obj, indent=4, ensure_ascii=False)
        except OSError as exc:
            raise ConfigError(f"Unable to save config to '{target}': {exc}") from exc

    def load(self, path: str) -> None:
        """Load configuration values from a JSON file and merge with defaults."""
        source = Path(path)

        if not source.exists():
            raise ConfigError(f"Config file not found: '{source}'")

        try:
            with source.open("r", encoding="utf-8") as file_obj:
                loaded = json.load(file_obj)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Invalid JSON config in '{source}': {exc}") from exc
        except OSError as exc:
            raise ConfigError(f"Unable to load config from '{source}': {exc}") from exc

        if not isinstance(loaded, dict):
            raise ConfigError("Configuration file must contain a JSON object.")

        merged = dict(self.DEFAULT_CONFIG)
        merged.update(cast(dict[str, Any], loaded))
        self._config = merged