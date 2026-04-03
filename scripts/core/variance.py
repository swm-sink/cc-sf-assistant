"""Core variance calculations - pure functions, Decimal only."""

from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

from scripts.core.favorability import determine_favorability
from scripts.core.materiality import check_materiality
from scripts.utils.types import (
    AccountType,
    MaterialityThreshold,
    VarianceResult,
)


def calculate_variance(
    actual: Decimal, budget: Decimal
) -> tuple[Decimal, Optional[Decimal], str]:
    """Calculate absolute and percentage variance.

    Returns:
        (absolute_variance, pct_variance_or_None, status)
        Status: "Normal", "No Activity", or "Zero Budget"
    """
    if not isinstance(actual, Decimal) or not isinstance(budget, Decimal):
        raise TypeError("Both actual and budget must be Decimal values")

    variance = actual - budget

    if budget == Decimal("0") and actual == Decimal("0"):
        return Decimal("0"), Decimal("0"), "No Activity"

    if budget == Decimal("0"):
        return variance, None, "Zero Budget"

    pct = ((actual - budget) / budget * Decimal("100")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    return variance, pct, "Normal"


def calculate_batch_variance(
    records: list[dict],
    threshold: Optional[MaterialityThreshold] = None,
) -> list[VarianceResult]:
    """Process a batch of account records into VarianceResults.

    Each record must have: account_code, account_name, department,
    account_type, budget, actual.
    """
    if threshold is None:
        threshold = MaterialityThreshold()

    results: list[VarianceResult] = []
    for rec in records:
        budget = Decimal(str(rec["budget"])) if not isinstance(rec["budget"], Decimal) else rec["budget"]
        actual = Decimal(str(rec["actual"])) if not isinstance(rec["actual"], Decimal) else rec["actual"]
        account_type: AccountType = rec["account_type"]

        variance_amount, variance_pct, status = calculate_variance(actual, budget)
        favorability = determine_favorability(variance_amount, account_type)
        is_material = check_materiality(variance_amount, variance_pct, threshold)

        results.append(
            VarianceResult(
                account_code=str(rec["account_code"]),
                account_name=str(rec["account_name"]),
                department=str(rec["department"]),
                account_type=account_type,
                budget=budget,
                actual=actual,
                variance_amount=variance_amount,
                variance_pct=variance_pct,
                favorability=favorability,
                is_material=is_material,
                status=status,
            )
        )

    return results


def calculate_category_subtotals(
    results: list[VarianceResult],
) -> dict[str, VarianceResult]:
    """Aggregate variance results by account type category."""
    categories: dict[str, dict[str, Decimal]] = {}

    for r in results:
        cat = _get_category_label(r.account_type)
        if cat not in categories:
            categories[cat] = {"budget": Decimal("0"), "actual": Decimal("0")}
        categories[cat]["budget"] += r.budget
        categories[cat]["actual"] += r.actual

    subtotals: dict[str, VarianceResult] = {}
    for cat, totals in categories.items():
        variance_amount, variance_pct, status = calculate_variance(
            totals["actual"], totals["budget"]
        )
        account_type = _category_to_account_type(cat)
        subtotals[cat] = VarianceResult(
            account_code=f"SUBTOTAL-{cat.upper()}",
            account_name=f"{cat} Total",
            department="ALL",
            account_type=account_type,
            budget=totals["budget"],
            actual=totals["actual"],
            variance_amount=variance_amount,
            variance_pct=variance_pct,
            favorability=determine_favorability(variance_amount, account_type),
            is_material=False,
            status=status,
        )

    return subtotals


def calculate_department_subtotals(
    results: list[VarianceResult],
) -> dict[str, VarianceResult]:
    """Aggregate variance results by department."""
    departments: dict[str, dict[str, Decimal]] = {}

    for r in results:
        dept = r.department
        if dept not in departments:
            departments[dept] = {"budget": Decimal("0"), "actual": Decimal("0")}
        departments[dept]["budget"] += r.budget
        departments[dept]["actual"] += r.actual

    subtotals: dict[str, VarianceResult] = {}
    for dept, totals in departments.items():
        variance_amount, variance_pct, status = calculate_variance(
            totals["actual"], totals["budget"]
        )
        subtotals[dept] = VarianceResult(
            account_code=f"DEPT-{dept.upper().replace(' ', '-')}",
            account_name=f"{dept} Total",
            department=dept,
            account_type="expense",
            budget=totals["budget"],
            actual=totals["actual"],
            variance_amount=variance_amount,
            variance_pct=variance_pct,
            favorability="neutral",
            is_material=False,
            status=status,
        )

    return subtotals


def _get_category_label(account_type: AccountType) -> str:
    """Map account type to display category."""
    mapping = {
        "revenue": "Revenue",
        "cogs": "COGS",
        "expense": "Operating Expenses",
        "asset": "Assets",
        "liability": "Liabilities",
    }
    return mapping.get(account_type, "Other")


def _category_to_account_type(category: str) -> AccountType:
    """Map category label back to account type."""
    mapping: dict[str, AccountType] = {
        "Revenue": "revenue",
        "COGS": "cogs",
        "Operating Expenses": "expense",
        "Assets": "asset",
        "Liabilities": "liability",
    }
    return mapping.get(category, "expense")
