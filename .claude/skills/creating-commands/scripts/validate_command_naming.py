#!/usr/bin/env python3
"""
validate_command_naming.py - Validate command file naming conventions

Exit codes:
  0 - Validation passed
  1 - Fatal error (invalid file pattern, wrong environment)
  2 - Warning (recommendations)

Checks:
  - File pattern: ^[a-z0-9]+(-[a-z0-9]+)*\.md$
  - Environment: File in dev/, prod/, or shared/ subdir
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any


def validate_command_naming(file_path: Path) -> Dict[str, Any]:
    """Validate command file naming conventions."""
    result = {
        'validator': 'validate_command_naming',
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }

    # Get filename
    filename = file_path.name
    result['info']['filename'] = filename

    # Validate file extension
    if not filename.endswith('.md'):
        result['passed'] = False
        result['errors'].append(f'File must have .md extension, got: {filename}')
        return result

    # Validate kebab-case pattern
    name_pattern = r'^[a-z0-9]+(-[a-z0-9]+)*\.md$'
    if not re.match(name_pattern, filename):
        result['passed'] = False
        result['errors'].append(f'Filename must be kebab-case (lowercase, hyphens): {filename}')
        result['info']['pattern'] = name_pattern

    # Extract command name (without .md extension)
    command_name = filename[:-3]
    result['info']['command_name'] = command_name

    # Validate environment (parent directory)
    parent_dir = file_path.parent.name
    result['info']['environment'] = parent_dir

    valid_environments = ['dev', 'prod', 'shared']
    if parent_dir not in valid_environments:
        result['passed'] = False
        result['errors'].append(f'Command must be in dev/, prod/, or shared/ directory, got: {parent_dir}/')
        result['info']['valid_environments'] = valid_environments

    # Check for uppercase letters (common mistake)
    if any(c.isupper() for c in command_name):
        result['errors'].append(f'Command name contains uppercase letters: {command_name}')
        result['passed'] = False

    # Check for underscores (should use hyphens)
    if '_' in command_name:
        suggested_name = command_name.replace('_', '-')
        result['errors'].append(f'Use hyphens instead of underscores. Suggested: {suggested_name}.md')
        result['passed'] = False

    # Warn if name is very short (might be too generic)
    if len(command_name) < 3:
        result['warnings'].append(f'Very short command name ({len(command_name)} chars). Consider more descriptive name.')

    # Warn if name is very long
    if len(command_name) > 50:
        result['warnings'].append(f'Very long command name ({len(command_name)} chars). Consider shorter name.')

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_command_naming.py <command_file.md>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(json.dumps({
            'validator': 'validate_command_naming',
            'passed': False,
            'errors': [f'File not found: {file_path}'],
            'warnings': [],
            'info': {}
        }))
        sys.exit(1)

    result = validate_command_naming(file_path)

    # Determine exit code
    exit_code = 0
    if not result['passed']:
        exit_code = 1
    elif result['warnings']:
        exit_code = 2

    # Output JSON result
    print(json.dumps(result, indent=2))

    # Human-readable summary
    print("\n--- Naming Validation Summary ---", file=sys.stderr)
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
