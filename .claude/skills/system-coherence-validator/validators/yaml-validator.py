#!/usr/bin/env python3
"""YAML frontmatter validation for skills, agents, commands."""

from pathlib import Path
from typing import Dict, List, Any, Literal
import yaml
import re


def extract_frontmatter(file_path: Path) -> Dict[str, Any]:
    """Extract YAML frontmatter from markdown file.

    Args:
        file_path: Path to markdown file

    Returns:
        Dictionary of frontmatter fields

    Raises:
        ValueError: If frontmatter not found or invalid YAML
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # Match YAML frontmatter between --- delimiters
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        raise ValueError(f"No YAML frontmatter found in {file_path}")

    try:
        frontmatter = yaml.safe_load(match.group(1))
        return frontmatter or {}
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {file_path}: {e}")


def validate_skill_frontmatter(file_path: Path) -> List[str]:
    """Validate SKILL.md YAML frontmatter.

    Required fields:
    - name: str
    - type: Literal['Discipline', 'Technique', 'Pattern', 'Reference']
    - auto_invoke: bool
    - cso_score: float (≥0.6, ≥0.7, or ≥0.8 depending on tier)

    Args:
        file_path: Path to SKILL.md

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    try:
        fm = extract_frontmatter(file_path)
    except ValueError as e:
        return [str(e)]

    # Check required fields
    required_fields = ['name', 'type', 'auto_invoke', 'cso_score']
    for field in required_fields:
        if field not in fm:
            errors.append(f"Missing required field: {field}")

    # Validate type
    if 'type' in fm:
        valid_types = ['Discipline', 'Technique', 'Pattern', 'Reference']
        if fm['type'] not in valid_types:
            errors.append(f"Invalid type '{fm['type']}'. Expected: {', '.join(valid_types)}")

    # Validate auto_invoke
    if 'auto_invoke' in fm and not isinstance(fm['auto_invoke'], bool):
        errors.append(f"auto_invoke must be boolean, got {type(fm['auto_invoke']).__name__}")

    # Validate cso_score
    if 'cso_score' in fm:
        try:
            score = float(fm['cso_score'])
            if score < 0 or score > 1:
                errors.append(f"cso_score must be between 0 and 1, got {score}")
        except (TypeError, ValueError):
            errors.append(f"cso_score must be numeric, got {fm['cso_score']}")

    return errors


def validate_agent_frontmatter(file_path: Path) -> List[str]:
    """Validate agent .md YAML frontmatter.

    Required fields:
    - name: str
    - tool_tier: Literal['read_only', 'read_web', 'full_access']
    - description: str

    Args:
        file_path: Path to agent .md file

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    try:
        fm = extract_frontmatter(file_path)
    except ValueError as e:
        return [str(e)]

    # Check required fields
    required_fields = ['name', 'tool_tier', 'description']
    for field in required_fields:
        if field not in fm:
            errors.append(f"Missing required field: {field}")

    # Validate tool_tier
    if 'tool_tier' in fm:
        valid_tiers = ['read_only', 'read_web', 'full_access']
        if fm['tool_tier'] not in valid_tiers:
            errors.append(f"Invalid tool_tier '{fm['tool_tier']}'. Expected: {', '.join(valid_tiers)}")

    # Validate description
    if 'description' in fm and not isinstance(fm['description'], str):
        errors.append(f"description must be string, got {type(fm['description']).__name__}")

    return errors


def validate_command_frontmatter(file_path: Path) -> List[str]:
    """Validate command .md YAML frontmatter.

    Required fields:
    - name: str
    - workflow_type: str (RPIV, Human Approval, Validation, etc.)
    - description: str

    Args:
        file_path: Path to command .md file

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    try:
        fm = extract_frontmatter(file_path)
    except ValueError as e:
        return [str(e)]

    # Check required fields
    required_fields = ['name', 'workflow_type', 'description']
    for field in required_fields:
        if field not in fm:
            errors.append(f"Missing required field: {field}")

    # Validate workflow_type
    valid_workflows = [
        'RPIV', 'Human Approval', 'Reflection', 'Validation',
        'Batch', 'Routing', 'ETL', 'Orchestration', 'Reporting'
    ]
    if 'workflow_type' in fm and fm['workflow_type'] not in valid_workflows:
        errors.append(f"Warning: workflow_type '{fm['workflow_type']}' not in common types: {', '.join(valid_workflows)}")

    # Validate description
    if 'description' in fm and not isinstance(fm['description'], str):
        errors.append(f"description must be string, got {type(fm['description']).__name__}")

    return errors


def validate_component(file_path: Path) -> Dict[str, Any]:
    """Validate component based on file type.

    Args:
        file_path: Path to component file

    Returns:
        Validation result with errors and warnings
    """
    result = {
        'file': str(file_path),
        'valid': True,
        'errors': [],
        'warnings': []
    }

    # Determine component type
    if file_path.name == 'SKILL.md':
        result['errors'] = validate_skill_frontmatter(file_path)
    elif file_path.parent.name in ['agents', 'validators', 'generators']:
        result['errors'] = validate_agent_frontmatter(file_path)
    elif file_path.parent.parent.name == 'commands':
        result['errors'] = validate_command_frontmatter(file_path)
    else:
        result['errors'] = [f"Unknown component type: {file_path}"]

    result['valid'] = len(result['errors']) == 0
    return result


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: yaml-validator.py <file_path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    result = validate_component(file_path)

    print(f"File: {result['file']}")
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
