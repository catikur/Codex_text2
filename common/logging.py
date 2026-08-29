"""Structured logging setup."""
from __future__ import annotations

import logging
import sys
from typing import Optional


def configure_logging(level: str = "INFO", service_name: Optional[str] = None) -> None:
    """Configure application-wide logging."""

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(level.upper())
    if not root.handlers:
        root.addHandler(handler)
    for handler in root.handlers:
        handler.setFormatter(formatter)
    if service_name:
        logging.getLogger(service_name)


def get_logger(name: str) -> logging.Logger:
    """Return logger for module."""

    return logging.getLogger(name)
