#!/bin/bash
# PreToolUse Hook - BLOCKING validation before tool execution
# Exit 0 = Allow tool execution
# Exit 2 = Block tool execution (stderr fed to Claude for fixing)
# Other = Warning (user decides)
#
# Use Cases:
# - Validate file permissions before Write/Edit
# - Check for float usage in currency code
# - Enforce naming conventions
# - Validate data before Bash commands
# - Prevent destructive operations

set -euo pipefail

# Exit codes
readonly SUCCESS=0
readonly BLOCKING_ERROR=2
readonly WARNING=1

# Hook parameters (provided by Claude Code)
TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

# Validation: Tool name must be provided
if [[ -z "$TOOL_NAME" ]]; then
  echo "ERROR: Tool name not provided to PreToolUse hook" >&2
  exit "$BLOCKING_ERROR"
fi

# TODO: Add validation logic here

# Example 1: Block Write on read-only files
# if [[ "$TOOL_NAME" == "Write" ]]; then
#   FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')
#   if [[ -f "$FILE_PATH" && ! -w "$FILE_PATH" ]]; then
#     echo "ERROR: Cannot write to read-only file: $FILE_PATH" >&2
#     exit "$BLOCKING_ERROR"
#   fi
# fi

# Example 2: Block float usage in currency code
# if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
#   FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')
#   if [[ "$FILE_PATH" == scripts/core/* ]]; then
#     CONTENT=$(echo "$TOOL_PARAMS" | jq -r '.content // .new_string // empty')
#     if echo "$CONTENT" | grep -q "float(.*currency\|price\|amount\|revenue\|expense\|budget\|actual)"; then
#       echo "ERROR: Float detected in currency calculation ($FILE_PATH)" >&2
#       echo "Use Decimal type for financial precision per CLAUDE.md" >&2
#       echo "Import: from decimal import Decimal" >&2
#       exit "$BLOCKING_ERROR"
#     fi
#   fi
# fi

# Example 3: Validate Bash commands against allowed list
# if [[ "$TOOL_NAME" == "Bash" ]]; then
#   COMMAND=$(echo "$TOOL_PARAMS" | jq -r '.command // empty')
#   if echo "$COMMAND" | grep -q "rm -rf /"; then
#     echo "ERROR: Destructive command detected: $COMMAND" >&2
#     exit "$BLOCKING_ERROR"
#   fi
# fi

# Example 4: Check file permissions before Edit
# if [[ "$TOOL_NAME" == "Edit" ]]; then
#   FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')
#   if [[ ! -f "$FILE_PATH" ]]; then
#     echo "ERROR: File does not exist: $FILE_PATH" >&2
#     echo "Use Write tool for new files, not Edit" >&2
#     exit "$BLOCKING_ERROR"
#   fi
# fi

# Success - allow tool execution
exit "$SUCCESS"
