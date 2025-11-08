"""
Unit tests for data validation module.

Tests structure validation, column checking, and data integrity.
"""

import pytest
import pandas as pd
from pathlib import Path
from decimal import Decimal

from src.core.data_validator import (
    validate_required_columns,
    validate_numeric_column,
    validate_date_column,
    DataValidationError
)


class TestValidateRequiredColumns:
    """Test required column validation."""

    def test_all_columns_present(self):
        """Test validation passes when all required columns exist."""
        df = pd.DataFrame({
            'account_code': ['A001', 'A002'],
            'account_name': ['Sales', 'Rent'],
            'amount': [100, 200]
        })

        issues = validate_required_columns(
            df,
            ['account_code', 'account_name', 'amount'],
            'test.xlsx'
        )

        assert len(issues) == 0

    def test_missing_columns(self):
        """Test validation fails when columns missing."""
        df = pd.DataFrame({
            'account_code': ['A001'],
            'amount': [100]
        })

        issues = validate_required_columns(
            df,
            ['account_code', 'account_name', 'amount'],
            'test.xlsx'
        )

        assert len(issues) == 1
        assert 'account_name' in issues[0]

    def test_multiple_missing_columns(self):
        """Test multiple missing columns reported."""
        df = pd.DataFrame({
            'account_code': ['A001']
        })

        issues = validate_required_columns(
            df,
            ['account_code', 'amount', 'date'],
            'test.xlsx'
        )

        assert len(issues) == 1
        assert 'amount' in issues[0]
        assert 'date' in issues[0]


class TestValidateNumericColumn:
    """Test numeric column validation."""

    def test_all_numeric_valid(self):
        """Test validation passes for all numeric values."""
        df = pd.DataFrame({
            'amount': [100, 200, 300]
        })

        issues = validate_numeric_column(df, 'amount', allow_null=False)

        assert len(issues) == 0

    def test_numeric_with_nulls_allowed(self):
        """Test validation passes with NaN when allowed."""
        df = pd.DataFrame({
            'amount': [100, None, 300]
        })

        issues = validate_numeric_column(df, 'amount', allow_null=True)

        assert len(issues) == 0

    def test_numeric_with_nulls_disallowed(self):
        """Test validation fails with NaN when not allowed."""
        df = pd.DataFrame({
            'amount': [100, None, 300]
        })

        issues = validate_numeric_column(df, 'amount', allow_null=False)

        assert len(issues) == 1
        assert 'non-numeric' in issues[0].lower()

    def test_non_numeric_values(self):
        """Test validation fails with text values."""
        df = pd.DataFrame({
            'amount': [100, 'invalid', 300]
        })

        issues = validate_numeric_column(df, 'amount', allow_null=False)

        assert len(issues) == 1
        assert '1' in issues[0]  # 1 non-numeric value

    def test_column_not_found(self):
        """Test validation fails gracefully if column missing."""
        df = pd.DataFrame({
            'amount': [100, 200]
        })

        issues = validate_numeric_column(df, 'missing_column')

        assert len(issues) == 1
        assert 'not found' in issues[0].lower()


class TestValidateDateColumn:
    """Test date column validation."""

    def test_valid_dates(self):
        """Test validation passes for valid dates."""
        df = pd.DataFrame({
            'date': ['2025-01-01', '2025-02-01', '2025-03-01']
        })

        issues = validate_date_column(df, 'date')

        assert len(issues) == 0

    def test_invalid_dates(self):
        """Test validation fails for invalid date strings."""
        df = pd.DataFrame({
            'date': ['2025-01-01', 'invalid', '2025-03-01']
        })

        issues = validate_date_column(df, 'date')

        assert len(issues) == 1
        assert '1' in issues[0]  # 1 invalid date

    def test_mixed_date_formats(self):
        """Test validation handles multiple date formats."""
        df = pd.DataFrame({
            'date': ['2025-01-01', '01/15/2025', 'March 1, 2025']
        })

        # pandas should parse all these formats
        issues = validate_date_column(df, 'date')

        assert len(issues) == 0

    def test_column_not_found(self):
        """Test validation fails gracefully if column missing."""
        df = pd.DataFrame({
            'date': ['2025-01-01']
        })

        issues = validate_date_column(df, 'missing_column')

        assert len(issues) == 1
        assert 'not found' in issues[0].lower()
