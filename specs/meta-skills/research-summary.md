# Meta-Skills Research Summary - CHECKPOINT 1

**Date:** 2025-11-09
**Phase:** Research (1 of 4)
**Status:** Awaiting user approval to proceed to Plan phase

---

## Research Scope

Analyzed 5 external repositories for project-wide best practices:
1. **superpowers** (obra) - 20+ skills, comprehensive patterns
2. **12-factor-agents** (humanlayer) - Production agent principles
3. **advanced-context-engineering-for-coding-agents** (humanlayer) - Context management
4. **awesome-claude-code-subagents** (VoltAgent) - Subagent patterns
5. **awesome-claude-code** (hesreallyhim) - Community resources

**Focus:** Modularity, scalability, context management for long-term project success.

---

## Key Findings

### 1. File Organization at Scale (from superpowers/)

**Current approach (what we have):**
```
.claude/skills/variance-analyzer/
├── SKILL.md (everything inline)
├── scripts/ (empty - future)
├── references/ (empty - future)
└── assets/ (empty - future)
```

**Scalable approach (what we should adopt):**
```
.claude/skills/skill-name/
├── SKILL.md                    # Core patterns only (<200 lines)
├── scripts/                    # Executable tools
│   └── helper.py              # Reusable code, not narrative
├── references/                 # Heavy documentation (loaded on-demand)
│   ├── api-reference.md       # 600+ lines OK here
│   └── edge-cases.md          # Detailed scenarios
└── assets/                     # Templates, configs
    └── template.xlsx
```

**Rules from external/superpowers/skills/writing-skills/SKILL.md:**
- **Keep inline:** Principles, concepts, code patterns <50 lines
- **Separate files for:** Heavy reference (100+ lines), reusable tools
- **Token target:** Frequently-loaded skills <200 words, others <500 words
- **Cross-reference:** Don't duplicate, link to other skills

**Example:** `external/superpowers/skills/writing-skills/SKILL.md` is 622 lines because it's foundational and rarely updated. Most skills are <200 lines.

---

### 2. Template Specialization (Option B Structure)

**Current:** One generic template per type

**Proposed (from superpowers patterns):**
```
.claude/templates/
├── skills/
│   ├── SKILL_TEMPLATE.md              # Generic base
│   ├── technique-template.md          # How-to guides (condition-based-waiting)
│   ├── pattern-template.md            # Mental models (flatten-with-flags)
│   ├── reference-template.md          # API docs (heavy reference)
│   ├── discipline-template.md         # Workflow enforcement (TDD, verification)
│   └── supporting/
│       ├── graphviz-conventions.dot   # Flowchart standards
│       ├── persuasion-principles.md   # Rationalization theory
│       └── cso-guide.md               # Claude Search Optimization
├── commands/
│   ├── COMMAND_TEMPLATE.md            # Standard workflow
│   └── checkpoint-template.md         # With human-in-loop gates
└── agents/
    ├── AGENT_TEMPLATE.md              # Standard agent
    ├── reviewer-template.md           # Read-only reviewers
    └── executor-template.md           # Code-writing agents
```

**Why specialized templates:**
- Different skill types need different sections
- Technique skills: step-by-step instructions
- Pattern skills: before/after comparisons
- Discipline skills: rationalization-proofing, red flags list
- Reference skills: tables, quick lookup

**Context benefit:** Meta-skills can select appropriate template, generating optimized structure.

---

### 3. Claude Search Optimization (CSO)

**Pattern from external/superpowers/skills/writing-skills/SKILL.md lines 138-184:**

**YAML frontmatter:**
```yaml
name: kebab-case-only            # No parentheses, special chars
description: Use when [specific triggers/symptoms] - [what it does, third person]
```

**Description requirements:**
- **Start with "Use when..."** - focuses on triggering conditions
- **Include keywords:** Error messages, symptoms, tools, situations
- **Technology-agnostic triggers** unless skill is tech-specific
- **Third person:** Injected into system prompt
- **Max 500 characters** if possible

**Examples from superpowers:**

✅ **Good:**
```yaml
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently - replaces arbitrary timeouts with condition polling for reliable async tests
```

Keywords: "race conditions", "timing dependencies", "inconsistent", "timeouts", "async tests"

❌ **Bad:**
```yaml
description: For async testing
```

No triggers, no symptoms, no keywords.

**Impact on our project:**
- All 3 meta-skills must generate CSO-optimized descriptions
- Existing skills should be updated (variance-analyzer, financial-validator)
- CLAUDE.md should document CSO requirements

---

### 4. Active Voice Naming Convention

**Pattern from writing-skills lines 182-250:**

**Use gerunds (-ing) for processes:**
- ✅ `creating-skills` not `skill-creation`
- ✅ `testing-skills-with-subagents` not `subagent-skill-testing`
- ✅ `writing-plans` not `plan-writing`

**Use verb-first for actions:**
- ✅ `condition-based-waiting` (what you DO)
- ✅ `root-cause-tracing` (the ACTION)
- ✅ `flatten-with-flags` (core INSIGHT)

**Analysis of superpowers/ skills:**
- `brainstorming/` - gerund
- `commands/` - plural noun (category)
- `condition-based-waiting/` - verb-first technique
- `executing-plans/` - gerund
- `requesting-code-review/` - gerund
- `using-git-worktrees/` - gerund
- `writing-skills/` - gerund

**Our current naming:**
- `variance-analyzer` - noun-based ❌
- Should be: `analyzing-variance` ✅

**Decision needed:** Rename existing or only apply to new artifacts?

---

### 5. TDD for Skills (Testing Protocol)

**From external/superpowers/skills/writing-skills/SKILL.md lines 340-528:**

**Core principle:** "Writing skills IS Test-Driven Development applied to process documentation."

**RED-GREEN-REFACTOR cycle for skills:**

**RED Phase - Write Failing Test (Baseline):**
1. Create pressure scenarios (3+ combined pressures for discipline skills)
2. Run scenarios WITHOUT the skill
3. Document baseline behavior verbatim (what rationalizations did agent use?)
4. Identify patterns in failures

**GREEN Phase - Write Minimal Skill:**
1. Write skill addressing specific baseline failures
2. Run same scenarios WITH skill
3. Verify agents now comply

**REFACTOR Phase - Close Loopholes:**
1. Identify NEW rationalizations from testing
2. Add explicit counters
3. Build rationalization table
4. Create red flags list
5. Re-test until bulletproof

**Testing different skill types:**

| Skill Type | Test Approach | Success Criteria |
|------------|---------------|------------------|
| **Discipline** (TDD, verification) | Pressure scenarios, academic questions | Agent follows rule under maximum pressure |
| **Technique** (how-to) | Application scenarios, edge cases | Agent applies technique to new scenario |
| **Pattern** (mental models) | Recognition scenarios, counter-examples | Agent knows when/how to apply |
| **Reference** (API docs) | Retrieval scenarios, gap testing | Agent finds and correctly applies info |

**Iron Law:** "NO SKILL WITHOUT A FAILING TEST FIRST"

**Application to our project:**
- First skill we create: `enforcing-research-plan-implement-verify` (discipline skill)
- Must test with subagents before deploying
- Document rationalizations: "I'll skip research, it's simple", "Plan is overkill"
- Build rationalization table
- Add red flags list

---

### 6. Rationalization-Proofing

**From writing-skills lines 426-498:**

**Purpose:** Make discipline-enforcing skills bulletproof against shortcuts.

**Techniques:**

**A. Close Every Loophole Explicitly**

❌ Bad:
```markdown
Write code before test? Delete it.
```

✅ Good:
```markdown
Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```

**B. Address "Spirit vs Letter" Arguments**

Add early:
```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

**C. Build Rationalization Table**

```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
```

**D. Create Red Flags List**

```markdown
## Red Flags - STOP and Start Over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**
```

**E. Update CSO for Violation Symptoms**

Add to description:
```yaml
description: use when implementing any feature or bugfix, before writing implementation code
```

**Application to CLAUDE.md:**
- Research → Plan → Implement → Verify is discipline-enforcing
- Need rationalization-proofing for:
  - "I'll skip research, it's simple"
  - "I'll write plan after implementing"
  - "This is just a quick fix"
  - "I'll add research docs later"

**Example red flags list for CLAUDE.md:**
```markdown
## Red Flags - STOP and Follow Workflow

- Starting implementation without research
- Writing code before approved plan
- "I'll document this later"
- "It's just a small change"
- "Research is overkill for this"

**All of these mean: STOP. Start with Research phase.**
```

---

### 7. Context Management (from 12-factor-agents & ace-fca)

**Key principles:**

**A. Frequent Intentional Compaction (ace-fca.md)**
- Keep context utilization at 40-60%
- Distill progress into structured artifacts
- Specs are source of truth (not chat history)

**B. Factor 3: Own Your Context Window (12-factor-agents)**
- Context window contents = ONLY lever for output quality
- What eats context: searching files, code flow, test logs, errors
- Solution: Compact into structured artifacts

**C. Factor 9: Compact Errors into Context Window**
- Don't paste full stack traces
- Extract: error type, location, relevant context only
- Pattern: error summary table

**D. Factor 12: Stateless Reducer**
- Each turn is a stateless function call
- Context window in → next step out
- All state must be in context or external DB

**Application to our workflow:**
- Research phase → research.md (compaction)
- Plan phase → plan.md (compaction)
- Checklist.md → progress tracker (state)
- CLAUDE.md → behavioral rules (stateless configuration)

**Already aligned:** Our specs/{topic}/ structure IS intentional compaction!

---

### 8. Token Efficiency (from writing-skills lines 186-240)

**Target word counts:**
- **getting-started workflows:** <150 words each
- **Frequently-loaded skills:** <200 words total
- **Other skills:** <500 words (still be concise)

**Techniques:**

**A. Move details to tool help:**
```bash
# ❌ BAD: Document all flags in SKILL.md
search-conversations supports --text, --both, --after DATE, --before DATE, --limit N

# ✅ GOOD: Reference --help
search-conversations supports multiple modes and filters. Run --help for details.
```

**B. Use cross-references:**
```markdown
# ❌ BAD: Repeat workflow details
When searching, dispatch subagent with template...
[20 lines of repeated instructions]

# ✅ GOOD: Reference other skill
Always use subagents (50-100x context savings). REQUIRED: Use [other-skill-name] for workflow.
```

**C. Compress examples:**
```markdown
# ❌ BAD: Verbose example (42 words)
your human partner: "How did we handle authentication errors in React Router before?"
You: I'll search past conversations for React Router authentication patterns.
[Dispatch subagent with search query: "React Router authentication error handling 401"]

# ✅ GOOD: Minimal example (20 words)
Partner: "How did we handle auth errors in React Router?"
You: Searching...
[Dispatch subagent → synthesis]
```

**D. Eliminate redundancy:**
- Don't repeat what's in cross-referenced skills
- Don't explain what's obvious from command
- Don't include multiple examples of same pattern

**Application to our meta-skills:**
- Generate concise skills by default
- Warn if SKILL.md >500 words
- Prompt user: "Move to references/?" if >200 lines
- Cross-reference validation scripts (don't inline all code)

---

### 9. Flowchart Usage (from writing-skills lines 263-289)

**When to use flowcharts:**
- ✅ Non-obvious decision points
- ✅ Process loops where you might stop too early
- ✅ "When to use A vs B" decisions

**Never use flowcharts for:**
- ❌ Reference material → Tables, lists
- ❌ Code examples → Markdown blocks
- ❌ Linear instructions → Numbered lists
- ❌ Labels without semantic meaning (step1, helper2)

**Graphviz conventions (referenced in writing-skills):**
- Diamond shapes for decisions
- Box shapes for actions
- Semantic labels (not generic step1/step2)

**Application:**
- Use sparingly in meta-skills
- Only for workflow decisions (e.g., "When to create subdirectory?")
- Add graphviz-conventions.dot to templates/supporting/

---

### 10. File Organization Patterns at Scale

**Analysis of superpowers/ skills directory (20+ skills):**

**Self-contained skills (no supporting files):**
```
defense-in-depth/
  SKILL.md (everything inline, <200 lines)
```
**When:** All content fits, no heavy reference needed

**Skills with reusable tools:**
```
condition-based-waiting/
  SKILL.md          # Overview + patterns
  example.ts        # Working helpers to adapt
```
**When:** Tool is reusable code, not just narrative

**Skills with heavy reference:**
```
testing-skills-with-subagents/
  SKILL.md               # Overview + workflow (<200 lines)
  subdir/
    pressure-testing.md  # Detailed techniques
    examples.md          # Many examples
```
**When:** Reference material too large for inline

**Cross-referencing syntax (from superpowers):**

✅ **Good:**
```markdown
**REQUIRED SUB-SKILL:** Use superpowers:test-driven-development
**REQUIRED BACKGROUND:** You MUST understand superpowers:systematic-debugging
```

❌ **Bad:**
```markdown
See skills/testing/test-driven-development  # Unclear if required
@skills/testing/test-driven-development/SKILL.md  # Force-loads, burns context
```

**Why no @ links:** @ syntax force-loads files immediately, consuming 200k+ context before needed.

**Application to our project:**
- Most skills should be self-contained (<200 lines)
- financial-validator might need references/ for edge cases
- Meta-skills need scripts/ for validation functions
- Use "REQUIRED:" prefix for cross-references

---

## Critical Decisions for Plan Phase

### 1. First Skill to Create

**Recommendation:** `enforcing-research-plan-implement-verify` (discipline skill)

**Why first:**
- Enforces workflow for ALL subsequent work
- Meta-skills themselves will use this workflow
- Prevents shortcuts during high-pressure implementation
- Sets quality standard

**Structure:**
```
.claude/skills/enforcing-research-plan-implement-verify/
├── SKILL.md
│   ├── When to Activate: "before implementing", "starting to code"
│   ├── 4-Phase Workflow documentation
│   ├── Rationalization table
│   ├── Red flags list
│   └── Checkpoint requirements
└── references/
    └── checkpoint-examples.md  # Detailed checkpoint patterns
```

**Must test with subagent BEFORE deploying** (TDD for skills).

---

### 2. Meta-Skills Architecture

**Proposed structure:**
```
.claude/skills/creating-skills/          # Renamed from skill-creator
├── SKILL.md                             # <200 lines, core workflow
├── scripts/
│   ├── validate_yaml.py
│   ├── validate_naming.py
│   ├── validate_structure.py
│   ├── generate_skill.py
│   └── atomic_file_ops.py
├── references/
│   ├── cso-guide.md                     # CSO patterns detailed
│   ├── testing-protocol.md             # TDD for skills process
│   └── rationalization-proofing.md     # How to bulletproof
└── assets/
    └── skill-templates/                 # Specialized templates
        ├── technique-template.md
        ├── pattern-template.md
        ├── reference-template.md
        └── discipline-template.md

.claude/skills/creating-commands/        # Renamed from command-creator
├── SKILL.md
├── scripts/
│   └── validate_command.py
└── assets/
    └── command-templates/
        ├── standard-template.md
        └── checkpoint-template.md

.claude/skills/creating-agents/          # Renamed from agent-creator
├── SKILL.md
├── scripts/
│   └── validate_agent.py
└── assets/
    └── agent-templates/
        ├── reviewer-template.md
        └── executor-template.md
```

**Key changes from original plan:**
- **Active-voice naming:** creating-skills, creating-commands, creating-agents
- **Template assets:** Specialized templates IN the skill (not global templates/)
- **Modular scripts:** Each validation function separate
- **Progressive disclosure:** Heavy docs in references/

---

### 3. Template Migration Strategy

**Option B (approved by user):**

**Phase 1:** Create specialized templates in meta-skills assets/
- Meta-skills use their own bundled templates
- Existing .claude/templates/ stays for backward compatibility

**Phase 2:** Deprecate .claude/templates/ after all meta-skills working
- Move to .claude/templates/archive/
- Update docs to reference meta-skills instead

**Why phased:**
- De-risk migration
- Test specialized templates in production first
- Easy rollback if issues

---

### 4. CLAUDE.md Enhancements

**Add sections:**

**A. Claude Search Optimization (CSO)**
```markdown
## Claude Search Optimization (CSO)

**All skills/commands/agents must have CSO-optimized descriptions:**

Format: `Use when [specific triggers/symptoms] - [what it does, third person]`

Keywords to include:
- Error messages that trigger this
- Symptoms that indicate need
- Tools/commands involved
- Situations where applicable

Example:
```yaml
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently - replaces arbitrary timeouts with condition polling for reliable async tests
```
\`\`\`

**B. Rationalization-Proofing for Research → Plan → Implement → Verify**

```markdown
## Red Flags - STOP and Follow Workflow

If you catch yourself thinking:
- "I'll skip research, it's simple"
- "I'll write the plan after implementing"
- "This is just a quick fix"
- "I'll document this later"
- "Research is overkill for this"
- "I already know the pattern"

**STOP. Start with Research phase. No exceptions.**

Violating the letter of the workflow IS violating the spirit of the workflow.
```

**C. Token Efficiency Guidelines**

```markdown
## Token Efficiency

**Target word counts:**
- Frequently-loaded skills: <200 words
- Other skills: <500 words
- Heavy reference: Move to references/ subdirectory

**Techniques:**
- Cross-reference other skills (don't duplicate)
- Move API docs to references/
- Compress examples
- Eliminate redundancy
```

---

### 5. Existing Artifact Updates

**Breaking changes allowed** - update existing skills:

**variance-analyzer:**
- Rename to `analyzing-variance`? (Active voice)
- Update description to CSO format
- Current description OK, just enhance with keywords

**financial-validator:**
- Description already decent
- Add CSO keywords: "Decimal precision", "float detection", "rounding errors"

**sync-docs:**
- Command is fine (active voice already: "sync")
- Enhance description with triggers

**code-reviewer:**
- Agent name OK
- Enhance description

---

## Recommendations for Plan Phase

### Priority Order

1. **enforcing-research-plan-implement-verify** (discipline skill)
   - Test with subagents BEFORE deploying
   - Build rationalization table
   - Add to CLAUDE.md red flags

2. **creating-skills** (meta-skill)
   - With specialized template assets
   - CSO generation
   - TDD testing protocol
   - Iteration workflow

3. **creating-commands** (meta-skill)
   - With checkpoint templates
   - CSO generation

4. **creating-agents** (meta-skill)
   - With reviewer/executor templates
   - Tool permissions security

5. **CLAUDE.md enhancements**
   - CSO section
   - Rationalization-proofing
   - Token efficiency guidelines

6. **Existing artifact updates** (optional Phase 2)
   - Rename to active voice
   - Enhance CSO descriptions

---

## Success Metrics

**Modularity:**
- ✅ Most skills <200 lines (core content)
- ✅ Heavy reference in separate files
- ✅ Clear cross-reference syntax
- ✅ No duplication across skills

**Scalability:**
- ✅ Specialized templates for different skill types
- ✅ Pattern works for 5 skills or 500 skills
- ✅ Easy to find and load relevant skills

**Context Management:**
- ✅ Token targets met (<200 words frequently-loaded)
- ✅ Progressive disclosure (load on-demand)
- ✅ Intentional compaction (specs/ structure)

**Quality:**
- ✅ CSO-optimized descriptions (Claude finds skills)
- ✅ TDD for skills (tested before deploying)
- ✅ Rationalization-proofed (bulletproof workflows)
- ✅ Active-voice naming (clear, consistent)

---

## Open Questions for User

### Naming Convention

**Current:** `variance-analyzer`, `financial-validator`

**Proposed:** `analyzing-variance`, `validating-financial-data`

**Question:** Rename existing skills to active voice, or only apply to new skills?

**Recommendation:** Rename for consistency. Breaking changes allowed per user.

### Template Location

**Option A:** Templates in meta-skills assets/
```
.claude/skills/creating-skills/assets/skill-templates/
```

**Option B:** Templates in centralized location
```
.claude/templates/skills/specialized/
```

**Recommendation:** Option A (bundled with meta-skill). More modular, easier to version with skill.

### Research Documentation

**Full research.md will include:**
- Detailed analysis of all 20+ superpowers skills
- Complete 12-factor-agents patterns
- ace-fca.md full context management techniques
- Line-by-line template comparisons
- Complete CSO keyword catalog
- Rationalization pattern catalog from writing-skills
- File organization decision tree
- Cross-referencing best practices

**Estimated:** 2000-3000 lines

**Question:** Proceed with full research.md creation now, or wait until after plan approval?

**Recommendation:** Create full research.md now (good reference during planning). Mark as READ-ONLY after CHECKPOINT 1 approval.

---

## Next Steps (Pending CHECKPOINT 1 Approval)

**If approved:**

1. ✅ Create full research.md (2000+ lines comprehensive analysis)
2. ✅ Mark research.md as READ-ONLY
3. → Proceed to PLAN phase (create detailed plan.md)
4. → Present plan at CHECKPOINT 2
5. → Get approval before implementation

**If changes requested:**
- Revise research approach
- Re-analyze specific repos
- Adjust recommendations
- Re-present at CHECKPOINT 1

---

## CHECKPOINT 1: User Approval Required

**Questions for user:**

1. **Approve overall research approach?** (Modularity, scalability, context management focus)

2. **Approve first skill priority?** (enforcing-research-plan-implement-verify before meta-skills)

3. **Approve active-voice naming?** (Rename existing skills or new only?)

4. **Approve template location?** (Bundled in meta-skills assets/ or centralized?)

5. **Proceed to full research.md creation?** (2000+ line detailed analysis)

**Awaiting user decision to proceed to Plan phase.**

---

**Research Sources:**
- external/superpowers/ (20+ skills, 622-line writing-skills)
- external/12-factor-agents/ (12 factors, workshops)
- external/advanced-context-engineering-for-coding-agents/ (ace-fca.md)
- external/awesome-claude-code-subagents/
- external/awesome-claude-code/

**Last Updated:** 2025-11-09
**Phase:** Research (1 of 4)
**Next Phase:** Plan (awaiting CHECKPOINT 1 approval)
