---
name: generating-presentations
description: Use when creating HTML presentations, building slide decks, need financial presentation templates, want board-ready slides, thinking "I need a presentation from this data", creating executive decks, building slide-based reports, or when user wants to customize presentation themes, add new slide types, modify slide layouts, or create presentation templates - provides patterns for self-contained HTML slide decks with keyboard navigation and Chart.js
---

# Generating Presentations

## Overview

**Purpose:** Create custom HTML slide-deck presentations from financial data, with keyboard navigation, Chart.js charts, and executive-friendly formatting.

**What this skill does:**
- Guides creation of self-contained HTML presentations (no PowerPoint/Slides needed)
- Shows how to add custom slide types
- Provides patterns for dark-theme executive presentations
- Explains keyboard navigation and print support

**Key principle:** Presentations are single HTML files. Arrow keys navigate slides. Print to PDF for distribution.

---

## When to Use

**Use when:**
- Creating a custom presentation layout
- Adding new slide types (trend analysis, forecast, comparison)
- Building a board deck from financial data
- Customizing presentation theme or styling

**Don't use when:**
- Running existing variance analysis (use running-variance-analysis skill)
- Need Google Slides integration (not yet implemented)
- Building interactive dashboards (use generating-dashboards skill)

---

## Architecture

The presentation system lives in `scripts/integrations/html_presentation.py`.

### Key Functions

```python
# Main entry point
generate_presentation(results, output_path, metadata) -> str

# Slide renderers (add new slides here)
_render_title_slide(metadata) -> str
_render_executive_summary_slide(results) -> str
_render_waterfall_slide(results) -> str
_render_department_slide(dept, dept_results) -> str
_render_material_variances_slide(results) -> str
_render_kpi_scorecard_slide(results) -> str
_render_appendix_slide(metadata) -> str
```

### Slide Structure

Each slide is a `<section class="slide">` element. The JS handles:
- Arrow key navigation (left/right)
- Spacebar advances
- Slide counter display
- Only one slide visible at a time (CSS `display: none/flex`)

---

## How to Add a Custom Slide

### Step 1: Create the Renderer

```python
def _render_trend_slide(results: list[VarianceResult]) -> str:
    return """
<div class="slide-content">
  <h2>Variance Trends</h2>
  <div class="chart-full">
    <canvas id="trendChart" height="400"></canvas>
  </div>
</div>"""
```

### Step 2: Add to Slide List

In `generate_presentation()`:
```python
slides = [
    _render_title_slide(metadata),
    _render_executive_summary_slide(results),
    _render_trend_slide(results),         # NEW
    _render_waterfall_slide(results),
    # ... rest of slides
]
```

### Step 3: Add Chart Data (if needed)

In `_prepare_presentation_chart_data()`:
```python
chart_data["trend"] = {
    "labels": ["Jan", "Feb", "Mar", ...],
    "values": [100, 120, 115, ...],
}
```

### Step 4: Initialize Chart in JS

In `_presentation_js()`, add Chart.js initialization:
```javascript
const trendCanvas = document.getElementById('trendChart');
if (trendCanvas && chartData.trend) {
    new Chart(trendCanvas, {
        type: 'line',
        data: { labels: chartData.trend.labels, datasets: [{ data: chartData.trend.values }] }
    });
}
```

---

## Slide Templates

### Data Table Slide
```python
def _render_table_slide(title, headers, rows):
    header_html = "".join(f"<th>{h}</th>" for h in headers)
    row_html = ""
    for row in rows:
        cells = "".join(f"<td>{cell}</td>" for cell in row)
        row_html += f"<tr>{cells}</tr>"
    return f"""
<div class="slide-content">
  <h2>{title}</h2>
  <table class="pres-table">
    <thead><tr>{header_html}</tr></thead>
    <tbody>{row_html}</tbody>
  </table>
</div>"""
```

### Comparison Slide (Side-by-Side KPIs)
```python
def _render_comparison_slide(period_a, period_b, kpis_a, kpis_b):
    return f"""
<div class="slide-content">
  <h2>{period_a} vs {period_b}</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px;">
    <div class="period-col">
      <h3>{period_a}</h3>
      <div class="kpi-number">{kpis_a['total_revenue']}</div>
    </div>
    <div class="period-col">
      <h3>{period_b}</h3>
      <div class="kpi-number">{kpis_b['total_revenue']}</div>
    </div>
  </div>
</div>"""
```

### Quote/Commentary Slide
```python
def _render_commentary_slide(title, commentary):
    return f"""
<div class="slide-content" style="display: flex; align-items: center; justify-content: center; height: 80%;">
  <div style="text-align: center; max-width: 800px;">
    <h2>{title}</h2>
    <blockquote style="font-size: 1.3em; color: #bbb; font-style: italic; margin-top: 30px;">
      "{commentary}"
    </blockquote>
  </div>
</div>"""
```

---

## Customizing the Theme

### Dark Theme (Default)
The presentation uses a dark gradient background (`#1a1a2e` to `#16213e`) with light text. This is optimized for projector/screen display.

### Light Theme
Override in `_presentation_css()`:
```css
body { background: #ffffff; color: #333; }
.slide { background: white; }
h2 { color: #2c3e50; }
.kpi-number { color: #2c3e50; }
.pres-table th { background: #3498db; }
```

### Brand Colors
Replace the color constants at the top of the CSS:
```css
/* Primary: #3498db → your brand blue */
/* Accent: #9b59b6 → your brand purple */
/* Favorable: #27ae60 → your success green */
/* Unfavorable: #e74c3c → your alert red */
```

---

## Printing to PDF

The presentation includes `@media print` rules:
- All slides display as block elements (one per page)
- `page-break-after: always` between slides
- Navigation controls hidden
- Background colors adjusted for print

**To generate PDF:**
1. Open HTML file in Chrome
2. Ctrl+P / Cmd+P
3. Select "Save as PDF"
4. Layout: Landscape recommended

---

## File Reference

| File | Purpose |
|------|---------|
| `scripts/integrations/html_presentation.py` | Main presentation generator |
| `scripts/core/metrics.py:build_kpi_scorecard` | KPI data for summary slides |
| `scripts/core/materiality.py:rank_by_impact` | Top variances for waterfall |
| `scripts/core/variance.py:calculate_department_subtotals` | Department data |
