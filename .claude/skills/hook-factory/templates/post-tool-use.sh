#!/bin/bash
# PostToolUse Hook - Validation after Write/Edit/Bash execution
# Exit 0 = Validation passed
# Exit 2 = Validation failed (rollback recommended)
# Other = Warning (user decides)
#
# Use Cases:
# - Run linters after Write/Edit (ruff, mypy)
# - Update audit logs after data transformations
# - Validate output file structure
# - Run tests after code changes
# - Generate documentation

set -euo pipefail

# Exit codes
readonly SUCCESS=0
readonly BLOCKING_ERROR=2
readonly WARNING=1

# Hook parameters (provided by Claude Code)
TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"
TOOL_RESULT="${3:-}"

# Validation: Tool name must be provided
if [[ -z "$TOOL_NAME" ]]; then
  echo "ERROR: Tool name not provided to PostToolUse hook" >&2
  exit "$BLOCKING_ERROR"
fi

# TODO: Add validation logic here

# Example 1: Run ruff formatter after Write/Edit on Python files
# if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
#   FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')
#   if [[ "$FILE_PATH" == *.py ]]; then
#     if command -v ruff &> /dev/null; then
#       ruff format "$FILE_PATH" || {
#         echo "ERROR: Ruff formatter failed on $FILE_PATH" >&2
#         exit "$BLOCKING_ERROR"
#       }
#     fi
#   fi
# fi

# Example 2: Update audit log after data transformation
# if [[ "$TOOL_NAME" == "Write" && "$FILE_PATH" == scripts/workflows/* ]]; then
#   FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')
#   echo "$(date -Iseconds) | $USER | $TOOL_NAME | $FILE_PATH" >> config/audit.log
# fi

# Example 3: Validate YAML syntax after Edit
# if [[ "$TOOL_NAME" == "Edit" ]]; then
#   FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')
#   if [[ "$FILE_PATH" == *.yaml || "$FILE_PATH" == *.yml ]]; then
#     if command -v yamllint &> /dev/null; then
#       yamllint "$FILE_PATH" || {
#         echo "ERROR: Invalid YAML syntax in $FILE_PATH" >&2
#         exit "$BLOCKING_ERROR"
#       }
#     fi
#   fi
# fi

# Example 4: Run mypy after Write on scripts/
# if [[ "$TOOL_NAME" == "Write" ]]; then
#   FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')
#   if [[ "$FILE_PATH" == scripts/*.py ]]; then
#     if command -v mypy &> /dev/null; then
#       mypy --strict "$FILE_PATH" || {
#         echo "WARNING: Mypy type checking failed on $FILE_PATH" >&2
#         echo "Consider fixing type hints for better code quality" >&2
#         exit "$WARNING"
#       }
#     fi
#   fi
# fi

# Example 5: Invoke System Coherence Validator after Write on .claude/
# if [[ "$TOOL_NAME" == "Write" ]]; then
#   FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')
#   if [[ "$FILE_PATH" == .claude/skills/* || "$FILE_PATH" == .claude/agents/* || "$FILE_PATH" == .claude/commands/* ]]; then
#     echo "INFO: Invoking System Coherence Validator on $FILE_PATH" >&2
#     # Validator invocation would happen here
#   fi
# fi

# Success
exit "$SUCCESS"
