"""Read Excel/CSV files with Decimal precision preservation."""

from decimal import Decimal
from pathlib import Path
from typing import Any, Optional

import pandas as pd

from scripts.utils.logger import log_audit
from scripts.utils.validator import (
    convert_amount_to_decimal,
    validate_dataframe_structure,
    validate_no_nulls,
)


REQUIRED_COLUMNS = ["Account Code", "Account Name", "Account Type", "Department", "Amount"]


def read_excel_file(
    path: str, sheet_name: Optional[str] = None
) -> pd.DataFrame:
    """Read Excel file, forcing Amount column to string to avoid float contamination."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # Read with string dtype for Amount to prevent float conversion
    df = pd.read_excel(
        path,
        sheet_name=sheet_name or 0,
        dtype={"Amount": str},
        engine="openpyxl",
    )
    return df


def convert_amounts_to_decimal(
    df: pd.DataFrame, amount_columns: Optional[list[str]] = None
) -> tuple[pd.DataFrame, list[str]]:
    """Convert amount columns from string/float to Decimal.

    Returns (modified_df, conversion_issues).
    """
    if amount_columns is None:
        amount_columns = ["Amount"]

    issues: list[str] = []
    result = df.copy()

    for col in amount_columns:
        if col not in result.columns:
            issues.append(f"Column '{col}' not found")
            continue

        converted = []
        for idx, value in result[col].items():
            dec_value = convert_amount_to_decimal(value)
            if dec_value is None and not pd.isna(value):
                issues.append(f"Row {idx}: Cannot convert '{value}' to Decimal in column '{col}'")
            converted.append(dec_value)

        result[col] = converted

    return result, issues


def load_budget(path: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Load and validate budget file.

    Returns (validated_df, metadata).
    """
    df = read_excel_file(path)

    valid, structure_issues = validate_dataframe_structure(df, REQUIRED_COLUMNS)
    if not valid:
        raise ValueError(f"Budget file structure invalid: {structure_issues}")

    df, conversion_issues = convert_amounts_to_decimal(df)

    null_valid, null_issues = validate_no_nulls(df, ["Amount"])

    metadata = {
        "source_file": str(path),
        "row_count": len(df),
        "columns": list(df.columns),
        "conversion_issues": conversion_issues,
        "null_issues": null_issues,
        "has_nulls": not null_valid,
    }

    log_audit("load_budget", [str(path)], {"rows": len(df), "issues": len(conversion_issues)})
    return df, metadata


def load_actuals(path: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Load and validate actuals file. Flags but does not drop NULL amounts."""
    df = read_excel_file(path)

    valid, structure_issues = validate_dataframe_structure(df, REQUIRED_COLUMNS)
    if not valid:
        raise ValueError(f"Actuals file structure invalid: {structure_issues}")

    df, conversion_issues = convert_amounts_to_decimal(df)

    null_valid, null_issues = validate_no_nulls(df, ["Amount"])

    # Flag NULL rows but keep them
    null_rows = df[df["Amount"].isna()].index.tolist()

    metadata = {
        "source_file": str(path),
        "row_count": len(df),
        "columns": list(df.columns),
        "conversion_issues": conversion_issues,
        "null_issues": null_issues,
        "null_row_indices": null_rows,
        "has_nulls": len(null_rows) > 0,
    }

    log_audit(
        "load_actuals",
        [str(path)],
        {"rows": len(df), "nulls": len(null_rows), "issues": len(conversion_issues)},
    )
    return df, metadata


def dataframe_to_records(
    budget_df: pd.DataFrame,
    actuals_df: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Merge budget and actuals DataFrames into calculation-ready records."""
    budget_map: dict[str, dict] = {}
    for _, row in budget_df.iterrows():
        code = str(row["Account Code"])
        budget_map[code] = {
            "account_code": code,
            "account_name": str(row["Account Name"]),
            "department": str(row["Department"]),
            "account_type": str(row["Account Type"]),
            "budget": row["Amount"] if isinstance(row["Amount"], Decimal) else Decimal("0"),
        }

    records: list[dict[str, Any]] = []
    for _, row in actuals_df.iterrows():
        code = str(row["Account Code"])
        actual_amount = row["Amount"]
        if actual_amount is None or (not isinstance(actual_amount, Decimal) and pd.isna(actual_amount)):
            continue  # Skip NULL actuals

        if code in budget_map:
            rec = dict(budget_map[code])
            rec["actual"] = actual_amount if isinstance(actual_amount, Decimal) else Decimal(str(actual_amount))
            records.append(rec)
        else:
            # Actuals-only account
            records.append({
                "account_code": code,
                "account_name": str(row["Account Name"]),
                "department": str(row["Department"]),
                "account_type": str(row["Account Type"]),
                "budget": Decimal("0"),
                "actual": actual_amount if isinstance(actual_amount, Decimal) else Decimal(str(actual_amount)),
            })

    return records
