---
description: {{DESCRIPTION}}
---

# {{COMMAND_TITLE}}

**Usage:** `/{{COMMAND_NAME}} {{REQUEST_INPUT}}`

**Purpose:** {{ONE_SENTENCE_PURPOSE}} with deterministic routing based on classification.

---

## Phase 1: Classify Input

Analyze request characteristics:

**Classification Dimensions:**

1. **Domain:** {{DOMAIN_CLASSIFICATION}}
   - Possible values: {{DOMAIN_1}} | {{DOMAIN_2}} | {{DOMAIN_3}} | {{DOMAIN_4}} | {{DOMAIN_5}}
   - Detection: {{DOMAIN_DETECTION_METHOD}}

2. **Complexity:** {{COMPLEXITY_CLASSIFICATION}}
   - Possible values: simple | moderate | complex
   - Detection: {{COMPLEXITY_DETECTION_METHOD}}

3. **Urgency:** {{URGENCY_CLASSIFICATION}}
   - Possible values: low | medium | high | critical
   - Detection: {{URGENCY_DETECTION_METHOD}}

4. **Required Expertise:** {{EXPERTISE_CLASSIFICATION}}
   - Possible values: specialist | generalist
   - Detection: {{EXPERTISE_DETECTION_METHOD}}

**Classification Result:**
```json
{
  "domain": "{{DETECTED_DOMAIN}}",
  "complexity": "{{DETECTED_COMPLEXITY}}",
  "urgency": "{{DETECTED_URGENCY}}",
  "expertise": "{{DETECTED_EXPERTISE}}"
}
```

---

## Phase 2: Route to Handler (Decision Table)

**Routing Decision Table:**

| Domain | Complexity | Urgency | Handler | Rationale |
|--------|-----------|---------|---------|-----------|
| {{DOMAIN_1}} | simple | any | {{HANDLER_1}} | {{RATIONALE_1}} |
| {{DOMAIN_1}} | moderate | any | {{HANDLER_2}} | {{RATIONALE_2}} |
| {{DOMAIN_1}} | complex | any | {{HANDLER_3}} | {{RATIONALE_3}} |
| {{DOMAIN_2}} | simple | any | {{HANDLER_4}} | {{RATIONALE_4}} |
| {{DOMAIN_2}} | moderate | any | {{HANDLER_5}} | {{RATIONALE_5}} |
| {{DOMAIN_2}} | complex | any | {{HANDLER_6}} | {{RATIONALE_6}} |
| {{DOMAIN_3}} | any | critical | {{HANDLER_7}} | {{RATIONALE_7}} |
| {{DOMAIN_4}} | any | any | {{HANDLER_8}} | {{RATIONALE_8}} |
| {{DOMAIN_5}} | any | any | {{HANDLER_9}} | {{RATIONALE_9}} |

**Routing Logic (Explicit):**

```
IF domain == "{{DOMAIN_1}}" AND complexity == "simple" THEN
  handler = {{HANDLER_1}}
  rationale = "{{RATIONALE_1}}"

ELSE IF domain == "{{DOMAIN_1}}" AND complexity == "moderate" THEN
  handler = {{HANDLER_2}}
  rationale = "{{RATIONALE_2}}"

ELSE IF domain == "{{DOMAIN_1}}" AND complexity == "complex" THEN
  handler = {{HANDLER_3}}
  rationale = "{{RATIONALE_3}}"

ELSE IF domain == "{{DOMAIN_2}}" AND complexity == "simple" THEN
  handler = {{HANDLER_4}}
  rationale = "{{RATIONALE_4}}"

ELSE IF domain == "{{DOMAIN_2}}" AND complexity IN ["moderate", "complex"] THEN
  handler = {{HANDLER_5}}
  rationale = "{{RATIONALE_5}}"

ELSE IF urgency == "critical" THEN
  handler = {{HANDLER_7}}
  rationale = "{{RATIONALE_7}}"

ELSE
  handler = {{DEFAULT_HANDLER}}
  rationale = "{{DEFAULT_RATIONALE}}"
```

**Selected Handler:** {{SELECTED_HANDLER}}
**Routing Rationale:** {{ROUTING_RATIONALE}}

---

## Phase 3: Delegate Execution

Invoke selected handler with full context:

**Handler Invocation:**

```
{{HANDLER_INVOCATION_FORMAT}} Please {{HANDLER_INSTRUCTION}}:

Original request:
{{ORIGINAL_REQUEST}}

Classification context:
- Domain: {{DETECTED_DOMAIN}}
- Complexity: {{DETECTED_COMPLEXITY}}
- Urgency: {{DETECTED_URGENCY}}
- Expertise: {{DETECTED_EXPERTISE}}

Routing rationale:
{{ROUTING_RATIONALE}}

Expected output format:
{{EXPECTED_OUTPUT_FORMAT}}
```

**Handler Execution:**
- Let handler process request
- Monitor progress
- Capture handler output

---

## Phase 4: Aggregate Results

Collect handler output and format for user:

**Handler Response:**
{{HANDLER_OUTPUT}}

**Routing Metadata:**
- Request received: {{REQUEST_TIMESTAMP}}
- Classification: {{CLASSIFICATION_JSON}}
- Handler selected: {{SELECTED_HANDLER}}
- Routing decision: {{ROUTING_DECISION}}
- Execution time: {{EXECUTION_TIME}}

**Analytics Tracking:**
- Log routing decision for analysis
- Track handler performance metrics
- Identify routing pattern trends

**Final Output:**
{{FORMATTED_OUTPUT}}

---

## Decision Table Examples

**Example 1: Financial Query Routing**

| Domain | Complexity | Handler | Example |
|--------|-----------|---------|---------|
| finance | simple | @fintech-quick-analyst | "What's Q3 revenue?" |
| finance | moderate | @fintech-engineer | "Calculate YoY variance with favorability" |
| finance | complex | @fintech-engineer + @compliance-auditor | "Multi-entity consolidation with FX" |
| legal | any | @compliance-auditor | "Is this SOC2 compliant?" |
| technical | simple | /validation | "Run config validation" |
| technical | complex | @python-pro | "Refactor variance calculation" |

**Example 2: Model Selection Routing**

| Complexity | Model | Rationale |
|-----------|-------|-----------|
| simple | haiku | Fast, low-cost, sufficient for basic queries |
| moderate | sonnet | Balanced performance and accuracy |
| complex | opus | Deep analysis required |

---

## Success Criteria

Before marking complete:

- [ ] Input classified on all dimensions (domain, complexity, urgency, expertise)
- [ ] Decision table consulted
- [ ] Handler selected deterministically (same inputs = same handler)
- [ ] Routing rationale documented
- [ ] Handler invoked with full context
- [ ] Handler output captured
- [ ] Routing metadata logged for analytics
- [ ] Final output formatted and delivered

---

## Example Invocation

```bash
/{{COMMAND_NAME}} "{{EXAMPLE_REQUEST}}"
```

**Expected Flow:**
1. Classify → Domain: {{EXAMPLE_DOMAIN}}, Complexity: {{EXAMPLE_COMPLEXITY}}
2. Route → Handler: {{EXAMPLE_HANDLER}} (rationale: {{EXAMPLE_RATIONALE}})
3. Delegate → {{EXAMPLE_HANDLER}} processes request
4. Aggregate → Format output + routing metadata

**Example Output:**
```
Classification:
- Domain: {{EXAMPLE_DOMAIN}}
- Complexity: {{EXAMPLE_COMPLEXITY}}
- Handler: {{EXAMPLE_HANDLER}}

Response:
{{EXAMPLE_HANDLER_OUTPUT}}

(Routed to {{EXAMPLE_HANDLER}} because {{EXAMPLE_RATIONALE}})
```

---

## Anti-Patterns (DON'T DO THIS)

❌ Route based on implicit/learned behavior (non-deterministic)
❌ Skip classification step
❌ Invoke handler without context
❌ Forget to log routing decision
❌ Undocumented decision table

✅ Deterministic routing (same inputs = same handler every time)
✅ Explicit classification on all dimensions
✅ Decision table visible in command prompt
✅ Full context passed to handler
✅ Routing analytics for improvement

---

**This command enforces Anthropic Routing pattern: deterministic classification and specialized handler delegation.**
