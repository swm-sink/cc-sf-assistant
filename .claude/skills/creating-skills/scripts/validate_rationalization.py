#!/usr/bin/env python3
"""
validate_rationalization.py - Validate rationalization-proofing for discipline skills

Checks for:
- Iron Law statement (ALL CAPS code block)
- Red Flags list (≥8 entries with Reality checks)
- Rationalization Table (≥10 entries with Excuse | Reality | Counter-Argument)
- Explicit Negations (≥6 "Don't X" statements)
- CSO for violation symptoms

Exit codes:
  0 - Validation passed
  1 - Fatal error (missing Iron Law for discipline skill)
  2 - Warning (incomplete rationalization-proofing)

Output: JSON with validation results + human-readable summary
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any


def is_discipline_skill(content: str) -> bool:
    """Detect if skill is discipline type."""
    # Check for discipline-specific sections
    discipline_markers = ["## The Iron Law", "## Rationalization Table", "## Red Flags"]
    return any(marker in content for marker in discipline_markers)


def check_iron_law(content: str) -> Dict[str, Any]:
    """Check for Iron Law statement in code block."""
    result = {
        "has_iron_law": False,
        "iron_law_in_code_block": False,
        "iron_law_all_caps": False,
        "explicit_negations_count": 0,
    }

    # Check for Iron Law section
    if "## The Iron Law" in content:
        result["has_iron_law"] = True

        # Extract content between ## The Iron Law and next ##
        pattern = r"## The Iron Law\s*\n(.*?)(?=\n## |\Z)"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            iron_law_section = match.group(1)

            # Check for code block with ALL CAPS
            code_block_pattern = r"```\s*\n([A-Z\s]+)\s*\n```"
            code_match = re.search(code_block_pattern, iron_law_section)

            if code_match:
                result["iron_law_in_code_block"] = True
                iron_law_text = code_match.group(1).strip()

                # Check if ALL CAPS (at least 80% uppercase letters)
                letters = [c for c in iron_law_text if c.isalpha()]
                if letters:
                    uppercase_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
                    result["iron_law_all_caps"] = uppercase_ratio >= 0.8

            # Count explicit negations (Don't X, Never Y, NO X)
            negation_patterns = [
                r"Don't\s+\w+",
                r"Never\s+\w+",
                r"NO\s+[A-Z]+",
                r"Don't\s+\"[^\"]+\"",
            ]

            negation_count = 0
            for pattern in negation_patterns:
                negation_count += len(re.findall(pattern, iron_law_section))

            result["explicit_negations_count"] = negation_count

    return result


def check_red_flags(content: str) -> Dict[str, Any]:
    """Check for Red Flags list."""
    result = {"has_red_flags_section": False, "red_flags_count": 0, "has_reality_checks": False}

    if "## Red Flags" in content:
        result["has_red_flags_section"] = True

        # Extract content between ## Red Flags and next ##
        pattern = r"## Red Flags\s*\n(.*?)(?=\n## |\Z)"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            red_flags_section = match.group(1)

            # Count numbered/bulleted red flags
            # Pattern: 1. **Thinking:** or - **Thinking:** or **Thinking:**
            flag_pattern = r"\*\*Thinking:\*\*|\*\*Feeling:\*\*|\*\*Noticing:\*\*"
            red_flags_count = len(re.findall(flag_pattern, red_flags_section))
            result["red_flags_count"] = red_flags_count

            # Check for Reality checks
            if "**Reality:**" in red_flags_section:
                result["has_reality_checks"] = True

    return result


def check_rationalization_table(content: str) -> Dict[str, Any]:
    """Check for Rationalization Table."""
    result = {
        "has_rationalization_table": False,
        "table_entries_count": 0,
        "has_excuse_column": False,
        "has_reality_column": False,
        "has_counter_argument_column": False,
    }

    if "## Rationalization Table" in content:
        result["has_rationalization_table"] = True

        # Extract content between ## Rationalization Table and next ##
        pattern = r"## Rationalization Table\s*\n(.*?)(?=\n## |\Z)"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            table_section = match.group(1)

            # Check for table columns
            if "| Excuse |" in table_section or "|--------|" in table_section:
                result["has_excuse_column"] = True

            if "| Reality |" in table_section:
                result["has_reality_column"] = True

            if "| Counter-Argument |" in table_section:
                result["has_counter_argument_column"] = True

            # Count table rows (exclude header and separator rows)
            table_rows = [
                line for line in table_section.split("\n") if line.strip().startswith("|")
            ]
            # First row is header, second is separator
            entry_rows = [row for row in table_rows[2:] if not row.strip().startswith("|---")]
            result["table_entries_count"] = len(entry_rows)

    return result


def validate_rationalization(content: str) -> Dict[str, Any]:
    """Validate rationalization-proofing for discipline skills."""
    result = {
        "validator": "validate_rationalization",
        "passed": True,
        "errors": [],
        "warnings": [],
        "info": {},
    }

    # Check if discipline skill
    is_discipline = is_discipline_skill(content)
    result["info"]["is_discipline_skill"] = is_discipline

    if not is_discipline:
        result["info"]["note"] = "Not a discipline skill (rationalization-proofing not required)"
        return result

    # Check Iron Law
    iron_law_data = check_iron_law(content)
    result["info"].update(iron_law_data)

    if not iron_law_data["has_iron_law"]:
        result["passed"] = False
        result["errors"].append('Missing "The Iron Law" section (required for discipline skills)')
    else:
        if not iron_law_data["iron_law_in_code_block"]:
            result["warnings"].append("Iron Law should be in code block (```)")

        if not iron_law_data["iron_law_all_caps"]:
            result["warnings"].append("Iron Law should be ALL CAPS for emphasis")

        if iron_law_data["explicit_negations_count"] < 6:
            result["warnings"].append(
                f'Explicit negations count low: {iron_law_data["explicit_negations_count"]} (recommend ≥6)'
            )

    # Check Red Flags
    red_flags_data = check_red_flags(content)
    result["info"].update(red_flags_data)

    if not red_flags_data["has_red_flags_section"]:
        result["passed"] = False
        result["errors"].append('Missing "Red Flags" section (required for discipline skills)')
    else:
        if red_flags_data["red_flags_count"] < 8:
            result["warnings"].append(
                f'Red flags count low: {red_flags_data["red_flags_count"]} (recommend ≥8)'
            )

        if not red_flags_data["has_reality_checks"]:
            result["warnings"].append("Red flags should include Reality checks")

    # Check Rationalization Table
    table_data = check_rationalization_table(content)
    result["info"].update(table_data)

    if not table_data["has_rationalization_table"]:
        result["passed"] = False
        result["errors"].append(
            'Missing "Rationalization Table" section (required for discipline skills)'
        )
    else:
        if table_data["table_entries_count"] < 10:
            result["warnings"].append(
                f'Rationalization table entries low: {table_data["table_entries_count"]} (recommend ≥10)'
            )

        if not all(
            [
                table_data["has_excuse_column"],
                table_data["has_reality_column"],
                table_data["has_counter_argument_column"],
            ]
        ):
            result["warnings"].append(
                "Rationalization table should have Excuse | Reality | Counter-Argument columns"
            )

    return result


def format_human_readable(result: Dict[str, Any]) -> str:
    """Format validation result as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append("Rationalization-Proofing Validation")
    lines.append(f"{'='*60}")

    if result["passed"]:
        lines.append("\n✅ PASSED")
    else:
        lines.append("\n❌ FAILED")

    if result["info"].get("is_discipline_skill"):
        lines.append("\n🔒 Discipline Skill Detected")

        # Iron Law status
        if result["info"].get("has_iron_law"):
            lines.append("\n✅ Iron Law present")
            lines.append(
                f"   • In code block: {'✅' if result['info'].get('iron_law_in_code_block') else '⚠️'}"
            )
            lines.append(
                f"   • ALL CAPS: {'✅' if result['info'].get('iron_law_all_caps') else '⚠️'}"
            )
            lines.append(
                f"   • Explicit negations: {result['info'].get('explicit_negations_count', 0)} (target ≥6)"
            )

        # Red Flags status
        if result["info"].get("has_red_flags_section"):
            lines.append("\n✅ Red Flags present")
            lines.append(f"   • Count: {result['info'].get('red_flags_count', 0)} (target ≥8)")
            lines.append(
                f"   • Reality checks: {'✅' if result['info'].get('has_reality_checks') else '⚠️'}"
            )

        # Rationalization Table status
        if result["info"].get("has_rationalization_table"):
            lines.append("\n✅ Rationalization Table present")
            lines.append(
                f"   • Entries: {result['info'].get('table_entries_count', 0)} (target ≥10)"
            )
            lines.append(
                f"   • Excuse column: {'✅' if result['info'].get('has_excuse_column') else '❌'}"
            )
            lines.append(
                f"   • Reality column: {'✅' if result['info'].get('has_reality_column') else '❌'}"
            )
            lines.append(
                f"   • Counter-Argument column: {'✅' if result['info'].get('has_counter_argument_column') else '❌'}"
            )
    else:
        lines.append("\nℹ️  Not a discipline skill (rationalization-proofing not required)")

    if result["errors"]:
        lines.append(f"\n🚨 Errors ({len(result['errors'])}):")
        for error in result["errors"]:
            lines.append(f"  - {error}")

    if result["warnings"]:
        lines.append(f"\n⚠️  Warnings ({len(result['warnings'])}):")
        for warning in result["warnings"]:
            lines.append(f"  - {warning}")

    lines.append(f"\n{'='*60}\n")
    return "\n".join(lines)


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: validate_rationalization.py <path/to/SKILL.md>", file=sys.stderr)
        return 1

    skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print(f"Error: File not found: {skill_path}", file=sys.stderr)
        return 1

    # Read file content
    content = skill_path.read_text(encoding="utf-8")

    # Validate rationalization-proofing
    result = validate_rationalization(content)

    # Output JSON to stdout
    print(json.dumps(result, indent=2))

    # Output human-readable to stderr
    print(format_human_readable(result), file=sys.stderr)

    # Return exit code
    if not result["passed"]:
        return 1
    elif result["warnings"]:
        return 2
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
