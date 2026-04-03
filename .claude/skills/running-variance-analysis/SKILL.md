---
name: running-variance-analysis
description: Use when running variance analysis, comparing budget vs actual, analyzing financial performance, need variance reports, want to generate Excel reports and HTML dashboards, thinking "I need to compare budget to actuals", processing financial data files, or when user provides budget and actuals Excel files - runs the full pipeline producing role-based outputs for analyst, senior analyst, and manager
---

# Running Variance Analysis

## Overview

**Purpose:** Execute end-to-end variance analysis using pre-built scripts that produce Excel reports, HTML dashboards, and HTML presentations with role-based views.

**What this skill does:**
- Loads budget and actuals from Excel files
- Calculates variances with Decimal precision (never float)
- Determines favorability by account type (revenue/expense/asset/liability/cogs)
- Flags material variances (configurable thresholds, default >10% or >$50K)
- Generates role-specific outputs (analyst detail, senior analyst summary, manager executive)

**Key principle:** One command runs the entire pipeline. Users pick their role to get the right level of detail.

---

## When to Use

**Use when:**
- User provides budget and actuals files
- User asks for variance analysis or budget vs actual comparison
- User wants financial dashboards or reports
- User mentions "monthly close" or "variance report"

**Don't use when:**
- User wants to modify the calculation logic (edit scripts/core/ directly)
- User wants to create a new dashboard layout (use generating-dashboards skill)
- User needs data from external systems like Databricks or Adaptive

---

## Step-by-Step Instructions

### Step 1: Identify Input Files

Confirm the user has:
- **Budget file** (Excel .xlsx) with columns: Account Code, Account Name, Account Type, Department, Amount
- **Actuals file** (Excel .xlsx) with the same columns
- **Role** preference: analyst (default), senior_analyst, or manager

If no files provided, offer sample data:
```
data/samples/budget_2025.xlsx
data/samples/actuals_nov_2025.xlsx
```

### Step 2: Run the Pipeline

Execute the variance workflow:

```python
python -m scripts.workflows.variance_workflow <budget_file> <actuals_file> <role>
```

**Roles and their outputs:**

| Role | Excel Report | HTML Dashboard | HTML Presentation |
|------|-------------|----------------|-------------------|
| analyst | Detailed (all accounts) | Full table with sort/filter/search | No |
| senior_analyst | Department summaries | Department cards + review queue | Yes (slide deck) |
| manager | Material variances only | Executive KPIs + traffic lights | Yes (slide deck) |

### Step 3: For All Three Roles at Once

```python
from scripts.workflows.report_generator import generate_role_based_outputs
from scripts.core.variance import calculate_batch_variance
from scripts.integrations.excel_reader import load_budget, load_actuals, dataframe_to_records

budget_df, _ = load_budget("path/to/budget.xlsx")
actuals_df, _ = load_actuals("path/to/actuals.xlsx")
records = dataframe_to_records(budget_df, actuals_df)
results = calculate_batch_variance(records)

outputs = generate_role_based_outputs(results, "output/", {
    "title": "Variance Analysis - November 2025",
    "period": "November 2025",
    "budget_file": "budget.xlsx",
    "actuals_file": "actuals.xlsx",
})
# Creates output/analyst/, output/senior_analyst/, output/manager/ directories
```

### Step 4: Present Results

Show the user:
1. Summary statistics (total accounts, material variances, favorable/unfavorable counts)
2. File paths for all generated outputs
3. Offer to open the HTML dashboard in their browser

---

## Customization Points

Users can customize by editing:

| What | File | How |
|------|------|-----|
| Materiality thresholds | `config/fpa_config.yaml` | Change pct_threshold and abs_threshold |
| Per-category thresholds | `config/fpa_config.yaml` | Add entries under materiality.by_category |
| Account type mappings | `config/fpa_config.yaml` | Change account_type_prefixes |
| Chart of accounts | `config/account_mapping.yaml` | Add/remove/modify accounts |
| Dashboard appearance | `scripts/integrations/html_dashboard.py` | Edit CSS in _generate_css() |
| Presentation theme | `scripts/integrations/html_presentation.py` | Edit _presentation_css() |

---

## Dependencies

**Scripts used:**
- `scripts/core/variance.py` - Variance calculations
- `scripts/core/favorability.py` - Favorability rules
- `scripts/core/materiality.py` - Threshold flagging
- `scripts/core/metrics.py` - KPI scorecard
- `scripts/integrations/excel_reader.py` - Load Excel with Decimal precision
- `scripts/integrations/excel_writer.py` - Multi-sheet Excel output
- `scripts/integrations/html_dashboard.py` - Role-based HTML dashboards
- `scripts/integrations/html_presentation.py` - HTML slide decks
- `scripts/workflows/variance_workflow.py` - Pipeline orchestrator

**Skills:**
- `financial-validator` - Auto-invoked for precision checks

---

## Anti-Patterns

- **Never** use float for currency - all amounts are Decimal
- **Never** silently drop NULL actuals - they are flagged in metadata
- **Never** skip the reconciliation step - unmatched accounts must be reported
- **Always** check the role parameter matches user's organizational level
