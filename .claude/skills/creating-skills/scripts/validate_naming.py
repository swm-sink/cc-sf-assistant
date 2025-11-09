#!/usr/bin/env python3
"""
validate_naming.py - Validate active-voice naming conventions

Checks for:
- Gerund form (creating-skills not skill-creator)
- Present participle (-ing verbs)
- Action-oriented naming

Exit codes:
  0 - Validation passed
  1 - Fatal error (cannot extract name)
  2 - Warning (naming suggestion, non-standard pattern)

Output: JSON with validation results + human-readable summary
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


# Common gerunds/present participles for active-voice naming
ACTIVE_VOICE_PATTERNS = [
    'creating', 'building', 'implementing', 'enforcing', 'analyzing',
    'validating', 'testing', 'reviewing', 'managing', 'handling',
    'processing', 'generating', 'transforming', 'calculating', 'comparing',
    'importing', 'exporting', 'syncing', 'integrating', 'orchestrating',
    'monitoring', 'tracking', 'logging', 'debugging', 'optimizing'
]

# Passive-voice patterns to avoid
PASSIVE_VOICE_PATTERNS = [
    'creator', 'builder', 'analyzer', 'validator', 'tester',
    'reviewer', 'manager', 'handler', 'processor', 'generator',
    'transformer', 'calculator', 'comparator', 'importer', 'exporter'
]


def extract_skill_name(content: str) -> Optional[str]:
    """Extract skill name from YAML frontmatter."""
    pattern = r'^---\s*\nname:\s*(.+?)\s*\n'
    match = re.search(pattern, content, re.MULTILINE)
    return match.group(1).strip() if match else None


def suggest_active_voice(name: str) -> Optional[str]:
    """Suggest active-voice alternative for a passive-voice name."""
    # Convert skill-creator → creating-skills
    # Convert variance-analyzer → analyzing-variance
    # Convert code-reviewer → reviewing-code

    parts = name.split('-')

    # Check if last part is passive voice
    if not parts:
        return None

    last_part = parts[-1]

    # Map passive to active
    passive_to_active = {
        'creator': 'creating',
        'builder': 'building',
        'analyzer': 'analyzing',
        'validator': 'validating',
        'tester': 'testing',
        'reviewer': 'reviewing',
        'manager': 'managing',
        'handler': 'handling',
        'processor': 'processing',
        'generator': 'generating',
        'transformer': 'transforming',
        'calculator': 'calculating',
        'comparator': 'comparing',
        'importer': 'importing',
        'exporter': 'exporting'
    }

    if last_part in passive_to_active:
        # Rebuild name with active voice first
        active_verb = passive_to_active[last_part]
        noun_parts = parts[:-1]

        if not noun_parts:
            return active_verb

        # Handle plural nouns (skills, commands, etc.)
        noun = '-'.join(noun_parts)

        return f"{active_verb}-{noun}"

    return None


def validate_naming(content: str) -> Dict[str, Any]:
    """Validate naming conventions for skills."""
    result = {
        'validator': 'validate_naming',
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }

    # Extract skill name
    name = extract_skill_name(content)

    if name is None:
        result['passed'] = False
        result['errors'].append('Cannot extract skill name from YAML frontmatter')
        return result

    result['info']['skill_name'] = name

    # Check for active voice patterns
    has_active_voice = any(pattern in name for pattern in ACTIVE_VOICE_PATTERNS)
    has_passive_voice = any(pattern in name for pattern in PASSIVE_VOICE_PATTERNS)

    result['info']['has_active_voice'] = has_active_voice
    result['info']['has_passive_voice'] = has_passive_voice

    if has_passive_voice:
        suggestion = suggest_active_voice(name)
        if suggestion:
            result['warnings'].append(f'Passive-voice naming detected: "{name}"')
            result['warnings'].append(f'Suggestion: Use active voice → "{suggestion}"')
            result['info']['suggested_name'] = suggestion
        else:
            result['warnings'].append(f'Passive-voice pattern detected in: "{name}"')
            result['warnings'].append('Consider using active voice (gerund form, e.g., creating-X, analyzing-Y)')

    if not has_active_voice and not has_passive_voice:
        # Neither active nor passive - might be reference skill or pattern skill
        # Don't fail, but provide info
        result['info']['naming_style'] = 'neutral (neither active nor passive)'
        result['info']['note'] = 'Neutral naming is acceptable for reference/pattern skills'

    # Check kebab-case format
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        result['passed'] = False
        result['errors'].append(f'Invalid name format: "{name}" (must be kebab-case)')

    # Length check (reasonable bounds)
    if len(name) < 3:
        result['warnings'].append(f'Name very short: "{name}" (recommend ≥10 chars for clarity)')

    if len(name) > 60:
        result['warnings'].append(f'Name very long: "{name}" (recommend ≤40 chars for readability)')

    return result


def format_human_readable(result: Dict[str, Any]) -> str:
    """Format validation result as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"Active-Voice Naming Validation")
    lines.append(f"{'='*60}")

    if result['passed']:
        lines.append("\n✅ PASSED")
    else:
        lines.append("\n❌ FAILED")

    if result['errors']:
        lines.append(f"\n🚨 Errors ({len(result['errors'])}):")
        for error in result['errors']:
            lines.append(f"  - {error}")

    if result['warnings']:
        lines.append(f"\n⚠️  Warnings ({len(result['warnings'])}):")
        for warning in result['warnings']:
            lines.append(f"  - {warning}")

    if result['info']:
        lines.append(f"\nℹ️  Info:")
        for key, value in result['info'].items():
            lines.append(f"  - {key}: {value}")

    lines.append(f"\n{'='*60}\n")
    return '\n'.join(lines)


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: validate_naming.py <path/to/SKILL.md>", file=sys.stderr)
        return 1

    skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print(f"Error: File not found: {skill_path}", file=sys.stderr)
        return 1

    # Read file content
    content = skill_path.read_text(encoding='utf-8')

    # Validate naming
    result = validate_naming(content)

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
