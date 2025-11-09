#!/usr/bin/env python3
"""
generate_command.py - Interactive command template generator

Orchestrates command generation with 9 template options:
  1. RPIV (Research-Plan-Implement-Verify)
  2. Human Approval
  3. Reflection
  4. Validation
  5. Batch Processing
  6. Routing
  7. Data Transformation
  8. Orchestration
  9. Reporting

Workflow:
  1. Interactive prompts
  2. Template selection
  3. Generate in temp dir
  4. Run all 4 validators
  5. If all pass: commit to .claude/commands/{env}/{name}.md
  6. If any fail: rollback temp dir
"""

import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional


# Template metadata
TEMPLATES = {
    '1': {'name': 'RPIV', 'file': 'COMMAND_RPIV_TEMPLATE.md', 'score': 9.8},
    '2': {'name': 'Human Approval', 'file': 'COMMAND_HUMAN_APPROVAL_TEMPLATE.md', 'score': 9.2},
    '3': {'name': 'Reflection', 'file': 'COMMAND_REFLECTION_TEMPLATE.md', 'score': 8.8},
    '4': {'name': 'Validation', 'file': 'COMMAND_VALIDATION_TEMPLATE.md', 'score': 8.6},
    '5': {'name': 'Batch Processing', 'file': 'COMMAND_BATCH_PROCESSING_TEMPLATE.md', 'score': 8.4},
    '6': {'name': 'Routing', 'file': 'COMMAND_ROUTING_TEMPLATE.md', 'score': 8.2},
    '7': {'name': 'Data Transformation', 'file': 'COMMAND_DATA_TRANSFORMATION_TEMPLATE.md', 'score': 7.8},
    '8': {'name': 'Orchestration', 'file': 'COMMAND_ORCHESTRATION_TEMPLATE.md', 'score': 7.5},
    '9': {'name': 'Reporting', 'file': 'COMMAND_REPORTING_TEMPLATE.md', 'score': 7.2},
}


def prompt(message: str, default: str = '') -> str:
    """Prompt user for input."""
    if default:
        user_input = input(f"{message} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{message}: ").strip()


def prompt_choice(message: str, choices: List[str]) -> str:
    """Prompt user to choose from list."""
    print(f"\n{message}")
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")
    while True:
        choice = input("Select (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(choices):
            return choices[int(choice) - 1]
        print(f"Invalid choice. Enter 1-{len(choices)}")


def show_templates():
    """Display available templates."""
    print("\n=== Available Command Templates ===\n")
    for key, template in TEMPLATES.items():
        print(f"{key}. {template['name']} (score: {template['score']}/10)")
        print(f"   File: {template['file']}")
    print()


def load_template(template_key: str, base_path: Path) -> str:
    """Load template content."""
    template_file = base_path / 'assets' / 'templates' / TEMPLATES[template_key]['file']
    return template_file.read_text()


def build_replacements(prompts: Dict[str, str]) -> Dict[str, str]:
    """Build replacement dictionary for placeholders."""
    return prompts


def run_validators(file_path: Path, scripts_dir: Path) -> Dict[str, Any]:
    """Run all 4 validators on generated file."""
    results = {}
    validators = [
        'validate_command_yaml.py',
        'validate_command_naming.py',
        'validate_command_structure.py',
        'validate_command_usage.py'
    ]

    all_passed = True

    for validator in validators:
        validator_path = scripts_dir / validator
        try:
            result = subprocess.run(
                [sys.executable, str(validator_path), str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )

            # Parse JSON output (first line)
            output_lines = result.stdout.split('\n')
            if output_lines:
                try:
                    validator_result = json.loads(output_lines[0])
                    results[validator] = validator_result
                    if not validator_result.get('passed', False):
                        all_passed = False
                except json.JSONDecodeError:
                    results[validator] = {
                        'passed': False,
                        'errors': ['Failed to parse validator output']
                    }
                    all_passed = False

        except Exception as e:
            results[validator] = {
                'passed': False,
                'errors': [f'Validator execution failed: {str(e)}']
            }
            all_passed = False

    return {'all_passed': all_passed, 'results': results}


def generate_command():
    """Main command generation workflow."""
    print("\n" + "="*60)
    print("  COMMAND TEMPLATE GENERATOR")
    print("="*60)

    # Find base path (where this script is located)
    base_path = Path(__file__).parent.parent

    # Step 1: Show templates
    show_templates()

    # Step 2: Get user inputs
    template_choice = prompt("Select template (1-9)", "1")
    if template_choice not in TEMPLATES:
        print(f"❌ Invalid template choice: {template_choice}")
        return 1

    command_name = prompt("Command name (kebab-case)", "my-command")
    environment = prompt("Environment (dev/prod/shared)", "dev")
    description = prompt("Description (≤1024 chars)", "Command description")

    # Step 3: Load template
    print(f"\n📝 Loading template: {TEMPLATES[template_choice]['name']}...")
    try:
        template_content = load_template(template_choice, base_path)
    except Exception as e:
        print(f"❌ Failed to load template: {e}")
        return 1

    # Step 4: Basic replacements (user can customize after generation)
    replacements = {
        '{{COMMAND_NAME}}': command_name,
        '{{DESCRIPTION}}': description,
        '{{COMMAND_TITLE}}': command_name.replace('-', ' ').title(),
    }

    output_content = template_content
    for placeholder, value in replacements.items():
        output_content = output_content.replace(placeholder, value)

    # Step 5: Create temp directory and generate file
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        output_file = temp_path / f"{command_name}.md"
        output_file.write_text(output_content)

        print(f"\n✅ Generated command in temp directory: {output_file}")

        # Step 6: Run validators
        print("\n🔍 Running validators...")
        scripts_dir = base_path / 'scripts'
        validation_results = run_validators(output_file, scripts_dir)

        # Display results
        print("\n--- Validation Results ---")
        for validator, result in validation_results['results'].items():
            status = "✅ PASS" if result.get('passed', False) else "❌ FAIL"
            print(f"{validator}: {status}")

            if result.get('errors'):
                for error in result['errors']:
                    print(f"    ❌ {error}")

            if result.get('warnings'):
                for warning in result['warnings']:
                    print(f"    ⚠️ {warning}")

        # Step 7: Commit or rollback
        if validation_results['all_passed']:
            # Create final path
            final_dir = Path(f".claude/commands/{environment}")
            final_dir.mkdir(parents=True, exist_ok=True)
            final_path = final_dir / f"{command_name}.md"

            # Copy from temp to final location
            shutil.copy2(output_file, final_path)

            print(f"\n✅ SUCCESS! Command created at:")
            print(f"   {final_path}")
            print(f"\n💡 Next steps:")
            print(f"   1. Edit {final_path} to fill remaining placeholders")
            print(f"   2. Test command: /{environment}:{command_name}")
            return 0
        else:
            print("\n❌ VALIDATION FAILED - Command not created")
            print("   Fix errors and try again")
            return 1


def main():
    try:
        return generate_command()
    except KeyboardInterrupt:
        print("\n\n⚠️ Generation cancelled by user")
        return 130
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
