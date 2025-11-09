#!/usr/bin/env python3
"""
validate_yaml.py - Validate YAML frontmatter in SKILL.md files

Exit codes:
  0 - Validation passed
  1 - Fatal error (missing YAML, invalid syntax, missing required fields)
  2 - Warning (recommendations, best practices)

Output: JSON with validation results + human-readable summary
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def extract_yaml_frontmatter(content: str) -> Optional[Dict[str, str]]:
    """Extract YAML frontmatter from markdown content."""
    # Match YAML frontmatter pattern: ---\nkey: value\n---
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None

    yaml_content = match.group(1)
    frontmatter = {}

    # Parse simple YAML (key: value pairs)
    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if ': ' in line:
            key, value = line.split(': ', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter


def validate_yaml_syntax(content: str) -> Dict[str, Any]:
    """Validate YAML frontmatter syntax and structure."""
    result = {
        'validator': 'validate_yaml',
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }

    # Check if YAML frontmatter exists
    if not content.startswith('---'):
        result['passed'] = False
        result['errors'].append('Missing YAML frontmatter (must start with ---)')
        return result

    # Extract frontmatter
    frontmatter = extract_yaml_frontmatter(content)

    if frontmatter is None:
        result['passed'] = False
        result['errors'].append('Invalid YAML frontmatter syntax (must end with ---)')
        return result

    # Check required fields
    required_fields = ['name', 'description']
    for field in required_fields:
        if field not in frontmatter:
            result['passed'] = False
            result['errors'].append(f'Missing required field: {field}')
        else:
            result['info'][field] = frontmatter[field]

    # Validate name field (kebab-case)
    if 'name' in frontmatter:
        name = frontmatter['name']
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
            result['passed'] = False
            result['errors'].append(f'Invalid name format: "{name}" (must be kebab-case: lowercase, hyphens only)')

    # Validate description field (should be non-empty)
    if 'description' in frontmatter:
        description = frontmatter['description']
        if len(description) < 20:
            result['warnings'].append(f'Description too short: {len(description)} chars (recommend ≥50 chars for CSO)')

        # Check for CSO keyword richness (basic heuristic)
        keyword_indicators = [
            'when', 'before', 'after', 'use when', 'thinking', 'noticing',
            'under pressure', 'need to', 'want to', 'experiencing'
        ]
        keyword_count = sum(1 for keyword in keyword_indicators if keyword.lower() in description.lower())
        result['info']['cso_keyword_count'] = keyword_count

        if keyword_count < 3:
            result['warnings'].append(f'Description has low CSO keyword count: {keyword_count} (recommend ≥3 for discoverability)')

    return result


def format_human_readable(result: Dict[str, Any]) -> str:
    """Format validation result as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"YAML Frontmatter Validation")
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
            if key == 'description':
                # Truncate long descriptions
                display_value = value[:80] + '...' if len(value) > 80 else value
                lines.append(f"  - {key}: {display_value}")
            else:
                lines.append(f"  - {key}: {value}")

    lines.append(f"\n{'='*60}\n")
    return '\n'.join(lines)


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: validate_yaml.py <path/to/SKILL.md>", file=sys.stderr)
        return 1

    skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print(f"Error: File not found: {skill_path}", file=sys.stderr)
        return 1

    # Read file content
    content = skill_path.read_text(encoding='utf-8')

    # Validate YAML
    result = validate_yaml_syntax(content)

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
