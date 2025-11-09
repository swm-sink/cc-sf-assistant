# Full-Access Implementer (Reviewer) Agent Guide

**Purpose:** Comprehensive guide for creating reviewer/auditor agents (read-only tool tier, 3-5% of production agents).

**Based on:** 4-6 validated agents from awesome-claude-code-subagents + project code-reviewer.md

---

## Overview

### What is a Reviewer Agent?

A reviewer agent analyzes, verifies, and provides structured feedback on code, configurations, and implementations WITHOUT making any modifications. It delivers comprehensive review findings with actionable recommendations.

**Key Characteristics:**
- **Verification-focused:** Analysis and feedback, not implementation
- **Read-only tool access:** Read, Grep, Glob ONLY (NO write/edit/bash/web)
- **Checklist-driven:** 8 verification checks for comprehensive coverage
- **Decision-making:** APPROVE / APPROVE_WITH_CONDITIONS / REJECT
- **Structured findings:** CRITICAL / WARNING / SUGGESTION severity levels

### Tool Tier: Read-Only

Reviewers have strictly read-only access:

```yaml
tools:
  - Read      # Read files and documentation
  - Grep      # Search content across codebase
  - Glob      # Find files by pattern
```

**NO write access:**
- Cannot modify files (Write, Edit tools not available)
- Cannot execute code (Bash tool not available)
- Cannot fetch web content (WebFetch, WebSearch not available)

**Why read-only?**
- **Security:** Reviewers can't accidentally modify code under review
- **Clear responsibility:** Review finds issues, implementation fixes them
- **Separation of concerns:** Analysis phase separate from modification phase
- **Audit integrity:** Read-only ensures unbiased review

---

## Review Scope Definition

### Verification Focus Areas

Each reviewer should have **8-15 review areas**, each with **8-12 verification capabilities**.

**Example Structure (code-reviewer):**

```markdown
### Code Quality

**Review capabilities:**
- Function length and complexity analysis
- Code duplication detection
- Naming convention consistency check
- Comment quality and completeness review
- Error handling pattern verification
- Code smell identification (long parameter lists, etc.)
- Adherence to project style guide (PEP 8, ESLint)
- Maintainability assessment (clear logic, simple structure)

### Security Vulnerabilities

**Review capabilities:**
- SQL injection vulnerability scanning
- Cross-site scripting (XSS) pattern detection
- Hardcoded credentials or secrets identification
- Insecure authentication/authorization patterns
- Input validation gap detection
- Sensitive data exposure risks
- Dependency vulnerability checking (known CVEs)
- Security best practice compliance (OWASP Top 10)

[... 6-13 more review areas ...]
```

**Review Area Categories:**
- **Code quality:** Structure, readability, maintainability
- **Security:** Vulnerabilities, best practices, compliance
- **Performance:** Efficiency, scalability, optimization opportunities
- **Testing:** Coverage, quality, edge cases
- **Documentation:** Completeness, accuracy, clarity
- **Architecture:** Design patterns, separation of concerns
- **Error handling:** Edge cases, failure modes, recovery
- **Compliance:** Regulatory requirements, standards adherence

---

## Verification Checklist Design

### 8-Item Comprehensive Checklist

Every reviewer should have an 8-item verification checklist.

**Example Checklist (code-reviewer):**

```markdown
- [ ] Code Quality - Meets project standards (style, structure, clarity)
- [ ] Security - No critical vulnerabilities (injection, XSS, hardcoded secrets)
- [ ] Error Handling - Comprehensive coverage (edge cases, failure modes)
- [ ] Testing - Adequate test coverage (unit tests, edge cases)
- [ ] Documentation - Complete and accurate (README, docstrings, comments)
- [ ] Performance - No obvious inefficiencies (N+1 queries, memory leaks)
- [ ] Best Practices - Follows language/framework conventions
- [ ] Maintainability - Clear logic, appropriate abstractions
```

**Example Checklist (security-auditor):**

```markdown
- [ ] Authentication - Secure credential handling (no plaintext passwords)
- [ ] Authorization - Proper access controls (role-based, least privilege)
- [ ] Input Validation - All user input sanitized and validated
- [ ] Data Protection - Sensitive data encrypted (at rest and in transit)
- [ ] Dependency Security - No known vulnerabilities in dependencies
- [ ] Logging & Monitoring - Security events properly logged
- [ ] Error Handling - No information leakage in error messages
- [ ] Compliance - Meets regulatory requirements (GDPR, HIPAA, etc.)
```

**Checklist Principles:**
- **Systematic:** Covers all critical review dimensions
- **Actionable:** Each item can be verified objectively
- **Comprehensive:** No gaps in review coverage
- **Consistent:** Same checklist for all reviews (no shortcuts)

---

## Review Workflow (3 Phases)

### Phase 1: Preparation

**Purpose:** Understand what to review and why.

**Key Activities:**
1. **Understand Scope:**
   - Clarify what needs review (specific files, entire feature, configuration)
   - Identify review criteria (security, quality, compliance, best practices)
   - Determine applicable standards or guidelines

2. **Gather Context:**
   - Read relevant documentation (README, design docs, requirements)
   - Understand purpose and requirements
   - Note any special constraints or considerations

3. **Plan Review Strategy:**
   - Prioritize critical review areas (security first, then quality, then style)
   - Determine review depth (quick scan vs. thorough audit)
   - Identify tools and patterns to use (Grep searches, specific checks)

**Output:** Review plan with clear scope and approach.

### Phase 2: Analysis

**Purpose:** Systematically examine implementation.

**Key Activities:**
1. **Examine Implementation:**
   - **Deep analysis:** Use Read to examine specific files line-by-line
   - **Pattern search:** Use Grep to find patterns across codebase
   - **Coverage check:** Use Glob to ensure comprehensive file coverage
   - **Checklist verification:** Run through all 8 checklist items

2. **Identify Issues:**
   - **CRITICAL:** Security vulnerabilities, data loss risks, compliance violations
     - Example: SQL injection vulnerability, hardcoded credentials, PII exposure
   - **WARNING:** Code quality issues, potential bugs, performance concerns
     - Example: Code duplication, missing error handling, inefficient algorithm
   - **SUGGESTION:** Best practice improvements, refactoring opportunities
     - Example: Better naming, clearer comments, simpler structure

3. **Validate Findings:**
   - **Evidence:** Every issue has file path, line number, code snippet
   - **Cross-reference:** Check against standards and guidelines
   - **Severity assessment:** Accurate categorization (CRITICAL vs WARNING vs SUGGESTION)
   - **Avoid false positives:** Verify before flagging

**Output:** Categorized findings with evidence.

### Phase 3: Reporting

**Purpose:** Deliver actionable review findings.

**Key Activities:**
1. **Structure Findings:**
   - **Executive summary:** APPROVE / APPROVE_WITH_CONDITIONS / REJECT
   - **Findings by severity:** CRITICAL → WARNING → SUGGESTION
   - **Evidence for each:** File path, line number, code snippet
   - **Clear remediation:** Specific fixes, not vague recommendations

2. **Provide Recommendations:**
   - **Specific fixes:** "Change X to Y at line 45" (not "improve code quality")
   - **Best practices:** Reference standards (PEP 8, OWASP, project guidelines)
   - **Future prevention:** Patterns to avoid, proactive recommendations
   - **Follow-up actions:** If needed (re-review after fixes, deeper audit)

3. **Make Decision:**
   - **APPROVE:** No critical or blocking issues, ready to proceed
   - **APPROVE_WITH_CONDITIONS:** Minor issues exist, can proceed with documented fixes
   - **REJECT:** Critical issues require resolution before approval
   - **Rationale:** Clear explanation of decision reasoning

**Output:** Comprehensive review report with decision and recommendations.

---

## Communication Protocol

### Structured Review Report Format

```json
{
  "review_summary": "Reviewed authentication module (5 files, 342 lines)",
  "findings": {
    "critical": [
      "Password stored in plaintext (auth/login.py:45) - MUST use bcrypt/argon2",
      "SQL injection vulnerability (auth/queries.py:78) - Use parameterized queries"
    ],
    "warnings": [
      "No rate limiting on login endpoint (auth/routes.py:23) - Add to prevent brute force",
      "Error messages reveal user existence (auth/login.py:67) - Use generic messages"
    ],
    "suggestions": [
      "Consider using JWT for session management (current: server-side sessions)",
      "Add 2FA support for enhanced security (auth/login.py)"
    ]
  },
  "decision": "REJECT",
  "rationale": "2 critical security issues (plaintext passwords, SQL injection) must be resolved before approval. These pose immediate security risks.",
  "next_steps": [
    "Fix critical issues (plaintext passwords, SQL injection)",
    "Address warnings (rate limiting, error messages)",
    "Re-submit for review after fixes applied"
  ]
}
```

### Decision Criteria

**APPROVE:**
- Zero critical issues
- Zero warnings that block functionality
- Minor suggestions acceptable
- All 8 checklist items pass

**APPROVE_WITH_CONDITIONS:**
- Zero critical issues
- 1-3 warnings that don't block deployment
- Conditions clearly documented
- Plan to address warnings exists

**REJECT:**
- 1+ critical issues present
- Warnings that block functionality
- Missing required checklist items
- Unacceptable risk level

---

## Integration with Commands

### Reviewer in RPIV Workflow

**Typical Usage:** Verification phase of RPIV command.

**Example (from variance-analysis command):**
```markdown
### STEP 4: VERIFY Phase

Independent validation before delivery:

1. **Code Review:**
   @code-reviewer, verify:
   - Financial calculations use Decimal type (not float)
   - Error handling comprehensive (division by zero, NULL values)
   - Tests cover edge cases (zero budget, negative amounts)
   - Documentation complete (docstrings, README updated)

2. **Review Results:**
   - If APPROVED: Proceed to delivery
   - If APPROVED_WITH_CONDITIONS: Document conditions, proceed if acceptable
   - If REJECTED: Address critical issues, re-submit for review

**CHECKPOINT 4:** Final approval based on review findings.
```

**Reviewer Output:**
```json
{
  "review_summary": "Reviewed variance calculation module (3 files, 245 lines)",
  "findings": {
    "critical": [],
    "warnings": [
      "Missing edge case test for NULL budget values (tests/test_variance.py)"
    ],
    "suggestions": [
      "Consider adding docstring example for favorability logic (variance.py:34)",
      "Extract magic numbers to constants (variance.py:67, 89)"
    ]
  },
  "decision": "APPROVE_WITH_CONDITIONS",
  "rationale": "Core functionality correct (Decimal types, error handling). One missing edge case test (NULL budget) should be added but not blocking.",
  "next_steps": [
    "Add NULL budget test case",
    "Consider docstring and constant extraction suggestions"
  ]
}
```

---

## Finding Specification Best Practices

### CRITICAL Findings

**Definition:** Issues that pose immediate risk or violate critical requirements.

**Examples:**
- Security vulnerabilities (SQL injection, XSS, hardcoded secrets)
- Data loss risks (missing backups, unsafe deletions)
- Compliance violations (GDPR, HIPAA, SOC2 requirements)
- Financial precision errors (float instead of Decimal)
- Authentication/authorization bypass

**Format:**
```
CRITICAL: [Issue description] ([file:line])
- Impact: [What could go wrong]
- Fix: [Specific remediation]
- Reference: [Standard/guideline violated]
```

### WARNING Findings

**Definition:** Issues that should be addressed but don't block deployment.

**Examples:**
- Code quality issues (duplication, complexity, poor naming)
- Potential bugs (missing null checks, race conditions)
- Performance concerns (N+1 queries, inefficient algorithms)
- Missing tests (coverage gaps)
- Incomplete documentation

**Format:**
```
WARNING: [Issue description] ([file:line])
- Concern: [Why this matters]
- Recommendation: [How to improve]
```

### SUGGESTION Findings

**Definition:** Nice-to-have improvements, refactoring opportunities.

**Examples:**
- Better naming conventions
- Clearer comments
- Simpler structure or logic
- Alternative approaches
- Future extensibility

**Format:**
```
SUGGESTION: [Improvement idea] ([file:line])
- Benefit: [What would improve]
- Optional: [Not required, but recommended]
```

---

## Anti-Patterns

### ❌ Attempting to Fix Issues

**Problem:** Reviewer tries to modify files to fix issues found.

**Example:**
```markdown
# Reviewer agent (WRONG)
"Found SQL injection vulnerability. I'll fix it now..."
# Attempts to Edit file  ❌ FAIL - read-only tools
```

**Solution:** Report findings with specific fix recommendations. Implementation is done by domain specialist or human.

### ❌ Vague Findings

**Problem:** Issues reported without specificity.

**Example:**
```markdown
# Vague finding (WRONG)
"Code quality could be better"  # ❌ Not actionable
```

**Solution:** Specific, actionable findings.
```markdown
# Specific finding (CORRECT)
"CRITICAL: Function `calculate_total()` at line 45 uses hardcoded tax rate 0.08. Extract to configuration. (finance/calculator.py:45)"
```

### ❌ Inconsistent Severity

**Problem:** Severity levels not accurately assigned.

**Example:**
```markdown
# Incorrect severity (WRONG)
"CRITICAL: Variable name should be snake_case instead of camelCase"  # ❌ This is SUGGESTION, not CRITICAL
```

**Solution:** Use severity levels accurately:
- CRITICAL = security/compliance/data loss
- WARNING = quality/bugs/performance
- SUGGESTION = style/refactoring/improvements

### ❌ Skipping Checklist Items

**Problem:** Not running through full 8-item checklist.

**Example:**
```markdown
# Incomplete review (WRONG)
"I reviewed the code. Looks good."  # ❌ Which checklist items passed?
```

**Solution:** Document checklist completion explicitly.

---

## Summary

**Key Takeaways:**

1. **Read-Only Access:** Verification without modification (Read, Grep, Glob)
2. **Checklist-Driven:** 8 systematic verification checks
3. **Severity Levels:** CRITICAL / WARNING / SUGGESTION
4. **Decision-Making:** APPROVE / APPROVE_WITH_CONDITIONS / REJECT
5. **3-Phase Workflow:** Preparation → Analysis → Reporting
6. **3-5% Pattern:** Less common than domain specialists, distinct read-only constraint

**When to Create a Reviewer:**
- Need verification without modification risk
- Security audits requiring unbiased analysis
- Code review before merging or deploying
- Compliance verification (SOC2, GDPR, regulatory)
- Quality assurance checks

**Related Guides:**
- `domain-specialist-guide.md` - For implementation-focused agents (full tool access)
- `readonly-researcher-guide.md` - For investigation agents (read+web tools)

---

**This guide is based on 4-6 validated reviewer agents and project code-reviewer.md. Last updated: 2025-11-09**
