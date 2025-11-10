#!/usr/bin/env python3
"""Cross-reference validator for links between components."""

from pathlib import Path
from typing import List, Dict, Any
import re


def extract_markdown_links(content: str) -> List[tuple]:
    """Extract markdown links from content.

    Args:
        content: Markdown content

    Returns:
        List of (link_text, link_url) tuples
    """
    # Match [text](url) format
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    return re.findall(pattern, content)


def validate_internal_links(file_path: Path) -> List[str]:
    """Validate internal links in markdown file.

    Args:
        file_path: Path to markdown file

    Returns:
        List of broken links
    """
    errors = []

    with open(file_path, 'r') as f:
        content = f.read()

    links = extract_markdown_links(content)

    for link_text, link_url in links:
        # Skip external links (http://, https://)
        if link_url.startswith('http://') or link_url.startswith('https://'):
            continue

        # Skip anchor links
        if link_url.startswith('#'):
            continue

        # Resolve relative path
        if link_url.startswith('/'):
            # Absolute path from project root
            target_path = Path(link_url.lstrip('/'))
        else:
            # Relative path from current file
            target_path = file_path.parent / link_url

        # Check if target exists
        if not target_path.exists():
            errors.append(f"Broken link: [{link_text}]({link_url}) -> {target_path} not found")

    return errors


def validate_skill_references(skill_dir: Path) -> List[str]:
    """Validate that SKILL.md references point to existing files.

    Args:
        skill_dir: Path to skill directory

    Returns:
        List of broken references
    """
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        return []

    return validate_internal_links(skill_md)


def validate_component_cross_references(component_path: Path) -> Dict[str, Any]:
    """Validate cross-references in component.

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

    if component_path.is_dir():
        # Validate skill references
        result['errors'] = validate_skill_references(component_path)
    elif component_path.is_file() and component_path.suffix == '.md':
        # Validate markdown file links
        result['errors'] = validate_internal_links(component_path)

    result['valid'] = len(result['errors']) == 0
    return result


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: cross-reference-validator.py <component_path>")
        sys.exit(1)

    component_path = Path(sys.argv[1])
    result = validate_component_cross_references(component_path)

    print(f"Path: {result['path']}")
    print(f"Valid: {result['valid']}")

    if result['errors']:
        print("\nBroken Links:")
        for error in result['errors']:
            print(f"  - {error}")

    sys.exit(0 if result['valid'] else 1)
