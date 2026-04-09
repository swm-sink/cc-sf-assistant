"""End-to-end variance analysis workflow."""

import os
import time
from decimal import Decimal
from typing import Any, Optional

from scripts.core.variance import calculate_batch_variance
from scripts.integrations.excel_reader import dataframe_to_records, load_actuals, load_budget
from scripts.integrations.excel_writer import create_variance_report
from scripts.integrations.html_dashboard import generate_dashboard
from scripts.integrations.html_presentation import generate_presentation
from scripts.utils.config_loader import get_materiality_thresholds, load_config
from scripts.utils.logger import log_audit, setup_logger
from scripts.utils.types import DashboardConfig, MaterialityThreshold, UserRole, VarianceResult
from scripts.utils.validator import reconcile_datasets


def run_variance_analysis(
    budget_path: str,
    actuals_path: str,
    output_dir: str = "output",
    role: UserRole = "analyst",
    config_path: str = "config/fpa_config.yaml",
    period: str = "",
) -> dict[str, Any]:
    """Run complete variance analysis pipeline.

    Returns summary dict with file paths, counts, and timing.
    """
    setup_logger()
    start_time = time.time()

    # 1. Load config
    config = load_config(config_path)
    threshold = get_materiality_thresholds(config)

    # 2. Read and validate budget
    budget_df, budget_meta = load_budget(budget_path)

    # 3. Read and validate actuals
    actuals_df, actuals_meta = load_actuals(actuals_path)

    # 4. Reconcile accounts
    reconciliation = reconcile_datasets(budget_df, actuals_df, "Account Code")

    # 5. Merge to records and calculate variances
    records = dataframe_to_records(budget_df, actuals_df)
    results = calculate_batch_variance(records, threshold)

    # 6. Generate outputs
    os.makedirs(output_dir, exist_ok=True)
    outputs = _generate_outputs(results, output_dir, role, period, budget_path, actuals_path, threshold)

    elapsed = time.time() - start_time

    summary = {
        "role": role,
        "period": period,
        "total_accounts": len(results),
        "material_count": sum(1 for r in results if r.is_material),
        "reconciliation": reconciliation,
        "budget_nulls": budget_meta.get("has_nulls", False),
        "actuals_nulls": actuals_meta.get("has_nulls", False),
        "actuals_null_rows": actuals_meta.get("null_row_indices", []),
        "outputs": outputs,
        "elapsed_seconds": round(elapsed, 2),
    }

    log_audit("run_variance_analysis", [budget_path, actuals_path], {
        "role": role,
        "accounts": len(results),
        "material": summary["material_count"],
        "elapsed": summary["elapsed_seconds"],
    })

    return summary


def _generate_outputs(
    results: list[VarianceResult],
    output_dir: str,
    role: UserRole,
    period: str,
    budget_path: str,
    actuals_path: str,
    threshold: MaterialityThreshold,
) -> dict[str, str]:
    """Generate role-appropriate outputs."""
    outputs: dict[str, str] = {}
    metadata = {
        "budget_file": budget_path,
        "actuals_file": actuals_path,
        "period": period,
        "pct_threshold": f"{threshold.pct_threshold}%",
        "abs_threshold": f"${threshold.abs_threshold:,.0f}",
        "title": f"Variance Analysis - {period}" if period else "Variance Analysis",
    }

    # Excel report (all roles)
    excel_path = os.path.join(output_dir, f"variance_report_{role}.xlsx")
    create_variance_report(results, excel_path, metadata)
    outputs["excel_report"] = excel_path

    # HTML Dashboard
    dashboard_config = DashboardConfig(
        role=role,
        title=metadata["title"],
        period=period,
        materiality_only=(role == "manager"),
    )
    dashboard_path = os.path.join(output_dir, f"dashboard_{role}.html")
    generate_dashboard(results, role, dashboard_path, dashboard_config)
    outputs["html_dashboard"] = dashboard_path

    # HTML Presentation (senior analyst and manager)
    if role in ("senior_analyst", "manager"):
        pres_path = os.path.join(output_dir, f"presentation_{role}.html")
        generate_presentation(results, pres_path, metadata)
        outputs["html_presentation"] = pres_path

    return outputs


if __name__ == "__main__":
    import sys

    budget = sys.argv[1] if len(sys.argv) > 1 else "data/samples/budget_2025.xlsx"
    actuals = sys.argv[2] if len(sys.argv) > 2 else "data/samples/actuals_nov_2025.xlsx"
    role = sys.argv[3] if len(sys.argv) > 3 else "analyst"

    summary = run_variance_analysis(
        budget_path=budget,
        actuals_path=actuals,
        output_dir="output",
        role=role,
        period="November 2025",
    )

    print(f"\nVariance Analysis Complete ({role})")
    print(f"  Accounts: {summary['total_accounts']}")
    print(f"  Material: {summary['material_count']}")
    print(f"  Time: {summary['elapsed_seconds']}s")
    print(f"  Outputs:")
    for name, path in summary["outputs"].items():
        print(f"    {name}: {path}")
