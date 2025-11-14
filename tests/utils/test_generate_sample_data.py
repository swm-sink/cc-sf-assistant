"""
Tests for sample data generation script.

Purpose:
    Validate that generated Excel files have correct structure, Decimal precision,
    edge cases, and variance scenarios per data/samples/README.md specification.
"""

from decimal import Decimal
from pathlib import Path

import pandas as pd


def test_budget_file_exists() -> None:
    """Test that budget_2025.xlsx file was generated."""
    budget_file = Path("data/samples/budget_2025.xlsx")
    assert budget_file.exists(), "budget_2025.xlsx should exist"


def test_actuals_nov_file_exists() -> None:
    """Test that actuals_nov_2025.xlsx file was generated."""
    actuals_file = Path("data/samples/actuals_nov_2025.xlsx")
    assert actuals_file.exists(), "actuals_nov_2025.xlsx should exist"


def test_actuals_dec_file_exists() -> None:
    """Test that actuals_dec_2025.xlsx file was generated."""
    actuals_file = Path("data/samples/actuals_dec_2025.xlsx")
    assert actuals_file.exists(), "actuals_dec_2025.xlsx should exist"


def test_budget_has_correct_structure() -> None:
    """Test that budget file has required columns and 50 accounts."""
    budget = pd.read_excel("data/samples/budget_2025.xlsx", sheet_name="Budget")

    # Check columns
    expected_columns = ["Account_Code", "Account_Name", "Department", "Amount"]
    assert list(budget.columns) == expected_columns

    # Check row count (50 accounts per spec)
    assert len(budget) == 50, f"Expected 50 accounts, got {len(budget)}"


def test_actuals_nov_has_correct_structure() -> None:
    """Test that November actuals file has required columns and 50 accounts."""
    actuals = pd.read_excel("data/samples/actuals_nov_2025.xlsx", sheet_name="Actuals")

    # Check columns
    expected_columns = ["Account_Code", "Account_Name", "Department", "Amount"]
    assert list(actuals.columns) == expected_columns

    # Check row count
    assert len(actuals) == 50, f"Expected 50 accounts, got {len(actuals)}"


def test_account_codes_match_spec() -> None:
    """Test that account codes follow spec pattern (4000-4090, 5000-5070, etc)."""
    budget = pd.read_excel(
        "data/samples/budget_2025.xlsx", sheet_name="Budget", dtype={"Account_Code": str}
    )

    # Revenue accounts should be 4000-4090
    revenue_accounts = budget[budget["Department"] == "Revenue"]["Account_Code"]
    assert all(code.startswith("4") for code in revenue_accounts)

    # COGS accounts should be 5000-5070
    cogs_accounts = budget[budget["Department"] == "COGS"]["Account_Code"]
    assert all(code.startswith("5") for code in cogs_accounts)

    # Engineering accounts should be 6000-6070
    eng_accounts = budget[budget["Department"] == "Engineering"]["Account_Code"]
    assert all(code.startswith("6") for code in eng_accounts)


def test_november_has_material_favorable_variances() -> None:
    """Test that November actuals include material favorable variances."""
    budget = pd.read_excel(
        "data/samples/budget_2025.xlsx", sheet_name="Budget", dtype={"Account_Code": str}
    )
    actuals = pd.read_excel(
        "data/samples/actuals_nov_2025.xlsx", sheet_name="Actuals", dtype={"Account_Code": str}
    )

    # Merge on Account_Code
    merged = budget.merge(actuals, on="Account_Code", suffixes=("_budget", "_actual"))

    # Check Account 4000 - Subscription Revenue (+15% favorable)
    sub_rev = merged[merged["Account_Code"] == "4000"].iloc[0]
    assert sub_rev["Amount_actual"] > sub_rev["Amount_budget"]
    variance_pct = (
        (sub_rev["Amount_actual"] - sub_rev["Amount_budget"]) / sub_rev["Amount_budget"]
    ) * 100
    assert variance_pct > 10, f"Expected >10% variance, got {variance_pct:.2f}%"

    # Check Account 4020 - Enterprise Revenue (+21.9% favorable)
    ent_rev = merged[merged["Account_Code"] == "4020"].iloc[0]
    assert ent_rev["Amount_actual"] > ent_rev["Amount_budget"]
    variance_pct = (
        (ent_rev["Amount_actual"] - ent_rev["Amount_budget"]) / ent_rev["Amount_budget"]
    ) * 100
    assert variance_pct > 10, f"Expected >10% variance, got {variance_pct:.2f}%"


def test_november_has_material_unfavorable_variances() -> None:
    """Test that November actuals include material unfavorable variances."""
    budget = pd.read_excel(
        "data/samples/budget_2025.xlsx", sheet_name="Budget", dtype={"Account_Code": str}
    )
    actuals = pd.read_excel(
        "data/samples/actuals_nov_2025.xlsx", sheet_name="Actuals", dtype={"Account_Code": str}
    )

    merged = budget.merge(actuals, on="Account_Code", suffixes=("_budget", "_actual"))

    # Check Account 7030 - Digital Advertising (+40% unfavorable)
    digital_ad = merged[merged["Account_Code"] == "7030"].iloc[0]
    assert digital_ad["Amount_actual"] > digital_ad["Amount_budget"]
    variance_pct = (
        (digital_ad["Amount_actual"] - digital_ad["Amount_budget"]) / digital_ad["Amount_budget"]
    ) * 100
    assert variance_pct > 10, f"Expected >10% variance, got {variance_pct:.2f}%"


def test_november_has_negative_value_edge_case() -> None:
    """Test that November actuals include negative value edge case (Account 4090)."""
    actuals = pd.read_excel(
        "data/samples/actuals_nov_2025.xlsx", sheet_name="Actuals", dtype={"Account_Code": str}
    )

    # Account 4090 - Deferred Revenue should be negative
    deferred_rev = actuals[actuals["Account_Code"] == "4090"]
    assert len(deferred_rev) > 0, "Account 4090 should exist"
    assert deferred_rev["Amount"].iloc[0] < 0, "Account 4090 should be negative"


def test_november_has_null_value_edge_case() -> None:
    """Test that November actuals include NULL value edge case (Account 7080)."""
    actuals = pd.read_excel(
        "data/samples/actuals_nov_2025.xlsx", sheet_name="Actuals", dtype={"Account_Code": str}
    )

    # Account 7080 - Partner Marketing should be NULL/NaN
    partner_mkt = actuals[actuals["Account_Code"] == "7080"]
    assert len(partner_mkt) > 0, "Account 7080 should exist"
    assert pd.isna(partner_mkt["Amount"].iloc[0]), "Account 7080 should be NULL"


def test_decimal_precision_maintained() -> None:
    """Test that amounts have proper decimal precision (2 places)."""
    budget = pd.read_excel("data/samples/budget_2025.xlsx", sheet_name="Budget")

    # Check that amounts are reasonable (not float errors like 2500000.0000001)
    for amount in budget["Amount"].dropna():
        # Convert to Decimal and check precision
        amount_dec = Decimal(str(amount))
        # All amounts should have 2 decimal places or be whole numbers
        assert abs(amount_dec - round(amount_dec, 2)) < Decimal("0.001")


def test_all_files_load_without_errors() -> None:
    """Test that all generated files can be loaded by pandas without errors."""
    files = [
        ("data/samples/budget_2025.xlsx", "Budget"),
        ("data/samples/actuals_nov_2025.xlsx", "Actuals"),
        ("data/samples/actuals_dec_2025.xlsx", "Actuals"),
    ]

    for filepath, sheet_name in files:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        assert df is not None
        assert len(df) > 0
        assert "Amount" in df.columns
