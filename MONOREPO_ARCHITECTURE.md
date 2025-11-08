# FP&A Automation Assistant - Monorepo Architecture

## Overview
Monorepo structure with clear separation of concerns, leveraging proven open-source libraries.

## Directory Structure

```
cc-sf-assistant/
├── spec.md                          # Business requirements (WHAT to build)
├── plan.md                          # Technical planning (HOW to build)
├── CLAUDE.md                        # AI behavioral rules
├── README.md                        # Project overview
├── MONOREPO_ARCHITECTURE.md        # This file
│
├── .claude/                         # Claude Code configuration
│   ├── skills/                      # Auto-invoked capabilities
│   ├── commands/                    # Manual slash commands
│   ├── agents/                      # Independent subagents
│   └── hooks/                       # Quality gates
│
├── packages/                        # Our custom code (separation of concerns)
│   ├── fpa-core/                   # Core FP&A business logic
│   │   ├── pyproject.toml
│   │   └── src/fpa_core/
│   │       ├── consolidation/      # Multi-dept data consolidation
│   │       ├── variance/           # Variance analysis & favorability
│   │       ├── forecasting/        # Rolling forecast maintenance
│   │       └── reporting/          # Report generation orchestration
│   │
│   ├── fpa-integrations/           # External system connectors
│   │   ├── pyproject.toml
│   │   └── src/fpa_integrations/
│   │       ├── google_sheets/      # Google Sheets API wrapper
│   │       ├── google_slides/      # Google Slides API wrapper
│   │       ├── excel/              # Excel read/write with validation
│   │       └── storage/            # File storage abstractions
│   │
│   ├── fpa-workflows/              # Human-in-loop workflows
│   │   ├── pyproject.toml
│   │   └── src/fpa_workflows/
│   │       ├── approval_gates/     # Human approval checkpoints
│   │       ├── reconciliation/     # Data reconciliation workflows
│   │       └── review/             # Report review workflows
│   │
│   └── fpa-cli/                    # Command-line interface
│       ├── pyproject.toml
│       └── src/fpa_cli/
│           └── commands/           # CLI commands for end users
│
├── external/                        # Cloned external repos (dependencies)
│   ├── humanlayer/                 # Human-in-the-loop framework
│   ├── mcp-gdrive/                 # Google Drive/Sheets MCP server
│   ├── gspread/                    # Google Sheets Python API
│   ├── slidio/                     # Google Slides template engine
│   ├── pyfpa/                      # FP&A-specific functions
│   └── py-money/                   # Decimal precision money handling
│
├── config/                         # Shared configuration
│   ├── pyproject.toml              # Root Poetry config
│   └── shared/                     # Shared config files
│
├── tests/                          # Monorepo-wide tests
│   ├── integration/                # Cross-package integration tests
│   └── e2e/                        # End-to-end user workflows
│
└── docs/                           # Documentation
    ├── architecture/               # Architecture decisions
    ├── user-guides/               # Non-technical user guides
    └── api/                       # API documentation

```

## Separation of Concerns

### 1. **packages/fpa-core/** - Pure Business Logic
- **Purpose:** Core FP&A calculations and data transformations
- **Dependencies:** None from other packages (most foundational)
- **What it does:**
  - Variance calculations (Actual - Budget, favorability logic)
  - Data consolidation algorithms
  - Forecast rolling logic
  - Financial metrics (materiality flagging, thresholds)
- **Key principle:** No I/O, no external APIs, pure functions

### 2. **packages/fpa-integrations/** - External System Adapters
- **Purpose:** Abstract external services (Google, Excel, storage)
- **Dependencies:** fpa-core (uses core types/models)
- **What it does:**
  - Google Sheets reader/writer
  - Google Slides template population
  - Excel file handlers with validation
  - Cloud storage connectors
- **Key principle:** Adapters pattern - swap implementations without changing core

### 3. **packages/fpa-workflows/** - Orchestration & Human-in-Loop
- **Purpose:** Coordinate multi-step processes with human approvals
- **Dependencies:** fpa-core, fpa-integrations
- **What it does:**
  - Research → Plan → Implement → Verify workflows
  - Approval gates (user reviews variance report before sending)
  - Reconciliation workflows (flag unmapped accounts, wait for resolution)
  - Multi-step orchestration
- **Key principle:** Checkpoints prevent automation from running unchecked

### 4. **packages/fpa-cli/** - User Interface
- **Purpose:** Non-technical user entry point
- **Dependencies:** All other packages
- **What it does:**
  - Simple commands: `fpa consolidate`, `fpa variance`, `fpa report`
  - Interactive prompts for file paths, date ranges
  - Progress indicators, human-friendly error messages
- **Key principle:** Hide complexity, expose value

## External Dependencies Strategy

### Cloned Repos (external/)
We clone external repos instead of pip-installing to:
1. **Pin exact versions** - No surprise breaking changes
2. **Customize if needed** - Can patch bugs or add features
3. **Audit code** - Review security and quality before use
4. **Offline development** - No dependency on PyPI availability

### Why Each External Repo?

| Repo | Why We Need It | What We'll Use |
|------|----------------|----------------|
| **humanlayer** | Human approval workflows | Slack/email approval gates, async human feedback |
| **mcp-gdrive** | Google integration via MCP | Standard protocol for Google Sheets/Drive access |
| **gspread** | Google Sheets API | Most popular, well-tested Sheets library (6.1.2) |
| **slidio** | Google Slides automation | Template-based slide generation from data |
| **pyfpa** | FP&A domain knowledge | Existing FP&A consolidation patterns |
| **py-money** | Financial precision | Decimal-based money handling (no float errors) |

## Monorepo Management

### Tool: Poetry with Workspaces
```toml
# config/pyproject.toml (root)
[tool.poetry]
name = "fpa-automation-monorepo"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.11"

# Workspace packages (path dependencies)
fpa-core = { path = "packages/fpa-core", develop = true }
fpa-integrations = { path = "packages/fpa-integrations", develop = true }
fpa-workflows = { path = "packages/fpa-workflows", develop = true }
fpa-cli = { path = "packages/fpa-cli", develop = true }

# External dependencies (from cloned repos)
humanlayer = { path = "external/humanlayer", develop = true }
gspread = { path = "external/gspread", develop = true }
# ... etc
```

### Development Workflow
```bash
# Install all packages in development mode
poetry install

# Run tests across entire monorepo
poetry run pytest

# Work on specific package
cd packages/fpa-core
poetry run pytest  # Package-specific tests

# Build CLI for distribution
cd packages/fpa-cli
poetry build
```

## Benefits of This Architecture

1. **Clear Boundaries:** Each package has single responsibility
2. **Independent Testing:** Test business logic without Google API calls
3. **Flexible Deployment:** Can deploy CLI only, or expose as web API
4. **Team Scalability:** Different people can own different packages
5. **Audit Trail:** External code isolated in `external/`, our code in `packages/`
6. **Non-Technical Users:** CLI hides complexity, slash commands in Claude Code

## Next Steps

1. Clone external repos to `external/`
2. Create package skeletons in `packages/`
3. Set up Poetry workspace in root
4. Wire up basic imports and tests
5. Begin implementation per spec.md priorities
