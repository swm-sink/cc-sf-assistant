# Production FP&A Workflow Hooks Reference

**Purpose:** Practical production hooks for FP&A automation workflows, data extraction, report generation, and audit trails.

**Audience:** FP&A teams implementing hooks for financial workflow automation

---

## Data Extraction Hooks

### Databricks Credentials Validator (SessionStart)

**Use Case:** Verify Databricks credentials loaded before data extraction

```bash
#!/bin/bash
# hooks/session-start-databricks-credentials.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

DATABRICKS_CREDS="config/credentials/databricks.json"

if [[ ! -f "$DATABRICKS_CREDS" ]]; then
  echo "ERROR: Missing Databricks credentials" >&2
  echo "Required: $DATABRICKS_CREDS" >&2
  echo "See config/credentials/README.md for setup instructions" >&2
  exit "$BLOCKING_ERROR"
fi

# Validate JSON syntax
if ! jq empty "$DATABRICKS_CREDS" 2>/dev/null; then
  echo "ERROR: Invalid JSON in $DATABRICKS_CREDS" >&2
  exit "$BLOCKING_ERROR"
fi

# Check required fields
REQUIRED_FIELDS=("server_hostname" "http_path" "access_token")
for field in "${REQUIRED_FIELDS[@]}"; do
  if ! jq -e ".$field" "$DATABRICKS_CREDS" &>/dev/null; then
    echo "ERROR: Missing required field '$field' in $DATABRICKS_CREDS" >&2
    exit "$BLOCKING_ERROR"
  fi
done

echo "✅ Databricks credentials valid"
exit "$SUCCESS"
```

---

### Adaptive Insights Credentials Validator (SessionStart)

**Use Case:** Verify Adaptive Insights API credentials

```bash
#!/bin/bash
# hooks/session-start-adaptive-credentials.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

ADAPTIVE_CREDS="config/credentials/adaptive.json"

if [[ ! -f "$ADAPTIVE_CREDS" ]]; then
  echo "ERROR: Missing Adaptive Insights credentials" >&2
  echo "Required: $ADAPTIVE_CREDS" >&2
  echo "See config/credentials/README.md for setup instructions" >&2
  exit "$BLOCKING_ERROR"
fi

# Validate JSON syntax
if ! jq empty "$ADAPTIVE_CREDS" 2>/dev/null; then
  echo "ERROR: Invalid JSON in $ADAPTIVE_CREDS" >&2
  exit "$BLOCKING_ERROR"
fi

# Check required fields
REQUIRED_FIELDS=("api_endpoint" "api_token" "instance_code")
for field in "${REQUIRED_FIELDS[@]}"; do
  if ! jq -e ".$field" "$ADAPTIVE_CREDS" &>/dev/null; then
    echo "ERROR: Missing required field '$field' in $ADAPTIVE_CREDS" >&2
    exit "$BLOCKING_ERROR"
  fi
done

echo "✅ Adaptive Insights credentials valid"
exit "$SUCCESS"
```

---

### Threshold Configuration Loader (UserPromptSubmit)

**Use Case:** Auto-load thresholds when variance analysis mentioned

```bash
#!/bin/bash
# hooks/user-prompt-submit-thresholds.sh
set -euo pipefail

readonly SUCCESS=0

USER_PROMPT="${1:-}"

if echo "$USER_PROMPT" | grep -qiE "variance analysis|calculate variance|variance report"; then
  if [[ -f config/thresholds.yaml ]]; then
    echo "INFO: Variance analysis detected - Loading thresholds" >&2
    echo "" >&2
    echo "Materiality Thresholds (config/thresholds.yaml):" >&2
    echo "  - Percentage: 10%" >&2
    echo "  - Absolute: \$50,000" >&2
    echo "" >&2
  else
    echo "WARNING: config/thresholds.yaml not found" >&2
    echo "Using default thresholds: 10% or \$50,000" >&2
  fi
fi

exit "$SUCCESS"
```

---

## Financial Precision Hooks

### Decimal Enforcement (PreToolUse)

**Use Case:** Block float usage in financial calculation code (BLOCKING)

```bash
#!/bin/bash
# hooks/pre-tool-use-decimal-enforcement.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  # Enforce Decimal in core financial logic
  if [[ "$FILE_PATH" == scripts/core/* ]]; then
    CONTENT=$(echo "$TOOL_PARAMS" | jq -r '.content // .new_string // empty')

    # Check for float usage with financial keywords
    if echo "$CONTENT" | grep -qE "float\s*\([^)]*\b(variance|revenue|expense|budget|actual|forecast|currency|price|amount|cost)\b"; then
      echo "ERROR: Float detected in financial calculation ($FILE_PATH)" >&2
      echo "" >&2
      echo "Financial calculations require Decimal type for precision:" >&2
      echo "  from decimal import Decimal" >&2
      echo "  variance = Decimal('100.00')  # NOT float(100.0)" >&2
      echo "" >&2
      echo "Rationale: Float causes rounding errors (0.1 + 0.2 ≠ 0.3)" >&2
      echo "Per CLAUDE.md financial precision requirements (Story 0.1)" >&2
      exit "$BLOCKING_ERROR"
    fi
  fi
fi

exit "$SUCCESS"
```

---

### Variance Calculation Validator (SubagentStop)

**Use Case:** Validate variance calculation agent used Decimal

```bash
#!/bin/bash
# hooks/subagent-stop-variance-validator.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

AGENT_NAME="${1:-}"
AGENT_OUTPUT="${2:-}"

if [[ "$AGENT_NAME" == "@variance-calculator" || "$AGENT_NAME" == "variance-agent" ]]; then
  # Check agent used Decimal
  if echo "$AGENT_OUTPUT" | grep -qE "float\s*\([^)]*\b(variance|revenue|expense|budget|actual)\b"; then
    echo "ERROR: Variance calculation agent used float (not Decimal)" >&2
    echo "Financial calculations must use Decimal type" >&2
    exit "$BLOCKING_ERROR"
  fi

  # Check materiality threshold applied
  if ! echo "$AGENT_OUTPUT" | grep -qi "materiality\|threshold\|significant"; then
    echo "WARNING: No materiality threshold mentioned in variance calculation" >&2
    echo "Consider applying 10% or \$50,000 threshold per config/thresholds.yaml" >&2
    exit 1
  fi

  echo "✅ Variance calculation validation passed"
fi

exit "$SUCCESS"
```

---

## Report Generation Hooks

### Report Structure Validator (PreToolUse)

**Use Case:** Validate report structure before generation

```bash
#!/bin/bash
# hooks/pre-tool-use-report-validator.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Write" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  # Validate report generation code
  if [[ "$FILE_PATH" == scripts/workflows/*report*.py ]]; then
    CONTENT=$(echo "$TOOL_PARAMS" | jq -r '.content // empty')

    # Check for required columns
    REQUIRED_COLUMNS=("Account" "Budget" "Actual" "Variance" "Variance %")
    MISSING_COLUMNS=()

    for col in "${REQUIRED_COLUMNS[@]}"; do
      if ! echo "$CONTENT" | grep -q "$col"; then
        MISSING_COLUMNS+=("$col")
      fi
    done

    if [[ ${#MISSING_COLUMNS[@]} -gt 0 ]]; then
      echo "ERROR: Report missing required columns: ${MISSING_COLUMNS[*]}" >&2
      echo "Per spec.md Story 1.3 variance report requirements" >&2
      exit "$BLOCKING_ERROR"
    fi
  fi
fi

exit "$SUCCESS"
```

---

### Excel Format Validator (PostToolUse)

**Use Case:** Validate Excel file structure after generation

```bash
#!/bin/bash
# hooks/post-tool-use-excel-validator.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Bash" ]]; then
  COMMAND=$(echo "$TOOL_PARAMS" | jq -r '.command // empty')

  # Detect report generation commands
  if echo "$COMMAND" | grep -q "generate.*report\|create.*excel"; then
    # Find generated .xlsx files in output/
    REPORTS=$(find output/ -name "*.xlsx" -mmin -1 2>/dev/null || echo "")

    if [[ -z "$REPORTS" ]]; then
      echo "ERROR: Report generation completed but no .xlsx file found in output/" >&2
      exit "$BLOCKING_ERROR"
    fi

    for report in $REPORTS; do
      # Validate Excel file is not corrupted
      if command -v python3 &> /dev/null; then
        python3 -c "import openpyxl; openpyxl.load_workbook('$report')" 2>/dev/null || {
          echo "ERROR: Invalid Excel file: $report" >&2
          exit "$BLOCKING_ERROR"
        }
        echo "✅ Excel file valid: $report"
      fi
    done
  fi
fi

exit "$SUCCESS"
```

---

## Audit Trail Hooks

### Transformation Logger (PostToolUse)

**Use Case:** Log all data transformations to audit trail

```bash
#!/bin/bash
# hooks/post-tool-use-audit-logger.sh
set -euo pipefail

readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

# Log Write operations on workflows/ and core/
if [[ "$TOOL_NAME" == "Write" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  if [[ "$FILE_PATH" == scripts/workflows/* || "$FILE_PATH" == scripts/core/* ]]; then
    # Ensure audit log exists
    if [[ ! -f config/audit.log ]]; then
      touch config/audit.log
    fi

    # Log transformation
    TIMESTAMP=$(date -Iseconds)
    USER="${USER:-unknown}"
    echo "$TIMESTAMP | $USER | $TOOL_NAME | $FILE_PATH" >> config/audit.log

    echo "✅ Logged transformation to audit trail"
  fi
fi

exit "$SUCCESS"
```

---

### Audit Log Validator (Stop)

**Use Case:** Verify audit log integrity on session end

```bash
#!/bin/bash
# hooks/stop-audit-validator.sh
set -euo pipefail

readonly WARNING=1
readonly SUCCESS=0

if [[ -f config/audit.log ]]; then
  # Check audit log is not empty
  if [[ ! -s config/audit.log ]]; then
    echo "WARNING: Audit log exists but is empty" >&2
    exit "$WARNING"
  fi

  # Count entries from this session
  SESSION_START=$(date +%Y-%m-%d)
  ENTRY_COUNT=$(grep -c "$SESSION_START" config/audit.log || echo "0")

  if [[ $ENTRY_COUNT -eq 0 ]]; then
    echo "WARNING: No audit log entries for today" >&2
    exit "$WARNING"
  fi

  echo "✅ Audit log valid: $ENTRY_COUNT entries today"
fi

exit "$SUCCESS"
```

---

## Data Validation Hooks

### Account Name Validator (PreToolUse)

**Use Case:** Validate account naming convention before processing

```bash
#!/bin/bash
# hooks/pre-tool-use-account-validator.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Bash" ]]; then
  COMMAND=$(echo "$TOOL_PARAMS" | jq -r '.command // empty')

  # Detect account consolidation commands
  if echo "$COMMAND" | grep -q "consolidate.*accounts\|merge.*accounts"; then
    # Extract file paths from command
    BUDGET_FILE=$(echo "$COMMAND" | grep -oP 'budget[^\s]*\.xlsx' || echo "")
    ACTUALS_FILE=$(echo "$COMMAND" | grep -oP 'actuals[^\s]*\.xlsx' || echo "")

    if [[ -n "$BUDGET_FILE" && -n "$ACTUALS_FILE" ]]; then
      # Validate files exist
      if [[ ! -f "$BUDGET_FILE" ]]; then
        echo "ERROR: Budget file not found: $BUDGET_FILE" >&2
        exit "$BLOCKING_ERROR"
      fi
      if [[ ! -f "$ACTUALS_FILE" ]]; then
        echo "ERROR: Actuals file not found: $ACTUALS_FILE" >&2
        exit "$BLOCKING_ERROR"
      fi

      echo "✅ Account consolidation files validated"
    fi
  fi
fi

exit "$SUCCESS"
```

---

### Materiality Threshold Enforcer (UserPromptSubmit)

**Use Case:** Remind about materiality thresholds for variance analysis

```bash
#!/bin/bash
# hooks/user-prompt-submit-materiality.sh
set -euo pipefail

readonly SUCCESS=0

USER_PROMPT="${1:-}"

if echo "$USER_PROMPT" | grep -qiE "variance|material|significant|threshold"; then
  echo "REMINDER: Materiality Thresholds (config/thresholds.yaml)" >&2
  echo "  - Percentage: 10% variance" >&2
  echo "  - Absolute: \$50,000 absolute difference" >&2
  echo "  - Apply both thresholds (either condition triggers materiality)" >&2
fi

exit "$SUCCESS"
```

---

## Workflow State Hooks

### Variance Report State Saver (PreCompact)

**Use Case:** Save in-progress variance report before context compaction

```bash
#!/bin/bash
# hooks/pre-compact-variance-saver.sh
set -euo pipefail

readonly BLOCKING_ERROR=2
readonly SUCCESS=0

# Save variance report draft if exists
if [[ -f /tmp/variance-report-draft.xlsx ]]; then
  mkdir -p config/workflow-state/
  BACKUP_FILE="config/workflow-state/variance-draft-$(date +%Y%m%d-%H%M%S).xlsx"

  cp /tmp/variance-report-draft.xlsx "$BACKUP_FILE" || {
    echo "ERROR: Failed to backup variance report draft" >&2
    exit "$BLOCKING_ERROR"
  }

  echo "✅ Saved variance report draft to $BACKUP_FILE"
fi

# Save calculation state
if [[ -f /tmp/calculation-state.json ]]; then
  mkdir -p config/workflow-state/
  CALC_FILE="config/workflow-state/calculations-$(date +%Y%m%d-%H%M%S).json"
  cp /tmp/calculation-state.json "$CALC_FILE"
  echo "✅ Saved calculation state to $CALC_FILE"
fi

exit "$SUCCESS"
```

---

## Performance Monitoring Hooks

### API Rate Limit Monitor (Notification)

**Use Case:** Alert when Databricks/Adaptive API rate limits low

```bash
#!/bin/bash
# hooks/notification-api-rate-limit.sh
set -euo pipefail

readonly WARNING=1
readonly SUCCESS=0

NOTIFICATION_TYPE="${1:-}"
NOTIFICATION_DATA="${2:-}"

if [[ "$NOTIFICATION_TYPE" == "api_rate_limit" ]]; then
  API_NAME=$(echo "$NOTIFICATION_DATA" | jq -r '.api // empty')
  REMAINING=$(echo "$NOTIFICATION_DATA" | jq -r '.remaining // empty')
  LIMIT=$(echo "$NOTIFICATION_DATA" | jq -r '.limit // empty')

  USAGE_PERCENT=$((100 - (REMAINING * 100 / LIMIT)))

  if [[ $USAGE_PERCENT -gt 80 ]]; then
    echo "WARNING: $API_NAME rate limit at ${USAGE_PERCENT}% ($REMAINING / $LIMIT remaining)" >&2
    echo "Consider throttling requests or waiting for reset" >&2
    exit "$WARNING"
  fi

  echo "✅ $API_NAME rate limit OK: $REMAINING / $LIMIT remaining"
fi

exit "$SUCCESS"
```

---

### Data Extraction Timer (Notification)

**Use Case:** Alert on slow data extraction

```bash
#!/bin/bash
# hooks/notification-extraction-timer.sh
set -euo pipefail

readonly WARNING=1
readonly SUCCESS=0

NOTIFICATION_TYPE="${1:-}"
NOTIFICATION_DATA="${2:-}"

if [[ "$NOTIFICATION_TYPE" == "tool_execution_time" ]]; then
  TOOL_NAME=$(echo "$NOTIFICATION_DATA" | jq -r '.tool // empty')
  DURATION=$(echo "$NOTIFICATION_DATA" | jq -r '.duration // 0')

  # Alert on slow Bash commands (likely data extraction)
  if [[ "$TOOL_NAME" == "Bash" && $DURATION -gt 30000 ]]; then
    DURATION_SEC=$((DURATION / 1000))
    echo "WARNING: Slow data extraction - took ${DURATION_SEC}s" >&2
    echo "Consider adding timeout or optimizing query" >&2
    exit "$WARNING"
  fi
fi

exit "$SUCCESS"
```

---

## Summary

**Data Extraction:**
- Databricks credentials validator (SessionStart - BLOCKING)
- Adaptive credentials validator (SessionStart - BLOCKING)
- Threshold configuration loader (UserPromptSubmit - informational)

**Financial Precision:**
- Decimal enforcement (PreToolUse - BLOCKING)
- Variance calculation validator (SubagentStop - BLOCKING)

**Report Generation:**
- Report structure validator (PreToolUse - BLOCKING)
- Excel format validator (PostToolUse - BLOCKING)

**Audit Trail:**
- Transformation logger (PostToolUse - informational)
- Audit log validator (Stop - warning)

**Data Validation:**
- Account name validator (PreToolUse - BLOCKING)
- Materiality threshold enforcer (UserPromptSubmit - reminder)

**Workflow State:**
- Variance report state saver (PreCompact - BLOCKING)

**Performance:**
- API rate limit monitor (Notification - warning)
- Data extraction timer (Notification - warning)

---

**Lines:** 480
**Last Updated:** 2025-11-10
