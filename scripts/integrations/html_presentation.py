"""HTML slide-deck presentation generation.

Generates self-contained HTML presentations with keyboard navigation,
Chart.js charts, and executive-friendly formatting.
"""

import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from scripts.core.materiality import count_material_by_favorability, filter_material_variances, rank_by_impact
from scripts.core.metrics import build_kpi_scorecard
from scripts.core.variance import calculate_category_subtotals, calculate_department_subtotals
from scripts.utils.logger import log_audit
from scripts.utils.types import VarianceResult

CHARTJS_CDN = "https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"


def generate_presentation(
    results: list[VarianceResult],
    output_path: str,
    metadata: dict[str, Any],
) -> str:
    """Generate an HTML slide-deck presentation."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    slides = [
        _render_title_slide(metadata),
        _render_executive_summary_slide(results),
        _render_waterfall_slide(results),
    ]

    # Department slides
    departments = sorted(set(r.department for r in results))
    for dept in departments:
        dept_results = [r for r in results if r.department == dept]
        slides.append(_render_department_slide(dept, dept_results))

    slides.append(_render_material_variances_slide(results))
    slides.append(_render_kpi_scorecard_slide(results))
    slides.append(_render_appendix_slide(metadata))

    chart_data = _prepare_presentation_chart_data(results)
    html = _generate_presentation_html(slides, chart_data, metadata)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    log_audit("generate_presentation", [output_path], {
        "slides": len(slides), "accounts": len(results),
    })
    return output_path


def _generate_presentation_html(
    slides: list[str], chart_data: dict, metadata: dict
) -> str:
    """Wrap slides in presentation HTML."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    slides_html = "\n".join(
        f'<section class="slide" id="slide-{i}">{s}</section>'
        for i, s in enumerate(slides)
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc(metadata.get('title', 'Variance Analysis'))}</title>
<style>{_presentation_css()}</style>
<script src="{CHARTJS_CDN}"></script>
</head>
<body>
<div class="presentation">
  {slides_html}
</div>
<div class="slide-controls">
  <button onclick="prevSlide()" class="nav-btn">&larr;</button>
  <span class="slide-counter" id="slideCounter">1 / {len(slides)}</span>
  <button onclick="nextSlide()" class="nav-btn">&rarr;</button>
</div>
<script>
const chartData = {json.dumps(chart_data, default=str)};
{_presentation_js(len(slides))}
</script>
</body>
</html>"""


def _render_title_slide(metadata: dict) -> str:
    now = datetime.now(timezone.utc).strftime("%B %d, %Y")
    period = metadata.get("period", "")
    return f"""
<div class="slide-content title-slide">
  <h1>Variance Analysis Report</h1>
  <h2>{_esc(period)}</h2>
  <div class="title-meta">
    <p>{now}</p>
    <p class="subtitle">Financial Planning &amp; Analysis</p>
  </div>
</div>"""


def _render_executive_summary_slide(results: list[VarianceResult]) -> str:
    kpis = build_kpi_scorecard(results)
    mat_counts = count_material_by_favorability(results)

    return f"""
<div class="slide-content">
  <h2>Executive Summary</h2>
  <div class="kpi-grid">
    <div class="kpi-box">
      <div class="kpi-number">{_fmt_currency(kpis['total_revenue_actual'])}</div>
      <div class="kpi-title">Revenue (Actual)</div>
      <div class="kpi-sub">Budget: {_fmt_currency(kpis['total_revenue_budget'])}</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-number">{_fmt_pct(kpis.get('gross_margin_pct'))}</div>
      <div class="kpi-title">Gross Margin</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-number">{_fmt_currency(kpis['revenue_variance'])}</div>
      <div class="kpi-title">Revenue Variance</div>
    </div>
    <div class="kpi-box alert">
      <div class="kpi-number">{mat_counts['total']}</div>
      <div class="kpi-title">Material Variances</div>
      <div class="kpi-sub">{mat_counts['favorable']} favorable / {mat_counts['unfavorable']} unfavorable</div>
    </div>
  </div>
</div>"""


def _render_waterfall_slide(results: list[VarianceResult]) -> str:
    return """
<div class="slide-content">
  <h2>Top Variance Drivers</h2>
  <div class="chart-full">
    <canvas id="presWaterfallChart" height="400"></canvas>
  </div>
</div>"""


def _render_department_slide(dept: str, dept_results: list[VarianceResult]) -> str:
    total_budget = sum(r.budget for r in dept_results)
    total_actual = sum(r.actual for r in dept_results)
    total_variance = total_actual - total_budget
    material = [r for r in dept_results if r.is_material]
    ranked = rank_by_impact(material)[:5]

    rows = ""
    for r in ranked:
        var_class = "favorable" if r.favorability == "favorable" else "unfavorable"
        rows += f"""
    <tr>
      <td>{_esc(r.account_name)}</td>
      <td>{_fmt_currency(r.budget)}</td>
      <td>{_fmt_currency(r.actual)}</td>
      <td class="{var_class}">{_fmt_currency(r.variance_amount)}</td>
      <td>{_fmt_pct(r.variance_pct)}</td>
    </tr>"""

    return f"""
<div class="slide-content">
  <h2>{_esc(dept)}</h2>
  <div class="dept-overview">
    <div class="dept-stat"><span class="label">Budget</span><span class="value">{_fmt_currency(total_budget)}</span></div>
    <div class="dept-stat"><span class="label">Actual</span><span class="value">{_fmt_currency(total_actual)}</span></div>
    <div class="dept-stat"><span class="label">Variance</span><span class="value {'favorable' if total_variance <= Decimal('0') else 'unfavorable'}">{_fmt_currency(total_variance)}</span></div>
    <div class="dept-stat"><span class="label">Material Items</span><span class="value">{len(material)}</span></div>
  </div>
  {'<h3>Top Material Variances</h3><table class="pres-table"><thead><tr><th>Account</th><th>Budget</th><th>Actual</th><th>Variance</th><th>%</th></tr></thead><tbody>' + rows + '</tbody></table>' if rows else '<p class="no-items">No material variances in this department.</p>'}
</div>"""


def _render_material_variances_slide(results: list[VarianceResult]) -> str:
    material = rank_by_impact(filter_material_variances(results))[:10]
    rows = ""
    for r in material:
        var_class = "favorable" if r.favorability == "favorable" else "unfavorable"
        rows += f"""
    <tr>
      <td>{_esc(r.account_name)}</td>
      <td>{_esc(r.department)}</td>
      <td class="{var_class}">{_fmt_currency(r.variance_amount)}</td>
      <td>{_fmt_pct(r.variance_pct)}</td>
      <td><span class="badge {r.favorability}">{r.favorability.title()}</span></td>
    </tr>"""

    return f"""
<div class="slide-content">
  <h2>Material Variances (Top 10)</h2>
  <table class="pres-table">
    <thead><tr><th>Account</th><th>Department</th><th>Variance</th><th>%</th><th>Status</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>"""


def _render_kpi_scorecard_slide(results: list[VarianceResult]) -> str:
    kpis = build_kpi_scorecard(results)
    return f"""
<div class="slide-content">
  <h2>KPI Scorecard</h2>
  <div class="scorecard-grid">
    <div class="score-item"><span class="score-label">Total Revenue</span><span class="score-value">{_fmt_currency(kpis['total_revenue_actual'])}</span></div>
    <div class="score-item"><span class="score-label">Gross Margin</span><span class="score-value">{_fmt_pct(kpis.get('gross_margin_pct'))}</span></div>
    <div class="score-item"><span class="score-label">Operating Margin</span><span class="score-value">{_fmt_pct(kpis.get('operating_margin_pct'))}</span></div>
    <div class="score-item"><span class="score-label">Budget Utilization</span><span class="score-value">{_fmt_pct(kpis.get('budget_utilization_pct'))}</span></div>
    <div class="score-item"><span class="score-label">Total Accounts</span><span class="score-value">{kpis['total_accounts']}</span></div>
    <div class="score-item"><span class="score-label">Material Variances</span><span class="score-value">{kpis['material_variance_count']}</span></div>
    <div class="score-item green"><span class="score-label">Favorable</span><span class="score-value">{kpis['favorable_count']}</span></div>
    <div class="score-item red"><span class="score-label">Unfavorable</span><span class="score-value">{kpis['unfavorable_count']}</span></div>
  </div>
</div>"""


def _render_appendix_slide(metadata: dict) -> str:
    return f"""
<div class="slide-content">
  <h2>Appendix</h2>
  <div class="appendix">
    <h3>Methodology</h3>
    <ul>
      <li>Variance = Actual - Budget</li>
      <li>% Variance = ((Actual - Budget) / Budget) &times; 100</li>
      <li>Materiality: |%| &ge; 10% OR |$| &ge; $50,000</li>
    </ul>
    <h3>Sources</h3>
    <ul>
      <li>Budget: {_esc(metadata.get('budget_file', 'N/A'))}</li>
      <li>Actuals: {_esc(metadata.get('actuals_file', 'N/A'))}</li>
    </ul>
    <h3>Notes</h3>
    <ul>
      <li>All calculations use exact decimal precision</li>
      <li>NULL actuals excluded from analysis</li>
      <li>Zero-budget accounts show N/A for percentage variance</li>
    </ul>
  </div>
</div>"""


def _prepare_presentation_chart_data(results: list[VarianceResult]) -> dict:
    ranked = rank_by_impact(results)[:10]
    return {
        "waterfall": {
            "labels": [r.account_name for r in ranked],
            "values": [float(r.variance_amount) for r in ranked],
            "colors": [
                "#27ae60" if r.favorability == "favorable"
                else "#e74c3c" if r.favorability == "unfavorable"
                else "#95a5a6"
                for r in ranked
            ],
        }
    }


def _presentation_css() -> str:
    return """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #1a1a2e; color: #eee; overflow: hidden; }
.presentation { width: 100vw; height: 100vh; position: relative; }
.slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; padding: 60px 80px; background: linear-gradient(135deg, #1a1a2e, #16213e); overflow-y: auto; }
.slide.active { display: flex; align-items: flex-start; justify-content: center; }
.slide-content { max-width: 1100px; width: 100%; }
.title-slide { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; }
.title-slide h1 { font-size: 3em; margin-bottom: 16px; background: linear-gradient(135deg, #3498db, #9b59b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.title-slide h2 { font-size: 1.5em; color: #bbb; margin-bottom: 30px; }
.title-meta { color: #888; font-size: 1em; }
.subtitle { margin-top: 8px; font-style: italic; }
h2 { font-size: 1.8em; margin-bottom: 24px; color: #3498db; border-bottom: 2px solid #3498db33; padding-bottom: 8px; }
h3 { font-size: 1.1em; color: #bbb; margin: 16px 0 8px; }

/* KPI Grid */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.kpi-box { background: #16213e; border: 1px solid #333; border-radius: 12px; padding: 24px; text-align: center; }
.kpi-box.alert { border-color: #e67e22; }
.kpi-number { font-size: 2em; font-weight: 700; color: #fff; }
.kpi-title { font-size: 0.9em; color: #888; margin-top: 4px; }
.kpi-sub { font-size: 0.8em; color: #666; margin-top: 4px; }

/* Tables */
.pres-table { width: 100%; border-collapse: collapse; margin-top: 16px; }
.pres-table th { background: #2c3e50; color: white; padding: 10px 14px; text-align: left; font-size: 0.9em; }
.pres-table td { padding: 8px 14px; border-bottom: 1px solid #333; font-size: 0.85em; }
.pres-table tr:hover { background: #ffffff08; }
.favorable { color: #27ae60; font-weight: 600; }
.unfavorable { color: #e74c3c; font-weight: 600; }
.badge { padding: 3px 10px; border-radius: 10px; font-size: 0.8em; }
.badge.favorable { background: #27ae6033; color: #27ae60; }
.badge.unfavorable { background: #e74c3c33; color: #e74c3c; }

/* Department */
.dept-overview { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px; }
.dept-stat { background: #16213e; border-radius: 8px; padding: 16px; text-align: center; }
.dept-stat .label { display: block; font-size: 0.8em; color: #888; }
.dept-stat .value { display: block; font-size: 1.4em; font-weight: 600; margin-top: 4px; }
.no-items { color: #888; font-style: italic; text-align: center; padding: 20px; }

/* Scorecard */
.scorecard-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.score-item { background: #16213e; border-radius: 8px; padding: 20px; text-align: center; border: 1px solid #333; }
.score-item.green { border-color: #27ae60; }
.score-item.red { border-color: #e74c3c; }
.score-label { display: block; font-size: 0.85em; color: #888; }
.score-value { display: block; font-size: 1.6em; font-weight: 700; margin-top: 4px; }

/* Chart */
.chart-full { width: 100%; max-height: 450px; }

/* Appendix */
.appendix ul { margin-left: 20px; margin-bottom: 12px; }
.appendix li { margin-bottom: 6px; color: #bbb; font-size: 0.9em; }

/* Navigation */
.slide-controls { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 16px; z-index: 100; background: #16213ecc; padding: 8px 20px; border-radius: 20px; backdrop-filter: blur(10px); }
.nav-btn { background: #3498db; color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 1em; }
.nav-btn:hover { background: #2980b9; }
.slide-counter { color: #888; font-size: 0.9em; min-width: 60px; text-align: center; }

@media print {
  .slide { position: relative; display: block !important; page-break-after: always; background: white !important; color: #333 !important; height: auto; min-height: 100vh; }
  .slide-controls { display: none; }
  body { background: white; }
  h2 { color: #2c3e50; }
  .kpi-number { color: #2c3e50; }
}
"""


def _presentation_js(total_slides: int) -> str:
    return f"""
let currentSlide = 0;
const totalSlides = {total_slides};

function showSlide(n) {{
  const slides = document.querySelectorAll('.slide');
  slides.forEach(s => s.classList.remove('active'));
  currentSlide = ((n % totalSlides) + totalSlides) % totalSlides;
  slides[currentSlide].classList.add('active');
  document.getElementById('slideCounter').textContent = (currentSlide + 1) + ' / ' + totalSlides;
}}

function nextSlide() {{ showSlide(currentSlide + 1); }}
function prevSlide() {{ showSlide(currentSlide - 1); }}

document.addEventListener('keydown', function(e) {{
  if (e.key === 'ArrowRight' || e.key === ' ') {{ e.preventDefault(); nextSlide(); }}
  if (e.key === 'ArrowLeft') {{ e.preventDefault(); prevSlide(); }}
}});

showSlide(0);

// Initialize presentation charts
document.addEventListener('DOMContentLoaded', function() {{
  if (typeof Chart === 'undefined' || typeof chartData === 'undefined') return;
  const wfCanvas = document.getElementById('presWaterfallChart');
  if (wfCanvas && chartData.waterfall) {{
    new Chart(wfCanvas, {{
      type: 'bar',
      data: {{
        labels: chartData.waterfall.labels,
        datasets: [{{
          label: 'Variance ($)',
          data: chartData.waterfall.values,
          backgroundColor: chartData.waterfall.colors,
          borderWidth: 0,
          borderRadius: 4
        }}]
      }},
      options: {{
        responsive: true,
        indexAxis: 'y',
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{
            callbacks: {{
              label: function(ctx) {{ return '$' + ctx.raw.toLocaleString('en-US'); }}
            }}
          }}
        }},
        scales: {{
          x: {{
            grid: {{ color: '#ffffff11' }},
            ticks: {{ color: '#888', callback: function(v) {{ return '$' + (v/1000).toFixed(0) + 'K'; }} }}
          }},
          y: {{
            grid: {{ display: false }},
            ticks: {{ color: '#bbb', font: {{ size: 12 }} }}
          }}
        }}
      }}
    }});
  }}
}});
"""


def _esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _fmt_currency(value: Decimal) -> str:
    if value < 0:
        return f"-${abs(value):,.2f}"
    return f"${value:,.2f}"


def _fmt_pct(value: Any) -> str:
    if value is None:
        return "N/A"
    return f"{value:.2f}%"
