# Adaptive Insights API Integration Specification

**System:** Workday Adaptive Planning (formerly Adaptive Insights)
**Purpose:** POST-CLOSE data export/import for variance analysis and budget finalization
**API Type:** REST API with XML-based data format
**Authentication:** API Token or OAuth 2.0

---

## Business Context

**Workflow Position:** POST-CLOSE (after month-end close)

```
Month-End Close (Separate System)
↓
[ADAPTIVE] Export actuals & budget
↓
[LOCAL] Variance analysis, stakeholder review
↓
[LOCAL] Adjustments and corrections
↓
[ADAPTIVE] Upload finalized data
↓
[GOOGLE] Generate reports (Slides, Sheets)
```

**Key Requirement:** Bidirectional data sync (export from Adaptive, import back after review)

---

## API Capabilities Research Summary

**Source 1:** Workiva Adaptive Insights Integration (2025)
- REST API with JSON/XML support
- Version-based data exports
- Budget vs Actual comparisons
- Custom dimensions (departments, regions, products)

**Source 2:** Tray.ai Adaptive Planning Connector
- Supports: Accounts, Actuals, Assumptions, Budgets, Versions
- Authentication: API token (recommended) or OAuth
- Rate limits: 100 requests/minute
- Batch operations supported

**Source 3:** Workato Adaptive Planning API
- Export formats: CSV, Excel, XML
- Import validation: Pre-checks before data upload
- Error handling: Detailed error codes for validation failures
- Audit trail: All API operations logged

---

## Authentication Strategy

### Option A: API Token (Recommended for Single-User)

**Setup:**
1. Adaptive admin generates API token
2. Store in `config/credentials/adaptive-token.json`
3. Git-ignore credentials (already configured)

**Token Format:**
```json
{
  "api_token": "your-adaptive-api-token",
  "instance_url": "https://your-company.adaptiveinsights.com",
  "api_version": "v1"
}
```

**Usage in Scripts:**
```python
from pathlib import Path
import json

def load_adaptive_credentials():
    cred_path = Path("config/credentials/adaptive-token.json")
    if not cred_path.exists():
        raise FileNotFoundError("Adaptive credentials not found")
    with open(cred_path) as f:
        return json.load(f)

creds = load_adaptive_credentials()
headers = {
    "Authorization": f"Bearer {creds['api_token']}",
    "Content-Type": "application/xml"
}
```

### Option B: OAuth 2.0 (Future Enhancement)

Defer to Phase 6+ if multi-user access needed.

---

## Data Export Operations

### Export Actuals (Monthly)

**Endpoint:** `GET /api/v1/actuals`

**Parameters:**
- `version`: Version name (e.g., "November 2025 Actuals")
- `start_date`: First day of month (e.g., "2025-11-01")
- `end_date`: Last day of month (e.g., "2025-11-30")
- `accounts`: Account list or "all"
- `dimensions`: ["Department", "Region", "Product"] (if needed)

**Response Format (XML):**
```xml
<ActualsExport version="November 2025 Actuals">
  <Account id="4000" name="Subscription Revenue">
    <Department name="Enterprise">
      <Amount>2875000.00</Amount>
      <Currency>USD</Currency>
    </Department>
  </Account>
  <Account id="6000" name="Engineering Salaries">
    <Department name="Engineering">
      <Amount>920000.00</Amount>
      <Currency>USD</Currency>
    </Department>
  </Account>
</ActualsExport>
```

**Python Implementation:**
```python
import requests
from decimal import Decimal
from xml.etree import ElementTree as ET

def export_actuals(version: str, start_date: str, end_date: str) -> dict:
    """Export actuals from Adaptive Insights.

    Returns: {account_id: {dept: Decimal(amount)}}
    """
    creds = load_adaptive_credentials()
    url = f"{creds['instance_url']}/api/v1/actuals"
    headers = {"Authorization": f"Bearer {creds['api_token']}"}

    params = {
        "version": version,
        "start_date": start_date,
        "end_date": end_date,
        "accounts": "all"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    # Parse XML
    root = ET.fromstring(response.content)
    actuals = {}

    for account in root.findall("Account"):
        account_id = account.get("id")
        account_name = account.get("name")
        actuals[account_id] = {"name": account_name, "departments": {}}

        for dept in account.findall("Department"):
            dept_name = dept.get("name")
            amount = Decimal(dept.find("Amount").text)
            actuals[account_id]["departments"][dept_name] = amount

    return actuals
```

### Export Budget

**Endpoint:** `GET /api/v1/budgets`

**Parameters:**
- `version`: Budget version (e.g., "FY 2025 Budget")
- `period`: Monthly, Quarterly, Annual
- `accounts`: Account list or "all"

**Response Format:** Same XML structure as actuals

---

## Data Import Operations

### Upload Adjusted Actuals

**Endpoint:** `POST /api/v1/actuals/import`

**Use Case:** After stakeholder review and adjustments, upload finalized data

**Request Format (XML):**
```xml
<ActualsImport version="November 2025 Actuals - Finalized">
  <Account id="7030" name="Digital Advertising">
    <Department name="Marketing">
      <Amount>420000.00</Amount>
      <Currency>USD</Currency>
      <Comment>Adjusted for Q4 campaign spend</Comment>
    </Department>
  </Account>
</ActualsImport>
```

**Validation Response:**
```xml
<ImportValidation>
  <Status>Success</Status>
  <RecordsProcessed>50</RecordsProcessed>
  <RecordsImported>48</RecordsImported>
  <Errors>
    <Error account="8999" message="Account not found in chart of accounts"/>
  </Errors>
</ImportValidation>
```

**Python Implementation:**
```python
def import_adjusted_actuals(actuals: dict, version: str) -> dict:
    """Upload adjusted actuals to Adaptive.

    Args:
        actuals: {account_id: {dept: Decimal(amount)}}
        version: Version name for import

    Returns: Validation results
    """
    creds = load_adaptive_credentials()
    url = f"{creds['instance_url']}/api/v1/actuals/import"
    headers = {
        "Authorization": f"Bearer {creds['api_token']}",
        "Content-Type": "application/xml"
    }

    # Build XML payload
    root = ET.Element("ActualsImport", version=version)
    for account_id, data in actuals.items():
        account_elem = ET.SubElement(root, "Account",
                                      id=account_id,
                                      name=data["name"])
        for dept, amount in data["departments"].items():
            dept_elem = ET.SubElement(account_elem, "Department", name=dept)
            amount_elem = ET.SubElement(dept_elem, "Amount")
            amount_elem.text = str(amount)
            currency_elem = ET.SubElement(dept_elem, "Currency")
            currency_elem.text = "USD"

    xml_payload = ET.tostring(root, encoding="unicode")

    response = requests.post(url, headers=headers, data=xml_payload)
    response.raise_for_status()

    # Parse validation response
    validation = ET.fromstring(response.content)
    return {
        "status": validation.find("Status").text,
        "records_processed": int(validation.find("RecordsProcessed").text),
        "records_imported": int(validation.find("RecordsImported").text),
        "errors": [
            {"account": err.get("account"), "message": err.get("message")}
            for err in validation.findall("Errors/Error")
        ]
    }
```

---

## Post-Close Workflow Integration

### Step 1: Export from Adaptive

```python
# scripts/workflows/post_close_review.py

def step1_export_adaptive_data(month: str, year: int):
    """Export actuals and budget from Adaptive."""
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]:02d}"

    # Export actuals
    actuals = export_actuals(
        version=f"{calendar.month_name[month]} {year} Actuals",
        start_date=start_date,
        end_date=end_date
    )

    # Export budget
    budget = export_budget(
        version=f"FY {year} Budget",
        period="monthly",
        month=month
    )

    # Save locally for analysis
    Path("data/adaptive-exports").mkdir(exist_ok=True)
    with open(f"data/adaptive-exports/actuals_{month}_{year}.json", "w") as f:
        json.dump(actuals, f, default=str)  # Decimal serialization

    with open(f"data/adaptive-exports/budget_{month}_{year}.json", "w") as f:
        json.dump(budget, f, default=str)

    return actuals, budget
```

### Step 2: Local Variance Analysis

```python
def step2_variance_analysis(actuals, budget):
    """Calculate variances locally."""
    from scripts.core.variance import calculate_variance

    variances = {}
    for account_id in actuals.keys():
        for dept in actuals[account_id]["departments"].keys():
            actual = actuals[account_id]["departments"][dept]
            budget_amt = budget[account_id]["departments"][dept]

            variance_result = calculate_variance(actual, budget_amt, account_type)
            variances[(account_id, dept)] = variance_result

    return variances
```

### Step 3: Stakeholder Review (Human Checkpoint)

```python
def step3_stakeholder_review(variances):
    """Present variances to user for review."""
    # Generate variance report
    report_path = generate_variance_report(variances)

    # Human checkpoint
    print(f"Variance report: {report_path}")
    print("Review material variances:")
    for (account, dept), var in variances.items():
        if var.is_material:
            print(f"  {account} - {dept}: {var.variance} ({var.percentage}%)")

    approval = input("Approve adjustments? (yes/no): ")
    return approval.lower() == "yes"
```

### Step 4: Upload to Adaptive

```python
def step4_upload_to_adaptive(adjusted_actuals, month: str, year: int):
    """Upload finalized actuals to Adaptive."""
    version = f"{calendar.month_name[month]} {year} Actuals - Finalized"

    validation = import_adjusted_actuals(adjusted_actuals, version)

    if validation["status"] == "Success":
        print(f"✅ Uploaded {validation['records_imported']} records")
    else:
        print(f"⚠️ Errors: {validation['errors']}")

    # Log to audit trail
    log_audit_event(
        operation="adaptive_upload",
        inputs={"month": month, "year": year},
        outputs={"validation": validation}
    )
```

---

## Error Handling

### Common Error Codes

| Code | Message | Resolution |
|------|---------|------------|
| 401 | Unauthorized | Check API token validity |
| 404 | Account not found | Verify account exists in chart of accounts |
| 422 | Validation failed | Check data format (Decimal precision) |
| 429 | Rate limit exceeded | Implement retry with exponential backoff |
| 500 | Server error | Retry after 5 minutes, contact Adaptive support |

### Retry Logic

```python
from time import sleep

def api_call_with_retry(func, max_retries=3):
    """Retry API calls with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except requests.HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Retrying in {wait_time}s...")
                sleep(wait_time)
            else:
                raise
    raise Exception(f"Max retries exceeded")
```

---

## Data Validation Pre-Checks

**Before Upload:**
- [ ] All account IDs exist in Adaptive chart of accounts
- [ ] All amounts are Decimal (not float)
- [ ] All currencies are "USD" (or configured currency)
- [ ] No NULL values in required fields
- [ ] Department names match Adaptive dimensions

**Implementation:**
```python
def validate_before_upload(actuals: dict) -> tuple[bool, list[str]]:
    """Validate data before Adaptive upload."""
    errors = []

    # Check account IDs
    valid_accounts = get_adaptive_chart_of_accounts()
    for account_id in actuals.keys():
        if account_id not in valid_accounts:
            errors.append(f"Invalid account: {account_id}")

    # Check data types
    for account_id, data in actuals.items():
        for dept, amount in data["departments"].items():
            if not isinstance(amount, Decimal):
                errors.append(f"Float detected: {account_id} - {dept}")
            if amount is None:
                errors.append(f"NULL value: {account_id} - {dept}")

    return len(errors) == 0, errors
```

---

## Audit Trail Requirements

**Log All Operations:**
```json
{
  "timestamp": "2025-11-08T14:32:15.123Z",
  "operation": "adaptive_export_actuals",
  "user": "user@life360.com",
  "inputs": {
    "version": "November 2025 Actuals",
    "start_date": "2025-11-01",
    "end_date": "2025-11-30"
  },
  "outputs": {
    "records_exported": 50,
    "total_amount": "15430000.00"
  },
  "metadata": {
    "api_response_time_ms": 1234,
    "file_saved": "data/adaptive-exports/actuals_11_2025.json"
  }
}
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_adaptive_client.py

def test_export_actuals_xml_parsing():
    """Verify XML parsing uses Decimal."""
    xml_response = """
    <ActualsExport>
      <Account id="4000" name="Revenue">
        <Department name="Sales">
          <Amount>2500000.00</Amount>
        </Department>
      </Account>
    </ActualsExport>
    """
    result = parse_actuals_xml(xml_response)
    assert isinstance(result["4000"]["departments"]["Sales"], Decimal)
    assert result["4000"]["departments"]["Sales"] == Decimal("2500000.00")
```

### Integration Tests

```python
@pytest.mark.integration
def test_export_and_import_roundtrip():
    """Test export → modify → import cycle."""
    # Export
    actuals = export_actuals("Test Version", "2025-11-01", "2025-11-30")

    # Modify
    actuals["4000"]["departments"]["Sales"] += Decimal("10000.00")

    # Import
    validation = import_adjusted_actuals(actuals, "Test Version - Adjusted")

    assert validation["status"] == "Success"
    assert validation["records_imported"] > 0
```

---

## Configuration

**settings.yaml:**
```yaml
adaptive:
  instance_url: "https://life360.adaptiveinsights.com"
  api_version: "v1"
  timeout_seconds: 30
  max_retries: 3
  rate_limit_pause_seconds: 2
```

---

## Implementation Checklist

- [ ] Create `scripts/integrations/adaptive_client.py`
- [ ] Implement authentication (API token)
- [ ] Implement export_actuals()
- [ ] Implement export_budget()
- [ ] Implement import_adjusted_actuals()
- [ ] Add retry logic with exponential backoff
- [ ] Add pre-upload validation
- [ ] Add audit logging
- [ ] Create tests (unit + integration)
- [ ] Document credential setup in QUICK_START.md
- [ ] Test with Adaptive sandbox/test instance

---

**References:**
- Workday Adaptive Planning API Documentation
- Workiva Adaptive Insights Integration Guide
- Tray.ai Adaptive Planning Connector
- Workato Adaptive Planning API Reference

**Last Updated:** 2025-11-08
