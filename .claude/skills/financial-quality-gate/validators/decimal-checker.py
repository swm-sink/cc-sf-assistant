#!/usr/bin/env python3
"""Decimal type validator for currency calculations.

Scans Python code for float usage in currency-related calculations.
BLOCKING validator - exits with code 2 if float detected.
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple


# Currency-related variable/function name patterns
CURRENCY_KEYWORDS = [
    'amount', 'price', 'cost', 'revenue', 'expense', 'budget', 'actual',
    'variance', 'total', 'subtotal', 'tax', 'fee', 'balance', 'payment',
    'refund', 'credit', 'debit', 'currency', 'monetary', 'financial',
    'dollar', 'usd', 'eur', 'gbp', 'money'
]


class FloatUsageDetector(ast.NodeVisitor):
    """AST visitor to detect float usage in currency calculations."""

    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []

    def _is_currency_related(self, name: str) -> bool:
        """Check if variable/function name is currency-related."""
        name_lower = name.lower()
        return any(keyword in name_lower for keyword in CURRENCY_KEYWORDS)

    def visit_Call(self, node: ast.Call) -> None:
        """Check for float() calls on currency variables."""
        if isinstance(node.func, ast.Name) and node.func.id == 'float':
            # Check if argument is currency-related
            if node.args:
                arg = node.args[0]
                if isinstance(arg, ast.Name) and self._is_currency_related(arg.id):
                    self.errors.append({
                        'line': node.lineno,
                        'col': node.col_offset,
                        'type': 'float_call',
                        'message': f'Float call on currency variable: {arg.id}',
                        'severity': 'ERROR'
                    })
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """Check type hints for float in currency variables."""
        if isinstance(node.target, ast.Name):
            var_name = node.target.id

            # Check if annotation is 'float'
            if isinstance(node.annotation, ast.Name) and node.annotation.id == 'float':
                if self._is_currency_related(var_name):
                    self.errors.append({
                        'line': node.lineno,
                        'col': node.col_offset,
                        'type': 'float_type_hint',
                        'message': f'Float type hint for currency variable: {var_name}',
                        'severity': 'ERROR'
                    })
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Check function parameter and return type hints."""
        # Check parameters
        for arg in node.args.args:
            if arg.annotation and isinstance(arg.annotation, ast.Name):
                if arg.annotation.id == 'float' and self._is_currency_related(arg.arg):
                    self.errors.append({
                        'line': node.lineno,
                        'col': node.col_offset,
                        'type': 'float_parameter',
                        'message': f'Float parameter for currency: {arg.arg} in {node.name}()',
                        'severity': 'ERROR'
                    })

        # Check return type
        if node.returns and isinstance(node.returns, ast.Name):
            if node.returns.id == 'float' and self._is_currency_related(node.name):
                self.errors.append({
                    'line': node.lineno,
                    'col': node.col_offset,
                    'type': 'float_return',
                    'message': f'Float return type for currency function: {node.name}()',
                    'severity': 'ERROR'
                })

        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        """Check for float literals in calculations (less strict - warning only)."""
        if isinstance(node.value, float):
            # Get parent context to check if it's in currency calculation
            # This is a simplified check - full implementation would need parent tracking
            self.warnings.append({
                'line': node.lineno,
                'col': node.col_offset,
                'type': 'float_literal',
                'message': f'Float literal detected: {node.value}',
                'severity': 'WARNING'
            })
        self.generic_visit(node)


def check_decimal_import(tree: ast.AST) -> bool:
    """Check if Decimal is imported from decimal module."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == 'decimal':
                for alias in node.names:
                    if alias.name == 'Decimal':
                        return True
    return False


def validate_file(file_path: Path) -> Tuple[bool, List[Dict[str, Any]]]:
    """Validate a Python file for Decimal usage.

    Args:
        file_path: Path to Python file

    Returns:
        Tuple of (is_valid, issues_list)
    """
    issues = []

    try:
        with open(file_path, 'r') as f:
            source = f.read()
    except Exception as e:
        issues.append({
            'line': 0,
            'col': 0,
            'type': 'file_error',
            'message': f'Cannot read file: {e}',
            'severity': 'ERROR'
        })
        return False, issues

    try:
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError as e:
        issues.append({
            'line': e.lineno or 0,
            'col': e.offset or 0,
            'type': 'syntax_error',
            'message': f'Syntax error: {e.msg}',
            'severity': 'ERROR'
        })
        return False, issues

    # Check for Decimal import
    has_decimal_import = check_decimal_import(tree)

    # Detect float usage
    detector = FloatUsageDetector()
    detector.visit(tree)

    # Combine errors and warnings
    all_issues = detector.errors + detector.warnings

    # If there are float usage errors and no Decimal import, add recommendation
    if detector.errors and not has_decimal_import:
        issues.append({
            'line': 0,
            'col': 0,
            'type': 'missing_import',
            'message': 'Missing Decimal import. Add: from decimal import Decimal',
            'severity': 'ERROR'
        })

    issues.extend(all_issues)

    # File is valid only if no ERROR severity issues
    has_errors = any(issue['severity'] == 'ERROR' for issue in issues)
    return not has_errors, issues


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: decimal-checker.py <file_path>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        sys.exit(2)

    if not file_path.suffix == '.py':
        # Not a Python file, skip validation
        sys.exit(0)

    is_valid, issues = validate_file(file_path)

    if not is_valid:
        print(f"❌ Financial Quality Gate BLOCKED: {file_path}", file=sys.stderr)
        print("", file=sys.stderr)

        errors = [i for i in issues if i['severity'] == 'ERROR']
        for issue in errors:
            print(f"  Line {issue['line']}: {issue['message']}", file=sys.stderr)

        print("", file=sys.stderr)
        print("Fix: Use Decimal type for all currency calculations:", file=sys.stderr)
        print("  from decimal import Decimal", file=sys.stderr)
        print("  amount = Decimal('100.00')  # Not float(100.0)", file=sys.stderr)

        sys.exit(2)  # BLOCKING

    # Check warnings
    warnings = [i for i in issues if i['severity'] == 'WARNING']
    if warnings:
        print(f"⚠️  Financial Quality Gate: {len(warnings)} warning(s) for {file_path}", file=sys.stderr)
        for issue in warnings:
            print(f"  Line {issue['line']}: {issue['message']}", file=sys.stderr)
        sys.exit(1)  # WARNING

    # All checks passed
    print(f"✅ Financial Quality Gate PASSED: {file_path}")
    sys.exit(0)


if __name__ == '__main__':
    main()
