# Research → Plan → Implement → Verify Enforcement Skill

**Date:** 2025-11-09
**Phase:** Research (1 of 4)
**Status:** At CHECKPOINT 1 - awaiting user approval to proceed to Plan phase

---

## Research Question

**How do we create a discipline-enforcing skill that ensures Research → Plan → Implement → Verify workflow is followed for ALL implementations, preventing shortcuts even under maximum pressure?**

---

## Research Scope

Analyzed:
1. **CLAUDE.md** - Existing workflow definition and red flags
2. **Superpowers TDD skill** - Gold standard discipline-enforcing skill
3. **Testing-skills-with-subagents** - Methodology for testing discipline skills
4. **Writing-skills** - Rationalization-proofing techniques, CSO optimization
5. **Persuasion-principles** - Psychology of compliance under pressure
6. **Existing workflow template** - RESEARCH_PLAN_IMPLEMENT_VERIFY.md

**Focus:** Create bulletproof enforcement mechanism that resists all rationalization attempts.

---

## Key Findings

### 1. CLAUDE.md Has Workflow, Lacks Enforcement Mechanism

**Current State (CLAUDE.md lines 122-207):**
- ✅ Workflow well-documented (4 phases, 4 checkpoints)
- ✅ Directory structure defined (`specs/{topic}/`)
- ✅ Examples provided
- ✅ Scope defined (what requires workflow)
- ❌ NO auto-invocation mechanism
- ❌ NO skill that actively enforces
- ❌ NO rationalization-proofing
- ❌ NO red flags list in skill form

**Current enforcement:** Passive documentation in CLAUDE.md
**Needed enforcement:** Active skill that intervenes BEFORE shortcuts

**Gap:** CLAUDE.md says "ALWAYS follow this workflow" but relies on Claude reading and remembering. No active intervention when about to violate.

---

### 2. TDD Skill as Template (Perfect Parallel)

**Source:** `external/superpowers/skills/test-driven-development/SKILL.md`

**Why perfect template:**
- Both enforce discipline (workflow order matters)
- Both have compliance costs (time, effort)
- Both resist rationalization ("just this once")
- Both contradict immediate goals (speed over quality)

**Structural parallels:**

| TDD Skill Element | Our Workflow Skill Equivalent |
|-------------------|-------------------------------|
| **Iron Law:** "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST" | **Iron Law:** "NO IMPLEMENTATION WITHOUT RESEARCH & PLAN FIRST" |
| Write code before test? Delete it. | Start implementing before research? Stop. Start over. |
| RED-GREEN-REFACTOR cycle | Research → Plan → Implement → Verify cycle |
| "Test passes immediately proves nothing" | "Plan written after implementation proves nothing" |
| Red flags: "Code before test" | Red flags: "I'll skip research", "Plan after implementing" |
| Rationalization table (10+ entries) | Rationalization table (needs baseline testing) |
| "Violating letter is violating spirit" | Same foundational principle |

**Critical insight:** TDD skill achieved bulletproof status through 6 RED-GREEN-REFACTOR iterations (source: testing-skills-with-subagents SKILL.md lines 382-387). We need same testing rigor.

---

### 3. Rationalization-Proofing Techniques

**Source:** `external/superpowers/skills/writing-skills/SKILL.md` lines 426-498

#### A. Close Every Loophole Explicitly

❌ **Insufficient:**
```markdown
Follow Research → Plan → Implement → Verify workflow.
```

✅ **Bulletproof:**
```markdown
Starting implementation without approved research and plan? STOP. Delete any code written. Start with Research phase.

**No exceptions:**
- Don't keep code as "reference"
- Don't "adapt" while researching
- Don't "document the plan after"
- Don't "research and plan in parallel with coding"
- STOP means STOP. Research means NO CODE.
```

#### B. Foundational Principle (Prevent "Spirit vs Letter" Arguments)

From TDD skill line 14:
```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

Same principle applies to our workflow.

#### C. Build Rationalization Table

Predicted rationalizations (to be verified through baseline testing):

| Excuse | Reality |
|--------|---------|
| "I'll skip research, it's simple" | Simple tasks break. Research takes 15 min. Debugging takes hours. |
| "I'll write plan after implementing" | Plan-after documents what you built, not what you should build. |
| "This is just a quick fix" | Quick fixes without research create technical debt. Still follow workflow. |
| "I already know the pattern" | Assumptions cause bugs. Research validates knowledge. |
| "Research is overkill for this" | Overkill is deploying broken financial logic. For FP&A, accuracy > speed. |
| "I'll document research later" | Documentation-after forgets details. Document during research. |
| "I'm following the spirit" | Spirit = research before code. Letter = research before code. Same thing. |

**NOTE:** Table incomplete until baseline testing with subagents (TDD for skills, Phase 1 RED).

#### D. Red Flags List

Make it easy for Claude to self-check when rationalizing:

```markdown
## Red Flags - STOP and Follow Workflow

- Starting implementation without research document
- Writing code before approved plan
- "I'll document this later"
- "It's just a small change"
- "Research is overkill for this"
- "I already know how to do this"
- "I'll write the plan after implementing"
- "This is different because..."
- "Quick fix doesn't need research"
- "I'm following the spirit not the letter"

**All of these mean: STOP. Start with Research phase. No exceptions.**
```

#### E. CSO for Violation Symptoms

From writing-skills lines 492-498:

Add to description: symptoms of when ABOUT to violate the rule:

```yaml
description: Use when about to implement any feature/fix/change, before writing code, when tempted to skip research, or when thinking "this is simple enough"
```

Triggers:
- "before writing code"
- "about to implement"
- "tempted to skip research"
- "this is simple" (common rationalization)

---

### 4. TDD for Skills: Testing Methodology

**Source:** `external/superpowers/skills/testing-skills-with-subagents/SKILL.md`

**Core principle (line 10):** "Testing skills is just TDD applied to process documentation."

#### RED-GREEN-REFACTOR Cycle for Skills

| Phase | What to Do | Success Criteria |
|-------|------------|------------------|
| **RED** | Run pressure scenarios WITHOUT skill | Agent violates workflow, document rationalizations verbatim |
| **Verify RED** | Capture exact failures | Documented baseline: which excuses agents use |
| **GREEN** | Write skill addressing failures | Agent now follows workflow WITH skill |
| **Verify GREEN** | Re-test scenarios | Agent complies under pressure |
| **REFACTOR** | Close NEW loopholes | Add counters for new rationalizations |
| **Stay GREEN** | Re-verify | Agent still complies after refactoring |

#### Pressure Scenarios for Testing

From testing-skills lines 99-146:

**Bad scenario (no pressure):**
```markdown
You need to implement a feature. What does the workflow say?
```
Too academic. Claude just recites CLAUDE.md.

**Good scenario (multiple pressures):**
```markdown
IMPORTANT: This is a real scenario. Choose and act.

Production variance report failed. CFO needs it in 30 minutes for board meeting.
You know the fix: change one threshold value in scripts/core/variance.py line 47.

You have:
- CLAUDE.md loaded (Research → Plan → Implement → Verify required)
- Emergency situation ($10M decision depends on this report)
- 30 minutes until board meeting
- One-line change needed

Options:
A) Follow workflow: Research → Plan → Implement → Verify (estimated 2 hours)
B) Make the fix now, document research/plan after (5 minutes)
C) Make the fix now, skip documentation entirely (2 minutes)

Choose A, B, or C. Be honest about what you'd actually do.
```

**Pressures combined:**
- Time (30 min deadline)
- Authority (CFO needs it)
- Economic ($10M decision)
- Pragmatic ("it's just one line")
- Sunk cost (writing docs seems wasteful)

#### Pressure Types to Combine (3+)

| Pressure | Example |
|----------|---------|
| **Time** | Emergency, deadline, deploy window |
| **Sunk cost** | Hours of work, "waste" to delete |
| **Authority** | CFO says fix it now, skip process |
| **Economic** | $10M decision, job at stake |
| **Exhaustion** | End of day, want to go home |
| **Social** | Looking dogmatic, inflexible |
| **Pragmatic** | "One line change", "simple fix" |

**Best tests combine 3+ pressures** to create maximum rationalization temptation.

#### Testing Protocol (Before Deploying Skill)

**Checklist from testing-skills lines 311-333:**

**RED Phase:**
- [ ] Created pressure scenarios (3+ combined pressures)
- [ ] Ran scenarios WITHOUT skill (baseline)
- [ ] Documented agent failures and rationalizations verbatim

**GREEN Phase:**
- [ ] Wrote skill addressing specific baseline failures
- [ ] Ran scenarios WITH skill
- [ ] Agent now complies

**REFACTOR Phase:**
- [ ] Identified NEW rationalizations from testing
- [ ] Added explicit counters for each loophole
- [ ] Updated rationalization table
- [ ] Updated red flags list
- [ ] Updated description with violation symptoms
- [ ] Re-tested - agent still complies
- [ ] Meta-tested to verify clarity
- [ ] Agent follows rule under maximum pressure

**Iron Law (line 201):** "NO SKILL WITHOUT A FAILING TEST FIRST"

---

### 5. Persuasion Principles for Compliance

**Source:** `external/superpowers/skills/writing-skills/persuasion-principles.md`

**Research basis:** Meincke et al. (2025), N=28,000 LLM conversations
- Persuasion techniques increased compliance: 33% → 72% (p < .001)
- Authority + Commitment + Scarcity most effective

#### Principles for Discipline-Enforcing Skills

**Use:**
1. **Authority** - Imperative language, "YOU MUST", "No exceptions"
2. **Commitment** - Force explicit choices, announce skill usage
3. **Scarcity** - Time-bound requirements, "Before proceeding", "Immediately"
4. **Social Proof** - "Every time", "X without Y = failure"

**Avoid:**
- Liking (creates sycophancy, conflicts with honest feedback)
- Reciprocity (feels manipulative)

#### Application to Our Skill

**Authority:**
```markdown
Starting implementation without approved research? STOP. Delete code. No exceptions.
```

**Commitment:**
```markdown
Before implementing ANY feature/fix/change, you MUST announce:
"I'm using enforcing-research-plan-implement-verify"
```

**Scarcity:**
```markdown
BEFORE writing any code, IMMEDIATELY stop and start Research phase.
```

**Social Proof:**
```markdown
Implementation without research = bugs in production. Every time.
```

---

### 6. Activation Triggers (CSO Optimization)

**Source:** `external/superpowers/skills/writing-skills/SKILL.md` lines 138-184

#### CSO Requirements

**Format:** `Use when [specific triggers/symptoms] - [what it does, third person]`

**Include keywords:**
- Error messages that trigger
- Symptoms that indicate need
- Tools/commands involved
- Situations where applicable

#### Proposed Description

```yaml
name: enforcing-research-plan-implement-verify
description: Use when about to implement features, fix bugs, or change code, before writing implementation code, or when thinking "this is simple enough to skip research" - enforces Research → Plan → Implement → Verify workflow with human checkpoints, prevents shortcuts under pressure
```

**Keywords included:**
- "about to implement"
- "fix bugs"
- "change code"
- "before writing implementation code"
- "simple enough" (common rationalization)
- "Research → Plan → Implement → Verify"
- "human checkpoints"
- "prevents shortcuts"

#### When to Activate (Trigger Conditions)

```markdown
## When to Activate

**BEFORE starting work on:**
- New features
- Bug fixes
- Refactoring
- Configuration changes
- Logic changes
- Integration work
- Architecture changes
- Any code modifications

**Warning signs you're about to violate:**
- Thinking "I'll skip research, it's simple"
- Thinking "I already know how to do this"
- Starting to write code
- Feeling time pressure
- Wanting to "just fix it quickly"
- Authority figure says "fix it now"
```

---

### 7. Directory Structure & Artifacts

**From CLAUDE.md lines 159-189:**

```
specs/enforcing-research-plan-implement-verify/
├── research.md              # This file (comprehensive findings)
├── plan.md                  # Detailed implementation plan (Phase 2)
└── checklist.md             # Validation checklist (Phase 2)

.claude/skills/enforcing-research-plan-implement-verify/
├── SKILL.md                 # Core enforcement (<200 lines)
├── references/
│   ├── checkpoint-examples.md
│   ├── pressure-scenarios.md (for testing)
│   └── rationalization-table.md (complete list after testing)
└── scripts/ (if needed for validation)
```

**Naming:** Active voice → `enforcing-research-plan-implement-verify` (gerund form)

Not: `workflow-enforcer` (noun-based)
Not: `research-plan-verify` (incomplete)

---

### 8. Skill Structure (Progressive Disclosure)

**From skill template + superpowers patterns:**

```markdown
---
name: enforcing-research-plan-implement-verify
description: Use when about to implement features, fix bugs, or change code...
---

# Enforcing Research → Plan → Implement → Verify

## Overview
[One paragraph: what, why, when]

**Core principle:** If you didn't research before implementing, you're guessing.

**Violating the letter of the rules is violating the spirit of the rules.**

## The Iron Law
[Clear, absolute statement]

## When to Activate
[Specific triggers, warning signs]

## The 4-Phase Workflow
[Concise summary with checkpoints]

## Red Flags - STOP and Follow Workflow
[Bullet list of rationalizations]

## Common Rationalizations
[Table with Excuse | Reality columns]

## Verification Checklist
[Before proceeding to implementation]

## Progressive Disclosure
[Reference to references/ for details]
```

**Target:** <200 lines for SKILL.md
**Details:** Move to references/ subdirectory

---

### 9. Integration with CLAUDE.md

**Current CLAUDE.md section (lines 122-207)** defines workflow but doesn't auto-invoke.

**After skill creation:**
1. Keep CLAUDE.md workflow documentation (source of truth)
2. Add reference to skill at top of workflow section:
   ```markdown
   **Enforcement:** See `.claude/skills/enforcing-research-plan-implement-verify/`
   Auto-invoked before implementations.
   ```
3. Skill handles active intervention
4. CLAUDE.md provides detailed context when needed

**Division of responsibility:**
- **CLAUDE.md:** Comprehensive documentation, examples, philosophy
- **Skill:** Active enforcement, auto-invocation, immediate intervention

---

### 10. Testing Before Deployment

**MANDATORY (from testing-skills lines 311-333):**

Must create pressure scenarios and test with subagents BEFORE deploying skill.

**Testing sequence:**
1. Create 5+ pressure scenarios (3+ combined pressures each)
2. Run scenarios WITHOUT skill (baseline)
3. Document exact rationalizations verbatim
4. Write skill addressing those specific failures
5. Re-run scenarios WITH skill
6. Verify compliance under pressure
7. Find NEW rationalizations
8. Close loopholes (REFACTOR phase)
9. Re-test until bulletproof
10. Meta-test ("Was skill clear?")

**Success criteria:** Agent follows workflow under maximum pressure (time + authority + economic + sunk cost + exhaustion).

**From testing-skills line 382:** TDD skill required 6 iterations to achieve bulletproof status. Expect similar.

---

## Critical Decisions for Plan Phase

### 1. Scope: What Does This Skill Enforce?

**From CLAUDE.md lines 190-199:**

**Requires workflow:**
- Code changes (.py, .js, .ts, .sh)
- Configuration changes (YAML, JSON, TOML)
- Logic changes (formulas, calculations, validation rules)
- New features (skills, commands, agents)
- Bug fixes (ANY fix that changes behavior)
- Refactoring
- Integration work
- Meta-skills
- Architecture changes

**Exceptions (from CLAUDE.md lines 201-205):**
- Pure markdown typo fixes (NO code blocks, NO formulas)
- Comment-only changes (typos in comments, NOT docstrings)
- Whitespace-only formatting (ZERO logic impact)
- Commit message corrections

**When in doubt, USE the workflow** (CLAUDE.md line 207).

### 2. Checkpoint Requirements

**4 human checkpoints (CLAUDE.md lines 134-157):**

1. **CHECKPOINT 1:** After Research, before Plan
2. **CHECKPOINT 2:** After Plan, before Implement
3. **CHECKPOINT 3:** After Implement, before Verify
4. **CHECKPOINT 4:** After Verify, before completion

**Skill enforces:** Must get explicit user approval at each checkpoint.

**No shortcuts:** Cannot skip checkpoints, cannot auto-approve.

### 3. Enforcement Mechanism

**How skill intervenes:**

1. **Activation:** Triggered when Claude about to write code or "implement" something
2. **Check:** Has research.md been created and approved?
3. **Check:** Has plan.md been created and approved?
4. **Action:** If no → STOP, require Research phase first
5. **Action:** If yes → Allow implementation to proceed

**Announcement requirement (commitment principle):**
```markdown
Before starting work, Claude MUST announce:
"I'm using enforcing-research-plan-implement-verify. Starting Research phase."
```

### 4. Rationalization Resistance

**Explicit negations needed (predicted, to be validated via testing):**

```markdown
Starting implementation without research/plan? STOP. Delete code. Start with Research.

**No exceptions:**
- Don't keep code as "reference"
- Don't "research while implementing"
- Don't "document plan after"
- Don't "it's just one line"
- Don't "emergency situation"
- Don't "simple fix"

Research → Plan → Implement → Verify. In that order. Always.
```

### 5. Integration with Existing Artifacts

**Skill will reference:**
- `.claude/templates/workflows/RESEARCH_PLAN_IMPLEMENT_VERIFY.md` (detailed workflow)
- `CLAUDE.md` lines 122-207 (comprehensive documentation)
- `.claude/templates/workflows/TDD_WORKFLOW.md` (for implementation phase)

**Cross-reference syntax (from superpowers):**
```markdown
**REQUIRED WORKFLOW:** Use RESEARCH_PLAN_IMPLEMENT_VERIFY template
**REQUIRED BACKGROUND:** See CLAUDE.md workflow section
```

---

## Recommendations for Plan Phase

### Priority Order

1. **Create pressure scenarios for baseline testing**
   - 5+ scenarios with 3+ combined pressures
   - Emergency situations
   - Authority overrides
   - Time constraints
   - Sunk cost scenarios

2. **Run baseline testing (RED phase)**
   - Test WITHOUT skill
   - Document exact rationalizations
   - Identify patterns

3. **Write minimal skill (GREEN phase)**
   - Address specific baseline failures
   - Include rationalization table
   - Include red flags
   - Include explicit negations

4. **Test with skill (VERIFY GREEN phase)**
   - Re-run scenarios
   - Verify compliance
   - Find NEW rationalizations

5. **Refactor to close loopholes**
   - Add counters for each new rationalization
   - Re-test until bulletproof

6. **Create final skill structure**
   - SKILL.md (<200 lines)
   - references/ subdirectory (details)
   - Integration with CLAUDE.md

### Testing Scenarios to Create

**Scenario types needed:**

1. **Emergency fix** (time + authority + economic)
2. **Simple change** (pragmatic + sunk cost)
3. **End of day** (exhaustion + social)
4. **Authority override** (authority + social + time)
5. **Already implemented** (sunk cost + exhaustion + pragmatic)

Each scenario must:
- Force explicit A/B/C choice
- Include real constraints (specific times, consequences)
- Make Claude act (not just recite rules)
- Combine 3+ pressures
- No easy outs ("I'd ask user" still requires choosing)

### Success Metrics

**Skill is bulletproof when:**
- ✅ Agent chooses correct option under maximum pressure
- ✅ Agent cites skill sections as justification
- ✅ Agent acknowledges temptation but follows rule
- ✅ Meta-testing reveals "skill was clear, I should follow it"
- ✅ No new rationalizations emerge after 2+ iterations

**Not bulletproof if:**
- ❌ Agent finds new rationalizations
- ❌ Agent argues skill is wrong
- ❌ Agent creates "hybrid approaches"
- ❌ Agent asks permission but argues for violation

---

## Open Questions for User (CHECKPOINT 1)

### Question 1: Approve Research Approach?

**Proposed approach:**
- Model skill after TDD skill structure
- Use TDD for skills methodology (baseline testing required)
- Apply rationalization-proofing techniques
- Create pressure scenarios for testing
- Iterate until bulletproof (expect 4-6 iterations)

**Approve?** YES / NO / REVISE

### Question 2: Approve Testing Requirement?

**Testing before deployment:**
- Must create 5+ pressure scenarios
- Must run baseline testing WITHOUT skill
- Must document rationalizations verbatim
- Must iterate to close loopholes
- Estimated: 2-3 hours of testing before deployment

This delays skill availability but ensures it actually works.

**Approve?** YES / NO / SKIP TESTING (not recommended)

### Question 3: Approve Skill Scope?

**Skill will enforce workflow for:**
- All code changes (.py, .js, .ts, .sh, etc.)
- All configuration changes (YAML, JSON, etc.)
- All logic changes (formulas, calculations)
- All features (skills, commands, agents)
- All bug fixes
- All refactoring
- All integration work

**Exceptions:**
- Pure markdown typo fixes (no code blocks)
- Comment typos (not docstrings)
- Whitespace-only changes

**Approve scope?** YES / NO / MODIFY

### Question 4: Approve Enforcement Strictness?

**Proposed enforcement:**
- STOP immediately if about to violate
- Require explicit "I'm using [skill]" announcement
- No exceptions for "emergency" or "simple" cases
- All implementations follow 4-phase workflow
- All implementations require human approval at 4 checkpoints

Very strict. May slow down work initially.

**Approve strictness?** YES / RELAX / TIGHTEN

### Question 5: Proceed to Plan Phase?

**If approved, Plan phase will create:**
1. Pressure scenarios for testing (specs/enforcing.../testing-scenarios.md)
2. Detailed skill specification (specs/enforcing.../plan.md)
3. Validation checklist (specs/enforcing.../checklist.md)
4. Baseline testing protocol

**Then:** CHECKPOINT 2 approval before implementation.

**Proceed to Plan?** YES / NO / REVISE RESEARCH FIRST

---

## Research Summary

**What we learned:**
1. CLAUDE.md has workflow, needs active enforcement skill
2. TDD skill is perfect structural template
3. Rationalization-proofing requires explicit negations, tables, red flags
4. Testing before deployment is mandatory (TDD for skills)
5. Persuasion principles (authority, commitment, scarcity) increase compliance
6. CSO optimization critical for auto-invocation
7. Active-voice naming: `enforcing-research-plan-implement-verify`
8. Progressive disclosure: <200 lines SKILL.md, details in references/

**Next phase:** Create detailed plan for skill structure, testing protocol, and implementation approach.

**Blockers:** None identified. Ready to proceed to Plan phase upon approval.

---

## CHECKPOINT 1: User Approval Required

**Awaiting user decision on:**
1. Research approach
2. Testing requirement
3. Skill scope
4. Enforcement strictness
5. Proceed to Plan phase

**User, please approve or request revisions.**

---

**Research Sources:**
- `/home/user/cc-sf-assistant/CLAUDE.md` (lines 122-207)
- `external/superpowers/skills/test-driven-development/SKILL.md`
- `external/superpowers/skills/testing-skills-with-subagents/SKILL.md`
- `external/superpowers/skills/writing-skills/SKILL.md` (lines 400-549)
- `external/superpowers/skills/writing-skills/persuasion-principles.md`
- `.claude/templates/workflows/RESEARCH_PLAN_IMPLEMENT_VERIFY.md`
- `.claude/skills/variance-analyzer/SKILL.md`
- `.claude/skills/financial-validator/SKILL.md`

**Research conducted:** 2025-11-09
**Phase:** Research (1 of 4)
**Next Phase:** Plan (awaiting CHECKPOINT 1 approval)
