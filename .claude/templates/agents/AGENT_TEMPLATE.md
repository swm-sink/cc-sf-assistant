---
name: agent-name
description: Brief description of when this agent should be invoked
tools: Read, Grep, Glob  # Optional - inherits all tools if omitted; use minimal tools for focused agents
model: sonnet  # Optional - sonnet, opus, haiku, or inherit
---

# Agent Name

## Role
Define the agent's specific role and expertise.

## Capabilities
- Capability 1
- Capability 2
- Capability 3

## Constraints
- Constraint 1 (e.g., "Read-only - cannot modify code")
- Constraint 2 (e.g., "Focus only on financial calculations")
- Constraint 3 (e.g., "Must provide evidence for all claims")

## Workflow

### Phase 1: [Name]
Description of what happens in this phase.

### Phase 2: [Name]
Description of what happens in this phase.

### Phase 3: [Name]
Description of what happens in this phase.

## Output Format
Specify the expected output format:
```
[Expected structure]
```

## Tool Permissions Guide
- **Read-only agents** (reviewers, auditors): Read, Grep, Glob
- **Research agents**: Read, Grep, Glob, WebFetch, WebSearch
- **Code writers**: Read, Write, Edit, Bash, Glob, Grep
- **Documentation agents**: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch

---

**Source:** Based on Claude Code subagents best practices (2025)
**Last Updated:** 2025-11-08
