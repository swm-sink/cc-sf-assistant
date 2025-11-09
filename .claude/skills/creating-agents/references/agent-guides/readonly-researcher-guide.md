# Read-Only Researcher Agent Guide

**Purpose:** Comprehensive guide for creating researcher agents with web access (read+web tool tier, 5% of production agents).

**Based on:** 6 validated agents from awesome-claude-code-subagents + research patterns from Anthropic/Google

---

## Overview

### What is a Read-Only Researcher Agent?

A researcher agent investigates, discovers, and synthesizes information from codebases, documentation, and web sources WITHOUT modifying any files. It provides comprehensive research findings that inform decision-making and planning.

**Key Characteristics:**
- **Investigation-focused:** Discovery and analysis, not implementation
- **Read+web tool access:** Read, Grep, Glob, WebFetch, WebSearch (NO write/edit/bash)
- **Research structure:** 8-15 research areas with investigation capabilities
- **Source validation:** Cross-reference multiple sources for accuracy
- **Research workflow:** Discovery → Investigation → Reporting (3 phases)

### Tool Tier: Read + Web

Researchers have read-only access PLUS web research capabilities:

```yaml
tools:
  - Read       # Read files and documentation
  - Grep       # Search content across codebase
  - Glob       # Find files by pattern
  - WebFetch   # Fetch content from URLs
  - WebSearch  # Search the web for information
```

**Why read-only?**
- Researchers investigate and recommend, they don't implement
- Focus on discovery prevents scope creep
- Clear separation: research phase vs. implementation phase
- Safety: Can't accidentally modify files during investigation

**Why web access?**
- Research often requires external sources (docs, papers, best practices)
- Competitive intelligence needs web research
- Technology evaluation requires comparison of options
- Best practices research benefits from latest online resources

---

## Research Scope Definition

### Investigation Focus Areas

Each researcher should have **8-15 research areas**, each with **8-12 investigation capabilities**.

**Example Structure (competitive-analyst):**

```markdown
### Market Analysis

**Investigation capabilities:**
- Competitor product feature comparison
- Pricing model research across industry
- Market share and growth trend analysis
- Customer review sentiment analysis
- Feature gap identification relative to competitors
- Go-to-market strategy evaluation
- Strategic partnership and acquisition tracking
- Market positioning and differentiation analysis

### Technology Stack Research

**Investigation capabilities:**
- Framework and library evaluation (pros/cons)
- Performance benchmarking from published data
- Community adoption metrics (GitHub stars, npm downloads)
- Security vulnerability tracking (CVE databases)
- Licensing and compliance review
- Dependency analysis and risk assessment
- Migration path research for legacy systems
- Best practice documentation synthesis

[... 6-13 more research areas ...]
```

**Research Area Categories:**
- **Codebase exploration:** Understanding existing code structure
- **Technology evaluation:** Comparing frameworks, libraries, tools
- **Best practices:** Industry standards, design patterns
- **Competitive intelligence:** Market analysis, competitor research
- **Documentation synthesis:** Aggregating scattered information
- **Pattern discovery:** Finding similar implementations across large codebases

---

## Research Quality Checklist

### 8-Item Validation Checklist

Every researcher should have an 8-item research quality checklist.

**Example Checklist:**

```markdown
- [ ] Research questions clearly defined and scoped
- [ ] Multiple sources consulted and cross-referenced (minimum 3 per claim)
- [ ] Findings validated for accuracy (conflicting info investigated)
- [ ] Source credibility assessed (official docs prioritized)
- [ ] Confidence levels documented (high/medium/low per finding)
- [ ] Gaps in information explicitly identified
- [ ] Recommendations are specific and actionable
- [ ] Methodology and sources fully documented
```

**Checklist Principles:**
- **Source validation:** No single-source claims
- **Confidence levels:** Honest assessment of certainty
- **Gap identification:** Note what couldn't be found
- **Actionable:** Research leads to clear next steps
- **Reproducible:** Methodology documented for verification

---

## Investigation Workflow (3 Phases)

### Phase 1: Discovery

**Purpose:** Define research scope and identify information sources.

**Key Activities:**
1. **Define Research Questions:**
   - Clarify what information is needed
   - Identify primary and secondary research goals
   - Determine success criteria for research completeness

2. **Identify Sources:**
   - **Codebase:** Files to examine (use Glob to find, Read to analyze)
   - **Documentation:** README, docs/, inline comments
   - **Web sources:** Official docs, research papers, blog posts, forums
   - **Existing patterns:** Similar implementations (use Grep to find)

3. **Plan Investigation Strategy:**
   - Prioritize high-value sources (official docs first, then community)
   - Determine search patterns and keywords
   - Establish validation criteria (how to verify findings)

**Output:** Research plan with defined questions and source strategy.

### Phase 2: Investigation

**Purpose:** Systematically gather and validate information.

**Key Activities:**
1. **Gather Information:**
   - **Codebase:** Use Glob to locate files, Read to examine
   - **Search:** Use Grep for pattern matching across files
   - **Web:** Use WebFetch for specific URLs, WebSearch for discovery
   - **Cross-reference:** Compare multiple sources for accuracy

2. **Validate Sources:**
   - **Credibility assessment:** Official docs > reputable blogs > forums
   - **Recency check:** Prefer recent information (check dates)
   - **Conflict resolution:** When sources disagree, investigate why
   - **Citation tracking:** Document source URLs and file paths

3. **Synthesize Findings:**
   - **Organize:** Group by theme or research question
   - **Identify patterns:** Common recommendations across sources
   - **Note gaps:** What information is missing or unclear
   - **Assess confidence:** High (verified across 3+ sources), Medium (2 sources), Low (single source or uncertain)

**Output:** Validated findings organized by research question.

### Phase 3: Reporting

**Purpose:** Deliver actionable research insights.

**Key Activities:**
1. **Structure Findings:**
   - **Executive summary:** High-level takeaways (2-3 sentences)
   - **Detailed findings:** Organized by research question or category
   - **Supporting evidence:** Code snippets, quotes, URLs with context
   - **Uncertainties:** Highlight contradictions or gaps

2. **Provide Recommendations:**
   - **Translate findings:** Research → actionable insights
   - **Suggest next steps:** What to do based on research
   - **Identify further research:** Areas needing deeper investigation
   - **Propose alternatives:** Multiple options when applicable

3. **Document Methodology:**
   - **Sources consulted:** Full list with URLs/file paths
   - **Search strategies:** Keywords and patterns used
   - **Limitations:** Time constraints, access limitations
   - **Confidence assessment:** Overall research quality evaluation

**Output:** Comprehensive research report with sources and recommendations.

---

## Communication Protocol

### Structured Research Report Format

```json
{
  "research_summary": "High-level findings in 2-3 sentences",
  "sources_consulted": [
    "Source 1: Official React docs - hooks best practices",
    "Source 2: src/components/UserProfile.tsx (existing pattern)",
    "Source 3: Kent C. Dodds blog - testing React components"
  ],
  "key_insights": [
    "Insight 1: React hooks recommended over class components (official guidance)",
    "Insight 2: Existing codebase uses custom hooks for data fetching (found in 12 files)",
    "Insight 3: Testing Library preferred over Enzyme (community consensus 2023-2025)"
  ],
  "recommendations": [
    "Recommendation 1: Migrate class components to hooks incrementally",
    "Recommendation 2: Standardize on Testing Library for new tests"
  ],
  "confidence_level": "high",
  "gaps_identified": [
    "Gap 1: No clear pattern for global state management (Redux vs Context unclear)",
    "Gap 2: Performance optimization guidelines not documented"
  ]
}
```

**Confidence Levels:**
- **High:** Verified across 3+ credible sources, no contradictions
- **Medium:** 2 sources agree, or single authoritative source
- **Low:** Single source, or conflicting information, or outdated data

---

## Web Research Best Practices

### Source Credibility Hierarchy

**Tier 1 (Highest Credibility):**
- Official documentation (e.g., reactjs.org, docs.python.org)
- Peer-reviewed research papers
- Framework/library maintainer blogs

**Tier 2 (High Credibility):**
- Well-known industry experts (e.g., Kent C. Dodds, Dan Abramov)
- Major tech company engineering blogs (Google, Meta, Anthropic)
- Established community sites (Stack Overflow accepted answers)

**Tier 3 (Medium Credibility):**
- Individual developer blogs (verify claims)
- Community forum discussions (look for consensus)
- Medium/dev.to articles (check author credentials)

**Tier 4 (Low Credibility):**
- Anonymous forum posts
- Outdated content (>2 years old for fast-moving tech)
- Unverified tutorials

**Validation Strategy:**
- Always consult Tier 1 sources first
- Require Tier 2+ confirmation for critical claims
- Tier 3-4 sources need cross-validation (3+ agreeing sources)

### Web Search Strategies

**1. Technology Evaluation:**
```
Query: "React vs Vue 2025 comparison performance"
+ Check official benchmarks
+ Look for recent blog posts (2024-2025)
+ Review GitHub issue discussions
+ Cross-reference multiple comparisons
```

**2. Best Practices Research:**
```
Query: "PostgreSQL query optimization best practices"
+ Start with official PostgreSQL docs
+ Check expert blogs (2ndQuadrant, Citus Data)
+ Review Stack Overflow canonical answers
+ Validate with multiple sources
```

**3. Security Research:**
```
Query: "JWT authentication vulnerabilities 2025"
+ Check OWASP recommendations
+ Review CVE databases
+ Examine security researcher blogs
+ Verify with official library guidance
```

---

## Codebase Exploration Patterns

### Pattern 1: Architecture Discovery

**Goal:** Understand how existing codebase is organized.

**Workflow:**
1. **High-level structure:**
   ```bash
   # Use Glob to find directory structure
   ls -R project_root/
   ```

2. **Identify patterns:**
   ```bash
   # Use Grep to find common patterns
   grep -r "export class" src/
   grep -r "function" src/ --include="*.ts"
   ```

3. **Read key files:**
   ```bash
   # Use Read to examine critical files
   cat package.json
   cat tsconfig.json
   cat README.md
   ```

4. **Synthesize findings:**
   - Directory structure follows [pattern name]
   - Framework used: [framework name]
   - Key conventions: [list conventions]

### Pattern 2: Feature Implementation Discovery

**Goal:** Find how similar features are implemented.

**Workflow:**
1. **Search for similar features:**
   ```bash
   # Use Grep to find existing implementations
   grep -r "authentication" src/
   grep -r "useAuth" src/
   ```

2. **Examine implementation:**
   ```bash
   # Use Read to analyze specific files
   cat src/hooks/useAuth.ts
   cat src/components/LoginForm.tsx
   ```

3. **Document pattern:**
   - Authentication uses custom hook `useAuth`
   - Login form implements [specific pattern]
   - Token storage: [localStorage/sessionStorage/cookie]

### Pattern 3: Dependency Analysis

**Goal:** Understand external dependencies and their usage.

**Workflow:**
1. **List dependencies:**
   ```bash
   # Use Read to check package.json
   cat package.json
   ```

2. **Find usage examples:**
   ```bash
   # Use Grep to see how dependencies are used
   grep -r "import.*axios" src/
   grep -r "import.*lodash" src/
   ```

3. **Assess impact:**
   - Axios used in 15 files (heavy dependency)
   - Lodash only used for debounce (consider lighter alternative)

---

## Integration with Commands

### Researcher in RPIV Workflow

**Typical Usage:** Research phase of RPIV command.

**Example (from variance-analysis command):**
```markdown
### STEP 1: RESEARCH Phase

Investigate financial calculation requirements:

1. **Invoke Researcher:**
   @research-analyst, investigate:
   - How existing variance calculations work (codebase exploration)
   - FP&A best practices for variance analysis (web research)
   - Favorability logic patterns (find similar implementations)

2. **Review Research Findings:**
   - Examine sources consulted
   - Validate confidence levels
   - Identify gaps that need clarification

**CHECKPOINT 1:** Approve research findings before proceeding to Plan phase.
```

**Researcher Output:**
```json
{
  "research_summary": "Found 3 existing variance calculation patterns in codebase. Industry best practice is Actual - Budget with favorability based on account type.",
  "sources_consulted": [
    "src/calculations/variance.py (existing implementation)",
    "https://www.wallstreetprep.com/knowledge/variance-analysis/ (best practices)",
    "specs/spec.md (project requirements)"
  ],
  "key_insights": [
    "Existing code uses float (should be Decimal per spec.md)",
    "Favorability logic exists but undocumented",
    "Industry standard: Revenue up = favorable, Expense up = unfavorable"
  ],
  "recommendations": [
    "Migrate existing calculations to Decimal type",
    "Document favorability logic in code comments",
    "Add unit tests for edge cases (zero budget, negative values)"
  ],
  "confidence_level": "high",
  "gaps_identified": [
    "Multi-currency variance handling not documented"
  ]
}
```

---

## Common Patterns

### Pattern 1: Technology Evaluation

**Use Case:** Compare multiple options for a decision.

**Example:**
```
User: "Should we use PostgreSQL or MySQL for our application?"

Researcher Workflow:
1. Discovery:
   - Research questions: Performance, features, ecosystem, cost
   - Sources: Official docs, benchmarks, community consensus

2. Investigation:
   - PostgreSQL: Advanced features (JSON, full-text search, extensions)
   - MySQL: Simpler, faster for read-heavy workloads
   - Cross-reference: 5 comparison articles + official docs

3. Reporting:
   - Recommendation: PostgreSQL for complex queries and data integrity
   - Confidence: High (consistent across sources)
   - Gaps: Specific workload performance needs testing
```

### Pattern 2: Best Practices Discovery

**Use Case:** Find recommended approaches for a task.

**Example:**
```
User: "What are React testing best practices in 2025?"

Researcher Workflow:
1. Discovery:
   - Sources: Official React docs, Testing Library docs, expert blogs

2. Investigation:
   - Testing Library recommended over Enzyme (official guidance)
   - Integration tests > unit tests for components (Kent C. Dodds)
   - Avoid implementation detail testing (test behavior, not state)

3. Reporting:
   - 5 key best practices with sources
   - Examples from official docs
   - Confidence: High (official + expert consensus)
```

### Pattern 3: Codebase Understanding

**Use Case:** New team member understanding architecture.

**Example:**
```
User: "Explain how our authentication system works."

Researcher Workflow:
1. Discovery:
   - Use Grep to find auth-related files
   - Identify entry points (login, signup, logout)

2. Investigation:
   - Read auth hooks, API routes, middleware
   - Trace flow from login button to token storage
   - Note dependencies (JWT library, bcrypt)

3. Reporting:
   - Authentication flow diagram
   - Key files and their responsibilities
   - Identified security considerations
```

---

## Anti-Patterns

### ❌ Implementation During Research

**Problem:** Researcher attempts to fix issues found during investigation.

**Example:**
```markdown
# Researcher agent (WRONG)
"I found a bug in the authentication code. I'll fix it now..."
# Attempts to Edit file  ❌ FAIL - read-only tools
```

**Solution:** Report findings, recommend fixes, don't implement them.

### ❌ Single-Source Claims

**Problem:** Research based on single source without validation.

**Example:**
```markdown
# Researcher report (WRONG)
"PostgreSQL is 10x faster than MySQL (source: random blog post)"
Confidence: High  # ❌ Wrong - single unverified source
```

**Solution:** Cross-reference 3+ sources, use appropriate confidence level.

### ❌ Outdated Research

**Problem:** Using old information for fast-moving technology.

**Example:**
```markdown
# Researcher report (WRONG)
"React class components are the best approach (source: 2018 article)"
# ❌ Wrong - React hooks are standard since 2019
```

**Solution:** Check publication dates, prioritize recent sources (2023-2025 for web tech).

---

## Summary

**Key Takeaways:**

1. **Read-Only + Web:** Investigation without modification (Read, Grep, Glob, WebFetch, WebSearch)
2. **Source Validation:** Cross-reference 3+ sources, assess credibility
3. **Confidence Levels:** Honest assessment (high/medium/low)
4. **3-Phase Workflow:** Discovery → Investigation → Reporting
5. **Research, Not Implementation:** Findings and recommendations, not code changes
6. **5% Pattern:** Less common than domain specialists, distinct web research capability

**When to Create a Researcher:**
- Need codebase exploration without modification risk
- Technology evaluation requires web research
- Competitive intelligence or market analysis
- Best practices discovery from multiple sources

**Related Guides:**
- `domain-specialist-guide.md` - For implementation-focused agents (full tool access)
- `full-access-implementer-guide.md` - For review/audit agents (read-only, no web)

---

**This guide is based on 6 validated researcher agents and research patterns from Anthropic/Google. Last updated: 2025-11-09**
