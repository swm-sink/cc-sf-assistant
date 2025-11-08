"""
File handling utilities for FP&A Automation Assistant.

Provides safe file operations with validation.
"""

from pathlib import Path
from typing import List, Optional
from datetime import datetime


class FileValidationError(Exception):
    """Raised when file validation fails."""
    pass


def discover_excel_files(folder_path: str) -> List[Path]:
    """
    Discover all Excel files in folder.

    Args:
        folder_path: Path to folder containing Excel files

    Returns:
        Sorted list of Path objects for .xlsx and .xls files

    Raises:
        FileNotFoundError: If folder doesn't exist
        FileValidationError: If folder is not a directory

    Example:
        >>> files = discover_excel_files('data/input')
        >>> for file in files:
        ...     print(file.name)
    """
    path = Path(folder_path)

    if not path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not path.is_dir():
        raise FileValidationError(f"Not a directory: {folder_path}")

    # Find all Excel files
    xlsx_files = list(path.glob("*.xlsx"))
    xls_files = list(path.glob("*.xls"))

    excel_files = xlsx_files + xls_files

    # Return in deterministic order
    return sorted(excel_files)


def validate_file_exists(file_path: str) -> Path:
    """
    Validate that file exists and is readable.

    Args:
        file_path: Path to file

    Returns:
        Path object if valid

    Raises:
        FileNotFoundError: If file doesn't exist
        FileValidationError: If path is not a file

    Example:
        >>> path = validate_file_exists('data/budget.xlsx')
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise FileValidationError(f"Not a file: {file_path}")

    return path


def ensure_output_directory(file_path: str) -> Path:
    """
    Ensure output directory exists, create if needed.

    Args:
        file_path: Path to output file

    Returns:
        Path object for file

    Example:
        >>> output_path = ensure_output_directory('data/output/report.xlsx')
    """
    path = Path(file_path)

    # Create parent directory if doesn't exist
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    return path


def generate_timestamped_filename(
    base_name: str,
    extension: str,
    output_dir: Optional[str] = None
) -> str:
    """
    Generate filename with timestamp.

    Args:
        base_name: Base filename (without extension)
        extension: File extension (with or without dot)
        output_dir: Optional output directory path

    Returns:
        Full path with timestamped filename

    Example:
        >>> filename = generate_timestamped_filename(
        ...     'variance_analysis',
        ...     '.xlsx',
        ...     'data/output'
        ... )
        >>> # Returns: 'data/output/variance_analysis_2025-11-08_143022.xlsx'
    """
    # Normalize extension
    if not extension.startswith('.'):
        extension = '.' + extension

    # Generate timestamp: YYYY-MM-DD_HHMMSS
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')

    # Create filename
    filename = f"{base_name}_{timestamp}{extension}"

    # Add directory if specified
    if output_dir:
        path = Path(output_dir) / filename
        return str(path)

    return filename


def safe_file_copy(source: str, destination: str, backup: bool = True) -> None:
    """
    Safely copy file with optional backup.

    Args:
        source: Source file path
        destination: Destination file path
        backup: If True and destination exists, create .bak backup

    Raises:
        FileNotFoundError: If source doesn't exist

    Example:
        >>> safe_file_copy('template.xlsx', 'output.xlsx', backup=True)
    """
    import shutil

    source_path = validate_file_exists(source)
    dest_path = Path(destination)

    # Backup existing file if requested
    if backup and dest_path.exists():
        backup_path = dest_path.with_suffix(dest_path.suffix + '.bak')
        shutil.copy2(dest_path, backup_path)

    # Copy file
    ensure_output_directory(destination)
    shutil.copy2(source_path, dest_path)
