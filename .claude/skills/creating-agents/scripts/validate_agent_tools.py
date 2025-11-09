#!/usr/bin/env python3
"""
validate_agent_tools.py - Validate tool tier compliance for agent .md files

Exit codes:
  0 - Validation passed
  1 - Fatal error (incorrect tool tier, missing tools field)
  2 - Warning (recommendations)

Output: JSON with validation results + human-readable summary

Tool Tiers:
- Reviewer (read-only): [Read, Grep, Glob]
- Researcher (read+web): [Read, Grep, Glob, WebFetch, WebSearch]
- Domain Specialist (full): [Read, Write, Edit, Bash, Glob, Grep]
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set


# Define tool tiers
TOOL_TIERS = {
    'reviewer': {'Read', 'Grep', 'Glob'},
    'researcher': {'Read', 'Grep', 'Glob', 'WebFetch', 'WebSearch'},
    'domain-specialist': {'Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep'}
}


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


def detect_agent_type(content: str) -> Optional[str]:
    """Detect agent type from content patterns."""
    # Check for read-only restrictions in content
    if 'Read-only' in content or 'read-only' in content or 'WITHOUT modifying' in content:
        if 'WebFetch' in content or 'WebSearch' in content or 'web research' in content.lower():
            return 'researcher'
        return 'reviewer'

    # Check for domain specialist patterns
    if 'Domain Specialist' in content or 'domain specialist' in content:
        return 'domain-specialist'

    # Check for researcher patterns
    if 'researcher' in content.lower() or 'research analyst' in content.lower():
        return 'researcher'

    # Check for reviewer patterns
    if 'reviewer' in content.lower() or 'auditor' in content.lower():
        return 'reviewer'

    return None


def validate_agent_tools(content: str) -> Dict[str, Any]:
    """Validate agent tool tier compliance."""
    result = {
        'validator': 'validate_agent_tools',
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }

    # Extract frontmatter
    frontmatter = extract_yaml_frontmatter(content)

    if frontmatter is None:
        result['passed'] = False
        result['errors'].append('Could not extract YAML frontmatter')
        return result

    # Check if tools field exists
    if 'tools' not in frontmatter:
        result['warnings'].append('No tools field in YAML (tools not restricted)')
        return result

    tools = frontmatter.get('tools', [])
    if not isinstance(tools, list):
        result['passed'] = False
        result['errors'].append('Tools field must be a list')
        return result

    tools_set = set(tools)
    result['info']['tools'] = sorted(tools)
    result['info']['tool_count'] = len(tools)

    # Detect agent type from content
    agent_type = detect_agent_type(content)
    result['info']['detected_type'] = agent_type or 'unknown'

    # Validate tool tier
    if agent_type:
        expected_tools = TOOL_TIERS[agent_type]
        result['info']['expected_tools'] = sorted(expected_tools)

        if tools_set != expected_tools:
            result['passed'] = False
            missing = expected_tools - tools_set
            extra = tools_set - expected_tools

            error_msg = f'{agent_type.title()} agent tool mismatch.'
            if missing:
                error_msg += f' Missing: {sorted(missing)}.'
            if extra:
                error_msg += f' Extra: {sorted(extra)}.'
            error_msg += f' Expected: {sorted(expected_tools)}'

            result['errors'].append(error_msg)
    else:
        # Unknown type, check against all tiers
        matched_tier = None
        for tier_name, tier_tools in TOOL_TIERS.items():
            if tools_set == tier_tools:
                matched_tier = tier_name
                break

        if matched_tier:
            result['info']['matched_tier'] = matched_tier
            result['warnings'].append(f'Tools match {matched_tier} tier, but agent type not clearly detected')
        else:
            result['warnings'].append('Tools do not match any standard tier (Reviewer/Researcher/Domain Specialist)')

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_agent_tools.py <agent_file.md>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(json.dumps({
            'validator': 'validate_agent_tools',
            'passed': False,
            'errors': [f'File not found: {file_path}'],
            'warnings': [],
            'info': {}
        }))
        sys.exit(1)

    content = file_path.read_text()
    result = validate_agent_tools(content)

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
