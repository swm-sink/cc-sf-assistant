"""Role-based report generation pipeline."""

import os
from typing import Any

from scripts.integrations.excel_writer import create_variance_report
from scripts.integrations.html_dashboard import generate_dashboard
from scripts.integrations.html_presentation import generate_presentation
from scripts.utils.logger import log_audit
from scripts.utils.types import DashboardConfig, UserRole, VarianceResult


def generate_all_reports(
    results: list[VarianceResult],
    output_dir: str,
    metadata: dict[str, Any],
) -> dict[str, str]:
    """Generate all output formats for a single role."""
    os.makedirs(output_dir, exist_ok=True)
    outputs: dict[str, str] = {}

    excel_path = os.path.join(output_dir, "variance_report.xlsx")
    create_variance_report(results, excel_path, metadata)
    outputs["excel"] = excel_path

    for role in ("analyst", "senior_analyst", "manager"):
        config = DashboardConfig(
            role=role,
            title=metadata.get("title", "Variance Analysis"),
            period=metadata.get("period", ""),
            materiality_only=(role == "manager"),
        )
        dash_path = os.path.join(output_dir, f"dashboard_{role}.html")
        generate_dashboard(results, role, dash_path, config)
        outputs[f"dashboard_{role}"] = dash_path

    for role in ("senior_analyst", "manager"):
        pres_path = os.path.join(output_dir, f"presentation_{role}.html")
        generate_presentation(results, pres_path, metadata)
        outputs[f"presentation_{role}"] = pres_path

    log_audit("generate_all_reports", [output_dir], {"formats": len(outputs)})
    return outputs


def generate_role_based_outputs(
    results: list[VarianceResult],
    output_dir: str,
    metadata: dict[str, Any],
) -> dict[UserRole, dict[str, str]]:
    """Generate role-specific output sets."""
    os.makedirs(output_dir, exist_ok=True)
    role_outputs: dict[UserRole, dict[str, str]] = {}

    roles: list[UserRole] = ["analyst", "senior_analyst", "manager"]
    for role in roles:
        role_dir = os.path.join(output_dir, role)
        os.makedirs(role_dir, exist_ok=True)

        outputs: dict[str, str] = {}

        # Excel
        excel_path = os.path.join(role_dir, "variance_report.xlsx")
        create_variance_report(results, excel_path, metadata)
        outputs["excel"] = excel_path

        # Dashboard
        config = DashboardConfig(
            role=role,
            title=metadata.get("title", "Variance Analysis"),
            period=metadata.get("period", ""),
            materiality_only=(role == "manager"),
        )
        dash_path = os.path.join(role_dir, "dashboard.html")
        generate_dashboard(results, role, dash_path, config)
        outputs["dashboard"] = dash_path

        # Presentation (senior analyst + manager)
        if role in ("senior_analyst", "manager"):
            pres_path = os.path.join(role_dir, "presentation.html")
            generate_presentation(results, pres_path, metadata)
            outputs["presentation"] = pres_path

        role_outputs[role] = outputs

    return role_outputs
