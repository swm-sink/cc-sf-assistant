# Rationalization-Proofing Guide

**Purpose:** Comprehensive guide to making discipline skills bulletproof against bypass attempts

**Target audience:** Creators of discipline-type skills (workflow enforcement, quality gates, process requirements)

**Key insight:** Discipline skills fail when agents rationalize shortcuts. Rationalization-proofing prevents this.

---

## Table of Contents

1. [Why Rationalization-Proofing?](#why-rationalization-proofing)
2. [The 5 Techniques](#the-5-techniques)
3. [Iron Law (Foundational Principle)](#technique-1-iron-law)
4. [Explicit Negations](#technique-2-explicit-negations)
5. [Rationalization Table](#technique-3-rationalization-table)
6. [Red Flags (Warning Signs)](#technique-4-red-flags)
7. [CSO for Violation Symptoms](#technique-5-cso-for-violation-symptoms)
8. [Examples](#examples)
9. [Testing Discipline Skills](#testing-discipline-skills)
10. [Iterating to Bulletproof](#iterating-to-bulletproof)

---

## Why Rationalization-Proofing?

### The Problem

**Discipline skills without rationalization-proofing get bypassed:**

**Example scenario:**
```
User: "Add Google Sheets integration"

Without rationalization-proofing:
Claude: "I'll start implementing right away!"
[Skips research, writes code immediately, breaks authentication]

With rationalization-proofing:
Claude: "I'm using enforcing-research-plan-implement-verify. Starting Research phase."
[Follows workflow, discovers existing gspread library, implements correctly]
```

**Why bypass happens:**

1. **Time pressure:** "It's urgent, skip the process"
2. **Overconfidence:** "I already know how to do this"
3. **Sunk cost:** "I already wrote the code, don't delete it"
4. **Authority:** "Manager says do it now"
5. **Pragmatism:** "It's just one line, doesn't need full workflow"

**Consequence:** Discipline skills exist but don't enforce discipline.

### The Solution

**Rationalization-proofing** = preemptively addressing bypass attempts in the skill itself.

**How it works:**

1. **Predict** common rationalizations for skipping workflow
2. **Document** each rationalization with reality check
3. **Counter** with specific argument why rationalization is wrong
4. **Trigger** skill BEFORE bypass attempt (via CSO)
5. **Remind** agent when red flags detected

**Result:** Agent recognizes rationalization, resists shortcut, follows workflow.

---

## The 5 Techniques

Rationalization-proofing uses 5 complementary techniques:

| Technique | Purpose | Location in SKILL.md |
|-----------|---------|----------------------|
| **1. Iron Law** | Foundational principle (absolute requirement) | ## The Iron Law |
| **2. Explicit Negations** | Predicted bypass attempts | Under Iron Law |
| **3. Rationalization Table** | Excuse catalog with counters | ## Rationalization Table |
| **4. Red Flags** | Warning signs to recognize | ## Red Flags |
| **5. CSO for Violations** | Auto-invoke before bypass | YAML description |

**All 5 required for bulletproof discipline skills.**

---

## Technique 1: Iron Law

### What is an Iron Law?

**Iron Law** = Absolute requirement stated in emphatic, unambiguous language.

**Format:**
```markdown
## The Iron Law

```
NO X WITHOUT Y FIRST
```

Explanation of what happens when violated. Instruction to stop and follow workflow.

**No exceptions:**
- Don't {PREDICTED_BYPASS_1}
- Don't {PREDICTED_BYPASS_2}
- Don't {PREDICTED_BYPASS_3}
...

STOP means STOP. Y means NO X.
```

### Key Elements

1. **ALL CAPS code block** (visual emphasis)
2. **Absolute language** ("NO", "WITHOUT", "FIRST")
3. **Violation instruction** ("STOP. Delete code. Start over.")
4. **Explicit negations** (≥6 "Don't X" statements)
5. **Emphatic closing** ("STOP means STOP")

### Examples

**Example 1: enforcing-research-plan-implement-verify**
```markdown
## The Iron Law

```
NO IMPLEMENTATION WITHOUT RESEARCH & APPROVED PLAN FIRST
```

Starting implementation without approved research.md and plan.md? STOP. Delete any code. Start with Research phase.

**No exceptions:**
- Don't keep code as "reference"
- Don't "research while implementing"
- Don't "document plan after implementing"
- Don't "it's just one line, doesn't need research"
- Don't "emergency situation, skip process"
- Don't "I already know how, skip research"

STOP means STOP. Research means NO CODE.
```

**Example 2: test-driven-development (from superpowers)**
```markdown
## The Iron Law

```
NO IMPLEMENTATION WITHOUT FAILING TEST FIRST
```

Starting implementation before writing test? STOP. Delete implementation. Write test first.

**No exceptions:**
- Don't keep implementation as "reference"
- Don't "test while implementing"
- Don't "test after implementing"
- Don't "just trying an approach"
- Don't "I already know it works"
- Don't "emergency, will test later"

STOP means STOP. Test means NO IMPLEMENTATION.
```

### Why Iron Law Works

**Psychological impact:**
- ALL CAPS = emphatic, hard to ignore
- Code block = visual separation, stands out
- Absolute language = no wiggle room
- Explicit negations = addresses specific bypass attempts
- Repetition = reinforces requirement

**When agent considers bypass:**
1. Sees Iron Law in memory
2. Recognizes matching negation
3. Re-reads "STOP means STOP"
4. Follows workflow instead

---

## Technique 2: Explicit Negations

### What are Explicit Negations?

**Explicit Negations** = List of specific bypass attempts, each preceded by "Don't"

**Purpose:** Address exact loopholes agent might exploit.

**Format:**
```markdown
**No exceptions:**
- Don't {PREDICTED_BYPASS_1}
- Don't {PREDICTED_BYPASS_2}
- Don't {PREDICTED_BYPASS_3}
- Don't {PREDICTED_BYPASS_4}
- Don't {PREDICTED_BYPASS_5}
- Don't {PREDICTED_BYPASS_6}
```

### How to Generate Negations

**Step 1: Baseline testing (or use proven patterns)**

Run pressure scenarios without skill. Observe bypass attempts.

**Step 2: Extract verbatim rationalizations**

Record exact phrases agent uses to justify shortcuts.

**Step 3: Convert to negations**

```
Agent says: "I'll keep the code as a reference and rewrite it properly"
Negation: Don't keep code as "reference"

Agent says: "I'll research while implementing to save time"
Negation: Don't "research while implementing"

Agent says: "It's just one line, doesn't need full workflow"
Negation: Don't "it's just one line, doesn't need research"
```

**Step 4: Add to Iron Law section**

Place under "No exceptions:" heading.

### Target: ≥6 Negations

**Why 6+?**
- Covers most common bypass attempts
- Demonstrates thoroughness
- Signals "we've thought of your excuses"

**Categories to cover:**
1. **Scope minimization:** "just one line", "simple change"
2. **Timing tricks:** "while implementing", "after implementing"
3. **Knowledge claims:** "I already know", "familiar with this"
4. **Reference loophole:** "keep as reference", "use as guide"
5. **Emergency claims:** "urgent", "no time", "production down"
6. **Spirit vs letter:** "following spirit not letter", "being pragmatic"

### Examples

**Example: enforcing-research-plan-implement-verify**
```markdown
**No exceptions:**
- Don't keep code as "reference"
- Don't "research while implementing"
- Don't "document plan after implementing"
- Don't "it's just one line, doesn't need research"
- Don't "emergency situation, skip process"
- Don't "I already know how, skip research"
```

**Analysis:**
1. Reference loophole: "keep code as reference" ✅
2. Timing trick: "while implementing", "after implementing" ✅
3. Scope minimization: "just one line" ✅
4. Emergency: "emergency situation" ✅
5. Knowledge: "I already know" ✅
6. Six negations total ✅

---

## Technique 3: Rationalization Table

### What is a Rationalization Table?

**Rationalization Table** = Catalog of excuses with reality checks and counter-arguments.

**Format:**
```markdown
| Excuse | Reality | Counter-Argument |
|--------|---------|------------------|
| "{RATIONALIZATION}" | {TRUTH} | {WHY_TRUTH_MATTERS} |
```

**Purpose:**
- Preemptively address bypass excuses
- Provide counter-arguments ready to deploy
- Show thoroughness (discourages new rationalizations)

### Structure

**3 columns required:**

1. **Excuse:** Exact rationalization (in quotes)
   - Example: "I'll skip research, it's simple"

2. **Reality:** Truth statement
   - Example: "Simple tasks break. Research takes 15 min, debugging takes hours."

3. **Counter-Argument:** Why excuse is wrong
   - Example: "Complexity isn't predictable. 'Simple' changes often have hidden dependencies. Research always required."

### Target: ≥10 Entries

**Why 10+?**
- Comprehensive coverage
- Demonstrates anticipation
- Signals "we've seen this before"

**Must cover:**
- Simplicity claims (3 entries)
- Knowledge claims (2 entries)
- Time/emergency claims (2 entries)
- Authority claims (1 entry)
- Sunk cost claims (1 entry)
- Meta (workflow criticism) (1 entry)

### Example Table

```markdown
| Excuse | Reality | Counter-Argument |
|--------|---------|------------------|
| "I'll skip research, it's simple" | Simple tasks break. Research takes 15 min, debugging takes hours. | Complexity isn't predictable. "Simple" changes often have hidden dependencies. Research always required. |
| "I already know how to do this" | Assumptions cause bugs. Research validates knowledge. | Knowledge changes. Codebase changes. Verify assumptions even when confident. |
| "No time for 2-hour workflow" | Debugging production bugs takes longer than 2 hours. Prevention faster than cure. | Time spent in workflow < time spent debugging. Pragmatic = workflow. |
| "Emergency situation, skip process" | Emergencies without research cause worse emergencies. Follow workflow. | Emergency fix breaking production = worse emergency. Research even under pressure. |
| "Manager says fix it now" | Manager doesn't understand workflow. Explain, then request USER override. | Manager authority ≠ workflow exception. Only USER can approve override. |
| "I already spent X hours implementing" | Sunk cost fallacy. Time already gone. Choice now: trusted code vs technical debt. | Past time is gone. Current choice: delete and verify, or keep unverified code. |
| "Just exploring, not implementing" | Fine. Throw away exploration code. Start fresh with research after exploring. | Exploration ≠ implementation. Explore, learn, delete, then follow workflow. |
| "This is refactoring, not new code" | Refactoring changes behavior. Requires research (what are we preserving?) and plan. | Refactoring = behavior changes. Research existing behavior, plan preservation, verify. |
| "Workflow is too strict" | Strictness prevents financial calculation errors. For FP&A, strictness = correctness. | Loose workflow = production bugs. Strict workflow = trusted systems. |
| "I should be trusted to decide" | Trust isn't the issue. Consistency is. Workflow applies universally for reliability. | Trust = assuming competence. Workflow = ensuring consistency. Both needed. |
```

**Analysis:**
- ✅ Simplicity: Row 1
- ✅ Knowledge: Row 2
- ✅ Time: Row 3
- ✅ Emergency: Row 4
- ✅ Authority: Row 5
- ✅ Sunk cost: Row 6
- ✅ Scope: Row 7
- ✅ Refactoring: Row 8
- ✅ Meta (strictness): Row 9
- ✅ Meta (trust): Row 10
- ✅ Total: 10 entries ✅

### How to Use Table

**During skill invocation:**
Agent sees rationalization table in skill content, recognizes matching excuse, reads counter-argument, follows workflow.

**Example:**
```
Agent thinks: "I already implemented it, I'll just document the plan after"

Agent sees table:
| "I already spent X hours implementing" | Sunk cost fallacy. Time already gone. | Past time is gone. Delete and verify, or keep unverified code. |

Agent response: "I see this is sunk cost fallacy. I'll delete the implementation and start with Research phase."
```

---

## Technique 4: Red Flags

### What are Red Flags?

**Red Flags** = Warning signs that agent is about to bypass workflow.

**Format:**
```markdown
## Red Flags

**Warning signs you're about to violate this discipline:**

1. **Thinking:** "{RED_FLAG_THOUGHT}"
   - **Reality:** {REALITY_CHECK}

2. **Feeling:** {RED_FLAG_EMOTION}
   - **Reality:** {REALITY_CHECK}

...

**If you notice ANY red flag:** STOP. Re-read The Iron Law. Follow the workflow.
```

### Categories

1. **Thoughts** (5-8 entries)
   - "I'll skip research, it's simple"
   - "I already know how to do this"
   - "Let me just try this approach first"

2. **Emotions** (1-2 entries)
   - Feeling time pressure
   - Feeling confident/overconfident

3. **Behaviors** (1-2 entries)
   - Already wrote implementation code
   - Looking at reference implementation

4. **External pressures** (1-2 entries)
   - Manager says "do it now"
   - CFO needs it urgently

### Target: ≥8 Red Flags

**Why 8+?**
- Covers thoughts, emotions, behaviors, pressures
- Comprehensive early warning system
- Multiple opportunities to self-correct

### Example Red Flags

```markdown
## Red Flags

**Warning signs you're about to violate this discipline:**

1. **Thinking:** "I'll skip research, it's simple"
   - **Reality:** Simple tasks break. Research takes 15 min, debugging takes hours.

2. **Thinking:** "I already know how to do this"
   - **Reality:** Assumptions cause bugs. Research validates knowledge.

3. **Thinking:** "Let me just try this approach first"
   - **Reality:** Trying = implementing. Research before trying.

4. **Thinking:** "It's just one line, doesn't need research"
   - **Reality:** One line can break financial calculations. Size ≠ impact.

5. **Thinking:** "I'll document plan after implementing"
   - **Reality:** Plan-after documents what you built, not what you should build.

6. **Feeling:** Time pressure
   - **Reality:** Time pressure = highest error risk. Workflow prevents panic mistakes.

7. **Noticing:** Already wrote implementation code
   - **Reality:** Delete code. Start with Research phase.

8. **Pressure from:** Manager says "fix it now"
   - **Reality:** Manager authority ≠ workflow exception. Request USER override.

**If you notice ANY red flag:** STOP. Re-read The Iron Law. Follow the workflow.
```

**Analysis:**
- ✅ Thoughts: 5 entries
- ✅ Emotions: 1 entry
- ✅ Behaviors: 1 entry
- ✅ External: 1 entry
- ✅ Total: 8 red flags ✅
- ✅ Instruction at end ✅

---

## Technique 5: CSO for Violation Symptoms

### What is CSO for Violation Symptoms?

**CSO for violation symptoms** = Including bypass indicators in skill description so skill auto-invokes BEFORE bypass.

**Purpose:** Trigger skill when agent is thinking about skipping workflow, not after.

**Keywords to include:**

1. **Shortcut thoughts**
   - "thinking 'this is simple'"
   - "thinking 'I already know'"
   - "thinking 'just trying'"

2. **Pressure indicators**
   - "under time pressure"
   - "under deadline"
   - "emergency situation"

3. **Violation behaviors**
   - "about to implement without research"
   - "before writing implementation code"
   - "after already implementing"

### Example

**Without violation CSO:**
```yaml
description: Enforces Research Plan Implement Verify workflow
```

**Problem:** Only triggers when user asks for workflow. Doesn't trigger when about to bypass.

**With violation CSO:**
```yaml
description: Use when about to implement features, fix bugs, change code, or refactor, before writing implementation code, when thinking "this is simple enough to skip research", or when under time pressure - enforces Research → Plan → Implement → Verify workflow
```

**Benefit:** Triggers when agent is:
- About to implement (before bypass)
- Thinking shortcut thoughts (during rationalization)
- Under pressure (bypass risk highest)

---

## Examples

### Example 1: Minimal Discipline Skill (Score: 3/10)

```markdown
## Workflow

Follow Research → Plan → Implement → Verify.

**Steps:**
1. Research
2. Plan
3. Implement
4. Verify
```

**Rationalization-proofing score: 3/10**
- ❌ No Iron Law
- ❌ No explicit negations
- ❌ No rationalization table
- ❌ No red flags
- ❌ No CSO for violations
- ⚠️ Easily bypassed

### Example 2: Moderate Discipline Skill (Score: 6/10)

```markdown
## The Iron Law

```
NO IMPLEMENTATION WITHOUT RESEARCH FIRST
```

Starting implementation before research? STOP.

**No exceptions:**
- Don't skip research
- Don't implement first
- Don't say "it's simple"

## The Workflow

Follow Research → Plan → Implement → Verify.
```

**Rationalization-proofing score: 6/10**
- ✅ Has Iron Law
- ✅ Has 3 explicit negations (target 6)
- ❌ No rationalization table
- ❌ No red flags
- ❌ No CSO for violations
- ⚠️ Partially protected

### Example 3: Bulletproof Discipline Skill (Score: 10/10)

```markdown
---
name: enforcing-workflow
description: Use when about to implement features, fix bugs, before writing code, when thinking "this is simple", or under time pressure - enforces workflow
---

## The Iron Law

```
NO IMPLEMENTATION WITHOUT RESEARCH & APPROVED PLAN FIRST
```

Starting implementation without approved research.md? STOP. Delete code. Start with Research.

**No exceptions:**
- Don't keep code as "reference"
- Don't "research while implementing"
- Don't "document after"
- Don't "it's just one line"
- Don't "emergency, skip process"
- Don't "I already know"

STOP means STOP. Research means NO CODE.

## Red Flags

1. **Thinking:** "I'll skip research, it's simple"
   - **Reality:** Simple tasks break. Research takes 15 min, debugging takes hours.

2. **Thinking:** "I already know how"
   - **Reality:** Assumptions cause bugs. Research validates knowledge.

3. **Thinking:** "Let me just try this first"
   - **Reality:** Trying = implementing. Research before trying.

4. **Thinking:** "Just one line, doesn't need research"
   - **Reality:** One line can break production. Size ≠ impact.

5. **Thinking:** "I'll document plan after"
   - **Reality:** Plan-after ≠ plan-first. Different purposes.

6. **Feeling:** Time pressure
   - **Reality:** Pressure = highest error risk. Workflow prevents mistakes.

7. **Noticing:** Already wrote code
   - **Reality:** Delete code. Start with Research.

8. **Pressure from:** Manager says "now"
   - **Reality:** Manager authority ≠ exception. Request USER override.

**If you notice ANY red flag:** STOP. Re-read The Iron Law. Follow workflow.

## Rationalization Table

| Excuse | Reality | Counter-Argument |
|--------|---------|------------------|
| "I'll skip research, it's simple" | Simple tasks break. Research takes 15 min, debugging takes hours. | Complexity isn't predictable. Research always required. |
| "I already know how" | Assumptions cause bugs. | Knowledge changes. Verify assumptions. |
| "No time for workflow" | Debugging takes longer. | Time in workflow < time debugging. |
| "Emergency, skip process" | Emergencies without research cause worse emergencies. | Research even under pressure. |
| "Manager says now" | Manager doesn't understand workflow. | Only USER can approve override. |
| "Already spent X hours" | Sunk cost fallacy. | Past time gone. Delete and verify. |
| "Just exploring" | Fine. Throw away exploration. | Explore, learn, delete, then research. |
| "This is refactoring" | Refactoring changes behavior. | Research what to preserve. |
| "Workflow too strict" | Strictness prevents bugs. | Loose workflow = production bugs. |
| "I should be trusted" | Trust isn't the issue. | Workflow ensures consistency. |

## The Workflow

... (rest of skill)
```

**Rationalization-proofing score: 10/10**
- ✅ Iron Law in ALL CAPS code block
- ✅ 6 explicit negations
- ✅ 10 rationalization table entries
- ✅ 8 red flags with Reality checks
- ✅ CSO for violation symptoms in description
- ✅ **Bulletproof**

---

## Testing Discipline Skills

See `testing-protocol.md` for comprehensive testing guide.

**Quick test:**

1. Create pressure scenario (3+ combined pressures)
2. Run scenario WITHOUT skill
3. Document bypass attempts (verbatim)
4. Add bypasses to rationalization table
5. Run scenario WITH skill
6. Verify skill prevents bypass
7. Iterate until bulletproof

---

## Iterating to Bulletproof

**RED-GREEN-REFACTOR for discipline skills:**

### RED: Baseline Testing

1. Create 5-6 pressure scenarios
2. Run WITHOUT skill
3. Document all bypass attempts
4. Identify patterns (simplicity, knowledge, time, authority, sunk cost)

### GREEN: Write Minimal Skill

1. Create Iron Law from most common bypass
2. Add 6 explicit negations from baseline
3. Create rationalization table (10 entries from baseline)
4. Add 8 red flags from observed thoughts/feelings
5. CSO description with violation symptoms

### VERIFY GREEN: Test With Skill

1. Re-run all pressure scenarios WITH skill
2. Check if skill prevents bypasses
3. Document any new bypass attempts
4. Note: May need multiple iterations

### REFACTOR: Close Loopholes

1. Add new bypasses to rationalization table
2. Add new red flags if new thoughts observed
3. Strengthen explicit negations if loopholes found
4. Re-test until bulletproof (0 bypasses in all scenarios)

**Target:** 0 bypasses across all pressure scenarios

---

## Quick Reference

**Rationalization-Proofing Checklist:**

- [ ] **Iron Law:** ALL CAPS code block with absolute requirement
- [ ] **Explicit Negations:** ≥6 "Don't X" statements under Iron Law
- [ ] **Rationalization Table:** ≥10 entries with Excuse | Reality | Counter-Argument
- [ ] **Red Flags:** ≥8 warning signs with Reality checks
- [ ] **CSO for Violations:** Description includes bypass symptoms
- [ ] **Emphatic Language:** "STOP means STOP" closing
- [ ] **Instruction:** "If you notice ANY red flag: STOP"
- [ ] **Coverage:** Simplicity, knowledge, time, authority, sunk cost, meta

**Score:**
- 5/5 techniques = Bulletproof (10/10)
- 4/5 techniques = Good (8/10)
- 3/5 techniques = Moderate (6/10)
- <3/5 techniques = Weak (<5/10)

---

**Last Updated:** 2025-11-09
**Related:** `cso-guide.md`, `testing-protocol.md`
**Validator:** `scripts/validate_rationalization.py`
**Source:** Based on TDD skill patterns from external/superpowers
