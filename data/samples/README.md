# Sample Financial Data for Testing

## Purpose

Realistic financial data files for testing FP&A automation workflows. Based on SaaS tech company structure similar to Life360.

**Sources:**
- SaaS Chart of Accounts best practices (Kruze Consulting, The SaaS CFO, 2024-2025)
- FP&A variance analysis patterns (NetSuite, Numeric, FloQast)
- Life360 context: Mobile app, subscription revenue, cloud infrastructure

---

## File Structure

```
data/samples/
├── README.md (this file)
├── budget_2025.xlsx                    # Annual budget for 2025
├── actuals_nov_2025.xlsx              # November actuals
├── actuals_dec_2025.xlsx              # December actuals
└── departments/                        # Multi-department consolidation test
    ├── engineering_budget.xlsx
    ├── sales_budget.xlsx
    ├── marketing_budget.xlsx
    ├── engineering_actuals_nov.xlsx
    ├── sales_actuals_nov.xlsx
    └── marketing_actuals_nov.xlsx
```

---

## Chart of Accounts Structure (50 accounts)

### Revenue Accounts (10)
| Account Code | Account Name | Type | Typical Monthly | Notes |
|--------------|--------------|------|-----------------|-------|
| 4000 | Subscription Revenue | Revenue | $2,500,000 | Core SaaS subscriptions |
| 4010 | Premium Features Revenue | Revenue | $450,000 | Add-on features |
| 4020 | Enterprise Revenue | Revenue | $800,000 | Enterprise contracts |
| 4030 | Professional Services | Revenue | $150,000 | Implementation, training |
| 4040 | Partner Revenue | Revenue | $200,000 | Channel/affiliate |
| 4050 | Advertising Revenue | Revenue | $100,000 | In-app advertising |
| 4060 | Data Licensing | Revenue | $75,000 | Anonymized data products |
| 4070 | Hardware Revenue | Revenue | $50,000 | IoT devices (if applicable) |
| 4080 | Other Revenue | Revenue | $25,000 | Miscellaneous |
| 4090 | Deferred Revenue Recognized | Revenue | $150,000 | Recognized from prior periods |

**Total Revenue: ~$4,500,000/month**

### Cost of Goods Sold - COGS (8)
| Account Code | Account Name | Type | Typical Monthly | Notes |
|--------------|--------------|------|-----------------|-------|
| 5000 | Cloud Hosting (AWS/GCP) | COGS | $450,000 | 10% of revenue |
| 5010 | Data Storage & Bandwidth | COGS | $180,000 | 4% of revenue |
| 5020 | Third-Party APIs | COGS | $90,000 | Google Maps, location services |
| 5030 | Payment Processing Fees | COGS | $135,000 | Stripe, PayPal (3% of revenue) |
| 5040 | Customer Success Salaries | COGS | $250,000 | CS team compensation |
| 5050 | Technical Support Salaries | COGS | $180,000 | Support team |
| 5060 | Onboarding & Implementation | COGS | $70,000 | Professional services costs |
| 5070 | License & Royalties | COGS | $45,000 | Third-party licenses |

**Total COGS: ~$1,400,000/month (31% gross margin)**

### Operating Expenses - Engineering (8)
| Account Code | Account Name | Type | Typical Monthly | Notes |
|--------------|--------------|------|-----------------|-------|
| 6000 | Engineering Salaries | OpEx | $800,000 | Development team |
| 6010 | Product Management Salaries | OpEx | $200,000 | PM team |
| 6020 | QA/Testing Salaries | OpEx | $150,000 | QA engineers |
| 6030 | Dev Tools & Software | OpEx | $50,000 | GitHub, IDEs, monitoring |
| 6040 | Contractors & Consultants | OpEx | $100,000 | External dev resources |
| 6050 | Infrastructure R&D | OpEx | $75,000 | Experimental infrastructure |
| 6060 | Security & Compliance | OpEx | $60,000 | Security tools, audits |
| 6070 | Training & Development | OpEx | $25,000 | Engineering education |

**Total Engineering OpEx: ~$1,460,000/month**

### Operating Expenses - Sales & Marketing (12)
| Account Code | Account Name | Type | Typical Monthly | Notes |
|--------------|--------------|------|-----------------|-------|
| 7000 | Sales Salaries | OpEx | $400,000 | Sales team base |
| 7010 | Sales Commissions | OpEx | $320,000 | Variable compensation |
| 7020 | Marketing Salaries | OpEx | $250,000 | Marketing team |
| 7030 | Digital Advertising | OpEx | $300,000 | Google, Facebook, etc. |
| 7040 | Content & SEO | OpEx | $80,000 | Content creation, SEO tools |
| 7050 | Events & Conferences | OpEx | $100,000 | Trade shows, sponsorships |
| 7060 | Marketing Tools | OpEx | $60,000 | HubSpot, analytics, etc. |
| 7070 | PR & Communications | OpEx | $50,000 | PR agency, comms |
| 7080 | Partner Marketing | OpEx | $70,000 | Co-marketing programs |
| 7090 | Lead Generation | OpEx | $90,000 | Paid lead gen |
| 7100 | Brand & Creative | OpEx | $75,000 | Design, creative assets |
| 7110 | Sales Enablement | OpEx | $45,000 | Sales tools, training |

**Total Sales & Marketing OpEx: ~$1,840,000/month**

### Operating Expenses - G&A (12)
| Account Code | Account Name | Type | Typical Monthly | Notes |
|--------------|--------------|------|-----------------|-------|
| 8000 | Executive Salaries | OpEx | $300,000 | C-suite compensation |
| 8010 | HR Salaries | OpEx | $120,000 | HR team |
| 8020 | Finance & Accounting Salaries | OpEx | $180,000 | Finance team (you!) |
| 8030 | IT & Systems | OpEx | $90,000 | Internal IT, hardware |
| 8040 | Legal & Professional Fees | OpEx | $120,000 | Legal, audit, consulting |
| 8050 | Office Rent | OpEx | $150,000 | Physical office space |
| 8060 | Office Utilities | OpEx | $20,000 | Electric, internet, etc. |
| 8070 | Insurance | OpEx | $60,000 | D&O, general liability |
| 8080 | Recruiting & HR Tools | OpEx | $80,000 | Recruiting fees, HRIS |
| 8090 | Travel & Entertainment | OpEx | $70,000 | Business travel |
| 8100 | Depreciation | OpEx | $50,000 | Equipment depreciation |
| 8110 | Other G&A | OpEx | $40,000 | Miscellaneous |

**Total G&A OpEx: ~$1,280,000/month**

---

## Budget vs Actuals - Variance Scenarios

### November 2025 Actuals (Sample)

**Material Favorable Variances (>10% and >$50k):**
- 4000 Subscription Revenue: Budget $2,500k, Actual $2,875k (+$375k, +15%) ✅ FAVORABLE
- 4020 Enterprise Revenue: Budget $800k, Actual $975k (+$175k, +21.9%) ✅ FAVORABLE
- 5000 Cloud Hosting: Budget $450k, Actual $405k (-$45k, -10%) ✅ FAVORABLE (expense down)

**Material Unfavorable Variances (>10% and >$50k):**
- 7030 Digital Advertising: Budget $300k, Actual $420k (+$120k, +40%) ❌ UNFAVORABLE (overspend)
- 7000 Sales Salaries: Budget $400k, Actual $480k (+$80k, +20%) ❌ UNFAVORABLE (overhiring)
- 6000 Engineering Salaries: Budget $800k, Actual $920k (+$120k, +15%) ❌ UNFAVORABLE (over budget)

**Immaterial Variances (<10% or <$50k):**
- Most other accounts within normal ranges

**Edge Cases for Testing:**
1. **Zero budget:** 6050 Infrastructure R&D: Budget $0, Actual $25k (new initiative)
2. **Negative actual:** 4090 Deferred Revenue: Actual -$50k (adjustment/refund)
3. **NULL value:** 7080 Partner Marketing: Missing data in actuals file
4. **Division by zero:** Account with $0 budget and $0 actual (no variance calculation needed)

---

## Excel File Format

### Columns (Consistent across all files):

| Column | Name | Data Type | Notes |
|--------|------|-----------|-------|
| A | Account_Code | Text | e.g., "4000", "5010" |
| B | Account_Name | Text | e.g., "Subscription Revenue" |
| C | Department | Text | "Engineering", "Sales", "Marketing", "G&A", "COGS" |
| D | Amount | Number (Decimal) | Dollar amount, 2 decimal places |
| E | Notes | Text (Optional) | Comments, explanations |

**Sample Row:**
```
4000 | Subscription Revenue | Revenue | 2500000.00 | Core monthly subscriptions
```

### File Specifications:

**budget_2025.xlsx:**
- Sheet: "Budget"
- 50 rows (accounts)
- No edge cases (clean baseline)

**actuals_nov_2025.xlsx:**
- Sheet: "Actuals"
- 50 rows (accounts)
- Includes edge cases:
  - Row 23 (4090 Deferred Revenue): Negative value -$50,000
  - Row 38 (7080 Partner Marketing): NULL/blank Amount
  - Row 42 (6050 Infrastructure R&D): Zero budget line item

**actuals_dec_2025.xlsx:**
- Sheet: "Actuals"
- 50 rows (accounts)
- Different variance pattern (recovery month after November overspend)

---

## Department-Level Files

### Purpose
Test multi-department consolidation workflows.

### Structure

Each department has:
- Budget file with their accounts only
- Actuals file with their accounts only

**engineering_budget.xlsx** (16 accounts):
- 6000-6070 (Engineering OpEx)
- 5040-5050 (CS/Support in COGS)

**sales_budget.xlsx** (12 accounts):
- 7000-7110 (Sales & Marketing OpEx)

**marketing_budget.xlsx** (10 accounts):
- 4000-4090 (Revenue accounts they forecast)

### Consolidation Test Scenarios

1. **Happy path:** All departments file present, all accounts match
2. **Missing department:** One department file not provided
3. **Duplicate accounts:** Same account in multiple department files (should flag error)
4. **Unmapped accounts:** Department uses account code not in master chart

---

## Data Generation Checklist

When creating Excel files:

- [ ] Use Decimal precision (2 decimal places for all amounts)
- [ ] Include all 50 accounts in budget and actuals files
- [ ] Implement 6 material variances (3 favorable, 3 unfavorable)
- [ ] Include 3 edge cases (negative, NULL, zero budget)
- [ ] Department files sum to consolidated totals
- [ ] Realistic dollar amounts based on SaaS benchmarks
- [ ] Consistent column naming across all files
- [ ] No floating point errors (use Decimal in generation script)

---

## Usage in Tests

```python
# Load sample data
budget = pd.read_excel("data/samples/budget_2025.xlsx")
actuals = pd.read_excel("data/samples/actuals_nov_2025.xlsx")

# Test variance calculation
from scripts.core.variance import calculate_variance
results = calculate_variance(budget, actuals)

# Verify material variances flagged
assert len(results[results['material'] == True]) == 6

# Verify edge cases handled
assert results[results['Account_Code'] == '4090']['variance'].iloc[0] < 0  # Negative
assert pd.isna(results[results['Account_Code'] == '7080']['variance'].iloc[0])  # NULL
```

---

## Future Enhancements

- Add quarterly data files (Q1-Q4 2025)
- Add multi-year data (2024 vs 2025 for YoY)
- Add forecast files (vs plan, vs prior forecast comparisons)
- Add actuals with daily/weekly granularity
- Add multi-currency examples

---

**Created:** 2025-11-08
**Last Updated:** 2025-11-08
**Source:** Research from SaaS FP&A best practices + Life360 context
