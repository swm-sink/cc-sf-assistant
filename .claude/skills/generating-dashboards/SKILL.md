---
name: generating-dashboards
description: Use when creating HTML dashboards, building financial visualizations, need custom dashboard layouts, want role-based views, thinking "I need a dashboard for this data", creating interactive reports, building KPI displays, or when user wants to customize dashboard appearance, add new chart types, create new role views, or modify existing dashboard templates - provides patterns for self-contained HTML dashboards with Chart.js
---

# Generating Dashboards

## Overview

**Purpose:** Create custom HTML dashboards from financial data, extending the three built-in role views (analyst, senior analyst, manager) or building entirely new layouts.

**What this skill does:**
- Guides creation of self-contained HTML dashboards (no server needed)
- Provides patterns for Chart.js chart integration
- Shows how to add custom KPI cards, tables, filters
- Explains the role-based architecture for extension

**Key principle:** Dashboards are single HTML files with embedded CSS, JS, and Chart.js. Share by email, open in any browser.

---

## When to Use

**Use when:**
- Creating a new dashboard view beyond analyst/senior_analyst/manager
- Adding custom charts or KPI cards to existing dashboards
- Building a dashboard for non-variance data (forecasting, consolidation)
- Customizing colors, layout, or chart types

**Don't use when:**
- Running existing variance analysis (use running-variance-analysis skill)
- Need server-side dashboards (this produces static HTML only)

---

## Architecture

The dashboard system lives in `scripts/integrations/html_dashboard.py`.

### Key Functions

```python
# Main entry point - generates complete HTML file
generate_dashboard(results, role, output_path, config) -> str

# Role-specific renderers (add new roles here)
_render_analyst_view(results, config) -> str      # Full detail
_render_senior_analyst_view(results, config) -> str  # Department summary
_render_manager_view(results, config) -> str      # Executive KPIs
```

### Data Flow

```
VarianceResult[] → _prepare_chart_data() → JSON → Chart.js renders
                 → _render_*_view()      → HTML tables/cards
                 → _generate_css(role)   → Role-specific styling
                 → _generate_js(role)    → Sort/filter/chart init
```

---

## How to Create a Custom Dashboard View

### Step 1: Define the Role

Add a new role to `scripts/utils/types.py`:
```python
UserRole = Literal["analyst", "senior_analyst", "manager", "board_member"]
```

### Step 2: Create the Renderer

Add a new function in `scripts/integrations/html_dashboard.py`:

```python
def _render_board_member_view(results: list[VarianceResult], config: DashboardConfig) -> str:
    """Ultra-high-level view for board members."""
    kpis = build_kpi_scorecard(results)

    # Only show 3-4 large KPI cards
    return f"""
<section class="board-kpis">
  <div class="mega-kpi">
    <div class="mega-value">{_fmt_currency(kpis['total_revenue_actual'])}</div>
    <div class="mega-label">Revenue</div>
  </div>
  <!-- Add more cards -->
</section>"""
```

### Step 3: Register in generate_dashboard()

```python
def generate_dashboard(results, role, output_path, config):
    if role == "board_member":
        body = _render_board_member_view(results, config)
    # ... existing roles
```

### Step 4: Add Role-Specific CSS

Add a new block in `_generate_css()`:
```python
elif role == "board_member":
    return base + """
.mega-kpi { font-size: 3em; padding: 40px; }
/* Ultra-spacious layout for boardroom projector */
"""
```

---

## How to Add Custom Charts

### Adding a New Chart.js Chart

1. Add data to `_prepare_chart_data()`:
```python
chart_data["myChart"] = {
    "labels": ["Q1", "Q2", "Q3", "Q4"],
    "values": [100, 200, 150, 300],
}
```

2. Add a canvas in your renderer:
```python
'<canvas id="myNewChart" height="300"></canvas>'
```

3. Add initialization in `_generate_js()`:
```javascript
const myCanvas = document.getElementById('myNewChart');
if (myCanvas && chartData.myChart) {
    new Chart(myCanvas, {
        type: 'line',  // bar, doughnut, radar, etc.
        data: { labels: chartData.myChart.labels, datasets: [{ data: chartData.myChart.values }] },
        options: { responsive: true }
    });
}
```

### Available Chart Types (Chart.js 4.x)
- `bar` / `horizontalBar` - Variance comparisons
- `line` - Trend analysis
- `doughnut` / `pie` - Category breakdowns
- `radar` - Department scorecards
- `scatter` - Correlation analysis
- `bubble` - Multi-dimensional comparison

---

## How to Add Custom KPI Cards

```python
def _render_custom_kpi(label: str, value: str, status: str) -> str:
    return f"""
<div class="kpi-card">
  <div class="traffic-light {status}"></div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-label">{label}</div>
</div>"""
```

Status values: `green`, `yellow`, `red` (uses existing CSS traffic light styles).

---

## How to Add Filters

The analyst view includes a complete filter system. To add filters to other views:

```html
<select id="customFilter" onchange="filterTable()">
  <option value="">All</option>
  <option value="critical">Critical Only</option>
</select>
```

Add data attributes to table rows:
```html
<tr data-custom="critical">...</tr>
```

The `filterTable()` JS function reads filter values and toggles row visibility.

---

## Template: Minimal Custom Dashboard

```python
from scripts.integrations.html_dashboard import generate_dashboard, _generate_html_shell
from scripts.utils.types import DashboardConfig

def my_custom_dashboard(data, output_path):
    body = """
    <section class="custom-section">
      <h2>My Custom View</h2>
      <!-- Your HTML here -->
    </section>
    """
    config = DashboardConfig(role="analyst", title="Custom Dashboard", period="Q4 2025")
    html = _generate_html_shell("Custom Dashboard", body, "analyst", config)
    with open(output_path, "w") as f:
        f.write(html)
```

---

## File Reference

| File | Purpose |
|------|---------|
| `scripts/integrations/html_dashboard.py` | Main dashboard generator (modify this) |
| `scripts/utils/types.py:DashboardConfig` | Dashboard configuration dataclass |
| `scripts/utils/types.py:UserRole` | Role type definition |
| `scripts/core/metrics.py:build_kpi_scorecard` | KPI calculation (data source for cards) |
| `scripts/core/variance.py:calculate_*_subtotals` | Aggregation functions for summaries |
