# Decimal Precision Reference

**Purpose:** Why Decimal is mandatory for currency, float pitfalls, usage patterns, performance considerations.

---

## The Float Precision Problem

### Why Float Fails for Currency

**Binary Representation:** Float uses binary floating-point (IEEE 754), which cannot exactly represent most decimal fractions.

```python
# ❌ WRONG: Float precision error
>>> 0.1 + 0.2
0.30000000000000004  # NOT 0.3!

>>> 0.1 + 0.1 + 0.1 - 0.3
5.551115123125783e-17  # NOT 0!

# Real-world example
>>> price = 0.1
>>> quantity = 3
>>> total = price * quantity
>>> total
0.30000000000000004  # Incorrect!
```

**Compounding Errors:** Small errors compound in complex calculations:

```python
# ❌ Invoice calculation with float
items = [19.99, 29.99, 9.99]
subtotal = sum(items)  # 59.97
tax = subtotal * 0.08  # 4.7976 (should be 4.7976, but displayed as 4.80)
total = subtotal + tax  # 64.7676 (displayed as 64.77)

# With rounding errors at each step, results diverge from accounting standards
```

---

## Decimal: The Correct Solution

### Why Decimal Works

**Decimal Representation:** Uses base-10 arithmetic, exactly matching human decimal notation.

```python
# ✅ CORRECT: Decimal precision
>>> from decimal import Decimal
>>> Decimal('0.1') + Decimal('0.2')
Decimal('0.3')  # Exact!

>>> Decimal('0.1') + Decimal('0.1') + Decimal('0.1') - Decimal('0.3')
Decimal('0.0')  # Exact!
```

### Correct Usage Patterns

**String Initialization (REQUIRED):**

```python
from decimal import Decimal

# ✅ CORRECT: String initialization
amount = Decimal('100.00')
price = Decimal('19.99')

# ❌ WRONG: Float initialization (defeats the purpose!)
amount = Decimal(100.0)  # Contains float rounding error already!
```

**Arithmetic Operations:**

```python
from decimal import Decimal

budget = Decimal('1000.00')
actual = Decimal('1234.56')

# All operations preserve precision
variance = actual - budget  # Decimal('234.56')
variance_pct = (variance / budget) * 100  # Decimal('23.456')
```

**Division and Zero Handling:**

```python
from decimal import Decimal

def calculate_variance_pct(variance: Decimal, budget: Decimal) -> Decimal | None:
    """Calculate variance percentage, handling zero division."""
    if budget == 0:
        return None  # Cannot calculate percentage
    return (variance / budget) * 100

# Example usage
variance = Decimal('50.00')
budget = Decimal('0.00')
pct = calculate_variance_pct(variance, budget)  # None (not error)
```

---

## Rounding Rules

### Only Round at Display/Storage Layer

**NEVER in Intermediate Calculations:**

```python
from decimal import Decimal, ROUND_HALF_UP

# ✅ CORRECT: Rounding only at display layer
def calculate_total(items: list[Decimal]) -> Decimal:
    """Calculate total with proper rounding."""
    # Intermediate calculations - NO rounding
    subtotal = sum(items)
    tax = subtotal * Decimal('0.08')
    total = subtotal + tax

    # Rounding only for display/storage
    total_display = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return total_display

# ❌ WRONG: Rounding in intermediate steps
def calculate_total_wrong(items: list[Decimal]) -> Decimal:
    subtotal = sum(items).quantize(Decimal('0.01'))  # BAD!
    tax = (subtotal * Decimal('0.08')).quantize(Decimal('0.01'))  # BAD!
    return subtotal + tax  # Compounding rounding errors
```

### Standard Rounding Mode: ROUND_HALF_UP

```python
from decimal import Decimal, ROUND_HALF_UP

amount = Decimal('123.455')

# Round to 2 decimal places (cents)
rounded = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
# Result: Decimal('123.46')
```

---

## Type Hints and Function Signatures

### Correct Type Annotations

```python
from decimal import Decimal
from typing import Optional

# ✅ CORRECT: Decimal type hints
def calculate_variance(
    actual: Decimal,
    budget: Decimal
) -> tuple[Decimal, Optional[float]]:
    """Calculate variance and variance percentage.

    Args:
        actual: Actual amount (Decimal)
        budget: Budget amount (Decimal)

    Returns:
        Tuple of (variance, variance_pct)
        variance_pct is None if budget is 0
    """
    variance = actual - budget

    # Percentage can be float (not currency)
    variance_pct = float(variance / budget * 100) if budget != 0 else None

    return variance, variance_pct

# ❌ WRONG: Float type hints for currency
def calculate_variance_wrong(
    actual: float,  # BAD!
    budget: float   # BAD!
) -> tuple[float, Optional[float]]:
    # Precision errors from the start
    pass
```

---

## Performance Considerations

### Decimal is Slower than Float (But Worth It)

**Benchmark (approximate):**
- Float arithmetic: ~10 ns per operation
- Decimal arithmetic: ~200 ns per operation

**Trade-off:** 20x slower, but:
1. Correctness >>> Speed for financial data
2. Typical FP&A workloads: thousands of calculations (not millions)
3. I/O (Excel reading, database queries) dominates runtime

**Real-world impact:**
- Processing 10,000 line items with Decimal: ~2 ms
- Same with float: ~0.1 ms
- Excel file I/O: ~500 ms

**Conclusion:** Decimal overhead is negligible in FP&A context.

---

## Common Pitfalls

### 1. Float to Decimal Conversion

```python
from decimal import Decimal

# ❌ WRONG: Converting float to Decimal
amount = Decimal(19.99)  # Already has rounding error!
# Result: Decimal('19.989999999999998436805981327...')

# ✅ CORRECT: String to Decimal
amount = Decimal('19.99')  # Exact representation
# Result: Decimal('19.99')
```

### 2. Mixing Decimal and Float

```python
from decimal import Decimal

# ❌ WRONG: Mixing types
amount = Decimal('100.00')
tax_rate = 0.08  # Float!
tax = amount * tax_rate  # Converts to float, loses precision

# ✅ CORRECT: Both Decimal
amount = Decimal('100.00')
tax_rate = Decimal('0.08')
tax = amount * tax_rate  # Preserves precision
```

### 3. Equality Comparisons with Different Precision

```python
from decimal import Decimal

# Be careful with equality
amount1 = Decimal('100.00')
amount2 = Decimal('100.0')  # Different precision

amount1 == amount2  # True (value equality)
amount1.as_tuple() == amount2.as_tuple()  # False (different exponent)
```

---

## Integration with Pandas

### Correct DataFrame Handling

```python
import pandas as pd
from decimal import Decimal

# ✅ CORRECT: Read Excel with Decimal
df = pd.read_excel('budget.xlsx', dtype={'Amount': object})
df['Amount'] = df['Amount'].apply(lambda x: Decimal(str(x)))

# ✅ CORRECT: Create DataFrame with Decimal
df = pd.DataFrame({
    'Account': ['Revenue', 'Expense'],
    'Budget': [Decimal('1000.00'), Decimal('500.00')],
    'Actual': [Decimal('1200.00'), Decimal('450.00')]
})

# ❌ WRONG: Default pandas dtype (float64)
df = pd.read_excel('budget.xlsx')  # Amount is float64, loses precision
```

---

## When Float is Acceptable

**Non-currency calculations:**
- Percentages (after division): `variance_pct = float(variance / budget * 100)`
- Ratios: `ratio = float(actual / budget)`
- Statistical metrics: `mean`, `std_dev`

**Rule:** Float OK for **derived metrics**, NOT for **currency amounts**.

---

**Lines:** 246
**Last Updated:** 2025-11-10
