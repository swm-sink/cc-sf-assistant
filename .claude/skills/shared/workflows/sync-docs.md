---
description: Validate documentation consistency across the project
model: sonnet
---

# Documentation Sync & Consistency Validator

Validates that all documentation files are consistent with each other and with the actual project state. Prevents documentation drift and confusion for AI agents.

## Purpose

Ensure that:
1. **spec.md ↔ plan.md** - Business requirements match technical implementation
2. **plan.md ↔ .claude/ structure** - Described directory structure exists
3. **README.md ↔ actual project** - README claims match reality
4. **Templates ↔ actual files** - Template documentation matches actual templates
5. **Version consistency** - All docs reference same version number

## Validation Checks

### 1. Version Number Consistency

Check that version numbers match across:
- README.md (header)
- pyproject.toml (`version = "X.Y.Z"`)
- spec.md (if version mentioned)
- plan.md (if version mentioned)

**Expected:** All should reference same version (e.g., `0.2.0-DEV`)

### 2. Directory Structure Consistency

Verify directories described in plan.md actually exist:
- `.claude/agents/dev/`, `.claude/agents/prod/`, `.claude/agents/shared/`
- `.claude/commands/dev/`, `.claude/commands/prod/`, `.claude/commands/shared/`
- `.claude/skills/dev/`, `.claude/skills/prod/`, `.claude/skills/shared/`
- `.claude/templates/`
- `scripts/core/`, `scripts/integrations/`, `scripts/workflows/`, `scripts/utils/`
- `data/samples/`
- `templates/`
- `docs/notebooks/`
- `config/credentials/`, `config/workflow-state/`
- `tests/`
- `external/` (with submodules)

**Action:** Read plan.md, extract directory structure, verify with `ls` commands.

### 3. Template Documentation Consistency

Verify `.claude/templates/README.md` accurately describes templates that exist:
- `.claude/templates/skills/SKILL_TEMPLATE.md`
- `.claude/templates/commands/COMMAND_TEMPLATE.md`
- `.claude/templates/agents/AGENT_TEMPLATE.md`
- `.claude/templates/workflows/TDD_WORKFLOW.md`
- `.claude/templates/workflows/RESEARCH_PLAN_IMPLEMENT_VERIFY.md`

**Action:** Read template README, verify all referenced files exist with `ls .claude/templates/**/*`

### 4. External Dependencies Consistency

Verify external dependencies mentioned in docs match `.gitmodules`:
- README.md lists: humanlayer, gspread, slidio, pyfpa, py-money, mcp-gdrive
- EXTERNAL_DEPENDENCIES.md documents same repos
- `.gitmodules` contains same submodules
- `external/` directory contains cloned repos

**Action:** Parse `.gitmodules`, compare with docs, verify with `ls external/`

### 5. Operational Decisions Consistency

Verify operational decisions in spec.md match implementation details in plan.md:
- Script versioning (git-based)
- Audit log (centralized in config/audit.log)
- Data validation (pre-checks)
- Template customization (generic → Life360)
- Error recovery (save state)
- Testing (sample data + pre-commit hooks)
- Deployment (single-user, local, Poetry)
- Security (simple credential storage)
- Documentation (Jupyter notebooks)
- Monitoring (future addition)

**Action:** Extract decisions from spec.md, verify matching sections exist in plan.md.

### 6. Command References Consistency

Verify commands referenced in docs actually exist or are planned:
- README.md mentions: `/prod:variance-analysis`, `/prod:monthly-close`, `/prod:consolidate`, `/dev:create-script`, `/dev:validate-script`, `/shared:help`, `/shared:sync-docs`
- QUICK_START.md mentions same commands
- Check if command files exist in `.claude/commands/dev/`, `.claude/commands/prod/`, `.claude/commands/shared/`

**Action:** Extract command references from docs, check `.claude/commands/**/*.md` files.

### 7. Dependency List Consistency

Verify dependencies listed in docs match `pyproject.toml`:
- README.md "External Dependencies" section
- QUICK_START.md installation instructions
- `pyproject.toml` `[tool.poetry.dependencies]` section

**Action:** Extract deps from README, compare with pyproject.toml.

### 8. Phase Status Consistency

Verify phase status in README.md matches current state:
- README.md shows: Phase 0 complete, Phase 1 in progress
- Verify no implementation code exists yet (only docs and templates)
- Confirm scripts/, .claude/agents/, .claude/commands/, .claude/skills/ are mostly empty

**Action:** Check for .py files in scripts/ (should be minimal/none), check .claude/ subdirs.

### 9. Success Metrics Consistency

Verify success metrics in README.md match spec.md:
- Both should list same metrics
- Both should use same "[TO BE MEASURED]" markers
- Both should reference same enforcement mechanisms

**Action:** Extract metrics from both files, compare.

### 10. Jupyter Notebook References

Verify notebook structure mentioned in docs matches plan.md:
- spec.md mentions 7 notebooks
- plan.md lists: 01_getting_started, 02_variance_analysis, 03_monthly_close, 04_board_deck, 05_consolidation, 06_custom_analysis, 07_google_integration
- README.md mentions "7 notebooks covering all workflows"

**Action:** Verify notebook count and names are consistent.

## Validation Report Format

```
📋 Documentation Sync Report

Version Consistency:
✅ README.md: 0.2.0-DEV
✅ pyproject.toml: 0.2.0
✅ All versions match (allowing -DEV suffix)

Directory Structure:
✅ .claude/agents/dev/ exists
✅ .claude/commands/prod/ exists
⚠️  scripts/core/ does not exist yet (expected for current phase)
✅ 8/10 directories verified

Template Documentation:
✅ All 5 templates exist and match README
✅ SKILL_TEMPLATE.md found
✅ COMMAND_TEMPLATE.md found
✅ AGENT_TEMPLATE.md found
✅ TDD_WORKFLOW.md found
✅ RESEARCH_PLAN_IMPLEMENT_VERIFY.md found

External Dependencies:
✅ .gitmodules contains 6 submodules
✅ All submodules match docs
✅ external/ directory has 6 repos

Operational Decisions:
✅ All 10 decisions in spec.md have matching plan.md sections
✅ Script versioning: git-based ✓
✅ Audit log: centralized ✓
✅ Data validation: pre-checks ✓
✅ ... (all 10 checks)

Command References:
⚠️  /prod:variance-analysis mentioned but .claude/commands/prod/variance-analysis.md does not exist (expected for current phase)
⚠️  6/8 commands not yet implemented (Phase 1 in progress)

Dependency List:
✅ README.md dependencies match pyproject.toml
✅ 12 dependencies verified

Phase Status:
✅ README shows Phase 0 complete, Phase 1 in progress
✅ No premature implementation (scripts/ mostly empty)
✅ Status matches actual project state

Success Metrics:
✅ README metrics match spec.md
✅ All [TO BE MEASURED] markers consistent

Jupyter Notebooks:
✅ 7 notebooks planned in spec.md
✅ 7 notebooks documented in plan.md
⚠️  docs/notebooks/ directory does not exist yet (expected for current phase)

Overall Status: ✅ CONSISTENT (3 expected warnings for Phase 1)

Expected Warnings:
- Implementation directories don't exist yet (Phase 1 in progress)
- Commands not implemented yet (planned for Phase 2+)
- Notebooks not created yet (planned for Phase 2+)

Critical Issues: None

Recommendation: Documentation is consistent. Proceed with implementation.
```

## Workflow

1. Run all 10 validation checks sequentially
2. Collect results (✅ pass, ⚠️ warning, ❌ error)
3. Generate validation report
4. If critical issues found: Stop and alert user
5. If only warnings: Explain why they're expected
6. If all pass: Confirm documentation is synchronized

## Error Handling

**Critical Issues (block implementation):**
- Version numbers don't match across docs
- Operational decisions in spec.md missing from plan.md
- External dependencies listed don't match .gitmodules
- README directory structure fundamentally different from plan.md

**Warnings (acceptable for current phase):**
- Directories planned but not yet created
- Commands documented but not yet implemented
- Scripts mentioned but not yet written

## Usage

```bash
# Validate all documentation
/shared:sync-docs

# Expected output if consistent:
# 📋 Running documentation sync validation...
# ✅ CONSISTENT - All documentation is synchronized
#
# Expected output if drift detected:
# ⚠️  DRIFT DETECTED - 3 inconsistencies found
# [Details of inconsistencies]
```

## Implementation Notes

**DO NOT IMPLEMENT CODE YET - This is specification only**

When implementing (Phase 1):
1. Use Read tool to extract info from docs
2. Use Bash (`ls`, `find`) to verify directories exist
3. Use Grep to search for version numbers, command references
4. Generate structured report
5. Present findings to user

**Files to Read:**
- README.md
- spec.md
- plan.md
- pyproject.toml
- .gitmodules
- .claude/templates/README.md
- QUICK_START.md
- EXTERNAL_DEPENDENCIES.md

**Bash Commands to Run:**
- `ls -la .claude/agents/dev/`
- `ls -la .claude/commands/prod/`
- `find scripts/ -name "*.py"`
- `find .claude/templates/ -name "*.md"`
- `ls -la external/`

---

**Created:** 2025-11-08
**Purpose:** Prevent documentation drift and ensure AI agents have consistent context
**Frequency:** Run before starting any new phase of implementation
