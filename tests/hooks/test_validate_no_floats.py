"""Tests for float validator pre-commit hook."""
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.hooks import validate_no_floats  # noqa: E402


def test_float_validator_detects_float_usage() -> None:
    """Test that validator detects float() in Python files."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("amount = float(123.45)\n")
        temp_file = Path(f.name)

    try:
        result = subprocess.run(
            ["python", "scripts/hooks/validate_no_floats.py", str(temp_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "FLOAT USAGE DETECTED" in result.stderr
    finally:
        temp_file.unlink()


def test_float_validator_passes_decimal_usage() -> None:
    """Test that validator passes when Decimal is used."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("from decimal import Decimal\namount = Decimal('123.45')\n")
        temp_file = Path(f.name)

    try:
        result = subprocess.run(
            ["python", "scripts/hooks/validate_no_floats.py", str(temp_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
    finally:
        temp_file.unlink()


def test_float_validator_ignores_comments() -> None:
    """Test that validator ignores float mentions in comments."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("# Do not use float() for currency\namount = Decimal('123.45')\n")
        temp_file = Path(f.name)

    try:
        result = subprocess.run(
            ["python", "scripts/hooks/validate_no_floats.py", str(temp_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
    finally:
        temp_file.unlink()


def test_float_validator_detects_float_with_whitespace() -> None:
    """Test that validator detects float( with various whitespace."""
    test_cases = ["amount = float(value)", "amount = float (value)"]

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
            assert result.returncode == 1
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
    assert "does not exist" in result.stderr or result.returncode == 0


def test_float_validator_with_no_arguments() -> None:
    """Test validator prints usage when called with no arguments."""
    result = subprocess.run(
        ["python", "scripts/hooks/validate_no_floats.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Usage:" in result.stderr


def test_float_validator_check_file_read_error() -> None:
    """Test check_file() handles read errors gracefully."""
    with patch.object(Path, "read_text", side_effect=OSError("Permission denied")):
        result = validate_no_floats.check_file(Path("fake_file.py"))
    assert result is False
