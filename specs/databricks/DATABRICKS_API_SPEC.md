# Databricks SQL API Integration Specification

**System:** Databricks SQL Warehouse
**Purpose:** Query financial data for variance analysis and reporting
**API Type:** SQL Statement Execution API (REST)
**Authentication:** Personal Access Token (PAT)

---

## Business Context

**Workflow Position:** POST-CLOSE data extraction

```
[DATABRICKS] Query actuals from data warehouse
↓
[LOCAL] Combine with Adaptive budget data
↓
[LOCAL] Variance analysis
↓
[ADAPTIVE] Upload finalized data
↓
[GOOGLE] Generate reports
```

**Key Requirement:** Read-only access to financial tables for analysis

---

## API Capabilities Research Summary

**Source 1:** Databricks SQL Statement Execution API (2025)
- Execute SQL queries via REST API
- Supports parameterized statements (SQL injection prevention)
- Pagination for large result sets
- Asynchronous execution with polling

**Source 2:** Databricks Financial Data Integration Best Practices
- Use Delta Lake for ACID transactions
- System tables for audit logging (`system.access.audit`)
- Unity Catalog for data governance
- SQL warehouses for analytics (not clusters)

**Source 3:** Databricks REST API 2.0
- Authentication: Personal Access Token
- Rate limits: 1000 requests/hour (standard tier)
- Result format: JSON (rows as arrays or objects)
- Max result size: 25 MB per query

---

## Authentication Strategy

### Personal Access Token (Recommended)

**Setup:**
1. Databricks workspace → User Settings → Access Tokens
2. Generate token with SQL Warehouse access
3. Store in `config/credentials/databricks-token.json`
4. Git-ignore credentials (already configured)

**Token Format:**
```json
{
  "token": "dapi1234567890abcdef",
  "workspace_url": "https://life360.cloud.databricks.com",
  "warehouse_id": "abc123xyz456",
  "catalog": "finance",
  "schema": "actuals"
}
```

**Usage in Scripts:**
```python
from pathlib import Path
import json

def load_databricks_credentials():
    cred_path = Path("config/credentials/databricks-token.json")
    if not cred_path.exists():
        raise FileNotFoundError("Databricks credentials not found")
    with open(cred_path) as f:
        return json.load(f)

creds = load_databricks_credentials()
headers = {
    "Authorization": f"Bearer {creds['token']}",
    "Content-Type": "application/json"
}
```

---

## SQL Statement Execution API

### Execute Query

**Endpoint:** `POST /api/2.0/sql/statements/`

**Request Format:**
```json
{
  "warehouse_id": "abc123xyz456",
  "catalog": "finance",
  "schema": "actuals",
  "statement": "SELECT account_id, account_name, department, amount FROM monthly_actuals WHERE month = :month AND year = :year",
  "parameters": [
    {"name": "month", "value": "11"},
    {"name": "year", "value": "2025"}
  ],
  "wait_timeout": "30s",
  "on_wait_timeout": "CONTINUE"
}
```

**Response Format:**
```json
{
  "statement_id": "01234567-89ab-cdef-0123-456789abcdef",
  "status": {
    "state": "SUCCEEDED"
  },
  "manifest": {
    "total_row_count": 50,
    "total_chunk_count": 1
  },
  "result": {
    "data_array": [
      ["4000", "Subscription Revenue", "Enterprise", "2875000.00"],
      ["4010", "Premium Features", "Product", "495000.00"]
    ]
  }
}
```

---

## Python Implementation

### Query Execution

```python
import requests
from decimal import Decimal
from typing import List, Dict, Any

def execute_databricks_query(
    query: str,
    parameters: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """Execute SQL query on Databricks SQL Warehouse.

    Args:
        query: SQL statement (use :param for parameterization)
        parameters: {param_name: value} for parameterized queries

    Returns: List of rows as dictionaries
    """
    creds = load_databricks_credentials()
    url = f"{creds['workspace_url']}/api/2.0/sql/statements/"
    headers = {
        "Authorization": f"Bearer {creds['token']}",
        "Content-Type": "application/json"
    }

    # Build request payload
    payload = {
        "warehouse_id": creds["warehouse_id"],
        "catalog": creds["catalog"],
        "schema": creds["schema"],
        "statement": query,
        "wait_timeout": "30s",
        "on_wait_timeout": "CONTINUE"
    }

    # Add parameters if provided
    if parameters:
        payload["parameters"] = [
            {"name": k, "value": str(v)}
            for k, v in parameters.items()
        ]

    # Execute query
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    # Check if query succeeded
    if result["status"]["state"] != "SUCCEEDED":
        raise RuntimeError(f"Query failed: {result['status']}")

    # Parse results
    return parse_databricks_result(result)


def parse_databricks_result(result: dict) -> List[Dict[str, Any]]:
    """Parse Databricks API result into structured data.

    Converts amounts to Decimal for financial precision.
    """
    rows = []
    data_array = result["result"]["data_array"]

    # Get column names from manifest (if available)
    # Otherwise infer from query
    columns = result["manifest"].get("schema", {}).get("columns", [])

    for row in data_array:
        row_dict = {}
        for i, value in enumerate(row):
            col_name = columns[i]["name"] if i < len(columns) else f"col_{i}"

            # Convert amounts to Decimal
            if col_name in ["amount", "budget", "actual", "variance"]:
                row_dict[col_name] = Decimal(value) if value else None
            else:
                row_dict[col_name] = value

        rows.append(row_dict)

    return rows
```

---

## Common Queries

### Query Monthly Actuals

```python
def query_monthly_actuals(month: int, year: int) -> Dict[str, Dict[str, Decimal]]:
    """Query monthly actuals from Databricks.

    Returns: {account_id: {dept: Decimal(amount)}}
    """
    query = """
    SELECT
        account_id,
        account_name,
        department,
        SUM(amount) as total_amount
    FROM finance.actuals.monthly_actuals
    WHERE month = :month
      AND year = :year
    GROUP BY account_id, account_name, department
    ORDER BY account_id, department
    """

    rows = execute_databricks_query(query, {"month": month, "year": year})

    # Structure data
    actuals = {}
    for row in rows:
        account_id = row["account_id"]
        if account_id not in actuals:
            actuals[account_id] = {
                "name": row["account_name"],
                "departments": {}
            }
        actuals[account_id]["departments"][row["department"]] = row["total_amount"]

    return actuals
```

### Query Department Summary

```python
def query_department_summary(month: int, year: int, dept: str) -> List[Dict]:
    """Query all accounts for a specific department.

    Returns: List of {account_id, account_name, amount}
    """
    query = """
    SELECT
        account_id,
        account_name,
        SUM(amount) as total_amount
    FROM finance.actuals.monthly_actuals
    WHERE month = :month
      AND year = :year
      AND department = :dept
    GROUP BY account_id, account_name
    ORDER BY account_id
    """

    return execute_databricks_query(query, {
        "month": month,
        "year": year,
        "dept": dept
    })
```

### Query YoY Comparison

```python
def query_yoy_comparison(month: int, year: int) -> List[Dict]:
    """Query year-over-year comparison for same month.

    Returns: List of {account_id, current_year, prior_year, yoy_variance}
    """
    query = """
    SELECT
        account_id,
        account_name,
        SUM(CASE WHEN year = :year THEN amount ELSE 0 END) as current_year,
        SUM(CASE WHEN year = :prior_year THEN amount ELSE 0 END) as prior_year,
        (SUM(CASE WHEN year = :year THEN amount ELSE 0 END) -
         SUM(CASE WHEN year = :prior_year THEN amount ELSE 0 END)) as yoy_variance
    FROM finance.actuals.monthly_actuals
    WHERE month = :month
      AND year IN (:year, :prior_year)
    GROUP BY account_id, account_name
    ORDER BY account_id
    """

    return execute_databricks_query(query, {
        "month": month,
        "year": year,
        "prior_year": year - 1
    })
```

---

## Asynchronous Query Execution

For large queries (>30 seconds):

```python
import time

def execute_async_query(query: str, parameters: dict = None) -> str:
    """Submit query for asynchronous execution.

    Returns: statement_id for polling
    """
    creds = load_databricks_credentials()
    url = f"{creds['workspace_url']}/api/2.0/sql/statements/"
    headers = {
        "Authorization": f"Bearer {creds['token']}",
        "Content-Type": "application/json"
    }

    payload = {
        "warehouse_id": creds["warehouse_id"],
        "catalog": creds["catalog"],
        "schema": creds["schema"],
        "statement": query,
        "wait_timeout": "0s",  # Return immediately
    }

    if parameters:
        payload["parameters"] = [
            {"name": k, "value": str(v)}
            for k, v in parameters.items()
        ]

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    return result["statement_id"]


def poll_query_status(statement_id: str, max_wait_seconds: int = 300) -> dict:
    """Poll query status until completion.

    Args:
        statement_id: Statement ID from execute_async_query()
        max_wait_seconds: Maximum time to wait

    Returns: Query result
    """
    creds = load_databricks_credentials()
    url = f"{creds['workspace_url']}/api/2.0/sql/statements/{statement_id}"
    headers = {"Authorization": f"Bearer {creds['token']}"}

    start_time = time.time()
    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()

        state = result["status"]["state"]

        if state == "SUCCEEDED":
            return result
        elif state in ["FAILED", "CANCELED", "CLOSED"]:
            raise RuntimeError(f"Query {state}: {result['status']}")
        elif time.time() - start_time > max_wait_seconds:
            raise TimeoutError(f"Query exceeded {max_wait_seconds}s timeout")
        else:
            time.sleep(2)  # Poll every 2 seconds
```

---

## Data Validation Pre-Checks

**Before Processing Results:**
- [ ] All amounts converted to Decimal (not float)
- [ ] NULL values handled explicitly
- [ ] Account IDs match expected format
- [ ] Department names match Adaptive dimensions
- [ ] No duplicate rows (GROUP BY applied correctly)

**Implementation:**
```python
def validate_databricks_result(rows: List[Dict]) -> tuple[bool, list[str]]:
    """Validate query results before use."""
    errors = []

    # Check for required fields
    required_fields = ["account_id", "account_name", "amount"]
    for i, row in enumerate(rows):
        for field in required_fields:
            if field not in row:
                errors.append(f"Row {i}: Missing field '{field}'")

        # Check Decimal type
        if "amount" in row and not isinstance(row["amount"], Decimal):
            errors.append(f"Row {i}: Amount is not Decimal: {type(row['amount'])}")

        # Check NULL values
        if row.get("amount") is None:
            errors.append(f"Row {i}: NULL amount for account {row.get('account_id')}")

    return len(errors) == 0, errors
```

---

## Error Handling

### Common Error Codes

| Code | Message | Resolution |
|------|---------|------------|
| 401 | Unauthorized | Check PAT token validity |
| 403 | Forbidden | Verify SQL Warehouse permissions |
| 404 | Warehouse not found | Check warehouse_id in credentials |
| 429 | Rate limit exceeded | Implement exponential backoff |
| 500 | Query execution failed | Check SQL syntax, table permissions |

### Retry Logic

```python
from time import sleep

def databricks_query_with_retry(query: str, params: dict = None, max_retries: int = 3):
    """Retry Databricks queries with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return execute_databricks_query(query, params)
        except requests.HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt
                print(f"Rate limited. Retrying in {wait_time}s...")
                sleep(wait_time)
            elif e.response.status_code >= 500:  # Server error
                wait_time = 5 * (attempt + 1)
                print(f"Server error. Retrying in {wait_time}s...")
                sleep(wait_time)
            else:
                raise
    raise Exception(f"Max retries exceeded for query")
```

---

## Audit Trail Requirements

**Log All Queries:**
```json
{
  "timestamp": "2025-11-08T14:32:15.123Z",
  "operation": "databricks_query_actuals",
  "user": "user@life360.com",
  "inputs": {
    "query": "SELECT ... FROM monthly_actuals WHERE ...",
    "parameters": {"month": 11, "year": 2025}
  },
  "outputs": {
    "rows_returned": 50,
    "query_duration_ms": 2341
  },
  "metadata": {
    "warehouse_id": "abc123xyz456",
    "statement_id": "01234567-89ab-cdef-0123-456789abcdef"
  }
}
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_databricks_client.py

def test_parse_databricks_result_decimal_conversion():
    """Verify amounts parsed as Decimal."""
    mock_result = {
        "status": {"state": "SUCCEEDED"},
        "manifest": {
            "schema": {
                "columns": [
                    {"name": "account_id"},
                    {"name": "amount"}
                ]
            }
        },
        "result": {
            "data_array": [
                ["4000", "2500000.00"],
                ["5000", "450000.00"]
            ]
        }
    }

    rows = parse_databricks_result(mock_result)

    assert isinstance(rows[0]["amount"], Decimal)
    assert rows[0]["amount"] == Decimal("2500000.00")
```

### Integration Tests

```python
@pytest.mark.integration
def test_query_monthly_actuals_from_databricks():
    """Test actual Databricks query (requires credentials)."""
    # Only run if credentials exist
    if not Path("config/credentials/databricks-token.json").exists():
        pytest.skip("Databricks credentials not configured")

    actuals = query_monthly_actuals(month=11, year=2025)

    assert len(actuals) > 0
    for account_id, data in actuals.items():
        assert isinstance(account_id, str)
        assert "name" in data
        assert "departments" in data
        for dept, amount in data["departments"].items():
            assert isinstance(amount, Decimal)
```

---

## Workflow Integration

### Combine Databricks + Adaptive Data

```python
# scripts/workflows/post_close_review.py

def step1_gather_data(month: int, year: int):
    """Gather data from both Databricks and Adaptive."""

    # Query actuals from Databricks
    databricks_actuals = query_monthly_actuals(month, year)

    # Export budget from Adaptive
    adaptive_budget = export_budget(
        version=f"FY {year} Budget",
        period="monthly",
        month=month
    )

    # Reconcile accounts (ensure same account set)
    databricks_accounts = set(databricks_actuals.keys())
    adaptive_accounts = set(adaptive_budget.keys())

    missing_in_databricks = adaptive_accounts - databricks_accounts
    missing_in_adaptive = databricks_accounts - adaptive_accounts

    if missing_in_databricks or missing_in_adaptive:
        print("⚠️ Account reconciliation required:")
        if missing_in_databricks:
            print(f"  Missing in Databricks: {missing_in_databricks}")
        if missing_in_adaptive:
            print(f"  Missing in Adaptive: {missing_in_adaptive}")

    return databricks_actuals, adaptive_budget
```

---

## Security Considerations

**SQL Injection Prevention:**
- ALWAYS use parameterized queries (`:param` syntax)
- NEVER concatenate user input into SQL strings

**Bad (SQL Injection Risk):**
```python
# DON'T DO THIS
dept = input("Enter department: ")
query = f"SELECT * FROM actuals WHERE department = '{dept}'"
```

**Good (Parameterized):**
```python
# DO THIS
dept = input("Enter department: ")
query = "SELECT * FROM actuals WHERE department = :dept"
result = execute_databricks_query(query, {"dept": dept})
```

**Token Security:**
- Store in git-ignored credentials file
- Rotate tokens every 90 days
- Use minimum permissions (read-only for analytics)

---

## Configuration

**settings.yaml:**
```yaml
databricks:
  workspace_url: "https://life360.cloud.databricks.com"
  catalog: "finance"
  schema: "actuals"
  timeout_seconds: 30
  max_retries: 3
  rate_limit_pause_seconds: 2
```

---

## Implementation Checklist

- [ ] Create `scripts/integrations/databricks_client.py`
- [ ] Implement authentication (PAT)
- [ ] Implement execute_databricks_query()
- [ ] Implement parse_databricks_result() with Decimal conversion
- [ ] Implement async query execution and polling
- [ ] Add retry logic with exponential backoff
- [ ] Add result validation
- [ ] Add audit logging
- [ ] Create tests (unit + integration)
- [ ] Document credential setup in QUICK_START.md
- [ ] Test with Databricks test warehouse

---

**References:**
- Databricks SQL Statement Execution API (2025)
- Databricks REST API 2.0 Documentation
- Databricks Unity Catalog Best Practices
- Databricks Financial Data Integration Guide

**Last Updated:** 2025-11-08
