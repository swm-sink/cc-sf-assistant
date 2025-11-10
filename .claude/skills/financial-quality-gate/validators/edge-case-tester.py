#!/usr/bin/env python3
"""Edge case test coverage validator.

Validates that financial calculation tests cover mandatory edge cases:
- Zero division (budget = 0)
- Negative values (reversals, credits)
- NULL/missing data
- Large numbers (billions)
- Precision boundaries (very small Decimals)

WARNING validator - exits with code 1 if edge cases not tested.
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple, Set


# Edge case patterns to detect in test code
EDGE_CASE_PATTERNS = {
    'zero_division': ['budget == 0', 'budget = 0', '/ 0', 'division by zero', 'ZeroDivisionError'],
    'negative_values': ['negative', '< 0', 'reversal', 'credit', '- amount'],
    'null_missing': ['None', 'null', 'missing', 'NaN', 'is None', '== None'],
    'large_numbers': ['billion', '1000000000', '1_000_000_000', 'overflow'],
    'precision': ['0.001', '0.01', 'quantize', 'precision', 'ROUND_HALF_UP']
}


class EdgeCaseTestDetector(ast.NodeVisitor):
    """AST visitor to detect edge case test coverage."""

    def __init__(self):
        self.test_functions: List[Dict[str, Any]] = []
        self.edge_cases_covered: Set[str] = set()
        self.has_pytest_import = False

    def _is_test_function(self, name: str) -> bool:
        """Check if function is a test."""
        return name.startswith('test_') or name.startswith('Test')

    def _detect_edge_cases(self, node: ast.FunctionDef) -> Set[str]:
        """Detect which edge cases are covered in test function."""
        covered = set()

        # Get function source as string (simplified - would need source context)
        func_name_lower = node.name.lower()

        # Check function name for edge case keywords
        for edge_type, patterns in EDGE_CASE_PATTERNS.items():
            for pattern in patterns:
                pattern_lower = pattern.lower().replace(' ', '_')
                if pattern_lower in func_name_lower:
                    covered.add(edge_type)
                    break

        # Walk through function body to detect edge case patterns
        for child in ast.walk(node):
            # Check for string literals containing edge case patterns
            if isinstance(child, ast.Constant) and isinstance(child.value, str):
                value_lower = child.value.lower()
                for edge_type, patterns in EDGE_CASE_PATTERNS.items():
                    for pattern in patterns:
                        if pattern.lower() in value_lower:
                            covered.add(edge_type)
                            break

            # Check for numeric comparisons (e.g., budget == 0)
            if isinstance(child, ast.Compare):
                # Check for comparison with 0
                for comparator in child.comparators:
                    if isinstance(comparator, ast.Constant) and comparator.value == 0:
                        covered.add('zero_division')

            # Check for None comparisons
            if isinstance(child, ast.Compare):
                for comparator in child.comparators:
                    if isinstance(comparator, ast.Constant) and comparator.value is None:
                        covered.add('null_missing')

            # Check for negative number literals
            if isinstance(child, ast.UnaryOp) and isinstance(child.op, ast.USub):
                if isinstance(child.operand, ast.Constant):
                    if isinstance(child.operand.value, (int, float)) and child.operand.value > 0:
                        covered.add('negative_values')

        return covered

    def visit_Import(self, node: ast.Import) -> None:
        """Check for pytest import."""
        for alias in node.names:
            if alias.name == 'pytest':
                self.has_pytest_import = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Check for pytest import."""
        if node.module and node.module.startswith('pytest'):
            self.has_pytest_import = True
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Check test functions for edge case coverage."""
        if self._is_test_function(node.name):
            edge_cases = self._detect_edge_cases(node)
            self.test_functions.append({
                'name': node.name,
                'line': node.lineno,
                'edge_cases': edge_cases
            })
            # Add to global coverage
            self.edge_cases_covered.update(edge_cases)

        self.generic_visit(node)


def validate_file(file_path: Path) -> Tuple[bool, List[Dict[str, Any]]]:
    """Validate a Python test file for edge case coverage.

    Args:
        file_path: Path to Python test file

    Returns:
        Tuple of (is_valid, issues_list)
    """
    issues = []

    # Only validate test files
    if not ('test_' in file_path.name or file_path.name.startswith('test')):
        return True, []

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

    # Detect edge case coverage
    detector = EdgeCaseTestDetector()
    detector.visit(tree)

    # If no test functions found, skip validation
    if not detector.test_functions:
        return True, []

    # Check which edge cases are missing
    all_edge_cases = set(EDGE_CASE_PATTERNS.keys())
    missing_edge_cases = all_edge_cases - detector.edge_cases_covered

    if missing_edge_cases:
        missing_list = ', '.join(sorted(missing_edge_cases))
        issues.append({
            'line': 0,
            'type': 'missing_edge_cases',
            'message': f'Missing edge case tests: {missing_list}',
            'severity': 'WARNING'
        })

        # Provide specific recommendations for each missing edge case
        for edge_case in sorted(missing_edge_cases):
            recommendation = get_edge_case_recommendation(edge_case)
            issues.append({
                'line': 0,
                'type': 'edge_case_recommendation',
                'message': recommendation,
                'severity': 'INFO'
            })

    return True, issues


def get_edge_case_recommendation(edge_case: str) -> str:
    """Get specific recommendation for missing edge case."""
    recommendations = {
        'zero_division': 'Test zero division: budget = Decimal("0"), actual = Decimal("100") → variance_pct should be None',
        'negative_values': 'Test negative values: revenue reversal with actual < 0, expense credit with amount < 0',
        'null_missing': 'Test NULL/missing data: unmatched accounts, missing budget for actual expense',
        'large_numbers': 'Test large numbers: amounts in billions (Decimal("1000000000.00")), verify no overflow',
        'precision': 'Test precision boundaries: very small amounts (Decimal("0.001")), verify exact representation'
    }
    return recommendations.get(edge_case, f'Add test for {edge_case}')


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: edge-case-tester.py <file_path>", file=sys.stderr)
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
        print(f"⚠️  Edge Case Coverage: {len(warnings)} warning(s) for {file_path}", file=sys.stderr)
        print("", file=sys.stderr)

        for issue in warnings:
            print(f"  {issue['message']}", file=sys.stderr)

        if infos:
            print("", file=sys.stderr)
            print("Recommendations:", file=sys.stderr)
            for issue in infos:
                print(f"  • {issue['message']}", file=sys.stderr)

        sys.exit(1)  # WARNING

    # All checks passed
    print(f"✅ Edge Case Coverage PASSED: {file_path}")
    sys.exit(0)


if __name__ == '__main__':
    main()
