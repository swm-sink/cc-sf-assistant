"""
Unit tests for account mapping module.

Tests account code mapping, reconciliation, and consolidation.
"""

import pytest
import pandas as pd

from src.core.account_mapper import (
    map_account_codes,
    create_reconciliation_report,
    validate_mapping_config,
    merge_department_data,
    AccountMappingError
)


class TestMapAccountCodes:
    """Test account code mapping functionality."""

    def test_all_accounts_mapped(self):
        """Test successful mapping of all account codes."""
        df = pd.DataFrame({
            'account_code': ['SALES001', 'RENT001', 'SALARIES001'],
            'amount': [100, 200, 300]
        })

        mapping = {
            'SALES001': '4000',
            'RENT001': '6100',
            'SALARIES001': '6000'
        }

        mapped_df, unmapped = map_account_codes(df, mapping)

        assert 'corporate_account' in mapped_df.columns
        assert len(unmapped) == 0
        assert mapped_df.loc[0, 'corporate_account'] == '4000'
        assert mapped_df.loc[1, 'corporate_account'] == '6100'

    def test_some_accounts_unmapped(self):
        """Test handling of unmapped accounts."""
        df = pd.DataFrame({
            'account_code': ['SALES001', 'UNKNOWN999', 'RENT001'],
            'amount': [100, 200, 300]
        })

        mapping = {
            'SALES001': '4000',
            'RENT001': '6100'
        }

        mapped_df, unmapped = map_account_codes(df, mapping)

        assert len(unmapped) == 1
        assert 'UNKNOWN999' in unmapped
        assert pd.isna(mapped_df.loc[1, 'corporate_account'])

    def test_missing_source_column(self):
        """Test error when source column doesn't exist."""
        df = pd.DataFrame({
            'different_column': ['A001']
        })

        mapping = {'A001': '4000'}

        with pytest.raises(AccountMappingError, match="Source column"):
            map_account_codes(df, mapping, source_column='account_code')

    def test_custom_column_names(self):
        """Test mapping with custom column names."""
        df = pd.DataFrame({
            'dept_code': ['SALES001', 'RENT001'],
            'amount': [100, 200]
        })

        mapping = {'SALES001': '4000', 'RENT001': '6100'}

        mapped_df, unmapped = map_account_codes(
            df,
            mapping,
            source_column='dept_code',
            target_column='gl_account'
        )

        assert 'gl_account' in mapped_df.columns
        assert len(unmapped) == 0


class TestCreateReconciliationReport:
    """Test reconciliation report generation."""

    def test_empty_unmapped(self):
        """Test report with no unmapped accounts."""
        unmapped = {}

        report = create_reconciliation_report(unmapped)

        assert len(report) == 0
        assert list(report.columns) == ['source_file', 'unmapped_account', 'status']

    def test_single_file_unmapped(self):
        """Test report with unmapped accounts from one file."""
        unmapped = {
            'sales.xlsx': ['SALES999', 'SALES998']
        }

        report = create_reconciliation_report(unmapped)

        assert len(report) == 2
        assert report.iloc[0]['source_file'] == 'sales.xlsx'
        assert report.iloc[0]['unmapped_account'] == 'SALES999'
        assert report.iloc[0]['status'] == 'Needs Mapping'

    def test_multiple_files_unmapped(self):
        """Test report with unmapped from multiple files."""
        unmapped = {
            'sales.xlsx': ['SALES999'],
            'marketing.xlsx': ['MKT999', 'MKT998']
        }

        report = create_reconciliation_report(unmapped)

        assert len(report) == 3
        assert 'sales.xlsx' in report['source_file'].values
        assert 'marketing.xlsx' in report['source_file'].values


class TestValidateMappingConfig:
    """Test mapping configuration validation."""

    def test_valid_config(self):
        """Test validation passes for valid config."""
        mapping = {
            'SALES001': '4000',
            'RENT001': '6100',
            'SALARIES001': '6000'
        }

        issues = validate_mapping_config(mapping)

        assert len(issues) == 0

    def test_empty_config(self):
        """Test validation fails for empty config."""
        mapping = {}

        issues = validate_mapping_config(mapping)

        assert len(issues) == 1
        assert 'empty' in issues[0].lower()

    def test_none_values(self):
        """Test validation fails for None values."""
        mapping = {
            'SALES001': '4000',
            'SALES002': None,
            'SALES003': ''
        }

        issues = validate_mapping_config(mapping)

        assert len(issues) == 1
        assert 'invalid mapping values' in issues[0].lower()


class TestMergeDepartmentData:
    """Test department data merging."""

    def test_merge_multiple_departments(self):
        """Test merging data from multiple departments."""
        df1 = pd.DataFrame({
            'corporate_account': ['4000', '6000'],
            'amount': [100, 200]
        })

        df2 = pd.DataFrame({
            'corporate_account': ['4000', '6100'],
            'amount': [150, 300]
        })

        merged = merge_department_data([
            ('sales.xlsx', df1),
            ('ops.xlsx', df2)
        ])

        assert len(merged) == 4  # All records preserved
        assert 'source_file' in merged.columns
        assert 'sales.xlsx' in merged['source_file'].values
        assert 'ops.xlsx' in merged['source_file'].values

    def test_empty_list_raises_error(self):
        """Test error when no dataframes provided."""
        with pytest.raises(AccountMappingError, match="No dataframes"):
            merge_department_data([])

    def test_source_file_tracking(self):
        """Test source file is tracked for each record."""
        df1 = pd.DataFrame({
            'corporate_account': ['4000'],
            'amount': [100]
        })

        merged = merge_department_data([('sales.xlsx', df1)])

        assert merged.iloc[0]['source_file'] == 'sales.xlsx'
