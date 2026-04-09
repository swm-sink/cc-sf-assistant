"""Tests for materiality threshold logic."""

from decimal import Decimal

from scripts.core.materiality import (
    check_materiality,
    count_material_by_favorability,
    filter_material_variances,
    rank_by_impact,
)
from scripts.utils.types import MaterialityThreshold


class TestCheckMateriality:
    def test_above_pct_threshold(self, default_threshold):
        assert check_materiality(Decimal("8000"), Decimal("15"), default_threshold) is True

    def test_above_abs_threshold(self, default_threshold):
        assert check_materiality(Decimal("55000"), Decimal("5"), default_threshold) is True

    def test_above_both_thresholds(self, default_threshold):
        assert check_materiality(Decimal("60000"), Decimal("15"), default_threshold) is True

    def test_below_both_thresholds(self, default_threshold):
        assert check_materiality(Decimal("25000"), Decimal("5"), default_threshold) is False

    def test_exactly_at_pct_threshold(self, default_threshold):
        """10.00% should be material (>=)."""
        assert check_materiality(Decimal("1000"), Decimal("10.00"), default_threshold) is True

    def test_just_below_pct_threshold(self, default_threshold):
        assert check_materiality(Decimal("1000"), Decimal("9.99"), default_threshold) is False

    def test_exactly_at_abs_threshold(self, default_threshold):
        """$50,000 should be material (>=)."""
        assert check_materiality(Decimal("50000"), Decimal("5"), default_threshold) is True

    def test_just_below_abs_threshold(self, default_threshold):
        assert check_materiality(Decimal("49999"), Decimal("5"), default_threshold) is False

    def test_zero_budget_materiality(self, default_threshold):
        """None pct (zero budget case) checks absolute only."""
        assert check_materiality(Decimal("60000"), None, default_threshold) is True
        assert check_materiality(Decimal("10000"), None, default_threshold) is False

    def test_custom_thresholds(self):
        strict = MaterialityThreshold(pct_threshold=Decimal("5"), abs_threshold=Decimal("25000"))
        assert check_materiality(Decimal("1000"), Decimal("6"), strict) is True
        assert check_materiality(Decimal("1000"), Decimal("4"), strict) is False

    def test_negative_variance_uses_absolute(self, default_threshold):
        assert check_materiality(Decimal("-55000"), Decimal("-12"), default_threshold) is True


class TestFilterAndRank:
    def test_filter_material(self, sample_variance_results):
        material = filter_material_variances(sample_variance_results)
        assert all(r.is_material for r in material)
        assert len(material) == 3

    def test_count_by_favorability(self, sample_variance_results):
        counts = count_material_by_favorability(sample_variance_results)
        assert counts["total"] == 3
        assert counts["favorable"] == 1
        assert counts["unfavorable"] == 2

    def test_rank_by_impact(self, sample_variance_results):
        ranked = rank_by_impact(sample_variance_results)
        amounts = [abs(r.variance_amount) for r in ranked]
        assert amounts == sorted(amounts, reverse=True)
