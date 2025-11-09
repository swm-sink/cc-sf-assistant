#!/usr/bin/env python3
"""
validate_cso.py - Validate CSO (Claude Search Optimization) score

Checks for:
- Trigger phrases (when, before, after, use when, need to)
- Symptom keywords (thinking, feeling, noticing, experiencing)
- Technology-agnostic keywords (generic actions, domain concepts)
- Specific examples (concrete use cases)

CSO Score = (trigger_count + symptom_count + agnostic_count + example_count) / 4
Target: ≥0.7

Exit codes:
  0 - Validation passed (CSO ≥0.7)
  1 - Fatal error (cannot extract description)
  2 - Warning (CSO <0.7)

Output: JSON with validation results + human-readable summary
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


# CSO Keyword Categories (4 pillars)
TRIGGER_PHRASES = [
    'when', 'before', 'after', 'use when', 'need to', 'want to',
    'about to', 'during', 'while', 'if you', 'whenever'
]

SYMPTOM_KEYWORDS = [
    'thinking', 'feeling', 'noticing', 'experiencing', 'under pressure',
    'struggling', 'finding', 'having trouble', 'can\'t', 'unable to'
]

AGNOSTIC_KEYWORDS = [
    'creating', 'building', 'implementing', 'enforcing', 'analyzing',
    'validating', 'testing', 'reviewing', 'managing', 'handling',
    'workflow', 'process', 'methodology', 'approach', 'pattern',
    'calculating', 'transforming', 'integrating', 'orchestrating'
]

EXAMPLE_INDICATORS = [
    'google', 'sheets', 'excel', 'databricks', 'adaptive', 'api',
    'variance', 'budget', 'forecast', 'revenue', 'expense',
    'integration', 'report', 'calculation', 'import', 'export'
]


def extract_description(content: str) -> Optional[str]:
    """Extract description from YAML frontmatter."""
    pattern = r'^---\s*\n.*?description:\s*(.+?)\s*\n'
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else None


def calculate_cso_score(description: str) -> Dict[str, Any]:
    """Calculate CSO score for description."""
    desc_lower = description.lower()

    # Count trigger phrases
    trigger_count = sum(1 for phrase in TRIGGER_PHRASES if phrase in desc_lower)

    # Count symptom keywords
    symptom_count = sum(1 for keyword in SYMPTOM_KEYWORDS if keyword in desc_lower)

    # Count agnostic keywords
    agnostic_count = sum(1 for keyword in AGNOSTIC_KEYWORDS if keyword in desc_lower)

    # Count example indicators
    example_count = sum(1 for indicator in EXAMPLE_INDICATORS if indicator in desc_lower)

    # Normalize to 0-1 scale (assuming 3+ of each is excellent)
    trigger_score = min(trigger_count / 3, 1.0)
    symptom_score = min(symptom_count / 2, 1.0)
    agnostic_score = min(agnostic_count / 3, 1.0)
    example_score = min(example_count / 2, 1.0)

    # CSO score is average of 4 pillars
    cso_score = (trigger_score + symptom_score + agnostic_score + example_score) / 4

    return {
        'trigger_count': trigger_count,
        'trigger_score': round(trigger_score, 2),
        'symptom_count': symptom_count,
        'symptom_score': round(symptom_score, 2),
        'agnostic_count': agnostic_count,
        'agnostic_score': round(agnostic_score, 2),
        'example_count': example_count,
        'example_score': round(example_score, 2),
        'cso_score': round(cso_score, 2)
    }


def validate_cso(content: str) -> Dict[str, Any]:
    """Validate CSO score."""
    result = {
        'validator': 'validate_cso',
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }

    # Extract description
    description = extract_description(content)

    if description is None:
        result['passed'] = False
        result['errors'].append('Cannot extract description from YAML frontmatter')
        return result

    result['info']['description'] = description
    result['info']['description_length'] = len(description)

    # Calculate CSO score
    cso_data = calculate_cso_score(description)
    result['info'].update(cso_data)

    cso_score = cso_data['cso_score']
    result['info']['target_score'] = 0.7

    if cso_score < 0.7:
        result['warnings'].append(f'CSO score below target: {cso_score} (target ≥0.7)')
        result['warnings'].append('Recommendations:')

        if cso_data['trigger_score'] < 0.7:
            result['warnings'].append('  • Add more trigger phrases (when, before, after, use when, need to)')

        if cso_data['symptom_score'] < 0.7:
            result['warnings'].append('  • Add symptom keywords (thinking, feeling, noticing, under pressure)')

        if cso_data['agnostic_score'] < 0.7:
            result['warnings'].append('  • Add technology-agnostic keywords (creating, implementing, workflow, process)')

        if cso_data['example_score'] < 0.7:
            result['warnings'].append('  • Add specific examples (Google Sheets, variance, budget, integration)')

    # Check description length
    if len(description) < 50:
        result['warnings'].append(f'Description short: {len(description)} chars (recommend ≥50 for keyword richness)')

    return result


def format_human_readable(result: Dict[str, Any]) -> str:
    """Format validation result as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"CSO (Claude Search Optimization) Validation")
    lines.append(f"{'='*60}")

    if result['passed']:
        lines.append("\n✅ PASSED")
    else:
        lines.append("\n❌ FAILED")

    if 'cso_score' in result['info']:
        cso_score = result['info']['cso_score']
        target = result['info'].get('target_score', 0.7)

        lines.append(f"\n📊 CSO Score: {cso_score} / 1.0 (target ≥{target})")

        if cso_score >= target:
            lines.append(f"   ✅ Score meets target")
        else:
            lines.append(f"   ⚠️  Score below target")

        # Show pillar breakdown
        lines.append(f"\n🔍 Pillar Breakdown:")
        lines.append(f"   • Trigger Phrases: {result['info']['trigger_count']} → {result['info']['trigger_score']}")
        lines.append(f"   • Symptom Keywords: {result['info']['symptom_count']} → {result['info']['symptom_score']}")
        lines.append(f"   • Agnostic Keywords: {result['info']['agnostic_count']} → {result['info']['agnostic_score']}")
        lines.append(f"   • Example Indicators: {result['info']['example_count']} → {result['info']['example_score']}")

    if result['errors']:
        lines.append(f"\n🚨 Errors ({len(result['errors'])}):")
        for error in result['errors']:
            lines.append(f"  - {error}")

    if result['warnings']:
        lines.append(f"\n⚠️  Warnings ({len(result['warnings'])}):")
        for warning in result['warnings']:
            lines.append(f"  {warning}")

    lines.append(f"\n{'='*60}\n")
    return '\n'.join(lines)


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: validate_cso.py <path/to/SKILL.md>", file=sys.stderr)
        return 1

    skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print(f"Error: File not found: {skill_path}", file=sys.stderr)
        return 1

    # Read file content
    content = skill_path.read_text(encoding='utf-8')

    # Validate CSO
    result = validate_cso(content)

    # Output JSON to stdout
    print(json.dumps(result, indent=2))

    # Output human-readable to stderr
    print(format_human_readable(result), file=sys.stderr)

    # Return exit code
    if not result['passed']:
        return 1
    elif result['warnings']:
        return 2
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())