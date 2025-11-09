#!/usr/bin/env python3
"""
validate_agent_naming.py - Validate naming conventions for agent .md files

Exit codes:
  0 - Validation passed
  1 - Fatal error (invalid name format, file/name mismatch)

Output: JSON with validation results + human-readable summary
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, Optional


def extract_agent_name_from_yaml(content: str) -> Optional[str]:
    """Extract agent name from YAML frontmatter."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None

    yaml_content = match.group(1)

    for line in yaml_content.split('\n'):
        line = line.strip()
        if line.startswith('name:'):
            name = line.split(':', 1)[1].strip()
            return name

    return None


def validate_agent_naming(file_path: Path, content: str) -> Dict[str, Any]:
    """Validate agent naming conventions."""
    result = {
        'validator': 'validate_agent_naming',
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }

    # Check file name format (kebab-case)
    file_name = file_path.stem  # without .md extension
    kebab_case_pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'

    if not re.match(kebab_case_pattern, file_name):
        result['passed'] = False
        result['errors'].append(f'File name "{file_name}" is not kebab-case (e.g., "code-reviewer")')

    result['info']['file_name'] = file_name

    # Extract agent name from YAML
    agent_name = extract_agent_name_from_yaml(content)

    if agent_name is None:
        result['passed'] = False
        result['errors'].append('Could not find "name" field in YAML frontmatter')
        return result

    result['info']['agent_name'] = agent_name

    # Check agent name format (kebab-case)
    if not re.match(kebab_case_pattern, agent_name):
        result['passed'] = False
        result['errors'].append(f'Agent name "{agent_name}" is not kebab-case')

    # Check file name matches agent name
    if file_name != agent_name:
        result['passed'] = False
        result['errors'].append(f'File name "{file_name}.md" does not match agent name "{agent_name}"')

    # Check file location (should be in .claude/agents/)
    # This is a check if file_path contains 'agents' directory
    if '.claude/agents' not in str(file_path):
        result['warnings'].append(f'File not in .claude/agents/ directory: {file_path}')

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_agent_naming.py <agent_file.md>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(json.dumps({
            'validator': 'validate_agent_naming',
            'passed': False,
            'errors': [f'File not found: {file_path}'],
            'warnings': [],
            'info': {}
        }))
        sys.exit(1)

    content = file_path.read_text()
    result = validate_agent_naming(file_path, content)

    # Determine exit code
    exit_code = 0
    if not result['passed']:
        exit_code = 1
    elif result['warnings']:
        exit_code = 0  # Warnings don't fail validation for naming

    # Output JSON result
    print(json.dumps(result, indent=2))

    # Human-readable summary
    print("\n--- Validation Summary ---", file=sys.stderr)
    print(f"File: {file_path}", file=sys.stderr)
    print(f"Status: {'✅ PASS' if result['passed'] else '❌ FAIL'}", file=sys.stderr)

    if result['errors']:
        print(f"Errors: {len(result['errors'])}", file=sys.stderr)
        for error in result['errors']:
            print(f"  ❌ {error}", file=sys.stderr)

    if result['warnings']:
        print(f"Warnings: {len(result['warnings'])}", file=sys.stderr)
        for warning in result['warnings']:
            print(f"  ⚠️ {warning}", file=sys.stderr)

    if result['info']:
        print("Info:", file=sys.stderr)
        for key, value in result['info'].items():
            print(f"  - {key}: {value}", file=sys.stderr)

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
