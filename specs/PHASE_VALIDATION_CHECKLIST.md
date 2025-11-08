# Phase Validation Checklist

**Purpose:** Quality gates and exit criteria for each development phase

**Usage:** Review this checklist before moving to next phase. ALL items must pass.

---

## Phase 0: Spec & Planning ✅ COMPLETE

### Documentation
- [x] spec.md defines business requirements (WHAT to build)
- [x] plan.md defines technical implementation (HOW to build)
- [x] CLAUDE.md defines AI behavioral rules
- [x] README.md updated with architecture overview
- [x] QUICK_START.md provides installation guide
- [x] All docs synchronized (run `/shared:sync-docs`)

### Architecture Decisions
- [x] Claude Code-native architecture confirmed
- [x] Dev/Prod/Shared environment split defined
- [x] External dependencies strategy defined (submodules)
- [x] Deployment model defined (single-user, local)
- [x] 10 operational decisions documented

### Infrastructure
- [x] Directory structure created (.claude/, scripts/, data/, etc.)
- [x] .gitignore configured (credentials, audit logs excluded)
- [x] Git submodules added (humanlayer, gspread, slidio, pyfpa, py-money)
- [x] pyproject.toml configured with Poetry
- [x] Sample data specification created

### Exit Criteria
- [x] User approval on spec.md
- [x] User approval on plan.md
- [x] User approval on architecture decisions
- [x] All documentation consistent

---

## Phase 0A: Meta-Skills (BEFORE Phase 1) ⏳ IN PROGRESS

### Meta-Skill Creation
- [ ] skill-creator meta-skill implemented
- [ ] command-creator meta-skill implemented
- [ ] agent-creator meta-skill implemented
- [ ] All meta-skills tested with sample artifacts

### Integration Specifications
- [ ] specs/adaptive/ADAPTIVE_API_SPEC.md created
- [ ] specs/databricks/DATABRICKS_API_SPEC.md created
- [ ] specs/google/GOOGLE_WORKSPACE_SPEC.md created

### Documentation Updates
- [ ] spec.md updated: POST-CLOSE focus (not month-end close)
- [ ] plan.md updated: 95% coverage enforcement
- [ ] CLAUDE.md updated: Architecture principles extracted
- [ ] EXTERNAL_DEPENDENCIES.md reviewed and updated

### Quality Gates
- [ ] Phase validation checklist (this file) added to spec.md reference
- [ ] Pre-commit hook design validated
- [ ] TDD workflow template tested
- [ ] All docs synchronized (run `/shared:sync-docs`)

### Exit Criteria
- [ ] All 3 meta-skills successfully generate artifacts
- [ ] Integration specs complete
- [ ] All documentation updated and consistent
- [ ] User approval to proceed to Phase 1

---

## Phase 1: Infrastructure Setup

### Python Environment
- [ ] Poetry virtual environment created (`poetry install`)
- [ ] All dependencies installed successfully
- [ ] Import verification passes (pandas, gspread, openpyxl, etc.)
- [ ] Pre-commit hooks installed (`scripts/utils/install_hooks.py`)

### Git Configuration
- [ ] Pre-commit hook runs pytest, mypy, ruff, bandit
- [ ] Pre-commit hook blocks versioned filenames (_v2.py, etc.)
- [ ] Pre-commit hook enforces 95%+ test coverage
- [ ] Git workflow tested (commit, push)

### Sample Data
- [ ] data/samples/budget_2025.xlsx created (50 accounts)
- [ ] data/samples/actuals_nov_2025.xlsx created (with variances)
- [ ] Department-level sample files created
- [ ] Edge case data included (zero budget, negatives, NULL)

### Templates
- [ ] templates/variance_report.xlsx created
- [ ] templates/board_deck.pptx created
- [ ] Template metadata documented

### Shared Skills
- [ ] decimal-precision-enforcer skill created
- [ ] audit-trail-enforcer skill created
- [ ] Both skills tested and auto-invoke correctly

### Testing Infrastructure
- [ ] tests/ directory structure finalized
- [ ] pytest configuration validated
- [ ] Coverage reporting configured (95%+ requirement)
- [ ] Test fixtures for sample data created

### Exit Criteria
- [ ] `poetry run pytest` passes (even with 0 tests initially)
- [ ] Pre-commit hook runs all quality checks successfully
- [ ] Sample data loads without errors
- [ ] All shared skills auto-invoke correctly
- [ ] Documentation updated and synchronized

---

## Phase 2: Dev Workflows

### Meta-Skills Validation
- [ ] skill-creator used to generate 2+ production skills
- [ ] command-creator used to generate 2+ production commands
- [ ] agent-creator used to generate 2+ production agents
- [ ] All generated artifacts follow templates

### Core Dev Skills
- [ ] python-best-practices skill created
- [ ] financial-script-generator skill created
- [ ] tdd-enforcer skill created
- [ ] All skills tested with real script generation

### Dev Agents
- [ ] script-generator agent created
- [ ] script-validator agent created
- [ ] code-reviewer agent created (independent review)
- [ ] All agents tested with sample scripts

### Dev Commands
- [ ] /dev:create-script command created and tested
- [ ] /dev:validate-script command created and tested
- [ ] /dev:review-code command created and tested
- [ ] Human approval checkpoints validated

### TDD Workflow
- [ ] RED-GREEN-REFACTOR-VALIDATE cycle enforced
- [ ] Test-first development verified
- [ ] Coverage threshold enforced (95%+)
- [ ] Independent review required before approval

### Sample Script Generation
- [ ] Generate 1 simple script (e.g., account mapper)
- [ ] Generate 1 complex script (e.g., variance calculator)
- [ ] Both scripts pass all quality gates
- [ ] Both scripts have 95%+ test coverage

### Exit Criteria
- [ ] /dev:create-script successfully generates robust scripts
- [ ] All generated scripts use Decimal for currency
- [ ] All generated scripts have type hints
- [ ] All generated scripts pass independent review
- [ ] 95%+ test coverage enforced automatically
- [ ] User approval on dev workflow quality

---

## Phase 3: Core Scripts - Excel

### Core Calculation Scripts
- [ ] scripts/core/variance.py created (Decimal precision)
- [ ] scripts/core/consolidation.py created
- [ ] scripts/core/favorability.py created
- [ ] scripts/core/account_mapper.py created
- [ ] All scripts have 95%+ test coverage
- [ ] All scripts pass mypy type checking

### Integration Scripts
- [ ] scripts/integrations/excel_reader.py created
- [ ] scripts/integrations/excel_writer.py created
- [ ] scripts/integrations/template_loader.py created
- [ ] All integration scripts tested with sample data

### Utility Scripts
- [ ] scripts/utils/logger.py created (audit trail)
- [ ] scripts/utils/validator.py created (data validation)
- [ ] scripts/utils/config_loader.py created
- [ ] All utilities tested independently

### Test Suite
- [ ] tests/test_variance.py (edge cases: zero budget, negatives, NULL)
- [ ] tests/test_consolidation.py
- [ ] tests/test_favorability.py
- [ ] tests/test_excel_reader.py
- [ ] tests/test_excel_writer.py
- [ ] Overall coverage ≥95%

### Financial Precision Verification
- [ ] NO float usage in any currency calculations
- [ ] Decimal precision to 2+ decimal places verified
- [ ] Audit logging in all transformations
- [ ] Edge cases tested (division by zero, negative values, NULL)

### Exit Criteria
- [ ] All core scripts implemented and tested
- [ ] 95%+ test coverage achieved
- [ ] Zero financial calculation errors
- [ ] Audit trail complete for all operations
- [ ] Pre-commit hooks pass on all commits
- [ ] User approval on script quality

---

## Phase 4: Prod Workflows - Excel

### Prod Skills
- [ ] variance-analyzer skill created
- [ ] account-mapper skill created
- [ ] report-generator skill created
- [ ] All skills tested with real data

### Prod Agents
- [ ] finance-reviewer agent created (validates reports)
- [ ] data-validator agent created (pre-checks)
- [ ] reconciler agent created (unmatched accounts)
- [ ] All agents tested with sample workflows

### Prod Commands
- [ ] /prod:variance-analysis command created
- [ ] /prod:monthly-close command created (Excel-only initially)
- [ ] /prod:consolidate command created
- [ ] All commands include human approval checkpoints

### Workflow Scripts
- [ ] scripts/workflows/variance_report.py created
- [ ] scripts/workflows/monthly_close.py created
- [ ] scripts/workflows/consolidation_report.py created
- [ ] All workflows tested end-to-end

### Data Validation
- [ ] Pre-execution validation reports implemented
- [ ] Column presence checks
- [ ] Data type validation
- [ ] Non-null requirement checks
- [ ] Anomaly flagging (no silent data drops)

### Error Recovery
- [ ] Workflow state saving implemented
- [ ] Resume-on-failure tested
- [ ] User presented with resume/restart choice
- [ ] State files in config/workflow-state/

### Audit Logging
- [ ] All workflows log to config/audit.log
- [ ] Log format: JSON with timestamp, user, operation, inputs, outputs
- [ ] Audit log parsing and review tools created
- [ ] Reproducibility verified (same inputs → same outputs)

### Exit Criteria
- [ ] /prod:variance-analysis completes end-to-end successfully
- [ ] Human approval checkpoints work correctly
- [ ] Error recovery tested and working
- [ ] Audit trail complete and parseable
- [ ] Zero financial calculation errors
- [ ] User acceptance testing passed

---

## Phase 5: Google Integration

### Integration Specifications
- [ ] specs/google/GOOGLE_WORKSPACE_SPEC.md finalized
- [ ] API authentication strategy tested
- [ ] Credential management documented

### Google Scripts
- [ ] scripts/integrations/gsheet_reader.py created
- [ ] scripts/integrations/gsheet_writer.py created
- [ ] scripts/integrations/gslides_generator.py created
- [ ] All scripts tested with real Google API

### Credential Management
- [ ] config/credentials/README.md documented
- [ ] Service account setup guide created
- [ ] OAuth flow documented (if needed)
- [ ] Credentials validated (not committed to git)

### Google Skills
- [ ] gsheet-sync skill created
- [ ] board-deck-generator skill created
- [ ] Both skills tested with sample data

### Google Commands
- [ ] /prod:sync-to-gsheets command created
- [ ] /prod:generate-board-deck command created
- [ ] Both commands tested end-to-end

### Workflow Updates
- [ ] scripts/workflows/variance_report.py updated (Google Sheets output)
- [ ] scripts/workflows/board_deck_generator.py created
- [ ] Both workflows tested with real Google Workspace

### Exit Criteria
- [ ] Google Sheets read/write working
- [ ] Google Slides generation working
- [ ] Credentials secure (git-ignored)
- [ ] All workflows support Excel AND Google
- [ ] User acceptance testing passed

---

## Phase 6: Post-Close Integration (Adaptive & Databricks)

### Integration Specifications
- [ ] specs/adaptive/ADAPTIVE_API_SPEC.md finalized
- [ ] specs/databricks/DATABRICKS_API_SPEC.md finalized
- [ ] API authentication tested for both

### Adaptive Integration
- [ ] scripts/integrations/adaptive_client.py created
- [ ] Data export from Adaptive tested
- [ ] Data upload to Adaptive tested
- [ ] XML format handling implemented

### Databricks Integration
- [ ] scripts/integrations/databricks_client.py created
- [ ] SQL Statement Execution API tested
- [ ] Parameterized queries implemented
- [ ] Result set parsing implemented

### Post-Close Workflow
- [ ] scripts/workflows/post_close_review.py created
- [ ] Workflow: close → review → adjustments → finalize → upload
- [ ] Stakeholder review checkpoint implemented
- [ ] Adjustment cycle tested

### Skills & Commands
- [ ] adaptive-uploader skill created
- [ ] databricks-query skill created
- [ ] /prod:post-close-review command created
- [ ] All tested end-to-end

### Exit Criteria
- [ ] Data successfully pulled from Adaptive and Databricks
- [ ] Variance analysis completed
- [ ] Stakeholder review workflow tested
- [ ] Adjustments applied and finalized
- [ ] Data uploaded back to Adaptive
- [ ] Reports generated in Google Slides/Sheets
- [ ] User acceptance testing passed

---

## Phase 7: Life360 Branding & Polish

### Life360 Customization
- [ ] templates/life360/ populated with branded templates
- [ ] Life360 logo and assets added
- [ ] Company-specific account mapping configured
- [ ] Department structure configured

### Documentation Polish
- [ ] All 7 Jupyter notebooks created:
  - [ ] 01_getting_started.ipynb
  - [ ] 02_variance_analysis.ipynb
  - [ ] 03_monthly_close.ipynb
  - [ ] 04_board_deck.ipynb
  - [ ] 05_consolidation.ipynb
  - [ ] 06_custom_analysis.ipynb
  - [ ] 07_google_integration.ipynb
- [ ] All notebooks tested with sample data
- [ ] docs/user-guides/ finalized (troubleshooting, FAQ, best practices)

### Performance Optimization
- [ ] Large dataset testing (>1000 rows)
- [ ] Performance profiling completed
- [ ] Optimization applied where needed
- [ ] Performance expectations documented

### Final Quality Gates
- [ ] All tests passing (95%+ coverage)
- [ ] All documentation synchronized (`/shared:sync-docs`)
- [ ] All commands documented in README.md
- [ ] QUICK_START.md validated with fresh install
- [ ] Zero security vulnerabilities (bandit scan)

### Exit Criteria
- [ ] End-to-end workflows tested with Life360 data
- [ ] All 7 Jupyter notebooks executable
- [ ] User can complete monthly workflow independently
- [ ] Documentation complete and accurate
- [ ] Project ready for production use
- [ ] User final approval and sign-off

---

## Continuous Quality Gates (All Phases)

### Git Workflow
- [ ] All commits pass pre-commit hooks
- [ ] Conventional commit messages used
- [ ] No versioned filenames committed (_v2.py, etc.)
- [ ] No credentials committed

### Testing
- [ ] 95%+ test coverage maintained
- [ ] All tests pass before commits
- [ ] Edge cases tested (zero, negatives, NULL)
- [ ] Integration tests passing

### Financial Precision
- [ ] Decimal-only for currency (enforced by skills)
- [ ] Type hints on all functions (enforced by mypy)
- [ ] Audit logging on all transformations
- [ ] No silent data drops or modifications

### Documentation
- [ ] README.md up to date
- [ ] spec.md and plan.md synchronized
- [ ] CLAUDE.md behavioral rules followed
- [ ] `/shared:sync-docs` passes

### Code Quality
- [ ] mypy type checking passes
- [ ] ruff linting passes
- [ ] bandit security scanning passes
- [ ] Independent code review for financial scripts

---

## Usage

**Before Starting New Phase:**
```bash
# 1. Review checklist for current phase
# 2. Verify all items completed
# 3. Run validation
/shared:sync-docs

# 4. Run tests
poetry run pytest --cov=scripts

# 5. Get user approval
# Present checklist status to user
# Request approval to proceed

# 6. Move to next phase
```

**During Phase:**
- Reference checklist frequently
- Mark items complete as you go
- Don't skip quality gates
- Document deviations (with user approval)

**After Phase Complete:**
- Verify ALL items checked
- Run full validation suite
- Update documentation
- Get user sign-off
- Commit phase completion

---

**References:**
- spec.md - Business requirements
- plan.md - Technical implementation
- CLAUDE.md - AI behavioral rules

**Last Updated:** 2025-11-08
