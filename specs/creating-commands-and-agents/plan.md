# Creating Commands & Agents Skills - Implementation Plan

**Date:** 2025-11-09
**Status:** Planning Phase
**Scope:** Implementation roadmap for meta-skills that generate slash commands and subagents

---

## Executive Summary

**Objective:** Implement two production-grade meta-skills (`creating-commands` and `creating-agents`) following the proven `creating-skills` architecture pattern.

**Total Deliverables:**
- **12 templates** (9 commands + 3 agents)
- **26 reference guides** (16 for commands, 10 for agents, 7 shared prompting patterns)
- **8 validators** (4 per skill)
- **2 orchestrators** (generate_command.py, generate_agent.py)
- **2 skills** (SKILL.md for each)

**Evidence Base:**
- 116 external agents (awesome-claude-code-subagents)
- 12-Factor Agents principles (HumanLayer/Dex Horthy)
- Anthropic Building Effective Agents (2024-2025)
- Google/DeepMind agentic patterns (2024-2025)
- Production lessons 2024-2025

**Timeline:** 5 implementation phases (prioritized by score and impact)

---

## Part 1: Architecture Overview

### 1.1 Directory Structure

```
.claude/skills/
├── creating-commands/
│   ├── SKILL.md                                        # Main skill (<200 lines)
│   ├── assets/templates/                               # 9 command templates
│   ├── scripts/                                        # 4 validators + 1 orchestrator
│   └── references/                                     # 16 guides (9 command + 7 prompting patterns)
└── creating-agents/
    ├── SKILL.md                                        # Main skill (<200 lines)
    ├── assets/templates/                               # 3 agent templates
    ├── scripts/                                        # 4 validators + 1 orchestrator
    └── references/                                     # 10 guides (3 agent + 7 symlinked prompting patterns)
```

### 1.2 Template Summary

**Commands (9 templates, scores 7.2-9.8):**
| Template | Score | Source | Lines | Sections |
|----------|-------|--------|-------|----------|
| COMMAND_RPIV | 9.8/10 | Project (variance-analysis.md) | ~250 | 8 |
| COMMAND_HUMAN_APPROVAL | 9.2/10 | HumanLayer Factor 7 | ~270 | 9 |
| COMMAND_REFLECTION | 8.8/10 | Anthropic/Google | ~260 | 8 |
| COMMAND_VALIDATION | 8.6/10 | Project (sync-docs.md) | ~200 | 6 |
| COMMAND_BATCH_PROCESSING | 8.4/10 | FP&A patterns | ~230 | 7 |
| COMMAND_ROUTING | 8.2/10 | Anthropic Routing | ~220 | 7 |
| COMMAND_DATA_TRANSFORMATION | 7.8/10 | ETL patterns | ~220 | 7 |
| COMMAND_ORCHESTRATION | 7.5/10 | 12-Factor Agents | ~240 | 8 |
| COMMAND_REPORTING | 7.2/10 | Analytics patterns | ~210 | 7 |

**Agents (3 templates, scores 7.8-9.5):**
| Template | Score | Source | Lines | Sections |
|----------|-------|--------|-------|----------|
| AGENT_DOMAIN_SPECIALIST | 9.5/10 | 116 agents (86% frequency) | ~280 | 6 |
| AGENT_RESEARCHER | 8.6/10 | 6 agents (web tools) | ~280 | 6 |
| AGENT_REVIEWER | 7.8/10 | 4-6 agents (read-only) | ~280 | 6 |

**Reference Guides (26 total):**
- 9 command-specific guides (300-400 lines each)
- 3 agent-specific guides (300-400 lines each)
- 7 prompting pattern guides (340-420 lines each, shared between skills)

---

## Part 2: Implementation Phases

### Phase 1: Critical Production Patterns (Week 1)

**Priority:** Highest scores + production-critical patterns

**Deliverables:**
1. **COMMAND_RPIV_TEMPLATE.md** (9.8/10)
   - Source: Project variance-analysis.md
   - 4 checkpoints (Research, Plan, Implement, Verify)
   - Progress tracking tables
   - Success criteria checklists
   - Reference: `references/rpiv-workflow-guide.md`

2. **COMMAND_HUMAN_APPROVAL_TEMPLATE.md** (9.2/10) 🆕
   - Source: HumanLayer Factor 7
   - Structured approval requests (JSON format)
   - Risk assessment (risk_level, reversible flag)
   - Audit trail (timestamp, user, decision, action)
   - Timeout handling
   - Reference: `references/human-approval-guide.md`

3. **AGENT_DOMAIN_SPECIALIST_TEMPLATE.md** (9.5/10)
   - Source: 116 external agents (PRIMARY pattern)
   - 6 major sections (standardized)
   - 8-15 domain areas
   - Full tool access
   - Reference: `references/domain-specialist-guide.md`

**Validators Needed:**
- `validate_command_yaml.py` (supports RPIV + Human Approval)
- `validate_agent_yaml.py` (supports Domain Specialist)
- `validate_command_structure.py` (2 templates: 8-9 sections)
- `validate_agent_structure.py` (1 template: 6 sections)

**Success Criteria:**
- [ ] RPIV template generates variance-analysis.md equivalent
- [ ] Human Approval template validates with risk assessment fields
- [ ] Domain Specialist template generates fintech-engineer.md equivalent
- [ ] All validators pass on generated outputs

---

### Phase 2: High-Value Self-Improvement & Research Patterns (Week 2)

**Priority:** High scores (8.6-8.8) + distinct capabilities

**Deliverables:**
4. **COMMAND_REFLECTION_TEMPLATE.md** (8.8/10) 🆕
   - Source: Anthropic Evaluator-Optimizer + Google reflection
   - Self-evaluation loops (Draft → Reflect → Identify → Refine)
   - Quality thresholds (stop when all dimensions ≥8/10)
   - Max iteration limits (prevent infinite loops)
   - Transparent improvement tracking
   - Reference: `references/reflection-guide.md`

5. **COMMAND_VALIDATION_TEMPLATE.md** (8.6/10)
   - Source: Project sync-docs.md
   - Systematic checks (10+ validation rules)
   - ✅⚠️❌ reporting format
   - Read-only operations
   - No checkpoints (single execution)
   - Reference: `references/validation-patterns.md`

6. **AGENT_RESEARCHER_TEMPLATE.md** (8.6/10)
   - Source: 6 external agents (web research pattern)
   - Read + Web tools (WebFetch, WebSearch)
   - Investigation workflow structure
   - Discovery focus (NOT transformation)
   - Reference: `references/researcher-patterns.md`

**Validators Updated:**
- `validate_command_structure.py` (4 templates now: 6-9 sections)
- `validate_agent_structure.py` (2 templates now: 6 sections each)

**Success Criteria:**
- [ ] Reflection template demonstrates quality improvement loop
- [ ] Validation template generates sync-docs.md equivalent
- [ ] Researcher template has correct web tool restrictions
- [ ] Quality gates prevent infinite reflection loops

---

### Phase 3: Supporting Workflow Patterns (Week 3)

**Priority:** Supporting workflows (7.8-8.4) + high FP&A demand

**Deliverables:**
7. **COMMAND_BATCH_PROCESSING_TEMPLATE.md** (8.4/10)
   - Source: FP&A multi-file patterns
   - Per-item error handling (don't stop batch)
   - Progress tracking table
   - Summary report (successes/failures/total)
   - Graceful degradation
   - Reference: `references/batch-processing-guide.md`

8. **COMMAND_ROUTING_TEMPLATE.md** (8.2/10) 🆕
   - Source: Anthropic Routing pattern
   - Classification first (domain, complexity, urgency)
   - Decision table (explicit routing logic)
   - Specialized handler delegation
   - Model selection support (haiku vs sonnet)
   - Reference: `references/routing-guide.md`

9. **AGENT_REVIEWER_TEMPLATE.md** (7.8/10)
   - Source: Project code-reviewer.md + 4-6 external agents
   - Read-only tools (security constraint)
   - Verification checklist (8 items)
   - APPROVE/REJECT output format
   - CRITICAL/WARNING/SUGGESTION structure
   - Reference: `references/reviewer-patterns.md`

10. **COMMAND_DATA_TRANSFORMATION_TEMPLATE.md** (7.8/10)
    - Source: ETL patterns
    - Load → Transform → Validate → Output pipeline
    - Data quality gates
    - No research phase (transformation rules known)
    - Reference: `references/data-transformation-guide.md`

**Validators Updated:**
- `validate_command_structure.py` (7 templates now: 6-9 sections)
- `validate_agent_structure.py` (3 templates complete: 6 sections each)
- `validate_agent_tools.py` (3 tool tiers validated)
- `validate_command_usage.py` (batch and routing arg patterns)

**Success Criteria:**
- [ ] Batch template handles per-item failures gracefully
- [ ] Routing template has explicit decision table
- [ ] Reviewer template enforces read-only tool restrictions
- [ ] Data Transformation template has quality gates

---

### Phase 4: Specialized Command Workflows (Week 4)

**Priority:** Specialized patterns (7.2-7.5)

**Deliverables:**
11. **COMMAND_ORCHESTRATION_TEMPLATE.md** (7.5/10)
    - Source: 12-Factor Agents (Factor 8, 10)
    - Dependency graph management
    - Multi-agent coordination (commands coordinate agents)
    - State management across invocations
    - Reference: `references/orchestration-guide.md`

12. **COMMAND_REPORTING_TEMPLATE.md** (7.2/10)
    - Source: Analytics/BI patterns
    - Aggregate → Analyze → Format → Distribute
    - Multi-format output (Excel, PDF, HTML)
    - Distribution channels
    - Reference: `references/reporting-guide.md`

**Validators Complete:**
- `validate_command_structure.py` (9 templates final: 6-9 sections)
- All 4 validators operational for each skill

**Success Criteria:**
- [ ] Orchestration template manages dependencies correctly
- [ ] Reporting template supports multi-format output
- [ ] All 9 command templates pass validators
- [ ] All 3 agent templates pass validators

---

### Phase 5: Optimal Prompting Pattern Guides (Week 5)

**Priority:** Reference documentation (shared across skills)

**Deliverables (7 prompting pattern guides):**
13. **own-your-prompts.md** (~350 lines)
    - Source: HumanLayer Factor 2
    - Anti-pattern: Framework abstraction
    - Claude Code pattern: Direct .md editing
    - Benefits: Full control, version control, testing, transparency

14. **reflection-pattern.md** (~400 lines)
    - Source: Anthropic Evaluator-Optimizer + Google/DeepMind
    - Pattern: Draft → Reflect → Identify → Refine → Quality Gate
    - When: Quality > speed, literary translation, peer review simulation
    - Claude Code: COMMAND_REFLECTION_TEMPLATE implementation

15. **planning-pattern.md** (~380 lines)
    - Source: Anthropic Orchestrator-Workers + DeepMind
    - Pattern: Decompose → Estimate → Execute → Adapt
    - When: Complex multi-step (20+), unpredictable subtasks
    - Claude Code: COMMAND_ORCHESTRATION_TEMPLATE implementation

16. **human-in-loop.md** (~420 lines)
    - Source: HumanLayer Factor 7
    - Pattern: Structured approval requests (JSON format)
    - When: High-risk, irreversible, compliance-critical
    - Claude Code: COMMAND_HUMAN_APPROVAL_TEMPLATE implementation

17. **context-management.md** (~360 lines)
    - Source: HumanLayer Factor 3 + Production 2024-2025
    - Pattern: Evolved context (not context dump)
    - Progressive disclosure (add details as needed)
    - Claude Code: RPIV checkpoints, phase-based context

18. **tool-documentation.md** (~340 lines)
    - Source: Anthropic ACI principles
    - Best practices: Absolute paths, clear boundaries, examples
    - Common mistakes: Relative paths, unclear names, format-heavy
    - Claude Code: Agent frontmatter + inline examples

19. **eval-driven-development.md** (~390 lines)
    - Source: Production 2024-2025
    - Scientific iteration: Define → Baseline → Iterate → A/B Test → Monitor
    - Tools: Test sets, automated scoring, logging, A/B framework
    - Claude Code: Validators as quality gates, version control for A/B

**Reference Guide Organization:**
```
.claude/skills/creating-commands/references/
├── rpiv-workflow-guide.md
├── human-approval-guide.md
├── reflection-guide.md
├── validation-patterns.md
├── batch-processing-guide.md
├── routing-guide.md
├── data-transformation-guide.md
├── orchestration-guide.md
├── reporting-guide.md
└── prompting-patterns/
    ├── own-your-prompts.md
    ├── reflection-pattern.md
    ├── planning-pattern.md
    ├── human-in-loop.md
    ├── context-management.md
    ├── tool-documentation.md
    └── eval-driven-development.md

.claude/skills/creating-agents/references/
├── domain-specialist-guide.md
├── researcher-patterns.md
├── reviewer-patterns.md
└── prompting-patterns/  → symlink to ../creating-commands/references/prompting-patterns/
```

**Success Criteria:**
- [ ] All 7 prompting pattern guides <500 lines
- [ ] Each guide includes examples from source research
- [ ] Anti-patterns clearly documented
- [ ] Claude Code adaptations explicit
- [ ] Cross-references to implementing templates

---

## Part 3: Orchestrator Scripts

### 3.1 generate_command.py

**Purpose:** Interactive command template generator

**Features:**
- 9 template options (RPIV, Human Approval, Reflection, Validation, Batch, Routing, Data Transformation, Orchestration, Reporting)
- Interactive prompts (name, environment, description, args, template-specific params)
- Placeholder replacement (`{{VARIABLE}}` → actual values)
- Temp directory generation → validation → commit/rollback
- Atomic operations (all validators pass OR rollback)

**Workflow:**
```python
def generate_command():
    # 1. Interactive prompts
    name = prompt("Command name (kebab-case): ")
    env = prompt("Environment (dev/prod/shared): ")
    template_type = prompt("Template type (1-9): ")
    description = prompt("Description (≤1024 chars): ")
    args = prompt_args()  # Template-specific

    # 2. Select template
    template = load_template(template_type)

    # 3. Generate in temp dir
    temp_path = create_temp_dir()
    replacements = build_replacements(name, env, description, args)
    output = template.format(**replacements)
    write_file(temp_path / f"{name}.md", output)

    # 4. Run all validators
    results = []
    results.append(validate_command_yaml(temp_path))
    results.append(validate_command_naming(temp_path, env))
    results.append(validate_command_structure(temp_path, template_type))
    results.append(validate_command_usage(temp_path))

    # 5. Commit or rollback
    if all(r.exit_code == 0 for r in results):
        move_to_final(temp_path, f".claude/commands/{env}/{name}.md")
        print(f"✅ Created {env}/{name}.md")
    else:
        rollback_temp(temp_path)
        print("❌ Validation failed, rolled back")
        for r in results:
            if r.exit_code != 0:
                print(f"  - {r.validator}: {r.errors}")
```

**Template-Specific Prompts:**
| Template | Additional Prompts |
|----------|-------------------|
| RPIV | Research steps, plan steps, implement tasks, verify criteria |
| Human Approval | Action, risk_level, reversible, urgency |
| Reflection | Quality criteria, max_iterations, quality_threshold |
| Validation | Check names, expected results (10+) |
| Batch | Input dir, pattern, loop steps |
| Routing | Domains, complexities, handlers (decision table) |
| Data Transformation | Source file, transformations, quality checks |
| Orchestration | Agents, dependencies, state vars |
| Reporting | Data sources, metrics, formats |

---

### 3.2 generate_agent.py

**Purpose:** Interactive agent template generator

**Features:**
- 3 template options (Domain Specialist, Researcher, Reviewer)
- Interactive prompts (name, description, tool tier, domain areas)
- Placeholder replacement
- Temp directory → validation → commit/rollback
- Tool tier enforcement (exact tool list per template type)

**Workflow:**
```python
def generate_agent():
    # 1. Interactive prompts
    name = prompt("Agent name (kebab-case): ")
    template_type = prompt("Template type (domain-specialist/researcher/reviewer): ")
    description = prompt("Description (100-150 chars): ")
    domain = prompt("Domain (e.g., financial, python, data-analysis): ")

    # 2. Tool tier auto-assigned
    tool_tier = TOOL_TIERS[template_type]
    # domain-specialist: [Read, Write, Edit, Bash, Glob, Grep]
    # researcher: [Read, Grep, Glob, WebFetch, WebSearch]
    # reviewer: [Read, Grep, Glob]

    # 3. Template-specific prompts
    if template_type == "domain-specialist":
        areas = prompt_domain_areas(8, 15)  # 8-15 areas
    elif template_type == "researcher":
        research_focus = prompt("Research focus: ")
    elif template_type == "reviewer":
        checklist_items = prompt_checklist(8)  # 8 items

    # 4. Generate in temp dir
    temp_path = create_temp_dir()
    template = load_template(template_type)
    replacements = build_replacements(name, description, domain, areas, tool_tier)
    output = template.format(**replacements)
    write_file(temp_path / f"{name}.md", output)

    # 5. Run all validators
    results = []
    results.append(validate_agent_yaml(temp_path))
    results.append(validate_agent_naming(temp_path))
    results.append(validate_agent_structure(temp_path, template_type))
    results.append(validate_agent_tools(temp_path, template_type))

    # 6. Commit or rollback
    if all(r.exit_code == 0 for r in results):
        move_to_final(temp_path, f".claude/agents/{name}.md")
        print(f"✅ Created agents/{name}.md")
    else:
        rollback_temp(temp_path)
        print("❌ Validation failed, rolled back")
```

---

## Part 4: Validator Specifications

### 4.1 Command Validators

**validate_command_yaml.py:**
- Required: `description` (≤1024 chars)
- Optional: `model`, `allowed-tools`, `argument-hint`, `disable-model-invocation`
- Exit 0 if valid, 1 if error, 2 if warning

**validate_command_naming.py:**
- File pattern: `^[a-z0-9]+(-[a-z0-9]+)*\.md$`
- Environment: File in `dev/`, `prod/`, or `shared/` subdir
- Name matches file (consistency check)

**validate_command_structure.py:**
- 9 template types, each with defined section count:
  - RPIV: 8 sections (Header, STEP 1-4, Success Criteria, Example, Anti-Patterns)
  - Human Approval: 9 sections (Header, Phase 1-4, Approval Format, Success Criteria, Example, Anti-Patterns)
  - Reflection: 8 sections (Header, Phase 1-6, Success Criteria, Example)
  - Validation: 6 sections (Header, Checks, Report Format, Usage Example, Anti-Patterns)
  - Batch: 7 sections (Header, Discovery, Loop, Summary, Error Handling, Example, Anti-Patterns)
  - Routing: 7 sections (Header, Classify, Route, Delegate, Aggregate, Decision Table, Example)
  - Data Transformation: 7 sections (Header, Load, Transform, Validate, Output, Example, Anti-Patterns)
  - Orchestration: 8 sections (Header, Dependency Graph, Coordination, State, Execution, Success Criteria, Example, Anti-Patterns)
  - Reporting: 7 sections (Header, Data Sources, Aggregation, Analysis, Formatting, Distribution, Example)

**validate_command_usage.py:**
- Usage line present: `**Usage:** /command <arg1> [arg2]`
- Arguments match `argument-hint` if specified
- Positional args documented ($1, $2, $3 if used)
- Template-specific validation (e.g., Human Approval requires risk assessment fields)

---

### 4.2 Agent Validators

**validate_agent_yaml.py:**
- Required: `name` (kebab-case), `description` (100-150 chars)
- Optional: `tools`, `model`
- No CSO check (explicit `@name` invocation)

**validate_agent_naming.py:**
- File pattern: `^[a-z0-9]+(-[a-z0-9]+)*\.md$`
- Name matches file
- Location: `.claude/agents/` (global, not environment-specific)

**validate_agent_structure.py:**
- All 3 templates: 6 major sections
  1. Role Statement
  2. Communication Protocol
  3. Checklist (8 items)
  4. Development Workflow (3 phases)
  5. Integration Notes (optional)
  6. Anti-Patterns (optional)
- Domain Specialist: 8-15 domain areas (subsections)
- Researcher: Investigation workflow structure
- Reviewer: Verification checklist + output format

**validate_agent_tools.py:**
- Reviewer: `tools: [Read, Grep, Glob]` (exactly - read-only)
- Researcher: `tools: [Read, Grep, Glob, WebFetch, WebSearch]` (exactly - read + web)
- Domain Specialist: `tools: [Read, Write, Edit, Bash, Glob, Grep]` (exactly - full access)
- Error if tools don't match template type exactly

---

## Part 5: Testing Strategy

### 5.1 Validator Testing

**Unit Tests (pytest):**
```python
# test_validate_command_yaml.py
def test_missing_description():
    content = "---\nmodel: sonnet\n---\n"
    result = validate_yaml(content)
    assert result.exit_code == 1
    assert "description required" in result.errors

def test_description_too_long():
    content = f"---\ndescription: {'x' * 1025}\n---\n"
    result = validate_yaml(content)
    assert result.exit_code == 2  # warning

# test_validate_command_structure.py
def test_rpiv_has_8_sections():
    content = generate_rpiv_template(valid_params)
    result = validate_structure(content, "rpiv")
    assert result.exit_code == 0

def test_human_approval_has_9_sections():
    content = generate_human_approval_template(valid_params)
    result = validate_structure(content, "human-approval")
    assert result.exit_code == 0
    # Must have risk_level field
    assert "risk_level" in content

# test_validate_agent_tools.py
def test_reviewer_requires_read_only():
    content = """
---
name: code-reviewer
tools: [Read, Write, Grep, Glob]  # WRONG - has Write
---
"""
    result = validate_tools(content, "reviewer")
    assert result.exit_code == 1
    assert "must be [Read, Grep, Glob]" in result.errors
```

**Integration Tests:**
```python
# test_generate_command.py
def test_rpiv_end_to_end():
    result = generate_command(
        name="test-workflow",
        template="rpiv",
        environment="dev",
        description="Test RPIV workflow",
        args=["file1", "file2"]
    )
    assert result.success == True
    assert Path(".claude/commands/dev/test-workflow.md").exists()

    # Run all validators
    for validator in VALIDATORS:
        assert run_validator(validator, result.path).exit_code == 0

def test_human_approval_end_to_end():
    result = generate_command(
        name="deploy-approval",
        template="human-approval",
        environment="prod",
        description="Deployment approval workflow",
        args=["tag", "environment"],
        risk_params={"risk_level": "high", "reversible": False}
    )
    assert result.success == True
    content = read_file(result.path)
    assert "risk_level" in content
    assert "reversible" in content
    assert "audit_context" in content
```

---

### 5.2 Template Testing

**Checklist for Each Template:**
- [ ] All placeholders (`{{VARIABLE}}`) documented
- [ ] Example replacement values provided
- [ ] Generated file passes all validators
- [ ] Matches external patterns (awesome-claude-code-subagents for agents)
- [ ] Progressive disclosure links work
- [ ] Section count correct
- [ ] Tool restrictions correct (agents)

**Manual Testing:**
1. Generate command/agent from template using orchestrator script
2. Fill placeholders manually (verify prompts make sense)
3. Invoke command/agent in real scenario
4. Verify output matches expected format
5. Iterate based on usability feedback

**Template-Specific Tests:**
- **RPIV:** 4 checkpoints work, progress table tracks tasks
- **Human Approval:** Approval request is structured, audit trail logs
- **Reflection:** Quality gates prevent infinite loops, improvement demonstrated
- **Routing:** Decision table is explicit, routes to correct handlers
- **Domain Specialist:** 8-15 areas, full tools, 6 sections
- **Researcher:** Web tools only, investigation structure
- **Reviewer:** Read-only tools, APPROVE/REJECT output

---

## Part 6: Success Criteria (Quality Gates)

### 6.1 creating-commands Skill

**Required Deliverables:**
- [ ] SKILL.md (<200 lines)
- [ ] 9 templates (RPIV, Human Approval, Reflection, Validation, Batch, Routing, Data Transformation, Orchestration, Reporting)
- [ ] 4 validators (yaml, naming, structure for 9 templates, usage)
- [ ] 1 orchestrator (generate_command.py with 9 template options)
- [ ] 16 reference guides (9 command-specific + 7 prompting patterns)

**Quality Gates:**
- [ ] All validators pass on creating-commands SKILL.md
- [ ] Generated variance-analysis.md from RPIV template passes validators (project-proven)
- [ ] Generated sync-docs.md from Validation template passes validators (project-proven)
- [ ] Generated deployment-approval.md from Human Approval template validates (HumanLayer pattern)
- [ ] Generated translation-refine.md from Reflection template validates (Anthropic pattern)
- [ ] Generated query-router.md from Routing template validates (Anthropic pattern)
- [ ] Manual test: Generate new command from each template, verify functionality
- [ ] All 16 reference guides <500 lines (progressive disclosure target)

---

### 6.2 creating-agents Skill

**Required Deliverables:**
- [ ] SKILL.md (<200 lines)
- [ ] 3 templates (Domain Specialist, Researcher, Reviewer)
- [ ] 4 validators (yaml, naming, structure, tools)
- [ ] 1 orchestrator (generate_agent.py with 3 template options)
- [ ] 10 reference guides (3 agent-specific + 7 shared prompting patterns)

**Quality Gates:**
- [ ] All validators pass on creating-agents SKILL.md
- [ ] Generated code-reviewer.md from Reviewer template passes validators (project-proven)
- [ ] Generated fintech-engineer.md from Domain Specialist template passes validators (PRIMARY, 86%)
- [ ] Generated research-analyst.md from Researcher template passes validators (web tools)
- [ ] Manual test: Generate new agent from each template, invoke successfully
- [ ] All templates use 6 major sections (validated against 116 external agents)
- [ ] Tool tier validation: Reviewer (read-only), Researcher (read+web), Domain Specialist (full)
- [ ] All 10 reference guides accessible (3 agent + 7 shared prompting patterns)

---

### 6.3 Integration with creating-skills

**Consistency Checks:**
- [ ] Same directory structure (assets/templates/, scripts/, references/)
- [ ] Same orchestrator pattern (interactive prompts → temp dir → validate → commit/rollback)
- [ ] Same validator exit codes (0=pass, 1=error, 2=warning)
- [ ] Same placeholder format (`{{VARIABLE}}`)
- [ ] Same progressive disclosure strategy (main <200 lines, references/ for depth)
- [ ] Same atomic operations (all validators pass OR rollback)

---

## Part 7: Risk Mitigation

### 7.1 Technical Risks

**Risk 1: Template complexity creep**
- **Mitigation:** Strict line count targets (200-280 lines per template)
- **Validation:** Automated line count checks in validators
- **Escalation:** If template exceeds target by >20%, split into multiple templates or use references/

**Risk 2: Validator false positives/negatives**
- **Mitigation:** Comprehensive test suite (unit + integration tests)
- **Validation:** Test against known-good examples (variance-analysis.md, code-reviewer.md)
- **Escalation:** Manual review if validator disagrees with project-proven examples

**Risk 3: Placeholder replacement errors**
- **Mitigation:** Clear placeholder naming conventions (`{{COMMAND_NAME}}`, not `{{NAME}}`)
- **Validation:** Search for remaining `{{` after generation
- **Escalation:** Interactive prompts include examples (e.g., "Command name (kebab-case): variance-analysis")

**Risk 4: Reference guide duplication**
- **Mitigation:** Symlink prompting-patterns/ between creating-commands and creating-agents
- **Validation:** Single source of truth for shared patterns
- **Escalation:** If symlink not supported, use duplicate files with sync script

---

### 7.2 Scope Risks

**Risk 1: Scope expansion beyond 12 templates**
- **Mitigation:** Evidence-based template addition (score ≥7.0/10, distinct use case)
- **Validation:** Validate against external patterns (116 agents) + research (Anthropic, HumanLayer, Google)
- **Escalation:** User approval required for templates beyond 12

**Risk 2: Reference guide length explosion**
- **Mitigation:** Progressive disclosure (main <200 lines, references/ 300-500 lines)
- **Validation:** Automated length checks
- **Escalation:** Split long guides into multiple files (e.g., rpiv-workflow-guide.md → rpiv-checkpoints.md + rpiv-progress-tracking.md)

---

## Part 8: Implementation Timeline

### Week 1: Critical Production Patterns (Phase 1)
- [ ] COMMAND_RPIV_TEMPLATE.md + rpiv-workflow-guide.md
- [ ] COMMAND_HUMAN_APPROVAL_TEMPLATE.md + human-approval-guide.md
- [ ] AGENT_DOMAIN_SPECIALIST_TEMPLATE.md + domain-specialist-guide.md
- [ ] 4 validators (basic structure, 2-3 templates each)
- [ ] 2 orchestrators (basic, 1-3 template options each)

### Week 2: High-Value Patterns (Phase 2)
- [ ] COMMAND_REFLECTION_TEMPLATE.md + reflection-guide.md
- [ ] COMMAND_VALIDATION_TEMPLATE.md + validation-patterns.md
- [ ] AGENT_RESEARCHER_TEMPLATE.md + researcher-patterns.md
- [ ] Validators updated (4-6 templates)
- [ ] Orchestrators updated (2-6 template options)

### Week 3: Supporting Patterns (Phase 3)
- [ ] COMMAND_BATCH_PROCESSING_TEMPLATE.md + batch-processing-guide.md
- [ ] COMMAND_ROUTING_TEMPLATE.md + routing-guide.md
- [ ] AGENT_REVIEWER_TEMPLATE.md + reviewer-patterns.md
- [ ] COMMAND_DATA_TRANSFORMATION_TEMPLATE.md + data-transformation-guide.md
- [ ] Validators updated (7-10 templates)
- [ ] Orchestrators complete (9 commands, 3 agents)

### Week 4: Specialized Workflows (Phase 4)
- [ ] COMMAND_ORCHESTRATION_TEMPLATE.md + orchestration-guide.md
- [ ] COMMAND_REPORTING_TEMPLATE.md + reporting-guide.md
- [ ] All validators complete (9 commands, 3 agents)
- [ ] Integration testing (all templates + validators)

### Week 5: Prompting Pattern Guides (Phase 5)
- [ ] own-your-prompts.md (HumanLayer Factor 2)
- [ ] reflection-pattern.md (Anthropic/Google)
- [ ] planning-pattern.md (Anthropic/DeepMind)
- [ ] human-in-loop.md (HumanLayer Factor 7)
- [ ] context-management.md (HumanLayer Factor 3 + Production)
- [ ] tool-documentation.md (Anthropic ACI)
- [ ] eval-driven-development.md (Production 2024-2025)
- [ ] Symlink/duplicate for creating-agents
- [ ] Final integration testing (all deliverables)

---

## Part 9: Definition of Done

**For Each Template:**
- [ ] Template file exists in correct location
- [ ] All placeholders documented
- [ ] Example replacement values provided
- [ ] Passes all 4 validators
- [ ] Matches external pattern (if applicable)
- [ ] Reference guide complete (<500 lines)
- [ ] Cross-references to prompting patterns (if applicable)

**For Each Validator:**
- [ ] Python script in scripts/ directory
- [ ] Exit codes correct (0=pass, 1=error, 2=warning)
- [ ] Unit tests pass (pytest)
- [ ] Integration tests pass (end-to-end)
- [ ] Clear error messages
- [ ] Template-specific validation rules implemented

**For Each Orchestrator:**
- [ ] Interactive prompts implemented
- [ ] Template selection working
- [ ] Placeholder replacement working
- [ ] Temp dir creation/cleanup working
- [ ] All validators invoked
- [ ] Atomic commit/rollback working
- [ ] Clear success/failure messages

**For Each Reference Guide:**
- [ ] File in references/ directory
- [ ] <500 lines (progressive disclosure)
- [ ] Examples from source research included
- [ ] Anti-patterns documented
- [ ] Claude Code adaptations explicit
- [ ] Cross-references to templates work

**For Each Skill (SKILL.md):**
- [ ] <200 lines (high-level overview)
- [ ] CSO description (explicit invocation, not auto)
- [ ] Template characteristics table
- [ ] Validator descriptions
- [ ] Progressive disclosure pointers
- [ ] Passes creating-skills validators (if applicable)

---

## Appendix A: Evidence Cross-Reference

### A.1 Research Sources

**116 External Agents:**
- `/home/user/cc-sf-assistant/external/awesome-claude-code-subagents/`
- Pattern frequency: 86% Domain Specialist, 5% Researcher, 3-5% Reviewer
- Validation: Tool tiers, section counts, line lengths

**12-Factor Agents (HumanLayer/Dex Horthy):**
- `/home/user/cc-sf-assistant/external/12-factor-agents/`
- Factor 2: Own Your Prompts → prompting-patterns/own-your-prompts.md
- Factor 3: Own Your Context Window → prompting-patterns/context-management.md
- Factor 7: Contact Humans with Tools → COMMAND_HUMAN_APPROVAL_TEMPLATE.md
- Factor 8: Own Your Control Flow → COMMAND_ORCHESTRATION_TEMPLATE.md
- Factor 10: Small Focused Agents → Agent template validation (3 types only)

**Anthropic Building Effective Agents:**
- Web research 2024-2025
- Evaluator-Optimizer pattern → COMMAND_REFLECTION_TEMPLATE.md
- Routing pattern → COMMAND_ROUTING_TEMPLATE.md
- Orchestrator-Workers pattern → COMMAND_ORCHESTRATION_TEMPLATE.md + prompting-patterns/planning-pattern.md
- Tool documentation → prompting-patterns/tool-documentation.md

**Google/DeepMind Agentic Patterns:**
- Web research 2024-2025
- Reflection pattern → COMMAND_REFLECTION_TEMPLATE.md + prompting-patterns/reflection-pattern.md
- Planning pattern → prompting-patterns/planning-pattern.md

**Production Lessons 2024-2025:**
- Web research (multiple sources)
- Structured workflows over autonomy → COMMAND_ROUTING_TEMPLATE.md (deterministic routing)
- Evaluation-driven development → prompting-patterns/eval-driven-development.md
- Context engineering → prompting-patterns/context-management.md

---

### A.2 Project Files

**Existing Implementations:**
- `.claude/commands/prod/variance-analysis.md` → COMMAND_RPIV_TEMPLATE.md source
- `.claude/commands/shared/sync-docs.md` → COMMAND_VALIDATION_TEMPLATE.md source
- `.claude/agents/code-reviewer.md` → AGENT_REVIEWER_TEMPLATE.md source
- `.claude/skills/creating-skills/` → Architecture pattern model

---

## Appendix B: Template Placeholder Reference

### B.1 Command Placeholders

**Common (All Templates):**
- `{{COMMAND_NAME}}` - Kebab-case name (e.g., variance-analysis)
- `{{COMMAND_TITLE}}` - Human-readable title (e.g., Variance Analysis Command)
- `{{ENVIRONMENT}}` - dev | prod | shared
- `{{DESCRIPTION}}` - Help menu description (≤1024 chars)
- `{{ARG_1}}`, `{{ARG_2}}`, `{{ARG_3}}` - Positional arguments

**RPIV-Specific:**
- `{{RESEARCH_STEP_1}}...{{RESEARCH_STEP_N}}` - Research phase steps
- `{{PLAN_COMPONENT_1}}...{{PLAN_COMPONENT_N}}` - Plan phase components
- `{{IMPLEMENT_TASK_1}}...{{IMPLEMENT_TASK_N}}` - Implementation tasks
- `{{VERIFY_CRITERION_1}}...{{VERIFY_CRITERION_N}}` - Verification criteria

**Human Approval-Specific:**
- `{{ACTION}}` - What will happen (e.g., "Deploy backend v1.2.3")
- `{{IMPACT}}` - Who/what affected (e.g., "10,000 users")
- `{{RISK_LEVEL}}` - high | medium | low
- `{{REVERSIBLE}}` - true | false
- `{{URGENCY}}` - high | medium | low

**Reflection-Specific:**
- `{{QUALITY_CRITERIA}}` - Dimensions to evaluate (Accuracy, Completeness, Clarity, etc.)
- `{{MAX_ITERATIONS}}` - Maximum refinement loops (default: 3)
- `{{QUALITY_THRESHOLD}}` - Stop when all dimensions ≥ threshold (default: 8/10)

**Routing-Specific:**
- `{{DOMAIN_1}}...{{DOMAIN_N}}` - Classification domains (finance, legal, technical, etc.)
- `{{COMPLEXITY_LEVEL}}` - simple | moderate | complex
- `{{HANDLER_1}}...{{HANDLER_N}}` - @agent-name or /command-name to route to

---

### B.2 Agent Placeholders

**Common (All Templates):**
- `{{AGENT_NAME}}` - Kebab-case name (e.g., code-reviewer)
- `{{AGENT_TITLE}}` - Human-readable title (e.g., Code Reviewer)
- `{{ROLE_DESCRIPTION}}` - "You are a senior..." (1-2 paragraphs)
- `{{DOMAIN}}` - Expertise domain (financial systems, Python, etc.)
- `{{TOOL_TIER}}` - read-only | read+web | full (auto-assigned by template type)

**Domain Specialist-Specific:**
- `{{AREA_1_NAME}}...{{AREA_15_NAME}}` - Domain areas (8-15 total)
- `{{AREA_1_BULLETS}}...{{AREA_15_BULLETS}}` - Bullets per area (8-12 each)
- `{{CHECKLIST_1}}...{{CHECKLIST_8}}` - Verification checklist (8 items)

**Researcher-Specific:**
- `{{RESEARCH_FOCUS}}` - Focus area (competitive intelligence, market analysis, etc.)
- `{{QUERY_1}}...{{QUERY_N}}` - Investigation queries
- `{{SOURCE_TYPES}}` - Types of sources to search (web, docs, code, etc.)

**Reviewer-Specific:**
- `{{CHECK_1_NAME}}...{{CHECK_8_NAME}}` - Verification checks (8 items)
- `{{OUTPUT_FORMAT}}` - CRITICAL/WARNING/SUGGESTION structure
- `{{APPROVAL_CRITERIA}}` - APPROVE/REJECT decision criteria

---

## Appendix C: Research Document Cross-References

**Primary Research:**
- `specs/creating-commands-and-agents/research.md` (2,181 lines)
  - Part 2: Command templates (6 original + 3 new)
  - Part 3: Agent templates (3 validated)
  - Part 11: Optimal prompting patterns (7 guides)

**Validation Addendum:**
- `specs/creating-commands-and-agents/research-validation-addendum.md` (545 lines)
  - Agent template reduction (6 → 3)
  - Orchestrator anti-pattern analysis
  - 50+ source validation

**This Document:**
- `specs/creating-commands-and-agents/plan.md` (current)
  - 5-phase implementation roadmap
  - 12 templates + 26 reference guides
  - Orchestrator and validator specifications

---

**END OF PLAN**

**Status:** Ready for implementation (CHECKPOINT 2: User approval before implementation)

**Next Steps:**
1. User reviews plan for approval
2. Begin Phase 1 implementation (Week 1)
3. Iterative development following 5 phases
4. Continuous validation against success criteria
5. Final integration testing and delivery
