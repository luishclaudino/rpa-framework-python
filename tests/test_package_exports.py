"""Import smoke tests for package export surfaces."""

from rpa_3003 import Config, RPAFormatter, RPAFrameworkError, RPALogger
from rpa_3003.utils import append_to_csv, read_csv, write_csv


def test_root_package_exports_core_types() -> None:
    assert Config is not None
    assert RPAFormatter is not None
    assert RPAFrameworkError is not None
    assert RPALogger is not None


def test_utils_package_exports_csv_helpers() -> None:
    assert append_to_csv is not None
    assert read_csv is not None
    assert write_csv is not None