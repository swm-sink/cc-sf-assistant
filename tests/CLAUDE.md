# Tests - Behavioral Overrides

**Purpose:** Component-specific behavior for tests/ directory.

**Inherits:** Root CLAUDE.md (all core principles apply)

**Overrides:** This file takes precedence for tests/** work

---

## Testing Standards

**Financial Calculations:**
- Unit tests with edge cases (zero budget, negative values, NULL handling)
- Precision verification: Test decimal accuracy to 2+ decimal places
- Integration tests with realistic data volumes (50-200 accounts typical)
- Regression tests: Ensure calculation changes don't break existing accuracy

---

## Edge Case Coverage Requirements

**Mandatory Edge Cases for Financial Code:**

1. **Zero Division:** Budget = 0, Actual > 0 (show N/A or handle gracefully)
2. **Negative Values:** Revenue reversals, expense credits
3. **NULL/Missing Data:** Unmatched accounts, missing columns
4. **Large Numbers:** Billions (ensure no overflow)
5. **Precision Boundaries:** Very small Decimals (0.001, 0.01)

**Example:**
```python
from decimal import Decimal

def test_variance_calculation_zero_budget():
    """Test variance calculation when budget is zero."""
    actual = Decimal('100.00')
    budget = Decimal('0.00')

    variance, variance_pct, favorability = calculate_variance(
        actual, budget, 'revenue'
    )

    assert variance == Decimal('100.00')
    assert variance_pct is None  # Cannot calculate percentage
    assert favorability == 'Favorable'
```

---

## Financial Precision Test Cases

**Decimal Accuracy Tests:**
- Assert to 2+ decimal places for currency
- Use `Decimal` in test assertions (not float)
- Test rounding behavior explicitly

**Example:**
```python
def test_decimal_precision_maintained():
    """Verify Decimal precision through calculations."""
    amount1 = Decimal('0.1')
    amount2 = Decimal('0.2')
    result = amount1 + amount2

    assert result == Decimal('0.3')  # NOT 0.30000000000000004

def test_rounding_applied_correctly():
    """Verify rounding uses ROUND_HALF_UP."""
    from decimal import ROUND_HALF_UP

    value = Decimal('10.555')
    rounded = value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    assert rounded == Decimal('10.56')  # Rounds up at .5
```

**Float Detection Tests:**
```python
def test_no_float_in_currency_code():
    """Verify code uses Decimal, not float."""
    with open('scripts/core/variance.py') as f:
        code = f.read()

    import re
    pattern = r'float\s*\([^)]*\b(currency|price|amount|revenue|expense|budget|actual)\b'
    matches = re.findall(pattern, code)

    assert len(matches) == 0, f"Float detected in currency code: {matches}"
```

---

## Test Data Fixture Patterns

**Fixture Location:**
```
tests/
├── fixtures/
│   ├── budget.xlsx                 # Sample budget data
│   ├── actuals.xlsx                # Sample actuals data
│   └── edge_cases/
│       ├── zero_budget.xlsx
│       ├── negative_revenue.xlsx
│       └── missing_accounts.xlsx
```

**Fixture Best Practices:**
- Use realistic account names (not "Account1", "Account2")
- Include representative account types (revenue, expense, asset, liability)
- Keep fixtures small (<100 rows preferred)

---

## Assertion Precision

**Decimal Assertions:**
```python
# ✅ CORRECT: Compare Decimals directly
assert result == Decimal('10.00')

# ❌ WRONG: Comparing Decimal to float
assert result == 10.0  # Precision mismatch
```

**Percentage Assertions:**
```python
# ✅ CORRECT: Use pytest.approx for floats
import pytest
assert variance_pct == pytest.approx(10.5, abs=0.01)
```

---

## Edge Case Reference

**Comprehensive Test Suite Examples:**
- Float precision errors (0.1 + 0.2 ≠ 0.3)
- Zero division, negative values, NULL/missing data
- Concurrent transactions (future), multi-currency scenarios (future)

---

## Test Organization

**Directory Structure:**
```
tests/
├── unit/                           # Unit tests (pure functions)
│   ├── test_variance.py
│   ├── test_consolidation.py
│   └── test_favorability.py
├── integration/                    # Integration tests (workflows)
│   ├── test_report_generation.py
│   └── test_data_extraction.py
├── fixtures/                       # Test data
└── conftest.py                     # Pytest configuration
```

---

**Precedence:** This config overrides root CLAUDE.md for tests/**
**Inherits:** All root principles (DRY, chain of verification, RPIV workflow)
