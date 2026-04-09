"""Tests for favorability determination."""

from decimal import Decimal

import pytest

from scripts.core.favorability import determine_favorability, get_favorability_direction
from scripts.utils.types import InvalidAccountTypeError


class TestFavorability:
    def test_revenue_favorable(self):
        assert determine_favorability(Decimal("10000"), "revenue") == "favorable"

    def test_revenue_unfavorable(self):
        assert determine_favorability(Decimal("-10000"), "revenue") == "unfavorable"

    def test_expense_favorable(self):
        """Lower actual = negative variance = favorable for expenses."""
        assert determine_favorability(Decimal("-5000"), "expense") == "favorable"

    def test_expense_unfavorable(self):
        assert determine_favorability(Decimal("5000"), "expense") == "unfavorable"

    def test_asset_favorable(self):
        assert determine_favorability(Decimal("1000"), "asset") == "favorable"

    def test_asset_unfavorable(self):
        assert determine_favorability(Decimal("-1000"), "asset") == "unfavorable"

    def test_liability_favorable(self):
        assert determine_favorability(Decimal("-2000"), "liability") == "favorable"

    def test_liability_unfavorable(self):
        assert determine_favorability(Decimal("2000"), "liability") == "unfavorable"

    def test_cogs_favorable(self):
        """COGS behaves like expense: lower is favorable."""
        assert determine_favorability(Decimal("-3000"), "cogs") == "favorable"

    def test_cogs_unfavorable(self):
        assert determine_favorability(Decimal("3000"), "cogs") == "unfavorable"

    def test_zero_variance_neutral(self):
        assert determine_favorability(Decimal("0"), "revenue") == "neutral"
        assert determine_favorability(Decimal("0"), "expense") == "neutral"

    def test_invalid_account_type_raises(self):
        with pytest.raises(InvalidAccountTypeError):
            determine_favorability(Decimal("100"), "invalid_type")


class TestFavorabilityDirection:
    def test_revenue_direction(self):
        assert get_favorability_direction("revenue") == "higher_is_favorable"

    def test_expense_direction(self):
        assert get_favorability_direction("expense") == "lower_is_favorable"

    def test_invalid_type_raises(self):
        with pytest.raises(InvalidAccountTypeError):
            get_favorability_direction("bogus")
