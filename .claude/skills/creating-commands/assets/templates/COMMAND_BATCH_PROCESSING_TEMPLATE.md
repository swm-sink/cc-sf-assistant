---
description: {{DESCRIPTION}}
---

# {{COMMAND_TITLE}}

**Usage:** `/{{COMMAND_NAME}} {{INPUT_DIR}} {{OUTPUT_DIR}} [{{PATTERN}}]`

**Purpose:** {{ONE_SENTENCE_PURPOSE}} with graceful error handling and progress tracking.

---

## Phase 1: Discovery

Scan input directory for files matching pattern:

1. **Locate input files:**
   - Directory: {{INPUT_DIR}} (arg $1)
   - Pattern: {{PATTERN}} (arg $3, default: `{{DEFAULT_PATTERN}}`)
   - Search command: `find {{INPUT_DIR}} -name "{{PATTERN}}"`

2. **Count and validate:**
   - Total files found: {{FILE_COUNT}}
   - Estimated processing time: {{ESTIMATE_FORMULA}}
   - Storage check: Output directory has sufficient space

3. **Present file list for approval:**

   | # | Filename | Size | Last Modified |
   |---|----------|------|---------------|
   | 1 | {{FILE_1}} | {{SIZE_1}} | {{DATE_1}} |
   | 2 | {{FILE_2}} | {{SIZE_2}} | {{DATE_2}} |
   | 3 | {{FILE_3}} | {{SIZE_3}} | {{DATE_3}} |
   | ... | ... | ... | ... |

**CHECKPOINT 1:** Approve file list before processing.

---

## Phase 2: Processing Loop

For each file, execute transformation with error isolation:

**Progress Tracking:**

| File | Status | Result | Error | Duration |
|------|--------|--------|-------|----------|
| {{FILE_1}} | Complete | ✅ | - | {{TIME_1}}s |
| {{FILE_2}} | Complete | ✅ | - | {{TIME_2}}s |
| {{FILE_3}} | In Progress | - | - | - |
| {{FILE_4}} | Pending | - | - | - |
| {{FILE_5}} | Failed | ❌ | {{ERROR_MESSAGE}} | {{TIME_5}}s |
| {{FILE_6}} | Pending | - | - | - |

**Processing Steps (Per File):**

1. **Load and validate:**
   - Read file: {{FILE_PATH}}
   - {{VALIDATION_CHECK_1}}
   - {{VALIDATION_CHECK_2}}
   - If validation fails: Log error, continue to next file

2. **Apply transformation:**
   - {{TRANSFORMATION_STEP_1}}
   - {{TRANSFORMATION_STEP_2}}
   - {{TRANSFORMATION_STEP_3}}

3. **Handle errors gracefully:**
   - Try-catch wrapper around transformation
   - On error:
     - Log to `{{ERROR_LOG_FILE}}`
     - Mark file as "Failed" in progress table
     - Continue processing (don't stop batch)
   - On success:
     - Mark file as "Complete"
     - Update progress

4. **Save output:**
   - Output location: `{{OUTPUT_DIR}}/{{OUTPUT_FILENAME_PATTERN}}`
   - Include metadata: source file, timestamp, transformation applied

**Error Isolation:**
- Per-file errors don't stop batch processing
- Failed files logged for manual review
- Successful files saved immediately (no rollback)

---

## Phase 3: Summary Report

After all files processed:

**Batch Processing Summary**

**Overall Statistics:**
- Files processed: {{SUCCESSFUL_COUNT}}/{{TOTAL_COUNT}}
- Successes: {{SUCCESSFUL_COUNT}}
- Failures: {{FAILED_COUNT}}
- Total duration: {{TOTAL_DURATION}}
- Average time per file: {{AVG_TIME}}

**Successful Files:**
1. {{SUCCESS_FILE_1}} → {{OUTPUT_FILE_1}}
2. {{SUCCESS_FILE_2}} → {{OUTPUT_FILE_2}}
3. {{SUCCESS_FILE_3}} → {{OUTPUT_FILE_3}}
...

**Failed Files:**
1. {{FAILED_FILE_1}} - Error: {{ERROR_1}}
2. {{FAILED_FILE_2}} - Error: {{ERROR_2}}

**Output Location:**
- Directory: {{OUTPUT_DIR}}
- Error log: {{ERROR_LOG_FILE}}

**Next Steps:**
{{NEXT_STEPS_DESCRIPTION}}

---

## Error Handling

**Error Categories:**

1. **Validation Errors:**
   - Invalid file format
   - Missing required fields
   - Data type mismatches
   - Action: Log and skip file

2. **Transformation Errors:**
   - Calculation failures
   - Business logic exceptions
   - Action: Log and skip file

3. **I/O Errors:**
   - Permission denied
   - Disk full
   - File corruption
   - Action: Log and retry once, then skip

**Error Log Format:**
```json
{
  "timestamp": "{{ISO_8601_TIMESTAMP}}",
  "file": "{{FILE_PATH}}",
  "error_type": "{{ERROR_TYPE}}",
  "error_message": "{{ERROR_MESSAGE}}",
  "stack_trace": "{{STACK_TRACE}}"
}
```

**Recovery Options:**
- Retry failed files: `/{{COMMAND_NAME}} {{OUTPUT_DIR}}/failed_files.txt {{OUTPUT_DIR}}`
- Manual review: Inspect `{{ERROR_LOG_FILE}}`

---

## Success Criteria

Before marking complete:

- [ ] All files in input directory scanned
- [ ] File list approved by user
- [ ] All files processed (success or logged failure)
- [ ] Progress table updated throughout
- [ ] Output files saved to {{OUTPUT_DIR}}
- [ ] Error log generated (if any failures)
- [ ] Summary report presented
- [ ] {{SUCCESS_CRITERION_1}}
- [ ] {{SUCCESS_CRITERION_2}}

---

## Example Invocation

```bash
/{{COMMAND_NAME}} data/input/ data/output/ "*.xlsx"
```

**Expected Flow:**
1. Discovery → Found 50 files matching `*.xlsx`
2. User approves file list
3. Processing → Progress: 50/50 (45 successful, 5 failed)
4. Summary report → 45 outputs in `data/output/`, errors in `error_log.json`

**Example Output:**
```
Batch Processing Summary

Overall Statistics:
- Files processed: 45/50
- Successes: 45
- Failures: 5
- Total duration: 3m 42s

Failed Files:
1. budget_2024_Q4.xlsx - Error: Missing "Account" column
2. actuals_2025_01_corrupted.xlsx - Error: File read error

Output Location: data/output/
Error log: data/output/error_log.json
```

---

## Anti-Patterns (DON'T DO THIS)

❌ Stop batch on first error
❌ Process all files before showing progress
❌ Skip error logging
❌ Silently drop failed files
❌ Overwrite outputs without backup

✅ Continue batch despite per-file errors
✅ Update progress table in real-time
✅ Log all errors with context
✅ Clear success/failure reporting
✅ Graceful degradation (partial success acceptable)

---

**This command enforces batch processing best practices: error isolation, progress tracking, and graceful degradation.**
