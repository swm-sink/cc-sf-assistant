# Cascading Rules Reference

**Purpose:** Precedence algorithm and conflict resolution for hierarchical CLAUDE.md.

---

## Precedence Algorithm

**Rule:** Most nested CLAUDE.md wins for conflicts

### Hierarchy Example
```
/CLAUDE.md (depth 0 - root)
    ↓ applies everywhere
scripts/CLAUDE.md (depth 1)
    ↓ applies to scripts/**
scripts/core/CLAUDE.md (depth 2)
    ↓ applies to scripts/core/**
```

### Precedence Order
1. **Deepest match wins:** scripts/core/CLAUDE.md > scripts/CLAUDE.md > /CLAUDE.md
2. **Inheritance:** All depths inherit from parent unless overridden
3. **Explicit override:** Subdirectory must explicitly state rule to override

---

## Conflict Resolution

### Scenario 1: Direct Conflict
**Root:** "Be concise (1-3 sentences)"
**scripts/:** "Docstrings: Detailed (purpose, parameters, returns, examples)"

**Resolution:**
- In scripts/: Detailed docstrings (subdirectory wins)
- In .claude/: Concise responses (root applies)
- No conflict: Different contexts

### Scenario 2: Contradictory Instructions
**Root:** "Use float for calculations"
**scripts/:** "Use Decimal for currency calculations"

**Resolution:**
- Root is wrong (financial precision requires Decimal)
- Fix root to say "Use appropriate types"
- scripts/ specifies "Decimal for currency"

### Scenario 3: Partial Override
**Root:** "Type hints on all functions"
**scripts/:** "Type hints: parameters, returns, exceptions (strict mypy)"

**Resolution:**
- scripts/ extends root (more specific)
- Both apply: Type hints + mypy strict
- Not a conflict: Refinement

---

## Override vs Append Behavior

### Override (Default)
Subdirectory **replaces** root rule entirely.

**Example:**
```markdown
# Root CLAUDE.md
Response length: 1-3 sentences default

# scripts/CLAUDE.md
Response length: Detailed docstrings (purpose, parameters, returns, examples)
```

**Effective in scripts/:** Detailed docstrings (override)

### Append (Explicit)
Subdirectory **adds to** root rule.

**Example:**
```markdown
# Root CLAUDE.md
Error handling: Explicit exceptions

# scripts/CLAUDE.md
Error handling (inherits root + adds):
  - Root: Explicit exceptions ✅
  - Plus: Custom domain exceptions (InvalidAccountTypeError, etc.)
```

**Effective in scripts/:** Both apply

---

## Testing Cascading Behavior

### Test 1: Verify Override
```markdown
# Root CLAUDE.md
Be ultra-concise (1-3 sentences)

# scripts/CLAUDE.md
Docstrings: Detailed with examples

# Test in scripts/
Prompt: "Document calculate_variance function"
Expected: Detailed docstring (subdirectory overrides root)
```

### Test 2: Verify Inheritance
```markdown
# Root CLAUDE.md
Chain of verification: Mark [NEEDS VERIFICATION] for uncertain claims

# scripts/CLAUDE.md
(no mention of verification)

# Test in scripts/
Prompt: "What's the average variance in Q3?"
Expected: Should mark [NEEDS VERIFICATION] (inherits from root)
```

### Test 3: Verify Depth Precedence
```markdown
# Root CLAUDE.md
Use standard naming (camelCase)

# scripts/CLAUDE.md
Use Python naming (snake_case)

# scripts/core/CLAUDE.md
Use strict naming (snake_case + type prefixes)

# Test in scripts/core/
Expected: Strict naming (depth 2 wins over depth 1 and 0)
```

---

## Common Precedence Patterns

### Pattern 1: General → Specific
```
Root: General principle
Subdirectory: Specific implementation
```

**Example:**
- Root: "Use appropriate data types"
- scripts/: "Use Decimal for currency (not float)"

### Pattern 2: Behavioral → Technical
```
Root: How to think/respond
Subdirectory: Technical requirements
```

**Example:**
- Root: "Be skeptical analyst, challenge assumptions"
- scripts/: "Type hints on all functions (mypy strict)"

### Pattern 3: Cross-Cutting → Component
```
Root: Applies to all work
Subdirectory: Applies to this component only
```

**Example:**
- Root: "RPIV workflow for implementations"
- tests/: "Edge cases mandatory for financial tests"

---

## Debugging Precedence Issues

### Issue: Config Not Applied
**Symptom:** Subdirectory rule not being followed

**Debug Steps:**
1. Verify subdirectory CLAUDE.md exists in correct location
2. Check file is named exactly `CLAUDE.md` (case-sensitive)
3. Verify rule is explicitly stated (not assumed inherited)
4. Test with simple prompt in that directory context

### Issue: Conflicting Behavior
**Symptom:** Unclear which rule applies

**Debug Steps:**
1. Check for contradictions (root vs subdirectory)
2. Verify precedence (most nested should win)
3. Make override explicit in subdirectory: "This overrides root"
4. Test with edge case prompts

### Issue: No Inheritance
**Symptom:** Root rules not applying in subdirectory

**Debug Steps:**
1. Verify root CLAUDE.md exists
2. Check subdirectory hasn't overridden that specific rule
3. Test with prompt that should trigger root rule
4. Add inheritance note to subdirectory: "Inherits: Root CLAUDE.md"

---

## Validation Commands

### Check Hierarchy
```bash
# Find all CLAUDE.md files
find . -name "CLAUDE.md" -type f

# Expected output:
# ./CLAUDE.md
# ./scripts/CLAUDE.md
# ./.claude/CLAUDE.md
# ./tests/CLAUDE.md
```

### Check for Contradictions
```bash
# Search for conflicting instructions
grep -i "concise" */CLAUDE.md CLAUDE.md

# Manual review: Ensure no direct contradictions
```

### Test Precedence
```bash
# Create test scenarios for each subdirectory
# Verify most nested rule applies
```

---

## Best Practices

1. **Explicit overrides:** State "This overrides root" in subdirectory
2. **Document inheritance:** Note "Inherits: Root CLAUDE.md"
3. **Avoid contradictions:** Root and subdirectory should not say opposite things
4. **Test each level:** Verify behavior at each depth
5. **Keep precedence clear:** Most nested wins, document exceptions

---

## Summary

- **Precedence:** Most nested CLAUDE.md wins
- **Inheritance:** All levels inherit from parent
- **Override:** Default behavior (subdirectory replaces root)
- **Append:** Explicit (subdirectory adds to root)
- **Testing:** Verify with prompts in each context

---

**Lines:** 250
**Last Updated:** 2025-11-10
