---
name: financial-validator
description: Validates financial data structures and calculations for FP&A workflows. Use when processing Excel files, performing variance calculations, or generating financial reports. Ensures decimal precision, handles edge cases, and maintains audit trails.
---

# Financial Data Validator Skill

## Purpose

Validate financial data and calculations to ensure:
- Decimal precision (never float/double for currency)
- Edge case handling (zero division, negative values, NULL data)
- Audit trail compliance (timestamp, source, user, operation)
- Data integrity (no silent data loss)

## When to Use This Skill

Claude automatically invokes this skill when:
- Loading budget or actuals Excel files
- Performing variance calculations
- Validating financial formulas
- Generating financial reports
- User mentions "validate", "check data", "verify calculations"

## Core Validation Steps

### Step 1: Data Structure Validation
```python
# Check required columns exist
# Validate data types (numeric amounts, valid dates)
# Ensure no completely empty columns
# Flag duplicate column names
```

### Step 2: Financial Precision Validation
```python
# CRITICAL: Ensure all currency uses Decimal, not float
# Verify percentage calculations maintain 2+ decimal places
# Check rounding only at display/storage layer
# Validate reproducibility (same inputs → same outputs)
```

### Step 3: Edge Case Handling
```python
# Zero division: Budget=0, Actual≠0 → Variance=Actual, %=N/A
# Both zero: Budget=0, Actual=0 → Variance=0, 0%, "No Activity"
# Negative values: Calculate variance normally
# NULL/missing: Flag explicitly, don't silently drop
```

### Step 4: Audit Trail Verification
```python
# Every transformation logs: timestamp, user, source, operation
# Metadata includes: source files, thresholds, generation time
# Version control: Never overwrite without backup
```

## Comprehensive Edge Cases

**See references/edge-cases.md for detailed test suite**

Quick reference:
- Float precision: `0.1 + 0.2 = 0.30000000000000004` (FAIL)
- Decimal precision: `Decimal('0.1') + Decimal('0.2') = Decimal('0.3')` (PASS)
- Zero budget with actuals: Absolute variance = actual value, % variance = N/A
- Concurrent transactions: Validate all transformations are atomic
- Multi-currency: Require explicit currency codes, no silent conversion

## Scripts Available

- `scripts/validate_structure.py` - Validates DataFrame structure and data quality
- `scripts/validate_precision.py` - Checks decimal precision compliance
- `scripts/validate_edge_cases.py` - Tests edge case handling

## Example Usage

```python
from decimal import Decimal

# CORRECT: Use Decimal for currency
budget = Decimal('100000.00')
actual = Decimal('115000.00')
variance = actual - budget  # Decimal('15000.00')

# INCORRECT: Don't use float
budget = 100000.00  # float
actual = 115000.00  # float
variance = actual - budget  # May have precision errors
```

## Validation Checklist

Before approving any financial calculation or data processing:

- [ ] All currency values use Decimal type
- [ ] Division by zero handled explicitly
- [ ] NULL/missing data flagged, not dropped
- [ ] Negative values handled correctly
- [ ] Audit trail includes timestamp, source, user, operation
- [ ] Output includes generation metadata
- [ ] Version control prevents data loss
- [ ] Test cases pass for all edge conditions

## References

- See `references/edge-cases.md` for comprehensive test suite
- See `references/decimal-precision.md` for precision requirements
- See `references/audit-trail.md` for logging standards

---

**Progressive Disclosure:** This SKILL.md provides core guidance. Claude loads reference documents only when needed to reduce token usage.
