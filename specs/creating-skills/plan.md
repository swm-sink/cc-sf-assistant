# Creating Skills Meta-Skill - Implementation Plan

**Date:** 2025-11-09
**Phase:** Plan (2 of 4)
**Status:** At CHECKPOINT 2 - awaiting user approval to proceed to Implementation

---

## Plan Overview

**Objective:** Create meta-skill that generates new skills with CSO optimization, proper structure, and comprehensive validation.

**Approach:** Build modular system with specialized templates, validation scripts, and guides - all bundled within creating-skills skill directory.

**Deliverables:**
- `.claude/skills/creating-skills/SKILL.md` - Main orchestration skill
- `.claude/skills/creating-skills/assets/templates/` - 4 specialized templates
- `.claude/skills/creating-skills/scripts/` - 5 validation scripts + orchestrator
- `.claude/skills/creating-skills/references/` - CSO guide, rationalization-proofing guide, testing protocol

---

## Part 1: Specialized Templates Design

### 1.1 Template Architecture

**Location:** `.claude/skills/creating-skills/assets/templates/`

**4 Template Types:**
1. **technique-template.md** - How-to guides (step-by-step instructions)
2. **pattern-template.md** - Mental models (before/after comparisons)
3. **discipline-template.md** - Workflow enforcement (Iron Law, Red Flags, rationalization table)
4. **reference-template.md** - API docs (tables, quick lookup)

**Why 4 types:** Different skill purposes need different structures. Technique skills focus on "how", Pattern skills on "when", Discipline on "must", Reference on "what".

### 1.2 Technique Template Structure

**File:** `technique-template.md`

**Purpose:** Step-by-step how-to guides (e.g., condition-based-waiting, git-worktrees)

**Structure (6 sections):**
```markdown
---
name: {skill-name}
description: Use when {specific triggers/symptoms} - {what it does, third person}
---

# {Skill Title}

## Overview
[One paragraph: what problem this solves, when to use it]

## When to Use
- Specific trigger 1
- Specific trigger 2
- Symptoms that indicate need

## Step-by-Step Instructions

### Step 1: {Action Name}
[Clear, actionable instruction]

### Step 2: {Action Name}
[Clear, actionable instruction]

### Step 3: {Action Name}
[Clear, actionable instruction]

## Common Pitfalls
- ❌ Pitfall 1
- ❌ Pitfall 2
- ✅ Instead do this

## Examples

### Example 1: {Use Case}
[Before/after or input/output]

### Example 2: {Use Case}
[Before/after or input/output]

## Progressive Disclosure
[References to detailed docs if needed]
```

**Target:** <200 lines, <500 words

### 1.3 Pattern Template Structure

**File:** `pattern-template.md`

**Purpose:** Mental models and when-to-use decisions (e.g., flatten-with-flags)

**Structure (7 sections):**
```markdown
---
name: {pattern-name}
description: Use when {decision point symptoms} - {what pattern provides, third person}
---

# {Pattern Name}

## Overview
[What is this pattern, when does it help]

## When to Apply This Pattern
- Signal 1 (e.g., "code becoming nested")
- Signal 2 (e.g., "hard to test")
- Decision point (e.g., "A vs B choice")

## The Pattern

### Before (Without Pattern)
[Show the problem]

### After (With Pattern)
[Show the solution]

## Benefits
- Benefit 1
- Benefit 2

## Trade-offs
- When NOT to use
- Costs of applying

## Examples

### Example 1: {Domain}
[Concrete before/after]

### Example 2: {Domain}
[Concrete before/after]

## Progressive Disclosure
[References if needed]
```

**Target:** <200 lines, <500 words

### 1.4 Discipline Template Structure

**File:** `discipline-template.md`

**Purpose:** Workflow enforcement, mandatory processes (e.g., TDD, workflow enforcement)

**Structure (12 sections - matches enforcing-research-plan-implement-verify):**
```markdown
---
name: {discipline-name}
description: Use when {about to violate symptoms} - {what it enforces, third person}
---

# {Discipline Name}

## Overview
[What this enforces, why it exists]

**Core principle:** {Foundational belief}

**Violating the letter of the rules is violating the spirit of the rules.**

## The Iron Law
```
{ABSOLUTE REQUIREMENT IN CAPS}
```

{Clear statement of requirement}

**No exceptions:**
- Don't {workaround 1}
- Don't {workaround 2}
- Don't {workaround 3}

{Command} means {Command}.

## When to Activate
**BEFORE:**
- Action 1
- Action 2

**Warning signs you're about to violate:**
- Thought 1
- Thought 2

**Exceptions (rare):**
- Exception 1
- Exception 2

## The Required Process
[Detailed workflow steps with checkpoints]

## Required Artifacts
[What must exist before proceeding]

## Commitment & Announcement
**Before starting, you MUST announce:**
"{Announcement template}"

**Why:** {Psychological principle}

## Red Flags - STOP and Follow Process
If you catch yourself thinking:
- "{Rationalization 1}"
- "{Rationalization 2}"
- "{Rationalization 3}"

**STOP. {Required action}. No exceptions.**

## Common Rationalizations
| Excuse | Reality |
|--------|---------|
| "{Excuse 1}" | {Reality check} |
| "{Excuse 2}" | {Reality check} |

## Verification Checklist
**Before proceeding:**
- [ ] Requirement 1
- [ ] Requirement 2

**Can't check all boxes? {Consequence}**

## Progressive Disclosure
[References to detailed guides]

## Integration with {Related Doc}
[How this fits with broader documentation]

## Final Rule
```
{Enforcement statement}
```

No exceptions without {authority}'s explicit permission.
```

**Target:** <250 lines (discipline skills can be longer), comprehensive rationalization-proofing

### 1.5 Reference Template Structure

**File:** `reference-template.md`

**Purpose:** API docs, command references, quick lookup tables

**Structure (5 sections):**
```markdown
---
name: {reference-name}
description: Use when {looking for information about X} - {what information provided, third person}
---

# {Reference Title}

## Overview
[What this documents, how to use this reference]

## Quick Reference

### Category 1
| Item | Description | Usage |
|------|-------------|-------|
| Item1 | Description | Example |

### Category 2
| Item | Description | Usage |
|------|-------------|-------|
| Item1 | Description | Example |

## Detailed Documentation

### Topic 1
[Detailed explanation]

### Topic 2
[Detailed explanation]

## Common Use Cases

### Use Case 1
[How to use reference for this case]

### Use Case 2
[How to use reference for this case]

## Progressive Disclosure
[Additional detailed docs if needed]
```

**Target:** Varies (can be longer for comprehensive references)

---

## Part 2: Validation Scripts Specification

### 2.1 Validation Architecture

**Location:** `.claude/skills/creating-skills/scripts/`

**5 Validators + 1 Orchestrator:**
1. `validate_yaml.py` - YAML syntax and structure
2. `validate_naming.py` - Active voice, kebab-case
3. `validate_structure.py` - Required sections by skill type
4. `validate_cso.py` - CSO keyword richness
5. `validate_rationalization.py` - Discipline skills: Iron Law, Red Flags, table
6. `generate_skill.py` - Orchestrator (calls all validators)

**Design Principles:**
- Each validator is independent (can run separately)
- Exit codes: 0=pass, 1=error, 2=warning
- JSON output for programmatic use
- Human-readable messages for CLI
- Atomic operations (validate before committing files)

### 2.2 validate_yaml.py Specification

**Purpose:** Validate YAML frontmatter syntax and format

**Inputs:**
- `skill_file_path` - Path to SKILL.md file

**Validations:**
1. YAML syntax valid (parseable)
2. Required fields present: `name`, `description`
3. Optional fields recognized: `version`, `author`, `tags`
4. Name format: lowercase, kebab-case, no special characters
5. Description format: Starts with "Use when", third person, <500 chars
6. Description not empty
7. Name not empty

**Output:**
```python
{
    "valid": bool,
    "errors": [
        {"type": "YAML_SYNTAX_ERROR", "message": "...", "line": int}
    ],
    "warnings": [
        {"type": "DESCRIPTION_LENGTH", "message": "...", "current": int, "max": 500}
    ]
}
```

**Exit codes:**
- 0: Valid
- 1: Errors (YAML syntax, required fields missing)
- 2: Warnings (description length, format suggestions)

**Example usage:**
```bash
python scripts/validate_yaml.py .claude/skills/my-skill/SKILL.md
```

### 2.3 validate_naming.py Specification

**Purpose:** Validate and suggest active-voice naming

**Inputs:**
- `name` - Skill name from YAML

**Validations:**
1. Kebab-case format (lowercase, hyphens)
2. Active voice detection (gerunds: -ing, action verbs)
3. Passive voice detection (nouns: -er, -or, -ator)
4. Suggestions for passive → active conversion

**Active voice patterns:**
- Gerunds: `creating-`, `analyzing-`, `enforcing-`, `testing-`
- Action verbs: `flatten-with-`, `condition-based-`
- Avoid: `-creator`, `-analyzer`, `-validator`, `-helper`

**Output:**
```python
{
    "valid": bool,
    "active_voice": bool,
    "suggestions": [
        {
            "current": "skill-creator",
            "suggested": "creating-skills",
            "reason": "Use gerund form for process-oriented skills"
        }
    ],
    "warnings": []
}
```

**Exit codes:**
- 0: Active voice
- 2: Passive voice (warning, not error)

### 2.4 validate_structure.py Specification

**Purpose:** Validate required sections by skill type

**Inputs:**
- `skill_file_path` - Path to SKILL.md
- `skill_type` - One of: technique, pattern, discipline, reference

**Required Sections by Type:**

**Technique:**
1. Overview
2. When to Use
3. Step-by-Step Instructions (or Instructions)
4. Common Pitfalls (or Anti-Patterns)
5. Examples
6. Progressive Disclosure

**Pattern:**
1. Overview
2. When to Apply This Pattern
3. The Pattern
4. Before (or Without Pattern)
5. After (or With Pattern)
6. Benefits
7. Trade-offs
8. Examples

**Discipline:**
1. Overview
2. The Iron Law
3. When to Activate
4. The Required Process (or workflow sections)
5. Red Flags
6. Common Rationalizations
7. Verification Checklist
8. Final Rule

**Reference:**
1. Overview
2. Quick Reference
3. Detailed Documentation
4. Common Use Cases

**Output:**
```python
{
    "valid": bool,
    "skill_type": str,
    "missing_sections": ["Red Flags", "Common Rationalizations"],
    "found_sections": ["Overview", "The Iron Law", ...],
    "line_count": int,
    "word_count": int,
    "warnings": [
        {"type": "LINE_COUNT_HIGH", "message": "227 lines > 200 target", "severity": "info"}
    ]
}
```

**Exit codes:**
- 0: All required sections present
- 1: Missing required sections
- 2: Line count warnings

### 2.5 validate_cso.py Specification

**Purpose:** Validate Claude Search Optimization (CSO) quality

**Inputs:**
- `description` - YAML description field

**CSO Quality Metrics:**
1. **Triggers present:** "Use when", "before", "when thinking", "when tempted"
2. **Symptoms/signals:** Error messages, situations, tools mentioned
3. **Keywords:** Technology-agnostic unless skill is tech-specific
4. **Specificity:** Concrete vs vague language
5. **Keyword richness:** Count of searchable keywords (target ≥3)

**Keyword extraction:**
- Extract nouns, verbs, specific phrases
- Technology names (if tech-specific)
- Symptoms (e.g., "race conditions", "timing dependencies")
- Actions (e.g., "implementing", "testing", "debugging")

**Output:**
```python
{
    "valid": bool,
    "cso_score": float,  # 0.0 to 1.0
    "keyword_count": int,
    "has_trigger_phrase": bool,  # Starts with "Use when"
    "keywords_found": ["implementing", "features", "time pressure"],
    "suggestions": [
        "Add more symptom keywords (e.g., error messages, situations)"
    ],
    "warnings": []
}
```

**CSO Score Calculation:**
- Trigger phrase present: +0.3
- Keyword count ≥3: +0.3
- Keyword count ≥5: +0.2
- Specificity (concrete examples): +0.2

**Exit codes:**
- 0: CSO score ≥0.7
- 2: CSO score <0.7 (warning)

### 2.6 validate_rationalization.py Specification

**Purpose:** Validate discipline skills have rationalization-proofing

**Inputs:**
- `skill_file_path` - Path to SKILL.md
- Only runs if skill_type=discipline

**Validations:**
1. **Iron Law present:** Section titled "The Iron Law" or "Iron Law"
2. **Iron Law has absolute language:** Contains "NO", "MUST", "NEVER", or caps requirement
3. **Red Flags section present**
4. **Red Flags has entries:** At least 3 warning signs
5. **Rationalization table present:** Table with "Excuse" and "Reality" columns
6. **Rationalization table has entries:** At least 3 rows
7. **Explicit negations:** "Don't", "No exceptions", "means" statements
8. **Foundational principle:** "Violating letter is violating spirit" or similar

**Output:**
```python
{
    "valid": bool,
    "errors": [],
    "warnings": [],
    "found": {
        "iron_law": bool,
        "iron_law_absolute": bool,
        "red_flags": bool,
        "red_flags_count": int,
        "rationalization_table": bool,
        "rationalization_count": int,
        "explicit_negations": int,
        "foundational_principle": bool
    },
    "suggestions": []
}
```

**Exit codes:**
- 0: All rationalization-proofing elements present
- 1: Missing Iron Law or Red Flags
- 2: Weak rationalization-proofing (table too small, no negations)

### 2.7 generate_skill.py Orchestrator

**Purpose:** End-to-end skill generation with validation

**Workflow:**
1. **Prompt for skill details:**
   - Skill name (suggest active voice)
   - Skill type (technique/pattern/discipline/reference)
   - Description (validate CSO)
   - Purpose/overview

2. **Load appropriate template:**
   - Read from `assets/templates/{type}-template.md`
   - Substitute placeholders

3. **Create skill in temp directory:**
   - Generate SKILL.md
   - Create directory structure

4. **Run all validators:**
   - validate_yaml.py
   - validate_naming.py
   - validate_structure.py
   - validate_cso.py
   - validate_rationalization.py (if discipline)

5. **Report validation results:**
   - Show errors, warnings
   - Ask user to fix or proceed

6. **Atomic commit:**
   - If valid, move from temp to `.claude/skills/{name}/`
   - If invalid, show errors, don't create

7. **Output:**
   - Created file path
   - Validation summary
   - Next steps (references to add, testing to do)

**Command-line interface:**
```bash
python scripts/generate_skill.py

# Prompts:
# Skill name: analyzing-variance
# Skill type (technique/pattern/discipline/reference): technique
# Description: Use when calculating budget vs actual variance...
# ...

# Output:
# ✅ Generated .claude/skills/analyzing-variance/SKILL.md
# ✅ All validations passed
#
# Next steps:
# - Add examples to SKILL.md
# - Create references/ if needed
# - Test skill with sample scenario
```

---

## Part 3: Supporting Guides

### 3.1 CSO Guide (references/cso-guide.md)

**Purpose:** Comprehensive guide to Claude Search Optimization

**Content:**
1. **What is CSO:** How Claude discovers skills via keyword matching
2. **4 Pillars of CSO:**
   - Trigger phrases ("Use when", "before", "when thinking")
   - Symptom keywords (error messages, situations)
   - Technology-agnostic keywords (unless tech-specific)
   - Specific examples (concrete > vague)
3. **Description formula:** "Use when [triggers/symptoms] - [what it does, third person]"
4. **Keyword richness:** Target ≥3 searchable keywords, ≥5 ideal
5. **Examples:**
   - ✅ Good: "Use when tests have race conditions, timing dependencies, or pass/fail inconsistently - replaces arbitrary timeouts with condition polling"
   - ❌ Bad: "For async testing"
6. **Testing CSO:** How to test if description triggers on relevant queries
7. **Common mistakes:** Too vague, too tech-specific, missing triggers

**Target:** ~300-400 lines comprehensive guide

### 3.2 Rationalization-Proofing Guide (references/rationalization-proofing.md)

**Purpose:** How to make discipline skills bulletproof against shortcuts

**Content:**
1. **Why rationalization-proofing:** Discipline skills resist rationalization under pressure
2. **5 Techniques:**
   - Close every loophole explicitly (specific negations)
   - Address "spirit vs letter" arguments (foundational principle)
   - Build rationalization table (Excuse | Reality)
   - Create red flags list (self-checking)
   - Update CSO for violation symptoms
3. **Examples from TDD skill and enforcing-workflow skill**
4. **Testing discipline skills:** Pressure scenarios, RED-GREEN-REFACTOR
5. **Iterating to bulletproof:** How to find and close loopholes

**Target:** ~400-500 lines comprehensive guide

### 3.3 Testing Protocol (references/testing-protocol.md)

**Purpose:** How to test skills before deployment

**Content:**
1. **TDD for skills:** RED-GREEN-REFACTOR applied to process documentation
2. **Skill types and testing:**
   - Discipline: MUST test with pressure scenarios
   - Technique: SHOULD test with application scenarios
   - Pattern: SHOULD test with recognition scenarios
   - Reference: Test with retrieval scenarios
3. **Creating pressure scenarios:** 3+ combined pressures (time, authority, sunk cost, etc.)
4. **Baseline testing:** Run WITHOUT skill, document failures
5. **Validation testing:** Run WITH skill, verify compliance
6. **Iteration:** Close loopholes until bulletproof
7. **Success criteria:** Agent follows rules under maximum pressure

**Target:** ~300-400 lines

---

## Part 4: creating-skills SKILL.md Structure

### 4.1 Skill Type

**Type:** Technique skill (how-to guide for skill generation)

**Why technique:** Orchestrates step-by-step process, not enforcing discipline

### 4.2 Sections (6 sections per technique template)

```markdown
---
name: creating-skills
description: Use when creating new Claude Code skills, need skill templates, or want CSO-optimized descriptions - generates skills with proper structure, validation, and testing protocols
---

# Creating Skills

## Overview
Generate new skills with proper structure, CSO optimization, and comprehensive validation.

Uses specialized templates (technique/pattern/discipline/reference), validates structure, enforces active-voice naming, and ensures CSO discoverability.

## When to Use
- Creating new skill from scratch
- Need template for specific skill type
- Want CSO-optimized description
- Generating skill with validation
- Unsure which skill type to use

## Step-by-Step Instructions

### Step 1: Choose Skill Type
[Guide to choosing technique/pattern/discipline/reference]

### Step 2: Generate Skill
[How to use generate_skill.py orchestrator]

### Step 3: Customize Content
[Fill in examples, details, references]

### Step 4: Validate
[Run validators, fix errors/warnings]

### Step 5: Test (If Discipline)
[Create pressure scenarios, run RED-GREEN-REFACTOR]

### Step 6: Deploy
[Commit skill, document in project]

## Common Pitfalls
- ❌ Using passive voice names (skill-creator vs creating-skills)
- ❌ Vague CSO descriptions (missing trigger phrases, keywords)
- ❌ Missing required sections for skill type
- ❌ Skipping validation (discipline skills especially)
- ❌ Not testing discipline skills before deployment
- ✅ Use specialized templates, validate thoroughly, test discipline skills

## Examples

### Example 1: Creating Technique Skill
[Step-by-step example of generating technique skill]

### Example 2: Creating Discipline Skill
[Step-by-step example with rationalization-proofing]

## Progressive Disclosure
**Templates:** `assets/templates/{type}-template.md`
**Validation:** `scripts/validate_*.py`
**Guides:**
- `references/cso-guide.md` - CSO optimization comprehensive guide
- `references/rationalization-proofing.md` - Bulletproofing discipline skills
- `references/testing-protocol.md` - Testing skills before deployment
```

**Target:** <200 lines

---

## Part 5: Implementation Steps

### 5.1 Phase 3: Implementation Order

**Step 1: Create specialized templates (2 hours)**
1. Create `assets/templates/technique-template.md`
2. Create `assets/templates/pattern-template.md`
3. Create `assets/templates/discipline-template.md`
4. Create `assets/templates/reference-template.md`
5. Test templates by manually generating test skill

**Step 2: Create validation scripts (3 hours)**
1. Create `scripts/validate_yaml.py`
2. Create `scripts/validate_naming.py`
3. Create `scripts/validate_structure.py`
4. Create `scripts/validate_cso.py`
5. Create `scripts/validate_rationalization.py`
6. Test each validator independently

**Step 3: Create orchestrator (1.5 hours)**
1. Create `scripts/generate_skill.py`
2. Integrate all validators
3. Test end-to-end skill generation

**Step 4: Create supporting guides (2 hours)**
1. Create `references/cso-guide.md`
2. Create `references/rationalization-proofing.md`
3. Create `references/testing-protocol.md`

**Step 5: Create creating-skills SKILL.md (1 hour)**
1. Write SKILL.md using technique template
2. Document all steps
3. Add examples

**Step 6: Test meta-skill itself (1.5 hours)**
1. Use creating-skills to generate test skill
2. Validate generated skill
3. Iterate on templates/validators based on testing
4. Verify end-to-end workflow

**Total estimated time:** 11 hours

### 5.2 Validation Approach

**Validators must validate themselves:**
- Use validate_yaml.py to validate template YAML
- Use validate_structure.py to check template sections
- Use validate_cso.py to score template descriptions

**Testing protocol:**
1. Generate test skill using each template
2. Run all validators on generated skills
3. Fix any issues in templates or validators
4. Repeat until all validations pass

---

## Part 6: Success Criteria

### 6.1 Templates Success Criteria

- ✅ 4 specialized templates created (technique/pattern/discipline/reference)
- ✅ Each template has appropriate structure (6-12 sections)
- ✅ Templates have placeholder syntax documented
- ✅ Templates validate against their own validators
- ✅ Can generate working skills from each template

### 6.2 Validation Success Criteria

- ✅ 5 validators + 1 orchestrator created
- ✅ Each validator runs independently (can be used separately)
- ✅ JSON output for programmatic use
- ✅ Human-readable CLI output
- ✅ Exit codes correct (0=pass, 1=error, 2=warning)
- ✅ Validators catch common mistakes (tested with bad inputs)

### 6.3 Guides Success Criteria

- ✅ CSO guide comprehensive (300-400 lines)
- ✅ Rationalization-proofing guide complete (400-500 lines)
- ✅ Testing protocol documented (300-400 lines)
- ✅ Examples included in all guides
- ✅ References to external research cited

### 6.4 creating-skills SKILL.md Success Criteria

- ✅ Uses technique template structure
- ✅ <200 lines
- ✅ CSO-optimized description (score ≥0.7)
- ✅ Active-voice name (creating-skills)
- ✅ Step-by-step instructions clear
- ✅ Examples included
- ✅ All validators pass on SKILL.md itself

### 6.5 End-to-End Success Criteria

- ✅ Can generate skill using generate_skill.py
- ✅ Generated skill validates successfully
- ✅ Generated skill has proper structure
- ✅ Generated skill has CSO-optimized description
- ✅ Can use creating-skills to create new skills

---

## Part 7: Open Questions & Decisions

### 7.1 Existing Skill Renaming

**Question:** Rename existing skills as part of this work or separate task?

**Current skills with passive names:**
- `variance-analyzer` → should be `analyzing-variance`
- `financial-validator` → should be `validating-financial-data`

**Options:**
A) Rename as part of creating-skills implementation (holistic cleanup)
B) Defer renaming to separate task (focused scope)
C) Generate rename script, let user decide when to run

**Recommendation:** Option C - Generate `scripts/rename_skill.py` utility, document renaming recommendations, let user decide timing.

### 7.2 Validation Strictness

**Question:** How strict should validators be?

**Options:**
A) Strict: Errors for naming, CSO score, line count
B) Moderate: Errors for structure, warnings for naming/CSO
C) Lenient: Warnings for everything except YAML syntax

**Recommendation:** Option B - Errors for structural issues (missing sections, YAML errors), warnings for quality issues (naming, CSO, line count). Allow user to proceed with warnings.

### 7.3 Testing Requirements

**Question:** Which skill types MUST be tested before deployment?

**Options:**
A) All skills must be tested
B) Only discipline skills must be tested
C) Testing recommended but not required

**Recommendation:** Option B - MUST test discipline skills (too risky without testing), SHOULD test others (recommended in guide but not enforced).

### 7.4 Template Versioning

**Question:** How to handle template updates over time?

**Options:**
A) Version templates (technique-template-v1.md)
B) Update templates in place, document changes
C) No versioning, always use latest

**Recommendation:** Option B - Update in place, document changes in template comments, regenerate skills as needed. Keep simple.

---

## Part 8: Risk Analysis

### 8.1 Risks

**Risk 1: Template complexity**
- Concern: 4 templates might confuse users
- Mitigation: generate_skill.py prompts for type, suggests based on description
- Status: Mitigated

**Risk 2: Validator false positives**
- Concern: Validators flag valid skills as invalid
- Mitigation: Warnings vs errors, clear messages, override flag
- Status: Mitigated

**Risk 3: Generated skills too generic**
- Concern: Templates produce cookie-cutter skills
- Mitigation: Templates are starting points, guide emphasizes customization
- Status: Acceptable

**Risk 4: CSO validation too subjective**
- Concern: CSO score calculation might be arbitrary
- Mitigation: Clear scoring rubric, examples, user can override
- Status: Mitigated

### 8.2 Dependencies

**External dependencies:**
- Python 3.11+ (already required)
- PyYAML (for YAML parsing)
- No new dependencies needed

**Internal dependencies:**
- Templates must exist before orchestrator can use them
- Validators must work before orchestrator can call them
- Guides referenced by SKILL.md must exist

**Mitigation:** Build in order (templates → validators → orchestrator → guides → SKILL.md)

---

## Part 9: Timeline & Milestones

**Phase 1: Research** ✅ COMPLETE (1582 lines, approved)

**Phase 2: Plan** 🔄 IN PROGRESS (this document, awaiting CHECKPOINT 2)

**Phase 3: Implementation** ⏳ PENDING (after CHECKPOINT 2 approval)
- Templates: 2 hours
- Validators: 3 hours
- Orchestrator: 1.5 hours
- Guides: 2 hours
- SKILL.md: 1 hour
- Testing: 1.5 hours
- **Total: 11 hours**

**Phase 4: Verification** ⏳ PENDING (after CHECKPOINT 3 approval)
- Validate all templates
- Test all validators
- End-to-end testing
- Documentation review
- **Total: 2 hours**

**Overall estimate:** 13 hours from CHECKPOINT 2 approval to completion

---

## CHECKPOINT 2: User Approval Required

**Please review and approve:**

1. **4 Specialized templates approach** (technique/pattern/discipline/reference)
2. **5 Validation scripts + orchestrator** (modular, JSON output, exit codes)
3. **Supporting guides structure** (CSO, rationalization-proofing, testing protocol)
4. **creating-skills SKILL.md** (technique type, 6 sections, <200 lines)
5. **Implementation order** (templates → validators → orchestrator → guides → SKILL.md)
6. **Open question decisions:**
   - Generate rename utility (don't force rename now)
   - Moderate validation strictness (errors for structure, warnings for quality)
   - MUST test discipline skills, SHOULD test others
   - Update templates in place (no versioning)
7. **Timeline estimate** (11 hours implementation, 2 hours verification)

**Questions:**
- Approve overall plan?
- Any adjustments needed?
- Proceed to Implementation phase?

**User, please approve or request revisions.**

---

**Planning Sources:**
- Research findings: `specs/creating-skills/research.md`
- External patterns: `external/superpowers/skills/writing-skills/SKILL.md`
- Existing skill examples: `enforcing-research-plan-implement-verify`, `variance-analyzer`, `financial-validator`
- Workflow template: `.claude/templates/workflows/RESEARCH_PLAN_IMPLEMENT_VERIFY.md`

**Plan created:** 2025-11-09
**Phase:** Plan (2 of 4)
**Next Phase:** Implementation (awaiting CHECKPOINT 2 approval)
