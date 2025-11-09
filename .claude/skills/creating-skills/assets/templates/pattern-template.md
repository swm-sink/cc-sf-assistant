# Pattern Template

**Purpose:** Template for pattern-type skills (mental models with before/after comparisons)

**Use when:** Teaching a design pattern, anti-pattern, or structural approach

**Structure:** 7 sections (Overview → Problem → Solution → Before/After → When to Apply → Examples → Progressive Disclosure)

---

## Template Structure

```markdown
---
name: {{SKILL_NAME}}
description: {{CSO_OPTIMIZED_DESCRIPTION}}
---

# {{SKILL_TITLE}}

## Overview

**Pattern type:** {{PATTERN_TYPE}}

**Core idea:** {{ONE_SENTENCE_SUMMARY}}

**What this pattern provides:**
- {{BENEFIT_1}}
- {{BENEFIT_2}}
- {{BENEFIT_3}}

**What this pattern doesn't solve:**
- {{NON_BENEFIT_1}}
- {{NON_BENEFIT_2}}

---

## The Problem

### Symptoms

{{PROBLEM_DESCRIPTION}}

**You'll notice:**
- {{SYMPTOM_1}}
- {{SYMPTOM_2}}
- {{SYMPTOM_3}}

**Why this is a problem:**
- {{CONSEQUENCE_1}}
- {{CONSEQUENCE_2}}
- {{CONSEQUENCE_3}}

**Common causes:**
- {{ROOT_CAUSE_1}}
- {{ROOT_CAUSE_2}}

---

## The Solution Pattern

### Pattern Structure

{{PATTERN_DESCRIPTION}}

**Key components:**

1. **{{COMPONENT_1_NAME}}**
   - {{COMPONENT_1_PURPOSE}}
   - {{COMPONENT_1_RESPONSIBILITY}}

2. **{{COMPONENT_2_NAME}}**
   - {{COMPONENT_2_PURPOSE}}
   - {{COMPONENT_2_RESPONSIBILITY}}

3. **{{COMPONENT_3_NAME}}**
   - {{COMPONENT_3_PURPOSE}}
   - {{COMPONENT_3_RESPONSIBILITY}}

**How components interact:**

{{INTERACTION_DESCRIPTION}}

**Why this works:**

{{RATIONALE}}

---

## Before/After Comparison

### ❌ Before (Anti-Pattern)

**Structure:**
```
{{BEFORE_STRUCTURE}}
```

**Problems:**
- {{BEFORE_PROBLEM_1}}
- {{BEFORE_PROBLEM_2}}
- {{BEFORE_PROBLEM_3}}

**Code smell example:**
```{{LANGUAGE}}
{{BEFORE_CODE_EXAMPLE}}
```

### ✅ After (Pattern Applied)

**Structure:**
```
{{AFTER_STRUCTURE}}
```

**Improvements:**
- {{AFTER_BENEFIT_1}}
- {{AFTER_BENEFIT_2}}
- {{AFTER_BENEFIT_3}}

**Pattern example:**
```{{LANGUAGE}}
{{AFTER_CODE_EXAMPLE}}
```

### What Changed

| Aspect | Before | After |
|--------|--------|-------|
| {{ASPECT_1}} | {{BEFORE_STATE_1}} | {{AFTER_STATE_1}} |
| {{ASPECT_2}} | {{BEFORE_STATE_2}} | {{AFTER_STATE_2}} |
| {{ASPECT_3}} | {{BEFORE_STATE_3}} | {{AFTER_STATE_3}} |

---

## When to Apply

### Use this pattern when:

- {{TRIGGER_1}}
- {{TRIGGER_2}}
- {{TRIGGER_3}}

### Don't use this pattern when:

- {{ANTI_TRIGGER_1}}
- {{ANTI_TRIGGER_2}}
- {{ANTI_TRIGGER_3}}

### Prerequisites:

- {{PREREQUISITE_1}}
- {{PREREQUISITE_2}}

### Trade-offs:

| Gain | Cost |
|------|------|
| {{GAIN_1}} | {{COST_1}} |
| {{GAIN_2}} | {{COST_2}} |
| {{GAIN_3}} | {{COST_3}} |

---

## Examples

### Example 1: {{EXAMPLE_1_DOMAIN}}

**Context:** {{EXAMPLE_1_CONTEXT}}

**Before pattern:**
```{{LANGUAGE}}
{{EXAMPLE_1_BEFORE}}
```

**Problem:** {{EXAMPLE_1_PROBLEM}}

**After pattern:**
```{{LANGUAGE}}
{{EXAMPLE_1_AFTER}}
```

**Improvement:** {{EXAMPLE_1_IMPROVEMENT}}

### Example 2: {{EXAMPLE_2_DOMAIN}}

**Context:** {{EXAMPLE_2_CONTEXT}}

**Before pattern:**
```{{LANGUAGE}}
{{EXAMPLE_2_BEFORE}}
```

**Problem:** {{EXAMPLE_2_PROBLEM}}

**After pattern:**
```{{LANGUAGE}}
{{EXAMPLE_2_AFTER}}
```

**Improvement:** {{EXAMPLE_2_IMPROVEMENT}}

{{ADDITIONAL_EXAMPLES}}

---

## Progressive Disclosure

**For detailed information, see:**
- `references/{{REFERENCE_DOC_1}}.md` - {{REFERENCE_DOC_1_PURPOSE}}
- `references/{{REFERENCE_DOC_2}}.md` - {{REFERENCE_DOC_2_PURPOSE}}

**Advanced patterns:**
- {{ADVANCED_PATTERN_1}}
- {{ADVANCED_PATTERN_2}}

**Related patterns:**
- {{RELATED_PATTERN_1}}
- {{RELATED_PATTERN_2}}

**Further reading:**
- {{EXTERNAL_REFERENCE_1}}
- {{EXTERNAL_REFERENCE_2}}
```

---

## Placeholder Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{SKILL_NAME}}` | Kebab-case skill directory name | `adapter-pattern`, `separation-of-concerns` |
| `{{CSO_OPTIMIZED_DESCRIPTION}}` | Description with problem symptoms and pattern keywords | "Use when external APIs tightly coupled to business logic, noticing repeated API code, or wanting to swap implementations" |
| `{{SKILL_TITLE}}` | Human-readable title | "Adapter Pattern", "Separation of Concerns" |
| `{{PATTERN_TYPE}}` | Classification | "Structural", "Behavioral", "Architectural" |
| `{{ONE_SENTENCE_SUMMARY}}` | Core concept | "Abstract external dependencies so business logic remains pure" |
| `{{BENEFIT_X}}` | What pattern provides | "Testable business logic without API calls" |
| `{{NON_BENEFIT_X}}` | What pattern doesn't solve | "Doesn't improve API performance" |
| `{{PROBLEM_DESCRIPTION}}` | Problem context | "Business logic tightly coupled to Google Sheets API makes testing impossible" |
| `{{SYMPTOM_X}}` | Observable issue | "Can't test variance calculation without live API calls" |
| `{{CONSEQUENCE_X}}` | Impact of problem | "Tests fail when API down, slow test suite" |
| `{{ROOT_CAUSE_X}}` | Why problem exists | "Direct API calls scattered throughout business logic" |
| `{{PATTERN_DESCRIPTION}}` | How pattern works | "Introduce adapter layer between business logic and external system" |
| `{{COMPONENT_X_NAME}}` | Pattern element | "AdapterInterface", "ConcreteAdapter", "BusinessLogic" |
| `{{COMPONENT_X_PURPOSE}}` | Element role | "Defines contract for data access" |
| `{{COMPONENT_X_RESPONSIBILITY}}` | Element duties | "Abstracts external system details" |
| `{{INTERACTION_DESCRIPTION}}` | How components work together | "BusinessLogic depends on AdapterInterface, ConcreteAdapter implements interface" |
| `{{RATIONALE}}` | Why pattern effective | "Business logic tests with mock adapter, swap adapters without changing logic" |
| `{{BEFORE_STRUCTURE}}` | Anti-pattern organization | "variance.py → calls gspread directly" |
| `{{BEFORE_PROBLEM_X}}` | Anti-pattern issue | "Can't test without API credentials" |
| `{{BEFORE_CODE_EXAMPLE}}` | Code smell | `calculate_variance(gspread.open('sheet'))` |
| `{{AFTER_STRUCTURE}}` | Pattern organization | "variance.py → AdapterInterface ← GoogleSheetsAdapter" |
| `{{AFTER_BENEFIT_X}}` | Pattern advantage | "Test with MockAdapter" |
| `{{AFTER_CODE_EXAMPLE}}` | Clean pattern | `calculate_variance(adapter.read_data())` |
| `{{ASPECT_X}}` | Comparison dimension | "Testability", "Coupling", "Flexibility" |
| `{{BEFORE_STATE_X}}` | Pre-pattern state | "Impossible (needs live API)" |
| `{{AFTER_STATE_X}}` | Post-pattern state | "Easy (mock adapter)" |
| `{{TRIGGER_X}}` | When to apply | "Need to swap implementations" |
| `{{ANTI_TRIGGER_X}}` | When NOT to apply | "Single API call in entire system" |
| `{{PREREQUISITE_X}}` | Required before applying | "Identified external dependency" |
| `{{GAIN_X}}` | Pattern benefit | "Testability" |
| `{{COST_X}}` | Pattern overhead | "Extra interface layer" |
| `{{EXAMPLE_X_DOMAIN}}` | Example context | "FP&A Budget Import" |
| `{{EXAMPLE_X_CONTEXT}}` | Scenario setup | "Import budget from Google Sheets for variance analysis" |
| `{{EXAMPLE_X_BEFORE}}` | Before code | Code with tight coupling |
| `{{EXAMPLE_X_PROBLEM}}` | Issue demonstrated | "Can't test without Google credentials" |
| `{{EXAMPLE_X_AFTER}}` | After code | Code with adapter pattern |
| `{{EXAMPLE_X_IMPROVEMENT}}` | Result achieved | "Tests run offline with mock data" |
| `{{LANGUAGE}}` | Code language | `python`, `typescript`, `markdown` |
| `{{REFERENCE_DOC_X}}` | Supporting document | "adapter-implementations", "testing-adapters" |
| `{{ADVANCED_PATTERN_X}}` | Deep-dive topic | "Multi-adapter composition" |
| `{{RELATED_PATTERN_X}}` | Connected pattern | "Dependency injection", "Strategy pattern" |
| `{{EXTERNAL_REFERENCE_X}}` | Outside resource | "Gang of Four Design Patterns" |

---

## CSO Optimization Guidelines

**Pattern skills should include:**

1. **Problem symptom keywords** (what observable issues indicate need)
   - "noticing X", "experiencing Y", "finding Z difficult"
   - Example: "noticing tight coupling", "can't test without API"

2. **Trigger phrases** (when pattern applies)
   - "when X", "need to Y", "want to Z"
   - Example: "when swapping implementations", "need to test without API"

3. **Domain-agnostic pattern names** (reusable across contexts)
   - Classic pattern names: "adapter", "observer", "strategy"
   - Structural concepts: "separation", "abstraction", "composition"

4. **Before/after keywords** (transformation language)
   - "tightly coupled" → "loosely coupled"
   - "untestable" → "testable"
   - "rigid" → "flexible"

**Target CSO score: ≥0.7** (measured by validate_cso.py)

---

## Validation Checklist

When using this template, validate:

- [ ] YAML frontmatter present with name + CSO-optimized description
- [ ] All 7 sections present (Overview → Problem → Solution → Before/After → When to Apply → Examples → Progressive Disclosure)
- [ ] The Problem section describes symptoms, consequences, causes
- [ ] The Solution Pattern section defines ≥3 components with interactions
- [ ] Before/After Comparison shows clear transformation (structure + code examples)
- [ ] When to Apply includes use cases, anti-cases, prerequisites, trade-offs
- [ ] Examples has ≥2 concrete scenarios with before/after code
- [ ] Progressive Disclosure references supporting docs in references/
- [ ] Line count <200 (main SKILL.md, not including references/)
- [ ] Active-voice naming if applicable
- [ ] CSO score ≥0.7

---

**Template Version:** 1.0
**Last Updated:** 2025-11-09
**Skill Type:** Pattern (mental model with before/after comparison)
