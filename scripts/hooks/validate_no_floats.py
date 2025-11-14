#!/usr/bin/env python3
"""Pre-commit hook: Reject float() usage in financial calculation scripts.

Enforces Decimal-only precision to prevent rounding errors in financial code.
"""

import re
import sys
from pathlib import Path
from typing import List


def check_file(filepath: Path) -> bool:
    """Check if file contains float() usage.

    Returns:
        True if float() found (violation), False if clean
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"ERROR: Cannot read {filepath}: {e}", file=sys.stderr)
        return False

    violations: List[tuple[int, str]] = []
    for match in re.finditer(r"\bfloat\s*\(", content):
        line_num = content[: match.start()].count("\n") + 1
        lines = content.split("\n")
        line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ""

        if not line_content.startswith("#"):
            violations.append((line_num, line_content))

    if violations:
        print(f"\n❌ FLOAT USAGE DETECTED: {filepath}", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        for line_num, line_content in violations:
            print(f"  Line {line_num}: {line_content}", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        print("\n🔧 FIX: Replace float() with Decimal()", file=sys.stderr)
        print("   from decimal import Decimal", file=sys.stderr)
        print("   amount = Decimal('123.45')  # NOT float(123.45)", file=sys.stderr)
        print("\n📖 Reference: CLAUDE.md > Financial Domain Requirements", file=sys.stderr)
        print("💡 Read: .claude/prompts/fix-quality-issues.md\n", file=sys.stderr)
        return True

    return False


def main() -> int:
    """Main entry point for pre-commit hook."""
    if len(sys.argv) < 2:
        print("Usage: validate_no_floats.py <file1> [file2] ...", file=sys.stderr)
        return 0

    filepaths = [Path(arg) for arg in sys.argv[1:]]
    violations_found = False

    for filepath in filepaths:
        if not filepath.exists():
            print(f"WARNING: {filepath} does not exist, skipping", file=sys.stderr)
            continue

        if check_file(filepath):
            violations_found = True

    if violations_found:
        print("\n❌ COMMIT BLOCKED: Float usage in financial code", file=sys.stderr)
        print("   Fix violations above and re-commit\n", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
