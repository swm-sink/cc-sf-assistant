#!/bin/bash
# SubagentStop Hook - BLOCKING subagent completion validation
# Exit 0 = Subagent output valid
# Exit 2 = Subagent output invalid (retry recommended)
# Other = Warning (user decides)
#
# Use Cases:
# - Validate research agent found required sources
# - Verify code generation agent produced valid code
# - Check validator agent flagged issues
# - Ensure agent followed instructions
# - Aggregate multi-agent results

set -euo pipefail

# Exit codes
readonly SUCCESS=0
readonly BLOCKING_ERROR=2
readonly WARNING=1

# Hook parameters (provided by Claude Code)
AGENT_NAME="${1:-}"
AGENT_OUTPUT="${2:-}"

# Validation: Agent name must be provided
if [[ -z "$AGENT_NAME" ]]; then
  echo "ERROR: Agent name not provided to SubagentStop hook" >&2
  exit "$BLOCKING_ERROR"
fi

# TODO: Add validation logic here

# Example 1: Validate research agent found 10+ sources
# if [[ "$AGENT_NAME" == "research-agent" || "$AGENT_NAME" == "Explore" ]]; then
#   SOURCE_COUNT=$(echo "$AGENT_OUTPUT" | grep -c "Source:\|Reference:\|\[.*\](" || true)
#   if [[ $SOURCE_COUNT -lt 10 ]]; then
#     echo "ERROR: Research agent found only $SOURCE_COUNT sources (minimum 10 required)" >&2
#     echo "Agent needs to search more comprehensively" >&2
#     exit "$BLOCKING_ERROR"
#   fi
# fi

# Example 2: Verify code generator used Decimal (not float)
# if [[ "$AGENT_NAME" == "script-generator" || "$AGENT_NAME" == "@script-generator" ]]; then
#   if echo "$AGENT_OUTPUT" | grep -q "float(.*currency\|price\|amount\|revenue\|expense)"; then
#     echo "ERROR: Code generator used float for currency calculations" >&2
#     echo "Must use Decimal type per CLAUDE.md financial precision requirements" >&2
#     exit "$BLOCKING_ERROR"
#   fi
# fi

# Example 3: Check validator agent flagged issues
# if [[ "$AGENT_NAME" == "@databricks-validator" || "$AGENT_NAME" == "@adaptive-validator" ]]; then
#   if ! echo "$AGENT_OUTPUT" | grep -q "VALIDATION:"; then
#     echo "WARNING: Validator agent did not provide validation results" >&2
#     exit "$WARNING"
#   fi
# fi

# Example 4: Ensure agent completed task (didn't hit timeout)
# if echo "$AGENT_OUTPUT" | grep -qi "timeout\|interrupted\|incomplete"; then
#   echo "ERROR: Agent task incomplete or timed out" >&2
#   echo "Consider increasing timeout or breaking task into smaller steps" >&2
#   exit "$BLOCKING_ERROR"
# fi

# Example 5: Validate file created by generator exists
# if [[ "$AGENT_NAME" == "@script-generator" || "$AGENT_NAME" == "@test-generator" ]]; then
#   FILE_PATH=$(echo "$AGENT_OUTPUT" | grep -oP 'Created: \K[^\s]+' || echo "")
#   if [[ -n "$FILE_PATH" && ! -f "$FILE_PATH" ]]; then
#     echo "ERROR: Agent claimed to create $FILE_PATH but file not found" >&2
#     exit "$BLOCKING_ERROR"
#   fi
# fi

# Success
exit "$SUCCESS"
