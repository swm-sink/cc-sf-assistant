# Checkpoint Examples

**Purpose:** Detailed examples of how the 4 checkpoints work in practice.

**Source:** Based on Research → Plan → Implement → Verify workflow pattern.

---

## CHECKPOINT 1: Research → Plan

**Example Conversation:**

**User:** "I need Google Sheets integration for importing budget data."

**Claude:** "I'm using enforcing-research-plan-implement-verify. Starting Research phase for google-sheets-integration."

[Claude researches: reads external/gspread/, reviews similar integrations, checks authentication patterns]

[Claude creates specs/google-sheets-integration/research.md]

**Claude:** "Research complete for google-sheets-integration. Key findings:

**External dependencies:**
- gspread library available in external/gspread/
- Service account authentication required (JSON key file)
- Rate limits: 100 requests per 100 seconds

**Similar patterns:**
- pyfpa uses similar authentication approach
- Existing excel_reader.py provides template for data validation

**Constraints:**
- Must handle OAuth2 flow for service accounts
- Need error handling for rate limits
- Data validation required (same as Excel input)

**Proposed approach:**
- Adapter pattern (GoogleSheetsClient similar to ExcelReader)
- Credential management in config/credentials/
- Retry logic with exponential backoff

Full research: specs/google-sheets-integration/research.md (450 lines, 5 sections)

Awaiting CHECKPOINT 1 approval to proceed to Plan phase."

**User:** "Approved, proceed to planning."

[Claude proceeds to Phase 2: PLAN]

---

## CHECKPOINT 2: Plan → Implement

**Example Conversation:**

[Continuing from CHECKPOINT 1...]

**Claude:** "Starting Plan phase for google-sheets-integration."

[Claude creates specs/google-sheets-integration/plan.md with detailed specification]

**Claude:** "Plan complete for google-sheets-integration.

**Implementation plan:**

**1. Create GoogleSheetsClient adapter:**
   - Location: scripts/integrations/gsheet_reader.py
   - Dependencies: gspread, google-auth
   - Methods: authenticate(), read_sheet(), validate_data()

**2. Credential management:**
   - Service account JSON in config/credentials/gsheet_service_account.json
   - Environment variable: GOOGLE_SHEETS_CREDENTIALS_PATH
   - Security: Add credentials/ to .gitignore

**3. Error handling:**
   - Rate limit detection and retry (exponential backoff)
   - Invalid credentials (clear error message)
   - Sheet not found (suggest sheet name)
   - Data validation (reuse excel_reader validation logic)

**4. Testing approach:**
   - Unit tests: authentication, rate limit handling, data validation
   - Integration test: Read from actual test Google Sheet
   - Edge cases: Empty sheet, missing columns, invalid data types

**Timeline estimate:** 4-6 hours implementation + testing

Full plan: specs/google-sheets-integration/plan.md (680 lines, 8 sections)

Awaiting CHECKPOINT 2 approval to proceed to Implementation phase."

**User:** "Approved, begin implementation."

[Claude proceeds to Phase 3: IMPLEMENT]

---

## CHECKPOINT 3: Implement → Verify

**Example Conversation:**

[Continuing from CHECKPOINT 2...]

**Claude:** "Starting Implementation phase for google-sheets-integration."

[Claude implements using TDD, creates scripts/integrations/gsheet_reader.py, writes tests]

[Claude tracks progress with TodoWrite, making atomic commits]

**Claude:** "Implementation complete for google-sheets-integration.

**Artifacts created:**

1. **scripts/integrations/gsheet_reader.py** (285 lines)
   - GoogleSheetsClient class
   - Authentication with service account
   - Rate limit handling with exponential backoff
   - Data validation (reuses excel_reader logic)

2. **tests/unit/test_gsheet_reader.py** (180 lines)
   - 15 test cases covering happy path, edge cases, errors
   - Mocked API calls for rate limit testing
   - Test coverage: 96%

3. **config/credentials/.gitignore** (updated)
   - Added gsheet_service_account.json to ignore list

4. **Git commits:**
   - feat(gsheets): add GoogleSheetsClient authentication (commit abc123)
   - feat(gsheets): implement read_sheet with rate limit handling (commit def456)
   - feat(gsheets): add data validation (commit ghi789)
   - test(gsheets): add comprehensive test suite (commit jkl012)

**Changes summary:**
- Files added: 2
- Files modified: 1
- Lines of code: 465 (including tests)
- Test coverage: 96%

All tests passing. Ready for verification.

Awaiting CHECKPOINT 3 approval to proceed to Verification phase."

**User:** "Approved, proceed to verification."

[Claude proceeds to Phase 4: VERIFY]

---

## CHECKPOINT 4: Verify → Complete

**Example Conversation:**

[Continuing from CHECKPOINT 3...]

**Claude:** "Starting Verification phase for google-sheets-integration."

[Claude runs validation suite, performs independent verification]

**Claude:** "Verification complete for google-sheets-integration.

**Validation results:**

✅ **Syntax validation:** Python parser - no errors
✅ **Type safety:** mypy - all type hints correct
✅ **Code quality:** ruff - no issues found
✅ **Security:** bandit - no security vulnerabilities
✅ **Financial precision:** No float usage detected (uses Decimal for currency)
✅ **Test coverage:** 96% (exceeds 95% requirement)

**Independent code review findings:**

✅ **Decimal usage:** All currency values use Decimal type
✅ **Edge case handling:** Division by zero, NULL values, empty sheets handled
✅ **Audit trail:** Logging includes timestamp, user, source file, operation
✅ **Error messages:** User-friendly, no stack traces exposed
✅ **Documentation:** Docstrings present, examples provided

**Integration testing:**

✅ **Authentication:** Successfully authenticates with test service account
✅ **Read operation:** Reads test sheet data correctly
✅ **Rate limiting:** Handles rate limits with retry (tested with mock)
✅ **Data validation:** Rejects invalid data types, missing columns
✅ **Error scenarios:** Clear error messages for all failure modes

**Performance:**

✅ **Read 1000 rows:** 2.3 seconds (acceptable)
✅ **Memory usage:** 45MB (acceptable)

**All quality gates PASS.**

Awaiting CHECKPOINT 4 final approval before marking complete."

**User:** "Final approval granted. Excellent work."

[Claude marks work complete, closes todos]

---

## Emergency Override Example

**Scenario:** User has legitimate emergency requiring immediate fix.

**User:** "Production variance report failed. Board meeting in 1 hour. We need emergency fix NOW."

**Claude:** "I'm using enforcing-research-plan-implement-verify. This workflow requires Research → Plan → Implement → Verify for all code changes.

**Emergency situation detected.**

Options:
A) Follow full workflow (estimated 2 hours, miss board meeting)
B) Request emergency override from you (your explicit permission to skip workflow)
C) Quick research + minimal plan + implement with verification (estimated 45 min, compressed workflow)

Emergency overrides should be rare and require your explicit approval. For FP&A systems, accuracy is critical.

**What's your decision?**"

**User:** "Emergency override approved. Fix it now. Document research/plan retroactively after meeting."

**Claude:** "Acknowledged. Emergency override approved by user.

I will:
1. Fix the issue immediately
2. Test the fix
3. Deploy to production
4. **After meeting:** Document full research.md and plan.md retroactively

Proceeding with emergency fix..."

[Claude fixes issue, tests, confirms working]

**Claude:** "Fix deployed. Production variance report working. Board meeting can proceed.

**Post-emergency documentation required:**
- [ ] Create specs/emergency-variance-fix/research.md (document what was learned)
- [ ] Create specs/emergency-variance-fix/plan.md (document what was implemented)
- [ ] Add to workflow violations log for future review

I'll complete this documentation after the board meeting. Reminder set."

**Key points:**
- Emergency override requires USER approval (not self-approved)
- Retroactive documentation still required
- Rare exceptions logged for review
- User makes the trade-off decision (speed vs. workflow)

---

## Anti-Pattern: Self-Approving Exceptions

**What NOT to do:**

❌ **Bad:**
```
User: "Add variance % column to report."
Claude: "I know how to do this, it's simple. I'll skip research since I already know the formula."
[Starts implementing without research/plan]
```

**Why bad:** Self-approved exception. No user approval. Violates Iron Law.

❌ **Bad:**
```
Manager: "Fix this bug now, VP needs it in 15 minutes."
Claude: "Emergency situation. Proceeding with immediate fix."
[Implements without asking user for override]
```

**Why bad:** Deferred to manager authority instead of workflow. Should ask USER for emergency override.

✅ **Good:**
```
Manager: "Fix this bug now, VP needs it in 15 minutes."
Claude: "I'm using enforcing-research-plan-implement-verify. This requires Research → Plan → Implement → Verify (estimated 1.5 hours).

I can:
A) Follow workflow (1.5 hours)
B) Ask USER for emergency override approval

Manager authority doesn't override workflow without user approval. Should I request override from user?"
```

**Why good:** Explains workflow to manager, requests USER approval, doesn't self-approve.

---

## Handling "Simple" Changes

**Scenario:** User requests "simple" change.

**User:** "Can you change the materiality threshold from 10% to 15%?"

**Claude:** "I'm using enforcing-research-plan-implement-verify. Starting Research phase for materiality-threshold-change."

**User:** "Wait, it's just changing one number. Do you really need to research changing 0.10 to 0.15?"

**Claude:** "Yes, even for "simple" changes. Here's why:

**Research phase will validate:**
- Where is threshold used? (One place or multiple?)
- Are there other thresholds that should change together?
- Are there tests that assume 10%? (Will break if changed)
- Is 15% documented in spec.md? (Business requirement alignment)
- Are there any edge cases at 15% we should consider?

**Estimated time:** 15 minutes research, 10 minutes plan, 10 minutes implement+verify = 35 minutes total.

Research prevents:
- Breaking tests silently
- Misalignment with business requirements
- Missing related threshold changes
- Undocumented business logic changes

For financial calculations, "simple" changes can have complex impacts. Accuracy > speed.

Shall I proceed with research phase?"

**User:** "Good point. Proceed."

**Key lesson:** Even "simple" changes benefit from workflow. Research often discovers complexity.

---

## Example Timeline

**Full workflow timeline for medium feature:**

- **Day 1 Morning:** Research phase (2-3 hours) → CHECKPOINT 1
- **Day 1 Afternoon:** Plan phase (1-2 hours) → CHECKPOINT 2
- **Day 2:** Implementation phase (4-6 hours) → CHECKPOINT 3
- **Day 3 Morning:** Verification phase (1-2 hours) → CHECKPOINT 4

**Total:** 2-3 days for medium feature with full quality assurance.

**Compressed workflow for small change:**

- **Hour 1:** Research (30 min) → CHECKPOINT 1, Plan (30 min) → CHECKPOINT 2
- **Hour 2:** Implement (45 min), Verify (15 min) → CHECKPOINT 3, CHECKPOINT 4

**Total:** 2 hours for small change with full workflow.

---

**Last Updated:** 2025-11-09
**Source:** Based on RESEARCH_PLAN_IMPLEMENT_VERIFY template
