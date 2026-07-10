#!/usr/bin/env python3
"""
wellspring_geo_analysis.py
Pulls zipcode-level performance data from Google Ads API and generates
an HTML analysis report saved to 01_Reports/.

Run with:
  python wellspring_geo_analysis.py
  # Optional: add --days 60 for a longer date range
"""

import os
import sys
import csv
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# ── Credentials ──────────────────────────────────────────────────────────────
# Loaded from environment variables — never hardcode these.
# Set GOOGLE_ADS_DEVELOPER_TOKEN, GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET,
# GOOGLE_ADS_REFRESH_TOKEN before running (e.g. in a local .env file, gitignored).
CREDENTIALS = {
    "developer_token":   os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
    "client_id":         os.environ["GOOGLE_ADS_CLIENT_ID"],
    "client_secret":     os.environ["GOOGLE_ADS_CLIENT_SECRET"],
    "refresh_token":     os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
    "use_proto_plus":    True,
}
CUSTOMER_ID = "5093164652"

BASE_DIR    = Path(__file__).parent
REPORTS_DIR = BASE_DIR / "01_Reports"
DATA_DIR    = BASE_DIR / "04_Data"

# ── Nearby zip codes for Wellspring locations ─────────────────────────────────
TROY_ZIPS    = {"48083", "48084", "48085", "48098", "48007", "48099"}
CLINTON_ZIPS = {"48035", "48036", "48038", "48044", "48045"}
KNOWN_ZIPS   = TROY_ZIPS | CLINTON_ZIPS


# ── Data fetch ────────────────────────────────────────────────────────────────
def fetch_geo_rows(client, customer_id: str, start_date, end_date) -> list[dict]:
    """
    Two-step fetch:
      1. geographic_view  → criterion IDs + metrics
      2. geo_target_constant → names / types for those IDs
    (geo_target_constant cannot be joined directly from geographic_view in API v24)
    """
    ga = client.get_service("GoogleAdsService")

    # ── Step 1: get criterion IDs and metrics ─────────────────────────────────
    q1 = f"""
        SELECT
            geographic_view.country_criterion_id,
            geographic_view.location_type,
            metrics.clicks,
            metrics.impressions,
            metrics.cost_micros,
            metrics.conversions,
            metrics.average_cpc,
            metrics.ctr
        FROM geographic_view
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
            AND metrics.clicks > 0
        ORDER BY metrics.clicks DESC
        LIMIT 2000
    """
    geo_data: dict = {}
    try:
        for batch in ga.search_stream(customer_id=customer_id, query=q1):
            for row in batch.results:
                cid = row.geographic_view.country_criterion_id
                lt  = row.geographic_view.location_type.name
                m   = row.metrics
                geo_data[(cid, lt)] = {
                    "clicks":      int(m.clicks),
                    "impressions": int(m.impressions),
                    "cost":        round(m.cost_micros / 1_000_000, 2),
                    "conversions": round(float(m.conversions), 2),
                    "avg_cpc":     round(m.average_cpc / 1_000_000, 2),
                    "ctr":         round(m.ctr * 100, 2),
                }
    except Exception as exc:
        print(f"  ERROR in step 1 (geographic_view): {exc}")
        raise

    if not geo_data:
        return []

    print(f"  Step 1 complete: {len(geo_data)} (criterion, location_type) pairs")

    # ── Step 2: look up names for unique criterion IDs ────────────────────────
    unique_ids = list({k[0] for k in geo_data})
    id_map: dict = {}
    chunk_size = 100

    for i in range(0, len(unique_ids), chunk_size):
        chunk = unique_ids[i : i + chunk_size]
        ids_str = ", ".join(str(x) for x in chunk)
        q2 = f"""
            SELECT
                geo_target_constant.id,
                geo_target_constant.name,
                geo_target_constant.target_type,
                geo_target_constant.country_code
            FROM geo_target_constant
            WHERE geo_target_constant.id IN ({ids_str})
        """
        try:
            for row in ga.search(customer_id=customer_id, query=q2):
                gtc = row.geo_target_constant
                id_map[gtc.id] = {
                    "name":         gtc.name,
                    "target_type":  str(gtc.target_type),
                    "country_code": gtc.country_code,
                }
        except Exception as exc:
            print(f"  WARNING in step 2 (geo_target_constant chunk {i}): {exc}")

    print(f"  Step 2 complete: resolved {len(id_map)} of {len(unique_ids)} criterion IDs")

    # ── Step 3: join ──────────────────────────────────────────────────────────
    rows = []
    for (cid, lt), metrics in geo_data.items():
        info = id_map.get(cid, {})
        rows.append({
            "zipcode":       info.get("name", f"ID:{cid}"),
            "country_code":  info.get("country_code", ""),
            "target_type":   info.get("target_type", ""),
            "location_type": lt,
            **metrics,
        })
    return rows


def process_rows(raw: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split into USER_LOCATION and AREA_OF_INTEREST postal-code rows, add CPL."""
    postal = [r for r in raw if "Postal Code" in r["target_type"]]

    def add_cpl(rows):
        for r in rows:
            r["cpl"] = round(r["cost"] / r["conversions"], 2) if r["conversions"] > 0 else None
            r["near_office"] = r["zipcode"] in KNOWN_ZIPS
        return sorted(rows, key=lambda x: x["clicks"], reverse=True)

    user_loc = add_cpl([r for r in postal if r["location_type"] == "USER_LOCATION"])
    aoi      = add_cpl([r for r in postal if r["location_type"] == "AREA_OF_INTEREST"])
    return user_loc, aoi


def summarize(rows: list[dict]) -> dict:
    if not rows:
        return dict(clicks=0, impressions=0, cost=0, conversions=0, cpl=0, ctr=0, zip_count=0)
    total_clicks   = sum(r["clicks"] for r in rows)
    total_impr     = sum(r["impressions"] for r in rows)
    total_cost     = round(sum(r["cost"] for r in rows), 2)
    total_conv     = round(sum(r["conversions"] for r in rows), 1)
    return {
        "clicks":      total_clicks,
        "impressions": total_impr,
        "cost":        total_cost,
        "conversions": total_conv,
        "cpl":         round(total_cost / total_conv, 2) if total_conv > 0 else 0,
        "ctr":         round(total_clicks / total_impr * 100, 2) if total_impr > 0 else 0,
        "zip_count":   len(rows),
    }


# ── CSV export ────────────────────────────────────────────────────────────────
def save_csv(rows: list[dict], path: Path):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


# ── HTML report ───────────────────────────────────────────────────────────────
def _kpi_card(label: str, value: str, note: str = "") -> str:
    return f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {f'<div class="kpi-note">{note}</div>' if note else ""}
        </div>"""


def _table_rows(rows: list[dict]) -> str:
    html = ""
    for i, r in enumerate(rows):
        cpl_str  = f"${r['cpl']:.2f}"  if r["cpl"]  else "—"
        conv_str = f"{r['conversions']:.0f}" if r["conversions"] > 0 else "0"
        badge    = ' <span class="office-badge">near office</span>' if r["near_office"] else ""
        html += f"""
            <tr>
                <td class="rank">{i + 1}</td>
                <td class="zip">{r["zipcode"]}{badge}</td>
                <td>{r["clicks"]:,}</td>
                <td>{r["impressions"]:,}</td>
                <td>{r["ctr"]:.2f}%</td>
                <td>${r["avg_cpc"]:.2f}</td>
                <td>${r["cost"]:.2f}</td>
                <td>{conv_str}</td>
                <td class="cpl">{cpl_str}</td>
            </tr>"""
    return html


def _auto_insights(user_rows: list[dict], s: dict) -> str:
    cards = []

    # Best converting zip (min CPL, ≥2 conversions)
    converters = [r for r in user_rows if r["conversions"] >= 2 and r["cpl"]]
    if converters:
        best = min(converters, key=lambda x: x["cpl"])
        cards.append(("chart-line", "Best CPL Zipcode",
                       f"<strong>{best['zipcode']}</strong> delivers the lowest cost-per-lead at "
                       f"<strong>${best['cpl']:.2f}</strong> with {int(best['conversions'])} conversions. "
                       f"Consider increasing bids or adding it as a location bid modifier."))

    # High spend / zero conversions
    waste = [r for r in user_rows if r["conversions"] == 0 and r["cost"] > 20]
    if waste:
        waste.sort(key=lambda x: x["cost"], reverse=True)
        names = ", ".join(r["zipcode"] for r in waste[:3])
        total_waste = round(sum(r["cost"] for r in waste), 2)
        cards.append(("exclamation-triangle", "Zero-Conversion Zips",
                       f"<strong>{len(waste)} zipcodes</strong> ({names}{', …' if len(waste) > 3 else ''}) "
                       f"spent <strong>${total_waste:.2f}</strong> with 0 conversions. "
                       f"Review and consider excluding or reducing bids for these areas."))

    # Near-office coverage
    near = [r for r in user_rows if r["near_office"]]
    if near:
        near_clicks = sum(r["clicks"] for r in near)
        near_pct    = round(near_clicks / s["clicks"] * 100, 1) if s["clicks"] else 0
        cards.append(("map-marker", "Office Coverage",
                       f"Zipcodes near Troy and Clinton Township account for "
                       f"<strong>{near_pct}% of clicks</strong> ({near_clicks:,} clicks across "
                       f"{len(near)} proximate zipcodes)."))

    if not cards:
        cards.append(("info-circle", "Data Looks Clean",
                       "No major anomalies detected. All active zipcodes have reasonable spend distribution."))

    icons = {"chart-line": "📈", "exclamation-triangle": "⚠️",
             "map-marker": "📍", "info-circle": "ℹ️"}

    html = ""
    for icon_key, title, body in cards:
        html += f"""
            <div class="insight-card">
                <div class="insight-icon">{icons.get(icon_key, "•")}</div>
                <div>
                    <div class="insight-title">{title}</div>
                    <div class="insight-body">{body}</div>
                </div>
            </div>"""
    return html


def generate_html(user_rows: list[dict], aoi_rows: list[dict],
                  start_date, end_date, generated_at: str) -> str:
    s = summarize(user_rows)
    top10 = user_rows[:10]

    chart_labels    = str([r["zipcode"]      for r in top10]).replace("'", '"')
    chart_clicks    = str([r["clicks"]       for r in top10])
    chart_conv      = str([r["conversions"]  for r in top10])

    date_range_str  = f"{start_date.strftime('%d %b %Y')} – {end_date.strftime('%d %b %Y')}"
    kpis            = (
        _kpi_card("Zipcodes Active",     f"{s['zip_count']}",              "user location") +
        _kpi_card("Total Clicks",        f"{s['clicks']:,}",               "") +
        _kpi_card("Total Conversions",   f"{s['conversions']:.0f}",        "") +
        _kpi_card("Total Spend",         f"${s['cost']:,.2f}",             "") +
        _kpi_card("Avg CPL",             f"${s['cpl']:.2f}" if s["cpl"] else "—", "conv ≥ 1") +
        _kpi_card("Overall CTR",         f"{s['ctr']:.2f}%",              "")
    )
    table_html      = _table_rows(user_rows)
    aoi_table_html  = _table_rows(aoi_rows[:30]) if aoi_rows else "<tr><td colspan='9'>No data</td></tr>"
    insights_html   = _auto_insights(user_rows, s)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Wellspring — Zipcode Analysis {date_range_str}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>
    :root {{
      --teal:      #1a3a3a;
      --teal-mid:  #254f4f;
      --teal-lite: #2d6060;
      --gold:      #c9a84c;
      --gold-lite: #e8c97a;
      --cream:     #f5f0e8;
      --cream2:    #ede6d8;
      --white:     #ffffff;
      --red:       #d64c4c;
      --green:     #2e8b57;
      --text:      #1a1a1a;
      --muted:     #5a6370;
      --border:    #d5cfc4;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'DM Sans', sans-serif;
      background: var(--cream);
      color: var(--text);
      font-size: 14px;
    }}

    /* ── Header ── */
    .report-header {{
      background: var(--teal);
      color: var(--cream);
      padding: 40px 48px 32px;
    }}
    .header-eyebrow {{
      font-family: 'DM Sans', sans-serif;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 10px;
    }}
    .header-title {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 36px;
      font-weight: 600;
      color: var(--cream);
      line-height: 1.2;
    }}
    .header-subtitle {{
      margin-top: 8px;
      font-size: 13px;
      color: rgba(245,240,232,0.65);
    }}
    .header-meta {{
      display: flex;
      gap: 24px;
      margin-top: 20px;
    }}
    .header-meta-item {{
      font-size: 12px;
      color: rgba(245,240,232,0.7);
    }}
    .header-meta-item strong {{
      color: var(--gold-lite);
      font-weight: 500;
    }}

    /* ── Layout ── */
    .report-body {{ padding: 36px 48px; max-width: 1400px; margin: 0 auto; }}
    .section-divider {{
      display: flex;
      align-items: center;
      gap: 16px;
      margin: 40px 0 24px;
    }}
    .section-divider-line {{ flex: 1; height: 1px; background: var(--border); }}
    .section-divider-label {{
      font-family: 'DM Sans', sans-serif;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--gold);
      white-space: nowrap;
    }}

    /* ── KPI cards ── */
    .kpi-row {{
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 16px;
      margin-bottom: 32px;
    }}
    .kpi-card {{
      background: var(--white);
      border: 1px solid var(--border);
      border-top: 3px solid var(--gold);
      border-radius: 8px;
      padding: 20px 18px 16px;
    }}
    .kpi-label {{
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 8px;
    }}
    .kpi-value {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 30px;
      font-weight: 700;
      color: var(--teal);
      line-height: 1;
    }}
    .kpi-note {{
      font-size: 11px;
      color: var(--muted);
      margin-top: 6px;
    }}

    /* ── Two-col layout ── */
    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 28px; }}
    .panel {{
      background: var(--white);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }}
    .panel-full {{ grid-column: 1 / -1; }}
    .panel-header {{
      background: var(--teal);
      color: var(--cream);
      padding: 14px 20px;
      font-family: 'Cormorant Garamond', serif;
      font-size: 17px;
      font-weight: 600;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .panel-header small {{ font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 400; opacity: 0.7; }}
    .panel-body {{ padding: 20px; }}

    /* ── Chart ── */
    .chart-container {{ position: relative; height: 320px; }}

    /* ── Table ── */
    .data-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    .data-table thead tr {{
      background: var(--teal);
      color: var(--cream);
    }}
    .data-table thead th {{
      padding: 11px 14px;
      text-align: left;
      font-weight: 500;
      font-size: 11px;
      letter-spacing: 0.5px;
      white-space: nowrap;
    }}
    .data-table thead th.right {{ text-align: right; }}
    .data-table tbody tr {{ border-bottom: 1px solid var(--border); }}
    .data-table tbody tr:hover {{ background: rgba(201,168,76,0.06); }}
    .data-table tbody tr:last-child {{ border-bottom: none; }}
    .data-table td {{ padding: 10px 14px; }}
    .data-table td.rank {{ color: var(--muted); font-size: 12px; width: 36px; }}
    .data-table td.zip {{ font-weight: 600; color: var(--teal); }}
    .data-table td.cpl {{ font-weight: 600; color: var(--teal-mid); }}
    .data-table td:not(.rank):not(.zip) {{ text-align: right; color: var(--muted); }}
    .data-table td.cpl {{ text-align: right; }}

    /* ── Near-office badge ── */
    .office-badge {{
      display: inline-block;
      background: var(--gold);
      color: var(--teal);
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      padding: 1px 6px;
      border-radius: 3px;
      margin-left: 6px;
      vertical-align: middle;
    }}

    /* ── Insights ── */
    .insights-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
      padding: 20px;
    }}
    .insight-card {{
      display: flex;
      gap: 14px;
      align-items: flex-start;
      background: var(--cream);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
    }}
    .insight-icon {{ font-size: 22px; flex-shrink: 0; margin-top: 2px; }}
    .insight-title {{ font-weight: 600; color: var(--teal); margin-bottom: 5px; font-size: 13px; }}
    .insight-body {{ font-size: 12.5px; color: var(--muted); line-height: 1.55; }}
    .insight-body strong {{ color: var(--text); }}

    /* ── Footer ── */
    .report-footer {{
      background: var(--teal);
      color: rgba(245,240,232,0.5);
      text-align: center;
      padding: 20px;
      font-size: 11px;
      margin-top: 48px;
    }}

    /* ── Responsive ── */
    @media (max-width: 900px) {{
      .kpi-row {{ grid-template-columns: repeat(3, 1fr); }}
      .two-col {{ grid-template-columns: 1fr; }}
      .report-body {{ padding: 20px 16px; }}
    }}
    @media (max-width: 600px) {{
      .kpi-row {{ grid-template-columns: repeat(2, 1fr); }}
    }}
  </style>
</head>
<body>

<!-- ── HEADER ── -->
<div class="report-header">
  <div class="header-eyebrow">Wellspring Therapeutic Partners · Paid Ads</div>
  <div class="header-title">Zipcode Performance Analysis</div>
  <div class="header-subtitle">Google Ads — Geographic Breakdown by Postal Code</div>
  <div class="header-meta">
    <div class="header-meta-item">Date Range: <strong>{date_range_str}</strong></div>
    <div class="header-meta-item">Account: <strong>Wellspring (5093164652)</strong></div>
    <div class="header-meta-item">Generated: <strong>{generated_at}</strong></div>
    <div class="header-meta-item">Primary view: <strong>User Location</strong></div>
  </div>
</div>

<!-- ── REPORT BODY ── -->
<div class="report-body">

  <!-- KPI cards -->
  <div class="section-divider">
    <div class="section-divider-line"></div>
    <div class="section-divider-label">Section 1 — Summary (User Location)</div>
    <div class="section-divider-line"></div>
  </div>
  <div class="kpi-row">
    {kpis}
  </div>

  <!-- Chart + Top 10 table -->
  <div class="section-divider">
    <div class="section-divider-line"></div>
    <div class="section-divider-label">Section 2 — Top Zipcodes</div>
    <div class="section-divider-line"></div>
  </div>
  <div class="two-col">
    <div class="panel">
      <div class="panel-header">
        Top 10 Zipcodes — Clicks &amp; Conversions
        <small>User Location · sorted by clicks</small>
      </div>
      <div class="panel-body">
        <div class="chart-container">
          <canvas id="zipChart"></canvas>
        </div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-header">
        Top 10 Zipcodes
        <small>Clicks · Conversions · CPL</small>
      </div>
      <div class="panel-body" style="padding:0;">
        <table class="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Zipcode</th>
              <th class="right">Clicks</th>
              <th class="right">Conv.</th>
              <th class="right">Spend</th>
              <th class="right">CPL</th>
            </tr>
          </thead>
          <tbody>
            {''.join(_top10_mini_rows(top10))}
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Full data table -->
  <div class="section-divider">
    <div class="section-divider-line"></div>
    <div class="section-divider-label">Section 3 — Full Zipcode Table</div>
    <div class="section-divider-line"></div>
  </div>
  <div class="panel panel-full">
    <div class="panel-header">
      All Zipcodes — User Location
      <small>sorted by clicks desc · Gold badge = near Troy or Clinton Township office</small>
    </div>
    <div style="overflow-x:auto;">
      <table class="data-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Zipcode</th>
            <th class="right">Clicks</th>
            <th class="right">Impressions</th>
            <th class="right">CTR</th>
            <th class="right">Avg CPC</th>
            <th class="right">Spend</th>
            <th class="right">Conversions</th>
            <th class="right">CPL</th>
          </tr>
        </thead>
        <tbody>
          {table_html}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Area of interest table -->
  <div class="section-divider">
    <div class="section-divider-line"></div>
    <div class="section-divider-label">Section 4 — Area of Interest (Search Intent)</div>
    <div class="section-divider-line"></div>
  </div>
  <div class="panel panel-full">
    <div class="panel-header">
      Area of Interest — Top 30 Zipcodes
      <small>Where users searched FROM regardless of physical location</small>
    </div>
    <div style="overflow-x:auto;">
      <table class="data-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Zipcode</th>
            <th class="right">Clicks</th>
            <th class="right">Impressions</th>
            <th class="right">CTR</th>
            <th class="right">Avg CPC</th>
            <th class="right">Spend</th>
            <th class="right">Conversions</th>
            <th class="right">CPL</th>
          </tr>
        </thead>
        <tbody>
          {aoi_table_html}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Key insights -->
  <div class="section-divider">
    <div class="section-divider-line"></div>
    <div class="section-divider-label">Section 5 — Key Observations</div>
    <div class="section-divider-line"></div>
  </div>
  <div class="panel panel-full">
    <div class="panel-header">Key Observations</div>
    <div class="insights-grid">
      {insights_html}
    </div>
  </div>

</div><!-- /report-body -->

<!-- ── FOOTER ── -->
<div class="report-footer">
  Wellspring Therapeutic Partners · Confidential · Prepared by Damco Digital · {generated_at}
</div>

<script>
// ── Bar chart ─────────────────────────────────────────────────────────────────
const ctx = document.getElementById('zipChart').getContext('2d');
new Chart(ctx, {{
  type: 'bar',
  data: {{
    labels: {chart_labels},
    datasets: [
      {{
        label: 'Clicks',
        data: {chart_clicks},
        backgroundColor: 'rgba(26,58,58,0.8)',
        borderColor: '#1a3a3a',
        borderWidth: 1,
        borderRadius: 3,
      }},
      {{
        label: 'Conversions',
        data: {chart_conv},
        backgroundColor: 'rgba(201,168,76,0.85)',
        borderColor: '#c9a84c',
        borderWidth: 1,
        borderRadius: 3,
        yAxisID: 'y2',
      }}
    ]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    interaction: {{ mode: 'index', intersect: false }},
    plugins: {{
      legend: {{ position: 'bottom', labels: {{ font: {{ family: 'DM Sans', size: 12 }}, padding: 16 }} }},
      tooltip: {{
        callbacks: {{
          label: ctx => {{
            const v = ctx.parsed.y;
            return ` ${{ctx.dataset.label}}: ${{v % 1 === 0 ? v : v.toFixed(1)}}`;
          }}
        }}
      }}
    }},
    scales: {{
      x: {{ ticks: {{ font: {{ family: 'DM Sans', size: 11 }} }}, grid: {{ display: false }} }},
      y: {{
        title: {{ display: true, text: 'Clicks', font: {{ family: 'DM Sans', size: 11 }} }},
        ticks: {{ font: {{ family: 'DM Sans', size: 11 }} }}
      }},
      y2: {{
        position: 'right',
        title: {{ display: true, text: 'Conversions', font: {{ family: 'DM Sans', size: 11 }} }},
        ticks: {{ font: {{ family: 'DM Sans', size: 11 }} }},
        grid: {{ drawOnChartArea: false }},
      }}
    }}
  }}
}});

// ── Sortable table (click header to sort) ────────────────────────────────────
document.querySelectorAll('.data-table thead th').forEach((th, colIdx) => {{
  th.style.cursor = 'pointer';
  th.title = 'Click to sort';
  let asc = false;
  th.addEventListener('click', () => {{
    const table = th.closest('table');
    const tbody = table.querySelector('tbody');
    const rows  = Array.from(tbody.querySelectorAll('tr'));
    rows.sort((a, b) => {{
      const av = a.cells[colIdx]?.innerText.replace(/[$,%↑↓]/g, '').trim() || '';
      const bv = b.cells[colIdx]?.innerText.replace(/[$,%↑↓]/g, '').trim() || '';
      const an = parseFloat(av), bn = parseFloat(bv);
      if (!isNaN(an) && !isNaN(bn)) return asc ? an - bn : bn - an;
      return asc ? av.localeCompare(bv) : bv.localeCompare(av);
    }});
    asc = !asc;
    rows.forEach(r => tbody.appendChild(r));
  }});
}});
</script>
</body>
</html>"""


def _top10_mini_rows(rows: list[dict]) -> list[str]:
    html = []
    for i, r in enumerate(rows):
        cpl_str  = f"${r['cpl']:.2f}" if r["cpl"] else "—"
        conv_str = f"{r['conversions']:.0f}" if r["conversions"] > 0 else "0"
        badge    = ' <span class="office-badge">✓</span>' if r["near_office"] else ""
        html.append(f"""
            <tr>
                <td class="rank">{i + 1}</td>
                <td class="zip">{r["zipcode"]}{badge}</td>
                <td>{r["clicks"]:,}</td>
                <td>{conv_str}</td>
                <td>${r["cost"]:.2f}</td>
                <td class="cpl">{cpl_str}</td>
            </tr>""")
    return html


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Wellspring Google Ads Zipcode Analysis")
    parser.add_argument("--days", type=int, default=90, help="Number of days to analyse (default: 90)")
    args = parser.parse_args()

    end_date   = datetime.now().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=args.days - 1)
    generated_at = datetime.now().strftime("%d %b %Y, %H:%M")

    print(f"Wellspring Geo Analysis")
    print(f"  Date range : {start_date} to {end_date} ({args.days} days)")
    print(f"  Customer ID: {CUSTOMER_ID}")

    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ImportError:
        sys.exit("ERROR: google-ads library not installed. Run script with PPC-Agent venv.\n"
                 "  & \"C:\\Users\\Rishabhb\\Downloads\\PPC-Agent\\backend\\venv\\Scripts\\python.exe\" "
                 "wellspring_geo_analysis.py")

    print("  Connecting to Google Ads API…")
    client   = GoogleAdsClient.load_from_dict(CREDENTIALS)
    raw_rows = fetch_geo_rows(client, CUSTOMER_ID, start_date, end_date)
    print(f"  Raw rows returned: {len(raw_rows)}")

    user_loc, aoi = process_rows(raw_rows)
    print(f"  Postal code rows — User Location: {len(user_loc)} | Area of Interest: {len(aoi)}")

    s = summarize(user_loc)
    print(f"  Summary: {s['clicks']} clicks | {s['conversions']} conv | ${s['cost']} spend | CPL ${s['cpl']}")

    # Save CSV
    date_tag  = f"{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}"
    csv_path  = DATA_DIR / f"wellspring_geo_{date_tag}.csv"
    html_path = REPORTS_DIR / f"wellspring_geo_analysis_{date_tag}.html"

    save_csv(user_loc, csv_path)
    print(f"  CSV saved  : {csv_path}")

    # Generate HTML
    html = generate_html(user_loc, aoi, start_date, end_date, generated_at)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")
    print(f"  Report saved: {html_path}")
    print(f"\nDone. Open the report in your browser:\n  {html_path}")


if __name__ == "__main__":
    main()
