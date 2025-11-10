# Validation Rules Reference

**Purpose:** Complete specification of all 15 validation rules.

---

## Critical Rules (ERROR)

### 1. YAML Frontmatter Completeness
**Validator:** `yaml-validator.py`
**Pass Criteria:**
- Skills: name, type, auto_invoke, cso_score present
- Agents: name, tool_tier, description present
- Commands: name, workflow_type, description present

### 2. CSO Score Thresholds
**Validator:** `cso-scorer.py`
**Pass Criteria:**
- Critical skills (hook-factory, financial-quality-gate): ≥0.8
- High priority (other meta-skills): ≥0.7
- Standard (remaining): ≥0.6

### 3. File Naming Conventions
**Validator:** `naming-validator.py`
**Pass Criteria:**
- kebab-case for all files and directories
- SKILL.md (exactly) for skills
- .md extension for agents/commands

### 4. Directory Structure
**Validator:** `structure-validator.py`
**Pass Criteria:**
- Skills: SKILL.md + README.md required
- references/ and templates/ recommended
- SKILL.md ≤200 lines (progressive disclosure)

### 5. No Duplication
**Validator:** Manual review
**Pass Criteria:** Same content not repeated across components

---

## Important Rules (WARNING)

### 6-10. Structure and Integration
- references/ exists for complex skills
- Progressive disclosure (≤200 lines)
- Cross-references resolve (no broken links)
- Tool tier enforcement (read_only for validators)
- Workflow type correctness (matches pattern)

---

## Quality Rules (INFO)

### 11-15. Quality and Completeness
- Templates syntactically correct
- Integration tested
- Documentation complete (README.md)
- Example quality (4-5 examples)
- No broken external links

---

**Lines:** 58
**Last Updated:** 2025-11-10
