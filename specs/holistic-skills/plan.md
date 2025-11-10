# Holistic Meta-Skills - Implementation Plan

**Status:** 🔄 Planning Phase (RPIV Checkpoint 2)
**Created:** 2025-11-10
**Research Complete:** ✅ specs/holistic-skills/research.md (574 lines)
**User Decisions:** ✅ Q1-Q10 documented, Q11-Q20 validated
**Next Phase:** Implementation (after user approval)

---

## Executive Summary

**Objective:** Implement 5 holistic meta-skills that ensure system-wide coherence, context management, and quality enforcement across all .claude components.

**Key Principle:** Meta-Infrastructure First - These skills are tools to build tools, ensuring consistency across all 35 planned components.

**Timeline:** 5 weeks (20-30% faster than sequential via parallelization)
**Dependencies:** 2 BLOCKING (Hook Factory → Financial Quality Gate, Multi-Agent Coordinator → 7 agents)

**Success Criteria:**
- All 5 skills pass System Coherence Validator validation
- CSO scores: Critical skills ≥0.8, others ≥0.7
- Zero regressions in existing 4 meta-skills
- 70%+ context reduction demonstrated via hierarchical CLAUDE.md

---

## Phase 1: Foundation Skills (Week 1)

### 1.1 Hook Factory

**Purpose:** Generate Claude Code hooks following 8 lifecycle patterns with exit code enforcement.

**Priority:** CRITICAL (blocks Financial Quality Gate per Q4 decision)

**Implementation:**

#### File Structure
```
.claude/skills/hook-factory/
├── SKILL.md                          # Main skill (198 lines, ≤200 target)
├── README.md                         # User-facing documentation
├── references/
│   ├── hook-patterns.md              # 8 hook types with exit codes
│   ├── exit-code-contract.md         # Exit 0/2/other behavior
│   ├── dev-hooks.md                  # Development hooks (quality gates)
│   ├── prod-hooks.md                 # Production hooks (FP&A workflows)
│   └── testing-strategies.md         # Hook testing with mock tools
└── templates/
    ├── session-start.sh              # SessionStart template
    ├── pre-tool-use.sh               # PreToolUse BLOCKING template
    ├── post-tool-use.sh              # PostToolUse validation template
    ├── stop.sh                       # Stop session cleanup template
    ├── subagent-stop.sh              # SubagentStop validation template
    ├── user-prompt-submit.sh         # UserPromptSubmit preprocessing template
    ├── pre-compact.sh                # PreCompact context save template
    └── notification.sh               # Notification handler template
```

#### SKILL.md Structure (Target: 198 lines)
```markdown
# Hook Factory

**Type:** Meta-Infrastructure Skill (Tools to Build Tools)
**Discipline:** Code Generation
**Auto-Invoke:** YES (CSO + PostToolUse hook + user override)

## Core Function
Generates Claude Code hooks following 8 lifecycle patterns with exit code contracts.

## When to Use
[Trigger phrases: "create hook", "generate SessionStart", "add validation hook"]
[Symptoms: Needing quality gates, session initialization, tool validation]
[Agnostic keywords: automation, lifecycle, preprocessing, validation]

## Process
1. Identify hook type (SessionStart, PreToolUse, PostToolUse, Stop, SubagentStop, UserPromptSubmit, PreCompact, Notification)
2. Select template from templates/
3. Customize exit code behavior (0 = success, 2 = BLOCKING, other = warning)
4. Generate hook script with proper error handling
5. Validate hook script (syntax, exit codes, error messages)
6. Test hook with mock scenarios

## Exit Code Contract
- Exit 0: Success (stdout visible in transcript)
- Exit 2: BLOCKING error (stderr fed to Claude for fixing)
- Other: Non-blocking warning (user decides)

## References
- [Hook Patterns](references/hook-patterns.md) - 8 hook types detailed
- [Exit Code Contract](references/exit-code-contract.md) - Behavior specifications
- [Dev Hooks](references/dev-hooks.md) - Quality gates, linters, validators
- [Prod Hooks](references/prod-hooks.md) - FP&A workflow hooks
- [Testing Strategies](references/testing-strategies.md) - Mock tools and scenarios

## Examples
[4-5 examples showing different hook types and exit codes]

## CSO Optimization
**Target Score:** ≥0.8 (Critical skill)
- Trigger Phrases: 10+ variations (0.9)
- Symptoms: 8+ scenarios (0.85)
- Agnostic Keywords: 15+ terms (0.75)
- Examples: 5 examples (0.7)
**Weighted Average:** 0.81
```

#### Templates (8 files)
Each template includes:
- Shebang and error handling setup
- Exit code constants (SUCCESS=0, BLOCKING=2)
- Parameter validation
- Core logic placeholder with comments
- Error message formatting (stderr for exit 2)
- Exit code usage examples

**Example: templates/pre-tool-use.sh**
```bash
#!/bin/bash
# PreToolUse Hook - BLOCKING validation before tool execution
# Exit 0 = Allow tool execution
# Exit 2 = Block tool execution (stderr fed to Claude)
# Other = Warning (user decides)

set -euo pipefail

# Exit codes
readonly SUCCESS=0
readonly BLOCKING_ERROR=2

# Hook parameters (provided by Claude Code)
TOOL_NAME="${1:-}"
TOOL_PARAMS="${2:-}"

# Validation logic
if [[ -z "$TOOL_NAME" ]]; then
  echo "ERROR: Tool name not provided" >&2
  exit "$BLOCKING_ERROR"
fi

# TODO: Add validation logic here
# Example: Block Write tool on read-only files
# Example: Validate Bash commands against allowed list
# Example: Check file permissions before Edit

# Success
exit "$SUCCESS"
```

#### references/hook-patterns.md (300-400 lines)
- Complete documentation of 8 hook types
- Use cases for each hook (dev vs prod)
- Exit code behavior with examples
- Integration with Claude Code lifecycle
- Common patterns and anti-patterns

#### references/dev-hooks.md (200-300 lines)
- Quality gates (decimal precision checker, audit trail validator)
- Linters and formatters (ruff, mypy, pre-commit integration)
- Git workflow hooks (commit message validation, branch name checks)
- Testing hooks (pytest before push, coverage thresholds)

#### references/prod-hooks.md (200-300 lines)
- FP&A workflow hooks (variance analysis preprocessing)
- Data extraction hooks (validate credentials before Databricks query)
- Report generation hooks (check thresholds before formatting)
- Audit trail hooks (log all data transformations)

#### Testing Strategy
1. **Syntax validation:** Shellcheck on all templates
2. **Mock scenarios:** Test exit codes with mock tool calls
3. **Integration tests:** Test hooks in actual Claude Code session (dev environment)
4. **Documentation validation:** Verify references/ link correctly from SKILL.md

#### Success Metrics
- ✅ 8 templates generate valid hooks
- ✅ CSO score ≥0.8
- ✅ All references/ documents <500 lines each
- ✅ Zero syntax errors in generated hooks
- ✅ Exit codes behave as specified

---

### 1.2 Hierarchical Context Manager

**Purpose:** Manage cascading CLAUDE.md configuration (root + subdirectory overrides) with token estimation.

**Priority:** HIGH (enables context reduction for all future work)

**Implementation:**

#### File Structure
```
.claude/skills/hierarchical-context-manager/
├── SKILL.md                          # Main skill (195 lines, ≤200 target)
├── README.md                         # Migration guide for users
├── references/
│   ├── migration-strategy.md         # Root vs subdirectory content
│   ├── token-estimation.md           # ~4 chars/token rule of thumb
│   ├── cascading-rules.md            # Override precedence
│   └── maintenance-patterns.md       # Keep CLAUDE.md files in sync
└── templates/
    ├── root-claude.md.template       # Orchestration and cross-cutting concerns
    ├── scripts-claude.md.template    # Python scripts behavior overrides
    ├── claude-dir-claude.md.template # .claude components behavior
    └── tests-claude.md.template      # Testing behavior overrides
```

#### SKILL.md Structure (Target: 195 lines)
```markdown
# Hierarchical Context Manager

**Type:** Meta-Infrastructure Skill (Tools to Build Tools)
**Technique:** Context Optimization
**Auto-Invoke:** YES (CSO + user override)

## Core Function
Manages cascading CLAUDE.md configuration with root orchestration + subdirectory overrides.

## When to Use
[Trigger phrases: "migrate CLAUDE.md", "reduce context", "hierarchical config"]
[Symptoms: Token limits reached, repetitive instructions, context bloat]
[Agnostic keywords: configuration, context window, progressive disclosure]

## Process
1. Analyze current CLAUDE.md size (estimate tokens via ~4 chars/token)
2. Identify component-specific vs cross-cutting concerns
3. Generate root CLAUDE.md (orchestration, anti-hallucination, financial precision)
4. Generate subdirectory CLAUDE.md files (component-specific overrides)
5. Validate cascading precedence (most nested wins)
6. Measure token reduction (compare before/after)

## Cascading Rules
- Root CLAUDE.md: Orchestration, verification, financial precision, RPIV workflow
- Subdirectory CLAUDE.md: Component-specific overrides (e.g., scripts/core/CLAUDE.md for core logic)
- Precedence: Most nested configuration wins for conflicts

## Token Estimation
**Rule of Thumb:** ~4 characters per token
**Example:** 2000 characters ≈ 500 tokens

## References
- [Migration Strategy](references/migration-strategy.md) - What goes where
- [Token Estimation](references/token-estimation.md) - Measurement techniques
- [Cascading Rules](references/cascading-rules.md) - Override precedence
- [Maintenance Patterns](references/maintenance-patterns.md) - Keep configs in sync

## Examples
[4-5 examples showing root vs subdirectory content, token reduction calculations]

## CSO Optimization
**Target Score:** ≥0.7 (High priority)
- Trigger Phrases: 8+ variations (0.85)
- Symptoms: 6+ scenarios (0.7)
- Agnostic Keywords: 12+ terms (0.65)
- Examples: 4 examples (0.6)
**Weighted Average:** 0.70
```

#### Templates (4 files)

**root-claude.md.template** - Orchestration layer
- Anti-hallucination protocol (chain of verification)
- Financial precision mandates (Decimal, audit trails)
- RPIV workflow enforcement
- Meta-infrastructure first principle
- Response format requirements (conciseness, verification)

**scripts-claude.md.template** - Python scripts overrides
- Type safety enforcement (mypy strict mode)
- Decimal precision for all currency calculations
- Audit trail logging requirements
- Performance considerations (chunking for >1000 rows)

**claude-dir-claude.md.template** - .claude components
- CSO optimization requirements
- Progressive disclosure (SKILL.md ≤200 lines + references/)
- Template validation (YAML frontmatter, naming conventions)
- Tool tier enforcement for agents

**tests-claude.md.template** - Testing overrides
- Edge case coverage requirements
- Financial precision test cases
- Integration test patterns
- Regression test expectations

#### references/migration-strategy.md (400-500 lines)
- Complete analysis of current root CLAUDE.md (identify sections)
- Decision tree: Which sections stay in root vs move to subdirectories
- Migration checklist (what to move, what to keep, what to delete)
- Before/after token comparison methodology

#### references/token-estimation.md (200-300 lines)
- Character-to-token rule of thumb (~4 chars/token)
- Edge cases (code blocks, JSON, lists)
- Measurement tools (wc -m for characters)
- Evidence from claude-code-skill-factory (70-77% reduction)

#### references/cascading-rules.md (200-300 lines)
- Precedence algorithm (most nested wins)
- Conflict resolution examples
- Override vs append behavior
- Testing cascading behavior

#### references/maintenance-patterns.md (200-300 lines)
- When to update root vs subdirectory
- Cross-cutting concern changes (propagate to all)
- Component-specific changes (subdirectory only)
- Validation: Ensure no contradictions across hierarchy

#### Testing Strategy
1. **Token measurement:** Measure current root CLAUDE.md tokens
2. **Migration test:** Create subdirectory CLAUDE.md files, measure reduction
3. **Precedence test:** Test cascading behavior with conflicting instructions
4. **Validation test:** Ensure no contradictions across hierarchy

#### Success Metrics
- ✅ 70%+ token reduction demonstrated (target: root CLAUDE.md from ~2000 lines to <600)
- ✅ CSO score ≥0.7
- ✅ 4 templates cover all use cases
- ✅ Cascading behavior tested and documented
- ✅ Migration guide enables user self-service

---

## Phase 2: Validation Skills (Week 2)

### 2.1 System Coherence Validator

**Purpose:** Validate consistency across all .claude components (skills, agents, commands) using 15 validation rules.

**Priority:** CRITICAL (validates all other work)

**Implementation:**

#### File Structure
```
.claude/skills/system-coherence-validator/
├── SKILL.md                          # Main skill (200 lines, ≤200 target)
├── README.md                         # User-facing validation guide
├── references/
│   ├── validation-rules.md           # 15 validation rules detailed
│   ├── retroactive-validation.md     # How to validate existing components
│   ├── continuous-validation.md      # Integration with hooks (Q1 decision)
│   └── error-reporting.md            # User-friendly error messages
├── validators/
│   ├── yaml-validator.py             # YAML frontmatter validation
│   ├── cso-scorer.py                 # CSO score calculation (Q13 tiered)
│   ├── naming-validator.py           # File naming conventions
│   ├── structure-validator.py        # Directory structure checks
│   ├── cross-reference-validator.py  # Links between components
│   └── integration-validator.py      # Component interaction checks
└── templates/
    └── validation-report.md.template # Structured validation report
```

#### SKILL.md Structure (Target: 200 lines)
```markdown
# System Coherence Validator

**Type:** Meta-Infrastructure Skill (Tools to Build Tools)
**Discipline:** Quality Assurance
**Auto-Invoke:** YES (Hybrid: CSO + PostToolUse hook + user override per Q15)

## Core Function
Validates consistency across all .claude components using 15 validation rules.

## When to Use
[Trigger phrases: "validate system", "check coherence", "run validation"]
[Symptoms: Inconsistencies, broken links, missing references/, low CSO scores]
[Agnostic keywords: quality gate, consistency check, integration validation]

## Process
1. Scan all .claude components (skills, agents, commands)
2. Run 15 validation rules (see references/validation-rules.md)
3. Calculate CSO scores with tiered thresholds (Q13 decision)
4. Check cross-references and links
5. Validate integration points
6. Generate validation report with actionable fixes

## Validation Scope
- ✅ Existing components (retroactive per Q2 decision)
- ✅ New components (continuous per Q1 decision)
- ✅ After creation via creating-* skills (PostToolUse hook per Q5 decision)
- ✅ Manual invocation (user override always available)

## Tiered CSO Thresholds (Q13 Evidence-Based)
- **Critical skills:** ≥0.8 (Hook Factory, Financial Quality Gate)
- **High priority:** ≥0.7 (Context Manager, System Coherence Validator, Multi-Agent Coordinator)
- **Rationale:** Only 25% of existing meta-skills meet 0.8 threshold

## Bootstrap Solution (Q12 Decision)
- **Phase 1:** Validator created using creating-skills' existing 5 validators
- **Phase 2:** After validator exists, it validates itself + retroactively validates first 3 skills

## References
- [Validation Rules](references/validation-rules.md) - 15 rules detailed
- [Retroactive Validation](references/retroactive-validation.md) - Existing component checks
- [Continuous Validation](references/continuous-validation.md) - Hook integration
- [Error Reporting](references/error-reporting.md) - User-friendly messages

## Examples
[4-5 examples showing validation failures and fixes]

## CSO Optimization
**Target Score:** ≥0.7 (High priority)
- Trigger Phrases: 8+ variations (0.8)
- Symptoms: 7+ scenarios (0.75)
- Agnostic Keywords: 12+ terms (0.65)
- Examples: 4 examples (0.6)
**Weighted Average:** 0.70
```

#### validators/ (6 Python scripts)

**yaml-validator.py**
```python
#!/usr/bin/env python3
"""YAML frontmatter validation for skills, agents, commands."""

from pathlib import Path
from typing import List, Dict, Any
import yaml

def validate_skill_frontmatter(file_path: Path) -> Dict[str, Any]:
    """Validate SKILL.md YAML frontmatter.

    Required fields:
    - name: str
    - type: Literal['Discipline', 'Technique', 'Pattern', 'Reference']
    - auto_invoke: bool
    - cso_score: float (≥0.7 or ≥0.8 depending on tier)
    """
    # Implementation
    pass

def validate_agent_frontmatter(file_path: Path) -> Dict[str, Any]:
    """Validate agent .md YAML frontmatter.

    Required fields:
    - name: str
    - tool_tier: Literal['read_only', 'read_web', 'full_access']
    - description: str
    """
    # Implementation
    pass

def validate_command_frontmatter(file_path: Path) -> Dict[str, Any]:
    """Validate command .md YAML frontmatter.

    Required fields:
    - name: str
    - workflow_type: Literal['RPIV', 'Human Approval', ...]
    - description: str
    """
    # Implementation
    pass
```

**cso-scorer.py** - Calculate CSO scores using 4-pillar framework
**naming-validator.py** - Check file naming conventions (kebab-case, .md extension)
**structure-validator.py** - Verify directory structure (SKILL.md + references/ + templates/)
**cross-reference-validator.py** - Validate links between components work
**integration-validator.py** - Check component interactions (e.g., commands invoke agents correctly)

#### references/validation-rules.md (500-600 lines)
15 validation rules documented:
1. YAML frontmatter completeness
2. CSO score thresholds (tiered)
3. File naming conventions
4. Directory structure requirements
5. References/ document existence
6. Progressive disclosure (SKILL.md ≤200 lines)
7. Cross-references resolve correctly
8. Tool tier enforcement for agents
9. Workflow type correctness for commands
10. Template validity
11. No duplication across components
12. Integration points tested
13. Documentation completeness
14. Example quality (4-5 examples minimum)
15. No broken links

#### references/continuous-validation.md (300-400 lines)
- Integration with PostToolUse hook (Q5 decision)
- Auto-invoke after Write/Edit on .claude/ files
- User override mechanism
- Error reporting in Claude transcript

#### references/retroactive-validation.md (200-300 lines)
- How to validate 4 existing meta-skills
- Batch validation script
- Prioritization (fix critical issues first)
- Validation report generation

#### Testing Strategy
1. **Self-validation:** Run validator on itself (bootstrap test)
2. **Retroactive validation:** Run on 4 existing meta-skills
3. **New component validation:** Test on newly created test skill
4. **Integration test:** Verify hook integration works

#### Success Metrics
- ✅ All 15 validation rules implemented
- ✅ CSO score ≥0.7
- ✅ Self-validation passes (bootstrap successful)
- ✅ 4 existing meta-skills validated (issues documented)
- ✅ Hook integration tested

---

### 2.2 Financial Quality Gate

**Purpose:** BLOCKING quality gate for financial precision (Decimal enforcement, audit trails, edge cases).

**Priority:** CRITICAL (ensures financial correctness per spec.md Story 0.1)

**Implementation:**

#### File Structure
```
.claude/skills/financial-quality-gate/
├── SKILL.md                          # Main skill (200 lines, ≤200 target)
├── README.md                         # User-facing quality requirements
├── references/
│   ├── decimal-precision.md          # Why Decimal, not float
│   ├── audit-trail-requirements.md   # Timestamp, source, operation logging
│   ├── edge-cases.md                 # Zero division, NULL, negative values
│   └── testing-standards.md          # Financial test suite requirements
├── validators/
│   ├── decimal-checker.py            # Scan for float usage in currency code
│   ├── audit-trail-checker.py        # Verify logging completeness
│   └── edge-case-tester.py           # Run edge case test suite
└── templates/
    ├── decimal-calculation.py.template   # Correct Decimal usage
    ├── audit-log-entry.py.template       # Structured audit log
    └── edge-case-test.py.template        # Test template with edge cases
```

#### SKILL.md Structure (Target: 200 lines)
```markdown
# Financial Quality Gate

**Type:** Meta-Infrastructure Skill (Tools to Build Tools)
**Discipline:** Quality Assurance
**Auto-Invoke:** YES (BLOCKING via PreToolUse hook per Q4+Q6 decisions)

## Core Function
BLOCKING quality gate enforcing financial precision, audit trails, and edge case coverage.

## When to Use
[Trigger phrases: "financial calculation", "currency code", "variance formula"]
[Symptoms: Float usage, missing audit logs, untested edge cases]
[Agnostic keywords: precision, compliance, SOX, financial data]

## Process
1. Scan code for float usage in currency calculations (BLOCK if found)
2. Verify Decimal type usage with proper rounding
3. Check audit trail completeness (timestamp, source, user, operation)
4. Validate edge case coverage (zero division, NULL, negative values)
5. Run financial precision test suite
6. BLOCK execution if any check fails (exit code 2)

## Financial Precision Requirements
- **Decimal type mandatory** for all currency calculations
- **No float/double** - causes rounding errors (0.1 + 0.2 ≠ 0.3)
- **Rounding:** Only at display/storage layer, NEVER intermediate calculations
- **Audit trails:** Every transformation logged with timestamp, source file, operation

## Edge Cases Tested
- Zero division (budget = 0, handle explicitly)
- Negative values (revenue can be negative in reversals)
- NULL/missing data (flag, don't drop silently)
- Concurrent transactions (locking for multi-user)
- Multi-currency (if applicable)

## Hook Integration (Q4 Decision)
- **PreToolUse hook** invokes this skill before Write/Edit on scripts/core/*.py
- **Exit code 2** if validation fails (BLOCKING)
- **User override** available but requires explicit approval

## References
- [Decimal Precision](references/decimal-precision.md) - Why Decimal, float pitfalls
- [Audit Trail Requirements](references/audit-trail-requirements.md) - SOX compliance
- [Edge Cases](references/edge-cases.md) - Comprehensive test scenarios
- [Testing Standards](references/testing-standards.md) - Financial test suite

## Examples
[4-5 examples showing correct Decimal usage, audit logging, edge case tests]

## CSO Optimization
**Target Score:** ≥0.8 (Critical skill)
- Trigger Phrases: 10+ variations (0.9)
- Symptoms: 8+ scenarios (0.85)
- Agnostic Keywords: 15+ terms (0.8)
- Examples: 5 examples (0.75)
**Weighted Average:** 0.83
```

#### validators/decimal-checker.py
```python
#!/usr/bin/env python3
"""Scan Python code for float usage in currency calculations."""

import ast
from pathlib import Path
from typing import List, Dict, Any

def scan_for_float_usage(file_path: Path) -> List[Dict[str, Any]]:
    """Scan for float usage in currency-related code.

    Detects:
    - float() calls on currency variables
    - Literal floats in calculations (e.g., 0.1 + 0.2)
    - Type hints using float instead of Decimal

    Returns:
        List of violations with line numbers and context
    """
    # Implementation using AST parsing
    pass

def verify_decimal_imports(file_path: Path) -> bool:
    """Verify Decimal is imported from decimal module."""
    # Implementation
    pass

def check_rounding_layer(file_path: Path) -> List[Dict[str, Any]]:
    """Ensure rounding only at display/storage, not intermediate calculations."""
    # Implementation
    pass
```

#### references/decimal-precision.md (400-500 lines)
- Why Decimal mandatory for financial calculations
- Float precision errors demonstrated (0.1 + 0.2 = 0.30000000000000004)
- Decimal usage patterns (import, initialization, arithmetic)
- Rounding strategies (ROUND_HALF_UP for currency)
- Performance considerations (Decimal slower but necessary)

#### references/audit-trail-requirements.md (300-400 lines)
- SOX compliance requirements (7 years retention)
- What to log (timestamp, user, source file, operation, inputs, outputs)
- Structured logging format (JSON preferred)
- Audit log storage location (config/audit.log)
- Search and retrieval patterns

#### references/edge-cases.md (500-600 lines)
- Zero division scenarios (budget = 0, show N/A variance)
- Negative values (revenue reversals, expense credits)
- NULL/missing data (flag as unmatched, don't drop)
- Concurrent transactions (locking strategies)
- Multi-currency (conversion rates, precision)
- Large numbers (billions, ensure no overflow)

#### references/testing-standards.md (400-500 lines)
- Unit test requirements (edge cases mandatory)
- Integration test patterns (realistic data volumes)
- Regression tests (ensure changes don't break accuracy)
- Test data fixtures (representative samples)
- Assertion precision (compare Decimal to 2+ places)

#### Testing Strategy
1. **Decimal scanner test:** Run on known float-using code, verify detection
2. **Audit trail test:** Verify logging completeness on sample transformations
3. **Edge case suite:** Run comprehensive edge case tests
4. **Integration test:** Test PreToolUse hook integration

#### Success Metrics
- ✅ CSO score ≥0.8
- ✅ Zero false positives on Decimal scanner
- ✅ 100% audit trail coverage on test transformations
- ✅ All edge cases tested and documented
- ✅ PreToolUse hook integration tested

---

## Phase 3: Orchestration Skill (Week 3-4)

### 3.1 Multi-Agent Workflow Coordinator

**Purpose:** Orchestrate complex workflows using 7 persistent agents with tool tier enforcement.

**Priority:** HIGH (enables complex FP&A workflows)

**Implementation:**

#### File Structure
```
.claude/skills/multi-agent-workflow-coordinator/
├── SKILL.md                          # Main skill (198 lines, ≤200 target)
├── README.md                         # User-facing workflow guide
├── references/
│   ├── agent-patterns.md             # When to use persistent vs Task()
│   ├── tool-tier-enforcement.md      # Read-only vs full access
│   ├── workflow-orchestration.md     # Coordination patterns
│   └── error-handling.md             # Rollback and retry strategies
└── templates/
    ├── validation-workflow.md.template    # Read-only agent workflow
    ├── generation-workflow.md.template    # Full access agent workflow
    └── hybrid-workflow.md.template        # Mixed agent types
```

#### SKILL.md Structure (Target: 198 lines)
```markdown
# Multi-Agent Workflow Coordinator

**Type:** Meta-Infrastructure Skill (Tools to Build Tools)
**Technique:** Orchestration
**Auto-Invoke:** YES (CSO + user override)

## Core Function
Orchestrates complex workflows using 7 persistent agents with tool tier enforcement.

## When to Use
[Trigger phrases: "orchestrate workflow", "coordinate agents", "multi-step validation"]
[Symptoms: Complex workflows, multiple validation steps, tool restriction needs]
[Agnostic keywords: coordination, workflow, multi-agent, orchestration]

## Process
1. Analyze workflow requirements (validation, generation, formatting)
2. Select appropriate agents from 7 pre-defined agents
3. Determine execution order (sequential vs parallel)
4. Invoke agents with proper parameters
5. Aggregate results using Task() for coordination
6. Handle errors with rollback capability

## 7 Pre-Defined Agents (Q5 Decision: Use persistent, not temporary)
**Read-Only Validators:**
1. @databricks-validator - Validate Databricks extraction code
2. @adaptive-validator - Validate Adaptive Insights integration
3. @report-formatter - Validate report structure and formatting
4. @slides-previewer - Preview slides before generation
5. @script-validator - Validate Python scripts for quality

**Full Access Generators:**
6. @script-generator - Generate Python scripts
7. @test-generator - Generate test suites

## Agent Selection Criteria (Q5 Research Finding)
- **Tool restrictions required?** → Persistent agent
- **Will be reused?** → Persistent agent
- **Domain expertise needed?** → Persistent agent
- **Financial/security-sensitive?** → Persistent agent
- **Simple one-off task?** → Task() acceptable for coordination

## Coordination Pattern (Hybrid Approach)
- **Persistent agents:** Validation, domain expertise, reusable work
- **Task():** Simple aggregation, one-off calculations, result synthesis

## References
- [Agent Patterns](references/agent-patterns.md) - Persistent vs Task() decision tree
- [Tool Tier Enforcement](references/tool-tier-enforcement.md) - Security boundaries
- [Workflow Orchestration](references/workflow-orchestration.md) - Sequential vs parallel
- [Error Handling](references/error-handling.md) - Rollback strategies

## Examples
[4-5 examples showing different workflow patterns]

## CSO Optimization
**Target Score:** ≥0.7 (High priority)
- Trigger Phrases: 8+ variations (0.8)
- Symptoms: 6+ scenarios (0.7)
- Agnostic Keywords: 12+ terms (0.65)
- Examples: 4 examples (0.6)
**Weighted Average:** 0.69
```

#### References

**references/agent-patterns.md** (400-500 lines)
- Decision tree: When to use persistent agents vs Task()
- Evidence from agent-orchestration-research.md (no temporary agents exist)
- Tool tier justification for each of 7 agents
- Performance considerations (persistent agents have overhead)

**references/tool-tier-enforcement.md** (300-400 lines)
- Read-only tier: Can Read, Glob, Grep, WebFetch only
- Read+Web tier: Read-only + WebSearch
- Full access tier: All tools including Write, Edit, Bash
- Security rationale for validators (read-only prevents accidental modifications)

**references/workflow-orchestration.md** (400-500 lines)
- Sequential workflows (validation → generation → testing)
- Parallel workflows (multiple validators simultaneously)
- Conditional workflows (if validation fails, halt)
- Aggregation patterns (Task() synthesizes agent results)

**references/error-handling.md** (300-400 lines)
- Agent failure scenarios (timeout, validation failure, tool restriction violation)
- Rollback strategies (undo Write operations on failure)
- Retry logic (exponential backoff for network errors)
- User intervention points (approval gates)

#### Testing Strategy
1. **Agent availability:** Verify 7 agents exist before skill complete
2. **Tool tier test:** Verify validators cannot Write/Edit
3. **Orchestration test:** Run multi-step workflow with validation → generation → testing
4. **Error handling test:** Simulate agent failures, verify rollback

#### Success Metrics
- ✅ CSO score ≥0.7
- ✅ 7 persistent agents created and tested
- ✅ Tool tier enforcement verified
- ✅ Orchestration patterns documented with examples
- ✅ Error handling tested with rollback scenarios

---

## Implementation Timeline (5 Weeks with Parallelization)

### Week 1: Foundation (Hook Factory + Context Manager)
**Days 1-3:** Hook Factory (sequential, BLOCKS Financial Quality Gate)
- Day 1: SKILL.md + 8 templates
- Day 2: references/ (4 documents)
- Day 3: Testing + validation

**Days 4-7:** Hierarchical Context Manager (parallel with Hook Factory Days 4-7)
- Day 4: SKILL.md + 4 templates
- Day 5: references/ (4 documents)
- Day 6: Migration of root CLAUDE.md
- Day 7: Testing + token measurement

**Deliverables:**
- ✅ Hook Factory complete with 8 templates
- ✅ Context Manager complete with token reduction demonstrated
- ✅ Root CLAUDE.md migrated (70%+ reduction)

---

### Week 2: Validation (System Coherence Validator + Financial Quality Gate)
**Days 1-4:** System Coherence Validator (sequential with bootstrap dependency)
- Day 1: SKILL.md + validators/ (6 scripts)
- Day 2: references/ (4 documents)
- Day 3: Self-validation (bootstrap test)
- Day 4: Retroactive validation of 4 existing meta-skills

**Days 5-7:** Financial Quality Gate (sequential, depends on Hook Factory)
- Day 5: SKILL.md + validators/ (3 scripts)
- Day 6: references/ (4 documents)
- Day 7: PreToolUse hook integration + testing

**Deliverables:**
- ✅ System Coherence Validator complete with 15 validation rules
- ✅ Bootstrap validation successful
- ✅ Financial Quality Gate complete with PreToolUse hook
- ✅ All existing meta-skills validated

---

### Week 3: Preparation for Orchestration
**Days 1-5:** Create 7 persistent agents (parallel using creating-agents skill)
1. @databricks-validator (read-only)
2. @adaptive-validator (read-only)
3. @report-formatter (read-only)
4. @slides-previewer (read-only)
5. @script-validator (read-only)
6. @script-generator (full access)
7. @test-generator (full access)

**Days 6-7:** Agent validation
- Test tool tier enforcement
- Validate agent YAML frontmatter
- Test agent invocation patterns

**Deliverables:**
- ✅ 7 persistent agents created and validated
- ✅ Tool tier enforcement tested

---

### Week 4: Orchestration (Multi-Agent Workflow Coordinator)
**Days 1-3:** Multi-Agent Workflow Coordinator implementation
- Day 1: SKILL.md + templates/ (3 workflow templates)
- Day 2: references/ (4 documents)
- Day 3: Testing with 7 agents

**Days 4-5:** Integration testing
- Test sequential workflows
- Test parallel workflows
- Test error handling and rollback

**Days 6-7:** Documentation and final validation
- Complete README.md for users
- Generate workflow examples
- Validate CSO score ≥0.7

**Deliverables:**
- ✅ Multi-Agent Workflow Coordinator complete
- ✅ All workflow patterns tested
- ✅ Integration with 7 agents validated

---

### Week 5: Final Validation and Documentation
**Days 1-2:** System-wide validation
- Run System Coherence Validator on all 5 skills
- Run System Coherence Validator on 7 agents
- Verify no regressions in existing 4 meta-skills

**Days 3-4:** Performance measurement
- Measure token reduction (Context Manager)
- Measure CSO scores (all 5 skills)
- Measure validation coverage (System Coherence Validator)

**Days 5-7:** Documentation and handoff
- Update spec.md with Phase 2 completion
- Update plan.md with actual timeline
- Create user guide for 5 new skills
- Document lessons learned

**Deliverables:**
- ✅ All 5 skills validated and documented
- ✅ Performance metrics measured and documented
- ✅ User guides complete
- ✅ Ready for Phase 3 (domain component creation)

---

## Dependency Graph

### BLOCKING Dependencies (Sequential)
1. **Hook Factory → Financial Quality Gate**
   - Financial Quality Gate uses PreToolUse hook (Q4 decision)
   - Must wait for Hook Factory complete
   - **Impact:** Hook Factory must complete before Financial Quality Gate starts

2. **7 Agents → Multi-Agent Workflow Coordinator**
   - Multi-Agent Coordinator orchestrates 7 agents
   - Must wait for agents to exist
   - **Impact:** Agents created in Week 3, Coordinator in Week 4

### Indirect Dependencies (Can Parallelize)
3. **Context Manager || Hook Factory (Week 1 Days 4-7)**
   - No shared dependencies
   - Can work in parallel after Hook Factory Days 1-3

4. **System Coherence Validator || Financial Quality Gate (Week 2)**
   - Validator has bootstrap dependency (uses creating-skills validators)
   - Financial Quality Gate depends on Hook Factory (Week 1 complete)
   - Can overlap Days 1-4 (Validator) with Days 5-7 (Quality Gate)

### No Dependencies (Fully Parallel)
5. **7 Agents (Week 3 Days 1-5)**
   - All agents independent
   - Can create 2-3 agents per day in parallel

---

## Risk Mitigation

### Risk 1: CSO Score Too Low
**Probability:** Medium (only 25% of existing meta-skills meet 0.8)
**Impact:** High (affects auto-invoke reliability)
**Mitigation:**
- Tiered thresholds (critical ≥0.8, others ≥0.7)
- Measure CSO scores during implementation, not after
- Iterate on trigger phrases/symptoms until target met

### Risk 2: Token Reduction Less Than 70%
**Probability:** Low (claude-code-skill-factory demonstrated 70-77%)
**Impact:** Medium (still improves context, but less than expected)
**Mitigation:**
- Measure before/after tokens explicitly
- Identify bloat sections in root CLAUDE.md
- Move more content to subdirectories if needed

### Risk 3: Bootstrap Paradox Unresolved
**Probability:** Low (creating-skills has 5 validators)
**Impact:** High (blocks System Coherence Validator)
**Mitigation:**
- Use creating-skills' existing validators for Phase 1
- Self-validate in Phase 2 (validator validates itself)
- Retroactive validation as final verification step

### Risk 4: Hook Integration Breaks Existing Workflows
**Probability:** Medium (exit code 2 is BLOCKING)
**Impact:** High (could block legitimate work)
**Mitigation:**
- Test hooks in dev environment first (.claude/environments/dev/)
- User override mechanism always available
- Clear error messages (stderr) for fixing

### Risk 5: 7 Agents Creation Takes Longer Than Week 3
**Probability:** Low (creating-agents skill exists)
**Impact:** Medium (delays Week 4 orchestration)
**Mitigation:**
- Parallelize agent creation (2-3 agents per day)
- Prioritize validators (read-only, simpler)
- Defer generators if time constrained

---

## Success Criteria (Exit Criteria for Phase 2)

### Functional Requirements
- ✅ All 5 skills complete with SKILL.md + references/ + templates/
- ✅ All 7 agents created with proper tool tier enforcement
- ✅ Hook Factory generates valid hooks for all 8 types
- ✅ Hierarchical Context Manager demonstrates 70%+ token reduction
- ✅ System Coherence Validator validates all components (self + retroactive)
- ✅ Financial Quality Gate blocks float usage in currency code
- ✅ Multi-Agent Workflow Coordinator orchestrates 7 agents successfully

### Quality Requirements
- ✅ CSO scores: Critical skills ≥0.8, others ≥0.7
- ✅ All skills pass System Coherence Validator (15 validation rules)
- ✅ Zero regressions in existing 4 meta-skills
- ✅ All references/ documents <600 lines each (progressive disclosure)
- ✅ SKILL.md files ≤200 lines (target: 195-200)

### Testing Requirements
- ✅ Bootstrap validation successful (validator validates itself)
- ✅ Retroactive validation complete (4 existing meta-skills + 5 new skills)
- ✅ Hook integration tested (dev environment)
- ✅ Agent tool tier enforcement tested (read-only cannot Write)
- ✅ Orchestration tested (sequential, parallel, error handling)

### Documentation Requirements
- ✅ User guides complete (README.md for each skill)
- ✅ Migration guide for Hierarchical Context Manager
- ✅ Validation report from System Coherence Validator
- ✅ Performance metrics documented (token reduction, CSO scores)

### Approval Requirements
- ✅ User reviews and approves Phase 2 completion
- ✅ User approves proceeding to Phase 3 (domain component creation)
- ✅ Lessons learned documented for future phases

---

## Next Steps After Plan Approval

1. **User reviews this plan** (RPIV Checkpoint 2)
2. **User approves plan** → Proceed to Implementation Phase
3. **Create checklist.md** → Track RPIV progress
4. **Week 1 Day 1:** Begin Hook Factory implementation
5. **Weekly check-ins:** Review progress, adjust timeline as needed
6. **Week 5 Day 7:** Final validation and user approval for Phase 3

---

## References

- **Research:** specs/holistic-skills/research.md (574 lines, all user decisions)
- **User Decisions:** Q1-Q10 in research.md, Q11-Q20 validated in Q11-Q15-CRITICAL-ANALYSIS.md
- **Dependency Analysis:** specs/holistic-skills/dependency-graph.md
- **Evidence:** Q11-Q15-CRITICAL-ANALYSIS.md (68KB, measured CSO scores, timing analysis)
- **Hook Research:** specs/claude-code-hooks-research.md (2,605 lines, 18 sources)
- **Agent Research:** specs/holistic-skills/agent-orchestration-research.md (1000+ lines)

---

**END OF PLAN**

**Status:** 🔄 Awaiting User Approval (RPIV Checkpoint 2)
**Next Action:** User reviews and approves → Create checklist.md → Begin Week 1 Implementation
