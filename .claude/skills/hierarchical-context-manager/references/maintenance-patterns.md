# Maintenance Patterns Reference

**Purpose:** Guidelines for updating and maintaining hierarchical CLAUDE.md configuration.

---

## When to Update Root vs Subdirectory

### Update Root CLAUDE.md When:
- Cross-cutting behavioral principle changes
- Anti-hallucination protocol updates
- RPIV workflow modifications
- New meta-infrastructure principles
- Response format requirements change

### Update Subdirectory CLAUDE.md When:
- Component-specific implementation details change
- New patterns for that component type
- Tool/library updates affecting component
- Component-specific anti-patterns discovered

---

## Cross-Cutting Changes

**Pattern:** Change affects ALL work (root + subdirectories)

### Example: New Verification Step
**Change:** Add "Check for magic numbers" to chain of verification

**Implementation:**
1. Update root CLAUDE.md:
   ```markdown
   ## Chain of Verification Protocol
   - ...existing steps...
   - Check for magic numbers (use config/thresholds.yaml)
   ```

2. Update scripts/CLAUDE.md (if needed):
   ```markdown
   ## Magic Numbers (Root Rule + Refinement)
   - Root: Use config/thresholds.yaml
   - scripts/: Specifically for materiality thresholds (10%, $50K)
   ```

3. Propagate to .claude/CLAUDE.md and tests/CLAUDE.md (if relevant)

### Validation:
- [ ] Root updated
- [ ] All relevant subdirectories updated or explicitly inherit
- [ ] No contradictions introduced
- [ ] Tested in each context

---

## Component-Specific Changes

**Pattern:** Change affects ONE component type only

### Example: New Python Type Hint Rule
**Change:** Require return type hints on all functions

**Implementation:**
1. Update scripts/CLAUDE.md only:
   ```markdown
   ## Type Safety Enforcement
   - Type hints: parameters AND returns (no exceptions)
   - ...
   ```

2. Root CLAUDE.md unchanged (not cross-cutting)
3. Other subdirectories unchanged

### Validation:
- [ ] Only relevant subdirectory updated
- [ ] Root unchanged (confirm not cross-cutting)
- [ ] Tested in that component context

---

## Validation: Ensure No Contradictions

### After ANY Update

**Step 1: Check for Duplication**
```bash
# Find duplicate content
comm -12 <(sort /CLAUDE.md) <(sort scripts/CLAUDE.md)
```

**Step 2: Check for Contradictions**
```bash
# Search for related keywords
grep -i "type hints" /CLAUDE.md scripts/CLAUDE.md .claude/CLAUDE.md tests/CLAUDE.md

# Manual review: Ensure consistent message
```

**Step 3: Test Precedence**
- Verify most nested rule applies
- Test with sample prompts in each context
- Confirm expected behavior

**Step 4: Measure Token Impact**
```bash
# Re-calculate token counts
./validate-token-reduction.sh

# Verify still ≥70% reduction
```

---

## Common Maintenance Scenarios

### Scenario 1: Add New Subdirectory
**Example:** Add `docs/CLAUDE.md` for documentation-specific rules

**Steps:**
1. Create docs/CLAUDE.md from template or custom
2. Add inheritance note: "Inherits: Root CLAUDE.md"
3. Add precedence note: "Precedence: Overrides root for docs/**"
4. Define docs-specific rules:
   ```markdown
   ## Documentation Style
   - Detailed explanations (override root conciseness)
   - Examples required for all features
   - User-facing language (not technical)
   ```
5. Test with documentation prompts

### Scenario 2: Remove Outdated Rule
**Example:** Remove "Use Python 3.8" (now using 3.11)

**Steps:**
1. Search all CLAUDE.md files:
   ```bash
   grep -r "Python 3.8" /CLAUDE.md scripts/CLAUDE.md .claude/CLAUDE.md tests/CLAUDE.md
   ```
2. Update all mentions to "Python 3.11"
3. Verify no other references (version-specific code)
4. Test to ensure no breakage

### Scenario 3: Refactor Overlapping Rules
**Example:** Root and scripts/ both mention Decimal precision

**Before:**
```
Root: "Use appropriate precision"
scripts/: "Use Decimal for currency"
```

**After (Refactored):**
```
Root: "Financial calculations require Decimal type (not float)"
scripts/: "Implementation: from decimal import Decimal, ROUND_HALF_UP"
```

**Benefits:**
- Root states principle (cross-cutting)
- scripts/ provides implementation detail
- No duplication, clear separation

---

## Periodic Maintenance Tasks

### Monthly
- [ ] Review recent changes to root CLAUDE.md
- [ ] Check for new patterns in subdirectories
- [ ] Verify no contradictions introduced
- [ ] Measure token reduction (should maintain ≥70%)

### Quarterly
- [ ] Comprehensive review of all CLAUDE.md files
- [ ] Consolidate overlapping rules
- [ ] Update examples in subdirectories
- [ ] Refresh templates if patterns changed

### Annually
- [ ] Full audit of hierarchical structure
- [ ] Consider adding new subdirectories (if components grew)
- [ ] Consider merging subdirectories (if redundant)
- [ ] Update token reduction baseline

---

## Documentation Requirements

### After Significant Changes
Create change log entry:
```markdown
## CLAUDE.md Change Log

### 2025-11-15: Add Magic Number Check
- **Type:** Cross-cutting change
- **Updated:** Root CLAUDE.md + all subdirectories
- **Reason:** Prevent hardcoded thresholds
- **Impact:** Prompts now reference config/thresholds.yaml
```

### For New Subdirectories
Create README:
```markdown
# docs/CLAUDE.md

**Purpose:** Documentation-specific behavioral overrides

**Inherits:** Root CLAUDE.md (all core principles)

**Overrides:**
- Conciseness: Detailed explanations (not 1-3 sentences)
- Audience: User-facing language (not technical jargon)
- Examples: Required for all features

**Created:** 2025-11-15
**Maintained By:** Documentation team
```

---

## Conflict Resolution Process

### If Contradiction Discovered

**Step 1: Identify Conflict**
```
Root: "Be concise"
scripts/: "Be detailed"
```

**Step 2: Determine Intent**
- Root intent: General responses concise
- scripts/ intent: Docstrings detailed

**Step 3: Clarify in Both**
```
Root: "Be concise (1-3 sentences) for responses. Exceptions: docstrings, documentation."
scripts/: "Docstrings: Detailed (purpose, parameters, returns, examples)"
```

**Step 4: Test Resolution**
- Verify expected behavior in both contexts
- Document resolution in change log

---

## Best Practices Summary

1. **Cross-cutting changes:** Update root + all relevant subdirectories
2. **Component-specific changes:** Update only relevant subdirectory
3. **Validate after changes:** Check for duplication/contradictions
4. **Test precedence:** Verify most nested wins
5. **Document significant changes:** Maintain change log
6. **Periodic reviews:** Monthly, quarterly, annual maintenance
7. **Keep token reduction:** Monitor and maintain ≥70%

---

**Lines:** 250
**Last Updated:** 2025-11-10
