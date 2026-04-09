"""Tests for data validation utilities."""

from decimal import Decimal

import pandas as pd

from scripts.utils.validator import (
    convert_amount_to_decimal,
    reconcile_datasets,
    validate_dataframe_structure,
    validate_decimal_column,
    validate_no_nulls,
)


class TestValidateStructure:
    def test_pass(self):
        df = pd.DataFrame({"Account Code": ["4000"], "Amount": [100]})
        valid, issues = validate_dataframe_structure(df, ["Account Code", "Amount"])
        assert valid is True
        assert issues == []

    def test_missing_columns(self):
        df = pd.DataFrame({"Account Code": ["4000"]})
        valid, issues = validate_dataframe_structure(df, ["Account Code", "Amount"])
        assert valid is False
        assert len(issues) == 1


class TestValidateDecimalColumn:
    def test_valid_numbers(self):
        df = pd.DataFrame({"Amount": ["100.50", "200", "300.00"]})
        valid, issues = validate_decimal_column(df, "Amount")
        assert valid is True

    def test_invalid_values(self):
        df = pd.DataFrame({"Amount": ["100", "abc", "300"]})
        valid, issues = validate_decimal_column(df, "Amount")
        assert valid is False
        assert len(issues) == 1

    def test_missing_column(self):
        df = pd.DataFrame({"Other": [1]})
        valid, issues = validate_decimal_column(df, "Amount")
        assert valid is False


class TestValidateNoNulls:
    def test_no_nulls(self):
        df = pd.DataFrame({"Amount": [100, 200, 300]})
        valid, issues = validate_no_nulls(df, ["Amount"])
        assert valid is True

    def test_with_nulls(self):
        df = pd.DataFrame({"Amount": [100, None, 300]})
        valid, issues = validate_no_nulls(df, ["Amount"])
        assert valid is False
        assert "NULL" in issues[0]


class TestConvertToDecimal:
    def test_from_int(self):
        assert convert_amount_to_decimal(100) == Decimal("100")

    def test_from_float(self):
        result = convert_amount_to_decimal(100.50)
        assert isinstance(result, Decimal)

    def test_from_string(self):
        assert convert_amount_to_decimal("100.50") == Decimal("100.50")

    def test_none_returns_none(self):
        assert convert_amount_to_decimal(None) is None

    def test_invalid_returns_none(self):
        assert convert_amount_to_decimal("not_a_number") is None


class TestReconcileDatasets:
    def test_full_match(self):
        budget = pd.DataFrame({"code": ["4000", "5000"]})
        actuals = pd.DataFrame({"code": ["4000", "5000"]})
        result = reconcile_datasets(budget, actuals, "code")
        assert result["fully_matched"] is True
        assert result["match_count"] == 2

    def test_partial_match(self):
        budget = pd.DataFrame({"code": ["4000", "5000", "6000"]})
        actuals = pd.DataFrame({"code": ["4000", "5000", "7000"]})
        result = reconcile_datasets(budget, actuals, "code")
        assert result["fully_matched"] is False
        assert result["budget_only_count"] == 1
        assert result["actuals_only_count"] == 1
        assert "6000" in result["budget_only"]
        assert "7000" in result["actuals_only"]
