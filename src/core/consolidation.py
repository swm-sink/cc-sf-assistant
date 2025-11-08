"""
Multi-department data consolidation workflow.

Consolidates financial data from multiple department Excel files
into single unified dataset with audit trail.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime, UTC
import pandas as pd

from src.utils.file_utils import discover_excel_files, validate_file_exists
from src.utils.logger import setup_logger, create_audit_entry
from src.core.data_validator import validate_department_file
from src.core.account_mapper import (
    map_account_codes,
    create_reconciliation_report,
    merge_department_data
)

logger = setup_logger(__name__)


class ConsolidationError(Exception):
    """Raised when consolidation process fails."""
    pass


def consolidate_departments(
    input_folder: str,
    mapping_config: Dict[str, str],
    required_columns: List[str],
    output_file: str = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Consolidate all department files into single dataset.

    Implements Epic 1, Story 1.1: Multi-Department Data Consolidation

    Args:
        input_folder: Path to folder containing department Excel files
        mapping_config: Dict mapping department codes to corporate codes
        required_columns: List of required column names
        output_file: Optional path to save consolidated output

    Returns:
        Tuple of (consolidated_dataframe, metadata_dict)

    Raises:
        FileNotFoundError: If input folder doesn't exist
        ConsolidationError: If consolidation fails

    Example:
        >>> consolidated, metadata = consolidate_departments(
        ...     'data/input',
        ...     mapping_config={'SALES001': '4000'},
        ...     required_columns=['account_code', 'amount']
        ... )
    """
    logger.info(f"Starting consolidation from folder: {input_folder}")

    # Initialize metadata
    metadata = {
        'start_time': datetime.now(UTC).isoformat(),
        'source_folder': input_folder,
        'source_files': [],
        'records_per_file': {},
        'unmapped_accounts_by_file': {},
        'total_records': 0,
        'validation_issues': {},
        'success': False
    }

    try:
        # Step 1: Discover Excel files
        files = discover_excel_files(input_folder)

        if not files:
            raise ConsolidationError(
                f"No Excel files found in folder: {input_folder}"
            )

        logger.info(f"Found {len(files)} Excel files to consolidate")
        metadata['file_count'] = len(files)

        # Step 2: Validate and load files
        valid_dataframes = []

        for file_path in files:
            file_name = file_path.name
            logger.info(f"Processing file: {file_name}")

            # Validate structure
            is_valid, issues = validate_department_file(
                file_path,
                required_columns
            )

            if not is_valid:
                logger.warning(
                    f"Validation failed for {file_name}: {issues}"
                )
                metadata['validation_issues'][file_name] = issues
                # Continue with other files instead of failing completely
                continue

            # Load file
            try:
                df = pd.read_excel(file_path, engine='openpyxl')

                metadata['source_files'].append(str(file_path))
                metadata['records_per_file'][file_name] = len(df)

                valid_dataframes.append((file_name, df))

                logger.info(
                    f"Loaded {file_name}: {len(df)} records"
                )

            except Exception as e:
                logger.error(f"Failed to load {file_name}: {e}")
                metadata['validation_issues'][file_name] = [str(e)]
                continue

        if not valid_dataframes:
            raise ConsolidationError(
                "No valid files to consolidate. Check validation_issues in metadata."
            )

        # Step 3: Map account codes
        mapped_dataframes = []

        for file_name, df in valid_dataframes:
            mapped_df, unmapped = map_account_codes(
                df,
                mapping_config,
                source_column='account_code',
                target_column='corporate_account'
            )

            if unmapped:
                metadata['unmapped_accounts_by_file'][file_name] = unmapped

            mapped_dataframes.append((file_name, mapped_df))

        # Step 4: Merge all dataframes
        consolidated = merge_department_data(
            mapped_dataframes,
            consolidation_column='corporate_account'
        )

        metadata['total_records'] = len(consolidated)

        # Step 5: Create reconciliation report if unmapped accounts exist
        if metadata['unmapped_accounts_by_file']:
            reconciliation = create_reconciliation_report(
                metadata['unmapped_accounts_by_file']
            )
            metadata['unmapped_count'] = len(reconciliation)

            logger.warning(
                f"Consolidation complete with {len(reconciliation)} unmapped accounts"
            )
        else:
            logger.info("Consolidation complete - all accounts mapped")
            metadata['unmapped_count'] = 0

        # Step 6: Save output if path provided
        if output_file:
            from src.utils.file_utils import ensure_output_directory

            output_path = ensure_output_directory(output_file)

            consolidated.to_excel(output_path, index=False, engine='openpyxl')

            logger.info(f"Consolidated data saved to: {output_file}")
            metadata['output_file'] = output_file

        # Finalize metadata
        metadata['end_time'] = datetime.now(UTC).isoformat()
        metadata['success'] = True

        # Create audit trail entry
        audit_entry = create_audit_entry(
            operation='department_consolidation',
            source_files=metadata['source_files'],
            output_file=output_file,
            records_processed=metadata['total_records'],
            files_processed=len(valid_dataframes),
            unmapped_accounts=metadata['unmapped_count']
        )

        logger.info("Consolidation completed successfully", extra=audit_entry)

        return consolidated, metadata

    except Exception as e:
        metadata['end_time'] = datetime.now(UTC).isoformat()
        metadata['error'] = str(e)
        metadata['success'] = False

        logger.error(f"Consolidation failed: {e}", extra=metadata)

        raise ConsolidationError(f"Consolidation failed: {e}") from e
