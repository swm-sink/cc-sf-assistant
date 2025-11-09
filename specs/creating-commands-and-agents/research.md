# Creating Commands & Agents Skills - Research

**Date:** 2025-11-09
**Status:** Research Phase Complete
**Scope:** Deep exploration of patterns for meta-skills that generate slash commands and subagents

---

## Executive Summary

**Objective:** Create two meta-skills (`creating-commands` and `creating-agents`) that follow the proven pattern of `creating-skills`.

**Key Findings:**
1. **Validated Templates:** Multi-agent analysis recommends **9 command templates + 3 agent templates** (12 total, validated against 116 external agents + 12-factor principles + Anthropic/HumanLayer/Google research 2024-2025)
2. **External Validation:** 116 agents in awesome-claude-code-subagents + Anthropic Building Effective Agents + HumanLayer 12-Factor Agents + Google/DeepMind agentic patterns + Production lessons 2024-2025
3. **Architecture Model:** Follow creating-skills pattern (templates + validators + orchestrator + guides)
4. **Tool Patterns:** Commands allow full tools, agents use 3 distinct tool tiers (read-only, read+web, full)
5. **CSO Not Needed:** Commands/agents use explicit invocation (`/command`, `@agent`), not auto-invocation
6. **Critical Finding:** Orchestration is a COMMAND responsibility, not agent capability (commands coordinate agents)
7. **New Patterns:** Reflection (self-improvement), Human Approval (production safety), Routing (intelligent classification)
8. **Prompting Patterns:** 7 optimal prompting pattern guides from leading research (Anthropic, HumanLayer, Google, production)

**Deliverables Needed:**
- `.claude/skills/creating-commands/` - Command generator skill (9 templates, 16 reference guides)
- `.claude/skills/creating-agents/` - Agent generator skill (3 templates, 10 reference guides)
- Each with: SKILL.md, templates/, scripts/, references/

**Notes:**
- See `research-validation-addendum.md` for 116-agent validation analysis
- New templates/patterns based on 2024-2025 research (Anthropic, HumanLayer/Dex Horthy, Google/DeepMind, production lessons)

---

## Part 1: Pattern Analysis from creating-skills

### 1.1 Proven Architecture

**Source:** `/home/user/cc-sf-assistant/.claude/skills/creating-skills/`

**Directory Structure:**
```
creating-skills/
├── SKILL.md                           # Main skill definition (314 lines)
├── assets/
│   └── templates/
│       ├── technique-template.md      # 246 lines, 6 sections
│       ├── pattern-template.md        # 260 lines, 7 sections
│       ├── discipline-template.md     # 525 lines, 12 sections
│       └── reference-template.md      # 220 lines, 5 sections
├── scripts/
│   ├── generate_skill.py              # Orchestrator (382 lines)
│   ├── validate_yaml.py               # YAML frontmatter (147 lines)
│   ├── validate_naming.py             # Active voice check (184 lines)
│   ├── validate_structure.py          # Section count (294 lines)
│   ├── validate_cso.py                # CSO score (205 lines)
│   └── validate_rationalization.py    # Discipline bulletproofing (302 lines)
└── references/
    ├── cso-guide.md                   # CSO optimization (484 lines)
    ├── rationalization-proofing.md    # Discipline techniques (712 lines)
    └── testing-protocol.md            # TDD for skills (350 lines est)
```

**Key Insights:**
- **4 templates** cover skill type spectrum (technique → pattern → discipline → reference)
- **6 validators** ensure quality (5 specific + 1 orchestrator)
- **3 guides** provide progressive disclosure
- **Atomic operations:** Temp dir → validate → commit or rollback

### 1.2 Template Placeholder Pattern

**Source:** `.claude/skills/creating-skills/assets/templates/technique-template.md`

**Placeholder Format:**
```markdown
---
name: {{SKILL_NAME}}
description: {{CSO_OPTIMIZED_DESCRIPTION}}
---

# {{SKILL_TITLE}}

## Overview

**Purpose:** {{ONE_SENTENCE_PURPOSE}}

**What this technique does:**
- {{BENEFIT_1}}
- {{BENEFIT_2}}
- {{BENEFIT_3}}
```

**Benefits:**
- Clear indication of what needs customization (`{{VARIABLE}}`)
- F-string compatible (Python: `template.format(**replacements)`)
- Easy to validate (search for remaining `{{` after generation)
- Self-documenting (placeholder names explain purpose)

### 1.3 Validation Strategy

**5-Validator Pattern:**

| Validator | Purpose | Exit Codes | Key Checks |
|-----------|---------|------------|------------|
| `validate_yaml.py` | YAML frontmatter syntax | 0=pass, 1=error, 2=warning | Required fields, kebab-case name, description length |
| `validate_naming.py` | Active voice convention | 0=pass, 1=error | Verb-first pattern (`creating-X` not `X-creator`) |
| `validate_structure.py` | Section completeness | 0=pass, 1=error, 2=warning | Required sections by type (6 for technique, 12 for discipline) |
| `validate_cso.py` | Auto-invocation score | 0=pass, 1=error, 2=warning | CSO ≥0.7 (trigger phrases, symptom keywords) |
| `validate_rationalization.py` | Discipline proofing | 0=pass, 1=error | Iron Law, negations, table, red flags |

**Orchestrator Pattern:** `generate_skill.py`
1. Interactive prompts (skill name, type, title, description)
2. Select template based on type
3. Generate in temp directory with placeholder replacement
4. Run all validators sequentially
5. If all pass (exit code 0): move to `.claude/skills/{name}/SKILL.md`
6. If any fail (exit code 1): show errors, rollback temp dir
7. Warnings (exit code 2): show but allow commit

---

## Part 2: Command Structure Analysis

### 2.1 Official Requirements

**Source:** `docs.claude.com/en/docs/claude-code/slash-commands` (via research.md)

**YAML Frontmatter Fields:**

| Field | Required | Type | Purpose | Example |
|-------|----------|------|---------|---------|
| `description` | YES | string (≤1024 chars) | Shown in /help menu | "Budget vs actual variance analysis with human-in-loop checkpoints" |
| `model` | No | string | Force specific model | `sonnet`, `opus`, `haiku`, or model ID |
| `allowed-tools` | No | array | Restrict tool access | `[Read, Write, Edit, Bash, Glob, Grep]` |
| `argument-hint` | No | string | Hint for args | `<budget-file> <actual-file> [output-file]` |
| `disable-model-invocation` | No | boolean | Prevent auto-invoke | `false` (default) |

**Naming Convention:**
- File: `kebab-case.md` (e.g., `variance-analysis.md`)
- Invocation: `/environment:command-name` (e.g., `/prod:variance-analysis`)
- Environment: `dev/`, `prod/`, `shared/`

### 2.2 Content Structure Patterns

**Pattern A: RPIV (Research → Plan → Implement → Verify)**

**Source:** `.claude/commands/prod/variance-analysis.md` (184 lines)

**Structure:**
```markdown
---
description: Brief description
---

# Command Title

**Usage:** /command <arg1> <arg2> [arg3]
**Purpose:** 1-2 sentence explanation

---

## Workflow (Human-in-Loop)

### STEP 1: RESEARCH Phase
[Investigation steps without implementation]
**CHECKPOINT 1:** Present research findings. Wait for approval.

### STEP 2: PLAN Phase
[Specification creation without implementation]
**CHECKPOINT 2:** Present plan. Wait for approval.

### STEP 3: IMPLEMENT Phase
[Task-by-task execution with progress tracking]

| Task | Status | Notes |
|------|--------|-------|
| Task 1 | Pending | Details |
| Task 2 | Pending | Details |

**CHECKPOINT 3:** Review after major phases.

### STEP 4: VERIFY Phase
[Independent validation]
**CHECKPOINT 4:** Final approval before delivery.

---

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Example Invocation
/command file1.xlsx file2.xlsx output.xlsx

## Anti-Patterns
❌ Don't do this
✅ Do this instead
```

**Characteristics:**
- 4 human checkpoints (after Research, Plan, mid-Implement, Verify)
- Progress table for implementation tracking
- Success criteria as checklist
- Example invocation with real args
- Anti-patterns section

**Pattern B: Validation Checks**

**Source:** `.claude/commands/shared/sync-docs.md` (269 lines)

**Structure:**
```markdown
---
description: Validate documentation consistency
model: sonnet
---

# Command Title

**Purpose:** What gets validated

---

## Validation Checks

### Check 1: [Name]
**What to verify:** Description
**Expected result:** Success criteria
**Action steps:**
1. Read file X
2. Compare with Y
3. Report status

### Check 2: [Name]
...

---

## Validation Report Format

**Output Structure:**
- ✅ PASS: Description
- ⚠️ WARNING: Description (acceptable)
- ❌ ERROR: Description (critical)

---

## Usage Example
/command
Expected output: [sample]
```

**Characteristics:**
- Numbered validation checks (10 in sync-docs)
- No human checkpoints (single execution)
- Structured report format (✅⚠️❌)
- Read-only operations
- Clear distinction: critical errors vs acceptable warnings

**Pattern C: Batch Processing**

**Source:** Multi-agent analysis recommendation (not yet implemented)

**Expected Structure:**
```markdown
---
description: Process multiple files with progress tracking
---

# Batch Processing Command

**Usage:** /command <input-dir> <output-dir> [pattern]

---

## Workflow

### Phase 1: Discovery
1. Scan input directory for files matching pattern
2. Count files, estimate processing time
3. Present file list for approval

**CHECKPOINT 1:** Approve file list before processing.

### Phase 2: Processing Loop
For each file:
1. Load and validate
2. Apply transformation
3. Handle errors gracefully (log, continue)
4. Update progress

**Progress Tracking:**
| File | Status | Result | Error |
|------|--------|--------|-------|
| file1.xlsx | Complete | ✅ | - |
| file2.xlsx | In Progress | - | - |
| file3.xlsx | Pending | - | - |

### Phase 3: Summary Report
- Files processed: X/Y
- Successes: X
- Failures: Y (with details)
- Output location: path

---

## Error Handling
- Per-file errors don't stop batch
- Log errors to error_log.txt
- Include failed files in summary
```

**Characteristics:**
- Loop over multiple files
- Per-file error handling (don't stop batch)
- Progress tracking table
- Summary report with counts
- Graceful degradation

### 2.3 Validated Template Recommendations

**Source:** Multi-agent analysis + External pattern research (116 agents, 12-factor principles) + Anthropic/HumanLayer/Google research 2024-2025

**Final Recommendations (9 templates):**

| Template | Score | Use When | Lines | Sections | Unique Features |
|----------|-------|----------|-------|----------|-----------------|
| **COMMAND_RPIV_TEMPLATE.md** | 9.8/10 | Complex workflows (variance, consolidation, audits) | ~250 | 8 | 4 checkpoints, research-first, human-in-loop |
| **COMMAND_HUMAN_APPROVAL_TEMPLATE.md** | 9.2/10 | Production deployments, financial transactions, compliance | ~270 | 9 | Structured approval requests, risk assessment, audit trail |
| **COMMAND_REFLECTION_TEMPLATE.md** | 8.8/10 | Iterative refinement, quality gates, self-critique loops | ~260 | 8 | Self-evaluation, quality thresholds, autonomous improvement |
| **COMMAND_VALIDATION_TEMPLATE.md** | 8.6/10 | Systematic checks (docs, config, data quality) | ~200 | 6 | No checkpoints, ✅⚠️❌ reporting, read-only |
| **COMMAND_BATCH_PROCESSING_TEMPLATE.md** | 8.4/10 | Multiple files/departments/accounts | ~230 | 7 | Per-item errors, progress tracking, summary |
| **COMMAND_ROUTING_TEMPLATE.md** | 8.2/10 | Request classification, specialized handler delegation | ~220 | 7 | Classification first, decision table, model selection |
| **COMMAND_DATA_TRANSFORMATION_TEMPLATE.md** | 7.8/10 | ETL pipelines, data migration, format conversion | ~220 | 7 | Load → Transform → Validate → Output, data quality gates |
| **COMMAND_ORCHESTRATION_TEMPLATE.md** | 7.5/10 | Multi-agent coordination, workflow dependencies | ~240 | 8 | Dependency graph, state management, agent coordination |
| **COMMAND_REPORTING_TEMPLATE.md** | 7.2/10 | Analytics, dashboards, executive summaries | ~210 | 7 | Aggregate → Analyze → Format → Distribute, multi-format output |

**New Templates (2024-2025 Research):**
- **Human Approval (9.2/10):** HumanLayer Factor 7 pattern - production-safe automation with structured approvals
- **Reflection (8.8/10):** Anthropic Evaluator-Optimizer + Google/DeepMind self-feedback pattern
- **Routing (8.2/10):** Anthropic Routing pattern - deterministic classification before delegation

**Existing Templates (Validated):**
- **RPIV, Validation, Batch, Data Transformation, Orchestration, Reporting:** All validated against project patterns and FP&A needs

### 2.4 New Command Templates (2024-2025 Research)

**1. COMMAND_HUMAN_APPROVAL_TEMPLATE.md (Score: 9.2/10)**

**Source:** HumanLayer Factor 7 (Contact Humans with Tools) + 12-Factor Agents + Production lessons 2024-2025

**Use Cases:**
- Production deployments requiring sign-off
- Financial transactions needing approval (wire transfers, large purchases)
- Sensitive data operations (PII access, data deletion)
- Compliance-critical workflows (SOC2, GDPR, regulatory reporting)
- Irreversible actions with significant impact

**Structure (9 sections, ~270 lines):**
```markdown
## Phase 1: Prepare Request
- Gather context for human review
- Document what approval is for
- Assess risk and reversibility

## Phase 2: Request Approval (Structured)
{
  "intent": "request_human_approval",
  "action": "Deploy backend v1.2.3 to production",
  "impact": "Affects 10,000 active users",
  "risk_level": "high",
  "urgency": "medium",
  "reversible": false,
  "estimated_duration": "5 minutes"
}

CHECKPOINT: Explicit user approval required
- Options: Approve / Reject / Request Changes
- Timeout handling (default action or pause)

## Phase 3: Execute (Conditional on Approval)
Only proceed if approved

## Phase 4: Confirm & Audit
- Confirm completion to human
- Log audit trail: {timestamp, user, decision, action, outcome}
```

**Key Differentiators:**
- **Structured approval requests** (JSON format, not ad-hoc questions)
- **Risk assessment built-in** (risk_level, reversible flag)
- **Audit trail for compliance** (who approved, when, what happened)
- **Urgency levels** (prioritize critical approvals)
- **Timeout handling** (prevent workflow hanging)

**HumanLayer Evidence:**
- Factor 7: "Tools for different types of human contact allow for more specificity from the LLM"
- "Enables agents workflows **outside** of the traditional chatGPT-style interface"
- Solves 70-80% performance ceiling problem (agents need human guidance for hard decisions)

**Production Evidence:**
- "Wells Fargo's 245 million interactions without human handoffs" (when properly designed)
- "88% of early adopters report positive ROI" (with proper guardrails)
- Addresses "MD Anderson's $62 million loss on IBM Watson" (lacked proper approval gates)

**Adaptation to Claude Code:**
- Uses Claude's conversational interface for approval requests
- Audit trail via explicit logging + conversation history
- Structured format makes approval context clear
- Timeout via conversation pause/resume patterns

---

**2. COMMAND_REFLECTION_TEMPLATE.md (Score: 8.8/10)**

**Source:** Anthropic Evaluator-Optimizer pattern + Google/DeepMind reflection pattern

**Use Cases:**
- Literary translation requiring iterative refinement
- Complex financial analysis needing peer review simulation
- Content generation with quality gates
- Report writing requiring self-critique loops
- Any output where quality > speed

**Structure (8 sections, ~260 lines):**
```markdown
## Phase 1: DRAFT
Generate initial output without constraints
Document approach and assumptions

## Phase 2: REFLECT
Evaluate own output against criteria:
- Accuracy: Are all facts correct? (verify sources)
- Completeness: Did I miss anything? (check requirements)
- Clarity: Is this understandable? (read from user perspective)
- Edge cases: What could go wrong? (challenge assumptions)
- Quality score: Rate 1-10 on each dimension

## Phase 3: IDENTIFY IMPROVEMENTS
List specific, actionable changes:
1. Fix accuracy issue in section X (cite source)
2. Add missing analysis of Y (addresses gap)
3. Clarify explanation of Z (simpler language)

## Phase 4: REFINE
Implement improvements
Repeat REFLECT → IDENTIFY → REFINE up to N times

## Phase 5: QUALITY GATE
Stop when:
- Quality threshold met (e.g., all dimensions ≥8/10)
- Max iterations reached (prevent infinite loops)
- No further improvements identified

## Phase 6: FINAL OUTPUT
Deliver refined version with quality assessment
```

**Key Differentiators:**
- **Self-evaluation loop** (agent critiques its own work)
- **Iterative refinement** (not single-pass like RPIV)
- **Quality threshold gates** (objective stopping criteria)
- **No human checkpoints during reflection** (autonomous improvement)
- **Documented improvement rationale** (transparency)

**Anthropic Evidence:**
- Evaluator-Optimizer: "One LLM generates responses while another provides iterative feedback"
- "Works well for literary translation and complex search tasks requiring refinement"
- "When tasks require handling exceptions or adapting to changing conditions"

**Google/DeepMind Evidence:**
- Reflection pattern: "Self-feedback mechanism where an AI agent evaluates its outputs before finalizing responses"
- "Analyzing its work to identify errors and refine its approach"

**Production Evidence:**
- "The difference between a clever demo and a reliable AI agent comes down to engineering rigor"
- "Evaluation-driven development is applying the scientific method to building ML systems"

**Adaptation to Claude Code:**
- Uses internal loop structure (no subagent spawning needed)
- Reflection criteria defined in command prompt
- Quality gates prevent infinite loops (max iterations + threshold)
- Works well with existing Claude capabilities (self-critique is natural for LLMs)

---

**3. COMMAND_ROUTING_TEMPLATE.md (Score: 8.2/10)**

**Source:** Anthropic Routing pattern + Production "structured workflows over autonomy" principle

**Use Cases:**
- Customer service query classification → specialized handlers
- Multi-department request routing (finance vs legal vs technical)
- Complexity-based model selection (route simple to haiku, complex to sonnet)
- Specialized agent delegation (route financial to @fintech-engineer)
- Input validation → error handling vs normal processing

**Structure (7 sections, ~220 lines):**
```markdown
## Phase 1: Classify Input
Analyze request characteristics:
- Domain: finance | legal | technical | operational | general
- Complexity: simple | moderate | complex
- Urgency: low | medium | high | critical
- Required expertise: specialist | generalist

## Phase 2: Route to Handler (Decision Table)

| Domain | Complexity | Handler | Rationale |
|--------|-----------|---------|-----------|
| finance | simple | @fintech-quick-analyst | Basic calculations, no risk |
| finance | complex | @fintech-engineer | Full modeling, compliance checks |
| legal | any | @compliance-auditor | Requires legal review |
| technical | simple | /validation | Automated checks sufficient |
| technical | complex | @python-pro | Code changes needed |

Routing logic:
IF domain == "finance" AND complexity == "complex" THEN
  handler = @fintech-engineer
ELSE IF domain == "finance" AND complexity == "simple" THEN
  handler = @fintech-quick-analyst
...

## Phase 3: Delegate Execution
Invoke selected handler with full context:
@handler Please analyze this request:
<original request>
<classification context>
<urgency level>

## Phase 4: Aggregate Results
Collect handler output
Format for user presentation
Track routing decision for analytics
```

**Key Differentiators:**
- **Classification first** (determine what kind of request before processing)
- **Explicit routing logic** (decision table, not implicit)
- **Specialized handlers** (delegates to agents/commands, not one-size-fits-all)
- **Deterministic routing** (same inputs = same handler every time)
- **Model selection** (can route to different Claude models based on complexity)

**Anthropic Evidence:**
- Routing: "Classify inputs and direct them to specialized handlers"
- "Particularly useful for customer service queries or routing between model sizes based on complexity"

**Production Evidence:**
- "Most AI agent implementations fail because they confuse autonomy with reliability"
- "Building non-deterministic systems for deterministic business needs"
- Solution: **Deterministic routing logic** (decision table, not learned behavior)

**Adaptation to Claude Code:**
- Routes to agents (e.g., `@fintech-engineer`) not just functions
- Decision table explicitly in prompt (transparent, not black box)
- Can route to other commands for complex multi-step workflows
- Supports model selection via frontmatter (`model: haiku` or `model: sonnet`)

---

## Part 3: Agent Structure Analysis

### 3.1 Official Requirements

**Source:** Project code-reviewer.md + external awesome-claude-code-subagents

**YAML Frontmatter Fields:**

| Field | Required | Type | Purpose | Example |
|-------|----------|------|---------|---------|
| `name` | YES | string | Agent identifier | `code-reviewer` |
| `description` | YES | string (100-150 chars) | When to invoke | "Expert code reviewer specializing in financial calculations" |
| `tools` | No | array | Tool restrictions | `[Read, Grep, Glob]` |
| `model` | No | string | Force specific model | `sonnet`, `opus`, `haiku` |

**Naming Convention:**
- File: `kebab-case.md` (e.g., `code-reviewer.md`)
- Invocation: `@agent-name` (e.g., `@code-reviewer`)
- Location: `.claude/agents/` (global, no environment split)

### 3.2 Tool Permission Tiers

**Source:** Research analysis + external patterns

| Agent Type | Tools | Purpose | Examples |
|------------|-------|---------|----------|
| **Reviewer** | `Read, Grep, Glob` | Read-only verification | code-reviewer, financial-validator |
| **Researcher** | `Read, Grep, Glob, WebFetch, WebSearch` | Investigation + web | codebase-explorer, documentation-researcher |
| **Domain Specialist** | `Read, Write, Edit, Bash, Glob, Grep` | Constrained expertise | fintech-engineer, python-pro, kubernetes-specialist |

**Key Insight:** Agents have FEWER tools than commands (constraint by type, not per-command basis)

### 3.3 Content Structure Pattern

**Source:** Project code-reviewer.md (255 lines) + external fintech-engineer.md (286 lines)

**Standard Structure:**
```markdown
---
name: agent-name
description: Brief description
tools: Read, Grep, Glob
---

# Role Statement

You are a [seniority] [role] with expertise in [domain]. Your focus spans [areas] with emphasis on [priorities].

---

## When Invoked

1. Query context manager for [requirements]
2. Review [existing state]
3. Analyze [specific aspects]
4. [Action: implement/provide feedback/deliver]

---

## Checklist (Domain-Specific)

- [ ] Criterion 1 verified
- [ ] Criterion 2 achieved
- [ ] Criterion 3 maintained
- [ ] Criterion 4 certified

---

## Domain Area 1
- Sub-item 1
- Sub-item 2
- Sub-item 3

## Domain Area 2
[8-12 bulleted items per area]

## Domain Area 3
[Comprehensive coverage of domain]

---

## Communication Protocol (Optional)

### Context Query Format (JSON)
{
  "requirement": "...",
  "constraints": "..."
}

---

## Workflow Phases (Optional)

### Phase 1: [Name]
- Step 1
- Step 2

### Phase 2: [Name]
- Step 1
- Step 2

### Phase 3: [Name]
- Step 1
- Step 2

---

## Output Format (Critical for Reviewers)

### CRITICAL ISSUES (Must Fix)
- Issue 1: [File:line] - Description - Impact - Fix

### WARNINGS (Should Fix)
- Warning 1: ...

### SUGGESTIONS (Nice to Have)
- Suggestion 1: ...

### VERIFICATION RESULTS
- [ ] Check 1: PASS/FAIL
- [ ] Check 2: PASS/FAIL

### RECOMMENDATION
**APPROVE / REJECT / NEEDS REVISION**
**Rationale:** [Explain decision]

---

## Integration Notes (Optional)

Work with:
- @related-agent-1 on [task]
- @related-agent-2 on [task]

---

## Anti-Patterns (Optional)

❌ Bad practice 1
❌ Bad practice 2
✅ Good practice 1
✅ Good practice 2
```

**Section Counts by Agent Type:**

**IMPORTANT:** All external agents use **6 major sections** with subsections for workflow phases.

| Agent Type | Major Sections | Length | Depth |
|------------|----------------|--------|-------|
| **Reviewer** | 6 | 275-285 lines | Deep checklists (8 items), read-only verification |
| **Domain Specialist** | 6 | 275-285 lines | Comprehensive domain coverage (8-15 areas) |
| **Researcher** | 6 | 275-285 lines | Investigation structure, web research tools |

**Standard 6-Section Structure:**
1. Role Statement (1-2 paragraphs)
2. Communication Protocol (JSON query format)
3. Checklist (8 items)
4. Development Workflow (3 phases as subsections: Analysis, Implementation, Excellence)
5. Integration Notes (optional)
6. Anti-Patterns (optional)

### 3.4 Validated Template Recommendations

**Source:** Multi-agent analysis + External validation (116 production agents + 12-factor-agents principles)

**CRITICAL UPDATE:** Validated against 50+ sources. Reduced from 6 templates to **3 templates** based on evidence.
See `research-validation-addendum.md` for detailed analysis.

**Final Recommendations (3 templates):**

| Template | Score | Use When | Lines | Tool Tier | Pattern Frequency |
|----------|-------|----------|-------|-----------|-------------------|
| **AGENT_DOMAIN_SPECIALIST_TEMPLATE.md** | 9.5/10 ↑ | Financial expert, Python expert, domain knowledge, data analysis, CLI generation | ~280 | Full access | **PRIMARY** - 100+ agents (86%) |
| **AGENT_RESEARCHER_TEMPLATE.md** | 8.6/10 ↑ | Codebase exploration, web research, competitive intelligence | ~280 | Read + Web | 6 agents (5%) - DISTINCT web tools |
| **AGENT_REVIEWER_TEMPLATE.md** | 7.8/10 ↓ | Code review, security audit, compliance verification | ~280 | Read-only | 4-6 agents (3-5%) - DISTINCT read-only |

**Removed Templates (Anti-Patterns/Redundancies):**
- ❌ **AGENT_ORCHESTRATOR** (anti-pattern): Commands coordinate agents, not agents coordinate agents (context isolation violation)
- ❌ **AGENT_ANALYZER** (redundant): Same tools/structure as DOMAIN_SPECIALIST; data-analyst IS a domain specialist
- ❌ **AGENT_GENERATOR** (redundant): Same tools/structure as DOMAIN_SPECIALIST; cli-developer IS a domain specialist

**Key Architectural Principle:**
- **Commands = Orchestrators** (variance-analysis.md invokes @code-reviewer at checkpoints)
- **Agents = Workers** (domain specialists, researchers, reviewers - single responsibility)
- **Agents NEVER coordinate other agents** (context isolation by design per code-reviewer.md:254)

**Tool Tier Validation:**
- **3 distinct tiers:** Read-only (reviewers), Read+Web (researchers), Full access (specialists)
- **86% of agents** use Domain Specialist pattern (primary template)
- **All agent types use 6 major sections** (not 7-12 as initially proposed)

---

## Part 4: External Validation

### 4.1 awesome-claude-code-subagents Analysis

**Source:** `/home/user/cc-sf-assistant/external/awesome-claude-code-subagents/`

**Statistics:**
- **Total agents:** 116 across 10 categories
- **Average length:** 285 lines (range: 200-315)
- **Most common type:** Domain Specialist (86% of agents)

**Category Distribution:**

| Category | Count | Example Agents |
|----------|-------|----------------|
| Core Development | 11 | api-designer, backend-developer, fullstack-developer |
| Language Specialists | 22 | python-pro, typescript-pro, rust-engineer, golang-pro |
| Infrastructure | 12 | cloud-architect, devops-engineer, kubernetes-specialist |
| Quality & Security | 12 | code-reviewer, security-auditor, penetration-tester |
| Data & AI | 12 | ml-engineer, data-scientist, llm-architect |
| Developer Experience | 9 | cli-developer, documentation-engineer, dx-optimizer |
| Specialized Domains | 18 | **fintech-engineer**, **quant-analyst**, game-developer |
| Business/Product | 7 | product-manager, ux-researcher |
| Meta-Orchestration | 8 | workflow-orchestrator, task-distributor |
| Research/Analysis | 8 | competitive-analyst, trend-analyst |

**Key Patterns Observed:**

1. **Consistent Structure (100% of agents):**
   - YAML frontmatter with name, description, tools
   - Role statement (1-2 paragraphs)
   - "When invoked" section (4 steps)
   - Checklist (8 items)
   - 8-15 domain areas (8-12 bullet points each)
   - Communication protocol (JSON query format)
   - Workflow phases (3 phases)

2. **Tool Usage:**
   - 92% use full tools: `Read, Write, Edit, Bash, Glob, Grep`
   - 8% use read-only: `Read, Grep, Glob` (reviewers, auditors)
   - None use partial tool sets (it's all or read-only)

3. **Domain Specialist Dominance:**
   - 86% are domain specialists (not reviewers)
   - Constrained expertise in specific technology/domain
   - Comprehensive checklists (8+ items)
   - Deep domain coverage (8-15 areas)

4. **Financial Domain Examples:**
   - `fintech-engineer.md`: Payment systems, regulatory compliance, fraud detection
   - `quant-analyst.md`: Statistical models, risk analysis, algorithmic trading
   - `risk-manager.md`: Risk assessment, mitigation strategies

### 4.2 12-factor-agents Principles

**Source:** `/home/user/cc-sf-assistant/external/12-factor-agents/README.md`

**Relevant Factors for Creating-Commands/Agents:**

| Factor | Principle | Application |
|--------|-----------|-------------|
| 1. Natural Language to Tool Calls | LLMs translate intent → tool use | Commands/agents define available tools |
| 2. Own Your Prompts | Explicit prompt control | SKILL.md is the prompt for command/agent |
| 3. Own Your Context Window | Explicit context building | Commands use progressive disclosure |
| 7. Contact Humans with Tools | Human-in-loop | Commands use checkpoints, agents deliver to human |
| 8. Own Your Control Flow | Deterministic workflows | RPIV workflow in commands |
| 10. Small, Focused Agents | Single responsibility | Each agent has constrained expertise |

**Key Insight:** Commands and agents ARE deterministic prompts, not agentic loops. They guide Claude's behavior through structured instructions.

---

## Part 5: Comparison - Skills vs Commands vs Agents

### 5.1 Invocation & Discovery

| Aspect | Skills | Commands | Agents |
|--------|--------|----------|--------|
| **Invocation** | Auto (CSO-triggered) | Manual (`/env:name`) | Manual (`@name`) |
| **Discovery** | CSO-optimized description | Description in /help menu | Description in agent list |
| **Arguments** | No (context-driven) | Yes ($1, $2, $3) | No (conversation-driven) |
| **Environment** | Yes (dev/prod/shared skills) | Yes (dev/prod/shared dirs) | No (global agents) |

### 5.2 Structure & Content

| Aspect | Skills | Commands | Agents |
|--------|--------|----------|--------|
| **YAML Fields** | name, description | description, model, tools, args | name, description, tools, model |
| **CSO Required** | YES (≥0.7 score) | NO (explicit invocation) | NO (explicit invocation) |
| **Sections** | 6-12 (by type) | 6-8 (by pattern) | 6-15 (by type) |
| **Length** | <200 lines main | 180-270 lines | 200-315 lines |
| **Progressive Disclosure** | references/ subdirs | Inline or link to docs | Inline comprehensive |
| **Validation** | 5 validators | 3-4 validators (TBD) | 3-4 validators (TBD) |

### 5.3 Tools & Permissions

| Aspect | Skills | Commands | Agents |
|--------|--------|----------|--------|
| **Tool Control** | N/A (skills guide) | Optional restrict via `allowed-tools` | Recommended restrict via `tools` |
| **Common Patterns** | Instructional | Full access (Read, Write, Edit, Bash, Glob, Grep) | Type-based (read-only, read+web, full) |
| **Security Model** | Trust (instructions) | Optional constraint | Strong constraint by type |

---

## Part 6: Proposed Architecture

### 6.1 creating-commands Skill

**Directory Structure:**
```
.claude/skills/creating-commands/
├── SKILL.md                                    # Main skill (target: <200 lines)
├── assets/
│   └── templates/
│       ├── COMMAND_RPIV_TEMPLATE.md            # ~250 lines, 8 sections (9.8/10)
│       ├── COMMAND_HUMAN_APPROVAL_TEMPLATE.md  # ~270 lines, 9 sections (9.2/10) 🆕
│       ├── COMMAND_REFLECTION_TEMPLATE.md      # ~260 lines, 8 sections (8.8/10) 🆕
│       ├── COMMAND_VALIDATION_TEMPLATE.md      # ~200 lines, 6 sections (8.6/10)
│       ├── COMMAND_BATCH_PROCESSING_TEMPLATE.md # ~230 lines, 7 sections (8.4/10)
│       ├── COMMAND_ROUTING_TEMPLATE.md         # ~220 lines, 7 sections (8.2/10) 🆕
│       ├── COMMAND_DATA_TRANSFORMATION_TEMPLATE.md # ~220 lines, 7 sections (7.8/10)
│       ├── COMMAND_ORCHESTRATION_TEMPLATE.md   # ~240 lines, 8 sections (7.5/10)
│       └── COMMAND_REPORTING_TEMPLATE.md       # ~210 lines, 7 sections (7.2/10)
├── scripts/
│   ├── generate_command.py                     # Orchestrator (9 template options)
│   ├── validate_command_yaml.py                # YAML frontmatter
│   ├── validate_command_naming.py              # Kebab-case, env prefix
│   ├── validate_command_structure.py           # Required sections (9 templates)
│   └── validate_command_usage.py               # Usage line syntax
└── references/
    ├── rpiv-workflow-guide.md                  # Deep dive on RPIV pattern
    ├── human-approval-guide.md                 # Structured approvals, audit trails 🆕
    ├── reflection-guide.md                     # Self-improvement, quality gates 🆕
    ├── validation-patterns.md                  # Systematic check patterns
    ├── batch-processing-guide.md               # Error handling, progress tracking
    ├── routing-guide.md                        # Classification, decision tables 🆕
    ├── data-transformation-guide.md            # ETL pipelines, data quality gates
    ├── orchestration-guide.md                  # Multi-agent coordination, dependencies
    ├── reporting-guide.md                      # Aggregation, formatting, distribution
    └── prompting-patterns/                     # Optimal prompting patterns 🆕
        ├── own-your-prompts.md                 # Factor 2: Prompt ownership
        ├── reflection-pattern.md               # Self-evaluation loops
        ├── planning-pattern.md                 # Task decomposition
        ├── human-in-loop.md                    # Structured approval requests
        ├── context-management.md               # Context evolution
        ├── tool-documentation.md               # ACI best practices
        └── eval-driven-development.md          # Scientific iteration
```

**SKILL.md CSO Description:**
```yaml
description: Use when creating slash commands, building workflows, need command scaffolding, want /env:command patterns, before writing .claude/commands/*.md, thinking "I need a command template", planning RPIV/approval/reflection/validation/batch/routing/ETL/orchestration/reporting workflows - provides 9 specialized templates with validation for diverse workflow patterns including production-safe approvals and self-improvement loops
```

**Template Characteristics:**

| Template | Placeholders | Sections | Unique Features | Source |
|----------|--------------|----------|-----------------|--------|
| RPIV | `{{COMMAND_NAME}}`, `{{ARG_1}}`, `{{RESEARCH_STEP_1}}` | 8 | 4 checkpoints, research-first, progress table | Project proven |
| Human Approval | `{{ACTION}}`, `{{RISK_LEVEL}}`, `{{REVERSIBLE}}` | 9 | Structured approvals, audit trail, timeout handling | HumanLayer Factor 7 |
| Reflection | `{{QUALITY_CRITERIA}}`, `{{MAX_ITERATIONS}}` | 8 | Self-evaluation, quality gates, autonomous refinement | Anthropic/Google |
| Validation | `{{CHECK_1_NAME}}`, `{{EXPECTED_RESULT_1}}` | 6 | ✅⚠️❌ format, no checkpoints, read-only | Project proven |
| Batch | `{{INPUT_DIR}}`, `{{PATTERN}}`, `{{LOOP_STEP_1}}` | 7 | Per-item errors, progress tracking, summary report | FP&A patterns |
| Routing | `{{DOMAIN}}`, `{{COMPLEXITY}}`, `{{HANDLER}}` | 7 | Classification first, decision table, deterministic | Anthropic Routing |
| Data Transformation | `{{SOURCE_FILE}}`, `{{TRANSFORM_1}}`, `{{QUALITY_CHECK_1}}` | 7 | Load → Transform → Validate → Output pipeline | ETL patterns |
| Orchestration | `{{AGENT_1}}`, `{{DEPENDENCY_1}}`, `{{STATE_VAR_1}}` | 8 | Dependency graph, multi-agent coordination, state tracking | 12-Factor Agents |
| Reporting | `{{DATA_SOURCE}}`, `{{METRIC_1}}`, `{{FORMAT_1}}` | 7 | Aggregate → Analyze → Format → Distribute | Analytics patterns |

**Validators:**

1. **validate_command_yaml.py**
   - Required: `description` (≤1024 chars)
   - Optional: `model`, `allowed-tools`, `argument-hint`, `disable-model-invocation`
   - Kebab-case check (relaxed for command name, enforced for file)

2. **validate_command_naming.py**
   - File pattern: `^[a-z0-9]+(-[a-z0-9]+)*\.md$`
   - Environment: File in `dev/`, `prod/`, or `shared/` subdir
   - Invocation format: `/env:command-name` documented in usage line

3. **validate_command_structure.py**
   - RPIV: 8 sections (Header, STEP 1-4, Success Criteria, Example, Anti-Patterns)
   - Validation: 6 sections (Header, Checks, Report Format, Usage Example, Anti-Patterns)
   - Batch: 7 sections (Header, Discovery, Loop, Summary, Error Handling, Example, Anti-Patterns)
   - Data Transformation: 7 sections (Header, Load, Transform, Validate, Output, Example, Anti-Patterns)
   - Orchestration: 8 sections (Header, Dependency Graph, Agent Coordination, State Management, Execution, Success Criteria, Example, Anti-Patterns)
   - Reporting: 7 sections (Header, Data Sources, Aggregation, Analysis, Formatting, Distribution, Example)

4. **validate_command_usage.py**
   - Usage line present: `**Usage:** /command <arg1> [arg2]`
   - Arguments match `argument-hint` if specified
   - Positional args documented ($1, $2, $3 if used)

**Validator Updates for 9 Templates:**
- validate_command_structure.py now handles 9 template types (was 6)
- Each template has defined section count and structure requirements
- Human Approval requires risk assessment fields
- Reflection requires quality criteria and iteration limits
- Routing requires decision table structure

### 6.2 creating-agents Skill

**Directory Structure:**
```
.claude/skills/creating-agents/
├── SKILL.md                                    # Main skill (target: <200 lines)
├── assets/
│   └── templates/
│       ├── AGENT_DOMAIN_SPECIALIST_TEMPLATE.md # ~280 lines, full tools (PRIMARY)
│       ├── AGENT_RESEARCHER_TEMPLATE.md        # ~280 lines, read+web
│       └── AGENT_REVIEWER_TEMPLATE.md          # ~280 lines, read-only
├── scripts/
│   ├── generate_agent.py                       # Orchestrator (3 template options)
│   ├── validate_agent_yaml.py                  # YAML frontmatter
│   ├── validate_agent_naming.py                # Kebab-case
│   ├── validate_agent_structure.py             # Required sections (3 templates)
│   └── validate_agent_tools.py                 # Tool tier compliance
└── references/
    ├── domain-specialist-guide.md              # Constrained expertise, comprehensive coverage (PRIMARY)
    ├── researcher-patterns.md                  # Investigation structure, web research tools
    ├── reviewer-patterns.md                    # Checklist design, read-only verification
    └── prompting-patterns/                     # Optimal prompting patterns (symlink/shared) 🆕
        ├── own-your-prompts.md                 # Factor 2: Prompt ownership
        ├── reflection-pattern.md               # Self-evaluation loops
        ├── planning-pattern.md                 # Task decomposition
        ├── human-in-loop.md                    # Structured approval requests
        ├── context-management.md               # Context evolution
        ├── tool-documentation.md               # ACI best practices
        └── eval-driven-development.md          # Scientific iteration
```

**Note:** The `prompting-patterns/` directory is shared between creating-commands and creating-agents (symlink or duplicate content). These patterns apply to both commands and agents.

**SKILL.md CSO Description:**
```yaml
description: Use when creating agents, building subagents, need agent scaffolding, want @agent-name patterns, before writing .claude/agents/*.md, thinking "I need an agent template", planning domain specialist/researcher/reviewer agents - provides 3 validated templates with tool tier enforcement based on 116 production agents
```

**Template Characteristics:**

| Template | Placeholders | Tool Tier | Sections | Pattern Frequency |
|----------|--------------|-----------|----------|-------------------|
| Domain Specialist | `{{DOMAIN}}`, `{{AREA_1_NAME}}` | Full access | 6 | **PRIMARY** (86% of agents) |
| Researcher | `{{RESEARCH_FOCUS}}`, `{{QUERY_1}}` | Read + Web | 6 | Web research (5% of agents) |
| Reviewer | `{{AGENT_NAME}}`, `{{CHECK_1_NAME}}` | Read-only | 6 | Verification (3-5% of agents) |

**All templates use standardized 6-section structure:**
1. Role Statement
2. Communication Protocol (JSON query format)
3. Checklist (8 items)
4. Development Workflow (3 phases: Analysis, Implementation, Excellence)
5. Integration Notes (optional)
6. Anti-Patterns (optional)

**Validators:**

1. **validate_agent_yaml.py**
   - Required: `name` (kebab-case), `description` (100-150 chars)
   - Optional: `tools`, `model`
   - No CSO check (agents use explicit `@name` invocation)

2. **validate_agent_naming.py**
   - File pattern: `^[a-z0-9]+(-[a-z0-9]+)*\.md$`
   - Name matches file (name: `code-reviewer`, file: `code-reviewer.md`)
   - Location: `.claude/agents/` (global, not environment-specific)

3. **validate_agent_structure.py**
   - All templates: 6 major sections
   - Domain Specialist: 8-15 domain areas (subsections)
   - Researcher: Investigation workflow structure
   - Reviewer: Verification checklist structure

4. **validate_agent_tools.py**
   - Reviewer: `tools: [Read, Grep, Glob]` (exactly - read-only)
   - Researcher: `tools: [Read, Grep, Glob, WebFetch, WebSearch]` (exactly - read + web)
   - Domain Specialist: `tools: [Read, Write, Edit, Bash, Glob, Grep]` (exactly - full access)
   - Error if tools don't match template type exactly

---

## Part 7: Key Differences from creating-skills

### 7.1 No CSO Optimization

**Skills:** Auto-invoked based on CSO-optimized description (≥0.7 score)
**Commands:** Manual invocation via `/env:command` (no CSO needed)
**Agents:** Manual invocation via `@agent-name` (no CSO needed)

**Implication:**
- **Remove:** validate_cso.py (not applicable)
- **Add:** validate_usage.py (commands), validate_tools.py (agents)
- **Description:** Focus on discoverability in /help menu (commands) or agent list (agents)

### 7.2 No Rationalization-Proofing

**Skills:** Discipline skills need Iron Law, Red Flags, Rationalization table
**Commands:** Workflow structure enforces discipline (RPIV checkpoints)
**Agents:** No workflow enforcement (single-execution review/analysis)

**Implication:**
- **Remove:** validate_rationalization.py (not applicable)
- **Add:** validate_structure.py checks for checkpoints (RPIV commands)

### 7.3 Tool Permissions Critical

**Skills:** Instructional (no tool control)
**Commands:** Optional tool restrictions (`allowed-tools`)
**Agents:** Strong tool tier enforcement (`tools` field)

**Implication:**
- **Add:** validate_agent_tools.py (enforce tool tier by template type)
- **Add:** validate_command_usage.py (check argument-hint matches usage line)

### 7.4 Environment Split

**Skills:** Yes (dev/prod/shared subdirs)
**Commands:** Yes (dev/prod/shared subdirs)
**Agents:** No (global, flat structure)

**Implication:**
- `validate_command_naming.py` checks environment subdir
- `validate_agent_naming.py` checks `.claude/agents/` (no subdir)

---

## Part 8: Implementation Recommendations

### 8.1 Template Development Order

**Phase 1: Critical Production Patterns (Tier 1)**
1. COMMAND_RPIV_TEMPLATE.md (score: 9.8/10) - Proven in variance-analysis.md (project validation)
2. COMMAND_HUMAN_APPROVAL_TEMPLATE.md (score: 9.2/10) - **NEW** Production-safe automation (HumanLayer Factor 7)
3. AGENT_DOMAIN_SPECIALIST_TEMPLATE.md (score: 9.5/10 ↑) - **PRIMARY** agent pattern (86% frequency)

**Phase 2: High-Value Patterns (Tier 2)**
4. COMMAND_REFLECTION_TEMPLATE.md (score: 8.8/10) - **NEW** Self-improvement (Anthropic/Google)
5. COMMAND_VALIDATION_TEMPLATE.md (score: 8.6/10) - Proven in sync-docs.md (project validation)
6. AGENT_RESEARCHER_TEMPLATE.md (score: 8.6/10 ↑) - Distinct web research pattern

**Phase 3: Supporting Patterns (Tier 3)**
7. COMMAND_BATCH_PROCESSING_TEMPLATE.md (score: 8.4/10) - High FP&A demand
8. COMMAND_ROUTING_TEMPLATE.md (score: 8.2/10) - **NEW** Intelligent classification (Anthropic)
9. AGENT_REVIEWER_TEMPLATE.md (score: 7.8/10) - Proven in code-reviewer.md (project validation)
10. COMMAND_DATA_TRANSFORMATION_TEMPLATE.md (score: 7.8/10) - ETL workflows

**Phase 4: Specialized Workflows (Tier 4)**
11. COMMAND_ORCHESTRATION_TEMPLATE.md (score: 7.5/10) - Multi-agent coordination
12. COMMAND_REPORTING_TEMPLATE.md (score: 7.2/10) - Analytics and dashboards

**Phase 5: Reference Guides (Parallel Development)**
13. 7 Prompting Pattern guides (~350-420 lines each) - HumanLayer + Anthropic + Google + Production
14. 9 Command-specific guides (RPIV, Human Approval, Reflection, etc.)
15. 3 Agent-specific guides (Domain Specialist, Researcher, Reviewer)

**Rationale:**
- **Tier 1 (3 templates):** Highest scores + proven/critical patterns (RPIV project-proven, Human Approval production-critical, Domain Specialist most common)
- **Tier 2 (3 templates):** High scores 8.6-8.8 + distinct value (Reflection self-improvement, Validation project-proven, Researcher web research)
- **Tier 3 (4 templates):** Supporting workflows 7.8-8.4 (Batch FP&A demand, Routing classification, Reviewer security, ETL pipelines)
- **Tier 4 (2 templates):** Specialized patterns 7.2-7.5 (Orchestration multi-agent, Reporting analytics)
- **Tier 5 (19 guides):** Reference documentation (7 prompting patterns + 9 command guides + 3 agent guides)
- **3 new templates** (Human Approval, Reflection, Routing) integrated based on 2024-2025 research validation
- Agent templates unchanged (3 validated against 116 external agents)

### 8.2 Validator Complexity Ranking

**Simple (50-100 lines):**
- validate_command_naming.py (file pattern, environment check)
- validate_agent_naming.py (file pattern, name match)

**Medium (100-150 lines):**
- validate_command_yaml.py (5 fields, 1 required)
- validate_agent_yaml.py (4 fields, 2 required)
- validate_agent_tools.py (tool tier matching)

**Complex (150-300 lines):**
- validate_command_structure.py (9 templates × 6-9 sections) 🔄 UPDATED
- validate_agent_structure.py (3 templates × 6 sections each)
- validate_command_usage.py (usage line parsing, arg matching)

### 8.3 Progressive Disclosure Strategy

**Commands (9 templates, 16 reference guides):**
- Main SKILL.md: 6 sections (Overview, When to Use, Instructions, Pitfalls, Examples, Progressive Disclosure)

**Command-Specific Guides (9 guides, 300-400 lines each):**
- references/rpiv-workflow-guide.md: Deep dive on checkpoints, progress tracking
- references/human-approval-guide.md: Structured approvals, risk assessment, audit trails 🆕
- references/reflection-guide.md: Self-improvement loops, quality gates, iteration limits 🆕
- references/validation-patterns.md: ✅⚠️❌ reporting, systematic checks
- references/batch-processing-guide.md: Error handling, loop patterns, summary reports
- references/routing-guide.md: Classification logic, decision tables, handler delegation 🆕
- references/data-transformation-guide.md: ETL pipelines, data quality gates
- references/orchestration-guide.md: Multi-agent coordination (commands coordinate agents)
- references/reporting-guide.md: Aggregation, formatting, distribution

**Prompting Pattern Guides (7 guides, 340-420 lines each):** 🆕
- references/prompting-patterns/own-your-prompts.md: Factor 2 - prompt ownership, no frameworks
- references/prompting-patterns/reflection-pattern.md: Self-evaluation loops, quality thresholds
- references/prompting-patterns/planning-pattern.md: Task decomposition, dependency management
- references/prompting-patterns/human-in-loop.md: Structured approvals, audit trails
- references/prompting-patterns/context-management.md: Context evolution, progressive disclosure
- references/prompting-patterns/tool-documentation.md: ACI best practices, clear boundaries
- references/prompting-patterns/eval-driven-development.md: Scientific iteration, A/B testing

**Agents (3 templates, 10 reference guides):**
- Main SKILL.md: 6 sections (same as commands)

**Agent-Specific Guides (3 guides, 300-400 lines each):**
- references/domain-specialist-guide.md: Constrained expertise, comprehensive coverage (8-15 areas) - **PRIMARY**
- references/researcher-patterns.md: Investigation structure, web research tools
- references/reviewer-patterns.md: Checklist design, read-only verification

**Shared Prompting Patterns (7 guides via symlink/duplicate):**
- references/prompting-patterns/ → Same 7 guides as in creating-commands

**Targets:**
- Main SKILL.md: <200 lines (high-level overview)
- Command-specific guides: 300-400 lines each (deep dive on pattern)
- Agent-specific guides: 300-400 lines each (deep dive on pattern)
- Prompting pattern guides: 340-420 lines each (production-validated patterns)

**Removed Guides:**
- ❌ orchestrator-patterns.md (anti-pattern - commands coordinate agents)
- ❌ analyzer-patterns.md (redundant - use domain-specialist-guide.md)
- ❌ generator-patterns.md (redundant - use domain-specialist-guide.md)

---

## Part 11: Optimal Prompting Patterns (2024-2025 Research)

**Source:** Anthropic Building Effective Agents + HumanLayer 12-Factor Agents + Google/DeepMind Agentic Patterns + Production Lessons 2024-2025

**Purpose:** 7 reference guides documenting production-validated prompting patterns from leading AI research labs and real-world implementations

### 11.1 Own Your Prompts (HumanLayer Factor 2)

**File:** `references/prompting-patterns/own-your-prompts.md` (~350 lines)

**Key Principle:** "Don't outsource your prompt engineering to a framework. Treat prompts as first-class code."

**Anti-Pattern:**
```python
# Black-box framework abstraction
agent = Agent(
  role="deployment manager",
  goal="deploy safely",
  personality="cautious",
  tools=[deploy_tool, check_tool]
)
```

**Claude Code Pattern:**
```markdown
# In .claude/commands/prod/deploy.md (explicit prompt control)

You are a deployment manager that ensures safe and successful deployments.

Before deploying, you MUST check:
- Deployment environment (staging vs production)
- Correct tag/version exists
- Current system status is healthy

Always think through what to do first:
1. Check current deployment status
2. Verify the tag exists in git
3. Request approval if deploying to production
4. Deploy to staging first if possible
5. Monitor deployment progress
```

**Benefits for Claude Code:**
- **Full control:** Direct prompt editing in .md files (no framework layer)
- **Version control:** Git tracks all prompt changes
- **Testing:** A/B test via branches, measure with evals
- **Transparency:** Know exactly what instructions Claude receives
- **Iteration:** Modify based on real-world performance

**Evidence:**
- HumanLayer Factor 2: "I don't know what's the best prompt, but I know you want the flexibility to be able to try EVERYTHING."
- Anthropic: "Framework abstraction can obscure underlying prompts and responses, making debugging harder."

---

### 11.2 Reflection Pattern (Anthropic Evaluator-Optimizer + Google/DeepMind)

**File:** `references/prompting-patterns/reflection-pattern.md` (~400 lines)

**Pattern Structure:**
```markdown
## Step 1: Generate Initial Response
Create first draft without self-imposed constraints
Document approach and assumptions made

## Step 2: Self-Critique
Evaluate your own work against multiple dimensions:
- **Accuracy:** Are all facts correct? Verify sources cited
- **Completeness:** Did I miss requirements? Check spec against output
- **Clarity:** Would user understand? Read from their perspective
- **Edge cases:** What could go wrong? Challenge every assumption
- **Quality score:** Rate 1-10 on each dimension (be harsh)

## Step 3: Identify Specific Improvements
List actionable changes (not vague "make it better"):
1. Fix accuracy error in section X (cite correct source: [link])
2. Add missing analysis of edge case Y (addresses gap in spec)
3. Clarify confusing explanation of Z (use simpler language)

## Step 4: Refine
Implement identified improvements
Show before/after for each change

## Step 5: Repeat or Stop
- REPEAT if quality score <8/10 on any dimension AND iterations <max
- STOP if all dimensions ≥8/10 OR max iterations reached OR no improvements identified
```

**When to Use:**
- Complex analysis requiring multiple perspectives
- Content quality more important than speed
- Self-correction can find errors humans might miss
- Literary translation (Anthropic example)
- Financial reports requiring peer review simulation

**Evidence:**
- Anthropic Evaluator-Optimizer: "One LLM generates responses while another provides iterative feedback. Works well for literary translation and complex search tasks."
- Google/DeepMind: "Self-feedback mechanism where an AI agent evaluates its outputs before finalizing responses."

**Claude Code Application:**
- COMMAND_REFLECTION_TEMPLATE uses this pattern
- Quality gates prevent infinite loops
- Transparent improvement process (user sees critique)

---

### 11.3 Planning Pattern (Anthropic Orchestrator-Workers + DeepMind)

**File:** `references/prompting-patterns/planning-pattern.md` (~380 lines)

**Pattern Structure:**
```markdown
## Step 1: Decompose Task into Subtasks
Break down complex task:
1. Subtask A: [description] (depends on: none)
2. Subtask B: [description] (depends on: A)
3. Subtask C: [description] (depends on: A, B)
4. Subtask D: [description] (depends on: C)

## Step 2: Estimate Effort & Identify Dependencies
For each subtask:
- **Complexity:** low (5min) | medium (30min) | high (2h)
- **Dependencies:** Must complete [A, B] first
- **Tools needed:** @agent-name or /command-name
- **Risk:** What could fail? Mitigation strategy?

## Step 3: Execute in Dependency Order
Process dependency graph:
- Execute subtasks with no dependencies first
- Wait for dependencies to complete before starting dependent tasks
- Track progress and adjust plan if issues arise

## Step 4: Adapt Plan Dynamically
If subtask fails or reveals new requirements:
- Analyze failure root cause
- Add new subtasks if needed
- Adjust dependencies
- Re-plan affected downstream tasks
```

**When to Use:**
- Complex multi-step tasks (20+ steps)
- Unclear number of steps upfront (Anthropic: "unpredictable subtasks")
- Dependencies between steps
- Multi-file code changes (Anthropic example)

**Evidence:**
- Anthropic Orchestrator-Workers: "Central LLM breaks down tasks dynamically and delegates to worker LLMs. Best for unpredictable subtasks like multi-file code changes."
- DeepMind: "Planning involves creating a detailed plan or sequence of actions, allowing agent to anticipate challenges and allocate resources efficiently."

**Claude Code Application:**
- Commands do planning (centralized)
- Agents execute subtasks (delegated)
- COMMAND_ORCHESTRATION_TEMPLATE uses this

---

### 11.4 Human-in-Loop Pattern (HumanLayer Factor 7)

**File:** `references/prompting-patterns/human-in-loop.md` (~420 lines)

**Structured Approval Request Format:**
```json
{
  "intent": "request_human_approval",
  "question": "Would you like to proceed with deploying v1.2.3 to production?",
  "context": "This deployment will affect 10,000 active users. Changes include: [list].",
  "options": {
    "urgency": "high|medium|low",
    "risk_level": "high|medium|low",
    "format": "yes_no|multiple_choice|free_text",
    "choices": ["Approve", "Reject", "Request Changes"],
    "reversible": false,
    "estimated_duration": "5 minutes",
    "impact_scope": "production|staging|development"
  },
  "audit_context": {
    "timestamp": "2025-11-09T14:30:00Z",
    "requested_by": "agent-deployment-manager",
    "approval_required_from": "user@example.com"
  }
}
```

**When to Use:**
- Production deployments (irreversible, high impact)
- Financial transactions (regulatory compliance)
- Sensitive data operations (PII access, deletion)
- Compliance-critical decisions (SOC2, GDPR)
- Actions agent isn't confident about (70-80% ceiling problem)

**Benefits:**
1. **Clear Instructions:** Structured format vs ad-hoc questions
2. **Inner vs Outer Loop:** Enables agent→human workflows (not just human→agent)
3. **Multiple Humans:** Can coordinate input from different stakeholders
4. **Audit Trail:** Compliance-ready logging (who, when, what, decision)
5. **Durable:** Combined with pause/resume for long-running workflows

**Evidence:**
- HumanLayer Factor 7: "Tools for different types of human contact allow for more specificity from the LLM."
- Production 2024-2025: "Solves 70-80% performance ceiling problem. Agents hit limit, need human guidance for hard decisions."

**Claude Code Application:**
- COMMAND_HUMAN_APPROVAL_TEMPLATE implements this
- Audit trail via conversation history + explicit logging
- Timeout handling via conversation patterns

---

### 11.5 Context Management Pattern (HumanLayer Factor 3)

**File:** `references/prompting-patterns/context-management.md` (~360 lines)

**Key Principle:** "The best agents evolve their context as they work. They remember what they've done, learn what worked, and bring forward only what matters next."

**Anti-Pattern (Context Dump):**
```xml
<!-- Don't include entire conversation history every time -->
<context>
  <message1>User asked about X</message1>
  <message2>Agent responded Y</message2>
  <message3>User clarified Z</message3>
  ... (50 more messages) ...
  <message53>Current request</message53>
</context>
```

**Good Pattern (Evolved Context):**
```xml
<conversation_history>
  <learned_facts>
    - User prefers detailed financial analysis (from message 5)
    - Focus on YoY comparisons (from message 12)
    - Always include variance explanations (from message 23)
  </learned_facts>

  <recent_actions>
    - Analyzed Q3 variance (15 minutes ago)
    - Generated report for CFO (5 minutes ago)
  </recent_actions>

  <current_context>
    - Working on Q4 forecast
    - Same methodology as Q3
    - Deadline: tomorrow 9am
  </current_context>
</conversation_history>
```

**Progressive Disclosure:**
- Start with minimal context
- Add details as workflow progresses
- Summarize old context (don't repeat verbatim)
- Keep only what's relevant to next step

**Evidence:**
- HumanLayer Factor 3: "Own your context window"
- Production 2024-2025: "Context isn't just about remembering previous conversations, it's about maintaining state across complex processes that may span days or weeks."

**Claude Code Application:**
- Commands manage context across checkpoints
- Agents receive focused context (not entire history)
- Research phase → Plan phase → Implement phase (progressive context)

---

### 11.6 Tool Documentation Pattern (Anthropic ACI)

**File:** `references/prompting-patterns/tool-documentation.md` (~340 lines)

**Key Principle:** "Treat agent-computer interfaces (ACI) with as much care as human-computer interfaces (HCI)."

**Best Practices for Tool Definitions:**

```markdown
## Tool: deploy_backend

**Purpose:** Deploy backend service to specified environment with safety checks

**Parameters:**
- **tag** (string, REQUIRED): Git tag to deploy
  - Format: "v{major}.{minor}.{patch}" (e.g., "v1.2.3")
  - Must exist in repository
  - Validated before deployment

- **environment** (enum, REQUIRED): Target environment
  - Values: "staging" | "production" | "development"
  - Production requires additional approval

- **skip_tests** (boolean, OPTIONAL, default=false): Skip pre-deployment tests
  - WARNING: Only use in emergencies
  - Requires explicit justification

**Returns:**
{
  "status": "success" | "failure",
  "message": "Human-readable description",
  "timestamp": "ISO 8601 timestamp",
  "deployment_id": "unique-identifier"
}

**Example Usage:**
deploy_backend(tag="v1.2.3", environment="staging")
✅ Returns: {status: "success", message: "Deployed to staging", ...}

deploy_backend(tag="v999.0.0", environment="production")
❌ Returns: {status: "failure", message: "Tag v999.0.0 not found", ...}

**Edge Cases:**
- If tag doesn't exist → Error: "Tag not found in repository"
- If environment locked → Error: "Deployment already in progress"
- If tests fail (skip_tests=false) → Error: "Pre-deployment tests failed: [details]"

**Boundaries (What This Tool Does NOT Do):**
- ❌ Does NOT roll back previous versions (use rollback_deployment tool)
- ❌ Does NOT modify database schema (use db_migrate tool)
- ❌ Does NOT restart services (happens automatically on deployment)

**Related Tools:**
- Use `check_deployment_status` to verify deployment health
- Use `rollback_deployment` to revert if issues found
- Use `db_migrate` before deploying if schema changes needed
```

**Common Mistakes to Avoid:**
- ❌ Relative file paths (use absolute: `/home/user/file.txt` not `./file.txt`)
- ❌ Unclear parameter names (`data` vs `customer_purchase_data`)
- ❌ Format-heavy specifications (minimize JSON nesting)
- ❌ Ambiguous boundaries between similar tools

**Evidence:**
- Anthropic: "Tool design mistakes using relative filepaths, unclear parameter names, or format-heavy specifications causes model errors. Absolute paths and explicit naming prevent mistakes."

**Claude Code Application:**
- Agent tool documentation in frontmatter
- Examples included in prompts
- Clear boundaries prevent tool confusion

---

### 11.7 Evaluation-Driven Development Pattern (Production 2024-2025)

**File:** `references/prompting-patterns/eval-driven-development.md` (~390 lines)

**Key Principle:** "Eval-Driven Development is applying the scientific method to building ML systems. Iterate using science (EDD) rather than art (vibe checks)."

**Scientific Iteration Process:**

```markdown
## Step 1: Define Success Criteria (Before Implementation)
Measurable metrics with target values:
- **Accuracy:** ≥95% correct responses on test set
- **Completeness:** 0 missing required fields
- **Latency:** <2s p95 response time
- **User satisfaction:** ≥4/5 average rating

Test set:
- 20 typical cases (80% weight)
- 10 edge cases (15% weight)
- 5 error cases (5% weight)

## Step 2: Baseline Measurement
Run current prompt against all test cases
Record metrics for each case
Calculate aggregate scores

Example:
Accuracy: 18/20 typical (90%), 6/10 edge (60%), 3/5 error (60%) = 77% overall
Latency: p50=1.2s, p95=3.1s ❌ FAILS
Completeness: 2 cases missing fields ❌ FAILS

## Step 3: Iterate with Single Variable Changes
Change ONE thing at a time:
- Iteration A: Add examples for edge cases
- Iteration B: Simplify prompt language
- Iteration C: Add explicit error handling

For each iteration:
- Re-run full test set
- Record new metrics
- Compare to baseline
- Keep if improved ALL metrics, discard otherwise

## Step 4: A/B Test in Production
Deploy winning prompt to 10% traffic
Monitor real-world metrics (not just test set)
Compare A (baseline) vs B (new prompt)
Gradual rollout if B performs better

## Step 5: Continuous Monitoring
Production dashboards:
- Accuracy regression alerts (drop >2% from baseline)
- Latency p95 alerts (>2.5s)
- User feedback trends
- Monthly test set re-runs (prevent drift)
```

**Tools for Evaluation:**
- Test sets with expected outputs
- Automated scoring (exact match, semantic similarity, rubric-based)
- Logging infrastructure (every input/output pair)
- A/B testing framework (gradual rollout)

**Evidence:**
- Production 2024-2025: "The difference between a clever demo and a reliable AI agent comes down to engineering rigor. Prompt hacks and intuition alone won't cut it."
- "88% of early adopters report positive ROI" (when using systematic evaluation)

**Claude Code Application:**
- Validators enforce quality gates (analogous to test suites)
- Multiple template options enable A/B testing
- Version control allows comparing prompt performance over time

---

### 11.8 Summary: When to Use Each Pattern

| Pattern | Use When | Evidence Source | Implementation |
|---------|----------|-----------------|----------------|
| **Own Your Prompts** | Always | HumanLayer Factor 2 | Direct .md file editing |
| **Reflection** | Quality > speed | Anthropic Evaluator-Optimizer | COMMAND_REFLECTION_TEMPLATE |
| **Planning** | Complex multi-step | Anthropic Orchestrator-Workers | COMMAND_ORCHESTRATION_TEMPLATE |
| **Human-in-Loop** | High-risk actions | HumanLayer Factor 7 | COMMAND_HUMAN_APPROVAL_TEMPLATE |
| **Context Management** | Long workflows | HumanLayer Factor 3 | RPIV checkpoints |
| **Tool Documentation** | Agent uses tools | Anthropic ACI principles | Agent frontmatter + examples |
| **Eval-Driven Dev** | Production deployment | Production 2024-2025 | Validators + test sets |

**Note:** These patterns are composable. For example:
- RPIV uses Planning (decompose into phases) + Human-in-Loop (4 checkpoints)
- Reflection uses Eval-Driven Dev (quality thresholds) + Context Management (evolve context through iterations)
- Human Approval uses Tool Documentation (structured approval format) + Context Management (audit trail)

---

## Part 9: Testing Strategy

### 9.1 Validator Testing

**Unit Tests (pytest):**
```python
# test_validate_command_yaml.py
def test_missing_description():
    """YAML without description should fail."""
    content = "---\nname: test\n---\n"
    result = validate_yaml(content)
    assert result['passed'] == False
    assert 'description' in str(result['errors'])

def test_description_too_long():
    """Description >1024 chars should warn."""
    content = f"---\ndescription: {'x' * 1025}\n---\n"
    result = validate_yaml(content)
    assert result['exit_code'] == 2  # warning
```

**Integration Tests:**
```python
# test_generate_command.py
def test_rpiv_template_generation():
    """Generate RPIV command and validate all checks pass."""
    result = generate_command(
        name='test-workflow',
        template='rpiv',
        environment='dev',
        description='Test workflow',
        args=['file1', 'file2']
    )
    assert result['success'] == True
    assert Path('.claude/commands/dev/test-workflow.md').exists()
    # Run all validators
    for validator in VALIDATORS:
        assert run_validator(validator, result['path']) == 0
```

### 9.2 Template Testing

**Checklist for Each Template:**
- [ ] All placeholders documented
- [ ] Example replacement values provided
- [ ] Generated file passes all validators
- [ ] Matches external patterns (awesome-claude-code-subagents)
- [ ] Progressive disclosure links work

**Manual Testing:**
1. Generate command/agent from template
2. Fill placeholders manually
3. Invoke command/agent in real scenario
4. Verify output matches expected format
5. Iterate based on usability feedback

---

## Part 10: Success Criteria

### 10.1 creating-commands Skill

**Required Deliverables:**
- [ ] SKILL.md (technique type, <200 lines)
- [ ] **9 templates** (RPIV, Human Approval, Reflection, Validation, Batch, Routing, Data Transformation, Orchestration, Reporting)
- [ ] 4 validators (yaml, naming, structure with 9 template support, usage)
- [ ] 1 orchestrator (generate_command.py with 9 template options)
- [ ] **16 reference guides:**
  - [ ] 9 command-specific guides (rpiv, human-approval, reflection, validation, batch, routing, data-transformation, orchestration, reporting)
  - [ ] 7 prompting pattern guides (own-your-prompts, reflection-pattern, planning-pattern, human-in-loop, context-management, tool-documentation, eval-driven-development)

**Quality Gates:**
- [ ] All validators pass on creating-commands SKILL.md
- [ ] Generated variance-analysis.md from RPIV template passes validators (project-proven pattern)
- [ ] Generated sync-docs.md from Validation template passes validators (project-proven pattern)
- [ ] Generated deployment-approval.md from Human Approval template passes validators (HumanLayer pattern)
- [ ] Generated translation-refine.md from Reflection template passes validators (Anthropic pattern)
- [ ] Generated query-router.md from Routing template passes validators (Anthropic pattern)
- [ ] Manual test: Generate new command from each template, verify functionality
- [ ] All 16 reference guides <500 lines (progressive disclosure target)

### 10.2 creating-agents Skill

**Required Deliverables:**
- [ ] SKILL.md (technique type, <200 lines)
- [ ] **3 templates** (Domain Specialist, Researcher, Reviewer) - validated against 116 external agents
- [ ] 4 validators (yaml, naming, structure, tools)
- [ ] 1 orchestrator (generate_agent.py with 3 template options)
- [ ] **10 reference guides:**
  - [ ] 3 agent-specific guides (domain-specialist-guide.md, researcher-patterns.md, reviewer-patterns.md)
  - [ ] 7 shared prompting pattern guides (symlink to creating-commands/references/prompting-patterns/)

**Quality Gates:**
- [ ] All validators pass on creating-agents SKILL.md
- [ ] Generated code-reviewer.md from Reviewer template passes validators (project-proven pattern)
- [ ] Generated fintech-engineer.md from Domain Specialist template passes validators (PRIMARY pattern, 86% frequency)
- [ ] Generated research-analyst.md from Researcher template passes validators (web research pattern)
- [ ] Manual test: Generate new agent from each template, invoke it successfully
- [ ] Validation: All templates use 6 major sections (not 7-12)
- [ ] Tool tier validation: Reviewer (read-only), Researcher (read+web), Domain Specialist (full access)
- [ ] All 10 reference guides accessible (3 agent-specific + 7 shared prompting patterns)

**Removed Deliverables:**
- ❌ AGENT_ORCHESTRATOR template (anti-pattern - commands coordinate agents, context isolation violation)
- ❌ AGENT_ANALYZER template (redundant with Domain Specialist - same tools/structure)
- ❌ AGENT_GENERATOR template (redundant with Domain Specialist - same tools/structure)
- ❌ orchestrator-patterns.md, analyzer-patterns.md, generator-patterns.md (removed guides)

### 10.3 Integration with creating-skills

**Consistency Checks:**
- [ ] Same directory structure (assets/templates/, scripts/, references/)
- [ ] Same orchestrator pattern (interactive prompts → temp dir → validate → commit)
- [ ] Same validator exit codes (0=pass, 1=error, 2=warning)
- [ ] Same placeholder format (`{{VARIABLE}}`)
- [ ] Same progressive disclosure strategy (main <200 lines, references/ for depth)

---

## Appendix A: File Size Analysis

**Template Sizes (external awesome-claude-code-subagents):**
- Minimum: 200 lines (simple researcher agents)
- Maximum: 315 lines (comprehensive domain specialists)
- Average: 285 lines
- Mode: 285 lines (60% of agents)

**Command Sizes (project):**
- variance-analysis.md: 184 lines (RPIV pattern)
- sync-docs.md: 269 lines (Validation pattern)

**Implication:** Target template sizes:
- **Commands (9 templates):**
  - COMMAND_RPIV: ~250 lines (8 sections)
  - COMMAND_HUMAN_APPROVAL: ~270 lines (9 sections) 🆕
  - COMMAND_REFLECTION: ~260 lines (8 sections) 🆕
  - COMMAND_VALIDATION: ~200 lines (6 sections)
  - COMMAND_BATCH: ~230 lines (7 sections)
  - COMMAND_ROUTING: ~220 lines (7 sections) 🆕
  - COMMAND_DATA_TRANSFORMATION: ~220 lines (7 sections)
  - COMMAND_ORCHESTRATION: ~240 lines (8 sections)
  - COMMAND_REPORTING: ~210 lines (7 sections)
- **Agents (3 templates, standardized to 275-285 line range):**
  - AGENT_DOMAIN_SPECIALIST: ~280 lines (6 sections, PRIMARY)
  - AGENT_RESEARCHER: ~280 lines (6 sections)
  - AGENT_REVIEWER: ~280 lines (6 sections)

---

## Appendix B: Placeholder Naming Conventions

**Command Placeholders:**
```
{{COMMAND_NAME}}              # Kebab-case name (variance-analysis)
{{COMMAND_TITLE}}             # Human-readable title (Variance Analysis Command)
{{ENVIRONMENT}}               # dev, prod, shared
{{ARG_1}}, {{ARG_2}}          # Positional arguments
{{DESCRIPTION}}               # Help menu description
{{RESEARCH_STEP_1}}           # RPIV template steps
{{CHECK_1_NAME}}              # Validation template checks
{{INPUT_DIR}}, {{PATTERN}}    # Batch template parameters
```

**Agent Placeholders:**
```
{{AGENT_NAME}}                # Kebab-case name (code-reviewer)
{{AGENT_TITLE}}               # Human-readable title (Code Reviewer)
{{ROLE_DESCRIPTION}}          # "You are a senior..."
{{DOMAIN}}                    # Financial systems, Python ecosystem
{{CHECK_1_NAME}}              # Checklist items
{{AREA_1_NAME}}               # Domain areas (Banking, Payments, etc.)
{{TOOL_TIER}}                 # read-only, read+web, full
```

---

## Appendix C: External References

**Official Documentation:**
- docs.claude.com/en/docs/claude-code/slash-commands
- docs.claude.com/en/docs/claude-code/agents

**External Repos:**
- awesome-claude-code-subagents: 116 production agents
- 12-factor-agents: Principles for reliable LLM apps

**Project Files:**
- .claude/skills/creating-skills/ (proven meta-skill architecture)
- .claude/commands/prod/variance-analysis.md (RPIV example)
- .claude/commands/shared/sync-docs.md (Validation example)
- .claude/agents/code-reviewer.md (Reviewer example)
- specs/commands-and-agents/research.md (command/agent patterns)
- specs/commands-and-agents/multi-agent-analysis.md (template validation)

---

---

## Appendix D: Template Details and Validation

**CRITICAL UPDATE:** Based on deep validation against 116 external agents + 12-factor-agents principles, agent templates reduced from 6 to 3.
See `research-validation-addendum.md` for complete 50+ source validation analysis.

### D.1 Command Templates (6 Templates - All Validated)

**4. COMMAND_DATA_TRANSFORMATION_TEMPLATE.md (Score: 7.8/10)**

**Use Cases:**
- ETL pipelines (Extract, Transform, Load)
- Data format conversions (CSV ↔ Excel ↔ JSON)
- Data migration between systems
- Data quality improvement workflows

**Structure (7 sections):**
```markdown
# Data Transformation Command

## Phase 1: Load Data
- Validate source file format
- Check schema/structure
- Document data profile

## Phase 2: Transform Data
- Apply transformation rules
- Handle edge cases (NULL, duplicates)
- Track transformation metrics

## Phase 3: Validate Output
- Data quality checks
- Completeness verification
- Accuracy validation

## Phase 4: Output
- Write to target format
- Generate audit trail
- Create summary report
```

**Key Differentiators vs RPIV:**
- No research phase (transformation rules are known)
- Focus on data quality gates
- Pipeline-oriented (Load → Transform → Validate → Output)
- No human checkpoints (automated workflow)

**External Validation:** data-analyst pattern (transformation focus)

---

**5. COMMAND_ORCHESTRATION_TEMPLATE.md (Score: 7.5/10)**

**Use Cases:**
- Multi-agent coordination workflows
- Complex approval chains
- Dependency-driven processes
- State machine implementations

**Structure (8 sections):**
```markdown
# Orchestration Command

## Phase 1: Define Dependency Graph
- List agents/tasks
- Document dependencies
- Define execution order

## Phase 2: Initialize State
- Set up state variables
- Define transition rules
- Create monitoring structure

## Phase 3: Coordinate Execution
- Invoke agents in order
- Track state transitions
- Handle failures gracefully

## Phase 4: Aggregate Results
- Collect outputs from all agents
- Validate completion criteria
- Generate consolidated report
```

**Key Differentiators vs RPIV:**
- Manages multiple agents (not single workflow)
- Dependency tracking (execution order based on dependencies)
- State management (persistent state across agent invocations)
- Coordination focus (vs research/implementation focus)

**External Validation:** workflow-orchestrator, task-distributor patterns

---

**6. COMMAND_REPORTING_TEMPLATE.md (Score: 7.2/10)**

**Use Cases:**
- Executive dashboards
- Financial reports (variance, P&L, balance sheet)
- Analytics summaries
- KPI tracking reports

**Structure (7 sections):**
```markdown
# Reporting Command

## Phase 1: Define Data Sources
- Identify source files/databases
- Document required metrics
- Define aggregation rules

## Phase 2: Aggregate Data
- Load all data sources
- Apply aggregation logic
- Calculate derived metrics

## Phase 3: Analyze Trends
- Identify patterns
- Calculate variances
- Flag anomalies

## Phase 4: Format Report
- Apply formatting rules
- Generate visualizations (tables, charts)
- Add executive summaries

## Phase 5: Distribute
- Output to multiple formats (Excel, PDF, HTML)
- Send to distribution list
- Archive with timestamp
```

**Key Differentiators vs RPIV:**
- Aggregation focus (combine multiple sources)
- Multi-format output (Excel + PDF + HTML)
- Distribution channels (email, shared drive, etc.)
- No implementation phase (presentation-focused)

**External Validation:** data-analyst, business-analyst patterns (reporting specialization)

---

### D.2 Agent Templates (3 Templates - Validated Against 116 External Agents)

**VALIDATION SUMMARY:**
- ✅ **KEPT:** 3 templates (DOMAIN_SPECIALIST, RESEARCHER, REVIEWER) - architecturally distinct tool tiers
- ❌ **REMOVED:** 3 templates (ORCHESTRATOR, ANALYZER, GENERATOR) - anti-patterns or redundancies
- **Evidence:** 116 external agents in awesome-claude-code-subagents + 12-factor-agents principles

**1. AGENT_DOMAIN_SPECIALIST_TEMPLATE.md (Score: 9.5/10 ↑) - PRIMARY**

**Pattern Frequency:** 100+ agents (86% of total) 🌟

**Use Cases (Validated from External Agents):**
- Language expertise: python-pro, typescript-pro, rust-engineer (23 agents)
- Domain expertise: fintech-engineer, quant-analyst, healthcare-specialist (18 agents)
- Infrastructure: kubernetes-specialist, cloud-architect (12 agents)
- **Data analysis:** data-analyst, data-scientist (12 agents) - was "Analyzer"
- **Artifact generation:** cli-developer, tooling-engineer (10 agents) - was "Generator"

**Structure (6 major sections - STANDARDIZED):**
```markdown
# Role Statement (1-2 paragraphs)
You are a [seniority] [domain] specialist with expertise in [areas]...

## Communication Protocol
### Context Query Format (JSON)
{
  "requesting_agent": "domain-specialist-name",
  "requirements": "..."
}

## Checklist (8 items)
- [ ] Domain criterion 1 verified
- [ ] Domain criterion 2 achieved
...

## Development Workflow
### Phase 1: Analysis
- Understand requirements
- Review existing state
### Phase 2: Implementation
- Execute domain-specific work
- Track progress
### Phase 3: Excellence Delivery
- Validate quality
- Document results

## Integration Notes (Optional)
Work with:
- @related-agent-1 on [task]
...

## Anti-Patterns (Optional)
❌ Bad practice 1
✅ Good practice 1
```

**Tool Tier:** Full access - `[Read, Write, Edit, Bash, Glob, Grep]` (100% consistency across 100+ agents)

**Key Insights:**
- **THIS IS THE PRIMARY TEMPLATE** - use for 86% of agent needs
- data-analyst is NOT a separate template, it's a domain specialist in data analysis
- cli-developer is NOT a separate template, it's a domain specialist in CLI development
- External agents classify these as "domain specialists" not separate categories

**External Examples:**
- `/external/awesome-claude-code-subagents/categories/02-language-specialists/python-pro.md`
- `/external/awesome-claude-code-subagents/categories/07-specialized-domains/fintech-engineer.md`
- `/external/awesome-claude-code-subagents/categories/05-data-ai/data-analyst.md` (was "analyzer")
- `/external/awesome-claude-code-subagents/categories/06-developer-experience/cli-developer.md` (was "generator")

---

**2. AGENT_RESEARCHER_TEMPLATE.md (Score: 8.6/10 ↑)**

**Pattern Frequency:** 6 agents (5% of total, 100% tool consistency)

**Use Cases (Validated from External Agents):**
- competitive-analyst.md (competitive intelligence)
- data-researcher.md (data source discovery)
- market-researcher.md (market analysis)
- research-analyst.md (general research)
- search-specialist.md (information retrieval)
- trend-analyst.md (trend identification)

**Structure (6 major sections):**
Same as Domain Specialist, but with investigation-focused workflow.

**Tool Tier:** Read + Web - `[Read, Grep, Glob, WebFetch, WebSearch]` (100% consistency across 6 agents)

**Key Differentiator:**
- **ONLY template with web research tools** (WebFetch, WebSearch)
- Architecturally distinct from Domain Specialist (different tools = different permissions)
- Discovery focus (NOT transformation like analysts)

---

**3. AGENT_REVIEWER_TEMPLATE.md (Score: 7.8/10 ↓)**

**Pattern Frequency:** 4-6 agents (3-5% of total)

**Use Cases (Validated from External Agents):**
- code-reviewer.md (code quality verification)
- security-auditor.md (security compliance)
- architect-reviewer.md (architecture review)
- compliance-auditor.md (regulatory compliance)

**Structure (6 major sections):**
Same as Domain Specialist, but with verification-focused workflow and APPROVE/REJECT output.

**Tool Tier:** Read-only - `[Read, Grep, Glob]` (100% consistency across reviewers)

**Key Differentiator:**
- **Read-only by security design** (no code modification)
- Architecturally distinct from Domain Specialist (different tools = different permissions)
- Verification focus with structured output (CRITICAL/WARNING/SUGGESTION, APPROVE/REJECT)

**Note:** Project code-reviewer.md uses this pattern.

---

### D.3 Removed Templates (Anti-Patterns and Redundancies)

**❌ AGENT_ORCHESTRATOR (Anti-Pattern)**

**Why Removed:**
1. **Context Isolation Violation:** Agents operate in separate contexts (code-reviewer.md:254), cannot communicate
2. **No Task Tool:** Task tool for coordination is SDK-only, NOT available in `.claude/agents/`
3. **Duplicates Command Functionality:** Orchestration is what COMMANDS do (variance-analysis.md invokes @code-reviewer)
4. **12-Factor Violation:** Factor 10 states "agents are building blocks in a larger, mostly deterministic system" - the system = COMMAND

**Evidence:**
- `/external/12-factor-agents/content/factor-10-small-focused-agents.md`: "Agents are just one building block"
- `/external/awesome-claude-code-subagents/categories/09-meta-orchestration/` agents assume SDK context
- Project variance-analysis.md (COMMAND) invokes @code-reviewer (AGENT) at checkpoints

**Replacement:** Use **COMMAND_ORCHESTRATION_TEMPLATE** instead (commands coordinate agents).

---

**❌ AGENT_ANALYZER (Redundant with Domain Specialist)**

**Why Removed:**
1. **Same Tools:** Read, Write, Edit, Bash, Glob, Grep (identical to Domain Specialist)
2. **Same Structure:** 6 sections, 275-285 lines, 3-phase workflow
3. **Same Pattern:** External agents classify data-analyst AS a domain specialist
4. **Content vs Structure:** "Analysis" is domain content, not template structure

**Evidence:**
- `/external/awesome-claude-code-subagents/categories/05-data-ai/data-analyst.md` - uses Domain Specialist pattern
- Tools are identical to python-pro, fintech-engineer, kubernetes-specialist
- 12 data/AI agents ALL use Domain Specialist structure

**Replacement:** Use **AGENT_DOMAIN_SPECIALIST_TEMPLATE** with data analysis domain areas.

---

**❌ AGENT_GENERATOR (Redundant with Domain Specialist)**

**Why Removed:**
1. **Same Tools:** Read, Write, Edit, Bash, Glob, Grep (identical to Domain Specialist)
2. **Same Structure:** 6 sections, 275-285 lines, 3-phase workflow
3. **Same Pattern:** External agents classify cli-developer AS a domain specialist
4. **Content vs Structure:** "Generation" is domain content, not template structure

**Evidence:**
- `/external/awesome-claude-code-subagents/categories/06-developer-experience/cli-developer.md` - uses Domain Specialist pattern
- Tools are identical to python-pro, fintech-engineer, data-analyst
- 10 developer experience agents ALL use Domain Specialist structure

**Replacement:** Use **AGENT_DOMAIN_SPECIALIST_TEMPLATE** with CLI/artifact generation domain areas.

---

### D.4 Scoring Rationale

**Command Template Scores:**
- RPIV (9.8/10): Proven in production (variance-analysis.md), multi-agent consensus
- Validation (8.6/10): Proven in production (sync-docs.md), clear use cases
- Batch (8.4/10): High FP&A user demand, external validation
- **Data Transformation (7.8/10):** Distinct from RPIV (no research), data-analyst pattern, FP&A ETL needs
- **Orchestration (7.5/10):** Workflow-orchestrator pattern, multi-agent coordination unique
- **Reporting (7.2/10):** Previously 6.4/10, upgraded with distinct aggregation/formatting/distribution focus

**Agent Template Scores (REVISED after 50+ source validation):**
- **Domain Specialist (9.5/10 ↑):** PRIMARY template - 86% frequency, 100+ agents, gold standard pattern
- **Researcher (8.6/10 ↑):** Distinct web research tools, 100% tool consistency across 6 agents
- **Reviewer (7.8/10 ↓):** Niche but critical (3-5%), read-only security constraint, proven in code-reviewer.md
- ❌ ~~Orchestrator (N/A):~~ **REMOVED** - Anti-pattern (commands coordinate agents, not agents)
- ❌ ~~Analyzer (6.2/10):~~ **REMOVED** - Redundant (data-analyst IS a domain specialist)
- ❌ ~~Generator (6.0/10):~~ **REMOVED** - Redundant (cli-developer IS a domain specialist)

**Final Template Count:**
- **Commands:** 9 templates (6 original + 3 new from 2024-2025 research)
  - Project-validated: RPIV, Validation (variance-analysis.md, sync-docs.md)
  - FP&A patterns: Batch, Data Transformation, Orchestration, Reporting
  - 2024-2025 research: Human Approval (HumanLayer), Reflection (Anthropic/Google), Routing (Anthropic)
- **Agents:** 3 templates (validated against 116 external agents + 12-factor principles)
- **Total:** 12 templates (up from 9 originally, based on 2024-2025 research expansion)

**Validation Rigor:**
- 116 external agents analyzed for patterns (awesome-claude-code-subagents)
- 12-factor-agents architectural principles applied (HumanLayer/Dex Horthy)
- Anthropic Building Effective Agents (5 workflow patterns validated)
- Google/DeepMind agentic patterns (reflection, planning validated)
- Production lessons 2024-2025 (structured workflows, eval-driven development)
- Claude Code implementation examined (variance-analysis.md, code-reviewer.md)
- Tool tier consistency verified (100% match for Domain Specialist and Researcher)
- Section count standardized (6 major sections for all agents, 6-9 for commands)
- Anti-patterns identified and removed (orchestrator context violation)
- Redundancies eliminated (analyzer/generator merged into domain specialist)
- New patterns validated (human approval, reflection, routing from 2024-2025 research)

**Reference Guides Added:**
- 7 optimal prompting pattern guides (HumanLayer Factors 2, 3, 7 + Anthropic + Google + Production)
- Total reference guides: 16 for commands (9 command-specific + 7 prompting patterns)
- Total reference guides: 10 for agents (3 agent-specific + 7 shared prompting patterns)

---

**END OF RESEARCH**

Research phase complete with 2024-2025 expansion.

**Summary:**
- **12 templates total** (9 commands + 3 agents)
- **26 reference guides** (16 for commands, 10 for agents, 7 shared prompting patterns)
- **Validated against:** 116 external agents + 12-factor principles + Anthropic + HumanLayer + Google/DeepMind + Production 2024-2025
- **Ready for:** Planning phase (create plan.md with implementation roadmap)
