# Restructure Plan: Claude Code-Native Architecture with Dev/Prod Split

**Date:** 2025-11-08
**Status:** Awaiting approval before implementation

---

## Research Summary (10 Sources)

### Key Findings:

1. **Directory Structure Confirmed:**
   - `.claude/skills/` - Skill directories with `SKILL.md` files
   - `.claude/commands/` - Slash command markdown files
   - `.claude/agents/` - Standalone agent markdown files

2. **Subdirectory Support:**
   - Commands support subdirectories: `.claude/commands/dev/monthly-close.md` becomes `/dev:monthly-close`
   - Skills have internal subdirectories: `workflows/`, `scripts/`, `references/`, `context/`
   - Agents are standalone files (not nested in skills)

3. **Settings Hierarchy:**
   - `~/.claude/settings.json` - User-level (all projects)
   - `.claude/settings.json` - Project-level (version controlled)
   - `.claude/settings.local.json` - Personal preferences (not checked in)

4. **CLAUDE.md Hierarchy:**
   - Root `/CLAUDE.md` - General project behavior
   - Subdirectory `/foo/CLAUDE.md` - Loaded on-demand for specific directories
   - Keep under 100-200 lines; link to subdirectory configs if needed

---

## User Requirements Summary

Based on your 5 answers:

1. ✅ **Pre-written scripts** in `scripts/` directory that Claude executes
2. ✅ **Generate new scripts** when none exist: Create spec → Dev workflow → Build → Validate
3. ✅ **Google + Excel** integration required
4. ✅ **Single user** initially (can scale to team later)
5. ✅ **No manual code review** - Scripts must be robust and validated before use
6. ✅ **Offline + Online** capable (Excel local, Google cloud)
7. ✅ **Dev/Prod/Shared** split for skills, commands, agents

---

## Proposed Structure

```
cc-sf-assistant/
├── .claude/
│   ├── agents/
│   │   ├── dev/                          # Development agents
│   │   │   ├── script-generator.md       # Generates Python scripts from specs
│   │   │   ├── script-validator.md       # Validates script correctness
│   │   │   ├── test-generator.md         # Creates comprehensive tests
│   │   │   └── code-reviewer.md          # Reviews generated code
│   │   │
│   │   ├── prod/                         # Production agents
│   │   │   ├── finance-reviewer.md       # Reviews financial outputs
│   │   │   ├── data-validator.md         # Validates input data quality
│   │   │   └── reconciler.md             # Reconciles unmapped accounts
│   │   │
│   │   └── shared/                       # Shared utilities
│   │       └── research-agent.md         # General research tasks
│   │
│   ├── commands/
│   │   ├── dev/                          # Development workflows
│   │   │   ├── create-script.md          # /dev:create-script - Generate new analysis script
│   │   │   ├── validate-script.md        # /dev:validate-script - Run validation suite
│   │   │   ├── test-script.md            # /dev:test-script - Test with sample data
│   │   │   └── review-code.md            # /dev:review-code - Independent code review
│   │   │
│   │   ├── prod/                         # Production workflows
│   │   │   ├── monthly-close.md          # /prod:monthly-close - Monthly close workflow
│   │   │   ├── variance-analysis.md      # /prod:variance-analysis - Variance reporting
│   │   │   ├── consolidate.md            # /prod:consolidate - Multi-dept consolidation
│   │   │   ├── board-deck.md             # /prod:board-deck - Board presentation
│   │   │   └── forecast-update.md        # /prod:forecast-update - Rolling forecast
│   │   │
│   │   └── shared/                       # Shared commands
│   │       ├── help.md                   # /shared:help - System help
│   │       └── config.md                 # /shared:config - Configuration management
│   │
│   ├── skills/
│   │   ├── dev/                          # Development skills (auto-invoked during dev)
│   │   │   ├── python-best-practices/
│   │   │   │   ├── SKILL.md              # Enforces Python best practices
│   │   │   │   └── references/
│   │   │   │       ├── decimal-precision.md
│   │   │   │       ├── type-safety.md
│   │   │   │       └── error-handling.md
│   │   │   │
│   │   │   ├── financial-script-generator/
│   │   │   │   ├── SKILL.md              # Generates financial calculation scripts
│   │   │   │   ├── references/
│   │   │   │   │   ├── variance-patterns.md
│   │   │   │   │   ├── consolidation-patterns.md
│   │   │   │   │   └── favorability-logic.md
│   │   │   │   └── templates/
│   │   │   │       ├── variance.py.template
│   │   │   │       └── consolidation.py.template
│   │   │   │
│   │   │   └── test-suite-generator/
│   │   │       ├── SKILL.md              # Generates comprehensive tests
│   │   │       └── references/
│   │   │           └── edge-cases.md     # (moved from shared)
│   │   │
│   │   ├── prod/                         # Production skills (auto-invoked during prod)
│   │   │   ├── variance-analyzer/
│   │   │   │   ├── SKILL.md              # Auto-invoked for variance tasks
│   │   │   │   └── scripts/
│   │   │   │       └── validate_variance.py
│   │   │   │
│   │   │   ├── account-mapper/
│   │   │   │   ├── SKILL.md              # Auto-invoked for unmapped accounts
│   │   │   │   └── references/
│   │   │   │       └── account-hierarchy.md
│   │   │   │
│   │   │   └── report-generator/
│   │   │       ├── SKILL.md              # Auto-invoked for report generation
│   │   │       └── templates/
│   │   │           ├── variance_report.xlsx
│   │   │           └── board_deck.pptx
│   │   │
│   │   └── shared/                       # Shared skills (auto-invoked always)
│   │       ├── decimal-precision-enforcer/
│   │       │   ├── SKILL.md              # Enforces Decimal for currency
│   │       │   └── scripts/
│   │       │       └── check_float_usage.py
│   │       │
│   │       └── audit-trail-enforcer/
│   │           ├── SKILL.md              # Ensures audit logging
│   │           └── references/
│   │               └── audit-requirements.md
│   │
│   ├── hooks/
│   │   └── stop.sh                       # Quality gate (runs after every response)
│   │
│   ├── settings.json                     # Project settings (version controlled)
│   └── settings.local.json               # Personal settings (not checked in)
│
├── scripts/                              # Pre-written validated calculation scripts
│   ├── core/                             # Core calculations (Decimal precision)
│   │   ├── variance.py                   # Actual - Budget variance
│   │   ├── consolidation.py              # Multi-file Excel consolidation
│   │   ├── favorability.py               # Favorability logic (revenue vs expense)
│   │   └── materiality.py                # Materiality flagging (>10% AND >$50k)
│   │
│   ├── integrations/                     # Google/Excel integrations
│   │   ├── gsheet_reader.py              # Read from Google Sheets
│   │   ├── gsheet_writer.py              # Write to Google Sheets
│   │   ├── excel_reader.py               # Read Excel files (openpyxl)
│   │   ├── excel_writer.py               # Write Excel with formatting (xlsxwriter)
│   │   └── gslides_generator.py          # Google Slides from template
│   │
│   ├── workflows/                        # Workflow orchestration
│   │   ├── monthly_close.py              # Monthly close automation
│   │   ├── variance_report.py            # Variance analysis workflow
│   │   └── board_deck.py                 # Board deck generation
│   │
│   └── utils/                            # Shared utilities
│       ├── logger.py                     # Audit trail logging
│       ├── validator.py                  # Data validation
│       └── config_loader.py              # Configuration management
│
├── external/                             # Cloned GitHub repos (git submodules)
│   ├── humanlayer/                       # Human-in-loop patterns (reference)
│   ├── mcp-gdrive/                       # Google Drive MCP (reference)
│   ├── gspread/                          # Used via pip install
│   ├── slidio/                           # Google Slides templates
│   ├── pyfpa/                            # FP&A patterns (reference)
│   └── py-money/                         # Decimal precision (reference)
│
├── templates/                            # Report templates
│   ├── variance_report.xlsx             # Variance analysis template
│   ├── board_deck.pptx                  # Board presentation template
│   └── consolidated_report.xlsx         # Consolidation output template
│
├── tests/                                # Comprehensive test suite
│   ├── test_variance.py                 # Variance calculation tests
│   ├── test_consolidation.py            # Consolidation tests
│   ├── test_integrations.py             # Google/Excel integration tests
│   └── test_edge_cases.py               # Edge case validation
│
├── config/                               # Configuration files
│   ├── settings.yaml                    # Application settings
│   └── credentials/                     # Google service account keys
│       └── .gitignore                   # Ignore credentials
│
├── docs/                                # Documentation
│   ├── COMPREHENSIVE_GITHUB_SOURCES.md  # Research results (keep)
│   ├── user-guides/                     # Non-technical guides
│   └── workflows/                       # Workflow documentation
│
├── spec.md                              # Business requirements (WHAT)
├── plan.md                              # Technical planning (HOW)
├── CLAUDE.md                            # AI behavioral rules
├── README.md                            # Project overview
├── MONOREPO_ARCHITECTURE.md             # Architecture (update)
├── EXTERNAL_DEPENDENCIES.md             # External repos (keep)
├── QUICK_START.md                       # Setup guide (update)
├── pyproject.toml                       # Python dependencies
└── .gitignore                           # Git ignore rules
```

---

## Key Changes from Current Structure

### 1. **Remove**
- ❌ `packages/` directory - Switching to Claude Code-native approach
- ❌ `packages/fpa-core/`, `packages/fpa-integrations/`, etc.
- ❌ Package-based Python distribution model

### 2. **Create**
- ✅ `.claude/agents/dev/` - Development agents
- ✅ `.claude/agents/prod/` - Production agents
- ✅ `.claude/commands/dev/` - Development workflows
- ✅ `.claude/commands/prod/` - Production workflows
- ✅ `.claude/skills/dev/` - Development skills
- ✅ `.claude/skills/prod/` - Production skills
- ✅ `.claude/skills/shared/` - Shared skills
- ✅ `scripts/` - Pre-written calculation scripts
- ✅ `templates/` - Report templates

### 3. **Move**
- 📦 `.claude/agents/code-reviewer.md` → `.claude/agents/dev/code-reviewer.md`
- 📦 `.claude/commands/variance-analysis.md` → `.claude/commands/prod/variance-analysis.md`
- 📦 `.claude/skills/financial-validator/` → `.claude/skills/shared/decimal-precision-enforcer/`
- 📦 `.claude/hooks/stop.sh` → Keep in place (runs after every response)

### 4. **Update**
- 📝 `pyproject.toml` - Remove package references, keep dependencies
- 📝 `MONOREPO_ARCHITECTURE.md` → Rename to `ARCHITECTURE.md`, update for Claude Code-native
- 📝 `README.md` - Update quick start for new structure
- 📝 `QUICK_START.md` - Update installation steps

---

## Workflow Separation: Dev vs Prod

### **Dev Workflows** (Build Phase)
**When to use:** User requests analysis that doesn't have a script yet.

**Example:** `/dev:create-script "Calculate YoY revenue growth by department"`

**Steps:**
1. User invokes `/dev:create-script <description>`
2. Claude generates formal spec document
3. Human approves spec
4. `script-generator` agent writes Python script using templates
5. `test-generator` agent creates comprehensive tests
6. `script-validator` agent runs tests + validation suite
7. `code-reviewer` agent independently reviews
8. Human approves final script
9. Script saved to `scripts/` directory
10. Script now available for prod workflows

**Skills auto-invoked:**
- `python-best-practices` - Enforces Decimal, type hints, error handling
- `financial-script-generator` - Uses variance/consolidation patterns
- `test-suite-generator` - Generates edge case tests
- `decimal-precision-enforcer` - Blocks float usage
- `audit-trail-enforcer` - Ensures logging

### **Prod Workflows** (Execution Phase)
**When to use:** Daily FP&A tasks using existing scripts.

**Example:** `/prod:variance-analysis budget.xlsx actuals.xlsx`

**Steps:**
1. User invokes `/prod:variance-analysis <files>`
2. Claude executes pre-written `scripts/workflows/variance_report.py`
3. Human reviews flagged variances
4. Human approves report
5. Claude exports to Google Sheets or Excel
6. Audit trail logged

**Skills auto-invoked:**
- `variance-analyzer` - Validates variance calculations
- `account-mapper` - Handles unmapped accounts
- `report-generator` - Formats output
- `decimal-precision-enforcer` - Validates precision
- `audit-trail-enforcer` - Logs transformations

---

## Integration Strategy with External Repos

### **How External Repos Are Used:**

| Repo | Dev Use | Prod Use |
|------|---------|----------|
| **gspread** | Install via pip, use in scripts | Execute in prod workflows |
| **openpyxl** | Install via pip, use in scripts | Execute in prod workflows |
| **xlsxwriter** | Install via pip, use in scripts | Execute in prod workflows |
| **humanlayer** | Study patterns for approval gates | Reference in prod workflows |
| **pyfpa** | Study FP&A consolidation patterns | Reference algorithms in scripts |
| **py-money** | Reference Decimal precision patterns | Use Decimal type directly |
| **slidio** | Study Google Slides patterns | Potentially use in scripts |
| **mcp-gdrive** | Study MCP protocol | Potentially use in scripts |

### **Why Keep external/ if installing via pip?**
1. **Audit security** - Review code before using
2. **Learn patterns** - Study implementation approaches
3. **Offline development** - No internet required
4. **Pin versions** - Git submodules track exact commits
5. **Customization** - Can patch if needed

---

## Script Generation Validation Requirements

**To ensure robust scripts without manual review:**

### **1. Comprehensive Testing** (Enforced by dev skills)
- Unit tests for all functions
- Edge case tests (from `.claude/skills/dev/test-suite-generator/references/edge-cases.md`)
- Integration tests with sample data
- Regression tests against known outputs

### **2. Anti-Patterns Blocked** (Enforced by dev skills)
- ❌ Float usage for currency → `decimal-precision-enforcer` blocks
- ❌ Missing type hints → `python-best-practices` requires them
- ❌ No error handling → `python-best-practices` requires try/except
- ❌ No audit logging → `audit-trail-enforcer` requires it
- ❌ Unmapped accounts silently dropped → `account-mapper` flags them

### **3. Code Review Gate** (Enforced by dev workflow)
- Independent `code-reviewer` agent runs
- Separate context window (no bias from generation)
- Read-only tools (can't modify, only review)
- Human approval required after review

### **4. Validation Suite** (Enforced by dev workflow)
- `script-validator` agent runs:
  - Syntax check (Python parser)
  - Type check (mypy)
  - Lint check (ruff)
  - Security check (bandit)
  - Financial precision check (no floats in src/)
  - Test coverage check (>80% required)

---

## Questions for Clarification

Before implementing, please confirm:

**1. Script Generation Rigor:**
- Should ALL new scripts go through the full dev workflow (spec → generate → test → review → approve)?
- Or are simple scripts (e.g., "sum column A") allowed to be generated inline without full validation?

**2. Prod Workflow Flexibility:**
- If a prod workflow needs a variation (e.g., variance with custom threshold), should it:
  - A) Generate a new script via dev workflow?
  - B) Pass parameters to existing script?
  - C) Both (parameters for simple changes, new script for complex)?

**3. Google Authentication:**
- Will you use a service account (JSON key file) or OAuth user login?
- Should credentials be in `config/credentials/` or `~/.claude/` personal directory?

**4. Offline Priority:**
- Should Excel-only workflows be implemented first (no Google dependency)?
- Or build Google integration from the start?

**5. External Repo Usage:**
- Should we install `pyfpa` and `slidio` via pip if available?
- Or only use them as reference (study patterns, don't install)?

---

## Implementation Steps (If Approved)

1. Remove `packages/` directory
2. Create `.claude/agents/dev/`, `.claude/agents/prod/`, `.claude/agents/shared/`
3. Create `.claude/commands/dev/`, `.claude/commands/prod/`, `.claude/commands/shared/`
4. Create `.claude/skills/dev/`, `.claude/skills/prod/`, `.claude/skills/shared/`
5. Move existing files to new locations
6. Create `scripts/` directory with initial pre-written scripts
7. Create `templates/` directory with Excel/PowerPoint templates
8. Update `pyproject.toml` to remove package references
9. Create dev skills (script-generator, validator, test-generator, code-reviewer)
10. Create prod skills (variance-analyzer, account-mapper, report-generator)
11. Create dev commands (create-script, validate-script, review-code)
12. Create prod commands (monthly-close, variance-analysis, consolidate, board-deck)
13. Create dev agents (script-generator, script-validator, test-generator, code-reviewer)
14. Create prod agents (finance-reviewer, data-validator, reconciler)
15. Update documentation (ARCHITECTURE.md, README.md, QUICK_START.md)
16. Commit and push restructured repository

---

**Awaiting your approval and answers to the 5 clarification questions before proceeding.**
