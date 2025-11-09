---
description: {{DESCRIPTION}}
---

# {{COMMAND_TITLE}}

**Usage:** `/{{COMMAND_NAME}} {{SOURCE_FILE}} {{TARGET_FILE}} [{{CONFIG_FILE}}]`

**Purpose:** {{ONE_SENTENCE_PURPOSE}} with data quality gates and audit trails.

---

## Phase 1: Load Data

Read source data and validate structure:

1. **Load source file:**
   - File path: {{SOURCE_FILE}} (arg $1)
   - Format: {{SOURCE_FORMAT}}
   - Expected schema: {{EXPECTED_SCHEMA}}

2. **Validate source structure:**
   - {{VALIDATION_CHECK_1}}
   - {{VALIDATION_CHECK_2}}
   - {{VALIDATION_CHECK_3}}

3. **Document data profile:**
   - Total records: {{RECORD_COUNT}}
   - Columns: {{COLUMN_LIST}}
   - Data types: {{DATA_TYPE_SUMMARY}}
   - Null counts: {{NULL_SUMMARY}}
   - Date range: {{DATE_RANGE}}

4. **Load configuration (optional):**
   - Config file: {{CONFIG_FILE}} (arg $3, optional)
   - Transformation rules: {{TRANSFORMATION_RULES}}
   - Quality thresholds: {{QUALITY_THRESHOLDS}}

**Pre-Load Quality Gate:**
- [ ] Source file exists and is readable
- [ ] Schema matches expected structure
- [ ] No critical data quality issues

---

## Phase 2: Transform Data

Apply transformation rules to source data:

**Transformation Steps:**

1. **{{TRANSFORMATION_1_NAME}}:**
   - Rule: {{TRANSFORMATION_1_RULE}}
   - Input: {{TRANSFORMATION_1_INPUT}}
   - Output: {{TRANSFORMATION_1_OUTPUT}}
   - Example: {{TRANSFORMATION_1_EXAMPLE}}

2. **{{TRANSFORMATION_2_NAME}}:**
   - Rule: {{TRANSFORMATION_2_RULE}}
   - Input: {{TRANSFORMATION_2_INPUT}}
   - Output: {{TRANSFORMATION_2_OUTPUT}}
   - Example: {{TRANSFORMATION_2_EXAMPLE}}

3. **{{TRANSFORMATION_3_NAME}}:**
   - Rule: {{TRANSFORMATION_3_RULE}}
   - Input: {{TRANSFORMATION_3_INPUT}}
   - Output: {{TRANSFORMATION_3_OUTPUT}}
   - Example: {{TRANSFORMATION_3_EXAMPLE}}

4. **{{TRANSFORMATION_4_NAME}}:**
   - Rule: {{TRANSFORMATION_4_RULE}}
   - Input: {{TRANSFORMATION_4_INPUT}}
   - Output: {{TRANSFORMATION_4_OUTPUT}}
   - Example: {{TRANSFORMATION_4_EXAMPLE}}

**Edge Case Handling:**
- **{{EDGE_CASE_1}}:** {{EDGE_CASE_1_HANDLING}}
- **{{EDGE_CASE_2}}:** {{EDGE_CASE_2_HANDLING}}
- **{{EDGE_CASE_3}}:** {{EDGE_CASE_3_HANDLING}}
- **NULL values:** {{NULL_HANDLING_STRATEGY}}
- **Duplicates:** {{DUPLICATE_HANDLING_STRATEGY}}

**Transformation Tracking:**
- Records processed: {{PROCESSED_COUNT}}
- Records transformed: {{TRANSFORMED_COUNT}}
- Records skipped: {{SKIPPED_COUNT}}
- Transformation errors: {{ERROR_COUNT}}

---

## Phase 3: Validate Output

Verify transformed data meets quality standards:

**Data Quality Checks:**

1. **{{QUALITY_CHECK_1_NAME}}:**
   - Criteria: {{QUALITY_CHECK_1_CRITERIA}}
   - Threshold: {{QUALITY_CHECK_1_THRESHOLD}}
   - Result: {{QUALITY_CHECK_1_RESULT}}

2. **{{QUALITY_CHECK_2_NAME}}:**
   - Criteria: {{QUALITY_CHECK_2_CRITERIA}}
   - Threshold: {{QUALITY_CHECK_2_THRESHOLD}}
   - Result: {{QUALITY_CHECK_2_RESULT}}

3. **{{QUALITY_CHECK_3_NAME}}:**
   - Criteria: {{QUALITY_CHECK_3_CRITERIA}}
   - Threshold: {{QUALITY_CHECK_3_THRESHOLD}}
   - Result: {{QUALITY_CHECK_3_RESULT}}

4. **{{QUALITY_CHECK_4_NAME}}:**
   - Criteria: {{QUALITY_CHECK_4_CRITERIA}}
   - Threshold: {{QUALITY_CHECK_4_THRESHOLD}}
   - Result: {{QUALITY_CHECK_4_RESULT}}

**Completeness Verification:**
- [ ] All required fields present
- [ ] No unexpected nulls in critical columns
- [ ] Record count matches expected (source → target reconciliation)
- [ ] Data types consistent
- [ ] Business rules satisfied

**Accuracy Validation:**
- [ ] {{ACCURACY_CHECK_1}}
- [ ] {{ACCURACY_CHECK_2}}
- [ ] Spot-check: Sample {{SAMPLE_SIZE}} records manually

**Post-Transform Quality Gate:**
- [ ] All quality checks pass thresholds
- [ ] Completeness verified
- [ ] Accuracy validated

---

## Phase 4: Output

Write transformed data to target file:

1. **Generate output file:**
   - Target path: {{TARGET_FILE}} (arg $2)
   - Format: {{TARGET_FORMAT}}
   - Schema: {{OUTPUT_SCHEMA}}

2. **Include metadata:**
   - Source file: {{SOURCE_FILE}}
   - Transformation timestamp: {{TIMESTAMP}}
   - Transformation rules applied: {{RULES_APPLIED}}
   - Quality checks passed: {{QUALITY_CHECKS_SUMMARY}}

3. **Generate audit trail:**
   ```json
   {
     "timestamp": "{{ISO_8601_TIMESTAMP}}",
     "source_file": "{{SOURCE_FILE}}",
     "target_file": "{{TARGET_FILE}}",
     "config_file": "{{CONFIG_FILE}}",
     "records_source": {{SOURCE_RECORD_COUNT}},
     "records_target": {{TARGET_RECORD_COUNT}},
     "transformations_applied": [
       "{{TRANSFORMATION_1_NAME}}",
       "{{TRANSFORMATION_2_NAME}}",
       "{{TRANSFORMATION_3_NAME}}",
       "{{TRANSFORMATION_4_NAME}}"
     ],
     "quality_checks": [
       {"check": "{{QUALITY_CHECK_1_NAME}}", "status": "{{STATUS_1}}"},
       {"check": "{{QUALITY_CHECK_2_NAME}}", "status": "{{STATUS_2}}"},
       {"check": "{{QUALITY_CHECK_3_NAME}}", "status": "{{STATUS_3}}"},
       {"check": "{{QUALITY_CHECK_4_NAME}}", "status": "{{STATUS_4}}"}
     ],
     "duration_seconds": {{DURATION_SECONDS}}
   }
   ```

4. **Archive audit trail:**
   - Save to: {{AUDIT_TRAIL_LOCATION}}

---

## Success Criteria

Before marking complete:

- [ ] Source file loaded successfully
- [ ] Schema validated
- [ ] All transformations applied
- [ ] Edge cases handled appropriately
- [ ] All quality checks passed
- [ ] Output file generated
- [ ] Metadata included in output
- [ ] Audit trail saved
- [ ] Source → target reconciliation verified

---

## Example Invocation

```bash
/{{COMMAND_NAME}} data/source/raw_data.csv data/output/transformed_data.xlsx config/transformation_rules.json
```

**Expected Flow:**
1. Load → raw_data.csv (1,000 records, validated schema)
2. Transform → Apply 4 transformation rules, handle edge cases
3. Validate → All quality checks pass
4. Output → transformed_data.xlsx (1,000 records, metadata included, audit trail saved)

**Example Output:**
```
Data Transformation Summary

Source: data/source/raw_data.csv (1,000 records)
Target: data/output/transformed_data.xlsx (1,000 records)

Transformations Applied:
1. {{TRANSFORMATION_1_NAME}} (1,000 records)
2. {{TRANSFORMATION_2_NAME}} (1,000 records)
3. {{TRANSFORMATION_3_NAME}} (1,000 records)
4. {{TRANSFORMATION_4_NAME}} (1,000 records)

Quality Checks:
✅ {{QUALITY_CHECK_1_NAME}}: PASS
✅ {{QUALITY_CHECK_2_NAME}}: PASS
✅ {{QUALITY_CHECK_3_NAME}}: PASS
✅ {{QUALITY_CHECK_4_NAME}}: PASS

Audit trail: data/output/audit_trail_20251109_143022.json
```

---

## Anti-Patterns (DON'T DO THIS)

❌ Skip schema validation
❌ Transform without quality gates
❌ Ignore edge cases and nulls
❌ Silently drop records
❌ Forget audit trail
❌ Overwrite source file

✅ Load → Transform → Validate → Output pipeline
✅ Quality gates after load and transform
✅ Explicit edge case handling
✅ Complete audit trail with metadata
✅ Separate source and target files

---

**This command enforces ETL best practices: structured pipeline with quality gates at each phase.**
