# Test-Driven Development (TDD) Workflow Template

## Overview
TDD workflow for building financial calculation scripts with Claude Code.

## Phases

### Phase 1: RED - Write Failing Tests
**Objective:** Define expected behavior through tests before writing implementation.

**Steps:**
1. Define test cases based on requirements
2. Write tests for non-existent functionality
3. Include edge cases (from `.claude/skills/shared/test-suite-generator/references/edge-cases.md`)
4. Run tests to confirm they fail
5. Commit failing tests

**Example:**
```python
# test_variance.py
from decimal import Decimal
import pytest

def test_variance_calculation():
    """Test basic variance calculation: Actual - Budget"""
    actual = Decimal('115000.00')
    budget = Decimal('100000.00')

    result = calculate_variance(actual, budget)

    assert result.variance == Decimal('15000.00')
    assert result.variance_pct == Decimal('15.00')
    assert result.favorability == 'favorable'  # Revenue up = good

# This test will FAIL because calculate_variance() doesn't exist yet
```

---

### Phase 2: GREEN - Write Minimal Implementation
**Objective:** Write just enough code to make tests pass.

**Steps:**
1. Implement minimum code to pass tests
2. Use Decimal for all financial calculations (NEVER float)
3. Add type hints
4. Run tests to confirm they pass
5. Do NOT add features not covered by tests

**Example:**
```python
# variance.py
from decimal import Decimal
from typing import NamedTuple, Literal

class VarianceResult(NamedTuple):
    variance: Decimal
    variance_pct: Decimal
    favorability: Literal['favorable', 'unfavorable']

def calculate_variance(
    actual: Decimal,
    budget: Decimal,
    account_type: Literal['revenue', 'expense'] = 'revenue'
) -> VarianceResult:
    """Calculate variance with favorability logic."""
    variance = actual - budget
    variance_pct = (variance / budget * 100) if budget else Decimal('0')

    # Favorability logic
    if account_type == 'revenue':
        favorability = 'favorable' if variance > 0 else 'unfavorable'
    else:  # expense
        favorability = 'unfavorable' if variance > 0 else 'favorable'

    return VarianceResult(variance, variance_pct, favorability)
```

---

### Phase 3: REFACTOR - Improve Code Quality
**Objective:** Improve code while keeping tests green.

**Steps:**
1. Run tests to confirm still passing
2. Refactor for readability, performance, maintainability
3. Add docstrings
4. Add error handling
5. Add audit logging
6. Run tests after each refactor
7. Commit when tests still pass

**Quality Checks:**
- ✅ Decimal precision maintained
- ✅ Type hints on all functions
- ✅ Comprehensive docstrings
- ✅ Error handling for edge cases
- ✅ Audit trail logging
- ✅ No code duplication
- ✅ Tests still passing

---

### Phase 4: VALIDATE - Independent Review
**Objective:** Verify correctness through independent agent review.

**Steps:**
1. Invoke `code-reviewer` agent (read-only, separate context)
2. Review agent checks for:
   - Float usage (BLOCKING)
   - Missing type hints
   - Edge case coverage
   - Financial calculation correctness
   - Audit trail presence
3. Address review findings
4. Re-run tests
5. Get human approval
6. Commit final version

---

## Key Principles

### 1. Tests First, Always
Write tests BEFORE implementation. Be explicit with Claude: "This is TDD, write tests for functionality that doesn't exist yet."

### 2. Fail Fast
Confirm tests fail before writing implementation. Prevents false positives.

### 3. Minimal Implementation
Write only enough code to pass tests. Don't add speculative features.

### 4. Refactor with Confidence
Tests allow safe refactoring. Make small changes, run tests frequently.

### 5. Human Runs Tests
Don't let Claude loop around itself. Human verifies test results at each phase.

---

## Anti-Patterns to Avoid

❌ **Writing implementation before tests**
✅ Write failing tests first

❌ **Using float for currency**
✅ Use Decimal for all financial calculations

❌ **Skipping edge case tests**
✅ Test edge cases from comprehensive list

❌ **Over-implementing beyond tests**
✅ Write minimum code to pass tests

❌ **Refactoring without running tests**
✅ Run tests after every refactor

---

## Tools & Skills Auto-Invoked

**Development Skills:**
- `python-best-practices` - Enforces Decimal, type hints, error handling
- `test-suite-generator` - Generates comprehensive edge case tests
- `decimal-precision-enforcer` - Blocks float usage

**Validation Agents:**
- `script-validator` - Runs pytest, mypy, ruff, security checks
- `code-reviewer` - Independent review with separate context

---

## Example TDD Session

```bash
# Phase 1: RED
User: "Write tests for YoY revenue growth calculation using TDD"
Claude: [Writes comprehensive tests including edge cases]
Claude: [Runs pytest - confirms all fail]
User: "Good, commit the failing tests"

# Phase 2: GREEN
Claude: [Implements minimal code using Decimal]
Claude: [Runs pytest - all pass]
User: "Tests pass, now refactor for quality"

# Phase 3: REFACTOR
Claude: [Adds docstrings, error handling, audit logging]
Claude: [Runs pytest after each change - still passing]
User: "Request code review"

# Phase 4: VALIDATE
User: "@code-reviewer Please review scripts/core/yoy_growth.py"
code-reviewer: [Provides independent review]
Claude: [Addresses findings]
Claude: [Runs pytest - still passing]
User: "Approved, commit final version"
```

---

**Source:** Based on Claude Code TDD best practices (2025)
**References:**
- https://github.com/nizos/tdd-guard (Automated TDD enforcement)
- https://www.claudecode101.com/en/tutorial/workflows/test-driven
- Anthropic Claude Code Best Practices
**Last Updated:** 2025-11-08
