# fpa-core

**Purpose:** Core FP&A business logic - pure calculations and data transformations.

## Responsibilities

- Variance calculations (Actual - Budget, favorability logic)
- Data consolidation algorithms
- Forecast rolling logic
- Financial metrics (materiality flagging, thresholds)

## Key Principle

**No I/O, no external APIs, pure functions.** This package contains only business logic that can be tested independently without network calls or file system access.

## Dependencies

- **pandas** - Data manipulation
- **py-money** (optional) - Decimal precision money handling
- Python's built-in `decimal` module for financial calculations

## Financial Precision Requirements

All currency calculations MUST use `Decimal` type, never `float`.

```python
from decimal import Decimal

# ✅ CORRECT
budget = Decimal('100000.00')
actual = Decimal('115000.00')
variance = actual - budget  # Exact: Decimal('15000.00')

# ❌ INCORRECT
budget = 100000.00  # float - causes rounding errors
```

## Structure

```
src/fpa_core/
├── consolidation/      # Multi-department data consolidation
├── variance/           # Variance analysis & favorability
├── forecasting/        # Rolling forecast maintenance
└── reporting/          # Report generation orchestration
```

(Subdirectories will be created during implementation phase after spec approval)
