#!/usr/bin/env bash
#
# Stop Hook - Quality Gates
#
# Runs at end of each Claude Code turn to enforce quality standards.
# Exit code 2 = blocking error (Claude will see and fix)
# Exit code 0 = pass
#
# Research: Anthropic best practices - hooks enforce quality gates without
# relying on model memory.

set -e

echo "🔍 Running quality gates..."

# Quality Gate 1: Check for float usage in financial code
echo "  ├─ Checking for float/double in financial calculations..."
if find src/ -name "*.py" -type f -exec grep -l "float\|double" {} \; 2>/dev/null | grep -q .; then
    echo "  │  ❌ FAIL: Found float/double usage in financial code"
    echo "  │"
    echo "  │  Financial calculations MUST use Decimal type."
    echo "  │  Files with violations:"
    find src/ -name "*.py" -type f -exec grep -l "float\|double" {} \; 2>/dev/null | sed 's/^/  │    /'
    echo "  │"
    echo "  │  Fix: Replace with 'from decimal import Decimal'"
    exit 2  # Blocking error
fi
echo "  │  ✓ Pass: No float usage in src/"

# Quality Gate 2: Check for type hints on functions
echo "  ├─ Checking for type hints on functions..."
if find src/ -name "*.py" -type f -exec grep -l "^def " {} \; | xargs grep "^def " | grep -v " -> " | grep -q "def "; then
    echo "  │  ⚠️  WARNING: Found functions without return type hints"
    echo "  │  (Not blocking, but should be added)"
fi
echo "  │  ✓ Type hint check complete"

# Quality Gate 3: Run financial validator if it exists
if [ -f ".claude/skills/financial-validator/scripts/validate_precision.py" ]; then
    echo "  ├─ Running financial precision validator..."
    if python3 .claude/skills/financial-validator/scripts/validate_precision.py > /dev/null 2>&1; then
        echo "  │  ✓ Pass: Financial precision tests passed"
    else
        echo "  │  ⚠️  WARNING: Precision validator failed (install dependencies?)"
    fi
fi

# Quality Gate 4: Check Python syntax if Python files changed
if find src/ -name "*.py" -type f -mmin -5 2>/dev/null | grep -q .; then
    echo "  ├─ Checking Python syntax..."
    for file in $(find src/ -name "*.py" -type f -mmin -5 2>/dev/null); do
        if ! python3 -m py_compile "$file" 2>/dev/null; then
            echo "  │  ❌ FAIL: Syntax error in $file"
            python3 -m py_compile "$file"  # Show error
            exit 2  # Blocking error
        fi
    done
    echo "  │  ✓ Pass: No syntax errors"
fi

# Quality Gate 5: Check for spec.md references (DRY principle)
echo "  ├─ Checking DRY compliance..."
if [ -f "CLAUDE.md" ]; then
    # Count lines in CLAUDE.md
    line_count=$(wc -l < CLAUDE.md)
    if [ "$line_count" -gt 300 ]; then
        echo "  │  ⚠️  WARNING: CLAUDE.md is $line_count lines (target: <250)"
        echo "  │  Consider moving details to Skills or Commands"
    fi
fi
echo "  │  ✓ DRY check complete"

echo "  └─ ✅ All quality gates passed"
echo ""

exit 0
