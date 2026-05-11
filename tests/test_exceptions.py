"""Focused tests for the core exception hierarchy."""

from rpa_3003.core import (
    BrowserNotFoundError,
    ConfigError,
    ElementNotFoundError,
    EngineNotSupportedError,
    FileOperationError,
    ProjectExistsError,
    ProjectNotFoundError,
    RPAFrameworkError,
)


def test_all_framework_exceptions_inherit_from_base_exception() -> None:
    exception_types = [
        BrowserNotFoundError,
        ConfigError,
        ElementNotFoundError,
        EngineNotSupportedError,
        FileOperationError,
        ProjectExistsError,
        ProjectNotFoundError,
    ]

    for exception_type in exception_types:
        assert issubclass(exception_type, RPAFrameworkError)