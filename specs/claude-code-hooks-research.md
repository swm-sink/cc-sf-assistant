# Claude Code Hooks: Comprehensive Research Report

**Research Date:** 2025-11-10
**Objective:** Document comprehensive Claude Code hooks capabilities for deterministic behavior and enhanced functionality in FP&A automation workflows

---

## Executive Summary

Claude Code hooks are user-defined shell commands that execute automatically at specific lifecycle points, providing **deterministic, programmatic control** over AI agent behavior. Released June 30, 2025, hooks transform polite suggestions ("please run tests") into guaranteed actions that execute every time.

**Key Finding:** Hooks enable financial automation workflows to enforce validation, maintain audit trails, and prevent errors through automated quality gates—critical for FP&A systems requiring precision and compliance.

---

## 1. Authoritative Sources (15+ Identified)

### Official Documentation

1. **Claude Code Hooks Reference**
   URL: `https://docs.claude.com/en/docs/claude-code/hooks`
   Coverage: Complete API reference for all 8 hook events, exit codes, JSON schemas

2. **Claude Code Hooks Guide (Getting Started)**
   URL: `https://docs.claude.com/en/docs/claude-code/hooks-guide`
   Coverage: Quickstart examples, configuration patterns, best practices

3. **Claude Code Security Documentation**
   URL: `https://docs.claude.com/en/docs/claude-code/security`
   Coverage: Permission systems, security best practices, hook safety

4. **Claude Code Best Practices (Anthropic Engineering)**
   URL: `https://www.anthropic.com/engineering/claude-code-best-practices`
   Coverage: Production deployment patterns, workflow automation

### Community Repositories

5. **disler/claude-code-hooks-mastery**
   URL: `https://github.com/disler/claude-code-hooks-mastery`
   Coverage: All 8 hook events with JSON payloads, UV single-file scripts, deterministic control patterns

6. **johnlindquist/claude-hooks**
   URL: `https://github.com/johnlindquist/claude-hooks`
   Coverage: TypeScript-powered hooks with full type safety and auto-completion

7. **hesreallyhim/awesome-claude-code**
   URL: `https://github.com/hesreallyhim/awesome-claude-code`
   Coverage: Curated collection of hooks, commands, workflows

8. **disler/claude-code-hooks-multi-agent-observability**
   URL: `https://github.com/disler/claude-code-hooks-multi-agent-observability`
   Coverage: Real-time monitoring through hook event tracking

9. **decider/claude-hooks**
   URL: `https://github.com/decider/claude-hooks`
   Coverage: Python-based hooks for validation, quality checks, notifications

10. **carlrannaberg/claudekit**
    URL: `https://github.com/carlrannaberg/claudekit`
    Coverage: File-guard, unused parameter detection hooks

### Technical Articles & Tutorials

11. **GitButler Blog: Automate Your AI Workflows**
    URL: `https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks`
    Coverage: Practical automation patterns, workflow integration

12. **Medium: Claude Code Hooks - Making AI Gen Deterministic**
    URL: `https://medium.com/@richardhightower/claude-code-hooks-making-ai-gen-deterministic-ad4779c3a801`
    Coverage: Deterministic behavior patterns, exit code strategies

13. **Steve Kinney: Claude Code Hooks Course**
    URL: `https://stevekinney.com/courses/ai-development/claude-code-hooks`
    Coverage: Hook control flow, permissions, examples

14. **ClaudeLog Documentation**
    URL: `https://claudelog.com/mechanics/hooks/`
    Coverage: Hook mechanics, FAQs, implementation patterns

15. **Francis Bourre's Hook Schema Gist**
    URL: `https://gist.github.com/FrancisBourre/50dca37124ecc43eaf08328cdcccdb34`
    Coverage: Precise JSON schema for all hook payloads

### Additional Resources

16. **Backslash Security: Claude Code Security Best Practices**
    Coverage: Security patterns, PreToolUse blocking, permission configs

17. **eesel AI: Complete Guide to Hooks**
    Coverage: Development workflow automation, configuration examples

18. **Superagent Documentation**
    URL: `https://docs.superagent.sh/examples/claude-code-userprompt`
    Coverage: Security integration with UserPromptSubmit hooks

---

## 2. Hook Types Available in Claude Code

Claude Code provides **8 lifecycle hook events**:

### 2.1 UserPromptSubmit

**Trigger:** When user submits a prompt, before Claude processes it

**Capabilities:**
- Add additional context visible to Claude
- Validate prompts for dangerous patterns
- Block prompts (exit code 2)
- Inject security scanning
- Log prompt history with timestamps

**Input Payload:**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "user's input text"
}
```

**Output Control:**
```json
{
  "decision": "block",
  "reason": "Explanation shown to Claude",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Context appended to prompt"
  }
}
```

**Exit Code Behavior:**
- `0`: stdout added as context before Claude sees prompt
- `2`: Block prompt; stderr shown to user
- Other: Non-blocking error

### 2.2 PreToolUse

**Trigger:** After Claude creates tool parameters, before tool execution

**Capabilities:**
- **BLOCKING**: Prevent dangerous commands
- Validate tool inputs
- Modify tool parameters (v2.0.10+)
- Enforce security policies
- Implement sandboxing

**Input Payload:**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash|Edit|Write|Read|etc",
  "tool_input": {
    // Tool-specific parameters
    // Bash: { "command": "..." }
    // Edit: { "file_path": "...", "old_string": "...", "new_string": "..." }
  }
}
```

**Output Control:**
```json
{
  "decision": "approve" | "block",
  "reason": "Explanation fed back to Claude",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "string"
  }
}
```

**Matcher Patterns:**
- Simple: `"Bash"` - exact match
- Regex: `"Edit|Write"` - multiple tools
- Wildcard: `"*"` - all tools
- MCP: `"mcp__memory__.*"` - all tools from MCP server

**Exit Code Behavior:**
- `0`: Allow tool execution
- `2`: **BLOCK** tool; stderr fed to Claude
- Other: Non-blocking error

### 2.3 PostToolUse

**Trigger:** Immediately after tool completes successfully

**Capabilities:**
- Auto-format code (Prettier, Black, Ruff)
- Run tests automatically
- Validate outputs
- Log completed operations
- Trigger downstream workflows

**Input Payload:**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "PostToolUse",
  "tool_name": "string",
  "tool_input": { /* original parameters */ },
  "tool_response": { /* tool execution result */ }
}
```

**Output Control:**
```json
{
  "decision": "block",
  "reason": "Guide Claude's next steps"
}
```

**Note:** Tool has already executed; cannot retroactively block, but can influence Claude's subsequent actions.

**Matcher Support:** Same as PreToolUse

### 2.4 Notification

**Trigger:** When Claude Code sends notifications

**Notification Types:**
- Permission requests ("Claude needs your permission to use Bash")
- Idle prompts (60+ seconds of inactivity)

**Capabilities:**
- Display desktop notifications (macOS, Linux, Windows)
- Play sounds/TTS announcements
- Send alerts to external systems
- Log notification events

**Input Payload:**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "Notification",
  "message": "Notification text"
}
```

**Note:** Informational only; cannot block notifications

### 2.5 Stop

**Trigger:** When main Claude Code agent finishes responding (not on user interrupts)

**Capabilities:**
- **BLOCKING**: Force continuation with guidance
- Generate AI completion messages
- Play TTS completion announcements
- Log session metrics
- Trigger post-session workflows

**Input Payload:**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "Stop",
  "stop_hook_active": boolean  // Prevent infinite continuation
}
```

**Output Control:**
```json
{
  "decision": "block",
  "reason": "Instructions to Claude on what to do next"
}
```

**Exit Code 2:** Block stopping; `reason` guides Claude's continuation

**Prompt-Based Hook Support:** YES (uses Haiku for intelligent evaluation)

### 2.6 SubagentStop

**Trigger:** When a subagent completes its task

**Capabilities:** Identical to Stop hook, but for subagents

**Input Payload:** Same structure as Stop hook

**Output Control:** Same as Stop hook

**Prompt-Based Hook Support:** YES

### 2.7 PreCompact

**Trigger:** Before Claude Code compacts context (when context window fills)

**Capabilities:**
- Backup transcript before compaction
- Preserve critical context
- Log compaction events
- Restore state after compaction

**Input Payload:**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "PreCompact",
  "permission_mode": "string",
  "trigger": "manual" | "auto",
  "custom_instructions": "string"
}
```

**Note:** Cannot block compaction; informational/backup purposes

### 2.8 SessionStart

**Trigger:** When Claude Code starts new session or resumes existing session

**Capabilities:**
- Load development context (git status, recent issues)
- Install/sync dependencies (npm, pip, bundle)
- Initialize environment variables
- Display project status
- Inject session-wide context

**Input Payload:**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "SessionStart",
  "source": "startup" | "resume" | "clear"
}
```

**Exit Code Behavior:**
- `0`: stdout added as context for entire session
- Other: Error logged but session continues

**Note:** No matcher support; always executes

---

## 3. Configuration Patterns and Examples

### 3.1 Settings File Hierarchy

Claude Code hooks configured in:

```
~/.claude/settings.json          # User settings (all projects)
.claude/settings.json            # Project settings (team-shared, in git)
.claude/settings.local.json      # Local project settings (personal, .gitignored)
```

**Priority:** Local > Project > User

### 3.2 Basic Configuration Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",  // PreToolUse/PostToolUse only
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.sh",
            "timeout": 30  // Optional, seconds
          }
        ]
      }
    ]
  }
}
```

### 3.3 Exit Code Patterns

**Universal Exit Code Contract:**

- **Exit 0**: Success
  - Stdout visible in transcript (Ctrl-R)
  - For `UserPromptSubmit`/`SessionStart`: stdout adds context to Claude

- **Exit 2**: Blocking error
  - Stderr fed back to Claude (PreToolUse) or user (UserPromptSubmit)
  - Prevents tool execution (PreToolUse)
  - Prevents prompt processing (UserPromptSubmit)
  - Prevents stopping (Stop/SubagentStop)

- **Other non-zero**: Non-blocking error
  - Stderr shown to user
  - Execution continues

### 3.4 JSON Output Control

**Common Fields (All Hooks):**

```json
{
  "continue": false,           // Halt execution entirely
  "stopReason": "message",     // Custom stop message
  "suppressOutput": true       // Hide stdout from transcript
}
```

**Hook-Specific Fields:**

**PreToolUse:**
```json
{
  "decision": "approve" | "block",
  "reason": "Fed back to Claude",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "string"
  }
}
```

**Stop/SubagentStop:**
```json
{
  "decision": "block",
  "reason": "Guide Claude on next steps"
}
```

**UserPromptSubmit/SessionStart:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Context injected into prompt"
  }
}
```

### 3.5 Production Examples

#### Example 1: Block Dangerous Bash Commands (PreToolUse)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/security-validator.py"
          }
        ]
      }
    ]
  }
}
```

**security-validator.py:**
```python
#!/usr/bin/env python3
import json
import sys

# Read hook input
input_data = json.load(sys.stdin)
command = input_data.get('tool_input', {}).get('command', '')

# Define dangerous patterns
dangerous = [
    'rm -rf',
    'sudo rm',
    'chmod 777',
    'format',
    '> /dev/sda',
    'dd if='
]

# Check for dangerous commands
for pattern in dangerous:
    if pattern in command:
        print(f"🚫 BLOCKED: Dangerous command pattern '{pattern}' detected", file=sys.stderr)
        print(f"Command attempted: {command}", file=sys.stderr)
        sys.exit(2)  # Exit code 2 = BLOCK

# Allow safe commands
sys.exit(0)
```

#### Example 2: Auto-Format TypeScript Files (PostToolUse)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/auto-format.sh"
          }
        ]
      }
    ]
  }
}
```

**auto-format.sh:**
```bash
#!/bin/bash

# Read hook input and extract file path
file_path=$(jq -r '.tool_input.file_path' <&0)

# Only format TypeScript files
if [[ "$file_path" == *.ts || "$file_path" == *.tsx ]]; then
    npx prettier --write "$file_path" 2>&1
    echo "✅ Formatted: $file_path"
fi

exit 0
```

#### Example 3: Automated Testing (PostToolUse)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "pytest tests/ --maxfail=1 -v"
          }
        ]
      }
    ]
  }
}
```

#### Example 4: Session Context Loading (SessionStart)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/load-context.sh"
          }
        ]
      }
    ]
  }
}
```

**load-context.sh:**
```bash
#!/bin/bash

echo "## Development Context"
echo ""
echo "### Git Status"
git status --short
echo ""
echo "### Recent Commits"
git log -3 --oneline
echo ""
echo "### Open Issues"
gh issue list --limit 5 2>/dev/null || echo "No GitHub CLI configured"
echo ""
echo "### Dependencies Status"
if [ -f "package.json" ]; then
    echo "Node.js project detected"
    npm outdated || echo "All npm dependencies up to date"
fi

if [ -f "requirements.txt" ]; then
    echo "Python project detected"
    pip list --outdated | head -10 || echo "All pip dependencies up to date"
fi

exit 0  # stdout becomes session context
```

#### Example 5: Financial Precision Validator (PreToolUse)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/financial-precision-check.py"
          }
        ]
      }
    ]
  }
}
```

**financial-precision-check.py:**
```python
#!/usr/bin/env python3
"""
Prevents float usage in financial calculations.
Enforces Decimal type for currency operations.
"""
import json
import sys
import re

input_data = json.load(sys.stdin)
tool_input = input_data.get('tool_input', {})

# Extract content being written/edited
content = tool_input.get('new_string', '') or tool_input.get('content', '')
file_path = tool_input.get('file_path', '')

# Only check Python financial modules
if not (file_path.endswith('.py') and ('finance' in file_path or 'fpa' in file_path)):
    sys.exit(0)

# Detect float usage in currency calculations
dangerous_patterns = [
    r'price\s*=\s*float\(',
    r'amount\s*=\s*float\(',
    r'currency\s*=\s*float\(',
    r'total\s*=\s*float\(',
    r'variance\s*=\s*float\(',
    r'\.to_float\(\)',
]

violations = []
for pattern in dangerous_patterns:
    if re.search(pattern, content, re.IGNORECASE):
        violations.append(pattern)

if violations:
    msg = f"""
🚫 FINANCIAL PRECISION VIOLATION

File: {file_path}

Detected float usage in financial calculations:
{chr(10).join(f'  - {v}' for v in violations)}

REQUIRED: Use decimal.Decimal for all currency calculations.

Example:
  ❌ price = float(value)
  ✅ price = Decimal(str(value))

Reason: Floats introduce rounding errors (0.1 + 0.2 ≠ 0.3)
Reference: CLAUDE.md Financial Domain Requirements
"""
    print(msg, file=sys.stderr)
    sys.exit(2)  # BLOCK

sys.exit(0)
```

#### Example 6: Stop Hook with AI Completion Messages

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/completion-message.py"
          }
        ]
      }
    ]
  }
}
```

**completion-message.py:**
```python
#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "openai>=1.0.0",
#     "anthropic>=0.40.0"
# ]
# ///

import json
import sys
import os
from openai import OpenAI

input_data = json.load(sys.stdin)

# Prevent infinite continuation
if input_data.get('stop_hook_active'):
    sys.exit(0)

# Generate completion message with OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "system",
        "content": "Generate a brief, professional completion message for a coding session."
    }],
    max_tokens=50
)

message = response.choices[0].message.content
print(message)  # Visible in transcript

# Optionally play TTS
os.system(f'say "{message}"')  # macOS

sys.exit(0)
```

#### Example 7: Prompt-Based Hook (Stop - Intelligent Evaluation)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Analyze the conversation. If all tasks are complete and tests pass, allow stopping. If tasks remain or tests fail, block stopping and explain what's needed."
          }
        ]
      }
    ]
  }
}
```

**How it works:**
1. Claude Code sends hook input + prompt to Haiku (fast LLM)
2. Haiku responds with structured JSON:
   ```json
   {
     "decision": "block",
     "reason": "Tests are failing. Fix validation errors in variance.py before completing."
   }
   ```
3. Claude receives `reason` and continues work

#### Example 8: UserPromptSubmit - Security Scanning

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "superagent guard"
          }
        ]
      }
    ]
  },
  "env": {
    "SUPERAGENT_API_KEY": "your_api_key_here"
  }
}
```

**Superagent Integration:**
- Scans prompts for secrets, PII, jailbreak attempts
- Blocks malicious prompts (exit code 2)
- Logs security events

#### Example 9: TypeScript Hooks (johnlindquist/claude-hooks)

**Installation:**
```bash
npx claude-hooks
```

**Generated structure:**
```
.claude/
├── settings.json
└── hooks/
    ├── index.ts         # User-editable handlers
    ├── lib.ts           # Type definitions
    └── session.ts       # Session tracking
```

**index.ts example:**
```typescript
import type { PreToolUsePayload, WriteToolInput, HookResponse } from './lib'

export async function preToolUse(payload: PreToolUsePayload): Promise<HookResponse> {
  // Full TypeScript auto-completion
  if (payload.tool_name === 'Write') {
    const { file_path, content } = payload.tool_input as WriteToolInput

    // Block writes to .env files
    if (file_path.endsWith('.env')) {
      return {
        action: 'block',
        reason: 'Cannot modify .env files directly. Use .env.example instead.'
      }
    }
  }

  return { action: 'continue' }
}

export async function postToolUse(payload: PostToolUsePayload): Promise<HookResponse> {
  console.log(`Completed: ${payload.tool_name}`)
  return { action: 'continue' }
}
```

**Benefits:**
- Full type safety
- Auto-completion for payloads
- Familiar TypeScript syntax
- Bun runtime for fast execution

#### Example 10: PreCompact - Transcript Backup

```json
{
  "hooks": {
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/backup-transcript.sh"
          }
        ]
      }
    ]
  }
}
```

**backup-transcript.sh:**
```bash
#!/bin/bash

# Read hook input
input=$(cat)
transcript_path=$(echo "$input" | jq -r '.transcript_path')
session_id=$(echo "$input" | jq -r '.session_id')

# Create backup directory
backup_dir="$HOME/.claude/backups/$(date +%Y-%m)"
mkdir -p "$backup_dir"

# Backup transcript
backup_file="$backup_dir/${session_id}-$(date +%s).jsonl"
cp "$transcript_path" "$backup_file"

echo "✅ Transcript backed up to: $backup_file"
exit 0
```

---

## 4. Best Practices for Determinism

### 4.1 Core Principles

**1. Hooks Over Prompts**

❌ **Non-Deterministic (Prompt-based):**
```
"Always run pytest after editing test files"
```
- LLM might forget
- Inconsistent execution
- No guarantee

✅ **Deterministic (Hook-based):**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "pytest tests/ -v"
      }]
    }]
  }
}
```
- Guaranteed execution
- Always runs after edits
- Programmatic control

**2. Exit Code Discipline**

Use exit codes consistently:

```python
# Security check hook
if violation_detected:
    print("Error message", file=sys.stderr)
    sys.exit(2)  # BLOCK - always use 2 for blocking

if warning_condition:
    print("Warning message", file=sys.stderr)
    sys.exit(1)  # Non-blocking warning

# Success
sys.exit(0)
```

**3. Idempotent Hooks**

Hooks should be safe to run multiple times:

```bash
#!/bin/bash
# ❌ BAD: Side effects accumulate
echo "Line added" >> file.txt

# ✅ GOOD: Idempotent
if ! grep -q "Line added" file.txt; then
    echo "Line added" >> file.txt
fi
```

**4. Prevent Infinite Loops**

Always check `stop_hook_active` in Stop/SubagentStop hooks:

```python
input_data = json.load(sys.stdin)

if input_data.get('stop_hook_active'):
    sys.exit(0)  # Allow stop to prevent infinite continuation
```

**5. Structured Output Over Text**

Use JSON output for sophisticated control:

```python
# ✅ GOOD: Structured output
output = {
    "decision": "block",
    "reason": "Tests failed: 3 failures in variance.py",
    "continue": False,
    "stopReason": "Fix test failures before proceeding"
}
print(json.dumps(output))
sys.exit(2)
```

### 4.2 Financial Automation Patterns

**Pattern 1: Decimal Enforcement**

```python
# PreToolUse hook for financial modules
if 'finance' in file_path or 'fpa' in file_path:
    if re.search(r'float\(.*price|amount|currency', content):
        print("Use Decimal, not float", file=sys.stderr)
        sys.exit(2)
```

**Pattern 2: Audit Trail Logging**

```python
# PostToolUse hook for financial calculations
if tool_name in ['Edit', 'Write']:
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": os.getenv('USER'),
        "file": file_path,
        "operation": tool_name,
        "session_id": session_id
    }
    with open('.audit/changes.jsonl', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
```

**Pattern 3: Test Enforcement**

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "pytest tests/financial/ --tb=short --maxfail=1"
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Check if all financial tests pass. Block stopping if any test fails."
      }]
    }]
  }
}
```

**Pattern 4: Validation Gates**

```python
# PreToolUse hook for budget files
if tool_name == 'Edit' and 'budget' in file_path:
    # Validate new content
    try:
        # Assume CSV format
        import pandas as pd
        from decimal import Decimal

        df = pd.read_csv(io.StringIO(new_content))

        # Validate required columns
        required = ['Account', 'Budget', 'Actual']
        if not all(col in df.columns for col in required):
            print("Missing required columns", file=sys.stderr)
            sys.exit(2)

        # Validate decimal precision
        for col in ['Budget', 'Actual']:
            for val in df[col]:
                try:
                    Decimal(str(val))
                except:
                    print(f"Invalid decimal in {col}: {val}", file=sys.stderr)
                    sys.exit(2)

    except Exception as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        sys.exit(2)
```

### 4.3 Hook Development Workflow

**Step 1: Start Simple**

```bash
#!/bin/bash
# Simple logging hook
echo "Hook triggered at $(date)" >> /tmp/hook.log
exit 0
```

**Step 2: Add JSON Parsing**

```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)
print(f"Tool: {input_data.get('tool_name')}", file=sys.stderr)
sys.exit(0)
```

**Step 3: Implement Logic**

```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)
tool_name = input_data.get('tool_name')
tool_input = input_data.get('tool_input', {})

if tool_name == 'Bash':
    command = tool_input.get('command', '')
    if 'rm -rf' in command:
        print("Dangerous command blocked", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
```

**Step 4: Add Structured Output**

```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)

output = {
    "decision": "block",
    "reason": "Detailed explanation",
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny"
    }
}

print(json.dumps(output))
sys.exit(2)
```

**Step 5: Test with UV Single-File Scripts**

```python
#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas>=2.0.0",
#     "openpyxl>=3.1.0"
# ]
# ///

import json
import sys
import pandas as pd

# Hook logic with dependencies
input_data = json.load(sys.stdin)
# ... implementation
```

### 4.4 Security Best Practices

**1. Input Validation**

```python
# Always validate hook input
input_data = json.load(sys.stdin)

# Sanitize file paths
file_path = input_data.get('tool_input', {}).get('file_path', '')
if '..' in file_path or file_path.startswith('/'):
    print("Invalid file path", file=sys.stderr)
    sys.exit(2)
```

**2. Permission Boundaries**

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/bash-sandbox.py"
      }]
    }]
  }
}
```

**bash-sandbox.py:**
```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)
command = input_data.get('tool_input', {}).get('command', '')

# Allowlist safe commands
safe_prefixes = ['ls', 'cat', 'grep', 'find', 'git', 'pytest']
if not any(command.startswith(cmd) for cmd in safe_prefixes):
    output = {
        "decision": "ask",  # Escalate to user
        "reason": f"Command not in allowlist: {command}"
    }
    print(json.dumps(output))
    sys.exit(0)

sys.exit(0)  # Allow safe commands
```

**3. Secret Detection**

```python
# UserPromptSubmit hook
import re

secrets_patterns = [
    r'sk-[a-zA-Z0-9]{48}',  # OpenAI API key
    r'AIza[0-9A-Za-z\\-_]{35}',  # Google API key
    r'AKIA[0-9A-Z]{16}',  # AWS Access Key
]

prompt = input_data.get('prompt', '')
for pattern in secrets_patterns:
    if re.search(pattern, prompt):
        print("🚫 Secret detected in prompt", file=sys.stderr)
        sys.exit(2)
```

**4. File Protection**

```python
# PreToolUse hook
protected_paths = [
    '.env',
    '.env.local',
    'credentials.json',
    '.git/config',
    'id_rsa'
]

file_path = input_data.get('tool_input', {}).get('file_path', '')
if any(protected in file_path for protected in protected_paths):
    print(f"🚫 Protected file: {file_path}", file=sys.stderr)
    sys.exit(2)
```

### 4.5 Performance Optimization

**1. Conditional Execution**

```python
# Only run expensive checks when relevant
file_path = input_data.get('tool_input', {}).get('file_path', '')

if not file_path.endswith('.py'):
    sys.exit(0)  # Skip hook for non-Python files

# Expensive Python linting only for .py files
os.system('ruff check ' + file_path)
```

**2. Timeouts**

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "pytest tests/",
        "timeout": 30
      }]
    }]
  }
}
```

**3. Background Execution**

```bash
#!/bin/bash
# Run slow tasks in background, don't block Claude
(pytest tests/ > /tmp/test-results.txt 2>&1) &
exit 0  # Return immediately
```

**4. Caching**

```python
import hashlib
import os

# Cache validation results
content = input_data.get('tool_input', {}).get('content', '')
content_hash = hashlib.sha256(content.encode()).hexdigest()
cache_file = f'/tmp/validation-cache/{content_hash}'

if os.path.exists(cache_file):
    print("✅ Validation cached")
    sys.exit(0)

# Run expensive validation
# ... validation logic

# Cache result
os.makedirs('/tmp/validation-cache', exist_ok=True)
open(cache_file, 'w').write('validated')
```

---

## 5. Specific Applications for FP&A Automation Workflows

### 5.1 Variance Analysis Automation

**Use Case:** Enforce validation and audit trail during variance calculation workflows

**Hook Configuration:**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/variance-validator.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/test-variance.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify all variance calculations produce audit trail with timestamp, source files, and user. Block stopping if audit trail incomplete."
          }
        ]
      }
    ]
  }
}
```

**variance-validator.py:**
```python
#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas>=2.0.0",
#     "openpyxl>=3.1.0"
# ]
# ///

import json
import sys
import re
from decimal import Decimal

input_data = json.load(sys.stdin)
tool_input = input_data.get('tool_input', {})
file_path = tool_input.get('file_path', '')
content = tool_input.get('new_string', '') or tool_input.get('content', '')

# Only validate variance calculation modules
if 'variance' not in file_path:
    sys.exit(0)

violations = []

# Check 1: Decimal usage for currency
if 'float(' in content and any(kw in content for kw in ['actual', 'budget', 'variance']):
    violations.append("Float detected in variance calculation - use Decimal")

# Check 2: Audit trail logging
if 'def calculate_variance' in content:
    if 'timestamp' not in content or 'audit' not in content:
        violations.append("Missing audit trail in calculate_variance function")

# Check 3: Division by zero handling
if '/ budget' in content or '/budget' in content:
    if 'if budget == 0' not in content and 'if not budget' not in content:
        violations.append("Missing zero-budget handling")

# Check 4: Percentage precision
if 'percentage' in content or 'pct' in content:
    if 'round(' in content:
        violations.append("Avoid rounding in calculations - round only for display")

if violations:
    error_msg = f"""
🚫 VARIANCE CALCULATION VALIDATION FAILED

File: {file_path}

Violations:
{chr(10).join(f'  ❌ {v}' for v in violations)}

Required patterns:
  ✅ Use Decimal for all currency calculations
  ✅ Include audit trail: timestamp, user, source_files
  ✅ Handle zero budget explicitly
  ✅ Maintain precision - no rounding in intermediate calculations

Reference: CLAUDE.md Financial Domain Requirements
"""
    print(error_msg, file=sys.stderr)
    sys.exit(2)  # BLOCK

print("✅ Variance validation passed", file=sys.stderr)
sys.exit(0)
```

**test-variance.sh:**
```bash
#!/bin/bash
# PostToolUse hook - run tests after code changes

if [[ $(cat <&0 | jq -r '.tool_input.command // ""') == *"variance"* ]]; then
    echo "Running variance calculation tests..."
    pytest tests/test_variance.py -v --tb=short
    exit_code=$?

    if [ $exit_code -ne 0 ]; then
        echo "⚠️  Variance tests failed" >&2
    else
        echo "✅ Variance tests passed" >&2
    fi
fi

exit 0  # Non-blocking (informational)
```

### 5.2 Excel Import Validation

**Use Case:** Validate Excel files before processing for budget/actual data

**Hook Configuration:**

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/excel-path-validator.py"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/excel-structure-validator.py"
          }
        ]
      }
    ]
  }
}
```

**excel-path-validator.py:**
```python
#!/usr/bin/env python3
import json
import sys
import re
import os

input_data = json.load(sys.stdin)
prompt = input_data.get('prompt', '')

# Extract Excel file paths from prompt
excel_patterns = [
    r'([^\s]+\.xlsx?)',
    r'"([^"]+\.xlsx?)"',
    r"'([^']+\.xlsx?)'"
]

excel_files = []
for pattern in excel_patterns:
    matches = re.findall(pattern, prompt, re.IGNORECASE)
    excel_files.extend(matches)

# Validate files exist
missing = []
for file in excel_files:
    if not os.path.exists(file):
        missing.append(file)

if missing:
    error = f"""
🚫 EXCEL FILES NOT FOUND

Missing files:
{chr(10).join(f'  ❌ {f}' for f in missing)}

Please verify file paths before proceeding.
"""
    print(error, file=sys.stderr)
    sys.exit(2)  # Block prompt

# Add context about found files
if excel_files:
    context = f"\n\n## Excel Files Detected\n"
    for file in excel_files:
        size = os.path.getsize(file)
        context += f"- {file} ({size:,} bytes)\n"
    print(context)  # Add to context

sys.exit(0)
```

**excel-structure-validator.py:**
```python
#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas>=2.0.0",
#     "openpyxl>=3.1.0"
# ]
# ///

import json
import sys
import pandas as pd

input_data = json.load(sys.stdin)
tool_input = input_data.get('tool_input', {})
file_path = tool_input.get('file_path', '')

# Only validate Excel files
if not file_path.endswith(('.xlsx', '.xls')):
    sys.exit(0)

try:
    # Quick validation - read first 5 rows only
    df = pd.read_excel(file_path, nrows=5)

    # Check for required columns (budget/actual analysis)
    required_columns = ['Account']
    has_budget = 'Budget' in df.columns or 'budget' in df.columns
    has_actual = 'Actual' in df.columns or 'actual' in df.columns

    if not has_budget and not has_actual:
        error = f"""
⚠️  EXCEL STRUCTURE WARNING

File: {file_path}

Expected columns for budget/actual analysis not found.
Found columns: {', '.join(df.columns)}

Continuing, but verify this is the correct file.
"""
        print(error, file=sys.stderr)
        # Non-blocking warning (exit 1)
        sys.exit(1)

    # Add file metadata to context
    metadata = f"""
📊 Excel File Metadata:
- Columns: {', '.join(df.columns)}
- Sample rows: {len(df)}
- Budget column: {'✅' if has_budget else '❌'}
- Actual column: {'✅' if has_actual else '❌'}
"""
    print(metadata)

except Exception as e:
    print(f"⚠️  Could not validate Excel: {e}", file=sys.stderr)
    sys.exit(1)  # Non-blocking warning

sys.exit(0)
```

### 5.3 Audit Trail Enforcement

**Use Case:** Ensure all financial calculations generate audit trails

**SessionStart hook:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/init-audit-trail.sh"
          }
        ]
      }
    ]
  }
}
```

**init-audit-trail.sh:**
```bash
#!/bin/bash

# Create audit directory structure
mkdir -p .audit/{calculations,file_changes,test_results}

# Initialize audit log
cat > .audit/session-$(date +%s).json <<EOF
{
  "session_start": "$(date -Iseconds)",
  "user": "$USER",
  "cwd": "$(pwd)",
  "git_branch": "$(git branch --show-current 2>/dev/null || echo 'N/A')",
  "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'N/A')"
}
EOF

echo "✅ Audit trail initialized at .audit/"
exit 0
```

**PostToolUse hook for calculations:**
```python
#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime

input_data = json.load(sys.stdin)
tool_name = input_data.get('tool_name')
tool_input = input_data.get('tool_input', {})

# Only log Bash commands containing financial calculations
if tool_name == 'Bash':
    command = tool_input.get('command', '')
    if any(kw in command for kw in ['variance', 'calculate', 'budget', 'actual']):
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": os.getenv('USER'),
            "command": command,
            "session_id": input_data.get('session_id'),
            "cwd": input_data.get('cwd')
        }

        audit_file = '.audit/calculations/log.jsonl'
        with open(audit_file, 'a') as f:
            f.write(json.dumps(audit_entry) + '\n')

        print(f"✅ Logged to audit trail: {audit_file}", file=sys.stderr)

sys.exit(0)
```

### 5.4 Decimal Precision Enforcement

**Global PreToolUse hook:**
```python
#!/usr/bin/env python3
"""
Enforces Decimal usage for all financial calculations.
Blocks float usage in currency operations.
"""
import json
import sys
import re

input_data = json.load(sys.stdin)
tool_input = input_data.get('tool_input', {})
file_path = tool_input.get('file_path', '')

# Only check financial modules
financial_indicators = ['finance', 'fpa', 'budget', 'variance', 'currency', 'accounting']
if not any(indicator in file_path.lower() for indicator in financial_indicators):
    sys.exit(0)

content = tool_input.get('new_string', '') or tool_input.get('content', '')

# Pattern detection
float_violations = []

# Check 1: Direct float() calls
float_calls = re.findall(r'(\w+)\s*=\s*float\([^)]+\)', content)
for var in float_calls:
    if any(kw in var.lower() for kw in ['price', 'amount', 'total', 'currency', 'variance', 'budget', 'actual']):
        float_violations.append(f"Variable '{var}' uses float()")

# Check 2: Float type hints
float_hints = re.findall(r'(\w+):\s*float', content)
for var in float_hints:
    if any(kw in var.lower() for kw in ['price', 'amount', 'total', 'currency']):
        float_violations.append(f"Variable '{var}' has float type hint")

# Check 3: Pandas .astype(float)
if '.astype(float)' in content or ".astype('float')" in content:
    float_violations.append("DataFrame column conversion to float detected")

if float_violations:
    error = f"""
🚫 DECIMAL PRECISION VIOLATION

File: {file_path}

Float usage detected in financial calculations:
{chr(10).join(f'  ❌ {v}' for v in float_violations)}

REQUIRED FIX:

Instead of:
  price = float(value)
  amount: float = 100.50
  df['Amount'].astype(float)

Use Decimal:
  from decimal import Decimal
  price = Decimal(str(value))
  amount: Decimal = Decimal('100.50')
  df['Amount'] = df['Amount'].apply(lambda x: Decimal(str(x)))

REASON: Float precision errors
  float(0.1) + float(0.2) = 0.30000000000000004  ❌
  Decimal('0.1') + Decimal('0.2') = 0.3  ✅

Reference: CLAUDE.md § Financial Domain Requirements
spec.md § Data Types and Precision
"""
    print(error, file=sys.stderr)
    sys.exit(2)  # BLOCK

sys.exit(0)
```

### 5.5 Test Enforcement Before Completion

**Stop hook with prompt-based evaluation:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review the conversation transcript. Check if: (1) All financial calculation tests pass, (2) Decimal types used for currency, (3) Audit trail generated. If any requirement fails, block stopping and explain what's needed. Otherwise allow stopping."
          }
        ]
      }
    ]
  }
}
```

**Alternative: Command-based Stop hook:**
```python
#!/usr/bin/env python3
import json
import sys
import subprocess
import os

input_data = json.load(sys.stdin)

# Prevent infinite continuation
if input_data.get('stop_hook_active'):
    sys.exit(0)

# Check if tests pass
result = subprocess.run(
    ['pytest', 'tests/financial/', '-v', '--tb=no'],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    output = {
        "decision": "block",
        "reason": f"Financial tests failed. Fix the following before completing:\n{result.stdout}"
    }
    print(json.dumps(output))
    sys.exit(2)  # Block stopping

# Check for audit trail
if not os.path.exists('.audit/calculations/log.jsonl'):
    output = {
        "decision": "block",
        "reason": "No audit trail found. Ensure all calculations are logged to .audit/"
    }
    print(json.dumps(output))
    sys.exit(2)

print("✅ All quality gates passed")
sys.exit(0)
```

### 5.6 Data Reconciliation Validation

**PreToolUse hook for data processing:**
```python
#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas>=2.0.0"
# ]
# ///

import json
import sys
import pandas as pd
from decimal import Decimal

input_data = json.load(sys.stdin)
tool_name = input_data.get('tool_name')
tool_input = input_data.get('tool_input', {})

# Only validate Write operations for reconciliation files
if tool_name != 'Write':
    sys.exit(0)

file_path = tool_input.get('file_path', '')
if 'reconciliation' not in file_path:
    sys.exit(0)

content = tool_input.get('content', '')

try:
    # Parse CSV content
    from io import StringIO
    df = pd.read_csv(StringIO(content))

    # Validate required columns
    required = ['Account', 'Source', 'Amount', 'Status']
    missing = [col for col in required if col not in df.columns]

    if missing:
        print(f"❌ Missing columns: {', '.join(missing)}", file=sys.stderr)
        sys.exit(2)

    # Validate reconciliation status values
    valid_statuses = ['Matched', 'Unmatched', 'Pending']
    invalid = df[~df['Status'].isin(valid_statuses)]

    if not invalid.empty:
        print(f"❌ Invalid status values found: {invalid['Status'].unique()}", file=sys.stderr)
        print(f"Valid statuses: {', '.join(valid_statuses)}", file=sys.stderr)
        sys.exit(2)

    # Validate decimal amounts
    for idx, row in df.iterrows():
        try:
            Decimal(str(row['Amount']))
        except:
            print(f"❌ Invalid amount at row {idx}: {row['Amount']}", file=sys.stderr)
            sys.exit(2)

    print(f"✅ Reconciliation validation passed ({len(df)} records)", file=sys.stderr)

except Exception as e:
    print(f"❌ Validation error: {e}", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
```

### 5.7 Complete FP&A Workflow Example

**Full settings.json for FP&A automation:**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/fpa/init-session.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/fpa/validate-excel-paths.py"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/fpa/decimal-enforcement.py"
          },
          {
            "type": "command",
            "command": "~/.claude/hooks/fpa/variance-validator.py"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/fpa/security-validator.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "pytest tests/financial/ -v --tb=short",
            "timeout": 30
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/fpa/audit-logger.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify: (1) All tests pass, (2) Audit trail exists in .audit/, (3) All currency uses Decimal type, (4) No float usage in financial modules. Block if any check fails."
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/fpa/backup-transcript.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 6. Code Examples from Key Sources

### 6.1 From disler/claude-code-hooks-mastery

**UV Single-File Script Pattern:**
```python
#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anthropic>=0.40.0",
#     "openai>=1.0.0",
#     "elevenlabs>=1.10.1",
# ]
# ///

import json
import sys
import os
from openai import OpenAI

def main():
    input_data = json.load(sys.stdin)

    # Hook logic here
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    # ...

    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Benefits:**
- Self-contained dependencies
- No virtual environment management
- Fast UV dependency resolution
- Portable across projects

### 6.2 From johnlindquist/claude-hooks

**TypeScript Hook System:**

**lib.ts (Type Definitions):**
```typescript
export interface PreToolUsePayload {
  session_id: string
  transcript_path: string
  cwd: string
  hook_event_name: 'PreToolUse'
  tool_name: string
  tool_input: Record<string, any>
}

export interface WriteToolInput {
  file_path: string
  content: string
}

export interface EditToolInput {
  file_path: string
  old_string: string
  new_string: string
}

export interface HookResponse {
  action: 'continue' | 'block'
  reason?: string
}
```

**index.ts (User Implementation):**
```typescript
import type { PreToolUsePayload, WriteToolInput, HookResponse } from './lib'

export async function preToolUse(payload: PreToolUsePayload): Promise<HookResponse> {
  // Full type safety and auto-completion
  if (payload.tool_name === 'Write') {
    const { file_path, content } = payload.tool_input as WriteToolInput

    // Block writes to sensitive files
    if (file_path.includes('.env') || file_path.includes('credentials')) {
      return {
        action: 'block',
        reason: `Cannot write to sensitive file: ${file_path}`
      }
    }
  }

  return { action: 'continue' }
}
```

### 6.3 From Francis Bourre's Schema Gist

**Complete PreToolUse Payload Schema:**
```typescript
interface PreToolUseInput {
  session_id: string
  transcript_path: string
  cwd: string
  hook_event_name: "PreToolUse"
  tool_name: "Bash" | "Edit" | "Write" | "Read" | "Glob" | "Grep" | "NotebookEdit" | string
  tool_input: {
    // Bash
    command?: string
    dangerouslyDisableSandbox?: boolean
    description?: string
    run_in_background?: boolean
    timeout?: number

    // Edit
    file_path?: string
    old_string?: string
    new_string?: string
    replace_all?: boolean

    // Write
    content?: string

    // Read
    limit?: number
    offset?: number

    // Glob
    pattern?: string
    path?: string

    // Grep
    pattern?: string
    output_mode?: "content" | "files_with_matches" | "count"
    glob?: string
    type?: string

    // NotebookEdit
    notebook_path?: string
    cell_id?: string
    new_source?: string
    cell_type?: "code" | "markdown"
    edit_mode?: "replace" | "insert" | "delete"
  }
}
```

**Complete PreToolUse Output Schema:**
```typescript
interface PreToolUseOutput {
  // Common fields
  continue?: boolean
  stopReason?: string
  suppressOutput?: boolean

  // Hook-specific
  decision?: "approve" | "block"
  reason?: string

  hookSpecificOutput?: {
    hookEventName: "PreToolUse"
    permissionDecision: "allow" | "deny" | "ask"
    permissionDecisionReason?: string
  }
}
```

### 6.4 From ljw1004 Gist (Stop "You're Right" Pattern)

**UserPromptSubmit Hook to Prevent Reflexive Agreement:**
```bash
#!/bin/bash

# Read hook input
input=$(cat)
session_id=$(echo "$input" | jq -r '.session_id')
transcript_path=$(echo "$input" | jq -r '.transcript_path')

# Check last 3 Claude responses for agreement phrases
recent_responses=$(tail -3 "$transcript_path" | jq -r 'select(.type == "assistant") | .text')

if echo "$recent_responses" | grep -qiE "(You're right|you are correct|사용자가 맞다)"; then
    # Append system reminder to prompt
    cat <<'EOF'

<system-reminder>
You recently used reflexive agreement phrases like "You're right" or "you are correct."

IMPORTANT: Avoid agreeing without substance. Instead:
1. Identify potential flaws or edge cases
2. Provide concrete technical analysis
3. Explain WHY the user is correct (if they are)

Examples:

❌ BAD: "You're right, we should add null-checks."
✅ GOOD: "Null-checks are critical here because the API returns null when the user is unauthenticated. Without checks, we'd throw NullPointerException at line 42."

❌ BAD: "That's correct about the connection failure."
✅ GOOD: "Connection failures can occur in 3 scenarios: (1) network timeout, (2) invalid credentials, (3) server overload. The current code only handles timeout. We should add retry logic for overload and clear error messages for invalid credentials."
</system-reminder>
EOF
fi

exit 0  # stdout appended to prompt as context
```

### 6.5 From ClaudeLog Documentation

**Notification Hook for macOS:**
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

**Linux (notify-send):**
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input'"
          }
        ]
      }
    ]
  }
}
```

### 6.6 From Backslash Security Best Practices

**Zero-Trust PreToolUse Hook:**
```python
#!/usr/bin/env python3
"""
Zero-trust security hook for Claude Code.
Implements allowlist-first approach with denylist backup.
"""
import json
import sys
import re

input_data = json.load(sys.stdin)
tool_name = input_data.get('tool_name')
tool_input = input_data.get('tool_input', {})

# DENYLIST (nuclear shield)
denied_paths = [
    r'\.env',
    r'\.git/config',
    r'credentials\.json',
    r'id_rsa',
    r'\.ssh/',
    r'/etc/passwd'
]

file_path = tool_input.get('file_path', '')
for pattern in denied_paths:
    if re.search(pattern, file_path):
        print(f"🚫 DENIED: Access to {file_path} blocked by security policy", file=sys.stderr)
        sys.exit(2)

# BASH COMMAND RESTRICTIONS
if tool_name == 'Bash':
    command = tool_input.get('command', '')

    # Denylist dangerous commands
    dangerous = ['rm -rf /', 'sudo rm', 'chmod 777', 'curl', 'wget', 'nc -l']
    for cmd in dangerous:
        if cmd in command:
            print(f"🚫 DENIED: Dangerous command blocked: {cmd}", file=sys.stderr)
            sys.exit(2)

    # Allowlist safe commands
    safe_prefixes = ['ls', 'cat', 'grep', 'find', 'git', 'pytest', 'npm test', 'python -m']
    if not any(command.startswith(prefix) for prefix in safe_prefixes):
        output = {
            "decision": "ask",  # Escalate to user
            "reason": f"Command not in allowlist: {command}"
        }
        print(json.dumps(output))
        sys.exit(0)

# MCP SERVER RESTRICTIONS
if tool_name.startswith('mcp__'):
    # Only allow specific MCP servers
    allowed_servers = ['mcp__memory__', 'mcp__github__']
    if not any(tool_name.startswith(server) for server in allowed_servers):
        print(f"🚫 DENIED: MCP server not allowed: {tool_name}", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
```

### 6.7 From Steve Kinney's Course

**Hook Control Flow Example:**
```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)

# Priority order for flow control:
# 1. "continue": false (absolute precedence)
# 2. "decision": "block" (hook-specific)
# 3. Exit code 2 (simple blocking)

output = {
    "continue": False,  # <-- Takes priority over everything
    "stopReason": "Critical error detected",
    "decision": "block",  # <-- Ignored when continue=false
    "reason": "This won't be shown"
}

print(json.dumps(output))
sys.exit(2)  # <-- Also ignored
```

### 6.8 Real-World Production Pattern

**Multi-Stage Validation Pipeline:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/stage1-syntax.py",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "~/.claude/hooks/stage2-security.py",
            "timeout": 10
          },
          {
            "type": "command",
            "command": "~/.claude/hooks/stage3-business-rules.py",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

**stage1-syntax.py:**
```python
#!/usr/bin/env python3
# Fast syntax validation
import json, sys, ast

input_data = json.load(sys.stdin)
content = input_data.get('tool_input', {}).get('content', '')
file_path = input_data.get('tool_input', {}).get('file_path', '')

if file_path.endswith('.py'):
    try:
        ast.parse(content)
    except SyntaxError as e:
        print(f"Syntax error: {e}", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
```

**stage2-security.py:**
```python
#!/usr/bin/env python3
# Security checks
import json, sys, re

input_data = json.load(sys.stdin)
content = input_data.get('tool_input', {}).get('content', '')

# Check for secrets
secret_patterns = [r'sk-[a-zA-Z0-9]{48}', r'AIza[0-9A-Za-z\-_]{35}']
for pattern in secret_patterns:
    if re.search(pattern, content):
        print("Secret detected!", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
```

**stage3-business-rules.py:**
```python
#!/usr/bin/env python3
# Domain-specific validation
import json, sys

input_data = json.load(sys.stdin)
file_path = input_data.get('tool_input', {}).get('file_path', '')
content = input_data.get('tool_input', {}).get('content', '')

# Financial modules must use Decimal
if 'finance' in file_path and 'float(' in content:
    print("Use Decimal, not float!", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
```

---

## 7. Implementation Roadmap for FP&A Project

### Phase 1: Foundation (Week 1)

**Goal:** Basic hook infrastructure

**Tasks:**
1. Create `.claude/hooks/` directory structure
2. Implement SessionStart hook for context loading
3. Add basic PreToolUse hook for file protection
4. Configure settings.json hierarchy

**Deliverables:**
- `.claude/settings.json` with SessionStart and basic PreToolUse
- `.claude/hooks/init-session.sh`
- `.claude/hooks/file-guard.py`

### Phase 2: Financial Validation (Week 2)

**Goal:** Enforce Decimal precision and audit trails

**Tasks:**
1. Implement decimal-enforcement.py PreToolUse hook
2. Add variance-validator.py for calculation modules
3. Create audit-logger.py PostToolUse hook
4. Setup .audit/ directory structure

**Deliverables:**
- `.claude/hooks/fpa/decimal-enforcement.py`
- `.claude/hooks/fpa/variance-validator.py`
- `.claude/hooks/fpa/audit-logger.py`

### Phase 3: Testing & Quality Gates (Week 3)

**Goal:** Automated testing and Stop hook validation

**Tasks:**
1. Configure PostToolUse hook for automatic test runs
2. Implement prompt-based Stop hook for quality verification
3. Add PreCompact hook for transcript backup
4. Create test result logging

**Deliverables:**
- Automatic pytest execution after code changes
- Stop hook preventing completion with failing tests
- Transcript backup system

### Phase 4: Excel Integration (Week 4)

**Goal:** Validate Excel imports and data quality

**Tasks:**
1. Implement excel-path-validator.py UserPromptSubmit hook
2. Add excel-structure-validator.py PreToolUse hook
3. Create reconciliation-validator.py for data matching
4. Setup data quality reporting

**Deliverables:**
- Excel validation pipeline
- Reconciliation status validation
- Data quality reports in .audit/

### Phase 5: Production Hardening (Week 5)

**Goal:** Security, performance, error handling

**Tasks:**
1. Implement zero-trust security hook
2. Add timeout configurations
3. Create error recovery mechanisms
4. Performance profiling and optimization

**Deliverables:**
- Production-ready security configuration
- Performance benchmarks
- Error handling documentation

---

## 8. Key Takeaways

### For Deterministic Behavior

1. **Hooks > Prompts**: Guaranteed execution vs. LLM discretion
2. **Exit Code Discipline**: 0=success, 2=block, other=warn
3. **Structured Output**: JSON for sophisticated flow control
4. **Prevent Loops**: Check `stop_hook_active` in Stop hooks

### For FP&A Workflows

1. **Decimal Enforcement**: PreToolUse hooks block float usage
2. **Audit Trails**: PostToolUse hooks log all operations
3. **Test Gates**: Stop hooks prevent completion with failures
4. **Data Validation**: UserPromptSubmit hooks verify Excel files

### For Production Deployment

1. **Settings Hierarchy**: Local > Project > User
2. **UV Scripts**: Self-contained dependencies, portable
3. **Timeouts**: Prevent hanging hooks
4. **Security**: Allowlist + Denylist approach

### Hook Selection Guide

| Requirement | Hook Event | Pattern |
|-------------|------------|---------|
| Validate before execution | PreToolUse | Block with exit 2 |
| Auto-format after edit | PostToolUse | Run formatter |
| Load session context | SessionStart | Print to stdout |
| Verify before completion | Stop | Prompt-based or command |
| Backup before compaction | PreCompact | Copy transcript |
| Validate user input | UserPromptSubmit | Block or inject context |
| Desktop notifications | Notification | System notification |
| Subagent quality gates | SubagentStop | Check completion criteria |

---

## 9. References

### Official Documentation
- Hooks Reference: https://docs.claude.com/en/docs/claude-code/hooks
- Hooks Guide: https://docs.claude.com/en/docs/claude-code/hooks-guide
- Security: https://docs.claude.com/en/docs/claude-code/security
- Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices

### Key Repositories
- claude-code-hooks-mastery: https://github.com/disler/claude-code-hooks-mastery
- claude-hooks (TypeScript): https://github.com/johnlindquist/claude-hooks
- awesome-claude-code: https://github.com/hesreallyhim/awesome-claude-code
- Hook Schemas: https://gist.github.com/FrancisBourre/50dca37124ecc43eaf08328cdcccdb34

### Community Resources
- ClaudeLog: https://claudelog.com/mechanics/hooks/
- GitButler Blog: https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks
- Steve Kinney Course: https://stevekinney.com/courses/ai-development/claude-code-hooks
- Backslash Security: https://www.backslash.security/blog/claude-code-security-best-practices

---

## 10. Next Steps for This Project

### Immediate Actions

1. **Review SessionStart Hook Requirements**
   - Current: `.claude/skills/session-start-hook/SKILL.md`
   - Action: Align with research findings
   - Priority: Implement git status + dependency sync

2. **Implement Financial Validation Hooks**
   - Create `.claude/hooks/fpa/` directory
   - Port decimal-enforcement.py example
   - Add variance-validator.py
   - Configure in `.claude/settings.json`

3. **Setup Audit Trail System**
   - Initialize `.audit/` structure in SessionStart
   - Add PostToolUse logging hook
   - Create audit trail reporting

4. **Configure Stop Hook Quality Gates**
   - Implement prompt-based Stop hook
   - Verify test passage before completion
   - Check audit trail completeness

### Integration with Existing Skills

**variance-analyzer skill:**
- Add PreToolUse hook for decimal validation
- PostToolUse hook for automatic testing
- Stop hook for audit trail verification

**financial-validator skill:**
- Integrate with PreToolUse hook pipeline
- Share validation logic with hooks
- Consolidate error messages

### Testing Strategy

1. Create test suite for hooks in `tests/hooks/`
2. Verify exit code behavior
3. Test JSON output parsing
4. Validate security blocking
5. Measure performance impact

---

**END OF RESEARCH REPORT**

*Compiled from 15+ authoritative sources*
*Research Date: 2025-11-10*
