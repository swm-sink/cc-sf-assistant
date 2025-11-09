#!/usr/bin/env python3
"""
validate_command_structure.py - Validate command structure for 9 template types

Exit codes:
  0 - Validation passed
  1 - Fatal error (wrong section count, missing required sections)
  2 - Warning (recommendations)

Template Types and Section Counts:
  - RPIV: 8 sections
  - Human Approval: 9 sections
  - Reflection: 8 sections
  - Validation: 6 sections (including 10 checks)
  - Batch Processing: 7 sections
  - Routing: 7 sections
  - Data Transformation: 7 sections
  - Orchestration: 8 sections
  - Reporting: 7 sections
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


# Template structure definitions
TEMPLATE_STRUCTURES = {
    'rpiv': {
        'name': 'RPIV (Research-Plan-Implement-Verify)',
        'expected_sections': 8,
        'required_keywords': ['RESEARCH', 'PLAN', 'IMPLEMENT', 'VERIFY', 'CHECKPOINT'],
        'required_patterns': [r'CHECKPOINT \d+:', r'Success Criteria', r'Anti-Patterns']
    },
    'human-approval': {
        'name': 'Human Approval',
        'expected_sections': 9,
        'required_keywords': ['approval', 'risk_level', 'reversible', 'urgency', 'audit'],
        'required_patterns': [r'CHECKPOINT:', r'Approve|Reject', r'audit_context']
    },
    'reflection': {
        'name': 'Reflection',
        'expected_sections': 8,
        'required_keywords': ['DRAFT', 'REFLECT', 'IDENTIFY', 'REFINE', 'QUALITY GATE'],
        'required_patterns': [r'quality.*threshold', r'max.*iterations', r'\d+/10']
    },
    'validation': {
        'name': 'Validation',
        'expected_sections': 6,
        'required_keywords': ['Check', 'PASS', 'WARNING', 'ERROR'],
        'required_patterns': [r'Check \d+:', r'✅|⚠️|❌']
    },
    'batch-processing': {
        'name': 'Batch Processing',
        'expected_sections': 7,
        'required_keywords': ['Discovery', 'Processing Loop', 'Summary', 'Error Handling'],
        'required_patterns': [r'CHECKPOINT \d+:', r'per-file error', r'progress.*track']
    },
    'routing': {
        'name': 'Routing',
        'expected_sections': 7,
        'required_keywords': ['Classify', 'Route', 'Delegate', 'Decision Table'],
        'required_patterns': [r'domain.*complexity', r'Handler', r'IF.*THEN']
    },
    'data-transformation': {
        'name': 'Data Transformation',
        'expected_sections': 7,
        'required_keywords': ['Load', 'Transform', 'Validate', 'Output', 'Quality Gate'],
        'required_patterns': [r'quality.*check', r'audit.*trail', r'schema']
    },
    'orchestration': {
        'name': 'Orchestration',
        'expected_sections': 8,
        'required_keywords': ['Dependency Graph', 'State', 'Coordinate', 'Aggregate'],
        'required_patterns': [r'depends on', r'state.*management', r'@\w+']
    },
    'reporting': {
        'name': 'Reporting',
        'expected_sections': 7,
        'required_keywords': ['Data Sources', 'Aggregate', 'Analyze', 'Format', 'Distribute'],
        'required_patterns': [r'metric', r'trend', r'Excel|PDF|HTML']
    }
}


def count_sections(content: str) -> int:
    """Count major sections (## headers)."""
    sections = re.findall(r'^## ', content, re.MULTILINE)
    return len(sections)


def detect_template_type(content: str) -> Optional[str]:
    """Auto-detect template type based on content."""
    content_lower = content.lower()

    # Score each template type
    scores = {}
    for template_type, structure in TEMPLATE_STRUCTURES.items():
        score = 0
        # Check required keywords
        for keyword in structure['required_keywords']:
            if keyword.lower() in content_lower:
                score += 2
        # Check required patterns
        for pattern in structure['required_patterns']:
            if re.search(pattern, content, re.IGNORECASE):
                score += 3
        scores[template_type] = score

    # Return template with highest score (if above threshold)
    if scores:
        best_template = max(scores, key=scores.get)
        if scores[best_template] >= 5:  # Minimum confidence threshold
            return best_template

    return None


def validate_command_structure(content: str, template_type: Optional[str] = None) -> Dict[str, Any]:
    """Validate command structure against template requirements."""
    result = {
        'validator': 'validate_command_structure',
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }

    # Auto-detect template type if not specified
    if not template_type:
        template_type = detect_template_type(content)
        if not template_type:
            result['warnings'].append('Could not auto-detect template type. Skipping structure validation.')
            result['info']['detected_type'] = 'unknown'
            return result

    result['info']['template_type'] = template_type

    if template_type not in TEMPLATE_STRUCTURES:
        result['warnings'].append(f'Unknown template type: {template_type}')
        result['info']['valid_types'] = list(TEMPLATE_STRUCTURES.keys())
        return result

    structure = TEMPLATE_STRUCTURES[template_type]
    result['info']['template_name'] = structure['name']

    # Count sections
    section_count = count_sections(content)
    result['info']['section_count'] = section_count
    result['info']['expected_sections'] = structure['expected_sections']

    if section_count != structure['expected_sections']:
        result['passed'] = False
        result['errors'].append(
            f"Section count mismatch: expected {structure['expected_sections']}, got {section_count}"
        )

    # Check required keywords
    missing_keywords = []
    for keyword in structure['required_keywords']:
        if keyword.lower() not in content.lower():
            missing_keywords.append(keyword)

    if missing_keywords:
        result['warnings'].append(f"Missing recommended keywords: {', '.join(missing_keywords)}")

    # Check required patterns
    missing_patterns = []
    for pattern in structure['required_patterns']:
        if not re.search(pattern, content, re.IGNORECASE):
            missing_patterns.append(pattern)

    if missing_patterns:
        result['warnings'].append(f"Missing recommended patterns: {len(missing_patterns)}")
        result['info']['missing_patterns'] = missing_patterns

    # Template-specific validation
    if template_type == 'rpiv':
        # Check for 4 checkpoints
        checkpoints = re.findall(r'CHECKPOINT \d+:', content)
        if len(checkpoints) != 4:
            result['passed'] = False
            result['errors'].append(f"RPIV requires 4 checkpoints, found {len(checkpoints)}")

    elif template_type == 'human-approval':
        # Check for risk assessment fields
        if 'risk_level' not in content.lower():
            result['passed'] = False
            result['errors'].append("Human Approval requires risk_level field")
        if 'reversible' not in content.lower():
            result['passed'] = False
            result['errors'].append("Human Approval requires reversible field")

    elif template_type == 'reflection':
        # Check for quality thresholds and iteration limits
        if not re.search(r'quality.*threshold', content, re.IGNORECASE):
            result['passed'] = False
            result['errors'].append("Reflection requires quality threshold definition")
        if not re.search(r'max.*iterations', content, re.IGNORECASE):
            result['passed'] = False
            result['errors'].append("Reflection requires max iterations limit")

    elif template_type == 'routing':
        # Check for decision table
        if 'decision table' not in content.lower() and 'IF' not in content and 'THEN' not in content:
            result['passed'] = False
            result['errors'].append("Routing requires decision table or IF-THEN logic")

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_command_structure.py <command_file.md> [template_type]", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])
    template_type = sys.argv[2] if len(sys.argv) > 2 else None

    if not file_path.exists():
        print(json.dumps({
            'validator': 'validate_command_structure',
            'passed': False,
            'errors': [f'File not found: {file_path}'],
            'warnings': [],
            'info': {}
        }))
        sys.exit(1)

    content = file_path.read_text()
    result = validate_command_structure(content, template_type)

    # Determine exit code
    exit_code = 0
    if not result['passed']:
        exit_code = 1
    elif result['warnings']:
        exit_code = 2

    # Output JSON result
    print(json.dumps(result, indent=2))

    # Human-readable summary
    print("\n--- Structure Validation Summary ---", file=sys.stderr)
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
