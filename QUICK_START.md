# Quick Start - FP&A Automation Assistant

## Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Poetry 1.7+** - [Installation Guide](https://python-poetry.org/docs/#installation)
- **Git** - [Download](https://git-scm.com/downloads)

## Installation

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd cc-sf-assistant
```

### Step 2: Initialize Git Submodules

This clones the external dependencies (humanlayer, gspread, slidio, pyfpa, py-money) that we reference:

```bash
git submodule update --init --recursive
```

Expected output:
```
Submodule 'external/humanlayer' registered for path 'external/humanlayer'
Submodule 'external/gspread' registered for path 'external/gspread'
...
```

### Step 3: Install Dependencies

Poetry creates a virtual environment and installs all dependencies:

```bash
poetry install
```

This installs:
- Python calculation scripts dependencies (pandas, gspread, openpyxl, xlsxwriter)
- Claude Code interface libraries (click, rich, loguru)
- Google integration (google-auth, google-auth-oauthlib)
- Development tools (pytest, mypy, ruff, bandit)

Expected output:
```
Creating virtualenv cc-sf-assistant in ...
Installing dependencies from lock file
...
Installing the current project: fpa-automation-monorepo (0.2.0)
```

### Step 4: Install Pre-Commit Hooks

This sets up quality gates that run before every git commit:

```bash
poetry run python scripts/utils/install_hooks.py
```

Expected output:
```
✅ Pre-commit hook installed
```

The hook will run pytest, mypy, ruff, and bandit automatically before each commit.

### Step 5: Verify Installation

Run the test suite to verify everything is set up correctly:

```bash
poetry run pytest
```

Expected output:
```
============================= test session starts ==============================
collected X items

tests/test_variance.py ..                                            [ XX%]
tests/test_consolidation.py ..                                       [ XX%]
tests/test_edge_cases.py ..                                          [100%]

============================== X passed in X.XXs ===============================
```

### Step 6: Configure Credentials (Optional - For Google Integration)

If you plan to use Google Sheets/Slides integration:

```bash
# Create credentials directory
mkdir -p config/credentials

# Add your Google service account JSON
# (Obtain from Google Cloud Console)
cp ~/Downloads/service-account.json config/credentials/

# Or add OAuth token
# (Obtain via Google OAuth flow)
cp ~/Downloads/oauth-token.json config/credentials/
```

**Note:** Credentials are git-ignored and never committed.

---

## Verify Package Imports

Activate the Poetry shell and verify imports:

```bash
# Enter virtual environment
poetry shell

# Verify imports work
python -c "import pandas; import gspread; import openpyxl; print('✅ All imports successful')"
```

Expected output:
```
✅ All imports successful
```

---

## Directory Structure After Installation

```
cc-sf-assistant/
├── .venv/                   # Poetry virtual environment (auto-created)
├── .git/
│   └── hooks/
│       └── pre-commit       # Installed quality gate
├── external/                # Cloned submodules
│   ├── humanlayer/
│   ├── gspread/
│   ├── slidio/
│   ├── pyfpa/
│   └── py-money/
├── config/
│   └── credentials/         # Your Google credentials (not in git)
│       ├── service-account.json
│       └── oauth-token.json
└── ... (other project files)
```

---

## Using Claude Code

### Slash Commands (Explicit Invocation)

Execute workflows via slash commands:

```bash
# Production workflows
/variance-analysis budget_2025.xlsx actuals_nov.xlsx
/monthly-close november
/consolidate data/departments/

# Development workflows
/create-script "Calculate YoY revenue growth by department"
/validate-script scripts/core/yoy_growth.py
/review-code scripts/core/variance.py

# Shared utilities
/sync-docs                          # Validate documentation consistency
/help                               # Get help
```

### Skills (Auto-Invoked)

Skills are automatically invoked when you mention keywords:

```bash
# Just type in conversation:
"Can you run a variance analysis on budget_2025.xlsx and actuals_nov.xlsx?"

# Claude automatically invokes the variance-analyzer skill
# No slash command needed!
```

---

## Development Workflow

### Running Tests

```bash
# Activate virtual environment (if not already in it)
poetry shell

# Run all tests
pytest

# Run specific test file
pytest tests/test_variance.py

# Run with coverage report
pytest --cov=scripts --cov-report=term-missing

# Type checking
mypy scripts/

# Linting
ruff check scripts/

# Security scanning
bandit -r scripts/
```

### Git Workflow with Quality Gates

```bash
# Make changes to scripts
vim scripts/core/variance.py

# Stage changes
git add scripts/core/variance.py

# Commit (pre-commit hook runs automatically)
git commit -m "feat: add QoQ variance calculation"

# Pre-commit hook output:
# Running pre-commit quality checks...
# ✓ Running tests...
# ✓ Running type checks...
# ✓ Running linter...
# ✓ Running security checks...
# ✓ Checking for versioned filenames...
# ✅ All quality checks passed

# Push to remote
git push
```

---

## Troubleshooting

### Poetry Install Fails

**Issue:** `poetry install` fails with dependency resolution errors

**Solution:**
```bash
# Clear Poetry cache
poetry cache clear --all pypi

# Remove lock file and retry
rm poetry.lock
poetry install
```

### Import Errors

**Issue:** `ModuleNotFoundError: No module named 'pandas'`

**Solution:**
```bash
# Ensure you're in Poetry shell
poetry shell

# Reinstall packages
poetry install
```

### Git Submodule Issues

**Issue:** External dependencies not found

**Solution:**
```bash
# Reinitialize submodules
git submodule deinit -f external/
git submodule update --init --recursive
```

### Pre-Commit Hook Not Running

**Issue:** Commits succeed without quality checks

**Solution:**
```bash
# Reinstall hook
poetry run python scripts/utils/install_hooks.py

# Verify hook exists
ls -la .git/hooks/pre-commit

# Verify hook is executable
chmod +x .git/hooks/pre-commit
```

### Google Authentication Errors

**Issue:** `google.auth.exceptions.DefaultCredentialsError`

**Solution:**
```bash
# Verify credentials file exists
ls -la config/credentials/

# Check file permissions
chmod 600 config/credentials/service-account.json

# Verify JSON format is valid
python -c "import json; json.load(open('config/credentials/service-account.json'))"
```

---

## Next Steps

1. **Explore Jupyter Notebooks:** `docs/notebooks/01_getting_started.ipynb`
2. **Review Sample Data:** `data/samples/budget_2025.xlsx`
3. **Read Documentation:** `spec.md` (business requirements), `plan.md` (technical details)
4. **Try a Prod Workflow:** `/prod:variance-analysis` with sample data
5. **Generate a Custom Script:** `/dev:create-script "Your analysis idea"`

---

## Documentation Resources

| Document | Purpose |
|----------|---------|
| **README.md** | Project overview and key features |
| **spec.md** | Business requirements (WHAT we're building) |
| **plan.md** | Technical planning (HOW to build) |
| **CLAUDE.md** | AI behavioral rules |
| **EXTERNAL_DEPENDENCIES.md** | Cloned repository documentation |
| **docs/COMPREHENSIVE_GITHUB_SOURCES.md** | Research results (200+ repos) |
| **docs/notebooks/** | Interactive tutorials (7 notebooks) |

---

## Support

- **Troubleshooting:** `docs/user-guides/troubleshooting.md`
- **FAQ:** `docs/user-guides/faq.md`
- **Best Practices:** `docs/user-guides/best-practices.md`

---

**Last Updated:** 2025-11-08
