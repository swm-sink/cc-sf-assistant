# Financial Calculation Edge Cases - Comprehensive Test Suite

**Research Basis:** Financial application testing best practices, BFSI testing standards (2024-2025)

---

## 1. Float Precision Errors (CRITICAL)

**Problem:** JavaScript/Python floats cause precision issues in financial calculations.

**Test Cases:**

```python
# FAIL: Float arithmetic
assert 0.1 + 0.2 == 0.3  # Returns False! (0.30000000000000004)

# PASS: Decimal arithmetic
from decimal import Decimal
assert Decimal('0.1') + Decimal('0.2') == Decimal('0.3')  # Returns True
```

**Real-World Impact:**
- Tiny discrepancies accumulate into significant errors
- User trust violation
- Regulatory compliance issues

**Solution:** ALL currency calculations MUST use Decimal type.

---

## 2. Division by Zero

**Test Cases:**

```python
# Case 1: Zero budget with actuals
budget = Decimal('0')
actual = Decimal('50000')

expected_absolute_variance = Decimal('50000')
expected_percentage_variance = None  # or "N/A"
expected_status = "Flag for review - zero budget"

# Case 2: Both zero
budget = Decimal('0')
actual = Decimal('0')

expected_absolute_variance = Decimal('0')
expected_percentage_variance = Decimal('0')
expected_status = "No Activity"

# Case 3: Normal calculation
budget = Decimal('100000')
actual = Decimal('115000')

expected_absolute_variance = Decimal('15000')
expected_percentage_variance = Decimal('15.00')  # (15000/100000) * 100
```

**Handling:**
- Never raise unhandled exception
- Return explicit "N/A" or None for percentage when budget=0
- Log the case for audit trail

---

## 3. Negative Values

**Test Cases:**

```python
# Case 1: Negative budget (liability/contra account)
budget = Decimal('-10000')
actual = Decimal('-12000')

expected_variance = Decimal('-2000')  # More negative = unfavorable for liability
expected_percentage = Decimal('20.00')

# Case 2: Actual crosses zero
budget = Decimal('-5000')
actual = Decimal('3000')

expected_variance = Decimal('8000')
expected_percentage = Decimal('-160.00')  # Large swing
```

**Note:** Negative values are valid for:
- Liability accounts
- Contra-revenue accounts
- Refunds/returns

---

## 4. NULL / Missing Data

**Test Cases:**

```python
# Case 1: NULL in amount column
budget = None
actual = Decimal('50000')

expected_action = "Flag as error, do not proceed with calculation"
expected_message = "NULL value in budget for account X"

# Case 2: Missing account in actuals
budget_accounts = ['4000', '4100', '4200']
actual_accounts = ['4000', '4100']  # 4200 missing

expected_action = "Flag unmatched account 4200"
expected_report = "Budget account 4200 has no actuals - report as 'No Actuals Reported'"
```

**Handling:**
- NEVER silently drop data
- Flag all missing/NULL values
- Generate reconciliation report

---

## 5. Concurrent Transactions

**Test Case:**

```python
# Scenario: Two processes updating same account simultaneously
initial_balance = Decimal('100000')

# Process A: Add 5000
# Process B: Add 3000

# Expected final balance: 108000
# Risk: Race condition could result in 105000 or 103000

# Solution: Atomic operations, transaction isolation
```

**Testing:**
- Simulate concurrent writes
- Verify all transformations are atomic
- Check audit trail captures all operations

---

## 6. Multi-Currency

**Test Cases:**

```python
# Case 1: Mixed currencies (ERROR)
budget_usd = Decimal('100000')  # USD
actual_eur = Decimal('95000')   # EUR

expected_action = "REJECT - Cannot calculate variance across currencies"
expected_message = "Currency mismatch: USD vs EUR"

# Case 2: Explicit currency with conversion
budget = {'amount': Decimal('100000'), 'currency': 'USD'}
actual = {'amount': Decimal('85000'), 'currency': 'EUR'}
exchange_rate = Decimal('1.10')  # EUR to USD

actual_usd = actual['amount'] * exchange_rate  # 93500 USD
variance = actual_usd - budget['amount']  # -6500 USD
```

**Handling:**
- Require explicit currency codes
- Never perform silent currency conversion
- Log exchange rates used with timestamp

---

## 7. Rounding Precision

**Test Cases:**

```python
# INCORRECT: Rounding during intermediate calculation
revenue = Decimal('100000.123')
cogs = Decimal('60000.456')
gross_margin = round(revenue - cogs, 2)  # Premature rounding
margin_pct = (gross_margin / revenue) * 100  # Error propagated

# CORRECT: Rounding only at display
revenue = Decimal('100000.123')
cogs = Decimal('60000.456')
gross_margin = revenue - cogs  # Keep full precision
margin_pct = (gross_margin / revenue) * 100
display_margin = margin_pct.quantize(Decimal('0.01'))  # Round only for display
```

**Rule:** Rounding ONLY at display/storage layer, NEVER in intermediate calculations.

---

## 8. Boundary Conditions

**Test Cases:**

```python
# Case 1: Exactly at materiality threshold
budget = Decimal('100000')
actual = Decimal('110000')
variance_pct = Decimal('10.00')  # Exactly 10%

expected_material = True  # ≥10% is material

# Case 2: Just below threshold
budget = Decimal('100000')
actual = Decimal('109999')
variance_pct = Decimal('9.999')

expected_material = False  # <10% is not material

# Case 3: Absolute threshold
budget = Decimal('1000')
actual = Decimal('51000')
variance_pct = Decimal('5000.00')  # 5000%!
variance_abs = Decimal('50000')

expected_material = True  # Absolute variance = $50K threshold
```

---

## 9. Data Type Mismatches

**Test Cases:**

```python
# Case 1: String instead of number
budget = "100000"  # String
actual = Decimal('115000')

expected_action = "Convert to Decimal or reject"
expected_validation = "Data type mismatch in budget column"

# Case 2: Date in amount column
budget = Decimal('100000')
actual = "2025-11-08"  # Date accidentally in amount column

expected_action = "REJECT with clear error"
expected_message = "Invalid data type: expected Decimal, got str"
```

---

## 10. Large Numbers / Overflow

**Test Cases:**

```python
# Case: Very large budget values
budget = Decimal('999999999999.99')  # ~1 trillion
actual = Decimal('1000000000010.00')

variance = actual - budget  # Decimal handles arbitrary precision
variance_pct = ((actual - budget) / budget) * 100

# Decimal type handles arbitrary precision - no overflow
assert variance == Decimal('10.01')
```

**Note:** Decimal type in Python has arbitrary precision - no overflow risk.

---

## Validation Test Script

Run this before accepting any financial calculation implementation:

```python
def validate_financial_implementation():
    """Run comprehensive edge case validation."""

    test_results = {
        'float_precision': test_float_precision(),
        'zero_division': test_zero_division(),
        'negative_values': test_negative_values(),
        'null_handling': test_null_handling(),
        'concurrent_tx': test_concurrent_transactions(),
        'multi_currency': test_multi_currency(),
        'rounding': test_rounding_precision(),
        'boundaries': test_boundary_conditions(),
        'data_types': test_data_type_validation(),
        'large_numbers': test_large_numbers()
    }

    failures = [k for k, v in test_results.items() if not v]

    if failures:
        raise ValidationError(f"Failed edge case tests: {failures}")

    return True  # All tests passed
```

---

**Testing Mandate:** All edge case tests MUST pass before merging financial calculation code.

**Research Sources:**
- Financial Application Testing (TestGrid, QA Madness, 2024)
- BFSI Testing Standards (Katalon, 2025)
- Edge Cases in Software Testing (MuukTest, 2024)
