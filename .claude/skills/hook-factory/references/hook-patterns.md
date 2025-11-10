# Hook Patterns Reference

**Purpose:** Complete documentation of Claude Code's 8 lifecycle hook types with use cases, examples, and integration patterns.

**Audience:** Developers using Hook Factory to generate custom hooks

---

## Overview

Claude Code supports 8 lifecycle hook types that enable deterministic quality gates, workflow automation, and session management. Each hook type has specific use cases, timing, and exit code behavior.

### Hook Lifecycle

```
Session Start
    ↓
User Prompt → [UserPromptSubmit Hook]
    ↓
Claude Processing
    ↓
Tool Call → [PreToolUse Hook] → Tool Execution → [PostToolUse Hook]
    ↓
Subagent Launch → Subagent Work → [SubagentStop Hook]
    ↓
Context Full → [PreCompact Hook] → Compaction
    ↓
System Event → [Notification Hook]
    ↓
Session End → [Stop Hook]
```

---

## 1. SessionStart Hook

### When It Runs
- At the very beginning of a Claude Code session
- Before any user interaction or tool execution
- Once per session

### Use Cases

**Development:**
- Verify pre-commit hooks installed
- Check Python/Node environment setup
- Validate git configuration
- Initialize logging

**Production:**
- Load API credentials from config/credentials/
- Verify database connections
- Check file permissions
- Initialize audit log

### Parameters
None (SessionStart receives no parameters)

### Exit Codes
- **Exit 0:** Session ready, continue
- **Exit 2:** BLOCKING - missing credentials, invalid environment (halt session)
- **Other:** Warning - non-critical issue (user decides)

### Example: Load Credentials

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0
readonly BLOCKING_ERROR=2

# Check Databricks credentials
if [[ ! -f config/credentials/databricks.json ]]; then
  echo "ERROR: Missing databricks.json credentials" >&2
  echo "See config/credentials/README.md for setup" >&2
  exit "$BLOCKING_ERROR"
fi

# Check Adaptive credentials
if [[ ! -f config/credentials/adaptive.json ]]; then
  echo "ERROR: Missing adaptive.json credentials" >&2
  exit "$BLOCKING_ERROR"
fi

# Initialize audit log
if [[ ! -f config/audit.log ]]; then
  touch config/audit.log
  echo "$(date -Iseconds) | SESSION_START | Initialized audit log" >> config/audit.log
fi

echo "Session initialized: Credentials loaded, audit log ready"
exit "$SUCCESS"
```

### Integration Notes
- Keep lightweight (< 5 seconds execution time)
- Avoid network calls (no API validation during startup)
- Log to stderr for visibility in transcript
- Exit 2 only for critical issues (missing credentials, not warnings)

---

## 2. PreToolUse Hook (BLOCKING)

### When It Runs
- Immediately before any tool execution (Write, Edit, Bash, etc.)
- Can halt tool execution if validation fails
- Runs on EVERY tool call (performance matters)

### Use Cases

**Development:**
- Block Write on float-using currency code
- Validate file permissions before Edit
- Check Bash commands against allowed list
- Enforce naming conventions

**Production:**
- Validate report structure before generation
- Check thresholds before variance calculation
- Prevent destructive operations
- Ensure audit trail exists

### Parameters
1. **TOOL_NAME** - Name of tool about to execute (e.g., "Write", "Edit", "Bash")
2. **TOOL_PARAMS** - JSON string of tool parameters (e.g., `{"file_path": "...", "content": "..."}`)

### Exit Codes
- **Exit 0:** Allow tool execution
- **Exit 2:** BLOCKING - halt tool execution (stderr fed to Claude for fixing)
- **Other:** Warning - tool executes but user sees warning

### Example: Block Float in Currency Code

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0
readonly BLOCKING_ERROR=2

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

# Only validate Write/Edit on scripts/core/
if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  if [[ "$FILE_PATH" == scripts/core/* ]]; then
    # Extract content (Write uses .content, Edit uses .new_string)
    CONTENT=$(echo "$TOOL_PARAMS" | jq -r '.content // .new_string // empty')

    # Check for float usage with currency-related variables
    if echo "$CONTENT" | grep -qE "float\s*\([^)]*\b(currency|price|amount|revenue|expense|budget|actual|cost|sales)\b"; then
      echo "ERROR: Float detected in currency calculation ($FILE_PATH)" >&2
      echo "" >&2
      echo "Financial calculations require Decimal type for precision:" >&2
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

### Example: Validate File Exists Before Edit

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0
readonly BLOCKING_ERROR=2

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Edit" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  if [[ ! -f "$FILE_PATH" ]]; then
    echo "ERROR: Cannot edit non-existent file: $FILE_PATH" >&2
    echo "Use Write tool for new files, not Edit" >&2
    exit "$BLOCKING_ERROR"
  fi
fi

exit "$SUCCESS"
```

### Integration Notes
- Must execute quickly (< 1 second preferred)
- Parse TOOL_PARAMS carefully (JSON format, may have missing fields)
- Exit 2 provides stderr to Claude as error message (be specific and actionable)
- Consider whitelisting tools you don't need to validate (e.g., Read, Glob, Grep are read-only)

---

## 3. PostToolUse Hook

### When It Runs
- After Write, Edit, or Bash tool execution
- Tool has already executed (cannot prevent, only validate)
- Can trigger rollback if validation fails

### Use Cases

**Development:**
- Run linters after Write (ruff, mypy)
- Validate YAML/JSON syntax after Edit
- Update audit log after file changes
- Invoke System Coherence Validator on .claude/ files

**Production:**
- Log data transformations to audit trail
- Validate report structure after generation
- Run tests after script changes
- Update workflow state

### Parameters
1. **TOOL_NAME** - Tool that executed (e.g., "Write", "Edit", "Bash")
2. **TOOL_PARAMS** - JSON string of tool parameters
3. **TOOL_RESULT** - JSON string of tool result/output

### Exit Codes
- **Exit 0:** Validation passed
- **Exit 2:** BLOCKING - validation failed (recommend rollback)
- **Other:** Warning - issue detected but not critical

### Example: Run Ruff After Write

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0
readonly BLOCKING_ERROR=2

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  # Run ruff on Python files
  if [[ "$FILE_PATH" == *.py ]]; then
    if command -v ruff &> /dev/null; then
      ruff format "$FILE_PATH" || {
        echo "ERROR: Ruff formatter failed on $FILE_PATH" >&2
        exit "$BLOCKING_ERROR"
      }
      echo "Formatted $FILE_PATH with ruff"
    fi
  fi
fi

exit "$SUCCESS"
```

### Example: Update Audit Log

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

# Log all Write operations on workflows/
if [[ "$TOOL_NAME" == "Write" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  if [[ "$FILE_PATH" == scripts/workflows/* ]]; then
    echo "$(date -Iseconds) | $USER | $TOOL_NAME | $FILE_PATH" >> config/audit.log
    echo "Logged transformation to audit trail"
  fi
fi

exit "$SUCCESS"
```

### Integration Notes
- Tool already executed (PostToolUse cannot prevent)
- Exit 2 signals rollback recommended (Claude may attempt undo)
- Avoid long-running operations (tests, full builds) - use Bash explicitly instead
- Useful for auto-formatting, logging, validation checks

---

## 4. Stop Hook (BLOCKING)

### When It Runs
- At session end, before Claude exits
- After all work complete, before shutdown
- Once per session

### Use Cases

**Development:**
- Check for uncommitted changes (git status)
- Verify todos complete
- Cleanup temporary files
- Generate session summary

**Production:**
- Save workflow state to config/
- Backup in-progress reports
- Verify audit log integrity
- Archive session data

### Parameters
None (Stop receives no parameters)

### Exit Codes
- **Exit 0:** Clean exit allowed
- **Exit 2:** BLOCKING - halt session end (uncommitted changes, unsaved state)
- **Other:** Warning - non-critical issue (user decides)

### Example: Check Uncommitted Changes

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0
readonly BLOCKING_ERROR=2

# Check for uncommitted changes
git diff --quiet && git diff --staged --quiet
if [[ $? -ne 0 ]]; then
  echo "ERROR: Uncommitted changes detected" >&2
  echo "" >&2
  git status --short >&2
  echo "" >&2
  echo "Please commit or stash changes before ending session" >&2
  exit "$BLOCKING_ERROR"
fi

# Check for untracked files (warning only)
if [[ -n $(git ls-files --others --exclude-standard) ]]; then
  echo "WARNING: Untracked files detected:" >&2
  git ls-files --others --exclude-standard >&2
fi

exit "$SUCCESS"
```

### Integration Notes
- Common pattern: Block on dirty git status
- User can override exit 2 (emergency session end)
- Keep execution time reasonable (< 10 seconds)
- Consider warning vs BLOCKING carefully (distinguish critical from advisory)

---

## 5. SubagentStop Hook (BLOCKING)

### When It Runs
- After subagent task completes
- Before returning subagent result to main Claude session
- Per subagent invocation

### Use Cases

**Development:**
- Validate research agent found 10+ sources
- Check code generator used Decimal (not float)
- Ensure agent completed task (didn't timeout)
- Verify validator agent flagged issues

**Production:**
- Validate variance calculation agent results
- Check report generator produced valid file
- Ensure API extraction agent logged correctly
- Verify test generator created valid tests

### Parameters
1. **AGENT_NAME** - Name of agent that completed (e.g., "research-agent", "@databricks-validator")
2. **AGENT_OUTPUT** - Full text output from agent

### Exit Codes
- **Exit 0:** Subagent output valid
- **Exit 2:** BLOCKING - output invalid (retry or escalate)
- **Other:** Warning - minor issue (user decides)

### Example: Validate Research Sources

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0
readonly BLOCKING_ERROR=2

AGENT_NAME="${1:-}"
AGENT_OUTPUT="${2:-}"

# Validate research agents found 10+ sources
if [[ "$AGENT_NAME" == "research-agent" || "$AGENT_NAME" == "Explore" ]]; then
  SOURCE_COUNT=$(echo "$AGENT_OUTPUT" | grep -c "Source:\|Reference:\|\[.*\](" || true)

  if [[ $SOURCE_COUNT -lt 10 ]]; then
    echo "ERROR: Research agent found only $SOURCE_COUNT sources (minimum 10 required)" >&2
    echo "Agent output insufficient for evidence-based recommendations" >&2
    exit "$BLOCKING_ERROR"
  fi

  echo "Research validation: $SOURCE_COUNT sources found ✅"
fi

exit "$SUCCESS"
```

### Example: Validate Decimal Usage

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0
readonly BLOCKING_ERROR=2

AGENT_NAME="${1:-}"
AGENT_OUTPUT="${2:-}"

# Validate code generators used Decimal for currency
if [[ "$AGENT_NAME" == "@script-generator" ]]; then
  if echo "$AGENT_OUTPUT" | grep -qE "float\s*\([^)]*\b(currency|price|amount|revenue|expense)\b"; then
    echo "ERROR: Code generator used float for currency calculations" >&2
    echo "Must use Decimal type per CLAUDE.md financial precision requirements" >&2
    exit "$BLOCKING_ERROR"
  fi
fi

exit "$SUCCESS"
```

### Integration Notes
- Validate critical outputs only (not every agent)
- Use for quality gates (financial precision, source count, test coverage)
- Exit 2 can trigger retry or escalation to user
- Parse AGENT_OUTPUT carefully (large text, may have structure)

---

## 6. UserPromptSubmit Hook

### When It Runs
- After user submits prompt, before Claude processes
- Can inject context, route to specialized agents, preprocess
- Once per user message

### Use Cases

**Development:**
- Detect "implement feature" → invoke RPIV workflow
- Inject reminders (Decimal for currency)
- Route code review → @code-reviewer agent
- Detect meta-infrastructure requests → warn about approval

**Production:**
- Detect "variance analysis" → load thresholds
- Preprocess complex requests
- Add workflow context
- Route to specialized agents

### Parameters
1. **USER_PROMPT** - Full text of user's prompt

### Exit Codes
- **Exit 0:** Proceed with prompt processing
- **Exit 2:** Invalid prompt (RARE - use sparingly)
- **Other:** Warning - advisory message (user sees but proceeds)

### Example: Detect Implementation Requests

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0

USER_PROMPT="${1:-}"

# Detect implementation requests → invoke RPIV workflow
if echo "$USER_PROMPT" | grep -qiE "implement|add feature|create new|build.*feature|develop"; then
  echo "INFO: Implementation request detected" >&2
  echo "RPIV workflow required: Research → Plan → Implement → Verify" >&2
  echo "Invoking enforcing-research-plan-implement-verify skill..." >&2
fi

exit "$SUCCESS"
```

### Example: Load Thresholds for Variance Analysis

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0

USER_PROMPT="${1:-}"

# Detect variance analysis → load thresholds
if echo "$USER_PROMPT" | grep -qiE "variance analysis|calculate variance|variance report"; then
  if [[ -f config/thresholds.yaml ]]; then
    echo "INFO: Variance analysis detected - Loading thresholds" >&2
    echo "Materiality: 10% or \$50,000 absolute (config/thresholds.yaml)" >&2
  fi
fi

exit "$SUCCESS"
```

### Integration Notes
- Use sparingly for exit 2 (almost never block user prompts)
- Useful for context injection (load config, remind about patterns)
- Can route to specialized agents
- Keep execution fast (< 500ms)

---

## 7. PreCompact Hook

### When It Runs
- Before context window compaction
- When conversation history gets too long
- Rare (only when context nearly full)

### Use Cases

**Development:**
- Save todo list to file
- Backup task state
- Archive conversation log
- Preserve calculation intermediates

**Production:**
- Save variance report draft
- Backup workflow state
- Serialize calculation state
- Archive session data

### Parameters
None (PreCompact receives no parameters)

### Exit Codes
- **Exit 0:** Context saved successfully
- **Exit 2:** BLOCKING - save failed (compaction prevented)
- **Other:** Warning - partial save (compaction proceeds)

### Example: Save Todo List

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0
readonly BLOCKING_ERROR=2

# Save todo list if exists
if [[ -f .claude/todos/current.json ]]; then
  mkdir -p config/workflow-state/
  BACKUP_FILE="config/workflow-state/todos-backup-$(date +%Y%m%d-%H%M%S).json"

  cp .claude/todos/current.json "$BACKUP_FILE" || {
    echo "ERROR: Failed to backup todo list" >&2
    exit "$BLOCKING_ERROR"
  }

  echo "Saved todo list to $BACKUP_FILE"
fi

exit "$SUCCESS"
```

### Integration Notes
- Runs rarely (only when context full)
- Use to preserve critical state before compaction
- Exit 2 prevents compaction (use carefully)
- Keep execution fast (compaction is time-sensitive)

---

## 8. Notification Hook

### When It Runs
- On system notifications (errors, events, alerts)
- Varies by notification type
- Asynchronous to main workflow

### Use Cases

**Development:**
- Log tool execution times
- Monitor API rate limits
- Track context window usage
- Detect anomalies

**Production:**
- Alert on financial calculation errors
- Monitor resource usage
- Track performance metrics
- Escalate critical issues

### Parameters
1. **NOTIFICATION_TYPE** - Type of notification (e.g., "tool_execution_time", "api_rate_limit")
2. **NOTIFICATION_DATA** - JSON string with notification details

### Exit Codes
- **Exit 0:** Notification handled
- **Exit 2:** Critical notification requiring escalation
- **Other:** Warning - logged but not critical

### Example: Monitor API Rate Limits

```bash
#!/bin/bash
set -euo pipefail

readonly SUCCESS=0
readonly WARNING=1

NOTIFICATION_TYPE="${1:-}"
NOTIFICATION_DATA="${2:-}"

if [[ "$NOTIFICATION_TYPE" == "api_rate_limit" ]]; then
  API_NAME=$(echo "$NOTIFICATION_DATA" | jq -r '.api // empty')
  REMAINING=$(echo "$NOTIFICATION_DATA" | jq -r '.remaining // empty')

  if [[ "$REMAINING" -lt 10 ]]; then
    echo "WARNING: API rate limit low for $API_NAME (remaining: $REMAINING)" >&2
    exit "$WARNING"
  fi
fi

exit "$SUCCESS"
```

### Integration Notes
- Most flexible hook type (varies by notification)
- Use for logging, monitoring, alerting
- Exit 2 rare (escalation only)
- May run frequently (keep lightweight)

---

## Common Patterns

### Pattern 1: Validation Chain (PreToolUse + PostToolUse)

```bash
# PreToolUse: Prevent bad input
if [[ "$TOOL_NAME" == "Write" ]]; then
  # Block float in currency code
fi

# PostToolUse: Validate output
if [[ "$TOOL_NAME" == "Write" ]]; then
  # Run linters, check syntax
fi
```

### Pattern 2: Session Bookends (SessionStart + Stop)

```bash
# SessionStart: Initialize
- Load credentials
- Check environment

# Stop: Cleanup
- Check git status
- Save state
```

### Pattern 3: Agent Validation (SubagentStop)

```bash
# After agent completes:
- Validate output quality
- Check requirements met
- Ensure no errors
```

### Pattern 4: Context Injection (UserPromptSubmit)

```bash
# Before processing prompt:
- Load relevant config
- Remind about patterns
- Route to specialized agents
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Slow PreToolUse
```bash
# BAD: Network call in PreToolUse (blocks every tool)
if [[ "$TOOL_NAME" == "Write" ]]; then
  curl -X GET https://api.example.com/validate  # SLOW!
fi
```

**Fix:** Validate locally, or move to PostToolUse

### ❌ Anti-Pattern 2: Vague Error Messages
```bash
# BAD: Unhelpful error
echo "ERROR: Something went wrong" >&2
exit 2
```

**Fix:** Be specific and actionable
```bash
echo "ERROR: Float detected in currency calculation ($FILE_PATH)" >&2
echo "Use Decimal type: from decimal import Decimal" >&2
exit 2
```

### ❌ Anti-Pattern 3: Blocking Everything
```bash
# BAD: Exit 2 for minor issues
if [[ ! -f .editorconfig ]]; then
  exit 2  # BLOCKING for missing optional file
fi
```

**Fix:** Use exit 1 (warning) for non-critical issues

---

## Summary Table

| Hook Type | When | Blocking? | Common Use Cases |
|-----------|------|-----------|------------------|
| SessionStart | Session begin | No | Load credentials, check environment |
| PreToolUse | Before tool | **YES** | Validate input, prevent destructive operations |
| PostToolUse | After tool | No | Run linters, update audit log |
| Stop | Session end | **YES** | Check git status, save state |
| SubagentStop | After agent | **YES** | Validate agent output quality |
| UserPromptSubmit | Before processing | No | Inject context, route to agents |
| PreCompact | Before compaction | No | Save critical state |
| Notification | On events | No | Log, monitor, alert |

---

**Lines:** 547 (target 300-400, acceptable for comprehensive reference)
**Last Updated:** 2025-11-10
