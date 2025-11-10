# Token Estimation Reference

**Purpose:** Methods and tools for estimating and measuring context token usage.

---

## Rule of Thumb

**~4 characters per token** (approximate for English text)

### Rationale
- Average English word: ~5 characters
- Average token: ~0.75 words
- Result: ~4 characters per token

### Accuracy
- ±10% for typical documentation
- More accurate for prose than code
- Code/JSON may vary (3-5 chars/token)

---

## Measurement Commands

### Character Count
```bash
# Single file
wc -m CLAUDE.md
# Output: 8000 CLAUDE.md

# Multiple files
wc -m CLAUDE.md scripts/CLAUDE.md .claude/CLAUDE.md
# Output:
#   8000 CLAUDE.md
#   1200 scripts/CLAUDE.md
#    800 .claude/CLAUDE.md
#  10000 total
```

### Token Estimation
```bash
# Estimate tokens from characters
CHARS=$(wc -m < CLAUDE.md)
TOKENS=$(echo "scale=0; $CHARS / 4" | bc)
echo "$TOKENS tokens (estimated)"

# Example: 8000 chars → 2000 tokens
```

### Per-Context Calculation
```bash
# Effective context = root + one subdirectory
CHARS_ROOT=$(wc -m < /CLAUDE.md)
CHARS_SUBDIR=$(wc -m < scripts/CLAUDE.md)
CHARS_EFFECTIVE=$((CHARS_ROOT + CHARS_SUBDIR))
TOKENS_EFFECTIVE=$(echo "scale=0; $CHARS_EFFECTIVE / 4" | bc)

echo "Per-context: $TOKENS_EFFECTIVE tokens"
```

---

## Edge Cases

### Code Blocks
- Code is denser (more tokens per character)
- Adjustment: ~3 chars/token for code-heavy files

### JSON/YAML
- Structured data: ~3.5 chars/token
- Many special characters increase token count

### Lists and Tables
- Markdown lists: ~4 chars/token (standard)
- Tables: ~3.5 chars/token (more structure)

### Example Adjustments
```bash
# For code-heavy file (scripts/)
TOKENS_SCRIPTS=$(echo "scale=0; $CHARS_SCRIPTS / 3" | bc)

# For documentation (root/)
TOKENS_ROOT=$(echo "scale=0; $CHARS_ROOT / 4" | bc)
```

---

## Evidence: claude-code-skill-factory

**Source:** Claude Code skill factory project analysis

**Measured Reduction:** 70-77% via progressive disclosure

**Method:**
- Before: Monolithic SKILL.md
- After: SKILL.md ≤200 lines + references/ for details
- Result: Significant context savings

**Application to Hierarchical CLAUDE.md:**
- Same principle: Progressive disclosure
- Root CLAUDE.md: Essential only
- Subdirectories: Details as needed
- Expected: 70%+ reduction

---

## Calculation Examples

### Example 1: Simple Migration
```
Before:
/CLAUDE.md: 10,000 chars → 2,500 tokens

After:
/CLAUDE.md: 3,000 chars → 750 tokens
scripts/CLAUDE.md: 800 chars → 200 tokens
.claude/CLAUDE.md: 600 chars → 150 tokens
tests/CLAUDE.md: 400 chars → 100 tokens

Total: 4,800 chars → 1,200 tokens
Per-context: 3,800 chars → 950 tokens (root + scripts)

Reduction: (2,500 - 950) / 2,500 = 62% ✅
```

### Example 2: Large Project
```
Before:
/CLAUDE.md: 20,000 chars → 5,000 tokens

After:
/CLAUDE.md: 5,000 chars → 1,250 tokens
scripts/CLAUDE.md: 1,500 chars → 375 tokens
.claude/CLAUDE.md: 1,200 chars → 300 tokens
tests/CLAUDE.md: 800 chars → 200 tokens

Total: 8,500 chars → 2,125 tokens
Per-context: 6,500 chars → 1,625 tokens (root + scripts)

Reduction: (5,000 - 1,625) / 5,000 = 67.5% ✅
```

---

## Validation Script

```bash
#!/bin/bash
# validate-token-reduction.sh

set -euo pipefail

echo "=== Token Reduction Calculation ==="
echo ""

# Before migration
if [[ -f /CLAUDE.md.backup ]]; then
  CHARS_BEFORE=$(wc -m < /CLAUDE.md.backup)
  TOKENS_BEFORE=$(echo "scale=0; $CHARS_BEFORE / 4" | bc)
  echo "Before migration: $TOKENS_BEFORE tokens"
else
  echo "ERROR: /CLAUDE.md.backup not found"
  exit 1
fi

# After migration
CHARS_ROOT=$(wc -m < /CLAUDE.md)
CHARS_SCRIPTS=$(wc -m < scripts/CLAUDE.md 2>/dev/null || echo "0")
CHARS_CLAUDE=$(wc -m < .claude/CLAUDE.md 2>/dev/null || echo "0")
CHARS_TESTS=$(wc -m < tests/CLAUDE.md 2>/dev/null || echo "0")

TOKENS_ROOT=$(echo "scale=0; $CHARS_ROOT / 4" | bc)
TOKENS_SCRIPTS=$(echo "scale=0; $CHARS_SCRIPTS / 4" | bc)
TOKENS_CLAUDE=$(echo "scale=0; $CHARS_CLAUDE / 4" | bc)
TOKENS_TESTS=$(echo "scale=0; $CHARS_TESTS / 4" | bc)

TOKENS_TOTAL=$((TOKENS_ROOT + TOKENS_SCRIPTS + TOKENS_CLAUDE + TOKENS_TESTS))

echo "After migration (total): $TOKENS_TOTAL tokens"
echo "  - Root: $TOKENS_ROOT tokens"
echo "  - scripts/: $TOKENS_SCRIPTS tokens"
echo "  - .claude/: $TOKENS_CLAUDE tokens"
echo "  - tests/: $TOKENS_TESTS tokens"

# Per-context (root + largest subdirectory)
MAX_SUBDIR_TOKENS=$(echo -e "$TOKENS_SCRIPTS\n$TOKENS_CLAUDE\n$TOKENS_TESTS" | sort -nr | head -1)
TOKENS_EFFECTIVE=$((TOKENS_ROOT + MAX_SUBDIR_TOKENS))

echo ""
echo "Effective per context: $TOKENS_EFFECTIVE tokens (root + largest subdirectory)"

# Reduction
REDUCTION=$(echo "scale=1; 100 * (1 - $TOKENS_EFFECTIVE * 1.0 / $TOKENS_BEFORE)" | bc)
echo "Reduction: $REDUCTION%"

# Validate target
if (( $(echo "$REDUCTION >= 70" | bc -l) )); then
  echo "✅ Target achieved (≥70%)"
else
  echo "⚠️ Below target (got $REDUCTION%, expected ≥70%)"
fi
```

---

## Summary

- **Rule of Thumb:** ~4 chars/token
- **Measurement:** `wc -m` + divide by 4
- **Per-Context:** Root + one subdirectory
- **Target:** ≥70% reduction
- **Evidence:** claude-code-skill-factory demonstrated 70-77%

---

**Lines:** 250
**Last Updated:** 2025-11-10
