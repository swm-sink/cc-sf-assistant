#!/usr/bin/env python3
"""
validate_agent_yaml.py - Validate YAML frontmatter in agent .md files

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
        elif ': ' in line or line.endswith(':'):
            key, value = (line.split(': ', 1) + [''])[:2]
            key = key.strip()
            value = value.strip()
            current_key = key

            # Check if value looks like a list start
            if value == '' or value == '[]':
                frontmatter[key] = []
            else:
                frontmatter[key] = value

    return frontmatter


def validate_agent_yaml(content: str) -> Dict[str, Any]:
    """Validate agent YAML frontmatter."""
    result = {
        'validator': 'validate_agent_yaml',
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

    # Check required field: name
    if 'name' not in frontmatter:
        result['passed'] = False
        result['errors'].append('Missing required field: name')
    else:
        name = frontmatter['name']
        result['info']['name'] = name

        # Validate name format (kebab-case)
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
            result['passed'] = False
            result['errors'].append(f'Agent name "{name}" is not kebab-case')

    # Check required field: description
    if 'description' not in frontmatter:
        result['passed'] = False
        result['errors'].append('Missing required field: description')
    else:
        description = frontmatter['description']
        result['info']['description'] = description
        result['info']['description_length'] = len(description)

        # Validate description length (100-150 chars recommended)
        if len(description) < 100:
            result['warnings'].append(f'Description short ({len(description)} chars, recommended 100-150)')
        elif len(description) > 150:
            result['warnings'].append(f'Description long ({len(description)} chars, recommended 100-150)')

    # Optional field: tools
    if 'tools' in frontmatter:
        tools = frontmatter['tools']
        result['info']['tools'] = tools
        if isinstance(tools, list):
            result['info']['tool_count'] = len(tools)
        else:
            result['warnings'].append('Tools field should be a list')

    # Optional field: model
    if 'model' in frontmatter:
        model = frontmatter['model']
        result['info']['model'] = model
        valid_models = ['sonnet', 'opus', 'haiku']
        if model not in valid_models and not model.startswith('claude-'):
            result['warnings'].append(f'Model "{model}" not in common list: {valid_models}')

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_agent_yaml.py <agent_file.md>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(json.dumps({
            'validator': 'validate_agent_yaml',
            'passed': False,
            'errors': [f'File not found: {file_path}'],
            'warnings': [],
            'info': {}
        }))
        sys.exit(1)

    content = file_path.read_text()
    result = validate_agent_yaml(content)

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
