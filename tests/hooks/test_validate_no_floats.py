"""
Tests for float validator pre-commit hook.

Purpose:
    Validate that the float validator correctly detects float() usage in financial code
    and blocks commits that violate Decimal precision requirements.
"""

from pathlib import Path
import subprocess
import tempfile


def test_float_validator_detects_float_usage() -> None:
    """Test that validator detects float() in Python files."""
    # Create temporary file with float usage
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("amount = float(123.45)\n")
        temp_file = Path(f.name)

    try:
        # Run validator
        result = subprocess.run(
            ["python", "scripts/hooks/validate_no_floats.py", str(temp_file)],
            capture_output=True,
            text=True,
        )

        # Should fail (exit code 1)
        assert result.returncode == 1
        assert "FLOAT USAGE DETECTED" in result.stderr
    finally:
        temp_file.unlink()


def test_float_validator_passes_decimal_usage() -> None:
    """Test that validator passes when Decimal is used."""
    # Create temporary file with Decimal usage
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("from decimal import Decimal\namount = Decimal('123.45')\n")
        temp_file = Path(f.name)

    try:
        # Run validator
        result = subprocess.run(
            ["python", "scripts/hooks/validate_no_floats.py", str(temp_file)],
            capture_output=True,
            text=True,
        )

        # Should pass (exit code 0)
        assert result.returncode == 0
    finally:
        temp_file.unlink()


def test_float_validator_ignores_comments() -> None:
    """Test that validator ignores float mentions in comments."""
    # Create temporary file with float in comment
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("# Do not use float() for currency\namount = Decimal('123.45')\n")
        temp_file = Path(f.name)

    try:
        # Run validator
        result = subprocess.run(
            ["python", "scripts/hooks/validate_no_floats.py", str(temp_file)],
            capture_output=True,
            text=True,
        )

        # Should pass (exit code 0)
        assert result.returncode == 0
    finally:
        temp_file.unlink()


def test_float_validator_detects_float_with_whitespace() -> None:
    """Test that validator detects float( with various whitespace."""
    test_cases = [
        "amount = float(value)",
        "amount = float (value)",
        "amount = float  (value)",
    ]

    for code in test_cases:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code + "\n")
            temp_file = Path(f.name)

        try:
            result = subprocess.run(
                ["python", "scripts/hooks/validate_no_floats.py", str(temp_file)],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 1, f"Should detect float in: {code}"
            assert "FLOAT USAGE DETECTED" in result.stderr
        finally:
            temp_file.unlink()


def test_float_validator_handles_nonexistent_file() -> None:
    """Test that validator handles nonexistent files gracefully."""
    result = subprocess.run(
        ["python", "scripts/hooks/validate_no_floats.py", "/nonexistent/file.py"],
        capture_output=True,
        text=True,
    )

    # Should not crash, but warn and pass
    assert "does not exist" in result.stderr or result.returncode == 0
