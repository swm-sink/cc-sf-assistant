---
description: Budget vs actual variance analysis with human-in-loop checkpoints
---

# Variance Analysis Command

**Usage:** `/variance-analysis <budget_file> <actual_file> [output_file]`

**Purpose:** Automated budget vs. actual variance analysis following spec-driven workflow with human checkpoints.

---

## Workflow (Human-in-Loop)

### STEP 1: RESEARCH Phase

Investigate the data WITHOUT writing code:

1. **Load and inspect budget file:** $1
   - Document structure (columns, data types, date formats)
   - Count accounts and identify any anomalies
   - Note date range covered

2. **Load and inspect actuals file:** $2
   - Document structure (must match budget for comparison)
   - Identify structural differences from budget
   - Note missing accounts or periods

3. **Load configuration:**
   - Read `spec.md` for materiality thresholds (default: 10% or $50K)
   - Read `spec.md` for favorability rules by account type

4. **Generate Research Summary:**
   - Budget file structure and stats
   - Actuals file structure and stats
   - Compatibility assessment
   - Potential issues identified

**CHECKPOINT 1:** Present research findings. Wait for human approval to proceed.

---

### STEP 2: PLAN Phase

Create detailed specification WITHOUT implementing:

1. **Data Matching Strategy:**
   - How will accounts be matched? (account_code, account_name, etc.)
   - How to handle unmatched accounts?
   - What reconciliation report format?

2. **Calculation Logic:**
   - Absolute variance formula: `Actual - Budget`
   - Percentage variance formula: `((Actual - Budget) / Budget) * 100`
   - Edge case handling:
     - Budget=0, Actual≠0 → Variance=$Actual, %=N/A
     - Budget=0, Actual=0 → Variance=$0, %=0%, "No Activity"
     - Negative values → Calculate normally

3. **Favorability Assessment:**
   - Revenue: Actual > Budget = Favorable
   - Expense: Actual < Budget = Favorable
   - Asset: Actual > Budget = Favorable
   - Liability: Actual < Budget = Favorable

4. **Materiality Flagging:**
   - Material if: `|%Variance| > 10%` OR `|$Variance| > $50,000`

5. **Output Specification:**
   - Sheet 1: Executive Summary
   - Sheet 2: Detailed Variance Analysis
   - Sheet 3: Material Variances Only
   - File location: $3 or `data/output/variance_analysis_{YYYY-MM-DD}.xlsx`

**CHECKPOINT 2:** Present plan. Wait for human approval.

---

### STEP 3: IMPLEMENT Phase

Execute task-by-task with progress tracker:

**Implementation Plan:**

| Task | Status | Notes |
|------|--------|-------|
| 1. Load and validate budget data | Pending | Use financial-validator skill |
| 2. Load and validate actuals data | Pending | Use financial-validator skill |
| 3. Match accounts and reconcile | Pending | Flag unmatched |
| 4. Calculate variances | Pending | Use Decimal precision |
| 5. Apply favorability logic | Pending | Per account type |
| 6. Flag material variances | Pending | 10% or $50K threshold |
| 7. Generate Excel output | Pending | 3 sheets + formatting |
| 8. Validate output | Pending | Spot-check calculations |

**Execute each task:**
- Mark task "In Progress"
- Implement with Decimal precision
- Mark task "Complete"
- Show result summary

**CHECKPOINT 3:** After each major phase (load data, calculations, output generation), pause for review.

---

### STEP 4: VERIFY Phase

Independent validation before delivery:

1. **Invoke @code-reviewer subagent:**
   ```
   @code-reviewer Please verify variance calculation implementation:
   - Check Decimal precision throughout
   - Validate edge case handling (zero division, negatives)
   - Confirm favorability logic for all account types
   - Verify materiality threshold application
   ```

2. **Run validation script:**
   ```bash
   python .claude/skills/financial-validator/scripts/validate_precision.py
   ```

3. **Manual spot-checks:**
   - Pick 3 random accounts
   - Manually calculate variance
   - Compare to automated output
   - Verify favorability and materiality flags

4. **Output quality check:**
   - Excel file opens without errors
   - All sheets present and formatted
   - Conditional formatting applied
   - Metadata included (timestamp, source files, thresholds)

**CHECKPOINT 4:** Present verification results. Wait for final approval.

---

## Success Criteria

Before marking complete:

- [ ] All accounts matched or explicitly flagged as unmatched
- [ ] Zero edge cases pass validation tests
- [ ] Decimal precision maintained (no float usage)
- [ ] Favorability logic correct for all account types
- [ ] Material variances properly flagged
- [ ] Excel output file generated successfully
- [ ] Audit trail includes: timestamp, source files, thresholds
- [ ] Independent verification passed (@code-reviewer)
- [ ] Human final approval received

---

## Example Invocation

```bash
/variance-analysis budget_2025.xlsx actuals_2025_10.xlsx variance_report_oct2025.xlsx
```

**Expected Flow:**
1. Research findings presented → Human approves
2. Detailed plan presented → Human approves
3. Implementation executes with progress updates → Human reviews phases
4. Verification results presented → Human gives final approval
5. Output delivered with audit trail

---

## Anti-Patterns (DON'T DO THIS)

❌ Skip research and jump to coding
❌ Implement without human-approved plan
❌ Use float for currency calculations
❌ Silently drop unmatched accounts
❌ Skip verification before delivery
❌ Forget audit trail metadata

✅ Follow Research → Plan → Implement → Verify with checkpoints

---

**This command enforces Anthropic best practices: human-in-loop workflows with clear checkpoints and progressive disclosure.**
