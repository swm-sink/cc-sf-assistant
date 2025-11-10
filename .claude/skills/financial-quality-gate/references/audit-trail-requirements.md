# Audit Trail Requirements Reference

**Purpose:** SOX compliance, what to log, structured format, retention policy, search/retrieval.

---

## Why Audit Trails Are Mandatory

### SOX Compliance (Sarbanes-Oxley Act)

**Legal Requirement:** Public companies must maintain audit trails for financial data transformations.

**Key Provisions:**
- **Section 302:** Management certification of financial controls
- **Section 404:** Internal control assessment (includes data lineage)
- **Section 802:** Document retention (7 years minimum)

**Penalties for Non-Compliance:**
- Fines: Up to $5 million
- Prison: Up to 20 years
- Loss of investor confidence

---

## What to Log

### Every Data Transformation Must Log

**Transformation Definition:** Any operation that creates, modifies, or combines financial data.

**Examples:**
- Merging budget and actuals files
- Calculating variance (budget - actual)
- Aggregating account-level data to department level
- Converting currencies
- Applying adjustments or accruals
- Generating reports from source data

### Required Log Fields

**Minimum Required Information:**

1. **Timestamp** (ISO 8601 format with timezone)
   - Example: `2025-11-10T14:23:45.123456+00:00`
   - Why: Establish sequence of events

2. **User** (or 'system' for automated processes)
   - Example: `john.doe` or `system`
   - Why: Accountability and authorization tracking

3. **Operation** (function/script name)
   - Example: `consolidate_actuals`, `calculate_variance`
   - Why: Understand what transformation occurred

4. **Source File(s)** (if applicable)
   - Example: `budget_2025.xlsx`, `actuals_q1.csv`
   - Why: Data lineage and dependency tracking

5. **Target File** (if applicable)
   - Example: `variance_report_2025_q1.xlsx`
   - Why: Output tracking and version control

6. **Record Count** (optional but recommended)
   - Example: `1,234 records processed`
   - Why: Validation and completeness checking

---

## Structured Log Format

### Standard Format Template

```
{timestamp} | {user} | {operation} | {source_files} → {target_file} | {metadata}
```

**Example:**
```
2025-11-10T14:23:45.123456+00:00 | john.doe | consolidate_actuals | budget_2025.xlsx + actuals_q1.csv → variance_report.xlsx | 1234 records
```

---

## Implementation Patterns

### Python Logging Framework

```python
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',  # We provide our own format
    handlers=[
        logging.FileHandler('config/audit.log', mode='a'),
        logging.StreamHandler()  # Also print to console
    ]
)

logger = logging.getLogger(__name__)


def log_transformation(
    operation: str,
    source_files: list[str] | None = None,
    target_file: str | None = None,
    metadata: dict | None = None
) -> None:
    """Log a data transformation for audit trail.

    Args:
        operation: Name of operation (function name)
        source_files: List of source file paths
        target_file: Target file path
        metadata: Additional metadata (record count, etc.)
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    user = os.getenv('USER', 'system')

    # Format source files
    sources = ''
    if source_files:
        sources = ' + '.join(source_files)

    # Format target
    target = ''
    if target_file:
        target = f' → {target_file}'

    # Format metadata
    meta = ''
    if metadata:
        meta = ' | ' + ', '.join(f'{k}={v}' for k, v in metadata.items())

    # Construct log message
    log_msg = f'{timestamp} | {user} | {operation}'
    if sources:
        log_msg += f' | {sources}'
    if target:
        log_msg += target
    if meta:
        log_msg += meta

    logger.info(log_msg)


# Example usage
def consolidate_actuals(budget_file: str, actuals_file: str, output_file: str) -> None:
    """Consolidate budget and actuals with audit logging."""

    log_transformation(
        operation='consolidate_actuals',
        source_files=[budget_file, actuals_file],
        target_file=output_file
    )

    # Transformation logic here
    # ...

    # Log completion with metadata
    log_transformation(
        operation='consolidate_actuals',
        source_files=[budget_file, actuals_file],
        target_file=output_file,
        metadata={'records': 1234, 'status': 'complete'}
    )
```

---

## Retention Policy

### SOX Requirements: 7 Years

**Configuration:**

```python
# config/logging_config.py
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_audit_logging():
    """Configure audit logging with retention policy."""

    # Create handler with 7-year retention (2,555 days)
    handler = TimedRotatingFileHandler(
        filename='config/audit.log',
        when='D',  # Daily rotation
        interval=1,
        backupCount=2555,  # 7 years * 365 days
        encoding='utf-8'
    )

    # Structured format
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)

    # Configure root logger
    logger = logging.getLogger('audit')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger
```

---

## Search and Retrieval

### Common Audit Queries

**1. Find all transformations by user:**

```bash
grep "john.doe" config/audit.log
```

**2. Find all operations on a specific file:**

```bash
grep "budget_2025.xlsx" config/audit.log
```

**3. Find transformations in date range:**

```bash
grep "2025-11-" config/audit.log | grep "2025-11-0[1-5]"
```

**4. Find failed operations (if logging errors):**

```bash
grep "ERROR" config/audit.log
```

### Python Search Utilities

```python
from datetime import datetime, timezone
from pathlib import Path


def search_audit_log(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    user: str | None = None,
    operation: str | None = None,
    file_pattern: str | None = None
) -> list[str]:
    """Search audit log with filters.

    Args:
        start_date: Filter entries after this date
        end_date: Filter entries before this date
        user: Filter by user
        operation: Filter by operation name
        file_pattern: Filter by file name pattern

    Returns:
        List of matching log entries
    """
    matches = []

    with open('config/audit.log', 'r') as f:
        for line in f:
            parts = line.strip().split(' | ')
            if len(parts) < 3:
                continue

            timestamp_str, log_user, log_operation = parts[0], parts[1], parts[2]

            # Parse timestamp
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
            except ValueError:
                continue

            # Apply filters
            if start_date and timestamp < start_date:
                continue
            if end_date and timestamp > end_date:
                continue
            if user and log_user != user:
                continue
            if operation and operation not in log_operation:
                continue
            if file_pattern and file_pattern not in line:
                continue

            matches.append(line.strip())

    return matches


# Example usage
from datetime import timedelta

# Find all transformations by john.doe in last 7 days
recent = search_audit_log(
    start_date=datetime.now(timezone.utc) - timedelta(days=7),
    user='john.doe'
)
```

---

## Integration with Existing Scripts

### Decorator Pattern (Recommended)

```python
import functools
from typing import Callable, Any


def audit_logged(operation_name: str | None = None):
    """Decorator to automatically log function calls.

    Args:
        operation_name: Override operation name (default: function name)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            op_name = operation_name or func.__name__

            # Extract file arguments (simple heuristic)
            source_files = []
            target_file = None

            for arg in args:
                if isinstance(arg, (str, Path)) and str(arg).endswith(('.xlsx', '.csv', '.json')):
                    source_files.append(str(arg))

            if 'output_file' in kwargs:
                target_file = kwargs['output_file']

            # Log start
            log_transformation(
                operation=op_name,
                source_files=source_files if source_files else None,
                target_file=target_file,
                metadata={'status': 'started'}
            )

            try:
                # Execute function
                result = func(*args, **kwargs)

                # Log success
                log_transformation(
                    operation=op_name,
                    source_files=source_files if source_files else None,
                    target_file=target_file,
                    metadata={'status': 'success'}
                )

                return result

            except Exception as e:
                # Log failure
                log_transformation(
                    operation=op_name,
                    source_files=source_files if source_files else None,
                    target_file=target_file,
                    metadata={'status': 'failed', 'error': str(e)}
                )
                raise

        return wrapper
    return decorator


# Example usage
@audit_logged()
def consolidate_actuals(budget_file: str, actuals_file: str, output_file: str) -> None:
    """Consolidate budget and actuals (automatically logged)."""
    # Transformation logic
    pass
```

---

## Common Pitfalls

### 1. Logging Too Much

**Problem:** Logging every row operation creates gigabyte-sized logs.

**Solution:** Log transformations, not individual records.

```python
# ❌ WRONG: Log every row
for row in data:
    logger.info(f"Processing {row}")  # Millions of log entries!

# ✅ CORRECT: Log transformation summary
logger.info(f"Processing {len(data)} rows from {source_file}")
```

### 2. Missing Source Files

**Problem:** Logs operation but not which files were used.

**Solution:** Always log source and target files.

```python
# ❌ WRONG: No source tracking
logger.info(f"Calculated variance")

# ✅ CORRECT: Full lineage
logger.info(f"Calculated variance | budget.xlsx + actuals.xlsx → variance.xlsx")
```

### 3. No Timezone Information

**Problem:** Ambiguous timestamps (EST vs UTC?).

**Solution:** Always use UTC with timezone marker.

```python
# ❌ WRONG: Naive datetime
timestamp = datetime.now().isoformat()  # No timezone

# ✅ CORRECT: UTC with timezone
timestamp = datetime.now(timezone.utc).isoformat()  # 2025-11-10T14:23:45+00:00
```

---

## Validation Checklist

Before deploying a transformation script:

- [ ] Logging framework configured (config/audit.log)
- [ ] `log_transformation()` called at start of operation
- [ ] Source file(s) logged
- [ ] Target file logged (if applicable)
- [ ] Timestamp in ISO 8601 UTC format
- [ ] User identified (or 'system')
- [ ] 7-year retention configured
- [ ] Log file append-only (not overwritten)
- [ ] Search utilities available for auditors

---

**Lines:** 298
**Last Updated:** 2025-11-10
