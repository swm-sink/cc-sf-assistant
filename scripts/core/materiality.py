"""Materiality threshold flagging and variance ranking."""

from decimal import Decimal
from typing import Optional

from scripts.utils.types import MaterialityThreshold, VarianceResult


def check_materiality(
    variance_amount: Decimal,
    variance_pct: Optional[Decimal],
    threshold: MaterialityThreshold,
) -> bool:
    """Check if a variance exceeds materiality thresholds.

    Material if |pct| >= pct_threshold OR |amount| >= abs_threshold.
    If variance_pct is None (zero budget), checks absolute threshold only.
    """
    abs_exceeds = abs(variance_amount) >= threshold.abs_threshold

    if variance_pct is None:
        return abs_exceeds

    pct_exceeds = abs(variance_pct) >= threshold.pct_threshold
    return pct_exceeds or abs_exceeds


def filter_material_variances(
    results: list[VarianceResult],
) -> list[VarianceResult]:
    """Return only material variance results."""
    return [r for r in results if r.is_material]


def count_material_by_favorability(
    results: list[VarianceResult],
) -> dict[str, int]:
    """Count material variances grouped by favorability."""
    material = filter_material_variances(results)
    counts = {"favorable": 0, "unfavorable": 0, "neutral": 0, "total": len(material)}
    for r in material:
        counts[r.favorability] += 1
    return counts


def rank_by_impact(
    results: list[VarianceResult],
) -> list[VarianceResult]:
    """Sort variance results by absolute variance amount descending."""
    return sorted(results, key=lambda r: abs(r.variance_amount), reverse=True)
