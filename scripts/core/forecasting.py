"""Rolling forecast logic."""

from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Literal


def replace_forecast_with_actuals(
    forecast: list[dict[str, Any]],
    actuals: list[dict[str, Any]],
    closed_periods: list[str],
) -> list[dict[str, Any]]:
    """Replace forecast values with actuals for closed periods.

    Each record has 'account_code', 'period', and 'amount' keys.
    Returns updated forecast list with actuals substituted.
    """
    actuals_lookup: dict[tuple[str, str], Decimal] = {}
    for rec in actuals:
        key = (str(rec["account_code"]), str(rec["period"]))
        amount = rec["amount"]
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        actuals_lookup[key] = amount

    updated: list[dict[str, Any]] = []
    for rec in forecast:
        entry = dict(rec)
        period = str(entry["period"])
        code = str(entry["account_code"])

        if period in closed_periods:
            key = (code, period)
            if key in actuals_lookup:
                entry["amount"] = actuals_lookup[key]
                entry["source"] = "actual"
            else:
                entry["source"] = "forecast_no_actual"
        else:
            entry["source"] = "forecast"

        updated.append(entry)

    return updated


def extend_forecast_window(
    forecast: list[dict[str, Any]],
    periods_to_add: int,
    method: Literal["last_period", "average", "growth_rate"] = "last_period",
) -> list[dict[str, Any]]:
    """Extend forecast forward by adding new periods.

    Methods:
        last_period: Copy last period's values
        average: Use average of all existing periods
        growth_rate: Apply growth rate from last two periods
    """
    if not forecast or periods_to_add <= 0:
        return list(forecast)

    # Group by account
    accounts: dict[str, list[dict[str, Any]]] = {}
    for rec in forecast:
        code = str(rec["account_code"])
        if code not in accounts:
            accounts[code] = []
        accounts[code].append(rec)

    extended = list(forecast)

    for code, recs in accounts.items():
        sorted_recs = sorted(recs, key=lambda r: str(r["period"]))
        last_rec = sorted_recs[-1]

        for i in range(1, periods_to_add + 1):
            new_period = f"P+{i}"  # Placeholder period label
            amount = _calculate_extension_amount(sorted_recs, method)

            extended.append({
                "account_code": code,
                "account_name": last_rec.get("account_name", ""),
                "department": last_rec.get("department", ""),
                "period": new_period,
                "amount": amount,
                "source": "forecast_extended",
            })

    return extended


def _calculate_extension_amount(
    sorted_recs: list[dict[str, Any]],
    method: str,
) -> Decimal:
    """Calculate the amount for an extended forecast period."""
    amounts = []
    for r in sorted_recs:
        amt = r.get("amount", Decimal("0"))
        if not isinstance(amt, Decimal):
            amt = Decimal(str(amt))
        amounts.append(amt)

    if not amounts:
        return Decimal("0")

    if method == "last_period":
        return amounts[-1]

    if method == "average":
        total = sum(amounts, Decimal("0"))
        return (total / Decimal(str(len(amounts)))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    if method == "growth_rate" and len(amounts) >= 2:
        prev = amounts[-2]
        last = amounts[-1]
        if prev != Decimal("0"):
            growth = (last - prev) / prev
            return (last * (Decimal("1") + growth)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        return last

    return amounts[-1]


def track_assumption_changes(
    old_assumptions: dict[str, Any],
    new_assumptions: dict[str, Any],
) -> list[dict[str, Any]]:
    """Produce a change log comparing old and new forecast assumptions."""
    changes: list[dict[str, Any]] = []

    all_keys = set(old_assumptions.keys()) | set(new_assumptions.keys())

    for key in sorted(all_keys):
        old_val = old_assumptions.get(key)
        new_val = new_assumptions.get(key)

        if old_val != new_val:
            changes.append({
                "assumption": key,
                "old_value": old_val,
                "new_value": new_val,
                "change_type": _classify_change(old_val, new_val),
            })

    return changes


def _classify_change(old_val: Any, new_val: Any) -> str:
    """Classify the type of assumption change."""
    if old_val is None:
        return "added"
    if new_val is None:
        return "removed"
    return "modified"
