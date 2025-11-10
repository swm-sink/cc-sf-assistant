# FP&A Automation Assistant - Product Specification

**Version:** 1.1-DRAFT (Research-Validated)
**Last Updated:** 2025-11-08
**Status:** 🚧 IN REVIEW - Awaiting Stakeholder Validation
**Research Basis:** Industry studies 2024-2025, FP&A Trends Survey, McKinsey AI research
**Product Owner:** [NEEDS ASSIGNMENT]
**Target Users:** Financial Planning & Analysis (FP&A) Professionals

---

## Executive Summary

An intelligent automation assistant designed to eliminate repetitive data collection and consolidation tasks for FP&A professionals, enabling strategic analysis capacity.

**Core Value Proposition:** Transform FP&A from data processors to strategic advisors by automating the monthly close cycle, variance analysis, reporting, and forecast maintenance.

**Research Context:** Industry studies show that FP&A professionals spend only 35% of their time on high-value tasks, with 45% spent on low-value activities like data collection and validation. Finance teams report that over 60% of their time is dedicated to activities that can be automated.

---

## ⚠️ CRITICAL: Development Infrastructure First

**🚨 MANDATORY PREREQUISITE:** Epic 0 (Meta-Infrastructure) MUST be completed BEFORE any business feature implementation (Epics 1-4).

**WHY THIS ORDER IS NON-NEGOTIABLE:**

We are building a **Claude Code-native FP&A automation system** that uses commands, agents, and skills. Before we can build the business features (variance analysis, reporting, forecasts), we MUST first build the development infrastructure that creates those components.

**The Correct Build Sequence:**

```
1. FIRST: Development Infrastructure (Story 0.7)
   └─ Build the tools to build tools
   └─ /create-script, /validate-script, /review-code commands
   └─ @script-generator, @test-generator, @script-validator agents
   └─ python-best-practices, test-suite-generator skills

2. SECOND: Shared Foundation (Story 0.1)
   └─ Build quality enforcement
   └─ decimal-precision-enforcer, audit-trail-enforcer skills
   └─ /setup command

3. THIRD: Production Infrastructure (Stories 0.2-0.6, 0.8)
   └─ Build business feature components using dev tools
   └─ Data extraction, reconciliation, reporting, etc.
   └─ Each created using the development infrastructure from Step 1
```

**What Happens If We Skip This:**
- ❌ Manual script creation → high error rate, inconsistent patterns
- ❌ No automated validation → financial calculation bugs slip through
- ❌ No test generation → insufficient edge case coverage
- ❌ Reinventing the wheel for each component

**What Happens If We Follow This:**
- ✅ Automated script generation with validated templates
- ✅ Every component gets comprehensive test suite automatically
- ✅ Independent code review for financial calculations
- ✅ Consistent patterns enforced across all infrastructure

**Priority:** Development tools (Story 0.7) → Shared foundation (Story 0.1) → Production features (Stories 0.2-0.6, 0.8) → Business features (Epics 1-4)

**See:** [specs/meta-infrastructure/plan.md](specs/meta-infrastructure/plan.md) for resequenced 8-phase implementation plan

---

## Problem Statement

### Current Pain Points

**P1 - Monthly Close Bottleneck**
- Median month-end close cycle takes 6 calendar days; some organizations take 10+ days
- Manual Excel file collection from multiple department heads across the organization
- Data structure inconsistencies require significant reformatting time
- Error-prone copy/paste operations introduce reconciliation issues
- Management waiting for insights while analysts are stuck in Excel
- Manual processes identified as primary bottleneck by 49% of FP&A professionals

**P2 - Variance Analysis Time Sink**
- Budget vs. actual analysis performed manually each month
- 50-100 accounts requiring individual variance calculations
- Favorability logic (revenue up = good, expenses up = bad) applied inconsistently
- Material variances (>10% or >$50K) identified manually through sorting
- Commentary and explanations written from scratch each cycle

**P3 - Presentation Update Burden**
- Board decks and executive dashboards updated manually before every meeting
- Data copied from Excel into Google Slides slide-by-slide
- Charts recreated or manually updated with new data points
- "Last updated" timestamps forgotten, causing confusion
- Time-consuming manual updates divert focus from strategic preparation

**P4 - Rolling Forecast Maintenance Overhead**
- 12-month rolling forecasts updated monthly with latest actuals
- Manual replacement of forecast with actuals for closed periods
- Extension of forecast window forward
- Assumption recalibration based on actual trends performed in isolation
- No centralized documentation of assumption changes

---

## Target Users & Personas

### Primary Persona: Mid-Level FP&A Analyst

**Profile:**
- **Role:** Financial Analyst, Senior Financial Analyst
- **Experience:** 2-5 years in FP&A
- **Technical Skills:** Excel power user, basic SQL, Google Workspace familiarity
- **Daily Workflow:** Majority of time spent on data collection/processing vs. strategic analysis
- **Pain Point:** "I spend all my time collecting and cleaning data. I never have time for the analysis that actually adds value."
- **Research Finding:** Only 35% of FP&A professional time is spent on high-value tasks like generating insights

**Goals:**
- Significantly reduce monthly close cycle time (industry case studies show 10-day → 3-day reductions possible)
- Automate repetitive variance calculations
- Generate management reports faster
- Have time for proactive strategic analysis
- Increase time spent on strategic, high-value activities

**Success Metrics:**
- Hours saved per month
- Reduction in manual errors
- Faster delivery of insights to leadership

### Secondary Persona: FP&A Manager/Director

**Profile:**
- **Role:** FP&A Manager, Director of FP&A
- **Team Size:** 2-8 analysts
- **Responsibilities:** Oversight of budgeting, forecasting, reporting cycles
- **Pain Point:** "My team is stuck in Excel hell. We need them analyzing, not data wrangling."

**Goals:**
- Free team capacity for strategic work
- Ensure consistency in calculations and reporting
- Reduce cycle times for critical deliverables
- Minimize manual error risk

---

## User Stories & Acceptance Criteria

**Phase Validation:** See [specs/PHASE_VALIDATION_CHECKLIST.md](specs/PHASE_VALIDATION_CHECKLIST.md) for exit criteria for each implementation phase.

**Meta-Infrastructure:** See [specs/meta-infrastructure/](specs/meta-infrastructure/) for detailed plan of commands, agents, and skills infrastructure.

---

### Epic 0: Meta-Infrastructure (Foundation)

**Purpose:** Build the commands, agents, and skills infrastructure that enables all FP&A automation workflows.

**Status:** 📋 PLANNED - See [specs/meta-infrastructure/plan.md](specs/meta-infrastructure/plan.md)

**Scope:** This epic covers the creation of Claude Code-native infrastructure components:
- **Commands:** User-facing slash commands (e.g., `/variance-analysis`, `/extract-databricks`)
- **Agents:** Specialized subagents for validation and generation (e.g., `@code-reviewer`, `@databricks-validator`)
- **Skills:** Auto-invoked capabilities for enforcement and patterns (e.g., `decimal-precision-enforcer`, `audit-trail-enforcer`)

**Why This Matters:**
- Commands provide user-friendly interface hiding technical complexity
- Agents provide independent verification and specialized analysis
- Skills enforce quality standards (Decimal precision, audit trails) automatically
- Together, these components ensure financial accuracy and auditability

**Components to Build:** 35 total (10 exist, 25 to create)
- 12 commands (3 exist, 9 to create)
- 8 agents (1 exists, 7 to create)
- 15 skills (6 exist, 9 to create)

**Scope Refinement (2025-11-09):**
- ✅ Databricks and Adaptive use SAME account naming → No reconciliation infrastructure needed
- ✅ Focus on variance analysis and management reporting ONLY → No forecast maintenance
- ⚠️ Materiality thresholds must be centralized config (no magic numbers)

**Implementation Approach:** Research → Plan → Implement → Verify (RPIV workflow)

**Detailed Plan:** [specs/meta-infrastructure/plan.md](specs/meta-infrastructure/plan.md)

**Validation Checklist:** [specs/meta-infrastructure/checklist.md](specs/meta-infrastructure/checklist.md)

---

## 🔧 RESEQUENCED IMPLEMENTATION ORDER

**⚠️ CRITICAL:** Stories are numbered sequentially for reference, but **implementation order is different**.

**ACTUAL IMPLEMENTATION SEQUENCE:**

```
Priority 1: DEVELOPMENT INFRASTRUCTURE (Week 1-2)
  └─ Story 0.7: Development Workflow Infrastructure
     Build the tools to create all other components

Priority 2: SHARED FOUNDATION (Week 3)
  └─ Story 0.1: Shared Foundation Infrastructure
     Build quality enforcement that dev tools will use

Priority 3: PRODUCTION INFRASTRUCTURE (Week 4-9)
  └─ Story 0.2: Data Extraction Infrastructure (Week 4-5)
  └─ Story 0.4: Reporting Infrastructure (Week 6-7)
  └─ Story 0.5: Google Workspace Integration Infrastructure (Week 8-9)
     Build business components using dev tools from Priority 1

Priority 4: ORCHESTRATION (Week 10)
  └─ Story 0.8: Orchestration Infrastructure
     Tie everything together in end-to-end workflow
```

**Removed From Scope:**
- ~~Story 0.3: Account Reconciliation~~ - Databricks & Adaptive use SAME account naming
- ~~Story 0.6: Forecast Maintenance~~ - Focus on variance analysis and reporting only

**Rationale:** We cannot efficiently build production components without development tools (Story 0.7). Building dev infrastructure first ensures every subsequent component gets automated generation, comprehensive testing, and independent review.

**Stories Listed Below:** Stories appear in numerical order for organizational clarity, but **must be implemented in the priority order shown above**.

---

#### Story 0.1: Shared Foundation Infrastructure (Priority 2 - Week 3)

**⚠️ IMPLEMENT AFTER:** Story 0.7 (Development Workflow Infrastructure) is complete

**As a** Developer
**I want** shared enforcement skills and setup commands
**So that** all production and development components follow financial precision and audit standards

**Why After 0.7:**
- Development tools (0.7) will be used to BUILD these enforcement skills
- Ensures consistency with all other infrastructure components
- Enforcement skills are used by production components (0.2-0.6) built after this

**Acceptance Criteria:**
- [ ] `decimal-precision-enforcer` skill auto-invokes on all financial code generation
- [ ] `audit-trail-enforcer` skill auto-invokes on all data transformations
- [ ] `/setup` command guides users through initial project setup
- [ ] Pre-commit hooks installed and enforce quality gates
- [ ] Configuration directories created (credentials, workflow-state, logs)
- [ ] **Centralized config management** (`config/thresholds.yaml`) **NO MAGIC NUMBERS**
  - Materiality percentage threshold (default: 10%)
  - Materiality absolute threshold (default: $50,000)
  - All thresholds configurable, DRY principle enforced
- [ ] All tests pass after setup

**Components (Priority 2 - Week 3):**
- `decimal-precision-enforcer` skill (shared) - **Built using /create-script from 0.7**
- `audit-trail-enforcer` skill (shared) - **Built using /create-script from 0.7**
- `/setup` command (shared) - **Built using development tools from 0.7**
- `config/thresholds.yaml` - **Centralized configuration (NO MAGIC NUMBERS)**

**Success Metrics:**
- Setup time for new user: <30 minutes
- 100% of financial code uses Decimal type (enforced automatically)
- 100% of data transformations have audit trails (enforced automatically)
- Zero hardcoded thresholds in code (all values from centralized config)

---

#### Story 0.2: Data Extraction Infrastructure

**As an** FP&A Analyst
**I want** automated data extraction from Databricks and Adaptive Insights
**So that** I don't manually export CSV files every month

**Acceptance Criteria:**
- [ ] `/extract-databricks` command extracts actuals from Databricks SQL warehouse
- [ ] `/extract-adaptive` command extracts budget from Adaptive Insights API
- [ ] All amounts converted to Decimal precision (no float)
- [ ] NULL values explicitly flagged for review
- [ ] Retry logic handles network failures (exponential backoff)
- [ ] Audit trail logged for all extractions
- [ ] Independent validation by dedicated agents

**Components (Phase 2 - Week 2-3):**
- `databricks-extractor` skill (prod)
- `@databricks-validator` agent (prod)
- `/extract-databricks` command (prod)
- `adaptive-extractor` skill (prod)
- `@adaptive-validator` agent (prod)
- `/extract-adaptive` command (prod)

**Success Metrics:**
- [TO BE MEASURED] Time saved vs. manual CSV export
- Zero data precision errors (Decimal enforcement)
- Zero undetected NULL values

---

#### ~~Story 0.3: Account Reconciliation Infrastructure~~ ❌ REMOVED FROM SCOPE

**Status:** NOT NEEDED - Databricks and Adaptive use SAME account naming conventions

**Original Intent:** Automated account reconciliation between Databricks and Adaptive with fuzzy matching

**Why Removed:** User confirmed that both systems use identical account naming, eliminating the need for:
- ~~`/reconcile-accounts` command~~
- ~~`account-mapper` skill~~
- ~~`@account-reconciler` agent~~
- ~~Fuzzy matching logic~~
- ~~Account mapping configuration~~

**Simplified Workflow:**
```
OLD: Extract Databricks → Extract Adaptive → Reconcile Accounts → Calculate Variance → Report
NEW: Extract Databricks → Extract Adaptive → Calculate Variance → Report
```

**Impact:** Simplified data flow, faster implementation (removed 3 components, saved 1 week)

---

#### Story 0.4: Reporting Infrastructure

**As an** FP&A Manager
**I want** automated Excel report generation with professional formatting
**So that** my team delivers consistent, branded reports to leadership

**Acceptance Criteria:**
- [ ] `/generate-excel-report` command creates multi-sheet workbook
- [ ] Executive Summary, Detailed Analysis, Material Variances sheets included
- [ ] Conditional formatting applied (green=favorable, red=unfavorable)
- [ ] Number formatting correct (currency, percentage)
- [ ] Metadata embedded (timestamp, source files, thresholds)
- [ ] Independent validation ensures output quality

**Components (Phase 4 - Week 5-6):**
- `excel-report-generator` skill (prod)
- `@report-formatter` agent (prod)
- `/generate-excel-report` command (prod)

**Success Metrics:**
- [TO BE MEASURED] Time saved vs. manual report formatting
- 100% of reports pass formatting validation
- Zero Excel formula errors

---

#### Story 0.5: Google Workspace Integration Infrastructure

**As an** FP&A Analyst
**I want** automated Google Slides and Sheets updates
**So that** board decks are always current without manual slide-by-slide updates

**Acceptance Criteria:**
- [ ] `/update-google-slides` command updates presentations with latest data
- [ ] `/update-google-sheets` command updates spreadsheets with variance results
- [ ] Placeholder detection (e.g., `{{REVENUE_ACTUAL}}`) works correctly
- [ ] Preview mode shows changes before applying
- [ ] Human approval required before updating shared presentations
- [ ] "Last Updated" timestamp updated automatically
- [ ] OAuth and Service Account authentication both supported

**Components (Phase 5 - Week 7-9):**
- `google-slides-updater` skill (prod)
- `@slides-previewer` agent (prod)
- `/update-google-slides` command (prod)
- `google-sheets-updater` skill (prod)
- `/update-google-sheets` command (prod)

**Success Metrics:**
- [TO BE MEASURED] Time saved vs. manual slide updates
- Zero presentation errors (broken charts, wrong data)
- 100% of updates previewed before applying

---

#### ~~Story 0.6: Forecast Maintenance Infrastructure~~ ❌ REMOVED FROM SCOPE

**Status:** OUT OF SCOPE - Focus on variance analysis and management reporting ONLY

**Original Intent:** Automated rolling forecast updates with assumption tracking

**Why Removed:** User requested to focus exclusively on variance analysis and management reporting use cases. Rolling forecast maintenance is a separate future initiative.

**Components NOT Being Built:**
- ~~`/update-rolling-forecast` command~~
- ~~`/track-forecast-assumptions` command~~
- ~~`forecast-updater` skill~~
- ~~`assumption-tracker` skill~~
- ~~`@forecast-validator` agent~~
- ~~`@assumption-analyzer` agent~~

**Current Scope:**
```
FOCUS: Variance Analysis + Management Reporting
- Extract actuals (Databricks) and budget (Adaptive)
- Calculate variances with favorability logic
- Generate Excel reports with professional formatting
- Update Google Slides/Sheets dashboards
```

**Impact:** Reduced scope allows faster delivery of core use case (removed 6 components, saved 2 weeks)

---

#### Story 0.7: Development Workflow Infrastructure ⭐ **PRIORITY 1 - IMPLEMENT FIRST**

**🚨 CRITICAL:** This story MUST be implemented FIRST (Week 1-2), before all other stories, including Story 0.1.

**As a** Developer
**I want** automated script generation with TDD workflow
**So that** new financial calculations are generated correctly with comprehensive tests

**Why This Comes First:**
- This builds the **tools to build tools**
- All subsequent components (0.1-0.6, 0.8) will be created using these development tools
- Ensures consistency, quality, and comprehensive testing from day 1
- Prevents manual script creation errors that are costly in financial systems

**Acceptance Criteria:**
- [ ] `/create-script` command generates new Python scripts from specifications
- [ ] TDD workflow enforced: RED (write tests) → GREEN (implement) → REFACTOR → VERIFY
- [ ] `/validate-script` command runs pytest, mypy, ruff, bandit, coverage
- [ ] `/review-code` command invokes @code-reviewer for independent verification
- [ ] >95% test coverage required (enforced by pre-commit hook)
- [ ] All edge cases from financial-validator tested
- [ ] Scripts only saved to `scripts/` after human approval

**Components (Priority 1 - Week 1-2):**
- `python-best-practices` skill (dev)
- `test-suite-generator` skill (dev)
- `@script-generator` agent (dev)
- `@test-generator` agent (dev)
- `@script-validator` agent (dev)
- `/create-script` command (dev)
- `/validate-script` command (dev)
- `/review-code` command (dev)

**Success Metrics:**
- 100% of generated scripts use Decimal for currency
- >95% test coverage on all scripts
- Zero financial calculation errors in production

**Once Complete:** Use these tools to build all components in Stories 0.1-0.6 and 0.8

---

#### Story 0.8: Orchestration Infrastructure

**As an** FP&A Manager
**I want** a single command to run the entire monthly close process
**So that** my team executes a consistent, documented workflow every month

**Acceptance Criteria:**
- [ ] `/prod:monthly-close` command orchestrates full post-close workflow
- [ ] **Simplified Workflow:** Extract Databricks actuals → Extract Adaptive budget → Calculate variances → Generate Excel reports → Update Google dashboards
- [ ] Human checkpoints at each major phase
- [ ] Error recovery with workflow state management (resume from failure)
- [ ] Complete audit trail for entire workflow
- [ ] Execution summary with time saved metrics
- [ ] Load thresholds from centralized config (no hardcoded values)

**Components (Priority 4 - Week 10):**
- `/prod:monthly-close` command (prod, orchestration)

**Success Metrics:**
- [TO BE MEASURED] End-to-end execution time
- [TO BE MEASURED] Time saved vs. manual monthly close
- 100% workflow completion rate (with error recovery)
- Complete audit trail for compliance

---

### Epic 1: Post-Close Variance Analysis

**Scope Change:** Focus on POST-CLOSE processes, not month-end close itself. Month-end close happens in separate systems (Adaptive Insights, Databricks). This epic focuses on extracting closed data, analyzing variances, stakeholder review, adjustments, and finalizing reports.

**Workflow:**
1. **Close** (External) - Month closed in Adaptive/Databricks
2. **Extract** - Pull actuals from Databricks, budget from Adaptive
3. **Analyze** - Calculate variances, flag material items
4. **Review** - Present to stakeholders, gather feedback
5. **Adjust** - Apply approved adjustments
6. **Finalize** - Upload finalized data to Adaptive
7. **Report** - Generate Google Slides/Sheets reports

**Integration Specifications:**
- [specs/adaptive/ADAPTIVE_API_SPEC.md](specs/adaptive/ADAPTIVE_API_SPEC.md) - Adaptive Insights API integration
- [specs/databricks/DATABRICKS_API_SPEC.md](specs/databricks/DATABRICKS_API_SPEC.md) - Databricks SQL API integration
- [specs/google/GOOGLE_WORKSPACE_SPEC.md](specs/google/GOOGLE_WORKSPACE_SPEC.md) - Google Workspace integration

---

#### Story 1.1: Extract Actuals from Databricks

**As an** FP&A Analyst
**I want to** automatically extract monthly actuals from Databricks SQL warehouse
**So that** I can analyze variance without manual data exports

**Acceptance Criteria:**
- [ ] Connect to Databricks SQL warehouse via Personal Access Token
- [ ] Execute parameterized queries for specific month/year
- [ ] Pull actuals data grouped by account and department
- [ ] Convert all amounts to Decimal precision (no float)
- [ ] Handle NULL values explicitly (flag for review)
- [ ] Save extracted data locally for offline analysis
- [ ] Log all queries to audit trail with timestamp and parameters

**Success Metrics:**
- [TO BE MEASURED] Time saved vs. manual CSV export
- Zero data precision errors (Decimal enforcement)
- Complete audit trail of data extraction

**Edge Cases to Handle:**
- Databricks warehouse offline/unavailable (retry logic)
- Query timeout on large datasets (async execution)
- Account IDs not matching Adaptive chart of accounts (reconciliation report)
- NULL amounts in source data (flag, don't drop)

---

#### Story 1.2: Extract Budget from Adaptive Insights

**As an** FP&A Analyst
**I want to** automatically extract budget data from Adaptive Insights
**So that** I have both actuals and budget ready for variance analysis

**Acceptance Criteria:**
- [ ] Connect to Adaptive Insights API via API token
- [ ] Export budget for specific version (e.g., "FY 2025 Budget")
- [ ] Pull budget data for specific month/year
- [ ] Parse XML response format to structured data
- [ ] Convert amounts to Decimal precision
- [ ] Reconcile account lists (Databricks actuals vs Adaptive budget)
- [ ] Flag unmatched accounts for review
- [ ] Save extracted data locally

**Success Metrics:**
- Zero undetected account mismatches
- Complete audit trail for budget extraction
- Reconciliation report generated before analysis

**Edge Cases to Handle:**
- API rate limits (exponential backoff retry)
- Version not found (clear error message)
- Account structure changes (reconciliation workflow)
- Negative budget values (handle correctly for contra accounts)

---

### Epic 2: Variance Analysis Automation

#### Story 2.1: Budget vs. Actual Variance Calculation

**As an** FP&A Analyst
**I want to** automatically calculate variances between budget and actual for all accounts
**So that** I don't manually calculate 100+ variance formulas each month

**Acceptance Criteria:**
- [ ] System calculates absolute variance ($ difference) for every account
- [ ] System calculates percentage variance for every account
- [ ] Division by zero handled gracefully (zero budget with actuals = "N/A %")
- [ ] Both zero budget and zero actual = $0 variance, 0%, "No Activity"
- [ ] Negative values handled correctly in calculations
- [ ] All currency calculations maintain precision (no rounding errors)
- [ ] Calculations complete quickly (specific performance targets to be defined based on testing)

**Business Rules:**
```
Absolute Variance = Actual - Budget
Percentage Variance = ((Actual - Budget) / Budget) × 100

Special Cases:
- If Budget = 0 and Actual ≠ 0: Absolute Variance = Actual, Percentage = N/A
- If Budget = 0 and Actual = 0: Absolute = $0, Percentage = 0%, Status = "No Activity"
- If Budget < 0: Calculate variance normally (supports liability/contra accounts)
```

---

#### Story 2.2: Favorability Assessment

**As an** FP&A Analyst
**I want to** automatically determine if each variance is favorable or unfavorable
**So that** I can quickly identify areas needing management attention

**Acceptance Criteria:**
- [ ] Revenue variances: Actual > Budget = Favorable
- [ ] Expense variances: Actual < Budget = Favorable
- [ ] Asset variances: Actual > Budget = Favorable
- [ ] Liability variances: Actual < Budget = Favorable
- [ ] Each variance labeled clearly: "Favorable" or "Unfavorable"
- [ ] Account type determination automated (from chart of accounts or naming convention)
- [ ] Manual override option for special cases

**Business Context:**

*Revenue Example:*
- Budgeted quarterly sales: $500K
- Actual quarterly sales: $550K
- Variance: +$50K, +10%
- Favorability: ✅ FAVORABLE (exceeded revenue target)

*Expense Example:*
- Budgeted salaries: $100K
- Actual salaries: $105K
- Variance: +$5K, +5%
- Favorability: ❌ UNFAVORABLE (spent more than budgeted)

---

#### Story 2.3: Materiality Flagging

**As an** FP&A Manager
**I want to** automatically flag material variances requiring management review
**So that** my team focuses commentary on significant items, not every small variance

**Acceptance Criteria:**
- [ ] Percentage threshold configurable (default: 10%)
- [ ] Absolute dollar threshold configurable (default: $50,000)
- [ ] Variance flagged as material if EITHER threshold exceeded
- [ ] Material flag visible in reports (e.g., "Yes"/"No" column)
- [ ] Count of material variances shown in executive summary
- [ ] Ability to filter reports to material items only
- [ ] Thresholds can vary by account category (e.g., revenue vs. expense)

**Example Materiality Logic:**
```
Material = (|Percentage Variance| > 10%) OR (|Absolute Variance| > $50,000)

Example 1: Budget $100K, Actual $115K
- Variance: +$15K, +15%
- Material: YES (exceeds 10% threshold)

Example 2: Budget $5M, Actual $5.03M
- Variance: +$30K, +0.6%
- Material: NO (below both thresholds)

Example 3: Budget $10K, Actual $65K
- Variance: +$55K, +550%
- Material: YES (exceeds both thresholds)
```

---

### Epic 3: Management Reporting

#### Story 3.1: Variance Report Generation

**As an** FP&A Analyst
**I want to** generate a formatted variance analysis report in Excel
**So that** I can deliver management-ready analysis without manual formatting

**Acceptance Criteria:**
- [ ] Output is professional Excel workbook with multiple sheets
- [ ] Executive Summary sheet shows totals by category with conditional formatting
- [ ] Detailed Analysis sheet shows all accounts with variance calculations
- [ ] Material Variances sheet shows filtered view of significant items only
- [ ] All currency values formatted as $#,##0.00
- [ ] All percentage values formatted as 0.00%
- [ ] Conditional formatting: Green = Favorable & Material, Red = Unfavorable & Material
- [ ] File naming includes date/time for version control
- [ ] Metadata embedded: generation timestamp, source files used, thresholds applied

**Report Structure:**

*Sheet 1: Executive Summary*
- Total Budget vs. Total Actual by major category (Revenue, COGS, OpEx, etc.)
- Count of material favorable variances
- Count of material unfavorable variances
- High-level summary table with visual indicators

*Sheet 2: Detailed Variance Analysis*
- One row per account
- Columns: Account Code, Account Name, Department, Budget, Actual, $ Variance, % Variance, Favorability, Material Flag
- Sortable and filterable
- Conditional formatting for easy scanning

*Sheet 3: Material Variances Only*
- Same structure as Sheet 2
- Pre-filtered to Material = Yes
- Sorted by absolute variance descending (largest variances first)
- Empty "Management Commentary" column for analyst input

*Sheet 4: Visualizations* [NEEDS CLARIFICATION: Required charts?]
- [PLACEHOLDER: Waterfall chart of top variance drivers?]
- [PLACEHOLDER: Bar chart favorable vs. unfavorable?]
- [PLACEHOLDER: Department-level summary?]

---

#### Story 3.2: Executive Dashboard Updates

**As an** FP&A Manager
**I want to** automatically update Google Slides presentations with latest data
**So that** board decks are always current without time-consuming manual updates

**Acceptance Criteria:**
- [ ] System connects to Google Slides via API
- [ ] Identifies placeholder text in slides (e.g., {{REVENUE_ACTUAL}})
- [ ] Replaces placeholders with values from data source
- [ ] Updates chart data sources for embedded charts
- [ ] Updates "Last Updated: [DATE]" timestamp automatically
- [ ] Preview mode shows what will change before applying
- [ ] Confirmation required before making changes
- [ ] Original presentation preserved (updates applied to copy or version)
- [ ] Process completes efficiently (specific performance targets to be defined)

**Example Use Case:**

*Monthly Board Meeting Preparation*
- Presentation: "Board Meeting Nov 2025.pptx" (Google Slides)
- Data Source: Variance analysis output file
- Placeholders:
  - Slide 3: {{Q3_REVENUE}} → $12.5M
  - Slide 5: {{YTD_EBITDA}} → $3.2M
  - Slide 7: {{TOP_VARIANCE_1}} → "Sales exceeded budget by $450K (15%)"
  - Slide 12: {{LAST_UPDATED}} → "November 8, 2025"

**Success Metrics:**
- [TO BE MEASURED] Baseline: Time currently spent on manual presentation updates
- [TO BE VALIDATED] Target: Significant reduction in update time
- Expected outcome: Eliminate manual slide-by-slide data copying

---

### Epic 4: Rolling Forecast Maintenance

#### Story 4.1: Actuals Integration into Forecast

**As an** FP&A Analyst
**I want to** replace forecast values with actual results for closed periods
**So that** my rolling forecast always reflects real performance

**Acceptance Criteria:**
- [ ] System identifies which periods are now closed (have actuals)
- [ ] Forecast values for closed periods replaced with actual values
- [ ] Forecast window extended forward by same number of periods
- [ ] New forecast periods initialized with appropriate default values [NEEDS CLARIFICATION: copying prior period? using growth rate? manual input?]
- [ ] Audit log created showing which periods were replaced
- [ ] Original forecast file preserved (updates saved to new version)
- [ ] Process applies to all forecast categories consistently

**Example Scenario:**

*Current State (Beginning of November):*
- Forecast covers: Nov 2024 - Oct 2025 (12 months)
- October actuals just closed

*Desired State (After Update):*
- Forecast covers: Dec 2024 - Nov 2025 (12 months)
- Nov 2024 through Oct 2025: Replaced with actuals (where available)
- Nov 2025: New forecast period added

---

#### Story 4.2: Assumption Recalibration Tracking

**As an** FP&A Manager
**I want to** document what assumptions changed when updating the forecast
**So that** we have clear audit trail of forecast evolution

**Acceptance Criteria:**
- [ ] System prompts for assumption changes during forecast update [NEEDS CLARIFICATION: How are assumptions captured? Free text? Structured fields?]
- [ ] Assumption change log created with timestamp and user
- [ ] Key assumptions documented: growth rates, headcount plans, pricing changes, etc.
- [ ] Comparison view: previous assumptions vs. updated assumptions
- [ ] Change log exportable for audit purposes
- [ ] Link between assumption changes and forecast variances

**[NEEDS CLARIFICATION]:**
- What specific assumptions should be tracked?
- How are assumptions currently documented?
- Should system suggest assumption changes based on actual trends?

---

## Business Rules & Calculations

### Variance Calculations

**Absolute Variance:**
```
Absolute Variance ($) = Actual Amount - Budget Amount

Example:
Budget: $100,000
Actual: $115,000
Absolute Variance: $15,000
```

**Percentage Variance:**
```
Percentage Variance (%) = ((Actual - Budget) / Budget) × 100

Example:
Budget: $100,000
Actual: $115,000
Percentage Variance: ((115,000 - 100,000) / 100,000) × 100 = 15.00%

Special Case - Zero Budget:
Budget: $0
Actual: $5,000
Percentage Variance: N/A (undefined, cannot divide by zero)
Absolute Variance: $5,000 (still calculated and may be material)
```

**Favorability Logic:**
```
IF account_type = "Revenue":
    Favorable = (Actual > Budget)

IF account_type = "Expense":
    Favorable = (Actual < Budget)

IF account_type = "Asset":
    Favorable = (Actual > Budget)

IF account_type = "Liability":
    Favorable = (Actual < Budget)

Status = "Favorable" if Favorable = TRUE, else "Unfavorable"
```

**Materiality Determination:**
```
Material = (|Percentage Variance| > Percentage_Threshold)
           OR (|Absolute Variance| > Absolute_Threshold)

Default Thresholds:
- Percentage_Threshold = 10%
- Absolute_Threshold = $50,000

Example Material Variances:
1. Variance = $60K, 5% → Material (absolute exceeds $50K)
2. Variance = $8K, 12% → Material (percentage exceeds 10%)
3. Variance = $25K, 5% → Not Material (neither threshold exceeded)
```

---

### Financial Metrics Definitions

**Revenue Metrics:**
```
Revenue Growth Rate = ((Current Period Revenue - Prior Period Revenue) / Prior Period Revenue) × 100

Revenue vs Budget Variance = ((Actual Revenue - Budget Revenue) / Budget Revenue) × 100
```

**Profitability Metrics:**
```
Gross Margin % = ((Revenue - Cost of Goods Sold) / Revenue) × 100

EBITDA = Operating Income + Depreciation + Amortization

EBITDA Margin % = (EBITDA / Revenue) × 100

Operating Margin % = (Operating Income / Revenue) × 100
```

**Efficiency Metrics:**
```
Burn Rate (Monthly) = Total Monthly Cash Outflow

Days Sales Outstanding (DSO) = (Accounts Receivable / Revenue) × Days in Period

Operating Expense Ratio = (Operating Expenses / Revenue) × 100
```

**[NEEDS CLARIFICATION]:**
- Which metrics are required in standard reports?
- Are there industry-specific metrics needed?
- Should metrics be calculated automatically or on-demand?

---

## Data Requirements

### Input Data Specifications

#### Budget File Requirements

**Must Have:**
- File format: Excel (.xlsx, .xls) or CSV
- Account identifier column (account code, GL number, etc.)
- Account description/name column
- Numeric budget amounts for each period
- Data organized by rows (one account per row) or columns (one account per column) [NEEDS CLARIFICATION: Which layout is standard?]

**Should Have:**
- Department or cost center classification
- Account type indicator (revenue, expense, asset, liability)
- Period labels (month names, dates, or "Jan", "Feb", etc.)

**May Have:**
- Multiple sheets (Summary, Detail, by Department)
- Notes or commentary columns
- Formulas and calculations
- Formatting (colors, borders, fonts)

**Data Quality Expectations:**
- No merged cells in data range
- Consistent data types per column
- No embedded charts within data range
- Currency values as numbers (not text formatted as "$1,000")

---

#### Actuals File Requirements

**Must Have:**
- Same structural layout as budget file (for easy comparison)
- Account identifier matching budget file format
- Actual amounts for closed periods
- Clear indication of reporting period

**Should Have:**
- Same account list as budget (or explicit documentation of differences)
- Same column naming conventions
- Period identifiers matching budget file

**Known Variations to Handle:**
- Department actuals files may have different structure than consolidated budget
- Actuals from different source systems may have different account codes
- Some actuals files include MTD (Month-to-Date) and YTD (Year-to-Date) columns
- Date formats vary across systems

---

### Output Requirements

#### Variance Report Output

**File Format:** Excel (.xlsx)

**Required Sheets:**
1. Executive Summary
2. Detailed Variance Analysis
3. Material Variances Only

**Optional Sheets:** [NEEDS CLARIFICATION]
4. Visualizations / Charts
5. Reconciliation Report
6. Assumption Documentation

**Retention:**
- All generated reports must be timestamped and stored
- Audit trail: ability to reproduce any historical report
- Storage location: [NEEDS CLARIFICATION: Local filesystem? Cloud storage? Database?]

---

## Success Criteria & KPIs

### Time Savings (Primary Objective)

**Research Context:**
- Industry studies show FP&A professionals spend only 35% of time on high-value tasks
- 45% of FP&A time spent on low-value activities like data collection and validation
- Finance teams report over 60% of time on activities that can be automated
- McKinsey research: Finance professionals spend 20-30% less time on data processing with AI adoption
- Case study: Month-end close reduced from 10+ days to 3 days with automation

**Current State [TO BE MEASURED]:**
- Monthly close cycle time: [Establish baseline through user shadowing]
- Variance analysis time: [Establish baseline through user shadowing]
- Report generation time: [Establish baseline through user shadowing]
- Presentation update time: [Establish baseline through user shadowing]
- Rolling forecast update time: [Establish baseline through user shadowing]

**Target State:**
- Significant reduction in manual data collection and processing time
- Automation of repetitive calculation tasks
- Faster report generation through automation
- Elimination of manual slide-by-slide presentation updates

**Success Metrics:**
- Increase in time spent on strategic, high-value activities
- Reduction in time spent on data collection and validation
- Faster delivery of insights to leadership

---

### Error Reduction (Secondary Objective)

**Research Context:**
- Manual processes are identified as causing "serious bottlenecks" by industry analysts
- 75%+ of finance leaders report improvements in accuracy after automation
- Error-prone copy/paste operations commonly cited as pain point

**Current State [TO BE MEASURED]:**
- Error types and frequency to be documented through user interviews
- Common error sources: Manual calculations, copy/paste, formula mistakes, version control

**Target State:**
- Automated calculations eliminate manual formula errors
- Automated data extraction eliminates copy/paste errors
- Tested business logic ensures consistency
- File versioning and audit trails reduce version control issues

**Success Metrics:**
- Reduction in errors requiring rework
- Increased confidence in reported numbers
- Faster review and approval cycles

---

### Quality Improvements

**Consistency:**
- [ ] All variance calculations use identical formula logic
- [ ] Favorability assessment applied uniformly
- [ ] Materiality thresholds enforced consistently
- [ ] Report formatting standardized across periods

**Auditability:**
- [ ] Complete audit trail: source files → calculations → outputs
- [ ] Reproducible results (same inputs = same outputs)
- [ ] Timestamp and versioning on all artifacts
- [ ] Clear documentation of assumptions and business rules

**Timeliness:**
- [ ] Month-end reports delivered earlier (specific targets to be established based on baseline)
- [ ] Board materials ready with adequate buffer time (vs. last-minute updates)
- [ ] Rolling forecasts updated promptly after month-end close

---

## Constraints & Assumptions

### Technical Constraints [NEEDS CLARIFICATION]

**Data Volume:**
- Typical dataset: 500-1,500 accounts
- Maximum supported: [NEEDS CLARIFICATION: 10,000 accounts? More?]
- File size limits: [NEEDS CLARIFICATION: 50MB? 200MB?]

**Processing Time:**
- User expectation: Processes should feel responsive and not block workflow
- Performance targets to be defined based on user testing with real datasets
- Maximum acceptable processing time: [NEEDS CLARIFICATION based on dataset size]

**Environment:**
- Operating system: [NEEDS CLARIFICATION: Windows only? Mac? Linux?]
- Excel version: [NEEDS CLARIFICATION: Which versions must be supported?]
- Google Workspace access: [NEEDS CLARIFICATION: Authentication method?]

---

### Business Assumptions

**User Skills:**
- Users are Excel proficient (advanced formulas, pivot tables, etc.)
- Users understand financial concepts (variance, EBITDA, etc.)
- Users have basic file management skills
- Users can follow written instructions for setup

**Data Availability:**
- Budget data exists in structured Excel format
- Actuals data available within 3-5 business days of month-end
- Chart of accounts mapping is documented
- Materiality thresholds are defined by finance leadership

**Process Assumptions:**
- Variance analysis performed monthly (not weekly or daily)
- Rolling forecast updated monthly
- Board presentations occur monthly or quarterly
- Users have time to review automated outputs before distribution

---

### Out of Scope (V1.0)

**Explicitly NOT Included:**
- [ ] Direct integration with ERP systems (e.g., NetSuite, SAP, Oracle)
- [ ] Real-time data syncing
- [ ] Budgeting/planning workflows (creating budgets from scratch)
- [ ] Predictive forecasting / machine learning models
- [ ] Multi-currency conversion
- [ ] Collaboration features (commenting, approval workflows)
- [ ] Mobile app interface
- [ ] Custom chart/dashboard builder
- [ ] Scenario modeling / what-if analysis

**Future Consideration:**
- Direct ERP integration (Phase 2)
- Predictive analytics (Phase 3)
- Collaborative planning (Phase 2)

---

## Open Questions & Clarifications Needed

### Critical Path Items

**[NEEDS CLARIFICATION - BLOCKING]:**

1. **Data Structure Standards:**
   - What is the standard layout for budget/actuals files? (Rows vs. columns)
   - Are there multiple file format variations we must support?
   - How is account type determined? (Column in file? Naming convention? External mapping?)

2. **Google Workspace Integration:**
   - What authentication method for Google Slides API? (OAuth? Service Account?)
   - Should updates be applied to original file or create new version?
   - Are there access permission constraints to consider?

3. **File Storage & Retrieval:**
   - Where should input files reside? (Local folder? Google Drive? Sharepoint?)
   - Where should output files be saved?
   - How long should historical files be retained?

4. **User Interaction Model:**
   - Command-line interface? Web interface? Excel add-in? [NEEDS CLARIFICATION]
   - How much manual review/confirmation is required at each step?
   - Should processes run automatically on schedule or on-demand?

---

### Important But Non-Blocking

**[NEEDS CLARIFICATION - MEDIUM PRIORITY]:**

5. **Materiality Thresholds:**
   - Should thresholds vary by account category?
   - Who defines/updates thresholds? (User configurable or hardcoded?)

6. **Visualization Requirements:**
   - Which specific charts are required in variance reports?
   - Static images or interactive/updateable charts?
   - Chart library preferences?

7. **Forecast Extension Logic:**
   - How should new forecast periods be initialized? (Prior period? Growth rate? Manual?)
   - Should system suggest assumption updates based on trends?

8. **Assumption Tracking:**
   - What specific assumptions should be documented?
   - Structured fields or free-form text?
   - How are assumptions currently managed?

---

### Nice-to-Have Clarifications

**[NEEDS CLARIFICATION - LOW PRIORITY]:**

9. **Error Handling Philosophy:**
   - Should system halt on any data quality issue, or flag and continue?
   - How much validation is "too much" (slows down users)?

10. **Reporting Customization:**
    - Should report formats be customizable by user?
    - Template-based system or fixed format?

11. **Audit Trail Detail:**
    - What level of detail needed in audit logs?
    - Who will review audit logs and how often?

12. **Performance Expectations:**
    - What dataset size represents "large" for this use case?
    - Are there specific performance benchmarks to target?

---

## Validation & Next Steps

### Spec Review Checklist

Before proceeding to technical planning:

- [ ] **Stakeholder Review:** FP&A Manager/Director validates user stories
- [ ] **User Interview:** Validate pain points with actual FP&A analysts
- [ ] **Data Sample Review:** Obtain real (anonymized) budget/actuals files to validate assumptions
- [ ] **Clarifications Resolved:** All [NEEDS CLARIFICATION] items addressed
- [ ] **Success Metrics Approved:** Time savings targets confirmed realistic
- [ ] **Scope Agreement:** Confirm V1.0 scope and out-of-scope items
- [ ] **Priority Ranking:** Order epics/stories by business value

---

### Recommended Validation Activities

**1. Data Structure Discovery**
- Collect 3-5 sample budget files from target users
- Collect 3-5 sample actuals files from target users
- Document all structural variations observed
- Create canonical data structure specification

**2. User Workflow Shadowing**
- Observe FP&A analyst performing monthly close (2-3 hours)
- Observe variance analysis process (1-2 hours)
- Document current tools, pain points, workarounds
- Time each manual step to validate baseline metrics

**3. Stakeholder Interviews**
- Interview 2-3 FP&A analysts (primary users)
- Interview 1-2 FP&A managers (secondary users)
- Validate problem statement and prioritization
- Confirm success metrics and acceptance criteria

**4. Technical Feasibility Check**
- Confirm Google Slides API access available
- Validate Excel file parsing capabilities
- Test data volume limits with sample files
- Identify any technical blockers early

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1-DRAFT | 2025-11-08 | Claude | Research-backed revision: Removed unsupported time estimates and hallucinated claims. Added research sources and industry context. Replaced specific numbers with [TO BE MEASURED] placeholders requiring user validation. |
| 1.0-DRAFT | 2025-11-08 | Claude | Initial specification created from business requirements |

---

## Appendix: Reference Materials

### Research Sources

This specification is grounded in industry research conducted November 2024-2025:

**FP&A Time Allocation:**
- FP&A Trends Survey 2024: 35% of professional time spent on high-value tasks
- Industry analysis: 45% of FP&A time on low-value activities (data collection/validation)
- Finance teams: Over 60% of time on activities that can be automated
- Manual processes cited as bottleneck by 49% of FP&A professionals
- Only 46% able to fully execute all tasks due to manual process overhead

**Automation Benefits:**
- McKinsey research: 20-30% less time on data processing with AI adoption
- 75%+ of finance leaders report accuracy/speed improvements after automation
- 92% of finance leaders using or planning automation for half their work
- Finance teams: 60% less time on data preparation with modern tools

**Month-End Close:**
- Median close time: 6 calendar days
- Case study (Withum): 10+ days reduced to 3 days with automation
- Additional case study: 3.5-day reduction achieved
- Manual data aggregation from multiple sources cited as primary bottleneck

**Technology Adoption:**
- 65% of CFOs increased FP&A technology budgets by 20%+ in 2024
- 70% of teams now supported by cloud-based platforms
- 48% of CFOs cite GenAI adoption challenges as top internal concern
- 53% cite lack of analytical tools as biggest challenge

**Sources:** FP&A Trends Survey 2024, McKinsey research on AI in finance, Withum case studies, Finance Alliance State of FP&A 2025 survey, industry analyst reports 2024-2025.

---

### Real-World Example: Monthly Variance Analysis

**Scenario:** Retail company analyzing Q3 performance

**Budget (Q3):**
- Revenue: $500,000
- Cost of Goods Sold: $300,000
- Gross Profit: $200,000
- Operating Expenses: $150,000
- Operating Income: $50,000

**Actual (Q3):**
- Revenue: $450,000
- Cost of Goods Sold: $285,000
- Gross Profit: $165,000
- Operating Expenses: $155,000
- Operating Income: $10,000

**Variance Analysis:**

| Account | Budget | Actual | $ Variance | % Variance | Favorable? | Material? |
|---------|--------|--------|-----------|-----------|-----------|-----------|
| Revenue | $500K | $450K | -$50K | -10.0% | ❌ Unfavorable | ✅ Yes |
| COGS | $300K | $285K | -$15K | -5.0% | ✅ Favorable | ❌ No |
| Gross Profit | $200K | $165K | -$35K | -17.5% | ❌ Unfavorable | ✅ Yes |
| OpEx | $150K | $155K | +$5K | +3.3% | ❌ Unfavorable | ❌ No |
| Operating Income | $50K | $10K | -$40K | -80.0% | ❌ Unfavorable | ✅ Yes |

**Management Commentary:**
- Revenue shortfall due to new competitor impacting store traffic
- COGS favorability from improved vendor pricing (negotiated discount)
- OpEx slightly over budget due to unplanned marketing campaign
- Net impact: Operating income significantly below target, requires strategic pricing review

---

### Glossary of FP&A Terms

**Actuals:** Real financial results from closed accounting periods (what actually happened)

**Budget:** Financial plan for future period approved by management (what we expect to happen)

**Chart of Accounts:** Standardized list of all general ledger accounts with unique codes

**EBITDA:** Earnings Before Interest, Taxes, Depreciation, and Amortization (profitability metric)

**Favorable Variance:** Variance that positively impacts profitability (revenue up or expense down)

**Forecast:** Projection of future financial performance, updated regularly based on latest trends

**GL (General Ledger):** Complete record of all financial transactions organized by account

**Material Variance:** Variance significant enough to require management review and explanation

**Month-End Close:** Process of finalizing all financial transactions and reports for completed month

**Rolling Forecast:** Continuously updated forecast that always projects same time horizon forward (e.g., always next 12 months)

**Variance:** Difference between budgeted/expected amount and actual result

**YTD (Year-to-Date):** Cumulative total from beginning of fiscal year to current date

---

## Addendum: Development Approach & Architecture (Added 2025-11-08)

### Platform Choice: Claude Code-Native

**Decision:** Build as Claude Code workflows (skills, commands, agents) rather than standalone Python package distribution.

**Rationale:**
- Target users are FP&A professionals, not Python developers
- Conversational, human-in-loop workflows match FP&A approval processes
- No installation/dependency management for end users
- Iterative refinement by editing markdown files (non-technical)
- Immediate availability in Claude Code environment

**What This Means:**
- Primary interface: Slash commands (e.g., `/variance-analysis budget.xlsx actuals.xlsx`)
- Pre-written Python scripts in `scripts/` directory (executed by Claude)
- Skills auto-invoke for specific tasks (e.g., variance analysis, account mapping)
- Agents provide independent verification (e.g., code-reviewer, data-validator)

###  Environment Split: Dev vs Prod vs Shared

**Structure:**
```
.claude/
├── agents/
│   ├── dev/          # Development agents (script-generator, script-validator, code-reviewer)
│   ├── prod/         # Production agents (finance-reviewer, data-validator, reconciler)
│   └── shared/       # Shared utilities (research-agent)
├── commands/
│   ├── dev/          # Development workflows (/create-script, /validate-script)
│   ├── prod/         # Production workflows (/monthly-close, /variance-analysis)
│   └── shared/       # Shared commands (/help, /config)
└── skills/
    ├── dev/          # Dev skills (python-best-practices, financial-script-generator)
    ├── prod/         # Prod skills (variance-analyzer, account-mapper, report-generator)
    └── shared/       # Shared skills (decimal-precision-enforcer, audit-trail-enforcer)
```

**Dev Workflows:** Generate new scripts when needed (spec → build → test → review → approve)
**Prod Workflows:** Execute existing validated scripts for daily FP&A tasks

### Data Integration Strategy

**Phase 1: Excel-First (MVP)**
- Focus on local Excel file processing (openpyxl, xlsxwriter)
- No cloud dependencies required
- Works offline
- Faster initial development

**Phase 2: Google Integration**
- Google Sheets read/write (gspread)
- Google Slides report generation (slidio patterns)
- OAuth + Service Account authentication options
- Skills to convert Excel workflows → Google workflows

**Credentials:** `config/credentials/` directory (OAuth tokens, service account JSON)

### Script Generation & Validation Requirements

**Problem:** LLMs should not perform financial calculations directly (hallucination risk)
**Solution:** Generate robust, tested Python scripts that perform calculations

**All Scripts Must:**
1. Use Decimal for all currency calculations (NEVER float)
2. Include comprehensive type hints
3. Have edge case tests (division by zero, negative values, NULL)
4. Include audit trail logging (timestamp, user, source files, operation)
5. Pass independent code review by separate agent
6. Achieve >80% test coverage

**Validation Pipeline (Enforced by Dev Skills):**
1. `script-generator` agent writes code from spec
2. `test-generator` agent creates comprehensive tests (TDD)
3. `script-validator` agent runs: pytest, mypy, ruff, bandit, coverage
4. `code-reviewer` agent performs independent review (separate context, read-only)
5. Human approval required before script moves to `scripts/` directory

**Anti-Patterns Blocked:**
- ❌ Float usage for currency → Blocked by `decimal-precision-enforcer` skill
- ❌ Missing type hints → Blocked by `python-best-practices` skill
- ❌ No error handling → Blocked by `python-best-practices` skill
- ❌ No audit logging → Blocked by `audit-trail-enforcer` skill

### Workflow Templates

**Templates Location:** `.claude/templates/`

**Available Templates:**
1. **SKILL_TEMPLATE.md** - For creating new skills with Progressive Disclosure pattern
2. **COMMAND_TEMPLATE.md** - For creating slash commands with human checkpoints
3. **AGENT_TEMPLATE.md** - For creating subagents with tool permissions
4. **TDD_WORKFLOW.md** - Test-Driven Development cycle (RED-GREEN-REFACTOR-VALIDATE)
5. **RESEARCH_PLAN_IMPLEMENT_VERIFY.md** - Structured feature development workflow

**TDD Workflow (Mandatory for Financial Scripts):**
1. **RED:** Write failing tests first (define expected behavior)
2. **GREEN:** Write minimum code to pass tests (using Decimal)
3. **REFACTOR:** Improve quality while tests stay green (add docstrings, error handling, logging)
4. **VALIDATE:** Independent agent verification + human approval

**RPIV Workflow (For New Features):**
1. **RESEARCH:** Explore codebase, external libraries, document findings (no coding)
2. **PLAN:** Generate formal specification, get human approval (no coding)
3. **IMPLEMENT:** Follow TDD workflow with human checkpoints at each milestone
4. **VERIFY:** Independent validation suite + code review + human final approval

### External Libraries Integration

**Cloned Repos (in `external/`):**
- **humanlayer** - Study human-in-loop approval patterns (reference)
- **mcp-gdrive** - Study Google Drive MCP protocol (reference)
- **gspread** - Install via pip for Google Sheets integration
- **slidio** - May install or adapt patterns for Google Slides
- **pyfpa** - Study FP&A consolidation algorithms (may install if adaptable)
- **py-money** - Reference Decimal precision patterns (use Python's built-in decimal)

**Why Keep Cloned Repos:**
- Audit security before using
- Learn implementation patterns
- Pin exact versions (git submodules)
- Offline development capability
- Customize if needed

**Installation Strategy:**
- Install via pip when library is stable and fits our needs
- Study patterns and adapt when library needs customization
- Use as reference when we build custom solution

### Pre-written vs Generated Scripts

**Pre-written Scripts (in `scripts/`):**
- Core calculations (variance, consolidation, favorability, materiality)
- Google/Excel integrations (readers, writers)
- Workflow orchestration (monthly close, variance reports, board decks)
- Shared utilities (logger, validator, config loader)

**Generated Scripts (via Dev Workflows):**
- User requests analysis not covered by existing scripts
- Trigger: `/create-script "Calculate YoY revenue growth by department"`
- Process: Research → Plan (spec) → Implement (TDD) → Verify (validation + review) → Approve → Save to `scripts/`
- New script becomes available for future prod workflows

**Variation Handling:**
- Simple variations: Pass parameters to existing script
- Complex variations: Generate new script via dev workflow

### Success Metrics (Updated)

**For Script Generation Quality:**
- ✅ 100% of scripts use Decimal for currency (enforced by hooks)
- ✅ 100% of scripts have type hints (enforced by validation)
- ✅ >80% test coverage on all scripts (enforced by validation)
- ✅ Zero financial calculation errors in production (measured via audit logs)

**For User Experience:**
- [TO BE MEASURED] Time to complete monthly close (baseline vs automated)
- [TO BE MEASURED] User satisfaction with conversational interface
- [TO BE MEASURED] Number of scripts generated on-demand vs pre-written
- [TO BE MEASURED] Accuracy of generated scripts (human review approval rate)

**For Development Efficiency:**
- [TO BE MEASURED] Time to generate new script via dev workflow
- [TO BE MEASURED] Pass rate for validation suite (first attempt)
- [TO BE MEASURED] Code review findings per script (lower is better)

### Operational Decisions (Finalized 2025-11-08)

**Script Versioning:**
- **Decision:** Use git/GitHub for all versioning. NEVER create `script_v2.py`, `script_v3.py`, `script-new.py`, etc.
- **Rationale:** Git provides proper version control, diffs, and rollback. Avoids file naming confusion.
- **Implementation:** Archive old versions in git history. Users can revert to specific commits if needed.

**Audit Log Strategy:**
- **Decision:** Centralized audit log - all scripts write to single `audit.log` file with structured JSON entries.
- **Rationale:**
  - Easier compliance reporting (single source of truth)
  - Chronological ordering of all financial operations
  - Searchable by script, user, timestamp, operation type
  - Simpler backup and security controls
- **Location:** `config/audit.log` (version controlled structure, ignored data)

**Data Validation Pre-Checks:**
- **Decision:** Automatic validation before workflow execution with human approval of validation report.
- **Rationale:**
  - Fail fast - catch data issues before processing
  - Better user experience - know problems upfront
  - Prevents partial execution with corrupted data
  - Aligns with human-in-loop approval workflow
- **Implementation:** `data-validator` agent checks required columns, data types, non-null values, and presents findings for user approval before executing script.

**Template Customization:**
- **Decision:** Start with generic templates, add Life360 branding in Phase 6.
- **Rationale:** Keep MVP simple, add customization later.
- **Future:** User will provide Life360 logo, color scheme, brand guidelines towards end of development.

**Error Recovery:**
- **Decision:** Save progress on workflow failure, enable resumption.
- **Rationale:**
  - Long-running workflows (monthly close) shouldn't lose progress
  - Network/file issues are recoverable
  - Better user experience
- **Implementation:** Workflows save state to `config/workflow-state/` directory. On failure, user can resume from last checkpoint.

**Testing & Quality Assurance:**
- **Decision:** Version-controlled realistic sample data files for testing. Pre-commit hooks instead of CI/CD.
- **Rationale:**
  - Realistic test data ensures validation accuracy
  - Pre-commit hooks catch issues before they're committed
  - Simple setup without cloud CI/CD complexity
- **Implementation:** `data/samples/` directory with fake budget/actuals. Git pre-commit hook runs pytest, mypy, ruff, bandit.

**Deployment & Access:**
- **Decision:** Single-user, local-only deployment using Python virtual environment.
- **Rationale:**
  - Keep setup simple (no Docker, no cloud infrastructure)
  - Each FP&A professional downloads repo and configures for themselves
  - No multi-user complexity, authentication, or role-based permissions
- **Implementation:** Poetry manages virtual environment. Setup via `poetry install`.

**Security:**
- **Decision:** Simple credential storage (no encryption at rest).
- **Rationale:**
  - Keep MVP simple
  - Credentials stored in `config/credentials/` (git ignored)
  - User responsible for securing their local machine
- **Implementation:** `.gitignore` includes `config/credentials/`. User adds OAuth tokens and service account JSON manually.

**Documentation & Training:**
- **Decision:** Jupyter notebooks for tutorials and guides (not video, not interactive CLI).
- **Rationale:**
  - Executable documentation with sample data
  - Users can modify and experiment
  - Version-controlled, easy to update
- **Implementation:** `docs/notebooks/` directory with tutorials for common workflows (monthly close, variance analysis, board deck generation).

**Monitoring & Notifications:**
- **Decision:** No automated performance metrics or error notifications yet (future addition).
- **Rationale:**
  - Keep MVP simple
  - Claude Code informs user of errors directly
  - Add monitoring/alerting in later phases if needed
- **Implementation:** Future consideration. For now, errors displayed in Claude Code interface and logged to `config/audit.log`.

---

## Approval Signatures

**Product Owner:** _________________________ Date: _________

**FP&A Stakeholder:** _________________________ Date: _________

**Technical Lead:** _________________________ Date: _________

---

**END OF SPECIFICATION**

*This document focuses on WHAT we're building and WHY. Technical implementation details (HOW) will be addressed in separate technical planning documents.*
