# CLAUDE.md Migration Strategy Reference

**Purpose:** Decision framework and checklist for migrating root CLAUDE.md to hierarchical structure.

**Target Audience:** Developers performing CLAUDE.md migration

---

## Migration Overview

### Before Migration
```
/CLAUDE.md (single large file)
  ├─ Anti-hallucination protocol
  ├─ RPIV workflow
  ├─ Financial precision rules
  ├─ Type safety enforcement
  ├─ CSO optimization rules
  ├─ Testing requirements
  └─ ... (everything in one file)
```

### After Migration
```
/CLAUDE.md (orchestration layer only)
  ├─ Anti-hallucination protocol
  ├─ RPIV workflow
  ├─ Meta-infrastructure first
  └─ Cross-cutting concerns

scripts/CLAUDE.md (Python-specific)
  ├─ Type safety enforcement
  ├─ Decimal precision
  └─ Audit trail logging

.claude/CLAUDE.md (meta-infrastructure)
  ├─ CSO optimization rules
  ├─ Progressive disclosure
  └─ YAML frontmatter validation

tests/CLAUDE.md (testing-specific)
  ├─ Edge case requirements
  ├─ Financial precision tests
  └─ Regression test patterns
```

---

## Decision Tree: What Goes Where?

### Step 1: Identify Section Type

**Cross-Cutting Concerns (Root CLAUDE.md):**
- Anti-hallucination protocol
- DRY principle
- Chain of verification
- Critical thought partnership
- Conciseness requirements
- Meta-infrastructure first principle
- RPIV workflow enforcement
- Response format requirements
- Tool usage policy

**Component-Specific (Subdirectory CLAUDE.md):**
- Type safety rules → scripts/CLAUDE.md
- CSO optimization details → .claude/CLAUDE.md
- Edge case test requirements → tests/CLAUDE.md
- Specific implementation patterns → relevant subdirectory

### Step 2: Apply Decision Criteria

**Question 1: Does this apply to ALL work, or just specific components?**
- All work → Root CLAUDE.md
- Specific component → Subdirectory CLAUDE.md

**Question 2: Is this a behavioral principle or implementation detail?**
- Behavioral principle (how to think) → Root CLAUDE.md
- Implementation detail (what to do) → Subdirectory CLAUDE.md

**Question 3: Does this change frequently?**
- Rarely changes → Root CLAUDE.md (stable baseline)
- Changes with component evolution → Subdirectory CLAUDE.md (easier to update)

### Step 3: Examples

| Section | Root or Subdirectory? | Rationale |
|---------|----------------------|-----------|
| "Be concise (1-3 sentences)" | Root | Applies to all work |
| "Use Decimal for currency" | scripts/ | Specific to Python financial code |
| "CSO score ≥0.8 for critical skills" | .claude/ | Specific to meta-infrastructure |
| "Test edge cases for zero division" | tests/ | Specific to testing |
| "Chain of verification" | Root | Applies to all responses |
| "Type hints on all functions" | scripts/ | Specific to Python code |

---

## Migration Checklist

### Phase 1: Analyze Current CLAUDE.md

- [ ] Read entire root CLAUDE.md
- [ ] Identify all major sections
- [ ] Categorize each section (cross-cutting vs component-specific)
- [ ] Measure current size (characters, lines, estimated tokens)
- [ ] Document sections to migrate

### Phase 2: Create Root CLAUDE.md (Orchestration Layer)

- [ ] Use `templates/root-claude.md.template` as starting point
- [ ] Keep cross-cutting concerns:
  - [ ] DRY principle
  - [ ] Chain of verification
  - [ ] Critical thought partnership
  - [ ] Conciseness requirements
  - [ ] Meta-infrastructure first principle
  - [ ] RPIV workflow
  - [ ] Response format requirements
  - [ ] Tool usage policy
- [ ] Remove component-specific sections (will move to subdirectories)
- [ ] Add note at bottom: "Component-Specific Overrides: See subdirectory CLAUDE.md files"
- [ ] Verify conciseness (target ≤600 lines)

### Phase 3: Create scripts/CLAUDE.md

- [ ] Use `templates/scripts-claude.md.template` as starting point
- [ ] Customize for project-specific needs:
  - [ ] Type safety rules (mypy, type hints)
  - [ ] Decimal precision enforcement
  - [ ] Audit trail logging patterns
  - [ ] Error handling patterns
  - [ ] Performance considerations
- [ ] Include inheritance note: "Inherits: Root CLAUDE.md"
- [ ] Include precedence note: "Precedence: This config overrides root for scripts/**"
- [ ] Test with sample Python script scenarios

### Phase 4: Create .claude/CLAUDE.md

- [ ] Use `templates/claude-dir-claude.md.template` as starting point
- [ ] Customize for project-specific needs:
  - [ ] CSO score targets (critical ≥0.8, high priority ≥0.7)
  - [ ] Progressive disclosure requirements
  - [ ] YAML frontmatter specifications
  - [ ] Tool tier enforcement rules
  - [ ] Workflow pattern descriptions
- [ ] Include inheritance note
- [ ] Include precedence note
- [ ] Test with sample skill/agent/command scenarios

### Phase 5: Create tests/CLAUDE.md

- [ ] Use `templates/tests-claude.md.template` as starting point
- [ ] Customize for project-specific needs:
  - [ ] Edge case requirements
  - [ ] Financial precision test patterns
  - [ ] Regression test expectations
  - [ ] Test fixture organization
  - [ ] Coverage targets
- [ ] Include inheritance note
- [ ] Include precedence note
- [ ] Test with sample test scenarios

### Phase 6: Validate Migration

- [ ] Check for duplication (same content in multiple CLAUDE.md files)
- [ ] Check for contradictions (root says X, subdirectory says NOT X)
- [ ] Verify no gaps (all original content accounted for)
- [ ] Test cascading precedence (most nested wins)
- [ ] Measure token reduction (before vs after)

### Phase 7: Document Changes

- [ ] Update plan.md with migration completion
- [ ] Document token reduction achieved
- [ ] Note any deviations from templates
- [ ] Create migration completion report

---

## Before/After Comparison

### Example Project Migration

**Before Migration:**
```
/CLAUDE.md
├─ Lines: 2,000
├─ Characters: 8,000
├─ Tokens (estimated): ~2,000
└─ Sections: 15 major sections (all mixed together)
```

**After Migration:**
```
/CLAUDE.md
├─ Lines: 600
├─ Characters: 2,400
├─ Tokens (estimated): ~600

scripts/CLAUDE.md
├─ Lines: 150
├─ Characters: 600
├─ Tokens (estimated): ~150

.claude/CLAUDE.md
├─ Lines: 150
├─ Characters: 600
├─ Tokens (estimated): ~150

tests/CLAUDE.md
├─ Lines: 100
├─ Characters: 400
├─ Tokens (estimated): ~100

Total:
├─ Lines: 1,000 (50% reduction in lines)
├─ Characters: 4,000 (50% reduction in chars)
├─ Tokens (total): ~1,000
└─ Tokens (per context): ~750 (root + one subdirectory)

Effective Reduction: 2,000 → 750 = 62.5% per context ✅
```

---

## Content Mapping Table

| Original Section | New Location | Notes |
|-----------------|--------------|-------|
| DRY Principle | Root | Cross-cutting |
| Chain of Verification | Root | Cross-cutting |
| Conciseness | Root | Cross-cutting |
| Meta-Infrastructure First | Root | Cross-cutting |
| RPIV Workflow | Root | Cross-cutting |
| Type Safety | scripts/CLAUDE.md | Python-specific |
| Decimal Precision | scripts/CLAUDE.md | Financial code specific |
| Audit Logging | scripts/CLAUDE.md | Script-specific |
| CSO Optimization | .claude/CLAUDE.md | Meta-infrastructure specific |
| Progressive Disclosure | .claude/CLAUDE.md | Meta-infrastructure specific |
| YAML Frontmatter | .claude/CLAUDE.md | Meta-infrastructure specific |
| Tool Tier Enforcement | .claude/CLAUDE.md | Agent-specific |
| Edge Case Testing | tests/CLAUDE.md | Testing-specific |
| Financial Precision Tests | tests/CLAUDE.md | Testing-specific |
| Test Fixtures | tests/CLAUDE.md | Testing-specific |

---

## Common Migration Challenges

### Challenge 1: Overlapping Sections
**Problem:** Section applies to multiple components (e.g., "Use Decimal for currency" relevant to scripts/ and tests/)

**Solution:**
- Root CLAUDE.md: State principle ("Financial calculations use Decimal")
- scripts/CLAUDE.md: Implementation details ("from decimal import Decimal, ROUND_HALF_UP")
- tests/CLAUDE.md: Testing requirements ("Assert Decimal equality, not float")

### Challenge 2: Too Much in Root
**Problem:** Trying to keep everything in root "just in case"

**Solution:**
- Be aggressive with migration (trust cascading precedence)
- Component-specific details ALWAYS go to subdirectory
- Root keeps only cross-cutting concerns

### Challenge 3: Not Measuring Token Reduction
**Problem:** Assuming migration worked without calculating

**Solution:**
- Measure before: `wc -m /CLAUDE.md`
- Measure after: `wc -m /CLAUDE.md scripts/CLAUDE.md .claude/CLAUDE.md tests/CLAUDE.md`
- Calculate effective per-context (root + largest subdirectory)
- Document reduction percentage

### Challenge 4: Forgetting to Remove from Root
**Problem:** Copying content to subdirectory but leaving in root (duplication)

**Solution:**
- After copying section to subdirectory, DELETE from root
- Use grep to check for duplication: `grep -r "specific phrase" CLAUDE.md scripts/CLAUDE.md`

### Challenge 5: Contradictions
**Problem:** Root says X, subdirectory says NOT X (unclear precedence)

**Solution:**
- Make precedence explicit in subdirectory: "This overrides root CLAUDE.md"
- Avoid negative phrasing ("Don't be concise" → "Be detailed")
- Test with scenarios to verify expected behavior

---

## Validation Commands

### Check for Duplication
```bash
# Find duplicate lines across CLAUDE.md files
comm -12 <(sort /CLAUDE.md) <(sort scripts/CLAUDE.md)
```

### Measure Token Reduction
```bash
#!/bin/bash
# Calculate token reduction

# Before (characters in root CLAUDE.md)
CHARS_BEFORE=$(wc -m < /CLAUDE.md)
TOKENS_BEFORE=$(echo "scale=0; $CHARS_BEFORE / 4" | bc)

# After (characters in all CLAUDE.md files)
CHARS_ROOT=$(wc -m < /CLAUDE.md)
CHARS_SCRIPTS=$(wc -m < scripts/CLAUDE.md 2>/dev/null || echo "0")
CHARS_CLAUDE=$(wc -m < .claude/CLAUDE.md 2>/dev/null || echo "0")
CHARS_TESTS=$(wc -m < tests/CLAUDE.md 2>/dev/null || echo "0")

CHARS_TOTAL=$((CHARS_ROOT + CHARS_SCRIPTS + CHARS_CLAUDE + CHARS_TESTS))
TOKENS_TOTAL=$(echo "scale=0; $CHARS_TOTAL / 4" | bc)

# Per-context (root + largest subdirectory)
CHARS_MAX_SUBDIR=$(echo -e "$CHARS_SCRIPTS\n$CHARS_CLAUDE\n$CHARS_TESTS" | sort -nr | head -1)
CHARS_EFFECTIVE=$((CHARS_ROOT + CHARS_MAX_SUBDIR))
TOKENS_EFFECTIVE=$(echo "scale=0; $CHARS_EFFECTIVE / 4" | bc)

# Reduction
REDUCTION=$(echo "scale=1; 100 * (1 - $TOKENS_EFFECTIVE / $TOKENS_BEFORE)" | bc)

echo "Before: $TOKENS_BEFORE tokens"
echo "After (total): $TOKENS_TOTAL tokens"
echo "After (effective per context): $TOKENS_EFFECTIVE tokens"
echo "Reduction: $REDUCTION%"
```

### Verify No Contradictions
```bash
# Manual review - check for conflicting instructions
grep -i "concise" /CLAUDE.md scripts/CLAUDE.md .claude/CLAUDE.md tests/CLAUDE.md
# Verify: Root says "concise", subdirectories should either not mention or clarify exceptions
```

---

## Success Criteria

Migration successful if:
- ✅ Token reduction ≥70% per context (root + one subdirectory)
- ✅ No duplication (same content in multiple files)
- ✅ No contradictions (clear precedence)
- ✅ All original content accounted for
- ✅ Cascading precedence tested and documented
- ✅ Subdirectories have inheritance/precedence notes

---

**Lines:** 450
**Last Updated:** 2025-11-10
