"""Logging setup for SmartVault.

Provides a configured logger with a rotating file handler and colored
console output.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import colorlog


def setup_logger(name: str, config: dict) -> logging.Logger:
    """Create and configure a logger.

    Args:
        name: Name of the logger (typically __name__).
        config: Configuration dictionary from config.yaml.

    Returns:
        Configured :class:`logging.Logger` instance.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        # already configured
        return logger

    level = getattr(logging, config.get("log_level", "INFO"))
    logger.setLevel(level)

    log_dir = Path(config.get("log_dir", "logs"))
    log_dir.mkdir(parents=True, exist_ok=True)
    file_path = log_dir / "smartvault.log"

    fh = RotatingFileHandler(
        file_path,
        maxBytes=config.get("log_max_bytes", 5_242_880),
        backupCount=config.get("log_backup_count", 3),
    )
    fh.setLevel(level)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setLevel(level)
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s"
    )
    sh.setFormatter(color_formatter)
    logger.addHandler(sh)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Convenience function retrieving a logger.

    Args:
        name: Name for the logger.

    Returns:
        A configured logger (using default config if not provided).
    """
    # to avoid circular imports use a minimal default
    default_config = {"log_level": "INFO", "log_max_bytes": 5_242_880, "log_backup_count": 3, "log_dir": "logs"}
    return setup_logger(name, default_config)
