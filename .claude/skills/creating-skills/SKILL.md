---
name: creating-skills
description: Use when creating skills, building new capabilities, need templates, want scaffolding, generating skill files, before writing SKILL.md, thinking "I need a starting point", "how do I structure this", noticing missing CSO optimization, or planning technique/pattern/discipline/reference skills - provides specialized templates with validation, CSO optimization, rationalization-proofing, and examples for workflow enforcement, API reference, mental models
---

# Creating Skills

## Overview

**Purpose:** Generate new skills using specialized templates with built-in validation and best practices.

**What this technique does:**
- Provides 4 specialized templates (technique, pattern, discipline, reference)
- Validates skill structure, naming, CSO score, and rationalization-proofing
- Generates skills with CSO-optimized descriptions for auto-invocation
- Includes rationalization-proofing for discipline skills

**What this technique doesn't do:**
- Doesn't write skill content for you (provides templates with placeholders)
- Doesn't test skills (see `references/testing-protocol.md`)
- Doesn't auto-invoke skills (you invoke this when creating skills)

**Key principle:** Specialized templates for different skill types ensure consistent structure and quality.

---

## When to Use

**Use when:**
- Creating a new skill from scratch
- Need a starting point for skill structure
- Want to ensure skill follows best practices
- Building technique, pattern, discipline, or reference skill
- Need CSO optimization guidance
- Adding rationalization-proofing to discipline skill

**Don't use when:**
- Editing existing skill (use Read/Edit tools directly)
- Creating slash commands (use creating-commands instead)
- Creating agents (use creating-agents instead)
- Pure documentation (not a skill)

**Prerequisites:**
- Understand skill type (technique/pattern/discipline/reference)
- Have clear purpose for skill
- Know CSO requirements (or will learn from templates)

---

## Step-by-Step Instructions

### Step 1: Choose Skill Type

**Determine which template to use:**

| Type | Purpose | Sections | Use When |
|------|---------|----------|----------|
| **Technique** | How-to guides | 6 | Step-by-step instructions needed |
| **Pattern** | Mental models | 7 | Before/after transformation |
| **Discipline** | Workflow enforcement | 12 | Process enforcement with rationalization-proofing |
| **Reference** | Quick lookup | 5 | API docs, command reference, tables |

**Actions:**
1. Read skill purpose
2. Match to table above
3. Select appropriate type

**Expected outcome:** Clear skill type chosen (technique/pattern/discipline/reference).

### Step 2: Run Skill Generator

**Use orchestrator script to generate skill:**

**Actions:**
1. Navigate to `.claude/skills/creating-skills/scripts/`
2. Run: `python generate_skill.py`
3. Answer interactive prompts:
   - Skill name (kebab-case)
   - Skill type (technique/pattern/discipline/reference)
   - Skill title (human-readable)
   - Description (CSO-optimized, ≥50 chars)
   - One-sentence purpose
4. Script generates skill in temp directory
5. Script runs all 5 validators
6. If all pass, script commits to `.claude/skills/{skill-name}/SKILL.md`

**Expected outcome:** Skill scaffold created at `.claude/skills/{skill-name}/SKILL.md`.

### Step 3: Fill Placeholders

**Complete template placeholders with actual content:**

**Actions:**
1. Open `.claude/skills/{skill-name}/SKILL.md`
2. Find all `{{PLACEHOLDER}}` markers
3. Replace with actual content:
   - `{{BENEFIT_X}}`: Specific capabilities
   - `{{STEP_X_NAME}}`: Actual step names
   - `{{ACTION_X}}`: Concrete actions
   - `{{EXAMPLE_X}}`: Real examples
4. Remove any unused placeholder sections
5. Adjust structure as needed (templates are starting points)

**Expected outcome:** All placeholders replaced with meaningful content.

### Step 4: Optimize CSO Description

**Ensure description triggers auto-invocation:**

**Actions:**
1. Run: `python scripts/validate_cso.py .claude/skills/{skill-name}/SKILL.md`
2. Check CSO score (target ≥0.7)
3. If score low, add missing keywords:
   - Trigger phrases (when, before, after, use when, need to)
   - Symptom keywords (thinking, noticing, under pressure)
   - Agnostic keywords (creating, implementing, workflow)
   - Specific examples (Google Sheets, variance, budget)
4. Re-run validator until score ≥0.7

**Expected outcome:** CSO score ≥0.7, skill auto-invokes at right times.

### Step 5: Create Supporting Documents (Optional)

**Add progressive disclosure references:**

**Actions:**
1. Create `.claude/skills/{skill-name}/references/` directory
2. Move detailed content from SKILL.md to references/:
   - Complete examples
   - Comprehensive tables
   - Advanced topics
   - Testing scenarios
3. Reference from SKILL.md:
   - `See references/complete-examples.md`
   - `See references/advanced-topics.md`
4. Keep SKILL.md <200 lines

**Expected outcome:** Main SKILL.md concise, details in references/.

### Step 6: Validate and Test

**Run all validators and test skill:**

**Actions:**
1. Run all 5 validators:
   ```bash
   python scripts/validate_yaml.py .claude/skills/{skill-name}/SKILL.md
   python scripts/validate_naming.py .claude/skills/{skill-name}/SKILL.md
   python scripts/validate_structure.py .claude/skills/{skill-name}/SKILL.md
   python scripts/validate_cso.py .claude/skills/{skill-name}/SKILL.md
   python scripts/validate_rationalization.py .claude/skills/{skill-name}/SKILL.md
   ```
2. Fix any errors (exit code 1)
3. Consider warnings (exit code 2)
4. Test skill by invoking it in real scenario
5. Iterate based on testing feedback

**Expected outcome:** All validators pass, skill works as expected.

---

## Common Pitfalls

### Pitfall 1: Wrong Template Type

**Symptom:** Skill structure doesn't match purpose (e.g., using technique template for workflow enforcement)

**Why it happens:** Unclear distinction between skill types

**How to avoid:**
- Technique = step-by-step how-to
- Pattern = before/after transformation
- Discipline = workflow enforcement with rationalization-proofing
- Reference = quick lookup tables

### Pitfall 2: Poor CSO Optimization

**Symptom:** Skill never auto-invokes, CSO score <0.7

**Why it happens:** Description too generic, missing trigger keywords

**How to avoid:**
- Include "Use when" prefix
- Add 3+ trigger phrases (when, before, after, need to)
- Add 2+ symptom keywords (thinking, noticing, under pressure)
- Add 2+ specific examples (Google Sheets, variance)
- Run validate_cso.py until score ≥0.7

### Pitfall 3: Incomplete Rationalization-Proofing (Discipline Skills)

**Symptom:** Discipline skill gets bypassed under pressure

**Why it happens:** Missing Iron Law, red flags, or rationalization table

**How to avoid:**
- Use discipline template (has all required sections)
- Include Iron Law in ALL CAPS code block
- Add ≥6 explicit negations
- Create ≥10 rationalization table entries
- Add ≥8 red flags with Reality checks
- Run validate_rationalization.py

### Pitfall 4: Leaving Placeholders Unfilled

**Symptom:** SKILL.md contains {{PLACEHOLDER}} markers after "completion"

**Why it happens:** Forgot to replace template placeholders

**How to avoid:**
- Search for `{{` in SKILL.md
- Replace all placeholders with actual content
- Remove unused placeholder sections
- Validators will catch this (validate_structure.py warnings)

### Pitfall 5: SKILL.md Too Long

**Symptom:** SKILL.md exceeds 200 lines, hard to read

**Why it happens:** Including too much detail in main file

**How to avoid:**
- Move comprehensive examples to `references/complete-examples.md`
- Move advanced topics to `references/advanced-topics.md`
- Move complete tables to `references/complete-tables.md`
- Keep SKILL.md concise, use progressive disclosure
- Validators will warn if >250 lines

---

## Examples

### Example 1: Creating a Technique Skill

**Scenario:** "I need a skill for calculating variance with favorability logic"

**Application:**

**Step 1:** Choose skill type → Technique (step-by-step how-to)

**Step 2:** Run generator:
```bash
python generate_skill.py
# Skill name: calculating-variance-with-favorability
# Skill type: technique
# Description: Use when calculating variance, comparing budget vs actual, need favorability analysis for revenue/expense accounts, or analyzing budget variance...
```

**Step 3:** Fill placeholders:
- `{{STEP_1_NAME}}`: Calculate Raw Variance
- `{{STEP_1_ACTION_1}}`: Subtract budget from actual
- `{{EXAMPLE_1_SCENARIO}}`: Revenue account variance

**Step 4:** Validate CSO → Score: 0.82 ✅

**Step 5:** Create references/favorability-rules.md (detailed rules)

**Step 6:** All validators pass ✅

**Result:** Skill auto-invokes when "calculating variance" mentioned.

### Example 2: Creating a Discipline Skill

**Scenario:** "I need a skill to enforce code review before deployment"

**Application:**

**Step 1:** Choose skill type → Discipline (workflow enforcement)

**Step 2:** Run generator (use discipline template)

**Step 3:** Fill placeholders + rationalization-proofing:
- Iron Law: `NO DEPLOYMENT WITHOUT CODE REVIEW FIRST`
- Explicit negations: Don't "skip review for hotfix", Don't "self-review", Don't "deploy first review later"
- Rationalization table: 10 entries (simplicity, urgency, trust, etc.)
- Red flags: 8 entries (thinking "it's a small change", feeling time pressure, etc.)

**Step 4:** Validate CSO → Include "before deploying", "thinking 'just a hotfix'", "under deadline"

**Step 5:** Create references/code-review-checklist.md

**Step 6:** Test with pressure scenarios → 0% bypass rate ✅

**Result:** Skill prevents deployment shortcuts under pressure.

---

## Progressive Disclosure

**For detailed information, see:**
- `references/cso-guide.md` - CSO optimization (4 pillars, examples, testing)
- `references/rationalization-proofing.md` - Discipline skill bulletproofing (5 techniques, iteration)
- `references/testing-protocol.md` - TDD for skills (RED-GREEN-REFACTOR, pressure scenarios)

**Templates:**
- `assets/templates/technique-template.md` - How-to guides (6 sections)
- `assets/templates/pattern-template.md` - Mental models (7 sections, before/after)
- `assets/templates/discipline-template.md` - Workflow enforcement (12 sections, rationalization-proofing)
- `assets/templates/reference-template.md` - Quick lookup (5 sections, tables)

**Validation scripts:**
- `scripts/validate_yaml.py` - YAML frontmatter syntax and CSO keyword count
- `scripts/validate_naming.py` - Active-voice naming conventions
- `scripts/validate_structure.py` - Required sections by skill type
- `scripts/validate_cso.py` - CSO score calculation (≥0.7 target)
- `scripts/validate_rationalization.py` - Discipline skill rationalization-proofing

**Orchestrator:**
- `scripts/generate_skill.py` - End-to-end skill generation with validation

**Related skills:**
- `creating-commands` - Create slash commands (future)
- `creating-agents` - Create subagents (future)
- `enforcing-research-plan-implement-verify` - Workflow discipline for all implementations
