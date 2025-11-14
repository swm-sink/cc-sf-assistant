#!/usr/bin/env python3
"""
Pre-commit hook: Enforce 100-line file length limit.

Purpose:
    Ensure all Python files are ≤100 lines to maintain readability and modularity.
    Files exceeding limit should be refactored into smaller modules.

Returns:
    0 if all files pass, 1 if any file exceeds 100 lines
"""

import sys
from pathlib import Path


def check_file_length(filepath: Path, max_lines: int = 100) -> bool:
    """Check if file exceeds max line count.

    Args:
        filepath: Path to Python file
        max_lines: Maximum allowed lines (default: 100)

    Returns:
        True if file exceeds limit (violation), False if within limit
    """
    try:
        lines = filepath.read_text(encoding="utf-8").split("\n")
        line_count = len(lines)

        if line_count > max_lines:
            print(
                f"❌ FILE TOO LONG: {filepath} ({line_count} lines, max: {max_lines})",
                file=sys.stderr,
            )
            print(f"   Refactor into smaller modules (<{max_lines} lines each)\n", file=sys.stderr)
            return True

        return False
    except Exception as e:
        print(f"ERROR: Cannot read {filepath}: {e}", file=sys.stderr)
        return False


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        return 0

    violations_found = False
    for filepath_str in sys.argv[1:]:
        filepath = Path(filepath_str)
        if filepath.exists() and check_file_length(filepath):
            violations_found = True

    if violations_found:
        print("❌ COMMIT BLOCKED: Files exceed 100-line limit\n", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
