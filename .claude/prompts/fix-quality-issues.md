# Fix Pre-Commit Quality Issues

**Purpose**: Systematic guide for Claude to fix pre-commit hook failures in FP&A automation project.

**When to use**: Pre-commit hooks blocked your commit with quality violations.

---

## Step-by-Step Fix Protocol

### 1. Read the Error Output

Pre-commit shows which hooks failed. Common failures:

- **ruff** - Code formatting/linting issues
- **ruff-format** - Code formatting violations
- **mypy** - Type hint errors
- **pytest-coverage** - Test coverage <95% OR failing tests
- **validate-no-floats** - float() usage in scripts/

### 2. Fix Each Hook Failure Systematically

#### Ruff Formatting/Linting

**Symptoms**:
```
ruff....................................Failed
- hook id: ruff
```

**Fix**:
```bash
# Auto-fix most issues
poetry run ruff check scripts/ --fix

# Check what remains
poetry run ruff check scripts/

# Format code
poetry run ruff format scripts/
```

**Common Issues**:
- Unused imports → Remove them
- Line too long → Break into multiple lines
- Missing docstrings → Add them

---

#### Mypy Type Checking

**Symptoms**:
```
mypy....................................Failed
error: Function is missing a return type annotation
```

**Fix Pattern**:
```python
# ❌ BEFORE (no type hints)
def calculate_variance(actual, budget):
    return actual - budget

# ✅ AFTER (with type hints)
from decimal import Decimal

def calculate_variance(actual: Decimal, budget: Decimal) -> Decimal:
    """Calculate variance between actual and budget."""
    return actual - budget
```

**Requirements**:
- ALL functions must have type hints (params + return)
- Use `from typing import Optional, List, Dict, Tuple` as needed
- Reference: `pyproject.toml` [tool.mypy] `disallow_untyped_defs = true`

---

#### Pytest Coverage <95%

**Symptoms**:
```
pytest-coverage.........................Failed
FAILED tests/core/test_variance.py::test_calculate_variance
---------- coverage: 85% -----------
TOTAL                            85%
```

**Fix Protocol** (TDD Mandatory):

**If tests are FAILING:**
```bash
# Run tests to see failures
poetry run pytest -v

# Fix the implementation code
# Re-run tests until passing
poetry run pytest -v
```

**If coverage is <95%:**

This means **code was written without TDD**. Per user requirements:

1. **DELETE the untested code**
2. **Restart with TDD**:
   - Write test first (RED)
   - Write minimal code to pass (GREEN)
   - Refactor (REFACTOR)
   - Verify coverage ≥95%

**Example TDD Workflow**:
```python
# Step 1: Write test FIRST (tests/core/test_variance.py)
from decimal import Decimal
from scripts.core.variance import calculate_variance

def test_calculate_variance_revenue_favorable():
    """Test revenue increase = favorable variance."""
    actual = Decimal('2500000.00')
    budget = Decimal('2000000.00')
    result = calculate_variance(actual, budget, account_type='revenue')

    assert result.variance == Decimal('500000.00')
    assert result.favorable is True
    assert result.percentage == Decimal('25.00')

# Step 2: Run test (should FAIL - RED)
# poetry run pytest tests/core/test_variance.py

# Step 3: Write MINIMAL code to pass (scripts/core/variance.py)
from decimal import Decimal
from typing import NamedTuple

class VarianceResult(NamedTuple):
    variance: Decimal
    favorable: bool
    percentage: Decimal

def calculate_variance(
    actual: Decimal,
    budget: Decimal,
    account_type: str
) -> VarianceResult:
    variance = actual - budget
    favorable = variance > 0 if account_type == 'revenue' else variance < 0
    percentage = (variance / budget * 100) if budget != 0 else Decimal('0')
    return VarianceResult(variance, favorable, percentage)

# Step 4: Run test (should PASS - GREEN)
# Step 5: Check coverage
# poetry run pytest --cov=scripts/core/variance --cov-report=term-missing
```

**Coverage Target**: ≥95% for ALL scripts/

---

#### Float Usage in Financial Code

**Symptoms**:
```
validate-no-floats......................Failed
❌ FLOAT USAGE DETECTED: scripts/core/variance.py
  Line 23: amount = float(budget_value)
```

**Fix**:
```python
# ❌ NEVER use float
amount = float(budget_value)
percentage = 0.1 + 0.2  # WRONG: equals 0.30000000000000004

# ✅ ALWAYS use Decimal
from decimal import Decimal

amount = Decimal(str(budget_value))
percentage = Decimal('0.1') + Decimal('0.2')  # CORRECT: equals 0.3
```

**Rationale**: Float introduces rounding errors that violate financial precision requirements, break audit trails, and fail SOX compliance.

**Reference**: `CLAUDE.md` > Financial Domain Requirements > Precision & Accuracy

---

## 3. Re-run Pre-Commit After Fixes

```bash
# Test your fixes
poetry run pre-commit run --all-files

# If all pass, commit
git add .
git commit -m "fix: resolve pre-commit quality issues"
```

---

## 4. Prevention Tips

**Always use TDD**:
1. Write test FIRST
2. Run test (should fail)
3. Write minimal code to pass
4. Check coverage ≥95%
5. Commit

**Type hints from the start**:
- Add type hints while writing functions
- Don't write code then add hints later

**Use Decimal immediately**:
- Financial code: `from decimal import Decimal` at top
- Never use float/double for currency

**Run pre-commit before committing**:
```bash
# Check everything before commit
poetry run pre-commit run --all-files
```

---

## 5. Emergency Override (DISCOURAGED)

If you MUST bypass pre-commit (production hotfix only):
```bash
git commit --no-verify -m "hotfix: critical issue"
```

**Warning**: Bypassing hooks creates technical debt. Fix quality issues ASAP.

---

## Quality Gates Summary

| Hook | Purpose | Fix Command |
|------|---------|-------------|
| **ruff** | Linting | `poetry run ruff check --fix` |
| **ruff-format** | Formatting | `poetry run ruff format` |
| **mypy** | Type checking | Add type hints to functions |
| **pytest-coverage** | Tests + Coverage | Write tests first (TDD), achieve 95%+ |
| **validate-no-floats** | Financial precision | Replace float() with Decimal() |

---

**Created**: 2025-11-13
**Purpose**: Systematic quality issue resolution for CI/CD enforcement
**Reference**: `.pre-commit-config.yaml`, `CLAUDE.md`
