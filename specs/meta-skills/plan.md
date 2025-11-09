# Meta-Skills Implementation Plan

**Version:** 1.0.0
**Status:** 📋 Planning Phase - Awaiting User Approval
**Created:** 2025-11-09
**Based On:** research-meta-skills.md (20+ sources synthesized)

---

## Executive Summary

This plan details implementation of three **meta-skills** (skill-creator, command-creator, agent-creator) that generate Claude Code artifacts. These are force multipliers - they automate creation of future skills, commands, and agents while enforcing official Anthropic patterns.

**Critical Decision:** Build these FIRST (Phase 0A) before Phase 1 implementation. They enforce quality gates and official structure for all future work.

**Implementation Approach:**
- Template-based code generation using Python f-strings
- Human-in-loop approval at Research → Plan → Implement → Verify checkpoints
- YAML frontmatter validation using PyYAML + jsonschema
- Atomic file operations with rollback on failure
- Minimal tool permissions (Read, Write, Edit, Glob, Grep, Bash only)

**Timeline:** [TO BE MEASURED - estimate 3-5 implementation sessions]

**Success Metrics:**
- Generated artifacts validate against official patterns (100% pass rate)
- Human approval checkpoints enforced (4 per generation workflow)
- Zero float precision violations in generated financial code
- All generated files match kebab-case naming convention

---

## 1. Architecture Overview

### 1.1 Official Anthropic Patterns

**Source:** research-meta-skills.md Part 1, anthropics/skills GitHub repo

**Skills Structure:**
```
.claude/skills/{skill-name}/
├── SKILL.md                   # YAML frontmatter + Markdown
│   ├── name: kebab-case
│   ├── description: <200 chars
│   └── [Instructions section]
├── scripts/                   # Optional - Python/Bash executables
├── references/                # Optional - Detailed docs (progressive disclosure)
└── assets/                    # Optional - Templates, configs, binaries
```

**Commands Structure:**
```
.claude/commands/{subdir}/{command-name}.md
├── YAML frontmatter
│   └── description: Brief description
└── Markdown instructions
```

**Agents Structure:**
```
.claude/agents/{subdir}/{agent-name}.md
├── YAML frontmatter
│   ├── name: kebab-case
│   ├── model: sonnet|opus|haiku
│   └── tools: [Read, Write, ...]
└── Markdown instructions
```

### 1.2 Meta-Skills Responsibilities

| Meta-Skill | Creates | Validates | Tools Needed |
|------------|---------|-----------|--------------|
| **skill-creator** | .claude/skills/{name}/SKILL.md + subdirs | YAML, naming, structure | Read, Write, Edit, Glob, Grep, Bash |
| **command-creator** | .claude/commands/{subdir}/{name}.md | YAML, naming, description | Read, Write, Edit, Glob, Grep |
| **agent-creator** | .claude/agents/{subdir}/{name}.md | YAML, naming, tools list | Read, Write, Edit, Glob, Grep |

**Why These Tools:**
- **Read/Glob/Grep:** Research existing patterns before generation
- **Write:** Create new files atomically
- **Edit:** Placeholder (future - modify existing artifacts)
- **Bash:** Create directories, git operations (skill-creator only)

**Why NOT These Tools:**
- **Task:** No nested agent invocation (avoids infinite recursion)
- **WebFetch/WebSearch:** No external data needed (all patterns local)
- **NotebookEdit:** Not creating Jupyter notebooks

### 1.3 Human-in-Loop Workflow

**Source:** research-meta-skills.md Part 2, external/humanlayer patterns

**Four Checkpoints:**

```
┌─────────────────────────────────────────────────────────────┐
│                     Meta-Skill Workflow                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  RESEARCH → [CHECKPOINT 1] → PLAN → [CHECKPOINT 2] →        │
│  IMPLEMENT → [CHECKPOINT 3] → VERIFY → [CHECKPOINT 4] →     │
│  COMPLETE                                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Checkpoint 1 (Research):
  - Present existing patterns analysis
  - Show template to be used
  - Identify similar artifacts
  - Wait for approval

Checkpoint 2 (Plan):
  - Show artifact specification (name, description, structure)
  - Display YAML frontmatter preview
  - List files to be created
  - Wait for approval

Checkpoint 3 (Implement):
  - Show generated artifact content
  - Highlight key sections (When to Activate, Tools, etc.)
  - Display directory structure created
  - Wait for approval

Checkpoint 4 (Verify):
  - Run validation functions
  - Show validation report (YAML valid, naming correct, structure complete)
  - Present final artifact location
  - Wait for final approval
```

**Implementation:** Use markdown tables and code blocks to present each checkpoint clearly. Pause execution after each checkpoint.

---

## 2. Meta-Skill Specifications

### 2.1 skill-creator

**File:** `.claude/skills/skill-creator/SKILL.md`

**Purpose:** Generate new skills with official structure (SKILL.md + scripts/, references/, assets/ subdirectories).

**YAML Frontmatter:**
```yaml
---
name: skill-creator
description: Generate Claude Code skills with official Anthropic structure (YAML + Markdown + subdirs)
version: 1.0.0
author: claude-code
tags: [meta, code-generation, infrastructure]
---
```

**When to Activate:**
- **Creation:** User says: "create a new skill for...", "skill that auto-invokes when...", "generate skill"
- **Iteration:** User says: "update skill {name}", "improve {skill-name}", "add to {skill-name} skill"
- Keywords: "skill-creator", "skill-updater", "modify skill", "enhance skill"

**Workflow:**

**STEP 1 - RESEARCH:**
1. Read `.claude/templates/skills/SKILL_TEMPLATE.md`
2. Glob `.claude/skills/*/SKILL.md` to find similar skills
3. Grep for related keywords in existing skills
4. Present findings with template preview

**CHECKPOINT 1:** User approves template and approach

**STEP 2 - PLAN:**
1. Prompt user for:
   - Skill name (validate kebab-case)
   - Description (<200 chars for auto-invocation)
   - When to activate triggers
   - Tags (optional)
2. Generate YAML frontmatter preview
3. Plan directory structure:
   ```
   .claude/skills/{skill-name}/
   ├── SKILL.md
   ├── scripts/ (if executable code needed)
   ├── references/ (if detailed docs needed)
   └── assets/ (if templates needed)
   ```
4. Present plan with file paths

**CHECKPOINT 2:** User approves specification

**STEP 3 - IMPLEMENT:**
1. Validate name: `^[a-z0-9]+(-[a-z0-9]+)*$`
2. Check for conflicts: skill name must be unique
3. Create directory: `.claude/skills/{skill-name}/`
4. Generate SKILL.md from template:
   - Replace `{name}`, `{description}`, `{triggers}`
   - Use Python f-strings for substitution
5. Create subdirectories if needed
6. Create README.md in each subdirectory explaining future contents
7. Display generated content

**CHECKPOINT 3:** User approves generated artifact

**STEP 4 - VERIFY:**
1. **YAML Validation:**
   ```python
   import yaml
   import jsonschema

   # Load frontmatter
   with open('.claude/skills/{name}/SKILL.md') as f:
       content = f.read()
       frontmatter = yaml.safe_load(content.split('---')[1])

   # Validate against schema
   schema = {
       "type": "object",
       "required": ["name", "description"],
       "properties": {
           "name": {"type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"},
           "description": {"type": "string", "maxLength": 200}
       }
   }
   jsonschema.validate(frontmatter, schema)
   ```

2. **Naming Convention:**
   ```python
   import re
   assert re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', skill_name), "Must be kebab-case"
   ```

3. **Directory Structure:**
   ```python
   from pathlib import Path
   skill_path = Path(f'.claude/skills/{skill_name}')
   assert skill_path.exists(), "Skill directory missing"
   assert (skill_path / 'SKILL.md').exists(), "SKILL.md missing"
   ```

4. **Content Quality:**
   - Check for `## When to Activate` section
   - Verify example triggers present
   - Ensure progressive disclosure note if >200 lines

5. Present validation report

**CHECKPOINT 4:** User gives final approval

**SUCCESS CRITERIA:**
- [ ] YAML frontmatter valid (PyYAML + jsonschema pass)
- [ ] Name matches kebab-case pattern
- [ ] Description <200 characters
- [ ] SKILL.md exists with all required sections
- [ ] Subdirectories created (if specified)
- [ ] README.md in each subdirectory
- [ ] No duplicate skill name
- [ ] All 4 checkpoints passed

---

**ITERATION WORKFLOW (skill-updater capability):**

When user requests updating an existing skill:

**STEP 1 - RESEARCH:**
1. Read existing skill: `.claude/skills/{skill-name}/SKILL.md`
2. Parse current YAML frontmatter and content
3. Identify what user wants to change (description, triggers, instructions, examples)
4. Present current state with proposed changes highlighted

**CHECKPOINT 1:** User approves changes to make

**STEP 2 - PLAN:**
1. Show diff of proposed changes
2. Validate changes don't break structure (YAML still valid, naming unchanged)
3. Identify if new subdirectories needed
4. Present plan

**CHECKPOINT 2:** User approves plan

**STEP 3 - IMPLEMENT:**
1. Use Edit tool to modify SKILL.md
2. Add new subdirectories if requested
3. Update version number in YAML frontmatter
4. Show complete updated content

**CHECKPOINT 3:** User approves updated artifact

**STEP 4 - VERIFY:**
1. Run all validation functions (YAML, structure, content quality)
2. Verify changes applied correctly
3. Present validation report

**CHECKPOINT 4:** User gives final approval

**ITERATION SUCCESS CRITERIA:**
- [ ] All validation gates still pass after update
- [ ] Version number incremented
- [ ] Changes applied as requested
- [ ] No structural breakage
- [ ] All 4 checkpoints passed

---

**Tools:** Read, Write, Edit, Glob, Grep, Bash (mkdir if new subdirs needed)

**Anti-Patterns:**
- ❌ Skip research phase
- ❌ Generate without user approval
- ❌ Use camelCase or snake_case for skill name
- ❌ Omit YAML frontmatter
- ❌ Create >200 line SKILL.md without progressive disclosure plan

---

### 2.2 command-creator

**File:** `.claude/skills/command-creator/SKILL.md`

**Purpose:** Generate slash commands in `.claude/commands/{subdir}/{name}.md`.

**YAML Frontmatter:**
```yaml
---
name: command-creator
description: Generate Claude Code slash commands with YAML frontmatter and structured workflows
version: 1.0.0
author: claude-code
tags: [meta, code-generation, infrastructure]
---
```

**When to Activate:**
- **Creation:** User says: "create a new command for...", "slash command that...", "generate /command"
- **Iteration:** User says: "update /command-name", "improve {command}", "modify /workflow"
- Keywords: "command-creator", "command-updater", "generate command", "modify command"

**Workflow:**

**STEP 1 - RESEARCH:**
1. Read `.claude/templates/commands/COMMAND_TEMPLATE.md`
2. Glob `.claude/commands/**/*.md` to find similar commands
3. Identify which subdirectory (prod/, dev/, shared/) based on user description
4. Present findings with template preview

**CHECKPOINT 1:** User approves template and subdirectory choice

**STEP 2 - PLAN:**
1. Prompt user for:
   - Command name (validate kebab-case)
   - Description (concise, appears in /help)
   - Subdirectory (optional: prod/, dev/, shared/)
   - Expected parameters ($1, $2, ...)
2. Generate YAML frontmatter preview
3. Plan file path: `.claude/commands/{subdir}/{name}.md`
4. Present specification

**CHECKPOINT 2:** User approves specification

**STEP 3 - IMPLEMENT:**
1. Validate name: `^[a-z0-9]+(-[a-z0-9]+)*$`
2. Check for conflicts: command name must be unique within subdirectory
3. Create subdirectory if needed: `.claude/commands/{subdir}/`
4. Generate command file from template:
   - Replace `{name}`, `{description}`, `{parameters}`
   - Include human-in-loop checkpoint structure if workflow is complex
   - Use Python f-strings for substitution
5. Display generated content

**CHECKPOINT 3:** User approves generated artifact

**STEP 4 - VERIFY:**
1. **YAML Validation:**
   ```python
   import yaml

   # Load frontmatter
   with open(f'.claude/commands/{subdir}/{name}.md') as f:
       content = f.read()
       if content.startswith('---'):
           frontmatter = yaml.safe_load(content.split('---')[1])
           assert 'description' in frontmatter, "Missing description"
   ```

2. **Naming Convention:**
   ```python
   import re
   assert re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', command_name), "Must be kebab-case"
   ```

3. **File Exists:**
   ```python
   from pathlib import Path
   cmd_path = Path(f'.claude/commands/{subdir}/{command_name}.md')
   assert cmd_path.exists(), "Command file missing"
   ```

4. **Content Quality:**
   - Check for usage example (`**Usage:** /command-name <args>`)
   - Verify workflow steps if applicable
   - Ensure success criteria section present

5. Present validation report

**CHECKPOINT 4:** User gives final approval

**SUCCESS CRITERIA:**
- [ ] YAML frontmatter valid
- [ ] Name matches kebab-case pattern
- [ ] Command file exists at correct path
- [ ] Description concise and clear
- [ ] Usage example included
- [ ] No duplicate command name in subdirectory
- [ ] All 4 checkpoints passed

---

**ITERATION WORKFLOW (command-updater capability):**

When user requests updating an existing command:

**STEP 1 - RESEARCH:**
1. Glob to find command file: `.claude/commands/**/{command-name}.md`
2. Read existing command content
3. Parse YAML frontmatter
4. Identify what user wants to change (description, workflow steps, parameters)
5. Present current state with proposed changes highlighted

**CHECKPOINT 1:** User approves changes to make

**STEP 2 - PLAN:**
1. Show diff of proposed changes
2. Validate changes don't break structure
3. Ensure YAML still valid
4. Present plan

**CHECKPOINT 2:** User approves plan

**STEP 3 - IMPLEMENT:**
1. Use Edit tool to modify command file
2. Update content as requested
3. Maintain proper formatting
4. Show complete updated content

**CHECKPOINT 3:** User approves updated artifact

**STEP 4 - VERIFY:**
1. Run YAML validation
2. Verify naming convention unchanged
3. Check content quality (usage example, workflow steps)
4. Present validation report

**CHECKPOINT 4:** User gives final approval

**ITERATION SUCCESS CRITERIA:**
- [ ] All validation gates still pass after update
- [ ] Changes applied as requested
- [ ] No structural breakage
- [ ] All 4 checkpoints passed

---

**Tools:** Read, Write, Edit, Glob, Grep, Bash (mkdir -p if subdir needed)

**Anti-Patterns:**
- ❌ Forget usage example
- ❌ Use underscores in command name
- ❌ Omit description in frontmatter
- ❌ Create command without researching existing patterns

---

### 2.3 agent-creator

**File:** `.claude/skills/agent-creator/SKILL.md`

**Purpose:** Generate specialized agents in `.claude/agents/{subdir}/{name}.md`.

**YAML Frontmatter:**
```yaml
---
name: agent-creator
description: Generate Claude Code agents with tool permissions and specialized instructions
version: 1.0.0
author: claude-code
tags: [meta, code-generation, infrastructure]
---
```

**When to Activate:**
- **Creation:** User says: "create a new agent for...", "subagent that can...", "generate agent"
- **Iteration:** User says: "update agent {name}", "modify {agent} permissions", "improve {agent}"
- Keywords: "agent-creator", "agent-updater", "generate agent", "modify agent"

**Workflow:**

**STEP 1 - RESEARCH:**
1. Read `.claude/templates/agents/AGENT_TEMPLATE.md`
2. Read `.claude/agents/code-reviewer.md` (example production agent)
3. Glob `.claude/agents/**/*.md` to find similar agents
4. Present findings with template preview

**CHECKPOINT 1:** User approves template

**STEP 2 - PLAN:**
1. Prompt user for:
   - Agent name (validate kebab-case)
   - Description (purpose and specialization)
   - Model (sonnet, opus, haiku) - default: haiku for cost efficiency
   - Tools needed (principle of least privilege)
   - Subdirectory (optional: prod/, dev/, shared/)
2. **Tool Permission Review:**
   - If agent modifies code: [Read, Write, Edit]
   - If agent only reviews: [Read, Glob, Grep]
   - If agent runs tests: [Read, Bash]
   - Never include: [Task] (prevents infinite recursion)
3. Generate YAML frontmatter preview
4. Plan file path: `.claude/agents/{subdir}/{name}.md`
5. Present specification

**CHECKPOINT 2:** User approves specification

**STEP 3 - IMPLEMENT:**
1. Validate name: `^[a-z0-9]+(-[a-z0-9]+)*$`
2. Validate model: must be "sonnet", "opus", or "haiku"
3. Validate tools: must be subset of allowed tools
4. Check for conflicts: agent name must be unique within subdirectory
5. Create subdirectory if needed: `.claude/agents/{subdir}/`
6. Generate agent file from template:
   - Replace `{name}`, `{description}`, `{model}`, `{tools}`
   - Include specialized instructions section
   - Use Python f-strings for substitution
7. Display generated content

**CHECKPOINT 3:** User approves generated artifact

**STEP 4 - VERIFY:**
1. **YAML Validation:**
   ```python
   import yaml
   import jsonschema

   # Load frontmatter
   with open(f'.claude/agents/{subdir}/{name}.md') as f:
       content = f.read()
       frontmatter = yaml.safe_load(content.split('---')[1])

   # Validate schema
   schema = {
       "type": "object",
       "required": ["name", "model", "tools"],
       "properties": {
           "name": {"type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"},
           "model": {"type": "string", "enum": ["sonnet", "opus", "haiku"]},
           "tools": {"type": "array", "items": {"type": "string"}}
       }
   }
   jsonschema.validate(frontmatter, schema)
   ```

2. **Tool Permissions Security:**
   ```python
   forbidden_tools = ["Task"]  # Prevent infinite recursion
   tools = frontmatter.get("tools", [])
   assert not any(t in forbidden_tools for t in tools), "Forbidden tool detected"
   ```

3. **Naming Convention:**
   ```python
   import re
   assert re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', agent_name), "Must be kebab-case"
   ```

4. **File Exists:**
   ```python
   from pathlib import Path
   agent_path = Path(f'.claude/agents/{subdir}/{agent_name}.md')
   assert agent_path.exists(), "Agent file missing"
   ```

5. **Content Quality:**
   - Check for specialized instructions section
   - Verify tool list matches intended capabilities
   - Ensure model choice appropriate (haiku for simple tasks)

6. Present validation report

**CHECKPOINT 4:** User gives final approval

**SUCCESS CRITERIA:**
- [ ] YAML frontmatter valid (PyYAML + jsonschema pass)
- [ ] Name matches kebab-case pattern
- [ ] Model is valid (sonnet/opus/haiku)
- [ ] Tools list does not include forbidden tools
- [ ] Agent file exists at correct path
- [ ] Specialized instructions clear and focused
- [ ] No duplicate agent name in subdirectory
- [ ] All 4 checkpoints passed

---

**ITERATION WORKFLOW (agent-updater capability):**

When user requests updating an existing agent:

**STEP 1 - RESEARCH:**
1. Glob to find agent file: `.claude/agents/**/{agent-name}.md`
2. Read existing agent content
3. Parse YAML frontmatter (current model, tools, description)
4. Identify what user wants to change (tool permissions, model, instructions)
5. Present current state with proposed changes highlighted

**CHECKPOINT 1:** User approves changes to make

**STEP 2 - PLAN:**
1. Show diff of proposed changes
2. Validate tool permission changes (security review)
3. Ensure model choice is valid
4. Check YAML schema compliance
5. Present plan

**CHECKPOINT 2:** User approves plan

**STEP 3 - IMPLEMENT:**
1. Use Edit tool to modify agent file
2. Update YAML frontmatter if needed
3. Update specialized instructions if needed
4. Maintain proper formatting
5. Show complete updated content

**CHECKPOINT 3:** User approves updated artifact

**STEP 4 - VERIFY:**
1. Run YAML validation
2. Verify tool permissions (no forbidden tools)
3. Verify model is valid (sonnet/opus/haiku)
4. Check naming convention unchanged
5. Present validation report

**CHECKPOINT 4:** User gives final approval

**ITERATION SUCCESS CRITERIA:**
- [ ] All validation gates still pass after update
- [ ] Tool permissions secure (no Task tool)
- [ ] Model choice appropriate
- [ ] Changes applied as requested
- [ ] No structural breakage
- [ ] All 4 checkpoints passed

---

**Tools:** Read, Write, Edit, Glob, Grep, Bash (mkdir -p if subdir needed)

**Anti-Patterns:**
- ❌ Include Task tool (infinite recursion risk)
- ❌ Use "claude-3.5-sonnet" instead of "sonnet"
- ❌ Grant excessive tool permissions
- ❌ Forget to specify model (defaults to parent, wastes tokens)
- ❌ Omit specialized instructions

---

## 3. Implementation Phases

### Phase 0A.1: Build skill-creator (First Meta-Skill)

**Priority:** CRITICAL - Required before all others

**Steps:**
1. Create `.claude/skills/skill-creator/` directory
2. Write SKILL.md following template
3. Create scripts/, references/, assets/ subdirectories
4. Add README.md to each subdirectory
5. Test by generating a dummy skill
6. Validate with all quality gates

**Validation:**
- Generate test skill: `test-validation-skill`
- Verify YAML parses correctly
- Check directory structure created
- Delete test skill after validation

**Blockers:** None (foundational)

**Estimated Time:** [TO BE MEASURED]

---

### Phase 0A.2: Build command-creator

**Priority:** HIGH - Needed for prod/dev workflow commands

**Steps:**
1. Create `.claude/skills/command-creator/` directory
2. Write SKILL.md following template
3. Create scripts/, references/, assets/ subdirectories
4. Test by generating a dummy command
5. Validate with all quality gates

**Dependencies:** None (can run parallel with skill-creator)

**Validation:**
- Generate test command: `.claude/commands/test/test-workflow.md`
- Verify YAML parses correctly
- Delete test command after validation

**Blockers:** None

**Estimated Time:** [TO BE MEASURED]

---

### Phase 0A.3: Build agent-creator

**Priority:** MEDIUM - Needed for specialized agents

**Steps:**
1. Create `.claude/skills/agent-creator/` directory
2. Write SKILL.md following template
3. Create scripts/, references/, assets/ subdirectories
4. Test by generating a dummy agent
5. Validate with all quality gates

**Dependencies:** None (can run parallel with others)

**Validation:**
- Generate test agent: `.claude/agents/test/test-reviewer.md`
- Verify YAML parses correctly
- Check tool permissions list
- Delete test agent after validation

**Blockers:** None

**Estimated Time:** [TO BE MEASURED]

---

### Phase 0A.4: Integration Testing

**Priority:** CRITICAL - Validate entire meta-skill system

**Tests:**
1. **Generate Real Skill:**
   - Use skill-creator to create `monthly-close-processor`
   - Verify all validation gates pass
   - Keep artifact (don't delete)

2. **Generate Real Command:**
   - Use command-creator to create `/forecast-revenue`
   - Verify YAML valid
   - Keep artifact

3. **Generate Real Agent:**
   - Use agent-creator to create `financial-auditor`
   - Verify tool permissions correct
   - Keep artifact

4. **Conflict Detection:**
   - Try to create duplicate skill name
   - Verify error handling catches conflict

5. **Naming Validation:**
   - Try to create skill with invalid name "TestSkill_v2"
   - Verify validation rejects it

**Success Criteria:**
- All 3 real artifacts generated successfully
- All validation functions pass
- Conflict detection working
- Naming validation working
- Zero manual file editing needed

**Blockers:** Requires Phases 0A.1-0A.3 complete

**Estimated Time:** [TO BE MEASURED]

---

## 4. Validation Functions

### 4.1 YAML Validation

**Source:** research-meta-skills.md Part 9

**Library:** PyYAML + jsonschema

**Implementation:**
```python
# File: .claude/skills/skill-creator/scripts/validate_yaml.py

import yaml
import jsonschema
from pathlib import Path
from typing import Dict, Any

def validate_skill_yaml(skill_path: Path) -> tuple[bool, str]:
    """Validate YAML frontmatter in SKILL.md file.

    Args:
        skill_path: Path to SKILL.md file

    Returns:
        (is_valid, error_message) tuple
    """
    try:
        with open(skill_path, 'r') as f:
            content = f.read()

        # Extract YAML frontmatter
        if not content.startswith('---'):
            return False, "Missing YAML frontmatter (must start with ---)"

        parts = content.split('---')
        if len(parts) < 3:
            return False, "Invalid YAML frontmatter format"

        frontmatter = yaml.safe_load(parts[1])

        # Define schema
        schema = {
            "type": "object",
            "required": ["name", "description"],
            "properties": {
                "name": {
                    "type": "string",
                    "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"
                },
                "description": {
                    "type": "string",
                    "maxLength": 200
                },
                "version": {"type": "string"},
                "author": {"type": "string"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "additionalProperties": False
        }

        # Validate
        jsonschema.validate(frontmatter, schema)
        return True, "YAML valid"

    except yaml.YAMLError as e:
        return False, f"YAML parsing error: {e}"
    except jsonschema.ValidationError as e:
        return False, f"Schema validation error: {e.message}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def validate_command_yaml(command_path: Path) -> tuple[bool, str]:
    """Validate YAML frontmatter in command file.

    Args:
        command_path: Path to command .md file

    Returns:
        (is_valid, error_message) tuple
    """
    try:
        with open(command_path, 'r') as f:
            content = f.read()

        # Commands require at least description in frontmatter
        if not content.startswith('---'):
            return False, "Missing YAML frontmatter"

        parts = content.split('---')
        if len(parts) < 3:
            return False, "Invalid YAML frontmatter format"

        frontmatter = yaml.safe_load(parts[1])

        schema = {
            "type": "object",
            "required": ["description"],
            "properties": {
                "description": {"type": "string"}
            }
        }

        jsonschema.validate(frontmatter, schema)
        return True, "YAML valid"

    except Exception as e:
        return False, f"Validation error: {e}"


def validate_agent_yaml(agent_path: Path) -> tuple[bool, str]:
    """Validate YAML frontmatter in agent file.

    Args:
        agent_path: Path to agent .md file

    Returns:
        (is_valid, error_message) tuple
    """
    try:
        with open(agent_path, 'r') as f:
            content = f.read()

        if not content.startswith('---'):
            return False, "Missing YAML frontmatter"

        parts = content.split('---')
        if len(parts) < 3:
            return False, "Invalid YAML frontmatter format"

        frontmatter = yaml.safe_load(parts[1])

        schema = {
            "type": "object",
            "required": ["name", "model", "tools"],
            "properties": {
                "name": {
                    "type": "string",
                    "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"
                },
                "model": {
                    "type": "string",
                    "enum": ["sonnet", "opus", "haiku"]
                },
                "tools": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }

        jsonschema.validate(frontmatter, schema)

        # Security check: no forbidden tools
        forbidden = ["Task"]
        tools = frontmatter.get("tools", [])
        if any(t in forbidden for t in tools):
            return False, f"Forbidden tool detected: {forbidden}"

        return True, "YAML valid"

    except Exception as e:
        return False, f"Validation error: {e}"
```

---

### 4.2 Naming Convention Validation

**Source:** research-meta-skills.md Part 14

**Pattern:** Kebab-case `^[a-z0-9]+(-[a-z0-9]+)*$`

**Implementation:**
```python
# File: .claude/skills/skill-creator/scripts/validate_naming.py

import re
from pathlib import Path

def validate_kebab_case(name: str) -> tuple[bool, str]:
    """Validate name follows kebab-case convention.

    Args:
        name: Name to validate

    Returns:
        (is_valid, error_message) tuple
    """
    pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'

    if not re.match(pattern, name):
        return False, f"Name '{name}' must be kebab-case (lowercase, hyphens only)"

    return True, "Name valid"


def check_name_conflicts(name: str, artifact_type: str) -> tuple[bool, str]:
    """Check if name conflicts with existing artifacts.

    Args:
        name: Artifact name
        artifact_type: "skill", "command", or "agent"

    Returns:
        (is_unique, error_message) tuple
    """
    if artifact_type == "skill":
        search_path = Path(".claude/skills")
        existing = [p.name for p in search_path.iterdir() if p.is_dir()]

    elif artifact_type == "command":
        search_path = Path(".claude/commands")
        existing = [
            p.stem for p in search_path.rglob("*.md")
        ]

    elif artifact_type == "agent":
        search_path = Path(".claude/agents")
        existing = [
            p.stem for p in search_path.rglob("*.md")
        ]
    else:
        return False, f"Unknown artifact type: {artifact_type}"

    if name in existing:
        return False, f"Name '{name}' already exists in {artifact_type}s"

    return True, "Name is unique"
```

---

### 4.3 Directory Structure Validation

**Source:** research-meta-skills.md Part 8

**Implementation:**
```python
# File: .claude/skills/skill-creator/scripts/validate_structure.py

from pathlib import Path
from typing import List, Tuple

def validate_skill_structure(skill_name: str) -> Tuple[bool, List[str]]:
    """Validate skill directory structure matches official pattern.

    Args:
        skill_name: Name of skill to validate

    Returns:
        (is_valid, errors) tuple
    """
    errors = []
    base_path = Path(f".claude/skills/{skill_name}")

    # Check base directory
    if not base_path.exists():
        errors.append(f"Skill directory missing: {base_path}")
        return False, errors

    # Check SKILL.md
    skill_file = base_path / "SKILL.md"
    if not skill_file.exists():
        errors.append(f"SKILL.md missing: {skill_file}")

    # Optional subdirectories (check if created)
    for subdir in ["scripts", "references", "assets"]:
        subdir_path = base_path / subdir
        if subdir_path.exists():
            # If exists, must have README.md
            readme = subdir_path / "README.md"
            if not readme.exists():
                errors.append(f"README.md missing in {subdir}/")

    return len(errors) == 0, errors


def validate_command_structure(command_path: Path) -> Tuple[bool, List[str]]:
    """Validate command file exists at correct location.

    Args:
        command_path: Full path to command .md file

    Returns:
        (is_valid, errors) tuple
    """
    errors = []

    if not command_path.exists():
        errors.append(f"Command file missing: {command_path}")

    # Verify parent is .claude/commands/{optional-subdir}/
    if not str(command_path).startswith(".claude/commands/"):
        errors.append(f"Command must be in .claude/commands/ (got: {command_path})")

    return len(errors) == 0, errors


def validate_agent_structure(agent_path: Path) -> Tuple[bool, List[str]]:
    """Validate agent file exists at correct location.

    Args:
        agent_path: Full path to agent .md file

    Returns:
        (is_valid, errors) tuple
    """
    errors = []

    if not agent_path.exists():
        errors.append(f"Agent file missing: {agent_path}")

    # Verify parent is .claude/agents/{optional-subdir}/
    if not str(agent_path).startswith(".claude/agents/"):
        errors.append(f"Agent must be in .claude/agents/ (got: {agent_path})")

    return len(errors) == 0, errors
```

---

## 5. Template Generation Approach

**Source:** research-meta-skills.md Part 4, Part 17.1

**Decision:** Python f-strings (not Jinja2)

**Rationale:**
- Simpler for structured text (YAML + Markdown)
- No external dependencies
- Easier to debug
- Sufficient for meta-skills (no complex control flow)

**Example:**

```python
# File: .claude/skills/skill-creator/scripts/generate_skill.py

from pathlib import Path
from typing import List, Optional

def generate_skill_md(
    name: str,
    description: str,
    triggers: List[str],
    tags: Optional[List[str]] = None,
    version: str = "1.0.0",
    author: str = "claude-code"
) -> str:
    """Generate SKILL.md content from template.

    Args:
        name: Skill name (kebab-case)
        description: Brief description (<200 chars)
        triggers: List of activation triggers
        tags: Optional tags
        version: Version string
        author: Author name

    Returns:
        Complete SKILL.md content
    """
    tags_str = ", ".join(tags) if tags else "infrastructure"
    triggers_bullets = "\n".join([f"- {t}" for t in triggers])

    template = f"""---
name: {name}
description: {description}
version: {version}
author: {author}
tags: [{tags_str}]
---

# {name.replace('-', ' ').title()}

## Purpose
{description}

## When to Activate
{triggers_bullets}

## Instructions

### Step 1: [Action Name]
Clear, concise instruction for the first step.

### Step 2: [Action Name]
Clear, concise instruction for the second step.

### Step 3: [Action Name]
Clear, concise instruction for the third step.

## Best Practices
- Best practice 1
- Best practice 2
- Best practice 3

## Anti-Patterns to Avoid
- ❌ Anti-pattern 1
- ❌ Anti-pattern 2
- ❌ Anti-pattern 3

## Expected Outputs
- Output format 1
- Output format 2

## Progressive Disclosure
Keep SKILL.md concise (<200 lines). For additional details, create subdirectories:
- `scripts/` - Executable Python/Bash scripts
- `references/` - Detailed documentation (loaded on-demand)
- `assets/` - Templates, config files, binary files (images, fonts, etc.)

## Examples

### Example 1: [Use Case Name]
```
Input: [Example input]
Process: [Steps taken]
Output: [Example output]
```

### Example 2: [Use Case Name]
```
Input: [Example input]
Process: [Steps taken]
Output: [Example output]
```

---

**Source:** Based on Anthropic Skills best practices (2025)
**Last Updated:** 2025-11-09
"""

    return template
```

**Similar functions for:**
- `generate_command_md()`
- `generate_agent_md()`
- `generate_subdirectory_readme()`

---

## 6. Error Handling & Atomicity

**Source:** research-meta-skills.md Part 10

**Pattern:** Transaction-like approach with rollback

**Implementation:**

```python
# File: .claude/skills/skill-creator/scripts/atomic_file_ops.py

from pathlib import Path
import shutil
from typing import Callable, Any
from contextlib import contextmanager

@contextmanager
def atomic_skill_creation(skill_name: str):
    """Context manager for atomic skill creation.

    Creates skill in temp directory, moves to final location only on success.
    Rolls back on any exception.

    Usage:
        with atomic_skill_creation("my-skill") as temp_path:
            # Create files in temp_path
            # If exception raised, temp_path deleted automatically
            pass
        # If no exception, temp_path moved to .claude/skills/my-skill
    """
    temp_base = Path(".claude/skills/.tmp")
    temp_path = temp_base / skill_name
    final_path = Path(f".claude/skills/{skill_name}")

    try:
        # Create temp directory
        temp_path.mkdir(parents=True, exist_ok=True)

        yield temp_path

        # Success - move to final location
        if final_path.exists():
            raise FileExistsError(f"Skill already exists: {final_path}")

        shutil.move(str(temp_path), str(final_path))

    except Exception as e:
        # Rollback - delete temp directory
        if temp_path.exists():
            shutil.rmtree(temp_path)
        raise e

    finally:
        # Clean up temp base if empty
        if temp_base.exists() and not any(temp_base.iterdir()):
            temp_base.rmdir()


def safe_write_file(path: Path, content: str) -> None:
    """Write file atomically (temp file + rename pattern).

    Args:
        path: Destination file path
        content: Content to write
    """
    temp_path = path.with_suffix(path.suffix + ".tmp")

    try:
        # Write to temp file
        temp_path.write_text(content)

        # Atomic rename
        temp_path.rename(path)

    except Exception as e:
        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()
        raise e
```

**Usage in Meta-Skills:**

```python
# In skill-creator workflow
try:
    with atomic_skill_creation(skill_name) as temp_path:
        # Generate SKILL.md
        skill_content = generate_skill_md(name, description, triggers)
        safe_write_file(temp_path / "SKILL.md", skill_content)

        # Create subdirectories if needed
        for subdir in ["scripts", "references", "assets"]:
            subdir_path = temp_path / subdir
            subdir_path.mkdir(exist_ok=True)

            readme_content = generate_subdirectory_readme(subdir)
            safe_write_file(subdir_path / "README.md", readme_content)

        # All operations succeeded - context manager commits

except Exception as e:
    print(f"❌ Skill creation failed: {e}")
    print("All changes rolled back.")
    raise
```

---

## 7. Testing Strategy

**Source:** research-meta-skills.md Part 13

### 7.1 Unit Tests

**Test File:** `tests/test_meta_skills.py`

```python
import pytest
from pathlib import Path
from .claude.skills.skill-creator.scripts import (
    validate_yaml,
    validate_naming,
    generate_skill_md
)

class TestYAMLValidation:
    def test_valid_skill_yaml(self):
        # Create temp SKILL.md with valid YAML
        content = """---
name: test-skill
description: Test skill for validation
version: 1.0.0
tags: [test]
---

# Content here
"""
        temp_file = Path("/tmp/test_skill.md")
        temp_file.write_text(content)

        is_valid, msg = validate_yaml.validate_skill_yaml(temp_file)
        assert is_valid, msg

    def test_missing_frontmatter(self):
        content = "# No YAML frontmatter"
        temp_file = Path("/tmp/test_skill_no_yaml.md")
        temp_file.write_text(content)

        is_valid, msg = validate_yaml.validate_skill_yaml(temp_file)
        assert not is_valid
        assert "frontmatter" in msg.lower()


class TestNamingConventions:
    def test_valid_kebab_case(self):
        is_valid, msg = validate_naming.validate_kebab_case("my-skill-name")
        assert is_valid

    def test_invalid_camel_case(self):
        is_valid, msg = validate_naming.validate_kebab_case("MySkillName")
        assert not is_valid

    def test_invalid_underscore(self):
        is_valid, msg = validate_naming.validate_kebab_case("my_skill_name")
        assert not is_valid


class TestSkillGeneration:
    def test_generate_skill_md(self):
        content = generate_skill_md(
            name="test-skill",
            description="Test description",
            triggers=["When user says X", "When Y happens"],
            tags=["test", "demo"]
        )

        # Verify structure
        assert "---" in content
        assert "name: test-skill" in content
        assert "## When to Activate" in content
        assert "- When user says X" in content
```

### 7.2 Integration Tests

**Test File:** `tests/test_meta_skills_integration.py`

```python
import pytest
from pathlib import Path
import shutil

class TestSkillCreatorEnd2End:
    def setup_method(self):
        """Create temp workspace for each test."""
        self.test_dir = Path("/tmp/meta_skill_test")
        self.test_dir.mkdir(exist_ok=True)

    def teardown_method(self):
        """Clean up after each test."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_create_skill_full_workflow(self):
        """Test complete skill creation workflow."""
        from .claude.skills.skill_creator import create_skill

        # Invoke skill creator
        result = create_skill(
            name="test-integration-skill",
            description="Test skill for integration test",
            triggers=["Test trigger"],
            create_subdirs=True
        )

        # Verify skill created
        skill_path = Path(".claude/skills/test-integration-skill")
        assert skill_path.exists()
        assert (skill_path / "SKILL.md").exists()
        assert (skill_path / "scripts").exists()
        assert (skill_path / "references").exists()
        assert (skill_path / "assets").exists()

        # Verify YAML valid
        from .claude.skills.skill_creator.scripts.validate_yaml import validate_skill_yaml
        is_valid, msg = validate_skill_yaml(skill_path / "SKILL.md")
        assert is_valid, msg

        # Clean up
        shutil.rmtree(skill_path)
```

### 7.3 Manual Testing Checklist

**Test after implementation:**

- [ ] Create test skill using skill-creator
  - Verify 4 checkpoints presented
  - Verify YAML validates
  - Verify subdirectories created
  - Verify README.md in each subdir

- [ ] Create test command using command-creator
  - Verify kebab-case enforced
  - Verify description in frontmatter
  - Verify file created in correct subdir

- [ ] Create test agent using agent-creator
  - Verify tool permissions list validates
  - Verify model choice enforced (sonnet/opus/haiku)
  - Verify Task tool forbidden

- [ ] Test conflict detection
  - Try creating duplicate skill name
  - Verify error message clear

- [ ] Test naming validation
  - Try creating "TestSkill" (camelCase) - should fail
  - Try creating "test_skill" (snake_case) - should fail
  - Try creating "test-skill" (kebab-case) - should succeed

- [ ] Test rollback on failure
  - Introduce error mid-creation
  - Verify temp files cleaned up
  - Verify final directory NOT created

---

## 8. Git Automation

**Source:** research-meta-skills.md Part 6

**Pattern:** Conventional Commits

**Implementation:**

```python
# File: .claude/skills/skill-creator/scripts/git_automation.py

import subprocess
from pathlib import Path
from typing import Literal

def git_commit_artifact(
    artifact_type: Literal["skill", "command", "agent"],
    artifact_name: str,
    description: str
) -> bool:
    """Create git commit for newly generated artifact.

    Uses Conventional Commits format:
    feat(skill-creator): create {artifact_name} skill

    Args:
        artifact_type: Type of artifact
        artifact_name: Name of artifact
        description: Brief description

    Returns:
        True if commit successful, False otherwise
    """
    # Determine scope
    scope = f"{artifact_type}-creator"

    # Determine file path
    if artifact_type == "skill":
        file_path = f".claude/skills/{artifact_name}/"
    elif artifact_type == "command":
        # Glob to find command file (may be in subdir)
        matches = list(Path(".claude/commands").rglob(f"{artifact_name}.md"))
        if not matches:
            return False
        file_path = str(matches[0])
    elif artifact_type == "agent":
        matches = list(Path(".claude/agents").rglob(f"{artifact_name}.md"))
        if not matches:
            return False
        file_path = str(matches[0])
    else:
        return False

    # Create commit message
    commit_msg = f"feat({scope}): create {artifact_name} {artifact_type}\n\n{description}"

    try:
        # Stage files
        subprocess.run(
            ["git", "add", file_path],
            check=True,
            capture_output=True
        )

        # Commit
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            check=True,
            capture_output=True
        )

        return True

    except subprocess.CalledProcessError as e:
        print(f"Git commit failed: {e.stderr.decode()}")
        return False
```

**When to Use:**
- After CHECKPOINT 4 (final approval)
- Only if user approves git commit
- Optional feature - don't force commit

---

## 9. Success Criteria

### 9.1 Phase 0A Completion Criteria

**Meta-Skills Functional:**
- [ ] skill-creator generates valid skills
- [ ] command-creator generates valid commands
- [ ] agent-creator generates valid agents
- [ ] All validation functions pass
- [ ] All human checkpoints enforced
- [ ] Atomic operations with rollback working

**Quality Gates:**
- [ ] 100% YAML validation pass rate
- [ ] 100% kebab-case enforcement
- [ ] Zero forbidden tools in generated agents
- [ ] All generated artifacts have required sections
- [ ] Progressive disclosure pattern followed (subdirectories for >200 lines)

**Testing:**
- [ ] Unit tests pass (>80% coverage)
- [ ] Integration tests pass
- [ ] Manual testing checklist complete
- [ ] No false positives in validation

**Documentation:**
- [ ] Each meta-skill has SKILL.md with examples
- [ ] Validation scripts have docstrings
- [ ] README.md in all subdirectories
- [ ] This plan updated with [TO BE MEASURED] results

---

### 9.2 Long-Term Success Metrics

**Productivity:**
- [TO BE MEASURED] Time to create new skill: Manual vs. meta-skill
- [TO BE MEASURED] Error rate in generated artifacts: <5% validation failures
- [TO BE MEASURED] User satisfaction: Subjective feedback on workflow

**Quality:**
- [TO BE MEASURED] Generated artifacts require edits: <10%
- [TO BE MEASURED] Conflicts caught before file creation: 100%
- [TO BE MEASURED] Rollback success rate on errors: 100%

**Adoption:**
- [TO BE MEASURED] % of new artifacts created via meta-skills vs. manual
- [TO BE MEASURED] Meta-skill usage frequency (per week)

---

## 10. Anti-Patterns to Avoid

**Source:** research-meta-skills.md Part 19

**Code Generation:**
- ❌ Skip research phase and jump to generation
- ❌ Generate without human approval checkpoints
- ❌ Use Jinja2 when f-strings sufficient
- ❌ Hardcode templates in code (use template files)

**Validation:**
- ❌ Skip YAML validation (silent corruption)
- ❌ Assume naming conventions (must enforce)
- ❌ Allow duplicate names (conflicts)
- ❌ Skip structure validation (incomplete artifacts)

**Error Handling:**
- ❌ Leave temp files on failure
- ❌ Create final artifacts before validation
- ❌ Show stack traces to users (show friendly errors)

**Tool Permissions:**
- ❌ Grant Task tool to agents (infinite recursion)
- ❌ Grant all tools by default (principle of least privilege)
- ❌ Allow agents to modify meta-skills (self-modification risk)

**Workflow:**
- ❌ Skip checkpoints to "move faster"
- ❌ Auto-commit without user approval
- ❌ Generate artifacts in production directories before validation

---

## 11. Dependencies & Risks

### 11.1 External Dependencies

**Python Libraries:**
- **PyYAML** - YAML parsing (already in pyproject.toml)
- **jsonschema** - YAML validation (add to pyproject.toml)
- **pathlib** - File operations (stdlib, no install needed)

**Add to pyproject.toml:**
```toml
[tool.poetry.dependencies]
PyYAML = "^6.0"
jsonschema = "^4.20.0"
```

**Installation:**
```bash
poetry add jsonschema
```

### 11.2 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| YAML parsing errors | Medium | High | Comprehensive validation + clear error messages |
| Name conflicts | Low | Medium | Pre-flight conflict check before creation |
| Temp file cleanup failure | Low | Low | Use context managers (guaranteed cleanup) |
| Invalid tool permissions | Medium | High | Hardcoded forbidden list + schema validation |
| User skips checkpoints | Medium | Medium | Document importance + enforce in workflow |

### 11.3 Implementation Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Time estimation wrong | High | Low | Mark [TO BE MEASURED], iterate |
| Template complexity grows | Medium | Medium | Keep templates simple, use progressive disclosure |
| Validation too strict | Medium | Medium | Allow escape hatch for advanced users |
| Meta-skill recursion | Low | High | Forbid Task tool in all meta-skills |

---

## 12. Next Steps After Approval

1. **User reviews this plan**
2. **User approves or requests changes**
3. **Proceed with Phase 0A.1: Build skill-creator**
4. **Test skill-creator with dummy artifact**
5. **Proceed with Phases 0A.2-0A.4**
6. **Update success metrics with [TO BE MEASURED] results**
7. **Commit and push meta-skills**
8. **Begin Phase 1 implementation using meta-skills**

---

## 13. Implementation Decisions (APPROVED)

**User decisions (2025-11-09):**

1. **Git Automation:** ✅ **ALWAYS atomic commits for each task to enable rollbacks**
   - Every task completion creates a commit
   - Enables easy rollback if needed
   - Maintains clear audit trail

2. **Validation Strictness:** ✅ **Enforce 100% - no exceptions**
   - All validation gates must pass
   - No override flags or escape hatches
   - Quality over convenience

3. **Subdirectory Creation:** ✅ **Ask user during CHECKPOINT 2 (Plan phase)**
   - Present option to create scripts/, references/, assets/
   - User decides which subdirectories needed
   - Not all skills require all subdirectories

4. **Tool Permissions:** ✅ **Include Edit tool + iteration/improvement workflows**
   - Meta-skills need Edit for updating existing artifacts
   - Add iteration workflows to all meta-skills:
     - `skill-updater` capability within skill-creator
     - `command-updater` capability within command-creator
     - `agent-updater` capability within agent-creator
   - Support enhancement of existing artifacts, not just creation

5. **Testing Priority:** ✅ **Incremental implementation and testing**
   - Build skill-creator fully → test → validate
   - Then build command-creator → test → validate
   - Then build agent-creator → test → validate
   - Ensures quality before moving to next meta-skill

---

## Appendix A: File Manifest

**Files to be created in Phase 0A:**

```
.claude/skills/skill-creator/
├── SKILL.md
├── scripts/
│   ├── README.md
│   ├── validate_yaml.py
│   ├── validate_naming.py
│   ├── validate_structure.py
│   ├── generate_skill.py
│   ├── atomic_file_ops.py
│   └── git_automation.py
├── references/
│   ├── README.md
│   └── validation-patterns.md (future)
└── assets/
    └── README.md

.claude/skills/command-creator/
├── SKILL.md
├── scripts/
│   ├── README.md
│   ├── validate_yaml.py (symlink or copy)
│   ├── validate_naming.py (symlink or copy)
│   └── generate_command.py
├── references/
│   └── README.md
└── assets/
    └── README.md

.claude/skills/agent-creator/
├── SKILL.md
├── scripts/
│   ├── README.md
│   ├── validate_yaml.py (symlink or copy)
│   ├── validate_naming.py (symlink or copy)
│   └── generate_agent.py
├── references/
│   └── README.md
└── assets/
    └── README.md

tests/
├── test_meta_skills.py
└── test_meta_skills_integration.py
```

**Total:** ~20 new files

---

## Appendix B: Template Previews

### B.1 skill-creator/SKILL.md Template

```markdown
---
name: skill-creator
description: Generate Claude Code skills with official Anthropic structure (YAML + Markdown + subdirs)
version: 1.0.0
author: claude-code
tags: [meta, code-generation, infrastructure]
---

# Skill Creator

## Purpose
Meta-skill that generates new Claude Code skills following official Anthropic patterns.

## When to Activate
- User says: "create a new skill for..."
- User mentions: "skill that auto-invokes when..."
- Keywords: "skill-creator", "generate skill", "new capability"

## Instructions

[... Full workflow as specified in Section 2.1 ...]

## Progressive Disclosure
Validation scripts in `scripts/` directory. Load validation-patterns.md from `references/` for advanced validation rules.
```

### B.2 Generated Skill Example

**User Request:** "Create a skill that auto-invokes for monthly close workflows"

**Generated Artifact:**
```markdown
---
name: monthly-close-processor
description: Automates month-end close workflows with checklist tracking and approval gates
version: 1.0.0
author: claude-code
tags: [prod, fpa, monthly-close, workflow]
---

# Monthly Close Processor

## Purpose
Automates month-end financial close workflows with checklist tracking and approval gates.

## When to Activate
- User says: "run monthly close"
- User mentions: "month-end close", "period close"
- Keywords: "monthly-close", "close-the-books"

## Instructions

### Step 1: Load Close Checklist
Load month-end close checklist from config/close-checklist.yaml.

### Step 2: Execute Tasks
Execute each task in sequence with human approval gates.

### Step 3: Generate Close Report
Generate close report with completed tasks and timestamps.

[... etc ...]
```

---

**END OF PLAN**

**Next Action:** Awaiting user approval to proceed with Phase 0A.1 (Build skill-creator).

---

**References:**
- research-meta-skills.md (20+ sources synthesized)
- specs/META_SKILLS_DESIGN.md (architectural decisions)
- .claude/templates/* (official templates)
- external/humanlayer/* (human-in-loop patterns)

**Last Updated:** 2025-11-09
**Author:** Claude Code (Sonnet 4.5)
