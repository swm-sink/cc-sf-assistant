# Claude Code Templates

Templates for creating skills, commands, agents, and workflows.

## Directory Structure

```
.claude/templates/
├── skills/
│   └── SKILL_TEMPLATE.md           # Skill template with YAML frontmatter
├── commands/
│   └── COMMAND_TEMPLATE.md         # Slash command template
├── agents/
│   └── AGENT_TEMPLATE.md           # Subagent template with tool permissions
└── workflows/
    ├── TDD_WORKFLOW.md             # Test-Driven Development workflow
    └── RESEARCH_PLAN_IMPLEMENT_VERIFY.md  # RPIV workflow

```

## Usage

### Creating a New Skill
1. Copy `skills/SKILL_TEMPLATE.md` to `.claude/skills/dev/your-skill/` or `.claude/skills/prod/your-skill/`
2. Rename to `SKILL.md`
3. Update YAML frontmatter (name, description)
4. Fill in instructions following Progressive Disclosure pattern
5. Add `scripts/`, `references/`, `templates/` subdirectories as needed

### Creating a New Command
1. Copy `commands/COMMAND_TEMPLATE.md` to `.claude/commands/dev/` or `.claude/commands/prod/`
2. Rename to match command name (e.g., `monthly-close.md` → `/dev:monthly-close`)
3. Update YAML frontmatter (optional)
4. Define workflow steps
5. Add human checkpoints if needed

### Creating a New Agent
1. Copy `agents/AGENT_TEMPLATE.md` to `.claude/agents/dev/` or `.claude/agents/prod/`
2. Rename to match agent purpose (e.g., `script-generator.md`)
3. Update YAML frontmatter (name, description, tools, model)
4. Define role, capabilities, constraints
5. Use minimal tool permissions for focused agents

### Using Workflows
- **TDD Workflow**: Follow for all financial calculation scripts
- **RPIV Workflow**: Follow for new features or complex changes

## Best Practices

**Skills:**
- Keep SKILL.md concise (<200 lines)
- Write clear descriptions for auto-invocation
- Use Progressive Disclosure (split large content)

**Commands:**
- Use $ARGUMENTS placeholder for user input
- Add human checkpoints for critical decisions
- Specify allowed-tools for security

**Agents:**
- Grant minimal tool permissions
- Use read-only for reviewers/auditors
- Define clear role and constraints

**Workflows:**
- Always use TDD for financial scripts
- Get human approval at phase transitions
- Independent verification required

## Sources

Templates based on:
- Anthropic official skills repository
- Claude Code best practices (2025)
- Community examples (awesome-claude-skills, skill-factory)
- TDD best practices with Claude Code

## Last Updated
2025-11-08
