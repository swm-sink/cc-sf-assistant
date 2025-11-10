#!/bin/bash
# Stop Hook - BLOCKING session end validation
# Exit 0 = Clean exit allowed
# Exit 2 = Block session end (uncommitted changes, unsaved state)
# Other = Warning (user decides)
#
# Use Cases:
# - Check git status (uncommitted changes)
# - Save workflow state to config/
# - Cleanup temporary files
# - Verify all tasks completed
# - Generate session summary

set -euo pipefail

# Exit codes
readonly SUCCESS=0
readonly BLOCKING_ERROR=2
readonly WARNING=1

# Hook parameters (none for Stop)

# TODO: Add cleanup logic here

# Example 1: Check for uncommitted changes (BLOCKING)
# git diff --quiet && git diff --staged --quiet
# if [[ $? -ne 0 ]]; then
#   echo "ERROR: Uncommitted changes detected" >&2
#   echo "" >&2
#   git status --short >&2
#   echo "" >&2
#   echo "Please commit or stash changes before ending session" >&2
#   exit "$BLOCKING_ERROR"
# fi

# Example 2: Check for untracked files (WARNING)
# if [[ -n $(git ls-files --others --exclude-standard) ]]; then
#   echo "WARNING: Untracked files detected" >&2
#   git ls-files --others --exclude-standard >&2
#   echo "Consider adding to .gitignore or committing" >&2
#   exit "$WARNING"
# fi

# Example 3: Save workflow state
# if [[ -f config/workflow-state/current.json ]]; then
#   cp config/workflow-state/current.json config/workflow-state/backup-$(date +%Y%m%d-%H%M%S).json
# fi

# Example 4: Cleanup temporary files
# if [[ -d /tmp/claude-session-* ]]; then
#   rm -rf /tmp/claude-session-*
# fi

# Example 5: Verify todo list complete
# if [[ -f .claude/todos/current.json ]]; then
#   PENDING_COUNT=$(jq '[.[] | select(.status != "completed")] | length' .claude/todos/current.json)
#   if [[ $PENDING_COUNT -gt 0 ]]; then
#     echo "WARNING: $PENDING_COUNT pending todos remain" >&2
#     jq -r '.[] | select(.status != "completed") | "- [\(.status)] \(.content)"' .claude/todos/current.json >&2
#     exit "$WARNING"
#   fi
# fi

# Success
echo "Session cleanup complete"
exit "$SUCCESS"
