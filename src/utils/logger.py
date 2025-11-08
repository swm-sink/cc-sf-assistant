"""
Logging utility for FP&A Automation Assistant.

Provides structured logging with audit trail compliance.
All transformations log: timestamp, user, source, operation.
"""

import logging
import os
from datetime import datetime, UTC
from typing import Dict, Any, Optional
from pathlib import Path


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO
) -> logging.Logger:
    """
    Configure logger with file and console handlers.

    Args:
        name: Logger name (typically __name__)
        log_file: Optional log file path (defaults to logs/fpa_assistant.log)
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logger(__name__)
        >>> logger.info("Processing started")
    """
    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Default log file
    if log_file is None:
        log_file = str(log_dir / "fpa_assistant.log")

    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # Format: timestamp - module - level - message
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def create_audit_entry(
    operation: str,
    source_files: list[str],
    output_file: Optional[str] = None,
    records_processed: Optional[int] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Create standardized audit trail entry.

    Args:
        operation: Operation name (e.g., 'variance_calculation')
        source_files: List of source file paths
        output_file: Optional output file path
        records_processed: Optional record count
        **kwargs: Additional metadata

    Returns:
        Dict with audit trail fields (timestamp, user, operation, etc.)

    Example:
        >>> entry = create_audit_entry(
        ...     operation='consolidation',
        ...     source_files=['budget.xlsx', 'actuals.xlsx'],
        ...     records_processed=1500
        ... )
    """
    audit_entry = {
        'timestamp': datetime.now(UTC).isoformat(),
        'user': os.getenv('USER', 'unknown'),
        'operation': operation,
        'source_files': source_files,
    }

    if output_file:
        audit_entry['output_file'] = output_file

    if records_processed is not None:
        audit_entry['records_processed'] = records_processed

    # Add any additional metadata
    audit_entry.update(kwargs)

    return audit_entry


# Default logger for module-level imports
default_logger = setup_logger('fpa_assistant')
