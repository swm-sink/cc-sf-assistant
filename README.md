# FP&A Automation Assistant

**Version:** 1.1-DRAFT
**Status:** 🚧 Development Phase
**Approach:** Spec-Driven Development with Agentic Workflows

---

## Project Overview

Intelligent automation assistant for Financial Planning & Analysis (FP&A) professionals. Eliminates repetitive data collection/consolidation tasks, enabling strategic analysis capacity.

**Research Context:** FP&A professionals spend only 35% of time on high-value tasks. This project automates the 60%+ of activities that can be automated. [Source: FP&A Trends Survey 2024, spec.md]

---

## Architecture (Anthropic Best Practices)

This project follows Anthropic's recommended separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     CLAUDE.md                               │
│  Behavioral Rules & Quality Gates (245 lines)               │
│  - Chain of Verification protocol                           │
│  - Financial precision mandates                             │
│  - Pre-response checklist                                   │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Skills     │   │  Commands    │   │   Agents     │
│ (Auto-invoke)│   │  (Manual)    │   │ (Subagents)  │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────────────────────────────────────────────┐
│              Hooks (Quality Gates)                   │
│  Run at end-of-turn, enforce standards              │
└──────────────────────────────────────────────────────┘
```

---

## Component Responsibilities

### 1. CLAUDE.md (Behavioral Configuration)

**Purpose:** Define HOW Claude operates (not WHAT to build)

**Contains:**
- DRY principle enforcement
- Chain of Verification protocol (4-step anti-hallucination)
- Critical thinking mandate (skeptical analyst vs yes-man)
- Financial precision requirements (Decimal only, audit trails)
- Pre-response quality gate checklist
- Extreme conciseness defaults

**Does NOT contain:**
- Business requirements (→ spec.md)
- Comprehensive test suites (→ Skills)
- Implementation workflows (→ Commands)

**Line count:** 245 lines (target: <250 per Anthropic guidance)

---

### 2. Skills (.claude/skills/)

**Purpose:** Auto-invoked capabilities based on description matching

**Progressive Disclosure Pattern:**
1. Name + description loaded at startup
2. SKILL.md loaded when needed
3. References loaded on-demand

**Current Skills:**

#### financial-validator/
- **Triggers:** Excel files, variance calculations, data validation
- **Provides:** Edge case tests, precision validation, audit compliance
- **Structure:**
  - `SKILL.md` - Core validation guidance
  - `references/edge-cases.md` - Comprehensive test suite (10 categories)
  - `scripts/validate_precision.py` - Executable validation

**Benefit:** Keeps CLAUDE.md concise while providing deep domain expertise when triggered.

---

### 3. Commands (.claude/commands/)

**Purpose:** Manual slash commands for human-in-loop workflows

**Current Commands:**

#### /variance-analysis
- **Usage:** `/variance-analysis <budget> <actual> [output]`
- **Workflow:** Research → Plan → Implement → Verify (with checkpoints)
- **Human Checkpoints:**
  1. After research findings
  2. After plan approval
  3. During implementation phases
  4. After verification results
- **Enforces:** Spec-driven development, no shortcuts

**Benefit:** Structured workflows with human oversight at critical decision points.

---

### 4. Agents (.claude/agents/)

**Purpose:** Specialized subagents with separate context windows

**Current Agents:**

#### code-reviewer
- **Tools:** Read-only (Read, Grep, Glob)
- **Mission:** Independent verification, find bugs before merge
- **Specialty:** Financial precision, edge cases, Decimal validation
- **Mindset:** Skeptical senior engineer (assume bugs until proven otherwise)

**Benefit:** Context isolation prevents bias, enables ruthlessly honest review.

---

### 5. Hooks (.claude/hooks/)

**Purpose:** Automated quality gates that run without model memory

**Current Hooks:**

#### stop.sh (End-of-Turn)
- **Triggers:** After each Claude Code response
- **Checks:**
  - Float usage in financial code (BLOCKING)
  - Type hints on functions (WARNING)
  - Financial validator tests (if available)
  - Python syntax (BLOCKING)
  - CLAUDE.md line count (WARNING)
- **Exit Codes:**
  - 0 = Pass
  - 2 = Blocking error (Claude must fix)

**Benefit:** Enforces standards automatically, catches issues before commit.

---

## Key Files & Single Source of Truth

```
├── spec.md                    # WHAT to build (business requirements)
├── CLAUDE.md                  # HOW Claude operates (behavioral rules)
│
├── .claude/
│   ├── skills/
│   │   └── financial-validator/
│   │       ├── SKILL.md
│   │       ├── references/edge-cases.md
│   │       └── scripts/validate_precision.py
│   ├── commands/
│   │   └── variance-analysis.md
│   ├── agents/
│   │   └── code-reviewer.md
│   └── hooks/
│       └── stop.sh
│
├── src/                       # Implementation (future)
├── tests/                     # Test suite (future)
└── README.md                  # This file
```

**Hierarchy:** Claude prioritizes most nested config when multiple CLAUDE.md files exist.

---

## Development Workflow

### Research → Plan → Implement → Verify

Following Anthropic's agentic pattern:

**1. Research Phase (No Coding)**
- Use subagents for investigation
- Read files, understand context
- Document findings before proceeding

**2. Plan Phase (Specification)**
- Generate formal spec document
- Define inputs, outputs, validation
- Get human approval before implementation
- Specs are source of truth, code is derived

**3. Implement Phase (Checkpoints)**
- Break into logical tasks
- Progress tracker table
- Human approval at each checkpoint
- Update tracker after each task

**4. Verify Phase (Independent)**
- Run tests against specification
- Use subagents for verification
- Ensure no overfitting
- Human final review before commit

---

## Quality Gates (Enforced)

**Pre-Response Checklist (Every Response):**

| Check | Criteria | Action if Fail |
|-------|----------|----------------|
| DRY | No spec.md duplication | Reference instead |
| Source | Has citation or [TO BE MEASURED] | Add marker |
| Precision | Decimal for currency | Reject float |
| Audit | Logged transformation | Add logging |
| Critical | Assumption challenged | Re-analyze |
| Concise | ≤3 sentences default | Trim |

**Auto-reject response if ANY check fails.**

**End-of-Turn Hook (Automated):**
- Float usage in src/ → BLOCKING ERROR
- Missing type hints → WARNING
- Syntax errors → BLOCKING ERROR
- CLAUDE.md >300 lines → WARNING

---

## Financial Domain Mandates

### Decimal Precision (NON-NEGOTIABLE)

```python
# ✅ CORRECT
from decimal import Decimal
budget = Decimal('100000.00')
actual = Decimal('115000.00')
variance = actual - budget  # Exact: Decimal('15000.00')

# ❌ INCORRECT - WILL BE REJECTED BY HOOKS
budget = 100000.00  # float
variance = 0.1 + 0.2  # 0.30000000000000004 (precision error)
```

### Audit Trail (REQUIRED)

Every transformation must log:
- Timestamp (ISO 8601)
- User/process
- Source file(s)
- Operation performed
- Generation metadata

### Edge Cases (COMPREHENSIVE)

See `.claude/skills/financial-validator/references/edge-cases.md` for:
1. Float precision errors
2. Division by zero
3. Negative values
4. NULL/missing data
5. Concurrent transactions
6. Multi-currency
7. Rounding precision
8. Boundary conditions
9. Data type mismatches
10. Large numbers/overflow

---

## Quick Start

### Using Claude Code

```bash
# Run variance analysis (human-in-loop)
/variance-analysis budget.xlsx actuals.xlsx output.xlsx

# Validate precision (auto-invoked when working with financials)
# financial-validator skill activates automatically

# Request code review (independent verification)
@code-reviewer Please verify variance calculation in src/core/
```

### Running Validation Locally

```bash
# Run financial precision tests
python .claude/skills/financial-validator/scripts/validate_precision.py

# Run quality gates manually
.claude/hooks/stop.sh
```

---

## Success Metrics

**For Claude's Performance:**
- ✅ Zero hallucinated claims (all cited or marked [TO BE MEASURED])
- ✅ Zero float usage in currency calculations
- ✅ Every response passes pre-response checklist
- ✅ Concise by default, detailed on request
- ✅ Critical thinking demonstrated

**For Project Outcomes:**
- [TO BE MEASURED] Baseline time for manual processes
- [TO BE MEASURED] Time reduction with automation
- [TO BE MEASURED] Error reduction vs manual workflows
- Expected: 20-30% less time on data processing [Source: McKinsey AI research, spec.md]

---

## Research Basis

This architecture implements:
- **Chain of Verification** (Meta AI Research 2023) - Anti-hallucination
- **Self-Consistency** principles - Multiple reasoning paths
- **Critical Thinking** frameworks - Avoid sycophancy
- **Financial Testing Standards** (2024-2025) - Precision requirements
- **Anthropic Best Practices** (2025) - Claude Code architecture patterns

See `spec.md` appendix for comprehensive research sources.

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-08 | Initial repository setup with architecture |

---

## Next Steps

1. Review and approve spec.md (resolve [NEEDS CLARIFICATION] items)
2. Implement Priority Epic 1: Monthly Close Automation
3. Create unit tests following TDD approach
4. Build CI/CD pipeline with quality gates

---

**Maintained by:** Claude Code with human oversight
**License:** [TO BE DETERMINED]
**Contact:** [TO BE ADDED]
