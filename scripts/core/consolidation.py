"""Multi-department data consolidation."""

from decimal import Decimal
from typing import Any


def consolidate_records(
    department_records: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Consolidate records from multiple departments into a single list.

    Returns:
        (consolidated_records, metadata)
        metadata includes record counts per department and timestamp.
    """
    consolidated: list[dict[str, Any]] = []
    dept_counts: dict[str, int] = {}

    for dept_name, records in department_records.items():
        dept_counts[dept_name] = len(records)
        for rec in records:
            entry = dict(rec)
            if "department" not in entry:
                entry["department"] = dept_name
            consolidated.append(entry)

    metadata = {
        "department_counts": dept_counts,
        "total_records": len(consolidated),
        "departments": sorted(department_records.keys()),
    }

    return consolidated, metadata


def detect_duplicate_accounts(
    department_records: dict[str, list[dict[str, Any]]],
) -> list[tuple[str, list[str]]]:
    """Find account codes appearing in multiple departments.

    Returns list of (account_code, [department_names]).
    """
    account_depts: dict[str, list[str]] = {}

    for dept_name, records in department_records.items():
        for rec in records:
            code = str(rec.get("account_code", ""))
            if code not in account_depts:
                account_depts[code] = []
            account_depts[code].append(dept_name)

    return [
        (code, depts) for code, depts in sorted(account_depts.items()) if len(depts) > 1
    ]


def reconcile_to_total(
    department_totals: dict[str, Decimal],
    consolidated_total: Decimal,
) -> tuple[bool, Decimal]:
    """Verify sum of department totals equals consolidated total.

    Returns (matches, difference).
    """
    dept_sum = sum(department_totals.values(), Decimal("0"))
    difference = dept_sum - consolidated_total
    return difference == Decimal("0"), difference
