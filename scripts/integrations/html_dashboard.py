"""Role-based HTML dashboard generation with Chart.js.

Generates self-contained HTML files with embedded CSS, JS, and Chart.js
for interactive financial dashboards. Three distinct layouts:
- Analyst: Full detail with sortable/filterable tables
- Senior Analyst: Department summaries, charts, review queue
- Manager: Executive KPIs with traffic lights, material variances only
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
from scripts.utils.types import DashboardConfig, UserRole, VarianceResult


# Chart.js CDN fallback - embedded inline for self-containment
CHARTJS_CDN = "https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"


def generate_dashboard(
    results: list[VarianceResult],
    role: UserRole,
    output_path: str,
    config: DashboardConfig,
) -> str:
    """Generate a role-specific HTML dashboard."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    if role == "analyst":
        body = _render_analyst_view(results, config)
    elif role == "senior_analyst":
        body = _render_senior_analyst_view(results, config)
    else:
        body = _render_manager_view(results, config)

    html = _generate_html_shell(config.title, body, role, config)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    log_audit("generate_dashboard", [output_path], {"role": role, "accounts": len(results)})
    return output_path


def _generate_html_shell(title: str, body: str, role: UserRole, config: DashboardConfig) -> str:
    """Wrap body content in complete HTML document."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc(title)}</title>
<style>{_generate_css(role)}</style>
<script src="{CHARTJS_CDN}"></script>
</head>
<body>
<header class="dashboard-header">
  <div class="header-content">
    <h1>{_esc(title)}</h1>
    <div class="header-meta">
      <span class="role-badge role-{role}">{role.replace('_', ' ').title()}</span>
      <span class="period">{_esc(config.period or '')}</span>
      <span class="timestamp">Generated: {now}</span>
    </div>
  </div>
</header>
<main class="dashboard-main">
{body}
</main>
<script>{_generate_js(role)}</script>
</body>
</html>"""


def _render_analyst_view(results: list[VarianceResult], config: DashboardConfig) -> str:
    """Full detail view for analysts - all accounts with sort/filter."""
    kpis = build_kpi_scorecard(results)
    mat_counts = count_material_by_favorability(results)

    # Quick stats bar
    stats = f"""
<section class="stats-bar">
  <div class="stat-card">
    <div class="stat-value">{len(results)}</div>
    <div class="stat-label">Total Accounts</div>
  </div>
  <div class="stat-card material">
    <div class="stat-value">{mat_counts['total']}</div>
    <div class="stat-label">Material Variances</div>
  </div>
  <div class="stat-card favorable">
    <div class="stat-value">{mat_counts['favorable']}</div>
    <div class="stat-label">Favorable (Material)</div>
  </div>
  <div class="stat-card unfavorable">
    <div class="stat-value">{mat_counts['unfavorable']}</div>
    <div class="stat-label">Unfavorable (Material)</div>
  </div>
</section>"""

    # Filters
    departments = sorted(set(r.department for r in results))
    categories = sorted(set(r.account_type for r in results))
    dept_options = "".join(f'<option value="{_esc(d)}">{_esc(d)}</option>' for d in departments)
    cat_options = "".join(f'<option value="{_esc(c)}">{_esc(c)}</option>' for c in categories)

    filters = f"""
<section class="filters">
  <input type="text" id="searchBox" placeholder="Search accounts..." class="search-input" oninput="filterTable()">
  <select id="deptFilter" onchange="filterTable()">
    <option value="">All Departments</option>
    {dept_options}
  </select>
  <select id="catFilter" onchange="filterTable()">
    <option value="">All Categories</option>
    {cat_options}
  </select>
  <select id="matFilter" onchange="filterTable()">
    <option value="">All Variances</option>
    <option value="material">Material Only</option>
    <option value="immaterial">Immaterial Only</option>
  </select>
  <select id="favFilter" onchange="filterTable()">
    <option value="">All Favorability</option>
    <option value="favorable">Favorable</option>
    <option value="unfavorable">Unfavorable</option>
    <option value="neutral">Neutral</option>
  </select>
</section>"""

    # Main data table
    table = _render_variance_table(results, full_detail=True)

    # Chart section
    chart_data = _prepare_chart_data(results)
    charts = f"""
<section class="charts-section">
  <div class="chart-container">
    <h3>Top 10 Variance Drivers</h3>
    <canvas id="waterfallChart" height="300"></canvas>
  </div>
  <div class="chart-container">
    <h3>Favorable vs Unfavorable by Department</h3>
    <canvas id="deptChart" height="300"></canvas>
  </div>
</section>
<script>
const chartData = {json.dumps(chart_data, default=str)};
</script>"""

    return stats + filters + table + charts


def _render_senior_analyst_view(results: list[VarianceResult], config: DashboardConfig) -> str:
    """Department summary view for senior analysts."""
    kpis = build_kpi_scorecard(results)
    dept_subtotals = calculate_department_subtotals(results)
    cat_subtotals = calculate_category_subtotals(results)
    material = filter_material_variances(results)
    mat_counts = count_material_by_favorability(results)

    # Department summary cards
    dept_cards = ""
    for dept, sub in sorted(dept_subtotals.items()):
        dept_results = [r for r in results if r.department == dept]
        dept_material = [r for r in dept_results if r.is_material]
        variance_class = "positive" if sub.variance_amount >= Decimal("0") else "negative"
        dept_cards += f"""
    <div class="dept-card">
      <h3>{_esc(dept)}</h3>
      <div class="dept-metrics">
        <div class="metric"><span class="label">Budget</span><span class="value">{_fmt_currency(sub.budget)}</span></div>
        <div class="metric"><span class="label">Actual</span><span class="value">{_fmt_currency(sub.actual)}</span></div>
        <div class="metric {variance_class}"><span class="label">Variance</span><span class="value">{_fmt_currency(sub.variance_amount)}</span></div>
        <div class="metric"><span class="label">Material Items</span><span class="value">{len(dept_material)}</span></div>
      </div>
    </div>"""

    dept_section = f"""
<section class="dept-summary">
  <h2>Department Overview</h2>
  <div class="dept-grid">{dept_cards}</div>
</section>"""

    # KPI bar
    kpi_bar = f"""
<section class="kpi-bar">
  <div class="kpi"><span class="kpi-value">{_fmt_currency(kpis['total_revenue_actual'])}</span><span class="kpi-label">Total Revenue</span></div>
  <div class="kpi"><span class="kpi-value">{_fmt_pct(kpis.get('gross_margin_pct'))}</span><span class="kpi-label">Gross Margin</span></div>
  <div class="kpi"><span class="kpi-value">{mat_counts['total']}</span><span class="kpi-label">Material Variances</span></div>
  <div class="kpi"><span class="kpi-value">{len(results)}</span><span class="kpi-label">Total Accounts</span></div>
</section>"""

    # Charts
    chart_data = _prepare_chart_data(results)
    charts = f"""
<section class="charts-section">
  <div class="chart-container">
    <h3>Department Comparison</h3>
    <canvas id="deptCompareChart" height="300"></canvas>
  </div>
  <div class="chart-container">
    <h3>Category Breakdown</h3>
    <canvas id="categoryChart" height="300"></canvas>
  </div>
</section>
<script>
const chartData = {json.dumps(chart_data, default=str)};
</script>"""

    # Review queue - material variances needing attention
    review_table = _render_review_queue(material)

    return kpi_bar + dept_section + charts + review_table


def _render_manager_view(results: list[VarianceResult], config: DashboardConfig) -> str:
    """Executive dashboard for managers - KPIs and material variances only."""
    kpis = build_kpi_scorecard(results)
    mat_counts = count_material_by_favorability(results)
    material = rank_by_impact(filter_material_variances(results))
    dept_subtotals = calculate_department_subtotals(results)

    # Large KPI cards with traffic lights
    revenue_status = _traffic_light(kpis["revenue_variance"], "revenue")
    margin_status = _traffic_light_pct(kpis.get("gross_margin_pct"), Decimal("30"))
    util_status = _traffic_light_pct(kpis.get("budget_utilization_pct"), Decimal("100"), invert=True)

    kpi_cards = f"""
<section class="executive-kpis">
  <div class="kpi-card large">
    <div class="traffic-light {revenue_status}"></div>
    <div class="kpi-value">{_fmt_currency(kpis['total_revenue_actual'])}</div>
    <div class="kpi-label">Revenue (Actual)</div>
    <div class="kpi-detail">Budget: {_fmt_currency(kpis['total_revenue_budget'])} | Var: {_fmt_currency(kpis['revenue_variance'])}</div>
  </div>
  <div class="kpi-card large">
    <div class="traffic-light {margin_status}"></div>
    <div class="kpi-value">{_fmt_pct(kpis.get('gross_margin_pct'))}</div>
    <div class="kpi-label">Gross Margin</div>
  </div>
  <div class="kpi-card large">
    <div class="traffic-light {_traffic_light_count(mat_counts['unfavorable'])}"></div>
    <div class="kpi-value">{mat_counts['total']}</div>
    <div class="kpi-label">Material Variances</div>
    <div class="kpi-detail">{mat_counts['favorable']} favorable, {mat_counts['unfavorable']} unfavorable</div>
  </div>
  <div class="kpi-card large">
    <div class="traffic-light {util_status}"></div>
    <div class="kpi-value">{_fmt_pct(kpis.get('budget_utilization_pct'))}</div>
    <div class="kpi-label">Budget Utilization</div>
  </div>
</section>"""

    # Department scorecard
    dept_rows = ""
    for dept, sub in sorted(dept_subtotals.items()):
        dept_mat = [r for r in results if r.department == dept and r.is_material]
        dept_unfav = [r for r in dept_mat if r.favorability == "unfavorable"]
        status_class = "green" if len(dept_unfav) == 0 else "yellow" if len(dept_unfav) <= 2 else "red"
        pct_str = _fmt_pct(sub.variance_pct)
        dept_rows += f"""
      <tr>
        <td>{_esc(dept)}</td>
        <td>{_fmt_currency(sub.budget)}</td>
        <td>{_fmt_currency(sub.actual)}</td>
        <td class="{_variance_class(sub.variance_amount, sub.account_type)}">{_fmt_currency(sub.variance_amount)}</td>
        <td>{pct_str}</td>
        <td><span class="status-dot {status_class}"></span> {len(dept_mat)} items</td>
      </tr>"""

    dept_scorecard = f"""
<section class="dept-scorecard">
  <h2>Department Scorecard</h2>
  <table class="scorecard-table">
    <thead>
      <tr><th>Department</th><th>Budget</th><th>Actual</th><th>Variance</th><th>%</th><th>Status</th></tr>
    </thead>
    <tbody>{dept_rows}</tbody>
  </table>
</section>"""

    # Material variances table (compact)
    mat_rows = ""
    for r in material[:15]:  # Top 15 for managers
        mat_rows += f"""
      <tr class="{r.favorability}">
        <td>{_esc(r.account_name)}</td>
        <td>{_esc(r.department)}</td>
        <td class="{_variance_class(r.variance_amount, r.account_type)}">{_fmt_currency(r.variance_amount)}</td>
        <td>{_fmt_pct(r.variance_pct)}</td>
        <td><span class="fav-badge {r.favorability}">{r.favorability.title()}</span></td>
      </tr>"""

    mat_table = f"""
<section class="material-section">
  <h2>Material Variances (Top {min(15, len(material))} by Impact)</h2>
  <table class="material-table">
    <thead><tr><th>Account</th><th>Department</th><th>$ Variance</th><th>% Variance</th><th>Status</th></tr></thead>
    <tbody>{mat_rows}</tbody>
  </table>
</section>"""

    # Chart
    chart_data = _prepare_chart_data(results)
    chart = f"""
<section class="charts-section">
  <div class="chart-container full-width">
    <h3>Top Variance Drivers</h3>
    <canvas id="waterfallChart" height="250"></canvas>
  </div>
</section>
<script>
const chartData = {json.dumps(chart_data, default=str)};
</script>"""

    return kpi_cards + dept_scorecard + mat_table + chart


def _render_variance_table(results: list[VarianceResult], full_detail: bool = True) -> str:
    """Render full variance data table."""
    rows = ""
    for r in results:
        var_class = _variance_class(r.variance_amount, r.account_type)
        mat_class = "material-row" if r.is_material else ""
        rows += f"""
      <tr class="{mat_class}" data-dept="{_esc(r.department)}" data-cat="{_esc(r.account_type)}" data-mat="{'material' if r.is_material else 'immaterial'}" data-fav="{r.favorability}">
        <td>{_esc(r.account_code)}</td>
        <td>{_esc(r.account_name)}</td>
        <td>{_esc(r.department)}</td>
        <td>{_esc(r.account_type)}</td>
        <td class="number">{_fmt_currency(r.budget)}</td>
        <td class="number">{_fmt_currency(r.actual)}</td>
        <td class="number {var_class}">{_fmt_currency(r.variance_amount)}</td>
        <td class="number">{_fmt_pct(r.variance_pct)}</td>
        <td><span class="fav-badge {r.favorability}">{r.favorability.title()}</span></td>
        <td>{'Yes' if r.is_material else 'No'}</td>
      </tr>"""

    return f"""
<section class="data-section">
  <h2>Detailed Variance Analysis</h2>
  <table class="data-table" id="varianceTable">
    <thead>
      <tr>
        <th onclick="sortTable(0)">Code &#x25B4;&#x25BE;</th>
        <th onclick="sortTable(1)">Account Name &#x25B4;&#x25BE;</th>
        <th onclick="sortTable(2)">Department &#x25B4;&#x25BE;</th>
        <th onclick="sortTable(3)">Type &#x25B4;&#x25BE;</th>
        <th onclick="sortTable(4)">Budget &#x25B4;&#x25BE;</th>
        <th onclick="sortTable(5)">Actual &#x25B4;&#x25BE;</th>
        <th onclick="sortTable(6)">$ Variance &#x25B4;&#x25BE;</th>
        <th onclick="sortTable(7)">% Variance &#x25B4;&#x25BE;</th>
        <th onclick="sortTable(8)">Favorability &#x25B4;&#x25BE;</th>
        <th onclick="sortTable(9)">Material &#x25B4;&#x25BE;</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</section>"""


def _render_review_queue(material: list[VarianceResult]) -> str:
    """Render material variances as review queue for senior analysts."""
    ranked = rank_by_impact(material)
    rows = ""
    for i, r in enumerate(ranked, 1):
        rows += f"""
      <tr>
        <td>{i}</td>
        <td>{_esc(r.account_code)}</td>
        <td>{_esc(r.account_name)}</td>
        <td>{_esc(r.department)}</td>
        <td class="{_variance_class(r.variance_amount, r.account_type)}">{_fmt_currency(r.variance_amount)}</td>
        <td>{_fmt_pct(r.variance_pct)}</td>
        <td><span class="fav-badge {r.favorability}">{r.favorability.title()}</span></td>
        <td class="status-pending">Needs Review</td>
      </tr>"""

    return f"""
<section class="review-section">
  <h2>Review Queue ({len(ranked)} items)</h2>
  <table class="review-table">
    <thead><tr><th>#</th><th>Code</th><th>Account</th><th>Dept</th><th>$ Variance</th><th>%</th><th>Favorability</th><th>Status</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</section>"""


def _prepare_chart_data(results: list[VarianceResult]) -> dict[str, Any]:
    """Prepare data structures for Chart.js charts."""
    # Top 10 variances for waterfall
    ranked = rank_by_impact(results)[:10]
    waterfall = {
        "labels": [r.account_name for r in ranked],
        "values": [float(r.variance_amount) for r in ranked],
        "colors": [
            "#27ae60" if r.favorability == "favorable" else "#e74c3c" if r.favorability == "unfavorable" else "#95a5a6"
            for r in ranked
        ],
    }

    # Department comparison
    dept_subtotals = calculate_department_subtotals(results)
    dept_compare = {
        "labels": list(dept_subtotals.keys()),
        "budgets": [float(s.budget) for s in dept_subtotals.values()],
        "actuals": [float(s.actual) for s in dept_subtotals.values()],
        "variances": [float(s.variance_amount) for s in dept_subtotals.values()],
    }

    # Category breakdown
    cat_subtotals = calculate_category_subtotals(results)
    category = {
        "labels": list(cat_subtotals.keys()),
        "budgets": [float(s.budget) for s in cat_subtotals.values()],
        "actuals": [float(s.actual) for s in cat_subtotals.values()],
    }

    # Favorability distribution
    mat_counts = count_material_by_favorability(results)

    return {
        "waterfall": waterfall,
        "deptCompare": dept_compare,
        "category": category,
        "materialCounts": mat_counts,
    }


def _generate_css(role: UserRole) -> str:
    """Generate role-appropriate CSS."""
    base = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f6fa; color: #2c3e50; }
.dashboard-header { background: linear-gradient(135deg, #2c3e50, #3498db); color: white; padding: 20px 30px; }
.header-content { max-width: 1400px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }
.header-content h1 { font-size: 1.5em; font-weight: 600; }
.header-meta { display: flex; gap: 15px; align-items: center; font-size: 0.85em; opacity: 0.9; }
.role-badge { padding: 4px 12px; border-radius: 12px; font-weight: 600; font-size: 0.8em; text-transform: uppercase; }
.role-analyst { background: #3498db; }
.role-senior_analyst { background: #9b59b6; }
.role-manager { background: #e67e22; }
.dashboard-main { max-width: 1400px; margin: 20px auto; padding: 0 20px; }
section { margin-bottom: 24px; }
h2 { font-size: 1.2em; margin-bottom: 12px; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 6px; }
h3 { font-size: 1em; margin-bottom: 8px; color: #34495e; }

/* Tables */
table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
th { background: #2c3e50; color: white; padding: 10px 12px; text-align: left; font-size: 0.85em; cursor: pointer; user-select: none; white-space: nowrap; }
td { padding: 8px 12px; border-bottom: 1px solid #ecf0f1; font-size: 0.85em; }
tr:hover { background: #f8f9fa; }
.number { text-align: right; font-variant-numeric: tabular-nums; }
.material-row { font-weight: 500; }

/* Variance colors */
.variance-favorable { color: #27ae60; font-weight: 600; }
.variance-unfavorable { color: #e74c3c; font-weight: 600; }

/* Favorability badges */
.fav-badge { padding: 2px 8px; border-radius: 10px; font-size: 0.8em; font-weight: 600; }
.fav-badge.favorable { background: #d5f5e3; color: #1e8449; }
.fav-badge.unfavorable { background: #fadbd8; color: #c0392b; }
.fav-badge.neutral { background: #eaecee; color: #7f8c8d; }

/* Status */
.status-pending { color: #e67e22; font-weight: 600; }
.status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }
.status-dot.green { background: #27ae60; }
.status-dot.yellow { background: #f1c40f; }
.status-dot.red { background: #e74c3c; }

/* Traffic lights */
.traffic-light { width: 16px; height: 16px; border-radius: 50%; display: inline-block; margin-right: 8px; }
.traffic-light.green { background: #27ae60; box-shadow: 0 0 6px rgba(39,174,96,0.5); }
.traffic-light.yellow { background: #f1c40f; box-shadow: 0 0 6px rgba(241,196,15,0.5); }
.traffic-light.red { background: #e74c3c; box-shadow: 0 0 6px rgba(231,76,60,0.5); }

/* Charts */
.charts-section { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.chart-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.chart-container.full-width { grid-column: 1 / -1; }

/* Print */
@media print {
  .dashboard-header { background: #2c3e50 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .filters { display: none; }
  .charts-section { break-inside: avoid; }
  body { background: white; }
  table { box-shadow: none; }
}

@media (max-width: 768px) {
  .charts-section { grid-template-columns: 1fr; }
  .header-content { flex-direction: column; align-items: flex-start; }
}
"""

    if role == "analyst":
        return base + """
.stats-bar { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px; }
.stat-card { background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.stat-value { font-size: 2em; font-weight: 700; color: #2c3e50; }
.stat-label { font-size: 0.85em; color: #7f8c8d; margin-top: 4px; }
.stat-card.favorable .stat-value { color: #27ae60; }
.stat-card.unfavorable .stat-value { color: #e74c3c; }
.stat-card.material .stat-value { color: #e67e22; }
.filters { display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
.search-input, select { padding: 8px 12px; border: 1px solid #bdc3c7; border-radius: 6px; font-size: 0.85em; }
.search-input { flex: 1; min-width: 200px; }
@media (max-width: 768px) { .stats-bar { grid-template-columns: repeat(2, 1fr); } }
"""
    elif role == "senior_analyst":
        return base + """
.kpi-bar { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.kpi { background: white; padding: 16px; border-radius: 8px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.kpi-value { font-size: 1.4em; font-weight: 700; color: #2c3e50; }
.kpi-label { font-size: 0.8em; color: #7f8c8d; }
.dept-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
.dept-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid #3498db; }
.dept-card h3 { color: #2c3e50; margin-bottom: 12px; }
.dept-metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.metric { display: flex; flex-direction: column; }
.metric .label { font-size: 0.75em; color: #7f8c8d; }
.metric .value { font-size: 1em; font-weight: 600; }
.metric.positive .value { color: #27ae60; }
.metric.negative .value { color: #e74c3c; }
.review-table .status-pending { color: #e67e22; }
"""
    else:  # manager
        return base + """
.executive-kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 28px; }
.kpi-card { background: white; padding: 24px; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.kpi-card.large .kpi-value { font-size: 2.2em; font-weight: 700; color: #2c3e50; }
.kpi-card .kpi-label { font-size: 0.9em; color: #7f8c8d; margin-top: 4px; }
.kpi-card .kpi-detail { font-size: 0.8em; color: #95a5a6; margin-top: 8px; }
.scorecard-table th { background: #34495e; }
.material-table th { background: #8e44ad; }
tr.favorable td:first-child { border-left: 3px solid #27ae60; }
tr.unfavorable td:first-child { border-left: 3px solid #e74c3c; }
@media (max-width: 900px) { .executive-kpis { grid-template-columns: repeat(2, 1fr); } }
"""


def _generate_js(role: UserRole) -> str:
    """Generate client-side JavaScript for interactivity and charts."""
    base = """
// Sort table by column
let sortDir = {};
function sortTable(col) {
  const table = document.getElementById('varianceTable');
  if (!table) return;
  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  sortDir[col] = !sortDir[col];
  rows.sort((a, b) => {
    let aVal = a.cells[col]?.textContent.trim() || '';
    let bVal = b.cells[col]?.textContent.trim() || '';
    // Try numeric sort
    let aNum = parseFloat(aVal.replace(/[$,%]/g, '').replace(/,/g, ''));
    let bNum = parseFloat(bVal.replace(/[$,%]/g, '').replace(/,/g, ''));
    if (!isNaN(aNum) && !isNaN(bNum)) {
      return sortDir[col] ? aNum - bNum : bNum - aNum;
    }
    return sortDir[col] ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
  });
  rows.forEach(r => tbody.appendChild(r));
}

// Filter table (analyst view)
function filterTable() {
  const search = (document.getElementById('searchBox')?.value || '').toLowerCase();
  const dept = document.getElementById('deptFilter')?.value || '';
  const cat = document.getElementById('catFilter')?.value || '';
  const mat = document.getElementById('matFilter')?.value || '';
  const fav = document.getElementById('favFilter')?.value || '';
  const table = document.getElementById('varianceTable');
  if (!table) return;
  const rows = table.querySelectorAll('tbody tr');
  rows.forEach(row => {
    const text = row.textContent.toLowerCase();
    const matchSearch = !search || text.includes(search);
    const matchDept = !dept || row.dataset.dept === dept;
    const matchCat = !cat || row.dataset.cat === cat;
    const matchMat = !mat || row.dataset.mat === mat;
    const matchFav = !fav || row.dataset.fav === fav;
    row.style.display = (matchSearch && matchDept && matchCat && matchMat && matchFav) ? '' : 'none';
  });
}
"""

    chart_init = """
// Initialize Chart.js charts
document.addEventListener('DOMContentLoaded', function() {
  if (typeof Chart === 'undefined' || typeof chartData === 'undefined') return;

  // Waterfall chart (top variances)
  const wfCanvas = document.getElementById('waterfallChart');
  if (wfCanvas && chartData.waterfall) {
    new Chart(wfCanvas, {
      type: 'bar',
      data: {
        labels: chartData.waterfall.labels,
        datasets: [{
          label: 'Variance ($)',
          data: chartData.waterfall.values,
          backgroundColor: chartData.waterfall.colors,
          borderColor: chartData.waterfall.colors.map(c => c),
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        indexAxis: 'y',
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function(ctx) {
                return '$' + ctx.raw.toLocaleString('en-US', {minimumFractionDigits: 0});
              }
            }
          }
        },
        scales: {
          x: {
            ticks: {
              callback: function(v) { return '$' + (v/1000).toFixed(0) + 'K'; }
            }
          }
        }
      }
    });
  }

  // Department comparison chart
  const dcCanvas = document.getElementById('deptCompareChart') || document.getElementById('deptChart');
  if (dcCanvas && chartData.deptCompare) {
    new Chart(dcCanvas, {
      type: 'bar',
      data: {
        labels: chartData.deptCompare.labels,
        datasets: [
          { label: 'Budget', data: chartData.deptCompare.budgets, backgroundColor: '#3498db88' },
          { label: 'Actual', data: chartData.deptCompare.actuals, backgroundColor: '#2c3e5088' }
        ]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'top' } },
        scales: {
          y: {
            ticks: { callback: function(v) { return '$' + (v/1000).toFixed(0) + 'K'; } }
          }
        }
      }
    });
  }

  // Category chart
  const catCanvas = document.getElementById('categoryChart');
  if (catCanvas && chartData.category) {
    new Chart(catCanvas, {
      type: 'doughnut',
      data: {
        labels: chartData.category.labels,
        datasets: [{
          data: chartData.category.actuals,
          backgroundColor: ['#27ae60', '#e74c3c', '#3498db', '#f1c40f', '#9b59b6']
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'right' },
          tooltip: {
            callbacks: {
              label: function(ctx) {
                return ctx.label + ': $' + ctx.raw.toLocaleString('en-US', {minimumFractionDigits: 0});
              }
            }
          }
        }
      }
    });
  }
});
"""
    return base + chart_init


# --- Formatting helpers ---

def _esc(text: str) -> str:
    """HTML-escape text."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _fmt_currency(value: Decimal) -> str:
    """Format Decimal as currency string."""
    if value < 0:
        return f"-${abs(value):,.2f}"
    return f"${value:,.2f}"


def _fmt_pct(value: Any) -> str:
    """Format percentage or return N/A."""
    if value is None:
        return "N/A"
    return f"{value:.2f}%"


def _variance_class(amount: Decimal, account_type: str) -> str:
    """CSS class for variance coloring based on favorability."""
    if amount == Decimal("0"):
        return ""
    if account_type in ("revenue", "asset"):
        return "variance-favorable" if amount > 0 else "variance-unfavorable"
    else:
        return "variance-favorable" if amount < 0 else "variance-unfavorable"


def _traffic_light(value: Decimal, context: str) -> str:
    """Determine traffic light color."""
    if context == "revenue":
        if value > Decimal("0"):
            return "green"
        elif value >= Decimal("-50000"):
            return "yellow"
        return "red"
    return "yellow"


def _traffic_light_pct(value: Any, threshold: Decimal, invert: bool = False) -> str:
    """Traffic light based on percentage vs threshold."""
    if value is None:
        return "yellow"
    val = Decimal(str(value))
    if invert:
        if val <= threshold:
            return "green"
        elif val <= threshold + Decimal("10"):
            return "yellow"
        return "red"
    else:
        if val >= threshold:
            return "green"
        elif val >= threshold - Decimal("10"):
            return "yellow"
        return "red"


def _traffic_light_count(count: int) -> str:
    """Traffic light based on unfavorable count."""
    if count == 0:
        return "green"
    elif count <= 3:
        return "yellow"
    return "red"
