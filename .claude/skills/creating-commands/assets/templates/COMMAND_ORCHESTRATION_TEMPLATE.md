---
description: {{DESCRIPTION}}
---

# {{COMMAND_TITLE}}

**Usage:** `/{{COMMAND_NAME}} {{WORKFLOW_ARG_1}} [{{WORKFLOW_ARG_2}}]`

**Purpose:** {{ONE_SENTENCE_PURPOSE}} with dependency management and state tracking.

---

## Phase 1: Define Dependency Graph

List agents/tasks and their dependencies:

**Agent/Task Roster:**

| ID | Agent/Task | Dependencies | Estimated Time |
|----|------------|--------------|----------------|
| A | {{AGENT_1}} | None | {{TIME_A}} |
| B | {{AGENT_2}} | A | {{TIME_B}} |
| C | {{AGENT_3}} | A | {{TIME_C}} |
| D | {{AGENT_4}} | B, C | {{TIME_D}} |
| E | {{AGENT_5}} | D | {{TIME_E}} |

**Dependency Graph:**
```
    A ({{AGENT_1}})
    ├── B ({{AGENT_2}})
    │   └── D ({{AGENT_4}})
    │       └── E ({{AGENT_5}})
    └── C ({{AGENT_3}})
        └── D ({{AGENT_4}})
```

**Execution Order:**
1. A (no dependencies)
2. B, C (depends on A) - can run in parallel
3. D (depends on B, C) - wait for both
4. E (depends on D)

**Critical Path:** A → B → D → E (total: {{CRITICAL_PATH_TIME}})

---

## Phase 2: Initialize State

Set up state management for workflow:

**State Variables:**

```json
{
  "workflow_id": "{{WORKFLOW_ID}}",
  "status": "{{WORKFLOW_STATUS}}",
  "current_phase": "{{CURRENT_PHASE}}",
  "agents": {
    "{{AGENT_1}}": {"status": "pending", "output": null, "duration": null},
    "{{AGENT_2}}": {"status": "pending", "output": null, "duration": null},
    "{{AGENT_3}}": {"status": "pending", "output": null, "duration": null},
    "{{AGENT_4}}": {"status": "pending", "output": null, "duration": null},
    "{{AGENT_5}}": {"status": "pending", "output": null, "duration": null}
  },
  "start_time": "{{START_TIMESTAMP}}",
  "end_time": null,
  "total_duration": null
}
```

**State Transition Rules:**
- `pending` → `in_progress` (agent invoked)
- `in_progress` → `completed` (agent finished successfully)
- `in_progress` → `failed` (agent encountered error)
- `failed` → `retry` (retry logic triggered)

**Monitoring Structure:**
- State file: {{STATE_FILE_LOCATION}}
- Update frequency: After each agent completes
- Persistence: Save state after each transition

---

## Phase 3: Coordinate Execution

Invoke agents in dependency order:

**Execution Log:**

**Agent A ({{AGENT_1}}):**
- Status: {{AGENT_A_STATUS}}
- Started: {{AGENT_A_START}}
- Dependencies: None (ready to execute)
- Invocation:
  ```
  @{{AGENT_1}} {{AGENT_1_INSTRUCTIONS}}
  ```
- Output: {{AGENT_A_OUTPUT}}
- Duration: {{AGENT_A_DURATION}}

**Agent B ({{AGENT_2}}):**
- Status: {{AGENT_B_STATUS}}
- Started: {{AGENT_B_START}}
- Dependencies: A (✅ completed)
- Invocation:
  ```
  @{{AGENT_2}} {{AGENT_2_INSTRUCTIONS}}
  Context from A: {{AGENT_A_OUTPUT}}
  ```
- Output: {{AGENT_B_OUTPUT}}
- Duration: {{AGENT_B_DURATION}}

**Agent C ({{AGENT_3}}):**
- Status: {{AGENT_C_STATUS}}
- Started: {{AGENT_C_START}}
- Dependencies: A (✅ completed)
- Invocation:
  ```
  @{{AGENT_3}} {{AGENT_3_INSTRUCTIONS}}
  Context from A: {{AGENT_A_OUTPUT}}
  ```
- Output: {{AGENT_C_OUTPUT}}
- Duration: {{AGENT_C_DURATION}}

**Agent D ({{AGENT_4}}):**
- Status: {{AGENT_D_STATUS}}
- Started: {{AGENT_D_START}}
- Dependencies: B (✅ completed), C (✅ completed)
- Invocation:
  ```
  @{{AGENT_4}} {{AGENT_4_INSTRUCTIONS}}
  Context from B: {{AGENT_B_OUTPUT}}
  Context from C: {{AGENT_C_OUTPUT}}
  ```
- Output: {{AGENT_D_OUTPUT}}
- Duration: {{AGENT_D_DURATION}}

**Agent E ({{AGENT_5}}):**
- Status: {{AGENT_E_STATUS}}
- Started: {{AGENT_E_START}}
- Dependencies: D (✅ completed)
- Invocation:
  ```
  @{{AGENT_5}} {{AGENT_5_INSTRUCTIONS}}
  Context from D: {{AGENT_D_OUTPUT}}
  ```
- Output: {{AGENT_E_OUTPUT}}
- Duration: {{AGENT_E_DURATION}}

**State Tracking:**
- Update state file after each agent completes
- Pass outputs to dependent agents as context
- Handle failures gracefully (retry or fail-fast based on criticality)

---

## Phase 4: Handle Failures

Manage agent failures with retry or escalation:

**Failure Scenarios:**

1. **Non-Critical Failure ({{AGENT_X}}):**
   - Error: {{ERROR_MESSAGE}}
   - Impact: Workflow can continue with degraded results
   - Action: Log warning, mark as failed, continue

2. **Critical Failure ({{AGENT_Y}}):**
   - Error: {{ERROR_MESSAGE}}
   - Impact: Downstream agents cannot proceed
   - Action: Retry {{RETRY_COUNT}} times, then fail workflow

3. **Retry Logic:**
   - Max retries: {{MAX_RETRIES}}
   - Retry delay: {{RETRY_DELAY}}
   - Retry with modified parameters if applicable

**Failure Handling Flow:**
```
Agent fails
  ├─ Is critical?
  │  ├─ Yes → Retry up to {{MAX_RETRIES}} times
  │  │  ├─ Success → Continue workflow
  │  │  └─ All retries failed → FAIL WORKFLOW
  │  └─ No → Log warning, continue with degraded results
  └─ Update state file with failure details
```

---

## Phase 5: Aggregate Results

Collect outputs from all agents:

**Consolidated Results:**

1. **{{AGENT_1}} Output:**
   {{AGENT_1_CONSOLIDATED_OUTPUT}}

2. **{{AGENT_2}} Output:**
   {{AGENT_2_CONSOLIDATED_OUTPUT}}

3. **{{AGENT_3}} Output:**
   {{AGENT_3_CONSOLIDATED_OUTPUT}}

4. **{{AGENT_4}} Output:**
   {{AGENT_4_CONSOLIDATED_OUTPUT}}

5. **{{AGENT_5}} Output:**
   {{AGENT_5_CONSOLIDATED_OUTPUT}}

**Workflow Summary:**
- Total agents: {{TOTAL_AGENTS}}
- Successful: {{SUCCESSFUL_COUNT}}
- Failed (non-critical): {{FAILED_NON_CRITICAL_COUNT}}
- Failed (critical): {{FAILED_CRITICAL_COUNT}}
- Total duration: {{TOTAL_DURATION}}

**Final State:**
```json
{
  "workflow_id": "{{WORKFLOW_ID}}",
  "status": "{{FINAL_STATUS}}",
  "agents": {{FINAL_AGENT_STATES}},
  "start_time": "{{START_TIMESTAMP}}",
  "end_time": "{{END_TIMESTAMP}}",
  "total_duration": "{{TOTAL_DURATION}}"
}
```

---

## Success Criteria

Before marking complete:

- [ ] Dependency graph documented
- [ ] Execution order determined
- [ ] State initialized
- [ ] All agents invoked in correct order
- [ ] Dependencies respected (no agent runs before prerequisites)
- [ ] State updated after each agent completes
- [ ] Failures handled (retry or escalate)
- [ ] Outputs aggregated
- [ ] Final state saved
- [ ] Workflow summary presented

---

## Example Invocation

```bash
/{{COMMAND_NAME}} {{EXAMPLE_ARG_1}} {{EXAMPLE_ARG_2}}
```

**Expected Flow:**
1. Define graph → 5 agents (A → B,C → D → E)
2. Initialize state → All pending
3. Execute:
   - A completes → B,C start (parallel)
   - B,C complete → D starts
   - D completes → E starts
   - E completes → Workflow done
4. Aggregate → Consolidate all outputs

**Example Dependency Graph:**
```
@data-loader
  ├── @data-validator (depends on @data-loader)
  │   └── @data-transformer (depends on @data-validator, @config-parser)
  │       └── @report-generator (depends on @data-transformer)
  └── @config-parser (depends on @data-loader)
```

---

## Anti-Patterns (DON'T DO THIS)

❌ Execute agents without checking dependencies
❌ Forget state management
❌ Ignore failures (no retry logic)
❌ Sequential execution when parallelization possible
❌ Pass wrong context to dependent agents

✅ Dependency graph first, execution second
✅ Persistent state tracking
✅ Retry critical failures, log non-critical
✅ Parallelize when dependencies allow
✅ Context propagation (pass outputs to dependents)

---

**This command enforces 12-Factor Agents principles: orchestration commands coordinate agents with dependency management.**
