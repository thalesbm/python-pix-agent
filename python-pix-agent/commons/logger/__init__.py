"""
Logger module - Sistema de logging centralizado para o Doc Expert Agent.
"""

from .logger_config import setup_logging, get_logger, set_log_level

__all__ = [
    "setup_logging",
    "get_logger", 
    "set_log_level"
] 