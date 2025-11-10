#!/usr/bin/env python3
"""Integration validator for component interactions."""

from pathlib import Path
from typing import List, Dict, Any
import re


def validate_command_agent_integration(command_file: Path) -> List[str]:
    """Validate that commands correctly reference agents.

    Args:
        command_file: Path to command .md file

    Returns:
        List of integration errors
    """
    errors = []

    with open(command_file, 'r') as f:
        content = f.read()

    # Find agent references (e.g., @agent-name)
    agent_refs = re.findall(r'@([a-z][a-z0-9-]+)', content)

    # Check if referenced agents exist
    agents_dir = Path('.claude/agents')
    for agent_ref in set(agent_refs):
        # Check in all agent subdirectories
        found = False
        if agents_dir.exists():
            for agent_file in agents_dir.rglob(f'{agent_ref}.md'):
                found = True
                break

        if not found:
            errors.append(f"Referenced agent @{agent_ref} not found in .claude/agents/")

    return errors


def validate_skill_template_integration(skill_dir: Path) -> List[str]:
    """Validate that skills correctly reference templates.

    Args:
        skill_dir: Path to skill directory

    Returns:
        List of integration errors
    """
    errors = []

    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        return []

    with open(skill_md, 'r') as f:
        content = f.read()

    # Find template references
    template_refs = re.findall(r'templates/([a-z][a-z0-9-]+\.[a-z]+)', content)

    templates_dir = skill_dir / 'templates'
    for template_ref in set(template_refs):
        template_path = templates_dir / template_ref
        if not template_path.exists():
            errors.append(f"Referenced template {template_ref} not found in templates/")

    return errors


def validate_component_integration(component_path: Path) -> Dict[str, Any]:
    """Validate component integration.

    Args:
        component_path: Path to component

    Returns:
        Validation result dictionary
    """
    result = {
        'path': str(component_path),
        'valid': True,
        'errors': []
    }

    if component_path.is_dir() and (component_path / 'SKILL.md').exists():
        # Validate skill-template integration
        result['errors'] = validate_skill_template_integration(component_path)
    elif component_path.is_file() and 'commands' in component_path.parts:
        # Validate command-agent integration
        result['errors'] = validate_command_agent_integration(component_path)

    result['valid'] = len(result['errors']) == 0
    return result


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: integration-validator.py <component_path>")
        sys.exit(1)

    component_path = Path(sys.argv[1])
    result = validate_component_integration(component_path)

    print(f"Path: {result['path']}")
    print(f"Valid: {result['valid']}")

    if result['errors']:
        print("\nIntegration Errors:")
        for error in result['errors']:
            print(f"  - {error}")

    sys.exit(0 if result['valid'] else 1)
