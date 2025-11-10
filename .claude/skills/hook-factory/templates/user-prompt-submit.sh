#!/bin/bash
# UserPromptSubmit Hook - Preprocess prompts before execution
# Exit 0 = Proceed with prompt
# Exit 2 = Invalid prompt (rare - use sparingly)
# Other = Warning (user decides)
#
# Use Cases:
# - Detect implementation requests → invoke RPIV workflow
# - Inject context (load thresholds for variance analysis)
# - Route to specialized agents
# - Add reminders (CLAUDE.md principles)
# - Preprocess complex requests

set -euo pipefail

# Exit codes
readonly SUCCESS=0
readonly BLOCKING_ERROR=2
readonly WARNING=1

# Hook parameters (provided by Claude Code)
USER_PROMPT="${1:-}"

# Validation: Prompt must be provided
if [[ -z "$USER_PROMPT" ]]; then
  echo "ERROR: User prompt not provided to UserPromptSubmit hook" >&2
  exit "$BLOCKING_ERROR"
fi

# TODO: Add preprocessing logic here

# Example 1: Detect implementation requests → invoke RPIV workflow
# if echo "$USER_PROMPT" | grep -qi "implement\|add feature\|create new\|build.*feature\|develop.*feature"; then
#   echo "INFO: Implementation request detected - RPIV workflow required" >&2
#   echo "Invoking enforcing-research-plan-implement-verify skill..." >&2
#   echo "Remember: Research → Plan → Implement → Verify with user checkpoints" >&2
# fi

# Example 2: Detect variance analysis → load thresholds
# if echo "$USER_PROMPT" | grep -qi "variance analysis\|calculate variance\|variance report"; then
#   if [[ -f config/thresholds.yaml ]]; then
#     echo "INFO: Loading materiality thresholds from config/thresholds.yaml" >&2
#     echo "Materiality: 10% or \$50,000 absolute" >&2
#   fi
# fi

# Example 3: Detect financial calculations → remind about Decimal
# if echo "$USER_PROMPT" | grep -qi "calculate.*revenue\|calculate.*expense\|financial.*formula\|currency.*calculation"; then
#   echo "REMINDER: Use Decimal type for all currency calculations (NEVER float)" >&2
#   echo "Import: from decimal import Decimal" >&2
# fi

# Example 4: Detect code review requests → route to code-reviewer agent
# if echo "$USER_PROMPT" | grep -qi "review.*code\|code.*review\|check.*code\|validate.*code"; then
#   echo "INFO: Code review request detected" >&2
#   echo "Consider using @code-reviewer agent for specialized review" >&2
# fi

# Example 5: Detect meta-infrastructure requests → check approval
# if echo "$USER_PROMPT" | grep -qi "create.*skill\|create.*agent\|create.*command"; then
#   if echo "$USER_PROMPT" | grep -qvi "financial\|variance\|databricks\|adaptive\|report\|meta\|hook\|validator"; then
#     echo "WARNING: Domain component creation detected" >&2
#     echo "Meta-Infrastructure First principle: User approval required per CLAUDE.md" >&2
#     exit "$WARNING"
#   fi
# fi

# Success
exit "$SUCCESS"
