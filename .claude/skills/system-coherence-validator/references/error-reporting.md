# Error Reporting Reference

**Purpose:** Structured validation report format with actionable fixes.

---

## Report Structure

```json
{
  "component": ".claude/skills/example-skill/",
  "type": "skill",
  "overall_status": "FAIL",
  "issues": [
    {
      "severity": "ERROR",
      "rule": "CSO Score Threshold",
      "message": "CSO score 0.62 below threshold 0.7 for high priority skill",
      "fix": "Improve trigger phrases (add 2+), symptoms (add 2+), or keywords (add 4+)"
    },
    {
      "severity": "WARNING",
      "rule": "Progressive Disclosure",
      "message": "SKILL.md has 215 lines (target ≤200)",
      "fix": "Move detailed content to references/ directory"
    },
    {
      "severity": "INFO",
      "rule": "Example Quality",
      "message": "Only 3 examples found (recommended 4-5)",
      "fix": "Add 1-2 more concrete usage examples"
    }
  ]
}
```

---

## Severity Levels

**ERROR:** Critical failure (component non-functional or violates core standards)
**WARNING:** Important issue (degraded quality, should fix)
**INFO:** Quality improvement opportunity (nice to have)

---

## Actionable Fix Recommendations

Each issue includes specific fix:
- CSO low: "Add X trigger phrases, Y symptoms"
- Naming wrong: "Rename to kebab-case: example-skill"
- Broken link: "Create missing-doc.md or remove link"
- Size too large: "Move content to references/"

---

**Lines:** 41
**Last Updated:** 2025-11-10
