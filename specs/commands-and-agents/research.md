# Slash Commands & Agents Research

**Date:** 2025-11-09  
**Status:** Complete  
**Scope:** Medium-level exploration of command/agent patterns in existing codebase

---

## PART 1: SLASH COMMANDS STRUCTURE

### Location & Organization

**Directory Structure:**
```
.claude/commands/
├── shared/
│   └── sync-docs.md                    # /shared:sync-docs
├── prod/
│   └── variance-analysis.md            # /prod:variance-analysis
└── dev/
    └── (empty - no dev commands yet)
```

**Naming Convention:**
- Format: `/environment:command-name` (kebab-case, lowercase)
- Environment prefixes: `shared`, `prod`, `dev`
- File naming: `command-name.md` (kebab-case)
- Command invoked as: `/prod:variance-analysis` (using colon separator)

---

### Command File Structure

**YAML Frontmatter (REQUIRED per official docs):**
```yaml
---
description: Brief description of what the command does  # REQUIRED, max 1024 chars, shown in /help
model: claude-3-5-sonnet-20241022  # Optional: specific model or sonnet/opus/haiku
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]  # Optional: restrict tools available
argument-hint: [file-path]  # Optional: hint about expected arguments shown in menu
disable-model-invocation: false  # Optional: prevent auto-invocation (default: false)
---
```

**Official Field Specifications (from docs.claude.com/claude-code/slash-commands):**

1. **`description`** (REQUIRED)
   - Brief description of what the command does
   - Shows up in `/help` menu for discoverability
   - Max 1024 characters
   - Should explain both WHAT the command does and WHEN to use it

2. **`allowed-tools`** (Optional)
   - List of tools the command can use
   - Examples: `Read, Grep, Glob, Bash, Edit, Write`
   - Use for security (e.g., read-only commands: `[Read, Grep, Glob]`)

3. **`model`** (Optional)
   - Force command to use specific model
   - Examples: `claude-3-5-sonnet-20241022`, `sonnet`, `opus`, `haiku`
   - Defaults to user's current model selection if not specified

4. **`argument-hint`** (Optional)
   - Hint about expected arguments
   - Format: `[arg1] [arg2]` or `<required-arg> [optional-arg]`
   - Examples: `[issue-number] [priority]`, `<budget-file> <actual-file> [output-file]`

5. **`disable-model-invocation`** (Optional)
   - Boolean: `true` or `false`
   - When `true`, prevents auto-invocation (must be manually called)
   - Default: `false` (allows auto-invocation)

**Source:** Anthropic official documentation (docs.claude.com/en/docs/claude-code/slash-commands, 2025)

**Content Sections (Based on variance-analysis.md analysis):**

1. **Header & Usage**
   - `# Command Title`
   - **Usage:** Syntax with arguments (e.g., `/variance-analysis <budget_file> <actual_file> [output_file]`)
   - **Purpose:** 1-2 sentence explanation of what the command does

2. **Workflow Steps** (Human-in-Loop)
   - Research Phase (STEP 1) - Investigate WITHOUT implementing
   - Plan Phase (STEP 2) - Create specification WITHOUT implementing
   - Implement Phase (STEP 3) - Execute task-by-task with progress tracker
   - Verify Phase (STEP 4) - Independent verification before delivery
   - Each phase has explicit CHECKPOINT with human approval

3. **Expected Behaviors**
   - Success criteria (checklist format)
   - Example invocation
   - Expected flow/output
   - Anti-patterns to avoid

4. **Integration Points**
   - References to other systems (@code-reviewer subagent invocation)
   - Financial validator skill usage
   - Output file specifications

---

### Example: /prod:variance-analysis Command

**Key Features:**
- Follows Research → Plan → Implement → Verify workflow with 4 checkpoints
- Uses financial-validator skill for data validation
- Invokes @code-reviewer subagent for independent verification
- Decimal precision enforcement throughout
- Audit trail metadata inclusion
- Human approval gates at each phase boundary
- Favorability logic by account type (revenue, expense, asset, liability)
- Edge case handling (zero budget, negative values)
- Output specification (3-sheet Excel file with formatting)

**Unique to Commands:**
- Arguments passed via $1, $2, $3 syntax (positional parameters)
- Optional arguments supported (e.g., [output_file])
- Clear workflow steps designed for human execution
- Success criteria presented as actionable checklist

---

### Example: /shared:sync-docs Command

**Key Features:**
- Documentation validation and consistency checking
- 10 separate validation checks (version numbers, directories, templates, etc.)
- Structured report output format
- Warnings vs. critical issues distinction
- Can accommodate expected issues based on project phase
- Non-destructive (read-only validation)

**Design Pattern:**
- Systematic checklist approach (10 specific checks)
- Clear pass/fail/warning indicators (✅ ⚠️ ❌)
- Detailed report generation
- Distinguishes critical issues from acceptable warnings

---

## PART 2: AGENTS STRUCTURE

### Location & Organization

**Directory Structure:**
```
.claude/agents/
├── code-reviewer.md                     # Available agent
├── shared/
│   └── (empty)
├── prod/
│   └── (empty)
└── dev/
    └── (empty)
```

**Naming Convention:**
- File naming: `agent-purpose.md` (kebab-case, descriptive)
- Invocation: `@agent-name` (using @ prefix in conversation)
- No environment prefix (agents are global, not environment-specific)
- Single global agents directory (not split by env like commands)

---

### Agent File Structure

**YAML Frontmatter (Required):**
```yaml
---
name: code-reviewer  # Short identifier for invocation (@code-reviewer)
description: Brief description of when this agent should be invoked  # 100-150 chars
tools: [Read, Grep, Glob]  # Minimal tool list - read-only for reviewers
model: sonnet  # Optional: sonnet, opus, haiku, or inherit
---
```

**Content Sections (Based on code-reviewer.md analysis):**

1. **Role Definition**
   - `# Agent Name` - Title
   - **Purpose:** Concise statement of agent's job
   - **Mindset:** Critical approach/philosophy (e.g., "skeptical senior engineer")

2. **Capabilities**
   - Bulleted list of specific capabilities
   - Example: "Financial calculation validation, edge case verification, precision checking"

3. **Constraints**
   - Tool restrictions (read-only, no editing)
   - Focus boundaries (specific domain)
   - Authority limits (can review, cannot approve)

4. **Review/Analysis Mandate**
   - Checklist of specific things to verify
   - Detailed search patterns (grep examples for finding violations)
   - Rejection criteria (hard stops that block approval)

5. **Output Format**
   - Structured feedback template
   - CRITICAL ISSUES, WARNINGS, SUGGESTIONS sections
   - Verification results checklist
   - RECOMMENDATION: APPROVE/REJECT/NEEDS REVISION

6. **Example Output**
   - Real example of how agent output should look
   - Shows proper formatting and depth

---

### Example: @code-reviewer Agent

**Key Features:**
- Read-only tools: Read, Grep, Glob (cannot modify code)
- Financial-focused review mandate
- 7-point verification checklist:
  1. Decimal Precision (CRITICAL)
  2. Division by Zero Handling
  3. Edge Case Coverage
  4. Type Hints & Documentation
  5. Favorability Logic
  6. Audit Trail Compliance
  7. Error Handling
- Explicit rejection criteria for each check (hard stops)
- Skeptical reviewer mindset ("assume code has bugs until proven otherwise")
- Structured output with critical/warning/suggestion tiers
- Final recommendation with rationale and estimated fix time

---

## PART 3: COMMAND vs AGENT COMPARISON

| Aspect | Slash Commands | Agents (Subagents) |
|--------|----------------|--------------------|
| **Invocation** | `/namespace:command-name` | `@agent-name` |
| **Directory** | `.claude/commands/{env}/` | `.claude/agents/` (global, not split by env) |
| **File Naming** | `kebab-case.md` | `kebab-case.md` |
| **YAML Required** | Optional (description only) | Required (name, description, tools, model) |
| **Environment Split** | YES - dev/prod/shared | NO - global agents only |
| **Arguments** | YES - $1, $2, $3 positional | NO - via conversation |
| **Tools Restriction** | Optional (allowed-tools field) | Standard (tools field) |
| **Primary Use** | User-initiated workflows | Invoked from commands/workflows or directly |
| **Workflow Pattern** | Research → Plan → Implement → Verify | Specialized review/analysis task |
| **Checkpoints** | Multiple (4-step RPIV pattern) | Single execution (review, analysis, recommendation) |
| **Output Expectation** | Structured report with progress | Detailed review feedback with recommendation |
| **Human Involvement** | High (checkpoints at each phase) | Mid (calls for approval in main command) |
| **Typical Duration** | Multi-step (hours of work) | Single session (focused analysis) |

---

## PART 4: PATTERNS & BEST PRACTICES

### Command Patterns Observed

**Pattern 1: Research → Plan → Implement → Verify (RPIV)**
- Used in: `/prod:variance-analysis`
- Characteristics:
  - Phase 1: Investigate data WITHOUT implementing
  - Phase 2: Create specification WITHOUT implementing
  - Phase 3: Execute with task-by-task progress tracker
  - Phase 4: Independent verification before delivery
  - Human checkpoint after each phase
  - Success criteria as checklist

**Pattern 2: Systematic Validation Checks**
- Used in: `/shared:sync-docs`
- Characteristics:
  - Numbered checklist of validation checks (10 checks)
  - Each check has specific action/verification step
  - Results formatted as ✅/⚠️/❌
  - Distinguishes critical from acceptable issues
  - Generates structured report

**Pattern 3: Common Features Across Commands**
- YAML frontmatter with description (auto-invocation friendly)
- Optional model/tools specification
- Clear usage line with argument examples
- Workflow section with numbered steps
- Success criteria checklist
- Example invocation
- Anti-patterns/best practices section

---

### Agent Patterns Observed

**Pattern 1: Specialist Reviewer**
- Used in: `@code-reviewer`
- Characteristics:
  - Minimal tool set (read-only: Read, Grep, Glob)
  - Skeptical/critical mindset
  - Specific domain expertise (financial calculations)
  - Structured checklist approach
  - Clear rejection criteria
  - Recommendation with rationale

**Pattern 2: Expected Agent Types (Not Yet Implemented)**
- **Code Writer:** Read, Write, Edit, Bash, Glob, Grep
- **Research Agent:** Read, Grep, Glob, WebFetch, WebSearch
- **Documentation Agent:** Read, Write, Edit, Glob, Grep, WebFetch, WebSearch

---

## PART 5: SIMILARITIES & REUSABLE PATTERNS

### What Commands and Agents Share

1. **YAML Frontmatter Pattern**
   - Both use frontmatter for metadata
   - Both have `description` field (auto-invocation friendly, 60-150 chars)
   - Both optionally specify `model` (sonnet/opus/haiku/inherit)

2. **Structured Output Format**
   - Commands output checkpoints/phases
   - Agents output verification results with tiers
   - Both use markdown formatting
   - Both include examples

3. **Tool Restrictions**
   - Both can restrict tools (allowed-tools vs tools field)
   - Both support Read, Grep, Glob, Write, Edit, Bash
   - Both emphasize read-only for reviewers

4. **Workflow Orientation**
   - Both define steps/phases
   - Both clarify when to use them
   - Both have constraints/boundaries
   - Both include anti-patterns/best practices

5. **Human-in-Loop Integration**
   - Commands have explicit checkpoints
   - Agents are invoked for review/approval
   - Both support decision gates

---

## PART 6: CREATING-SKILLS AS REFERENCE PATTERN

### How creating-skills Succeeds (Applicable to Commands/Agents)

**1. Multiple Specialized Templates**
   - Technique template (how-to guides)
   - Pattern template (mental models)
   - Discipline template (workflow enforcement)
   - Reference template (quick lookup)
   - **Lesson:** Different types need different structures

**2. CSO Optimization**
   - Description optimized for auto-invocation
   - Clear trigger conditions
   - Specific purpose statement
   - **Lesson:** Descriptions must be discoverable

**3. Rationalization-Proofing**
   - Clear "when to use" vs "when not to use"
   - Prerequisites documented
   - Anti-patterns explicitly listed
   - **Lesson:** Boundary conditions prevent misuse

**4. Progressive Disclosure**
   - Main SKILL.md stays <200 lines
   - Supporting content in subdirectories:
     - `scripts/` - Executable code
     - `references/` - Detailed docs
     - `assets/` - Templates, configs
   - **Lesson:** Large documentation should be split

**5. Template Validation**
   - Validators for naming, structure, CSO score
   - Can auto-generate scaffolds
   - **Lesson:** Consistency can be enforced programmatically

---

## PART 7: RECOMMENDATIONS FOR META-SKILLS

### For creating-commands Meta-Skill

**Structure Recommendations:**
1. **Multiple Command Templates:**
   - Workflow command (Research → Plan → Implement → Verify pattern)
   - Validation command (systematic checklist pattern)
   - Data processing command (load → transform → output pattern)
   - Reporting command (data aggregation → formatting → distribution)

2. **Required Sections for All Commands:**
   - YAML frontmatter (description, optional: model, allowed-tools)
   - Usage line with argument syntax
   - Purpose (1-2 sentences)
   - Workflow section (numbered steps)
   - Success criteria (checklist)
   - Example invocation
   - Anti-patterns section

3. **Environment-Aware:**
   - `/dev:` for development/experimental
   - `/prod:` for production workflows
   - `/shared:` for utilities (documentation sync, help)

4. **Validation Checklist for Commands:**
   - Valid environment prefix (dev/prod/shared)
   - Kebab-case naming
   - YAML frontmatter with description
   - Usage line present
   - Workflow steps numbered
   - Human checkpoints identified
   - Success criteria as checklist

5. **Template Variants:**
   ```
   .claude/templates/commands/
   ├── COMMAND_RPIV_TEMPLATE.md           # Research→Plan→Implement→Verify
   ├── COMMAND_VALIDATION_TEMPLATE.md     # Systematic checks
   ├── COMMAND_DATA_PROCESSING_TEMPLATE.md # Load→Transform→Output
   └── COMMAND_REPORTING_TEMPLATE.md      # Aggregation→Format→Distribute
   ```

---

### For creating-agents Meta-Skill

**Structure Recommendations:**
1. **Multiple Agent Templates:**
   - Reviewer agent (read-only: Read, Grep, Glob)
   - Research agent (read-only: Read, Grep, Glob, WebFetch, WebSearch)
   - Code writer agent (Write, Edit, Bash, Glob, Grep)
   - Documentation agent (Write, Edit, Glob, Grep, WebFetch, WebSearch)

2. **Required Sections for All Agents:**
   - YAML frontmatter (name, description, tools, optional: model)
   - Role definition (title + purpose)
   - Capabilities (bulleted list)
   - Constraints (boundaries, restrictions)
   - Workflow/Process section
   - Output format (structured template)
   - Example output showing expected quality/depth

3. **Tool Permission Tiers:**
   - **Read-only:** Read, Grep, Glob (reviewers, auditors, researchers)
   - **Research:** + WebFetch, WebSearch (research agents)
   - **Code Writers:** + Write, Edit, Bash (developers)
   - **Documentation:** + Write, Edit (document creators)

4. **Validation Checklist for Agents:**
   - Valid agent name (kebab-case)
   - YAML frontmatter with name, description, tools, optional model
   - Role and capabilities clearly defined
   - Constraints explicitly listed
   - Workflow/process steps numbered
   - Output format specified
   - Example output provided
   - Tool permissions match agent type

5. **Template Variants:**
   ```
   .claude/templates/agents/
   ├── AGENT_REVIEWER_TEMPLATE.md         # Read-only: Code/financial review
   ├── AGENT_RESEARCHER_TEMPLATE.md       # Read + Web: Research & analysis
   ├── AGENT_CODE_WRITER_TEMPLATE.md      # Write: Code generation
   └── AGENT_DOCUMENTATION_TEMPLATE.md    # Write: Doc creation
   ```

---

## PART 8: KEY DIFFERENCES FROM SKILLS

| Aspect | Skills | Commands | Agents |
|--------|--------|----------|--------|
| **Triggered By** | Auto-invoked based on keywords | User executes via `/command` | User invokes via `@agent` in text |
| **Execution Model** | Runs when conditions met | Runs from user initiation | Runs in response to request |
| **Workflow Type** | Progressive disclosure style | Step-by-step workflows | Focused analysis/review |
| **Human Checkpoints** | Few/none | Multiple (RPIV pattern) | Implicit in conversation |
| **Output Style** | Instructions/guidance | Structured reports with checkpoints | Review feedback with recommendation |
| **Directory Structure** | .claude/skills/{name}/ with subdirs | .claude/commands/{env}/name.md | .claude/agents/name.md (global) |
| **Environment Split** | dev/prod/shared subdirs | dev/prod/shared subdirs | Global (no split) |
| **Tools Approach** | Guided instructions | May restrict tools | Typically restricted (minimal) |
| **Use for Workflows** | Technique/pattern/discipline/reference | Multi-step process orchestration | Specialized review/analysis tasks |

---

## PART 9: IMPLEMENTATION IMPLICATIONS

### Design Decisions Required

**For creating-commands Meta-Skill:**
1. **Should commands live in .claude/commands/{env}/ or elsewhere?**
   - Current: YES, organized by environment (shared/prod/dev)
   - Recommendation: Keep this structure

2. **Should we auto-generate command scaffolds?**
   - Current: Manual creation from templates
   - Recommendation: YES, auto-generate like creating-skills does

3. **How many template variants needed?**
   - Current: 1 generic template
   - Recommendation: 4 variants (RPIV, validation, data processing, reporting)

4. **What validates command quality?**
   - Current: Manual review
   - Recommendation: Automated checks for:
     - Valid environment prefix
     - Kebab-case naming
     - YAML frontmatter present
     - Usage line syntax
     - Success criteria format

---

### Design Decisions Required

**For creating-agents Meta-Skill:**
1. **Should agents be environment-specific or global?**
   - Current: Global (no env split)
   - Recommendation: Keep global structure

2. **Should agents have maximum tool sets?**
   - Current: Minimal tools per agent type
   - Recommendation: YES, enforce tool minimalism

3. **How many agent templates needed?**
   - Current: 1 generic template
   - Recommendation: 4 variants (reviewer, researcher, code writer, doc)

4. **Should tool combinations be validated?**
   - Current: Manual selection
   - Recommendation: YES, preset templates with allowed combinations:
     - Reviewer: Read, Grep, Glob
     - Researcher: + WebFetch, WebSearch
     - Code Writer: Read, Write, Edit, Bash, Glob, Grep
     - Documentation: Read, Write, Edit, Glob, Grep, WebFetch

---

## PART 10: DISCOVERY & AUTO-INVOCATION

### Command Discovery
- Listed in slash command menu (via description field)
- Environment prefix helps users find appropriate commands
- Description field ≤200 chars for menu display
- Example: `/prod:variance-analysis - Budget vs actual variance analysis with human-in-loop checkpoints`

### Agent Discovery
- Accessible via `@agent-name` syntax
- Listed in agent menu (via description field)
- Description field helps users understand when to use
- Example: `@code-reviewer - Independent code reviewer specializing in financial calculation verification`

---

## SUMMARY OF PATTERNS

### Slash Commands Pattern:
✅ Environment-organized (dev/prod/shared)  
✅ YAML metadata for discovery  
✅ Multi-phase workflows (RPIV or validation)  
✅ Human checkpoints at phase boundaries  
✅ Structured success criteria  
✅ Anti-patterns documentation  

### Agents Pattern:
✅ Global namespace (no environment split)  
✅ YAML metadata with tool restrictions  
✅ Specialist role with clear mandate  
✅ Structured verification checklist  
✅ Explicit rejection criteria  
✅ Recommendation/decision output  

### Shared Patterns (Reusable):
✅ YAML frontmatter for metadata  
✅ Clear "when to use" boundary conditions  
✅ Anti-patterns/constraints documentation  
✅ Structured output formats  
✅ Example outputs/invocations  
✅ Tool restrictions for security  

---

## RESEARCH CONCLUSION

Commands and agents share a common **metadata + structured workflow** architecture but serve different purposes:

- **Commands** orchestrate multi-step user-initiated workflows with human approval gates
- **Agents** provide specialist analysis or review with focused tool access

Both can benefit from the **creating-skills approach**: multiple templates, validation, auto-generation, and progressive disclosure of supporting documentation.

**Next Steps:** Use this research to plan meta-skills for creating commands and agents (see plan.md).

---

**Research Conducted:** 2025-11-09  
**Evidence Base:** 5 existing implementations (2 commands, 1 agent, 3 templates) + CLAUDE.md workflow docs  
**Verification:** All patterns extracted from actual codebase, not inferred
