# Meta-Infrastructure Dependency Flow Map

**Version:** 1.0
**Date:** 2025-11-09
**Purpose:** Comprehensive dependency analysis for all 44 meta-infrastructure components

---

## Executive Summary

**Critical Finding:** Development workflows (Priority 1) have ZERO dependencies on other phases, making them the correct starting point.

**Dependency Chain:**
```
Priority 1: Development Workflows (Phase 7 in docs)
  └─ NO external dependencies
  └─ Enables automated creation of ALL subsequent components

Priority 2: Shared Foundation (Phase 1 in docs)
  └─ Depends on: Priority 1 tools to BUILD the components
  └─ Provides enforcement used by Priority 3

Priority 3: Production Infrastructure (Phases 2-6 in docs)
  └─ Depends on: Priority 1 tools (to build), Priority 2 enforcement (to use)
  └─ Can be built in parallel once Priorities 1-2 complete

Priority 4: Orchestration (Phase 8 in docs)
  └─ Depends on: All Priority 3 components to orchestrate
```

---

## Priority 1: Development Workflows (Week 1-2)

### Component Dependencies

#### 1.1 `python-best-practices` Skill
**Type:** Discipline skill
**Dependencies:**
- ✅ NONE - Pure enforcement rules, no external dependencies
**Used By:** All components in Priorities 2-4
**Python Packages:** None (just enforces patterns)

#### 1.2 `test-suite-generator` Skill
**Type:** Technique skill
**Dependencies:**
- `.claude/skills/financial-validator/` (EXISTS - already created)
- `.claude/skills/financial-validator/references/edge-cases.md` (EXISTS)
**Used By:** All components in Priorities 2-4
**Python Packages:**
- pytest (dev dependency)
- hypothesis (dev dependency)
- pytest-cov (dev dependency)

#### 1.3 `@script-generator` Agent
**Type:** Full Access Implementer
**Dependencies:**
- `python-best-practices` skill (1.1 - same priority)
- `decimal-precision-enforcer` will use it later (but not dependency)
**Used By:** Priority 2, 3, 4 components
**Python Packages:** None (generates code, doesn't execute)

#### 1.4 `@test-generator` Agent
**Type:** Full Access Implementer
**Dependencies:**
- `test-suite-generator` skill (1.2 - same priority)
- `.claude/skills/financial-validator/references/edge-cases.md` (EXISTS)
**Used By:** Priority 2, 3, 4 components
**Python Packages:** None (generates code, doesn't execute)

#### 1.5 `@script-validator` Agent
**Type:** Read + Bash Only
**Dependencies:**
- ✅ NONE - Just runs validation tools
**Python Packages:**
- pytest (dev dependency)
- mypy (dev dependency)
- ruff (dev dependency)
- pytest-cov (dev dependency)

#### 1.6 `/create-script` Command
**Type:** Workflow orchestration
**Dependencies:**
- `@script-generator` agent (1.3 - same priority)
- `@test-generator` agent (1.4 - same priority)
- `python-best-practices` skill (1.1 - same priority)
**Used By:** Developer to create Priorities 2-4
**Python Packages:** None

#### 1.7 `/validate-script` Command
**Type:** Workflow orchestration
**Dependencies:**
- `@script-validator` agent (1.5 - same priority)
**Used By:** Developer to validate Priorities 2-4
**Python Packages:** All dev dependencies

#### 1.8 `/review-code` Command
**Type:** Workflow orchestration
**Dependencies:**
- `@code-reviewer` agent (EXISTS - already created)
**Used By:** Developer for final review of Priorities 2-4
**Python Packages:** None

### Priority 1 Python Package Requirements

**Required BEFORE starting Priority 1:**
```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"          # For test-suite-generator and @script-validator
pytest-cov = "^4.1.0"      # For coverage enforcement
mypy = "^1.7.1"            # For type checking in @script-validator
ruff = "^0.1.9"            # For linting in @script-validator
hypothesis = "^6.90.0"     # For property-based test generation
```

**Status:** ✅ ALL INSTALLED (already in pyproject.toml)

---

## Priority 2: Shared Foundation (Week 3)

### Component Dependencies

#### 2.1 `decimal-precision-enforcer` Skill
**Type:** Discipline skill
**Dependencies:**
- **BUILD DEPENDENCY:** `/create-script` command (Priority 1) - to create the skill
- **BUILD DEPENDENCY:** `@script-generator` agent (Priority 1) - to generate implementation
**Used By:** All Priority 3 production components
**Python Packages:**
- typeguard (for runtime type checking)
- ✅ Already added to pyproject.toml

#### 2.2 `audit-trail-enforcer` Skill
**Type:** Discipline skill
**Dependencies:**
- **BUILD DEPENDENCY:** `/create-script` command (Priority 1)
- **BUILD DEPENDENCY:** `@script-generator` agent (Priority 1)
**Used By:** All Priority 3 production components
**Python Packages:**
- loguru (for audit logging)
- python-dotenv (for config)
- ✅ Already added to pyproject.toml

#### 2.3 `/setup` Command
**Type:** Workflow orchestration
**Dependencies:**
- **BUILD DEPENDENCY:** `/create-script` command (Priority 1)
- **BUILD DEPENDENCY:** `@script-generator` agent (Priority 1)
**Used By:** End users for initial setup
**Python Packages:**
- All packages in pyproject.toml (installs them)

### Priority 2 Python Package Requirements

**Required BEFORE starting Priority 2:**
```toml
# Precision & Currency (Priority 2 - Shared Foundation)
stockholm = "^0.3.0"       # Decimal precision patterns
typeguard = "^4.0.0"       # Runtime type checking

# Core utilities
python-dotenv = "^1.0.0"   # Environment config
loguru = "^0.7.2"          # Audit logging
```

**Status:** ✅ ALL INSTALLED (already in pyproject.toml)

---

## Priority 3: Production Infrastructure (Week 4-11)

### Phase 2 (Data Extraction) - Week 4-5

#### 3.1 `databricks-extractor` Skill
**Dependencies:**
- **BUILD:** Priority 1 tools (`/create-script`)
- **RUNTIME:** `decimal-precision-enforcer` (Priority 2)
- **RUNTIME:** `audit-trail-enforcer` (Priority 2)
**Python Packages:**
- tenacity (retry logic)
- pydantic (data validation)
- pandera (DataFrame validation)

#### 3.2 `@databricks-validator` Agent
**Dependencies:**
- **BUILD:** Priority 1 tools
- **RUNTIME:** `databricks-extractor` skill (3.1 - same phase)
**Python Packages:**
- pandera (validation)
- great-expectations (optional, data quality)

#### 3.3 `/extract-databricks` Command
**Dependencies:**
- **BUILD:** Priority 1 tools
- **RUNTIME:** `databricks-extractor` skill (3.1)
- **RUNTIME:** `@databricks-validator` agent (3.2)
**Python Packages:**
- All from 3.1, 3.2

#### 3.4-3.6 Adaptive Components (similar pattern)
**Dependencies:** Same as Databricks (3.1-3.3)
**Python Packages:** Same as Databricks

**Phase 2 Python Packages:**
```toml
# API Integration (Priority 3 - Phase 2)
tenacity = "^8.2.0"        # Retry logic

# Data Validation (Priority 3 - Phase 2)
pydantic = "^2.0.0"        # Type validation
pandera = "^0.17.0"        # DataFrame validation

# Data Warehouse & Quality (Priority 3 - Phase 2)
duckdb = "^0.9.0"          # Local SQL for validation
great-expectations = "^0.18.0"  # Optional data quality
```

**Status:** ✅ ALL INSTALLED

---

### Phase 3 (Account Reconciliation) - Week 6

#### 3.7 `account-mapper` Skill
**Dependencies:**
- **BUILD:** Priority 1 tools
- **RUNTIME:** Priority 2 enforcement
- **DATA:** Requires output from Phase 2 (databricks + adaptive extracts)
**Python Packages:**
- rapidfuzz (fuzzy matching)
- duckdb (local SQL for matching)

#### 3.8 `@account-reconciler` Agent
**Dependencies:**
- **BUILD:** Priority 1 tools
- **RUNTIME:** `account-mapper` skill (3.7)
**Python Packages:**
- Same as 3.7

#### 3.9 `/reconcile-accounts` Command
**Dependencies:**
- **BUILD:** Priority 1 tools
- **RUNTIME:** 3.7, 3.8
- **WORKFLOW:** Must run AFTER `/extract-databricks` and `/extract-adaptive`
**Python Packages:**
- Same as 3.7

**Phase 3 Python Packages:**
```toml
# Reconciliation (Priority 3 - Phase 3)
rapidfuzz = "^3.5.0"       # Fuzzy string matching
```

**Status:** ✅ INSTALLED

---

### Phase 4 (Reporting) - Week 7-8

#### 3.10 `excel-report-generator` Skill
**Dependencies:**
- **BUILD:** Priority 1 tools
- **RUNTIME:** Priority 2 enforcement
- **DATA:** Requires reconciled data from Phase 3
**Python Packages:**
- xlsxwriter (Excel generation)
- great-tables (table formatting)
- pandas (data manipulation)

#### 3.11 `@report-formatter` Agent
**Dependencies:**
- **BUILD:** Priority 1 tools
- **RUNTIME:** `excel-report-generator` skill (3.10)
**Python Packages:**
- Same as 3.10

#### 3.12 `/generate-excel-report` Command
**Dependencies:**
- **BUILD:** Priority 1 tools
- **RUNTIME:** 3.10, 3.11
- **WORKFLOW:** Must run AFTER `/reconcile-accounts`
**Python Packages:**
- Same as 3.10

**Phase 4 Python Packages:**
```toml
# Core (already installed)
pandas = "^2.1.0"
openpyxl = "^3.1.2"        # Excel read/write
xlsxwriter = "^3.1.9"      # Excel generation

# Reporting & Tables (Priority 3 - Phase 4)
great-tables = "^0.2.0"    # Advanced table formatting
```

**Status:** ✅ ALL INSTALLED

---

### Phase 5 (Google Workspace Integration) - Week 9-11

#### 3.13-3.15 Google Slides Components
**Dependencies:**
- **BUILD:** Priority 1 tools
- **RUNTIME:** Priority 2 enforcement
- **DATA:** Requires variance data from Phase 3
**Python Packages:**
- google-auth
- google-auth-oauthlib
- google-api-python-client

#### 3.16-3.18 Google Sheets Components
**Dependencies:**
- **BUILD:** Priority 1 tools
- **RUNTIME:** Priority 2 enforcement
- **DATA:** Requires variance data from Phase 3
**Python Packages:**
- gspread
- gspread-dataframe

**Phase 5 Python Packages:**
```toml
# Google Workspace APIs (Priority 3 - Phase 5)
google-auth = "^2.23.0"
google-auth-oauthlib = "^1.1.0"
google-api-python-client = "^2.100.0"
gspread = "^6.1.2"
gspread-dataframe = "^4.0.0"
```

**Status:** ✅ ALL INSTALLED

---

### Phase 6 (Forecast Maintenance) - Week 12-13

#### 3.19-3.24 Forecast Components
**Dependencies:**
- **BUILD:** Priority 1 tools
- **RUNTIME:** Priority 2 enforcement
- **DATA:** Requires historical actuals from Phase 2
**Python Packages:**
- pyxirr (IRR/NPV calculations)
- pandas (time series)

**Phase 6 Python Packages:**
```toml
# Financial Calculations (Priority 3 - Phase 6)
pyxirr = "^0.10.0"         # IRR/NPV calculations
```

**Status:** ✅ INSTALLED

---

## Priority 4: Orchestration (Week 14)

### Component Dependencies

#### 4.1 `/prod:monthly-close` Command
**Type:** Orchestration workflow
**Dependencies:**
- **BUILD:** Priority 1 tools (`/create-script`)
- **RUNTIME:** ALL Priority 3 commands:
  - `/extract-databricks` (Phase 2)
  - `/extract-adaptive` (Phase 2)
  - `/reconcile-accounts` (Phase 3)
  - `/generate-excel-report` (Phase 4)
  - `/update-google-slides` (Phase 5)
  - `/update-google-sheets` (Phase 5)
**Workflow Sequence:**
1. Extract Databricks actuals
2. Extract Adaptive budget
3. Reconcile accounts
4. Calculate variances
5. Generate Excel report
6. Update Google Slides
7. Update Google Sheets

**Python Packages:**
```toml
[tool.poetry.group.orchestration]
optional = true

[tool.poetry.group.orchestration.dependencies]
prefect = "^2.14.0"        # Workflow orchestration
```

**Status:** ✅ INSTALLED (optional group)

---

## Critical Dependency Issues Found

### Issue 1: pyproject.toml Phase Comments WRONG ❌

**Current state (INCORRECT):**
```toml
# Precision & Currency (Phase 1 - Shared Foundation)
stockholm = "^0.3.0"

# Data Validation (Phase 1-2)
pydantic = "^2.0.0"

# Property-based testing (Phase 7)
hypothesis = "^6.90.0"
```

**Problem:** Uses OLD phase numbers that don't match implementation priority

**Should be:**
```toml
# Precision & Currency (Priority 2 - Shared Foundation)
stockholm = "^0.3.0"

# Data Validation (Priority 3 - Data Extraction)
pydantic = "^2.0.0"

# Property-based testing (Priority 1 - Development Workflows)
hypothesis = "^6.90.0"
```

### Issue 2: External Integration Guide Uses OLD Phase Numbers ❌

**Current:** Maps repos to "Phase 1-8"
**Should:** Map repos to "Priority 1-4" with sub-phases

### Issue 3: Component Build Order Not Explicit ❌

**Missing:** Clear statement that ALL Priority 2-4 components MUST be built using Priority 1 tools

---

## Corrected Dependency Matrix

| Component Category | Implementation Priority | Build Tool | Runtime Dependencies | Python Packages |
|-------------------|------------------------|-----------|---------------------|-----------------|
| **Development Workflows** | Priority 1 (Week 1-2) | Manual (meta-skills) | None | pytest, mypy, ruff, hypothesis |
| **Shared Foundation** | Priority 2 (Week 3) | Priority 1 tools | None | stockholm, typeguard, loguru |
| **Data Extraction** | Priority 3a (Week 4-5) | Priority 1 tools | Priority 2 enforcement | tenacity, pydantic, pandera |
| **Account Reconciliation** | Priority 3b (Week 6) | Priority 1 tools | Priority 2 + 3a | rapidfuzz, duckdb |
| **Reporting** | Priority 3c (Week 7-8) | Priority 1 tools | Priority 2 + 3b | xlsxwriter, great-tables |
| **Google Integration** | Priority 3d (Week 9-11) | Priority 1 tools | Priority 2 + 3b | google-api-python-client, gspread |
| **Forecast Maintenance** | Priority 3e (Week 12-13) | Priority 1 tools | Priority 2 + 3a | pyxirr |
| **Orchestration** | Priority 4 (Week 14) | Priority 1 tools | ALL Priority 3 | prefect (optional) |

---

## Build Order Rules

### Rule 1: Priority 1 MUST Complete First
**Rationale:** Cannot build other components without automation tools

### Rule 2: Priority 2 MUST Complete After Priority 1
**Rationale:** Need Priority 1 tools to build enforcement skills

### Rule 3: Priority 3 Sub-Phases Have Dependencies
**Safe Parallel:** Phase 4 (Reporting) and Phase 5 (Google) can be built in parallel
**Sequential:** Phase 2 → Phase 3 → Phase 4 (data flow dependency)

### Rule 4: Priority 4 MUST Complete Last
**Rationale:** Orchestrates all Priority 3 components

---

## Python Package Installation Order

### Install Before Priority 1:
```bash
poetry install  # Installs all dev dependencies
```

### Install Before Priority 2:
```bash
# Already installed in step above:
# - stockholm, typeguard, loguru, python-dotenv
```

### Install Before Priority 3:
```bash
# Already installed:
# - tenacity, pydantic, pandera, rapidfuzz
# - xlsxwriter, great-tables
# - google-api-python-client, gspread
# - pyxirr, duckdb
```

### Install Before Priority 4:
```bash
poetry install --with orchestration  # Optional: Prefect
```

**Status:** ✅ ALL PACKAGES ALREADY INSTALLED

---

## External Repository Mapping (Corrected)

### Priority 1 (Development Workflows)
**Primary Repos:**
- external/data-validation/hypothesis/ - Property-based testing patterns
- external/data-validation/typeguard/ - Runtime type checking
- external/audit-compliance/python-audit-log/ - Audit patterns

### Priority 2 (Shared Foundation)
**Primary Repos:**
- external/precision-currency/stockholm/ - Decimal precision patterns
- external/py-money/ - Currency validation patterns
- external/audit-compliance/python-audit-log/ - Centralized logging

### Priority 3 (Production Infrastructure)
**Phase 2 (Data Extraction):**
- external/data-validation/pandera/ - DataFrame validation
- external/data-warehouse/great-expectations/ - Data quality
- external/api-integration/tenacity/ - Retry logic

**Phase 3 (Reconciliation):**
- external/reconciliation/splink/ - Fuzzy matching
- external/reconciliation/dedupe/ - ML matching
- external/data-warehouse/duckdb/ - Local SQL

**Phase 4 (Reporting):**
- external/reporting-automation/XlsxWriter/ - Excel generation
- external/reporting-automation/great-tables/ - Table formatting

**Phase 5 (Google Integration):**
- external/api-integration/google-api-python-client/ - OAuth patterns
- external/gspread/ - Sheets automation

**Phase 6 (Forecast):**
- external/financial-modeling/FinanceToolkit/ - Financial ratios
- external/financial-modeling/pyxirr/ - IRR/NPV
- external/financial-modeling/mplfinance/ - Visualization

### Priority 4 (Orchestration)
**Primary Repos:**
- external/etl-pipelines/prefect/ - Workflow orchestration
- external/etl-pipelines/dbt-core/ - SQL transformation patterns

---

## Validation Checklist

### Dependency Flow Validation
- ✅ Priority 1 has NO dependencies on other priorities
- ✅ Priority 2 depends ONLY on Priority 1 (for build tools)
- ✅ Priority 3 depends on Priority 1 (build) and Priority 2 (enforcement)
- ✅ Priority 4 depends on ALL Priority 3 components
- ✅ No circular dependencies exist

### Python Package Validation
- ✅ All Priority 1 packages installed (dev group)
- ✅ All Priority 2 packages installed (main dependencies)
- ✅ All Priority 3 packages installed (main dependencies)
- ✅ Priority 4 packages available (optional group)

### Documentation Consistency
- ❌ pyproject.toml uses OLD phase numbers (needs fix)
- ❌ External integration guide uses OLD phase numbers (needs fix)
- ✅ spec.md uses correct priority order
- ✅ plan.md uses correct priority order
- ✅ specs/meta-infrastructure/plan.md uses correct priority order
- ✅ specs/meta-infrastructure/checklist.md uses correct priority order

---

## Next Actions

1. **Fix pyproject.toml phase comments** - Update to Priority 1-4
2. **Fix external integration guide** - Update to Priority 1-4
3. **Create build automation checklist** - Ensure Priority 1 tools used for all others
4. **Validate cross-references** - Ensure all docs use consistent terminology

---

**Last Updated:** 2025-11-09
**Status:** ✅ DEPENDENCY FLOW VALIDATED
**Critical Issues:** 2 (pyproject.toml comments, external integration guide)
**Blocking Issues:** 0 (all packages installed, no true dependency violations)
