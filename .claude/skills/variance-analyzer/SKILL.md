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

**Python Scripts:** (To be implemented in Phase 3-4)
- `scripts/core/variance.py` - Core variance calculation logic
- `scripts/core/favorability.py` - Favorability assessment by account type
- `scripts/integrations/excel_reader.py` - Excel file reading
- `scripts/integrations/excel_writer.py` - Excel output generation

## Testing

**Unit tests required:**
- `tests/unit/test_variance.py` - Variance calculation edge cases
- `tests/unit/test_favorability.py` - All account type favorability logic

**Coverage requirement:** 95%+

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
