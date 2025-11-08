"""
Account code mapping for department consolidation.

Maps department-specific account codes to corporate chart of accounts.
Tracks unmapped accounts for reconciliation.
"""

from typing import Dict, List, Tuple
import pandas as pd

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class AccountMappingError(Exception):
    """Raised when account mapping fails."""
    pass


def map_account_codes(
    department_df: pd.DataFrame,
    mapping_config: Dict[str, str],
    source_column: str = 'account_code',
    target_column: str = 'corporate_account'
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Map department account codes to corporate chart of accounts.

    Args:
        department_df: DataFrame with department data
        mapping_config: Dict mapping dept codes to corporate codes
        source_column: Column containing department account codes
        target_column: Name for new column with corporate codes

    Returns:
        Tuple of (mapped_dataframe, list_of_unmapped_accounts)

    Raises:
        AccountMappingError: If source column missing

    Example:
        >>> df = pd.DataFrame({'account_code': ['SALES001', 'RENT001']})
        >>> mapping = {'SALES001': '4000', 'RENT001': '6100'}
        >>> mapped_df, unmapped = map_account_codes(df, mapping)
        >>> assert 'corporate_account' in mapped_df.columns
    """
    if source_column not in department_df.columns:
        raise AccountMappingError(
            f"Source column '{source_column}' not found in DataFrame"
        )

    # Create copy to avoid modifying original
    df = department_df.copy()

    # Map account codes
    df[target_column] = df[source_column].map(mapping_config)

    # Identify unmapped accounts
    unmapped_mask = df[target_column].isna()
    unmapped_accounts = df.loc[unmapped_mask, source_column].unique().tolist()

    if unmapped_accounts:
        logger.warning(
            f"Found {len(unmapped_accounts)} unmapped account codes",
            extra={'unmapped': unmapped_accounts}
        )
    else:
        logger.info("All account codes successfully mapped")

    return df, unmapped_accounts


def create_reconciliation_report(
    unmapped_by_file: Dict[str, List[str]]
) -> pd.DataFrame:
    """
    Create reconciliation report for unmapped accounts.

    Args:
        unmapped_by_file: Dict mapping filenames to unmapped account lists

    Returns:
        DataFrame with columns: source_file, unmapped_account, status

    Example:
        >>> unmapped = {
        ...     'sales.xlsx': ['SALES999'],
        ...     'marketing.xlsx': ['MKT999']
        ... }
        >>> report = create_reconciliation_report(unmapped)
        >>> assert len(report) == 2
    """
    records = []

    for file_name, unmapped_accounts in unmapped_by_file.items():
        for account in unmapped_accounts:
            records.append({
                'source_file': file_name,
                'unmapped_account': account,
                'status': 'Needs Mapping'
            })

    if not records:
        # No unmapped accounts
        return pd.DataFrame(columns=['source_file', 'unmapped_account', 'status'])

    df = pd.DataFrame(records)

    logger.info(
        f"Created reconciliation report with {len(df)} unmapped accounts"
    )

    return df


def validate_mapping_config(
    mapping_config: Dict[str, str]
) -> List[str]:
    """
    Validate account mapping configuration.

    Args:
        mapping_config: Mapping dict to validate

    Returns:
        List of validation issues (empty if valid)

    Example:
        >>> mapping = {'SALES001': '4000', 'SALES002': None}
        >>> issues = validate_mapping_config(mapping)
        >>> # Returns issues about None values
    """
    issues = []

    if not mapping_config:
        issues.append("Mapping configuration is empty")
        return issues

    # Check for None or empty values
    invalid_mappings = {
        k: v for k, v in mapping_config.items()
        if v is None or (isinstance(v, str) and not v.strip())
    }

    if invalid_mappings:
        issues.append(
            f"Found {len(invalid_mappings)} invalid mapping values: "
            f"{list(invalid_mappings.keys())[:5]}"
        )

    # Check for duplicate target codes (multiple dept codes → same corporate code)
    # This is actually valid, but we log it for awareness
    reverse_mapping = {}
    duplicates = []

    for dept_code, corp_code in mapping_config.items():
        if corp_code in reverse_mapping:
            duplicates.append(
                f"{dept_code} and {reverse_mapping[corp_code]} both map to {corp_code}"
            )
        else:
            reverse_mapping[corp_code] = dept_code

    if duplicates:
        logger.info(
            f"Note: {len(duplicates)} corporate codes have multiple department mappings",
            extra={'examples': duplicates[:3]}
        )

    return issues


def merge_department_data(
    mapped_dataframes: List[Tuple[str, pd.DataFrame]],
    consolidation_column: str = 'corporate_account'
) -> pd.DataFrame:
    """
    Merge multiple department DataFrames into single dataset.

    Args:
        mapped_dataframes: List of (filename, dataframe) tuples
        consolidation_column: Column present in all dataframes (for reference)

    Returns:
        Consolidated DataFrame with all records from input files

    Example:
        >>> df1 = pd.DataFrame({
        ...     'corporate_account': ['4000', '6000'],
        ...     'amount': [100, 200]
        ... })
        >>> df2 = pd.DataFrame({
        ...     'corporate_account': ['4000', '6100'],
        ...     'amount': [150, 300]
        ... })
        >>> consolidated = merge_department_data([
        ...     ('sales.xlsx', df1),
        ...     ('ops.xlsx', df2)
        ... ])
    """
    if not mapped_dataframes:
        raise AccountMappingError("No dataframes provided for consolidation")

    # Concatenate all dataframes with source tracking
    all_data = []

    for file_name, df in mapped_dataframes:
        df_copy = df.copy()
        df_copy['source_file'] = file_name
        all_data.append(df_copy)

    consolidated = pd.concat(all_data, ignore_index=True)

    logger.info(
        f"Consolidated {len(mapped_dataframes)} files into "
        f"{len(consolidated)} total records"
    )

    return consolidated
