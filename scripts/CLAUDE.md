# Python Scripts - Behavioral Overrides

**Purpose:** Component-specific behavior for Python scripts.

**Inherits:** Root CLAUDE.md (all core principles apply)

**Overrides:** This file takes precedence for scripts/** work

---

## Financial Precision Requirements

**Decimal Type Mandatory:**
- ALL currency calculations use `from decimal import Decimal`
- NEVER use float or double for currency/percentages
- Rationale: Float causes rounding errors (0.1 + 0.2 ≠ 0.3)

**Rounding:**
- Only at display/storage layer, NEVER intermediate calculations
- Use `Decimal.quantize()` with `ROUND_HALF_UP` for currency
- Division by zero: Handle explicitly, document in business logic

**Example:**
```python
from decimal import Decimal, ROUND_HALF_UP

# ✅ CORRECT
budget = Decimal('100.00')
actual = Decimal('150.00')
variance = actual - budget  # Decimal('50.00')

# Display rounding
variance_display = variance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# ❌ WRONG
budget = 100.0  # float causes precision errors
actual = 150.0
variance = actual - budget
```

---

## Audit Trail Mandates

**Every Data Transformation Must Log:**
- Timestamp (ISO 8601 format)
- User (or 'system')
- Source file(s)
- Operation performed
- Target file (if applicable)

**Example:**
```python
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def transform_data(source_file: str, target_file: str) -> None:
    """Transform data with audit logging."""
    timestamp = datetime.now(timezone.utc).isoformat()
    logger.info(
        f"{timestamp} | {os.getenv('USER', 'system')} | "
        f"transform_data | {source_file} → {target_file}"
    )
    # Transformation logic
```

**Audit Log Location:** `config/audit.log`

**Requirements:**
- Calculations must be reproducible (same inputs = same outputs)
- Metadata required: source files used, thresholds applied, generation timestamp

---

## Type Safety Enforcement

**Type Hints Mandatory:**
- Type hints on ALL functions (parameters, returns, exceptions)
- Use typing module: `Optional`, `List`, `Dict`, `Literal`, etc.
- No `Any` types without justification

**Example:**
```python
from typing import Optional
from decimal import Decimal

def calculate_variance(
    actual: Decimal,
    budget: Decimal,
    account_type: Literal['revenue', 'expense']
) -> tuple[Decimal, Optional[float], str]:
    """Calculate variance with percentage and favorability.

    Args:
        actual: Actual amount (Decimal for precision)
        budget: Budget amount (Decimal for precision)
        account_type: Account classification

    Returns:
        Tuple of (variance, variance_pct, favorability)

    Raises:
        ValueError: If account_type not 'revenue' or 'expense'
    """
    pass
```

---

## Error Handling

**Explicit Exceptions:**
- Custom exceptions for domain errors
- User-friendly error messages (not stack traces for expected errors)
- Log all errors with context (file, line, inputs)
- NEVER fail silently

**Example:**
```python
class InvalidAccountTypeError(ValueError):
    """Raised when account type is not recognized."""
    pass

def calculate_favorability(variance: Decimal, account_type: str) -> str:
    """Determine favorability based on account type."""
    if account_type not in ('revenue', 'expense', 'asset', 'liability'):
        raise InvalidAccountTypeError(
            f"Unknown account type '{account_type}'. "
            f"Expected: revenue, expense, asset, or liability"
        )
    # Logic
```

---

## Data Integrity

**Validation:**
- Validate all inputs before processing (column presence, data types, non-null requirements)
- Flag anomalies, never silently drop data
- Reconciliation reports for unmatched accounts
- Version control for output files (never overwrite without backup)

---

## Documentation Requirements

**Docstrings:**
- Purpose, parameters, returns, raises, examples
- Update spec.md if business rules discovered during implementation

**Inline Comments:**
- For complex business logic only (not obvious code)

---

## Performance Considerations

**Chunking:**
- If dataset >1000 rows, consider chunking
- Use `pandas.read_csv(chunksize=1000)` or similar
- Document performance expectations: [TO BE MEASURED] until tested

**Optimization:**
- No premature optimization
- Profile before optimizing, measure after

---

## Architecture Principles

**Separation of Concerns:**

**1. Pure Business Logic (scripts/core/)**
- Core FP&A calculations (variance, consolidation, forecasting)
- NO I/O, NO external APIs, pure functions
- Example: `calculate_variance(actual: Decimal, budget: Decimal, account_type: str) -> VarianceResult`

**2. External System Adapters (scripts/integrations/)**
- Abstract external services (Adaptive, Databricks, Google)
- Adapters pattern - swap implementations without changing core
- Example: `AdaptiveClient`, `DatabricksClient`, `GoogleSheetsClient`

**3. Orchestration & Human-in-Loop (scripts/workflows/)**
- Coordinate multi-step processes with human approval checkpoints
- Depends on core + integrations

---

**Precedence:** This config overrides root CLAUDE.md for scripts/**
**Inherits:** All root principles (DRY, chain of verification, RPIV workflow)
