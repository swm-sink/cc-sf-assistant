# Development Hooks Reference

**Purpose:** Practical development hooks for quality gates, linters, validators, and git workflow automation.

**Audience:** Developers implementing hooks for code quality and development workflow

---

## Quality Gate Hooks

### Decimal Precision Checker (PreToolUse)

**Use Case:** Block Write/Edit on scripts/core/ if float detected in currency code

```bash
#!/bin/bash
# hooks/pre-tool-use-decimal-checker.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  if [[ "$FILE_PATH" == scripts/core/* ]]; then
    CONTENT=$(echo "$TOOL_PARAMS" | jq -r '.content // .new_string // empty')

    if echo "$CONTENT" | grep -qE "float\s*\([^)]*\b(currency|price|amount|revenue|expense|budget|actual)\b"; then
      echo "ERROR: Float detected in currency calculation ($FILE_PATH)" >&2
      echo "" >&2
      echo "Financial calculations require Decimal type:" >&2
      echo "  from decimal import Decimal" >&2
      echo "  amount = Decimal('123.45')  # NOT float(123.45)" >&2
      echo "" >&2
      echo "Per CLAUDE.md financial precision requirements" >&2
      exit "$BLOCKING_ERROR"
    fi
  fi
fi

exit "$SUCCESS"
```

**Integration:** .claude/hooks/pre-tool-use.sh

---

### Audit Trail Validator (PreToolUse)

**Use Case:** Ensure audit logging exists in workflow scripts

```bash
#!/bin/bash
# hooks/pre-tool-use-audit-checker.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Write" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  if [[ "$FILE_PATH" == scripts/workflows/* ]]; then
    CONTENT=$(echo "$TOOL_PARAMS" | jq -r '.content // empty')

    # Check for audit logging
    if ! echo "$CONTENT" | grep -q "audit.*log\|logger\."; then
      echo "WARNING: No audit logging detected in workflow script" >&2
      echo "Consider adding: logger.info(f'{timestamp} | {operation} | {file}'))" >&2
      exit 1
    fi
  fi
fi

exit "$SUCCESS"
```

---

## Linter Integration Hooks

### Ruff Formatter (PostToolUse)

**Use Case:** Auto-format Python files after Write/Edit

```bash
#!/bin/bash
# hooks/post-tool-use-ruff.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  if [[ "$FILE_PATH" == *.py ]]; then
    if command -v ruff &> /dev/null; then
      echo "Running ruff formatter on $FILE_PATH..." >&2
      ruff format "$FILE_PATH" || {
        echo "ERROR: Ruff formatter failed" >&2
        exit "$BLOCKING_ERROR"
      }
      echo "✅ Formatted with ruff"
    fi
  fi
fi

exit "$SUCCESS"
```

---

### Mypy Type Checker (PostToolUse)

**Use Case:** Run type checking after Write on Python files (warning only)

```bash
#!/bin/bash
# hooks/post-tool-use-mypy.sh
set -euo pipefail

readonly WARNING=1
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Write" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  if [[ "$FILE_PATH" == scripts/*.py ]]; then
    if command -v mypy &> /dev/null; then
      echo "Running mypy on $FILE_PATH..." >&2
      mypy --strict "$FILE_PATH" || {
        echo "WARNING: Mypy type checking failed" >&2
        echo "Consider fixing type hints for better code quality" >&2
        exit "$WARNING"
      }
      echo "✅ Mypy passed"
    fi
  fi
fi

exit "$SUCCESS"
```

---

### YAML Validator (PostToolUse)

**Use Case:** Validate YAML syntax after Edit

```bash
#!/bin/bash
# hooks/post-tool-use-yaml-validator.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Edit" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  if [[ "$FILE_PATH" == *.yaml || "$FILE_PATH" == *.yml ]]; then
    if command -v yamllint &> /dev/null; then
      yamllint "$FILE_PATH" || {
        echo "ERROR: Invalid YAML syntax in $FILE_PATH" >&2
        exit "$BLOCKING_ERROR"
      }
      echo "✅ YAML syntax valid"
    fi
  fi
fi

exit "$SUCCESS"
```

---

## Git Workflow Hooks

### Uncommitted Changes Blocker (Stop)

**Use Case:** Block session end if uncommitted changes exist

```bash
#!/bin/bash
# hooks/stop-git-checker.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly WARNING=1
readonly SUCCESS=0

# Check for uncommitted changes (BLOCKING)
git diff --quiet && git diff --staged --quiet
if [[ $? -ne 0 ]]; then
  echo "ERROR: Uncommitted changes detected" >&2
  echo "" >&2
  git status --short >&2
  echo "" >&2
  echo "Commit or stash changes before ending session" >&2
  exit "$BLOCKING_ERROR"
fi

# Check for untracked files (WARNING)
UNTRACKED=$(git ls-files --others --exclude-standard)
if [[ -n "$UNTRACKED" ]]; then
  echo "WARNING: Untracked files detected:" >&2
  echo "$UNTRACKED" >&2
  echo "Consider adding to .gitignore or committing" >&2
  exit "$WARNING"
fi

echo "✅ Git status clean"
exit "$SUCCESS"
```

---

### Branch Name Validator (SessionStart)

**Use Case:** Validate branch name follows convention (claude/*)

```bash
#!/bin/bash
# hooks/session-start-branch-validator.sh
set -euo pipefail

readonly WARNING=1
readonly SUCCESS=0

BRANCH=$(git branch --show-current 2>/dev/null || echo "")

if [[ -n "$BRANCH" && ! "$BRANCH" =~ ^claude/ ]]; then
  echo "WARNING: Branch name '$BRANCH' does not follow convention" >&2
  echo "Expected: claude/<description>-<session-id>" >&2
  exit "$WARNING"
fi

exit "$SUCCESS"
```

---

### Commit Message Validator (PostToolUse)

**Use Case:** Validate commit message format after git commit

```bash
#!/bin/bash
# hooks/post-tool-use-commit-validator.sh
set -euo pipefail

readonly WARNING=1
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Bash" ]]; then
  COMMAND=$(echo "$TOOL_PARAMS" | jq -r '.command // empty')

  if echo "$COMMAND" | grep -q "git commit"; then
    # Get last commit message
    COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null || echo "")

    # Check for conventional commit format
    if ! echo "$COMMIT_MSG" | grep -qE "^(feat|fix|docs|refactor|test|chore|perf|ci|build|style)\(.*\):"; then
      echo "WARNING: Commit message does not follow conventional format" >&2
      echo "Expected: type(scope): description" >&2
      echo "Example: feat(hook-factory): implement SessionStart hook" >&2
      exit "$WARNING"
    fi
  fi
fi

exit "$SUCCESS"
```

---

## Environment Validation Hooks

### Python Environment Checker (SessionStart)

**Use Case:** Verify Python and required packages installed

```bash
#!/bin/bash
# hooks/session-start-python-checker.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

# Check Python 3 installed
if ! command -v python3 &> /dev/null; then
  echo "ERROR: python3 not found in PATH" >&2
  exit "$BLOCKING_ERROR"
fi

# Check Python version (≥3.11)
PYTHON_VERSION=$(python3 --version | grep -oP '\\d+\\.\\d+')
if [[ $(echo "$PYTHON_VERSION < 3.11" | bc) -eq 1 ]]; then
  echo "ERROR: Python $PYTHON_VERSION detected, requires ≥3.11" >&2
  exit "$BLOCKING_ERROR"
fi

# Check required packages (optional check)
if [[ -f pyproject.toml ]]; then
  if ! python3 -c "import pandas, decimal, openpyxl" 2>/dev/null; then
    echo "WARNING: Missing required packages" >&2
    echo "Run: pip install -e ." >&2
    exit 1
  fi
fi

echo "✅ Python environment valid ($PYTHON_VERSION)"
exit "$SUCCESS"
```

---

### Pre-commit Hooks Checker (SessionStart)

**Use Case:** Verify pre-commit hooks installed

```bash
#!/bin/bash
# hooks/session-start-precommit-checker.sh
set -euo pipefail

readonly WARNING=1
readonly SUCCESS=0

if [[ -f .pre-commit-config.yaml ]]; then
  if [[ ! -f .git/hooks/pre-commit ]]; then
    echo "WARNING: pre-commit hooks not installed" >&2
    echo "Run: pre-commit install" >&2
    exit "$WARNING"
  fi
  echo "✅ Pre-commit hooks installed"
fi

exit "$SUCCESS"
```

---

## Testing Automation Hooks

### Pytest Runner (PostToolUse)

**Use Case:** Run tests after Write on test files

```bash
#!/bin/bash
# hooks/post-tool-use-pytest.sh
set -euo pipefail

readonly WARNING=1
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Write" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  if [[ "$FILE_PATH" == tests/test_*.py ]]; then
    if command -v pytest &> /dev/null; then
      echo "Running pytest on $FILE_PATH..." >&2
      pytest "$FILE_PATH" -v || {
        echo "WARNING: Tests failed" >&2
        exit "$WARNING"
      }
      echo "✅ Tests passed"
    fi
  fi
fi

exit "$SUCCESS"
```

---

### Coverage Checker (PostToolUse)

**Use Case:** Check test coverage after pytest run

```bash
#!/bin/bash
# hooks/post-tool-use-coverage.sh
set -euo pipefail

readonly WARNING=1
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Bash" ]]; then
  COMMAND=$(echo "$TOOL_PARAMS" | jq -r '.command // empty')

  if echo "$COMMAND" | grep -q "pytest.*--cov"; then
    # Check coverage report
    COVERAGE=$(coverage report | grep TOTAL | grep -oP '\\d+%' | tr -d '%')
    if [[ $COVERAGE -lt 80 ]]; then
      echo "WARNING: Test coverage ${COVERAGE}% < 80% target" >&2
      exit "$WARNING"
    fi
    echo "✅ Test coverage ${COVERAGE}%"
  fi
fi

exit "$SUCCESS"
```

---

## Performance Monitoring Hooks

### Tool Execution Timer (Notification)

**Use Case:** Log slow tool executions

```bash
#!/bin/bash
# hooks/notification-timer.sh
set -euo pipefail

readonly WARNING=1
readonly SUCCESS=0

NOTIFICATION_TYPE="${1:-}"
NOTIFICATION_DATA="${2:-}"

if [[ "$NOTIFICATION_TYPE" == "tool_execution_time" ]]; then
  TOOL_NAME=$(echo "$NOTIFICATION_DATA" | jq -r '.tool // empty')
  DURATION=$(echo "$NOTIFICATION_DATA" | jq -r '.duration // 0')

  # Log to performance.log
  echo "$(date -Iseconds) | $TOOL_NAME | ${DURATION}ms" >> config/performance.log

  # Warn if > 5 seconds
  if [[ $DURATION -gt 5000 ]]; then
    echo "WARNING: Slow tool execution - $TOOL_NAME took ${DURATION}ms" >&2
    exit "$WARNING"
  fi
fi

exit "$SUCCESS"
```

---

## Context Management Hooks

### Todo List Saver (PreCompact)

**Use Case:** Save todo list before context compaction

```bash
#!/bin/bash
# hooks/pre-compact-todos.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

if [[ -f .claude/todos/current.json ]]; then
  mkdir -p config/workflow-state/
  BACKUP_FILE="config/workflow-state/todos-$(date +%Y%m%d-%H%M%S).json"

  cp .claude/todos/current.json "$BACKUP_FILE" || {
    echo "ERROR: Failed to backup todo list" >&2
    exit "$BLOCKING_ERROR"
  }

  echo "✅ Saved todo list to $BACKUP_FILE"
fi

exit "$SUCCESS"
```

---

## Summary

**Quality Gates (PreToolUse):**
- Decimal precision checker (BLOCKING)
- Audit trail validator (warning)

**Linters (PostToolUse):**
- Ruff formatter (BLOCKING on error)
- Mypy type checker (warning)
- YAML validator (BLOCKING on syntax error)

**Git Workflow:**
- Uncommitted changes blocker (Stop - BLOCKING)
- Branch name validator (SessionStart - warning)
- Commit message validator (PostToolUse - warning)

**Environment:**
- Python environment checker (SessionStart - BLOCKING)
- Pre-commit hooks checker (SessionStart - warning)

**Testing:**
- Pytest runner (PostToolUse - warning)
- Coverage checker (PostToolUse - warning)

**Performance:**
- Tool execution timer (Notification - warning)

**Context:**
- Todo list saver (PreCompact - BLOCKING)

---

**Lines:** 420
**Last Updated:** 2025-11-10
