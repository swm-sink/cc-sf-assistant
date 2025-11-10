# .claude/ Meta-Infrastructure - Behavioral Overrides

**Purpose:** Component-specific behavior for .claude/ directory (skills, agents, commands).

**Inherits:** Root CLAUDE.md (all core principles apply)

**Overrides:** This file takes precedence for .claude/** work

---

## Meta-Infrastructure Status

**Current:**
- ✅ Phase 1 Complete: 4 meta-skills (creating-skills, creating-agents, creating-commands, enforcing-RPIV)
- 🔄 Phase 2 In Progress: 5 holistic meta-skills (hierarchical-context-manager, hook-factory, system-coherence-validator, financial-quality-gate, multi-agent-workflow-coordinator)
- ⏸️ Phase 3 Pending: User approval + validation before domain component creation

**What Requires User Approval:**
- ❌ Creating financial-validator skill → Domain component (get approval)
- ❌ Creating @code-reviewer agent → Domain component (get approval)
- ❌ Creating /variance-analysis command → Domain component (get approval)
- ✅ Improving creating-skills skill → Meta-infrastructure (proceed)
- ✅ Creating hook-factory skill → Meta-infrastructure (proceed with plan approval)

**If User Requests Domain Component Without Approval:**
1. Acknowledge request
2. Explain meta-infrastructure-first principle
3. Propose: "Let me use [meta-skill] to create this properly"
4. Get explicit approval before proceeding

---

## Progressive Disclosure

**SKILL.md / Agent / Command Size:**
- Target: ≤200 lines for main file
- Structure: Main file + references/ for details
- Rationale: Claude processes smaller files faster

**Example:**
```
.claude/skills/skill-name/
├── SKILL.md                # ≤200 lines
├── README.md
├── references/             # Detailed docs (<600 lines each)
└── templates/              # Code templates
```

---

## CSO Optimization Requirements

**Target Scores:**
- **Critical components:** CSO ≥0.8 (Hook Factory, Financial Quality Gate)
- **High priority components:** CSO ≥0.7 (other meta-skills, key agents)

**CSO Framework (4 Pillars):**
1. **Trigger Phrases (40% weight):** Exact phrases users say
2. **Symptoms (30% weight):** Problems this solves
3. **Agnostic Keywords (20% weight):** Generic terms
4. **Examples (10% weight):** Concrete usage examples

---

## YAML Frontmatter Validation

**Skills:**
```yaml
---
name: skill-name
type: Discipline | Technique | Pattern | Reference
auto_invoke: true | false
cso_score: 0.73
created: 2025-11-10
---
```

**Agents:**
```yaml
---
name: agent-name
tool_tier: read_only | read_web | full_access
description: Brief description
created: 2025-11-10
---
```

**Commands:**
```yaml
---
name: command-name
workflow_type: RPIV | Human Approval | Validation | etc.
description: Brief description
created: 2025-11-10
---
```

---

## Naming Conventions

**Files:** kebab-case (skill-name/SKILL.md, agent-name.md, command-name.md)

**Directories:**
```
.claude/
├── skills/skill-name/          # kebab-case
├── agents/
│   ├── validators/             # group by function
│   └── generators/
├── commands/
│   ├── development-workflows/  # group by context
│   └── fpa-workflows/
```

---

## Tool Tier Enforcement

**Read-Only Agents (Validators):**
- Can use: Read, Glob, Grep, WebFetch
- Cannot use: Write, Edit, Bash
- Examples: @databricks-validator, @report-formatter

**Full Access Agents (Generators):**
- Can use: All tools including Write, Edit, Bash
- Examples: @script-generator, @test-generator

**Rationale:** Validators should not accidentally modify files

---

## User Interface Layer

**Commands (.claude/commands/):**
- Slash commands hide complexity from non-technical users
- Interactive prompts for file paths, date ranges
- Human-friendly error messages
- Example: `/variance-analysis budget.xlsx actuals.xlsx`

---

**Precedence:** This config overrides root CLAUDE.md for .claude/**
**Inherits:** All root principles (DRY, chain of verification, RPIV workflow)
