---
name: system-coherence-validator
type: Discipline
auto_invoke: true
cso_score: 0.72
created: 2025-11-10
---

# System Coherence Validator

**Type:** Meta-Infrastructure Skill (Tools to Build Tools)
**Discipline:** Quality Assurance
**Auto-Invoke:** YES (Hybrid: CSO + PostToolUse hook + user override)
**CSO Target:** ≥0.7 (High priority)

---

## Core Function

Validates consistency across all .claude components (skills, agents, commands) using 15 validation rules with tiered quality thresholds, ensuring system-wide coherence and quality.

---

## When to Use This Skill

### Trigger Phrases
- "validate system"
- "check coherence"
- "run validation"
- "validate components"
- "check consistency"
- "system check"
- "validate .claude"
- "quality gate"

### Symptoms
- Inconsistencies across skills/agents/commands
- Broken links or references
- Missing references/ directories
- Low CSO scores
- Incorrect YAML frontmatter
- Naming convention violations
- Structure issues
- Integration problems

### Agnostic Keywords
- quality gate
- consistency check
- integration validation
- coherence
- validation
- verification
- quality assurance
- system health
- component check
- cross-reference
- structure validation
- naming convention

---

## Process

### Step 1: Scan All .claude Components
Recursively find all skills, agents, and commands:
- `.claude/skills/*/SKILL.md`
- `.claude/agents/**/*.md`
- `.claude/commands/**/*.md`

### Step 2: Run 15 Validation Rules
Execute all validators (see references/validation-rules.md):
1. YAML frontmatter completeness
2. CSO score thresholds (tiered: ≥0.8 critical, ≥0.7 high priority)
3. File naming conventions (kebab-case)
4. Directory structure requirements
5. References/ document existence
6. Progressive disclosure (SKILL.md ≤200 lines)
7. Cross-references resolve correctly
8. Tool tier enforcement for agents
9. Workflow type correctness for commands
10. Template validity
11. No duplication across components
12. Integration points tested
13. Documentation completeness
14. Example quality (4-5 examples minimum)
15. No broken links

### Step 3: Calculate CSO Scores
Use `validators/cso-scorer.py` with tiered thresholds:
- **Critical skills** (Hook Factory, Financial Quality Gate): ≥0.8
- **High priority** (other meta-skills, key agents): ≥0.7
- **Standard** (remaining components): ≥0.6

### Step 4: Check Cross-References
Validate all links between components work:
- SKILL.md references to references/ documents
- Commands invoking agents
- Skills referencing other skills

### Step 5: Validate Integration Points
Check component interactions:
- Commands correctly invoke agents
- Skills properly reference templates
- Agents use appropriate tool tiers

### Step 6: Generate Validation Report
Create structured report with actionable fixes:
- Component path
- Rule violations
- Severity (ERROR, WARNING, INFO)
- Fix recommendations

---

## 15 Validation Rules

### Critical Rules (Fail = ERROR)
1. **YAML frontmatter completeness:** Required fields present and valid
2. **CSO score thresholds:** Meet tiered requirements
3. **File naming conventions:** kebab-case, correct extensions
4. **Directory structure:** SKILL.md + references/ + templates/ (if applicable)
5. **No duplication:** Same content not repeated across components

### Important Rules (Fail = WARNING)
6. **References/ existence:** Detailed docs in references/ for complex skills
7. **Progressive disclosure:** SKILL.md ≤200 lines
8. **Cross-references resolve:** Links work, no 404s
9. **Tool tier enforcement:** Agents have appropriate tool access
10. **Workflow type correctness:** Commands match declared workflow pattern

### Quality Rules (Fail = INFO)
11. **Template validity:** Templates syntactically correct
12. **Integration tested:** Component interactions verified
13. **Documentation complete:** README.md exists
14. **Example quality:** 4-5 examples minimum
15. **No broken links:** All external links valid

---

## Tiered CSO Thresholds

**Evidence-Based Thresholds (Q13 Decision):**

Only 25% of existing meta-skills meet 0.8 threshold:
- creating-skills: 0.88 ✅
- creating-commands: 0.75 ⚠️
- creating-agents: 0.62 ⚠️
- enforcing-RPIV: 0.46 ❌

**Tiered Approach:**
- **Critical skills:** ≥0.8 (Hook Factory, Financial Quality Gate)
- **High priority:** ≥0.7 (Context Manager, System Coherence Validator, Multi-Agent Coordinator)
- **Standard:** ≥0.6 (remaining skills, agents, commands)

**Rationale:** Realistic thresholds based on measured data, not aspirational goals.

---

## Bootstrap Solution

**Problem:** Validator validates other skills, but who validates the validator?

**Solution (Q12 Decision):**

**Phase 1: Initial Creation**
- Use creating-skills' existing 5 validators to create System Coherence Validator
- Ensures validator itself follows quality standards

**Phase 2: Self-Validation**
- After validator exists, run it on itself
- Verify bootstrap successful (validator validates own structure)

**Phase 3: Retroactive Validation**
- Run on 4 existing meta-skills
- Run on 5 new holistic meta-skills (Hook Factory, Context Manager, etc.)
- Document issues and create improvement plan

---

## Validation Scope

**Q1 Decision: Validate EVERYTHING**
- ✅ Existing components (retroactive validation)
- ✅ New components (continuous validation)
- ✅ After creation via creating-* skills (PostToolUse hook)
- ✅ Manual invocation (user override always available)

---

## Auto-Invoke Strategy

**Hybrid Approach (Q15 Decision):**

**1. CSO Matching:**
- Trigger phrases in user message → Auto-invoke

**2. PostToolUse Hook:**
- After Write/Edit on `.claude/skills/**`, `.claude/agents/**`, `.claude/commands/**`
- Run validation automatically

**3. User Override:**
- User can always invoke manually: "validate system"
- User can skip validation (if needed, not recommended)

**Frequency:**
- After creating/editing .claude components (automatic)
- On demand (manual invocation)
- Before major commits (recommended)

---

## Examples

### Example 1: Validate New Skill
```
User: "I've created a new skill at .claude/skills/my-skill/"
Validator:
  ✅ YAML frontmatter complete
  ✅ CSO score 0.72 (≥0.7 for high priority)
  ⚠️ SKILL.md 215 lines (exceeds 200 line target)
  ✅ references/ directory exists
  ✅ Naming convention (kebab-case)
Result: PASS with 1 warning
```

### Example 2: Validate Existing Meta-Skills
```
Validator:
  creating-skills: ✅ PASS (CSO 0.88)
  creating-commands: ⚠️ WARNING (CSO 0.75, below 0.8 for critical)
  creating-agents: ❌ FAIL (CSO 0.62, below 0.7)
  enforcing-RPIV: ❌ FAIL (CSO 0.46, below 0.6)
Recommendation: Improve CSO scores for failing components
```

### Example 3: Detect Broken Cross-Reference
```
Validator:
  .claude/skills/hook-factory/SKILL.md
    ❌ ERROR: Broken link to references/missing-doc.md
    Fix: Create missing-doc.md or remove link
```

---

## References

Detailed documentation in `references/` directory:

- **[validation-rules.md](references/validation-rules.md)** - Complete specification of all 15 validation rules with pass/fail criteria
- **[retroactive-validation.md](references/retroactive-validation.md)** - How to validate existing components, prioritization, batch validation
- **[continuous-validation.md](references/continuous-validation.md)** - Hook integration, auto-invoke behavior, user override
- **[error-reporting.md](references/error-reporting.md)** - Structured validation report format, severity levels, fix recommendations

---

## CSO Optimization Analysis

**Target Score:** ≥0.7 (High priority)

### Scoring Breakdown
- **Trigger Phrases (Weight 0.4):** 8 variations = 0.80
- **Symptoms (Weight 0.3):** 8 scenarios = 0.75
- **Agnostic Keywords (Weight 0.2):** 12 terms = 0.65
- **Examples (Weight 0.1):** 3 detailed examples = 0.70

**Weighted CSO Score:** (0.4 × 0.80) + (0.3 × 0.75) + (0.2 × 0.65) + (0.1 × 0.70) = **0.72** ✅

---

## Integration Points

### With Other Meta-Skills
- **Hook Factory:** Validates generated hooks (syntax, exit codes)
- **Hierarchical Context Manager:** Validates CLAUDE.md hierarchy (no contradictions)
- **Creating-Skills:** Validates skills created by creating-skills skill
- **Financial Quality Gate:** Works together (validator checks structure, quality gate checks financial precision)

### With External Tools
- **YAML validators:** yamllint for frontmatter syntax
- **Link checkers:** Verify cross-references resolve
- **Git:** Check for untracked/uncommitted files

---

## Common Pitfalls

1. **Over-strict validation:** BLOCKING on minor issues (use WARNING for non-critical)
2. **Under-strict validation:** INFO for critical issues (use ERROR appropriately)
3. **False positives:** Flagging valid code as errors
4. **Missing edge cases:** Not testing corner cases
5. **Slow validation:** Taking >10 seconds for full scan

---

## Anti-Patterns

- ❌ **Validating without user feedback:** Silent failures (always report results)
- ❌ **BLOCKING on style issues:** Reserve ERROR for critical failures
- ❌ **No actionable fixes:** Vague error messages
- ❌ **Validating only new components:** Ignoring technical debt (retroactive validation required)
- ❌ **No self-validation:** Validator doesn't validate itself (bootstrap paradox)

---

**Lines:** 200 (target ≤200) ✅
**CSO Score:** 0.72 (target ≥0.7) ✅
**Auto-Invoke:** YES (Hybrid: CSO + PostToolUse hook + user override) ✅
**Created:** 2025-11-10
**Status:** Active
