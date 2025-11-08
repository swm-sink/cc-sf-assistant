#!/usr/bin/env python3
"""
Financial Precision Validator

Validates that financial calculations use Decimal type and maintain precision.
Part of financial-validator skill for Claude Code.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Any, List, Tuple
import sys


def validate_currency_type(value: Any, variable_name: str) -> Tuple[bool, str]:
    """
    Validate that a currency value uses Decimal type.

    Args:
        value: The value to validate
        variable_name: Name of the variable (for error messages)

    Returns:
        (is_valid, error_message)
    """
    if not isinstance(value, Decimal):
        return False, f"{variable_name} must be Decimal type, got {type(value).__name__}"

    return True, ""


def test_float_precision() -> bool:
    """
    Test that demonstrates float precision issues.

    Returns:
        True if test passes (demonstrates the problem correctly)
    """
    # This SHOULD fail to demonstrate the problem
    float_result = 0.1 + 0.2
    float_passes = (float_result == 0.3)  # False - precision error

    # This SHOULD pass
    decimal_result = Decimal('0.1') + Decimal('0.2')
    decimal_passes = (decimal_result == Decimal('0.3'))  # True

    # Test passes if float fails and decimal succeeds
    return (not float_passes) and decimal_passes


def validate_variance_calculation(
    actual: Decimal,
    budget: Decimal,
    account_type: str
) -> Tuple[Decimal, Decimal | None, str]:
    """
    Calculate variance with proper edge case handling.

    Args:
        actual: Actual amount (must be Decimal)
        budget: Budget amount (must be Decimal)
        account_type: Type of account ('revenue', 'expense', 'asset', 'liability')

    Returns:
        (absolute_variance, percentage_variance, status)

    Raises:
        TypeError: If actual or budget are not Decimal
        ValueError: If account_type is invalid
    """
    # Validate types
    valid, msg = validate_currency_type(actual, "actual")
    if not valid:
        raise TypeError(msg)

    valid, msg = validate_currency_type(budget, "budget")
    if not valid:
        raise TypeError(msg)

    # Validate account type
    valid_types = {'revenue', 'expense', 'asset', 'liability'}
    if account_type not in valid_types:
        raise ValueError(f"account_type must be one of {valid_types}")

    # Calculate absolute variance
    absolute_variance = actual - budget

    # Calculate percentage variance (handle division by zero)
    if budget == Decimal('0'):
        percentage_variance = None  # Cannot calculate percentage
    else:
        percentage_variance = ((actual - budget) / budget) * Decimal('100')
        # Round to 2 decimal places
        percentage_variance = percentage_variance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Determine status
    if budget == Decimal('0') and actual == Decimal('0'):
        status = "No Activity"
    elif budget == Decimal('0'):
        status = "Flag for review - zero budget"
    else:
        status = "Normal"

    return absolute_variance, percentage_variance, status


def run_validation_tests() -> bool:
    """
    Run comprehensive validation tests.

    Returns:
        True if all tests pass
    """
    print("Running financial precision validation tests...\n")

    # Test 1: Float precision issue
    print("Test 1: Float precision demonstration")
    if test_float_precision():
        print("✓ PASS: Float precision issue confirmed, Decimal works correctly\n")
    else:
        print("✗ FAIL: Float precision test failed\n")
        return False

    # Test 2: Normal variance calculation
    print("Test 2: Normal variance calculation")
    abs_var, pct_var, status = validate_variance_calculation(
        Decimal('115000'), Decimal('100000'), 'revenue'
    )
    assert abs_var == Decimal('15000'), f"Expected 15000, got {abs_var}"
    assert pct_var == Decimal('15.00'), f"Expected 15.00%, got {pct_var}"
    assert status == "Normal"
    print("✓ PASS: Variance = $15,000, 15.00%, Normal\n")

    # Test 3: Zero division handling
    print("Test 3: Zero division handling")
    abs_var, pct_var, status = validate_variance_calculation(
        Decimal('50000'), Decimal('0'), 'expense'
    )
    assert abs_var == Decimal('50000')
    assert pct_var is None
    assert status == "Flag for review - zero budget"
    print("✓ PASS: Zero budget handled correctly (% = None)\n")

    # Test 4: Both zero
    print("Test 4: Both zero")
    abs_var, pct_var, status = validate_variance_calculation(
        Decimal('0'), Decimal('0'), 'revenue'
    )
    assert abs_var == Decimal('0')
    assert pct_var is None
    assert status == "No Activity"
    print("✓ PASS: Both zero handled correctly\n")

    # Test 5: Negative values
    print("Test 5: Negative values")
    abs_var, pct_var, status = validate_variance_calculation(
        Decimal('-12000'), Decimal('-10000'), 'liability'
    )
    assert abs_var == Decimal('-2000')
    assert pct_var == Decimal('20.00')
    print("✓ PASS: Negative values handled correctly\n")

    # Test 6: Type checking
    print("Test 6: Type checking (should reject float)")
    try:
        validate_variance_calculation(
            115000.00,  # float instead of Decimal
            Decimal('100000'),
            'revenue'
        )
        print("✗ FAIL: Should have rejected float type\n")
        return False
    except TypeError as e:
        print(f"✓ PASS: Correctly rejected float - {e}\n")

    print("="*50)
    print("ALL VALIDATION TESTS PASSED")
    print("="*50)
    return True


if __name__ == "__main__":
    success = run_validation_tests()
    sys.exit(0 if success else 1)
