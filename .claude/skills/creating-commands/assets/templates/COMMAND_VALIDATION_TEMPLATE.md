---
description: {{DESCRIPTION}}
model: sonnet
---

# {{COMMAND_TITLE}}

**Usage:** `/{{COMMAND_NAME}}`

{{VALIDATION_PURPOSE_DESCRIPTION}}

## Purpose

Ensure that:
1. {{VALIDATION_GOAL_1}}
2. {{VALIDATION_GOAL_2}}
3. {{VALIDATION_GOAL_3}}
4. {{VALIDATION_GOAL_4}}
5. {{VALIDATION_GOAL_5}}

---

## Validation Checks

### Check 1: {{CHECK_1_NAME}}

**What to verify:** {{CHECK_1_DESCRIPTION}}

**Expected result:** {{CHECK_1_EXPECTED}}

**Action steps:**
1. {{CHECK_1_STEP_1}}
2. {{CHECK_1_STEP_2}}
3. {{CHECK_1_STEP_3}}

**Pass criteria:** {{CHECK_1_PASS_CRITERIA}}

---

### Check 2: {{CHECK_2_NAME}}

**What to verify:** {{CHECK_2_DESCRIPTION}}

**Expected result:** {{CHECK_2_EXPECTED}}

**Action steps:**
1. {{CHECK_2_STEP_1}}
2. {{CHECK_2_STEP_2}}
3. {{CHECK_2_STEP_3}}

**Pass criteria:** {{CHECK_2_PASS_CRITERIA}}

---

### Check 3: {{CHECK_3_NAME}}

**What to verify:** {{CHECK_3_DESCRIPTION}}

**Expected result:** {{CHECK_3_EXPECTED}}

**Action steps:**
1. {{CHECK_3_STEP_1}}
2. {{CHECK_3_STEP_2}}
3. {{CHECK_3_STEP_3}}

**Pass criteria:** {{CHECK_3_PASS_CRITERIA}}

---

### Check 4: {{CHECK_4_NAME}}

**What to verify:** {{CHECK_4_DESCRIPTION}}

**Expected result:** {{CHECK_4_EXPECTED}}

**Action steps:**
1. {{CHECK_4_STEP_1}}
2. {{CHECK_4_STEP_2}}
3. {{CHECK_4_STEP_3}}

**Pass criteria:** {{CHECK_4_PASS_CRITERIA}}

---

### Check 5: {{CHECK_5_NAME}}

**What to verify:** {{CHECK_5_DESCRIPTION}}

**Expected result:** {{CHECK_5_EXPECTED}}

**Action steps:**
1. {{CHECK_5_STEP_1}}
2. {{CHECK_5_STEP_2}}
3. {{CHECK_5_STEP_3}}

**Pass criteria:** {{CHECK_5_PASS_CRITERIA}}

---

### Check 6: {{CHECK_6_NAME}}

**What to verify:** {{CHECK_6_DESCRIPTION}}

**Expected result:** {{CHECK_6_EXPECTED}}

**Action steps:**
1. {{CHECK_6_STEP_1}}
2. {{CHECK_6_STEP_2}}
3. {{CHECK_6_STEP_3}}

**Pass criteria:** {{CHECK_6_PASS_CRITERIA}}

---

### Check 7: {{CHECK_7_NAME}}

**What to verify:** {{CHECK_7_DESCRIPTION}}

**Expected result:** {{CHECK_7_EXPECTED}}

**Action steps:**
1. {{CHECK_7_STEP_1}}
2. {{CHECK_7_STEP_2}}
3. {{CHECK_7_STEP_3}}

**Pass criteria:** {{CHECK_7_PASS_CRITERIA}}

---

### Check 8: {{CHECK_8_NAME}}

**What to verify:** {{CHECK_8_DESCRIPTION}}

**Expected result:** {{CHECK_8_EXPECTED}}

**Action steps:**
1. {{CHECK_8_STEP_1}}
2. {{CHECK_8_STEP_2}}
3. {{CHECK_8_STEP_3}}

**Pass criteria:** {{CHECK_8_PASS_CRITERIA}}

---

### Check 9: {{CHECK_9_NAME}}

**What to verify:** {{CHECK_9_DESCRIPTION}}

**Expected result:** {{CHECK_9_EXPECTED}}

**Action steps:**
1. {{CHECK_9_STEP_1}}
2. {{CHECK_9_STEP_2}}
3. {{CHECK_9_STEP_3}}

**Pass criteria:** {{CHECK_9_PASS_CRITERIA}}

---

### Check 10: {{CHECK_10_NAME}}

**What to verify:** {{CHECK_10_DESCRIPTION}}

**Expected result:** {{CHECK_10_EXPECTED}}

**Action steps:**
1. {{CHECK_10_STEP_1}}
2. {{CHECK_10_STEP_2}}
3. {{CHECK_10_STEP_3}}

**Pass criteria:** {{CHECK_10_PASS_CRITERIA}}

---

## Validation Report Format

Present results in this structure:

**{{COMMAND_TITLE}} - Validation Report**

**Summary:**
- Total checks: 10
- Passed: {{PASSED_COUNT}}
- Warnings: {{WARNING_COUNT}}
- Errors: {{ERROR_COUNT}}

**Results:**

✅ **PASS:** {{CHECK_NAME}} - {{PASS_DESCRIPTION}}
⚠️ **WARNING:** {{CHECK_NAME}} - {{WARNING_DESCRIPTION}} (acceptable)
❌ **ERROR:** {{CHECK_NAME}} - {{ERROR_DESCRIPTION}} (critical)

**Status:** {{OVERALL_STATUS}}

---

## Usage Example

```bash
/{{COMMAND_NAME}}
```

**Expected output:**

```
{{COMMAND_TITLE}} - Validation Report

Summary:
- Total checks: 10
- Passed: 8
- Warnings: 2
- Errors: 0

Results:

✅ PASS: {{EXAMPLE_CHECK_1}} - {{EXAMPLE_RESULT_1}}
✅ PASS: {{EXAMPLE_CHECK_2}} - {{EXAMPLE_RESULT_2}}
⚠️ WARNING: {{EXAMPLE_CHECK_3}} - {{EXAMPLE_RESULT_3}}

Status: VALIDATION SUCCESSFUL (warnings acceptable)
```

---

## Anti-Patterns (DON'T DO THIS)

❌ Skip checks (must run all 10)
❌ Modify system during validation (read-only operations)
❌ Ignore warnings without documenting
❌ Report ERROR as WARNING
❌ Proceed with errors unresolved

✅ Run all validation checks systematically
✅ Clear distinction: ✅ PASS, ⚠️ WARNING, ❌ ERROR
✅ Read-only verification (no modifications)

---

**This command provides systematic validation checks with clear pass/warning/error reporting.**
