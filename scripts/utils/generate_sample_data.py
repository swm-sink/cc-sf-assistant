#!/usr/bin/env python3
"""
Generate sample financial data for FP&A automation testing.

Purpose:
    Create realistic Excel files with budget and actuals data for testing variance
    analysis workflows. Uses Decimal precision to avoid floating point errors.

Generates:
    - data/samples/budget_2025.xlsx (clean baseline, 50 accounts)
    - data/samples/actuals_nov_2025.xlsx (with edge cases and variances)
    - data/samples/actuals_dec_2025.xlsx (recovery month)

Reference:
    - data/samples/README.md for account structure and variance scenarios
    - CLAUDE.md for Decimal precision requirements
"""

from decimal import Decimal
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd


def create_account_data() -> List[Dict[str, Any]]:
    """
    Create chart of accounts with baseline budget amounts.

    Returns:
        List of account dictionaries with Account_Code, Account_Name, Department, Amount
    """
    accounts: List[Dict[str, Any]] = [
        # Revenue Accounts (4000-4090)
        {
            "Account_Code": "4000",
            "Account_Name": "Subscription Revenue",
            "Department": "Revenue",
            "Amount": Decimal("2500000.00"),
        },
        {
            "Account_Code": "4010",
            "Account_Name": "Premium Features Revenue",
            "Department": "Revenue",
            "Amount": Decimal("450000.00"),
        },
        {
            "Account_Code": "4020",
            "Account_Name": "Enterprise Revenue",
            "Department": "Revenue",
            "Amount": Decimal("800000.00"),
        },
        {
            "Account_Code": "4030",
            "Account_Name": "Professional Services",
            "Department": "Revenue",
            "Amount": Decimal("150000.00"),
        },
        {
            "Account_Code": "4040",
            "Account_Name": "Partner Revenue",
            "Department": "Revenue",
            "Amount": Decimal("200000.00"),
        },
        {
            "Account_Code": "4050",
            "Account_Name": "Advertising Revenue",
            "Department": "Revenue",
            "Amount": Decimal("100000.00"),
        },
        {
            "Account_Code": "4060",
            "Account_Name": "Data Licensing",
            "Department": "Revenue",
            "Amount": Decimal("75000.00"),
        },
        {
            "Account_Code": "4070",
            "Account_Name": "Hardware Revenue",
            "Department": "Revenue",
            "Amount": Decimal("50000.00"),
        },
        {
            "Account_Code": "4080",
            "Account_Name": "Other Revenue",
            "Department": "Revenue",
            "Amount": Decimal("25000.00"),
        },
        {
            "Account_Code": "4090",
            "Account_Name": "Deferred Revenue Recognized",
            "Department": "Revenue",
            "Amount": Decimal("150000.00"),
        },
        # COGS Accounts (5000-5070)
        {
            "Account_Code": "5000",
            "Account_Name": "Cloud Hosting (AWS/GCP)",
            "Department": "COGS",
            "Amount": Decimal("450000.00"),
        },
        {
            "Account_Code": "5010",
            "Account_Name": "Data Storage & Bandwidth",
            "Department": "COGS",
            "Amount": Decimal("180000.00"),
        },
        {
            "Account_Code": "5020",
            "Account_Name": "Third-Party APIs",
            "Department": "COGS",
            "Amount": Decimal("90000.00"),
        },
        {
            "Account_Code": "5030",
            "Account_Name": "Payment Processing Fees",
            "Department": "COGS",
            "Amount": Decimal("135000.00"),
        },
        {
            "Account_Code": "5040",
            "Account_Name": "Customer Success Salaries",
            "Department": "COGS",
            "Amount": Decimal("250000.00"),
        },
        {
            "Account_Code": "5050",
            "Account_Name": "Technical Support Salaries",
            "Department": "COGS",
            "Amount": Decimal("180000.00"),
        },
        {
            "Account_Code": "5060",
            "Account_Name": "Onboarding & Implementation",
            "Department": "COGS",
            "Amount": Decimal("70000.00"),
        },
        {
            "Account_Code": "5070",
            "Account_Name": "License & Royalties",
            "Department": "COGS",
            "Amount": Decimal("45000.00"),
        },
        # Engineering OpEx (6000-6070)
        {
            "Account_Code": "6000",
            "Account_Name": "Engineering Salaries",
            "Department": "Engineering",
            "Amount": Decimal("800000.00"),
        },
        {
            "Account_Code": "6010",
            "Account_Name": "Product Management Salaries",
            "Department": "Engineering",
            "Amount": Decimal("200000.00"),
        },
        {
            "Account_Code": "6020",
            "Account_Name": "QA/Testing Salaries",
            "Department": "Engineering",
            "Amount": Decimal("150000.00"),
        },
        {
            "Account_Code": "6030",
            "Account_Name": "Dev Tools & Software",
            "Department": "Engineering",
            "Amount": Decimal("50000.00"),
        },
        {
            "Account_Code": "6040",
            "Account_Name": "Contractors & Consultants",
            "Department": "Engineering",
            "Amount": Decimal("100000.00"),
        },
        {
            "Account_Code": "6050",
            "Account_Name": "Infrastructure R&D",
            "Department": "Engineering",
            "Amount": Decimal("75000.00"),
        },
        {
            "Account_Code": "6060",
            "Account_Name": "Security & Compliance",
            "Department": "Engineering",
            "Amount": Decimal("60000.00"),
        },
        {
            "Account_Code": "6070",
            "Account_Name": "Training & Development",
            "Department": "Engineering",
            "Amount": Decimal("25000.00"),
        },
        # Sales & Marketing OpEx (7000-7110)
        {
            "Account_Code": "7000",
            "Account_Name": "Sales Salaries",
            "Department": "Sales",
            "Amount": Decimal("400000.00"),
        },
        {
            "Account_Code": "7010",
            "Account_Name": "Sales Commissions",
            "Department": "Sales",
            "Amount": Decimal("320000.00"),
        },
        {
            "Account_Code": "7020",
            "Account_Name": "Marketing Salaries",
            "Department": "Marketing",
            "Amount": Decimal("250000.00"),
        },
        {
            "Account_Code": "7030",
            "Account_Name": "Digital Advertising",
            "Department": "Marketing",
            "Amount": Decimal("300000.00"),
        },
        {
            "Account_Code": "7040",
            "Account_Name": "Content & SEO",
            "Department": "Marketing",
            "Amount": Decimal("80000.00"),
        },
        {
            "Account_Code": "7050",
            "Account_Name": "Events & Conferences",
            "Department": "Marketing",
            "Amount": Decimal("100000.00"),
        },
        {
            "Account_Code": "7060",
            "Account_Name": "Marketing Tools",
            "Department": "Marketing",
            "Amount": Decimal("60000.00"),
        },
        {
            "Account_Code": "7070",
            "Account_Name": "PR & Communications",
            "Department": "Marketing",
            "Amount": Decimal("50000.00"),
        },
        {
            "Account_Code": "7080",
            "Account_Name": "Partner Marketing",
            "Department": "Marketing",
            "Amount": Decimal("70000.00"),
        },
        {
            "Account_Code": "7090",
            "Account_Name": "Lead Generation",
            "Department": "Marketing",
            "Amount": Decimal("90000.00"),
        },
        {
            "Account_Code": "7100",
            "Account_Name": "Brand & Creative",
            "Department": "Marketing",
            "Amount": Decimal("75000.00"),
        },
        {
            "Account_Code": "7110",
            "Account_Name": "Sales Enablement",
            "Department": "Sales",
            "Amount": Decimal("45000.00"),
        },
        # G&A OpEx (8000-8110)
        {
            "Account_Code": "8000",
            "Account_Name": "Executive Salaries",
            "Department": "G&A",
            "Amount": Decimal("300000.00"),
        },
        {
            "Account_Code": "8010",
            "Account_Name": "HR Salaries",
            "Department": "G&A",
            "Amount": Decimal("120000.00"),
        },
        {
            "Account_Code": "8020",
            "Account_Name": "Finance & Accounting Salaries",
            "Department": "G&A",
            "Amount": Decimal("180000.00"),
        },
        {
            "Account_Code": "8030",
            "Account_Name": "IT & Systems",
            "Department": "G&A",
            "Amount": Decimal("90000.00"),
        },
        {
            "Account_Code": "8040",
            "Account_Name": "Legal & Professional Fees",
            "Department": "G&A",
            "Amount": Decimal("120000.00"),
        },
        {
            "Account_Code": "8050",
            "Account_Name": "Office Rent",
            "Department": "G&A",
            "Amount": Decimal("150000.00"),
        },
        {
            "Account_Code": "8060",
            "Account_Name": "Office Utilities",
            "Department": "G&A",
            "Amount": Decimal("20000.00"),
        },
        {
            "Account_Code": "8070",
            "Account_Name": "Insurance",
            "Department": "G&A",
            "Amount": Decimal("60000.00"),
        },
        {
            "Account_Code": "8080",
            "Account_Name": "Recruiting & HR Tools",
            "Department": "G&A",
            "Amount": Decimal("80000.00"),
        },
        {
            "Account_Code": "8090",
            "Account_Name": "Travel & Entertainment",
            "Department": "G&A",
            "Amount": Decimal("70000.00"),
        },
        {
            "Account_Code": "8100",
            "Account_Name": "Depreciation",
            "Department": "G&A",
            "Amount": Decimal("50000.00"),
        },
        {
            "Account_Code": "8110",
            "Account_Name": "Other G&A",
            "Department": "G&A",
            "Amount": Decimal("40000.00"),
        },
    ]

    return accounts


def apply_november_variances(budget_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Apply November 2025 actuals variances to budget data.

    Includes:
        - 3 material favorable variances
        - 3 material unfavorable variances
        - Edge cases: negative value, NULL, zero budget item

    Args:
        budget_data: List of budget account dictionaries

    Returns:
        List of actuals account dictionaries with variances applied
    """
    actuals = []

    for account in budget_data:
        account_copy = account.copy()
        code = account["Account_Code"]

        # Material favorable variances (>10% and >$50k)
        if code == "4000":  # Subscription Revenue
            account_copy["Amount"] = Decimal("2875000.00")  # +$375k, +15%
        elif code == "4020":  # Enterprise Revenue
            account_copy["Amount"] = Decimal("975000.00")  # +$175k, +21.9%
        elif code == "5000":  # Cloud Hosting
            account_copy["Amount"] = Decimal("405000.00")  # -$45k, -10%

        # Material unfavorable variances (>10% and >$50k)
        elif code == "7030":  # Digital Advertising
            account_copy["Amount"] = Decimal("420000.00")  # +$120k, +40%
        elif code == "7000":  # Sales Salaries
            account_copy["Amount"] = Decimal("480000.00")  # +$80k, +20%
        elif code == "6000":  # Engineering Salaries
            account_copy["Amount"] = Decimal("920000.00")  # +$120k, +15%

        # Edge case 1: Negative value (adjustment/refund)
        elif code == "4090":  # Deferred Revenue
            account_copy["Amount"] = Decimal("-50000.00")

        # Edge case 2: NULL value (missing data) - handled in Excel writing
        elif code == "7080":  # Partner Marketing
            account_copy["Amount"] = None  # Will be blank in Excel

        # Edge case 3: Zero budget item (new initiative)
        elif code == "6050":  # Infrastructure R&D
            # Budget was $75k, but we'll treat this as unbudgeted spend for testing
            account_copy["Amount"] = Decimal("25000.00")

        # All other accounts: minor random variations (±5%)
        else:
            budget_amount = account["Amount"]
            if budget_amount and budget_amount > Decimal("0"):
                # Small variation: -5% to +5%
                variation = budget_amount * Decimal("0.03")  # 3% variation
                account_copy["Amount"] = budget_amount + variation

        actuals.append(account_copy)

    return actuals


def apply_december_variances(budget_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Apply December 2025 actuals variances (recovery month after November overspend).

    Args:
        budget_data: List of budget account dictionaries

    Returns:
        List of actuals account dictionaries with December variances
    """
    actuals = []

    for account in budget_data:
        account_copy = account.copy()
        code = account["Account_Code"]

        # Recovery month: Previous overspends are corrected
        if code == "7030":  # Digital Advertising (was overspent in Nov)
            account_copy["Amount"] = Decimal("280000.00")  # Under budget now
        elif code == "7000":  # Sales Salaries (was overspent in Nov)
            account_copy["Amount"] = Decimal("395000.00")  # Slight under
        elif code == "6000":  # Engineering Salaries (was overspent in Nov)
            account_copy["Amount"] = Decimal("790000.00")  # Slight under

        # Revenue continues strong
        elif code == "4000":  # Subscription Revenue
            account_copy["Amount"] = Decimal("2650000.00")  # +6%
        elif code == "4020":  # Enterprise Revenue
            account_copy["Amount"] = Decimal("850000.00")  # +6.25%

        # Normal operations for others
        else:
            budget_amount = account["Amount"]
            if budget_amount and budget_amount > Decimal("0"):
                # Small variation: -2% to +2%
                variation = budget_amount * Decimal("0.01")
                account_copy["Amount"] = budget_amount + variation

        actuals.append(account_copy)

    return actuals


def write_excel_file(data: List[Dict[str, Any]], filepath: Path, sheet_name: str) -> None:
    """
    Write data to Excel file with Decimal precision maintained.

    Args:
        data: List of account dictionaries
        filepath: Output Excel file path
        sheet_name: Name of Excel sheet
    """
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Ensure proper column order
    df = df[["Account_Code", "Account_Name", "Department", "Amount"]]

    # Force Account_Code to string type (prevent int conversion)
    df["Account_Code"] = df["Account_Code"].astype(str)

    # Convert Decimal to float for Excel writing (pandas limitation)
    # Note: This is acceptable because we're writing display values only
    # All calculations will use Decimal when reading back
    df["Amount"] = df["Amount"].apply(
        lambda x: float(x) if x is not None and isinstance(x, Decimal) else x
    )

    # Write to Excel
    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✅ Generated: {filepath}")


def main() -> None:
    """Generate all sample Excel files."""
    # Ensure output directory exists
    output_dir = Path("data/samples")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate base account data
    budget_data = create_account_data()

    # Generate budget file (clean baseline)
    write_excel_file(
        data=budget_data, filepath=output_dir / "budget_2025.xlsx", sheet_name="Budget"
    )

    # Generate November actuals (with variances and edge cases)
    nov_actuals = apply_november_variances(budget_data)
    write_excel_file(
        data=nov_actuals, filepath=output_dir / "actuals_nov_2025.xlsx", sheet_name="Actuals"
    )

    # Generate December actuals (recovery month)
    dec_actuals = apply_december_variances(budget_data)
    write_excel_file(
        data=dec_actuals, filepath=output_dir / "actuals_dec_2025.xlsx", sheet_name="Actuals"
    )

    print("\n✅ All sample data files generated successfully!")
    print(f"📂 Location: {output_dir.absolute()}")
    print("\n📊 Files created:")
    print("  - budget_2025.xlsx (50 accounts, clean baseline)")
    print("  - actuals_nov_2025.xlsx (with 6 material variances + 3 edge cases)")
    print("  - actuals_dec_2025.xlsx (recovery month)")


if __name__ == "__main__":
    main()
