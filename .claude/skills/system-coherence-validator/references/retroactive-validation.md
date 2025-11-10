# Retroactive Validation Reference

**Purpose:** Validate existing components (4 meta-skills + 2 holistic skills).

---

## Batch Validation Script

```bash
#!/bin/bash
# validate-all.sh - Run validation on all .claude components

for skill in .claude/skills/*/SKILL.md; do
  echo "Validating $(dirname $skill)..."
  python .claude/skills/system-coherence-validator/validators/yaml-validator.py "$skill"
  python .claude/skills/system-coherence-validator/validators/cso-scorer.py "$skill"
  python .claude/skills/system-coherence-validator/validators/naming-validator.py "$(dirname $skill)"
  python .claude/skills/system-coherence-validator/validators/structure-validator.py "$(dirname $skill)"
  python .claude/skills/system-coherence-validator/validators/cross-reference-validator.py "$(dirname $skill)"
done
```

---

## Prioritization

**Phase 1:** Meta-skills (highest priority)
- creating-skills
- creating-commands
- creating-agents
- enforcing-research-plan-implement-verify

**Phase 2:** Holistic meta-skills
- hook-factory
- hierarchical-context-manager

**Phase 3:** Agents and commands (future)

---

## Expected Issues

Based on measured CSO scores:
- creating-skills: 0.88 ✅ (likely passes all checks)
- creating-commands: 0.75 ⚠️ (may need CSO improvement for critical tier)
- creating-agents: 0.62 ❌ (needs CSO improvement)
- enforcing-RPIV: 0.46 ❌ (significant CSO improvement needed)

---

**Lines:** 38
**Last Updated:** 2025-11-10
