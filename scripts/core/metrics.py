"""Financial metrics calculations - margins, ratios, KPIs."""

from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

from scripts.utils.types import VarianceResult


def calculate_gross_margin(
    revenue: Decimal, cogs: Decimal
) -> tuple[Decimal, Optional[Decimal]]:
    """Calculate gross profit and gross margin percentage.

    Returns (gross_profit, margin_pct_or_None).
    """
    gross_profit = revenue - cogs
    if revenue == Decimal("0"):
        return gross_profit, None
    margin_pct = (gross_profit / revenue * Decimal("100")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return gross_profit, margin_pct


def calculate_operating_margin(
    revenue: Decimal, total_opex: Decimal
) -> tuple[Decimal, Optional[Decimal]]:
    """Calculate operating income and operating margin percentage."""
    operating_income = revenue - total_opex
    if revenue == Decimal("0"):
        return operating_income, None
    margin_pct = (operating_income / revenue * Decimal("100")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return operating_income, margin_pct


def calculate_burn_rate(
    total_expenses: Decimal, months: int = 1
) -> Decimal:
    """Calculate monthly burn rate."""
    if months <= 0:
        months = 1
    return (total_expenses / Decimal(str(months))).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


def calculate_budget_utilization(
    actual: Decimal, budget: Decimal
) -> Optional[Decimal]:
    """Calculate percentage of budget consumed. Returns None if budget is zero."""
    if budget == Decimal("0"):
        return None
    return (actual / budget * Decimal("100")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


def calculate_revenue_per_department(
    results: list[VarianceResult],
) -> dict[str, Decimal]:
    """Sum actual revenue by department."""
    dept_revenue: dict[str, Decimal] = {}
    for r in results:
        if r.account_type == "revenue":
            dept_revenue[r.department] = dept_revenue.get(r.department, Decimal("0")) + r.actual
    return dept_revenue


def build_kpi_scorecard(results: list[VarianceResult]) -> dict:
    """Build executive KPI dictionary from variance results."""
    total_revenue_budget = Decimal("0")
    total_revenue_actual = Decimal("0")
    total_cogs_actual = Decimal("0")
    total_opex_actual = Decimal("0")
    total_expense_budget = Decimal("0")
    total_expense_actual = Decimal("0")
    material_count = 0
    favorable_count = 0
    unfavorable_count = 0

    for r in results:
        if r.account_type == "revenue":
            total_revenue_budget += r.budget
            total_revenue_actual += r.actual
        elif r.account_type == "cogs":
            total_cogs_actual += r.actual
            total_expense_budget += r.budget
            total_expense_actual += r.actual
        elif r.account_type in ("expense", "liability"):
            total_opex_actual += r.actual
            total_expense_budget += r.budget
            total_expense_actual += r.actual

        if r.is_material:
            material_count += 1
        if r.favorability == "favorable":
            favorable_count += 1
        elif r.favorability == "unfavorable":
            unfavorable_count += 1

    gross_profit, gross_margin_pct = calculate_gross_margin(
        total_revenue_actual, total_cogs_actual
    )
    _, operating_margin_pct = calculate_operating_margin(
        total_revenue_actual, total_cogs_actual + total_opex_actual
    )
    budget_util = calculate_budget_utilization(total_expense_actual, total_expense_budget)

    revenue_variance = total_revenue_actual - total_revenue_budget

    return {
        "total_revenue_actual": total_revenue_actual,
        "total_revenue_budget": total_revenue_budget,
        "revenue_variance": revenue_variance,
        "gross_profit": gross_profit,
        "gross_margin_pct": gross_margin_pct,
        "operating_margin_pct": operating_margin_pct,
        "total_expenses_actual": total_expense_actual,
        "total_expenses_budget": total_expense_budget,
        "budget_utilization_pct": budget_util,
        "material_variance_count": material_count,
        "favorable_count": favorable_count,
        "unfavorable_count": unfavorable_count,
        "total_accounts": len(results),
    }
