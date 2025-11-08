# FP&A Automation Assistant - Technical Planning Document

**Version:** 1.0-DRAFT
**Last Updated:** 2025-11-08
**Status:** 🚧 IN PLANNING
**References:** spec.md (business requirements), CLAUDE.md (behavioral rules)

**Key Principle:** spec.md defines WHAT to build. This document defines HOW to build it.

---

## Table of Contents

1. [Technology Stack](#technology-stack)
2. [Architecture Overview](#architecture-overview)
3. [Implementation Strategy](#implementation-strategy)
4. [Directory Structure](#directory-structure)
5. [Code Quality Standards](#code-quality-standards)
6. [Testing Strategy](#testing-strategy)
7. [Deployment Approach](#deployment-approach)
8. [Performance Considerations](#performance-considerations)
9. [Security & Compliance](#security--compliance)
10. [Development Workflow](#development-workflow)

---

## Technology Stack

### Core Languages & Runtime

**Python 3.11+**
- Rationale: Industry standard for data processing, extensive library ecosystem
- Decimal type built-in for financial precision
- Type hints support for code quality
- Async/await for potential concurrent operations

### Required Dependencies

```python
# Core Data Processing
pandas==2.2.0                    # DataFrame operations [VERIFIED: Latest stable]
numpy==1.26.3                    # Numerical computations (NOT for currency)
openpyxl==3.1.2                  # Excel read/write (.xlsx)
xlrd==2.0.1                      # Legacy Excel (.xls) if needed

# Google Workspace Integration
gspread==6.1.2                   # Google Sheets API
google-auth==2.35.0              # Authentication
google-api-python-client==2.150.0  # Slides/Drive API

# Presentation & Reporting
python-pptx==1.0.2               # PowerPoint generation (if needed)
matplotlib==3.9.2                # Static charts
plotly==5.24.1                   # Interactive dashboards (optional)

# Utilities
python-dotenv==1.0.1             # Environment configuration
pyyaml==6.0.1                    # Config file parsing
typing-extensions==4.9.0         # Extended type hints

# Development & Testing
pytest==7.4.3                    # Testing framework
pytest-cov==4.1.0                # Coverage reporting
black==23.12.1                   # Code formatting
mypy==1.7.1                      # Static type checking
ruff==0.1.9                      # Fast linting
```

### Version Management

**Tool:** `pyenv` for Python version management
**Approach:** Pin all dependencies to exact versions in `requirements.txt`
**Updates:** Review quarterly for security patches

---

## Architecture Overview

### Separation of Concerns

Following Anthropic best practices for Claude Code projects:

```
┌────────────────────────────────────────────────────────┐
│                    Configuration Layer                  │
│  - spec.md (WHAT to build)                             │
│  - plan.md (HOW to build - this document)             │
│  - CLAUDE.md (behavioral rules)                         │
└────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Skills     │ │  Commands    │ │   Agents     │
│ (Auto)       │ │  (Manual)    │ │ (Sub)        │
└──────────────┘ └──────────────┘ └──────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
┌────────────────────────────────────────────────────────┐
│                 Implementation Layer                    │
│  /src                                                   │
│  ├── core/           (business logic)                  │
│  ├── integrations/   (external APIs)                   │
│  ├── reporting/      (output generation)               │
│  └── utils/          (helpers)                         │
└────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────┐
│                    Data Layer                          │
│  /data                                                  │
│  ├── input/          (source files - git-ignored)      │
│  ├── output/         (generated reports - git-ignored) │
│  └── templates/      (report templates - versioned)    │
└────────────────────────────────────────────────────────┘
```

### Key Architectural Patterns

**1. Progressive Disclosure (Skills)**
- Metadata loaded at startup
- Full content loaded on-demand
- Reduces token usage, improves performance

**2. Human-in-Loop (Commands)**
- Checkpoints at decision points
- Prevents automated errors
- Maintains user control

**3. Context Isolation (Agents)**
- Independent verification
- Unbiased code review
- Separate tool access

**4. Quality Gates (Hooks)**
- Automated enforcement
- No reliance on model memory
- Fail-fast on critical issues

---

## Implementation Strategy

### Epic 1: Monthly Close Automation

#### Story 1.1: Multi-Department Data Consolidation

**Technical Approach:**

1. **File Discovery**
```python
# src/core/file_discovery.py
from pathlib import Path
from typing import List, Dict

def discover_excel_files(folder_path: str) -> List[Path]:
    """
    Discover all Excel files in folder.

    Returns:
        List of Path objects for .xlsx and .xls files
    """
    path = Path(folder_path)
    excel_files = list(path.glob("*.xlsx")) + list(path.glob("*.xls"))
    return sorted(excel_files)  # Deterministic order
```

2. **Structure Validation**
```python
# Uses financial-validator skill
from decimal import Decimal
import pandas as pd

def validate_department_file(
    file_path: Path,
    required_columns: List[str]
) -> Tuple[bool, List[str]]:
    """
    Validate department file structure.

    Returns:
        (is_valid, list_of_issues)
    """
    # Load file
    df = pd.read_excel(file_path, engine='openpyxl')

    issues = []

    # Check required columns
    missing = set(required_columns) - set(df.columns)
    if missing:
        issues.append(f"Missing columns: {missing}")

    # Check data types
    # Validate amounts are numeric
    # Flag NULL values

    return len(issues) == 0, issues
```

3. **Account Mapping**
```python
# config/account_mapping.yaml loaded via PyYAML
# Maps department-specific codes to corporate chart of accounts

def map_account_codes(
    department_df: pd.DataFrame,
    mapping_config: Dict[str, str]
) -> pd.DataFrame:
    """
    Map department account codes to corporate codes.

    Uses account_mapping.yaml configuration.
    """
    df = department_df.copy()
    df['corporate_account'] = df['account_code'].map(mapping_config)

    # Flag unmapped accounts
    unmapped = df[df['corporate_account'].isna()]
    if not unmapped.empty:
        # Log warning, create reconciliation report
        pass

    return df
```

4. **Consolidation**
```python
def consolidate_departments(
    files: List[Path],
    mapping_config: Dict
) -> Tuple[pd.DataFrame, Dict]:
    """
    Consolidate all department files.

    Returns:
        (consolidated_df, metadata)
    """
    all_data = []
    metadata = {
        'source_files': [],
        'records_per_file': {},
        'unmatched_accounts': [],
        'timestamp': datetime.now(UTC).isoformat()
    }

    for file in files:
        df = load_and_validate(file)
        df = map_account_codes(df, mapping_config)
        df['source_file'] = str(file)

        all_data.append(df)
        metadata['source_files'].append(str(file))
        metadata['records_per_file'][str(file)] = len(df)

    consolidated = pd.concat(all_data, ignore_index=True)

    return consolidated, metadata
```

**Testing Approach:**
- Unit tests for each function with edge cases
- Integration test with sample department files
- Reconciliation report validation

---

#### Story 2.1: Budget vs. Actual Variance Calculation

**Technical Approach:**

```python
# src/core/variance_calculator.py
from decimal import Decimal, ROUND_HALF_UP
from typing import Tuple, Optional, Literal

def calculate_variance(
    actual: Decimal,
    budget: Decimal,
    account_type: Literal['revenue', 'expense', 'asset', 'liability']
) -> Tuple[Decimal, Optional[Decimal], bool, str]:
    """
    Calculate financial variance with edge case handling.

    Args:
        actual: Actual amount (Decimal required)
        budget: Budget amount (Decimal required)
        account_type: Type for favorability logic

    Returns:
        (absolute_variance, percentage_variance, is_favorable, status)

    Raises:
        TypeError: If actual or budget are not Decimal
        ValueError: If account_type invalid
    """
    # Type validation (enforced by financial-validator skill)
    if not isinstance(actual, Decimal):
        raise TypeError(f"actual must be Decimal, got {type(actual)}")
    if not isinstance(budget, Decimal):
        raise TypeError(f"budget must be Decimal, got {type(budget)}")

    # Calculate absolute variance
    absolute_variance = actual - budget

    # Calculate percentage variance (handle zero division)
    if budget == Decimal('0'):
        if actual == Decimal('0'):
            percentage_variance = Decimal('0')
            status = "No Activity"
        else:
            percentage_variance = None  # Cannot calculate
            status = "Zero Budget - Flag for Review"
    else:
        pct = (absolute_variance / budget) * Decimal('100')
        percentage_variance = pct.quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )
        status = "Normal"

    # Determine favorability
    if account_type == 'revenue':
        is_favorable = (actual > budget)
    elif account_type == 'expense':
        is_favorable = (actual < budget)
    elif account_type == 'asset':
        is_favorable = (actual > budget)
    elif account_type == 'liability':
        is_favorable = (actual < budget)
    else:
        raise ValueError(f"Invalid account_type: {account_type}")

    return absolute_variance, percentage_variance, is_favorable, status
```

**Testing Requirements:**
- Edge cases from `.claude/skills/financial-validator/references/edge-cases.md`
- All 10 categories must pass
- Type enforcement validated
- Decimal precision verified

---

### Epic 3: Management Reporting

#### Story 3.1: Variance Report Generation

**Technical Approach:**

```python
# src/reporting/excel_report_builder.py
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, numbers
from typing import Dict

def create_variance_report(
    variance_data: pd.DataFrame,
    output_path: str,
    metadata: Dict
) -> None:
    """
    Generate Excel workbook with variance analysis.

    Sheets:
    1. Executive Summary
    2. Detailed Variance Analysis
    3. Material Variances Only
    4. Metadata/Audit Trail
    """
    wb = Workbook()

    # Sheet 1: Executive Summary
    ws_summary = wb.active
    ws_summary.title = "Executive Summary"
    create_summary_sheet(ws_summary, variance_data)

    # Sheet 2: Detailed Analysis
    ws_detail = wb.create_sheet("Detailed Analysis")
    create_detail_sheet(ws_detail, variance_data)

    # Sheet 3: Material Variances
    ws_material = wb.create_sheet("Material Variances")
    material_data = variance_data[variance_data['is_material'] == True]
    create_material_sheet(ws_material, material_data)

    # Sheet 4: Metadata
    ws_meta = wb.create_sheet("Metadata")
    create_metadata_sheet(ws_meta, metadata)

    # Apply conditional formatting
    apply_conditional_formatting(ws_detail)

    # Save
    wb.save(output_path)
```

**Conditional Formatting Rules:**
- Green: Favorable & Material
- Red: Unfavorable & Material
- Yellow: Favorable but Immaterial
- Gray: Unfavorable but Immaterial

---

## Directory Structure

```
fpa-automation-assistant/
├── spec.md                      # WHAT to build (business requirements)
├── plan.md                      # HOW to build (this document)
├── CLAUDE.md                    # Behavioral configuration
├── README.md                    # Project overview
│
├── .claude/                     # Claude Code configuration
│   ├── skills/                  # Auto-invoked capabilities
│   │   ├── financial-validator/
│   │   │   ├── SKILL.md
│   │   │   ├── references/edge-cases.md
│   │   │   └── scripts/validate_precision.py
│   │   ├── excel-extractor/
│   │   └── variance-calculator/
│   ├── commands/                # Manual slash commands
│   │   ├── variance-analysis.md
│   │   ├── consolidate-data.md
│   │   └── update-slides.md
│   ├── agents/                  # Subagents
│   │   ├── code-reviewer.md
│   │   ├── data-analyst.md
│   │   └── research-specialist.md
│   └── hooks/                   # Quality gates
│       ├── stop.sh
│       └── pre-commit.sh
│
├── src/                         # Implementation
│   ├── __init__.py
│   ├── core/                    # Business logic
│   │   ├── __init__.py
│   │   ├── variance_calculator.py
│   │   ├── financial_metrics.py
│   │   ├── data_validator.py
│   │   └── account_mapper.py
│   ├── integrations/            # External systems
│   │   ├── __init__.py
│   │   ├── excel_handler.py
│   │   ├── google_sheets_client.py
│   │   └── google_slides_client.py
│   ├── reporting/               # Output generation
│   │   ├── __init__.py
│   │   ├── excel_report_builder.py
│   │   └── chart_generator.py
│   └── utils/                   # Helpers
│       ├── __init__.py
│       ├── config_loader.py
│       ├── logger.py
│       └── file_utils.py
│
├── config/                      # Configuration
│   ├── fpa_config.yaml          # Business rules (thresholds, etc.)
│   ├── account_mapping.yaml     # Chart of accounts mapping
│   ├── .env.example             # Environment template
│   └── credentials.json         # Google service account (git-ignored)
│
├── data/                        # Data files (git-ignored except templates)
│   ├── input/                   # Source files
│   ├── output/                  # Generated reports
│   └── templates/               # Report templates (versioned)
│       ├── variance_report_template.xlsx
│       └── board_presentation_template.pptx
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── unit/                    # Unit tests
│   │   ├── test_variance_calculator.py
│   │   ├── test_data_validator.py
│   │   └── test_financial_metrics.py
│   ├── integration/             # Integration tests
│   │   ├── test_consolidation_workflow.py
│   │   └── test_variance_analysis_e2e.py
│   └── fixtures/                # Test data
│       ├── sample_budget.xlsx
│       └── sample_actuals.xlsx
│
├── logs/                        # Application logs (git-ignored)
├── .gitignore
├── requirements.txt             # Python dependencies
├── requirements-dev.txt         # Development dependencies
├── setup.py or pyproject.toml   # Package configuration
└── Makefile                     # Common commands
```

---

## Code Quality Standards

### Type Hints (MANDATORY)

```python
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Literal
from datetime import datetime

def calculate_variance(
    actual: Decimal,
    budget: Decimal,
    account_type: Literal['revenue', 'expense', 'asset', 'liability']
) -> Tuple[Decimal, Optional[Decimal], bool, str]:
    """Full type hints on ALL functions."""
    pass
```

### Docstring Format (Google Style)

```python
def consolidate_departments(
    files: List[Path],
    mapping_config: Dict[str, str]
) -> Tuple[pd.DataFrame, Dict]:
    """
    Consolidate department Excel files into single DataFrame.

    Args:
        files: List of Path objects to Excel files
        mapping_config: Dict mapping dept codes to corporate codes

    Returns:
        Tuple of (consolidated_dataframe, metadata_dict)

    Raises:
        FileNotFoundError: If file in list doesn't exist
        ValueError: If file structure validation fails

    Example:
        >>> files = [Path("sales.xlsx"), Path("marketing.xlsx")]
        >>> mapping = {"S001": "4000", "M001": "6000"}
        >>> df, meta = consolidate_departments(files, mapping)
    """
    pass
```

### Error Handling Pattern

```python
import logging
from typing import Any

logger = logging.getLogger(__name__)

class FinancialCalculationError(Exception):
    """Base exception for financial calculation errors."""
    pass

class DivisionByZeroError(FinancialCalculationError):
    """Raised when attempting to divide by zero budget."""
    pass

class InvalidAccountTypeError(FinancialCalculationError):
    """Raised when account type is not recognized."""
    pass

def safe_calculation(actual: Decimal, budget: Decimal) -> Decimal:
    """
    Perform calculation with comprehensive error handling.
    """
    try:
        if budget == Decimal('0'):
            logger.warning(f"Zero budget detected: actual={actual}")
            raise DivisionByZeroError(
                f"Cannot calculate percentage with zero budget. "
                f"Actual: {actual}, Budget: {budget}"
            )

        result = (actual / budget) * Decimal('100')

        logger.info(f"Calculation successful: {result}%")
        return result

    except DivisionByZeroError:
        # Re-raise custom exceptions
        raise
    except Exception as e:
        # Catch unexpected errors, log with context
        logger.error(
            f"Unexpected error in calculation: {e}",
            extra={'actual': str(actual), 'budget': str(budget)}
        )
        raise FinancialCalculationError(
            f"Calculation failed: {e}"
        ) from e
```

### Logging Standards

```python
import logging
from datetime import datetime, UTC

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/fpa_assistant.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usage
logger.info(
    "Variance calculated",
    extra={
        'account': account_code,
        'absolute_variance': str(abs_var),
        'percentage_variance': str(pct_var) if pct_var else 'N/A',
        'is_favorable': is_favorable,
        'timestamp': datetime.now(UTC).isoformat()
    }
)
```

---

## Testing Strategy

### Unit Testing

**Coverage Target:** 80%+ for all modules

```python
# tests/unit/test_variance_calculator.py
import pytest
from decimal import Decimal
from src.core.variance_calculator import calculate_variance

class TestVarianceCalculator:
    """Comprehensive unit tests for variance calculations."""

    def test_normal_revenue_variance(self):
        """Test standard revenue variance calculation."""
        abs_var, pct_var, is_fav, status = calculate_variance(
            Decimal('115000'),
            Decimal('100000'),
            'revenue'
        )

        assert abs_var == Decimal('15000')
        assert pct_var == Decimal('15.00')
        assert is_fav == True
        assert status == "Normal"

    def test_zero_budget_zero_actual(self):
        """Test edge case: both values zero."""
        abs_var, pct_var, is_fav, status = calculate_variance(
            Decimal('0'),
            Decimal('0'),
            'expense'
        )

        assert abs_var == Decimal('0')
        assert pct_var == Decimal('0')
        assert status == "No Activity"

    def test_float_rejection(self):
        """Test that float types are rejected."""
        with pytest.raises(TypeError, match="must be Decimal"):
            calculate_variance(
                115000.00,  # float - should fail
                Decimal('100000'),
                'revenue'
            )

    @pytest.mark.parametrize("account_type,actual,budget,expected_favorable", [
        ('revenue', Decimal('110'), Decimal('100'), True),
        ('revenue', Decimal('90'), Decimal('100'), False),
        ('expense', Decimal('90'), Decimal('100'), True),
        ('expense', Decimal('110'), Decimal('100'), False),
        ('asset', Decimal('110'), Decimal('100'), True),
        ('liability', Decimal('90'), Decimal('100'), True),
    ])
    def test_favorability_logic(
        self, account_type, actual, budget, expected_favorable
    ):
        """Test favorability for all account types."""
        _, _, is_fav, _ = calculate_variance(actual, budget, account_type)
        assert is_fav == expected_favorable
```

### Integration Testing

```python
# tests/integration/test_variance_analysis_e2e.py
import pytest
from pathlib import Path
from src.core.variance_analyzer import VarianceAnalyzer

class TestVarianceAnalysisEndToEnd:
    """End-to-end integration tests."""

    @pytest.fixture
    def sample_files(self, tmp_path):
        """Create sample budget and actuals files."""
        budget_file = tmp_path / "budget.xlsx"
        actuals_file = tmp_path / "actuals.xlsx"

        # Create sample files with test data
        # ... (file creation logic)

        return budget_file, actuals_file

    def test_full_workflow(self, sample_files):
        """Test complete variance analysis workflow."""
        budget_file, actuals_file = sample_files
        output_file = Path("tests/output/variance_report.xlsx")

        analyzer = VarianceAnalyzer()
        result = analyzer.analyze(
            budget_file=str(budget_file),
            actuals_file=str(actuals_file),
            output_file=str(output_file)
        )

        assert result.success == True
        assert output_file.exists()
        assert result.material_variances_count > 0

        # Verify output structure
        # ... (detailed assertions)
```

### Edge Case Testing

**All edge cases from `.claude/skills/financial-validator/references/edge-cases.md` MUST pass:**

1. Float precision errors
2. Division by zero (3 scenarios)
3. Negative values
4. NULL/missing data
5. Concurrent transactions
6. Multi-currency
7. Rounding precision
8. Boundary conditions
9. Data type mismatches
10. Large numbers/overflow

**Validation Script:**
Run before every commit:
```bash
python .claude/skills/financial-validator/scripts/validate_precision.py
```

---

## Deployment Approach

### Environment Setup

**Development:**
```bash
# 1. Python environment
pyenv install 3.11.7
pyenv local 3.11.7
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Configuration
cp config/.env.example config/.env
# Edit .env with appropriate values

# 4. Verify setup
python .claude/skills/financial-validator/scripts/validate_precision.py
pytest tests/ -v
```

**Production:**
[TO BE DETERMINED - depends on deployment target]
- Option 1: Local installation per user
- Option 2: Shared server deployment
- Option 3: Cloud function (serverless)

### Configuration Management

**config/fpa_config.yaml:**
```yaml
# Business rules and thresholds
variance_thresholds:
  percentage: 0.10  # 10%
  absolute: 50000   # $50,000

favorability_rules:
  revenue: "actual_gt_budget"
  expense: "actual_lt_budget"
  asset: "actual_gt_budget"
  liability: "actual_lt_budget"

output_settings:
  excel_formats:
    currency: "$#,##0.00"
    percentage: "0.00%"
  conditional_formatting:
    favorable_material: "#00FF00"    # Green
    unfavorable_material: "#FF0000"  # Red
    favorable_immaterial: "#FFFF00"  # Yellow
    unfavorable_immaterial: "#808080" # Gray
```

---

## Performance Considerations

### Data Volume Handling

**Small Datasets (<1,000 rows):**
- Load entire file into memory
- Process in single pass
- Expected time: <10 seconds

**Medium Datasets (1,000-10,000 rows):**
- Load into memory with chunking if needed
- Process in batches of 5,000
- Expected time: <60 seconds

**Large Datasets (>10,000 rows):**
- Use chunked reading: `pd.read_excel(chunksize=5000)`
- Process incrementally
- Write results progressively
- Expected time: [TO BE MEASURED based on testing]

### Optimization Strategy

**Rule:** No premature optimization

**Approach:**
1. Implement with clarity and correctness first
2. Profile with realistic data
3. Optimize bottlenecks only
4. Measure improvements
5. Document performance characteristics

**Profiling:**
```python
import cProfile
import pstats

def profile_variance_analysis():
    """Profile variance analysis performance."""
    profiler = cProfile.Profile()
    profiler.enable()

    # Run analysis
    analyzer.analyze(budget_file, actuals_file, output_file)

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
```

---

## Security & Compliance

### Data Protection

**Sensitive Data (NEVER commit):**
- `.env` files with credentials
- `credentials.json` (Google service account)
- Actual financial data in `/data/input/`
- Generated reports in `/data/output/`
- Log files with PII

**Gitignore Rules:**
```
# Credentials
.env
credentials.json
*.pem
*.key

# Data
data/input/
data/output/
logs/

# Environment
venv/
__pycache__/
*.pyc
```

### Audit Trail Requirements

**Every transformation must log:**
```python
audit_entry = {
    'timestamp': datetime.now(UTC).isoformat(),
    'user': os.getenv('USER', 'unknown'),
    'operation': 'variance_calculation',
    'source_files': [str(budget_file), str(actuals_file)],
    'output_file': str(output_file),
    'records_processed': len(df),
    'thresholds': {
        'percentage': config['percentage_threshold'],
        'absolute': config['absolute_threshold']
    },
    'material_variances_count': material_count,
    'errors': error_list
}

logger.info("Audit trail", extra=audit_entry)
```

### Access Control

**File Permissions:**
- Configuration files: Read-only after setup
- Credentials: Restricted to application user
- Output files: User-specific access

**API Authentication:**
- Google Workspace: Service account with minimal scopes
- Read-only access where possible
- Scope limitation per function

---

## Development Workflow

### Git Branch Strategy

**Branches:**
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/epic-1-story-1` - Feature branches
- `bugfix/issue-123` - Bug fixes
- `claude/session-id` - Claude Code branches

**Workflow:**
1. Create feature branch from `develop`
2. Implement with tests
3. Run quality gates (hooks)
4. Create PR to `develop`
5. Code review (@code-reviewer agent)
6. Merge after approval
7. Periodic merge `develop` → `main`

### Commit Message Format

```
type(scope): short description

Longer description if needed.

- Bullet points for details
- Reference issues: Closes #123
- Reference specs: Implements spec.md Story 1.1
```

**Types:** feat, fix, docs, test, refactor, chore

### Quality Gates (Automated)

**Pre-commit (Local):**
- Black formatting
- Ruff linting
- MyPy type checking
- Basic test suite

**Stop Hook (Claude Code):**
- Float usage check (BLOCKING)
- Type hints check (WARNING)
- Financial validator tests
- Python syntax validation

**CI/CD (Future):**
- Full test suite
- Coverage report
- Security scanning
- Performance benchmarks

---

## Next Steps & Priorities

### Phase 1: Foundation (Current)
- [x] Architecture design
- [x] CLAUDE.md behavioral configuration
- [x] Financial validator skill
- [x] Quality gates (hooks)
- [ ] Core directory structure
- [ ] Base classes and utilities

### Phase 2: Epic 1 Implementation
- [ ] Story 1.1: Multi-department consolidation
- [ ] Story 1.2: GL account reconciliation
- [ ] Unit tests for Epic 1
- [ ] Integration tests
- [ ] Documentation

### Phase 3: Epic 2 Implementation
- [ ] Story 2.1: Variance calculation
- [ ] Story 2.2: Favorability assessment
- [ ] Story 2.3: Materiality flagging
- [ ] Comprehensive edge case testing
- [ ] Independent verification

### Phase 4: Epic 3 Implementation
- [ ] Story 3.1: Excel report generation
- [ ] Story 3.2: Google Slides integration
- [ ] Template system
- [ ] Chart generation

### Phase 5: Production Readiness
- [ ] Performance optimization
- [ ] Security audit
- [ ] User documentation
- [ ] Deployment packaging
- [ ] Training materials

---

## Architecture Restructure (Added 2025-11-08)

### Decision: Claude Code-Native Approach

**Change:** Shifted from traditional Python package distribution (`packages/fpa-core`, etc.) to Claude Code-native architecture (`.claude/` skills, commands, agents).

**Rationale:**
- Target users are FP&A professionals, not developers
- Conversational interface with human-in-loop matches FP&A approval workflows
- No installation burden for end users
- Iterative refinement via markdown editing (non-technical)

### Directory Structure (Final)

```
cc-sf-assistant/
├── .claude/
│   ├── agents/
│   │   ├── dev/                      # Development agents
│   │   │   ├── script-generator.md
│   │   │   ├── script-validator.md
│   │   │   ├── test-generator.md
│   │   │   └── code-reviewer.md
│   │   ├── prod/                     # Production agents
│   │   │   ├── finance-reviewer.md
│   │   │   ├── data-validator.md
│   │   │   └── reconciler.md
│   │   └── shared/
│   │       └── research-agent.md
│   │
│   ├── commands/
│   │   ├── dev/                      # Development workflows
│   │   │   ├── create-script.md      # /dev:create-script
│   │   │   ├── validate-script.md    # /dev:validate-script
│   │   │   └── review-code.md        # /dev:review-code
│   │   ├── prod/                     # Production workflows
│   │   │   ├── monthly-close.md      # /prod:monthly-close
│   │   │   ├── variance-analysis.md  # /prod:variance-analysis
│   │   │   ├── consolidate.md        # /prod:consolidate
│   │   │   └── board-deck.md         # /prod:board-deck
│   │   └── shared/
│   │       ├── help.md
│   │       └── config.md
│   │
│   ├── skills/
│   │   ├── dev/                      # Dev skills (auto-invoked during dev)
│   │   │   ├── python-best-practices/
│   │   │   ├── financial-script-generator/
│   │   │   └── test-suite-generator/
│   │   ├── prod/                     # Prod skills (auto-invoked during prod)
│   │   │   ├── variance-analyzer/
│   │   │   ├── account-mapper/
│   │   │   └── report-generator/
│   │   └── shared/                   # Shared skills (always auto-invoked)
│   │       ├── decimal-precision-enforcer/
│   │       └── audit-trail-enforcer/
│   │
│   ├── templates/                    # Templates for creating skills/commands/agents
│   │   ├── skills/SKILL_TEMPLATE.md
│   │   ├── commands/COMMAND_TEMPLATE.md
│   │   ├── agents/AGENT_TEMPLATE.md
│   │   └── workflows/
│   │       ├── TDD_WORKFLOW.md
│   │       └── RESEARCH_PLAN_IMPLEMENT_VERIFY.md
│   │
│   └── hooks/
│       └── stop.sh                   # Quality gate (runs after every response)
│
├── scripts/                          # Pre-written validated calculation scripts
│   ├── core/
│   │   ├── variance.py
│   │   ├── consolidation.py
│   │   ├── favorability.py
│   │   └── materiality.py
│   ├── integrations/
│   │   ├── gsheet_reader.py
│   │   ├── gsheet_writer.py
│   │   ├── excel_reader.py
│   │   ├── excel_writer.py
│   │   └── gslides_generator.py
│   ├── workflows/
│   │   ├── monthly_close.py
│   │   ├── variance_report.py
│   │   └── board_deck.py
│   └── utils/
│       ├── logger.py
│       ├── validator.py
│       └── config_loader.py
│
├── external/                         # Cloned GitHub repos (git submodules)
│   ├── humanlayer/
│   ├── mcp-gdrive/
│   ├── gspread/
│   ├── slidio/
│   ├── pyfpa/
│   └── py-money/
│
├── templates/                        # Report templates
│   ├── variance_report.xlsx
│   ├── board_deck.pptx
│   └── consolidated_report.xlsx
│
├── tests/                            # Comprehensive test suite
│   ├── test_variance.py
│   ├── test_consolidation.py
│   ├── test_integrations.py
│   └── test_edge_cases.py
│
├── config/
│   ├── settings.yaml
│   └── credentials/                  # OAuth + service account keys
│
├── docs/
│   ├── COMPREHENSIVE_GITHUB_SOURCES.md
│   ├── user-guides/
│   └── workflows/
│
├── spec.md
├── plan.md
├── CLAUDE.md
├── README.md
├── EXTERNAL_DEPENDENCIES.md
├── pyproject.toml
└── .gitignore
```

### Workflow Separation: Dev vs Prod

#### **Dev Workflows** (Script Generation)
**Purpose:** Generate new financial calculation scripts when needed.

**Trigger:** User requests analysis not covered by existing scripts.
**Example:** `/dev:create-script "Calculate YoY revenue growth by department"`

**Process:**
1. Research existing patterns (no coding)
2. Generate formal specification
3. Get human approval on spec
4. Follow TDD workflow:
   - RED: Write failing tests
   - GREEN: Implement with Decimal
   - REFACTOR: Add docstrings, error handling, logging
   - VALIDATE: Independent agent review
5. Human approval on final script
6. Save to `scripts/` directory
7. Script now available for prod workflows

**Skills Auto-Invoked:**
- `python-best-practices` - Enforces Decimal, type hints, error handling
- `financial-script-generator` - Uses variance/consolidation patterns
- `test-suite-generator` - Generates edge case tests
- `decimal-precision-enforcer` - Blocks float usage
- `audit-trail-enforcer` - Ensures logging

**Agents Used:**
- `script-generator` - Writes Python code from spec
- `test-generator` - Creates comprehensive tests
- `script-validator` - Runs pytest, mypy, ruff, bandit, coverage
- `code-reviewer` - Independent review (separate context, read-only)

#### **Prod Workflows** (Script Execution)
**Purpose:** Execute pre-written, validated scripts for daily FP&A tasks.

**Trigger:** User requests common FP&A analysis.
**Example:** `/prod:variance-analysis budget.xlsx actuals.xlsx`

**Process:**
1. Execute pre-written script from `scripts/`
2. Human reviews results (e.g., flagged variances)
3. Human approves report
4. Export to Excel or Google Sheets
5. Audit trail logged

**Skills Auto-Invoked:**
- `variance-analyzer` - Validates variance calculations
- `account-mapper` - Handles unmapped accounts
- `report-generator` - Formats output
- `decimal-precision-enforcer` - Validates precision
- `audit-trail-enforcer` - Logs transformations

**Agents Used:**
- `finance-reviewer` - Reviews financial outputs for accuracy
- `data-validator` - Validates input data quality
- `reconciler` - Reconciles unmapped accounts with human input

### Data Integration Approach

#### Phase 1: Excel-First (MVP)
- Focus on local Excel file processing
- Libraries: openpyxl (read), xlsxwriter (write with formatting)
- No cloud dependencies
- Works offline
- Faster development

#### Phase 2: Google Integration
- Google Sheets: gspread + gspread-dataframe
- Google Slides: slidio patterns (or custom implementation)
- Authentication: OAuth + Service Account JSON
- Credentials: `config/credentials/`
- Skills to convert Excel → Google workflows

### Script Generation Validation Requirements

**Problem:** LLMs cannot be trusted to perform financial math directly (hallucination risk).
**Solution:** Generate robust, tested Python scripts that perform deterministic calculations.

**Validation Pipeline (Enforced):**
1. Specification generated and human-approved
2. TDD cycle: Write tests → Implement → Refactor
3. Automated validation:
   - pytest (test execution)
   - mypy (type checking)
   - ruff (linting)
   - bandit (security)
   - coverage (>80% required)
4. Independent code review by separate agent (read-only context)
5. Human final approval
6. Script saved to `scripts/` directory

**Anti-Patterns Blocked:**
- ❌ Float for currency → `decimal-precision-enforcer` blocks
- ❌ Missing type hints → `python-best-practices` requires
- ❌ No error handling → `python-best-practices` requires
- ❌ No audit logging → `audit-trail-enforcer` requires
- ❌ Low test coverage → `script-validator` blocks (<80%)

### External Library Integration Strategy

**Installed via pip:**
- pandas (data manipulation)
- gspread + gspread-dataframe (Google Sheets)
- openpyxl (Excel read)
- xlsxwriter (Excel write with formatting)
- google-auth (authentication)

**Cloned for Reference/Adaptation:**
- humanlayer - Study human-in-loop patterns
- pyfpa - Study FP&A consolidation algorithms (may install if adaptable)
- slidio - Study Google Slides patterns (may install or adapt)
- py-money - Reference Decimal precision (use Python's built-in decimal)
- mcp-gdrive - Study MCP protocol patterns

**Why Keep Cloned Repos:**
- Security audit before use
- Learn implementation patterns
- Pin exact versions (git submodules)
- Offline development
- Customize if needed

### Workflow Templates (`.claude/templates/`)

**Research Findings (10 Sources):**
- GitHub: anthropics/skills (official templates)
- GitHub: alirezarezvani/claude-code-skill-factory (skill factory)
- GitHub: travisvn/awesome-claude-skills (community examples)
- GitHub: Pimzino/claude-code-spec-workflow (RPIV workflow)
- GitHub: nizos/tdd-guard (TDD enforcement)
- Anthropic: Official skills best practices
- Anthropic: Claude Code best practices
- Anthropic: Subagents documentation
- Claude Code TDD guides (multiple sources)
- Community slash command examples

**Created Templates:**
1. **SKILL_TEMPLATE.md** - YAML frontmatter, Progressive Disclosure pattern
2. **COMMAND_TEMPLATE.md** - $ARGUMENTS placeholder, human checkpoints
3. **AGENT_TEMPLATE.md** - Tool permissions, role definition
4. **TDD_WORKFLOW.md** - RED-GREEN-REFACTOR-VALIDATE cycle
5. **RESEARCH_PLAN_IMPLEMENT_VERIFY.md** - Structured feature development

### Implementation Priority

**Phase 1: Infrastructure (Week 1-2)**
- Create `.claude/` directory structure (dev/prod/shared)
- Create templates for skills/commands/agents
- Set up `scripts/` directory
- Configure `pyproject.toml` dependencies
- Set up `tests/` directory with pytest

**Phase 2: Dev Workflows (Week 3-4)**
- Build dev skills (python-best-practices, financial-script-generator, test-suite-generator)
- Build dev agents (script-generator, script-validator, test-generator, code-reviewer)
- Build dev commands (/dev:create-script, /dev:validate-script, /dev:review-code)
- Test script generation pipeline

**Phase 3: Core Scripts - Excel (Week 5-7)**
- Pre-write core calculation scripts (variance, consolidation, favorability, materiality)
- Excel integration scripts (reader, writer)
- Comprehensive tests for all scripts
- Validate with independent code review

**Phase 4: Prod Workflows - Excel (Week 8-10)**
- Build prod skills (variance-analyzer, account-mapper, report-generator)
- Build prod agents (finance-reviewer, data-validator, reconciler)
- Build prod commands (/prod:monthly-close, /prod:variance-analysis, /prod:consolidate)
- End-to-end testing with sample data

**Phase 5: Google Integration (Week 11-13)**
- Google Sheets integration (gspread)
- Google Slides integration (slidio patterns or custom)
- OAuth + Service Account authentication
- Excel → Google conversion skills
- Integration testing

**Phase 6: Polish & Documentation (Week 14-15)**
- User documentation (non-technical guides)
- Workflow documentation
- Training materials
- Performance optimization
- Security audit
- Life360 branding customization (logo, colors, templates)

---

## Implementation Details for Operational Decisions

### 1. Script Versioning (Git-Based)

**Rule:** NEVER create files named `script_v2.py`, `script_v3.py`, `script-new.py`, etc.

**Implementation:**
```bash
# When updating existing script
git add scripts/core/variance.py
git commit -m "feat: add QoQ variance calculation to variance.py"
git push

# To revert to old version
git log scripts/core/variance.py  # Find commit hash
git checkout <commit-hash> scripts/core/variance.py
```

**Enforced By:**
- `.claude/hooks/stop.sh` checks for files matching `*_v[0-9]*.py`, `*-new.py`, `*-old.py` patterns
- Blocks commit if versioned filenames detected

**Benefits:**
- Proper version control with diffs
- Rollback to any previous state
- Clear commit history
- No file naming confusion

---

### 2. Centralized Audit Log

**Structure:**
```
config/
├── audit.log              # Actual audit entries (git ignored)
├── .gitignore             # Ignores audit.log data file
└── audit-schema.json      # Log structure (version controlled)
```

**Audit Entry Format (JSON):**
```json
{
  "timestamp": "2025-11-08T14:32:15.123Z",
  "user": "user@life360.com",
  "script": "scripts/workflows/variance_report.py",
  "operation": "variance_calculation",
  "inputs": {
    "budget_file": "budget_2025.xlsx",
    "actual_file": "actuals_nov.xlsx"
  },
  "outputs": {
    "variance_report": "variance_nov_2025.xlsx",
    "material_variances_count": 3
  },
  "metadata": {
    "execution_time_ms": 2341,
    "rows_processed": 50,
    "errors": []
  }
}
```

**Implementation in Scripts:**
```python
# scripts/utils/logger.py
from loguru import logger
import json
from pathlib import Path
from datetime import datetime

AUDIT_LOG = Path("config/audit.log")

def log_audit_entry(
    script: str,
    operation: str,
    inputs: dict,
    outputs: dict,
    metadata: dict
) -> None:
    """Write structured audit entry to centralized log."""
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": os.getenv("USER", "unknown"),
        "script": script,
        "operation": operation,
        "inputs": inputs,
        "outputs": outputs,
        "metadata": metadata
    }

    with AUDIT_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
```

**Querying Audit Log:**
```python
# Example: Find all variance calculations in November
import json
from pathlib import Path

with Path("config/audit.log").open() as f:
    for line in f:
        entry = json.loads(line)
        if entry["operation"] == "variance_calculation":
            if "2025-11" in entry["timestamp"]:
                print(entry)
```

**Skills/Agents Enforcing:**
- `audit-trail-enforcer` skill checks all scripts import and use `log_audit_entry()`
- `code-reviewer` agent verifies audit logging before approval

---

### 3. Data Validation Pre-Checks

**Workflow Integration:**

Every prod workflow starts with validation phase:

```markdown
## /prod:variance-analysis Workflow

### Phase 1: Data Validation (Automatic)
1. Invoke `data-validator` agent
2. Check budget file:
   - Required columns exist (Account, Department, Amount)
   - Data types correct (Amount is numeric)
   - No NULL values in required fields
   - Amounts are positive decimals
3. Check actual file (same checks)
4. Generate validation report
5. **HUMAN CHECKPOINT:** User reviews validation report and approves/rejects

### Phase 2: Execution (After Approval)
1. Execute variance calculation script
2. Generate report
3. **HUMAN CHECKPOINT:** User reviews variance results
4. Export to Excel/Sheets
5. Log audit entry
```

**Validation Report Format:**
```
📊 Data Validation Report

Budget File: budget_2025.xlsx
✅ File exists and is readable
✅ Required columns present: Account, Department, Amount
✅ Data types valid: Amount is numeric (50/50 rows)
✅ No NULL values in required fields
✅ All amounts are positive Decimals
✅ 50 accounts found

Actual File: actuals_nov.xlsx
✅ File exists and is readable
✅ Required columns present: Account, Department, Amount
⚠️  WARNING: 2 NULL values found in Amount column (rows 23, 47)
✅ Data types valid: Amount is numeric (48/50 rows)
❌ ERROR: 2 amounts are negative (rows 15, 32)
✅ 50 accounts found

❌ VALIDATION FAILED - 1 error, 1 warning

Proceed anyway? (y/n):
```

**Implementation:**
```python
# scripts/utils/validator.py
from decimal import Decimal
import pandas as pd
from typing import NamedTuple

class ValidationResult(NamedTuple):
    passed: bool
    errors: list[str]
    warnings: list[str]
    summary: str

def validate_financial_file(
    file_path: str,
    required_columns: list[str],
    amount_column: str = "Amount"
) -> ValidationResult:
    """Validate Excel file before processing."""
    errors = []
    warnings = []

    # Check file exists
    if not Path(file_path).exists():
        errors.append(f"File not found: {file_path}")
        return ValidationResult(False, errors, warnings, "")

    # Load file
    df = pd.read_excel(file_path)

    # Check required columns
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        errors.append(f"Missing columns: {missing}")

    # Check for NULLs
    null_counts = df[required_columns].isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            warnings.append(f"{count} NULL values in {col}")

    # Check amount is Decimal-compatible
    try:
        df[amount_column] = df[amount_column].apply(Decimal)
    except:
        errors.append(f"{amount_column} contains non-numeric values")

    # Check for negative amounts (may be valid in some contexts)
    negatives = (df[amount_column] < 0).sum()
    if negatives > 0:
        errors.append(f"{negatives} negative amounts found")

    passed = len(errors) == 0
    summary = f"{'✅ PASSED' if passed else '❌ FAILED'} - {len(errors)} errors, {len(warnings)} warnings"

    return ValidationResult(passed, errors, warnings, summary)
```

**Skills/Agents:**
- `data-validator` agent (prod) - Runs validation, generates report, waits for human approval
- `decimal-precision-enforcer` skill (shared) - Ensures amounts are Decimal-compatible

---

### 4. Template Customization

**Phase 1-5: Generic Templates**

```
templates/
├── variance_report.xlsx         # Generic variance report
├── board_deck.pptx              # Generic board presentation
└── consolidated_report.xlsx     # Generic consolidation output
```

**Phase 6: Life360 Branding**

User provides:
- Life360 logo (PNG, SVG)
- Brand colors (hex codes)
- Font specifications
- PowerPoint master template

**Implementation:**
```python
# scripts/utils/branding.py
BRAND_CONFIG = {
    "company_name": "Life360",
    "logo_path": "templates/assets/life360_logo.png",
    "primary_color": "#5200FF",  # Life360 purple
    "secondary_color": "#00D4AA",  # Life360 teal
    "font_family": "Montserrat",
}

def apply_branding_to_pptx(prs: Presentation) -> Presentation:
    """Apply Life360 branding to PowerPoint presentation."""
    # Add logo to title slide
    # Set color scheme
    # Apply fonts
    return prs
```

**Created During Phase 6:**
```
templates/
├── life360/
│   ├── variance_report.xlsx     # Branded variance report
│   ├── board_deck.pptx          # Branded board deck
│   ├── consolidated_report.xlsx # Branded consolidation
│   └── assets/
│       ├── life360_logo.png
│       └── brand_colors.json
└── generic/                      # Keep generic for reference
    ├── variance_report.xlsx
    └── board_deck.pptx
```

---

### 5. Error Recovery & State Management

**Workflow State Structure:**

```
config/
└── workflow-state/
    ├── monthly-close-2025-11.json       # State for Nov 2025 monthly close
    ├── variance-analysis-2025-11.json   # State for Nov 2025 variance
    └── .gitignore                        # Ignore state files
```

**State File Format:**
```json
{
  "workflow": "monthly-close",
  "period": "2025-11",
  "started_at": "2025-11-08T10:00:00Z",
  "last_updated": "2025-11-08T14:32:15Z",
  "status": "in_progress",
  "completed_steps": [
    "validate_input_data",
    "consolidate_departments",
    "calculate_variances"
  ],
  "current_step": "generate_board_deck",
  "remaining_steps": [
    "export_to_google_sheets",
    "send_notifications"
  ],
  "intermediate_outputs": {
    "consolidated_file": "/tmp/consolidated_nov2025.xlsx",
    "variance_file": "/tmp/variance_nov2025.xlsx"
  },
  "error": null
}
```

**Resumption Workflow:**

```python
# scripts/workflows/monthly_close.py
from pathlib import Path
import json

STATE_DIR = Path("config/workflow-state")

def save_state(workflow: str, period: str, state: dict) -> None:
    """Save workflow state for resumption."""
    state_file = STATE_DIR / f"{workflow}-{period}.json"
    state_file.write_text(json.dumps(state, indent=2))

def load_state(workflow: str, period: str) -> dict | None:
    """Load workflow state if exists."""
    state_file = STATE_DIR / f"{workflow}-{period}.json"
    if state_file.exists():
        return json.loads(state_file.read_text())
    return None

def monthly_close_workflow(period: str, resume: bool = False):
    """Run monthly close workflow with error recovery."""
    state = load_state("monthly-close", period) if resume else None

    if state:
        print(f"Resuming from step: {state['current_step']}")
        steps = state['remaining_steps']
    else:
        print("Starting new monthly close workflow")
        steps = ["validate", "consolidate", "variance", "board_deck", "export"]

    for step in steps:
        try:
            print(f"Executing step: {step}")
            execute_step(step)

            # Update state after each step
            save_state("monthly-close", period, {
                "current_step": step,
                "completed_steps": [...],
                "status": "in_progress"
            })
        except Exception as e:
            # Save error state
            save_state("monthly-close", period, {
                "current_step": step,
                "status": "failed",
                "error": str(e)
            })
            print(f"❌ Workflow failed at step {step}. State saved. Resume with: /prod:monthly-close --resume")
            raise

    # Mark complete
    save_state("monthly-close", period, {"status": "completed"})
```

**Command with Resume:**
```markdown
---
name: monthly-close
description: Monthly close workflow with error recovery
---

# Monthly Close Workflow

## Usage
`/prod:monthly-close november [--resume]`

## Arguments
- Period: Month name or YYYY-MM format
- --resume: Resume from last saved state (optional)

## Workflow
1. Check for existing state file
2. If --resume flag: Load state and continue from last step
3. If new: Start from beginning
4. Save state after each step
5. On error: Save error state, inform user how to resume
```

**Benefits:**
- Long workflows don't lose progress on transient failures
- User can review intermediate outputs before continuing
- Network/file issues are recoverable
- Better user experience for multi-hour workflows

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0-DRAFT | 2025-11-08 | Claude | Initial technical planning document |

---

## References

- **spec.md** - Business requirements (WHAT to build)
- **CLAUDE.md** - Behavioral configuration (HOW Claude operates)
- **README.md** - Project overview and quick start
- **.claude/** - Claude Code configuration (Skills, Commands, Agents, Hooks)

---

**END OF TECHNICAL PLANNING DOCUMENT**

*This document defines HOW to build what spec.md describes. Implementation should follow this plan while adapting to discoveries made during development.*
