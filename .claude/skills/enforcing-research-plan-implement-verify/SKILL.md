---
name: enforcing-research-plan-implement-verify
description: Use when about to implement features, fix bugs, change code, or refactor, before writing implementation code, when thinking "this is simple enough to skip research", or when under time pressure - enforces Research → Plan → Implement → Verify workflow with human checkpoints at each phase, prevents shortcuts and ensures quality
---

# Enforcing Research → Plan → Implement → Verify

## Overview

Follow Research → Plan → Implement → Verify workflow for all implementations. No exceptions.

**Core principle:** If you didn't research before implementing, you're guessing.

**Violating the letter of the rules is violating the spirit of the rules.**

**Why this exists:** CLAUDE.md documents the workflow. This skill enforces it.

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

## When to Activate

**BEFORE starting work on:**
- New features
- Bug fixes
- Refactoring
- Configuration changes (YAML, JSON, TOML)
- Logic changes (formulas, calculations, validation)
- New skills, commands, agents
- Integration work
- Architecture changes
- ANY code modifications (.py, .js, .ts, .sh, etc.)

**Warning signs you're about to violate:**
- Thinking "I'll skip research, it's simple"
- Thinking "I already know how to do this"
- Starting to write code without specs/{topic}/research.md
- Feeling time pressure ("fix it now")
- Authority override ("CFO says fix it immediately")
- Sunk cost ("I already spent 2 hours implementing")

**Exceptions (rare - when workflow NOT required):**
- Pure markdown typo fixes (NO code blocks, NO formulas)
- Comment-only typo fixes (NOT docstrings)
- Whitespace-only formatting (ZERO logic impact)
- Commit message corrections

**When in doubt, USE the workflow.**

## The 4-Phase Workflow

### Phase 1: RESEARCH (No Coding)
- Investigate WITHOUT writing code
- Read existing patterns, similar implementations
- Search external repos, documentation
- **Create:** `specs/{topic}/research.md`
- **CHECKPOINT 1:** Present research to user, get approval before planning

### Phase 2: PLAN (Specification)
- Create detailed specification based on research
- Document decisions, structure, validation approach
- Show examples of what will be created
- **Create:** `specs/{topic}/plan.md`
- **CHECKPOINT 2:** Present plan to user, get approval before implementation

### Phase 3: IMPLEMENT (With Progress Tracking)
- Execute task-by-task, track progress with TodoWrite
- Follow approved plan exactly
- Use atomic operations with rollback capability
- **Create:** Implementation artifacts in proper directories
- **CHECKPOINT 3:** Present implementation to user, get approval before verification

### Phase 4: VERIFY (Independent Validation)
- Run validation functions (syntax, types, tests)
- Test generated artifacts
- Present verification report
- **CHECKPOINT 4:** User gives final approval before completion

**See `.claude/templates/workflows/RESEARCH_PLAN_IMPLEMENT_VERIFY.md` for detailed workflow.**

## Required Artifacts

**Before proceeding to Implementation, these MUST exist:**

1. **specs/{topic}/research.md** - Research findings, approved at CHECKPOINT 1
2. **specs/{topic}/plan.md** - Implementation plan, approved at CHECKPOINT 2
3. **specs/{topic}/checklist.md** - Validation checklist (created during Plan phase)

**Topic naming:** kebab-case, descriptive (e.g., `enforcing-research-plan-implement-verify`)

**Status tracking:** Update checklist.md with ✅ 🔄 ⏳ ❌ as work progresses

**After approval:** Documents are READ-ONLY (create new version if major changes needed)

## Commitment & Announcement

**Before starting ANY implementation work, you MUST announce:**

"I'm using enforcing-research-plan-implement-verify. Starting Research phase for [topic]."

**Why:** Public declaration increases compliance (commitment principle).

**At each checkpoint:**
- "Research complete for [topic]. Awaiting CHECKPOINT 1 approval."
- "Plan complete for [topic]. Awaiting CHECKPOINT 2 approval."
- "Implementation complete for [topic]. Awaiting CHECKPOINT 3 approval."
- "Verification complete for [topic]. Awaiting CHECKPOINT 4 approval."

## Red Flags - STOP and Follow Workflow

If you catch yourself thinking:
- "I'll skip research, it's simple"
- "I'll write the plan after implementing"
- "This is just a quick fix"
- "I already know the pattern, no need to research"
- "Research is overkill for this"
- "I'll document research later"
- "Emergency situation, skip process"
- "CFO/Manager says fix it now, no time for research"
- "I already spent X hours implementing, documenting now is wasteful"
- "I'm following the spirit not the letter"
- "This is different because..."
- "One line change doesn't need research/plan"
- "Keep implementation as reference, document properly after"

**STOP. Start with Research phase. No exceptions.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll skip research, it's simple" | Simple tasks break. Research takes 15 min, debugging takes hours. |
| "I'll write plan after implementing" | Plan-after documents what you built, not what you should build. |
| "This is just a quick fix" | Quick fixes without research create technical debt. Follow workflow. |
| "I already know how to do this" | Assumptions cause bugs. Research validates knowledge. |
| "Research is overkill for this" | Overkill is deploying broken financial logic. For FP&A, accuracy > speed. |
| "I'll document research later" | Documentation-after forgets details. Document during research. |
| "Emergency situation, skip process" | Emergencies without research cause worse emergencies. Follow workflow. |
| "I already spent X hours implementing" | Sunk cost fallacy. Delete and start with research. Unverified code is technical debt. |
| "I'm following the spirit not letter" | Spirit = research before code. Letter = research before code. Same thing. |
| "Keep as reference, document properly" | You'll adapt it. That's implementation-first. Delete means delete. |
| "Manager/CFO says fix it now" | Authority doesn't override correctness. Get USER approval for emergency override. |
| "One line change is too small" | One line can break financial calculations. Size doesn't matter. |

**All of these mean: STOP. Start with Research phase.**

## Verification Checklist

**Before proceeding from Research to Plan:**
- [ ] `specs/{topic}/research.md` created
- [ ] Research findings documented with examples and references
- [ ] Presented to user at CHECKPOINT 1
- [ ] User explicitly approved

**Before proceeding from Plan to Implementation:**
- [ ] `specs/{topic}/plan.md` created
- [ ] Detailed specification with structure, decisions, validation
- [ ] Examples of what will be created included
- [ ] Presented to user at CHECKPOINT 2
- [ ] User explicitly approved

**Before proceeding from Implementation to Verification:**
- [ ] Implementation complete per approved plan
- [ ] Progress tracked with TodoWrite
- [ ] Atomic commits made
- [ ] Presented to user at CHECKPOINT 3
- [ ] User explicitly approved

**Before marking work complete:**
- [ ] Validation suite run
- [ ] Independent verification complete
- [ ] All quality gates pass
- [ ] Presented to user at CHECKPOINT 4
- [ ] User final approval received

**Can't check all boxes? Go back to last approved checkpoint.**

## Progressive Disclosure

**For detailed workflow:** `.claude/templates/workflows/RESEARCH_PLAN_IMPLEMENT_VERIFY.md`

**For checkpoint examples:** `references/checkpoint-examples.md`

**For complete rationalization catalog:** `references/complete-rationalization-table.md`

**For workflow definition:** `CLAUDE.md` lines 122-207

**For testing this skill:** `specs/enforcing-research-plan-implement-verify/pressure-scenarios.md`

## Integration with CLAUDE.md

**Division of responsibility:**
- **CLAUDE.md (lines 122-207):** Comprehensive documentation, philosophy, examples
- **This skill:** Active enforcement, auto-invocation, immediate intervention

**When activated:** This skill reminds you to follow CLAUDE.md workflow section.

**When NOT activated:** Pure documentation changes (markdown typos, comment fixes, whitespace).

## Final Rule

```
Implementation → specs/{topic}/research.md & plan.md exist and approved
Otherwise → not compliant with workflow
```

No exceptions without user's explicit permission for emergency override.

---

**Source:** Based on TDD skill patterns from external/superpowers/
**Last Updated:** 2025-11-09
