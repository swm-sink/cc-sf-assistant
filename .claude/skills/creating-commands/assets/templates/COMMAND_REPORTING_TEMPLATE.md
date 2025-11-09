---
description: {{DESCRIPTION}}
---

# {{COMMAND_TITLE}}

**Usage:** `/{{COMMAND_NAME}} {{DATA_SOURCE}} {{OUTPUT_FORMAT}} [{{DATE_RANGE}}]`

**Purpose:** {{ONE_SENTENCE_PURPOSE}} with multi-format output and distribution.

---

## Phase 1: Define Data Sources

Identify and document all data sources:

**Data Source Inventory:**

| Source | Type | Location | Key Metrics |
|--------|------|----------|-------------|
| {{SOURCE_1}} | {{TYPE_1}} | {{LOCATION_1}} | {{METRICS_1}} |
| {{SOURCE_2}} | {{TYPE_2}} | {{LOCATION_2}} | {{METRICS_2}} |
| {{SOURCE_3}} | {{TYPE_3}} | {{LOCATION_3}} | {{METRICS_3}} |

**Required Metrics:**
1. {{METRIC_1_NAME}}: {{METRIC_1_DESCRIPTION}}
2. {{METRIC_2_NAME}}: {{METRIC_2_DESCRIPTION}}
3. {{METRIC_3_NAME}}: {{METRIC_3_DESCRIPTION}}
4. {{METRIC_4_NAME}}: {{METRIC_4_DESCRIPTION}}
5. {{METRIC_5_NAME}}: {{METRIC_5_DESCRIPTION}}

**Date Range:**
- Start: {{START_DATE}} (from arg $3 or default {{DEFAULT_START}})
- End: {{END_DATE}} (from arg $3 or default {{DEFAULT_END}})

---

## Phase 2: Aggregate Data

Load and combine data from all sources:

**Aggregation Steps:**

1. **Load {{SOURCE_1}}:**
   - Query: {{QUERY_1}}
   - Filters: {{FILTERS_1}}
   - Result: {{RESULT_1_DESCRIPTION}}

2. **Load {{SOURCE_2}}:**
   - Query: {{QUERY_2}}
   - Filters: {{FILTERS_2}}
   - Result: {{RESULT_2_DESCRIPTION}}

3. **Load {{SOURCE_3}}:**
   - Query: {{QUERY_3}}
   - Filters: {{FILTERS_3}}
   - Result: {{RESULT_3_DESCRIPTION}}

4. **Combine data:**
   - Join strategy: {{JOIN_STRATEGY}}
   - Reconciliation: {{RECONCILIATION_METHOD}}
   - Combined dataset: {{COMBINED_DATASET_DESCRIPTION}}

**Aggregation Rules:**
- {{AGGREGATION_RULE_1}}
- {{AGGREGATION_RULE_2}}
- {{AGGREGATION_RULE_3}}

**Calculated Metrics:**
- {{CALCULATED_METRIC_1}}: {{CALCULATION_FORMULA_1}}
- {{CALCULATED_METRIC_2}}: {{CALCULATION_FORMULA_2}}
- {{CALCULATED_METRIC_3}}: {{CALCULATION_FORMULA_3}}

---

## Phase 3: Analyze Trends

Identify patterns and insights:

**Trend Analysis:**

1. **{{TREND_ANALYSIS_1_NAME}}:**
   - Method: {{ANALYSIS_METHOD_1}}
   - Finding: {{FINDING_1}}
   - Insight: {{INSIGHT_1}}

2. **{{TREND_ANALYSIS_2_NAME}}:**
   - Method: {{ANALYSIS_METHOD_2}}
   - Finding: {{FINDING_2}}
   - Insight: {{INSIGHT_2}}

3. **{{TREND_ANALYSIS_3_NAME}}:**
   - Method: {{ANALYSIS_METHOD_3}}
   - Finding: {{FINDING_3}}
   - Insight: {{INSIGHT_3}}

**Variance Calculation:**
- Actual vs. Target: {{VARIANCE_CALCULATION}}
- Favorability: {{FAVORABILITY_LOGIC}}
- Material variances flagged: {{MATERIALITY_THRESHOLD}}

**Anomaly Detection:**
- Outliers identified: {{OUTLIER_DETECTION_METHOD}}
- Anomalies: {{ANOMALIES_FOUND}}
- Investigation notes: {{INVESTIGATION_NOTES}}

---

## Phase 4: Format Report

Apply formatting rules for presentation:

**Report Structure:**

1. **Executive Summary:**
   - {{EXECUTIVE_SUMMARY_COMPONENT_1}}
   - {{EXECUTIVE_SUMMARY_COMPONENT_2}}
   - {{EXECUTIVE_SUMMARY_COMPONENT_3}}

2. **Key Metrics:**
   | Metric | Current | Target | Variance | Status |
   |--------|---------|--------|----------|--------|
   | {{METRIC_1_NAME}} | {{CURRENT_1}} | {{TARGET_1}} | {{VARIANCE_1}} | {{STATUS_1}} |
   | {{METRIC_2_NAME}} | {{CURRENT_2}} | {{TARGET_2}} | {{VARIANCE_2}} | {{STATUS_2}} |
   | {{METRIC_3_NAME}} | {{CURRENT_3}} | {{TARGET_3}} | {{VARIANCE_3}} | {{STATUS_3}} |

3. **Detailed Analysis:**
   - {{DETAILED_SECTION_1}}
   - {{DETAILED_SECTION_2}}
   - {{DETAILED_SECTION_3}}

4. **Visualizations:**
   - {{CHART_1_DESCRIPTION}}
   - {{CHART_2_DESCRIPTION}}
   - {{CHART_3_DESCRIPTION}}

**Formatting Rules:**
- Conditional formatting: {{CONDITIONAL_FORMAT_RULES}}
- Color coding: {{COLOR_CODE_SCHEME}}
- Font styling: {{FONT_STYLING}}

---

## Phase 5: Distribute

Output to multiple formats and distribution channels:

**Output Formats:**

1. **Excel ({{OUTPUT_EXCEL_PATH}}):**
   - Sheets: {{EXCEL_SHEETS}}
   - Charts: {{EXCEL_CHARTS}}
   - Conditional formatting: {{EXCEL_FORMATTING}}

2. **PDF ({{OUTPUT_PDF_PATH}}):**
   - Layout: {{PDF_LAYOUT}}
   - Pages: {{PDF_PAGES}}
   - Print-optimized: {{PDF_PRINT_SETTINGS}}

3. **HTML ({{OUTPUT_HTML_PATH}}):**
   - Interactive: {{HTML_INTERACTIVE_FEATURES}}
   - Responsive: {{HTML_RESPONSIVE_DESIGN}}
   - Embeddable: {{HTML_EMBED_CODE}}

**Distribution Channels:**
- Email: {{EMAIL_RECIPIENTS}}
- Shared drive: {{SHARED_DRIVE_LOCATION}}
- Dashboard: {{DASHBOARD_URL}}

**Archival:**
- Archive location: {{ARCHIVE_LOCATION}}
- Retention period: {{RETENTION_PERIOD}}
- Version control: {{VERSION_CONTROL_METHOD}}

---

## Success Criteria

Before marking complete:

- [ ] All data sources loaded successfully
- [ ] Metrics calculated correctly
- [ ] Aggregation rules applied
- [ ] Trends analyzed
- [ ] Anomalies flagged
- [ ] Executive summary generated
- [ ] All output formats created (Excel, PDF, HTML)
- [ ] Formatting applied consistently
- [ ] Distribution channels executed
- [ ] Archive copy saved

---

## Example Invocation

```bash
/{{COMMAND_NAME}} data/financial_data.xlsx "excel,pdf,html" "2025-Q1"
```

**Expected Flow:**
1. Define sources → 3 data sources identified
2. Aggregate → Load and combine data for Q1 2025
3. Analyze → Identify 2 trends, 1 anomaly
4. Format → Create executive summary + 5 key metrics + 3 visualizations
5. Distribute → Generate Excel, PDF, HTML outputs

**Example Output:**
```
Financial Performance Report - Q1 2025

Executive Summary:
- Revenue: $5.2M (+8% vs target)
- Expenses: $3.1M (-5% vs budget, favorable)
- Net Income: $2.1M (+15% vs forecast)

Key Findings:
- Product sales exceeded target by 12%
- Operating expenses under budget due to hiring freeze
- Cash flow positive for 3rd consecutive quarter

Outputs:
- Excel: reports/Q1_2025_financial_performance.xlsx
- PDF: reports/Q1_2025_financial_performance.pdf
- HTML: reports/Q1_2025_financial_performance.html

Distributed to: finance-team@company.com
Archived: archive/reports/2025/Q1/
```

---

## Anti-Patterns (DON'T DO THIS)

❌ Aggregate without data source validation
❌ Skip trend analysis (just raw numbers)
❌ Single output format only
❌ Forget to archive reports
❌ Hardcode date ranges (make configurable)

✅ Validate all data sources before aggregation
✅ Analyze trends, calculate variances, flag anomalies
✅ Multi-format output (Excel + PDF + HTML)
✅ Archive with version control
✅ Configurable date ranges and filters

---

**This command enforces analytics best practices: structured aggregation, trend analysis, multi-format reporting, and distribution.**
