# Agent Orchestration and Lifecycle Management Research

**Date:** 2025-11-10
**Project:** FP&A Automation Assistant - Multi-Agent Workflow Coordinator Skill
**Purpose:** Determine whether to use pre-defined persistent agents OR create custom temporary one-off agents

---

## Executive Summary

**Research Question:** Should the Multi-Agent Workflow Coordinator use pre-defined persistent agents OR create custom temporary one-off agents?

**Answer:** **USE PRE-DEFINED PERSISTENT AGENTS** - No evidence of temporary/ephemeral agent support in Claude Code SDK.

**Key Finding:** "Fresh subagent" patterns (like subagent-driven-development) refer to fresh CONTEXT WINDOWS with general-purpose capabilities, NOT dynamically created agents with custom tool tiers or constraints.

**Recommendation:** Multi-Agent Workflow Coordinator should:
1. **Primary pattern:** Invoke pre-defined persistent agents via `@agent-name` for specialized work
2. **Secondary pattern:** Use `Task("description")` for general-purpose coordination tasks
3. **Hybrid approach:** Combine both based on task requirements and tool tier needs

---

## 1. Current State: How Agents Work Today

### 1.1 Agent Storage and Structure

**Location:** `.claude/agents/` with environment subdirectories

```
.claude/agents/
├── dev/          # Development-only agents
├── prod/         # Production-validated agents
└── shared/       # Cross-environment agents
```

**Format:** Markdown files with YAML frontmatter

```yaml
---
name: agent-name
description: Agent purpose and capabilities
tools: [Read, Grep, Glob]  # Tool tier restriction
---

# Agent Content
[Agent instructions, domain knowledge, workflow steps]
```

**Current Inventory:**
- 1 agent exists: code-reviewer.md (read-only)
- 7 agents planned (databricks-validator, adaptive-validator, script-generator, etc.)
- 0 agents in dev/, prod/, shared/ directories (empty with .gitkeep files)

### 1.2 Agent Creation Process

**Method:** creating-agents skill (meta-infrastructure)

**Steps:**
1. Choose template (Domain Specialist, Researcher, Reviewer)
2. Run interactive generator: `python generate_agent.py`
3. Fill placeholders with domain content
4. Validate with 4 validators:
   - `validate_agent_yaml.py` - YAML frontmatter
   - `validate_agent_naming.py` - Kebab-case conventions
   - `validate_agent_structure.py` - Section counts
   - `validate_agent_tools.py` - Tool tier enforcement
5. Save to `.claude/agents/{name}.md`
6. Test via `@agent-name` invocation

**Quality Gates:**
- Tool tier enforcement (3 tiers: read-only, read+web, full access)
- Naming conventions (kebab-case)
- Structure validation (template-specific rules)
- YAML schema compliance

**Validation:**
- Based on 116 production agents (awesome-claude-code-subagents)
- Enforces 12-Factor Agents principles
- Ensures consistency across all agents

### 1.3 Agent Invocation Patterns

**Pattern 1: Direct Agent Invocation**
```
@agent-name
```
- Invokes persistent agent from `.claude/agents/`
- Agent receives full context window
- Tool restrictions enforced based on YAML frontmatter
- Example: `@code-reviewer` (read-only tools only)

**Pattern 2: General-Purpose Task**
```
Task("Implement feature X with tests")
```
- Creates subagent with general-purpose capabilities
- Description becomes part of system prompt
- Uses default tool access (likely full access)
- Fresh context window (no prior conversation history)

**Pattern 3: Specific Plugin Agent**
```
Task(subagent_type="superpowers:code-reviewer")
```
- Invokes agent from external plugin
- Plugin agents have their own tool tiers
- Context passed via prompt template
- Example: wshobson-agents uses `subagent_type="error-debugging::debugger"`

**Pattern 4: Parallel Dispatch**
```
Task("Fix bug A")
Task("Fix bug B")
Task("Fix bug C")
# All three run concurrently
```
- Multiple Task() calls in succession execute in parallel
- Each has independent context window
- No shared state between agents
- Used in dispatching-parallel-agents skill

### 1.4 Agent Lifecycle

**Creation:** Via creating-agents skill → persistent .md file
**Invocation:** Via `@agent-name` or `Task(subagent_type="...")`
**Execution:** Fresh context window per invocation
**Termination:** Automatic when agent completes task
**Persistence:** Agent definition persists, context window does not

**Key Insight:** "Fresh subagent" means fresh CONTEXT WINDOW, not new agent file.

---

## 2. Persistent Agent Pattern (Current Implementation)

### 2.1 Definition

**Persistent Agents** are agent definitions saved as `.md` files in `.claude/agents/` that can be invoked repeatedly across sessions.

### 2.2 Characteristics

**Storage:**
- Permanent .md files in git-tracked directory
- Environment-specific subdirectories (dev/, prod/, shared/)
- YAML frontmatter with metadata and tool restrictions

**Creation:**
- Interactive generator with templates
- 4-step validation pipeline
- Quality gates enforced before saving

**Invocation:**
- `@agent-name` syntax for direct invocation
- `Task(subagent_type="plugin:agent-name")` for plugin agents
- Fresh context window per invocation

**Tool Access:**
- Explicitly defined in YAML frontmatter
- 3 tiers enforced: read-only, read+web, full access
- Validated during creation (cannot be bypassed)

**Reusability:**
- Same agent used across multiple workflows
- Consistent behavior guaranteed
- Can be tested and refined independently

### 2.3 Pros

✅ **Quality Assurance:**
- 4 validators ensure correctness
- Tool tier enforcement (security)
- Template-based consistency
- Based on 116 production agents (proven patterns)

✅ **Reusability:**
- Define once, use everywhere
- Consistent behavior across workflows
- Reduces duplication

✅ **Testing:**
- Can test agent independently
- Iterate based on performance
- Version control for changes

✅ **Tool Tier Enforcement:**
- Read-only agents cannot modify code (safety)
- Web-enabled agents for research
- Full access for implementation

✅ **Documentation:**
- Agent purpose clearly defined
- Domain knowledge preserved
- Workflow steps documented

✅ **Integration with Meta-Infrastructure:**
- creating-agents skill handles creation
- System Coherence Validator can check agents
- Naming conventions enforced

### 2.4 Cons

❌ **Upfront Overhead:**
- Must create agent definition before use
- 4-step validation process
- Fill template placeholders

❌ **Less Flexible:**
- Cannot customize per-task
- Fixed tool tier (cannot grant temporary permissions)
- Must edit .md file to change behavior

❌ **Storage Overhead:**
- One file per agent
- Could accumulate many agents over time
- Must manage agent inventory

❌ **Not Suitable for One-Off Tasks:**
- Creating agent for single-use is wasteful
- Better to use general-purpose Task() for simple tasks

### 2.5 When to Use Persistent Agents

✅ **Use When:**
- Agent will be reused across multiple workflows
- Tool tier restrictions required (read-only, read+web)
- Domain expertise needs to be preserved
- Quality validation important
- Example: @databricks-validator, @code-reviewer, @script-generator

❌ **Don't Use When:**
- One-off task that won't recur
- General-purpose work (no special tools/constraints)
- Rapid prototyping (overhead not justified)
- Example: "Calculate sum of these 3 numbers"

---

## 3. Temporary Agent Pattern (Feasibility Analysis)

### 3.1 Definition

**Temporary Agents** would be agent definitions created in-memory at runtime, used once, then discarded without saving to `.claude/agents/`.

### 3.2 Expected Characteristics (Hypothetical)

**Storage:**
- In-memory only (not persisted to disk)
- Created dynamically from templates or prompts
- Discarded after single use

**Creation:**
- Programmatic generation (no interactive prompts)
- Potentially use creating-agents templates
- Skip or auto-pass validation

**Invocation:**
- Would need Task() to accept inline agent definition
- Or Task() to generate agent from description

**Tool Access:**
- Would need to specify tool tier at creation
- Must enforce restrictions (cannot bypass security)

**Reusability:**
- None - created for single task
- Would need to recreate for each use

### 3.3 Research Findings: Is This Possible?

**Evidence Search:**
- ✅ Searched external/superpowers/ for temporary/ephemeral/dynamic patterns
- ✅ Searched external/12-factor-agents/ for runtime agent creation
- ✅ Searched Claude Code documentation references
- ✅ Reviewed Task() usage patterns across codebase

**Result:** **NO EVIDENCE** of temporary/ephemeral agent support in Claude Code SDK.

**What "Fresh Subagent" Actually Means:**
- "Fresh subagent per task" (subagent-driven-development) = fresh CONTEXT WINDOW
- NOT a dynamically created agent with custom tools
- Task("description") uses general-purpose capabilities with prompt

**Key Quote from subagent-driven-development:**
```
Dispatch fresh subagent:
  Task tool (general-purpose):
    description: "Implement Task N: [task name]"
    prompt: |
      You are implementing Task N from [plan-file].
      [instructions...]
```

**Interpretation:**
- Task() accepts a description/prompt, NOT an agent definition
- "Fresh" refers to clean context (no prior conversation)
- No mechanism to specify tool tier or custom constraints inline

**Task() API Analysis:**
```python
# What EXISTS:
Task("description")                           # General-purpose subagent
Task(subagent_type="plugin:agent-name")       # Pre-defined plugin agent

# What DOESN'T exist (no evidence found):
Task(agent_definition={...})                  # Inline agent definition
Task(tools=[Read, Grep], description="...")   # Custom tool tier
create_temporary_agent(...)                   # Dynamic agent creation API
```

### 3.4 Pros (Hypothetical - If It Existed)

✅ **Flexibility:**
- Customize agent per task
- No need to create persistent file
- Rapid prototyping

✅ **No Storage Overhead:**
- No .md files accumulating
- Clean agent directory

✅ **One-Off Tasks:**
- Perfect for unique, non-repeating work
- No wasted persistent agents

### 3.5 Cons (Even If It Existed)

❌ **No Quality Gates:**
- Cannot validate before use (happens at runtime)
- Risk of incorrect tool tier
- No template enforcement

❌ **No Reusability:**
- Must recreate for each use
- Cannot refine based on testing
- Duplicated effort

❌ **Tool Tier Enforcement Risk:**
- How to ensure read-only constraint?
- What prevents granting full access inappropriately?
- Security implications

❌ **No Documentation:**
- Agent logic ephemeral (lost after use)
- Cannot review or audit
- Hard to debug failures

❌ **Not Compatible with creating-agents:**
- Bypasses meta-infrastructure
- No validation pipeline
- Inconsistent with project principles

### 3.6 Verdict: Temporary Agents NOT Viable

**Reasons:**
1. **No API Support:** Claude Code SDK doesn't expose temporary agent creation
2. **Security Risk:** Cannot enforce tool tier restrictions without validation
3. **Violates Meta-Infrastructure Principle:** Bypasses creating-agents quality gates
4. **Not Worth Implementation Cost:** Task() already handles general-purpose work

**Alternative:** Use `Task("description")` for simple coordination, persistent agents for specialized work.

---

## 4. Hybrid Approach (Recommended)

### 4.1 Decision Matrix

| Use Case | Pattern | Rationale |
|----------|---------|-----------|
| **Specialized validation** | `@databricks-validator` | Persistent agent with read-only tools, reusable |
| **Code review** | `@code-reviewer` | Persistent agent, proven template, read-only |
| **Script generation** | `@script-generator` | Persistent agent with full access, quality gates |
| **General coordination** | `Task("Aggregate results from A, B, C")` | Simple task, no special tools needed |
| **Parallel dispatch** | Multiple `Task()` calls | Independent tasks, fresh contexts |
| **Domain expertise** | `@financial-analyst` | Persistent agent with domain knowledge |
| **One-off calculation** | `Task("Calculate variance")` | Simple task, general-purpose |

### 4.2 When to Use Which Pattern

**Use Persistent Agent (`@agent-name`) When:**
- ✅ Tool tier restriction required (read-only, read+web)
- ✅ Domain expertise needs preservation
- ✅ Agent will be reused (>2-3 times)
- ✅ Quality validation critical (financial, security)
- ✅ Workflow complexity justifies dedicated agent

**Use General-Purpose Task (`Task("description")`) When:**
- ✅ One-off coordination task
- ✅ Simple aggregation or calculation
- ✅ No special tool restrictions needed
- ✅ No domain expertise required
- ✅ Rapid prototyping

**Example Hybrid Workflow:**
```
# Orchestrator uses Task() for coordination
Task("Coordinate variance analysis workflow")

# Within that coordination, invoke specialized agents:
1. @databricks-validator (validates query results - read-only)
2. Task("Calculate variances using Decimal") (simple math - general)
3. @report-formatter (validates Excel output - read-only)
4. @code-reviewer (final review - read-only)
```

### 4.3 Multi-Agent Workflow Coordinator Design

**Architecture:**

```
Multi-Agent Workflow Coordinator (Skill)
├─ Define dependency graph
├─ Initialize state tracking
├─ Coordinate execution:
│  ├─ Persistent agents for specialized work (@agent-name)
│  ├─ General tasks for coordination (Task())
│  └─ Parallel dispatch where applicable
├─ Handle failures with retry logic
└─ Aggregate results
```

**Agent Invocation Strategy:**

**Phase 1: Define Roster**
- Identify required agents (persistent vs. general)
- Map dependencies between agents
- Assign tool tier based on task risk

**Phase 2: Invoke Agents**
```python
# Persistent agent for validation (read-only)
@databricks-validator
  Input: Query results from Phase 1
  Output: Validation report

# General task for transformation
Task("Transform data using pandas with Decimal precision")
  Input: Validated data
  Output: Transformed dataset

# Persistent agent for final review (read-only)
@code-reviewer
  Input: All changes
  Output: Approval/rejection
```

**Phase 3: Result Aggregation**
- Coordinator uses Task() to aggregate outputs
- No special tools needed (just consolidation)

### 4.4 Quality Considerations

**For Persistent Agents:**
- ✅ Must pass 4 validators before use
- ✅ Tool tier enforcement guaranteed
- ✅ Consistent with creating-agents meta-skill
- ✅ Can be tested independently

**For General Tasks:**
- ⚠️ No validation (Task() accepts any description)
- ⚠️ Tool access unrestricted (likely full access)
- ⚠️ Cannot enforce read-only constraint
- ✅ Good for simple coordination

**Mitigation:**
- Use persistent agents for ANY task requiring tool restrictions
- Reserve Task() for genuinely simple coordination
- Document decision criteria in Multi-Agent Workflow Coordinator skill

---

## 5. Command Orchestration vs. Skill Orchestration

### 5.1 Commands That Orchestrate Agents

**Pattern:** Commands (slash commands) coordinate workflows using agents and skills.

**Example:** Orchestration Template (COMMAND_ORCHESTRATION_TEMPLATE.md)

```markdown
## Phase 3: Coordinate Execution

**Agent A (data-loader):**
- Invocation: @data-loader {instructions}
- Output: {data}

**Agent B (data-validator):**
- Dependencies: A completed
- Invocation: @data-validator {data from A}
- Output: {validation report}
```

**Key Features:**
- Commands use `@agent-name` syntax
- Dependency graph explicit
- State tracking per agent
- Context passed between agents

**Orchestration Template Agents:**
```
@data-loader → @data-validator → @data-transformer → @report-generator
                ↓
              @config-parser → (merges into data-transformer)
```

### 5.2 Skills That Orchestrate Agents

**Pattern:** Skills (auto-invoked) coordinate agent work using Task() tool.

**Example:** subagent-driven-development

```
For each task in plan:
  1. Task("Implement Task N from plan")
  2. Task(subagent_type="superpowers:code-reviewer")
  3. If issues: Task("Fix issues from review")
```

**Key Features:**
- Skills use Task() tool for invocation
- Can invoke persistent agents via subagent_type
- Can use general-purpose Task("description")
- Parallel dispatch with multiple Task() calls

### 5.3 Difference Between @agent-name and Task()

**`@agent-name` Invocation:**
- Direct call in conversation (user-facing)
- Agent must exist in `.claude/agents/`
- Used in command templates
- Example: `@code-reviewer` in markdown

**`Task()` Tool Invocation:**
- Programmatic call (tool usage)
- Two modes:
  - `Task("description")` - general-purpose
  - `Task(subagent_type="plugin:agent-name")` - specific agent
- Used in skills for orchestration
- Example: `Task(subagent_type="superpowers:code-reviewer")`

**Equivalence:**
```
# In conversation / command template:
@code-reviewer

# In skill using Task() tool:
Task(subagent_type="superpowers:code-reviewer")
```

### 5.4 Orchestration Pattern for Multi-Agent Workflow Coordinator

**Decision:** Multi-Agent Workflow Coordinator is a **SKILL**, not a command.

**Rationale:**
- Auto-invoked when complex multi-agent work needed
- Uses Task() tool for orchestration
- Can invoke both persistent agents and general tasks
- Skill description triggers auto-invocation

**Invocation Patterns:**

**For Persistent Agents:**
```python
# Option 1: Direct agent invocation (if allowed in skill context)
@databricks-validator

# Option 2: Task with subagent_type (if agent in plugin)
Task(subagent_type="project:databricks-validator")

# Option 3: General task with detailed prompt
Task("Validate Databricks query results using read-only tools...")
```

**For General Coordination:**
```python
Task("Aggregate variance results from 3 departments")
Task("Calculate total budget across all accounts using Decimal")
```

**Parallel Dispatch:**
```python
# All run concurrently (independent)
Task("Analyze department A variance")
Task("Analyze department B variance")
Task("Analyze department C variance")
```

---

## 6. Implementation Considerations

### 6.1 Agent Creation Workflow

**For New Persistent Agents:**
1. Identify need (e.g., "Need databricks-validator")
2. Invoke creating-agents skill
3. Choose template (Reviewer for read-only validation)
4. Run generator, fill placeholders
5. Validate with 4 validators
6. Save to `.claude/agents/prod/databricks-validator.md`
7. Test: `@databricks-validator` (or via Task())

**Timeline:**
- Simple agent: ~30 minutes (template + validation)
- Complex agent: ~2 hours (extensive domain knowledge)

**When to Create:**
- Before using in Multi-Agent Workflow Coordinator
- During planning phase (not during execution)
- Batch creation (create all 7 planned agents together)

### 6.2 Tool Tier Enforcement

**3 Tool Tiers:**

**Tier 1: Read-Only (3-5% of agents)**
- Tools: `[Read, Grep, Glob]`
- Use for: Validators, reviewers, auditors
- Example: @databricks-validator, @code-reviewer
- Security: Cannot modify code or files

**Tier 2: Read + Web (5% of agents)**
- Tools: `[Read, Grep, Glob, WebFetch, WebSearch]`
- Use for: Researchers, documentation generators
- Example: @documentation-researcher
- Security: Can fetch external data, but cannot modify code

**Tier 3: Full Access (86% of agents)**
- Tools: `[Read, Write, Edit, Bash, Glob, Grep, ...]`
- Use for: Implementers, script generators
- Example: @script-generator, @test-generator
- Security: Full code modification (use with caution)

**Enforcement:**
- YAML frontmatter defines tools
- Validator checks tool tier during creation
- Cannot be bypassed (hard constraint)

**Multi-Agent Workflow Coordinator Responsibility:**
- Route tasks to appropriate agent based on tool needs
- Use read-only agents for validation
- Use full-access agents for implementation
- Document tool tier decisions

### 6.3 Quality Gates

**For Persistent Agents:**
- ✅ 4 validators (YAML, naming, structure, tools)
- ✅ Template-based consistency
- ✅ Based on 116 production agents

**For Task() Calls:**
- ⚠️ No validators (direct execution)
- ⚠️ Prompt quality determines success
- ⚠️ Must manually ensure quality

**Quality Strategy for Multi-Agent Workflow Coordinator:**
1. **Persistent agents for critical work** (validation, code review)
2. **Task() for simple coordination** (aggregation, calculation)
3. **Document decision rationale** in skill
4. **Test workflows end-to-end** before production use

### 6.4 Lifecycle Management

**Agent Lifecycle:**
```
Create (via creating-agents)
  ↓
Validate (4 validators)
  ↓
Save (.claude/agents/{env}/{name}.md)
  ↓
Invoke (@agent-name or Task(subagent_type="..."))
  ↓
Execute (fresh context window per invocation)
  ↓
Terminate (context discarded, agent persists)
  ↓
Refine (edit .md file, re-validate)
```

**Multi-Agent Workflow Coordinator Responsibilities:**
1. **Pre-flight:** Verify required agents exist
2. **Execution:** Invoke agents in dependency order
3. **State tracking:** Maintain workflow state
4. **Error handling:** Retry failed agents
5. **Aggregation:** Consolidate outputs
6. **Cleanup:** No cleanup needed (agents persist, contexts auto-discard)

### 6.5 Context Passing Between Agents

**Pattern:**
```python
# Agent A executes
output_A = Task("Load data from Databricks")

# Agent B receives context from A
output_B = Task(f"""
Validate data from Agent A:
{output_A}

Check for:
- Null values
- Duplicate accounts
- Invalid account types
""")

# Agent C receives context from A and B
output_C = Task(f"""
Generate variance report using:
- Data: {output_A}
- Validation: {output_B}

Use Decimal precision.
""")
```

**Key Points:**
- Context passed via prompt (f-string)
- Each agent has fresh context window
- No shared state between agents
- Coordinator manages context flow

---

## 7. Recommendation for Multi-Agent Workflow Coordinator

### 7.1 Primary Recommendation

**USE PRE-DEFINED PERSISTENT AGENTS** as the primary pattern.

**Rationale:**
1. ✅ No evidence of temporary/ephemeral agent API in Claude Code
2. ✅ Quality gates enforced via creating-agents
3. ✅ Tool tier enforcement for security
4. ✅ Reusability across workflows
5. ✅ Testable and refineable
6. ✅ Consistent with meta-infrastructure principles
7. ✅ Proven pattern (116 production agents)

### 7.2 Hybrid Approach

**Combine persistent agents and general tasks:**

**Persistent Agents For:**
- ✅ Validation (read-only tools)
- ✅ Code review (read-only tools)
- ✅ Script generation (full access, but quality gates)
- ✅ Domain expertise (financial, Python, etc.)
- ✅ Reusable workflows (>2-3 uses)

**General Tasks (Task()) For:**
- ✅ Simple coordination ("Aggregate results")
- ✅ One-off calculations ("Calculate sum")
- ✅ Data transformation ("Convert to Decimal")
- ✅ Result consolidation
- ✅ No special tool restrictions needed

### 7.3 Decision Criteria

**When designing Multi-Agent Workflow Coordinator, ask:**

1. **Does this task require tool restrictions?**
   - YES → Persistent agent (e.g., read-only validator)
   - NO → Can use Task()

2. **Will this task be reused?**
   - YES → Persistent agent (define once, use everywhere)
   - NO → Task() acceptable

3. **Does this need domain expertise?**
   - YES → Persistent agent (preserve knowledge)
   - NO → Task() acceptable

4. **Is quality validation critical?**
   - YES → Persistent agent (4 validators)
   - NO → Task() acceptable

5. **Is this financial/security-sensitive?**
   - YES → Persistent agent (audit trail, validation)
   - NO → Task() acceptable if simple

### 7.4 Implementation Plan

**Phase 1: Create Required Persistent Agents**
1. Identify specialized agents needed (7 planned)
2. Use creating-agents skill to generate
3. Validate all agents before proceeding
4. Save to appropriate directories (dev/, prod/)

**Phase 2: Implement Multi-Agent Workflow Coordinator Skill**
1. Design dependency graph logic
2. Implement agent invocation (hybrid approach)
3. State tracking and error handling
4. Result aggregation
5. Testing with mock workflows

**Phase 3: Integration Testing**
1. Test with real workflows (variance analysis)
2. Verify persistent agents work correctly
3. Verify Task() coordination works
4. Measure performance (parallel speedup)

**Phase 4: Documentation**
1. Document decision criteria (when to use which pattern)
2. Examples of hybrid workflows
3. Tool tier enforcement rationale
4. Troubleshooting guide

### 7.5 Example: Variance Analysis Workflow

**Using Hybrid Approach:**

```python
# Multi-Agent Workflow Coordinator orchestrates:

# Phase 1: Persistent agent for data validation (read-only)
validation_result = invoke_agent("@databricks-validator", {
    "task": "Validate query results",
    "input": databricks_output,
    "checks": ["null_values", "duplicates", "account_types"]
})

# Phase 2: General task for variance calculation (simple math)
variance_data = Task(f"""
Calculate variances using Decimal precision:
- Budget data: {budget_df}
- Actual data: {actual_df}
- Validation: {validation_result}

Return: DataFrame with absolute and percentage variances
""")

# Phase 3: Persistent agent for report formatting validation (read-only)
format_validation = invoke_agent("@report-formatter", {
    "task": "Validate Excel output structure",
    "input": variance_data,
    "checks": ["sheet_names", "column_headers", "formatting"]
})

# Phase 4: General task for final aggregation
final_report = Task(f"""
Aggregate results into executive summary:
- Variance data: {variance_data}
- Format validation: {format_validation}

Return: Executive summary with top 10 material variances
""")

# Phase 5: Persistent agent for final review (read-only)
review = invoke_agent("@code-reviewer", {
    "task": "Review variance analysis implementation",
    "base_sha": base_commit,
    "head_sha": current_commit,
    "requirements": variance_analysis_spec
})
```

**Benefits:**
- ✅ Read-only agents for validation (security)
- ✅ General tasks for simple coordination (efficiency)
- ✅ Tool tier enforcement where needed
- ✅ Quality gates for critical steps
- ✅ Clear separation of concerns

---

## 8. Key Insights

### 8.1 "Fresh Subagent" Clarification

**What it DOES mean:**
- Fresh CONTEXT WINDOW (no prior conversation history)
- Clean slate for each task
- No context pollution from previous work

**What it DOESN'T mean:**
- NOT a dynamically created agent with custom tools
- NOT a new agent definition file
- NOT a temporary/ephemeral agent

**Example from subagent-driven-development:**
```
Task("Implement Task 1")  # Fresh context window #1
Task("Implement Task 2")  # Fresh context window #2
Task("Implement Task 3")  # Fresh context window #3
```
- Each Task() gets a fresh context
- All use same general-purpose capabilities
- No custom agent definitions created

### 8.2 Task() vs. @agent-name

**Task():**
- Programmatic invocation (tool call)
- Fresh context window
- Two modes:
  - `Task("description")` - general-purpose
  - `Task(subagent_type="...")` - specific agent
- Used in skills for orchestration

**@agent-name:**
- Direct invocation (conversation syntax)
- Fresh context window
- Must be persistent agent in `.claude/agents/`
- Used in commands and conversations

**Equivalence:**
```python
# Conversation:
@code-reviewer

# Skill tool call:
Task(subagent_type="project:code-reviewer")
```

### 8.3 Parallel vs. Sequential Execution

**Parallel (Independent Tasks):**
```python
Task("Analyze department A")
Task("Analyze department B")
Task("Analyze department C")
# All run concurrently
```

**Sequential (Dependent Tasks):**
```python
data = Task("Load data")
validation = Task(f"Validate: {data}")
report = Task(f"Generate report: {validation}")
# Each waits for previous
```

**Multi-Agent Workflow Coordinator Must:**
- Identify independent vs. dependent tasks
- Parallelize where possible (speedup)
- Enforce dependencies where required (correctness)

### 8.4 Tool Tier Security

**Critical Insight:** Tool tier enforcement is WHY persistent agents matter.

**Without Persistent Agents:**
- Task() likely has full access (all tools)
- Cannot restrict to read-only
- Security risk (validator could modify code)

**With Persistent Agents:**
- YAML frontmatter defines tools
- Validator cannot modify (only Read, Grep, Glob)
- Security guaranteed

**Implication for Multi-Agent Workflow Coordinator:**
- MUST use persistent agents for read-only tasks
- Cannot rely on Task() for validation (no tool restriction)

---

## 9. Research Sources

### 9.1 Project Files Analyzed

**Agent Infrastructure:**
- `/home/user/cc-sf-assistant/.claude/skills/creating-agents/SKILL.md` (251 lines)
- `/home/user/cc-sf-assistant/.claude/agents/` (directories: dev, prod, shared - currently empty)

**Command Templates:**
- `/home/user/cc-sf-assistant/.claude/skills/creating-commands/SKILL.md` (230 lines)
- `/home/user/cc-sf-assistant/.claude/skills/creating-commands/assets/templates/COMMAND_ORCHESTRATION_TEMPLATE.md` (294 lines)

**External Patterns:**
- `/home/user/cc-sf-assistant/external/superpowers/skills/dispatching-parallel-agents/SKILL.md` (181 lines)
- `/home/user/cc-sf-assistant/external/superpowers/skills/subagent-driven-development/SKILL.md` (190 lines)
- `/home/user/cc-sf-assistant/external/claude-code/wshobson-agents/plugins/incident-response/commands/smart-fix.md` (835 lines)

**12-Factor Agents:**
- `/home/user/cc-sf-assistant/external/12-factor-agents/content/factor-10-small-focused-agents.md`
- `/home/user/cc-sf-assistant/external/12-factor-agents/content/factor-08-own-your-control-flow.md`
- `/home/user/cc-sf-assistant/external/12-factor-agents/content/factor-02-own-your-prompts.md`

**Project Documentation:**
- `/home/user/cc-sf-assistant/specs/holistic-skills/research.md` (609 lines)
- `/home/user/cc-sf-assistant/EXPLORATION_REPORT.md` (agent inventory)
- `/home/user/cc-sf-assistant/spec.md` (business requirements)
- `/home/user/cc-sf-assistant/plan.md` (technical implementation)

### 9.2 Search Patterns Used

- `Task\(` - Find Task() tool usage
- `@[a-z-]+` - Find agent invocations
- `subagent_type` - Find specific agent invocation
- `temporary|ephemeral|dynamic.*agent` - Search for temporary agent patterns
- `in-memory|runtime.*agent` - Search for runtime agent creation

### 9.3 Key Findings

1. **No temporary agent API** - No evidence in codebase or external patterns
2. **Task() is general-purpose** - Not for creating custom agents
3. **Fresh subagent = fresh context** - Not new agent definition
4. **Persistent agents are standard** - All examples use .md files
5. **Tool tier enforcement requires YAML** - Cannot do inline restriction

---

## 10. Conclusion

**Answer to Research Question:**

**USE PRE-DEFINED PERSISTENT AGENTS** for the Multi-Agent Workflow Coordinator.

**Key Reasons:**
1. No API support for temporary/ephemeral agents in Claude Code
2. Tool tier enforcement requires persistent agent definitions
3. Quality gates via creating-agents skill ensure correctness
4. Reusability and testability critical for production system
5. Consistent with meta-infrastructure-first principle
6. Proven pattern (116 production agents)

**Hybrid Approach Recommended:**
- Persistent agents for specialized work (validation, review, generation)
- General Task() for simple coordination (aggregation, calculation)
- Decision criteria based on tool restrictions, reusability, domain expertise

**Implementation Priority:**
1. **Create 7 planned persistent agents** (databricks-validator, script-generator, etc.)
2. **Implement Multi-Agent Workflow Coordinator skill** with hybrid approach
3. **Document decision criteria** for when to use which pattern
4. **Test workflows end-to-end** with real use cases

**Next Steps:**
- Get user approval for this research
- Proceed to detailed implementation plan (specs/holistic-skills/plan.md)
- Begin Phase 3: Implementation using creating-agents skill

---

**Research Phase Status:** ✅ COMPLETE (Agent Orchestration Analysis)
**Next Checkpoint:** Plan approval before implementation
