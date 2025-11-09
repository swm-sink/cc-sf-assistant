# Variance Analyzer - Scripts

This directory contains executable Python scripts for the variance analyzer skill.

## Contents (Future - Phase 3-4)

- `variance_calculator.py` - Core variance calculation with Decimal precision
- `favorability_assessor.py` - Favorability logic by account type
- `materiality_flagging.py` - Material variance detection
- `excel_formatter.py` - Output formatting with conditional formatting

## Architecture

These scripts are executed by Claude Code during workflow execution. They follow:
- Decimal precision for all currency calculations
- Type hints on all functions
- Comprehensive error handling
- Audit logging
- 95%+ test coverage

See `scripts/core/` in project root for actual implementations.
