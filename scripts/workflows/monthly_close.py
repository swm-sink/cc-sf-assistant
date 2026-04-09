"""Monthly close workflow with multi-department consolidation."""

import os
import time
from decimal import Decimal
from pathlib import Path
from typing import Any

from scripts.core.consolidation import consolidate_records, detect_duplicate_accounts
from scripts.core.variance import calculate_batch_variance
from scripts.integrations.excel_reader import load_budget, read_excel_file, convert_amounts_to_decimal
from scripts.integrations.html_dashboard import generate_dashboard
from scripts.integrations.html_presentation import generate_presentation
from scripts.integrations.excel_writer import create_variance_report
from scripts.utils.config_loader import get_materiality_thresholds, load_config
from scripts.utils.logger import log_audit, setup_logger
from scripts.utils.types import DashboardConfig, UserRole, VarianceResult
from scripts.utils.validator import convert_amount_to_decimal


def run_monthly_close(
    budget_path: str,
    actuals_dir: str,
    output_dir: str = "output/monthly_close",
    period: str = "",
    config_path: str = "config/fpa_config.yaml",
) -> dict[str, Any]:
    """Run monthly close with multi-department consolidation.

    Args:
        budget_path: Path to consolidated budget file
        actuals_dir: Directory containing per-department actuals files
        output_dir: Output directory for reports
        period: Period label (e.g., "November 2025")
        config_path: Configuration file path
    """
    setup_logger()
    start_time = time.time()
    config = load_config(config_path)
    threshold = get_materiality_thresholds(config)

    # 1. Load budget
    budget_df, budget_meta = load_budget(budget_path)

    # 2. Discover and load department actuals
    actuals_files = sorted(Path(actuals_dir).glob("*.xlsx"))
    dept_records: dict[str, list[dict[str, Any]]] = {}

    for f in actuals_files:
        dept_name = f.stem.replace("actuals_", "").replace("_", " ").title()
        df = read_excel_file(str(f))
        df, _ = convert_amounts_to_decimal(df)

        records = []
        for _, row in df.iterrows():
            amount = row.get("Amount")
            if amount is None:
                continue
            if not isinstance(amount, Decimal):
                amount = convert_amount_to_decimal(amount)
                if amount is None:
                    continue
            records.append({
                "account_code": str(row["Account Code"]),
                "account_name": str(row["Account Name"]),
                "account_type": str(row["Account Type"]),
                "department": dept_name,
                "actual": amount,
            })
        dept_records[dept_name] = records

    # 3. Detect duplicates
    duplicates = detect_duplicate_accounts(dept_records)

    # 4. Consolidate
    consolidated, consolidation_meta = consolidate_records(dept_records)

    # 5. Merge with budget
    budget_map: dict[str, dict] = {}
    for _, row in budget_df.iterrows():
        code = str(row["Account Code"])
        budget_amount = row["Amount"]
        if not isinstance(budget_amount, Decimal):
            budget_amount = convert_amount_to_decimal(budget_amount) or Decimal("0")
        budget_map[code] = {
            "account_code": code,
            "account_name": str(row["Account Name"]),
            "department": str(row["Department"]),
            "account_type": str(row["Account Type"]),
            "budget": budget_amount,
        }

    merged_records = []
    for rec in consolidated:
        code = rec["account_code"]
        if code in budget_map:
            entry = dict(budget_map[code])
            entry["actual"] = rec["actual"]
            entry["department"] = rec.get("department", entry["department"])
            merged_records.append(entry)

    # 6. Calculate variances
    results = calculate_batch_variance(merged_records, threshold)

    # 7. Generate outputs for all roles
    os.makedirs(output_dir, exist_ok=True)
    metadata = {
        "budget_file": budget_path,
        "actuals_dir": actuals_dir,
        "period": period,
        "title": f"Monthly Close - {period}" if period else "Monthly Close Report",
    }

    outputs: dict[str, str] = {}
    for role in ("analyst", "senior_analyst", "manager"):
        role_dir = os.path.join(output_dir, role)
        os.makedirs(role_dir, exist_ok=True)

        excel_path = os.path.join(role_dir, "variance_report.xlsx")
        create_variance_report(results, excel_path, metadata)
        outputs[f"excel_{role}"] = excel_path

        dash_config = DashboardConfig(
            role=role, title=metadata["title"],
            period=period, materiality_only=(role == "manager"),
        )
        dash_path = os.path.join(role_dir, "dashboard.html")
        generate_dashboard(results, role, dash_path, dash_config)
        outputs[f"dashboard_{role}"] = dash_path

        if role in ("senior_analyst", "manager"):
            pres_path = os.path.join(role_dir, "presentation.html")
            generate_presentation(results, pres_path, metadata)
            outputs[f"presentation_{role}"] = pres_path

    elapsed = time.time() - start_time

    summary = {
        "period": period,
        "departments": consolidation_meta["departments"],
        "total_records": len(results),
        "material_count": sum(1 for r in results if r.is_material),
        "duplicates": duplicates,
        "consolidation_meta": consolidation_meta,
        "outputs": outputs,
        "elapsed_seconds": round(elapsed, 2),
    }

    log_audit("run_monthly_close", [budget_path, actuals_dir], {
        "departments": len(dept_records),
        "records": len(results),
        "elapsed": summary["elapsed_seconds"],
    })

    return summary
