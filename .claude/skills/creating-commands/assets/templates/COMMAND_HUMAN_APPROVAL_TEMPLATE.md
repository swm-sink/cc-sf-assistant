---
description: {{DESCRIPTION}}
---

# {{COMMAND_TITLE}}

**Usage:** `/{{COMMAND_NAME}} {{ARG_1}} [{{ARG_2}}]`

**Purpose:** {{ONE_SENTENCE_PURPOSE}} with structured human approval gates for production safety.

---

## Phase 1: Prepare Approval Request

Gather context for human review:

1. **Document what requires approval:**
   - {{APPROVAL_SUBJECT}}
   - Affected systems/users: {{IMPACT_SCOPE}}
   - Estimated duration: {{ESTIMATED_DURATION}}

2. **Assess risk and reversibility:**
   - Risk level: {{RISK_ASSESSMENT_CRITERIA}}
   - Reversible: {{REVERSIBILITY_ASSESSMENT}}
   - Urgency: {{URGENCY_ASSESSMENT}}

3. **Gather supporting information:**
   - {{CONTEXT_ITEM_1}}
   - {{CONTEXT_ITEM_2}}
   - {{CONTEXT_ITEM_3}}

---

## Phase 2: Request Approval (Structured Format)

Present approval request in structured format:

```json
{
  "intent": "request_human_approval",
  "action": "{{ACTION_DESCRIPTION}}",
  "impact": "{{IMPACT_DESCRIPTION}}",
  "risk_level": "{{RISK_LEVEL}}",
  "urgency": "{{URGENCY_LEVEL}}",
  "reversible": {{REVERSIBLE}},
  "estimated_duration": "{{DURATION}}",
  "context": {
    "{{CONTEXT_KEY_1}}": "{{CONTEXT_VALUE_1}}",
    "{{CONTEXT_KEY_2}}": "{{CONTEXT_VALUE_2}}",
    "{{CONTEXT_KEY_3}}": "{{CONTEXT_VALUE_3}}"
  },
  "options": ["Approve", "Reject", "Request Changes"],
  "timeout_behavior": "{{TIMEOUT_ACTION}}"
}
```

**Approval Decision Options:**
- **Approve:** Proceed with {{ACTION_DESCRIPTION}}
- **Reject:** Cancel operation, no changes made
- **Request Changes:** Modify parameters and re-submit

**Timeout Handling:**
- If no response within {{TIMEOUT_DURATION}}, default action: {{DEFAULT_TIMEOUT_ACTION}}
- Paused workflows can be resumed later

**CHECKPOINT: Explicit user approval required before proceeding.**

---

## Phase 3: Execute (Conditional on Approval)

**IF Approved:**

1. **Pre-execution verification:**
   - {{PRE_EXECUTION_CHECK_1}}
   - {{PRE_EXECUTION_CHECK_2}}
   - {{PRE_EXECUTION_CHECK_3}}

2. **Execute approved action:**
   - {{EXECUTION_STEP_1}}
   - {{EXECUTION_STEP_2}}
   - {{EXECUTION_STEP_3}}

3. **Monitor execution:**
   - Track progress: {{PROGRESS_METRIC}}
   - Report status updates
   - Handle errors gracefully

**IF Rejected:**
- Log rejection reason
- Clean up any preparatory work
- Exit without making changes

**IF Request Changes:**
- Present modification form
- Adjust parameters per user input
- Re-submit for approval (return to Phase 2)

---

## Phase 4: Confirm & Audit

1. **Confirm completion to human:**
   - Action: {{ACTION_DESCRIPTION}}
   - Status: {{COMPLETION_STATUS}}
   - Duration: {{ACTUAL_DURATION}}
   - Outcome: {{OUTCOME_SUMMARY}}

2. **Log audit trail:**
   ```json
   {
     "timestamp": "{{ISO_8601_TIMESTAMP}}",
     "user": "{{APPROVING_USER}}",
     "command": "/{{COMMAND_NAME}}",
     "action": "{{ACTION_DESCRIPTION}}",
     "decision": "{{APPROVAL_DECISION}}",
     "risk_level": "{{RISK_LEVEL}}",
     "reversible": {{REVERSIBLE}},
     "outcome": "{{OUTCOME}}",
     "duration_seconds": {{DURATION_SECONDS}}
   }
   ```

3. **Archive audit trail:**
   - Save to: {{AUDIT_LOG_LOCATION}}
   - Include full context
   - Compliance-ready format

---

## Risk Assessment Guidelines

**Risk Levels:**

| Level | Criteria | Examples | Approval Authority |
|-------|----------|----------|-------------------|
| **High** | {{HIGH_RISK_CRITERIA}} | {{HIGH_RISK_EXAMPLE}} | {{HIGH_RISK_APPROVER}} |
| **Medium** | {{MEDIUM_RISK_CRITERIA}} | {{MEDIUM_RISK_EXAMPLE}} | {{MEDIUM_RISK_APPROVER}} |
| **Low** | {{LOW_RISK_CRITERIA}} | {{LOW_RISK_EXAMPLE}} | {{LOW_RISK_APPROVER}} |

**Reversibility Assessment:**
- **Reversible (true):** {{REVERSIBLE_CRITERIA}}
- **Irreversible (false):** {{IRREVERSIBLE_CRITERIA}}

**Urgency Levels:**
- **High:** {{HIGH_URGENCY_CRITERIA}}
- **Medium:** {{MEDIUM_URGENCY_CRITERIA}}
- **Low:** {{LOW_URGENCY_CRITERIA}}

---

## Success Criteria

Before marking complete:

- [ ] Approval request presented with complete context
- [ ] Risk level accurately assessed
- [ ] Reversibility correctly identified
- [ ] Human decision recorded (Approve/Reject/Request Changes)
- [ ] If approved: Action executed successfully
- [ ] If rejected: No changes made, clean exit
- [ ] Audit trail logged with all required fields
- [ ] Audit log saved to {{AUDIT_LOG_LOCATION}}
- [ ] Confirmation delivered to human

---

## Example Invocation

```bash
/{{COMMAND_NAME}} {{EXAMPLE_ARG_1}} {{EXAMPLE_ARG_2}}
```

**Expected Flow:**
1. Prepare approval request with risk assessment
2. Present structured approval request → Human decides
3. **IF Approved:** Execute action with monitoring
4. Confirm completion + log audit trail
5. Deliver outcome summary

**Example Approval Request:**
```
Action: {{EXAMPLE_ACTION}}
Impact: {{EXAMPLE_IMPACT}}
Risk: {{EXAMPLE_RISK_LEVEL}} ({{REVERSIBLE_YES_OR_NO}})
Urgency: {{EXAMPLE_URGENCY}}

[Approve] [Reject] [Request Changes]
```

---

## Anti-Patterns (DON'T DO THIS)

❌ Execute before receiving approval
❌ Skip risk assessment
❌ Omit reversibility information
❌ Forget audit trail logging
❌ Ignore timeout handling
❌ Proceed without structured approval format

✅ Always request approval BEFORE execution
✅ Assess risk, reversibility, and urgency
✅ Log complete audit trail for compliance

---

## Compliance Notes

**Regulatory Requirements:**
- {{COMPLIANCE_REQUIREMENT_1}}
- {{COMPLIANCE_REQUIREMENT_2}}

**Audit Trail Fields (Required):**
- Timestamp (ISO 8601)
- Approving user identity
- Action description
- Decision (Approve/Reject/Request Changes)
- Risk level and reversibility
- Outcome and duration

**Retention Policy:**
- Audit logs retained for {{RETENTION_PERIOD}}
- Stored in compliance-approved location
- Accessible for audits

---

**This command enforces HumanLayer Factor 7: Contact Humans with Tools for production-safe automation.**
