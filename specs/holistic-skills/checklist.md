# Holistic Meta-Skills - RPIV Checklist

**Status:** 🔄 Planning Phase
**Last Updated:** 2025-11-10
**Plan:** specs/holistic-skills/plan.md
**Research:** specs/holistic-skills/research.md

---

## Legend

- ✅ Complete
- 🔄 In Progress
- ⏳ Pending (blocked or not started)
- ❌ Failed (needs rework)

---

## Phase Overview

| Phase | Status | Completion |
|-------|--------|------------|
| **Research** | ✅ Complete | 100% |
| **Planning** | 🔄 In Progress | 95% (awaiting user approval) |
| **Implementation** | ⏳ Pending | 0% |
| **Verification** | ⏳ Pending | 0% |

---

## Research Phase (COMPLETE ✅)

### Research Activities
- ✅ Claude Code hooks research (18 sources, 2,605 lines)
- ✅ Holistic system management patterns (16 patterns, 25+ sources)
- ✅ Tree of thought analysis (20 options → 5 selected)
- ✅ User decisions Q1-Q10 documented
- ✅ Agent orchestration research (1000+ lines)
- ✅ Q11-Q20 validation with evidence (68KB analysis)
- ✅ Dependency graph analysis

### Research Artifacts
- ✅ specs/claude-code-hooks-research.md
- ✅ specs/holistic-system-management/research.md
- ✅ specs/holistic-skills-analysis/analysis.md
- ✅ specs/holistic-skills/research.md
- ✅ specs/holistic-skills/agent-orchestration-research.md
- ✅ Q11-Q15-CRITICAL-ANALYSIS.md
- ✅ specs/holistic-skills/dependency-graph.md

### User Decisions Captured
- ✅ Q1: Validate EVERYTHING continuously
- ✅ Q2: Include hook testing (dev + prod)
- ✅ Q3: Complete immediate CLAUDE.md migration
- ✅ Q4: Hook + Skill combination (robust)
- ✅ Q5: Auto-invoke with hybrid approach
- ✅ Q6: BLOCKING enforcement
- ✅ Q7: Option A - Separate directories by workflow type
- ✅ Q8: Character-based token estimation (~4 chars/token)
- ✅ Q9: BLOCKING for everything (zero tolerance)
- ✅ Q10: Meta-skills first, then agents/commands

### Evidence-Based Validation (Q11-Q20)
- ✅ Q11: Hybrid parallelization (20-30% time savings)
- ✅ Q12: Incremental with retroactive validation
- ✅ Q13: Tiered CSO thresholds (0.8 for critical, 0.7 for others)
- ✅ Q14: All 5 have references/ directory
- ✅ Q15: Hybrid auto-invoke (CSO + Hook + Override)
- ✅ Q16-Q20: Pragmatic validation complete

**Research Phase Checkpoint:** ✅ PASSED (User approved: "continue with this step by step")

---

## Planning Phase (IN PROGRESS 🔄)

### Planning Activities
- ✅ Overall architecture and phasing (5 weeks with parallelization)
- ✅ Detailed implementation plans for all 5 skills
- ✅ File structures, templates, validators defined
- ✅ Timeline with dependency graph
- ✅ Risk mitigation strategies
- ✅ Success criteria defined
- 🔄 Awaiting user approval of plan.md

### Planning Artifacts
- ✅ specs/holistic-skills/plan.md (comprehensive 5-week plan)
- ✅ specs/holistic-skills/checklist.md (this file)

### Planning Validation
- ✅ All 5 skills have detailed file structures
- ✅ All templates defined (8 hook templates, 4 CLAUDE.md templates, etc.)
- ✅ All validators defined (6 for System Coherence, 3 for Financial Quality Gate)
- ✅ All references/ documents scoped (<600 lines each)
- ✅ CSO optimization strategy defined (tiered thresholds)
- ✅ Integration points documented
- ✅ Testing strategies defined for each skill
- ⏳ User approval pending

**Planning Phase Checkpoint:** 🔄 PENDING USER APPROVAL

---

## Implementation Phase (PENDING ⏳)

### Week 1: Foundation Skills

#### 1.1 Hook Factory (Days 1-3)
- ⏳ Day 1: SKILL.md + 8 templates
  - ⏳ SKILL.md (target 198 lines, CSO ≥0.8)
  - ⏳ templates/session-start.sh
  - ⏳ templates/pre-tool-use.sh
  - ⏳ templates/post-tool-use.sh
  - ⏳ templates/stop.sh
  - ⏳ templates/subagent-stop.sh
  - ⏳ templates/user-prompt-submit.sh
  - ⏳ templates/pre-compact.sh
  - ⏳ templates/notification.sh
- ⏳ Day 2: references/ (4 documents)
  - ⏳ references/hook-patterns.md (300-400 lines)
  - ⏳ references/exit-code-contract.md (200-300 lines)
  - ⏳ references/dev-hooks.md (200-300 lines)
  - ⏳ references/prod-hooks.md (200-300 lines)
- ⏳ Day 3: Testing + validation
  - ⏳ Shellcheck all templates
  - ⏳ Test exit code behavior
  - ⏳ Verify CSO score ≥0.8
  - ⏳ Run System Coherence Validator

**Hook Factory Success Criteria:**
- ⏳ 8 templates generate valid hooks
- ⏳ CSO score ≥0.8
- ⏳ All references/ <500 lines each
- ⏳ Zero syntax errors in generated hooks
- ⏳ Exit codes behave as specified

#### 1.2 Hierarchical Context Manager (Days 4-7, parallel with Hook Factory Days 4-7)
- ⏳ Day 4: SKILL.md + 4 templates
  - ⏳ SKILL.md (target 195 lines, CSO ≥0.7)
  - ⏳ templates/root-claude.md.template
  - ⏳ templates/scripts-claude.md.template
  - ⏳ templates/claude-dir-claude.md.template
  - ⏳ templates/tests-claude.md.template
- ⏳ Day 5: references/ (4 documents)
  - ⏳ references/migration-strategy.md (400-500 lines)
  - ⏳ references/token-estimation.md (200-300 lines)
  - ⏳ references/cascading-rules.md (200-300 lines)
  - ⏳ references/maintenance-patterns.md (200-300 lines)
- ⏳ Day 6: Migration of root CLAUDE.md
  - ⏳ Measure current token count (~4 chars/token)
  - ⏳ Create subdirectory CLAUDE.md files
  - ⏳ Migrate content from root to subdirectories
  - ⏳ Measure token reduction (target ≥70%)
- ⏳ Day 7: Testing + token measurement
  - ⏳ Test cascading precedence (most nested wins)
  - ⏳ Verify no contradictions across hierarchy
  - ⏳ Verify CSO score ≥0.7
  - ⏳ Run System Coherence Validator

**Context Manager Success Criteria:**
- ⏳ 70%+ token reduction demonstrated
- ⏳ CSO score ≥0.7
- ⏳ 4 templates cover all use cases
- ⏳ Cascading behavior tested and documented
- ⏳ Migration guide enables user self-service

**Week 1 Checkpoint:** ⏳ PENDING

---

### Week 2: Validation Skills

#### 2.1 System Coherence Validator (Days 1-4)
- ⏳ Day 1: SKILL.md + validators/
  - ⏳ SKILL.md (target 200 lines, CSO ≥0.7)
  - ⏳ validators/yaml-validator.py
  - ⏳ validators/cso-scorer.py
  - ⏳ validators/naming-validator.py
  - ⏳ validators/structure-validator.py
  - ⏳ validators/cross-reference-validator.py
  - ⏳ validators/integration-validator.py
- ⏳ Day 2: references/ (4 documents)
  - ⏳ references/validation-rules.md (500-600 lines, 15 rules)
  - ⏳ references/retroactive-validation.md (200-300 lines)
  - ⏳ references/continuous-validation.md (300-400 lines)
  - ⏳ references/error-reporting.md (200-300 lines)
- ⏳ Day 3: Self-validation (bootstrap test)
  - ⏳ Run validator on itself using creating-skills validators (Phase 1)
  - ⏳ Fix any issues found
  - ⏳ Run validator on itself using its own validators (Phase 2)
  - ⏳ Verify bootstrap successful
- ⏳ Day 4: Retroactive validation of existing meta-skills
  - ⏳ Validate creating-skills (CSO 0.88 expected)
  - ⏳ Validate creating-commands (CSO 0.75 expected)
  - ⏳ Validate creating-agents (CSO 0.62, needs improvement)
  - ⏳ Validate enforcing-RPIV (CSO 0.46, needs improvement)
  - ⏳ Document issues and create improvement plan

**System Coherence Validator Success Criteria:**
- ⏳ All 15 validation rules implemented
- ⏳ CSO score ≥0.7
- ⏳ Self-validation passes (bootstrap successful)
- ⏳ 4 existing meta-skills validated (issues documented)
- ⏳ Hook integration tested

#### 2.2 Financial Quality Gate (Days 5-7)
- ⏳ Day 5: SKILL.md + validators/
  - ⏳ SKILL.md (target 200 lines, CSO ≥0.8)
  - ⏳ validators/decimal-checker.py
  - ⏳ validators/audit-trail-checker.py
  - ⏳ validators/edge-case-tester.py
- ⏳ Day 6: references/ (4 documents)
  - ⏳ references/decimal-precision.md (400-500 lines)
  - ⏳ references/audit-trail-requirements.md (300-400 lines)
  - ⏳ references/edge-cases.md (500-600 lines)
  - ⏳ references/testing-standards.md (400-500 lines)
- ⏳ Day 7: PreToolUse hook integration + testing
  - ⏳ Generate PreToolUse hook using Hook Factory
  - ⏳ Configure hook to invoke Financial Quality Gate before Write/Edit on scripts/core/*.py
  - ⏳ Test BLOCKING behavior (exit code 2)
  - ⏳ Test on known float-using code (should block)
  - ⏳ Verify user override mechanism works

**Financial Quality Gate Success Criteria:**
- ⏳ CSO score ≥0.8
- ⏳ Zero false positives on Decimal scanner
- ⏳ 100% audit trail coverage on test transformations
- ⏳ All edge cases tested and documented
- ⏳ PreToolUse hook integration tested

**Week 2 Checkpoint:** ⏳ PENDING

---

### Week 3: Agent Creation

#### 3.1 Create 7 Persistent Agents (Days 1-5, parallel)

**Read-Only Validators:**
- ⏳ @databricks-validator
  - ⏳ Create .claude/agents/validators/databricks-validator.md
  - ⏳ YAML frontmatter (tool_tier: read_only)
  - ⏳ Validation logic (SQL syntax, credential usage, timeout handling)
  - ⏳ Test with sample Databricks extraction code
- ⏳ @adaptive-validator
  - ⏳ Create .claude/agents/validators/adaptive-validator.md
  - ⏳ YAML frontmatter (tool_tier: read_only)
  - ⏳ Validation logic (API endpoint, token usage, retry logic)
  - ⏳ Test with sample Adaptive Insights integration code
- ⏳ @report-formatter
  - ⏳ Create .claude/agents/validators/report-formatter.md
  - ⏳ YAML frontmatter (tool_tier: read_only)
  - ⏳ Validation logic (Excel structure, formatting rules, data integrity)
  - ⏳ Test with sample report generation code
- ⏳ @slides-previewer
  - ⏳ Create .claude/agents/validators/slides-previewer.md
  - ⏳ YAML frontmatter (tool_tier: read_only)
  - ⏳ Validation logic (slide structure, template compliance, content checks)
  - ⏳ Test with sample slides generation code
- ⏳ @script-validator
  - ⏳ Create .claude/agents/validators/script-validator.md
  - ⏳ YAML frontmatter (tool_tier: read_only)
  - ⏳ Validation logic (type hints, error handling, documentation, style)
  - ⏳ Test with sample Python scripts

**Full Access Generators:**
- ⏳ @script-generator
  - ⏳ Create .claude/agents/generators/script-generator.md
  - ⏳ YAML frontmatter (tool_tier: full_access)
  - ⏳ Generation logic (Python scripts with type hints, error handling, audit trails)
  - ⏳ Test with sample script generation request
- ⏳ @test-generator
  - ⏳ Create .claude/agents/generators/test-generator.md
  - ⏳ YAML frontmatter (tool_tier: full_access)
  - ⏳ Generation logic (pytest tests with edge cases, fixtures, assertions)
  - ⏳ Test with sample test generation request

#### 3.2 Agent Validation (Days 6-7)
- ⏳ Test tool tier enforcement
  - ⏳ Verify read-only agents cannot Write/Edit
  - ⏳ Verify full access agents can Write/Edit
  - ⏳ Test tool restriction violations (should error)
- ⏳ Validate agent YAML frontmatter
  - ⏳ Run System Coherence Validator on all 7 agents
  - ⏳ Fix any validation issues
- ⏳ Test agent invocation patterns
  - ⏳ Test single agent invocation
  - ⏳ Test parallel agent invocation (2-3 validators simultaneously)
  - ⏳ Test sequential agent invocation (validator → generator → validator)

**Week 3 Success Criteria:**
- ⏳ All 7 agents created with proper YAML frontmatter
- ⏳ Tool tier enforcement tested and verified
- ⏳ All agents pass System Coherence Validator
- ⏳ Agent invocation patterns tested

**Week 3 Checkpoint:** ⏳ PENDING

---

### Week 4: Orchestration

#### 4.1 Multi-Agent Workflow Coordinator (Days 1-3)
- ⏳ Day 1: SKILL.md + templates/
  - ⏳ SKILL.md (target 198 lines, CSO ≥0.7)
  - ⏳ templates/validation-workflow.md.template
  - ⏳ templates/generation-workflow.md.template
  - ⏳ templates/hybrid-workflow.md.template
- ⏳ Day 2: references/ (4 documents)
  - ⏳ references/agent-patterns.md (400-500 lines)
  - ⏳ references/tool-tier-enforcement.md (300-400 lines)
  - ⏳ references/workflow-orchestration.md (400-500 lines)
  - ⏳ references/error-handling.md (300-400 lines)
- ⏳ Day 3: Testing with 7 agents
  - ⏳ Test validation workflow (read-only agents)
  - ⏳ Test generation workflow (full access agents)
  - ⏳ Test hybrid workflow (validators → generator → validators)

#### 4.2 Integration Testing (Days 4-5)
- ⏳ Test sequential workflows
  - ⏳ Databricks validation → script generation → script validation
  - ⏳ Adaptive validation → test generation → test execution
- ⏳ Test parallel workflows
  - ⏳ Multiple validators simultaneously (databricks-validator || adaptive-validator || report-formatter)
  - ⏳ Verify coordination via Task()
- ⏳ Test error handling and rollback
  - ⏳ Simulate validator failure (should halt workflow)
  - ⏳ Simulate generator failure (should rollback Write operations)
  - ⏳ Test retry logic (exponential backoff)

#### 4.3 Documentation and Final Validation (Days 6-7)
- ⏳ Complete README.md for users
- ⏳ Generate workflow examples (5+ patterns)
- ⏳ Validate CSO score ≥0.7
- ⏳ Run System Coherence Validator

**Multi-Agent Workflow Coordinator Success Criteria:**
- ⏳ CSO score ≥0.7
- ⏳ All workflow patterns tested
- ⏳ Integration with 7 agents validated
- ⏳ Error handling tested with rollback scenarios

**Week 4 Checkpoint:** ⏳ PENDING

---

### Week 5: Final Validation

#### 5.1 System-Wide Validation (Days 1-2)
- ⏳ Run System Coherence Validator on all 5 new skills
  - ⏳ Hook Factory
  - ⏳ Hierarchical Context Manager
  - ⏳ System Coherence Validator (self-validation)
  - ⏳ Financial Quality Gate
  - ⏳ Multi-Agent Workflow Coordinator
- ⏳ Run System Coherence Validator on 7 agents
- ⏳ Verify no regressions in existing 4 meta-skills
  - ⏳ creating-skills still functions correctly
  - ⏳ creating-commands still functions correctly
  - ⏳ creating-agents still functions correctly
  - ⏳ enforcing-RPIV still functions correctly

#### 5.2 Performance Measurement (Days 3-4)
- ⏳ Measure token reduction (Context Manager)
  - ⏳ Before: Root CLAUDE.md token count
  - ⏳ After: Root + subdirectory CLAUDE.md token count
  - ⏳ Reduction percentage (target ≥70%)
- ⏳ Measure CSO scores (all 5 skills)
  - ⏳ Hook Factory: ≥0.8
  - ⏳ Context Manager: ≥0.7
  - ⏳ System Coherence Validator: ≥0.7
  - ⏳ Financial Quality Gate: ≥0.8
  - ⏳ Multi-Agent Coordinator: ≥0.7
- ⏳ Measure validation coverage (System Coherence Validator)
  - ⏳ 15 validation rules implemented
  - ⏳ 9 components validated (4 existing + 5 new skills)
  - ⏳ 7 agents validated

#### 5.3 Documentation and Handoff (Days 5-7)
- ⏳ Update spec.md with Phase 2 completion
- ⏳ Update plan.md with actual timeline vs planned
- ⏳ Create user guides for 5 new skills
  - ⏳ Hook Factory user guide
  - ⏳ Hierarchical Context Manager migration guide
  - ⏳ System Coherence Validator usage guide
  - ⏳ Financial Quality Gate requirements guide
  - ⏳ Multi-Agent Workflow Coordinator orchestration guide
- ⏳ Document lessons learned
  - ⏳ What went well (parallelization, evidence-based validation)
  - ⏳ What could improve (CSO scoring iteration, bootstrap complexity)
  - ⏳ Recommendations for Phase 3 (domain component creation)

**Week 5 Checkpoint:** ⏳ PENDING

---

## Verification Phase (PENDING ⏳)

### Exit Criteria for Phase 2

#### Functional Requirements
- ⏳ All 5 skills complete with SKILL.md + references/ + templates/
- ⏳ All 7 agents created with proper tool tier enforcement
- ⏳ Hook Factory generates valid hooks for all 8 types
- ⏳ Hierarchical Context Manager demonstrates 70%+ token reduction
- ⏳ System Coherence Validator validates all components (self + retroactive)
- ⏳ Financial Quality Gate blocks float usage in currency code
- ⏳ Multi-Agent Workflow Coordinator orchestrates 7 agents successfully

#### Quality Requirements
- ⏳ CSO scores: Critical skills ≥0.8, others ≥0.7
  - ⏳ Hook Factory: ≥0.8
  - ⏳ Financial Quality Gate: ≥0.8
  - ⏳ Context Manager: ≥0.7
  - ⏳ System Coherence Validator: ≥0.7
  - ⏳ Multi-Agent Coordinator: ≥0.7
- ⏳ All skills pass System Coherence Validator (15 validation rules)
- ⏳ Zero regressions in existing 4 meta-skills
- ⏳ All references/ documents <600 lines each (progressive disclosure)
- ⏳ SKILL.md files ≤200 lines (target: 195-200)

#### Testing Requirements
- ⏳ Bootstrap validation successful (validator validates itself)
- ⏳ Retroactive validation complete (4 existing meta-skills + 5 new skills)
- ⏳ Hook integration tested (dev environment)
- ⏳ Agent tool tier enforcement tested (read-only cannot Write)
- ⏳ Orchestration tested (sequential, parallel, error handling)

#### Documentation Requirements
- ⏳ User guides complete (README.md for each skill)
- ⏳ Migration guide for Hierarchical Context Manager
- ⏳ Validation report from System Coherence Validator
- ⏳ Performance metrics documented (token reduction, CSO scores)

#### Approval Requirements
- ⏳ User reviews Phase 2 completion
- ⏳ User approves proceeding to Phase 3 (domain component creation)
- ⏳ Lessons learned documented for future phases

**Verification Phase Checkpoint:** ⏳ PENDING

---

## Risk Register

| Risk | Probability | Impact | Mitigation | Status |
|------|------------|--------|------------|--------|
| CSO scores too low | Medium | High | Tiered thresholds, iterate on trigger phrases | ⏳ Monitoring |
| Token reduction <70% | Low | Medium | Measure explicitly, move more to subdirectories | ⏳ Monitoring |
| Bootstrap paradox unresolved | Low | High | Use creating-skills validators for Phase 1 | ⏳ Mitigated |
| Hook integration breaks workflows | Medium | High | Test in dev environment, user override available | ⏳ Monitoring |
| Agent creation delayed | Low | Medium | Parallelize creation, prioritize validators | ⏳ Monitoring |

---

## Metrics Dashboard

### Overall Progress
- **Research:** 100% ✅
- **Planning:** 95% 🔄 (awaiting approval)
- **Implementation:** 0% ⏳
- **Verification:** 0% ⏳

### Timeline
- **Planned:** 5 weeks (20-30% faster than sequential)
- **Actual:** TBD
- **Start Date:** TBD (after user approval)
- **Target End Date:** TBD (5 weeks from start)

### Quality Metrics
- **CSO Scores:** TBD (target: critical ≥0.8, others ≥0.7)
- **Token Reduction:** TBD (target: ≥70%)
- **Validation Coverage:** TBD (target: 15 rules, 9 components, 7 agents)
- **Regression Count:** TBD (target: 0)

---

## Next Actions

**Immediate:**
1. 🔄 User reviews plan.md
2. ⏳ User approves plan → Update this checklist status to ✅
3. ⏳ Begin Week 1 Day 1: Hook Factory SKILL.md + templates

**After Planning Approval:**
4. ⏳ Create implementation branch (if needed)
5. ⏳ Set up dev environment for hook testing
6. ⏳ Weekly check-ins with user
7. ⏳ Update this checklist daily during implementation

---

**RPIV Status:** Planning Phase (Checkpoint 2)
**Blocking:** User approval of plan.md
**Last Updated:** 2025-11-10
