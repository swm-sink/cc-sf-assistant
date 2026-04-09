---
name: variance-analyzer
description: Budget vs actual variance analysis with human-in-loop workflows for FP&A professionals
version: 1.0.0
author: claude-code
tags: [prod, fpa, variance, financial-analysis]
---

# Variance Analyzer Skill

**Purpose:** Automate budget vs. actual variance analysis following production-grade workflows with human approval checkpoints.

**Auto-Invocation:** Triggered when user mentions "variance", "budget vs actual", "variance analysis", "variance report", or "material variances"

## Quick Start

This skill provides automated variance analysis capabilities:
- Decimal precision calculations
- Favorability assessment by account type
- Material variance flagging
- Auto-invoked when user mentions "variance", "budget vs actual", etc.

To execute variance analysis, use the slash command:
```
/variance-analysis budget_2025.xlsx actuals_2025_10.xlsx
```

## How This Skill Works

**Auto-Invocation:** This skill is automatically invoked when you mention variance-related keywords in conversation.

**Slash Command:** For explicit execution, use `/variance-analysis` (see `.claude/commands/prod/variance-analysis.md`)

**Workflow:**
- Research → Plan → Implement → Verify
- Human checkpoints at each phase
- Decimal precision enforcement
- Material variance flagging (>10% or >$50K)
- Excel output with 3 sheets (Executive Summary, Detailed, Material Only)

## Progressive Disclosure

**For basic usage:** Mention "variance analysis" in conversation or use `/variance-analysis`

**For detailed workflow:** See `.claude/commands/prod/variance-analysis.md`

**For variance formulas and edge cases:** See `references/` directory (to be created)

## Dependencies

**Skills:**
- `financial-validator` - Decimal precision enforcement
- `decimal-enforcer` - Auto-invoked for currency calculations

**Agents:**
- `code-reviewer` - Independent verification of calculations

**Python Scripts (Implemented):**
- `scripts/core/variance.py` - Core variance calculation logic
- `scripts/core/favorability.py` - Favorability assessment by account type
- `scripts/core/materiality.py` - Materiality threshold flagging
- `scripts/core/metrics.py` - KPI scorecard generation
- `scripts/integrations/excel_reader.py` - Excel file reading with Decimal precision
- `scripts/integrations/excel_writer.py` - Multi-sheet Excel output with conditional formatting
- `scripts/integrations/html_dashboard.py` - Role-based HTML dashboards with Chart.js
- `scripts/integrations/html_presentation.py` - HTML slide-deck presentations
- `scripts/workflows/variance_workflow.py` - End-to-end pipeline orchestrator

**Related Skills:**
- `running-variance-analysis` - Execute the full pipeline
- `generating-dashboards` - Create custom HTML dashboard views
- `generating-presentations` - Create custom HTML slide decks

## Testing

**Unit tests (74 passing):**
- `tests/unit/test_variance.py` - 15 tests: normal, zero budget, both zero, negative, precision
- `tests/unit/test_favorability.py` - 15 tests: all account types, zero variance, invalid type
- `tests/unit/test_materiality.py` - 14 tests: thresholds, boundaries, ranking
- `tests/unit/test_consolidation.py` - 7 tests: multi-dept, duplicates, reconciliation
- `tests/unit/test_metrics.py` - 9 tests: margins, utilization, scorecard
- `tests/unit/test_validator.py` - 14 tests: structure, nulls, decimal conversion

## Example Output

```
Variance Report - October 2025
================================

Material Variances (6 flagged):
  ✅ 4000 Subscription Revenue: +$375k (+15%) FAVORABLE
  ✅ 4020 Enterprise Revenue: +$175k (+21.9%) FAVORABLE
  ❌ 7030 Digital Advertising: +$120k (+40%) UNFAVORABLE
  ❌ 7000 Sales Salaries: +$80k (+20%) UNFAVORABLE
  ...

Total Accounts: 50
Material Favorable: 8
Material Unfavorable: 6
```

## Anti-Patterns

❌ **DON'T:** Skip human approval checkpoints
❌ **DON'T:** Use float for currency calculations
❌ **DON'T:** Silently drop unmatched accounts
❌ **DON'T:** Skip independent verification

✅ **DO:** Follow Research → Plan → Implement → Verify
✅ **DO:** Use Decimal precision throughout
✅ **DO:** Flag unmatched accounts explicitly
✅ **DO:** Get independent code review before delivery

---

**Last Updated:** 2025-11-08
