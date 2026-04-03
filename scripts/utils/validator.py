"""Data validation and reconciliation utilities."""

from decimal import Decimal, InvalidOperation
from typing import Any, Optional

import pandas as pd


def validate_dataframe_structure(
    df: pd.DataFrame, required_columns: list[str]
) -> tuple[bool, list[str]]:
    """Check that all required columns exist in the DataFrame."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        return False, [f"Missing column: {col}" for col in missing]
    return True, []


def validate_decimal_column(
    df: pd.DataFrame, column: str
) -> tuple[bool, list[str]]:
    """Ensure column values are convertible to Decimal. Returns issues per row."""
    issues: list[str] = []
    if column not in df.columns:
        return False, [f"Column '{column}' not found"]

    for idx, value in df[column].items():
        if pd.isna(value):
            continue  # NULLs handled separately by validate_no_nulls
        try:
            Decimal(str(value))
        except (InvalidOperation, ValueError):
            issues.append(f"Row {idx}: cannot convert '{value}' to Decimal")

    return len(issues) == 0, issues


def validate_no_nulls(
    df: pd.DataFrame, columns: list[str]
) -> tuple[bool, list[str]]:
    """Check for NULL/NaN values. Flags but never drops data."""
    issues: list[str] = []
    for col in columns:
        if col not in df.columns:
            issues.append(f"Column '{col}' not found")
            continue
        null_mask = df[col].isna()
        null_indices = df.index[null_mask].tolist()
        if null_indices:
            issues.append(f"Column '{col}' has NULL values at rows: {null_indices}")
    return len(issues) == 0, issues


def convert_amount_to_decimal(value: Any) -> Optional[Decimal]:
    """Safely convert a value to Decimal. Returns None for unconvertible values."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        # Convert via string to avoid float precision contamination
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def reconcile_datasets(
    budget_df: pd.DataFrame,
    actuals_df: pd.DataFrame,
    key_column: str,
) -> dict[str, Any]:
    """Reconcile two datasets by key column. Returns match report."""
    budget_keys = set(budget_df[key_column].astype(str))
    actuals_keys = set(actuals_df[key_column].astype(str))

    matched = budget_keys & actuals_keys
    budget_only = budget_keys - actuals_keys
    actuals_only = actuals_keys - budget_keys

    return {
        "matched": sorted(matched),
        "budget_only": sorted(budget_only),
        "actuals_only": sorted(actuals_only),
        "match_count": len(matched),
        "budget_only_count": len(budget_only),
        "actuals_only_count": len(actuals_only),
        "fully_matched": len(budget_only) == 0 and len(actuals_only) == 0,
    }
