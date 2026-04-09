"""Tests for core variance calculations."""

from decimal import Decimal

import pytest

from scripts.core.variance import (
    calculate_batch_variance,
    calculate_category_subtotals,
    calculate_department_subtotals,
    calculate_variance,
)
from scripts.utils.types import MaterialityThreshold


class TestCalculateVariance:
    def test_normal_variance(self):
        amount, pct, status = calculate_variance(Decimal("115000"), Decimal("100000"))
        assert amount == Decimal("15000")
        assert pct == Decimal("15.00")
        assert status == "Normal"

    def test_negative_variance(self):
        amount, pct, status = calculate_variance(Decimal("90000"), Decimal("100000"))
        assert amount == Decimal("-10000")
        assert pct == Decimal("-10.00")
        assert status == "Normal"

    def test_zero_budget_with_actuals(self):
        amount, pct, status = calculate_variance(Decimal("50000"), Decimal("0"))
        assert amount == Decimal("50000")
        assert pct is None
        assert status == "Zero Budget"

    def test_both_zero(self):
        amount, pct, status = calculate_variance(Decimal("0"), Decimal("0"))
        assert amount == Decimal("0")
        assert pct == Decimal("0")
        assert status == "No Activity"

    def test_negative_budget(self):
        """Liability/contra accounts can have negative budgets."""
        amount, pct, status = calculate_variance(Decimal("-12000"), Decimal("-10000"))
        assert amount == Decimal("-2000")
        assert status == "Normal"

    def test_actual_crosses_zero(self):
        """Budget negative, actual positive."""
        amount, pct, status = calculate_variance(Decimal("3000"), Decimal("-5000"))
        assert amount == Decimal("8000")
        assert status == "Normal"

    def test_large_numbers(self):
        amount, pct, status = calculate_variance(
            Decimal("1000000000000"), Decimal("999000000000")
        )
        assert amount == Decimal("1000000000")
        assert status == "Normal"

    def test_small_variance(self):
        amount, pct, status = calculate_variance(Decimal("100001"), Decimal("100000"))
        assert amount == Decimal("1")
        assert pct == Decimal("0.00")  # Rounds to 0.00%
        assert status == "Normal"

    def test_type_enforcement_rejects_float(self):
        with pytest.raises(TypeError):
            calculate_variance(115000.0, Decimal("100000"))

    def test_decimal_precision(self):
        """Verify Decimal avoids float precision issues."""
        amount, pct, status = calculate_variance(
            Decimal("0.3"), Decimal("0.1")
        )
        assert amount == Decimal("0.2")  # float would give 0.19999...


class TestBatchVariance:
    def test_batch_processing(self, sample_records):
        results = calculate_batch_variance(sample_records)
        assert len(results) == 4
        assert results[0].account_code == "4000"
        assert results[0].variance_amount == Decimal("70000")
        assert results[0].favorability == "favorable"

    def test_batch_with_zero_budget(self, sample_records):
        results = calculate_batch_variance(sample_records)
        r_and_d = next(r for r in results if r.account_code == "6050")
        assert r_and_d.status == "Zero Budget"
        assert r_and_d.variance_pct is None

    def test_batch_materiality(self, sample_records):
        results = calculate_batch_variance(sample_records)
        legal = next(r for r in results if r.account_code == "8060")
        assert legal.is_material is True  # 80% > 10%


class TestSubtotals:
    def test_category_subtotals(self, sample_variance_results):
        subtotals = calculate_category_subtotals(sample_variance_results)
        assert "Revenue" in subtotals
        assert subtotals["Revenue"].budget == Decimal("1170000")

    def test_department_subtotals(self, sample_variance_results):
        subtotals = calculate_department_subtotals(sample_variance_results)
        assert "Sales" in subtotals
        assert "Engineering" in subtotals
