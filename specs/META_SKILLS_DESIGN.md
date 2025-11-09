# Meta-Skills Design Specification

**Purpose:** Design meta-skills that create skills, commands, and agents following Anthropic best practices and Claude Sonnet 4.5 capabilities.

**Priority:** CRITICAL - Must be built BEFORE Phase 1 implementation

---

## Meta-Skill 1: skill-creator

**Location:** `.claude/skills/shared/skill-creator/SKILL.md`

**Purpose:** Generate new skills following Progressive Disclosure pattern with correct YAML frontmatter and 2025 architecture

**Auto-Invocation Trigger:** User requests "create a skill for..." or "I need a skill that..."

**Architecture Note (November 2025):** Commands are now INSIDE skills at `.claude/skills/{env}/{skill-name}/workflows/`, not standalone in `.claude/commands/`. Skills provide reusable expertise, commands are workflows that use that expertise.

### Workflow

1. **Gather Requirements:**
   - Skill name (kebab-case)
   - Description (for auto-invocation detection)
   - Target environment (dev/prod/shared)
   - Does this skill need commands (user-triggered workflows)?
   - Tool permissions needed (Read, Edit, Write, Bash, etc.)
   - Complexity estimate (simple/medium/complex)

2. **Research Phase:**
   - Search .claude/templates/skills/SKILL_TEMPLATE.md
   - Search existing skills for similar patterns
   - Review Progressive Disclosure best practices
   - Check Claude Sonnet 4.5 capabilities
   - **Sources:**
     - https://docs.claude.com/en/docs/claude-code/skills
     - https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
     - https://danielmiessler.com/blog/when-to-use-skills-vs-commands-vs-agents

3. **Generate Spec:**
   - Present skill specification to user
   - Include: name, description, workflows (commands), context files, tool permissions
   - User approval checkpoint

4. **Implement:**
   - Create directory structure:
     ```
     .claude/skills/{env}/{skill-name}/
     ├── SKILL.md                   # Main skill file (routing logic)
     ├── workflows/                 # Commands go here
     │   ├── command1.md
     │   └── command2.md
     └── context/                   # Supporting context files
         ├── formulas.md
         └── edge-cases.md
     ```
   - Generate SKILL.md with YAML frontmatter
   - Create workflows/ directory if skill needs commands
   - Create context/ directory for Progressive Disclosure

5. **Validate:**
   - Verify YAML frontmatter syntax
   - Check description clarity for auto-invocation
   - Ensure Progressive Disclosure (SKILL.md <200 lines, details in context/)
   - Test auto-invocation detection
   - Verify workflows/ commands have correct syntax

6. **Document:**
   - Add skill to README.md
   - Update .claude/skills/{env}/README.md if exists
   - Commit with message: `feat: add {skill-name} skill`

### Template Generation

```yaml
---
name: {skill-name}
description: {concise description for auto-invocation}
version: 1.0.0
author: claude-code
tags: [{tag1}, {tag2}]
---

# {Skill Title}

**Purpose:** {One sentence purpose}

**Auto-Invocation:** Triggered when user {specific condition}

## Quick Start

{1-2 sentence quick start}

## Workflow

1. {Step 1}
2. {Step 2}
...

## Examples

{Concrete examples}

## Progressive Disclosure

For detailed information, see:
- `references/detailed-guide.md`
- `scripts/implementation.py`
```

### Tool Permissions Strategy

- **Read-only skills:** `allowed-tools: [Read, Glob, Grep]`
- **Analysis skills:** `allowed-tools: [Read, Bash]`
- **Code generation:** `allowed-tools: [Read, Write, Edit, Bash]`
- **Meta-skills:** `allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]`

---

## Meta-Skill 2: command-creator

**Location:** `.claude/skills/shared/command-creator/SKILL.md`

**Purpose:** Generate workflow commands (within skills) with human checkpoints and $ARGUMENTS placeholders

**Auto-Invocation Trigger:** User requests "create a command for..." or "I need a /command that..." or "create a workflow for..."

**Architecture Note (November 2025):** Commands are workflows within skills, not standalone files. They live in `.claude/skills/{env}/{skill-name}/workflows/` and are invoked as `/{env}:{skill-name}:{workflow-name}`

### Workflow

1. **Gather Requirements:**
   - Command name (kebab-case)
   - Environment (dev/prod/shared)
   - Arguments needed ($BUDGET_FILE, $ACTUAL_FILE, etc.)
   - Human checkpoints required
   - Skill dependencies
   - Model preference (sonnet/haiku)

2. **Research Phase:**
   - Search .claude/templates/commands/COMMAND_TEMPLATE.md
   - Search existing commands for patterns
   - Review workflow templates (TDD, RPIV)

3. **Generate Spec:**
   - Present command specification
   - Include: workflow steps, arguments, checkpoints, skills invoked
   - User approval checkpoint

4. **Implement:**
   - Identify or create parent skill (commands must belong to a skill)
   - Create file: `.claude/skills/{env}/{skill-name}/workflows/{command-name}.md`
   - Generate YAML frontmatter + workflow
   - Add $ARGUMENTS placeholders
   - Insert human approval checkpoints
   - Update parent SKILL.md to reference new workflow

5. **Validate:**
   - Verify YAML frontmatter
   - Check argument substitution
   - Ensure human checkpoints at critical decisions
   - Test command invocation

6. **Document:**
   - Add to README.md usage section
   - Update parent SKILL.md's "Available Workflows" section
   - Update QUICK_START.md if user-facing
   - Commit: `feat: add /{env}:{skill-name}:{workflow-name} workflow`

### Template Generation

```markdown
---
description: {One-line description}
model: sonnet
allowed-tools: [Read, Write, Bash]
---

# {Command Title}

**Usage:** `/{env}:{skill-name}:{workflow-name} $ARG1 $ARG2`

**Purpose:** {One sentence}

**Parent Skill:** See `.claude/skills/{env}/{skill-name}/SKILL.md`

## Workflow

### Step 1: {Step Name}

{Instructions}

**Arguments:**
- `$ARG1` - {Description}
- `$ARG2` - {Description}

### Step 2: {Human Checkpoint}

Present {what} to user for approval:
- {Item 1}
- {Item 2}

**Wait for user approval before proceeding.**

### Step 3: {Execution}

Invoke skills:
1. `/skills/{skill-name}` with {parameters}
2. Execute {operation}

### Step 4: {Completion}

Output:
- {Result 1}
- {Result 2}

## Example

```bash
/{env}:{skill-name}:{workflow-name} budget.xlsx actuals.xlsx
```

**Real Example:**
```bash
/prod:variance-analyzer:analyze budget_2025.xlsx actuals_nov_2025.xlsx
```
```

---

## Meta-Skill 3: agent-creator

**Location:** `.claude/skills/shared/agent-creator/SKILL.md`

**Purpose:** Generate subagents with minimal tool permissions and clear roles

**Auto-Invocation Trigger:** User requests "create an agent for..." or "I need an agent that..."

### Workflow

1. **Gather Requirements:**
   - Agent name (kebab-case)
   - Environment (dev/prod/shared)
   - Role and responsibilities
   - Tool permissions (minimal principle)
   - Model (sonnet for complex, haiku for simple)
   - Read-only vs read-write

2. **Research Phase:**
   - Search .claude/templates/agents/AGENT_TEMPLATE.md
   - Search existing agents for patterns
   - Review Anthropic agent best practices

3. **Generate Spec:**
   - Present agent specification
   - Include: role, capabilities, constraints, tool permissions
   - Justify tool permissions
   - User approval checkpoint

4. **Implement:**
   - Create file: `.claude/agents/{env}/{agent-name}.md`
   - Generate YAML frontmatter
   - Define role, capabilities, constraints
   - Set minimal tool permissions

5. **Validate:**
   - Verify YAML frontmatter
   - Check tool permissions (minimal necessary)
   - Ensure clear role definition
   - Test agent invocation

6. **Document:**
   - Add to README.md
   - Commit: `feat: add {agent-name} agent`

### Template Generation

```markdown
---
name: {agent-name}
description: {One-line description}
model: sonnet
allowed-tools: [Read, Grep, Glob]
---

# {Agent Title}

**Role:** {Agent's specific role}

**Responsibilities:**
1. {Responsibility 1}
2. {Responsibility 2}
3. {Responsibility 3}

## Capabilities

- {Capability 1}
- {Capability 2}

## Constraints

- {Constraint 1 - e.g., "Read-only access"}
- {Constraint 2 - e.g., "No external API calls"}
- {Constraint 3 - e.g., "Must present findings, not make decisions"}

## Tool Permissions

**Allowed:** {list tools}

**Rationale:** {Why these specific tools}

## Workflow

When invoked:
1. {Step 1}
2. {Step 2}
3. Present findings to user

## Example Invocation

```
/agents/{agent-name} {parameters}
```
```

### Tool Permission Guidelines

**Read-Only Agents (Reviewers, Auditors):**
```yaml
allowed-tools: [Read, Grep, Glob]
```

**Analysis Agents:**
```yaml
allowed-tools: [Read, Grep, Glob, Bash]
```

**Code Generation Agents:**
```yaml
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
```

**Validation Agents:**
```yaml
allowed-tools: [Read, Bash]  # Run tests but don't modify
```

---

## Context Management Strategy

### Progressive Disclosure Pattern

**Problem:** Large skill files overwhelm context window

**Solution:**
```
.claude/skills/dev/variance-analyzer/
├── SKILL.md                    # <200 lines, quick start
├── references/
│   ├── variance-formulas.md   # Detailed formulas
│   ├── favorability-rules.md  # Account type rules
│   └── edge-cases.md          # Division by zero, negatives
├── scripts/
│   └── variance_template.py   # Reusable code
└── templates/
    └── variance_report.xlsx    # Output template
```

SKILL.md references these files, agent loads on-demand.

### Skill Invocation Patterns

**Auto-Invocation (Background):**
- Decimal precision enforcer (always active)
- Audit trail enforcer (always active)
- Python best practices (when writing .py files)

**Explicit Invocation (User Command):**
- `/dev:create-script` → invokes script-generator skill
- `/prod:variance-analysis` → invokes variance-analyzer skill

**Agent-Invoked:**
- script-generator agent invokes python-best-practices skill
- code-reviewer agent invokes security-scanner skill

---

## Integration with .claude/templates/

Meta-skills use templates as base:

1. **skill-creator** reads `SKILL_TEMPLATE.md`, customizes YAML + content
2. **command-creator** reads `COMMAND_TEMPLATE.md`, adds workflow + checkpoints
3. **agent-creator** reads `AGENT_TEMPLATE.md`, sets tool permissions + role

Templates updated → all generated skills/commands/agents benefit

---

## Claude Sonnet 4.5 Optimizations

**Leverage Enhanced Capabilities:**

1. **Extended Thinking:** Meta-skills use thinking blocks for complex decisions
   - Analyze user requirements before generating spec
   - Verify YAML syntax before writing files
   - Check for duplicate skills before creating

2. **Parallel Tool Execution:** Generate multiple files simultaneously
   - Create SKILL.md + subdirectories in one message
   - Read multiple templates in parallel

3. **Long-Horizon Reasoning:** Plan multi-step workflows
   - Research → Plan → Implement → Verify
   - Track dependencies across multiple skill creations

4. **Improved Code Generation:** Generate Python scripts for skill implementations
   - Type hints enforced
   - Decimal precision enforced
   - Audit logging included

---

## Quality Gates for Generated Artifacts

**Pre-Creation Checks:**
- [ ] Name follows kebab-case convention
- [ ] Description clear for auto-invocation (skills only)
- [ ] Environment (dev/prod/shared) appropriate
- [ ] Tool permissions minimal
- [ ] No duplicate name in target directory

**Post-Creation Validation:**
- [ ] YAML frontmatter valid
- [ ] File size <200 lines OR Progressive Disclosure used
- [ ] Examples included
- [ ] Committed to git with conventional commit message

**Runtime Validation:**
- [ ] Auto-invocation triggers correctly (skills)
- [ ] Arguments substituted correctly (commands)
- [ ] Tool permissions respected (agents)

---

## Meta-Skill Dependencies

```
skill-creator
├── Reads: .claude/templates/skills/SKILL_TEMPLATE.md
├── Searches: .claude/skills/**/* (find similar)
└── Creates: .claude/skills/{env}/{name}/SKILL.md

command-creator
├── Reads: .claude/templates/commands/COMMAND_TEMPLATE.md
├── Searches: .claude/commands/**/*.md (find patterns)
└── Creates: .claude/commands/{env}/{name}.md

agent-creator
├── Reads: .claude/templates/agents/AGENT_TEMPLATE.md
├── Searches: .claude/agents/**/*.md (find similar)
└── Creates: .claude/agents/{env}/{name}.md
```

All three use shared utilities:
- YAML validator
- Convention checker (kebab-case, description clarity)
- Git commit helper

---

## Implementation Priority

**Phase 0A (Before Phase 1):**
1. Create `skill-creator` meta-skill
2. Create `command-creator` meta-skill
3. Create `agent-creator` meta-skill

**Validation:**
- Use skill-creator to create a test skill
- Use command-creator to create a test command
- Use agent-creator to create a test agent
- Verify all artifacts follow templates correctly

**Then Proceed to Phase 1.**

---

## Success Criteria

- [ ] All 3 meta-skills created and tested
- [ ] Generated artifacts follow template conventions
- [ ] YAML frontmatter valid in all generated files
- [ ] Progressive Disclosure used when needed
- [ ] Tool permissions minimal and justified
- [ ] Git commits follow conventional commits
- [ ] Documentation updated (README.md)

---

**References:**
- Anthropic Skill Tool documentation
- Claude Sonnet 4.5 prompt engineering best practices
- .claude/templates/ directory
- Community examples: skill-creator (Anthropic), agent-skill-creator (GitHub)

**Last Updated:** 2025-11-08
