from __future__ import annotations

import logging
import os
from typing import Any, Dict

import structlog


def _get_processor_chain() -> list:
    return [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.JSONRenderer(),
    ]


def configure_logging(level: str | int | None = None) -> None:
    log_level = (
        level
        if level is not None
        else os.getenv("LOG_LEVEL", "INFO")
    )

    logging.basicConfig(format="%(message)s", level=getattr(logging, str(log_level).upper(), logging.INFO))

    structlog.configure(
        processors=_get_processor_chain(),
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, str(log_level).upper(), logging.INFO)),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
