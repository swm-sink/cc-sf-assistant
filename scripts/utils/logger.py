"""Audit trail logging using loguru."""

import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional

from loguru import logger

from scripts.utils.types import AuditEntry

_logger_configured = False


def setup_logger(log_dir: str = "logs/") -> "logger":
    """Configure loguru with file rotation and JSON format."""
    global _logger_configured
    if _logger_configured:
        return logger

    os.makedirs(log_dir, exist_ok=True)

    logger.remove()

    # Console: human-readable
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
        level="INFO",
    )

    # File: JSON for machine parsing, rotated daily
    logger.add(
        os.path.join(log_dir, "fpa_audit_{time:YYYY-MM-DD}.log"),
        format="{time:YYYY-MM-DDTHH:mm:ss.SSSZ} | {level} | {message} | {extra}",
        rotation="1 day",
        retention="30 days",
        level="DEBUG",
        serialize=True,
    )

    _logger_configured = True
    return logger


def log_audit(
    operation: str,
    source_files: list[str],
    details: Optional[dict[str, Any]] = None,
    user: Optional[str] = None,
) -> AuditEntry:
    """Create a structured audit trail entry and log it."""
    entry = AuditEntry(
        timestamp=datetime.now(timezone.utc),
        user=user or os.environ.get("USER", "system"),
        operation=operation,
        source_files=source_files,
        details=details or {},
    )

    logger.bind(
        audit=True,
        operation=entry.operation,
        user=entry.user,
        source_files=entry.source_files,
        details=entry.details,
    ).info(f"AUDIT: {entry.operation}")

    return entry
