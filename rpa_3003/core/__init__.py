"""
Core — Logger, Config e Exceptions.
"""

from rpa_3003.core.config import Config
from rpa_3003.core.exceptions import (
	BrowserNotFoundError,
	ConfigError,
	ElementNotFoundError,
	EngineNotSupportedError,
	FileOperationError,
	ProjectExistsError,
	ProjectNotFoundError,
	RPAFrameworkError,
)
from rpa_3003.core.logger import RPAFormatter, RPALogger

__all__ = [
	"BrowserNotFoundError",
	"Config",
	"ConfigError",
	"ElementNotFoundError",
	"EngineNotSupportedError",
	"FileOperationError",
	"ProjectExistsError",
	"ProjectNotFoundError",
	"RPAFormatter",
	"RPAFrameworkError",
	"RPALogger",
]
