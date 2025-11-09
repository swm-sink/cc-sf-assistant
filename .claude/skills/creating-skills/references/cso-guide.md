# CSO Guide - Claude Search Optimization

**Purpose:** Comprehensive guide to optimizing skill descriptions for auto-invocation discoverability

**Target audience:** Skill creators who want Claude to automatically invoke their skills at the right time

**Key insight:** CSO is like SEO, but for AI agent search instead of web search

---

## Table of Contents

1. [What is CSO?](#what-is-cso)
2. [The 4 Pillars](#the-4-pillars)
3. [Description Formula](#description-formula)
4. [Keyword Richness](#keyword-richness)
5. [Examples](#examples)
6. [Testing CSO](#testing-cso)
7. [Common Mistakes](#common-mistakes)

---

## What is CSO?

**CSO (Claude Search Optimization)** is the practice of writing skill descriptions that maximize the likelihood of Claude auto-invoking the skill when appropriate.

### Why CSO Matters

**Problem:** Skills with poor descriptions never get invoked
- Claude can't find the skill when user needs it
- Skill exists but remains unused
- User misses out on valuable capability

**Solution:** CSO-optimized descriptions trigger at the right time
- Claude recognizes trigger scenarios
- Skill auto-invokes when needed
- User gets help proactively

### CSO vs Traditional Documentation

| Traditional Docs | CSO-Optimized |
|------------------|---------------|
| "This skill helps create new skills" | "Use when creating skills, building new capabilities, need templates, or want to generate skill scaffolding" |
| "Enforces workflow discipline" | "Use when about to implement features, fix bugs, change code, before writing implementation code, when thinking 'this is simple enough to skip research', or under time pressure" |
| "Analyzes budget variance" | "Use when comparing budget vs actual, analyzing variance, noticing unexpected expense, or need favorability analysis for financial reports" |

**Key difference:** CSO descriptions include **trigger scenarios**, **symptoms**, **keywords**, and **examples**.

---

## The 4 Pillars

CSO is built on 4 pillars. A well-optimized description includes all 4.

### Pillar 1: Trigger Phrases

**What:** Phrases that indicate WHEN to use the skill

**Keywords to include:**
- "when X"
- "before Y"
- "after Z"
- "use when"
- "need to"
- "want to"
- "about to"
- "during"
- "while"

**Examples:**
- ✅ "Use when creating skills..."
- ✅ "Use when about to implement..."
- ✅ "Use when comparing budget vs actual..."
- ❌ "This skill creates skills" (no trigger)

**Target:** ≥3 trigger phrases per description

### Pillar 2: Symptom Keywords

**What:** Observable signs that the skill is needed (thoughts, feelings, behaviors)

**Keywords to include:**
- "thinking X"
- "feeling Y"
- "noticing Z"
- "experiencing"
- "under pressure"
- "struggling"
- "finding difficult"
- "having trouble"
- "can't"
- "unable to"

**Examples:**
- ✅ "...when thinking 'this is simple enough to skip research'..."
- ✅ "...when noticing unexpected expense..."
- ✅ "...when under time pressure..."
- ❌ "Helps with implementation" (no symptom)

**Target:** ≥2 symptom keywords per description

### Pillar 3: Technology-Agnostic Keywords

**What:** Generic action verbs and domain concepts that apply broadly

**Keywords to include:**
- Generic actions: creating, building, implementing, enforcing, analyzing, validating, testing, reviewing
- Domain concepts: workflow, process, methodology, pattern, approach
- Transformations: calculating, transforming, integrating, orchestrating

**Examples:**
- ✅ "...creating skills..."
- ✅ "...enforcing workflow..."
- ✅ "...analyzing variance..."
- ❌ "Uses gspread library" (technology-specific)

**Target:** ≥3 agnostic keywords per description

**Why agnostic?** Skills remain discoverable even when technologies change.

### Pillar 4: Specific Examples

**What:** Concrete use cases that users will encounter

**Keywords to include:**
- Tool names: Google Sheets, Excel, Databricks, Adaptive
- Domain terms: variance, budget, forecast, revenue, expense
- Operations: integration, report, calculation, import, export
- File types: .xlsx, .csv, .json

**Examples:**
- ✅ "...variance analysis..."
- ✅ "...Google Sheets integration..."
- ✅ "...budget vs actual..."
- ❌ "Data analysis" (too generic)

**Target:** ≥2 specific examples per description

---

## Description Formula

**Template:**
```
Use when {TRIGGER_SCENARIO}, {SYMPTOM_KEYWORD}, or {SPECIFIC_EXAMPLE} - {ACTION} {TECHNOLOGY_AGNOSTIC_CONCEPT} {ADDITIONAL_TRIGGERS}
```

**Breakdown:**

1. **Start with "Use when"** (establishes trigger context)
2. **List 2-3 trigger scenarios** (when X, before Y, after Z)
3. **Include 1-2 symptoms** (thinking X, noticing Y, under Z pressure)
4. **Add specific examples** (Google Sheets, variance calculation)
5. **Describe action** (enforces, creates, analyzes)
6. **Mention generic concepts** (workflow, process, integration)

**Example (enforcing-research-plan-implement-verify):**
```
Use when about to implement features, fix bugs, change code, or refactor, before writing implementation code, when thinking "this is simple enough to skip research", or when under time pressure - enforces Research → Plan → Implement → Verify workflow with human checkpoints at each phase, prevents shortcuts and ensures quality
```

**Analysis:**
- ✅ Trigger phrases: "when about to", "before writing", "when thinking", "when under"
- ✅ Symptoms: "thinking 'this is simple enough to skip research'", "under time pressure"
- ✅ Agnostic keywords: "implement", "fix", "refactor", "workflow", "process", "enforces"
- ✅ Specific examples: "features", "bugs", "code"
- ✅ CSO score: 0.92 (excellent)

---

## Keyword Richness

**Keyword richness** = number of relevant keywords / total words

**Target:** ≥30% keyword richness

**How to calculate:**

1. Count trigger phrases (4)
2. Count symptom keywords (2)
3. Count agnostic keywords (6)
4. Count specific examples (3)
5. Total keywords: 15
6. Total words: 45
7. Richness: 15/45 = 33% ✅

**Tips for increasing richness:**

- Remove filler words ("basically", "essentially", "actually")
- Combine related concepts ("creating and building" → "creating")
- Use comma-separated lists ("when X, Y, or Z")
- Avoid redundant explanations

**Before (low richness):**
```
This skill is designed to help you when you're working on creating new skills for the system. It provides templates that make it easier.
```
- Keywords: 3 (creating, skills, templates)
- Words: 24
- Richness: 12.5% ❌

**After (high richness):**
```
Use when creating skills, building capabilities, need templates, want scaffolding, or generating new skill files - provides technique/pattern/discipline/reference templates with validation
```
- Keywords: 12 (creating, building, need, want, generating, templates, scaffolding, validation, technique, pattern, discipline, reference)
- Words: 24
- Richness: 50% ✅

---

## Examples

### Example 1: Technique Skill (creating-skills)

**Poor CSO (score: 0.3):**
```
This skill helps create new skills using templates.
```

**Good CSO (score: 0.7):**
```
Use when creating skills, building new capabilities, or need templates - provides technique/pattern/discipline/reference templates with validation and CSO optimization
```

**Excellent CSO (score: 0.9):**
```
Use when creating skills, building capabilities, need templates, want scaffolding, or generating new skill files, thinking "I need a starting point for a new skill", or planning to add technique/pattern/discipline/reference skills - provides specialized templates with validation, CSO optimization, and rationalization-proofing
```

**Analysis:**
- ✅ Triggers: "when creating", "need templates", "want scaffolding", "thinking"
- ✅ Symptoms: "thinking 'I need a starting point'"
- ✅ Agnostic: "creating", "building", "generating", "planning"
- ✅ Examples: "technique", "pattern", "discipline", "reference", "templates"

### Example 2: Discipline Skill (enforcing-research-plan-implement-verify)

**Poor CSO (score: 0.4):**
```
Enforces the research plan implement verify workflow.
```

**Good CSO (score: 0.7):**
```
Use when about to implement code, before writing features, or under time pressure - enforces Research Plan Implement Verify workflow with checkpoints
```

**Excellent CSO (score: 0.95):**
```
Use when about to implement features, fix bugs, change code, or refactor, before writing implementation code, when thinking "this is simple enough to skip research", or when under time pressure - enforces Research → Plan → Implement → Verify workflow with human checkpoints at each phase, prevents shortcuts and ensures quality
```

**Analysis:**
- ✅ Triggers: "when about to", "before writing", "when thinking", "when under"
- ✅ Symptoms: "thinking 'this is simple enough to skip research'", "under time pressure"
- ✅ Agnostic: "implement", "fix", "refactor", "workflow", "checkpoints", "enforces"
- ✅ Examples: "features", "bugs", "code"

### Example 3: Pattern Skill (adapter-pattern)

**Poor CSO (score: 0.3):**
```
Implements adapter pattern for external systems.
```

**Good CSO (score: 0.7):**
```
Use when integrating external APIs, need to swap implementations, or testing without live connections - provides adapter pattern for abstracting external dependencies
```

**Excellent CSO (score: 0.85):**
```
Use when integrating Google Sheets, Databricks, or external APIs, noticing tight coupling between business logic and external systems, need to swap implementations, or want to test without live API connections - provides adapter pattern with interface abstraction, mock implementations, and separation of concerns
```

**Analysis:**
- ✅ Triggers: "when integrating", "need to swap", "want to test"
- ✅ Symptoms: "noticing tight coupling"
- ✅ Agnostic: "integrating", "testing", "pattern", "abstraction", "separation"
- ✅ Examples: "Google Sheets", "Databricks", "external APIs"

### Example 4: Reference Skill (bash-commands)

**Poor CSO (score: 0.2):**
```
Reference for bash commands.
```

**Good CSO (score: 0.7):**
```
Use when searching for file operations, text processing, or system utilities - quick reference for common bash commands with examples
```

**Excellent CSO (score: 0.8):**
```
Use when searching files, processing text, managing processes, need grep syntax, find command options, or sed examples - quick reference for bash file operations, text processing, and system utilities with copy-paste examples
```

**Analysis:**
- ✅ Triggers: "when searching", "need syntax", "need options"
- ✅ Symptoms: (not applicable for reference skills)
- ✅ Agnostic: "searching", "processing", "managing", "reference"
- ✅ Examples: "grep", "find", "sed", "files", "text", "processes"

---

## Testing CSO

### How to Test

**Method 1: Validator Script**
```bash
python validate_cso.py .claude/skills/{skill-name}/SKILL.md
```

**Expected output:**
```
📊 CSO Score: 0.87 / 1.0 (target ≥0.7)
   ✅ Score meets target

🔍 Pillar Breakdown:
   • Trigger Phrases: 5 → 1.0
   • Symptom Keywords: 3 → 1.0
   • Agnostic Keywords: 4 → 1.0
   • Example Indicators: 2 → 0.67
```

**Method 2: Manual Testing**

1. Write description
2. Count each pillar category
3. Calculate scores:
   - Trigger score = min(count / 3, 1.0)
   - Symptom score = min(count / 2, 1.0)
   - Agnostic score = min(count / 3, 1.0)
   - Example score = min(count / 2, 1.0)
4. CSO score = average of 4 scores
5. Target: ≥0.7

**Method 3: Invocation Testing**

1. Create skill with description
2. Ask Claude scenarios that should trigger skill
3. Check if skill auto-invokes
4. If not, add missing keywords from scenario

**Example:**
- Scenario: "I need to create a new skill for X"
- Skill invoked? ✅ YES → CSO working
- Skill invoked? ❌ NO → Add "create" and "need" to description

---

## Common Mistakes

### Mistake 1: Too Generic

❌ **Bad:**
```
Use when working with skills.
```

**Why bad:** "working with" is vague. What exactly triggers it?

✅ **Good:**
```
Use when creating skills, editing skill templates, or validating skill structure.
```

**Fix:** Replace generic verbs with specific actions.

### Mistake 2: Too Technical

❌ **Bad:**
```
Use when instantiating GoogleSheetsClient class via gspread library.
```

**Why bad:** Too implementation-specific. Won't trigger if implementation changes.

✅ **Good:**
```
Use when integrating Google Sheets, importing budget data from spreadsheets, or need to read Excel files.
```

**Fix:** Focus on user intent, not technical details.

### Mistake 3: Missing Symptoms

❌ **Bad:**
```
Use when implementing features or fixing bugs.
```

**Why bad:** No symptom keywords. Misses "thinking" and "feeling" triggers.

✅ **Good:**
```
Use when implementing features, fixing bugs, thinking "this is simple", or under time pressure.
```

**Fix:** Add what user is thinking/feeling when they need the skill.

### Mistake 4: No Specific Examples

❌ **Bad:**
```
Use when analyzing financial data.
```

**Why bad:** Too broad. What kind of financial data?

✅ **Good:**
```
Use when analyzing variance, comparing budget vs actual, or calculating favorability for revenue and expense accounts.
```

**Fix:** Replace generic terms with concrete examples.

### Mistake 5: Keyword Stuffing

❌ **Bad:**
```
Use when creating creating skills skills building building new new capabilities capabilities templates templates validation validation CSO CSO optimization optimization...
```

**Why bad:** Unreadable. Repetition doesn't help.

✅ **Good:**
```
Use when creating skills, building capabilities, need templates, or want validation - provides CSO optimization and structure checking.
```

**Fix:** Each keyword should appear once. Focus on natural language.

### Mistake 6: Missing "Use when" Prefix

❌ **Bad:**
```
Creating skills with templates and validation.
```

**Why bad:** Not a trigger statement. Doesn't establish WHEN context.

✅ **Good:**
```
Use when creating skills with templates and validation.
```

**Fix:** Always start with "Use when" for trigger clarity.

---

## Quick Reference

**CSO Checklist:**

- [ ] Starts with "Use when" (establishes trigger context)
- [ ] ≥3 trigger phrases (when X, before Y, need to Z)
- [ ] ≥2 symptom keywords (thinking X, noticing Y, under Z pressure)
- [ ] ≥3 technology-agnostic keywords (creating, implementing, workflow)
- [ ] ≥2 specific examples (Google Sheets, variance, budget)
- [ ] Description length ≥50 characters
- [ ] Keyword richness ≥30%
- [ ] CSO score ≥0.7 (measured by validate_cso.py)
- [ ] Natural language (readable, not keyword-stuffed)

**CSO Formula:**
```
Use when {TRIGGER}, {SYMPTOM}, or {EXAMPLE} - {ACTION} {CONCEPT} {DETAILS}
```

**Target Score:**
- 0.7+ = Good (skill will auto-invoke reliably)
- 0.8+ = Excellent (skill triggers at perfect times)
- 0.9+ = Outstanding (covers all scenarios comprehensively)

---

**Last Updated:** 2025-11-09
**Related:** `rationalization-proofing.md`, `testing-protocol.md`
**Validator:** `scripts/validate_cso.py`
