"""
Data validation for financial files.

Validates Excel file structure, data types, and required columns.
Ensures data integrity before processing.
"""

from decimal import Decimal
from pathlib import Path
from typing import List, Tuple, Dict, Any
import pandas as pd

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DataValidationError(Exception):
    """Raised when data validation fails."""
    pass


def validate_department_file(
    file_path: Path,
    required_columns: List[str]
) -> Tuple[bool, List[str]]:
    """
    Validate department file structure and data integrity.

    Args:
        file_path: Path to Excel file
        required_columns: List of column names that must be present

    Returns:
        Tuple of (is_valid, list_of_issues)

    Raises:
        FileNotFoundError: If file doesn't exist
        DataValidationError: If file cannot be read

    Example:
        >>> is_valid, issues = validate_department_file(
        ...     Path('sales.xlsx'),
        ...     ['account_code', 'account_name', 'amount']
        ... )
        >>> if not is_valid:
        ...     print(f"Validation failed: {issues}")
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    issues = []

    try:
        # Load Excel file
        df = pd.read_excel(file_path, engine='openpyxl')

        logger.info(
            f"Loaded file for validation: {file_path.name}",
            extra={'rows': len(df), 'columns': len(df.columns)}
        )

        # Check 1: Required columns present
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            issues.append(
                f"Missing required columns: {', '.join(missing_columns)}"
            )

        # Check 2: Duplicate column names
        duplicate_columns = df.columns[df.columns.duplicated()].tolist()
        if duplicate_columns:
            issues.append(
                f"Duplicate column names: {', '.join(duplicate_columns)}"
            )

        # Check 3: Completely empty columns
        empty_columns = [col for col in df.columns if df[col].isna().all()]
        if empty_columns:
            issues.append(
                f"Completely empty columns: {', '.join(empty_columns)}"
            )

        # Check 4: Data type validation for amount columns
        amount_columns = [col for col in df.columns if 'amount' in col.lower()]
        for col in amount_columns:
            if col in df.columns:
                # Check if column is numeric type (pandas dtype)
                non_numeric = df[col][~pd.to_numeric(df[col], errors='coerce').notna()]
                if not non_numeric.empty:
                    issues.append(
                        f"Non-numeric values in amount column '{col}': "
                        f"{len(non_numeric)} rows"
                    )

        # Check 5: File has data (not just headers)
        if len(df) == 0:
            issues.append("File contains no data rows (only headers)")

        is_valid = len(issues) == 0

        if is_valid:
            logger.info(f"Validation passed: {file_path.name}")
        else:
            logger.warning(
                f"Validation failed: {file_path.name}",
                extra={'issues': issues}
            )

        return is_valid, issues

    except Exception as e:
        raise DataValidationError(
            f"Failed to validate {file_path}: {e}"
        ) from e


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: List[str],
    file_name: str = "Unknown"
) -> List[str]:
    """
    Validate that DataFrame has all required columns.

    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        file_name: Optional filename for error messages

    Returns:
        List of validation issues (empty if valid)

    Example:
        >>> df = pd.DataFrame({'account': [1, 2], 'amount': [100, 200]})
        >>> issues = validate_required_columns(
        ...     df,
        ...     ['account', 'amount', 'date'],
        ...     'budget.xlsx'
        ... )
        >>> # Returns: ["Missing required columns: date"]
    """
    issues = []

    missing = set(required_columns) - set(df.columns)
    if missing:
        issues.append(
            f"[{file_name}] Missing required columns: {', '.join(missing)}"
        )

    return issues


def validate_numeric_column(
    df: pd.DataFrame,
    column_name: str,
    allow_null: bool = True
) -> List[str]:
    """
    Validate that column contains only numeric values.

    Args:
        df: DataFrame to validate
        column_name: Column to check
        allow_null: Whether NULL/NaN values are permitted

    Returns:
        List of validation issues (empty if valid)

    Example:
        >>> df = pd.DataFrame({'amount': [100, 200, 'invalid']})
        >>> issues = validate_numeric_column(df, 'amount', allow_null=False)
    """
    issues = []

    if column_name not in df.columns:
        issues.append(f"Column '{column_name}' not found")
        return issues

    col = df[column_name]

    # Check for non-numeric values using pandas numeric conversion
    numeric_values = pd.to_numeric(col, errors='coerce')

    if not allow_null:
        # Must be all numeric (no NaN allowed)
        non_numeric = col[~numeric_values.notna()]
    else:
        # Numeric or NaN allowed
        # Only flag values that are neither numeric nor null
        non_numeric = col[(~numeric_values.notna()) & col.notna()]

    if not non_numeric.empty:
        issues.append(
            f"Column '{column_name}' contains {len(non_numeric)} "
            f"non-numeric values"
        )

    return issues


def validate_date_column(
    df: pd.DataFrame,
    column_name: str
) -> List[str]:
    """
    Validate that column contains valid dates.

    Args:
        df: DataFrame to validate
        column_name: Column to check

    Returns:
        List of validation issues (empty if valid)

    Example:
        >>> df = pd.DataFrame({'date': ['2025-01-01', 'invalid']})
        >>> issues = validate_date_column(df, 'date')
    """
    issues = []

    if column_name not in df.columns:
        issues.append(f"Column '{column_name}' not found")
        return issues

    col = df[column_name]

    # Try parsing as dates
    try:
        parsed = pd.to_datetime(col, errors='coerce')
        invalid_dates = parsed.isna() & col.notna()

        if invalid_dates.any():
            issues.append(
                f"Column '{column_name}' contains {invalid_dates.sum()} "
                f"invalid date values"
            )
    except Exception as e:
        issues.append(f"Failed to parse column '{column_name}' as dates: {e}")

    return issues
