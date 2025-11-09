#!/usr/bin/env python3
"""
generate_agent.py - Interactive agent template generator

Workflow:
1. Interactive prompts (name, template type, description, domain)
2. Template-specific prompts (areas, focus, checks)
3. Generate in temp directory
4. Run all 4 validators
5. Commit (all pass) or rollback (any fail)
6. Output final path or errors
"""

import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional


# Get script directory and project root
SCRIPT_DIR = Path(__file__).parent.resolve()
TEMPLATES_DIR = SCRIPT_DIR.parent / 'assets' / 'templates'
AGENTS_DIR = Path('/home/user/cc-sf-assistant/.claude/agents')


def prompt_input(message: str, default: str = '') -> str:
    """Prompt user for input with optional default."""
    if default:
        user_input = input(f"{message} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        user_input = input(f"{message}: ").strip()
        while not user_input:
            print("This field is required.")
            user_input = input(f"{message}: ").strip()
        return user_input


def prompt_choice(message: str, choices: List[str]) -> str:
    """Prompt user to select from a list of choices."""
    print(f"\n{message}")
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")

    while True:
        selection = input(f"Enter choice (1-{len(choices)}): ").strip()
        try:
            index = int(selection) - 1
            if 0 <= index < len(choices):
                return choices[index]
        except ValueError:
            pass
        print(f"Invalid choice. Please enter a number between 1 and {len(choices)}.")


def prompt_list(message: str, min_count: int, max_count: int) -> List[str]:
    """Prompt user for a list of items."""
    print(f"\n{message} (minimum {min_count}, maximum {max_count})")
    items = []

    for i in range(max_count):
        if i < min_count:
            item = prompt_input(f"  Item {i+1}")
        else:
            item = input(f"  Item {i+1} (press Enter to finish): ").strip()
            if not item:
                break
        items.append(item)

    return items


def load_template(template_type: str) -> str:
    """Load template content from file."""
    template_map = {
        'domain-specialist': 'AGENT_DOMAIN_SPECIALIST_TEMPLATE.md',
        'researcher': 'AGENT_READONLY_RESEARCHER_TEMPLATE.md',
        'reviewer': 'AGENT_FULL_ACCESS_IMPLEMENTER_TEMPLATE.md'
    }

    template_file = TEMPLATES_DIR / template_map[template_type]

    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")

    return template_file.read_text()


def generate_agent_content(template_type: str, params: Dict[str, Any]) -> str:
    """Generate agent content from template and parameters."""
    template = load_template(template_type)

    # Replace placeholders
    replacements = {
        '{{AGENT_NAME}}': params['name'],
        '{{AGENT_TITLE}}': params['title'],
        '{{DESCRIPTION}}': params['description'],
        '{{DOMAIN}}': params.get('domain', params['name']),
        '{{DOMAIN_FOCUS}}': params.get('domain_focus', params['description']),
        '{{RESEARCH_FOCUS}}': params.get('research_focus', params['description']),
        '{{REVIEW_FOCUS}}': params.get('review_focus', params['description'])
    }

    # Replace area/check placeholders
    for i, area in enumerate(params.get('areas', []), 1):
        replacements[f'{{{{AREA_{i}_NAME}}}}'] = area
        replacements[f'{{{{RESEARCH_AREA_{i}_NAME}}}}'] = area
        replacements[f'{{{{REVIEW_AREA_{i}_NAME}}}}'] = area

        # Add placeholder bullets
        for j in range(1, 9):
            replacements[f'{{{{AREA_{i}_BULLET_{j}}}}}'] = f'{area} capability {j}'
            replacements[f'{{{{RESEARCH_AREA_{i}_BULLET_{j}}}}}'] = f'{area} investigation {j}'
            replacements[f'{{{{REVIEW_AREA_{i}_BULLET_{j}}}}}'] = f'{area} verification {j}'

    for i, check in enumerate(params.get('checks', []), 1):
        replacements[f'{{{{CHECKLIST_{i}}}}}'] = check
        replacements[f'{{{{CHECK_{i}_NAME}}}}'] = check
        replacements[f'{{{{CHECK_{i}_CRITERION}}}}'] = f'{check} passes'

    # Apply replacements
    content = template
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    return content


def run_validator(validator_name: str, file_path: Path) -> Dict[str, Any]:
    """Run a validator script and return results."""
    validator_path = SCRIPT_DIR / f'{validator_name}.py'

    try:
        result = subprocess.run(
            ['python', str(validator_path), str(file_path)],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Parse JSON output from stdout
        output_lines = result.stdout.strip().split('\n')
        json_output = output_lines[0] if output_lines else '{}'

        validation_result = json.loads(json_output)
        validation_result['exit_code'] = result.returncode

        return validation_result

    except subprocess.TimeoutExpired:
        return {
            'validator': validator_name,
            'passed': False,
            'errors': ['Validator timed out'],
            'warnings': [],
            'info': {},
            'exit_code': 1
        }
    except json.JSONDecodeError:
        return {
            'validator': validator_name,
            'passed': False,
            'errors': ['Could not parse validator output'],
            'warnings': [],
            'info': {},
            'exit_code': 1
        }
    except Exception as e:
        return {
            'validator': validator_name,
            'passed': False,
            'errors': [f'Validator error: {str(e)}'],
            'warnings': [],
            'info': {},
            'exit_code': 1
        }


def validate_agent(file_path: Path) -> tuple[bool, List[Dict[str, Any]]]:
    """Run all validators on agent file. Returns (success, results)."""
    validators = [
        'validate_agent_yaml',
        'validate_agent_naming',
        'validate_agent_structure',
        'validate_agent_tools'
    ]

    results = []
    all_passed = True

    for validator in validators:
        result = run_validator(validator, file_path)
        results.append(result)

        if not result['passed']:
            all_passed = False

    return all_passed, results


def main():
    """Main interactive flow."""
    print("=" * 60)
    print("Agent Generator - Creating Agents Skill")
    print("=" * 60)

    # 1. Choose template type
    template_type = prompt_choice(
        "Select agent template:",
        ['domain-specialist', 'researcher', 'reviewer']
    )

    # 2. Basic information
    print("\n--- Basic Information ---")
    name = prompt_input("Agent name (kebab-case)", "fintech-analyst")
    title = prompt_input("Agent title (human-readable)", name.replace('-', ' ').title())
    description = prompt_input(
        "Description (100-150 chars)",
        f"{title} providing expert analysis and recommendations"
    )

    # 3. Template-specific prompts
    params = {
        'name': name,
        'title': title,
        'description': description
    }

    if template_type == 'domain-specialist':
        print("\n--- Domain Specialist Configuration ---")
        domain = prompt_input("Domain (e.g., financial, python, data-analysis)", "financial")
        domain_focus = prompt_input(
            "Domain focus",
            f"{domain} systems and best practices"
        )
        areas = prompt_list("Domain expertise areas", 8, 15)

        params['domain'] = domain
        params['domain_focus'] = domain_focus
        params['areas'] = areas
        params['checks'] = [
            "Requirements understood and validated",
            "Edge cases identified and handled",
            "Best practices applied",
            "Code quality meets standards",
            "Security considerations addressed",
            "Performance implications assessed",
            "Documentation complete",
            "Tests cover critical paths"
        ]

    elif template_type == 'researcher':
        print("\n--- Researcher Configuration ---")
        research_focus = prompt_input(
            "Research focus",
            "competitive intelligence and market analysis"
        )
        areas = prompt_list("Research expertise areas", 8, 15)

        params['research_focus'] = research_focus
        params['areas'] = areas
        params['checks'] = [
            "Research questions clearly defined",
            "Multiple sources consulted and validated",
            "Findings cross-referenced for accuracy",
            "Source credibility assessed",
            "Confidence levels documented",
            "Gaps in information identified",
            "Recommendations are actionable",
            "Methodology documented"
        ]

    elif template_type == 'reviewer':
        print("\n--- Reviewer Configuration ---")
        review_focus = prompt_input(
            "Review focus",
            "code quality, security, and compliance"
        )
        checks = prompt_list("Verification checks", 8, 8)

        params['review_focus'] = review_focus
        params['areas'] = checks  # For reviewer, checks become areas
        params['checks'] = checks

    # 4. Generate content
    print("\n--- Generating Agent ---")
    content = generate_agent_content(template_type, params)

    # 5. Write to temp file
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / f"{name}.md"
        temp_path.write_text(content)

        print(f"Generated: {temp_path}")

        # 6. Run validators
        print("\n--- Running Validators ---")
        all_passed, results = validate_agent(temp_path)

        for result in results:
            validator_name = result['validator']
            status = '✅ PASS' if result['passed'] else '❌ FAIL'
            print(f"{validator_name}: {status}")

            if result['errors']:
                for error in result['errors']:
                    print(f"  ❌ {error}")

            if result['warnings']:
                for warning in result['warnings']:
                    print(f"  ⚠️  {warning}")

        # 7. Commit or rollback
        if all_passed:
            print("\n--- Validation Passed ---")
            final_path = AGENTS_DIR / f"{name}.md"

            # Ensure agents directory exists
            AGENTS_DIR.mkdir(parents=True, exist_ok=True)

            # Copy to final location
            shutil.copy2(temp_path, final_path)

            print(f"✅ Created agent: {final_path}")
            print(f"\nInvoke with: @{name}")
            return 0
        else:
            print("\n--- Validation Failed ---")
            print("❌ Agent generation rolled back.")
            print("\nErrors found:")
            for result in results:
                if result['errors']:
                    print(f"\n{result['validator']}:")
                    for error in result['errors']:
                        print(f"  - {error}")
            return 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
