# Meta-Infrastructure Implementation Plan

**Version:** 1.1-DRAFT (RESEQUENCED)
**Date:** 2025-11-09 (Updated for Dev-First Priority)
**Status:** 📋 PLANNING PHASE
**Purpose:** Detailed implementation plan for creating all commands, agents, and skills

---

## ⚠️ CRITICAL: RESEQUENCED IMPLEMENTATION ORDER

**🚨 BREAKING CHANGE:** Phase ordering has been RESEQUENCED to prioritize development infrastructure.

**OLD ORDER (Deprecated):**
~~Phase 1: Shared Foundation → Phase 2: Data Extraction → ... → Phase 7: Dev Workflows~~

**NEW ORDER (Effective 2025-11-09):**
```
Phase 1: Development Workflows (Week 1-2) ⭐ IMPLEMENT FIRST
  └─ Build the tools to build tools
  └─ /create-script, @script-generator, python-best-practices

Phase 2: Shared Foundation (Week 3)
  └─ Built using dev tools from Phase 1
  └─ decimal-precision-enforcer, audit-trail-enforcer

Phase 3-7: Production Infrastructure (Week 4-11)
  └─ Built using dev tools from Phase 1
  └─ All production components created with automated generation

Phase 8: Orchestration (Week 12)
  └─ Tie everything together
```

**WHY THIS MATTERS:**
- Phase 1 (Dev Workflows) builds the automation infrastructure
- All subsequent phases leverage that automation
- Ensures consistency, quality, comprehensive testing
- Prevents manual script creation errors in financial systems

**READ THIS ENTIRE PLAN WITH THE NEW PHASE NUMBERS:**
- What was "Phase 7" is now **Phase 1** (Development Workflows)
- What was "Phase 1" is now **Phase 2** (Shared Foundation)
- All other production phases shift accordingly

---

## Overview

Based on research findings (see `research.md`), we need to create:
- **15 commands** (3 exist, 12 to create)
- **11 agents** (1 exists, 10 to create)
- **18 skills** (6 exist, 12 to create)

**Total:** 44 infrastructure components (10 exist, 34 to create)

---

## Implementation Strategy

### Phased Rollout (RESEQUENCED)

**Phase-by-Phase Approach (NEW ORDER):**
1. **Phase 1: Build development workflows FIRST** (tools to build tools)
2. **Phase 2: Build shared foundation** (using dev tools from Phase 1)
3. **Phases 3-7: Build production components** (using dev tools from Phase 1)
4. **Phase 8: Build orchestration** (tie everything together)

**Per-Component Workflow:**
- Use meta-skills (`creating-commands`, `creating-agents`, `creating-skills`)
- Use Phase 1 dev tools (`/create-script`, `@script-generator`) for Phases 2-8
- Follow RPIV workflow for each component
- Human approval at each checkpoint
- Independent verification before marking complete

---

## Phase 1 ➡️ ACTUAL PHASE 2: Shared Foundation (Week 3)

### Priority: HIGH (implement AFTER Phase 7/Actual Phase 1)

**🚨 RESEQUENCED:** This is Phase 1 in the document, but **Phase 2 in implementation order**.

**Goal:** Build shared enforcement infrastructure using dev tools from Phase 7 (Actual Phase 1).

**Why After Phase 7:**
- Use `/create-script` and `@script-generator` from Phase 7 to build these components
- Ensures consistent quality and comprehensive testing
- Development tools are ready to validate enforcement logic

### 1.1: `decimal-precision-enforcer` Skill

**Pattern:** Discipline skill (enforces rules)

**Auto-Invocation Triggers:**
- Keywords: "financial", "currency", "money", "variance", "budget", "actual", "calculation"
- File patterns: `scripts/core/*.py`, `scripts/workflows/*.py`
- Always auto-invoke when generating Python code

**Behavior:**
```python
# When invoked, check:
1. Import statement includes: from decimal import Decimal, ROUND_HALF_UP
2. Currency variables use Decimal type
3. NO float or double for currency
4. Division operations protected against zero division

# If violations found:
- Block code generation
- Provide specific fix: file:line with exact correction
- Reference: .claude/skills/financial-validator/references/edge-cases.md
```

**Files to Create:**
- `.claude/skills/shared/decimal-precision-enforcer/SKILL.md`
- `.claude/skills/shared/decimal-precision-enforcer/references/decimal-usage-guide.md`

**Dependencies:** None

**Verification:**
- Test with intentional float usage → Should block
- Test with correct Decimal usage → Should pass

---

### 1.2: `audit-trail-enforcer` Skill

**Pattern:** Discipline skill (enforces rules)

**Auto-Invocation Triggers:**
- Keywords: "transformation", "calculation", "extract", "load", "update", "generate"
- File patterns: `scripts/core/*.py`, `scripts/integrations/*.py`, `scripts/workflows/*.py`
- Always auto-invoke when generating data transformation code

**Behavior:**
```python
# When invoked, check:
1. Import statement includes: import logging, from datetime import datetime, UTC
2. Audit entry includes:
   - timestamp (ISO 8601 format)
   - user (os.getenv("USER"))
   - operation name
   - source files
   - output files
   - record counts
3. Audit entry written to config/audit.log

# If violations found:
- Block code generation
- Provide template audit logging code
- Reference: plan.md Section 2 (Centralized Audit Log)
```

**Files to Create:**
- `.claude/skills/shared/audit-trail-enforcer/SKILL.md`
- `.claude/skills/shared/audit-trail-enforcer/references/audit-log-schema.json`
- `.claude/skills/shared/audit-trail-enforcer/references/audit-template.py`

**Dependencies:** None

**Verification:**
- Test with code missing audit logging → Should block
- Test with correct audit logging → Should pass

---

### 1.3: `/setup` Command

**Pattern:** Orchestration workflow

**Purpose:** Initial project setup for new users

**Arguments:** None

**Workflow:**
```markdown
1. Verify Python version (3.11+)
2. Check pyproject.toml exists
3. Run: poetry install
4. Create config directories:
   - config/credentials/
   - config/workflow-state/
   - data/samples/
   - logs/
5. Install pre-commit hooks:
   - Copy .claude/hooks/pre-commit to .git/hooks/pre-commit
   - Make executable (chmod +x)
6. Guide user through credential setup:
   - Google Service Account JSON
   - Databricks Personal Access Token
   - Adaptive API token
7. Validate setup:
   - Run: poetry run pytest tests/unit/
   - Check all tests pass
8. Display welcome message with next steps
```

**Files to Create:**
- `.claude/commands/shared/setup.md`

**Dependencies:**
- `pyproject.toml` (already exists)
- Pre-commit hook script (to be created)

**Verification:**
- Run `/setup` on fresh clone
- Verify all directories created
- Verify hooks installed
- Verify tests pass

---

## Phase 2: Data Extraction (Week 2-3)

### Priority: HIGH (enables all downstream workflows)

**Goal:** Extract actuals from Databricks and budget from Adaptive Insights.

### 2.1: `databricks-extractor` Skill

**Pattern:** Technique skill (provides implementation pattern)

**Auto-Invocation Triggers:**
- Keywords: "databricks", "extract actuals", "sql warehouse"
- File patterns: `scripts/integrations/databricks*.py`

**Behavior:**
```python
# When invoked, provide:
1. Connection pattern using databricks-sql-connector
2. Retry logic with exponential backoff
3. Async execution for large queries
4. NULL handling (flag, don't drop)
5. Decimal conversion for amounts
6. Audit logging template

# References:
- specs/databricks/DATABRICKS_API_SPEC.md
- External: databricks-sql-connector documentation
```

**Files to Create:**
- `.claude/skills/prod/databricks-extractor/SKILL.md`
- `.claude/skills/prod/databricks-extractor/references/connection-template.py`
- `.claude/skills/prod/databricks-extractor/references/retry-logic.py`

**Dependencies:**
- `databricks-sql-connector` package (add to pyproject.toml)
- `decimal-precision-enforcer` skill
- `audit-trail-enforcer` skill

---

### 2.2: `@databricks-validator` Agent

**Pattern:** Read-Only Researcher

**Tools:** Read, Grep, Glob (no Write/Edit)

**Specialty:** Databricks query result validation

**Behavior:**
```markdown
## Validation Checklist

When invoked to validate Databricks extraction:

1. **Data Type Validation:**
   - Amounts are Decimal (not float)
   - Dates are datetime objects
   - Account IDs are strings

2. **NULL Handling:**
   - Count NULL values in critical columns
   - Flag for human review
   - Don't silently drop rows

3. **Query Result Sanity Checks:**
   - Record count reasonable? (not 0, not millions)
   - Account IDs match expected pattern?
   - Date range matches requested period?

4. **Audit Trail:**
   - Query logged with timestamp
   - Parameters logged (month, year)
   - Execution time logged

## Output Format

**VALIDATION REPORT:**
- [ ] Data types: PASS/FAIL
- [ ] NULL handling: PASS/FAIL + count
- [ ] Sanity checks: PASS/FAIL + notes
- [ ] Audit trail: PASS/FAIL

**RECOMMENDATION:** APPROVE / REJECT / NEEDS REVIEW
```

**Files to Create:**
- `.claude/agents/prod/databricks-validator.md`

**Dependencies:**
- Read-only access pattern (no modifications)

---

### 2.3: `/extract-databricks` Command

**Pattern:** RPIV Workflow

**Arguments:** `<month> <year> [output_file]`

**Workflow:**
```markdown
### STEP 1: RESEARCH Phase
- Connect to Databricks (test connection)
- Inspect schema for actuals table
- Document column names, data types
- Identify NULL patterns
- **CHECKPOINT 1:** Present findings

### STEP 2: PLAN Phase
- Design SQL query for specified month/year
- Plan NULL handling strategy
- Define output file structure
- **CHECKPOINT 2:** Present plan

### STEP 3: IMPLEMENT Phase
- Execute query with retry logic
- Convert to Decimal precision
- Handle NULLs (flag for review)
- Save to output file
- Log audit entry
- **CHECKPOINT 3:** Review extraction results

### STEP 4: VERIFY Phase
- Invoke @databricks-validator
- Spot-check 5 random accounts
- Verify Decimal precision
- **CHECKPOINT 4:** Final approval
```

**Files to Create:**
- `.claude/commands/prod/extract-databricks.md`

**Dependencies:**
- `databricks-extractor` skill (auto-invoked)
- `@databricks-validator` agent (manual invoke in Step 4)
- `decimal-precision-enforcer` skill (auto-invoked)
- `audit-trail-enforcer` skill (auto-invoked)

---

### 2.4-2.6: Adaptive Insights Extraction (Similar Structure)

**Components:**
- `adaptive-extractor` skill (pattern similar to databricks-extractor)
- `@adaptive-validator` agent (pattern similar to databricks-validator)
- `/extract-adaptive` command (pattern similar to extract-databricks)

**Key Differences:**
- XML parsing instead of SQL queries
- API rate limit handling
- Version parameter (e.g., "FY 2025 Budget")

**Files to Create:**
- `.claude/skills/prod/adaptive-extractor/SKILL.md`
- `.claude/agents/prod/adaptive-validator.md`
- `.claude/commands/prod/extract-adaptive.md`

---

## Phase 3: Account Reconciliation (Week 4)

### Priority: HIGH (required before variance analysis can run)

**Goal:** Match accounts between Databricks (actuals) and Adaptive (budget).

### 3.1: `account-mapper` Skill

**Pattern:** Technique skill

**Auto-Invocation Triggers:**
- Keywords: "account reconciliation", "account mapping", "unmatched accounts"
- File patterns: `scripts/core/account_mapper.py`

**Behavior:**
```python
# When invoked, provide:
1. Load mapping configuration: config/account_mapping.yaml
2. Fuzzy matching logic for unmapped accounts
3. Suggest mappings based on naming patterns
4. Generate reconciliation report:
   - Matched accounts (count)
   - Unmatched Databricks accounts (list)
   - Unmatched Adaptive accounts (list)
   - Suggested mappings with confidence scores

# References:
- Example: "7000 Sales Salaries" → "70-000 Salaries - Sales"
- Use Levenshtein distance for similarity
```

**Files to Create:**
- `.claude/skills/prod/account-mapper/SKILL.md`
- `.claude/skills/prod/account-mapper/references/fuzzy-matching-examples.md`
- `config/account_mapping.yaml` (template)

**Dependencies:**
- `fuzzywuzzy` or `rapidfuzz` package (add to pyproject.toml)

---

### 3.2: `@account-reconciler` Agent

**Pattern:** Read-Only Researcher

**Tools:** Read, Grep, Glob

**Specialty:** Intelligent account matching with suggestions

**Behavior:**
```markdown
## Reconciliation Analysis

When invoked to reconcile accounts:

1. **Load both account lists:**
   - Databricks accounts from actuals file
   - Adaptive accounts from budget file

2. **Apply mapping configuration:**
   - Load config/account_mapping.yaml
   - Apply known mappings

3. **Identify unmatched accounts:**
   - Databricks accounts not in mapping
   - Adaptive accounts not in mapping

4. **Generate suggestions:**
   - Use fuzzy matching (Levenshtein distance)
   - Rank by confidence (0-100%)
   - Provide top 3 suggestions per unmatched account

5. **Format reconciliation report:**
   - Matched: 45/50 accounts (90%)
   - Unmatched Databricks (5): [list with suggestions]
   - Unmatched Adaptive (3): [list with suggestions]

## Output Format

**RECONCILIATION REPORT:**

Matched Accounts: 45/50 (90%)

Unmatched Databricks Accounts (5):
1. "7005 Digital Marketing" → Suggestions:
   - "70-005 Marketing - Digital" (95% confidence)
   - "70-050 Advertising - Digital" (78% confidence)
   - "60-005 Marketing Expenses" (65% confidence)

...

**RECOMMENDATION:**
- If >90% matched: APPROVE (minor manual fixes)
- If 70-90% matched: NEEDS REVIEW (significant gaps)
- If <70% matched: REJECT (likely data quality issue)
```

**Files to Create:**
- `.claude/agents/prod/account-reconciler.md`

**Dependencies:**
- `account-mapper` skill (uses same fuzzy matching logic)

---

### 3.3: `/reconcile-accounts` Command

**Pattern:** Human Approval Workflow

**Arguments:** `<databricks_file> <adaptive_file> [mapping_file]`

**Workflow:**
```markdown
### STEP 1: Load and Analyze
- Load Databricks actuals file
- Load Adaptive budget file
- Load mapping configuration (or use default)
- Apply known mappings

### STEP 2: Generate Reconciliation Report
- Invoke @account-reconciler agent
- Present reconciliation report with suggestions

### STEP 3: Human Review and Decision
**CHECKPOINT:** User reviews report and chooses:
- Option A: Accept suggested mappings
- Option B: Manual mapping (provide account pairs)
- Option C: Abort and fix data quality issues

### STEP 4: Update Mapping Configuration
- If Option A or B: Update config/account_mapping.yaml
- Save updated mapping
- Re-run reconciliation to verify 100% match

### STEP 5: Output
- Generate final reconciliation report
- Save matched accounts to output file
- Log audit entry
```

**Files to Create:**
- `.claude/commands/prod/reconcile-accounts.md`

**Dependencies:**
- `account-mapper` skill (auto-invoked)
- `@account-reconciler` agent (manual invoke in Step 2)

---

## Phase 4: Reporting (Week 5-6)

### Priority: MEDIUM (depends on variance analysis being complete)

**Goal:** Generate Excel reports and update Google Slides presentations.

### 4.1: `excel-report-generator` Skill

**Pattern:** Technique skill

**Auto-Invocation Triggers:**
- Keywords: "excel report", "variance report", "generate report"
- File patterns: `scripts/reporting/excel*.py`

**Behavior:**
```python
# When invoked, provide:
1. Use xlsxwriter for formatted Excel output (not openpyxl for writing)
2. Create multi-sheet workbook structure:
   - Sheet 1: Executive Summary
   - Sheet 2: Detailed Variance Analysis
   - Sheet 3: Material Variances Only
   - Sheet 4: Metadata
3. Apply conditional formatting:
   - Green: Favorable & Material
   - Red: Unfavorable & Material
   - Yellow: Favorable but Immaterial
   - Gray: Unfavorable but Immaterial
4. Number formatting:
   - Currency: $#,##0.00
   - Percentage: 0.00%
5. Embed metadata:
   - Generation timestamp
   - Source files
   - Thresholds applied

# References:
- xlsxwriter documentation
- templates/variance_report.xlsx (example structure)
```

**Files to Create:**
- `.claude/skills/prod/excel-report-generator/SKILL.md`
- `.claude/skills/prod/excel-report-generator/references/formatting-guide.md`
- `templates/variance_report.xlsx` (template with desired structure)

**Dependencies:**
- `xlsxwriter` package (add to pyproject.toml)

---

### 4.2: `@report-formatter` Agent

**Pattern:** Read-Only Researcher

**Tools:** Read, Grep, Glob

**Specialty:** Excel output validation

**Behavior:**
```markdown
## Excel Validation Checklist

When invoked to validate Excel report:

1. **Sheet Structure:**
   - [ ] Executive Summary sheet exists
   - [ ] Detailed Analysis sheet exists
   - [ ] Material Variances sheet exists
   - [ ] Metadata sheet exists

2. **Column Headers:**
   - [ ] All required columns present
   - [ ] Headers match spec (Account, Budget, Actual, Variance $, Variance %, Favorable, Material)

3. **Formatting:**
   - [ ] Currency columns formatted as $#,##0.00
   - [ ] Percentage columns formatted as 0.00%
   - [ ] Conditional formatting applied

4. **Data Validation:**
   - [ ] No #DIV/0! errors
   - [ ] No #VALUE! errors
   - [ ] Material flag logic correct

5. **Metadata:**
   - [ ] Timestamp present
   - [ ] Source files documented
   - [ ] Thresholds documented

## Output Format

**VALIDATION REPORT:**
- [ ] Sheet structure: PASS/FAIL
- [ ] Column headers: PASS/FAIL
- [ ] Formatting: PASS/FAIL
- [ ] Data validation: PASS/FAIL
- [ ] Metadata: PASS/FAIL

**RECOMMENDATION:** APPROVE / REJECT / NEEDS REVISION
```

**Files to Create:**
- `.claude/agents/prod/report-formatter.md`

**Dependencies:** None (read-only validation)

---

### 4.3: `/generate-excel-report` Command

**Pattern:** Data Transformation Workflow

**Arguments:** `<variance_data_file> [output_file] [template]`

**Workflow:**
```markdown
### STEP 1: Load Variance Data
- Load variance analysis results (CSV or Excel)
- Validate data structure (required columns present)

### STEP 2: Transform and Format
- Group by account type for Executive Summary
- Filter to material variances for Material sheet
- Apply conditional formatting rules

### STEP 3: Generate Workbook
- Create multi-sheet workbook using xlsxwriter
- Apply number formatting
- Add conditional formatting
- Embed metadata

### STEP 4: Validate Output
- Invoke @report-formatter agent
- **CHECKPOINT:** Review validation report
- Fix any issues found

### STEP 5: Save and Log
- Save Excel file to output path
- Log audit entry
- Display success message with file location
```

**Files to Create:**
- `.claude/commands/prod/generate-excel-report.md`

**Dependencies:**
- `excel-report-generator` skill (auto-invoked)
- `@report-formatter` agent (manual invoke in Step 4)

---

## Phase 5: Google Integration (Week 7-9)

### Priority: MEDIUM (nice-to-have, not critical path)

**Goal:** Update Google Slides and Google Sheets with variance results.

### 5.1-5.3: Google Slides Updater

**Components:**
- `google-slides-updater` skill
- `@slides-previewer` agent
- `/update-google-slides` command

**Key Features:**
- OAuth or Service Account authentication
- Placeholder detection (e.g., `{{REVENUE_ACTUAL}}`)
- Preview before applying changes
- Update "Last Updated" timestamp

**Files to Create:**
- `.claude/skills/prod/google-slides-updater/SKILL.md`
- `.claude/agents/prod/slides-previewer.md`
- `.claude/commands/prod/update-google-slides.md`

**Dependencies:**
- `google-api-python-client` package
- `google-auth` package
- OAuth credentials or Service Account JSON

---

### 5.4-5.6: Google Sheets Updater

**Components:**
- `google-sheets-updater` skill
- `/update-google-sheets` command

**Key Features:**
- `gspread` library integration
- Append or replace data modes
- Preserve formulas and formatting

**Files to Create:**
- `.claude/skills/prod/google-sheets-updater/SKILL.md`
- `.claude/commands/prod/update-google-sheets.md`

**Dependencies:**
- `gspread` package
- `gspread-dataframe` package (optional, simplifies DataFrame → Sheets)

---

## Phase 6: Forecast Maintenance (Week 10-11)

### Priority: LOW (Phase 2 feature, not MVP)

**Goal:** Update rolling forecasts with actuals and track assumption changes.

### 6.1-6.4: Rolling Forecast Updater

**Components:**
- `forecast-updater` skill
- `@forecast-validator` agent
- `/update-rolling-forecast` command

**Key Features:**
- Identify closed periods (have actuals)
- Replace forecast with actuals for closed periods
- Extend forecast window forward
- Preserve forecast formulas for future periods

**Files to Create:**
- `.claude/skills/prod/forecast-updater/SKILL.md`
- `.claude/agents/prod/forecast-validator.md`
- `.claude/commands/prod/update-rolling-forecast.md`

---

### 6.5-6.7: Assumption Tracker

**Components:**
- `assumption-tracker` skill
- `@assumption-analyzer` agent
- `/track-forecast-assumptions` command

**Key Features:**
- Prompt user for assumption changes
- Log changes with timestamp and user
- Compare actual trends to assumptions
- Suggest recalibrations

**Files to Create:**
- `.claude/skills/prod/assumption-tracker/SKILL.md`
- `.claude/agents/prod/assumption-analyzer.md`
- `.claude/commands/prod/track-forecast-assumptions.md`

---

## Phase 7 ➡️ ACTUAL PHASE 1: Development Workflows ⭐ **IMPLEMENT FIRST** (Week 1-2)

### Priority: CRITICAL - IMPLEMENT BEFORE ALL OTHER PHASES

**🚨 RESEQUENCED:** This is Phase 7 in the document, but **Phase 1 in implementation order**.

**Goal:** Build the tools to build tools - enable automated component generation with TDD workflow.

**Why First:**
- Cannot efficiently build 34 components manually
- Provides automated script generation for all subsequent phases
- Ensures consistency and quality from day 1
- TDD workflow catches financial calculation errors early

### 7.1: `python-best-practices` Skill

**Pattern:** Discipline skill

**Auto-Invocation Triggers:**
- Always auto-invoke when generating Python code
- Keywords: "script", "function", "class", "python"

**Behavior:**
```python
# When invoked, enforce:
1. Type hints on ALL functions
2. Docstrings (Google style) on ALL functions
3. Error handling (no bare except, no silent failures)
4. Logging for all significant operations
5. Audit trail for data transformations
6. Decimal for currency (delegates to decimal-precision-enforcer)

# If violations found:
- Block code generation
- Provide template with correct structure
- Reference: plan.md code quality standards section
```

**Files to Create:**
- `.claude/skills/dev/python-best-practices/SKILL.md`
- `.claude/skills/dev/python-best-practices/references/code-template.py`
- `.claude/skills/dev/python-best-practices/references/docstring-template.md`

---

### 7.2: `test-suite-generator` Skill

**Pattern:** Technique skill

**Auto-Invocation Triggers:**
- Keywords: "test", "pytest", "unit test", "edge case"
- File patterns: `tests/unit/*.py`, `tests/integration/*.py`

**Behavior:**
```python
# When invoked, generate:
1. Parametrized tests for all account types
2. Edge case tests from financial-validator references:
   - Division by zero (3 scenarios)
   - Negative values
   - NULL handling
   - Boundary conditions
3. Test fixtures for sample data
4. Coverage configuration (>95% required)

# Structure:
- tests/unit/ for fast isolated tests
- tests/integration/ for API tests
- tests/fixtures/conftest.py for shared fixtures

# References:
- .claude/skills/financial-validator/references/edge-cases.md
- plan.md testing strategy section
```

**Files to Create:**
- `.claude/skills/dev/test-suite-generator/SKILL.md`
- `.claude/skills/dev/test-suite-generator/references/test-template.py`
- `.claude/skills/dev/test-suite-generator/references/fixture-examples.py`

---

### 7.3-7.5: Script Generation Agents

**Components:**
- `@script-generator` agent (Full Access Implementer - can Write/Edit)
- `@test-generator` agent (Full Access Implementer - can Write/Edit)
- `@script-validator` agent (Read + Bash for running validation)

**Behavior:**

**@script-generator:**
- Reads specification
- Writes Python script using TDD workflow
- Uses Decimal precision, type hints, docstrings, error handling
- Logs audit trail

**@test-generator:**
- Reads script implementation
- Generates comprehensive test suite
- Covers all edge cases from financial-validator
- Ensures >95% coverage

**@script-validator:**
- Runs pytest, mypy, ruff, bandit, coverage
- Generates validation report
- PASS/FAIL decision

**Files to Create:**
- `.claude/agents/dev/script-generator.md`
- `.claude/agents/dev/test-generator.md`
- `.claude/agents/dev/script-validator.md`

---

### 7.6-7.8: Development Commands

**Commands:**
- `/create-script` - Generate new financial script with TDD
- `/validate-script` - Run validation suite
- `/review-code` - Request code review from @code-reviewer

**Workflows:**

**/create-script:**
```markdown
### STEP 1: RESEARCH Phase
- User describes what script should do
- Research existing patterns in scripts/
- Identify reusable components
- **CHECKPOINT 1:** Present research findings

### STEP 2: PLAN Phase
- Generate formal specification
- Define function signatures with type hints
- Identify edge cases to handle
- **CHECKPOINT 2:** Present specification

### STEP 3: IMPLEMENT Phase (TDD)
- Invoke @test-generator to write failing tests (RED)
- Invoke @script-generator to implement (GREEN)
- Refactor: Add docstrings, error handling, logging (REFACTOR)
- **CHECKPOINT 3:** Review implementation

### STEP 4: VERIFY Phase
- Invoke @script-validator to run validation suite
- Invoke @code-reviewer for independent review
- **CHECKPOINT 4:** Final approval before saving to scripts/
```

**Files to Create:**
- `.claude/commands/dev/create-script.md`
- `.claude/commands/dev/validate-script.md`
- `.claude/commands/dev/review-code.md`

---

## Phase 8: Orchestration (Week 14)

### Priority: LOW (combines all production workflows)

**Goal:** Single command to run entire monthly close process.

### 8.1: `/prod:monthly-close` Command

**Pattern:** Orchestration Workflow

**Arguments:** `<month> <year>`

**Workflow:**
```markdown
### Overview
This command orchestrates the entire post-close workflow:
1. Extract data (Databricks + Adaptive)
2. Reconcile accounts
3. Calculate variances
4. Generate reports
5. Update dashboards

### Execution Flow

**Phase 1: Data Extraction**
- Run: /extract-databricks <month> <year>
- Run: /extract-adaptive "FY 2025 Budget" <month> <year>
- **CHECKPOINT 1:** Verify extraction successful

**Phase 2: Account Reconciliation**
- Run: /reconcile-accounts <databricks_file> <adaptive_file>
- **CHECKPOINT 2:** Review reconciliation report, approve mappings

**Phase 3: Variance Analysis**
- Run: /variance-analysis <budget_file> <actuals_file>
- **CHECKPOINT 3:** Review variance results

**Phase 4: Report Generation**
- Run: /generate-excel-report <variance_data_file>
- Run: /update-google-slides <presentation_id> <variance_data_file> --preview
- Run: /update-google-sheets <spreadsheet_id> <sheet_name> <variance_data_file>
- **CHECKPOINT 4:** Review reports and dashboards

**Phase 5: Finalization**
- Display summary:
  - Total accounts: 50
  - Material variances: 6
  - Reports generated: 3
  - Time saved: [TO BE MEASURED]
- Log audit entry for entire workflow
```

**Error Handling:**
- If any step fails, save state to `config/workflow-state/monthly-close-{YYYY-MM}.json`
- User can resume with: `/prod:monthly-close <month> <year> --resume`

**Files to Create:**
- `.claude/commands/prod/monthly-close.md`

**Dependencies:**
- All production commands from Phases 1-5
- Workflow state management (see plan.md Section 5: Error Recovery)

---

## Implementation Order Summary

**Week 1: Shared Foundation**
1. `decimal-precision-enforcer` skill
2. `audit-trail-enforcer` skill
3. `/setup` command

**Week 2-3: Data Extraction**
4. `databricks-extractor` skill
5. `@databricks-validator` agent
6. `/extract-databricks` command
7. `adaptive-extractor` skill
8. `@adaptive-validator` agent
9. `/extract-adaptive` command

**Week 4: Account Reconciliation**
10. `account-mapper` skill
11. `@account-reconciler` agent
12. `/reconcile-accounts` command

**Week 5-6: Reporting**
13. `excel-report-generator` skill
14. `@report-formatter` agent
15. `/generate-excel-report` command

**Week 7-9: Google Integration**
16. `google-slides-updater` skill
17. `@slides-previewer` agent
18. `/update-google-slides` command
19. `google-sheets-updater` skill
20. `/update-google-sheets` command

**Week 10-11: Forecast Maintenance**
21. `forecast-updater` skill
22. `@forecast-validator` agent
23. `/update-rolling-forecast` command
24. `assumption-tracker` skill
25. `@assumption-analyzer` agent
26. `/track-forecast-assumptions` command

**Week 12-13: Development Workflows**
27. `python-best-practices` skill
28. `test-suite-generator` skill
29. `@script-generator` agent
30. `@test-generator` agent
31. `@script-validator` agent
32. `/create-script` command
33. `/validate-script` command
34. `/review-code` command

**Week 14: Orchestration**
35. `/prod:monthly-close` command

---

## Quality Gates

### Per-Component Checklist

Before marking any component complete:

**For Skills:**
- [ ] SKILL.md file created with YAML frontmatter
- [ ] Progressive Disclosure pattern followed
- [ ] Auto-invocation triggers documented
- [ ] References directory created (if needed)
- [ ] Tested with sample scenario

**For Agents:**
- [ ] Agent markdown file created with YAML frontmatter
- [ ] Tool permissions specified correctly (Read-only vs Full Access)
- [ ] Specialty and role clearly documented
- [ ] Output format template provided
- [ ] Tested with invocation scenario

**For Commands:**
- [ ] Command markdown file created with description
- [ ] Arguments documented with examples
- [ ] RPIV or appropriate workflow pattern followed
- [ ] Human checkpoints clearly marked
- [ ] Success criteria listed
- [ ] Anti-patterns documented
- [ ] Tested with sample data

**For ALL Components:**
- [ ] Independent verification by @code-reviewer (if applicable)
- [ ] Human approval received before marking complete
- [ ] Documentation updated (README if needed)
- [ ] Git commit with clear message

---

## Dependencies & Prerequisites

### Python Packages to Add

**Add to pyproject.toml:**
```toml
[tool.poetry.dependencies]
# Existing
pandas = "^2.2.0"
openpyxl = "^3.1.2"

# New additions
xlsxwriter = "^3.1.9"              # Excel writing with formatting
databricks-sql-connector = "^3.0"   # Databricks extraction
google-api-python-client = "^2.150" # Google Slides/Sheets
google-auth = "^2.35"               # Google authentication
gspread = "^6.1"                    # Google Sheets simplified
gspread-dataframe = "^4.0"          # DataFrame → Sheets conversion
rapidfuzz = "^3.0"                  # Fuzzy account matching
```

### Configuration Files to Create

1. `config/account_mapping.yaml` (template)
2. `config/fpa_config.yaml` (thresholds, formatting rules)
3. `config/credentials/.gitignore` (ignore all credential files)
4. `.git/hooks/pre-commit` (quality gates)
5. `templates/variance_report.xlsx` (example structure)

### External API Specifications

**Required (per spec.md):**
- `specs/databricks/DATABRICKS_API_SPEC.md` - Databricks SQL warehouse API
- `specs/adaptive/ADAPTIVE_API_SPEC.md` - Adaptive Insights API
- `specs/google/GOOGLE_WORKSPACE_SPEC.md` - Google Slides/Sheets API

**Status:** To be created (reference external API documentation)

---

## Testing Strategy

### Per-Component Testing

**Skills:**
- Test auto-invocation triggers
- Test with intentional violations → Should block
- Test with correct usage → Should pass

**Agents:**
- Test with valid input → Should approve
- Test with invalid input → Should reject
- Test output format matches template

**Commands:**
- Test with sample data (use `data/samples/`)
- Test each checkpoint (human approval)
- Test error handling (missing files, invalid data)

### Integration Testing

**End-to-End Workflows:**
- Run `/prod:monthly-close` with sample data
- Verify all steps complete successfully
- Verify audit trail logged
- Verify output files generated correctly

---

## Rollout Strategy

### Incremental Release

**Phase 1 Release: Variance Analysis (Current)**
- ✅ `/variance-analysis` command
- ✅ `variance-analyzer` skill
- ✅ `@code-reviewer` agent
- ✅ `financial-validator` skill

**Phase 2 Release: Data Extraction**
- Add Databricks extraction
- Add Adaptive extraction
- Add account reconciliation

**Phase 3 Release: Reporting**
- Add Excel report generation
- Optional: Google integration

**Phase 4 Release: Full Automation**
- Add orchestration command
- Add forecast maintenance
- Add development workflows

---

## Success Metrics

### Component-Level Metrics

**Per Command:**
- [ ] Executes without errors on sample data
- [ ] Human checkpoints work as expected
- [ ] Output matches specification
- [ ] Audit trail logged correctly

**Per Agent:**
- [ ] Provides accurate validation/analysis
- [ ] Output format consistent with template
- [ ] No false approvals (strict review)

**Per Skill:**
- [ ] Auto-invokes when expected
- [ ] Blocks violations correctly
- [ ] Provides helpful guidance

### Project-Level Metrics

- [ ] All 34 new components created
- [ ] 100% of components pass quality gates
- [ ] End-to-end monthly close workflow executes successfully
- [ ] User documentation complete
- [ ] Setup time for new user: <30 minutes

---

## Open Questions & Decisions

### 1. Command Invocation from Other Commands

**Question:** Can `/prod:monthly-close` invoke `/extract-databricks` directly, or does it need to duplicate logic?

**Options:**
- A: Invoke other commands (DRY, but may have nesting issues)
- B: Duplicate workflow inline (more control, but not DRY)
- C: Call Python scripts directly (bypasses command checkpoints)

**Recommendation:** Option A (invoke other commands) - Test with simple example first

---

### 2. Google Authentication Method

**Question:** OAuth or Service Account JSON for Google integration?

**Options:**
- A: OAuth (user-specific, more secure, requires browser)
- B: Service Account (shared account, simpler setup, no browser)
- C: Support both (flexible, but more complexity)

**Recommendation:** Option C (support both) - Let user choose based on their IT policies

---

### 3. Pre-Commit Hook Automation

**Question:** Should `/setup` command install pre-commit hooks automatically?

**Options:**
- A: Yes, automatic (better enforcement, but users lose control)
- B: No, manual (user choice, but may forget)
- C: Prompt user (ask during setup)

**Recommendation:** Option C (prompt user) - Explain benefits and ask permission

---

## Next Steps

1. ✅ Research complete (research.md)
2. ✅ Plan complete (plan.md)
3. ⏳ Create validation checklist (checklist.md)
4. ⏳ Update spec.md with meta-infrastructure epic
5. ⏳ Update plan.md with phase-by-phase implementation
6. ⏳ **CHECKPOINT:** Present plan for human approval

---

**Planning Status:** ✅ COMPLETE
**Ready for:** Checklist Creation and spec.md/plan.md Updates
