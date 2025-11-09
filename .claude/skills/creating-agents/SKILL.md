---
name: creating-agents
description: Use when creating agents, building subagents, need agent scaffolding, want @agent-name patterns, before writing .claude/agents/*.md, thinking "I need an agent template", planning domain specialist/researcher/reviewer agents - provides 3 validated templates with tool tier enforcement based on 116 production agents
---

# Creating Agents

## Overview

**Purpose:** Generate subagents using specialized templates with built-in validation and tool tier enforcement.

**What this technique does:**
- Provides 3 specialized agent templates (Domain Specialist, Researcher, Reviewer)
- Validates agent structure, naming, YAML frontmatter, and tool tier compliance
- Generates agents with proper tool restrictions (read-only, read+web, full access)
- Enforces best practices from 116 production agents (awesome-claude-code-subagents)

**What this technique doesn't do:**
- Doesn't write agent logic for you (provides templates with placeholders)
- Doesn't auto-invoke agents (agents use explicit `@name` invocation)
- Doesn't test agents (manual testing required)

**Key principle:** 3 distinct tool tiers ensure security and appropriate capabilities per agent type.

---

## When to Use

**Use when:**
- Creating a new agent from scratch
- Need specialized expertise (financial, Python, data analysis, etc.)
- Building read-only reviewer/auditor agents
- Creating research agents with web access
- Want validated agent structure (3 template types)

**Don't use when:**
- Editing existing agent (use Read/Edit tools directly)
- Creating skills (use creating-skills instead)
- Creating slash commands (use creating-commands instead)
- Need orchestration (commands coordinate agents, not agents)

**Prerequisites:**
- Understand agent type needed (domain specialist/researcher/reviewer)
- Have clear domain expertise scope
- Know tool tier requirements

---

## Step-by-Step Instructions

### Step 1: Choose Agent Template

**Determine which template to use:**

| Template | Tool Tier | Use When | Pattern Frequency |
|----------|-----------|----------|-------------------|
| **Domain Specialist** | Full access | Financial expert, Python expert, domain knowledge | PRIMARY (86% of agents) |
| **Researcher** | Read + Web | Codebase exploration, web research, competitive intelligence | 5% of agents |
| **Reviewer** | Read-only | Code review, security audit, compliance verification | 3-5% of agents |

**Expected outcome:** Clear template type chosen.

### Step 2: Run Agent Generator

**Use orchestrator script to generate agent:**

**Actions:**
1. Navigate to `.claude/skills/creating-agents/scripts/`
2. Run: `python generate_agent.py`
3. Answer interactive prompts:
   - Template selection (domain-specialist/researcher/reviewer)
   - Agent name (kebab-case)
   - Description (100-150 chars)
   - Domain (e.g., financial, python, data-analysis)
4. Script generates agent in temp directory
5. Script runs all 4 validators
6. If all pass, script commits to `.claude/agents/{name}.md`

**Expected outcome:** Agent scaffold created at `.claude/agents/{name}.md`.

### Step 3: Fill Placeholders

**Complete template placeholders with actual content:**

**Actions:**
1. Open `.claude/agents/{name}.md`
2. Find all `{{PLACEHOLDER}}` markers
3. Replace with actual content based on template type:
   - **Domain Specialist:** 8-15 domain areas with 8-12 bullets each
   - **Researcher:** Research focus, query types, source validation
   - **Reviewer:** 8 verification checks, output format, approval criteria
4. Remove any unused placeholder sections
5. Adjust structure as needed (templates are starting points)

**Expected outcome:** All placeholders replaced with meaningful content.

### Step 4: Validate Agent

**Ensure agent passes all validation checks:**

**Actions:**
1. Run all 4 validators:
   ```bash
   python scripts/validate_agent_yaml.py .claude/agents/{name}.md
   python scripts/validate_agent_naming.py .claude/agents/{name}.md
   python scripts/validate_agent_structure.py .claude/agents/{name}.md
   python scripts/validate_agent_tools.py .claude/agents/{name}.md
   ```
2. Fix any errors (exit code 1)
3. Consider warnings (exit code 2)

**Expected outcome:** All validators pass (exit code 0).

### Step 5: Test Agent

**Verify agent works as expected:**

**Actions:**
1. Invoke agent: `@{name}` in conversation
2. Verify domain expertise is appropriate
3. Test tool restrictions (e.g., reviewer can't write files)
4. Verify workflow executes correctly
5. Iterate based on testing feedback

**Expected outcome:** Agent works as designed.

---

## Common Pitfalls

### Pitfall 1: Wrong Template Type

**Symptom:** Agent has wrong tools or structure for its purpose

**Why it happens:** Unclear distinction between template types

**How to avoid:**
- Domain Specialist: Full access, comprehensive domain coverage (86% of agents)
- Researcher: Read+web only, investigation structure
- Reviewer: Read-only, verification checklist

### Pitfall 2: Incorrect Tool Tier

**Symptom:** Validators fail with tool tier mismatch

**Why it happens:** Manually editing tools without understanding restrictions

**How to avoid:**
- Domain Specialist: `[Read, Write, Edit, Bash, Glob, Grep]` exactly
- Researcher: `[Read, Grep, Glob, WebFetch, WebSearch]` exactly
- Reviewer: `[Read, Grep, Glob]` exactly
- Use validate_agent_tools.py to verify

### Pitfall 3: Leaving Placeholders Unfilled

**Symptom:** Agent contains `{{PLACEHOLDER}}` markers after "completion"

**Why it happens:** Forgot to replace template placeholders

**How to avoid:**
- Search for `{{` in agent file
- Replace all placeholders with actual content
- Remove unused sections
- Validators will catch this

---

## Examples

### Example 1: Creating a Domain Specialist

**Scenario:** "I need a fintech expert agent for payment systems"

**Application:**

**Step 1:** Choose template → Domain Specialist (PRIMARY pattern)

**Step 2:** Run generator:
```bash
python generate_agent.py
# Template: domain-specialist
# Name: fintech-analyst
# Description: Financial technology expert specializing in payment systems, compliance, and fraud detection
# Domain: financial-technology
```

**Step 3:** Fill placeholders:
- `{{AREA_1_NAME}}`: Payment Processing Systems
- `{{AREA_1_BULLETS}}`: ACH, wire transfers, card networks, real-time payments, etc.
- 8-15 total areas with 8-12 bullets each

**Step 4:** Validate → All 4 validators pass ✅

**Step 5:** Test → `@fintech-analyst` provides payment systems expertise

**Result:** Agent provides comprehensive financial domain knowledge.

### Example 2: Creating a Reviewer

**Scenario:** "I need a code review agent that can't modify code"

**Application:**

**Step 1:** Choose template → Reviewer (read-only constraint)

**Step 2:** Run generator (reviewer template auto-assigns read-only tools)

**Step 3:** Fill placeholders:
- `{{CHECK_1_NAME}}`: Code Quality
- `{{CHECK_2_NAME}}`: Security Vulnerabilities
- 8 total verification checks

**Step 4:** Validate → Tool tier check confirms read-only ✅

**Step 5:** Test → `@code-reviewer` can analyze but not modify files

**Result:** Agent performs verification without modification risk.

---

## Progressive Disclosure

**For detailed information, see:**

**Agent-Specific Guides (references/agent-guides/):**
- `domain-specialist-guide.md` - Constrained expertise, comprehensive coverage (PRIMARY pattern)
- `readonly-researcher-guide.md` - Investigation structure, web research tools
- `full-access-implementer-guide.md` - Read-only verification, checklist design

**Templates:**
- `assets/templates/AGENT_DOMAIN_SPECIALIST_TEMPLATE.md` (9.5/10, PRIMARY - 86% frequency)
- `assets/templates/AGENT_READONLY_RESEARCHER_TEMPLATE.md` (8.6/10, web tools)
- `assets/templates/AGENT_FULL_ACCESS_IMPLEMENTER_TEMPLATE.md` (7.8/10, read-only)

**Validation scripts:**
- `scripts/validate_agent_yaml.py` - YAML frontmatter validation
- `scripts/validate_agent_naming.py` - Kebab-case, name consistency
- `scripts/validate_agent_structure.py` - Section count, template-specific rules
- `scripts/validate_agent_tools.py` - Tool tier enforcement

**Orchestrator:**
- `scripts/generate_agent.py` - Interactive agent generation

**Related skills:**
- `creating-skills` - Create auto-invoked skills
- `creating-commands` - Create /command workflows

---

**This skill enforces best practices from 116 production agents (awesome-claude-code-subagents) and 12-Factor Agents principles.**
