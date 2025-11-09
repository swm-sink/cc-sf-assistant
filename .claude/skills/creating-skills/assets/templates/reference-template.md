# Reference Template

**Purpose:** Template for reference-type skills (API docs, quick lookup tables, cheat sheets)

**Use when:** Creating documentation for APIs, command references, or structured data

**Structure:** 5 sections (Overview → Quick Reference → Detailed Reference → Examples → Progressive Disclosure)

**Key feature:** Table-heavy, scannable, optimized for quick lookup

---

## Template Structure

```markdown
---
name: {{SKILL_NAME}}
description: {{CSO_OPTIMIZED_DESCRIPTION}}
---

# {{SKILL_TITLE}}

## Overview

**Purpose:** {{ONE_SENTENCE_PURPOSE}}

**What this reference covers:**
- {{COVERAGE_1}}
- {{COVERAGE_2}}
- {{COVERAGE_3}}

**What this reference doesn't cover:**
- {{NON_COVERAGE_1}}
- {{NON_COVERAGE_2}}

**When to use this reference:**
- {{USE_CASE_1}}
- {{USE_CASE_2}}
- {{USE_CASE_3}}

---

## Quick Reference

### {{QUICK_REF_SECTION_1}}

| {{COLUMN_1}} | {{COLUMN_2}} | {{COLUMN_3}} | {{COLUMN_4}} |
|--------------|--------------|--------------|--------------|
| {{ROW_1_COL_1}} | {{ROW_1_COL_2}} | {{ROW_1_COL_3}} | {{ROW_1_COL_4}} |
| {{ROW_2_COL_1}} | {{ROW_2_COL_2}} | {{ROW_2_COL_3}} | {{ROW_2_COL_4}} |
| {{ROW_3_COL_1}} | {{ROW_3_COL_2}} | {{ROW_3_COL_3}} | {{ROW_3_COL_4}} |
| {{ROW_4_COL_1}} | {{ROW_4_COL_2}} | {{ROW_4_COL_3}} | {{ROW_4_COL_4}} |

### {{QUICK_REF_SECTION_2}}

| {{COLUMN_1}} | {{COLUMN_2}} | {{COLUMN_3}} |
|--------------|--------------|--------------|
| {{ROW_1_COL_1}} | {{ROW_1_COL_2}} | {{ROW_1_COL_3}} |
| {{ROW_2_COL_1}} | {{ROW_2_COL_2}} | {{ROW_2_COL_3}} |
| {{ROW_3_COL_1}} | {{ROW_3_COL_2}} | {{ROW_3_COL_3}} |
| {{ROW_4_COL_1}} | {{ROW_4_COL_2}} | {{ROW_4_COL_3}} |

### {{QUICK_REF_SECTION_3}}

**{{SUBSECTION_1}}**
```{{LANGUAGE}}
{{CODE_SNIPPET_1}}
```

**{{SUBSECTION_2}}**
```{{LANGUAGE}}
{{CODE_SNIPPET_2}}
```

**{{SUBSECTION_3}}**
```{{LANGUAGE}}
{{CODE_SNIPPET_3}}
```

---

## Detailed Reference

### {{DETAILED_SECTION_1}}

#### {{ITEM_1_NAME}}

**Signature:** `{{ITEM_1_SIGNATURE}}`

**Purpose:** {{ITEM_1_PURPOSE}}

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| {{PARAM_1_NAME}} | {{PARAM_1_TYPE}} | {{PARAM_1_REQUIRED}} | {{PARAM_1_DEFAULT}} | {{PARAM_1_DESC}} |
| {{PARAM_2_NAME}} | {{PARAM_2_TYPE}} | {{PARAM_2_REQUIRED}} | {{PARAM_2_DEFAULT}} | {{PARAM_2_DESC}} |

**Returns:** {{ITEM_1_RETURNS}}

**Raises:** {{ITEM_1_RAISES}}

**Example:**
```{{LANGUAGE}}
{{ITEM_1_EXAMPLE}}
```

#### {{ITEM_2_NAME}}

**Signature:** `{{ITEM_2_SIGNATURE}}`

**Purpose:** {{ITEM_2_PURPOSE}}

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| {{PARAM_1_NAME}} | {{PARAM_1_TYPE}} | {{PARAM_1_REQUIRED}} | {{PARAM_1_DEFAULT}} | {{PARAM_1_DESC}} |
| {{PARAM_2_NAME}} | {{PARAM_2_TYPE}} | {{PARAM_2_REQUIRED}} | {{PARAM_2_DEFAULT}} | {{PARAM_2_DESC}} |

**Returns:** {{ITEM_2_RETURNS}}

**Raises:** {{ITEM_2_RAISES}}

**Example:**
```{{LANGUAGE}}
{{ITEM_2_EXAMPLE}}
```

{{ADDITIONAL_ITEMS}}

### {{DETAILED_SECTION_2}}

#### {{CATEGORY_1}}

| {{COL_1}} | {{COL_2}} | {{COL_3}} | {{COL_4}} |
|-----------|-----------|-----------|-----------|
| {{ROW_1_COL_1}} | {{ROW_1_COL_2}} | {{ROW_1_COL_3}} | {{ROW_1_COL_4}} |
| {{ROW_2_COL_1}} | {{ROW_2_COL_2}} | {{ROW_2_COL_3}} | {{ROW_2_COL_4}} |

**Notes:**
- {{NOTE_1}}
- {{NOTE_2}}

#### {{CATEGORY_2}}

| {{COL_1}} | {{COL_2}} | {{COL_3}} | {{COL_4}} |
|-----------|-----------|-----------|-----------|
| {{ROW_1_COL_1}} | {{ROW_1_COL_2}} | {{ROW_1_COL_3}} | {{ROW_1_COL_4}} |
| {{ROW_2_COL_1}} | {{ROW_2_COL_2}} | {{ROW_2_COL_3}} | {{ROW_2_COL_4}} |

**Notes:**
- {{NOTE_1}}
- {{NOTE_2}}

{{ADDITIONAL_CATEGORIES}}

---

## Examples

### Example 1: {{EXAMPLE_1_SCENARIO}}

**Use case:** {{EXAMPLE_1_USE_CASE}}

**Code:**
```{{LANGUAGE}}
{{EXAMPLE_1_CODE}}
```

**Output:**
```{{OUTPUT_FORMAT}}
{{EXAMPLE_1_OUTPUT}}
```

**Explanation:** {{EXAMPLE_1_EXPLANATION}}

### Example 2: {{EXAMPLE_2_SCENARIO}}

**Use case:** {{EXAMPLE_2_USE_CASE}}

**Code:**
```{{LANGUAGE}}
{{EXAMPLE_2_CODE}}
```

**Output:**
```{{OUTPUT_FORMAT}}
{{EXAMPLE_2_OUTPUT}}
```

**Explanation:** {{EXAMPLE_2_EXPLANATION}}

### Example 3: {{EXAMPLE_3_SCENARIO}}

**Use case:** {{EXAMPLE_3_USE_CASE}}

**Code:**
```{{LANGUAGE}}
{{EXAMPLE_3_CODE}}
```

**Output:**
```{{OUTPUT_FORMAT}}
{{EXAMPLE_3_OUTPUT}}
```

**Explanation:** {{EXAMPLE_3_EXPLANATION}}

{{ADDITIONAL_EXAMPLES}}

---

## Progressive Disclosure

**For comprehensive reference, see:**
- `references/{{REFERENCE_DOC_1}}.md` - {{REFERENCE_DOC_1_PURPOSE}}
- `references/{{REFERENCE_DOC_2}}.md` - {{REFERENCE_DOC_2_PURPOSE}}

**Related references:**
- {{RELATED_REFERENCE_1}}
- {{RELATED_REFERENCE_2}}

**External documentation:**
- {{EXTERNAL_DOC_1}}
- {{EXTERNAL_DOC_2}}

**Migration guides:**
- {{MIGRATION_GUIDE_1}}
- {{MIGRATION_GUIDE_2}}

**Changelog:**
- {{CHANGELOG_REFERENCE}}
```

---

## Placeholder Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{SKILL_NAME}}` | Kebab-case skill directory name | `bash-commands-reference`, `python-api-reference` |
| `{{CSO_OPTIMIZED_DESCRIPTION}}` | Description with lookup keywords and use cases | "Quick reference for Bash commands, use when searching for file operations, text processing, or system utilities" |
| `{{SKILL_TITLE}}` | Human-readable title | "Bash Commands Reference", "Python API Reference" |
| `{{ONE_SENTENCE_PURPOSE}}` | Concise purpose | "Quick lookup for common Bash commands and their options" |
| `{{COVERAGE_X}}` | What's documented | "File operations (read, write, search)" |
| `{{NON_COVERAGE_X}}` | What's excluded | "Advanced scripting (use Bash skill instead)" |
| `{{USE_CASE_X}}` | When to consult | "Need to find files by pattern" |
| `{{QUICK_REF_SECTION_X}}` | Quick table category | "File Operations", "Text Processing" |
| `{{COLUMN_X}}` | Table column header | "Command", "Description", "Example", "Options" |
| `{{ROW_X_COL_X}}` | Table cell content | "`grep pattern file`", "Search file for pattern" |
| `{{SUBSECTION_X}}` | Quick snippet category | "Read file", "Write file" |
| `{{LANGUAGE}}` | Code language | `bash`, `python`, `json`, `yaml` |
| `{{CODE_SNIPPET_X}}` | Quick code example | `cat file.txt`, `python script.py` |
| `{{DETAILED_SECTION_X}}` | Detailed reference category | "Core Functions", "Utility Methods" |
| `{{ITEM_X_NAME}}` | API item name | "`calculate_variance()`", "`read_sheet()`" |
| `{{ITEM_X_SIGNATURE}}` | Function signature | `calculate_variance(actual: Decimal, budget: Decimal) -> Decimal` |
| `{{ITEM_X_PURPOSE}}` | What item does | "Calculate variance between actual and budget" |
| `{{PARAM_X_NAME}}` | Parameter name | `actual`, `budget`, `account_type` |
| `{{PARAM_X_TYPE}}` | Parameter type | `Decimal`, `str`, `Optional[int]` |
| `{{PARAM_X_REQUIRED}}` | Required? | `Yes`, `No` |
| `{{PARAM_X_DEFAULT}}` | Default value | `None`, `0`, `"revenue"` |
| `{{PARAM_X_DESC}}` | Parameter description | "Actual amount from financial system" |
| `{{ITEM_X_RETURNS}}` | Return value | `Decimal` (variance amount) |
| `{{ITEM_X_RAISES}}` | Exceptions raised | `ValueError` if invalid account_type |
| `{{ITEM_X_EXAMPLE}}` | Usage example | `variance = calculate_variance(Decimal("1000"), Decimal("950"))` |
| `{{CATEGORY_X}}` | Detailed table category | "Error Codes", "Configuration Options" |
| `{{COL_X}}` | Detailed table column | "Code", "Message", "Resolution" |
| `{{NOTE_X}}` | Additional note | "Use Decimal for currency precision" |
| `{{EXAMPLE_X_SCENARIO}}` | Example title | "Basic Usage", "Advanced Filtering", "Error Handling" |
| `{{EXAMPLE_X_USE_CASE}}` | Example context | "Calculate variance for revenue account" |
| `{{EXAMPLE_X_CODE}}` | Example code | Full code example |
| `{{OUTPUT_FORMAT}}` | Output language | `json`, `text`, `python` |
| `{{EXAMPLE_X_OUTPUT}}` | Example output | Result of running code |
| `{{EXAMPLE_X_EXPLANATION}}` | What example shows | "Demonstrates proper Decimal usage for financial calculations" |
| `{{REFERENCE_DOC_X}}` | Supporting document | "complete-api-reference", "configuration-guide" |
| `{{REFERENCE_DOC_X_PURPOSE}}` | Document purpose | "Comprehensive API documentation with all methods" |
| `{{RELATED_REFERENCE_X}}` | Related reference | "Command-line reference", "Configuration reference" |
| `{{EXTERNAL_DOC_X}}` | External resource | "Official Python docs", "Bash manual" |
| `{{MIGRATION_GUIDE_X}}` | Version migration | "Migrating from v1 to v2" |
| `{{CHANGELOG_REFERENCE}}` | Version history | "`references/changelog.md`" |

---

## CSO Optimization Guidelines

**Reference skills should include:**

1. **Lookup keywords** (what users search for)
   - Action verbs: "find", "list", "search", "check"
   - Item types: "command", "function", "option", "parameter"
   - Example: "find command for searching files", "list available options"

2. **Domain-specific terms** (technical vocabulary)
   - Technology names: "Bash", "Python", "API"
   - Concept names: "file operations", "text processing"
   - Example: "grep command", "variance calculation function"

3. **Use case keywords** (when to consult)
   - Task descriptions: "when X", "need to Y"
   - Example: "when searching files", "need to calculate variance"

4. **Quick lookup phrases** (reference-specific)
   - "quick reference", "cheat sheet", "command list"
   - Example: "Bash command cheat sheet", "API quick reference"

**Target CSO score: ≥0.7** (measured by validate_cso.py)

**CRITICAL:** Reference skills auto-invoke during lookup tasks, not during implementation.

---

## Validation Checklist

When using this template, validate:

- [ ] YAML frontmatter present with name + CSO-optimized description
- [ ] All 5 sections present (Overview → Quick Reference → Detailed Reference → Examples → Progressive Disclosure)
- [ ] Quick Reference has ≥2 tables or code snippet categories
- [ ] Detailed Reference provides comprehensive documentation for ≥3 items
- [ ] Parameter tables include Name | Type | Required | Default | Description
- [ ] Examples has ≥3 concrete scenarios with code + output + explanation
- [ ] Progressive Disclosure references comprehensive docs in references/
- [ ] Line count <200 (main SKILL.md, comprehensive reference in references/)
- [ ] Tables formatted correctly (readable, aligned)
- [ ] Code examples tested and working
- [ ] CSO score ≥0.7

---

**Template Version:** 1.0
**Last Updated:** 2025-11-09
**Skill Type:** Reference (API docs, quick lookup, cheat sheets)
**Complexity:** Low (primarily documentation and tables)
