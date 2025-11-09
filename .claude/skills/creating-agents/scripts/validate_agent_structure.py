#!/usr/bin/env python3
"""
validate_agent_structure.py - Validate structural requirements for agent .md files

Exit codes:
  0 - Validation passed
  1 - Fatal error (wrong section count, missing required sections)
  2 - Warning (recommendations)

Output: JSON with validation results + human-readable summary

All agent templates use 6 major sections:
1. Role Statement (1-2 paragraphs)
2. Communication Protocol (JSON query format)
3. Domain/Research/Review Expertise Areas (8-15 areas with bullets)
4. Quality/Research/Verification Checklist (8 items)
5. Development/Investigation/Review Workflow (3 phases)
6. Integration Notes + Anti-Patterns
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def extract_sections(content: str) -> List[str]:
    """Extract all ## section headers from content."""
    # Remove YAML frontmatter
    if content.startswith('---'):
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # Find all ## headers (but not ### or #)
    sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
    return sections


def detect_agent_type(content: str) -> Optional[str]:
    """Detect agent type from content patterns."""
    # Check for domain specialist patterns
    if 'Domain Specialist' in content or 'domain specialist' in content or 'Domain Expertise Areas' in content:
        return 'domain-specialist'

    # Check for researcher patterns
    if 'research analyst' in content.lower() or 'Research Expertise Areas' in content or 'Investigation Workflow' in content:
        return 'researcher'

    # Check for reviewer patterns
    if 'reviewer' in content.lower() or 'Review Expertise Areas' in content or 'Review Workflow' in content or 'Verification Checklist' in content:
        return 'reviewer'

    return None


def count_domain_areas(content: str) -> int:
    """Count number of domain/research/review areas (### subsections under expertise section)."""
    # Find the expertise section
    expertise_pattern = r'## (?:Domain|Research|Review) Expertise Areas(.*?)(?=## |$)'
    match = re.search(expertise_pattern, content, re.DOTALL)

    if not match:
        return 0

    expertise_content = match.group(1)

    # Count ### subsections (domain areas)
    areas = re.findall(r'^### ', expertise_content, re.MULTILINE)
    return len(areas)


def count_checklist_items(content: str) -> int:
    """Count number of checklist items."""
    # Find checklist section
    checklist_pattern = r'## (?:Quality|Research Quality|Verification) Checklist(.*?)(?=## |$)'
    match = re.search(checklist_pattern, content, re.DOTALL)

    if not match:
        return 0

    checklist_content = match.group(1)

    # Count checklist items (- [ ])
    items = re.findall(r'- \[ \]', checklist_content)
    return len(items)


def count_workflow_phases(content: str) -> int:
    """Count number of workflow phases (### subsections under workflow section)."""
    # Find workflow section
    workflow_pattern = r'## (?:Development|Investigation|Review) Workflow(.*?)(?=## |$)'
    match = re.search(workflow_pattern, content, re.DOTALL)

    if not match:
        return 0

    workflow_content = match.group(1)

    # Count ### subsections (phases)
    phases = re.findall(r'^### Phase \d+', workflow_content, re.MULTILINE)
    return len(phases)


def validate_agent_structure(content: str) -> Dict[str, Any]:
    """Validate agent structure."""
    result = {
        'validator': 'validate_agent_structure',
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }

    # Detect agent type
    agent_type = detect_agent_type(content)
    result['info']['detected_type'] = agent_type or 'unknown'

    # Extract sections
    sections = extract_sections(content)
    result['info']['section_count'] = len(sections)
    result['info']['sections'] = sections

    # All agent types should have 6 major sections
    expected_section_count = 6

    if len(sections) < expected_section_count:
        result['passed'] = False
        result['errors'].append(f'Too few sections: {len(sections)} (expected {expected_section_count})')
    elif len(sections) > expected_section_count:
        result['warnings'].append(f'More sections than expected: {len(sections)} (expected {expected_section_count})')

    # Check for required sections
    required_sections = [
        ('Communication Protocol', r'Communication Protocol'),
        ('Expertise Areas', r'(?:Domain|Research|Review) Expertise Areas'),
        ('Checklist', r'(?:Quality|Research Quality|Verification) Checklist'),
        ('Workflow', r'(?:Development|Investigation|Review) Workflow'),
        ('Integration Notes', r'Integration Notes'),
        ('Anti-Patterns', r'Anti-Patterns')
    ]

    for section_name, section_pattern in required_sections:
        if not any(re.search(section_pattern, section) for section in sections):
            result['passed'] = False
            result['errors'].append(f'Missing required section: {section_name}')

    # Count domain/research/review areas
    area_count = count_domain_areas(content)
    result['info']['expertise_area_count'] = area_count

    if agent_type in ['domain-specialist', 'researcher', 'reviewer']:
        if area_count < 8:
            result['warnings'].append(f'Few expertise areas: {area_count} (recommended 8-15)')
        elif area_count > 15:
            result['warnings'].append(f'Many expertise areas: {area_count} (recommended 8-15)')

    # Count checklist items
    checklist_count = count_checklist_items(content)
    result['info']['checklist_item_count'] = checklist_count

    if checklist_count != 8:
        result['warnings'].append(f'Checklist items: {checklist_count} (expected 8)')

    # Count workflow phases
    workflow_phases = count_workflow_phases(content)
    result['info']['workflow_phase_count'] = workflow_phases

    if workflow_phases != 3:
        result['warnings'].append(f'Workflow phases: {workflow_phases} (expected 3)')

    # Template-specific checks
    if agent_type == 'domain-specialist':
        if 'Full access' not in content and 'full access' not in content:
            result['warnings'].append('Domain Specialist should mention "full access" tools')

    elif agent_type == 'researcher':
        if 'Read-only' not in content and 'read-only' not in content:
            result['warnings'].append('Researcher should mention "read-only" tool restrictions')
        if 'WebFetch' not in content or 'WebSearch' not in content:
            result['warnings'].append('Researcher should have WebFetch and WebSearch tools')

    elif agent_type == 'reviewer':
        if 'Read-only' not in content and 'read-only' not in content:
            result['warnings'].append('Reviewer should mention "read-only" tool restrictions')
        if 'APPROVE' not in content or 'REJECT' not in content:
            result['warnings'].append('Reviewer should have APPROVE/REJECT decision format')

    # Check for coordination anti-pattern
    if 'coordinate other agents' in content.lower() or 'coordinates other agents' in content.lower():
        if 'does NOT coordinate other agents' not in content and 'NEVER coordinate other agents' not in content:
            result['errors'].append('Agent appears to coordinate other agents (anti-pattern). Commands coordinate agents, not agents.')

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_agent_structure.py <agent_file.md>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(json.dumps({
            'validator': 'validate_agent_structure',
            'passed': False,
            'errors': [f'File not found: {file_path}'],
            'warnings': [],
            'info': {}
        }))
        sys.exit(1)

    content = file_path.read_text()
    result = validate_agent_structure(content)

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
