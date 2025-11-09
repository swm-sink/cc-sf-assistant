# Complete Rationalization Table

**Purpose:** Comprehensive catalog of rationalizations for skipping Research → Plan → Implement → Verify workflow, with reality checks and counter-arguments.

**Source:** Based on patterns from `external/superpowers/skills/test-driven-development/SKILL.md` and workflow enforcement research.

**Status:** Initial version (will be updated after baseline testing with actual observed rationalizations).

---

## Core Rationalizations

| Category | Excuse | Reality | Counter-Argument |
|----------|--------|---------|------------------|
| **Simplicity** | "I'll skip research, it's simple" | Simple tasks break. Research takes 15 min, debugging takes hours. | Complexity isn't predictable. "Simple" changes often have hidden dependencies. Research always required. |
| **Simplicity** | "One line change is too small for workflow" | One line can break financial calculations. Size doesn't matter. | Variance formula bug in one line = $M decisions wrong. Line count ≠ impact. |
| **Simplicity** | "Research is overkill for this" | Overkill is deploying broken financial logic. For FP&A, accuracy > speed. | FP&A systems require precision. No shortcuts. Financial errors destroy trust. |
| **Knowledge** | "I already know how to do this" | Assumptions cause bugs. Research validates knowledge. | Knowledge changes. Codebase changes. Verify assumptions even when confident. |
| **Knowledge** | "I'm the one who built this system" | Even authors forget details. Research documents current state. | Memory fades. Code evolves. Author assumptions become stale. |
| **Knowledge** | "Nothing to research, I already know the pattern" | Research ISN'T just learning. It's validating and discovering edge cases. | Research finds: edge cases you forgot, existing patterns to reuse, constraints you missed. |
| **Timing** | "I'll write plan after implementing" | Plan-after documents what you built, not what you should build. | Plan-first = design. Plan-after = documentation. Different purposes. Tests different things. |
| **Timing** | "I'll document research later" | Documentation-after forgets details. Document during research. | Memory fades. Context lost. Document findings immediately while fresh. |
| **Timing** | "Research and plan while implementing" | Can't research objectively when code already written. Biased by implementation. | Research requires open mind. Existing code biases toward adapting vs rethinking. |
| **Speed** | "This is just a quick fix" | Quick fixes without research create technical debt. Follow workflow. | "Quick" fix becomes permanent code. Treat seriously. Shortcuts compound. |
| **Speed** | "No time for 2-hour workflow" | Debugging production bugs takes longer than 2 hours. Prevention faster than cure. | Time spent in workflow < time spent debugging. Pragmatic = workflow. |
| **Speed** | "Workflow will slow me down" | Workflow faster than debugging. Research prevents wrong paths. | Going fast in wrong direction = slower. Workflow ensures right direction first. |
| **Emergency** | "Emergency situation, skip process" | Emergencies without research cause worse emergencies. Follow workflow. | Emergency fix breaking production = worse emergency. Research even under pressure. |
| **Emergency** | "Production is down, no time" | Broken fix extends downtime. Better: quick research, then fix correctly. | Downtime from wrong fix > downtime from research. Fix it right. |
| **Emergency** | "Board meeting in 1 hour, must deploy" | Deploying broken code to board = career risk. Request emergency override from USER. | Board seeing broken demo = worse than delay. User decides trade-off. |
| **Authority** | "Manager says fix it now, skip workflow" | Manager doesn't understand workflow. Explain, then request USER override. | Manager authority ≠ workflow exception. Only USER can approve override. |
| **Authority** | "CFO/VP says it's urgent" | CFO doesn't understand technical risk. Request USER override, explain trade-offs. | CFO sees business urgency, not code quality risk. User balances both. |
| **Authority** | "My boss will be upset if I take 2 hours" | Boss will be more upset if broken code reaches production. Explain workflow value. | Short-term boss happiness < long-term code quality. Educate boss on workflow. |
| **Sunk Cost** | "I already spent X hours implementing" | Sunk cost fallacy. Time already gone. Choice now: trusted code vs technical debt. | Past time is gone. Current choice: delete and verify, or keep unverified code. |
| **Sunk Cost** | "Deleting working code is wasteful" | Keeping unverified code is wasteful. Working ≠ correct. Research verifies correctness. | "Works on my machine" ≠ production-ready. Research finds edge cases manual testing missed. |
| **Sunk Cost** | "I manually tested all edge cases" | Manual testing is ad-hoc. Can't prove all edge cases covered. Tests aren't documented. | "I tested it" = unverifiable. Automated tests = reproducible. Manual testing forgets cases. |
| **Reference** | "Keep implementation as reference, document after" | You'll adapt reference code. That's implementation-first. Delete means delete. | Reference = temptation to adapt instead of research. Compromises workflow. Delete completely. |
| **Reference** | "Keep as reference, write tests first" | You'll look at it and adapt. That's testing after. Delete means delete. | Can't unsee code. Reference biases toward adapting. True TDD requires delete. |
| **Reference** | "I can research properly, just use as guide" | Existing code biases research toward justifying implementation. Not objective. | Research with implementation in mind = confirmation bias. Start fresh. |
| **Spirit vs Letter** | "I'm following the spirit not the letter" | Spirit = research before code. Letter = research before code. Same thing. | No daylight between spirit and letter in this workflow. Both require same sequence. |
| **Spirit vs Letter** | "Being pragmatic not dogmatic" | Workflow IS pragmatic. Prevents bugs. Dogmatic = skipping workflow "because I know better." | Pragmatic = preventing bugs via workflow. Shortcuts = hope. |
| **Spirit vs Letter** | "This case is different because..." | All implementations are different. All follow same workflow. No exceptions. | "Different" doesn't mean exempt. Workflow applies universally. |
| **Scope** | "Just exploring, not implementing" | Fine. Throw away exploration code. Start fresh with research after exploring. | Exploration ≠ implementation. Explore, learn, delete, then follow workflow. |
| **Scope** | "This is refactoring, not new code" | Refactoring changes behavior. Requires research (what are we preserving?) and plan. | Refactoring = behavior changes. Research existing behavior, plan preservation, verify. |
| **Scope** | "Just adding comments/docstrings" | Docstrings can contain business logic errors. If logic explanation, research business rules. | Docstrings documenting formulas = business logic. Research validates correctness. |
| **Process** | "Workflow is too heavyweight for small changes" | Small changes break production. Size doesn't determine risk. Follow workflow. | Small changes, large impact. Change size ≠ risk level. Workflow scales. |
| **Process** | "I'll follow workflow next time" | "Next time" never comes. Follow workflow now. Build habit. | Exceptions become rules. "Just this once" = always. Discipline requires consistency. |
| **Process** | "Let me just try this approach first" | Trying = implementing. If you write code, it's implementation. Research first. | "Trying" = writing code = implementation. Research before trying. |

---

## Advanced Rationalizations (Combination Pressures)

| Scenario | Excuse | Reality | Counter-Argument |
|----------|--------|---------|------------------|
| **Sunk Cost + Emergency** | "I already built it AND it's urgent, can't delete now" | Both pressures don't override workflow. Request emergency override from USER. | Multiple pressures don't create exceptions. USER decides trade-offs in emergencies. |
| **Authority + Time** | "Manager says now AND only 15 minutes left" | Manager + deadline don't override workflow. Explain to manager, request USER override. | Compounding pressures = request USER override. Don't self-approve. |
| **Knowledge + Simplicity** | "I know how AND it's simple, double reason to skip" | Confidence + simplicity = double reason TO research. Validates assumptions. | High confidence = highest risk of blind spots. Research catches overconfidence. |
| **Emergency + Pragmatic** | "Urgent AND one line, obviously skip research" | Most dangerous combination. One-line emergency fixes often break more. Request override. | "Obvious" fixes under pressure = highest error rate. USER decides. |

---

## Meta-Rationalizations (About the Workflow Itself)

| Excuse | Reality | Counter-Argument |
|--------|---------|------------------|
| "This workflow is too strict" | Strictness prevents financial calculation errors. For FP&A, strictness = correctness. | Loose workflow = production bugs. Strict workflow = trusted systems. |
| "Real engineers don't need this much process" | Real engineers prevent bugs via discipline. Workflow = professionalism. | Amateur hour = "I don't need process." Professional = disciplined workflow. |
| "This feels like micromanagement" | Workflow isn't micromanagement. It's quality assurance. Protects users and developers. | Micromanagement = controlling HOW. Workflow = ensuring quality. Different. |
| "I should be trusted to decide when workflow applies" | Trust isn't the issue. Consistency is. Workflow applies universally for reliability. | Trust = assuming competence. Workflow = ensuring consistency. Both needed. |
| "Workflow slows down innovation" | Innovation without validation = chaos. Workflow enables sustainable innovation. | Fast innovation that breaks = not innovation. Workflow enables sustainable pace. |

---

## Domain-Specific Rationalizations (FP&A)

| Excuse | Reality | Counter-Argument |
|--------|---------|------------------|
| "Finance users won't notice this bug" | Financial errors compound. Users may not notice until $M decisions affected. | Users notice when quarterly results don't reconcile. Too late then. |
| "This is just for internal analysis" | Internal analysis drives external decisions. Still requires accuracy. | "Internal only" analysis becomes board presentation. Treat seriously. |
| "Budget variance isn't mission-critical" | Budget variance drives resource allocation. $M decisions. Mission-critical. | CFO trusts variance report for headcount decisions. Mission-critical. |
| "It's just a threshold tweak" | Threshold changes affect which variances flagged. Material impact. Research needed. | Threshold = what CFO sees vs doesn't see. High impact. |
| "Finance formulas are simple math" | Finance formulas have business rules (favorability, materiality). Research validates rules. | (Revenue - Budget) simple. (Revenue - Budget) with favorability rules = complex. |

---

## Psychological Patterns

| Pattern | Manifestation | Counter-Strategy |
|---------|---------------|------------------|
| **Overconfidence** | "I already know" variations | Research validates knowledge. Confidence = time to double-check. |
| **Sunk Cost Fallacy** | "I already spent X hours" variations | Past time is gone. Current choice: quality vs speed. |
| **Authority Deference** | "Manager/CFO says" variations | Manager authority ≠ workflow exception. USER decides. |
| **Time Pressure** | "Urgent/emergency/deadline" variations | Time pressure = highest error risk. Workflow prevents panic mistakes. |
| **Scope Minimization** | "Just one line/simple/small" variations | Size ≠ impact. One line can break millions in decisions. |
| **Process Resistance** | "Too heavy/dogmatic/strict" variations | Discipline isn't dogma. Workflow = professionalism. |

---

## How to Use This Table

### During Implementation

**If you catch yourself thinking any excuse from table:**
1. STOP immediately
2. Identify which row matches your thought
3. Read "Reality" column
4. Read "Counter-Argument" column
5. Follow workflow anyway

### After Testing (RED-GREEN-REFACTOR)

**When new rationalizations observed:**
1. Add exact wording to table (verbatim from testing)
2. Analyze why rationalization emerged
3. Write reality check
4. Write counter-argument
5. Add to SKILL.md red flags if not already present

### For Meta-Analysis

**Patterns to watch:**
- Which rationalizations appear most frequently?
- Which pressures create strongest temptation?
- Which combinations are hardest to resist?
- Are there new categories emerging?

---

## Testing Notes

**This table will be updated after baseline testing with:**
- Actual rationalizations observed from subagent tests
- Exact wording from pressure scenario responses
- New categories that emerge
- Frequency counts (which excuses appear most)

**Current status:** Initial version based on TDD skill patterns from superpowers

**Next update:** After RED-GREEN-REFACTOR iterations complete

---

**Last Updated:** 2025-11-09
**Source:** Based on test-driven-development/SKILL.md rationalization patterns
**Status:** v1.0 (pre-testing baseline)
