# FP&A Automation Assistant

**Version:** 0.2.0-DEV
**Status:** 🏗️ Development Phase - Documentation Complete
**Platform:** Claude Code-Native Architecture
**Deployment:** Single-User, Local Setup

---

## Project Overview

Claude Code-based automation assistant for Financial Planning & Analysis (FP&A) professionals. Automates repetitive data consolidation, variance analysis, and reporting workflows through conversational commands and Python scripts.

**Key Insight:** FP&A professionals spend 60%+ of time on manual data tasks. This project automates those tasks, enabling focus on strategic analysis.

**Source:** FP&A Trends Survey 2024 (referenced in spec.md)

---

## Architecture

**Claude Code-Native:** Built as skills, commands, and agents for Claude Code - not traditional Python packages.

**Environment Split:**
- **Dev workflows** - Generate new scripts when needed (`/dev:create-script`)
- **Prod workflows** - Execute pre-written validated scripts (`/prod:variance-analysis`)
- **Shared utilities** - Quality enforcement (Decimal precision, audit trails)

### Directory Structure

```
cc-sf-assistant/
├── spec.md                  # Business requirements (WHAT to build)
├── plan.md                  # Technical planning (HOW to build)
├── CLAUDE.md                # AI behavioral rules
├── README.md                # This file
├── pyproject.toml           # Python dependencies
│
├── .claude/                 # Claude Code configuration
│   ├── agents/
│   │   ├── dev/            # script-generator, script-validator, code-reviewer
│   │   ├── prod/           # finance-reviewer, data-validator, reconciler
│   │   └── shared/         # research-agent
│   ├── skills/             # Skills with embedded workflows
│   │   ├── dev/            # Development skills
│   │   │   └── {skill-name}/
│   │   │       ├── SKILL.md          # Main skill file
│   │   │       ├── workflows/        # Commands/workflows
│   │   │       └── context/          # Progressive disclosure
│   │   ├── prod/           # Production skills
│   │   │   └── variance-analyzer/
│   │   │       ├── SKILL.md          # Variance analysis skill
│   │   │       └── workflows/
│   │   │           └── variance-analysis.md
│   │   └── shared/         # Shared utilities
│   │       └── workflows/
│   │           └── sync-docs.md
│   ├── templates/          # Templates for creating skills/commands/agents
│   └── hooks/              # Quality gates (pre-commit, stop.sh)
│
├── scripts/                # Pre-written validated calculation scripts
│   ├── core/              # variance.py, consolidation.py, favorability.py
│   ├── integrations/      # gsheet_reader.py, excel_writer.py
│   ├── workflows/         # monthly_close.py, variance_report.py
│   └── utils/             # logger.py, validator.py, config_loader.py
│
├── external/              # Cloned GitHub repos (git submodules)
│   ├── humanlayer/        # Human-in-loop patterns (reference)
│   ├── gspread/           # Google Sheets API (install via pip)
│   ├── slidio/            # Google Slides patterns (reference)
│   ├── pyfpa/             # FP&A algorithms (reference)
│   └── py-money/          # Decimal precision (reference)
│
├── data/                  # Sample data for testing
│   └── samples/           # Realistic budget/actuals files (version controlled)
│
├── templates/             # Report templates
│   ├── variance_report.xlsx
│   ├── board_deck.pptx
│   └── life360/           # Life360-branded templates (Phase 6)
│
├── docs/                  # Documentation
│   ├── notebooks/         # Jupyter notebook tutorials
│   ├── user-guides/       # Markdown guides
│   └── COMPREHENSIVE_GITHUB_SOURCES.md  # Research results
│
├── config/                # Configuration
│   ├── settings.yaml      # Non-sensitive settings (version controlled)
│   ├── credentials/       # Google credentials (git ignored)
│   ├── audit.log          # Centralized audit log (git ignored)
│   └── workflow-state/    # Saved workflow progress (git ignored)
│
└── tests/                 # Comprehensive test suite
    ├── test_variance.py
    ├── test_consolidation.py
    └── test_edge_cases.py
```

---

## Quick Start

**See [QUICK_START.md](QUICK_START.md) for complete installation instructions.**

### Installation (Brief)

```bash
# 1. Clone repository
git clone <repository-url>
cd cc-sf-assistant

# 2. Initialize git submodules
git submodule update --init --recursive

# 3. Install dependencies with Poetry
poetry install

# 4. Install pre-commit hooks
poetry run python scripts/utils/install_hooks.py

# 5. Verify setup
poetry run pytest
```

### Using Claude Code

```bash
# Production workflows (execute pre-written scripts)
/prod:variance-analyzer:analyze budget.xlsx actuals.xlsx
/prod:monthly-close november
/prod:consolidate data/departments/

# Development workflows (generate new scripts)
/dev:create-script "Calculate YoY revenue growth by department"
/dev:validate-script scripts/core/yoy_growth.py

# Shared utilities
/shared:help
/shared:sync-docs  # Validate documentation consistency
```

---

## Key Features

### 1. Dev/Prod Workflow Separation

**Dev Workflows:** Generate robust, tested Python scripts on-demand
- Research → Plan (spec) → Implement (TDD) → Verify (independent review) → Approve
- ALL scripts use Decimal for currency (enforced by skills)
- >80% test coverage required (enforced by validation)
- Independent code review by separate agent

**Prod Workflows:** Execute pre-written scripts for daily FP&A tasks
- Data validation pre-checks (human approval)
- Variance analysis, consolidation, board decks
- Error recovery (save state, resume on failure)
- Centralized audit logging

### 2. Financial Precision Guarantees

- **Decimal-only:** Float usage for currency blocked by skills
- **Type safety:** All functions have type hints (enforced by mypy)
- **Audit trails:** Every operation logged with timestamp, user, inputs, outputs
- **Edge cases:** Comprehensive tests for division by zero, negative values, NULL handling

### 3. Human-in-Loop Approval

- Data validation: Review validation report before execution
- Variance review: Approve material variances before export
- Script generation: Approve spec, approve final code
- Workflow resumption: Choose to resume or restart after failures

### 4. Simple Local Setup

- **No Docker:** Python virtual environment via Poetry
- **No cloud:** All processing happens locally
- **Single-user:** Each FP&A professional has independent setup
- **No multi-user complexity:** No authentication, no role-based permissions

### 5. Jupyter Notebook Tutorials

- Executable documentation with sample data
- 7 notebooks covering all workflows
- Users can modify and experiment
- Version-controlled, easy to update

---

## External Dependencies

### Installed via pip:
- **pandas** - Data manipulation
- **gspread + gspread-dataframe** - Google Sheets integration
- **openpyxl** - Read Excel files
- **xlsxwriter** - Write Excel files with formatting
- **loguru** - Audit logging
- **click + rich** - CLI interface

### Cloned for Reference:
- **humanlayer** - Study human-in-loop approval patterns
- **pyfpa** - Study FP&A consolidation algorithms
- **slidio** - Study Google Slides template patterns
- **py-money** - Reference Decimal precision implementation
- **gspread** - Also cloned for security audit before use

---

## Documentation

- **spec.md** - Business requirements (WHAT we're building, WHY)
- **plan.md** - Technical planning (HOW to build, implementation details)
- **CLAUDE.md** - AI behavioral rules (verification protocols, conciseness)
- **QUICK_START.md** - Setup and installation guide
- **EXTERNAL_DEPENDENCIES.md** - Cloned repository documentation
- **docs/COMPREHENSIVE_GITHUB_SOURCES.md** - Research results (200+ repos)
- **docs/notebooks/** - Jupyter notebook tutorials (7 notebooks)

---

## Development Workflow

### Creating a New Script via Dev Workflow

```bash
# 1. Request new analysis
/dev:create-script "Calculate QoQ revenue growth with seasonality adjustment"

# 2. Claude researches existing patterns
# 3. Claude generates formal specification
# 4. Human approves spec

# 5. Claude follows TDD workflow:
#    - RED: Write failing tests
#    - GREEN: Implement using Decimal
#    - REFACTOR: Add docstrings, error handling, logging
#    - VALIDATE: Independent agent review

# 6. Human approves final script
# 7. Script saved to scripts/core/qoq_growth.py
# 8. Script now available for prod workflows
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests for specific module
poetry run pytest tests/test_variance.py

# Run with coverage
poetry run pytest --cov=scripts

# Type check
poetry run mypy scripts/

# Lint
poetry run ruff check scripts/

# Security check
poetry run bandit -r scripts/
```

### Git Workflow

```bash
# All quality checks run automatically before commit (pre-commit hook)
git add scripts/core/variance.py
git commit -m "feat: add QoQ variance to variance.py"

# Pre-commit hook runs:
# ✓ pytest
# ✓ mypy
# ✓ ruff
# ✓ bandit
# ✓ Check for versioned filenames (blocks *_v2.py, etc.)

# Push to remote
git push
```

---

## Success Metrics

**For Script Generation Quality:**
- ✅ 100% of scripts use Decimal for currency (enforced by hooks)
- ✅ 100% of scripts have type hints (enforced by mypy)
- ✅ >80% test coverage on all scripts (enforced by validation)
- ✅ Zero financial calculation errors in production (measured via audit logs)

**For User Experience:**
- [TO BE MEASURED] Time to complete monthly close (baseline vs automated)
- [TO BE MEASURED] User satisfaction with conversational interface
- [TO BE MEASURED] Number of scripts generated on-demand vs pre-written
- [TO BE MEASURED] Accuracy of generated scripts (human review approval rate)

---

## Deployment Model

**Single-User, Local Setup:**
1. User clones repository
2. Follows QUICK_START.md instructions
3. Configures Google credentials manually
4. Customizes for their company (Life360 branding in Phase 6)
5. Independent setup - no shared infrastructure

**Why This Approach:**
- Simple for non-technical FP&A users
- No cloud costs, no authentication complexity
- Each user owns their data and configuration
- Easy to customize and extend

---

## Phase Status

- ✅ **Phase 0:** Spec & Planning Complete
- 🏗️ **Phase 1:** Infrastructure Setup (In Progress)
- ⏳ **Phase 2:** Dev Workflows
- ⏳ **Phase 3:** Core Scripts - Excel
- ⏳ **Phase 4:** Prod Workflows - Excel
- ⏳ **Phase 5:** Google Integration
- ⏳ **Phase 6:** Life360 Branding & Polish

---

## License

[TO BE DETERMINED]

## Contact

[TO BE ADDED]

---

**Maintained by:** Claude Code with human oversight
**Last Updated:** 2025-11-08
