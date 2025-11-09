#!/usr/bin/env python3
"""
validate_structure.py - Validate skill structure based on type

Checks for:
- Required sections for each skill type (technique/pattern/discipline/reference)
- Section order
- Line count targets

Exit codes:
  0 - Validation passed
  1 - Fatal error (missing required sections)
  2 - Warning (section order, line count recommendations)

Output: JSON with validation results + human-readable summary
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set


# Required sections for each skill type
REQUIRED_SECTIONS = {
    'technique': [
        'Overview',
        'When to Use',
        'Step-by-Step Instructions',
        'Common Pitfalls',
        'Examples',
        'Progressive Disclosure'
    ],
    'pattern': [
        'Overview',
        'The Problem',
        'The Solution Pattern',
        'Before/After Comparison',
        'When to Apply',
        'Examples',
        'Progressive Disclosure'
    ],
    'discipline': [
        'Overview',
        'The Iron Law',
        'Red Flags',
        'The Workflow',
        'Rationalization Table',
        'Checkpoint Requirements',
        'Emergency Override Protocol',
        'Examples',
        'Testing This Skill',
        'How to Resist Shortcuts',
        'Meta',
        'Progressive Disclosure'
    ],
    'reference': [
        'Overview',
        'Quick Reference',
        'Detailed Reference',
        'Examples',
        'Progressive Disclosure'
    ]
}


def extract_sections(content: str) -> List[str]:
    """Extract section headings from markdown content."""
    # Match ## Section Name patterns
    pattern = r'^## (.+?)$'
    sections = re.findall(pattern, content, re.MULTILINE)
    return sections


def detect_skill_type(content: str, sections: List[str]) -> Optional[str]:
    """Detect skill type based on sections present."""
    # Check for discipline-specific sections
    if 'The Iron Law' in sections or 'Rationalization Table' in sections:
        return 'discipline'

    # Check for pattern-specific sections
    if 'The Problem' in sections and 'The Solution Pattern' in sections:
        return 'pattern'

    # Check for reference-specific sections
    if 'Quick Reference' in sections and 'Detailed Reference' in sections:
        return 'reference'

    # Default to technique if has step-by-step
    if 'Step-by-Step Instructions' in sections:
        return 'technique'

    # Cannot determine
    return None


def count_lines(content: str) -> int:
    """Count non-empty lines in content."""
    return len([line for line in content.split('\n') if line.strip()])


def validate_structure(content: str) -> Dict[str, Any]:
    """Validate skill structure."""
    result = {
        'validator': 'validate_structure',
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }

    # Extract sections
    sections = extract_sections(content)
    result['info']['sections_found'] = sections
    result['info']['section_count'] = len(sections)

    # Detect skill type
    skill_type = detect_skill_type(content, sections)

    if skill_type is None:
        result['passed'] = False
        result['errors'].append('Cannot detect skill type (technique/pattern/discipline/reference)')
        result['errors'].append(f'Sections found: {", ".join(sections)}')
        return result

    result['info']['detected_type'] = skill_type

    # Check required sections for type
    required = REQUIRED_SECTIONS[skill_type]
    result['info']['required_sections'] = required

    missing_sections = [sec for sec in required if sec not in sections]
    extra_sections = [sec for sec in sections if sec not in required]

    if missing_sections:
        result['passed'] = False
        for section in missing_sections:
            result['errors'].append(f'Missing required section for {skill_type} type: "{section}"')

    if extra_sections:
        # Extra sections are warnings, not errors
        for section in extra_sections:
            result['warnings'].append(f'Extra section (not in {skill_type} template): "{section}"')

    # Check section order
    present_required = [sec for sec in required if sec in sections]
    actual_order = [sec for sec in sections if sec in required]

    if present_required != actual_order:
        result['warnings'].append('Sections out of order')
        result['info']['expected_order'] = present_required
        result['info']['actual_order'] = actual_order

    # Check line count
    line_count = count_lines(content)
    result['info']['line_count'] = line_count

    if line_count > 250:
        result['warnings'].append(f'Line count high: {line_count} lines (recommend <200, use references/ for details)')
    elif line_count < 50:
        result['warnings'].append(f'Line count low: {line_count} lines (skill may be incomplete)')

    # Type-specific validations
    if skill_type == 'discipline':
        # Discipline skills should have Iron Law in code block
        if '```' not in content:
            result['warnings'].append('Discipline skill should have Iron Law in code block (```)')

        # Should have rationalization table
        if '|' not in content:
            result['warnings'].append('Discipline skill should have rationalization table with | separators')

    return result


def format_human_readable(result: Dict[str, Any]) -> str:
    """Format validation result as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"Structure Validation")
    lines.append(f"{'='*60}")

    if result['passed']:
        lines.append("\n✅ PASSED")
    else:
        lines.append("\n❌ FAILED")

    if result['errors']:
        lines.append(f"\n🚨 Errors ({len(result['errors'])}):")
        for error in result['errors']:
            lines.append(f"  - {error}")

    if result['warnings']:
        lines.append(f"\n⚠️  Warnings ({len(result['warnings'])}):")
        for warning in result['warnings']:
            lines.append(f"  - {warning}")

    if result['info']:
        lines.append(f"\nℹ️  Info:")
        for key, value in result['info'].items():
            if key in ['sections_found', 'required_sections', 'expected_order', 'actual_order']:
                # Format lists nicely
                if isinstance(value, list):
                    lines.append(f"  - {key}:")
                    for item in value:
                        lines.append(f"      • {item}")
            else:
                lines.append(f"  - {key}: {value}")

    lines.append(f"\n{'='*60}\n")
    return '\n'.join(lines)


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: validate_structure.py <path/to/SKILL.md>", file=sys.stderr)
        return 1

    skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print(f"Error: File not found: {skill_path}", file=sys.stderr)
        return 1

    # Read file content
    content = skill_path.read_text(encoding='utf-8')

    # Validate structure
    result = validate_structure(content)

    # Output JSON to stdout
    print(json.dumps(result, indent=2))

    # Output human-readable to stderr
    print(format_human_readable(result), file=sys.stderr)

    # Return exit code
    if not result['passed']:
        return 1
    elif result['warnings']:
        return 2
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
