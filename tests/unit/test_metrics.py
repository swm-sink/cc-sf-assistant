"""Tests for financial metrics calculations."""

from decimal import Decimal

from scripts.core.metrics import (
    build_kpi_scorecard,
    calculate_budget_utilization,
    calculate_burn_rate,
    calculate_gross_margin,
    calculate_operating_margin,
)


class TestGrossMargin:
    def test_normal_margin(self):
        profit, pct = calculate_gross_margin(Decimal("1000000"), Decimal("600000"))
        assert profit == Decimal("400000")
        assert pct == Decimal("40.00")

    def test_zero_revenue(self):
        profit, pct = calculate_gross_margin(Decimal("0"), Decimal("50000"))
        assert profit == Decimal("-50000")
        assert pct is None


class TestOperatingMargin:
    def test_normal_margin(self):
        income, pct = calculate_operating_margin(Decimal("1000000"), Decimal("800000"))
        assert income == Decimal("200000")
        assert pct == Decimal("20.00")


class TestBurnRate:
    def test_monthly_burn(self):
        rate = calculate_burn_rate(Decimal("300000"), 3)
        assert rate == Decimal("100000.00")

    def test_zero_months_defaults_to_one(self):
        rate = calculate_burn_rate(Decimal("100000"), 0)
        assert rate == Decimal("100000.00")


class TestBudgetUtilization:
    def test_normal(self):
        util = calculate_budget_utilization(Decimal("90000"), Decimal("100000"))
        assert util == Decimal("90.00")

    def test_over_budget(self):
        util = calculate_budget_utilization(Decimal("120000"), Decimal("100000"))
        assert util == Decimal("120.00")

    def test_zero_budget(self):
        util = calculate_budget_utilization(Decimal("50000"), Decimal("0"))
        assert util is None


class TestKPIScorecard:
    def test_scorecard_structure(self, sample_variance_results):
        kpis = build_kpi_scorecard(sample_variance_results)
        assert "total_revenue_actual" in kpis
        assert "gross_margin_pct" in kpis
        assert "material_variance_count" in kpis
        assert "total_accounts" in kpis
        assert kpis["total_accounts"] == 5
