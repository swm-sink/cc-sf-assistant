"""
Unit tests for consolidation workflow.

Tests multi-department consolidation, Decimal conversion, and metadata generation.
"""

import pytest
import pandas as pd
from pathlib import Path
from decimal import Decimal
from unittest.mock import patch, MagicMock

from src.core.consolidation import (
    convert_amounts_to_decimal,
    consolidate_departments,
    ConsolidationError
)


class TestConvertAmountsToDecimal:
    """Test Decimal conversion for financial amounts."""

    def test_converts_amount_columns_to_decimal(self):
        """Test automatic detection and conversion of amount columns."""
        df = pd.DataFrame({
            'account': ['A001', 'A002'],
            'amount': [100.50, 200.75],
            'budget_amount': [110.00, 190.00]
        })

        result = convert_amounts_to_decimal(df)

        # Check Decimal type
        assert isinstance(result.iloc[0]['amount'], Decimal)
        assert isinstance(result.iloc[0]['budget_amount'], Decimal)

        # Check values preserved
        assert result.iloc[0]['amount'] == Decimal('100.50')
        assert result.iloc[1]['budget_amount'] == Decimal('190.00')

    def test_handles_null_values(self):
        """Test NULL values preserved during conversion."""
        df = pd.DataFrame({
            'amount': [100.50, None, 200.75]
        })

        result = convert_amounts_to_decimal(df)

        assert isinstance(result.iloc[0]['amount'], Decimal)
        assert result.iloc[1]['amount'] is None
        assert isinstance(result.iloc[2]['amount'], Decimal)

    def test_explicit_column_list(self):
        """Test conversion with explicitly specified columns."""
        df = pd.DataFrame({
            'revenue': [1000.00, 2000.00],
            'cost': [500.00, 750.00],
            'other': [10, 20]
        })

        result = convert_amounts_to_decimal(df, amount_columns=['revenue', 'cost'])

        # revenue and cost converted
        assert isinstance(result.iloc[0]['revenue'], Decimal)
        assert isinstance(result.iloc[0]['cost'], Decimal)

        # other NOT converted (not in list)
        assert not isinstance(result.iloc[0]['other'], Decimal)

    def test_preserves_decimal_precision(self):
        """Test no precision loss during conversion."""
        df = pd.DataFrame({
            'amount': [0.01, 0.02, 0.03]
        })

        result = convert_amounts_to_decimal(df)

        # Verify exact decimal precision
        assert result.iloc[0]['amount'] == Decimal('0.01')
        assert result.iloc[1]['amount'] == Decimal('0.02')
        assert result.iloc[2]['amount'] == Decimal('0.03')

        # Verify sum is exact (not 0.060000000000000005)
        total = sum(result['amount'])
        assert total == Decimal('0.06')

    def test_negative_amounts(self):
        """Test negative amounts (liabilities, contra-accounts)."""
        df = pd.DataFrame({
            'amount': [-1000.50, -500.25]
        })

        result = convert_amounts_to_decimal(df)

        assert result.iloc[0]['amount'] == Decimal('-1000.50')
        assert result.iloc[1]['amount'] == Decimal('-500.25')

    def test_zero_amounts(self):
        """Test zero amounts handled correctly."""
        df = pd.DataFrame({
            'amount': [0, 0.00, 0.0]
        })

        result = convert_amounts_to_decimal(df)

        assert result.iloc[0]['amount'] == Decimal('0')
        assert result.iloc[1]['amount'] == Decimal('0.00')
        assert result.iloc[2]['amount'] == Decimal('0.0')


class TestConsolidateDepartments:
    """Test main consolidation workflow."""

    @patch('src.core.consolidation.discover_excel_files')
    @patch('src.core.consolidation.validate_department_file')
    @patch('pandas.read_excel')
    def test_successful_consolidation(
        self,
        mock_read_excel,
        mock_validate,
        mock_discover
    ):
        """Test successful multi-file consolidation."""
        # Setup mocks
        file1 = Path('sales.xlsx')
        file2 = Path('ops.xlsx')
        mock_discover.return_value = [file1, file2]
        mock_validate.return_value = (True, [])

        # Mock DataFrame returns
        df1 = pd.DataFrame({
            'account_code': ['SALES001'],
            'amount': [100.0]
        })
        df2 = pd.DataFrame({
            'account_code': ['OPS001'],
            'amount': [200.0]
        })

        mock_read_excel.side_effect = [df1, df2]

        # Execute
        mapping = {'SALES001': '4000', 'OPS001': '6000'}
        required_cols = ['account_code', 'amount']

        consolidated, metadata = consolidate_departments(
            'data/input',
            mapping,
            required_cols
        )

        # Verify
        assert len(consolidated) == 2
        assert metadata['success'] is True
        assert metadata['file_count'] == 2
        assert metadata['total_records'] == 2
        assert metadata['unmapped_count'] == 0

    @patch('src.core.consolidation.discover_excel_files')
    def test_no_files_raises_error(self, mock_discover):
        """Test error when no Excel files found."""
        mock_discover.return_value = []

        with pytest.raises(ConsolidationError, match="No Excel files found"):
            consolidate_departments(
                'empty_folder',
                {},
                ['account_code']
            )

    @patch('src.core.consolidation.discover_excel_files')
    @patch('src.core.consolidation.validate_department_file')
    @patch('pandas.read_excel')
    def test_unmapped_accounts_tracked(
        self,
        mock_read_excel,
        mock_validate,
        mock_discover
    ):
        """Test unmapped accounts flagged in metadata."""
        file1 = Path('sales.xlsx')
        mock_discover.return_value = [file1]
        mock_validate.return_value = (True, [])

        df = pd.DataFrame({
            'account_code': ['SALES001', 'UNKNOWN999'],
            'amount': [100.0, 200.0]
        })
        mock_read_excel.return_value = df

        mapping = {'SALES001': '4000'}  # UNKNOWN999 not in mapping
        required_cols = ['account_code', 'amount']

        consolidated, metadata = consolidate_departments(
            'data/input',
            mapping,
            required_cols
        )

        # Verify unmapped tracking
        assert metadata['unmapped_count'] == 1
        assert 'sales.xlsx' in metadata['unmapped_accounts_by_file']
        assert 'UNKNOWN999' in metadata['unmapped_accounts_by_file']['sales.xlsx']

    @patch('src.core.consolidation.discover_excel_files')
    @patch('src.core.consolidation.validate_department_file')
    def test_validation_failures_tracked(self, mock_validate, mock_discover):
        """Test validation failures tracked in metadata."""
        file1 = Path('bad.xlsx')
        mock_discover.return_value = [file1]
        mock_validate.return_value = (False, ['Missing column: account_code'])

        mapping = {}
        required_cols = ['account_code', 'amount']

        with pytest.raises(ConsolidationError, match="No valid files"):
            consolidate_departments(
                'data/input',
                mapping,
                required_cols
            )
