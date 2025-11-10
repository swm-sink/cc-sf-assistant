#!/usr/bin/env python3
"""File naming convention validator."""

from pathlib import Path
from typing import List, Dict, Any
import re


def is_kebab_case(name: str) -> bool:
    """Check if name is in kebab-case format.

    Args:
        name: String to check

    Returns:
        True if kebab-case, False otherwise
    """
    # kebab-case: lowercase letters, numbers, hyphens only
    # Must start with letter, no consecutive hyphens
    pattern = r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$'
    return bool(re.match(pattern, name))


def validate_skill_naming(skill_dir: Path) -> List[str]:
    """Validate skill directory and file naming.

    Expected:
    - Directory: kebab-case (e.g., hook-factory)
    - Main file: SKILL.md (exactly)
    - References: kebab-case.md in references/
    - Templates: kebab-case.template in templates/

    Args:
        skill_dir: Path to skill directory

    Returns:
        List of validation errors
    """
    errors = []

    # Check directory name
    if not is_kebab_case(skill_dir.name):
        errors.append(f"Directory name '{skill_dir.name}' not kebab-case")

    # Check SKILL.md exists
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        errors.append("SKILL.md not found")

    # Check references/ files
    refs_dir = skill_dir / 'references'
    if refs_dir.exists():
        for ref_file in refs_dir.glob('*.md'):
            if not is_kebab_case(ref_file.stem):
                errors.append(f"Reference file '{ref_file.name}' not kebab-case")

    # Check templates/ files
    templates_dir = skill_dir / 'templates'
    if templates_dir.exists():
        for template_file in templates_dir.iterdir():
            if template_file.is_file():
                # Templates can have various extensions
                name_without_ext = template_file.stem
                if not is_kebab_case(name_without_ext):
                    errors.append(f"Template file '{template_file.name}' not kebab-case")

    return errors


def validate_agent_naming(agent_file: Path) -> List[str]:
    """Validate agent file naming.

    Expected: kebab-case.md (e.g., databricks-validator.md)

    Args:
        agent_file: Path to agent .md file

    Returns:
        List of validation errors
    """
    errors = []

    if agent_file.suffix != '.md':
        errors.append(f"Agent file must have .md extension, got {agent_file.suffix}")

    if not is_kebab_case(agent_file.stem):
        errors.append(f"Agent filename '{agent_file.name}' not kebab-case")

    return errors


def validate_command_naming(command_file: Path) -> List[str]:
    """Validate command file naming.

    Expected: kebab-case.md (e.g., variance-analysis.md)

    Args:
        command_file: Path to command .md file

    Returns:
        List of validation errors
    """
    errors = []

    if command_file.suffix != '.md':
        errors.append(f"Command file must have .md extension, got {command_file.suffix}")

    if not is_kebab_case(command_file.stem):
        errors.append(f"Command filename '{command_file.name}' not kebab-case")

    return errors


def validate_component_naming(component_path: Path) -> Dict[str, Any]:
    """Validate component naming based on type.

    Args:
        component_path: Path to component (directory or file)

    Returns:
        Validation result dictionary
    """
    result = {
        'path': str(component_path),
        'valid': True,
        'errors': []
    }

    # Determine component type
    if component_path.is_dir() and (component_path / 'SKILL.md').exists():
        result['errors'] = validate_skill_naming(component_path)
    elif component_path.is_file() and component_path.suffix == '.md':
        if 'agents' in component_path.parts:
            result['errors'] = validate_agent_naming(component_path)
        elif 'commands' in component_path.parts:
            result['errors'] = validate_command_naming(component_path)
    else:
        result['errors'] = [f"Unknown component type: {component_path}"]

    result['valid'] = len(result['errors']) == 0
    return result


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: naming-validator.py <component_path>")
        sys.exit(1)

    component_path = Path(sys.argv[1])
    result = validate_component_naming(component_path)

    print(f"Path: {result['path']}")
    print(f"Valid: {result['valid']}")

    if result['errors']:
        print("\nErrors:")
        for error in result['errors']:
            print(f"  - {error}")

    sys.exit(0 if result['valid'] else 1)
