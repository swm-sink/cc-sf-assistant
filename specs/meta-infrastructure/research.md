# Meta-Infrastructure Research: Commands, Agents, and Skills

**Version:** 1.0-DRAFT
**Date:** 2025-11-09
**Status:** 🔬 RESEARCH PHASE
**Purpose:** Identify all commands, agents, and skills needed to support FP&A automation per spec.md

---

## Research Scope

Analyze spec.md Epics 1-4 to identify:
1. **Commands** - User-facing slash commands (e.g., `/variance-analysis`)
2. **Agents** - Specialized subagents for specific tasks (e.g., `@code-reviewer`)
3. **Skills** - Auto-invoked capabilities (e.g., `financial-validator`)

**Methodology:** Map each user story to required infrastructure components.

---

## Epic 1: Post-Close Variance Analysis

**Workflow:** Close (External) → Extract → Analyze → Review → Adjust → Finalize → Report

### Story 1.1: Extract Actuals from Databricks

**Required Infrastructure:**

**Commands:**
- `/extract-databricks` - Extract monthly actuals from Databricks SQL warehouse
  - Arguments: `<month> <year> [output_file]`
  - Pattern: RPIV workflow with human checkpoints
  - Phases: Research (inspect schema) → Plan (query design) → Implement (execute extraction) → Verify (data validation)

**Agents:**
- `@databricks-validator` - Validate Databricks query results
  - Tools: Read, Grep, Glob (read-only)
  - Specialty: SQL query verification, data type validation, NULL handling
  - Validates extracted data before saving

**Skills:**
- `databricks-extractor` - Auto-invoked for Databricks extraction
  - Provides retry logic, async execution, connection handling
  - References: `specs/databricks/DATABRICKS_API_SPEC.md`

---

### Story 1.2: Extract Budget from Adaptive Insights

**Required Infrastructure:**

**Commands:**
- `/extract-adaptive` - Extract budget data from Adaptive Insights
  - Arguments: `<version_name> <month> <year> [output_file]`
  - Pattern: RPIV workflow with human checkpoints
  - Handles XML parsing, account reconciliation

**Agents:**
- `@adaptive-validator` - Validate Adaptive API responses
  - Tools: Read, Grep, Glob (read-only)
  - Specialty: XML parsing validation, account reconciliation
  - Flags unmatched accounts for review

**Skills:**
- `adaptive-extractor` - Auto-invoked for Adaptive extraction
  - Provides API rate limit handling, exponential backoff retry
  - XML parsing and data structure conversion
  - References: `specs/adaptive/ADAPTIVE_API_SPEC.md`

---

### Story 1.3: Account Reconciliation (Implicit Requirement)

**Required Infrastructure:**

**Commands:**
- `/reconcile-accounts` - Reconcile accounts between Databricks and Adaptive
  - Arguments: `<databricks_file> <adaptive_file> [mapping_file]`
  - Pattern: Human-in-loop approval for unmapped accounts
  - Generates reconciliation report with suggested mappings

**Agents:**
- `@account-reconciler` - Intelligent account matching
  - Tools: Read, Grep, Glob (read-only)
  - Specialty: Fuzzy matching, pattern detection, mapping suggestions
  - Uses account naming conventions to suggest matches

**Skills:**
- `account-mapper` - Auto-invoked for account mapping tasks
  - Loads mapping configuration from `config/account_mapping.yaml`
  - Flags unmatched accounts
  - Suggests mappings based on naming patterns

---

## Epic 2: Variance Analysis Automation

### Story 2.1, 2.2, 2.3: Variance Calculation, Favorability, Materiality

**Required Infrastructure:**

**Commands:**
- ✅ `/variance-analysis` - **ALREADY CREATED**
  - Status: Implemented
  - Pattern: RPIV workflow
  - Location: `.claude/commands/prod/variance-analysis.md`

**Agents:**
- ✅ `@code-reviewer` - **ALREADY CREATED**
  - Status: Implemented
  - Location: `.claude/agents/code-reviewer.md`

**Skills:**
- ✅ `variance-analyzer` - **ALREADY CREATED**
  - Status: Implemented
  - Location: `.claude/skills/variance-analyzer/SKILL.md`
- ✅ `financial-validator` - **ALREADY CREATED**
  - Status: Implemented
  - Location: `.claude/skills/financial-validator/SKILL.md`

**Additional Skills Needed:**
- `decimal-precision-enforcer` - Auto-invoked to block float usage
  - Checks all financial calculations use Decimal type
  - Raises error if float detected in currency operations
  - References: `.claude/skills/financial-validator/references/edge-cases.md`

---

## Epic 3: Management Reporting

### Story 3.1: Variance Report Generation (Excel)

**Required Infrastructure:**

**Commands:**
- `/generate-excel-report` - Generate formatted Excel variance report
  - Arguments: `<variance_data_file> [output_file] [template]`
  - Pattern: Data Transformation workflow
  - Creates 3-sheet workbook with conditional formatting

**Agents:**
- `@report-formatter` - Validate Excel output formatting
  - Tools: Read (can open and inspect Excel files)
  - Specialty: Excel structure validation, formatting verification
  - Checks: Sheet presence, column headers, conditional formatting applied

**Skills:**
- `excel-report-generator` - Auto-invoked for Excel report generation
  - Uses `openpyxl` for reading, `xlsxwriter` for writing (formatting)
  - Applies conditional formatting rules from `config/fpa_config.yaml`
  - Embeds metadata (timestamp, source files, thresholds)

---

### Story 3.2: Executive Dashboard Updates (Google Slides)

**Required Infrastructure:**

**Commands:**
- `/update-google-slides` - Update Google Slides presentation with latest data
  - Arguments: `<presentation_id> <data_file> [--preview]`
  - Pattern: Human Approval workflow (preview before applying)
  - Replaces placeholders (e.g., `{{REVENUE_ACTUAL}}`) with values

**Agents:**
- `@slides-previewer` - Generate preview of changes before applying
  - Tools: Read, Grep, Glob (read-only)
  - Specialty: Placeholder detection, change preview generation
  - Shows before/after comparison for human approval

**Skills:**
- `google-slides-updater` - Auto-invoked for Google Slides updates
  - Authenticates via OAuth or Service Account
  - Detects placeholders in slides
  - Updates chart data sources
  - Updates "Last Updated" timestamp
  - References: `specs/google/GOOGLE_WORKSPACE_SPEC.md`

---

### Additional Reporting Requirements

**Commands:**
- `/update-google-sheets` - Update Google Sheets with variance results
  - Arguments: `<spreadsheet_id> <sheet_name> <data_file>`
  - Pattern: Data Transformation workflow
  - Appends or replaces data in specified sheet

**Skills:**
- `google-sheets-updater` - Auto-invoked for Google Sheets updates
  - Uses `gspread` library
  - Handles authentication
  - Preserves formulas and formatting where possible

---

## Epic 4: Rolling Forecast Maintenance

### Story 4.1: Actuals Integration into Forecast

**Required Infrastructure:**

**Commands:**
- `/update-rolling-forecast` - Replace forecast with actuals for closed periods
  - Arguments: `<forecast_file> <actuals_file> <output_file>`
  - Pattern: Human Approval workflow
  - Shows which periods will be replaced (preview)
  - Extends forecast window forward

**Agents:**
- `@forecast-validator` - Validate forecast update logic
  - Tools: Read, Grep, Glob (read-only)
  - Specialty: Period matching, date range validation
  - Ensures actuals are correctly substituted for forecast

**Skills:**
- `forecast-updater` - Auto-invoked for forecast updates
  - Identifies closed periods (have actuals)
  - Replaces forecast values with actuals
  - Extends forecast window forward
  - Preserves forecast formulas for future periods

---

### Story 4.2: Assumption Recalibration Tracking

**Required Infrastructure:**

**Commands:**
- `/track-forecast-assumptions` - Document assumption changes
  - Arguments: `<forecast_period> [assumption_type]`
  - Pattern: Reflection workflow
  - Prompts user for assumption changes
  - Stores in assumption change log

**Agents:**
- `@assumption-analyzer` - Suggest assumption updates based on actuals
  - Tools: Read, Grep, Glob (read-only)
  - Specialty: Trend analysis, variance pattern detection
  - Suggests assumption recalibrations based on actual trends

**Skills:**
- `assumption-tracker` - Auto-invoked for assumption tracking
  - Loads previous assumptions from log
  - Compares actual trends to assumptions
  - Generates suggested updates
  - Logs changes with timestamp and user

---

## Development & Shared Commands

### Development Workflows

**Commands:**
- `/create-script` - Generate new financial calculation script
  - Arguments: `<description> [output_file]`
  - Pattern: RPIV workflow (enforced by `enforcing-research-plan-implement-verify` skill)
  - Phases: Research existing patterns → Plan specification → Implement TDD → Verify with code review

- `/validate-script` - Run validation suite on script
  - Arguments: `<script_path>`
  - Pattern: Validation workflow
  - Runs: pytest, mypy, ruff, bandit, coverage (>95% required)

- `/review-code` - Request independent code review
  - Arguments: `<file_path> [focus_area]`
  - Pattern: Invokes `@code-reviewer` agent
  - Provides structured feedback

**Agents (Development):**
- `@script-generator` - Generate Python scripts from specifications
  - Tools: Read, Write, Edit (full access for generation)
  - Specialty: TDD workflow, Decimal precision, financial edge cases

- `@test-generator` - Generate comprehensive test suites
  - Tools: Read, Write, Edit (full access for test generation)
  - Specialty: Edge case identification, parametrized tests, fixtures

- `@script-validator` - Run automated validation pipeline
  - Tools: Bash, Read (execute tests and linters)
  - Specialty: pytest, mypy, ruff, bandit, coverage reporting

**Skills (Development):**
- ✅ `enforcing-research-plan-implement-verify` - **ALREADY CREATED**
  - Auto-invoked when about to implement features/fixes
  - Enforces RPIV workflow with human checkpoints

- `python-best-practices` - Auto-invoked for Python code generation
  - Enforces type hints, docstrings, error handling
  - Blocks code without audit logging

- `test-suite-generator` - Auto-invoked for test generation
  - Uses edge cases from `financial-validator` references
  - Generates parametrized tests for all account types
  - Ensures >95% coverage requirement

---

### Shared Workflows

**Commands:**
- ✅ `/shared:sync-docs` - **ALREADY CREATED**
  - Validate documentation consistency
  - Location: `.claude/commands/shared/sync-docs.md`

- `/setup` - Initial project setup
  - Pattern: Orchestration workflow
  - Installs pre-commit hooks
  - Validates dependencies
  - Creates config directories
  - Guides user through credential setup

**Skills (Shared):**
- `decimal-precision-enforcer` - Auto-invoked for ALL financial operations
  - Blocks float usage in currency calculations
  - Enforces Decimal type
  - Checks imports include `from decimal import Decimal, ROUND_HALF_UP`

- `audit-trail-enforcer` - Auto-invoked for ALL data transformations
  - Ensures logging includes: timestamp, user, source files, operation
  - Validates audit log structure
  - References centralized audit log: `config/audit.log`

---

## Meta-Skills (Already Created)

**Skills for Creating Infrastructure:**
- ✅ `creating-commands` - **ALREADY CREATED**
  - Templates: RPIV, Human Approval, Batch Processing, Validation, Reporting, etc.
  - Location: `.claude/skills/creating-commands/`

- ✅ `creating-agents` - **ALREADY CREATED**
  - Templates: Domain Specialist, Read-Only Researcher, Full Access Implementer
  - Location: `.claude/skills/creating-agents/`

- ✅ `creating-skills` - **ALREADY CREATED**
  - Templates: Technique, Pattern, Discipline, Reference
  - Location: `.claude/skills/creating-skills/`

---

## Summary: Infrastructure Inventory

### Commands Needed

**Production (10 commands):**
1. ✅ `/variance-analysis` - ALREADY CREATED
2. ⏳ `/extract-databricks` - TO BE CREATED
3. ⏳ `/extract-adaptive` - TO BE CREATED
4. ⏳ `/reconcile-accounts` - TO BE CREATED
5. ⏳ `/generate-excel-report` - TO BE CREATED
6. ⏳ `/update-google-slides` - TO BE CREATED
7. ⏳ `/update-google-sheets` - TO BE CREATED
8. ⏳ `/update-rolling-forecast` - TO BE CREATED
9. ⏳ `/track-forecast-assumptions` - TO BE CREATED
10. ⏳ `/prod:monthly-close` - Orchestration command (combines multiple workflows)

**Development (3 commands):**
11. ⏳ `/create-script` - TO BE CREATED
12. ⏳ `/validate-script` - TO BE CREATED
13. ⏳ `/review-code` - TO BE CREATED

**Shared (2 commands):**
14. ✅ `/shared:sync-docs` - ALREADY CREATED
15. ⏳ `/setup` - TO BE CREATED

**Total:** 15 commands (3 created, 12 to be created)

---

### Agents Needed

**Production (6 agents):**
1. ✅ `@code-reviewer` - ALREADY CREATED
2. ⏳ `@databricks-validator` - TO BE CREATED
3. ⏳ `@adaptive-validator` - TO BE CREATED
4. ⏳ `@account-reconciler` - TO BE CREATED
5. ⏳ `@report-formatter` - TO BE CREATED
6. ⏳ `@slides-previewer` - TO BE CREATED
7. ⏳ `@forecast-validator` - TO BE CREATED
8. ⏳ `@assumption-analyzer` - TO BE CREATED

**Development (3 agents):**
9. ⏳ `@script-generator` - TO BE CREATED
10. ⏳ `@test-generator` - TO BE CREATED
11. ⏳ `@script-validator` - TO BE CREATED

**Total:** 11 agents (1 created, 10 to be created)

---

### Skills Needed

**Production (9 skills):**
1. ✅ `variance-analyzer` - ALREADY CREATED
2. ✅ `financial-validator` - ALREADY CREATED
3. ⏳ `databricks-extractor` - TO BE CREATED
4. ⏳ `adaptive-extractor` - TO BE CREATED
5. ⏳ `account-mapper` - TO BE CREATED
6. ⏳ `excel-report-generator` - TO BE CREATED
7. ⏳ `google-slides-updater` - TO BE CREATED
8. ⏳ `google-sheets-updater` - TO BE CREATED
9. ⏳ `forecast-updater` - TO BE CREATED
10. ⏳ `assumption-tracker` - TO BE CREATED

**Development (2 skills):**
11. ⏳ `python-best-practices` - TO BE CREATED
12. ⏳ `test-suite-generator` - TO BE CREATED

**Shared (2 skills):**
13. ⏳ `decimal-precision-enforcer` - TO BE CREATED
14. ⏳ `audit-trail-enforcer` - TO BE CREATED

**Meta-Skills (Already Created):**
15. ✅ `creating-commands` - ALREADY CREATED
16. ✅ `creating-agents` - ALREADY CREATED
17. ✅ `creating-skills` - ALREADY CREATED
18. ✅ `enforcing-research-plan-implement-verify` - ALREADY CREATED

**Total:** 18 skills (6 created, 12 to be created)

---

## Research Findings

### Pattern Analysis

**Most Common Command Patterns:**
1. **RPIV Workflow** (7 commands) - Research → Plan → Implement → Verify with human checkpoints
2. **Human Approval Workflow** (3 commands) - Preview before applying changes
3. **Data Transformation** (2 commands) - Transform and load data
4. **Orchestration** (1 command) - Combine multiple workflows

**Most Common Agent Patterns:**
1. **Read-Only Validators** (6 agents) - Validate without modifying
2. **Full-Access Implementers** (3 agents) - Generate code/scripts
3. **Specialized Analyzers** (2 agents) - Suggest improvements based on analysis

**Most Common Skill Patterns:**
1. **Auto-Invoked Extractors** (4 skills) - Handle external API integrations
2. **Auto-Invoked Enforcers** (2 skills) - Block anti-patterns
3. **Auto-Invoked Generators** (2 skills) - Generate reports/outputs

### Dependencies & Relationships

**Dependency Graph:**
```
/variance-analysis (command)
├── variance-analyzer (skill) - Auto-invoked on "variance" mention
├── financial-validator (skill) - Auto-invoked for Decimal enforcement
├── decimal-precision-enforcer (skill) - Blocks float usage
├── audit-trail-enforcer (skill) - Ensures logging
└── @code-reviewer (agent) - Independent verification

/extract-databricks (command)
├── databricks-extractor (skill) - Auto-invoked for Databricks ops
├── decimal-precision-enforcer (skill) - Enforces Decimal
├── audit-trail-enforcer (skill) - Logs extraction
└── @databricks-validator (agent) - Validates query results

/prod:monthly-close (orchestration command)
├── /extract-databricks (command)
├── /extract-adaptive (command)
├── /reconcile-accounts (command)
├── /variance-analysis (command)
├── /generate-excel-report (command)
├── /update-google-slides (command)
└── Multiple agents/skills from above
```

**Critical Shared Dependencies:**
- All financial operations depend on `decimal-precision-enforcer`
- All data transformations depend on `audit-trail-enforcer`
- All command workflows should use RPIV pattern (enforced by `enforcing-research-plan-implement-verify`)

### Implementation Priority

**Phase 1: Core Shared Infrastructure (Week 1)**
- `decimal-precision-enforcer` skill
- `audit-trail-enforcer` skill
- `/setup` command

**Phase 2: Variance Analysis (Already Done)**
- ✅ `/variance-analysis` command
- ✅ `variance-analyzer` skill
- ✅ `@code-reviewer` agent
- ✅ `financial-validator` skill

**Phase 3: Data Extraction (Week 2-3)**
- `/extract-databricks` command
- `/extract-adaptive` command
- `databricks-extractor` skill
- `adaptive-extractor` skill
- `@databricks-validator` agent
- `@adaptive-validator` agent

**Phase 4: Account Reconciliation (Week 4)**
- `/reconcile-accounts` command
- `account-mapper` skill
- `@account-reconciler` agent

**Phase 5: Reporting (Week 5-6)**
- `/generate-excel-report` command
- `excel-report-generator` skill
- `@report-formatter` agent

**Phase 6: Google Integration (Week 7-9)**
- `/update-google-slides` command
- `/update-google-sheets` command
- `google-slides-updater` skill
- `google-sheets-updater` skill
- `@slides-previewer` agent

**Phase 7: Forecast Maintenance (Week 10-11)**
- `/update-rolling-forecast` command
- `/track-forecast-assumptions` command
- `forecast-updater` skill
- `assumption-tracker` skill
- `@forecast-validator` agent
- `@assumption-analyzer` agent

**Phase 8: Development Workflows (Week 12-13)**
- `/create-script` command
- `/validate-script` command
- `/review-code` command
- `python-best-practices` skill
- `test-suite-generator` skill
- `@script-generator` agent
- `@test-generator` agent
- `@script-validator` agent

**Phase 9: Orchestration (Week 14)**
- `/prod:monthly-close` command (combines all prod workflows)

---

## Edge Cases & Considerations

### Authentication & Credentials
- Google Slides/Sheets: OAuth or Service Account JSON
- Databricks: Personal Access Token
- Adaptive Insights: API token
- All stored in `config/credentials/` (git-ignored)

### Error Handling
- Network failures: Exponential backoff retry (all external APIs)
- API rate limits: Respect limits, queue requests if needed
- Data validation failures: Flag for human review, don't silently drop

### Performance
- Large datasets: Chunked processing for >10,000 rows
- Async operations for long-running extractions
- Progress indicators for multi-step workflows

### Security
- Credentials never committed to git
- Audit log for all financial operations
- Read-only agents can't modify financial data

---

## Open Questions

1. **Command Naming Convention:**
   - Prefix production commands with `/prod:`? (e.g., `/prod:variance-analysis`)
   - Or use directory structure only? (current: `.claude/commands/prod/variance-analysis.md`)
   - **Recommendation:** Use directory structure, no prefix (cleaner UX)

2. **Agent Context Isolation:**
   - All validators should be read-only (no Write/Edit tools)
   - All generators need full access (Read/Write/Edit tools)
   - **Recommendation:** Follow creating-agents templates strictly

3. **Skill Auto-Invocation Triggers:**
   - Should `decimal-precision-enforcer` auto-invoke on ALL code generation?
   - Or only when keywords like "financial", "currency", "variance" mentioned?
   - **Recommendation:** Auto-invoke on ALL code generation (safer)

4. **Orchestration Command Structure:**
   - Should `/prod:monthly-close` be single command invoking others?
   - Or should it duplicate workflow inline?
   - **Recommendation:** Invoke other commands (DRY principle)

---

## Next Steps

1. ✅ Research complete - All commands/agents/skills identified
2. ⏳ Create detailed implementation plan (specs/meta-infrastructure/plan.md)
3. ⏳ Update spec.md to include meta-infrastructure epic
4. ⏳ Update plan.md to include phase-by-phase implementation details
5. ⏳ Create validation checklist (specs/meta-infrastructure/checklist.md)

---

**Research Status:** ✅ COMPLETE
**Ready for:** Planning Phase (Human Checkpoint 1)
