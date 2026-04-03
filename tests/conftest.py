"""Shared pytest fixtures for FP&A tests."""

from decimal import Decimal

import pytest

from scripts.utils.types import MaterialityThreshold, VarianceResult


@pytest.fixture
def default_threshold() -> MaterialityThreshold:
    return MaterialityThreshold(
        pct_threshold=Decimal("10"),
        abs_threshold=Decimal("50000"),
    )


@pytest.fixture
def sample_records() -> list[dict]:
    """Sample account records for batch variance testing."""
    return [
        {
            "account_code": "4000",
            "account_name": "Product Revenue",
            "department": "Sales",
            "account_type": "revenue",
            "budget": Decimal("850000"),
            "actual": Decimal("920000"),
        },
        {
            "account_code": "5000",
            "account_name": "Direct Materials",
            "department": "Engineering",
            "account_type": "cogs",
            "budget": Decimal("210000"),
            "actual": Decimal("225000"),
        },
        {
            "account_code": "6050",
            "account_name": "R&D Prototype Costs",
            "department": "R&D",
            "account_type": "expense",
            "budget": Decimal("0"),
            "actual": Decimal("15000"),
        },
        {
            "account_code": "8060",
            "account_name": "Legal Fees",
            "department": "G&A",
            "account_type": "expense",
            "budget": Decimal("40000"),
            "actual": Decimal("72000"),
        },
    ]


@pytest.fixture
def sample_variance_results() -> list[VarianceResult]:
    """Pre-computed variance results for testing."""
    return [
        VarianceResult(
            account_code="4000", account_name="Product Revenue",
            department="Sales", account_type="revenue",
            budget=Decimal("850000"), actual=Decimal("920000"),
            variance_amount=Decimal("70000"), variance_pct=Decimal("8.24"),
            favorability="favorable", is_material=True,
            status="Normal",
        ),
        VarianceResult(
            account_code="4010", account_name="Service Revenue",
            department="Sales", account_type="revenue",
            budget=Decimal("320000"), actual=Decimal("295000"),
            variance_amount=Decimal("-25000"), variance_pct=Decimal("-7.81"),
            favorability="unfavorable", is_material=False,
            status="Normal",
        ),
        VarianceResult(
            account_code="5030", account_name="Hosting & Infrastructure",
            department="Engineering", account_type="cogs",
            budget=Decimal("125000"), actual=Decimal("155000"),
            variance_amount=Decimal("30000"), variance_pct=Decimal("24.00"),
            favorability="unfavorable", is_material=True,
            status="Normal",
        ),
        VarianceResult(
            account_code="6050", account_name="R&D Prototype Costs",
            department="R&D", account_type="expense",
            budget=Decimal("0"), actual=Decimal("15000"),
            variance_amount=Decimal("15000"), variance_pct=None,
            favorability="unfavorable", is_material=False,
            status="Zero Budget",
        ),
        VarianceResult(
            account_code="8060", account_name="Legal Fees",
            department="G&A", account_type="expense",
            budget=Decimal("40000"), actual=Decimal("72000"),
            variance_amount=Decimal("32000"), variance_pct=Decimal("80.00"),
            favorability="unfavorable", is_material=True,
            status="Normal",
        ),
    ]
