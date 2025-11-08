# fpa-cli

**Purpose:** Command-line interface for non-technical FP&A users.

## Responsibilities

- Simple commands: `fpa consolidate`, `fpa variance`, `fpa report`
- Interactive prompts for file paths, date ranges
- Progress indicators, human-friendly error messages
- Hide complexity, expose value

## Key Principle

**Non-technical users should never see code or error stack traces.** All interactions are friendly and guided.

## Dependencies

- **click** - User-friendly CLI framework
- **rich** - Beautiful terminal output
- **tqdm** - Progress bars
- **python-dotenv** - Configuration management

## Usage Examples (Future)

```bash
# Consolidate department data
fpa consolidate --input data/departments/ --output reports/consolidated.xlsx

# Generate variance analysis
fpa variance --budget budget_2025.xlsx --actual actuals_nov.xlsx

# Create management report
fpa report --template templates/monthly.pptx --data reports/consolidated.xlsx
```

## Interactive Mode

```bash
$ fpa variance

📊 Variance Analysis Assistant

Budget file path: budget_2025.xlsx
Actual file path: actuals_nov.xlsx
Output path (optional): variance_report.xlsx

✓ Reading budget data... (50 accounts found)
✓ Reading actual data... (50 accounts matched)
✓ Calculating variances...
✓ Applying favorability logic...

⚠️  Found 3 material variances (>10%):
  - Revenue: +$15,000 (15%) FAVORABLE
  - Marketing: +$8,000 (20%) UNFAVORABLE
  - IT Costs: -$5,000 (10%) FAVORABLE

✓ Report saved: variance_report.xlsx

Would you like to send this to Google Sheets? (y/n):
```

## Structure

```
src/fpa_cli/
├── commands/           # CLI commands (consolidate, variance, report)
├── prompts/            # Interactive user prompts
└── formatters/         # Output formatting (tables, charts)
```

(Subdirectories will be created during implementation phase after spec approval)

## Installation (Future)

```bash
# Install from monorepo root
poetry install

# Run command
fpa --help
```
