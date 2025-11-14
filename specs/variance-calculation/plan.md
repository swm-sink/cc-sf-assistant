# Variance Calculation Implementation Plan

**Created:** 2025-01-14
**Phase:** PLAN (RPIV Workflow)
**Status:** 🔄 Awaiting User Approval

---

## Research Findings Summary

**From spec.md (Story 2.1, 2.2):**
- Absolute Variance = Actual - Budget
- Percentage Variance = ((Actual - Budget) / Budget) × 100
- Zero budget handling: N/A for percentage when budget = 0 and actual ≠ 0
- Favorability logic depends on account type (revenue/asset vs expense/liability)
- Decimal precision mandatory (no float)

**From research.md (Data Analysis Anti-Patterns):**
- Use Decimal type exclusively for currency calculations
- Initialize from strings, not floats: `Decimal('123.45')`
- Specify rounding mode explicitly in quantize()
- Property-based testing with Hypothesis for edge cases

**From sample data (generate_sample_data.py):**
- Edge cases: negative values, NULL amounts, zero budget with actuals
- Material variance thresholds: >10% OR >$50K

---

## Function Design

### Core Function Signature

```python
from decimal import Decimal
from typing import Optional, Literal

def calculate_variance(
    actual: Optional[Decimal],
    budget: Optional[Decimal],
    account_type: Literal["revenue", "expense", "asset", "liability"],
) -> tuple[Decimal, Optional[Decimal], str]:
    """
    Calculate variance between actual and budget with favorability assessment.

    Args:
        actual: Actual amount (None if missing data)
        budget: Budget amount (None if missing data)
        account_type: Account classification for favorability logic

    Returns:
        Tuple of (absolute_variance, percentage_variance, favorability)
        - absolute_variance: Actual - Budget (Decimal)
        - percentage_variance: ((Actual - Budget) / Budget) × 100 (Decimal or None if N/A)
        - favorability: "favorable" | "unfavorable" | "no_activity" | "insufficient_data"

    Raises:
        ValueError: If account_type is invalid

    Examples:
        >>> calculate_variance(Decimal('550000'), Decimal('500000'), 'revenue')
        (Decimal('50000'), Decimal('10.00'), 'favorable')

        >>> calculate_variance(Decimal('105000'), Decimal('100000'), 'expense')
        (Decimal('5000'), Decimal('5.00'), 'unfavorable')

        >>> calculate_variance(Decimal('100'), Decimal('0'), 'revenue')
        (Decimal('100'), None, 'insufficient_data')
    """
```

### Edge Cases to Handle

1. **NULL/None values**
   - `actual = None, budget = None` → (0, None, "insufficient_data")
   - `actual = None, budget = X` → Treat actual as 0? [DECISION NEEDED]
   - `actual = X, budget = None` → Treat budget as 0? [DECISION NEEDED]

2. **Zero budget scenarios**
   - `actual = 100, budget = 0` → (100, None, "insufficient_data")
   - `actual = 0, budget = 0` → (0, Decimal('0.00'), "no_activity")
   - `actual = -50, budget = 0` → (-50, None, "insufficient_data")

3. **Negative values**
   - Revenue: `actual = -50, budget = 100` → (-150, -150.00%, "unfavorable")
   - Expense: `actual = -50, budget = -100` → (50, -50.00%, "unfavorable")

4. **Very small budgets** (division precision)
   - `actual = 100.01, budget = 0.01` → (100.00, 1000000.00%, ???)
   - Need max percentage cap? Or flag extreme variances?

### Favorability Logic

```python
def _determine_favorability(
    variance: Decimal,
    account_type: Literal["revenue", "expense", "asset", "liability"],
) -> str:
    """
    Determine if variance is favorable based on account type.

    Rules:
    - Revenue/Asset: positive variance = favorable (exceeded target)
    - Expense/Liability: negative variance = favorable (spent less)
    - Zero variance = no_activity
    """
    if variance == 0:
        return "no_activity"

    if account_type in ("revenue", "asset"):
        return "favorable" if variance > 0 else "unfavorable"
    else:  # expense, liability
        return "favorable" if variance < 0 else "unfavorable"
```

---

## Test Strategy

### Example-Based Tests (pytest)

1. **Basic calculations**
   - Revenue favorable: actual > budget
   - Revenue unfavorable: actual < budget
   - Expense favorable: actual < budget
   - Expense unfavorable: actual > budget

2. **Edge cases**
   - Zero budget with actuals (percentage = None)
   - Both zero (no activity)
   - Negative amounts
   - NULL/None values

3. **Precision validation**
   - Verify Decimal type in/out
   - Check rounding to 2 decimal places for percentages
   - Test very large numbers (millions)
   - Test very small numbers (cents)

### Property-Based Tests (Hypothesis)

```python
from hypothesis import given
import hypothesis.strategies as st

@given(
    actual=st.decimals(min_value=-1000000, max_value=1000000, places=2),
    budget=st.decimals(min_value=-1000000, max_value=1000000, places=2).filter(lambda x: x != 0),
    account_type=st.sampled_from(["revenue", "expense", "asset", "liability"])
)
def test_variance_calculation_properties(actual, budget, account_type):
    """Test invariants that should always hold."""
    abs_var, pct_var, favorability = calculate_variance(actual, budget, account_type)

    # Property 1: Absolute variance should equal actual - budget
    assert abs_var == actual - budget

    # Property 2: Percentage should be calculable from absolute
    if pct_var is not None:
        expected_pct = ((actual - budget) / budget) * 100
        assert abs(pct_var - expected_pct) < Decimal('0.01')  # Within 0.01%

    # Property 3: Favorability should be consistent with variance sign
    if account_type in ("revenue", "asset"):
        if abs_var > 0:
            assert favorability == "favorable"
        elif abs_var < 0:
            assert favorability == "unfavorable"
    else:
        if abs_var < 0:
            assert favorability == "favorable"
        elif abs_var > 0:
            assert favorability == "unfavorable"
```

### Coverage Target

- **100% line coverage** (required by pre-commit hooks)
- **100% branch coverage** (all if/else paths tested)
- **All edge cases documented** in test docstrings

---

## Implementation Plan

### File Structure

```
scripts/core/
└── variance.py                    # Core variance calculation logic

tests/core/
├── test_variance.py               # Example-based tests
└── test_variance_properties.py   # Property-based tests with Hypothesis
```

### Implementation Steps

1. **Create directory structure**
   ```bash
   mkdir -p scripts/core tests/core
   ```

2. **Write tests first (TDD)**
   - `tests/core/test_variance.py` with 10-15 example tests
   - `tests/core/test_variance_properties.py` with 3-5 property tests

3. **Implement `scripts/core/variance.py`**
   - Import Decimal, typing
   - Implement calculate_variance() with full type hints
   - Handle all edge cases with explicit logic
   - Add comprehensive docstrings

4. **Run tests and iterate**
   - `poetry run pytest tests/core/ -v --cov=scripts/core`
   - Fix failing tests
   - Ensure 100% coverage

5. **Verify quality gates**
   - Run full pre-commit: `poetry run pre-commit run --all-files`
   - Check file length <100 lines
   - Validate no float usage in scripts/core/

---

## Open Questions for User Approval

**Q1:** How should we handle NULL actual with non-NULL budget?
- **Option A:** Treat NULL actual as $0 (calculate variance)
- **Option B:** Return "insufficient_data" favorability
- **Recommendation:** Option B (more conservative, flags data quality issues)

**Q2:** How should we handle NULL budget with non-NULL actual?
- **Option A:** Treat NULL budget as $0 (variance = actual)
- **Option B:** Return "insufficient_data" favorability
- **Recommendation:** Option B (budget should always exist)

**Q3:** Should we cap extreme percentage variances?
- **Scenario:** Budget = $0.01, Actual = $10,000 → 999,900% variance
- **Option A:** Return as-is, let reporting layer handle
- **Option B:** Cap at ±999% or return "N/A" for extreme cases
- **Recommendation:** Option A (preserve accuracy, flag in materiality check)

**Q4:** Precision for percentage variance?
- **Option A:** 2 decimal places (10.25%)
- **Option B:** Full Decimal precision, round in reporting layer
- **Recommendation:** Option B (preserve precision in calculations)

---

## Success Criteria

**Before moving to IMPLEMENT phase:**
- ✅ User approves function signature
- ✅ User approves NULL handling approach (Q1, Q2)
- ✅ User approves edge case handling (Q3, Q4)
- ✅ Test strategy reviewed and accepted

**IMPLEMENT phase complete when:**
- ✅ All tests passing (example + property-based)
- ✅ 100% test coverage achieved
- ✅ Pre-commit hooks pass (ruff, mypy, pytest@100%, file length)
- ✅ No float usage detected in scripts/core/
- ✅ Decimal precision validated with sample data

---

## Next Steps After Approval

1. User reviews this plan
2. User answers Q1-Q4 or approves recommendations
3. I proceed to IMPLEMENT phase with TDD
4. VERIFY phase validates all quality gates
5. Commit & push to branch

**Estimated Time:** 45 minutes (20 min tests, 15 min implementation, 10 min verification)
