# Testing Standards Reference

**Purpose:** Unit test requirements, integration tests, regression tests, fixtures, assertion precision.

---

## Testing Philosophy for Financial Code

**Principle:** Financial calculations must be **provably correct**, not just "probably correct".

**Standard:** 100% edge case coverage (zero division, negatives, NULL, large numbers, precision boundaries).

---

## Unit Test Requirements

### Pytest Framework

**All financial tests use pytest:**

```python
# tests/test_variance.py
import pytest
from decimal import Decimal
from scripts.core.variance import calculate_variance, calculate_variance_pct


def test_basic_variance():
    """Test basic variance calculation."""
    actual = Decimal('1200.00')
    budget = Decimal('1000.00')

    variance = calculate_variance(actual, budget)

    assert variance == Decimal('200.00')
```

### Test Organization

```
tests/
├── core/
│   ├── test_variance.py         # Variance calculation tests
│   ├── test_consolidation.py    # Consolidation tests
│   └── test_transformations.py  # Data transformation tests
├── integration/
│   ├── test_end_to_end.py       # Full workflow tests
│   └── test_file_io.py          # Excel/CSV I/O tests
├── fixtures/
│   ├── sample_budget.xlsx       # Test data files
│   └── sample_actuals.csv
└── conftest.py                   # Shared fixtures
```

---

## Mandatory Test Cases

### 1. Zero Division Tests

```python
def test_variance_pct_zero_budget():
    """Test variance percentage when budget is zero."""
    variance = Decimal('50000.00')
    budget = Decimal('0.00')

    pct = calculate_variance_pct(variance, budget)

    assert pct is None  # Not error, not 0


def test_variance_pct_zero_variance():
    """Test variance percentage when variance is zero."""
    variance = Decimal('0.00')
    budget = Decimal('1000.00')

    pct = calculate_variance_pct(variance, budget)

    assert pct == 0.0  # 0% variance is valid
```

### 2. Negative Value Tests

```python
def test_variance_negative_actual():
    """Test variance with negative actual (revenue reversal)."""
    actual = Decimal('-10000.00')
    budget = Decimal('50000.00')

    variance = calculate_variance(actual, budget)

    assert variance == Decimal('-60000.00')
    assert variance < 0


def test_variance_negative_budget():
    """Test variance with negative budget (expense credit)."""
    actual = Decimal('4000.00')
    budget = Decimal('-1000.00')

    variance = calculate_variance(actual, budget)

    assert variance == Decimal('5000.00')


def test_variance_both_negative():
    """Test variance when both amounts are negative."""
    actual = Decimal('-1000.00')
    budget = Decimal('-2000.00')

    variance = calculate_variance(actual, budget)

    assert variance == Decimal('1000.00')  # Less negative is favorable
```

### 3. NULL/Missing Data Tests

```python
def test_variance_null_actual():
    """Test variance when actual is NULL."""
    actual = None
    budget = Decimal('100000.00')

    variance, status = calculate_variance_nullable(actual, budget)

    assert variance is None
    assert status == "No spending"


def test_variance_null_budget():
    """Test variance when budget is NULL."""
    actual = Decimal('50000.00')
    budget = None

    variance, status = calculate_variance_nullable(actual, budget)

    assert variance is None
    assert status == "Unbudgeted spending"


def test_variance_both_null():
    """Test variance when both are NULL."""
    actual = None
    budget = None

    variance, status = calculate_variance_nullable(actual, budget)

    assert variance is None
    assert status == "No data"
```

### 4. Large Number Tests

```python
def test_variance_billions():
    """Test variance with amounts in billions."""
    actual = Decimal('5234567890.12')
    budget = Decimal('5000000000.00')

    variance = calculate_variance(actual, budget)

    # Verify exact precision to the cent
    assert variance == Decimal('234567890.12')
    assert str(variance) == '234567890.12'


def test_variance_trillion():
    """Test variance with amounts in trillions."""
    actual = Decimal('1234567890123.45')
    budget = Decimal('1000000000000.00')

    variance = calculate_variance(actual, budget)

    assert variance == Decimal('234567890123.45')
```

### 5. Precision Boundary Tests

```python
def test_variance_very_small():
    """Test variance with very small amounts."""
    actual = Decimal('0.003')
    budget = Decimal('0.001')

    variance = calculate_variance(actual, budget)

    assert variance == Decimal('0.002')


def test_allocation_remainder():
    """Test allocation with tracked remainder."""
    total = Decimal('1000000.00')
    num_units = 3

    per_unit, remainder = allocate_amount(total, num_units)

    assert per_unit == Decimal('333333.33')
    assert remainder == Decimal('0.01')

    # Verify sum equals original
    assert (per_unit * num_units) + remainder == total
```

---

## Assertion Precision

### Decimal Equality (Exact)

```python
# ✅ CORRECT: Exact Decimal comparison
def test_exact_decimal():
    result = Decimal('100.00') + Decimal('50.00')
    assert result == Decimal('150.00')  # Exact equality


# ❌ WRONG: Comparing Decimal to float
def test_decimal_to_float_wrong():
    result = Decimal('100.00') + Decimal('50.00')
    assert result == 150.0  # May fail due to type difference!
```

### Float Equality (Approximate)

```python
# When comparing floats (e.g., percentages), use approximate equality
import pytest


def test_variance_pct_approximate():
    """Test variance percentage (float comparison)."""
    variance = Decimal('234.56')
    budget = Decimal('1000.00')

    pct = calculate_variance_pct(variance, budget)

    # Float comparison with tolerance
    assert pct == pytest.approx(23.456, abs=1e-6)
```

---

## Fixtures and Test Data

### Shared Fixtures (conftest.py)

```python
# tests/conftest.py
import pytest
from decimal import Decimal
import pandas as pd


@pytest.fixture
def sample_budget_data():
    """Sample budget data for testing."""
    return pd.DataFrame({
        'Account': ['Revenue', 'Salaries', 'Marketing', 'R&D'],
        'Budget': [
            Decimal('1000000.00'),
            Decimal('500000.00'),
            Decimal('100000.00'),
            Decimal('0.00')  # Zero budget edge case
        ]
    })


@pytest.fixture
def sample_actuals_data():
    """Sample actuals data for testing."""
    return pd.DataFrame({
        'Account': ['Revenue', 'Salaries', 'Marketing', 'Operations'],
        'Actual': [
            Decimal('1200000.00'),
            Decimal('450000.00'),
            Decimal('120000.00'),
            Decimal('50000.00')  # Unbudgeted spending
        ]
    })


@pytest.fixture
def edge_case_data():
    """Edge case data for testing."""
    return pd.DataFrame({
        'Account': ['Reversal', 'Credit', 'Large', 'Tiny'],
        'Budget': [
            Decimal('50000.00'),
            Decimal('5000.00'),
            Decimal('5000000000.00'),
            Decimal('0.001')
        ],
        'Actual': [
            Decimal('-10000.00'),  # Negative
            Decimal('-1000.00'),   # Negative
            Decimal('5234567890.12'),  # Billion
            Decimal('0.003')       # Very small
        ]
    })
```

### Using Fixtures

```python
def test_consolidation_with_fixtures(sample_budget_data, sample_actuals_data):
    """Test consolidation using shared fixtures."""
    result = consolidate_actuals(sample_budget_data, sample_actuals_data)

    # Verify structure
    assert 'Account' in result.columns
    assert 'Budget' in result.columns
    assert 'Actual' in result.columns
    assert 'Variance' in result.columns

    # Verify data
    revenue_row = result[result['Account'] == 'Revenue'].iloc[0]
    assert revenue_row['Budget'] == Decimal('1000000.00')
    assert revenue_row['Actual'] == Decimal('1200000.00')
    assert revenue_row['Variance'] == Decimal('200000.00')
```

---

## Integration Tests

### End-to-End Workflow Tests

```python
# tests/integration/test_end_to_end.py
import pytest
from pathlib import Path
from scripts.consolidate_actuals import main as consolidate_main


def test_full_variance_workflow(tmp_path):
    """Test complete variance analysis workflow.

    1. Read budget Excel
    2. Read actuals CSV
    3. Consolidate
    4. Calculate variance
    5. Generate report
    """
    # Setup test files
    budget_file = tmp_path / 'budget.xlsx'
    actuals_file = tmp_path / 'actuals.csv'
    output_file = tmp_path / 'variance_report.xlsx'

    # Create test data files
    create_test_budget_file(budget_file)
    create_test_actuals_file(actuals_file)

    # Run workflow
    consolidate_main(
        budget_file=str(budget_file),
        actuals_file=str(actuals_file),
        output_file=str(output_file)
    )

    # Verify output exists
    assert output_file.exists()

    # Verify output contents
    import pandas as pd
    result = pd.read_excel(output_file)

    assert 'Account' in result.columns
    assert 'Variance' in result.columns
    assert len(result) > 0
```

---

## Regression Tests

### Preventing Fixed Bugs from Returning

```python
def test_regression_zero_division_bug():
    """Regression test for zero division bug (fixed 2025-11-05).

    Previously, calculate_variance_pct() raised ZeroDivisionError
    when budget was 0. Now it returns None.
    """
    variance = Decimal('50000.00')
    budget = Decimal('0.00')

    # Should NOT raise exception
    pct = calculate_variance_pct(variance, budget)

    # Should return None
    assert pct is None


def test_regression_float_precision_bug():
    """Regression test for float precision bug (fixed 2025-11-08).

    Previously, variance calculation used float, causing
    0.1 + 0.2 = 0.30000000000000004. Now uses Decimal.
    """
    from scripts.core.variance import calculate_variance

    actual = Decimal('0.2')
    budget = Decimal('0.1')

    variance = calculate_variance(actual, budget)

    # Should be exact Decimal, not float
    assert variance == Decimal('0.1')
    assert str(variance) == '0.1'  # Not '0.09999999999'
```

---

## Test Coverage Requirements

### Minimum Coverage: 100% for Financial Code

```bash
# Run tests with coverage
pytest --cov=scripts.core --cov-report=term-missing tests/

# Required coverage:
# scripts/core/variance.py: 100%
# scripts/core/consolidation.py: 100%
# scripts/core/transformations.py: 100%
```

### Coverage Configuration (pyproject.toml)

```toml
[tool.coverage.run]
source = ["scripts"]
omit = [
    "*/tests/*",
    "*/conftest.py",
]

[tool.coverage.report]
fail_under = 100  # Require 100% coverage for financial code
show_missing = true
```

---

## Parameterized Tests

### Testing Multiple Scenarios

```python
@pytest.mark.parametrize("actual,budget,expected_variance", [
    (Decimal('1200.00'), Decimal('1000.00'), Decimal('200.00')),   # Positive variance
    (Decimal('900.00'), Decimal('1000.00'), Decimal('-100.00')),  # Negative variance
    (Decimal('1000.00'), Decimal('1000.00'), Decimal('0.00')),    # Zero variance
    (Decimal('0.00'), Decimal('1000.00'), Decimal('-1000.00')),   # Zero actual
    (Decimal('1000.00'), Decimal('0.00'), Decimal('1000.00')),    # Zero budget
])
def test_variance_scenarios(actual, budget, expected_variance):
    """Test variance across multiple scenarios."""
    variance = calculate_variance(actual, budget)
    assert variance == expected_variance
```

---

## Test Naming Conventions

```python
# ✅ GOOD: Descriptive test names
def test_variance_pct_zero_budget():
    """Test variance percentage when budget is zero."""
    pass


def test_variance_negative_actual():
    """Test variance with negative actual (revenue reversal)."""
    pass


# ❌ BAD: Vague test names
def test_variance():
    """Test variance."""  # What about variance?
    pass


def test_case_1():
    """Test case 1."""  # What scenario?
    pass
```

---

## Testing Checklist

Before deploying financial code:

- [ ] All 5 mandatory edge cases tested (zero, negative, NULL, large, precision)
- [ ] 100% code coverage for financial functions
- [ ] Decimal equality assertions (not float)
- [ ] Fixtures created for reusable test data
- [ ] Integration test for end-to-end workflow
- [ ] Regression tests for previously fixed bugs
- [ ] Parameterized tests for multiple scenarios
- [ ] Descriptive test names
- [ ] Test docstrings explain scenario

---

**Lines:** 376
**Last Updated:** 2025-11-10
