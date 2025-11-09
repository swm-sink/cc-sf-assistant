# Technique Template

**Purpose:** Template for technique-type skills (how-to guides with step-by-step instructions)

**Use when:** Teaching a specific procedure, workflow, or method

**Structure:** 6 sections (Overview → When to Use → Instructions → Pitfalls → Examples → Progressive Disclosure)

---

## Template Structure

```markdown
---
name: {{SKILL_NAME}}
description: {{CSO_OPTIMIZED_DESCRIPTION}}
---

# {{SKILL_TITLE}}

## Overview

**Purpose:** {{ONE_SENTENCE_PURPOSE}}

**What this technique does:**
- {{BENEFIT_1}}
- {{BENEFIT_2}}
- {{BENEFIT_3}}

**What this technique doesn't do:**
- {{NON_BENEFIT_1}}
- {{NON_BENEFIT_2}}

**Key principle:** {{FOUNDATIONAL_PRINCIPLE}}

---

## When to Use This {{TECHNIQUE_NAME}}

**Use when:**
- {{TRIGGER_SCENARIO_1}}
- {{TRIGGER_SCENARIO_2}}
- {{TRIGGER_SCENARIO_3}}

**Don't use when:**
- {{ANTI_PATTERN_1}}
- {{ANTI_PATTERN_2}}

**Prerequisites:**
- {{PREREQUISITE_1}}
- {{PREREQUISITE_2}}

---

## Step-by-Step Instructions

### Step 1: {{STEP_1_NAME}}

{{STEP_1_DESCRIPTION}}

**Actions:**
1. {{ACTION_1}}
2. {{ACTION_2}}
3. {{ACTION_3}}

**Expected outcome:** {{STEP_1_OUTCOME}}

### Step 2: {{STEP_2_NAME}}

{{STEP_2_DESCRIPTION}}

**Actions:**
1. {{ACTION_1}}
2. {{ACTION_2}}
3. {{ACTION_3}}

**Expected outcome:** {{STEP_2_OUTCOME}}

### Step 3: {{STEP_3_NAME}}

{{STEP_3_DESCRIPTION}}

**Actions:**
1. {{ACTION_1}}
2. {{ACTION_2}}
3. {{ACTION_3}}

**Expected outcome:** {{STEP_3_OUTCOME}}

{{ADDITIONAL_STEPS}}

---

## Common Pitfalls

### Pitfall 1: {{PITFALL_1_NAME}}

**Symptom:** {{HOW_TO_RECOGNIZE}}

**Why it happens:** {{ROOT_CAUSE}}

**How to avoid:** {{PREVENTION_STRATEGY}}

### Pitfall 2: {{PITFALL_2_NAME}}

**Symptom:** {{HOW_TO_RECOGNIZE}}

**Why it happens:** {{ROOT_CAUSE}}

**How to avoid:** {{PREVENTION_STRATEGY}}

### Pitfall 3: {{PITFALL_3_NAME}}

**Symptom:** {{HOW_TO_RECOGNIZE}}

**Why it happens:** {{ROOT_CAUSE}}

**How to avoid:** {{PREVENTION_STRATEGY}}

{{ADDITIONAL_PITFALLS}}

---

## Examples

### Example 1: {{EXAMPLE_1_SCENARIO}}

**Context:** {{SCENARIO_DESCRIPTION}}

**Application:**

**Step 1:** {{EXAMPLE_STEP_1}}
**Step 2:** {{EXAMPLE_STEP_2}}
**Step 3:** {{EXAMPLE_STEP_3}}

**Result:** {{EXAMPLE_OUTCOME}}

### Example 2: {{EXAMPLE_2_SCENARIO}}

**Context:** {{SCENARIO_DESCRIPTION}}

**Application:**

**Step 1:** {{EXAMPLE_STEP_1}}
**Step 2:** {{EXAMPLE_STEP_2}}
**Step 3:** {{EXAMPLE_STEP_3}}

**Result:** {{EXAMPLE_OUTCOME}}

{{ADDITIONAL_EXAMPLES}}

---

## Progressive Disclosure

**For detailed information, see:**
- `references/{{REFERENCE_DOC_1}}.md` - {{REFERENCE_DOC_1_PURPOSE}}
- `references/{{REFERENCE_DOC_2}}.md` - {{REFERENCE_DOC_2_PURPOSE}}

**Advanced topics:**
- {{ADVANCED_TOPIC_1}}
- {{ADVANCED_TOPIC_2}}

**Related skills:**
- {{RELATED_SKILL_1}}
- {{RELATED_SKILL_2}}
```

---

## Placeholder Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{SKILL_NAME}}` | Kebab-case skill directory name | `creating-skills`, `enforcing-research-plan-implement-verify` |
| `{{CSO_OPTIMIZED_DESCRIPTION}}` | Description with trigger keywords, symptoms, examples (CSO ≥0.7) | "Use when about to implement features, fix bugs, change code, or refactor, before writing implementation code, when thinking 'this is simple enough to skip research', or when under time pressure" |
| `{{SKILL_TITLE}}` | Human-readable title | "Creating Skills", "Enforcing Research → Plan → Implement → Verify" |
| `{{ONE_SENTENCE_PURPOSE}}` | Concise purpose statement | "Enforce Research → Plan → Implement → Verify workflow for all implementations" |
| `{{BENEFIT_X}}` | Positive capability | "Prevents implementing without research" |
| `{{NON_BENEFIT_X}}` | Explicit exclusion | "Doesn't write code for you (enforces process only)" |
| `{{FOUNDATIONAL_PRINCIPLE}}` | Core concept | "NO IMPLEMENTATION WITHOUT RESEARCH & APPROVED PLAN FIRST" |
| `{{TRIGGER_SCENARIO_X}}` | When to invoke skill | "About to write implementation code" |
| `{{ANTI_PATTERN_X}}` | When NOT to use | "Pure documentation updates (no code changes)" |
| `{{PREREQUISITE_X}}` | Required before using | "User request requires code implementation" |
| `{{STEP_X_NAME}}` | Step label | "Research Phase", "Plan Phase" |
| `{{STEP_X_DESCRIPTION}}` | Step explanation | "Investigate existing patterns without writing code" |
| `{{ACTION_X}}` | Concrete action | "Read existing files with Read tool" |
| `{{STEP_X_OUTCOME}}` | Expected result | "Research findings documented in specs/{topic}/research.md" |
| `{{PITFALL_X_NAME}}` | Common mistake | "Skipping research for 'simple' changes" |
| `{{HOW_TO_RECOGNIZE}}` | Warning sign | "Thinking 'I already know how to do this'" |
| `{{ROOT_CAUSE}}` | Why mistake happens | "Overconfidence in existing knowledge" |
| `{{PREVENTION_STRATEGY}}` | How to avoid | "Research validates assumptions even when confident" |
| `{{EXAMPLE_X_SCENARIO}}` | Example context | "Google Sheets integration request" |
| `{{SCENARIO_DESCRIPTION}}` | Example setup | "User requests importing budget data from Google Sheets" |
| `{{EXAMPLE_STEP_X}}` | Example step execution | "Research: Read external/gspread/ to understand authentication" |
| `{{EXAMPLE_OUTCOME}}` | Example result | "Successfully integrated with proper error handling" |
| `{{REFERENCE_DOC_X}}` | Progressive disclosure doc | "checkpoint-examples", "complete-rationalization-table" |
| `{{ADVANCED_TOPIC_X}}` | Deep-dive topic | "Emergency override protocols" |
| `{{RELATED_SKILL_X}}` | Related skill reference | "creating-commands", "financial-validator" |

---

## CSO Optimization Guidelines

**Technique skills should include:**

1. **Trigger phrases** (what actions invoke this)
   - "when X", "before Y", "after Z"
   - Example: "when about to implement", "before writing code"

2. **Symptom keywords** (red flags that indicate need)
   - "thinking X", "feeling Y", "noticing Z"
   - Example: "thinking 'this is simple'", "under time pressure"

3. **Technology-agnostic keywords** (broad applicability)
   - Generic action verbs: "creating", "implementing", "analyzing"
   - Domain concepts: "workflow", "process", "methodology"

4. **Specific examples** (concrete use cases)
   - "Google Sheets integration", "variance calculation"
   - Real scenarios users will encounter

**Target CSO score: ≥0.7** (measured by validate_cso.py)

---

## Validation Checklist

When using this template, validate:

- [ ] YAML frontmatter present with name + CSO-optimized description
- [ ] All 6 sections present (Overview → When to Use → Instructions → Pitfalls → Examples → Progressive Disclosure)
- [ ] Step-by-Step Instructions has ≥3 steps with actions and outcomes
- [ ] Common Pitfalls has ≥3 pitfalls with symptoms, causes, prevention
- [ ] Examples has ≥2 concrete scenarios with step-by-step application
- [ ] Progressive Disclosure references supporting docs in references/
- [ ] Line count <200 (main SKILL.md, not including references/)
- [ ] Active-voice naming (creating-X not X-creator)
- [ ] CSO score ≥0.7

---

**Template Version:** 1.0
**Last Updated:** 2025-11-09
**Skill Type:** Technique (how-to guide)
