"""Generate realistic sample data for FP&A testing."""

import os
from decimal import Decimal
from pathlib import Path

import openpyxl


# 50 accounts with realistic monthly amounts
CHART_OF_ACCOUNTS = [
    # Revenue (4xxx)
    {"code": "4000", "name": "Product Revenue", "type": "revenue", "dept": "Sales", "budget": "850000"},
    {"code": "4010", "name": "Service Revenue", "type": "revenue", "dept": "Sales", "budget": "320000"},
    {"code": "4020", "name": "Subscription Revenue", "type": "revenue", "dept": "Sales", "budget": "480000"},
    {"code": "4030", "name": "Licensing Revenue", "type": "revenue", "dept": "Sales", "budget": "150000"},
    {"code": "4090", "name": "Other Revenue", "type": "revenue", "dept": "Sales", "budget": "-5000"},  # Negative edge case
    # COGS (5xxx)
    {"code": "5000", "name": "Direct Materials", "type": "cogs", "dept": "Engineering", "budget": "210000"},
    {"code": "5010", "name": "Direct Labor", "type": "cogs", "dept": "Engineering", "budget": "180000"},
    {"code": "5020", "name": "Manufacturing Overhead", "type": "cogs", "dept": "Engineering", "budget": "95000"},
    {"code": "5030", "name": "Hosting & Infrastructure", "type": "cogs", "dept": "Engineering", "budget": "125000"},
    {"code": "5070", "name": "Other COGS", "type": "cogs", "dept": "Engineering", "budget": "35000"},
    # Engineering OpEx (6xxx)
    {"code": "6000", "name": "Engineering Salaries", "type": "expense", "dept": "Engineering", "budget": "420000"},
    {"code": "6010", "name": "Engineering Benefits", "type": "expense", "dept": "Engineering", "budget": "105000"},
    {"code": "6020", "name": "Software Licenses", "type": "expense", "dept": "Engineering", "budget": "45000"},
    {"code": "6030", "name": "Cloud Computing", "type": "expense", "dept": "Engineering", "budget": "78000"},
    {"code": "6040", "name": "Development Tools", "type": "expense", "dept": "Engineering", "budget": "22000"},
    {"code": "6050", "name": "R&D Prototype Costs", "type": "expense", "dept": "R&D", "budget": "0"},  # Zero budget edge case
    {"code": "6060", "name": "Technical Training", "type": "expense", "dept": "Engineering", "budget": "18000"},
    {"code": "6070", "name": "QA & Testing", "type": "expense", "dept": "Engineering", "budget": "32000"},
    {"code": "6080", "name": "Research Partnerships", "type": "expense", "dept": "R&D", "budget": "55000"},
    # Sales OpEx (7xxx)
    {"code": "7000", "name": "Sales Salaries", "type": "expense", "dept": "Sales", "budget": "350000"},
    {"code": "7010", "name": "Sales Commissions", "type": "expense", "dept": "Sales", "budget": "120000"},
    {"code": "7020", "name": "Sales Benefits", "type": "expense", "dept": "Sales", "budget": "87500"},
    {"code": "7030", "name": "Travel & Entertainment", "type": "expense", "dept": "Sales", "budget": "45000"},
    {"code": "7040", "name": "Marketing Salaries", "type": "expense", "dept": "Marketing", "budget": "280000"},
    {"code": "7050", "name": "Digital Advertising", "type": "expense", "dept": "Marketing", "budget": "95000"},
    {"code": "7060", "name": "Content Marketing", "type": "expense", "dept": "Marketing", "budget": "35000"},
    {"code": "7070", "name": "Events & Conferences", "type": "expense", "dept": "Marketing", "budget": "60000"},
    {"code": "7080", "name": "PR & Communications", "type": "expense", "dept": "Marketing", "budget": "28000"},  # Will have NULL actual
    {"code": "7090", "name": "Marketing Tools", "type": "expense", "dept": "Marketing", "budget": "22000"},
    {"code": "7100", "name": "Brand & Design", "type": "expense", "dept": "Marketing", "budget": "18000"},
    {"code": "7110", "name": "Lead Generation", "type": "expense", "dept": "Marketing", "budget": "42000"},
    # G&A OpEx (8xxx)
    {"code": "8000", "name": "Executive Salaries", "type": "expense", "dept": "G&A", "budget": "250000"},
    {"code": "8010", "name": "Admin Salaries", "type": "expense", "dept": "G&A", "budget": "120000"},
    {"code": "8020", "name": "G&A Benefits", "type": "expense", "dept": "G&A", "budget": "92500"},
    {"code": "8030", "name": "Office Rent", "type": "expense", "dept": "G&A", "budget": "85000"},
    {"code": "8040", "name": "Utilities", "type": "expense", "dept": "G&A", "budget": "12000"},
    {"code": "8050", "name": "Insurance", "type": "expense", "dept": "G&A", "budget": "35000"},
    {"code": "8060", "name": "Legal Fees", "type": "expense", "dept": "G&A", "budget": "40000"},
    {"code": "8070", "name": "Accounting & Audit", "type": "expense", "dept": "G&A", "budget": "55000"},
    {"code": "8080", "name": "HR & Recruiting", "type": "expense", "dept": "G&A", "budget": "48000"},
    {"code": "8090", "name": "Office Supplies", "type": "expense", "dept": "G&A", "budget": "8000"},
    {"code": "8100", "name": "Depreciation", "type": "expense", "dept": "G&A", "budget": "65000"},
    {"code": "8110", "name": "Miscellaneous G&A", "type": "expense", "dept": "G&A", "budget": "15000"},
]

# Variance scenarios: (account_code, actual_multiplier_or_value, note)
VARIANCE_SCENARIOS: dict[str, dict] = {
    # Revenue: some above, some below budget
    "4000": {"actual": "920000", "note": "Product revenue exceeded target"},  # +8.2% favorable
    "4010": {"actual": "295000", "note": "Service below target"},  # -7.8% unfavorable
    "4020": {"actual": "510000", "note": "Subscription growth"},  # +6.25% favorable
    "4030": {"actual": "148000", "note": "Slight miss on licensing"},  # -1.3%
    "4090": {"actual": "-3000", "note": "Negative revenue (refund adjustment)"},
    # COGS: some over, some under
    "5000": {"actual": "225000", "note": "Material costs up"},  # +7.1% unfavorable
    "5010": {"actual": "175000", "note": "Labor slightly under"},  # -2.8% favorable
    "5020": {"actual": "94000", "note": "On track"},  # -1%
    "5030": {"actual": "155000", "note": "Infrastructure spike"},  # +24% unfavorable material
    "5070": {"actual": "33000", "note": "Under budget"},  # -5.7% favorable
    # Engineering OpEx
    "6000": {"actual": "430000", "note": "Slightly over"},
    "6010": {"actual": "108000", "note": "Benefits slightly up"},
    "6020": {"actual": "52000", "note": "New licenses"},  # +15.6% material
    "6030": {"actual": "92000", "note": "Cloud overage"},  # +17.9% material
    "6040": {"actual": "21000", "note": "Under budget"},
    "6050": {"actual": "15000", "note": "Zero budget but actual spend"},  # Zero budget edge case
    "6060": {"actual": "16500", "note": "Under budget"},
    "6070": {"actual": "31000", "note": "On track"},
    "6080": {"actual": "48000", "note": "Under budget on partnerships"},
    # Sales OpEx
    "7000": {"actual": "355000", "note": "Slightly over"},
    "7010": {"actual": "145000", "note": "Higher commissions from revenue"},  # +20.8% material
    "7020": {"actual": "88000", "note": "On track"},
    "7030": {"actual": "62000", "note": "Excess travel"},  # +37.8% material
    "7040": {"actual": "285000", "note": "Slightly over"},
    "7050": {"actual": "110000", "note": "Ad spend increase"},  # +15.8% material
    "7060": {"actual": "33000", "note": "Under budget"},
    "7070": {"actual": "75000", "note": "Extra conferences"},  # +25% material
    "7080": {"actual": None, "note": "NULL - data not yet received"},  # NULL edge case
    "7090": {"actual": "23000", "note": "Slightly over"},
    "7100": {"actual": "17000", "note": "Under budget"},
    "7110": {"actual": "55000", "note": "Lead gen overspend"},  # +31% material
    # G&A OpEx
    "8000": {"actual": "250000", "note": "On budget"},
    "8010": {"actual": "118000", "note": "Slightly under"},
    "8020": {"actual": "93000", "note": "On track"},
    "8030": {"actual": "85000", "note": "On budget"},
    "8040": {"actual": "13500", "note": "Utilities up"},  # +12.5% material
    "8050": {"actual": "35000", "note": "On budget"},
    "8060": {"actual": "72000", "note": "Legal dispute costs"},  # +80% material
    "8070": {"actual": "56000", "note": "Slightly over"},
    "8080": {"actual": "65000", "note": "Recruiting push"},  # +35.4% material
    "8090": {"actual": "7500", "note": "Under budget"},
    "8100": {"actual": "65000", "note": "On budget"},
    "8110": {"actual": "18000", "note": "Slightly over"},
}


def generate_budget_file(output_path: str) -> str:
    """Generate sample budget Excel file."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Budget"

    headers = ["Account Code", "Account Name", "Account Type", "Department", "Amount"]
    ws.append(headers)

    for acct in CHART_OF_ACCOUNTS:
        ws.append([
            acct["code"],
            acct["name"],
            acct["type"],
            acct["dept"],
            Decimal(acct["budget"]),
        ])

    wb.save(output_path)
    return output_path


def generate_actuals_file(output_path: str) -> str:
    """Generate sample actuals Excel file with edge cases."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Actuals"

    headers = ["Account Code", "Account Name", "Account Type", "Department", "Amount"]
    ws.append(headers)

    for acct in CHART_OF_ACCOUNTS:
        scenario = VARIANCE_SCENARIOS.get(acct["code"], {})
        actual_value = scenario.get("actual")

        ws.append([
            acct["code"],
            acct["name"],
            acct["type"],
            acct["dept"],
            Decimal(actual_value) if actual_value is not None else None,
        ])

    wb.save(output_path)
    return output_path


def generate_all_sample_data(output_dir: str = "data/samples") -> dict[str, str]:
    """Generate all sample data files. Returns dict of file type -> path."""
    os.makedirs(output_dir, exist_ok=True)

    budget_path = generate_budget_file(os.path.join(output_dir, "budget_2025.xlsx"))
    actuals_path = generate_actuals_file(os.path.join(output_dir, "actuals_nov_2025.xlsx"))

    return {
        "budget": budget_path,
        "actuals": actuals_path,
    }


if __name__ == "__main__":
    paths = generate_all_sample_data()
    for file_type, path in paths.items():
        print(f"Generated {file_type}: {path}")
