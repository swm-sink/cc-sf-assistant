# Research → Plan → Implement → Verify Workflow Template

## Overview
Structured workflow for building new features with Claude Code. Ensures thorough research, clear planning, systematic implementation, and independent verification.

---

## Phase 1: RESEARCH (No Coding)

### Objective
Understand requirements, existing patterns, and constraints before writing any code.

### Steps
1. **Read Requirements**
   - Review spec.md for business requirements
   - Identify user needs and pain points
   - Clarify ambiguous requirements with user

2. **Explore Codebase**
   - Use `@explore` agent or Task tool with subagent_type=Explore
   - Search for existing similar functionality (`Grep`, `Glob`)
   - Review external libraries (`external/` directory)
   - Identify reusable patterns

3. **Research External Solutions**
   - Search GitHub for relevant libraries/patterns
   - Review `docs/COMPREHENSIVE_GITHUB_SOURCES.md`
   - Check `external/` repos for applicable code
   - Document findings

4. **Document Findings**
   - Create `research-findings.md` with:
     - Requirements summary
     - Existing code patterns found
     - External libraries to leverage
     - Constraints identified
     - Proposed approach

5. **Human Checkpoint**
   - Present research findings to user
   - Get approval to proceed to planning phase

**Tools Used:** Read, Grep, Glob, WebSearch, WebFetch
**Agents:** `@explore`, `@research`
**Output:** `research-findings.md`

---

## Phase 2: PLAN (Specification)

### Objective
Create formal specification that defines inputs, outputs, validation rules, and test cases.

### Steps
1. **Generate Specification**
   - Define function signatures with type hints
   - Specify inputs (types, constraints, validation)
   - Specify outputs (types, format, audit trail)
   - Define business rules (e.g., favorability logic)
   - List edge cases to handle

2. **Define Test Cases**
   - Happy path scenarios
   - Edge cases (division by zero, negative values, NULL)
   - Error scenarios
   - Performance requirements

3. **Plan Implementation Steps**
   - Break into logical tasks
   - Identify dependencies
   - Estimate complexity
   - Note any risks

4. **Document Validation Criteria**
   - How will we know it works correctly?
   - What metrics indicate success?
   - What tests must pass?

5. **Human Checkpoint**
   - Present specification to user
   - Get explicit approval before coding
   - **DO NOT CODE until spec approved**

**Tools Used:** Read, Write
**Agents:** `@planner`
**Output:** `spec-[feature-name].md`

**Example Spec:**
```markdown
## Feature: YoY Revenue Growth Calculation

### Function Signature
```python
def calculate_yoy_growth(
    current_period: Decimal,
    prior_period: Decimal,
    period_type: Literal['monthly', 'quarterly', 'annual']
) -> YoYGrowthResult:
    ...
```

### Inputs
- `current_period`: Revenue for current period (Decimal, >= 0)
- `prior_period`: Revenue for prior year period (Decimal, >= 0)
- `period_type`: Time period granularity

### Outputs
```python
@dataclass
class YoYGrowthResult:
    growth_amount: Decimal
    growth_pct: Decimal
    period_type: str
    timestamp: str
    audit_trail: dict
```

### Business Rules
1. Growth % = (Current - Prior) / Prior * 100
2. If Prior = 0, growth % = None (cannot divide by zero)
3. Must use Decimal for all calculations
4. Must log audit trail

### Edge Cases
1. Prior period = 0
2. Current period = 0
3. Both periods = 0
4. Negative revenue (invalid input)

### Test Cases
1. Normal growth: current=115000, prior=100000 → 15% growth
2. Decline: current=85000, prior=100000 → -15% growth
3. Zero prior: current=100000, prior=0 → None
4. Both zero: current=0, prior=0 → None
```

---

## Phase 3: IMPLEMENT (With Checkpoints)

### Objective
Build feature systematically using TDD, with human approval at logical milestones.

### Steps
1. **Create Progress Tracker**
   ```markdown
   | Task | Status | Notes |
   |------|--------|-------|
   | Write tests | Pending | |
   | Implement core logic | Pending | |
   | Add error handling | Pending | |
   | Add audit logging | Pending | |
   | Refactor | Pending | |
   ```

2. **Follow TDD Workflow**
   - RED: Write failing tests
   - GREEN: Implement minimum code
   - REFACTOR: Improve quality
   - See `.claude/templates/workflows/TDD_WORKFLOW.md`

3. **Implement with Checkpoints**
   - **Checkpoint 1:** Tests written, all failing
     - Human reviews test coverage
     - Approval to implement
   - **Checkpoint 2:** Core logic implemented, tests passing
     - Human reviews basic functionality
     - Approval to add error handling
   - **Checkpoint 3:** Error handling + audit logging added
     - Human reviews robustness
     - Approval to refactor
   - **Checkpoint 4:** Code refactored, quality improved
     - Human reviews final code
     - Approval to verify

4. **Skills Auto-Invoked**
   - `python-best-practices`
   - `financial-script-generator`
   - `decimal-precision-enforcer`
   - `audit-trail-enforcer`

**Tools Used:** Read, Write, Edit, Bash (pytest)
**Agents:** `@implementer`, `@tester`
**Output:** Source code + tests in `scripts/` directory

---

## Phase 4: VERIFY (Independent)

### Objective
Independent verification by specialized agents and comprehensive testing.

### Steps
1. **Run Validation Suite**
   - Invoke `@script-validator` agent
   - Checks:
     - ✅ Syntax (Python parser)
     - ✅ Type safety (mypy)
     - ✅ Code quality (ruff)
     - ✅ Security (bandit)
     - ✅ Financial precision (no floats)
     - ✅ Test coverage (>80%)
   - Output: Validation report

2. **Independent Code Review**
   - Invoke `@code-reviewer` agent (separate context, read-only)
   - Reviews for:
     - Decimal usage correctness
     - Edge case handling
     - Audit trail presence
     - Business logic accuracy
     - Anti-patterns
   - Output: Review findings

3. **Address Findings**
   - Fix any issues identified
   - Re-run validation suite
   - Re-run code review if needed

4. **Run Comprehensive Tests**
   - Unit tests (pytest)
   - Edge case tests
   - Integration tests
   - Performance tests (if applicable)

5. **Human Final Review**
   - Review validation report
   - Review code review findings
   - Test manually with sample data
   - **APPROVE or REQUEST CHANGES**

6. **Finalize**
   - Commit code with clear message
   - Update documentation
   - Mark task as complete

**Tools Used:** Read, Grep, Bash (pytest, mypy, ruff)
**Agents:** `@script-validator`, `@code-reviewer`
**Output:** Validation report, review findings

---

## Phase Transitions

### Research → Plan
**Trigger:** Research findings documented and approved by human
**Gate:** No coding allowed in research phase

### Plan → Implement
**Trigger:** Specification approved by human
**Gate:** Must have formal spec before coding

### Implement → Verify
**Trigger:** All checkpoints passed, human approves implementation
**Gate:** Tests must be passing

### Verify → Complete
**Trigger:** Independent verification passed, human final approval
**Gate:** Validation suite + code review + human approval all green

---

## Example Session

```bash
# Phase 1: RESEARCH
User: "I need to calculate YoY revenue growth by department"
Claude: "Starting research phase. Let me explore existing code..."
Claude: [Uses @explore agent, searches codebase]
Claude: [Documents findings in research-findings.md]
User: "Approved, proceed to planning"

# Phase 2: PLAN
Claude: [Generates formal specification]
Claude: "Here's the spec for YoY growth calculation..."
User: "Looks good, one change: also calculate QoQ growth"
Claude: [Updates spec]
User: "Approved, begin implementation"

# Phase 3: IMPLEMENT
Claude: [Creates progress tracker]
Claude: [Writes failing tests]
User: "Checkpoint 1: Tests look comprehensive, implement core logic"
Claude: [Implements using Decimal]
User: "Checkpoint 2: Works, add error handling"
Claude: [Adds try/except, validation, audit logging]
User: "Checkpoint 3: Good, refactor for quality"
Claude: [Refactors with docstrings, type hints]
User: "Checkpoint 4: Approved, verify"

# Phase 4: VERIFY
User: "@script-validator validate scripts/core/yoy_growth.py"
script-validator: [Runs validation suite - all pass]
User: "@code-reviewer review scripts/core/yoy_growth.py"
code-reviewer: [Independent review - 1 suggestion]
Claude: [Addresses suggestion, re-validates]
User: "Final approval - commit and document"
Claude: [Commits with clear message]
```

---

## Key Principles

1. **No coding in research phase** - Understand first, code later
2. **Spec approval required** - Don't code without approved specification
3. **Human checkpoints** - User approves at each phase transition
4. **Independent verification** - Separate context agents review code
5. **TDD throughout** - Tests drive implementation
6. **Progressive disclosure** - Reveal details as needed

---

## Anti-Patterns to Avoid

❌ **Starting to code immediately**
✅ Research → Plan → Implement → Verify

❌ **Skipping specification**
✅ Get spec approved before coding

❌ **No human checkpoints**
✅ User approval at each phase

❌ **Self-review only**
✅ Independent agent verification

❌ **Testing after coding**
✅ TDD: Tests first, then code

---

**Source:** Based on Anthropic agentic patterns and Claude Code best practices (2025)
**References:**
- https://github.com/Pimzino/claude-code-spec-workflow
- Anthropic Claude Code Best Practices
- Research-Plan-Implement-Verify pattern
**Last Updated:** 2025-11-08
