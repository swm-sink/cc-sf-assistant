# Credentials Setup Guide

**Purpose:** Instructions for configuring API credentials for Databricks, Adaptive Insights, and Google Workspace integrations.

**Security:** All files in this directory are `.gitignore`d and will NEVER be committed to version control.

---

## Quick Start

1. Copy credential templates from examples below
2. Save as specified filenames in this directory
3. Verify `.gitignore` blocks these files from commits
4. Test connections using `/test-connection` commands (when implemented)

---

## Databricks SQL Warehouse

**File:** `databricks.json`

**Purpose:** Extract monthly actuals from Databricks SQL warehouse

**Required Credentials:**
```json
{
  "server_hostname": "your-workspace.cloud.databricks.com",
  "http_path": "/sql/1.0/warehouses/your-warehouse-id",
  "access_token": "dapi1234567890abcdef"
}
```

**How to Obtain:**
1. **Server Hostname:**
   - Navigate to your Databricks workspace
   - Copy URL (e.g., `adb-1234567890123456.7.azuredatabricks.net`)

2. **HTTP Path:**
   - Go to SQL Warehouses in sidebar
   - Select your warehouse
   - Click "Connection Details" tab
   - Copy HTTP Path (format: `/sql/1.0/warehouses/abc123def456`)

3. **Access Token:**
   - Click your user profile (top right)
   - Select "User Settings"
   - Navigate to "Access Tokens" tab
   - Click "Generate New Token"
   - Set comment: "FP&A Automation Assistant"
   - Set lifetime: 90 days (or as per company policy)
   - **COPY TOKEN IMMEDIATELY** (only shown once)

**Documentation:** [Databricks SQL Connector Docs](https://docs.databricks.com/dev-tools/python-sql-connector.html)

**Security Notes:**
- Tokens expire - set calendar reminder to regenerate
- Use workspace-scoped tokens (not account-level)
- Limit token to read-only access if possible

---

## Adaptive Insights API

**File:** `adaptive.json`

**Purpose:** Extract budget data from Adaptive Insights

**Required Credentials:**
```json
{
  "api_endpoint": "https://api.adaptiveinsights.com/api/v1",
  "api_token": "your-api-token-here",
  "instance_code": "your-instance-code"
}
```

**How to Obtain:**
1. **API Endpoint:**
   - Standard: `https://api.adaptiveinsights.com/api/v1`
   - EU: `https://api-eu.adaptiveinsights.com/api/v1`
   - Ask your Adaptive admin if unsure

2. **API Token:**
   - Log into Adaptive Insights as admin
   - Navigate to "Administration" → "API Tokens"
   - Click "Create New Token"
   - Set description: "FP&A Automation Assistant - [Your Name]"
   - Set permissions: Read-only access to budget versions
   - Copy token (only shown once)

3. **Instance Code:**
   - Provided by Adaptive during setup
   - Usually visible in URL: `https://[INSTANCE_CODE].adaptiveinsights.com`
   - Contact Adaptive support if unknown

**Documentation:** [Adaptive Insights API Docs](https://success.workday.com/s/adaptive-planning-integration-api)

**Security Notes:**
- Tokens do not expire but can be revoked
- Use read-only tokens (no write permissions needed)
- Document who owns each token for audit purposes

---

## Google Workspace (Sheets & Slides)

**File:** `google_credentials.json` (OAuth 2.0 service account)

**Purpose:** Upload variance reports to Google Sheets and Slides

**Required Credentials:**
Service account JSON file from Google Cloud Console

**How to Obtain:**

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Create Project"
3. Name: "FP&A Automation Assistant"
4. Click "Create"

### Step 2: Enable APIs
1. Navigate to "APIs & Services" → "Library"
2. Enable these APIs:
   - Google Sheets API
   - Google Slides API
   - Google Drive API (for file management)

### Step 3: Create Service Account
1. Navigate to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name: "fpa-automation-assistant"
4. Role: "Editor" (or custom role with Sheets/Slides access)
5. Click "Done"

### Step 4: Generate JSON Key
1. Click on created service account
2. Navigate to "Keys" tab
3. Click "Add Key" → "Create New Key"
4. Select JSON format
5. Click "Create" (downloads `google_credentials.json`)
6. **Move downloaded file to this directory**

### Step 5: Grant Access to Folders/Files
Service accounts need explicit access to Google Drive folders:

**Option A: Share with service account email**
- Service account email format: `fpa-automation-assistant@project-id.iam.gserviceaccount.com`
- Share target Google Drive folder with this email (Editor access)

**Option B: Domain-wide delegation** (enterprise only)
- Requires Google Workspace admin
- See [Domain-wide delegation guide](https://developers.google.com/identity/protocols/oauth2/service-account#delegatingauthority)

**Documentation:** [Google Workspace API Authentication](https://developers.google.com/workspace/guides/auth-overview)

**Security Notes:**
- Service account keys never expire
- Treat JSON file like a password (never commit to git)
- Rotate keys every 90 days per security best practices
- Monitor service account activity in Google Cloud Console

---

## Environment Variables (Alternative)

**File:** `.env` (in project root, NOT this directory)

**Purpose:** Store credentials as environment variables instead of JSON files

**Format:**
```bash
# Databricks
DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
DATABRICKS_ACCESS_TOKEN=dapi1234567890abcdef

# Adaptive Insights
ADAPTIVE_API_ENDPOINT=https://api.adaptiveinsights.com/api/v1
ADAPTIVE_API_TOKEN=your-api-token-here
ADAPTIVE_INSTANCE_CODE=your-instance-code

# Google (path to service account JSON)
GOOGLE_APPLICATION_CREDENTIALS=config/credentials/google_credentials.json
```

**Usage:**
Scripts will check for environment variables first, then fall back to JSON files.

**Security Notes:**
- `.env` files are `.gitignore`d (never committed)
- Use `.env.example` (committed) as template
- Load with `python-dotenv` package

---

## Verification Checklist

Before using credentials in production:

- [ ] All credential files are in `config/credentials/` directory
- [ ] `.gitignore` blocks credential files (test with `git status`)
- [ ] JSON files have valid syntax (test with `python -m json.tool file.json`)
- [ ] Databricks token has SQL warehouse access
- [ ] Adaptive token has read-only permissions
- [ ] Google service account email has access to target folders
- [ ] Document credential owner and expiration dates (if applicable)
- [ ] Calendar reminders set for token rotation (90-day cycle recommended)

---

## Troubleshooting

### "Permission Denied" Errors
- Databricks: Verify warehouse is running and token has `CAN USE` permission
- Adaptive: Verify token has access to budget version
- Google: Verify service account email is shared on target folder/file

### "Invalid Credentials" Errors
- Check for copy/paste errors (trailing spaces, line breaks)
- Verify JSON syntax is valid (`python -m json.tool file.json`)
- Confirm credentials haven't expired or been revoked

### "File Not Found" Errors
- Verify credential files are in `config/credentials/` directory
- Check filename matches exactly (case-sensitive)
- Ensure file has `.json` extension

---

## Security Best Practices

1. **NEVER commit credentials to git** - `.gitignore` enforced
2. **Rotate tokens every 90 days** - Set calendar reminders
3. **Use read-only permissions** where possible
4. **Document credential ownership** - Who created each token?
5. **Monitor API usage** - Check for anomalies monthly
6. **Revoke unused tokens** - Clean up old credentials
7. **Use separate credentials per user** - No shared tokens
8. **Encrypt credentials at rest** (enterprise) - Use secret managers like HashiCorp Vault

---

## Support

**Internal Questions:**
- Contact: [Your FP&A team lead]
- Slack: [Your internal channel]

**External Documentation:**
- Databricks: https://docs.databricks.com
- Adaptive Insights: https://success.workday.com
- Google Workspace: https://developers.google.com/workspace

---

**Last Updated:** 2025-11-10
**Maintained By:** FP&A Automation Team
