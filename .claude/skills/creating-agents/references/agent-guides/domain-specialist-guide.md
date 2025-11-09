# Domain Specialist Agent Guide

**Purpose:** Comprehensive guide for creating domain specialist agents using the PRIMARY template (86% of production agents).

**Based on:** 100+ validated agents from awesome-claude-code-subagents + 12-Factor Agents principles

---

## Overview

### What is a Domain Specialist Agent?

A domain specialist agent is a constrained expert with deep knowledge in a specific technology, domain, or discipline. It provides comprehensive guidance within well-defined boundaries while maintaining strict separation from areas outside its expertise.

**Key Characteristics:**
- **Constrained expertise:** Deep knowledge in specific domain (financial, Python, data analysis, etc.)
- **Full tool access:** Read, Write, Edit, Bash, Glob, Grep (can implement solutions)
- **Comprehensive coverage:** 8-15 domain areas with 8-12 capabilities each
- **Quality-focused:** 8-item verification checklist for all deliverables
- **Production-ready:** Follows best practices from 100+ validated agents

### Tool Tier: Full Access

Domain specialists have full tool access because they implement solutions:

```yaml
tools:
  - Read      # Read files and documentation
  - Write     # Create new files
  - Edit      # Modify existing files
  - Bash      # Execute commands (tests, builds, deployments)
  - Glob      # Find files by pattern
  - Grep      # Search content across codebase
```

**Why full access?**
- Domain specialists implement solutions, not just analyze
- Need to create files (new features, configurations, scripts)
- Need to modify files (refactoring, bug fixes, enhancements)
- Need to execute code (run tests, verify implementations, build systems)

---

## Domain Scope Definition

### Constrained Expertise

**Principle:** A domain specialist should be an expert in a SPECIFIC area, not a generalist.

**Good Examples:**
- `fintech-analyst` - Financial technology systems (payments, compliance, fraud detection)
- `python-pro` - Python programming (language features, ecosystem, best practices)
- `postgres-expert` - PostgreSQL databases (query optimization, schema design, replication)
- `react-specialist` - React framework (components, hooks, performance, testing)

**Bad Examples (Too Broad):**
- `software-engineer` - Too general, no constrained expertise
- `web-developer` - Covers too many technologies (HTML, CSS, JS, frameworks, backend)
- `data-professional` - Vague, could be analyst, engineer, scientist, etc.

### Domain Area Structure

Each domain specialist should have **8-15 domain areas**, each with **8-12 specific capabilities**.

**Example Structure (fintech-analyst):**

```markdown
### Payment Processing Systems

**Core capabilities:**
- ACH and wire transfer implementation
- Card network integration (Visa, Mastercard, Amex)
- Real-time payment systems (RTP, FedNow)
- Payment reconciliation and settlement
- Chargeback handling and dispute resolution
- PCI-DSS compliance for card data
- Payment gateway integration (Stripe, Braintree, Adyen)
- Multi-currency and foreign exchange handling

### Regulatory Compliance

**Core capabilities:**
- Know Your Customer (KYC) verification workflows
- Anti-Money Laundering (AML) transaction monitoring
- Sanctions screening (OFAC, EU, UN lists)
- Consumer protection regulations (TILA, EFTA, Reg E)
- Financial reporting requirements (SAR, CTR)
- Privacy regulations (GDPR, CCPA) for financial data
- Audit trail and record retention requirements
- Regulatory filing automation

[... 6-13 more areas ...]
```

**Benefits of Structure:**
- **Discoverability:** Users know exactly what expertise is available
- **Boundaries:** Clear scope prevents out-of-domain requests
- **Comprehensiveness:** 8-12 bullets ensure thorough coverage
- **Consistency:** 8-15 areas provides balanced depth vs. breadth

---

## Quality Checklist Design

### 8-Item Verification Checklist

Every domain specialist should have an 8-item quality checklist that ALL deliverables must pass.

**Checklist Principles:**
- **Universal:** Applies to all tasks within domain
- **Actionable:** Each item can be verified objectively
- **Comprehensive:** Covers quality, security, performance, documentation
- **Non-negotiable:** No shortcuts under time pressure

**Example Checklist (python-pro):**

```markdown
- [ ] Requirements understood and validated against specifications
- [ ] Edge cases identified and handled (null, empty, boundary values)
- [ ] Best practices applied (PEP 8, type hints, docstrings)
- [ ] Code quality meets standards (no code smells, clear logic)
- [ ] Security considerations addressed (input validation, no hardcoded secrets)
- [ ] Performance implications assessed (time/space complexity documented)
- [ ] Documentation complete (README, docstrings, usage examples)
- [ ] Tests cover critical paths (unit tests for core functions)
```

**Example Checklist (fintech-analyst):**

```markdown
- [ ] Financial calculations use Decimal type (never float)
- [ ] Regulatory compliance verified (applicable regulations documented)
- [ ] Audit trail complete (timestamp, user, source, operation logged)
- [ ] Data integrity validated (reconciliation checks, totals match)
- [ ] Edge cases handled (zero amounts, negative values, NULL handling)
- [ ] Security controls applied (encryption, access control, PII protection)
- [ ] Error handling comprehensive (specific errors, user-friendly messages)
- [ ] Testing complete (unit tests, integration tests, edge cases)
```

**Customization Guidelines:**
- Adapt to domain-specific quality standards
- Include regulatory/compliance items if applicable
- Cover security, performance, documentation, testing
- Make each item specific and verifiable

---

## Development Workflow (3 Phases)

### Phase 1: Analysis

**Purpose:** Understand the problem before implementing.

**Key Activities:**
1. **Understand Requirements:**
   - Read all provided context (files, specs, constraints)
   - Identify explicit and implicit requirements
   - Clarify ambiguities before proceeding (ask questions)

2. **Assess Scope:**
   - Determine which domain areas apply
   - Identify dependencies and integration points
   - Flag anything outside domain scope (recommend other specialists)

3. **Research Current State:**
   - Examine existing implementations (if applicable)
   - Review relevant patterns and best practices within domain
   - Note technical debt or limitations

**Output:** Clear understanding of what needs to be done and how it fits within domain expertise.

### Phase 2: Implementation

**Purpose:** Execute with systematic rigor.

**Key Activities:**
1. **Design First:**
   - Document approach before coding
   - Consider edge cases and error handling
   - Validate design against requirements

2. **Implement Incrementally:**
   - Break into logical phases
   - Test each component before integration
   - Maintain clear audit trail of decisions

3. **Validate Continuously:**
   - Run relevant validation checks
   - Verify against quality checklist
   - Ensure production-ready quality

**Output:** Working implementation that passes all quality checks.

### Phase 3: Excellence

**Purpose:** Deliver beyond functional requirements.

**Key Activities:**
1. **Optimize:**
   - Review for performance opportunities
   - Refactor for clarity and maintainability
   - Document complex logic

2. **Document:**
   - Explain design decisions
   - Provide usage examples
   - Note limitations or assumptions

3. **Future-Proof:**
   - Consider extensibility
   - Identify potential improvements
   - Suggest monitoring or validation approaches

**Output:** Production-ready deliverable with comprehensive documentation.

---

## Communication Protocol

### Structured Response Format

Domain specialists should respond using consistent structure:

```json
{
  "analysis": "Brief assessment of the request",
  "approach": "Recommended strategy (2-3 sentences)",
  "considerations": [
    "Key factor 1 affecting implementation",
    "Key factor 2 to be aware of",
    "Key factor 3 requiring attention"
  ],
  "next_steps": [
    "Action 1 to take",
    "Action 2 to take",
    "Action 3 to take"
  ]
}
```

**Benefits:**
- **Clarity:** User knows what agent will do
- **Transparency:** Approach and considerations are explicit
- **Actionable:** Next steps are concrete
- **Consistent:** Same format for all requests

**When to Break Format:**
- Long-form explanations (use markdown structure instead)
- Code implementations (provide code + explanation)
- Error reports (use severity levels: CRITICAL, WARNING, INFO)

---

## Integration with Commands

### Agent as Worker, Command as Orchestrator

**Principle:** Agents do NOT coordinate other agents. Commands coordinate agents.

**Correct Pattern:**
```markdown
# In .claude/commands/prod/variance-analysis.md (RPIV command)

### STEP 4: VERIFY Phase

Run comprehensive verification:

1. **Financial Validation:**
   Invoke @fintech-analyst to verify:
   - Decimal precision maintained
   - Regulatory compliance met
   - Audit trail complete

2. **Code Quality Review:**
   Invoke @code-reviewer to verify:
   - Code standards met
   - Security considerations addressed
   - Tests comprehensive
```

**Incorrect Pattern (Anti-Pattern):**
```markdown
# In .claude/agents/fintech-analyst.md (WRONG - agent coordinating agents)

### Workflow Phase 2: Implementation

After completing financial calculations:

1. Invoke @code-reviewer to verify code quality  # ❌ WRONG
2. Invoke @security-auditor to check for vulnerabilities  # ❌ WRONG
3. Report results to human  # ✅ Correct
```

**Why This Matters:**
- **Context isolation:** Each agent has separate context window
- **12-Factor Agents Factor 10:** Small, focused agents with single responsibility
- **Simplicity:** Commands manage complexity, agents execute tasks
- **Maintainability:** Clear separation of orchestration vs. execution

---

## Common Patterns

### Pattern 1: Analysis → Recommendation

**Use Case:** User asks for advice, not implementation.

**Example:**
```
User: "Should we use PostgreSQL or MongoDB for our financial transaction system?"

Agent Response:
{
  "analysis": "Financial transactions require ACID guarantees, audit trails, and complex queries. This favors relational databases.",
  "approach": "PostgreSQL is strongly recommended for financial systems due to transaction guarantees and data integrity.",
  "considerations": [
    "MongoDB lacks multi-document ACID transactions (before v4.0)",
    "Financial auditing requires SQL-style joins and aggregations",
    "Regulatory compliance often mandates relational data models"
  ],
  "next_steps": [
    "Design schema with proper normalization for audit trails",
    "Implement row-level security for data isolation",
    "Set up point-in-time recovery for compliance"
  ]
}
```

### Pattern 2: Implementation with Verification

**Use Case:** User requests a feature implementation.

**Example:**
```
User: "Implement a function to calculate compound interest with daily compounding."

Agent Workflow:
1. Analysis Phase:
   - Understand requirements (principal, rate, time, compounding frequency)
   - Identify domain area: Financial Calculations
   - Note precision requirement: Use Decimal type

2. Implementation Phase:
   - Write function with Decimal precision
   - Handle edge cases (zero principal, negative values)
   - Add comprehensive docstring

3. Excellence Phase:
   - Add unit tests with various scenarios
   - Document formula used
   - Provide usage examples

4. Deliver with quality checklist confirmation
```

### Pattern 3: Domain Boundary Enforcement

**Use Case:** User asks question outside domain scope.

**Example:**
```
User (to @fintech-analyst): "How do I optimize this React component?"

Agent Response:
"This question is outside my domain expertise (financial technology systems). For React optimization, I recommend invoking @react-specialist or @frontend-engineer who have deep expertise in:
- Component rendering optimization
- Memoization strategies
- Performance profiling tools

If you have financial domain questions about this component (e.g., 'How should we calculate interest in this component?'), I can help with that specific aspect."
```

---

## Best Practices

### 1. Stay Within Domain Boundaries

**Do:**
- Provide comprehensive answers within your 8-15 domain areas
- Recommend other specialists for out-of-scope questions
- Collaborate by delivering your part to human/command (not other agents)

**Don't:**
- Claim expertise outside defined domain areas
- Attempt to answer questions in unfamiliar domains
- Coordinate other agents (commands do orchestration)

### 2. Maintain Quality Standards

**Do:**
- Run through 8-item checklist for EVERY deliverable
- No shortcuts under time pressure
- Document edge case handling
- Provide production-ready code (tests, docs, error handling)

**Don't:**
- Skip checklist items for "simple" tasks
- Rationalize lower quality ("it's just a prototype")
- Deliver untested code
- Assume requirements (clarify first)

### 3. Communicate Clearly

**Do:**
- Use structured response format for consistency
- Provide specific, actionable next steps
- Document assumptions explicitly
- Explain complex logic with comments and docs

**Don't:**
- Provide vague recommendations ("improve code quality")
- Assume user knowledge level (explain domain concepts)
- Use jargon without explanation
- Skip documentation ("code is self-documenting")

---

## Anti-Patterns

### ❌ Generalist Agent

**Problem:** Agent claims expertise in too many unrelated domains.

**Example:**
```yaml
# Bad: Too broad, no constrained expertise
name: full-stack-engineer
description: Expert in frontend, backend, databases, DevOps, security, mobile, cloud, ML, data science...
```

**Solution:** Create multiple focused agents instead.

### ❌ Coordinator Agent

**Problem:** Agent coordinates other agents.

**Example:**
```markdown
## Workflow

1. Analyze requirements
2. Delegate to @backend-dev for API implementation  # ❌ Wrong
3. Delegate to @frontend-dev for UI implementation  # ❌ Wrong
4. Coordinate integration  # ❌ Wrong
```

**Solution:** Use a COMMAND to coordinate agents. Agents execute tasks, commands orchestrate.

### ❌ Checklist Shortcuts

**Problem:** Skipping quality checklist under pressure.

**Example:**
```markdown
# Agent thinking: "This is urgent, I'll skip the tests for now..."  # ❌ Wrong
```

**Solution:** Quality checklist is non-negotiable. If time-constrained, deliver partial implementation that passes checklist, not full implementation that fails it.

---

## Examples from Production Agents

### fintech-engineer (awesome-claude-code-subagents)

**Domain Areas (11 total):**
1. Payment Systems
2. Fraud Detection
3. Regulatory Compliance
4. Account Management
5. Transaction Processing
6. Reconciliation & Settlement
7. Reporting & Analytics
8. Security & Encryption
9. API Integration
10. Data Migration
11. Performance Optimization

**Quality Checklist:**
- Financial precision (Decimal types)
- Regulatory compliance verified
- Audit trails complete
- Security controls applied
- Error handling comprehensive
- Tests cover edge cases
- Documentation complete
- Performance benchmarked

### python-pro (awesome-claude-code-subagents)

**Domain Areas (12 total):**
1. Core Language Features
2. Standard Library
3. Package Management
4. Testing & Quality
5. Performance Optimization
6. Async Programming
7. Data Structures
8. Type System
9. Debugging Tools
10. Build & Deployment
11. Best Practices
12. Ecosystem Integration

**Quality Checklist:**
- PEP 8 compliance
- Type hints comprehensive
- Docstrings complete
- Error handling proper
- Tests cover edge cases
- Performance acceptable
- Dependencies minimal
- Security reviewed

---

## Summary

**Key Takeaways:**

1. **Constrained Expertise:** Deep knowledge in specific domain (8-15 areas)
2. **Full Tool Access:** Can implement solutions (Read, Write, Edit, Bash, Glob, Grep)
3. **Quality-Focused:** 8-item checklist for all deliverables
4. **3-Phase Workflow:** Analysis → Implementation → Excellence
5. **Worker, Not Orchestrator:** Agents execute tasks, commands coordinate
6. **86% Pattern:** Most common agent type in production (PRIMARY template)

**When to Create a Domain Specialist:**
- Need expert implementation in specific technology/domain
- Require full tool access (read, write, execute)
- Want comprehensive coverage of domain (8-15 areas)
- Production-ready quality needed (quality checklist enforcement)

**Related Guides:**
- `readonly-researcher-guide.md` - For investigation-focused agents (read+web tools)
- `full-access-implementer-guide.md` - For review/audit agents (read-only tools)

---

**This guide is based on analysis of 100+ production agents and 12-Factor Agents principles. Last updated: 2025-11-09**
