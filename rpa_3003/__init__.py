"""
RPA Framework Coop (rpa_3003)
Framework Python modular e extensível para automação RPA.
"""

__version__ = "1.0.0"
__author__ = "Coop Team"

from rpa_3003.core import Config, RPAFormatter, RPAFrameworkError, RPALogger

__all__ = [
	"Config",
	"RPAFormatter",
	"RPAFrameworkError",
	"RPALogger",
	"__author__",
	"__version__",
]
