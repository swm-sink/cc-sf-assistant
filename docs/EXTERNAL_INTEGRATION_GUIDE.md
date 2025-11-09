# External Repository Integration Guide

**Date:** 2025-11-09
**Purpose:** Strategic guide for leveraging 30+ cloned external repositories in FP&A automation development
**Total Repositories Cloned:** 30+ (6 Claude Code infrastructure + 18 domain-specific + 6 prior clones)

---

## Executive Summary

We've cloned a comprehensive set of repositories organized into 10 categories to accelerate FP&A automation development. This guide maps each repository to our meta-infrastructure phases and provides actionable integration strategies.

**Key Principle:** Learn patterns, don't copy-paste. These repos provide battle-tested approaches we adapt to our financial precision requirements (Decimal enforcement, audit trails).

---

## Repository Organization

```
external/
├── claude-code/                    # Meta-Infrastructure Patterns (6 repos)
│   ├── wshobson-agents/            # 85 agents, 47 skills production system
│   ├── claude-code-spec-workflow/  # RPIV workflow + dashboard
│   ├── claude-code-skill-factory/  # Skill generation factories
│   ├── awesome-claude-code/        # Community command catalog
│   ├── awesome-claude-code-subagents/ # 65+ specialized agents
│   └── anthropics-skills/          # Official Anthropic skills
│
├── financial-modeling/             # Financial Calculations (3 repos)
│   ├── FinanceToolkit/             # 150+ financial ratios
│   ├── mplfinance/                 # Financial visualization
│   └── pyxirr/                     # IRR/NPV calculations
│
├── data-warehouse/                 # SQL & Analytics (2 repos)
│   ├── duckdb/                     # In-process SQL database
│   └── great-expectations/         # Data validation framework
│
├── precision-currency/             # Decimal Precision (1 repo + 1 prior)
│   ├── stockholm/                  # 100% test coverage, Decimal-backed
│   └── ../py-money/                # Vimeo production currency lib
│
├── data-validation/                # Validation & Testing (3 repos)
│   ├── hypothesis/                 # Property-based testing
│   ├── pandera/                    # DataFrame validation
│   └── typeguard/                  # Runtime type checking
│
├── audit-compliance/               # Audit Trails (1 repo)
│   └── python-audit-log/           # Uniform audit logging
│
├── reporting-automation/           # Excel & Reports (2 repos + 1 prior)
│   ├── XlsxWriter/                 # Excel file generation
│   ├── great-tables/               # Advanced table formatting
│   └── ../gspread/                 # Google Sheets automation
│
├── etl-pipelines/                  # Orchestration (2 repos)
│   ├── dbt-core/                   # SQL transformation patterns
│   └── prefect/                    # Python workflow orchestration
│
├── reconciliation/                 # Fuzzy Matching (2 repos)
│   ├── dedupe/                     # ML-based fuzzy matching
│   └── splink/                     # Probabilistic record linkage
│
└── api-integration/                # REST API (2 repos)
    ├── google-api-python-client/   # OAuth 2.0, batch requests
    └── tenacity/                   # Retry library
```

---

## Integration by Meta-Infrastructure Priority

**⚠️ NOTE:** Sections below are ordered by Priority (implementation order), not Phase (document order).

**Implementation Sequence:**
- Priority 1: Development Workflows (Phase 7 in docs) - Week 1-2
- Priority 2: Shared Foundation (Phase 1 in docs) - Week 3
- Priority 3: Production Infrastructure (Phases 2-6 in docs) - Week 4-13
- Priority 4: Orchestration (Phase 8 in docs) - Week 14

---

### Priority 1: Development Workflows (Week 1-2) ⭐ **IMPLEMENT FIRST**

**Phase in Docs:** Phase 7 (Development Workflows)
**Goals:** python-best-practices, test-suite-generator, @script-generator, /create-script

#### Primary Repos to Study:
1. **hypothesis (data-validation/)** - Property-based testing
   - **Location:** `external/data-validation/hypothesis/`
   - **Key Files:**
     - `hypothesis/strategies.py` - Data generators
     - `hypothesis-python/examples/` - Test examples
   - **Extract:**
     ```python
     from hypothesis import given, strategies as st
     from decimal import Decimal

     # Pattern: Property-based testing for financial functions
     @given(
         actual=st.decimals(min_value=0, max_value=1000000, places=2),
         budget=st.decimals(min_value=0, max_value=1000000, places=2)
     )
     def test_variance_calculation_properties(actual: Decimal, budget: Decimal):
         variance = calculate_variance(actual, budget)

         # Property: variance = actual - budget
         assert variance == actual - budget

         # Property: reversibility
         assert budget + variance == actual
     ```
   - **Adapt For:** `test-suite-generator` skill - generate edge case tests

2. **typeguard (data-validation/)** - Runtime type checking
   - **Location:** `external/data-validation/typeguard/`
   - **Key Files:**
     - `src/typeguard/_decorators.py` - @typechecked decorator
     - `src/typeguard/_functions.py` - check_type function
   - **Extract:**
     ```python
     from typeguard import typechecked

     @typechecked
     def calculate_variance(actual: Decimal, budget: Decimal) -> Decimal:
         return actual - budget  # Runtime error if wrong types passed
     ```
   - **Adapt For:** Enforce Decimal types at runtime in all financial functions

3. **python-audit-log (audit-compliance/)** - Audit logging patterns
   - **Location:** `external/audit-compliance/python-audit-log/`
   - **Adapt For:** python-best-practices skill - audit trail enforcement

**Deliverable:** Development tools that will build ALL subsequent components

**Once Complete:** Use these tools to build Priorities 2-4

---

### Priority 2: Shared Foundation (Week 3)

**Phase in Docs:** Phase 1 (Shared Foundation)
**Goals:** decimal-precision-enforcer, audit-trail-enforcer, /setup command
**Built Using:** Priority 1 development tools

#### Primary Repos to Study:
1. **stockholm (precision-currency/)** - Decimal precision patterns
   - **Location:** `external/precision-currency/stockholm/`
   - **Key Files:**
     - `stockholm/money.py` - Immutable Money class with Decimal
     - `stockholm/currency.py` - Currency validation
     - `tests/` - 100% test coverage examples
   - **Extract:**
     ```python
     # Pattern: Type enforcement at initialization
     class Money:
         def __init__(self, amount: Union[str, int, Decimal], currency: str):
             if not isinstance(amount, Decimal):
                 amount = Decimal(str(amount))
             self._amount = amount
     ```
   - **Adapt For:** `decimal-precision-enforcer` skill - block float usage, enforce Decimal

2. **py-money (external/py-money/)** - Production currency handling (Vimeo)
   - **Location:** `external/py-money/`
   - **Key Files:**
     - `money/money.py` - Currency enforcement patterns
     - `money/currency.py` - Currency validation
   - **Extract:**
     ```python
     # Pattern: Arithmetic operations with type preservation
     def __add__(self, other: Money) -> Money:
         if not isinstance(other, Money):
             raise TypeError("Cannot add Money to non-Money")
         if self.currency != other.currency:
             raise ValueError("Cannot add different currencies")
         return Money(self.amount + other.amount, self.currency)
     ```
   - **Adapt For:** Our variance calculation logic with strict type checking

3. **python-audit-log (audit-compliance/)** - Audit logging patterns
   - **Location:** `external/audit-compliance/python-audit-log/`
   - **Key Files:**
     - `audit_log/` - Structured audit logging
     - `audit_log/middleware.py` - Auto-logging patterns
   - **Extract:**
     ```python
     # Pattern: Uniform audit log format
     audit_log.info(
         "data_transformation",
         extra={
             "timestamp": datetime.utcnow(),
             "user": get_current_user(),
             "source": "databricks_extract",
             "operation": "extract_actuals",
             "metadata": {"rows": 1000, "columns": 10}
         }
     )
     ```
   - **Adapt For:** `audit-trail-enforcer` skill - centralized audit logging to `config/audit.log`

4. **typeguard (data-validation/)** - Runtime type checking
   - **Location:** `external/data-validation/typeguard/`
   - **Key Files:**
     - `src/typeguard/_decorators.py` - @typechecked decorator
     - `src/typeguard/_functions.py` - check_type function
   - **Extract:**
     ```python
     from typeguard import typechecked

     @typechecked
     def calculate_variance(actual: Decimal, budget: Decimal) -> Decimal:
         return actual - budget  # Runtime error if wrong types passed
     ```
   - **Adapt For:** Enforce Decimal types at runtime in all financial functions

**Deliverable:** Shared foundation skills with patterns validated by production systems

---

### Priority 3a: Data Extraction (Week 4-5)

**Phase in Docs:** Phase 2 (Data Extraction)
**Goals:** Databricks/Adaptive extraction, validation agents
**Built Using:** Priority 1 development tools

#### Primary Repos to Study:
1. **great-expectations (data-warehouse/)** - Data validation framework
   - **Location:** `external/data-warehouse/great-expectations/`
   - **Key Files:**
     - `great_expectations/expectations/` - Built-in expectations
     - `great_expectations/dataset/` - Dataset validation
   - **Extract:**
     ```python
     # Pattern: Declarative data validation
     df_expectations = {
         "expect_column_to_exist": ["actual", "budget", "account"],
         "expect_column_values_to_not_be_null": ["actual", "budget"],
         "expect_column_values_to_be_of_type": {
             "actual": "decimal",
             "budget": "decimal"
         }
     }
     ```
   - **Adapt For:** `@databricks-validator` and `@adaptive-validator` agents

2. **pandera (data-validation/)** - DataFrame validation
   - **Location:** `external/data-validation/pandera/`
   - **Key Files:**
     - `pandera/api/pandas/` - Pandas schema validation
     - `pandera/dtypes.py` - Custom data types
   - **Extract:**
     ```python
     import pandera as pa
     from decimal import Decimal

     # Pattern: Schema definition with custom types
     class DatabricksActualsSchema(pa.DataFrameModel):
         account: str = pa.Field(nullable=False)
         actual: Decimal = pa.Field(ge=0)  # >= 0
         period: str = pa.Field(regex=r"^\d{4}-\d{2}$")

         class Config:
             strict = True
             coerce = True
     ```
   - **Adapt For:** Validate extracted data before processing

3. **tenacity (api-integration/)** - Retry logic
   - **Location:** `external/api-integration/tenacity/`
   - **Key Files:**
     - `tenacity/__init__.py` - Retry decorators
     - `tenacity/wait.py` - Backoff strategies
   - **Extract:**
     ```python
     from tenacity import retry, stop_after_attempt, wait_exponential

     @retry(
         stop=stop_after_attempt(3),
         wait=wait_exponential(multiplier=1, min=2, max=10),
         reraise=True
     )
     def extract_databricks_actuals(query: str) -> pd.DataFrame:
         # API call with automatic retry
         return databricks_client.execute_query(query)
     ```
   - **Adapt For:** All external API calls (Databricks, Adaptive, Google)

**Deliverable:** Robust extraction skills with validation and retry logic

---

### Priority 3b: Account Reconciliation (Week 6)

**Phase in Docs:** Phase 3 (Account Reconciliation)
**Goals:** Fuzzy account matching, reconciliation workflow
**Built Using:** Priority 1 development tools

#### Primary Repos to Study:
1. **splink (reconciliation/)** - Probabilistic record linkage
   - **Location:** `external/reconciliation/splink/`
   - **Key Files:**
     - `splink/linker.py` - Main linkage API
     - `splink/comparison_library.py` - Comparison functions
   - **Extract:**
     ```python
     from splink import Linker, DuckDBAPI

     # Pattern: Probabilistic fuzzy matching
     settings = {
         "link_type": "dedupe_only",
         "comparisons": [
             cl.jaro_winkler_at_thresholds("account_name", [0.9, 0.8, 0.7]),
             cl.exact_match("account_code"),
         ],
         "blocking_rules_to_generate_predictions": [
             "l.account_code = r.account_code",
             "l.account_name[1:3] = r.account_name[1:3]",
         ]
     }
     linker = Linker(df, settings, DuckDBAPI())
     matches = linker.predict()
     ```
   - **Adapt For:** `account-mapper` skill - match Databricks accounts to Adaptive accounts

2. **dedupe (reconciliation/)** - ML-based fuzzy matching
   - **Location:** `external/reconciliation/dedupe/`
   - **Key Files:**
     - `dedupe/core.py` - Dedupe main API
     - `dedupe/variables/` - Field types
   - **Extract:**
     ```python
     import dedupe

     # Pattern: Active learning for account matching
     fields = [
         {'field': 'account_name', 'type': 'String'},
         {'field': 'account_code', 'type': 'String'},
         {'field': 'department', 'type': 'Categorical'},
     ]
     deduper = dedupe.Dedupe(fields)
     deduper.prepare_training(data)
     # Interactive training...
     deduper.train()
     clusters = deduper.partition(data)
     ```
   - **Adapt For:** `@account-reconciler` agent - suggest high-confidence matches

3. **duckdb (data-warehouse/)** - Local SQL analysis
   - **Location:** `external/data-warehouse/duckdb/`
   - **Key Files:**
     - `tools/pythonpkg/` - Python API
     - `examples/` - SQL examples
   - **Extract:**
     ```python
     import duckdb

     # Pattern: In-memory SQL for fast local analysis
     conn = duckdb.connect(":memory:")
     conn.execute("""
         SELECT
             a.account AS databricks_account,
             b.account AS adaptive_account,
             jaro_winkler_similarity(a.account, b.account) AS similarity
         FROM databricks_actuals a
         CROSS JOIN adaptive_budget b
         WHERE similarity > 0.8
         ORDER BY similarity DESC
     """)
     matches = conn.fetchdf()
     ```
   - **Adapt For:** Fast local reconciliation analysis

**Deliverable:** Intelligent account reconciliation with human review workflow

---

### Priority 3c: Reporting (Week 7-8)

**Phase in Docs:** Phase 4 (Reporting)
**Goals:** Excel report generation with formatting
**Built Using:** Priority 1 development tools

#### Primary Repos to Study:
1. **XlsxWriter (reporting-automation/)** - Excel generation
   - **Location:** `external/reporting-automation/XlsxWriter/`
   - **Key Files:**
     - `xlsxwriter/workbook.py` - Workbook API
     - `xlsxwriter/worksheet.py` - Formatting methods
   - **Extract:**
     ```python
     import xlsxwriter
     from decimal import Decimal

     # Pattern: Rich Excel formatting
     workbook = xlsxwriter.Workbook('variance_report.xlsx')
     worksheet = workbook.add_worksheet('P&L Variance')

     # Formats
     header_format = workbook.add_format({
         'bold': True,
         'bg_color': '#4F81BD',
         'font_color': 'white'
     })
     currency_format = workbook.add_format({
         'num_format': '$#,##0.00',
         'align': 'right'
     })
     percent_format = workbook.add_format({
         'num_format': '0.00%',
         'align': 'center'
     })

     # Conditional formatting for variances
     worksheet.conditional_format('D2:D100', {
         'type': 'cell',
         'criteria': '<',
         'value': 0,
         'format': workbook.add_format({'bg_color': '#FFC7CE'})  # Red
     })
     ```
   - **Adapt For:** `excel-report-generator` skill

2. **great-tables (reporting-automation/)** - Advanced table formatting
   - **Location:** `external/reporting-automation/great-tables/`
   - **Key Files:**
     - `great_tables/gt.py` - Main GT class
     - `great_tables/formatting.py` - Number formatting
   - **Extract:**
     ```python
     from great_tables import GT
     from great_tables.data import sp500

     # Pattern: Publication-quality table formatting
     (
         GT(variance_df)
         .tab_header(title="P&L Variance Analysis", subtitle="October 2024")
         .fmt_currency(columns=["actual", "budget", "variance"], currency="USD")
         .fmt_percent(columns=["variance_pct"], decimals=1)
         .data_color(
             columns=["variance"],
             palette=["red", "white", "green"],
             domain=[-100000, 0, 100000]
         )
     )
     ```
   - **Adapt For:** Dashboard-ready table outputs

3. **gspread (external/gspread/)** - Google Sheets automation
   - **Location:** `external/gspread/`
   - **Key Files:**
     - `gspread/client.py` - Sheets API client
     - `gspread/worksheet.py` - Worksheet operations
   - **Extract:**
     ```python
     import gspread
     from gspread_dataframe import set_with_dataframe

     # Pattern: OAuth + batch updates
     gc = gspread.oauth()
     sheet = gc.open("Monthly Close Dashboard").worksheet("Variance")

     # Batch update to minimize API calls
     set_with_dataframe(
         sheet,
         variance_df,
         include_index=False,
         include_column_header=True,
         resize=True
     )
     ```
   - **Adapt For:** `google-sheets-updater` skill

**Deliverable:** Professional Excel and Google Sheets reports

---

### Priority 3d: Google Integration (Week 9-11)

**Phase in Docs:** Phase 5 (Google Workspace Integration)
**Goals:** Google Slides/Sheets updates with OAuth
**Built Using:** Priority 1 development tools

#### Primary Repos to Study:
1. **google-api-python-client (api-integration/)** - Google Workspace APIs
   - **Location:** `external/api-integration/google-api-python-client/`
   - **Key Files:**
     - `googleapiclient/discovery.py` - Service discovery
     - `samples/` - API examples
   - **Extract:**
     ```python
     from google.oauth2 import service_account
     from googleapiclient.discovery import build

     # Pattern: Service account authentication
     SCOPES = ['https://www.googleapis.com/auth/presentations']
     credentials = service_account.Credentials.from_service_account_file(
         'credentials.json',
         scopes=SCOPES
     )
     slides_service = build('slides', 'v1', credentials=credentials)

     # Batch update slides
     requests = [
         {
             'replaceAllText': {
                 'containsText': {'text': '{{variance}}'},
                 'replaceText': '$1,234,567'
             }
         }
     ]
     slides_service.presentations().batchUpdate(
         presentationId=presentation_id,
         body={'requests': requests}
     ).execute()
     ```
   - **Adapt For:** `google-slides-updater` skill

2. **gspread + gspread-dataframe** - See Phase 4 above
   - **Pattern:** OAuth flow for user consent
   - **Adapt For:** `google-sheets-updater` skill

**Deliverable:** Automated dashboard updates with OAuth

---

### Priority 3e: Forecast Maintenance (Week 12-13)

**Phase in Docs:** Phase 6 (Forecast Maintenance)
**Goals:** Rolling forecast updates, assumption tracking
**Built Using:** Priority 1 development tools

#### Primary Repos to Study:
1. **FinanceToolkit (financial-modeling/)** - Financial ratios and calculations
   - **Location:** `external/financial-modeling/FinanceToolkit/`
   - **Key Files:**
     - `financetoolkit/base/` - Base calculations
     - `financetoolkit/ratios/` - Financial ratios
   - **Extract:**
     ```python
     from financetoolkit import Toolkit

     # Pattern: Financial metric calculations
     companies = Toolkit(["AAPL", "MSFT"], api_key="YOUR_KEY")

     # Growth rates
     revenue_growth = companies.ratios.get_revenue_growth()

     # Adapt pattern for forecast assumptions
     def calculate_growth_rate(actuals: List[Decimal], periods: int = 3) -> Decimal:
         # Use trailing N periods to project forward
         recent_actuals = actuals[-periods:]
         return (recent_actuals[-1] / recent_actuals[0]) ** (1 / periods) - 1
     ```
   - **Adapt For:** `forecast-updater` skill - trend-based projections

2. **pyxirr (financial-modeling/)** - IRR/NPV calculations
   - **Location:** `external/financial-modeling/pyxirr/`
   - **Key Files:**
     - `src/pyxirr.pyi` - Type stubs
     - `tests/` - Usage examples
   - **Extract:**
     ```python
     from pyxirr import xirr, xnpv
     from datetime import date

     # Pattern: High-performance financial calculations
     dates = [date(2024, 1, 1), date(2024, 6, 1), date(2024, 12, 1)]
     amounts = [-1000, 500, 600]  # Investment, returns

     irr_rate = xirr(dates, amounts)
     npv_value = xnpv(0.10, dates, amounts)
     ```
   - **Adapt For:** Investment analysis in forecasts

3. **mplfinance (financial-modeling/)** - Financial visualization
   - **Location:** `external/financial-modeling/mplfinance/`
   - **Key Files:**
     - `src/mplfinance/` - Plotting functions
     - `examples/` - Chart examples
   - **Extract:**
     ```python
     import mplfinance as mpf

     # Pattern: Financial time series visualization
     mpf.plot(
         variance_df,
         type='line',
         title='Variance Trend Analysis',
         ylabel='Variance ($)',
         style='charles',
         volume=False
     )
     ```
   - **Adapt For:** Variance trend visualization

**Deliverable:** Intelligent forecast updates with assumption tracking

---

### ~~Phase 7: Development Workflows~~ → SEE PRIORITY 1 ABOVE ⭐

**Note:** This section originally appeared here but has been **MOVED TO PRIORITY 1** (top of document) as it must be implemented FIRST.

#### Primary Repos to Study:
1. **hypothesis (data-validation/)** - Property-based testing
   - **Location:** `external/data-validation/hypothesis/`
   - **Key Files:**
     - `hypothesis/strategies.py` - Data generators
     - `hypothesis-python/examples/` - Test examples
   - **Extract:**
     ```python
     from hypothesis import given, strategies as st
     from decimal import Decimal

     # Pattern: Property-based testing for financial functions
     @given(
         actual=st.decimals(min_value=0, max_value=1000000, places=2),
         budget=st.decimals(min_value=0, max_value=1000000, places=2)
     )
     def test_variance_calculation_properties(actual: Decimal, budget: Decimal):
         variance = calculate_variance(actual, budget)

         # Property: variance = actual - budget
         assert variance == actual - budget

         # Property: reversibility
         assert budget + variance == actual
     ```
   - **Adapt For:** `test-suite-generator` skill - generate edge case tests

2. **pandera (data-validation/)** - See Phase 2 above
   - **Pattern:** Schema-based testing for DataFrames
   - **Adapt For:** Validate script inputs/outputs

**Deliverable:** TDD workflow with >95% coverage (moved to Priority 1)

---

### Priority 4: Orchestration (Week 14)

**Phase in Docs:** Phase 8 (Orchestration)
**Goals:** Full monthly close workflow
**Built Using:** Priority 1 development tools
**Runtime Dependencies:** ALL Priority 3 components

#### Primary Repos to Study:
1. **prefect (etl-pipelines/)** - Python workflow orchestration
   - **Location:** `external/etl-pipelines/prefect/`
   - **Key Files:**
     - `src/prefect/` - Core orchestration
     - `examples/` - Workflow examples
   - **Extract:**
     ```python
     from prefect import flow, task

     @task(retries=3, retry_delay_seconds=60)
     def extract_databricks():
         return extract_databricks_actuals()

     @task(retries=3)
     def extract_adaptive():
         return extract_adaptive_budget()

     @task
     def reconcile_accounts(actuals_df, budget_df):
         return reconcile_accounts_workflow(actuals_df, budget_df)

     @flow(name="monthly-close")
     def monthly_close_flow():
         actuals = extract_databricks()
         budget = extract_adaptive()
         reconciled = reconcile_accounts(actuals, budget)
         report = generate_variance_report(reconciled)
         return report
     ```
   - **Adapt For:** `/prod:monthly-close` command orchestration

2. **dbt-core (etl-pipelines/)** - SQL transformation patterns
   - **Location:** `external/etl-pipelines/dbt-core/`
   - **Key Files:**
     - `core/dbt/` - Core transformations
     - `core/dbt/task/` - Task orchestration
   - **Extract:**
     ```sql
     -- Pattern: Incremental data models with audit fields
     {{ config(
         materialized='incremental',
         unique_key='account_id',
         on_schema_change='append_new_columns'
     ) }}

     SELECT
         account_id,
         account_name,
         actual_amount,
         budget_amount,
         actual_amount - budget_amount AS variance,
         CURRENT_TIMESTAMP AS processed_at,
         '{{ run_started_at }}' AS run_id
     FROM {{ source('databricks', 'actuals') }}
     ```
   - **Adapt For:** SQL-based data transformation patterns

**Deliverable:** End-to-end monthly close orchestration

---

## Claude Code Infrastructure Patterns

### Patterns from wshobson/agents (85 agents production system)

**Location:** `external/claude-code/wshobson-agents/`

**Key Learnings:**
1. **Model Selection Strategy:**
   - Haiku (47 agents): Fast, deterministic tasks (validators, formatters)
   - Sonnet (97 agents): Complex reasoning (planners, analyzers)
   - **Apply To:** Use Haiku for `@databricks-validator`, `@report-formatter`; Sonnet for `@account-reconciler`, `@assumption-analyzer`

2. **Progressive Disclosure Pattern:**
   ```yaml
   # YAML frontmatter (always loaded, ~30-50 tokens)
   name: variance-analyzer
   model: sonnet
   tools: [Read, Grep, Bash]

   # Instructions (loaded when activated)
   Calculate variance between actual and budget...

   # References (loaded on demand)
   See references/edge-cases.md for comprehensive test cases
   ```
   - **Apply To:** All our skills follow this pattern

3. **Plugin Architecture:**
   - Plugins group related agents/skills (e.g., `financial-analysis/` plugin with 10 agents)
   - **Apply To:** Consider grouping our agents by phase (extraction/, reconciliation/, reporting/)

### Patterns from claude-code-spec-workflow (RPIV + Dashboard)

**Location:** `external/claude-code/claude-code-spec-workflow/`

**Key Learnings:**
1. **Context Optimization (60-80% token reduction):**
   ```python
   # Pattern: Context extraction commands
   /get-steering-context  # Get high-level project goals
   /get-spec-context      # Get specific requirements
   /get-template-context  # Get code templates
   ```
   - **Apply To:** Create `/get-meta-context` for efficient access to meta-infrastructure docs

2. **Task Breakdown:**
   - Main task → subtasks with unique IDs
   - Each subtask gets auto-generated command: `/<name>-task-<id>`
   - **Apply To:** Break monthly close into subtasks (extract-task-1, reconcile-task-2, etc.)

### Patterns from claude-code-skill-factory (Skill Generation)

**Location:** `external/claude-code/claude-code-skill-factory/`

**Key Learnings:**
1. **Enhanced YAML Frontmatter:**
   ```yaml
   name: decimal-precision-enforcer
   model: sonnet
   color: "#FFD700"        # Gold (financial precision)
   field: finance
   expertise: ["decimal-arithmetic", "type-safety", "financial-compliance"]
   tools: [Read, Edit]
   auto_invoke: true
   ```
   - **Apply To:** Add `field: finance` and `expertise` to all our skills

2. **7-Point Quality Validation:**
   - Clear purpose
   - Proper tool permissions
   - Example usage
   - Anti-patterns documented
   - Edge cases listed
   - References provided
   - Success criteria defined
   - **Apply To:** Use for all our component quality gates

### Patterns from anthropics/skills (Official Skills)

**Location:** `external/claude-code/anthropics-skills/`

**Key Learnings:**
1. **Official Skills to Leverage:**
   - `xlsx` - Excel operations (already available)
   - `pdf` - PDF parsing (future use)
   - `jupyter` - Notebook integration (future use)

2. **Skill Invocation Patterns:**
   ```markdown
   Auto-invoke triggers:
   - Keyword matching: "variance" → variance-analyzer
   - File pattern: *.xlsx → xlsx skill
   - Task type: "calculate" + "financial" → financial-validator
   ```
   - **Apply To:** Define clear auto-invoke triggers for our skills

---

## Dependencies to Add to pyproject.toml

Based on cloned repos, these should be installed via pip (not cloned):

```toml
[project]
dependencies = [
    # Core dependencies (already likely installed)
    "pandas>=2.0.0",
    "openpyxl>=3.1.0",

    # Precision & Currency
    "stockholm>=0.3.0",  # Decimal-based money handling

    # Data Validation
    "pydantic>=2.0.0",  # Type validation
    "pandera>=0.17.0",  # DataFrame validation
    "typeguard>=4.0.0",  # Runtime type checking
    "hypothesis>=6.90.0",  # Property-based testing

    # API Integration
    "tenacity>=8.2.0",  # Retry logic
    "google-api-python-client>=2.100.0",  # Google Workspace APIs
    "google-auth>=2.23.0",  # Google authentication
    "google-auth-oauthlib>=1.1.0",  # OAuth flow
    "gspread>=5.12.0",  # Google Sheets wrapper
    "gspread-dataframe>=3.3.0",  # Pandas integration

    # Reporting
    "xlsxwriter>=3.1.0",  # Excel generation
    "great-tables>=0.2.0",  # Table formatting

    # Financial Calculations
    "pyxirr>=0.10.0",  # IRR/NPV calculations

    # Reconciliation
    "rapidfuzz>=3.5.0",  # Fuzzy string matching (faster than fuzzywuzzy)

    # Data Warehouse
    "duckdb>=0.9.0",  # In-process SQL
    "great-expectations>=0.18.0",  # Data validation

    # Audit & Compliance
    # (python-audit-log patterns to implement ourselves)
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.7.0",
    "ruff>=0.1.0",
]

orchestration = [
    "prefect>=2.14.0",  # Workflow orchestration (Phase 8)
]

visualization = [
    "mplfinance>=0.12.0",  # Financial charts
    "matplotlib>=3.8.0",
    "seaborn>=0.13.0",
]
```

---

## Integration Priority by Implementation Order

### Priority 1: Development Workflows (Week 1-2) ⭐ FIRST
1. **hypothesis** - Property-based testing patterns
2. **typeguard** - Runtime type checking
3. **python-audit-log** - Audit trail patterns

### Priority 2: Shared Foundation (Week 3)
1. **stockholm** - Decimal precision patterns
2. **py-money** - Currency validation

### Priority 3: Production Infrastructure (Week 4-13)

**Priority 3a (Week 4-5): Data Extraction**
1. **pandera** - DataFrame validation
2. **great-expectations** - Data quality checks
3. **tenacity** - Retry logic

**Priority 3b (Week 6): Account Reconciliation**
1. **splink** - Probabilistic record linkage
2. **dedupe** - ML-based fuzzy matching
3. **duckdb** - Local SQL analysis

**Priority 3c (Week 7-8): Reporting**
1. **XlsxWriter** - Excel generation
2. **great-tables** - Table formatting

**Priority 3d (Week 9-11): Google Integration**
1. **google-api-python-client** - Google Workspace APIs
2. **gspread** - Google Sheets automation

**Priority 3e (Week 12-13): Forecast Maintenance**
1. **FinanceToolkit** - Financial ratios
2. **pyxirr** - IRR/NPV calculations
3. **mplfinance** - Financial visualization

### Priority 4: Orchestration (Week 14)
1. **prefect** - Workflow orchestration
2. **dbt-core** - SQL transformation patterns

---

## Code Pattern Extraction Checklist

For each cloned repo, extract:

- [ ] **Core Patterns:** Key algorithms/approaches (fuzzy matching, retry logic, etc.)
- [ ] **Type Safety:** How they enforce types (decorators, runtime checks)
- [ ] **Error Handling:** Exception patterns, user-friendly messages
- [ ] **Testing Patterns:** Edge cases, property-based tests, fixtures
- [ ] **API Design:** Function signatures, return types, documentation
- [ ] **Performance:** Optimization techniques for large datasets

---

## Proof of Concept Priorities

### POC 1: Property-Based Test Generation (Priority 1) ⭐ FIRST
**Goal:** Validate automated test generation with edge cases
**Repos:** hypothesis, typeguard
**Test:** Generate comprehensive test suite for variance calculation
**Why First:** Validates dev tools work before building other components

### POC 2: Decimal Precision Enforcement (Priority 2)
**Goal:** Validate that all financial calculations use Decimal
**Repos:** stockholm, py-money, typeguard
**Test:** Create variance calculation with float rejection
**Depends On:** POC 1 (test generation)

### POC 3: Fuzzy Account Matching (Priority 3b)
**Goal:** Match Databricks accounts to Adaptive accounts
**Repos:** splink, dedupe, duckdb
**Test:** 100-account sample dataset with 80%+ match accuracy
**Depends On:** POC 1 (test framework), POC 2 (precision enforcement)

### POC 4: Excel Report Generation (Priority 3c)
**Goal:** Generate formatted variance report
**Repos:** XlsxWriter, great-tables
**Test:** Multi-tab report with conditional formatting
**Depends On:** POC 1, POC 2

### POC 5: Google Workspace Integration (Priority 3d)
**Goal:** Update Slides and Sheets via API
**Repos:** google-api-python-client, gspread
**Test:** OAuth flow + batch updates
**Depends On:** POC 1, POC 2

### POC 6: Workflow Orchestration (Priority 4)
**Goal:** End-to-end monthly close
**Repos:** prefect
**Test:** 5-step workflow with error handling
**Depends On:** All Priority 3 POCs complete

---

## Success Metrics

### Code Quality:
- [ ] 100% of currency calculations use Decimal (validated by stockholm/py-money patterns)
- [ ] All DataFrames validated with pandera schemas
- [ ] All API calls have retry logic (tenacity patterns)
- [ ] All external data validated (great-expectations patterns)

### Testing:
- [ ] >95% test coverage (hypothesis property-based tests)
- [ ] Edge cases covered (from financial-validator + hypothesis)
- [ ] Integration tests for all workflows

### Performance:
- [ ] <2 seconds for variance calculation (100 accounts)
- [ ] <5 seconds for fuzzy matching (1000 accounts)
- [ ] <10 seconds for Excel report generation

---

## Next Steps

1. **Update pyproject.toml** - Add production dependencies
2. **Create POC 1** - Decimal precision enforcement proof of concept
3. **Extract Patterns** - Document top 5 patterns from each priority repo
4. **Begin Phase 1** - Start building shared foundation using learned patterns

---

**Last Updated:** 2025-11-09
**Status:** ✅ READY FOR IMPLEMENTATION
**Total Repos Cloned:** 30+ organized and mapped to meta-infrastructure phases
