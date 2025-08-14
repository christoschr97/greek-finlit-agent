"""
Financial Literacy Agent Core Package

This package contains the core components of the financial literacy agent.
"""

from .config.settings import get_config, AVAILABLE_MODELS

# Conditional import to avoid dependency issues during testing
try:
    from .agent.core import FinancialAgent
    __all__ = ["FinancialAgent", "get_config", "AVAILABLE_MODELS"]
except ImportError:
    __all__ = ["get_config", "AVAILABLE_MODELS"]
