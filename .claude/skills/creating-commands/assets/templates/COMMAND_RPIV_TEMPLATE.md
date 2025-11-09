---
description: {{DESCRIPTION}}
---

# {{COMMAND_TITLE}}

**Usage:** `/{{COMMAND_NAME}} {{ARG_1}} {{ARG_2}} [{{ARG_3}}]`

**Purpose:** {{ONE_SENTENCE_PURPOSE}}

---

## Workflow (Human-in-Loop)

### STEP 1: RESEARCH Phase

Investigate {{RESEARCH_SUBJECT}} WITHOUT writing code:

1. **{{RESEARCH_STEP_1_NAME}}:**
   - {{RESEARCH_STEP_1_ACTION_1}}
   - {{RESEARCH_STEP_1_ACTION_2}}
   - {{RESEARCH_STEP_1_ACTION_3}}

2. **{{RESEARCH_STEP_2_NAME}}:**
   - {{RESEARCH_STEP_2_ACTION_1}}
   - {{RESEARCH_STEP_2_ACTION_2}}
   - {{RESEARCH_STEP_2_ACTION_3}}

3. **{{RESEARCH_STEP_3_NAME}}:**
   - {{RESEARCH_STEP_3_ACTION_1}}
   - {{RESEARCH_STEP_3_ACTION_2}}

4. **Generate Research Summary:**
   - {{SUMMARY_COMPONENT_1}}
   - {{SUMMARY_COMPONENT_2}}
   - {{SUMMARY_COMPONENT_3}}
   - {{SUMMARY_COMPONENT_4}}

**CHECKPOINT 1:** Present research findings. Wait for human approval to proceed.

---

### STEP 2: PLAN Phase

Create detailed specification WITHOUT implementing:

1. **{{PLAN_COMPONENT_1_NAME}}:**
   - {{PLAN_COMPONENT_1_QUESTION_1}}
   - {{PLAN_COMPONENT_1_QUESTION_2}}
   - {{PLAN_COMPONENT_1_QUESTION_3}}

2. **{{PLAN_COMPONENT_2_NAME}}:**
   - {{PLAN_COMPONENT_2_DETAIL_1}}
   - {{PLAN_COMPONENT_2_DETAIL_2}}
   - Edge case handling:
     - {{EDGE_CASE_1}} → {{EDGE_CASE_1_HANDLING}}
     - {{EDGE_CASE_2}} → {{EDGE_CASE_2_HANDLING}}
     - {{EDGE_CASE_3}} → {{EDGE_CASE_3_HANDLING}}

3. **{{PLAN_COMPONENT_3_NAME}}:**
   - {{PLAN_COMPONENT_3_RULE_1}}
   - {{PLAN_COMPONENT_3_RULE_2}}
   - {{PLAN_COMPONENT_3_RULE_3}}

4. **{{PLAN_COMPONENT_4_NAME}}:**
   - {{PLAN_COMPONENT_4_CRITERION_1}}

5. **Output Specification:**
   - {{OUTPUT_FORMAT_1}}
   - {{OUTPUT_FORMAT_2}}
   - {{OUTPUT_FORMAT_3}}
   - File location: {{OUTPUT_LOCATION}}

**CHECKPOINT 2:** Present plan. Wait for human approval.

---

### STEP 3: IMPLEMENT Phase

Execute task-by-task with progress tracker:

**Implementation Plan:**

| Task | Status | Notes |
|------|--------|-------|
| {{TASK_1_NAME}} | Pending | {{TASK_1_NOTES}} |
| {{TASK_2_NAME}} | Pending | {{TASK_2_NOTES}} |
| {{TASK_3_NAME}} | Pending | {{TASK_3_NOTES}} |
| {{TASK_4_NAME}} | Pending | {{TASK_4_NOTES}} |
| {{TASK_5_NAME}} | Pending | {{TASK_5_NOTES}} |
| {{TASK_6_NAME}} | Pending | {{TASK_6_NOTES}} |
| {{TASK_7_NAME}} | Pending | {{TASK_7_NOTES}} |
| {{TASK_8_NAME}} | Pending | {{TASK_8_NOTES}} |

**Execute each task:**
- Mark task "In Progress"
- {{IMPLEMENTATION_REQUIREMENT_1}}
- {{IMPLEMENTATION_REQUIREMENT_2}}
- Mark task "Complete"
- Show result summary

**CHECKPOINT 3:** After each major phase ({{PHASE_1}}, {{PHASE_2}}, {{PHASE_3}}), pause for review.

---

### STEP 4: VERIFY Phase

Independent validation before delivery:

1. **{{VERIFICATION_METHOD_1_NAME}}:**
   ```
   {{VERIFICATION_METHOD_1_COMMAND}}
   ```
   Expected checks:
   - {{VERIFICATION_CHECK_1}}
   - {{VERIFICATION_CHECK_2}}
   - {{VERIFICATION_CHECK_3}}

2. **{{VERIFICATION_METHOD_2_NAME}}:**
   ```bash
   {{VERIFICATION_METHOD_2_COMMAND}}
   ```

3. **{{VERIFICATION_METHOD_3_NAME}}:**
   - {{MANUAL_CHECK_1}}
   - {{MANUAL_CHECK_2}}
   - {{MANUAL_CHECK_3}}

4. **Output quality check:**
   - {{OUTPUT_CHECK_1}}
   - {{OUTPUT_CHECK_2}}
   - {{OUTPUT_CHECK_3}}
   - {{OUTPUT_CHECK_4}}

**CHECKPOINT 4:** Present verification results. Wait for final approval.

---

## Success Criteria

Before marking complete:

- [ ] {{SUCCESS_CRITERION_1}}
- [ ] {{SUCCESS_CRITERION_2}}
- [ ] {{SUCCESS_CRITERION_3}}
- [ ] {{SUCCESS_CRITERION_4}}
- [ ] {{SUCCESS_CRITERION_5}}
- [ ] {{SUCCESS_CRITERION_6}}
- [ ] {{SUCCESS_CRITERION_7}}
- [ ] Independent verification passed
- [ ] Human final approval received

---

## Example Invocation

```bash
/{{COMMAND_NAME}} {{EXAMPLE_ARG_1}} {{EXAMPLE_ARG_2}} {{EXAMPLE_ARG_3}}
```

**Expected Flow:**
1. Research findings presented → Human approves
2. Detailed plan presented → Human approves
3. Implementation executes with progress updates → Human reviews phases
4. Verification results presented → Human gives final approval
5. {{EXPECTED_OUTPUT}}

---

## Anti-Patterns (DON'T DO THIS)

❌ Skip research and jump to coding
❌ Implement without human-approved plan
❌ {{ANTI_PATTERN_1}}
❌ {{ANTI_PATTERN_2}}
❌ {{ANTI_PATTERN_3}}
❌ Skip verification before delivery

✅ Follow Research → Plan → Implement → Verify with checkpoints

---

**This command enforces best practices: human-in-loop workflows with clear checkpoints and progressive disclosure.**
