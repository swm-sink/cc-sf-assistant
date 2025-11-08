# Quick Start - FP&A Automation Monorepo

## Prerequisites

- Python 3.11+
- Poetry 1.7+
- Git

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd cc-sf-assistant
```

### 2. Initialize Git Submodules (External Dependencies)

```bash
git submodule update --init --recursive
```

This clones the 6 external dependencies:
- humanlayer (human-in-loop patterns)
- mcp-gdrive (Google Drive MCP)
- gspread (Google Sheets API)
- slidio (Google Slides templates)
- pyfpa (FP&A functions)
- py-money (Decimal precision)

### 3. Install Dependencies

```bash
# Install all packages in development mode
poetry install
```

This installs:
- All 4 workspace packages (fpa-core, fpa-integrations, fpa-workflows, fpa-cli)
- All common dependencies (pandas, gspread, click, rich, etc.)
- Development tools (pytest, black, mypy, ruff)

### 4. Verify Installation

```bash
# Activate Poetry virtual environment
poetry shell

# Verify packages are importable
python -c "import fpa_core; import fpa_integrations; import fpa_workflows; import fpa_cli"

# Should complete without errors
```

## Package Structure

```
cc-sf-assistant/
├── packages/               # Our custom code
│   ├── fpa-core/          # Pure business logic
│   ├── fpa-integrations/  # Google/Excel adapters
│   ├── fpa-workflows/     # Human-in-loop orchestration
│   └── fpa-cli/           # User interface
│
├── external/              # Cloned dependencies (git submodules)
│   ├── humanlayer/
│   ├── mcp-gdrive/
│   ├── gspread/
│   ├── slidio/
│   ├── pyfpa/
│   └── py-money/
│
└── .claude/               # Claude Code configuration
    ├── skills/
    ├── commands/
    ├── agents/
    └── hooks/
```

## Development Workflow

### Running Tests

```bash
# Run all tests across monorepo
poetry run pytest

# Run tests for specific package
cd packages/fpa-core
poetry run pytest
```

### Code Quality

```bash
# Format code
poetry run black packages/

# Lint code
poetry run ruff check packages/

# Type check
poetry run mypy packages/
```

### Working on a Package

```bash
# Example: Adding to fpa-core
cd packages/fpa-core

# Create new module
mkdir src/fpa_core/variance
touch src/fpa_core/variance/__init__.py

# Write code (after spec approval!)
# ...

# Run package-specific tests
poetry run pytest

# Type check
poetry run mypy src/
```

## Claude Code Usage

### Slash Commands

```bash
# Run variance analysis (human-in-loop workflow)
/variance-analysis budget.xlsx actuals.xlsx output.xlsx
```

### Skills (Auto-Invoked)

The `financial-validator` skill automatically activates when working with:
- Excel files
- Variance calculations
- Financial data structures

It provides:
- Edge case test suites
- Decimal precision validation
- Audit compliance checks

### Agents (Independent Review)

```bash
# Request code review from independent agent
@code-reviewer Please verify variance calculation in packages/fpa-core/
```

## Next Steps

**IMPORTANT:** Implementation code should NOT be written until spec.md is reviewed and approved.

Current status:
- ✅ Monorepo structure setup
- ✅ Package skeletons created
- ✅ External dependencies cloned
- ✅ Comprehensive research completed
- ⏳ Spec review pending
- ⏳ Implementation pending approval

### Once Spec Approved:

1. **Review spec.md** - Understand business requirements
2. **Review plan.md** - Understand technical approach
3. **Review docs/COMPREHENSIVE_GITHUB_SOURCES.md** - See available libraries
4. **Start implementation** - Follow Research → Plan → Implement → Verify workflow

## Troubleshooting

### Poetry Install Fails

```bash
# Clear Poetry cache
poetry cache clear --all pypi

# Remove lock file and retry
rm poetry.lock
poetry install
```

### Import Errors

```bash
# Ensure you're in Poetry shell
poetry shell

# Reinstall packages in development mode
poetry install
```

### Git Submodule Issues

```bash
# Reinitialize submodules
git submodule deinit -f external/
git submodule update --init --recursive
```

## Documentation

- **spec.md** - Business requirements (WHAT to build)
- **plan.md** - Technical planning (HOW to build)
- **CLAUDE.md** - AI behavioral rules
- **MONOREPO_ARCHITECTURE.md** - Architecture details
- **EXTERNAL_DEPENDENCIES.md** - Cloned repo documentation
- **docs/COMPREHENSIVE_GITHUB_SOURCES.md** - Research results (200+ repos)

## Support

See `.claude/` directory for:
- Skills: Auto-invoked capabilities
- Commands: Manual slash commands
- Agents: Independent subagents
- Hooks: Quality gates
