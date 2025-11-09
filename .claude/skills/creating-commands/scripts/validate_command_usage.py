#!/usr/bin/env python3
"""
validate_command_usage.py - Validate command usage line and arguments

Exit codes:
  0 - Validation passed
  1 - Fatal error (missing usage line, arg mismatch)
  2 - Warning (recommendations)

Checks:
  - Usage line present: **Usage:** /command <arg1> [arg2]
  - Arguments match argument-hint (if specified in YAML)
  - Positional args documented ($1, $2, $3 if used)
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def extract_yaml_frontmatter(content: str) -> Optional[Dict[str, str]]:
    """Extract YAML frontmatter from markdown content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None

    yaml_content = match.group(1)
    frontmatter = {}

    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ': ' in line:
            key, value = line.split(': ', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter


def extract_usage_line(content: str) -> Optional[str]:
    """Extract usage line from command file."""
    pattern = r'\*\*Usage:\*\*\s+(.+?)(?:\n|$)'
    match = re.search(pattern, content)
    return match.group(1).strip() if match else None


def parse_usage_args(usage_line: str) -> Dict[str, List[str]]:
    """Parse arguments from usage line."""
    result = {
        'required': [],
        'optional': []
    }

    # Extract command name and args
    parts = usage_line.split()
    if not parts:
        return result

    # Skip command name (first part, starts with /)
    args = parts[1:]

    for arg in args:
        # Required args: <arg> or {{ARG}}
        if arg.startswith('<') and arg.endswith('>'):
            result['required'].append(arg[1:-1])
        elif arg.startswith('{{') and arg.endswith('}}'):
            result['required'].append(arg[2:-2])
        # Optional args: [arg]
        elif arg.startswith('[') and arg.endswith(']'):
            optional_arg = arg[1:-1]
            # Strip any surrounding braces
            if optional_arg.startswith('{{') and optional_arg.endswith('}}'):
                optional_arg = optional_arg[2:-2]
            result['optional'].append(optional_arg)

    return result


def check_positional_args(content: str) -> List[str]:
    """Check for $1, $2, $3 usage in content."""
    positional_pattern = r'\$(\d+)'
    matches = re.findall(positional_pattern, content)
    return sorted(set(matches))


def validate_command_usage(content: str) -> Dict[str, Any]:
    """Validate command usage line and arguments."""
    result = {
        'validator': 'validate_command_usage',
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }

    # Extract YAML frontmatter
    frontmatter = extract_yaml_frontmatter(content)
    if frontmatter and 'argument-hint' in frontmatter:
        result['info']['argument_hint'] = frontmatter['argument-hint']

    # Check for usage line
    usage_line = extract_usage_line(content)
    if not usage_line:
        result['passed'] = False
        result['errors'].append('Missing usage line (**Usage:** /command <args>)')
        return result

    result['info']['usage_line'] = usage_line

    # Validate usage line format
    if not usage_line.startswith('/'):
        result['passed'] = False
        result['errors'].append('Usage line must start with / (slash command format)')

    # Parse arguments from usage line
    args = parse_usage_args(usage_line)
    result['info']['required_args'] = args['required']
    result['info']['optional_args'] = args['optional']
    result['info']['total_args'] = len(args['required']) + len(args['optional'])

    # Check if argument-hint matches usage line
    if frontmatter and 'argument-hint' in frontmatter:
        hint = frontmatter['argument-hint']
        # Simple check: hints should roughly match usage args
        hint_arg_count = len(re.findall(r'<[^>]+>', hint)) + len(re.findall(r'\[[^\]]+\]', hint))
        usage_arg_count = result['info']['total_args']

        if hint_arg_count != usage_arg_count:
            result['warnings'].append(
                f'Argument count mismatch: argument-hint has {hint_arg_count} args, '
                f'usage line has {usage_arg_count} args'
            )

    # Check for positional args ($1, $2, $3)
    positional_args = check_positional_args(content)
    if positional_args:
        result['info']['positional_args'] = positional_args

        # Verify positional args are documented in usage
        max_positional = int(max(positional_args)) if positional_args else 0
        total_documented = result['info']['total_args']

        if max_positional > total_documented:
            result['warnings'].append(
                f'Positional arg ${max_positional} used but only {total_documented} args in usage line'
            )

    # Warn if no arguments documented but placeholders exist
    if result['info']['total_args'] == 0:
        if '{{ARG' in content or '{{COMMAND_NAME}}' in content:
            result['warnings'].append('Template placeholders found but no arguments in usage line')

    # Check for common usage patterns
    if args['required']:
        # At least one required arg should be documented in content
        first_required = args['required'][0]
        # Simple check if arg name appears in content (case-insensitive)
        if first_required.lower() not in content.lower():
            result['warnings'].append(f'Required arg "{first_required}" not documented in content')

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_command_usage.py <command_file.md>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(json.dumps({
            'validator': 'validate_command_usage',
            'passed': False,
            'errors': [f'File not found: {file_path}'],
            'warnings': [],
            'info': {}
        }))
        sys.exit(1)

    content = file_path.read_text()
    result = validate_command_usage(content)

    # Determine exit code
    exit_code = 0
    if not result['passed']:
        exit_code = 1
    elif result['warnings']:
        exit_code = 2

    # Output JSON result
    print(json.dumps(result, indent=2))

    # Human-readable summary
    print("\n--- Usage Validation Summary ---", file=sys.stderr)
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
