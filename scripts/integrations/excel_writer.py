"""Write formatted multi-sheet Excel variance reports."""

import os
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from scripts.core.materiality import count_material_by_favorability, filter_material_variances, rank_by_impact
from scripts.core.metrics import build_kpi_scorecard
from scripts.core.variance import calculate_category_subtotals
from scripts.utils.logger import log_audit
from scripts.utils.types import VarianceResult

try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None


def create_variance_report(
    results: list[VarianceResult],
    output_path: str,
    metadata: dict[str, Any],
) -> str:
    """Generate multi-sheet Excel variance report."""
    if xlsxwriter is None:
        raise ImportError("xlsxwriter required for Excel report generation")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    wb = xlsxwriter.Workbook(output_path)

    # Formats
    header_fmt = wb.add_format({
        "bold": True, "bg_color": "#2C3E50", "font_color": "white",
        "border": 1, "text_wrap": True, "valign": "vcenter",
    })
    currency_fmt = wb.add_format({"num_format": "$#,##0.00", "border": 1})
    pct_fmt = wb.add_format({"num_format": "0.00%", "border": 1})
    text_fmt = wb.add_format({"border": 1, "valign": "vcenter"})
    favorable_fmt = wb.add_format({
        "num_format": "$#,##0.00", "border": 1,
        "bg_color": "#D5F5E3", "font_color": "#1E8449",
    })
    unfavorable_fmt = wb.add_format({
        "num_format": "$#,##0.00", "border": 1,
        "bg_color": "#FADBD8", "font_color": "#C0392B",
    })
    title_fmt = wb.add_format({
        "bold": True, "font_size": 14, "bottom": 2,
    })
    subtitle_fmt = wb.add_format({"italic": True, "font_color": "#7F8C8D"})

    _write_executive_summary(wb, results, metadata, header_fmt, currency_fmt, pct_fmt, text_fmt, title_fmt, subtitle_fmt, favorable_fmt, unfavorable_fmt)
    _write_detailed_analysis(wb, results, header_fmt, currency_fmt, pct_fmt, text_fmt, favorable_fmt, unfavorable_fmt)
    _write_material_variances(wb, results, header_fmt, currency_fmt, pct_fmt, text_fmt, favorable_fmt, unfavorable_fmt)
    _write_metadata_sheet(wb, metadata, text_fmt, title_fmt)

    wb.close()

    log_audit("create_variance_report", [output_path], {
        "accounts": len(results),
        "material_count": len(filter_material_variances(results)),
    })
    return output_path


def _write_executive_summary(wb, results, metadata, header_fmt, currency_fmt, pct_fmt, text_fmt, title_fmt, subtitle_fmt, fav_fmt, unfav_fmt):
    ws = wb.add_worksheet("Executive Summary")
    ws.set_column("A:A", 25)
    ws.set_column("B:F", 18)

    row = 0
    ws.write(row, 0, "Variance Analysis - Executive Summary", title_fmt)
    row += 1
    ws.write(row, 0, f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", subtitle_fmt)
    row += 2

    # KPI summary
    kpis = build_kpi_scorecard(results)
    mat_counts = count_material_by_favorability(results)

    kpi_data = [
        ("Total Revenue (Actual)", kpis["total_revenue_actual"]),
        ("Total Revenue (Budget)", kpis["total_revenue_budget"]),
        ("Revenue Variance", kpis["revenue_variance"]),
        ("Gross Margin %", kpis.get("gross_margin_pct")),
        ("Operating Margin %", kpis.get("operating_margin_pct")),
        ("Total Accounts", kpis["total_accounts"]),
        ("Material Variances", mat_counts["total"]),
        ("Favorable (Material)", mat_counts["favorable"]),
        ("Unfavorable (Material)", mat_counts["unfavorable"]),
    ]

    ws.write(row, 0, "Key Metric", header_fmt)
    ws.write(row, 1, "Value", header_fmt)
    row += 1

    for label, value in kpi_data:
        ws.write(row, 0, label, text_fmt)
        if isinstance(value, Decimal):
            ws.write(row, 1, float(value), currency_fmt)
        else:
            ws.write(row, 1, value, text_fmt)
        row += 1

    # Category subtotals
    row += 2
    ws.write(row, 0, "Category Summary", title_fmt)
    row += 1
    headers = ["Category", "Budget", "Actual", "$ Variance", "% Variance"]
    for col, h in enumerate(headers):
        ws.write(row, col, h, header_fmt)
    row += 1

    subtotals = calculate_category_subtotals(results)
    for cat_name, sub in subtotals.items():
        ws.write(row, 0, cat_name, text_fmt)
        ws.write(row, 1, float(sub.budget), currency_fmt)
        ws.write(row, 2, float(sub.actual), currency_fmt)
        fmt = fav_fmt if sub.favorability == "favorable" else unfav_fmt if sub.favorability == "unfavorable" else currency_fmt
        ws.write(row, 3, float(sub.variance_amount), fmt)
        if sub.variance_pct is not None:
            ws.write(row, 4, float(sub.variance_pct) / 100, pct_fmt)
        else:
            ws.write(row, 4, "N/A", text_fmt)
        row += 1


def _write_detailed_analysis(wb, results, header_fmt, currency_fmt, pct_fmt, text_fmt, fav_fmt, unfav_fmt):
    ws = wb.add_worksheet("Detailed Analysis")
    ws.set_column("A:A", 14)
    ws.set_column("B:B", 30)
    ws.set_column("C:C", 14)
    ws.set_column("D:D", 16)
    ws.set_column("E:I", 16)

    headers = [
        "Account Code", "Account Name", "Department", "Account Type",
        "Budget", "Actual", "$ Variance", "% Variance",
        "Favorability", "Material",
    ]
    for col, h in enumerate(headers):
        ws.write(0, col, h, header_fmt)

    for row_idx, r in enumerate(results, start=1):
        ws.write(row_idx, 0, r.account_code, text_fmt)
        ws.write(row_idx, 1, r.account_name, text_fmt)
        ws.write(row_idx, 2, r.department, text_fmt)
        ws.write(row_idx, 3, r.account_type, text_fmt)
        ws.write(row_idx, 4, float(r.budget), currency_fmt)
        ws.write(row_idx, 5, float(r.actual), currency_fmt)

        var_fmt = fav_fmt if r.favorability == "favorable" and r.is_material else unfav_fmt if r.favorability == "unfavorable" and r.is_material else currency_fmt
        ws.write(row_idx, 6, float(r.variance_amount), var_fmt)

        if r.variance_pct is not None:
            ws.write(row_idx, 7, float(r.variance_pct) / 100, pct_fmt)
        else:
            ws.write(row_idx, 7, "N/A", text_fmt)

        ws.write(row_idx, 8, r.favorability.title(), text_fmt)
        ws.write(row_idx, 9, "Yes" if r.is_material else "No", text_fmt)

    ws.autofilter(0, 0, len(results), len(headers) - 1)


def _write_material_variances(wb, results, header_fmt, currency_fmt, pct_fmt, text_fmt, fav_fmt, unfav_fmt):
    ws = wb.add_worksheet("Material Variances")
    ws.set_column("A:A", 14)
    ws.set_column("B:B", 30)
    ws.set_column("C:C", 14)
    ws.set_column("D:D", 16)
    ws.set_column("E:I", 16)
    ws.set_column("J:J", 40)

    headers = [
        "Account Code", "Account Name", "Department", "Account Type",
        "Budget", "Actual", "$ Variance", "% Variance",
        "Favorability", "Commentary",
    ]
    for col, h in enumerate(headers):
        ws.write(0, col, h, header_fmt)

    material = rank_by_impact(filter_material_variances(results))

    for row_idx, r in enumerate(material, start=1):
        ws.write(row_idx, 0, r.account_code, text_fmt)
        ws.write(row_idx, 1, r.account_name, text_fmt)
        ws.write(row_idx, 2, r.department, text_fmt)
        ws.write(row_idx, 3, r.account_type, text_fmt)
        ws.write(row_idx, 4, float(r.budget), currency_fmt)
        ws.write(row_idx, 5, float(r.actual), currency_fmt)

        var_fmt = fav_fmt if r.favorability == "favorable" else unfav_fmt
        ws.write(row_idx, 6, float(r.variance_amount), var_fmt)

        if r.variance_pct is not None:
            ws.write(row_idx, 7, float(r.variance_pct) / 100, pct_fmt)
        else:
            ws.write(row_idx, 7, "N/A", text_fmt)

        ws.write(row_idx, 8, r.favorability.title(), text_fmt)
        ws.write(row_idx, 9, r.commentary or "", text_fmt)


def _write_metadata_sheet(wb, metadata, text_fmt, title_fmt):
    ws = wb.add_worksheet("Metadata")
    ws.set_column("A:A", 25)
    ws.set_column("B:B", 60)

    ws.write(0, 0, "Report Metadata", title_fmt)

    items = [
        ("Generated", datetime.now(timezone.utc).isoformat()),
        ("Budget Source", metadata.get("budget_file", "N/A")),
        ("Actuals Source", metadata.get("actuals_file", "N/A")),
        ("Period", metadata.get("period", "N/A")),
        ("Materiality % Threshold", metadata.get("pct_threshold", "10%")),
        ("Materiality $ Threshold", metadata.get("abs_threshold", "$50,000")),
    ]

    for row_idx, (label, value) in enumerate(items, start=2):
        ws.write(row_idx, 0, label, text_fmt)
        ws.write(row_idx, 1, str(value), text_fmt)
