# Google Workspace Integration Specification

**Systems:** Google Sheets, Google Slides, Google Drive
**Purpose:** Export variance reports and board decks to Google Workspace
**API Type:** Google Workspace APIs (Sheets, Slides, Drive)
**Authentication:** Service Account or OAuth 2.0

---

## Business Context

**Workflow Position:** Final reporting step after variance analysis

```
[ADAPTIVE + DATABRICKS] Extract data
↓
[LOCAL] Variance analysis
↓
[LOCAL] Stakeholder review & adjustments
↓
[ADAPTIVE] Upload finalized data
↓
[GOOGLE SHEETS] Variance report
[GOOGLE SLIDES] Board deck
```

**Key Requirement:** Automated report generation with Life360 branding

---

## API Capabilities Overview

### Google Sheets API

**Purpose:** Export variance reports to Google Sheets for sharing

**Capabilities:**
- Create new spreadsheets
- Write data to ranges (batch updates)
- Apply formatting (colors, fonts, borders)
- Add charts and pivot tables
- Share with specific users

### Google Slides API

**Purpose:** Generate board decks from templates

**Capabilities:**
- Copy presentation templates
- Replace text placeholders
- Update chart data
- Insert images
- Export as PDF

### Google Drive API

**Purpose:** File management and sharing

**Capabilities:**
- Upload files
- Set permissions
- Create folders
- Move files to folders
- Get shareable links

---

## Authentication Strategy

### Option A: Service Account (Recommended for Automation)

**Setup:**
1. Google Cloud Console → Create Service Account
2. Enable Sheets API, Slides API, Drive API
3. Download JSON key file
4. Store in `config/credentials/google-service-account.json`
5. Share Google Drive folders with service account email

**Service Account JSON Format:**
```json
{
  "type": "service_account",
  "project_id": "life360-fpa-automation",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "fpa-automation@life360-fpa.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

**Usage in Scripts:**
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive'
]

def get_google_credentials():
    """Load service account credentials."""
    creds_path = Path("config/credentials/google-service-account.json")
    return service_account.Credentials.from_service_account_file(
        str(creds_path),
        scopes=SCOPES
    )

def get_sheets_client():
    """Get Google Sheets API client."""
    creds = get_google_credentials()
    return build('sheets', 'v4', credentials=creds)

def get_slides_client():
    """Get Google Slides API client."""
    creds = get_google_credentials()
    return build('slides', 'v1', credentials=creds)

def get_drive_client():
    """Get Google Drive API client."""
    creds = get_google_credentials()
    return build('drive', 'v3', credentials=creds)
```

### Option B: OAuth 2.0 (User-Based Access)

**Use Case:** When accessing user's personal Drive

**Implementation:** Defer to Phase 5+

---

## Google Sheets Integration

### Create Variance Report Spreadsheet

```python
from decimal import Decimal
from typing import List, Dict

def create_variance_report_sheet(
    variances: List[Dict],
    month: str,
    year: int
) -> str:
    """Create variance report in Google Sheets.

    Args:
        variances: List of variance results
        month: Month name
        year: Year

    Returns: Spreadsheet URL
    """
    sheets = get_sheets_client()

    # Create spreadsheet
    spreadsheet = {
        'properties': {
            'title': f'Variance Report - {month} {year}'
        },
        'sheets': [{
            'properties': {
                'title': 'Variance Analysis',
                'gridProperties': {
                    'rowCount': len(variances) + 10,
                    'columnCount': 10
                }
            }
        }]
    }

    result = sheets.spreadsheets().create(body=spreadsheet).execute()
    spreadsheet_id = result['spreadsheetId']

    # Write data
    write_variance_data_to_sheet(spreadsheet_id, variances)

    # Apply formatting
    format_variance_sheet(spreadsheet_id)

    # Share with team
    share_spreadsheet(spreadsheet_id, ['finance-team@life360.com'])

    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"


def write_variance_data_to_sheet(
    spreadsheet_id: str,
    variances: List[Dict]
):
    """Write variance data to Google Sheet."""
    sheets = get_sheets_client()

    # Prepare header
    header = [
        'Account ID',
        'Account Name',
        'Department',
        'Budget',
        'Actual',
        'Variance',
        'Variance %',
        'Favorable?',
        'Material?'
    ]

    # Prepare data rows
    rows = [header]
    for var in variances:
        rows.append([
            var['account_id'],
            var['account_name'],
            var['department'],
            float(var['budget']),  # Convert Decimal to float for Sheets
            float(var['actual']),
            float(var['variance']),
            float(var['variance_percentage']),
            var['is_favorable'],
            var['is_material']
        ])

    # Batch update
    body = {
        'values': rows
    }
    sheets.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Variance Analysis!A1',
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()


def format_variance_sheet(spreadsheet_id: str):
    """Apply formatting to variance report."""
    sheets = get_sheets_client()

    requests = [
        # Header row: Bold, background color
        {
            'repeatCell': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                        'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
                        'horizontalAlignment': 'CENTER'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
            }
        },
        # Freeze header row
        {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': 0,
                    'gridProperties': {'frozenRowCount': 1}
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        },
        # Currency format for Budget, Actual, Variance columns
        {
            'repeatCell': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': 1,
                    'startColumnIndex': 3,  # Budget column
                    'endColumnIndex': 6     # Through Variance column
                },
                'cell': {
                    'userEnteredFormat': {
                        'numberFormat': {
                            'type': 'CURRENCY',
                            'pattern': '$#,##0.00'
                        }
                    }
                },
                'fields': 'userEnteredFormat.numberFormat'
            }
        },
        # Percentage format for Variance % column
        {
            'repeatCell': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': 1,
                    'startColumnIndex': 6,  # Variance % column
                    'endColumnIndex': 7
                },
                'cell': {
                    'userEnteredFormat': {
                        'numberFormat': {
                            'type': 'PERCENT',
                            'pattern': '0.00%'
                        }
                    }
                },
                'fields': 'userEnteredFormat.numberFormat'
            }
        },
        # Auto-resize columns
        {
            'autoResizeDimensions': {
                'dimensions': {
                    'sheetId': 0,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': 9
                }
            }
        }
    ]

    body = {'requests': requests}
    sheets.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()
```

### Conditional Formatting (Highlight Unfavorable Variances)

```python
def add_conditional_formatting(spreadsheet_id: str, num_rows: int):
    """Highlight unfavorable variances in red."""
    sheets = get_sheets_client()

    requests = [
        {
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': 0,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows + 1,
                        'startColumnIndex': 7,  # Favorable? column
                        'endColumnIndex': 8
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': 'False'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 1, 'green': 0.8, 'blue': 0.8}
                        }
                    }
                },
                'index': 0
            }
        }
    ]

    body = {'requests': requests}
    sheets.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()
```

---

## Google Slides Integration

### Generate Board Deck from Template

```python
def generate_board_deck(
    variances: List[Dict],
    month: str,
    year: int,
    template_id: str
) -> str:
    """Generate board deck from Google Slides template.

    Args:
        variances: Variance analysis results
        month: Month name
        year: Year
        template_id: Google Slides template ID

    Returns: Presentation URL
    """
    slides = get_slides_client()
    drive = get_drive_client()

    # Copy template
    copy_title = f'Board Deck - {month} {year}'
    body = {'name': copy_title}
    deck = drive.files().copy(fileId=template_id, body=body).execute()
    presentation_id = deck['id']

    # Replace placeholders
    replace_text_placeholders(presentation_id, month, year)

    # Update variance summary slide
    update_variance_summary_slide(presentation_id, variances)

    # Update charts
    update_variance_charts(presentation_id, variances)

    return f"https://docs.google.com/presentation/d/{presentation_id}"


def replace_text_placeholders(presentation_id: str, month: str, year: int):
    """Replace text placeholders in slides."""
    slides = get_slides_client()

    requests = [
        {
            'replaceAllText': {
                'containsText': {'text': '{{MONTH}}'},
                'replaceText': month
            }
        },
        {
            'replaceAllText': {
                'containsText': {'text': '{{YEAR}}'},
                'replaceText': str(year)
            }
        },
        {
            'replaceAllText': {
                'containsText': {'text': '{{GENERATED_DATE}}'},
                'replaceText': datetime.now().strftime('%B %d, %Y')
            }
        }
    ]

    body = {'requests': requests}
    slides.presentations().batchUpdate(
        presentationId=presentation_id,
        body=body
    ).execute()


def update_variance_summary_slide(
    presentation_id: str,
    variances: List[Dict]
):
    """Update variance summary slide with top variances."""
    slides = get_slides_client()

    # Get top 5 material variances
    material_variances = [v for v in variances if v['is_material']]
    top_variances = sorted(
        material_variances,
        key=lambda v: abs(v['variance']),
        reverse=True
    )[:5]

    # Build summary text
    summary_lines = []
    for var in top_variances:
        favorable = "✓" if var['is_favorable'] else "⚠"
        summary_lines.append(
            f"{favorable} {var['account_name']}: "
            f"${var['variance']:,.0f} ({var['variance_percentage']:.1f}%)"
        )

    summary_text = '\n'.join(summary_lines)

    # Replace {{VARIANCE_SUMMARY}} placeholder
    requests = [{
        'replaceAllText': {
            'containsText': {'text': '{{VARIANCE_SUMMARY}}'},
            'replaceText': summary_text
        }
    }]

    body = {'requests': requests}
    slides.presentations().batchUpdate(
        presentationId=presentation_id,
        body=body
    ).execute()
```

---

## Google Drive Integration

### Share Files and Get Links

```python
def share_spreadsheet(spreadsheet_id: str, emails: List[str]):
    """Share spreadsheet with specific users."""
    drive = get_drive_client()

    for email in emails:
        permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': email
        }
        drive.permissions().create(
            fileId=spreadsheet_id,
            body=permission,
            sendNotificationEmail=False
        ).execute()


def get_shareable_link(file_id: str) -> str:
    """Get shareable link for file."""
    drive = get_drive_client()

    # Make file accessible to anyone with link
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    drive.permissions().create(
        fileId=file_id,
        body=permission
    ).execute()

    return f"https://drive.google.com/file/d/{file_id}"


def move_to_folder(file_id: str, folder_id: str):
    """Move file to specific Drive folder."""
    drive = get_drive_client()

    # Get current parents
    file_metadata = drive.files().get(
        fileId=file_id,
        fields='parents'
    ).execute()
    previous_parents = ','.join(file_metadata.get('parents', []))

    # Move to new folder
    drive.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()
```

---

## Workflow Integration

### Complete Post-Close Reporting Workflow

```python
# scripts/workflows/post_close_reporting.py

def generate_all_reports(
    variances: List[Dict],
    month: str,
    year: int
) -> Dict[str, str]:
    """Generate all Google Workspace reports.

    Returns: {report_type: url}
    """
    reports = {}

    # 1. Create variance report in Google Sheets
    print("Creating variance report in Google Sheets...")
    sheets_url = create_variance_report_sheet(variances, month, year)
    reports['variance_sheet'] = sheets_url
    print(f"✓ Variance report: {sheets_url}")

    # 2. Generate board deck in Google Slides
    print("Generating board deck in Google Slides...")
    template_id = load_slides_template_id()  # From config
    slides_url = generate_board_deck(variances, month, year, template_id)
    reports['board_deck'] = slides_url
    print(f"✓ Board deck: {slides_url}")

    # 3. Move to shared folder
    print("Organizing files in Drive...")
    folder_id = load_reports_folder_id()  # From config
    sheets_id = sheets_url.split('/')[-1]
    slides_id = slides_url.split('/')[-1]
    move_to_folder(sheets_id, folder_id)
    move_to_folder(slides_id, folder_id)
    print("✓ Files organized")

    # 4. Share with finance team
    print("Sharing with finance team...")
    team_emails = ['cfo@life360.com', 'finance-team@life360.com']
    share_spreadsheet(sheets_id, team_emails)
    share_spreadsheet(slides_id, team_emails)
    print("✓ Shared with team")

    # 5. Log to audit trail
    log_audit_event(
        operation="google_reports_generated",
        inputs={"month": month, "year": year, "variance_count": len(variances)},
        outputs={"sheets_url": sheets_url, "slides_url": slides_url}
    )

    return reports
```

---

## Data Type Conversion

**Important:** Google Sheets API doesn't support Python Decimal

```python
def decimal_to_float_for_sheets(data: Dict) -> Dict:
    """Convert Decimal values to float for Google Sheets.

    Recursively converts Decimal in nested structures.
    """
    if isinstance(data, dict):
        return {k: decimal_to_float_for_sheets(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [decimal_to_float_for_sheets(item) for item in data]
    elif isinstance(data, Decimal):
        return float(data)
    else:
        return data
```

**Usage:**
```python
# WRONG - Will fail
variance_data = {'budget': Decimal('100000.00')}
sheets.spreadsheets().values().update(..., body={'values': [variance_data]})

# CORRECT - Convert Decimal to float
variance_data = {'budget': Decimal('100000.00')}
sheets_data = decimal_to_float_for_sheets(variance_data)
sheets.spreadsheets().values().update(..., body={'values': [sheets_data]})
```

---

## Error Handling

### Common Error Codes

| Code | Message | Resolution |
|------|---------|------------|
| 401 | Invalid credentials | Check service account JSON file |
| 403 | Permission denied | Share template with service account email |
| 404 | File not found | Verify template ID, check sharing permissions |
| 429 | Rate limit exceeded | Implement exponential backoff |
| 500 | Backend error | Retry after delay |

### Retry Logic

```python
from time import sleep
import random

def google_api_call_with_retry(func, max_retries=3):
    """Retry Google API calls with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                wait_time = (2 ** attempt) + random.random()
                print(f"Rate limited. Retrying in {wait_time:.1f}s...")
                sleep(wait_time)
            elif "500" in str(e) or "503" in str(e):
                wait_time = 5 * (attempt + 1)
                print(f"Server error. Retrying in {wait_time}s...")
                sleep(wait_time)
            else:
                raise
    raise Exception(f"Max retries exceeded")
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_google_client.py

def test_decimal_to_float_conversion():
    """Verify Decimal→float conversion for Sheets."""
    data = {
        'budget': Decimal('100000.00'),
        'actual': Decimal('115000.50'),
        'nested': {'variance': Decimal('-15000.50')}
    }

    result = decimal_to_float_for_sheets(data)

    assert isinstance(result['budget'], float)
    assert result['budget'] == 100000.00
    assert isinstance(result['nested']['variance'], float)


@pytest.mark.integration
def test_create_variance_sheet():
    """Test actual Google Sheets creation (requires credentials)."""
    if not Path("config/credentials/google-service-account.json").exists():
        pytest.skip("Google credentials not configured")

    variances = [
        {
            'account_id': '4000',
            'account_name': 'Revenue',
            'budget': Decimal('100000'),
            'actual': Decimal('115000'),
            'variance': Decimal('15000'),
            'variance_percentage': Decimal('15'),
            'is_favorable': True,
            'is_material': True
        }
    ]

    url = create_variance_report_sheet(variances, "November", 2025)
    assert "docs.google.com/spreadsheets" in url
```

---

## Configuration

**settings.yaml:**
```yaml
google:
  service_account_file: "config/credentials/google-service-account.json"
  scopes:
    - "https://www.googleapis.com/auth/spreadsheets"
    - "https://www.googleapis.com/auth/presentations"
    - "https://www.googleapis.com/auth/drive"

  templates:
    board_deck_id: "1ABC...XYZ"  # Google Slides template
    variance_report_id: "1DEF...UVW"  # Google Sheets template (optional)

  folders:
    reports_folder_id: "1GHI...RST"  # Drive folder for reports

  sharing:
    finance_team:
      - "cfo@life360.com"
      - "finance-team@life360.com"
```

---

## Credential Setup Guide

**Step-by-Step for QUICK_START.md:**

1. **Create Google Cloud Project:**
   - Go to https://console.cloud.google.com
   - Create new project: "life360-fpa-automation"

2. **Enable APIs:**
   - Enable Google Sheets API
   - Enable Google Slides API
   - Enable Google Drive API

3. **Create Service Account:**
   - IAM & Admin → Service Accounts → Create Service Account
   - Name: "fpa-automation"
   - Grant role: "Editor" (or custom role with Sheets/Slides/Drive permissions)

4. **Download JSON Key:**
   - Service Account → Keys → Add Key → JSON
   - Download file
   - Save to `config/credentials/google-service-account.json`

5. **Share Templates and Folders:**
   - Open Google Slides template
   - Share with service account email: `fpa-automation@life360-fpa.iam.gserviceaccount.com`
   - Set permission: "Editor"
   - Repeat for Drive folders

6. **Verify Setup:**
   ```bash
   poetry run python scripts/integrations/test_google_auth.py
   ```

---

## Implementation Checklist

- [ ] Create `scripts/integrations/gsheet_writer.py`
- [ ] Create `scripts/integrations/gslides_generator.py`
- [ ] Create `scripts/integrations/gdrive_client.py`
- [ ] Implement service account authentication
- [ ] Implement variance report generation (Sheets)
- [ ] Implement board deck generation (Slides)
- [ ] Implement file sharing and permissions
- [ ] Add Decimal→float conversion helper
- [ ] Add retry logic for API calls
- [ ] Create tests (unit + integration)
- [ ] Create credential setup guide in QUICK_START.md
- [ ] Create Google Slides template with placeholders
- [ ] Test end-to-end workflow

---

**References:**
- Google Sheets API v4 Documentation
- Google Slides API v1 Documentation
- Google Drive API v3 Documentation
- gspread library (alternative client library)
- slidio patterns (community examples)

**Last Updated:** 2025-11-08
