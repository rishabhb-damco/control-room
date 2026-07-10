#!/usr/bin/env python3
"""
build_geo_report.py - Wellspring Geographic Analysis HTML Report
Matches the exact styling of the Wellspring weekly performance report.
Run: python build_geo_report.py
"""

import csv, re
from pathlib import Path

ZIP_CSV  = Path.home() / "Downloads" / "Matched locations report.csv"
CITY_CSV = Path.home() / "Downloads" / "Matched locations report (1).csv"
OUT_HTML = Path(__file__).parent / "01_Reports" / "wellspring_geo_analysis_apr1-jun26-2026.html"

DATE_RANGE = "Apr 1 &ndash; Jun 26, 2026"
GENERATED  = "26 June 2026"

TROY_ZIPS    = {"48083","48084","48085","48098","48007"}
CLINTON_ZIPS = {"48035","48036","48038","48044","48045"}
NEAR_ZIPS    = TROY_ZIPS | CLINTON_ZIPS

# ── CSV parser ────────────────────────────────────────────────────────────────
def pn(s):
    try: return float(s.replace(",","").replace("%","").strip())
    except: return 0.0

def read_csv(path, transform):
    rows, header = [], None
    with open(path, encoding="utf-8-sig") as f:
        for line in csv.reader(f):
            if not line or not line[0].strip(): continue
            if line[0].startswith("Total:") or "Matched locations" in line[0]: continue
            if header is None:
                if "Matched location" in line[0]: header = line
                continue
            if len(line) < 10: continue
            nm   = transform(line[0])
            cost = round(pn(line[6]), 2)
            conv = round(pn(line[8]), 2)
            rows.append({
                "name": nm,
                "clicks": int(pn(line[1])),
                "impressions": int(pn(line[2])),
                "ctr": round(pn(line[3]), 2),
                "avg_cpc": round(pn(line[5]), 2),
                "cost": cost,
                "conversions": conv,
                "cpl": round(cost/conv, 2) if conv > 0 else None,
            })
    return rows

def strip_mi(s):
    s = s.strip('"').strip()
    return re.sub(r",\s*Michigan,\s*United States$", "", s).strip()

zip_rows  = read_csv(ZIP_CSV,  strip_mi)
city_rows = read_csv(CITY_CSV, strip_mi)

for r in zip_rows:
    r["near_office"] = r["name"] in NEAR_ZIPS

zip_active  = sorted([r for r in zip_rows  if r["clicks"]>0], key=lambda x:x["clicks"], reverse=True)
city_active = sorted([r for r in city_rows if r["clicks"]>0], key=lambda x:x["clicks"], reverse=True)

def tot(rows, k): return sum(r[k] for r in rows)

z_clicks = tot(zip_active,"clicks")
z_impr   = tot(zip_active,"impressions")
z_cost   = round(tot(zip_active,"cost"),2)
z_conv   = round(tot(zip_active,"conversions"),2)
z_cpl    = round(z_cost/z_conv,2) if z_conv else 0
z_ctr    = round(z_clicks/z_impr*100,2) if z_impr else 0
z_count  = len(zip_active)

# ── HTML pieces ───────────────────────────────────────────────────────────────
def kpi3(label, value, explain, badge_html="", color="teal"):
    return f"""
    <div class="kpi-card {color}">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-explain">{explain}</div>
      {badge_html}
    </div>"""

def badge(text, kind="teal"):
    cls = {"up":"badge-up","down":"badge-down","warn":"badge-warn","teal":"badge-teal"}.get(kind,"badge-teal")
    return f'<span class="kpi-badge {cls}">{text}</span>'

def sec_div(title, subtitle="", color="teal"):
    dot_color = {"teal":"var(--teal)","amber":"var(--amber)","rust":"var(--rust)","violet":"var(--violet)","green":"var(--green)"}.get(color,"var(--teal)")
    sub = f'<span class="stag">{subtitle}</span>' if subtitle else ""
    return f"""
    <div class="section-divider">
      <span class="sdot" style="background:{dot_color}"></span>
      <h2>{title}</h2>{sub}
    </div>"""

def tr_zip(i, r):
    cpl  = f"${r['cpl']:.2f}" if r["cpl"] else "&mdash;"
    conv = f"{r['conversions']:.0f}" if r["conversions"] else "0"
    badge_html = ' <span class="loc-badge">near office</span>' if r["near_office"] else ""
    row_style  = ' style="background:var(--teal-pale);"' if r["near_office"] else ""
    return f'<tr{row_style}><td class="rank">{i}</td><td class="loc">{r["name"]}{badge_html}</td><td class="num">{r["clicks"]:,}</td><td class="num">{r["impressions"]:,}</td><td class="num">{r["ctr"]:.2f}%</td><td class="num">${r["avg_cpc"]:.2f}</td><td class="num">${r["cost"]:.2f}</td><td class="num">{conv}</td><td class="cpl-cell">{cpl}</td></tr>'

def tr_city(i, r):
    cpl  = f"${r['cpl']:.2f}" if r["cpl"] else "&mdash;"
    conv = f"{r['conversions']:.0f}" if r["conversions"] else "0"
    return f'<tr><td class="rank">{i}</td><td class="loc">{r["name"]}</td><td class="num">{r["clicks"]:,}</td><td class="num">{r["impressions"]:,}</td><td class="num">{r["ctr"]:.2f}%</td><td class="num">${r["avg_cpc"]:.2f}</td><td class="num">${r["cost"]:.2f}</td><td class="num">{conv}</td><td class="cpl-cell">{cpl}</td></tr>'

# Chart data
top10z = zip_active[:10]
top10c = city_active[:10]
z_labels = str([r["name"]        for r in top10z]).replace("'",'"')
z_clicks_d= str([r["clicks"]     for r in top10z])
z_conv_d  = str([r["conversions"]for r in top10z])
c_labels = str([r["name"]        for r in top10c]).replace("'",'"')
c_clicks_d= str([r["clicks"]     for r in top10c])
c_conv_d  = str([r["conversions"]for r in top10c])

zip_tbl  = "".join(tr_zip(i+1, r)  for i,r in enumerate(zip_active[:20]))
city_tbl = "".join(tr_city(i+1, r) for i,r in enumerate(city_active[:20]))

# KPI rows
kpi_row1 = (
    kpi3("Total clicks from ads", f"{z_clicks:,}",
         f"Across all {z_count} active zip codes, Apr 1 &ndash; Jun 26",
         badge("1,184 total clicks","teal")) +
    kpi3("Conversions (form fills &amp; calls)", f"{z_conv:.0f}",
         "People who clicked an ad and submitted a contact form or called",
         badge("51.7 conversions tracked","up"), "green") +
    kpi3("Average cost per conversion", f"${z_cpl:.2f}",
         "How much was spent on average to generate each enquiry",
         badge("vs $44 March benchmark","warn"), "amber")
)
kpi_row2 = (
    kpi3("Active zip codes", str(z_count),
         "Zip codes in Michigan that received at least one click",
         badge(f"{len([r for r in zip_active if r['near_office']])} near Wellspring offices","teal")) +
    kpi3("Total ad spend", f"${z_cost:,.2f}",
         "Total Google Ads spend attributed to location-matched zip codes",
         badge("Apr 1 &ndash; Jun 26, 2026","teal")) +
    kpi3("Overall CTR", f"{z_ctr:.2f}%",
         "Percentage of impressions that resulted in a click across all active zips",
         badge("6%+ = strong for healthcare","up"), "green")
)

# Insights
converters = sorted([r for r in zip_active if r["cpl"]], key=lambda x:x["cpl"])
best = converters[0] if converters else None
waste = sorted([r for r in zip_active if r["conversions"]==0 and r["cost"]>80], key=lambda x:x["cost"],reverse=True)
near  = [r for r in zip_active if r["near_office"]]
near_clicks = sum(r["clicks"] for r in near)
near_conv   = round(sum(r["conversions"] for r in near),1)
near_pct    = round(near_clicks/z_clicks*100,1) if z_clicks else 0

ins1 = f"""<div class="insight-card">
  <strong>&#8593; Best-performing zip code: {best["name"] if best else "—"}</strong><br>
  Lowest CPL at <strong>${best["cpl"]:.2f}</strong> with {int(best["conversions"])} conversions
  ({best["clicks"]} clicks, ${best["cost"]:.2f} spend).
  Recommend increasing bids or applying a positive location bid modifier for this zip.
</div>""" if best else ""

ins2 = f"""<div class="insight-card amber">
  <strong>&#9651; Zero-conversion spend to review</strong><br>
  <strong>{len(waste)} zip codes</strong> ({", ".join(r["name"] for r in waste[:3])}{"&hellip;" if len(waste)>3 else ""})
  spent a combined <strong>${round(sum(r["cost"] for r in waste),2):,.2f}</strong> with 0 conversions.
  Consider excluding these areas or reducing bids to recover budget for higher-performing zones.
</div>""" if waste else ""

ins3 = f"""<div class="insight-card">
  <strong>&#128205; Office vicinity coverage</strong><br>
  Zip codes near the Troy and Clinton Township offices account for
  <strong>{near_pct}% of all clicks</strong> &mdash; {near_clicks:,} clicks and {near_conv:.0f} conversions
  across {len(near)} proximate zip codes. These remain the core service area and perform as expected.
</div>"""

ins4 = """<div class="insight-card">
  <strong>&#127942; Top cities driving results</strong><br>
  <strong>Clinton Township</strong> leads by click volume (382 clicks, $96.62 CPL).
  <strong>Troy</strong> is a close second (342 clicks, $83.75 CPL).
  <strong>Royal Oak</strong> punches above its weight (42 clicks, 3 conversions, <strong>$70.04 CPL</strong>).
  <strong>Warren</strong> shows solid returns (54 clicks, 5 conversions, $77.12 CPL).
</div>"""

insights = ins1 + ins2 + ins3 + ins4

# ── Full HTML ─────────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Wellspring &mdash; Geographic Analysis {DATE_RANGE}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{{
  --cream:#F7F3EE; --cream-dark:#EDE7DC; --charcoal:#1C1C1A;
  --warm-mid:#6B6460; --teal:#3D7A72; --teal-pale:#EAF3F2;
  --rust:#C25B3F; --amber:#C9882A; --violet:#5C4E9E;
  --green:#3D8A60; --red:#C44040; --border:#DDD5C8;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#f0ece6;font-family:'DM Sans',sans-serif;color:var(--charcoal);font-size:13px;line-height:1.6;}}

/* Password gate */
#pw-gate{{position:fixed;inset:0;background:#1a2e2b;display:flex;align-items:center;justify-content:center;z-index:9999;}}
#pw-gate.hidden{{display:none;}}
.pw-box{{background:#F7F3EE;border-radius:14px;padding:40px 48px;width:360px;text-align:center;box-shadow:0 24px 60px rgba(0,0,0,0.4);}}
.pw-logo{{font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:500;color:#1C1C1A;}}
.pw-sub{{font-size:9px;letter-spacing:3px;text-transform:uppercase;color:#C25B3F;margin-top:4px;font-weight:500;}}
.pw-label{{font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#6B6460;font-weight:500;margin:24px 0 8px;}}
.pw-input{{width:100%;padding:10px 14px;border:1.5px solid #DDD5C8;border-radius:8px;font-family:'DM Sans',sans-serif;font-size:14px;color:#1C1C1A;background:#fff;outline:none;text-align:center;letter-spacing:2px;}}
.pw-input:focus{{border-color:#3D7A72;}}
.pw-btn{{width:100%;margin-top:14px;padding:11px;background:#3D7A72;color:#fff;border:none;border-radius:8px;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:500;cursor:pointer;}}
.pw-btn:hover{{background:#2e5e58;}}
.pw-error{{font-size:11.5px;color:#C25B3F;margin-top:10px;min-height:18px;}}
.pw-footer{{font-size:10px;color:#6B6460;margin-top:20px;}}
.pw-footer strong{{color:#1C1C1A;}}

/* Page layout */
.page{{max-width:1100px;margin:0 auto;padding:28px 32px;background:var(--cream);min-height:100vh;}}

/* Header */
.header{{display:flex;align-items:flex-start;justify-content:space-between;padding-bottom:16px;border-bottom:1.5px solid var(--border);margin-bottom:16px;}}
.logo-name{{font-family:'Cormorant Garamond',serif;font-size:34px;font-weight:500;letter-spacing:-0.5px;color:var(--charcoal);line-height:1;}}
.logo-sub{{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--rust);margin-top:4px;font-weight:500;}}
.header-meta{{text-align:right;}}
.report-label{{font-size:10px;text-transform:uppercase;letter-spacing:2px;color:var(--warm-mid);font-weight:500;}}
.report-week{{font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:600;color:var(--charcoal);margin-top:2px;}}
.report-prepared{{font-size:11px;color:var(--warm-mid);margin-top:4px;}}

/* Section helpers */
.section-label{{font-size:9px;text-transform:uppercase;letter-spacing:3px;color:var(--teal);font-weight:500;margin-bottom:8px;}}
.section-divider{{margin:20px 0 14px;padding-top:18px;border-top:2px solid var(--cream-dark);display:flex;align-items:center;gap:12px;}}
.sdot{{width:9px;height:9px;border-radius:50%;background:var(--teal);flex-shrink:0;}}
.section-divider h2{{font-family:'Cormorant Garamond',serif;font-size:18px;font-weight:600;color:var(--charcoal);}}
.stag{{font-size:10px;color:var(--warm-mid);font-weight:400;font-family:'DM Sans',sans-serif;}}

/* KPI cards */
.kpi-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:12px;}}
.kpi-card{{background:#fff;border:1px solid var(--border);border-radius:10px;padding:16px 20px;position:relative;overflow:hidden;}}
.kpi-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--teal);border-radius:10px 10px 0 0;}}
.kpi-card.amber::before{{background:var(--amber);}}
.kpi-card.green::before{{background:var(--green);}}
.kpi-card.rust::before{{background:var(--rust);}}
.kpi-label{{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:var(--warm-mid);font-weight:500;margin-bottom:6px;}}
.kpi-value{{font-family:'Cormorant Garamond',serif;font-size:44px;font-weight:600;color:var(--charcoal);line-height:1;}}
.kpi-explain{{font-size:12px;color:var(--warm-mid);margin-top:5px;line-height:1.5;}}
.kpi-badge{{display:inline-block;font-size:9.5px;padding:3px 8px;border-radius:20px;margin-top:6px;font-weight:500;}}
.badge-up{{background:#E8F5EC;color:#2E7D4F;}}
.badge-down{{background:#FDF1EE;color:#C25B3F;}}
.badge-warn{{background:#FDF6EC;color:#C9882A;}}
.badge-teal{{background:var(--teal-pale);color:var(--teal);}}

/* Two-col panels */
.two-col{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px;}}
.panel{{background:#fff;border:1px solid var(--border);border-radius:12px;padding:16px 18px;}}
.panel-title{{font-family:'Cormorant Garamond',serif;font-size:16px;font-weight:600;color:var(--charcoal);margin-bottom:10px;display:flex;align-items:center;gap:8px;}}
.panel-title .dot{{width:8px;height:8px;border-radius:50%;background:var(--teal);flex-shrink:0;}}

/* Charts */
canvas{{max-height:260px;}}

/* Tables */
.tbl-wrap{{overflow-x:auto;}}
.dt{{width:100%;border-collapse:collapse;font-size:12.5px;}}
.dt thead tr{{background:var(--teal);color:#fff;}}
.dt thead th{{padding:9px 12px;text-align:left;font-family:'DM Sans',sans-serif;font-size:10px;font-weight:500;letter-spacing:0.8px;text-transform:uppercase;white-space:nowrap;cursor:pointer;user-select:none;}}
.dt thead th:hover{{background:#2e5e58;}}
.dt tbody tr{{border-bottom:1px solid var(--border);transition:background 0.1s;}}
.dt tbody tr:last-child{{border-bottom:none;}}
.dt tbody tr:hover{{background:rgba(61,122,114,0.06);}}
.dt td{{padding:9px 12px;}}
.dt td.rank{{color:var(--warm-mid);font-size:11px;width:30px;}}
.dt td.loc{{font-weight:500;color:var(--charcoal);}}
.dt td.num{{text-align:right;color:var(--warm-mid);}}
.dt td.cpl-cell{{text-align:right;font-weight:600;color:var(--teal);}}
.loc-badge{{display:inline-block;background:var(--teal);color:#fff;font-size:8.5px;font-weight:600;letter-spacing:0.5px;text-transform:uppercase;padding:1px 6px;border-radius:3px;margin-left:6px;vertical-align:middle;}}

/* Insight cards */
.insight-card{{border-left:3px solid var(--teal);padding:10px 14px;margin-bottom:8px;background:var(--teal-pale);border-radius:0 8px 8px 0;font-size:12.5px;line-height:1.6;}}
.insight-card.amber{{border-left-color:var(--amber);background:#FDF6EC;}}
.insight-card.rust{{border-left-color:var(--rust);background:#FDF1EE;}}
.insight-card:last-child{{margin-bottom:0;}}

/* Footer */
.divider{{border:none;border-top:1px solid var(--border);margin:14px 0;}}
.footer{{margin-top:20px;padding-top:14px;border-top:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;}}
.footer-left{{font-size:10.5px;color:var(--warm-mid);line-height:1.7;}}
.footer-right{{font-family:'Cormorant Garamond',serif;font-size:15px;font-weight:500;color:var(--teal);}}

@media print{{body{{background:white;}}.page{{padding:16px 20px;}}#pw-gate{{display:none!important;}}}}
</style>
</head>
<body>

<!-- PASSWORD GATE -->
<div id="pw-gate">
  <div class="pw-box">
    <div class="pw-logo">Wellspring</div>
    <div class="pw-sub">Therapeutic Partners</div>
    <div class="pw-label">Enter report password</div>
    <input id="pw-input" class="pw-input" type="password" placeholder="............" autocomplete="off"/>
    <button class="pw-btn" onclick="checkPassword()">View Report</button>
    <div id="pw-error" class="pw-error"></div>
    <div class="pw-footer">Confidential &middot; Prepared by <strong>Damco Digital</strong></div>
  </div>
</div>
<script>
(function(){{if(sessionStorage.getItem('ws_auth')==='1'){{document.addEventListener('DOMContentLoaded',function(){{document.getElementById('pw-gate').classList.add('hidden');}});}}}}());
function checkPassword(){{
  if(document.getElementById('pw-input').value==='Wellspring123'){{
    sessionStorage.setItem('ws_auth','1');
    document.getElementById('pw-gate').classList.add('hidden');
  }}else{{
    document.getElementById('pw-error').textContent='Incorrect password.';
    document.getElementById('pw-input').value='';
    document.getElementById('pw-input').focus();
  }}
}}
document.addEventListener('DOMContentLoaded',function(){{
  var inp=document.getElementById('pw-input');
  if(inp){{
    inp.addEventListener('keydown',function(e){{if(e.key==='Enter')checkPassword();}});
    if(sessionStorage.getItem('ws_auth')!=='1')inp.focus();
  }}
}});
</script>

<!-- PAGE -->
<div class="page">

  <!-- HEADER -->
  <div class="header">
    <div>
      <div class="logo-name">Wellspring</div>
      <div class="logo-sub">Therapeutic Partners</div>
    </div>
    <div class="header-meta">
      <div class="report-label">Geographic Performance Analysis</div>
      <div class="report-week">{DATE_RANGE}</div>
      <div class="report-prepared">Prepared by Damco Digital &nbsp;&middot;&nbsp; Google Ads &mdash; Matched Locations</div>
    </div>
  </div>

  <!-- SECTION 1: OVERVIEW KPIs -->
  <div class="section-label">Geographic Overview &mdash; Where your ads are reaching across Michigan</div>
  <div class="kpi-grid">{kpi_row1}</div>
  <div class="kpi-grid">{kpi_row2}</div>

  <!-- SECTION 2: CHARTS -->
  {sec_div("Top Performers &mdash; Zip Code &amp; City Breakdown", f"{z_count} active zip codes &middot; {len(city_active)} cities with clicks")}
  <div class="two-col">
    <div class="panel">
      <div class="panel-title"><span class="dot"></span>Top 10 Zip Codes by Clicks</div>
      <canvas id="zipChart"></canvas>
    </div>
    <div class="panel">
      <div class="panel-title"><span class="dot" style="background:var(--amber)"></span>Top 10 Cities by Clicks</div>
      <canvas id="cityChart"></canvas>
    </div>
  </div>

  <!-- SECTION 3: CITY TABLE -->
  {sec_div("City Performance", "Top 20 cities by clicks &middot; click any header to re-sort", "amber")}
  <div class="panel" style="padding:0;">
    <div class="tbl-wrap">
      <table class="dt" id="cityTable">
        <thead><tr>
          <th>#</th><th>City</th><th>Clicks</th><th>Impr.</th>
          <th>CTR</th><th>Avg CPC</th><th>Spend</th><th>Conv.</th><th>CPL</th>
        </tr></thead>
        <tbody>{city_tbl}</tbody>
      </table>
    </div>
  </div>

  <!-- SECTION 4: ZIP TABLE -->
  {sec_div("Zip Code Performance", "Top 20 zip codes by clicks &middot; teal highlight = near Troy or Clinton Twp office &middot; click header to re-sort", "violet")}
  <div class="panel" style="padding:0;">
    <div class="tbl-wrap">
      <table class="dt" id="zipTable">
        <thead><tr>
          <th>#</th><th>Zip Code</th><th>Clicks</th><th>Impr.</th>
          <th>CTR</th><th>Avg CPC</th><th>Spend</th><th>Conv.</th><th>CPL</th>
        </tr></thead>
        <tbody>{zip_tbl}</tbody>
      </table>
    </div>
  </div>

  <!-- SECTION 5: INSIGHTS -->
  {sec_div("Key Observations", "auto-generated from location data")}
  <div class="panel">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
      <div>{ins1}{ins3}</div>
      <div>{ins2}{ins4}</div>
    </div>
  </div>

  <hr class="divider">
  <div class="footer">
    <div class="footer-left">
      Prepared by <strong>Damco Digital</strong> &nbsp;&middot;&nbsp; Confidential: For Wellspring Team Use Only<br>
      Data source: Google Ads Matched Locations Report (Apr 1 &ndash; Jun 26, 2026) &nbsp;&middot;&nbsp; Generated {GENERATED}
    </div>
    <div class="footer-right">Wellspring Therapeutic Partners</div>
  </div>

</div><!-- /page -->

<script>
window.addEventListener('load', function() {{
  const cfg = {{
    responsive: true,
    maintainAspectRatio: false,
    plugins: {{
      legend: {{ display: true, position: 'bottom', labels: {{ font: {{ family: 'DM Sans', size: 11 }}, color: '#6B6460', padding: 14 }} }},
      tooltip: {{ callbacks: {{ label: ctx => ` ${{ctx.dataset.label}}: ${{ctx.parsed.y % 1 === 0 ? ctx.parsed.y : ctx.parsed.y.toFixed(1)}}` }} }}
    }},
    scales: {{
      x: {{ grid: {{ display: false }}, ticks: {{ font: {{ family: 'DM Sans', size: 10 }}, color: '#6B6460' }} }},
      y:  {{ grid: {{ color: '#EDE7DC' }}, ticks: {{ font: {{ family: 'DM Sans', size: 10 }}, color: '#6B6460' }}, title: {{ display: true, text: 'Clicks', font: {{ family:'DM Sans', size:10 }}, color:'#6B6460' }} }},
      y2: {{ position: 'right', grid: {{ drawOnChartArea: false }}, ticks: {{ font: {{ family:'DM Sans', size:10 }}, color:'#C9882A' }}, title: {{ display: true, text: 'Conv.', font: {{ family:'DM Sans', size:10 }}, color:'#C9882A' }} }}
    }}
  }};

  new Chart(document.getElementById('zipChart'), {{
    type: 'bar',
    data: {{
      labels: {z_labels},
      datasets: [
        {{ label: 'Clicks', data: {z_clicks_d}, backgroundColor: '#3D7A72', borderRadius: 4, yAxisID: 'y' }},
        {{ label: 'Conversions', data: {z_conv_d}, backgroundColor: '#C9882A', borderRadius: 4, yAxisID: 'y2' }}
      ]
    }},
    options: cfg
  }});

  new Chart(document.getElementById('cityChart'), {{
    type: 'bar',
    data: {{
      labels: {c_labels},
      datasets: [
        {{ label: 'Clicks', data: {c_clicks_d}, backgroundColor: '#3D7A72', borderRadius: 4, yAxisID: 'y' }},
        {{ label: 'Conversions', data: {c_conv_d}, backgroundColor: '#C9882A', borderRadius: 4, yAxisID: 'y2' }}
      ]
    }},
    options: cfg
  }});

  // Sortable tables
  document.querySelectorAll('.dt').forEach(function(table) {{
    table.querySelectorAll('thead th').forEach(function(th, col) {{
      let asc = false;
      th.addEventListener('click', function() {{
        const tbody = table.querySelector('tbody');
        const rows  = [...tbody.querySelectorAll('tr')];
        rows.sort(function(a, b) {{
          const av = a.cells[col]?.innerText.replace(/[$,%]/g,'').replace(/—/g,'').trim()||'';
          const bv = b.cells[col]?.innerText.replace(/[$,%]/g,'').replace(/—/g,'').trim()||'';
          const an = parseFloat(av), bn = parseFloat(bv);
          if(!isNaN(an)&&!isNaN(bn)) return asc ? an-bn : bn-an;
          return asc ? av.localeCompare(bv) : bv.localeCompare(av);
        }});
        asc = !asc;
        rows.forEach(function(r){{tbody.appendChild(r);}});
        table.querySelectorAll('thead th').forEach(function(h){{h.textContent=h.textContent.replace(/ [▲▼]$/,'');}});
        th.textContent += asc ? ' ▲' : ' ▼';
      }});
    }});
  }});
}});
</script>
</body>
</html>"""

OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
OUT_HTML.write_text(html, encoding="utf-8")
print(f"Saved: {OUT_HTML}")
print(f"  Zip codes : {z_count}  |  Clicks: {z_clicks:,}  |  Conv: {z_conv:.1f}  |  Spend: ${z_cost:,.2f}  |  CPL: ${z_cpl:.2f}")
