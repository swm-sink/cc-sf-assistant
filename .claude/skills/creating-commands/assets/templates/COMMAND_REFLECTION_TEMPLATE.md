---
description: {{DESCRIPTION}}
---

# {{COMMAND_TITLE}}

**Usage:** `/{{COMMAND_NAME}} {{ARG_1}} [{{ARG_2}}]`

**Purpose:** {{ONE_SENTENCE_PURPOSE}} with iterative self-improvement until quality thresholds met.

---

## Phase 1: DRAFT

Generate initial output without self-imposed constraints:

1. **Create first draft:**
   - {{DRAFT_APPROACH_1}}
   - {{DRAFT_APPROACH_2}}
   - {{DRAFT_APPROACH_3}}

2. **Document approach:**
   - Methodology used: {{METHODOLOGY}}
   - Assumptions made: {{ASSUMPTION_1}}, {{ASSUMPTION_2}}, {{ASSUMPTION_3}}
   - Sources consulted: {{SOURCE_1}}, {{SOURCE_2}}

3. **Deliver draft output:**
   - {{OUTPUT_COMPONENT_1}}
   - {{OUTPUT_COMPONENT_2}}
   - {{OUTPUT_COMPONENT_3}}

---

## Phase 2: REFLECT

Evaluate own output against quality dimensions:

**Self-Evaluation Criteria:**

1. **{{QUALITY_DIMENSION_1}}:** {{DIMENSION_1_DESCRIPTION}}
   - Current assessment: [Rate 1-10]
   - Evidence: {{EVIDENCE_PROMPT_1}}

2. **{{QUALITY_DIMENSION_2}}:** {{DIMENSION_2_DESCRIPTION}}
   - Current assessment: [Rate 1-10]
   - Evidence: {{EVIDENCE_PROMPT_2}}

3. **{{QUALITY_DIMENSION_3}}:** {{DIMENSION_3_DESCRIPTION}}
   - Current assessment: [Rate 1-10]
   - Evidence: {{EVIDENCE_PROMPT_3}}

4. **{{QUALITY_DIMENSION_4}}:** {{DIMENSION_4_DESCRIPTION}}
   - Current assessment: [Rate 1-10]
   - Evidence: {{EVIDENCE_PROMPT_4}}

5. **{{QUALITY_DIMENSION_5}}:** {{DIMENSION_5_DESCRIPTION}}
   - Current assessment: [Rate 1-10]
   - Evidence: {{EVIDENCE_PROMPT_5}}

**Reflection Questions:**
- Are all facts correct? (Verify sources)
- Did I miss anything? (Check requirements against output)
- Is this understandable? (Read from user perspective)
- What could go wrong? (Challenge every assumption)
- Would this pass peer review?

---

## Phase 3: IDENTIFY IMPROVEMENTS

List specific, actionable changes (not vague "make it better"):

**Improvement Plan:**

1. **{{IMPROVEMENT_1_TITLE}}:**
   - Issue: {{ISSUE_DESCRIPTION_1}}
   - Fix: {{FIX_DESCRIPTION_1}}
   - Rationale: {{RATIONALE_1}}
   - Expected impact: {{DIMENSION_X}} improves from Y/10 to Z/10

2. **{{IMPROVEMENT_2_TITLE}}:**
   - Issue: {{ISSUE_DESCRIPTION_2}}
   - Fix: {{FIX_DESCRIPTION_2}}
   - Rationale: {{RATIONALE_2}}
   - Expected impact: {{DIMENSION_X}} improves from Y/10 to Z/10

3. **{{IMPROVEMENT_3_TITLE}}:**
   - Issue: {{ISSUE_DESCRIPTION_3}}
   - Fix: {{FIX_DESCRIPTION_3}}
   - Rationale: {{RATIONALE_3}}
   - Expected impact: {{DIMENSION_X}} improves from Y/10 to Z/10

**Prioritization:**
- Critical improvements (quality <6/10): {{CRITICAL_IMPROVEMENTS}}
- High-value improvements (quality 6-7/10): {{HIGH_VALUE_IMPROVEMENTS}}
- Nice-to-have improvements (quality 8-9/10): {{NICE_TO_HAVE_IMPROVEMENTS}}

---

## Phase 4: REFINE

Implement identified improvements:

**Iteration {{ITERATION_NUMBER}} Refinements:**

1. **{{IMPROVEMENT_1_TITLE}}:**
   - **Before:** {{BEFORE_STATE_1}}
   - **After:** {{AFTER_STATE_1}}
   - **Verification:** {{VERIFICATION_METHOD_1}}

2. **{{IMPROVEMENT_2_TITLE}}:**
   - **Before:** {{BEFORE_STATE_2}}
   - **After:** {{AFTER_STATE_2}}
   - **Verification:** {{VERIFICATION_METHOD_2}}

3. **{{IMPROVEMENT_3_TITLE}}:**
   - **Before:** {{BEFORE_STATE_3}}
   - **After:** {{AFTER_STATE_3}}
   - **Verification:** {{VERIFICATION_METHOD_3}}

**Progress Summary:**
- Improvements implemented: {{IMPROVEMENTS_COUNT}}
- Quality dimensions improved: {{DIMENSIONS_IMPROVED}}
- Overall quality score: {{OVERALL_SCORE}}/10

---

## Phase 5: QUALITY GATE

Determine whether to continue refining or deliver:

**Stopping Criteria:**

**STOP and deliver if ANY of:**
- ✅ All quality dimensions ≥ {{QUALITY_THRESHOLD}}/10
- ✅ Max iterations reached ({{MAX_ITERATIONS}})
- ✅ No further improvements identified

**CONTINUE refining if:**
- ❌ Any quality dimension < {{QUALITY_THRESHOLD}}/10
- ❌ Iterations remaining (current: {{CURRENT_ITERATION}}/{{MAX_ITERATIONS}})
- ❌ Improvements still identified

**Current Status:**
- Quality scores: {{DIMENSION_1}}={{SCORE_1}}/10, {{DIMENSION_2}}={{SCORE_2}}/10, {{DIMENSION_3}}={{SCORE_3}}/10, {{DIMENSION_4}}={{SCORE_4}}/10, {{DIMENSION_5}}={{SCORE_5}}/10
- Iterations used: {{CURRENT_ITERATION}}/{{MAX_ITERATIONS}}
- Decision: {{STOP_OR_CONTINUE}}

**If CONTINUE:** Return to Phase 2 (REFLECT) with refined output.

---

## Phase 6: FINAL OUTPUT

Deliver refined version with quality assessment:

**Final Output:**
{{FINAL_OUTPUT_CONTENT}}

**Quality Assessment:**
| Dimension | Score | Evidence |
|-----------|-------|----------|
| {{QUALITY_DIMENSION_1}} | {{FINAL_SCORE_1}}/10 | {{FINAL_EVIDENCE_1}} |
| {{QUALITY_DIMENSION_2}} | {{FINAL_SCORE_2}}/10 | {{FINAL_EVIDENCE_2}} |
| {{QUALITY_DIMENSION_3}} | {{FINAL_SCORE_3}}/10 | {{FINAL_EVIDENCE_3}} |
| {{QUALITY_DIMENSION_4}} | {{FINAL_SCORE_4}}/10 | {{FINAL_EVIDENCE_4}} |
| {{QUALITY_DIMENSION_5}} | {{FINAL_SCORE_5}}/10 | {{FINAL_EVIDENCE_5}} |
| **Overall** | **{{OVERALL_FINAL_SCORE}}/10** | Met {{QUALITY_THRESHOLD}}/10 threshold |

**Iteration Summary:**
- Total iterations: {{TOTAL_ITERATIONS}}
- Improvements made: {{TOTAL_IMPROVEMENTS}}
- Stopping reason: {{STOPPING_REASON}}

---

## Success Criteria

Before marking complete:

- [ ] Initial draft created
- [ ] Self-evaluation completed for all {{NUM_DIMENSIONS}} quality dimensions
- [ ] All dimensions rated 1-10 with evidence
- [ ] Improvements identified and prioritized
- [ ] Refinements implemented with before/after documentation
- [ ] Quality gate evaluated
- [ ] Either threshold met ({{QUALITY_THRESHOLD}}/10) OR max iterations reached ({{MAX_ITERATIONS}})
- [ ] Final output delivered with quality assessment
- [ ] Iteration summary documented

---

## Example Invocation

```bash
/{{COMMAND_NAME}} {{EXAMPLE_ARG_1}} {{EXAMPLE_ARG_2}}
```

**Expected Flow:**
1. Draft → {{EXAMPLE_DRAFT_DESCRIPTION}}
2. Reflect → Identify {{EXAMPLE_DIMENSION}} needs improvement (5/10)
3. Identify → Specific fix: {{EXAMPLE_FIX}}
4. Refine → Implement fix, {{EXAMPLE_DIMENSION}} now 8/10
5. Quality Gate → All dimensions ≥8/10, deliver final output

**Example Iteration:**
- Iteration 1: Accuracy 5/10 → Fixed source citations → 9/10
- Iteration 2: Clarity 6/10 → Simplified language → 8/10
- Iteration 3: All ≥8/10 → STOP and deliver

---

## Anti-Patterns (DON'T DO THIS)

❌ Skip self-evaluation (blind delivery)
❌ Vague improvements ("make it better")
❌ Infinite loops (ignore max iterations)
❌ Cherry-pick quality dimensions (evaluate ALL)
❌ Deliver without quality assessment

✅ Honest self-critique (be harsh, not generous)
✅ Specific, actionable improvements
✅ Respect quality gates (threshold OR max iterations)
✅ Document all before/after changes

---

**This command enforces Anthropic Evaluator-Optimizer and Google/DeepMind reflection patterns for iterative quality improvement.**
