# Edge Cases Reference

**Purpose:** Zero division, negative values, NULL data, large numbers, multi-currency, concurrent transactions.

---

## Mandatory Edge Cases for Financial Calculations

All financial calculation functions MUST handle these 5 edge cases with explicit tests.

---

## 1. Zero Division

### The Problem

**Scenario:** Budget is $0, Actual is non-zero.

**Example:**
- Account: "New Product Research"
- Budget: $0 (not budgeted)
- Actual: $50,000 (emergency spending)
- Variance %: ??? (cannot divide by zero)

### Correct Handling

```python
from decimal import Decimal
from typing import Optional


def calculate_variance_pct(variance: Decimal, budget: Decimal) -> Optional[float]:
    """Calculate variance percentage, handling zero division.

    Args:
        variance: Variance amount (actual - budget)
        budget: Budget amount

    Returns:
        Variance percentage as float, or None if budget is 0
    """
    if budget == 0:
        return None  # Cannot calculate percentage

    return float(variance / budget * 100)


# Test
variance = Decimal('50000.00')
budget = Decimal('0.00')
pct = calculate_variance_pct(variance, budget)
assert pct is None  # CORRECT: None, not error
```

### ❌ Wrong Approaches

```python
# WRONG 1: Let it crash
def calculate_variance_pct_wrong(variance: Decimal, budget: Decimal) -> float:
    return float(variance / budget * 100)  # ZeroDivisionError!

# WRONG 2: Return 0
def calculate_variance_pct_wrong2(variance: Decimal, budget: Decimal) -> float:
    if budget == 0:
        return 0.0  # Misleading! 0% variance is different from undefined
    return float(variance / budget * 100)

# WRONG 3: Return infinity
def calculate_variance_pct_wrong3(variance: Decimal, budget: Decimal) -> float:
    if budget == 0:
        return float('inf')  # Breaks downstream calculations
    return float(variance / budget * 100)
```

### Test Requirements

```python
def test_variance_pct_zero_budget():
    """Test variance percentage when budget is zero."""
    variance = Decimal('50000.00')
    budget = Decimal('0.00')

    pct = calculate_variance_pct(variance, budget)

    assert pct is None  # Not error, not 0, not infinity
```

---

## 2. Negative Values

### The Problem

**Scenario 1: Revenue Reversals**
- Original sale: $10,000
- Customer refund: -$10,000
- Net revenue: $0

**Scenario 2: Expense Credits**
- Original expense: $5,000
- Vendor refund: -$1,000
- Net expense: $4,000

### Correct Handling

```python
from decimal import Decimal


def calculate_variance(actual: Decimal, budget: Decimal) -> tuple[Decimal, str]:
    """Calculate variance with negative value handling.

    Args:
        actual: Actual amount (can be negative)
        budget: Budget amount (can be negative)

    Returns:
        Tuple of (variance, interpretation)
    """
    variance = actual - budget

    # Interpret variance
    if variance > 0:
        interpretation = "Unfavorable" if actual > budget else "Favorable"
    elif variance < 0:
        interpretation = "Favorable" if actual < budget else "Unfavorable"
    else:
        interpretation = "On budget"

    return variance, interpretation


# Test with negative values
actual = Decimal('-10000.00')  # Revenue reversal
budget = Decimal('50000.00')
variance, interp = calculate_variance(actual, budget)

assert variance == Decimal('-60000.00')
assert interp == "Favorable"  # Actual < Budget for revenue
```

### Common Pitfall: Absolute Values

```python
# ❌ WRONG: Using absolute values
def calculate_variance_wrong(actual: Decimal, budget: Decimal) -> Decimal:
    return abs(actual - budget)  # Loses direction information!

# ✅ CORRECT: Preserve sign
def calculate_variance(actual: Decimal, budget: Decimal) -> Decimal:
    return actual - budget  # Keep negative if actual < budget
```

### Test Requirements

```python
def test_variance_negative_revenue():
    """Test variance with revenue reversal."""
    actual = Decimal('-10000.00')  # Reversal
    budget = Decimal('50000.00')

    variance, _ = calculate_variance(actual, budget)

    assert variance == Decimal('-60000.00')
    assert variance < 0  # Negative variance


def test_variance_negative_expense():
    """Test variance with expense credit."""
    actual = Decimal('-1000.00')  # Credit
    budget = Decimal('5000.00')

    variance, _ = calculate_variance(actual, budget)

    assert variance == Decimal('-6000.00')
```

---

## 3. NULL/Missing Data

### The Problem

**Scenario:** Budget exists but no actual spending (or vice versa).

**Example:**
- Account: "Marketing Campaign Q4"
- Budget: $100,000
- Actual: NULL (no spending yet)

### Correct Handling

```python
from decimal import Decimal
from typing import Optional


def calculate_variance_nullable(
    actual: Optional[Decimal],
    budget: Optional[Decimal]
) -> tuple[Optional[Decimal], str]:
    """Calculate variance with NULL handling.

    Args:
        actual: Actual amount (can be None)
        budget: Budget amount (can be None)

    Returns:
        Tuple of (variance, status)
    """
    # Case 1: Both missing
    if actual is None and budget is None:
        return None, "No data"

    # Case 2: Budget exists, no actual
    if actual is None and budget is not None:
        return None, "No spending"

    # Case 3: Actual exists, no budget
    if actual is not None and budget is None:
        return None, "Unbudgeted spending"

    # Case 4: Both exist
    assert actual is not None and budget is not None
    variance = actual - budget
    return variance, "Complete"


# Test
actual = None
budget = Decimal('100000.00')
variance, status = calculate_variance_nullable(actual, budget)

assert variance is None
assert status == "No spending"
```

### ❌ Wrong Approach: Replacing NULL with 0

```python
# WRONG: NULL → 0 (loses information)
def calculate_variance_wrong(
    actual: Optional[Decimal],
    budget: Optional[Decimal]
) -> Decimal:
    actual = actual or Decimal('0')  # BAD!
    budget = budget or Decimal('0')  # BAD!
    return actual - budget

# Problem: Cannot distinguish "no data" from "$0 budget"
```

### Test Requirements

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
```

---

## 4. Large Numbers

### The Problem

**Scenario:** Amounts in billions (enterprise-level budgets).

**Example:**
- Annual Revenue Budget: $5,000,000,000 (5 billion)
- Precision requirement: Still accurate to the cent

### Correct Handling

```python
from decimal import Decimal


def calculate_variance_large(actual: Decimal, budget: Decimal) -> Decimal:
    """Calculate variance for large numbers.

    Args:
        actual: Actual amount (can be billions)
        budget: Budget amount (can be billions)

    Returns:
        Variance (maintains precision)
    """
    variance = actual - budget
    return variance


# Test with billions
budget = Decimal('5000000000.00')  # $5B
actual = Decimal('5234567890.12')  # $5.23B

variance = calculate_variance_large(actual, budget)

assert variance == Decimal('234567890.12')  # Exact to the cent
```

### Why Float Fails for Large Numbers

```python
# ❌ WRONG: Float loses precision for large numbers
budget_float = 5000000000.00
actual_float = 5234567890.12

variance_float = actual_float - budget_float
# Result: 234567890.1200001 (not exact!)

# ✅ CORRECT: Decimal maintains precision
budget = Decimal('5000000000.00')
actual = Decimal('5234567890.12')

variance = actual - budget
# Result: Decimal('234567890.12') (exact!)
```

### Test Requirements

```python
def test_variance_billions():
    """Test variance with amounts in billions."""
    budget = Decimal('5000000000.00')
    actual = Decimal('5234567890.12')

    variance = calculate_variance_large(actual, budget)

    # Verify exact precision to the cent
    assert variance == Decimal('234567890.12')
    assert str(variance) == '234567890.12'  # No floating point errors
```

---

## 5. Precision Boundaries

### The Problem

**Scenario:** Very small amounts (fractions of a cent).

**Example:**
- Per-unit allocation: $1,000,000 / 3 = $333,333.333333...
- Need to track remainder for reconciliation

### Correct Handling

```python
from decimal import Decimal, ROUND_HALF_UP


def allocate_amount(
    total: Decimal,
    num_units: int,
    precision: int = 2
) -> tuple[Decimal, Decimal]:
    """Allocate amount across units with remainder tracking.

    Args:
        total: Total amount to allocate
        num_units: Number of units
        precision: Decimal places (default 2 for cents)

    Returns:
        Tuple of (amount_per_unit, remainder)
    """
    # Calculate with high precision
    per_unit = total / num_units

    # Round for display/storage
    per_unit_rounded = per_unit.quantize(
        Decimal('0.01'),
        rounding=ROUND_HALF_UP
    )

    # Calculate remainder
    allocated = per_unit_rounded * num_units
    remainder = total - allocated

    return per_unit_rounded, remainder


# Test
total = Decimal('1000000.00')
num_units = 3

per_unit, remainder = allocate_amount(total, num_units)

assert per_unit == Decimal('333333.33')
assert remainder == Decimal('0.01')  # Track the penny!
```

### Test Requirements

```python
def test_allocation_precision():
    """Test allocation with precision boundaries."""
    total = Decimal('1000000.00')
    num_units = 3

    per_unit, remainder = allocate_amount(total, num_units)

    # Verify allocation
    assert per_unit == Decimal('333333.33')
    assert remainder == Decimal('0.01')

    # Verify sum equals original
    assert (per_unit * 3) + remainder == total


def test_very_small_amounts():
    """Test calculations with very small amounts."""
    amount1 = Decimal('0.001')
    amount2 = Decimal('0.002')

    total = amount1 + amount2

    assert total == Decimal('0.003')  # Exact representation
```

---

## Additional Edge Cases (Advanced)

### 6. Multi-Currency (Out of Scope for Phase 1)

**Problem:** Converting between currencies with exchange rates.

**Note:** Current implementation assumes single currency (USD). Multi-currency support requires exchange rate handling and is planned for future phases.

### 7. Concurrent Transactions (Out of Scope for Phase 1)

**Problem:** Two processes updating the same account simultaneously.

**Note:** Current implementation assumes batch processing. Real-time concurrent updates require transaction isolation and are planned for future phases.

---

## Edge Case Testing Checklist

Before deploying a financial calculation function:

- [ ] Zero division test (budget = 0)
- [ ] Negative value test (revenue reversals, expense credits)
- [ ] NULL/missing data test (unmatched accounts)
- [ ] Large number test (amounts in billions)
- [ ] Precision boundary test (very small amounts, allocation remainders)
- [ ] Combination test (negative + zero, NULL + large, etc.)

---

**Lines:** 353
**Last Updated:** 2025-11-10
