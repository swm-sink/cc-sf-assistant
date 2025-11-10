# Continuous Validation Reference

**Purpose:** Hook integration for automatic validation after component creation/modification.

---

## PostToolUse Hook Integration

**Hook Location:** `.claude/hooks/post-tool-use.sh`

**Trigger:** After Write/Edit on `.claude/skills/**, .claude/agents/**, .claude/commands/**`

**Logic:**
```bash
#!/bin/bash
TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
  FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // empty')

  # Validate .claude components
  if [[ "$FILE_PATH" == .claude/skills/* || "$FILE_PATH" == .claude/agents/* || "$FILE_PATH" == .claude/commands/* ]]; then
    echo "INFO: Running System Coherence Validator on $FILE_PATH" >&2
    # Run validators (non-blocking, report only)
  fi
fi
```

---

## User Override

**Always available:**
- User can skip validation: "Skip validation for now"
- User can invoke manually: "validate system"
- Validation never BLOCKS (report issues for user decision)

---

## Auto-Invoke via CSO

**Trigger phrases** automatically invoke validator:
- "validate system"
- "check coherence"
- "run validation"

---

**Lines:** 35
**Last Updated:** 2025-11-10
