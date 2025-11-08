# fpa-workflows

**Purpose:** Human-in-loop workflows - orchestrate multi-step processes with approval gates.

## Responsibilities

- Research → Plan → Implement → Verify workflows
- Approval gates (user reviews variance report before sending)
- Reconciliation workflows (flag unmapped accounts, wait for resolution)
- Multi-step orchestration with checkpoints

## Key Principle

**Checkpoints prevent automation from running unchecked.** Critical decisions require human approval.

## Dependencies

- **fpa-core** - Business logic
- **fpa-integrations** - External system access
- **loguru** - Structured logging
- **humanlayer** (optional) - Human approval patterns

## Human-in-Loop Pattern

```python
# Example workflow (future implementation)
from fpa_workflows.approval_gates import ApprovalGate

# 1. Run analysis
variance_report = calculate_variance(budget, actual)

# 2. Human checkpoint
gate = ApprovalGate("Review variance report before sending")
if gate.approved():
    send_to_management(variance_report)
else:
    revise_analysis(gate.feedback())
```

## Leveraged Patterns

From `external/humanlayer/`:
- Async approval workflows
- Keyboard-first interaction
- Context preservation across approvals

## Structure

```
src/fpa_workflows/
├── approval_gates/     # Human approval checkpoints
├── reconciliation/     # Data reconciliation workflows
└── review/             # Report review workflows
```

(Subdirectories will be created during implementation phase after spec approval)

## Workflow Phases

1. **Research** - Gather context without coding
2. **Plan** - Generate spec, get human approval
3. **Implement** - Build with checkpoints
4. **Verify** - Independent validation
