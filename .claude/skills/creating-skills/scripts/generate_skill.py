#!/usr/bin/env python3
"""
generate_skill.py - Orchestrator for end-to-end skill generation

Workflow:
1. Interactive prompts for skill details
2. Select template based on skill type
3. Generate skill in temp directory
4. Run all 5 validators
5. If all pass, move to .claude/skills/{skill-name}/SKILL.md
6. If any fail, show errors and rollback

Atomic operations: temp dir → validate → commit or rollback

Usage:
  python generate_skill.py
  python generate_skill.py --skill-name creating-commands --skill-type technique
"""

import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


# Template paths relative to this script
SCRIPT_DIR = Path(__file__).parent
TEMPLATE_DIR = SCRIPT_DIR.parent / 'assets' / 'templates'

SKILL_TYPES = ['technique', 'pattern', 'discipline', 'reference']

VALIDATORS = [
    'validate_yaml.py',
    'validate_naming.py',
    'validate_structure.py',
    'validate_cso.py',
    'validate_rationalization.py'
]


def prompt_user(prompt: str, default: Optional[str] = None) -> str:
    """Prompt user for input with optional default."""
    if default:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "

    user_input = input(prompt_text).strip()

    if not user_input and default:
        return default

    return user_input


def prompt_choice(prompt: str, choices: List[str], default: Optional[str] = None) -> str:
    """Prompt user to choose from list."""
    print(f"\n{prompt}")
    for i, choice in enumerate(choices, 1):
        marker = " (default)" if choice == default else ""
        print(f"  {i}. {choice}{marker}")

    while True:
        choice_input = input(f"\nSelect (1-{len(choices)}): ").strip()

        if not choice_input and default:
            return default

        try:
            choice_idx = int(choice_input) - 1
            if 0 <= choice_idx < len(choices):
                return choices[choice_idx]
            else:
                print(f"Invalid choice. Please select 1-{len(choices)}.")
        except ValueError:
            print(f"Invalid input. Please enter a number 1-{len(choices)}.")


def select_template(skill_type: str) -> Path:
    """Select template based on skill type."""
    template_map = {
        'technique': TEMPLATE_DIR / 'technique-template.md',
        'pattern': TEMPLATE_DIR / 'pattern-template.md',
        'discipline': TEMPLATE_DIR / 'discipline-template.md',
        'reference': TEMPLATE_DIR / 'reference-template.md'
    }

    template_path = template_map.get(skill_type)

    if not template_path or not template_path.exists():
        raise FileNotFoundError(f"Template not found for {skill_type}: {template_path}")

    return template_path


def read_template(template_path: Path) -> str:
    """Read template file content."""
    return template_path.read_text(encoding='utf-8')


def fill_placeholders(template_content: str, placeholders: Dict[str, str]) -> str:
    """Replace {{PLACEHOLDERS}} with actual values."""
    content = template_content

    for key, value in placeholders.items():
        placeholder = f"{{{{{key}}}}}"
        content = content.replace(placeholder, value)

    return content


def generate_skill_content(skill_type: str, skill_details: Dict[str, str]) -> str:
    """Generate skill content from template."""
    template_path = select_template(skill_type)
    template_content = read_template(template_path)

    # Extract just the template structure (between ```markdown and ```)
    import re
    pattern = r'```markdown\s*\n(.*?)\n```'
    match = re.search(pattern, template_content, re.DOTALL)

    if not match:
        raise ValueError(f"Cannot find template structure in {template_path}")

    template_structure = match.group(1)

    # Fill placeholders
    filled_content = fill_placeholders(template_structure, skill_details)

    return filled_content


def run_validator(validator_script: str, skill_path: Path) -> Tuple[int, Dict[str, Any]]:
    """Run a single validator and return exit code + results."""
    validator_path = SCRIPT_DIR / validator_script

    if not validator_path.exists():
        raise FileNotFoundError(f"Validator not found: {validator_path}")

    # Run validator
    result = subprocess.run(
        [sys.executable, str(validator_path), str(skill_path)],
        capture_output=True,
        text=True
    )

    # Parse JSON output from stdout
    try:
        validation_result = json.loads(result.stdout)
    except json.JSONDecodeError:
        validation_result = {
            'validator': validator_script,
            'passed': False,
            'errors': [f'Failed to parse validator output: {result.stdout}'],
            'warnings': [],
            'info': {}
        }

    return result.returncode, validation_result


def validate_skill(skill_path: Path) -> Tuple[bool, List[Dict[str, Any]]]:
    """Run all validators on generated skill."""
    all_results = []
    all_passed = True

    print("\n" + "="*60)
    print("Running Validators")
    print("="*60)

    for validator in VALIDATORS:
        print(f"\nRunning {validator}...")
        exit_code, result = run_validator(validator, skill_path)

        all_results.append(result)

        if exit_code == 0:
            print(f"  ✅ PASSED")
        elif exit_code == 2:
            print(f"  ⚠️  WARNINGS")
            for warning in result.get('warnings', []):
                print(f"     {warning}")
        else:
            print(f"  ❌ FAILED")
            for error in result.get('errors', []):
                print(f"     {error}")
            all_passed = False

    return all_passed, all_results


def create_skill_directory(skill_name: str) -> Path:
    """Create skill directory in .claude/skills/"""
    # Find project root (where .claude/ directory is)
    current = Path.cwd()
    while current != current.parent:
        claude_dir = current / '.claude'
        if claude_dir.exists() and claude_dir.is_dir():
            break
        current = current.parent
    else:
        raise FileNotFoundError("Cannot find .claude/ directory (not in Claude Code project?)")

    skill_dir = claude_dir / 'skills' / skill_name

    if skill_dir.exists():
        raise FileExistsError(f"Skill directory already exists: {skill_dir}")

    skill_dir.mkdir(parents=True, exist_ok=True)

    return skill_dir


def main() -> int:
    """Main entry point."""
    print("="*60)
    print("Skill Generator - Interactive Mode")
    print("="*60)

    # Collect skill details
    skill_name = prompt_user("Skill name (kebab-case)")

    if not skill_name:
        print("Error: Skill name is required", file=sys.stderr)
        return 1

    skill_type = prompt_choice("Select skill type", SKILL_TYPES)

    skill_title = prompt_user("Skill title (human-readable)", default=skill_name.replace('-', ' ').title())

    description = prompt_user("Description (CSO-optimized, ≥50 chars)")

    if not description:
        print("Error: Description is required", file=sys.stderr)
        return 1

    one_sentence_purpose = prompt_user("One-sentence purpose")

    if not one_sentence_purpose:
        print("Error: Purpose is required", file=sys.stderr)
        return 1

    # Build placeholder map
    placeholders = {
        'SKILL_NAME': skill_name,
        'SKILL_TITLE': skill_title,
        'CSO_OPTIMIZED_DESCRIPTION': description,
        'ONE_SENTENCE_PURPOSE': one_sentence_purpose,
    }

    print(f"\n{'='*60}")
    print(f"Generating {skill_type} skill: {skill_name}")
    print(f"{'='*60}")

    try:
        # Generate skill content
        print("\n1. Generating skill content from template...")
        skill_content = generate_skill_content(skill_type, placeholders)
        print(f"   ✅ Generated {len(skill_content)} chars")

        # Create temp directory
        print("\n2. Creating temporary directory...")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_skill_path = Path(temp_dir) / 'SKILL.md'
            temp_skill_path.write_text(skill_content, encoding='utf-8')
            print(f"   ✅ Temp skill: {temp_skill_path}")

            # Validate
            print("\n3. Validating skill...")
            all_passed, validation_results = validate_skill(temp_skill_path)

            if not all_passed:
                print(f"\n{'='*60}")
                print("❌ VALIDATION FAILED")
                print(f"{'='*60}")
                print("\nSkill generation aborted. Fix errors and try again.")
                return 1

            # All validations passed
            print(f"\n{'='*60}")
            print("✅ ALL VALIDATIONS PASSED")
            print(f"{'='*60}")

            # Commit: Move to final location
            print("\n4. Committing skill to .claude/skills/...")
            skill_dir = create_skill_directory(skill_name)
            final_skill_path = skill_dir / 'SKILL.md'

            shutil.copy(temp_skill_path, final_skill_path)
            print(f"   ✅ Skill created: {final_skill_path}")

        print(f"\n{'='*60}")
        print(f"✅ SUCCESS: Skill '{skill_name}' created successfully")
        print(f"{'='*60}")
        print(f"\nLocation: .claude/skills/{skill_name}/SKILL.md")
        print(f"\nNext steps:")
        print(f"  1. Fill in remaining placeholders in SKILL.md")
        print(f"  2. Create references/ subdirectory for supporting docs")
        print(f"  3. Run validators again to verify completeness")
        print(f"  4. Test skill by invoking it")

        return 0

    except Exception as e:
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"❌ ERROR", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)
        print(f"{e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
