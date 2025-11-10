#!/usr/bin/env python3
"""Directory structure validator."""

from pathlib import Path
from typing import List, Dict, Any


def validate_skill_structure(skill_dir: Path) -> List[str]:
    """Validate skill directory structure.

    Required:
    - SKILL.md (main file)
    - README.md (user-facing documentation)

    Optional but recommended:
    - references/ (detailed documentation)
    - templates/ (code templates if applicable)
    - validators/ (validator scripts if applicable)

    Progressive disclosure check:
    - SKILL.md should be ≤200 lines

    Args:
        skill_dir: Path to skill directory

    Returns:
        List of validation errors and warnings
    """
    errors = []

    # Check required files
    if not (skill_dir / 'SKILL.md').exists():
        errors.append("Missing required file: SKILL.md")

    if not (skill_dir / 'README.md').exists():
        errors.append("Warning: Missing README.md (recommended)")

    # Check SKILL.md size (progressive disclosure)
    skill_md = skill_dir / 'SKILL.md'
    if skill_md.exists():
        line_count = len(skill_md.read_text().splitlines())
        if line_count > 200:
            errors.append(f"Warning: SKILL.md has {line_count} lines (target ≤200 for progressive disclosure)")

    # Check for references/ if SKILL.md is complex
    if skill_md.exists() and line_count > 150 and not (skill_dir / 'references').exists():
        errors.append("Warning: SKILL.md >150 lines but no references/ directory (consider progressive disclosure)")

    return errors


def validate_agent_structure(agent_file: Path) -> List[str]:
    """Validate agent file structure.

    Expected:
    - Single .md file with YAML frontmatter
    - Agent description and usage examples

    Args:
        agent_file: Path to agent .md file

    Returns:
        List of validation errors
    """
    errors = []

    if not agent_file.exists():
        errors.append(f"Agent file not found: {agent_file}")
        return errors

    # Check file size (agents should be concise)
    line_count = len(agent_file.read_text().splitlines())
    if line_count > 300:
        errors.append(f"Warning: Agent file has {line_count} lines (consider making more concise)")

    return errors


def validate_command_structure(command_file: Path) -> List[str]:
    """Validate command file structure.

    Expected:
    - Single .md file with YAML frontmatter
    - Command description, workflow, and usage examples

    Args:
        command_file: Path to command .md file

    Returns:
        List of validation errors
    """
    errors = []

    if not command_file.exists():
        errors.append(f"Command file not found: {command_file}")
        return errors

    # Check file size (commands should be concise)
    line_count = len(command_file.read_text().splitlines())
    if line_count > 250:
        errors.append(f"Warning: Command file has {line_count} lines (consider making more concise)")

    return errors


def validate_component_structure(component_path: Path) -> Dict[str, Any]:
    """Validate component structure based on type.

    Args:
        component_path: Path to component

    Returns:
        Validation result dictionary
    """
    result = {
        'path': str(component_path),
        'valid': True,
        'errors': [],
        'warnings': []
    }

    # Determine component type and validate
    if component_path.is_dir() and (component_path / 'SKILL.md').exists():
        messages = validate_skill_structure(component_path)
    elif component_path.is_file() and 'agents' in component_path.parts:
        messages = validate_agent_structure(component_path)
    elif component_path.is_file() and 'commands' in component_path.parts:
        messages = validate_command_structure(component_path)
    else:
        result['errors'] = [f"Unknown component type: {component_path}"]
        result['valid'] = False
        return result

    # Separate errors and warnings
    for msg in messages:
        if msg.startswith('Warning:'):
            result['warnings'].append(msg.replace('Warning: ', ''))
        else:
            result['errors'].append(msg)

    result['valid'] = len(result['errors']) == 0
    return result


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: structure-validator.py <component_path>")
        sys.exit(1)

    component_path = Path(sys.argv[1])
    result = validate_component_structure(component_path)

    print(f"Path: {result['path']}")
    print(f"Valid: {result['valid']}")

    if result['errors']:
        print("\nErrors:")
        for error in result['errors']:
            print(f"  - {error}")

    if result['warnings']:
        print("\nWarnings:")
        for warning in result['warnings']:
            print(f"  - {warning}")

    sys.exit(0 if result['valid'] else 1)
