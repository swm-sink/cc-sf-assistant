---
name: creating-commands
description: Use when creating slash commands, building workflows, need command scaffolding, want /env:command patterns, before writing .claude/commands/*.md, thinking "I need a command template", planning RPIV/approval/reflection/validation/batch/routing/ETL/orchestration/reporting workflows - provides 9 specialized templates with validation for diverse workflow patterns including production-safe approvals and self-improvement loops
---

# Creating Commands

## Overview

**Purpose:** Generate slash commands using specialized templates with built-in validation.

**What this technique does:**
- Provides 9 specialized command templates (RPIV, Human Approval, Reflection, Validation, Batch Processing, Routing, Data Transformation, Orchestration, Reporting)
- Validates command structure, naming, YAML frontmatter, and usage patterns
- Generates commands with proper environment isolation (dev/prod/shared)
- Enforces best practices from Anthropic, HumanLayer, and Google/DeepMind research (2024-2025)

**What this technique doesn't do:**
- Doesn't write command logic for you (provides templates with placeholders)
- Doesn't auto-invoke commands (commands use explicit `/env:name` invocation)
- Doesn't test commands (manual testing required)

**Key principle:** Specialized templates for different workflow patterns ensure consistent structure and production-ready quality.

---

## When to Use

**Use when:**
- Creating a new slash command from scratch
- Need workflow scaffolding (RPIV, approval gates, reflection loops, etc.)
- Building production-safe automation with human checkpoints
- Implementing batch processing, routing, ETL, or reporting workflows
- Want validated command structure (9 template types)

**Don't use when:**
- Editing existing command (use Read/Edit tools directly)
- Creating skills (use creating-skills instead)
- Creating agents (use creating-agents instead)
- Pure scripting (commands are prompts, not scripts)

**Prerequisites:**
- Understand command type needed (RPIV/approval/reflection/validation/etc.)
- Have clear workflow purpose
- Know target environment (dev/prod/shared)

---

## Step-by-Step Instructions

### Step 1: Choose Command Template

**Determine which template to use:**

| Template | Score | Use When | Key Features |
|----------|-------|----------|--------------|
| **RPIV** | 9.8/10 | Complex workflows, multi-step processes | 4 checkpoints, research-first, human-in-loop |
| **Human Approval** | 9.2/10 | Production deployments, financial transactions | Structured approvals, risk assessment, audit trail |
| **Reflection** | 8.8/10 | Iterative refinement, quality gates | Self-evaluation, autonomous improvement |
| **Validation** | 8.6/10 | Systematic checks, consistency validation | Read-only, ✅⚠️❌ reporting |
| **Batch Processing** | 8.4/10 | Multiple files, departments, accounts | Per-item errors, progress tracking |
| **Routing** | 8.2/10 | Request classification, handler delegation | Decision table, deterministic routing |
| **Data Transformation** | 7.8/10 | ETL pipelines, format conversion | Load → Transform → Validate → Output |
| **Orchestration** | 7.5/10 | Multi-agent coordination | Dependency graph, state management |
| **Reporting** | 7.2/10 | Analytics, dashboards, summaries | Aggregate → Analyze → Format → Distribute |

**Expected outcome:** Clear template type chosen.

### Step 2: Run Command Generator

**Use orchestrator script to generate command:**

**Actions:**
1. Navigate to `.claude/skills/creating-commands/scripts/`
2. Run: `python generate_command.py`
3. Answer interactive prompts:
   - Template selection (1-9)
   - Command name (kebab-case)
   - Environment (dev/prod/shared)
   - Description (≤1024 chars)
4. Script generates command in temp directory
5. Script runs all 4 validators
6. If all pass, script commits to `.claude/commands/{env}/{name}.md`

**Expected outcome:** Command scaffold created at `.claude/commands/{env}/{name}.md`.

### Step 3: Fill Placeholders

**Complete template placeholders with actual content:**

**Actions:**
1. Open `.claude/commands/{env}/{name}.md`
2. Find all `{{PLACEHOLDER}}` markers
3. Replace with actual content based on template type:
   - **RPIV:** Research steps, plan components, implementation tasks, verification criteria
   - **Human Approval:** Action, risk_level, reversible flag, urgency, impact
   - **Reflection:** Quality dimensions, threshold, max iterations
   - **Validation:** Check names, expected results, pass criteria
   - **Batch:** Input pattern, transformation steps, error handling
   - **Routing:** Domains, handlers, decision table
4. Remove any unused placeholder sections
5. Adjust structure as needed (templates are starting points)

**Expected outcome:** All placeholders replaced with meaningful content.

### Step 4: Validate Command

**Ensure command passes all validation checks:**

**Actions:**
1. Run all 4 validators:
   ```bash
   python scripts/validate_command_yaml.py .claude/commands/{env}/{name}.md
   python scripts/validate_command_naming.py .claude/commands/{env}/{name}.md
   python scripts/validate_command_structure.py .claude/commands/{env}/{name}.md
   python scripts/validate_command_usage.py .claude/commands/{env}/{name}.md
   ```
2. Fix any errors (exit code 1)
3. Consider warnings (exit code 2)

**Expected outcome:** All validators pass (exit code 0).

### Step 5: Test Command

**Verify command works as expected:**

**Actions:**
1. Invoke command: `/{env}:{name} <args>`
2. Verify workflow executes correctly
3. Test checkpoints (if applicable)
4. Verify output format
5. Iterate based on testing feedback

**Expected outcome:** Command works as designed.

---

## Common Pitfalls

### Pitfall 1: Wrong Template Type

**Symptom:** Command structure doesn't match workflow purpose

**Why it happens:** Unclear distinction between template types

**How to avoid:**
- RPIV: Multi-step workflows with research/planning phases
- Human Approval: Production-critical actions requiring sign-off
- Reflection: Iterative quality improvement loops
- Validation: Systematic verification checks
- Batch: Multiple item processing with error isolation
- Routing: Classification → delegation workflows

### Pitfall 2: Leaving Placeholders Unfilled

**Symptom:** Command contains `{{PLACEHOLDER}}` markers after "completion"

**Why it happens:** Forgot to replace template placeholders

**How to avoid:**
- Search for `{{` in command file
- Replace all placeholders with actual content
- Remove unused sections
- Validators will catch this

### Pitfall 3: Missing Required Sections

**Symptom:** Validators fail with section count mismatch

**Why it happens:** Deleted required sections or added too many

**How to avoid:**
- Respect template section counts (6-9 sections depending on type)
- Don't delete required headers (## Phase, ## Step, etc.)
- Use validate_command_structure.py to verify

---

## Progressive Disclosure

**For detailed information, see:**

**Command-Specific Guides (references/command-guides/):**
- `rpiv-workflow-guide.md` - Deep dive on Research → Plan → Implement → Verify
- `human-approval-guide.md` - Structured approvals, risk assessment, audit trails
- `reflection-guide.md` - Self-improvement loops, quality gates
- `validation-patterns.md` - Systematic checks, ✅⚠️❌ reporting
- `batch-processing-guide.md` - Error handling, progress tracking
- `routing-guide.md` - Classification, decision tables, handler delegation
- `data-transformation-guide.md` - ETL pipelines, quality gates
- `orchestration-guide.md` - Multi-agent coordination, dependency management
- `reporting-guide.md` - Aggregation, formatting, distribution

**Prompting Pattern Guides (references/prompting-patterns/):**
- `own-your-prompts.md` - HumanLayer Factor 2: Prompt ownership
- `reflection-pattern.md` - Anthropic Evaluator-Optimizer pattern
- `planning-pattern.md` - Task decomposition, dependency management
- `human-in-loop.md` - HumanLayer Factor 7: Structured approval requests
- `context-management.md` - HumanLayer Factor 3: Context evolution
- `tool-documentation.md` - Anthropic ACI best practices
- `eval-driven-development.md` - Scientific iteration, A/B testing

**Templates:**
- `assets/templates/COMMAND_RPIV_TEMPLATE.md` (9.8/10, 8 sections)
- `assets/templates/COMMAND_HUMAN_APPROVAL_TEMPLATE.md` (9.2/10, 9 sections)
- `assets/templates/COMMAND_REFLECTION_TEMPLATE.md` (8.8/10, 8 sections)
- `assets/templates/COMMAND_VALIDATION_TEMPLATE.md` (8.6/10, 6 sections)
- `assets/templates/COMMAND_BATCH_PROCESSING_TEMPLATE.md` (8.4/10, 7 sections)
- `assets/templates/COMMAND_ROUTING_TEMPLATE.md` (8.2/10, 7 sections)
- `assets/templates/COMMAND_DATA_TRANSFORMATION_TEMPLATE.md` (7.8/10, 7 sections)
- `assets/templates/COMMAND_ORCHESTRATION_TEMPLATE.md` (7.5/10, 8 sections)
- `assets/templates/COMMAND_REPORTING_TEMPLATE.md` (7.2/10, 7 sections)

**Validation scripts:**
- `scripts/validate_command_yaml.py` - YAML frontmatter validation
- `scripts/validate_command_naming.py` - Kebab-case, environment checks
- `scripts/validate_command_structure.py` - Section count, template-specific rules
- `scripts/validate_command_usage.py` - Usage line, argument validation

**Orchestrator:**
- `scripts/generate_command.py` - Interactive command generation

**Related skills:**
- `creating-skills` - Create auto-invoked skills
- `creating-agents` - Create @agent subagents

---

**This skill enforces best practices from 2024-2025 research: Anthropic Building Effective Agents, HumanLayer 12-Factor Agents, Google/DeepMind agentic patterns, and production lessons.**
