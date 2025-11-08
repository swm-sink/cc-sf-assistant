# fpa-integrations

**Purpose:** External system adapters - abstract Google Workspace, Excel, and storage services.

## Responsibilities

- Google Sheets reader/writer
- Google Slides template population
- Excel file handlers with validation
- Cloud storage connectors

## Key Principle

**Adapters pattern.** Swap implementations without changing core business logic. All external I/O happens here.

## Dependencies

- **gspread** - Google Sheets Python API (6.1.2)
- **gspread-dataframe** - pandas DataFrame ↔ Sheets
- **openpyxl** - Read/write Excel files
- **xlsxwriter** - Excel formatting and charts
- **google-auth** - Google Workspace authentication

## External Libraries Leveraged

From `external/` directory:
- `gspread/` - Sheets integration patterns
- `slidio/` - Slides template engine
- `mcp-gdrive/` - MCP protocol reference

## Structure

```
src/fpa_integrations/
├── google_sheets/      # Google Sheets API wrapper
├── google_slides/      # Google Slides API wrapper
├── excel/              # Excel read/write with validation
└── storage/            # File storage abstractions
```

(Subdirectories will be created during implementation phase after spec approval)

## Usage Example (Future)

```python
from fpa_integrations.google_sheets import SheetsReader
from fpa_core.consolidation import consolidate_data

# Read data from Google Sheets
reader = SheetsReader(credentials_path="config/service-account.json")
df = reader.read_sheet("Monthly Reports", "November 2025")

# Process with core business logic
consolidated = consolidate_data(df)

# Write results back
reader.write_sheet("Consolidated Report", consolidated)
```
