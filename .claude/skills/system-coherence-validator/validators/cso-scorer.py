#!/usr/bin/env python3
"""CSO (Claude Search Optimization) score calculator."""

from pathlib import Path
from typing import Dict, Any
import re


def count_trigger_phrases(content: str) -> int:
    """Count trigger phrases in 'Trigger Phrases' section.

    Args:
        content: SKILL.md content

    Returns:
        Number of trigger phrases found
    """
    # Find Trigger Phrases section
    match = re.search(r'### Trigger Phrases\s*\n(.*?)(?=###|\n---|\Z)', content, re.DOTALL)
    if not match:
        return 0

    section = match.group(1)
    # Count bullet points (lines starting with -)
    phrases = re.findall(r'^\s*-\s*"([^"]+)"', section, re.MULTILINE)
    return len(phrases)


def count_symptoms(content: str) -> int:
    """Count symptoms in 'Symptoms' section.

    Args:
        content: SKILL.md content

    Returns:
        Number of symptoms found
    """
    match = re.search(r'### Symptoms\s*\n(.*?)(?=###|\n---|\Z)', content, re.DOTALL)
    if not match:
        return 0

    section = match.group(1)
    # Count bullet points
    symptoms = re.findall(r'^\s*-\s+', section, re.MULTILINE)
    return len(symptoms)


def count_agnostic_keywords(content: str) -> int:
    """Count agnostic keywords in 'Agnostic Keywords' section.

    Args:
        content: SKILL.md content

    Returns:
        Number of keywords found
    """
    match = re.search(r'### Agnostic Keywords\s*\n(.*?)(?=###|\n---|\Z)', content, re.DOTALL)
    if not match:
        return 0

    section = match.group(1)
    # Count bullet points or comma-separated terms
    keywords = re.findall(r'^\s*-\s+', section, re.MULTILINE)
    if keywords:
        return len(keywords)

    # Try comma-separated format
    keywords = [k.strip() for k in section.split('\n') if k.strip() and not k.strip().startswith('#')]
    if keywords:
        # Count words/phrases
        return sum(len([w for w in line.split(',') if w.strip()]) for line in keywords)

    return 0


def count_examples(content: str) -> int:
    """Count examples in 'Examples' section.

    Args:
        content: SKILL.md content

    Returns:
        Number of examples found
    """
    # Find Examples section
    match = re.search(r'## Examples\s*\n(.*?)(?=##|\n---|\Z)', content, re.DOTALL)
    if not match:
        return 0

    section = match.group(1)
    # Count example subsections (### Example 1, ### Example 2, etc.)
    examples = re.findall(r'### Example \d+', section)
    return len(examples)


def calculate_cso_score(file_path: Path) -> Dict[str, Any]:
    """Calculate CSO score for a SKILL.md file.

    CSO Framework (4 Pillars):
    - Trigger Phrases: 40% weight (0.4)
    - Symptoms: 30% weight (0.3)
    - Agnostic Keywords: 20% weight (0.2)
    - Examples: 10% weight (0.1)

    Scoring:
    - Each pillar scored 0-1 based on count:
      - Trigger Phrases: 10+ = 1.0, 8+ = 0.8, 5+ = 0.6, <5 = 0.4
      - Symptoms: 8+ = 1.0, 6+ = 0.8, 4+ = 0.6, <4 = 0.4
      - Keywords: 15+ = 1.0, 12+ = 0.8, 8+ = 0.6, <8 = 0.4
      - Examples: 5+ = 1.0, 4+ = 0.8, 3+ = 0.6, <3 = 0.4

    Args:
        file_path: Path to SKILL.md

    Returns:
        Dictionary with CSO score breakdown
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # Count each pillar
    trigger_count = count_trigger_phrases(content)
    symptom_count = count_symptoms(content)
    keyword_count = count_agnostic_keywords(content)
    example_count = count_examples(content)

    # Score each pillar (0-1)
    def score_pillar(count: int, thresholds: list) -> float:
        for threshold, score in reversed(thresholds):
            if count >= threshold:
                return score
        return 0.4

    trigger_score = score_pillar(trigger_count, [(10, 1.0), (8, 0.8), (5, 0.6)])
    symptom_score = score_pillar(symptom_count, [(8, 1.0), (6, 0.8), (4, 0.6)])
    keyword_score = score_pillar(keyword_count, [(15, 1.0), (12, 0.8), (8, 0.6)])
    example_score = score_pillar(example_count, [(5, 1.0), (4, 0.8), (3, 0.6)])

    # Calculate weighted CSO score
    cso_score = (
        0.4 * trigger_score +
        0.3 * symptom_score +
        0.2 * keyword_score +
        0.1 * example_score
    )

    return {
        'file': str(file_path),
        'cso_score': round(cso_score, 2),
        'breakdown': {
            'trigger_phrases': {
                'count': trigger_count,
                'score': trigger_score,
                'weight': 0.4
            },
            'symptoms': {
                'count': symptom_count,
                'score': symptom_score,
                'weight': 0.3
            },
            'agnostic_keywords': {
                'count': keyword_count,
                'score': keyword_score,
                'weight': 0.2
            },
            'examples': {
                'count': example_count,
                'score': example_score,
                'weight': 0.1
            }
        }
    }


def check_cso_threshold(cso_score: float, skill_name: str) -> Dict[str, Any]:
    """Check if CSO score meets tiered threshold.

    Tiered thresholds:
    - Critical skills: ≥0.8 (hook-factory, financial-quality-gate)
    - High priority: ≥0.7 (other meta-skills)
    - Standard: ≥0.6 (remaining skills)

    Args:
        cso_score: Calculated CSO score
        skill_name: Name of skill

    Returns:
        Dictionary with pass/fail result
    """
    # Critical skills
    critical_skills = ['hook-factory', 'financial-quality-gate']
    # High priority skills
    high_priority_skills = [
        'hierarchical-context-manager',
        'system-coherence-validator',
        'multi-agent-workflow-coordinator'
    ]

    if skill_name in critical_skills:
        threshold = 0.8
        tier = 'critical'
    elif skill_name in high_priority_skills:
        threshold = 0.7
        tier = 'high_priority'
    else:
        threshold = 0.6
        tier = 'standard'

    passed = cso_score >= threshold

    return {
        'tier': tier,
        'threshold': threshold,
        'actual': cso_score,
        'passed': passed,
        'margin': round(cso_score - threshold, 2)
    }


if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: cso-scorer.py <SKILL.md>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    result = calculate_cso_score(file_path)

    # Extract skill name from path
    skill_name = file_path.parent.name if file_path.name == 'SKILL.md' else 'unknown'
    threshold_check = check_cso_threshold(result['cso_score'], skill_name)

    print(f"File: {result['file']}")
    print(f"CSO Score: {result['cso_score']}")
    print(f"\nBreakdown:")
    for pillar, data in result['breakdown'].items():
        print(f"  {pillar}: {data['count']} items → score {data['score']} (weight {data['weight']})")

    print(f"\nThreshold Check:")
    print(f"  Tier: {threshold_check['tier']}")
    print(f"  Threshold: {threshold_check['threshold']}")
    print(f"  Actual: {threshold_check['actual']}")
    print(f"  Status: {'✅ PASS' if threshold_check['passed'] else '❌ FAIL'}")
    print(f"  Margin: {threshold_check['margin']:+.2f}")

    sys.exit(0 if threshold_check['passed'] else 1)
