#!/usr/bin/env python3
"""Audit trail validator for data transformations.

Verifies that audit logging is present for financial data transformations.
WARNING validator - exits with code 1 if audit trail missing.
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple


# Data transformation function name patterns
TRANSFORM_KEYWORDS = [
    'transform', 'convert', 'consolidate', 'merge', 'aggregate',
    'calculate', 'compute', 'process', 'load', 'import', 'export',
    'update', 'modify', 'adjust', 'reconcile'
]


class AuditTrailDetector(ast.NodeVisitor):
    """AST visitor to detect missing audit logging."""

    def __init__(self):
        self.functions: List[Dict[str, Any]] = []
        self.has_logging_import = False
        self.has_logger = False

    def _is_transform_function(self, name: str) -> bool:
        """Check if function name suggests data transformation."""
        name_lower = name.lower()
        return any(keyword in name_lower for keyword in TRANSFORM_KEYWORDS)

    def _has_logging_call(self, node: ast.FunctionDef) -> bool:
        """Check if function body contains logging calls."""
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                # Check for logger.info(), logger.warning(), etc.
                if isinstance(child.func, ast.Attribute):
                    if child.func.attr in ['info', 'warning', 'error', 'debug']:
                        return True
                # Check for logging.info(), logging.warning(), etc.
                elif isinstance(child.func, ast.Attribute):
                    if isinstance(child.func.value, ast.Name):
                        if child.func.value.id == 'logging':
                            return True
        return False

    def visit_Import(self, node: ast.Import) -> None:
        """Check for logging import."""
        for alias in node.names:
            if alias.name == 'logging':
                self.has_logging_import = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Check for logging import."""
        if node.module == 'logging':
            self.has_logging_import = True
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Check for logger assignment."""
        # Check for: logger = logging.getLogger(__name__)
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                if (isinstance(node.value.func.value, ast.Name) and
                    node.value.func.value.id == 'logging' and
                    node.value.func.attr == 'getLogger'):
                    self.has_logger = True
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Check if transformation functions have logging."""
        if self._is_transform_function(node.name):
            has_logging = self._has_logging_call(node)
            self.functions.append({
                'name': node.name,
                'line': node.lineno,
                'has_logging': has_logging,
                'is_transform': True
            })
        self.generic_visit(node)


def check_audit_trail_format(tree: ast.AST) -> List[str]:
    """Check if audit trail logging follows required format.

    Required format:
    - Timestamp (ISO 8601)
    - User (or 'system')
    - Operation/function name
    - Source file(s) if applicable
    - Target file if applicable

    Returns:
        List of recommendations for improvement
    """
    recommendations = []

    # This is a simplified check - full implementation would parse log strings
    # and verify they contain required fields

    # Check for datetime import (for timestamp)
    has_datetime = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == 'datetime':
                has_datetime = True
                break

    if not has_datetime:
        recommendations.append(
            "Consider importing datetime for ISO 8601 timestamps: "
            "from datetime import datetime, timezone"
        )

    return recommendations


def validate_file(file_path: Path) -> Tuple[bool, List[Dict[str, Any]]]:
    """Validate a Python file for audit trail logging.

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
            'type': 'syntax_error',
            'message': f'Syntax error: {e.msg}',
            'severity': 'ERROR'
        })
        return False, issues

    # Detect audit trail presence
    detector = AuditTrailDetector()
    detector.visit(tree)

    # Check for missing logging in transformation functions
    transform_functions = [f for f in detector.functions if f['is_transform']]

    if transform_functions:
        # Check if logging is set up
        if not detector.has_logging_import:
            issues.append({
                'line': 0,
                'type': 'missing_logging_import',
                'message': 'Missing logging import for audit trail',
                'severity': 'WARNING'
            })

        if not detector.has_logger:
            issues.append({
                'line': 0,
                'type': 'missing_logger',
                'message': 'Missing logger initialization: logger = logging.getLogger(__name__)',
                'severity': 'WARNING'
            })

        # Check each transformation function
        for func in transform_functions:
            if not func['has_logging']:
                issues.append({
                    'line': func['line'],
                    'type': 'missing_audit_log',
                    'message': f"Function {func['name']}() missing audit trail logging",
                    'severity': 'WARNING'
                })

    # Check format recommendations
    recommendations = check_audit_trail_format(tree)
    for rec in recommendations:
        issues.append({
            'line': 0,
            'type': 'audit_format',
            'message': rec,
            'severity': 'INFO'
        })

    # Audit trail validation only produces warnings/info (never blocking)
    return True, issues


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: audit-trail-checker.py <file_path>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        sys.exit(2)

    if not file_path.suffix == '.py':
        # Not a Python file, skip validation
        sys.exit(0)

    is_valid, issues = validate_file(file_path)

    # Separate by severity
    warnings = [i for i in issues if i['severity'] == 'WARNING']
    infos = [i for i in issues if i['severity'] == 'INFO']

    if warnings:
        print(f"⚠️  Audit Trail Check: {len(warnings)} warning(s) for {file_path}", file=sys.stderr)
        print("", file=sys.stderr)

        for issue in warnings:
            if issue['line'] > 0:
                print(f"  Line {issue['line']}: {issue['message']}", file=sys.stderr)
            else:
                print(f"  {issue['message']}", file=sys.stderr)

        print("", file=sys.stderr)
        print("Recommendation: Add audit trail logging for SOX compliance:", file=sys.stderr)
        print("  import logging", file=sys.stderr)
        print("  from datetime import datetime, timezone", file=sys.stderr)
        print("  ", file=sys.stderr)
        print("  logger = logging.getLogger(__name__)", file=sys.stderr)
        print("  timestamp = datetime.now(timezone.utc).isoformat()", file=sys.stderr)
        print("  logger.info(f'{timestamp} | {user} | {operation} | {source} → {target}')", file=sys.stderr)

        sys.exit(1)  # WARNING

    if infos:
        print(f"ℹ️  Audit Trail Check: {len(infos)} suggestion(s) for {file_path}")
        for issue in infos:
            print(f"  {issue['message']}")

    # All checks passed
    print(f"✅ Audit Trail Check PASSED: {file_path}")
    sys.exit(0)


if __name__ == '__main__':
    main()
