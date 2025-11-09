# Meta-Skills Research - Comprehensive Findings

**Research Date:** 2025-11-09
**Purpose:** Research foundation for building skill-creator, command-creator, and agent-creator meta-skills
**Sources:** 20+ web searches (November 2025), internal repo analysis, external dependencies review

---

## Executive Summary

Meta-skills are self-referential capabilities that generate other skills, commands, and agents. This research synthesizes official Anthropic documentation, community best practices, and production patterns to inform implementation of three critical meta-skills for the FP&A Automation Assistant project.

**Key Findings:**
1. **Official Anthropic Structure** confirmed: Skills use `scripts/`, `references/`, `assets/` subdirectories
2. **Progressive Disclosure** is critical for context management (load metadata first, content on-demand)
3. **Human-in-Loop** checkpoints should be risk-based, not universal
4. **Tool Permissions** must follow least-privilege principle
5. **Quality Gates** automated validation essential for generated artifacts
6. **Template Engines** - Jinja2 and string formatting both viable for simple generation

---

## Part 1: Claude Code Architecture (Official Anthropic 2025)

### 1.1 Skills vs Commands vs Agents - Architectural Differences

**Source:** docs.claude.com, Daniel Miessler blog, YoungLeaders.tech (#95)

| Aspect | Skills | Commands | Agents |
|--------|--------|----------|--------|
| **Invocation** | Auto (keywords) | Explicit (`/command`) | Explicit (Task tool) |
| **Discovery** | Progressive disclosure | Direct injection | Separate context |
| **Context** | Load on-demand | Injected into thread | Independent window |
| **Structure** | Folder (SKILL.md + subdirs) | Single .md file | Single .md file |
| **Location** | `.claude/skills/{name}/` | `.claude/commands/{env}/` | `.claude/agents/{env}/` |
| **Use Case** | Reusable expertise | Triggered workflows | Specialized review |

**Critical Insight:** Skills ≠ Commands. Don't conflate them. Commands are explicit triggers, Skills are auto-invoked context.

### 1.2 Official Skills Directory Structure

**Source:** anthropics/skills GitHub, docs.claude.com

```
.claude/skills/{skill-name}/
├── SKILL.md               # Required - YAML frontmatter + instructions
├── scripts/               # Optional - Executable Python/Bash
├── references/            # Optional - Detailed documentation
└── assets/                # Optional - Templates, configs, binaries
```

**NOT official:**
- `workflows/` subdirectory (community pattern, not Anthropic standard)
- `context/` subdirectory (should be `references/`)
- Environment-based nesting (`.claude/skills/prod/{skill-name}`)

**Validation:** Check anthropics/skills repo - zero instances of `workflows/` or `context/` subdirectories.

### 1.3 Progressive Disclosure Pattern

**Source:** IxDF (2025), NN/G, LogRocket, docs.claude.com

**Definition:** Gradually reveal information as needed to reduce cognitive load.

**Implementation in Skills:**
1. Claude sees ONLY skill name + description initially (via YAML frontmatter)
2. Decides relevance based on user's task
3. Loads full SKILL.md only if relevant
4. Loads `references/`, `scripts/`, `assets/` only if specifically needed

**Benefits:**
- Doesn't consume context window until needed
- Scales to hundreds of skills without bloat
- Reduces latency for skill discovery

**Best Practices (2025):**
- Keep SKILL.md <200 lines
- Move detailed docs to `references/`
- Use hypertext links for drill-down
- Layer information hierarchically

### 1.4 Skills Frontmatter (YAML)

**Source:** anthropics/skills, docs.claude.com, internal templates

**Required fields:**
```yaml
---
name: skill-name              # kebab-case, lowercase + hyphens only
description: Brief description for auto-invocation (max 200 chars)
---
```

**Optional fields:**
```yaml
version: 1.0.0               # Semantic versioning
author: claude-code          # Creator identifier
tags: [tag1, tag2]           # Categorization
allowed-tools: [Read, Bash]  # Tool permissions (inherits if omitted)
model: sonnet                # Model override (sonnet/opus/haiku)
```

**Validation Requirements:**
- Name: kebab-case only (`^[a-z0-9-]+$`)
- Description: Clear, includes when to use
- YAML syntax: PyYAML safe_load compatible

---

## Part 2: Human-in-Loop Workflows

**Sources:** Permit.io, Parseur, Cloudflare, Microsoft, HumanLayer SDK

### 2.1 Checkpoint Placement Strategy

**Risk-Based Routing (2025 Best Practice):**
- High-risk: Destructive actions, financial approvals, compliance decisions
- Medium-risk: Configuration changes, data transformations
- Low-risk: Read-only operations, idempotent actions

**Anti-Pattern:** Reviewing every output defeats automation purpose

**Framework Recommendation:** LangGraph's `interrupt()` function for checkpoints

### 2.2 Approval Checkpoint Design

**Best Practices (November 2025):**

1. **Clear Communication:**
   - Explain WHY approval needed
   - Don't overload with raw JSON
   - Summarize context concisely

2. **Audit Trails:**
   - Record approval/edit/denial
   - Capture before/after versions
   - Track AI confidence scores
   - Log reviewer time spent

3. **Policy-Driven:**
   - Use declarative policy engines
   - Avoid hard-coded rules
   - Version control policies

4. **Error Handling:**
   - Handle reviewer unavailability
   - Define escalation paths
   - Graceful degradation

### 2.3 Integration with Meta-Skills

For meta-skills generating artifacts:
- **CHECKPOINT 1:** After spec generation, before file creation
- **CHECKPOINT 2:** After validation, before git commit
- **NO CHECKPOINT:** YAML parsing, convention checks (automated gates)

---

## Part 3: Tool Permissions & Security

**Sources:** Skywork.ai (Claude Skills Security 2025), SteveKinney, medianeth.dev

### 3.1 Principle of Least Privilege

**Deny-all Default:**
```
Start from deny-all → allowlist only necessary tools → require confirmations for sensitive actions
```

**Permission Sprawl = Fastest path to unsafe autonomy**

### 3.2 Tool Permission Tiers

**Source:** Internal `.claude/agents/code-reviewer.md`, official docs

| Agent Type | Tools | Rationale |
|------------|-------|-----------|
| **Read-only** (reviewers, auditors) | Read, Grep, Glob | Cannot modify code |
| **Research** | Read, Grep, Glob, WebFetch, WebSearch | Information gathering |
| **Code writers** | Read, Write, Edit, Bash, Glob, Grep | Full development |
| **Meta-skills** | Read, Write, Edit, Glob, Grep, Bash | Generate artifacts |

**Meta-Skill Specific:**
- `skill-creator`: Read, Write, Edit, Glob, Grep, Bash (needs file creation)
- `command-creator`: Read, Write, Edit, Glob, Grep (no Bash needed)
- `agent-creator`: Read, Write, Edit, Glob, Grep (no Bash needed)

### 3.3 Security Checklist for Generated Artifacts

- [ ] Validate YAML before writing files
- [ ] Check for path traversal attacks in skill names
- [ ] Sanitize user input in templates
- [ ] Prevent overwriting existing files without confirmation
- [ ] Git commits only after human approval

---

## Part 4: Template-Based Code Generation

**Sources:** Stack Overflow (2024), Strumenta, pymultigen, Jinja2 docs (2025)

### 4.1 Template Engine Selection

**Jinja2 vs. Mako (2025 Comparison):**

| Feature | Jinja2 | Mako |
|---------|--------|------|
| **Performance** | ~4.35s (benchmark) | ~4.83s (similar) |
| **Adoption** | Very high | High |
| **Security** | HTML escaping, sandbox | Less built-in |
| **Syntax** | Django-like | Python-embedded |

**Recommendation:** **String formatting** for simple templates (SKILL.md generation), **Jinja2** if complexity increases

**Rationale:** Meta-skills generate structured text (YAML + Markdown), not HTML. String `.format()` or f-strings sufficient.

### 4.2 Multi-File Generation Pattern

**Source:** pymultigen library

For generating multiple files (SKILL.md + subdirectories):
1. Plan directory structure first
2. Use `pathlib.Path.mkdir(parents=True, exist_ok=True)`
3. Generate files sequentially (not parallel to avoid race conditions)
4. Validate each file before moving to next

### 4.3 Template Best Practices (2025)

- Predefined templates ensure consistency
- Test generated code for correctness
- Follow domain frameworks for maintainability
- Minimize human error (typos, naming inconsistencies)

---

## Part 5: Quality Gates & Validation

**Sources:** Qodo.ai (Code Quality 2025), Sonar, InfoQ, Augment Code

### 5.1 Automated Validation Pipeline

**2025 Trend:** AI-generated code requires MORE validation, not less

**Quality Gate Layers:**
1. **Syntax Validation:** YAML parsing, Markdown linting
2. **Convention Enforcement:** kebab-case names, description clarity
3. **Structure Validation:** Required files present, correct subdirectories
4. **Semantic Validation:** Tool permissions minimal, anti-patterns avoided
5. **Security Validation:** No path traversal, no arbitrary code execution

### 5.2 Python Validation Tools (2025)

| Tool | Purpose | Meta-Skill Use |
|------|---------|----------------|
| **PyYAML** | YAML parsing | Validate frontmatter |
| **jsonschema** | Schema validation | Validate YAML against schema |
| **pathvalidate** | Path sanitization | Validate skill names |
| **Pylint** | Naming conventions | Check kebab-case (optional) |

### 5.3 Quality Gate Implementation

**Pre-Creation Checks:**
```python
def validate_skill_name(name: str) -> bool:
    """Validate skill name follows kebab-case convention."""
    import re
    return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name))

def validate_yaml_frontmatter(content: str) -> dict:
    """Parse and validate YAML frontmatter."""
    import yaml
    # Extract frontmatter between --- delimiters
    # Parse with yaml.safe_load()
    # Validate required fields present
    # Return parsed dict or raise exception
```

**Post-Creation Verification:**
- File exists at expected path
- YAML frontmatter parses successfully
- Required subdirectories created (if any)
- No TODO placeholders left in template

---

## Part 6: Git Automation

**Sources:** Baeldung, Adaltas (2021), FreeCodeCamp, MarkAICode (Git 4.0)

### 6.1 Conventional Commits (2025)

**Format:**
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types for meta-skills:**
- `feat:` - Add new skill/command/agent
- `fix:` - Fix bug in generated artifact
- `refactor:` - Update template structure
- `docs:` - Update meta-skill documentation

### 6.2 AI-Generated Commit Messages (Git 4.0)

**2025 Trend:** Git 4.0 analyzes code changes to generate descriptive commits

**For Meta-Skills:**
- After artifact creation, analyze files created
- Generate commit message based on artifact type
- Include artifact name in scope: `feat(skill): add variance-analyzer skill`

### 6.3 Python Git Automation

**Library:** `commitizen` + `pre-commit`
- `commitizen`: Validates conventional commit format
- `pre-commit`: Runs validation before git commit

**Meta-Skill Integration:**
```python
import subprocess

def git_commit_artifact(artifact_type: str, artifact_name: str, file_paths: list[str]):
    """Create conventional commit for generated artifact."""
    # Stage files
    subprocess.run(['git', 'add'] + file_paths)

    # Generate commit message
    msg = f"feat({artifact_type}): add {artifact_name} {artifact_type}"

    # Commit with message
    subprocess.run(['git', 'commit', '-m', msg])
```

---

## Part 7: Claude Sonnet 4.5 Capabilities

**Sources:** Anthropic (Sep 29, 2025), Medium, AWS Bedrock docs

### 7.1 Extended Thinking for Meta-Tasks

**Released:** September 29, 2025

**Key Capabilities:**
- Visible step-by-step reasoning blocks
- 30+ hours autonomous operation (up from 7 hours)
- Interleaved thinking (think between tool calls)
- Best coding model on SWE-bench Verified

**For Meta-Skills:**
- Enable extended thinking for complex spec generation
- Use interleaved thinking after reading templates
- Leverage 30-hour autonomy for batch skill creation

### 7.2 Performance on Code Generation

- **Terminal-Bench:** 61.3% success (first to break 60%)
- Advanced planning and system design
- Better instruction following

**Implication:** Sonnet 4.5 ideal for meta-skill reasoning (plan artifact structure before generating)

### 7.3 Pricing ($3/$15 per million tokens)

Same cost as predecessor, dramatically better performance

**Meta-Skill Cost Estimate:**
- Generating 1 skill: ~5K tokens input, 2K tokens output ≈ $0.045
- Affordable for batch generation

---

## Part 8: Directory Structure Validation

**Sources:** pathlib docs (Nov 8, 2025), pathvalidate (June 2025), Stack Overflow

### 8.1 Modern Python Approach (pathlib)

**Best Practice (2025):**
```python
from pathlib import Path

# Create nested directories
skill_dir = Path(f".claude/skills/{skill_name}")
skill_dir.mkdir(parents=True, exist_ok=True)

# Create subdirectories
(skill_dir / "scripts").mkdir(exist_ok=True)
(skill_dir / "references").mkdir(exist_ok=True)
(skill_dir / "assets").mkdir(exist_ok=True)
```

**Why pathlib?**
- Object-oriented, cleaner syntax
- Cross-platform (Windows/Linux/Mac)
- Introduced Python 3.4, now standard (2025)

### 8.2 Path Validation Library

**pathvalidate (June 15, 2025):**
- Sanitizes filenames and file paths
- Python 3.9+ compatible
- No external dependencies

```python
from pathvalidate import validate_filename, sanitize_filename

# Validate before creating
validate_filename(skill_name)  # Raises exception if invalid

# Sanitize user input
safe_name = sanitize_filename(user_input)
```

### 8.3 Directory Existence Checks

**Robust Pattern:**
```python
# Check if directory exists
if skill_dir.exists():
    # Prompt user for confirmation before overwriting
    # Or: raise FileExistsError with clear message
    pass

# Check specific file exists
if (skill_dir / "SKILL.md").exists():
    # Prevent overwriting without confirmation
    pass
```

---

## Part 9: YAML Validation Strategies

**Sources:** Stack Overflow, 23andMe/Yamale, PyKwalify, HitchDev

### 9.1 PyYAML + jsonschema Approach (Most Common)

**Rationale:** YAML has 1:1 mapping to JSON, reuse jsonschema validators

```python
import yaml
import jsonschema

# Load YAML
with open('skill.md', 'r') as f:
    content = f.read()

# Extract frontmatter (between --- delimiters)
# Parse YAML
frontmatter = yaml.safe_load(frontmatter_text)

# Define schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "pattern": "^[a-z0-9-]+$"},
        "description": {"type": "string", "maxLength": 200},
        "version": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["name", "description"]
}

# Validate
jsonschema.validate(frontmatter, schema)
```

### 9.2 Alternative Libraries

**Yamale (23andMe):**
- Schema and validator specifically for YAML
- Simpler syntax than jsonschema

**PyKwalify:**
- Supports Ruamel.yaml (YAML 1.2 spec)
- More actively developed

**Recommendation:** Start with PyYAML + jsonschema (most documentation, widest adoption)

### 9.3 YAML Gotchas (2025)

- YAML 1.1: `YES`/`NO` become booleans (unexpected)
- Solution: Use YAML 1.2 or quote strings
- `safe_load()` vs `load()`: Always use `safe_load()` (security)

---

## Part 10: Error Handling & Atomicity

**Sources:** Django docs (5.2), GeeksforGeeks, Bomberbot, cevheri.medium.com (2024)

### 10.1 Transaction-Like Pattern for File Operations

**Concept:** Database ACID principles applied to file generation

```python
from pathlib import Path
import shutil

def create_skill_atomic(skill_name: str, content: dict) -> Path:
    """Create skill atomically - all files or none."""

    temp_dir = Path(f".temp/{skill_name}")
    final_dir = Path(f".claude/skills/{skill_name}")

    try:
        # Create in temp location first
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Generate all files
        (temp_dir / "SKILL.md").write_text(content['skill'])
        (temp_dir / "scripts").mkdir()
        (temp_dir / "references").mkdir()
        # ... create all files

        # Validate generated files
        validate_skill_structure(temp_dir)

        # Move to final location (atomic on same filesystem)
        shutil.move(str(temp_dir), str(final_dir))

        return final_dir

    except Exception as e:
        # Rollback: delete temp directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        raise RuntimeError(f"Skill creation failed: {e}") from e
```

### 10.2 Error Handling Best Practices (2025)

1. **Catch Specific Exceptions:**
   ```python
   try:
       yaml.safe_load(content)
   except yaml.YAMLError as e:
       # Handle YAML parsing errors specifically
   except OSError as e:
       # Handle file system errors
   ```

2. **Provide User-Friendly Messages:**
   - Not: "YAMLError: mapping values are not allowed here"
   - Better: "Invalid YAML frontmatter in SKILL.md: check for proper indentation"

3. **Log with Context:**
   ```python
   logger.error({
       "operation": "create_skill",
       "skill_name": skill_name,
       "error": str(e),
       "timestamp": datetime.now(UTC).isoformat()
   })
   ```

---

## Part 11: Meta-Programming & Code Introspection

**Sources:** Python ast docs (Nov 8, 2025), metap, LibCST, Medium

### 11.1 When to Use AST vs. String Templates

**AST Manipulation:**
- Modifying existing Python code
- Adding decorators, type hints
- Complex transformations

**String Templates:**
- Generating new files from scratch
- Markdown, YAML, simple Python scripts
- **Recommended for meta-skills** (simpler, less error-prone)

### 11.2 Code Introspection for Validation

**Use Case:** Validate generated Python scripts before writing

```python
import ast

def validate_python_syntax(code: str) -> bool:
    """Check if generated Python code is syntactically valid."""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False
```

### 11.3 Type Checking Generated Code

**MyPy Integration:**
```python
import subprocess

def check_types(file_path: Path) -> bool:
    """Run mypy on generated Python file."""
    result = subprocess.run(
        ['mypy', str(file_path)],
        capture_output=True,
        text=True
    )
    return result.returncode == 0
```

---

## Part 12: Self-Improving Systems (Future-Proofing)

**Sources:** MIT Tech Review (Aug 2025), Medium (May 2025), Darwin Gödel Machine, OpenReview (ICLR 2025)

### 12.1 Self-Improving Coding Agents (2025 Breakthrough)

**Key Development:** Agents can autonomously edit themselves and improve performance

**Example:** Darwin Gödel Machine rewrites own code to improve on programming tasks

**SWE-Bench Results:** 17% → 53% improvement through self-modification

### 12.2 Meta-Learning Integration

**SMART Framework:** LLMs autonomously learn and select effective strategies

**Implication for Meta-Skills:**
- Meta-skills could analyze generated artifacts
- Learn which templates produce better results
- Self-improve generation patterns over time

### 12.3 Recursive Self-Improvement Potential

**Phase 0:** Meta-skills generate skills/commands/agents
**Phase 1:** Generated artifacts provide feedback on quality
**Phase 2:** Meta-skills learn from feedback, improve templates
**Phase 3:** Meta-skills generate better meta-skills

**Caution:** Keep human-in-loop for template modifications (safety gate)

---

## Part 13: Testing Generated Artifacts

**Sources:** testRigor, Qodo.ai, Parasoft (2025), ContextAI

### 13.1 Specification-Driven Testing

**Approach:** Write specs describing expected behavior, then test against spec

```python
def test_generated_skill_structure():
    """Verify generated skill follows official structure."""
    skill_dir = Path(".claude/skills/test-skill")

    assert (skill_dir / "SKILL.md").exists()
    assert (skill_dir / "scripts").is_dir()  # Optional, but if present must be dir
    assert (skill_dir / "references").is_dir()
    assert (skill_dir / "assets").is_dir()
```

### 13.2 Validation Tiers

**Tier 1: Syntax**
- YAML parses correctly
- Markdown valid
- Python syntax valid (if generating scripts)

**Tier 2: Structure**
- Required files present
- Correct directory layout
- No extra/unexpected files

**Tier 3: Semantics**
- Skill name follows conventions
- Description clear and concise
- Tool permissions minimal

**Tier 4: Integration**
- Skill discoverable by Claude
- Auto-invocation triggers correctly
- Commands execute without errors

### 13.3 Self-Generating Test Artifacts

**2025 Trend:** AI generates test cases for own code

**Meta-Skill Application:**
- Generate skill → Generate tests for that skill
- Validate tests pass before committing
- Ensures generated artifacts are immediately testable

---

## Part 14: Naming Conventions & Enforcement

**Sources:** Wikipedia (Snake case), FreeCodeCamp, Medium, Stack Overflow

### 14.1 Kebab-Case for Skills/Commands

**Pattern:** `^[a-z0-9]+(-[a-z0-9]+)*$`

**Examples:**
- ✅ `variance-analyzer`
- ✅ `code-reviewer`
- ✅ `skill-creator`
- ❌ `VarianceAnalyzer` (PascalCase)
- ❌ `variance_analyzer` (snake_case)
- ❌ `variance analyzer` (spaces)

### 14.2 Python Validation

```python
import re

def is_kebab_case(name: str) -> bool:
    """Validate string follows kebab-case convention."""
    pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'
    return bool(re.match(pattern, name))
```

### 14.3 Enforcement Tools

**Pylint Configuration:**
```ini
[NAMING]
# Enforce specific naming styles
function-naming-style=snake_case
class-naming-style=PascalCase
# No built-in kebab-case check (files/CLI args only)
```

**ESLint (for file names):**
- Can enforce kebab-case for file names
- Not applicable to Python module names (can't use hyphens)

**Recommendation:** Custom validation function in meta-skill

---

## Part 15: Internal Repo Patterns

### 15.1 Existing Skill Structure (variance-analyzer)

**Current Implementation:**
```
.claude/skills/variance-analyzer/
├── SKILL.md            # ✅ Correct
├── scripts/            # ✅ Official subdirectory
│   └── README.md       # Placeholder for future
├── references/         # ✅ Official subdirectory
│   └── README.md       # Placeholder
└── assets/             # ✅ Official subdirectory
    └── README.md       # Placeholder
```

**Observations:**
- Follows official Anthropic pattern
- Uses placeholder READMEs (good practice for empty dirs)
- No environment nesting (prod/) - correct

### 15.2 Existing Command Structure (variance-analysis)

**Current Implementation:**
```
.claude/commands/prod/variance-analysis.md
```

**YAML Frontmatter:**
```yaml
---
description: Budget vs actual variance analysis with human-in-loop checkpoints
---
```

**Observations:**
- Missing `argument-hint` field (recommended for autocomplete)
- Missing `model` field (inherits from conversation)
- Missing `allowed-tools` field (inherits from conversation)

**Improvement Opportunity:** Add optional fields for clarity

### 15.3 Existing Agent Structure (code-reviewer)

**Current Implementation:**
```yaml
---
name: code-reviewer
description: Independent code reviewer specializing in financial calculation verification
tools: [Read, Grep, Glob]
model: sonnet
---
```

**Observations:**
- ✅ Minimal tool permissions (read-only)
- ✅ Explicit model specification
- ✅ Clear, focused description
- **Template-ready:** Can be used as reference for agent-creator

### 15.4 Template Quality Assessment

**Skill Template:** ✅ Updated with official subdirectories
**Command Template:** ✅ Includes all optional fields
**Agent Template:** ✅ Includes tool permission guidance

**Conclusion:** Templates are comprehensive and aligned with official patterns

---

## Part 16: External Dependencies Patterns (HumanLayer)

**Source:** `external/humanlayer/` cloned repo

**Relevant Files:**
- `CLAUDE.md` - Behavioral instructions for AI
- `README.md` - Human-in-loop SDK overview
- `test-slash-commands.md` - Command testing patterns

**Key Takeaways:**
1. **Approval Decorators:** `@require_approval` pattern for functions
2. **Slack Integration:** Familiar tools for human interaction
3. **Checkpoint Placement:** Before destructive/irreversible actions
4. **Policy-Driven:** Declarative approval rules

**Application to Meta-Skills:**
- Present generated spec for approval before file creation
- Log all artifact creations for audit trail
- Allow "edit mode" before finalizing

---

## Part 17: Research Synthesis - Critical Decisions

### 17.1 Template Engine Decision

**Options Evaluated:**
1. Jinja2 (complex, overkill for YAML+Markdown)
2. Mako (similar to Jinja2)
3. String formatting (simple, sufficient)

**Decision:** **Python f-strings and .format()**

**Rationale:**
- Meta-skills generate structured text (YAML + Markdown), not HTML
- No complex control flow needed
- Simpler = fewer bugs
- Easier to maintain and understand

### 17.2 Validation Library Selection

**YAML:** `PyYAML` + `jsonschema`
**Paths:** `pathvalidate` + `pathlib`
**Naming:** Custom regex function

**Rationale:** Widely adopted, well-documented, no exotic dependencies

### 17.3 Tool Permissions for Meta-Skills

| Meta-Skill | Tools | Why |
|------------|-------|-----|
| skill-creator | Read, Write, Edit, Glob, Grep, Bash | Create dirs, files; research templates |
| command-creator | Read, Write, Edit, Glob, Grep | Create files, no dir nesting |
| agent-creator | Read, Write, Edit, Glob, Grep | Create files, no dir nesting |

**No WebFetch/WebSearch:** Meta-skills use internal templates, not web research

### 17.4 Human-in-Loop Checkpoints

**skill-creator:** 3 checkpoints
1. After gathering requirements
2. After generating spec (before file creation)
3. After validation (before git commit)

**command-creator:** 2 checkpoints
1. After gathering requirements
2. After generating spec (before file creation)

**agent-creator:** 2 checkpoints
1. After gathering requirements
2. After generating spec (before file creation)

**Rationale:** Approve specs BEFORE irreversible file operations

---

## Part 18: Success Metrics for Meta-Skills

### 18.1 Quality Metrics

**Correctness:**
- [ ] 100% of generated artifacts have valid YAML frontmatter
- [ ] 100% follow official Anthropic structure
- [ ] 100% pass convention checks (kebab-case names)

**Usability:**
- [ ] Generated skills auto-invoke correctly
- [ ] Generated commands execute without errors
- [ ] Generated agents load in separate context

**Efficiency:**
- [ ] Skill generation: <2 minutes user time
- [ ] Command generation: <1 minute user time
- [ ] Agent generation: <1 minute user time

### 18.2 Safety Metrics

**Security:**
- [ ] Zero path traversal vulnerabilities
- [ ] Zero arbitrary code execution risks
- [ ] All tool permissions validated

**Atomicity:**
- [ ] Zero partial artifact creation (all-or-nothing)
- [ ] Rollback works on any failure
- [ ] No corrupted git state

### 18.3 Adoption Metrics (Phase 2+)

**Usage:**
- How many skills created via skill-creator vs. manual?
- How many commands created via command-creator vs. manual?
- How many agents created via agent-creator vs. manual?

**Quality Over Time:**
- Do generated artifacts require manual fixes?
- Do users trust meta-skills for production artifacts?

---

## Part 19: Anti-Patterns to Avoid

### 19.1 Don't: Skip Validation

❌ Write files directly without YAML validation
✅ Parse and validate frontmatter BEFORE file I/O

### 19.2 Don't: Hard-Code Templates

❌ Embed templates as Python strings in meta-skill code
✅ Read from `.claude/templates/` directory for maintainability

### 19.3 Don't: Ignore Existing Files

❌ Overwrite existing skills without warning
✅ Check `Path.exists()` and prompt user for confirmation

### 19.4 Don't: Generate Incomplete Artifacts

❌ Create SKILL.md without required subdirectories
✅ Create full structure (SKILL.md + scripts/, references/, assets/) atomically

### 19.5 Don't: Auto-Commit Without Approval

❌ `git commit` immediately after generation
✅ Show generated files, get user approval, THEN commit

### 19.6 Don't: Use Unofficial Patterns

❌ Generate `workflows/` or `context/` subdirectories
✅ Use official `scripts/`, `references/`, `assets/` only

---

## Part 20: Recommendations for Implementation

### 20.1 Immediate Actions

1. **Create 3 meta-skills** following official patterns
2. **Use Python f-strings** for template generation (not Jinja2)
3. **Validate with PyYAML + jsonschema** before file creation
4. **Implement atomic file operations** with temp directory pattern
5. **Add human checkpoints** after spec generation

### 20.2 Testing Strategy

1. **Unit tests** for validation functions (YAML parsing, kebab-case, path sanitization)
2. **Integration tests** for end-to-end artifact generation
3. **Manual testing** by generating real skills/commands/agents

### 20.3 Documentation Requirements

1. **Update README.md** with meta-skill usage examples
2. **Create QUICK_START.md section** for skill creation workflow
3. **Document failure modes** and recovery procedures

### 20.4 Future Enhancements (Post-Phase 0)

1. **Self-improvement loop:** Analyze generated artifacts, improve templates
2. **Batch generation:** Create multiple skills from specifications
3. **Template versioning:** Track template evolution over time
4. **Quality metrics dashboard:** Track generated artifact quality

---

## Conclusion

Meta-skills represent a force multiplier for FP&A Automation Assistant development. By implementing skill-creator, command-creator, and agent-creator with:

- **Official Anthropic patterns** (scripts/, references/, assets/)
- **Robust validation** (YAML, naming, structure)
- **Human-in-loop checkpoints** (approval before irreversible actions)
- **Atomic file operations** (rollback on failure)
- **Minimal tool permissions** (least-privilege principle)

...we create a foundation for rapid, consistent, production-grade artifact generation that scales across Phase 2-5 implementation.

**Next Step:** Create `plan-meta-skills.md` with detailed implementation plan.

---

**Research Sources:**
- 20+ web searches (November 2025)
- Official Anthropic documentation
- Internal repo analysis (templates, existing artifacts)
- External dependencies (HumanLayer patterns)
- Community best practices (Daniel Miessler, Lee Hanchung, Simon Willison)

**Last Updated:** 2025-11-09
