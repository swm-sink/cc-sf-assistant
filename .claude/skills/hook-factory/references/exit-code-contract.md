# Exit Code Contract Reference

**Purpose:** Detailed specifications for Claude Code hook exit codes with behavior, edge cases, and best practices.

---

## Exit Code Standard

Claude Code hooks use the following exit code contract:

| Exit Code | Meaning | Behavior | Use When |
|-----------|---------|----------|----------|
| **0** | Success | Continue workflow, stdout visible | Validation passed, no issues |
| **2** | BLOCKING Error | Halt workflow, stderr fed to Claude | Critical failure, must fix before proceeding |
| **Other** (1, 3-255) | Warning | Pause for user decision | Advisory issue, user chooses to continue/abort |

---

## Exit 0: Success

### Behavior
- Workflow continues normally
- Hook stdout visible in Claude transcript
- No user intervention required
- Next step in workflow proceeds immediately

### When to Use
- Validation passed completely
- No issues detected
- Environment ready
- Output valid

### Examples

```bash
# Example 1: Git status clean
git diff --quiet && git diff --staged --quiet
if [[ $? -eq 0 ]]; then
  echo "Git status clean ✅"
  exit 0
fi
```

```bash
# Example 2: Credentials loaded
if [[ -f config/credentials/databricks.json ]]; then
  echo "Credentials loaded successfully"
  exit 0
fi
```

```bash
# Example 3: Tool execution allowed
if [[ "$TOOL_NAME" == "Read" ]]; then
  # Read-only tools always allowed
  exit 0
fi
```

---

## Exit 2: BLOCKING Error

### Behavior
- Workflow halts immediately
- stderr content fed to Claude as error message for fixing
- User intervention optional (Claude attempts automatic fix)
- Critical failures only

### When to Use
- **Must fix before proceeding:** Float in currency code, missing credentials, invalid syntax
- **Data integrity risk:** Destructive operation, invalid input
- **Policy violation:** Security rule broken, quality gate failed
- **Unrecoverable error:** File not found for Edit, network failure

### When NOT to Use
- Advisory warnings (use exit 1)
- Optional improvements (use exit 1)
- Non-critical issues (use exit 1)
- User preference matters (use exit 1)

### Error Message Requirements
1. **Specific:** Identify exact issue and location
2. **Actionable:** Explain how to fix
3. **Contextual:** Reference relevant documentation
4. **Concise:** 1-5 lines preferred

### Examples

```bash
# Example 1: Float detected (BLOCKING)
if echo "$CONTENT" | grep -q "float(.*currency"; then
  echo "ERROR: Float detected in currency calculation ($FILE_PATH)" >&2
  echo "Use Decimal type for financial precision per CLAUDE.md" >&2
  echo "Import: from decimal import Decimal" >&2
  exit 2
fi
```

```bash
# Example 2: Missing credentials (BLOCKING)
if [[ ! -f config/credentials/databricks.json ]]; then
  echo "ERROR: Missing databricks.json credentials" >&2
  echo "See config/credentials/README.md for setup instructions" >&2
  exit 2
fi
```

```bash
# Example 3: Uncommitted changes (BLOCKING)
git diff --quiet || {
  echo "ERROR: Uncommitted changes detected" >&2
  git status --short >&2
  echo "Commit or stash changes before ending session" >&2
  exit 2
}
```

```bash
# Example 4: Invalid syntax (BLOCKING)
yamllint "$FILE_PATH" || {
  echo "ERROR: Invalid YAML syntax in $FILE_PATH" >&2
  exit 2
}
```

### stderr vs stdout
- **stderr (>&2):** Error messages, fed to Claude on exit 2
- **stdout:** Normal output, visible in transcript on exit 0

```bash
# Correct usage
echo "INFO: Starting validation..." >&2  # stderr for logging
validate_file || {
  echo "ERROR: Validation failed" >&2    # stderr for error
  exit 2
}
echo "Validation passed"                 # stdout for success
exit 0
```

---

## Exit 1 (or other): Warning

### Behavior
- Workflow pauses for user decision
- User chooses to continue or abort
- Advisory checks, non-critical issues
- User preference matters

### When to Use
- **Optional improvements:** Code style, documentation
- **Advisory checks:** Large file detected, performance warning
- **User preference:** Proceed despite warning?
- **Non-critical issues:** Missing optional config, untracked files

### Examples

```bash
# Example 1: Untracked files (warning)
if [[ -n $(git ls-files --others --exclude-standard) ]]; then
  echo "WARNING: Untracked files detected" >&2
  git ls-files --others --exclude-standard >&2
  exit 1
fi
```

```bash
# Example 2: Large file (advisory)
if [[ $FILE_SIZE -gt 1048576 ]]; then
  echo "WARNING: Large file detected: $FILE_PATH ($(numfmt --to=iec $FILE_SIZE))" >&2
  echo "Consider splitting or using .gitignore" >&2
  exit 1
fi
```

```bash
# Example 3: Mypy warnings (non-blocking)
mypy --strict "$FILE_PATH" || {
  echo "WARNING: Mypy type checking failed" >&2
  echo "Consider fixing type hints for better code quality" >&2
  exit 1
}
```

---

## Edge Cases

### Edge Case 1: Exit 0 with stderr
```bash
# Logging to stderr does NOT trigger exit 2 behavior
echo "INFO: Starting validation..." >&2
validate_file
exit 0  # Success - stderr was just informational
```

**Behavior:** Exit 0 dominates - workflow continues, stderr visible but not fed to Claude as error

### Edge Case 2: Exit 2 with stdout
```bash
# stdout ignored on exit 2
echo "This is ignored"
echo "ERROR: Critical failure" >&2
exit 2
```

**Behavior:** Only stderr fed to Claude, stdout discarded

### Edge Case 3: Non-zero exit without stderr
```bash
# Exit 1 but no error message
validate_file
exit $?  # Could be 1, but no stderr
```

**Behavior:** Workflow pauses, but user sees no explanation (bad practice)

**Fix:** Always provide context
```bash
validate_file || {
  echo "WARNING: Validation failed" >&2
  exit 1
}
```

### Edge Case 4: Exit 0 despite failure
```bash
# Silent failure - BAD!
validate_file || true  # Always returns 0
exit 0
```

**Behavior:** Workflow continues despite failure (data integrity risk)

**Fix:** Propagate failures
```bash
validate_file || {
  echo "ERROR: Validation failed" >&2
  exit 2
}
exit 0
```

### Edge Case 5: Multiple exit codes
```bash
# First exit wins
if [[ condition1 ]]; then
  exit 2
fi
if [[ condition2 ]]; then
  exit 1  # Never reached if condition1 true
fi
exit 0
```

**Behavior:** Hook exits at first exit statement (order matters)

---

## Hook-Specific Exit Code Usage

### SessionStart
- **Exit 0:** Session ready (credentials loaded, environment valid)
- **Exit 2:** BLOCKING - missing critical credentials, invalid environment
- **Exit 1:** Warning - optional config missing, non-critical issue

### PreToolUse (BLOCKING by design)
- **Exit 0:** Allow tool execution
- **Exit 2:** Block tool execution (invalid input, policy violation)
- **Exit 1:** Warning - tool executes but user warned

### PostToolUse
- **Exit 0:** Validation passed
- **Exit 2:** Validation failed (recommend rollback)
- **Exit 1:** Warning - minor issue detected

### Stop (BLOCKING by design)
- **Exit 0:** Clean exit allowed
- **Exit 2:** Block session end (uncommitted changes, unsaved state)
- **Exit 1:** Warning - advisory issue (user decides)

### SubagentStop (BLOCKING by design)
- **Exit 0:** Subagent output valid
- **Exit 2:** Output invalid (retry or escalate)
- **Exit 1:** Warning - minor quality issue

### UserPromptSubmit
- **Exit 0:** Proceed with prompt
- **Exit 2:** Invalid prompt (RARE - almost never use)
- **Exit 1:** Warning - advisory message (user sees but proceeds)

### PreCompact
- **Exit 0:** Context saved successfully
- **Exit 2:** Save failed (prevent compaction)
- **Exit 1:** Warning - partial save

### Notification
- **Exit 0:** Notification handled
- **Exit 2:** Critical notification (escalate)
- **Exit 1:** Warning - logged but not critical

---

## Best Practices

### 1. Be Conservative with Exit 2
```bash
# ❌ BAD: Too strict
if [[ ! -f .editorconfig ]]; then
  exit 2  # Blocking for optional file
fi

# ✅ GOOD: Reserve exit 2 for critical
if [[ ! -f config/credentials/databricks.json ]]; then
  exit 2  # Blocking for required credentials
fi
```

### 2. Always Provide Context
```bash
# ❌ BAD: Vague error
echo "ERROR: Failed" >&2
exit 2

# ✅ GOOD: Specific and actionable
echo "ERROR: Float detected in currency calculation ($FILE_PATH)" >&2
echo "Use Decimal type: from decimal import Decimal" >&2
exit 2
```

### 3. Use set -e Carefully
```bash
# ❌ BAD: set -e causes unexpected exits
set -e
command_that_might_fail  # Exits hook with $? (not 0 or 2)

# ✅ GOOD: Explicit error handling
command_that_might_fail || {
  echo "ERROR: Command failed" >&2
  exit 2
}
```

### 4. Test All Exit Paths
```bash
# Ensure every path has explicit exit
if [[ condition1 ]]; then
  exit 0
elif [[ condition2 ]]; then
  exit 2
else
  exit 1  # Don't forget default case
fi
```

### 5. Distinguish BLOCKING vs Advisory
```bash
# Critical: Use exit 2
if [[ float in currency code ]]; then
  exit 2
fi

# Advisory: Use exit 1
if [[ code style issue ]]; then
  exit 1
fi
```

---

## Testing Exit Codes

### Manual Testing

```bash
# Test exit 0 (success)
./hook.sh && echo "Exit 0 ✅" || echo "Exit non-zero ❌"

# Test exit 2 (BLOCKING)
./hook.sh 2>/tmp/stderr.txt
if [[ $? -eq 2 ]]; then
  echo "Exit 2 detected ✅"
  cat /tmp/stderr.txt
fi

# Test exit 1 (warning)
./hook.sh
if [[ $? -eq 1 ]]; then
  echo "Exit 1 detected ✅"
fi
```

### Automated Testing

```bash
#!/bin/bash
# test_hook_exit_codes.sh

# Test success case
output=$(./hook.sh valid_input 2>&1)
if [[ $? -ne 0 ]]; then
  echo "FAIL: Success case exited non-zero"
fi

# Test BLOCKING case
output=$(./hook.sh invalid_input 2>&1)
if [[ $? -ne 2 ]]; then
  echo "FAIL: BLOCKING case did not exit 2"
fi

# Test warning case
output=$(./hook.sh warning_input 2>&1)
if [[ $? -ne 1 ]]; then
  echo "FAIL: Warning case did not exit 1"
fi
```

---

## Summary

**Key Principles:**
1. **Exit 0:** Validation passed, continue
2. **Exit 2:** BLOCKING error, must fix (use sparingly)
3. **Exit 1:** Warning, user decides (advisory)
4. **stderr:** Error messages (fed to Claude on exit 2)
5. **stdout:** Normal output (visible on exit 0)

**Decision Tree:**
```
Is this a critical failure that MUST be fixed?
├─ YES → Exit 2 (float in currency, missing credentials)
└─ NO → Is this an issue worth warning about?
    ├─ YES → Exit 1 (untracked files, code style)
    └─ NO → Exit 0 (all good)
```

---

**Lines:** 400
**Last Updated:** 2025-11-10
