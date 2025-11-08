# External Dependencies - Cloned GitHub Repos

## Summary

We've cloned 6 high-quality open-source repos to leverage for our FP&A Automation Assistant. These provide proven solutions for Google integrations, human-in-the-loop workflows, and financial precision.

## Cloned Repositories

### 1. **humanlayer/** - AI Coding Agent Framework
- **GitHub:** https://github.com/humanlayer/humanlayer
- **Stars:** 6,686+ ⭐
- **License:** Apache-2.0
- **Language:** TypeScript, Python
- **Last Updated:** Nov 7, 2025

**What It Is:**
CodeLayer - Open source IDE for orchestrating AI coding agents with battle-tested workflows for complex codebases. Built on Claude Code.

**What We'll Use:**
- Human-in-the-loop approval workflows
- Multi-agent orchestration patterns
- Context engineering techniques for scaling Claude Code
- Keyboard-first workflow patterns

**Key Features:**
- Superhuman-style keyboard shortcuts
- Parallel Claude Code session management
- Advanced context engineering for team collaboration
- Battle-tested workflows for large codebases

**Why We Need It:**
Our FP&A workflows require human approval gates (e.g., "Review variance report before sending to management"). HumanLayer provides proven patterns for these checkpoints.

---

### 2. **mcp-gdrive/** - Google Drive MCP Server
- **GitHub:** https://github.com/isaacphi/mcp-gdrive
- **License:** MIT
- **Language:** TypeScript
- **Protocol:** Model Context Protocol (Anthropic standard)

**What It Is:**
MCP server for reading from Google Drive and editing Google Sheets using Anthropic's standardized protocol.

**What We'll Use:**
- Standard protocol for Google Sheets integration
- Google Drive file listing and searching
- Sheet reading and writing via MCP

**Key Features:**
- Lists, reads, searches Google Drive files
- Reads and writes Google Sheets
- Built on Anthropic's MCP standard (backed by GitHub, Microsoft, Google)
- Type-safe TypeScript implementation

**Why We Need It:**
MCP is the emerging standard for AI-to-data integrations. Using this ensures future compatibility with Claude and other AI tools.

---

### 3. **gspread/** - Google Sheets Python API
- **GitHub:** https://github.com/burnash/gspread
- **PyPI:** gspread 6.1.2
- **License:** MIT
- **Language:** Python
- **Python:** 3.8+

**What It Is:**
Most popular Python library for Google Sheets (simple interface, mature codebase).

**What We'll Use:**
- Open spreadsheets by title, key, or URL
- Read, write, format cell ranges
- Sharing and access control
- Batch updates for performance

**Basic Usage:**
```python
import gspread

gc = gspread.service_account()  # Auth with service account
sh = gc.open("November Financial Report")  # Open by title
worksheet = sh.sheet1

# Get a list of all records
list_of_hashes = worksheet.get_all_records()

# Update a range of cells
worksheet.update([[1, 2], [3, 4]])
```

**Note:** Maintainers seeking new help (as of search date). Code is stable but may need vetting for production use.

**Why We Need It:**
Well-tested, widely used Python library for Sheets. Simpler than raw Google API calls.

---

### 4. **slidio/** - Google Slides Template Engine
- **GitHub:** https://github.com/mickaelandrieu/slidio
- **Language:** Python
- **License:** Not specified in README

**What It Is:**
Python library to dynamically generate Google Slides from templates using text, charts, and tables.

**What We'll Use:**
- Replace text in placeholder text boxes
- Insert matplotlib figures (charts)
- Insert tables with data
- Alt-text-based placeholders for flexibility
- Create new presentations from templates

**Key Features:**
```python
# Create from template
from slidio import Presentation
pres = Presentation.from_template("template_id")

# Replace placeholders
pres.replace_text("{{variance_summary}}", "Revenue up 15%")

# Insert chart
pres.insert_figure("chart_placeholder", matplotlib_figure)

# Save
pres.save()
```

**Why We Need It:**
Automates board deck generation. Template-based approach ensures brand consistency while automating data updates.

---

### 5. **pyfpa/** - FP&A Functions in Python
- **GitHub:** https://github.com/warrenpilot/pyfpa
- **PyPI:** pyfpa
- **Language:** Python
- **Status:** Beta version

**What It Is:**
Essential Financial Planning & Analysis functions in Python. Designed specifically for corporate FP&A analysts moving from Excel to Python.

**What We'll Use:**
- Multidimensional dataframe patterns for FP&A data
- Excel data collection and consolidation patterns
- Variance analysis algorithms
- Dimension management (account hierarchy, time periods, departments)
- Record-to-table transformations for pivot tables

**Key Capabilities:**
- Collect data from Excel files → high-dimensional data cube
- Combine periodic reports to search for trends
- Track snapshots over time
- Map custom budget/actual reports
- Golden Source repository patterns
- Source and version control tracking
- Easy slicing/dicing by dimensions
- Consolidation based on dimensions
- Variance analysis
- Excel export

**Why We Need It:**
Domain-specific patterns for FP&A. Avoids reinventing consolidation and variance algorithms. Written by FP&A professionals.

---

### 6. **py-money/** - Decimal Precision Money Handling
- **GitHub:** https://github.com/vimeo/py-money
- **Maintainer:** Vimeo (production-grade)
- **Language:** Python
- **License:** Not specified

**What It Is:**
Money class for Python 3 with enforced decimal precision. Prevents floating-point rounding errors in financial calculations.

**What We'll Use:**
- Decimal-based money representation
- Correct number of decimal places per currency
- Locale-aware formatting
- Automatic rounding after operations
- Immutable money objects

**Key Features:**
```python
from money import Money
from money.currency import USD

# Create money object
revenue = Money('1500.50', USD)
cost = Money('800.25', USD)

# Operations maintain precision
profit = revenue - cost  # Money('700.25', USD)

# No floating-point errors
# 0.1 + 0.2 = 0.30000000000000004 ❌
# Money('0.1') + Money('0.2') = Money('0.30') ✅

# Format for display
print(profit.format('en_US'))  # $700.25
```

**Why We Need It:**
Financial calculations require exact decimal math. Floats cause rounding errors that break trust and compliance. This enforces correctness.

---

## Integration Strategy

### How External Repos Fit Into Our Monorepo

```
cc-sf-assistant/
├── external/                    # Cloned repos (read-only reference)
│   ├── humanlayer/             # Patterns and architecture reference
│   ├── mcp-gdrive/             # MCP protocol implementation
│   ├── gspread/                # Direct dependency
│   ├── slidio/                 # Direct dependency
│   ├── pyfpa/                  # Direct dependency
│   └── py-money/               # Direct dependency
│
└── packages/                    # Our custom code
    ├── fpa-core/               # Uses: py-money, pyfpa patterns
    ├── fpa-integrations/       # Uses: gspread, slidio, mcp-gdrive
    ├── fpa-workflows/          # Uses: humanlayer patterns
    └── fpa-cli/                # Orchestrates all packages
```

### Dependency Model

**Option 1: Direct Path Dependencies (Current)**
```toml
# packages/fpa-integrations/pyproject.toml
[tool.poetry.dependencies]
gspread = { path = "../../external/gspread", develop = true }
slidio = { path = "../../external/slidio", develop = true }
```

**Option 2: Install from PyPI (Simpler)**
```toml
[tool.poetry.dependencies]
gspread = "^6.1.2"  # Install from PyPI
```

**Recommendation:** Start with PyPI installs (simpler). Clone repos for:
1. Reference implementation patterns
2. Reading source code for deep understanding
3. Future customization if needed
4. Audit security before production use

---

## Next Steps

1. **Review External Code**
   - Read source to understand patterns
   - Check licenses for compatibility
   - Verify security (no malware, no credential leaks)

2. **Set Up Package Dependencies**
   - Create pyproject.toml for each package in `packages/`
   - Install external deps via PyPI or path references
   - Set up Poetry workspace at root

3. **Extract Patterns**
   - Study humanlayer workflow patterns
   - Adopt pyfpa consolidation algorithms
   - Learn gspread best practices

4. **Build Abstractions**
   - Wrap external libs in our interfaces
   - Add FP&A-specific logic on top
   - Ensure clean separation (easy to swap implementations)

---

## License Compatibility

| Repo | License | Commercial Use? | Attribution Required? |
|------|---------|-----------------|----------------------|
| humanlayer | Apache-2.0 | ✅ Yes | ✅ Yes (include license) |
| mcp-gdrive | MIT | ✅ Yes | ✅ Yes (include license) |
| gspread | MIT | ✅ Yes | ✅ Yes (include license) |
| slidio | Unknown | ⚠️ Check | ⚠️ Check |
| pyfpa | Unknown | ⚠️ Check | ⚠️ Check |
| py-money | Unknown | ⚠️ Check | ⚠️ Check |

**Action Required:** Check licenses for slidio, pyfpa, py-money before production use.

---

## Alternatives Considered

If any external repo becomes unmaintained or unsuitable:

| Category | Primary Choice | Alternative |
|----------|---------------|-------------|
| Google Sheets | gspread | google-api-python-client (official but complex) |
| Google Slides | slidio | python-pptx (for PowerPoint) + manual Slides API |
| Money handling | py-money | stockholm, dinero, PreciseMoney |
| FP&A patterns | pyfpa | Build from scratch (slower but full control) |
| Human-in-loop | humanlayer patterns | Build custom approval system |
| MCP Server | mcp-gdrive | Use gspread directly (simpler) |

---

## Maintenance Notes

- **Last Cloned:** 2025-11-08
- **Git Status:** External repos are full Git clones (can pull updates)
- **Update Strategy:** Periodically `git pull` in each repo to get latest
- **Freeze Strategy:** Pin commit SHAs in production for stability

---

**END OF EXTERNAL DEPENDENCIES DOCUMENTATION**
