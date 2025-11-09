# Discipline Template

**Purpose:** Template for discipline-type skills (workflow enforcement with rationalization-proofing)

**Use when:** Enforcing a process, preventing shortcuts, or requiring specific behavior

**Structure:** 12 sections (Overview → Iron Law → Red Flags → Workflow → Rationalization Table → Checkpoints → Emergency Override → Examples → Testing → Resistance → Meta → Progressive Disclosure)

**Key feature:** Rationalization-proofing to make skill bulletproof against bypass attempts

---

## Template Structure

```markdown
---
name: {{SKILL_NAME}}
description: {{CSO_OPTIMIZED_DESCRIPTION}}
---

# {{SKILL_TITLE}}

## Overview

**Purpose:** {{ONE_SENTENCE_PURPOSE}}

**This skill enforces:**
- {{ENFORCEMENT_1}}
- {{ENFORCEMENT_2}}
- {{ENFORCEMENT_3}}

**This skill does NOT:**
- {{NON_ENFORCEMENT_1}}
- {{NON_ENFORCEMENT_2}}

**Why this discipline matters:**

{{RATIONALE_PARAGRAPH}}

---

## The Iron Law

```
{{IRON_LAW_STATEMENT}}
```

{{IRON_LAW_EXPLANATION}}

**No exceptions:**
- Don't {{EXCEPTION_ATTEMPT_1}}
- Don't {{EXCEPTION_ATTEMPT_2}}
- Don't {{EXCEPTION_ATTEMPT_3}}
- Don't {{EXCEPTION_ATTEMPT_4}}
- Don't {{EXCEPTION_ATTEMPT_5}}
- Don't {{EXCEPTION_ATTEMPT_6}}

{{STOP_MEANS_STOP_STATEMENT}}

---

## Red Flags

**Warning signs you're about to violate this discipline:**

1. **Thinking:** "{{RED_FLAG_THOUGHT_1}}"
   - **Reality:** {{REALITY_CHECK_1}}

2. **Thinking:** "{{RED_FLAG_THOUGHT_2}}"
   - **Reality:** {{REALITY_CHECK_2}}

3. **Thinking:** "{{RED_FLAG_THOUGHT_3}}"
   - **Reality:** {{REALITY_CHECK_3}}

4. **Thinking:** "{{RED_FLAG_THOUGHT_4}}"
   - **Reality:** {{REALITY_CHECK_4}}

5. **Thinking:** "{{RED_FLAG_THOUGHT_5}}"
   - **Reality:** {{REALITY_CHECK_5}}

6. **Feeling:** {{RED_FLAG_EMOTION_1}}
   - **Reality:** {{REALITY_CHECK_6}}

7. **Noticing:** {{RED_FLAG_BEHAVIOR_1}}
   - **Reality:** {{REALITY_CHECK_7}}

8. **Pressure from:** {{RED_FLAG_PRESSURE_1}}
   - **Reality:** {{REALITY_CHECK_8}}

{{ADDITIONAL_RED_FLAGS}}

**If you notice ANY red flag:** STOP. Re-read The Iron Law. Follow the workflow.

---

## The Workflow

### Phase 1: {{PHASE_1_NAME}}

**Purpose:** {{PHASE_1_PURPOSE}}

**Actions:**
1. {{PHASE_1_ACTION_1}}
2. {{PHASE_1_ACTION_2}}
3. {{PHASE_1_ACTION_3}}

**Deliverable:** {{PHASE_1_DELIVERABLE}}

**CHECKPOINT 1:** {{CHECKPOINT_1_REQUIREMENT}}

### Phase 2: {{PHASE_2_NAME}}

**Purpose:** {{PHASE_2_PURPOSE}}

**Actions:**
1. {{PHASE_2_ACTION_1}}
2. {{PHASE_2_ACTION_2}}
3. {{PHASE_2_ACTION_3}}

**Deliverable:** {{PHASE_2_DELIVERABLE}}

**CHECKPOINT 2:** {{CHECKPOINT_2_REQUIREMENT}}

### Phase 3: {{PHASE_3_NAME}}

**Purpose:** {{PHASE_3_PURPOSE}}

**Actions:**
1. {{PHASE_3_ACTION_1}}
2. {{PHASE_3_ACTION_2}}
3. {{PHASE_3_ACTION_3}}

**Deliverable:** {{PHASE_3_DELIVERABLE}}

**CHECKPOINT 3:** {{CHECKPOINT_3_REQUIREMENT}}

### Phase 4: {{PHASE_4_NAME}}

**Purpose:** {{PHASE_4_PURPOSE}}

**Actions:**
1. {{PHASE_4_ACTION_1}}
2. {{PHASE_4_ACTION_2}}
3. {{PHASE_4_ACTION_3}}

**Deliverable:** {{PHASE_4_DELIVERABLE}}

**CHECKPOINT 4:** {{CHECKPOINT_4_REQUIREMENT}}

---

## Rationalization Table

**Common excuses for skipping this workflow, with reality checks:**

| Excuse | Reality | Counter-Argument |
|--------|---------|------------------|
| "{{RATIONALIZATION_1}}" | {{REALITY_1}} | {{COUNTER_1}} |
| "{{RATIONALIZATION_2}}" | {{REALITY_2}} | {{COUNTER_2}} |
| "{{RATIONALIZATION_3}}" | {{REALITY_3}} | {{COUNTER_3}} |
| "{{RATIONALIZATION_4}}" | {{REALITY_4}} | {{COUNTER_4}} |
| "{{RATIONALIZATION_5}}" | {{REALITY_5}} | {{COUNTER_5}} |
| "{{RATIONALIZATION_6}}" | {{REALITY_6}} | {{COUNTER_6}} |
| "{{RATIONALIZATION_7}}" | {{REALITY_7}} | {{COUNTER_7}} |
| "{{RATIONALIZATION_8}}" | {{REALITY_8}} | {{COUNTER_8}} |
| "{{RATIONALIZATION_9}}" | {{REALITY_9}} | {{COUNTER_9}} |
| "{{RATIONALIZATION_10}}" | {{REALITY_10}} | {{COUNTER_10}} |

**If you catch yourself making ANY excuse from this table:** Read the Reality and Counter-Argument columns. Follow the workflow anyway.

**For comprehensive rationalization catalog, see:** `references/complete-rationalization-table.md`

---

## Checkpoint Requirements

### What is a Checkpoint?

{{CHECKPOINT_DEFINITION}}

### Checkpoint Protocol

**At each checkpoint:**

1. **{{CHECKPOINT_ACTION_1}}**
2. **{{CHECKPOINT_ACTION_2}}**
3. **{{CHECKPOINT_ACTION_3}}**
4. **{{CHECKPOINT_ACTION_4}}**

**User must explicitly approve** before proceeding to next phase.

**Acceptable approval phrases:**
- "{{APPROVAL_PHRASE_1}}"
- "{{APPROVAL_PHRASE_2}}"
- "{{APPROVAL_PHRASE_3}}"

**If user doesn't approve:** {{NON_APPROVAL_ACTION}}

**For detailed checkpoint examples, see:** `references/checkpoint-examples.md`

---

## Emergency Override Protocol

### When Emergency Override Needed

{{EMERGENCY_DEFINITION}}

**Examples of legitimate emergencies:**
- {{EMERGENCY_EXAMPLE_1}}
- {{EMERGENCY_EXAMPLE_2}}
- {{EMERGENCY_EXAMPLE_3}}

### Emergency Override Process

**Step 1: Explain situation to user**

```
{{EMERGENCY_EXPLANATION_TEMPLATE}}
```

**Step 2: Present options**

```
A) {{OPTION_A}}
B) {{OPTION_B}}
C) {{OPTION_C}}
```

**Step 3: Wait for USER approval**

Only proceed with emergency override if user explicitly approves.

**Step 4: Post-emergency documentation**

Even with override, retroactively document:
- {{POST_EMERGENCY_DOC_1}}
- {{POST_EMERGENCY_DOC_2}}

**CRITICAL:** Emergency override requires USER approval. Never self-approve.

---

## Examples

### Example 1: {{EXAMPLE_1_SCENARIO}}

**User request:** "{{EXAMPLE_1_REQUEST}}"

**Without this skill:**
{{EXAMPLE_1_WITHOUT_SKILL}}

**With this skill:**
{{EXAMPLE_1_WITH_SKILL}}

**Outcome:** {{EXAMPLE_1_OUTCOME}}

### Example 2: {{EXAMPLE_2_SCENARIO}}

**User request:** "{{EXAMPLE_2_REQUEST}}"

**Red flags detected:** {{EXAMPLE_2_RED_FLAGS}}

**How skill prevented shortcut:** {{EXAMPLE_2_PREVENTION}}

**Outcome:** {{EXAMPLE_2_OUTCOME}}

### Example 3: {{EXAMPLE_3_SCENARIO}} (Emergency Override)

**Situation:** {{EXAMPLE_3_SITUATION}}

**Emergency override requested:** {{EXAMPLE_3_OVERRIDE_REQUEST}}

**User decision:** {{EXAMPLE_3_USER_DECISION}}

**Outcome:** {{EXAMPLE_3_OUTCOME}}

{{ADDITIONAL_EXAMPLES}}

---

## Testing This Skill

### How to Test Discipline Skills

{{TESTING_PHILOSOPHY}}

### Pressure Scenarios

**Test with combined pressures:**
- {{PRESSURE_TYPE_1}} + {{PRESSURE_TYPE_2}} + {{PRESSURE_TYPE_3}}

**Example scenario:**

```
{{PRESSURE_SCENARIO_TEMPLATE}}
```

**Expected behavior:**
- {{EXPECTED_BEHAVIOR_1}}
- {{EXPECTED_BEHAVIOR_2}}
- {{EXPECTED_BEHAVIOR_3}}

**For comprehensive testing protocol, see:** `references/testing-protocol.md`

---

## How to Resist Shortcuts

### When Under Pressure

**If thinking about skipping workflow:**

1. **{{RESISTANCE_STEP_1}}**
2. **{{RESISTANCE_STEP_2}}**
3. **{{RESISTANCE_STEP_3}}**
4. **{{RESISTANCE_STEP_4}}**

### Common Pressure Types

| Pressure | Resistance Strategy |
|----------|---------------------|
| {{PRESSURE_1}} | {{STRATEGY_1}} |
| {{PRESSURE_2}} | {{STRATEGY_2}} |
| {{PRESSURE_3}} | {{STRATEGY_3}} |
| {{PRESSURE_4}} | {{STRATEGY_4}} |

### Commitment Mechanism

{{COMMITMENT_DESCRIPTION}}

**How to commit:**
```
{{COMMITMENT_TEMPLATE}}
```

---

## Meta: How This Skill Prevents Itself From Being Bypassed

### Rationalization-Proofing Techniques Used

This skill uses {{X}} techniques to prevent bypass:

1. **{{TECHNIQUE_1_NAME}}:** {{TECHNIQUE_1_DESCRIPTION}}
2. **{{TECHNIQUE_2_NAME}}:** {{TECHNIQUE_2_DESCRIPTION}}
3. **{{TECHNIQUE_3_NAME}}:** {{TECHNIQUE_3_DESCRIPTION}}
4. **{{TECHNIQUE_4_NAME}}:** {{TECHNIQUE_4_DESCRIPTION}}
5. **{{TECHNIQUE_5_NAME}}:** {{TECHNIQUE_5_DESCRIPTION}}

**Why these techniques work:**

{{META_RATIONALE}}

**For comprehensive rationalization-proofing guide, see:** `references/rationalization-proofing.md`

---

## Progressive Disclosure

**Supporting documents:**
- `references/{{REF_DOC_1}}.md` - {{REF_DOC_1_PURPOSE}}
- `references/{{REF_DOC_2}}.md` - {{REF_DOC_2_PURPOSE}}
- `references/{{REF_DOC_3}}.md` - {{REF_DOC_3_PURPOSE}}

**Related disciplines:**
- {{RELATED_DISCIPLINE_1}}
- {{RELATED_DISCIPLINE_2}}

**Further reading:**
- {{EXTERNAL_READING_1}}
- {{EXTERNAL_READING_2}}
```

---

## Placeholder Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{SKILL_NAME}}` | Kebab-case skill directory name | `enforcing-research-plan-implement-verify` |
| `{{CSO_OPTIMIZED_DESCRIPTION}}` | Description with trigger keywords, shortcuts symptoms, pressure scenarios (CSO ≥0.7) | "Use when about to implement features, fix bugs, change code, or refactor, before writing implementation code, when thinking 'this is simple enough to skip research', or when under time pressure" |
| `{{SKILL_TITLE}}` | Human-readable title | "Enforcing Research → Plan → Implement → Verify" |
| `{{ONE_SENTENCE_PURPOSE}}` | Concise purpose | "Prevent implementing code without research and approved plan" |
| `{{ENFORCEMENT_X}}` | What skill requires | "Research before implementation" |
| `{{NON_ENFORCEMENT_X}}` | What skill doesn't do | "Doesn't write code for you" |
| `{{RATIONALE_PARAGRAPH}}` | Why discipline important | "Financial systems require accuracy. Research prevents bugs that debugging can't catch." |
| `{{IRON_LAW_STATEMENT}}` | Absolute requirement (ALL CAPS) | `NO IMPLEMENTATION WITHOUT RESEARCH & APPROVED PLAN FIRST` |
| `{{IRON_LAW_EXPLANATION}}` | Why law is absolute | "Starting implementation without approved research.md and plan.md? STOP. Delete any code. Start with Research phase." |
| `{{EXCEPTION_ATTEMPT_X}}` | Predicted bypass attempt | "keep code as 'reference'" |
| `{{STOP_MEANS_STOP_STATEMENT}}` | Emphatic enforcement | "STOP means STOP. Research means NO CODE." |
| `{{RED_FLAG_THOUGHT_X}}` | Common rationalization | "I'll skip research, it's simple" |
| `{{REALITY_CHECK_X}}` | Truth statement | "Simple tasks break. Research takes 15 min, debugging takes hours." |
| `{{RED_FLAG_EMOTION_X}}` | Emotional warning sign | "Feeling time pressure" |
| `{{RED_FLAG_BEHAVIOR_X}}` | Behavioral warning sign | "Already wrote implementation code" |
| `{{RED_FLAG_PRESSURE_X}}` | External pressure | "Manager says fix it now" |
| `{{PHASE_X_NAME}}` | Workflow phase | "Research", "Plan", "Implement", "Verify" |
| `{{PHASE_X_PURPOSE}}` | Phase goal | "Investigate existing patterns without writing code" |
| `{{PHASE_X_ACTION_X}}` | Phase step | "Read existing files with Read tool" |
| `{{PHASE_X_DELIVERABLE}}` | Phase output | "`specs/{topic}/research.md` created" |
| `{{CHECKPOINT_X_REQUIREMENT}}` | Gate condition | "Present research findings to user for approval before planning" |
| `{{RATIONALIZATION_X}}` | Bypass excuse | "I already know how to do this" |
| `{{REALITY_X}}` | Truth about excuse | "Assumptions cause bugs. Research validates knowledge." |
| `{{COUNTER_X}}` | Counter-argument | "Knowledge changes. Codebase changes. Verify assumptions even when confident." |
| `{{CHECKPOINT_DEFINITION}}` | What checkpoints are | "Human-in-loop approval gate between phases" |
| `{{CHECKPOINT_ACTION_X}}` | Checkpoint step | "Present phase deliverable to user" |
| `{{APPROVAL_PHRASE_X}}` | Valid approval | "Approved", "Proceed", "Continue" |
| `{{NON_APPROVAL_ACTION}}` | What to do if rejected | "Revise deliverable based on feedback, re-present for approval" |
| `{{EMERGENCY_DEFINITION}}` | What qualifies as emergency | "Situation where workflow time exceeds business cost" |
| `{{EMERGENCY_EXAMPLE_X}}` | Legitimate emergency | "Production down, board meeting in 1 hour" |
| `{{EMERGENCY_EXPLANATION_TEMPLATE}}` | How to explain emergency | Template for emergency communication |
| `{{OPTION_X}}` | Emergency choice | "Follow full workflow (estimated time)", "Request emergency override" |
| `{{POST_EMERGENCY_DOC_X}}` | Retroactive documentation | "Create research.md documenting what was learned" |
| `{{EXAMPLE_X_SCENARIO}}` | Example context | "Google Sheets integration" |
| `{{EXAMPLE_X_REQUEST}}` | User's ask | "Add Google Sheets support" |
| `{{EXAMPLE_X_WITHOUT_SKILL}}` | Behavior without skill | "Starts implementing immediately, breaks authentication" |
| `{{EXAMPLE_X_WITH_SKILL}}` | Behavior with skill | "Research → Plan → Implement → Verify, successful integration" |
| `{{EXAMPLE_X_OUTCOME}}` | Result | "Working integration with proper error handling" |
| `{{TESTING_PHILOSOPHY}}` | How to validate discipline | "Use pressure scenarios with 3+ combined pressures" |
| `{{PRESSURE_TYPE_X}}` | Pressure category | "Time", "Authority", "Sunk Cost", "Exhaustion" |
| `{{PRESSURE_SCENARIO_TEMPLATE}}` | Test scenario format | Template for pressure testing |
| `{{EXPECTED_BEHAVIOR_X}}` | Correct response | "Follow workflow despite pressure" |
| `{{RESISTANCE_STEP_X}}` | How to resist shortcut | "STOP immediately", "Re-read Iron Law", "Identify which rationalization" |
| `{{PRESSURE_X}}` | Specific pressure | "Time pressure" |
| `{{STRATEGY_X}}` | How to resist | "Time pressure = highest error risk. Workflow prevents panic mistakes." |
| `{{COMMITMENT_DESCRIPTION}}` | Public declaration mechanism | "Announce using skill publicly before starting work" |
| `{{COMMITMENT_TEMPLATE}}` | Commitment format | "I'm using enforcing-research-plan-implement-verify. Starting Research phase for {topic}." |
| `{{TECHNIQUE_X_NAME}}` | Rationalization-proofing technique | "Explicit Negations", "Foundational Principles", "Iron Law" |
| `{{TECHNIQUE_X_DESCRIPTION}}` | How technique works | "State exact opposite of predicted bypass attempts" |
| `{{META_RATIONALE}}` | Why techniques effective | "Addresses psychological patterns that cause shortcuts" |
| `{{REF_DOC_X}}` | Supporting document | "checkpoint-examples", "complete-rationalization-table", "testing-protocol" |
| `{{REF_DOC_X_PURPOSE}}` | Document purpose | "Detailed checkpoint conversation examples" |
| `{{RELATED_DISCIPLINE_X}}` | Related skill | "test-driven-development", "code-review-discipline" |
| `{{EXTERNAL_READING_X}}` | Outside reference | "Atomic Habits by James Clear" |

---

## CSO Optimization Guidelines

**Discipline skills should include:**

1. **Shortcut symptom keywords** (red flags that indicate bypass attempt)
   - "thinking X", "feeling Y", "under Z pressure"
   - Example: "thinking 'this is simple'", "feeling time pressure", "under deadline"

2. **Trigger phrases** (when workflow applies)
   - "when X", "before Y", "about to Z"
   - Example: "when implementing", "before writing code", "about to fix bug"

3. **Violation keywords** (what behavior triggers enforcement)
   - "implementing without", "skipping", "bypassing"
   - Example: "implementing without research", "skipping plan"

4. **Pressure keywords** (combined pressures that tempt shortcuts)
   - "emergency", "urgent", "deadline", "manager says", "I already spent"
   - Example: "production emergency", "CFO needs it now", "already implemented"

**Target CSO score: ≥0.7** (measured by validate_cso.py)

**CRITICAL:** Discipline skills require highest CSO scores for auto-invocation before violations occur.

---

## Rationalization-Proofing Checklist

When using this template, apply 5 rationalization-proofing techniques:

### 1. Iron Law (Foundational Principle)
- [ ] Absolute statement in ALL CAPS code block
- [ ] Explains what to do when violated (DELETE code, start over)
- [ ] No wiggle room in language

### 2. Explicit Negations
- [ ] ≥6 "Don't X" statements under Iron Law
- [ ] Each negation addresses predicted bypass attempt
- [ ] Covers common loopholes ("reference", "while implementing", "after")

### 3. Rationalization Table
- [ ] ≥10 entries in main SKILL.md
- [ ] Each entry has Excuse | Reality | Counter-Argument
- [ ] References `complete-rationalization-table.md` for comprehensive list
- [ ] Table populated from baseline testing or proven patterns

### 4. Red Flags (Warning Signs)
- [ ] ≥8 red flags with Reality checks
- [ ] Covers thoughts, emotions, behaviors, external pressures
- [ ] Includes "If you notice ANY red flag: STOP" instruction

### 5. CSO for Violation Symptoms
- [ ] Description includes shortcut keywords
- [ ] Description includes pressure scenarios
- [ ] Description includes common rationalization phrases
- [ ] Triggers BEFORE violation occurs (not after)

**For comprehensive rationalization-proofing guide, see planned supporting document:** `references/rationalization-proofing.md`

---

## Validation Checklist

When using this template, validate:

- [ ] YAML frontmatter present with name + CSO-optimized description
- [ ] All 12 sections present (Overview → Iron Law → Red Flags → Workflow → Rationalization Table → Checkpoints → Emergency Override → Examples → Testing → Resistance → Meta → Progressive Disclosure)
- [ ] Iron Law in ALL CAPS code block with ≥6 explicit negations
- [ ] Red Flags has ≥8 entries with Reality checks
- [ ] The Workflow defines ≥3 phases with checkpoints
- [ ] Rationalization Table has ≥10 entries with Excuse | Reality | Counter-Argument
- [ ] Checkpoint Requirements defines protocol for user approval
- [ ] Emergency Override Protocol requires USER approval (not self-approved)
- [ ] Examples includes ≥3 scenarios (normal, red flags, emergency)
- [ ] Testing This Skill references pressure scenarios
- [ ] How to Resist Shortcuts provides concrete strategies
- [ ] Meta section explains rationalization-proofing techniques used
- [ ] Progressive Disclosure references ≥3 supporting docs in references/
- [ ] Line count <200 (main SKILL.md, details in references/)
- [ ] Active-voice naming
- [ ] CSO score ≥0.7

---

**Template Version:** 1.0
**Last Updated:** 2025-11-09
**Skill Type:** Discipline (workflow enforcement with rationalization-proofing)
**Complexity:** Highest (requires baseline testing or proven pattern adaptation)
