"""Custom exception hierarchy for the RPA framework."""


class RPAFrameworkError(Exception):
    """Base exception for framework-level errors."""


class BrowserNotFoundError(RPAFrameworkError):
    """Raised when the requested browser is not available or supported."""


class ElementNotFoundError(RPAFrameworkError):
    """Raised when a web element is not found within the timeout."""


class EngineNotSupportedError(RPAFrameworkError):
    """Raised when the automation engine is not supported."""


class ProjectExistsError(RPAFrameworkError):
    """Raised when creating a project that already exists."""


class ProjectNotFoundError(RPAFrameworkError):
    """Raised when a requested project cannot be found."""


class ConfigError(RPAFrameworkError):
    """Raised when configuration loading or validation fails."""


class FileOperationError(RPAFrameworkError):
    """Raised when a file operation fails inside the framework."""