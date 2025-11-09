#!/usr/bin/env python3
"""
validate_command_yaml.py - Validate YAML frontmatter in command .md files

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


def extract_yaml_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from markdown content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None

    yaml_content = match.group(1)
    frontmatter = {}

    # Parse simple YAML (key: value pairs, including lists)
    current_key = None
    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.startswith('- '):
            # List item
            if current_key and isinstance(frontmatter.get(current_key), list):
                frontmatter[current_key].append(line[2:].strip())
        elif ': ' in line:
            key, value = line.split(': ', 1)
            key = key.strip()
            value = value.strip()
            current_key = key

            # Check if value looks like a list start
            if value == '' or value == '[]':
                frontmatter[key] = []
            else:
                frontmatter[key] = value

    return frontmatter


def validate_command_yaml(content: str) -> Dict[str, Any]:
    """Validate command YAML frontmatter."""
    result = {
        'validator': 'validate_command_yaml',
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

    # Check required field: description
    if 'description' not in frontmatter:
        result['passed'] = False
        result['errors'].append('Missing required field: description')
    else:
        description = frontmatter['description']
        result['info']['description'] = description
        result['info']['description_length'] = len(description)

        # Validate description length (≤1024 chars per spec)
        if len(description) > 1024:
            result['warnings'].append(f'Description too long ({len(description)} chars, max 1024)')

        # Warn if description too short
        if len(description) < 20:
            result['warnings'].append(f'Description very short ({len(description)} chars, recommended ≥20)')

    # Optional fields validation
    if 'model' in frontmatter:
        model = frontmatter['model']
        result['info']['model'] = model
        valid_models = ['sonnet', 'opus', 'haiku']
        if model not in valid_models and not model.startswith('claude-'):
            result['warnings'].append(f'Model "{model}" not in common list: {valid_models}')

    if 'allowed-tools' in frontmatter:
        tools = frontmatter['allowed-tools']
        result['info']['allowed_tools'] = tools
        if isinstance(tools, list):
            result['info']['tool_count'] = len(tools)

    if 'argument-hint' in frontmatter:
        result['info']['argument_hint'] = frontmatter['argument-hint']

    if 'disable-model-invocation' in frontmatter:
        result['info']['disable_model_invocation'] = frontmatter['disable-model-invocation']

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_command_yaml.py <command_file.md>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(json.dumps({
            'validator': 'validate_command_yaml',
            'passed': False,
            'errors': [f'File not found: {file_path}'],
            'warnings': [],
            'info': {}
        }))
        sys.exit(1)

    content = file_path.read_text()
    result = validate_command_yaml(content)

    # Determine exit code
    exit_code = 0
    if not result['passed']:
        exit_code = 1
    elif result['warnings']:
        exit_code = 2

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
