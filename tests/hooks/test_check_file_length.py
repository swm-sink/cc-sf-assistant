"""Tests for check_file_length.py pre-commit hook."""

import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.hooks import check_file_length  # noqa: E402


def test_check_file_length_with_short_file() -> None:
    """Test file length checker passes files under 100 lines."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("# Short file\n" * 50)
        temp_file = Path(f.name)

    try:
        result = subprocess.run(
            ["python", "scripts/hooks/check_file_length.py", str(temp_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "FILE TOO LONG" not in result.stderr
    finally:
        temp_file.unlink()


def test_check_file_length_with_long_file() -> None:
    """Test file length checker fails files over 100 lines."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("# Long file\n" * 150)
        temp_file = Path(f.name)

    try:
        result = subprocess.run(
            ["python", "scripts/hooks/check_file_length.py", str(temp_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "FILE TOO LONG" in result.stderr
        assert "151 lines" in result.stderr
    finally:
        temp_file.unlink()


def test_check_file_length_with_no_arguments() -> None:
    """Test file length checker with no arguments."""
    result = subprocess.run(
        ["python", "scripts/hooks/check_file_length.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_file_length_read_error() -> None:
    """Test check_file_length() handles read errors gracefully."""
    test_file = Path("fake_file.py")

    with patch.object(Path, "read_text", side_effect=OSError("Permission denied")):
        result = check_file_length.check_file_length(test_file)

    assert result is False
