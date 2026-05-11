"""Focused tests for core configuration handling."""

import json

import pytest

from rpa_3003.core import Config, ConfigError


def test_config_uses_defaults_when_no_file_is_provided() -> None:
    config = Config()

    assert config.get("engine") == "selenium"
    assert config.get("browser") == "chrome"
    assert config.get("timeout") == 10
    assert config.get("log_max_bytes") == 10_485_760


def test_config_load_merges_file_values_with_defaults(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps({"engine": "playwright", "headless": True}),
        encoding="utf-8",
    )

    config = Config(str(config_path))

    assert config.get("engine") == "playwright"
    assert config.get("headless") is True
    assert config.get("browser") == "chrome"


def test_config_save_persists_current_values(tmp_path) -> None:
    config = Config()
    config.set("browser", "firefox")

    config_path = tmp_path / "nested" / "config.json"
    config.save(str(config_path))

    saved = json.loads(config_path.read_text(encoding="utf-8"))
    assert saved["browser"] == "firefox"
    assert saved["engine"] == "selenium"


def test_config_raises_for_missing_file(tmp_path) -> None:
    missing_path = tmp_path / "missing.json"

    with pytest.raises(ConfigError, match="Config file not found"):
        Config(str(missing_path))


def test_config_raises_for_invalid_json(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text("not valid json", encoding="utf-8")

    with pytest.raises(ConfigError, match="Invalid JSON config"):
        Config(str(config_path))


def test_config_raises_when_json_root_is_not_an_object(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(["invalid"]), encoding="utf-8")

    with pytest.raises(ConfigError, match="must contain a JSON object"):
        Config(str(config_path))