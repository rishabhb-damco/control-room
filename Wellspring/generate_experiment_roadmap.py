"""
Generate Wellspring Q3 2026 Campaign Experiment Roadmap deck.
Covers all 5 experiments: PMax, LSAs, Competitor Conquest, Display Retargeting, Bing.
Matches QBR visual style.
"""

import sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE as MSO
from pptx.oxml.ns import qn
from lxml import etree

# ── Palette ───────────────────────────────────────────────────────────────────
PRIMARY = RGBColor(0x4B, 0x3B, 0xC8)
BLUE    = RGBColor(0x3B, 0x82, 0xF6)
INDIGO  = RGBColor(0x63, 0x66, 0xF1)
DARK    = RGBColor(0x1E, 0x1E, 0x2E)
GRAY    = RGBColor(0x6B, 0x72, 0x80)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
BG      = RGBColor(0xF5, 0xF6, 0xFA)
LIGHT   = RGBColor(0xEE, 0xF2, 0xFF)
LIGHT2  = RGBColor(0xC9, 0xCB, 0xF0)
GREEN   = RGBColor(0x10, 0xB9, 0x81)
AMBER   = RGBColor(0xF5, 0x9E, 0x0B)
RED     = RGBColor(0xEF, 0x44, 0x44)
DGRAY   = RGBColor(0xE5, 0xE7, 0xEB)

I = Inches

def hc(s):
    return RGBColor(int(s[0:2],16), int(s[2:4],16), int(s[4:6],16))

# ── Primitives ────────────────────────────────────────────────────────────────

def set_bg(slide, color=None):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color or BG

def rect(slide, l, t, w, h, color, lc=None):
    shp = slide.shapes.add_shape(MSO.RECTANGLE, I(l), I(t), I(w), I(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = color
    if lc: shp.line.color.rgb = lc
    else:  shp.line.fill.background()
    return shp

def oval(slide, l, t, w, h, color):
    shp = slide.shapes.add_shape(MSO.OVAL, I(l), I(t), I(w), I(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return shp

def txb(slide, text, l, t, w, h, sz=12, bold=False, clr=None,
        align=PP_ALIGN.LEFT, font='Calibri', italic=False):
    box = slide.shapes.add_textbox(I(l), I(t), I(w), I(h))
    tf = box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.name = font; r.font.size = Pt(sz)
    r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = clr or DARK
    return box

def set_cell_bg(cell, hex_str):
    tc = cell._tc
    tcPr = tc.find(qn('a:tcPr'))
    if tcPr is None: tcPr = etree.SubElement(tc, qn('a:tcPr'))
    for tag in ['a:solidFill','a:gradFill','a:noFill','a:pattFill','a:blipFill']:
        for e in tcPr.findall(qn(tag)): tcPr.remove(e)
    sf = etree.SubElement(tcPr, qn('a:solidFill'))
    sc = etree.SubElement(sf, qn('a:srgbClr')); sc.set('val', hex_str)

def set_cell_text(cell, text, sz=11, bold=False, color='1E1E2E',
                  align=PP_ALIGN.LEFT, font='Calibri'):
    tf = cell.text_frame
    for para in tf.paragraphs[1:]: para._p.getparent().remove(para._p)
    p = tf.paragraphs[0]
    for run in p.runs: run._r.getparent().remove(run._r)
    p.alignment = align
    r = p.add_run(); r.text = text
    r.font.name = font; r.font.size = Pt(sz); r.font.bold = bold
    r.font.color.rgb = hc(color)

def std_header(slide, title, subtitle=None):
    rect(slide, 0.0, 0.0, 13.33, 0.82, PRIMARY)
    txb(slide, title, 0.55, 0.10, 10.5, 0.62, sz=22, bold=True, clr=WHITE, font='Arial Black')
    if subtitle:
        txb(slide, subtitle, 0.55, 0.60, 12.00, 0.28, sz=10, clr=LIGHT2)

def std_footer(slide, n):
    rect(slide, 12.72, 7.10, 0.50, 0.34, PRIMARY)
    txb(slide, str(n), 12.72, 7.10, 0.50, 0.34, sz=11, bold=True, clr=WHITE, align=PP_ALIGN.CENTER)
    txb(slide, 'Copyright © 2025 Damco Group. All Rights Reserved.',
        0.30, 7.24, 11.0, 0.22, sz=9, clr=GRAY)

def new_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])

def section_divider(prs, title, subtitle, page, color=PRIMARY):
    s = new_slide(prs)
    set_bg(s, WHITE)
    rect(s, 0.0, 0.0, 4.80, 7.50, color)
    rect(s, 4.80, 2.60, 0.10, 2.30, LIGHT2)
    txb(s, title,    0.45, 2.80, 4.10, 1.20, sz=34, bold=True, clr=WHITE, font='Arial Black')
    txb(s, subtitle, 0.45, 4.10, 4.10, 0.70, sz=13, clr=LIGHT2)
    std_footer(s, page)
    return s

# ── Experiment card helper ────────────────────────────────────────────────────

def exp_card(slide, l, t, w, h, color, number, title, budget, month, bullets):
    """Compact experiment summary card."""
    rect(slide, l, t, w, 0.42, color)
    oval(slide, l + 0.12, t + 0.10, 0.24, 0.24, WHITE)
    txb(slide, number, l + 0.12, t + 0.10, 0.24, 0.24, sz=9, bold=True,
        clr=color, align=PP_ALIGN.CENTER)
    txb(slide, title, l + 0.45, t + 0.11, w - 0.55, 0.26, sz=12, bold=True, clr=WHITE)
    rect(slide, l, t + 0.42, w, h - 0.42, WHITE)
    # Month + budget tags
    rect(slide, l + 0.12, t + 0.56, 0.80, 0.22, LIGHT)
    txb(slide, month,  l + 0.12, t + 0.57, 0.80, 0.20, sz=8, bold=True, clr=color, align=PP_ALIGN.CENTER)
    rect(slide, l + 1.00, t + 0.56, 1.00, 0.22, LIGHT)
    txb(slide, budget, l + 1.00, t + 0.57, 1.00, 0.20, sz=8, bold=True, clr=color, align=PP_ALIGN.CENTER)
    # Bullet points
    for i, b in enumerate(bullets):
        top = t + 0.88 + i * 0.44
        oval(slide, l + 0.12, top + 0.12, 0.10, 0.10, color)
        txb(slide, b, l + 0.30, top + 0.04, w - 0.42, 0.36, sz=10, clr=DARK)

# ─────────────────────────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = I(13.33)
prs.slide_height = I(7.50)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1  Cover
# ══════════════════════════════════════════════════════════════════════════════
s = new_slide(prs)
set_bg(s)
for (l, t, sz_c, col) in [(7.8,-1.2,5.0,'EEF0FF'),(9.3,0.6,6.2,'C9CBF0')]:
    shp = s.shapes.add_shape(MSO.OVAL, I(l), I(t), I(sz_c), I(sz_c))
    shp.fill.solid(); shp.fill.fore_color.rgb = hc(col); shp.line.fill.background()

txb(s, 'Damco Digital × Wellspring',          1.5, 1.85, 10.3, 0.62, sz=18, bold=True, clr=DARK)
txb(s, 'Q3 2026 Campaign',                     1.5, 2.55, 10.3, 0.90, sz=48, bold=True, clr=PRIMARY, font='Arial Black')
txb(s, 'Experiment Roadmap',                   1.5, 3.45, 10.3, 0.80, sz=48, bold=True, clr=PRIMARY, font='Arial Black')
txb(s, 'June – August 2026  |  5 Tests  |  Budget Proposal', 1.5, 4.38, 10.3, 0.55, sz=17, clr=GRAY)
txb(s, 'Wellspring Therapeutic Partners  |  Prepared by Damco Digital',
    1.5, 4.96, 10.3, 0.46, sz=14, clr=GRAY)
txb(s, 'Copyright © 2025 Damco Group. All Rights Reserved.',
    0.30, 7.24, 11.0, 0.22, sz=9, clr=GRAY)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2  Where We Stand — what's validated
# ══════════════════════════════════════════════════════════════════════════════
s = new_slide(prs)
set_bg(s)
std_header(s, 'Where We Stand (Q1–Q2 2026)',
           'What has been tested, what is validated, and what is the gap we are filling in Q3')
std_footer(s, 2)

# 3 status cards
cards_s2 = [
    (PRIMARY, '✓  VALIDATED WINNER',   'DSA Campaign',
     ['$22–$57 CPA — 2–4x better than Generic Search every single week',
      'CTR: 6–9% consistently', 'Budget already being increased']),
    (AMBER,   '⟳  IN TEST (May 2026)', 'Regional Search Campaign',
     ['Launched 06 May 2026', 'Too early to read — first full data week pending',
      'Covers Troy + Clinton Twp geo-split']),
    (RED,     '✗  BLOCKED',            'YouTube / Demand Gen',
     ['Google Healthcare certificate required for full YouTube ad access',
      '$53 wasted in early test before policy block was discovered',
      'Cert application: medium-priority open action — PMax is the workaround for now']),
]
for i, (clr, badge, title, bullets) in enumerate(cards_s2):
    l = 0.55 + i * 4.25
    rect(s, l, 1.05, 4.00, 0.38, clr)
    txb(s, badge, l+0.15, 1.09, 3.72, 0.30, sz=11, bold=True, clr=WHITE)
    rect(s, l, 1.43, 4.00, 4.90, WHITE)
    txb(s, title, l+0.18, 1.56, 3.66, 0.42, sz=15, bold=True, clr=clr)
    for j, b in enumerate(bullets):
        oval(s, l+0.18, 2.10 + j*0.78 + 0.14, 0.12, 0.12, clr)
        txb(s, b, l+0.40, 2.10 + j*0.78 + 0.04, 3.45, 0.66, sz=11, clr=DARK)

# Bottom call-out
rect(s, 0.0, 6.55, 13.33, 0.60, LIGHT)
rect(s, 0.0, 6.55, 0.10, 0.60, PRIMARY)
txb(s, 'DSA is the template. The Q3 goal is to find the next winner — then scale it.',
    0.28, 6.63, 12.85, 0.40, sz=13, bold=True, clr=PRIMARY)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3  The 5 Experiments — Overview Table
# ══════════════════════════════════════════════════════════════════════════════
s = new_slide(prs)
set_bg(s)
std_header(s, 'The 5 Experiments: Overview',
           'One experiment per month pair — each with a distinct hypothesis and engagement target')
std_footer(s, 3)

# Summary table
hdrs3 = ['#', 'Experiment', 'Month', 'Budget / Month', 'Platform', 'Hypothesis']
rows3 = [
    ('1', 'Performance Max',       'June',   '$500–$600', 'Google (all channels)',    'PMax finds intent signals DSA misses + gets us on YouTube for therapy without Healthcare cert'),
    ('2', 'Local Service Ads',     'June',   '$300–$400', 'Google LSA',               'Pay-per-lead format + position zero improves lead quality vs CPC campaigns'),
    ('3', 'Competitor Conquest',   'July',   '$200–$250', 'Google Search',            'GLPG\'s weak reputation (2.6★) makes their branded queries easy to intercept'),
    ('4', 'Display Remarketing',   'July',   '$150–$200', 'Google Display Network',   'Re-engaging warm website visitors at low CPM keeps Wellspring top-of-mind between searches'),
    ('5', 'Bing / Microsoft Ads',  'August', '$150–$200', 'Microsoft Advertising',    '30–50% lower CPCs + 45+ demographic skew = more commercially insured leads for less spend'),
]
col_ws3 = [0.35, 2.10, 0.80, 1.30, 1.95, 5.75]
tbl3 = s.shapes.add_table(len(rows3)+1, 6, I(0.30), I(1.02), I(12.75), I(6.10)).table
for ci, cw in enumerate(col_ws3): tbl3.columns[ci].width = I(cw)

for ci, h in enumerate(hdrs3):
    cell = tbl3.cell(0, ci)
    set_cell_bg(cell, '4B3BC8')
    set_cell_text(cell, h, sz=10, bold=True, color='FFFFFF')

exp_colors = ['4B3BC8','4B3BC8','3B82F6','3B82F6','6366F1']
for ri, row in enumerate(rows3):
    bg = 'EEF2FF' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate(row):
        cell = tbl3.cell(ri+1, ci)
        set_cell_bg(cell, bg)
        if ci == 0:
            set_cell_bg(cell, exp_colors[ri])
            set_cell_text(cell, val, sz=12, bold=True, color='FFFFFF', align=PP_ALIGN.CENTER)
        elif ci == 1:
            set_cell_text(cell, val, sz=11, bold=True, color='1E1E2E')
        elif ci == 2:
            set_cell_text(cell, val, sz=11, bold=True, color=exp_colors[ri])
        else:
            set_cell_text(cell, val, sz=10, color='1E1E2E')

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4  Exp 1 — Performance Max
# ══════════════════════════════════════════════════════════════════════════════
s = new_slide(prs)
set_bg(s)
std_header(s, 'Experiment 1 — Performance Max',
           'June 2026  |  Budget: $500–$600/month  |  Platform: Google (Search, Display, YouTube, Gmail, Discover, Maps)')
std_footer(s, 4)

# Exp tag
rect(s, 0.55, 1.05, 1.60, 0.34, PRIMARY)
txb(s, 'EXPERIMENT 1', 0.62, 1.09, 1.48, 0.26, sz=10, bold=True, clr=WHITE)
txb(s, 'Performance Max', 2.28, 1.02, 8.0, 0.45, sz=20, bold=True, clr=PRIMARY, font='Arial Black')

# What + Why side by side
rect(s, 0.55, 1.55, 6.10, 0.30, PRIMARY)
txb(s, 'WHAT IT IS', 0.70, 1.58, 6.00, 0.25, sz=10, bold=True, clr=WHITE)
rect(s, 0.55, 1.85, 6.10, 2.10, WHITE)
txb(s, 'PMax runs a single campaign across all Google inventory — Search, Display, YouTube, Gmail, Discover, and Maps — using AI to find the best placements automatically.\n\nFor Wellspring, the key advantage is YouTube reach for therapy content. PMax is the practical workaround for YouTube access while the Google Healthcare certificate application is pending.',
    0.72, 1.95, 5.78, 1.90, sz=11, clr=DARK)

rect(s, 6.90, 1.55, 5.95, 0.30, BLUE)
txb(s, 'WHY WE\'RE TESTING IT', 7.05, 1.58, 5.80, 0.25, sz=10, bold=True, clr=WHITE)
rect(s, 6.90, 1.85, 5.95, 2.10, WHITE)
why_pts = [
    'Only campaign type that reaches YouTube for therapy without Healthcare cert',
    'AI allocation finds intent signals that keyword-based DSA misses',
    'Captures "research phase" users who are not actively searching yet',
    'Needs 4–6 weeks to exit learning mode — launch in June, read in August',
]
for i, pt in enumerate(why_pts):
    oval(s, 7.05, 1.98 + i*0.46 + 0.12, 0.12, 0.12, BLUE)
    txb(s, pt, 7.28, 1.98 + i*0.46 + 0.02, 5.45, 0.40, sz=11, clr=DARK)

# Projections table
rect(s, 0.55, 4.10, 12.25, 0.32, DARK)
txb(s, 'PROJECTED ENGAGEMENT AT $550/MONTH',
    0.70, 4.14, 12.00, 0.26, sz=11, bold=True, clr=WHITE)

proj4 = [
    ('Search (PMax)',        '$5–8 CPC',    '68–110 clicks',      '—'),
    ('Display',              '$4–6 CPM',    '600–900 clicks',     '15,000–23,000 impressions'),
    ('YouTube (therapy)',    '$6–10 CPM',   '—',                  '8,000–14,000 views'),
    ('Gmail / Discover',     '$2–4 CPM',    '—',                  '5,000–8,000 impressions'),
    ('TOTAL',                'Blended',     '670–1,010 clicks',   '28,000–45,000 impressions'),
]
hdrs4 = ['Channel', 'Avg CPC / CPM', 'Clicks', 'Impressions / Views']
col_ws4 = [2.50, 2.50, 3.62, 3.63]
tbl4 = s.shapes.add_table(len(proj4)+1, 4, I(0.55), I(4.45), I(12.25), I(2.72)).table
for ci, cw in enumerate(col_ws4): tbl4.columns[ci].width = I(cw)
for ci, h in enumerate(hdrs4):
    cell = tbl4.cell(0, ci)
    set_cell_bg(cell, '4B3BC8'); set_cell_text(cell, h, sz=10, bold=True, color='FFFFFF')
for ri, row in enumerate(proj4):
    is_total = ri == len(proj4)-1
    bg = '1E1E2E' if is_total else ('EEF2FF' if ri % 2 == 0 else 'FFFFFF')
    tc = 'FFFFFF' if is_total else '1E1E2E'
    for ci, val in enumerate(row):
        cell = tbl4.cell(ri+1, ci)
        set_cell_bg(cell, bg)
        set_cell_text(cell, val, sz=10, bold=is_total or ci==0, color=tc)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5  Exp 2 — Local Service Ads
# ══════════════════════════════════════════════════════════════════════════════
s = new_slide(prs)
set_bg(s)
std_header(s, 'Experiment 2 — Local Service Ads (LSAs)',
           'June 2026  |  Budget: $300–$400/month  |  Platform: Google LSA (separate from Google Ads)')
std_footer(s, 5)

rect(s, 0.55, 1.05, 1.60, 0.34, PRIMARY)
txb(s, 'EXPERIMENT 2', 0.62, 1.09, 1.48, 0.26, sz=10, bold=True, clr=WHITE)
txb(s, 'Local Service Ads', 2.28, 1.02, 8.0, 0.45, sz=20, bold=True, clr=PRIMARY, font='Arial Black')

rect(s, 0.55, 1.55, 6.10, 0.30, PRIMARY)
txb(s, 'WHAT IT IS', 0.70, 1.58, 6.00, 0.25, sz=10, bold=True, clr=WHITE)
rect(s, 0.55, 1.85, 6.10, 2.10, WHITE)
txb(s, 'LSAs are Google\'s pay-per-lead product for service businesses. They appear ABOVE all regular Search Ads with a "Google Screened" badge. Wellspring only pays when someone calls or messages — not per click.\n\nManaged in a separate LSA dashboard. Requires licence verification, insurance, and background checks (2–4 week approval).',
    0.72, 1.95, 5.78, 1.90, sz=11, clr=DARK)

rect(s, 6.90, 1.55, 5.95, 0.30, BLUE)
txb(s, 'WHY WE\'RE TESTING IT', 7.05, 1.58, 5.80, 0.25, sz=10, bold=True, clr=WHITE)
rect(s, 6.90, 1.85, 5.95, 2.10, WHITE)
why5 = [
    'Position 0 — appears above our own paid search ads',
    'Pay per lead, not per click — better budget efficiency if lead quality is good',
    '"Google Screened" badge builds trust Wellspring currently lacks (near-zero reviews)',
    'Key risk: review count heavily influences LSA rank vs RCBM (2,273 reviews)',
]
for i, pt in enumerate(why5):
    oval(s, 7.05, 1.98 + i*0.46 + 0.12, 0.12, 0.12, BLUE)
    txb(s, pt, 7.28, 1.98 + i*0.46 + 0.02, 5.45, 0.40, sz=11, clr=DARK)

rect(s, 0.55, 4.10, 12.25, 0.32, DARK)
txb(s, 'PROJECTED ENGAGEMENT AT $350/MONTH',
    0.70, 4.14, 12.00, 0.26, sz=11, bold=True, clr=WHITE)

proj5 = [
    ('Impressions (position 0)',  'CPM N/A — shown above all ads',     '4,000–8,000 / month'),
    ('Leads (calls + messages)',  '$15–$30 per lead (pay-per-lead)',    '12–23 leads / month'),
    ('Cost model',                'No CPC — charged per lead received', 'Dispute invalid leads within 30 days'),
]
hdrs5 = ['Metric', 'Cost Basis', 'Projected Volume']
col_ws5 = [3.50, 4.62, 4.13]
tbl5 = s.shapes.add_table(len(proj5)+1, 3, I(0.55), I(4.45), I(12.25), I(2.72)).table
for ci, cw in enumerate(col_ws5): tbl5.columns[ci].width = I(cw)
for ci, h in enumerate(hdrs5):
    cell = tbl5.cell(0, ci)
    set_cell_bg(cell, '4B3BC8'); set_cell_text(cell, h, sz=10, bold=True, color='FFFFFF')
for ri, row in enumerate(proj5):
    bg = 'EEF2FF' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate(row):
        cell = tbl5.cell(ri+1, ci)
        set_cell_bg(cell, bg)
        set_cell_text(cell, val, sz=10, bold=(ci==0), color='4B3BC8' if ci==0 else '1E1E2E')

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6  Exp 3 — Competitor Conquest
# ══════════════════════════════════════════════════════════════════════════════
s = new_slide(prs)
set_bg(s)
std_header(s, 'Experiment 3 — Competitor Conquest',
           'July 2026  |  Budget: $200–$250/month  |  Platform: Google Search')
std_footer(s, 6)

rect(s, 0.55, 1.05, 1.60, 0.34, BLUE)
txb(s, 'EXPERIMENT 3', 0.62, 1.09, 1.48, 0.26, sz=10, bold=True, clr=WHITE)
txb(s, 'Competitor Conquest', 2.28, 1.02, 8.0, 0.45, sz=20, bold=True, clr=BLUE, font='Arial Black')

rect(s, 0.55, 1.55, 6.10, 0.30, BLUE)
txb(s, 'WHAT IT IS', 0.70, 1.58, 6.00, 0.25, sz=10, bold=True, clr=WHITE)
rect(s, 0.55, 1.85, 6.10, 2.10, WHITE)
txb(s, 'Bid on competitor brand-term keywords. When someone searches for a competitor by name, Wellspring\'s ad appears alongside.\n\nPrimary target: Great Lakes Psychology Group (GLPG) — they run active Google + Meta ads but have only 2.6★ reviews and weak brand trust. Anyone searching for them and finding a poor reputation is a qualified Wellspring therapy prospect.\n\nNote: you can bid on competitor names. You cannot use their name in the ad copy.',
    0.72, 1.95, 5.78, 1.90, sz=11, clr=DARK)

rect(s, 6.90, 1.55, 5.95, 0.30, BLUE)
txb(s, 'TARGET COMPETITORS', 7.05, 1.58, 5.80, 0.25, sz=10, bold=True, clr=WHITE)
rect(s, 6.90, 1.85, 5.95, 2.10, WHITE)
targets = [
    ('GLPG (Primary)',   '2.6★ / 47 reviews — confirmed Google + Meta spend. No Med Mgmt.'),
    ('Ellie Mental Health', 'Franchise model. Users often prefer private practice. Active ad budget.'),
    ('Helios Psychiatry', 'Direct Med Mgmt competitor. Overflow / waitlist searches are capturable.'),
]
for i, (name, reason) in enumerate(targets):
    top = 1.92 + i * 0.62
    rect(s, 6.90, top, 5.95, 0.55, LIGHT if i % 2 == 0 else WHITE)
    rect(s, 6.90, top, 0.10, 0.55, BLUE)
    txb(s, name,   7.12, top + 0.05, 5.60, 0.22, sz=11, bold=True, clr=BLUE)
    txb(s, reason, 7.12, top + 0.28, 5.60, 0.22, sz=10, clr=DARK)

rect(s, 0.55, 4.10, 12.25, 0.32, DARK)
txb(s, 'PROJECTED ENGAGEMENT AT $225/MONTH',
    0.70, 4.14, 12.00, 0.26, sz=11, bold=True, clr=WHITE)

proj6 = [
    ('Competitor brand keywords', '$1.50–$3.00 CPC', '75–150 clicks / month', '1,500–3,750 impressions'),
    ('Ad copy angle',             'N/A',              '"48-hour intake, no waitlist"', 'Differentiator vs competitor wait times'),
    ('TOTAL',                     '$2.25 avg CPC',    '75–150 clicks',         '1,500–3,750 impressions'),
]
hdrs6 = ['Keyword Type', 'Avg CPC', 'Est. Clicks', 'Est. Impressions']
col_ws6 = [3.20, 2.20, 3.42, 3.43]
tbl6 = s.shapes.add_table(len(proj6)+1, 4, I(0.55), I(4.45), I(12.25), I(2.72)).table
for ci, cw in enumerate(col_ws6): tbl6.columns[ci].width = I(cw)
for ci, h in enumerate(hdrs6):
    cell = tbl6.cell(0, ci)
    set_cell_bg(cell, '3B82F6'); set_cell_text(cell, h, sz=10, bold=True, color='FFFFFF')
for ri, row in enumerate(proj6):
    is_total = ri == len(proj6)-1
    bg = '1E1E2E' if is_total else ('EEF2FF' if ri % 2 == 0 else 'FFFFFF')
    tc = 'FFFFFF' if is_total else '1E1E2E'
    for ci, val in enumerate(row):
        cell = tbl6.cell(ri+1, ci)
        set_cell_bg(cell, bg)
        set_cell_text(cell, val, sz=10, bold=is_total or ci==0, color=tc)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7  Exp 4 — Display Remarketing
# ══════════════════════════════════════════════════════════════════════════════
s = new_slide(prs)
set_bg(s)
std_header(s, 'Experiment 4 — Display Remarketing',
           'July 2026  |  Budget: $150–$200/month  |  Platform: Google Display Network')
std_footer(s, 7)

rect(s, 0.55, 1.05, 1.60, 0.34, BLUE)
txb(s, 'EXPERIMENT 4', 0.62, 1.09, 1.48, 0.26, sz=10, bold=True, clr=WHITE)
txb(s, 'Display Remarketing', 2.28, 1.02, 8.0, 0.45, sz=20, bold=True, clr=BLUE, font='Arial Black')

rect(s, 0.55, 1.55, 6.10, 0.30, BLUE)
txb(s, 'WHAT IT IS', 0.70, 1.58, 6.00, 0.25, sz=10, bold=True, clr=WHITE)
rect(s, 0.55, 1.85, 6.10, 2.10, WHITE)
txb(s, 'Display banner ads shown only to people who have already visited the Wellspring website but did not convert. Ads appear across Google\'s network of 2M+ partner sites.\n\nThis is a brand recall play. Someone who searched, visited, and left — they\'re still in the consideration window. Staying visible to them at low cost ($3–5 CPM) keeps Wellspring top-of-mind until they are ready to book.',
    0.72, 1.95, 5.78, 1.90, sz=11, clr=DARK)

rect(s, 6.90, 1.55, 5.95, 0.30, BLUE)
txb(s, 'WHY WE\'RE TESTING IT', 7.05, 1.58, 5.80, 0.25, sz=10, bold=True, clr=WHITE)
rect(s, 6.90, 1.85, 5.95, 2.10, WHITE)
why7 = [
    'Cheapest way to stay visible to warm audiences ($3–5 CPM vs $5–8 CPC)',
    'Complements every other experiment — retargets people PMax and Search bring in',
    'Requires minimum ~300 users in the pixel pool — check current site traffic first',
    'This is an impressions play, not a direct lead play',
]
for i, pt in enumerate(why7):
    oval(s, 7.05, 1.98 + i*0.46 + 0.12, 0.12, 0.12, BLUE)
    txb(s, pt, 7.28, 1.98 + i*0.46 + 0.02, 5.45, 0.40, sz=11, clr=DARK)

rect(s, 0.55, 4.10, 12.25, 0.32, DARK)
txb(s, 'PROJECTED ENGAGEMENT AT $175/MONTH',
    0.70, 4.14, 12.00, 0.26, sz=11, bold=True, clr=WHITE)

proj7 = [
    ('Display banners (GDN)',     '$3–5 CPM',     '350–500 clicks',    '35,000–58,000 impressions'),
    ('Audience',                  'Website visitors who did not convert', 'Warm — already know Wellspring', ''),
    ('TOTAL',                     '$4 avg CPM',   '350–500 clicks',    '35,000–58,000 impressions'),
]
hdrs7 = ['Format', 'Cost Basis', 'Est. Clicks', 'Est. Impressions']
col_ws7 = [3.20, 3.42, 2.62, 3.01]
tbl7 = s.shapes.add_table(len(proj7)+1, 4, I(0.55), I(4.45), I(12.25), I(2.72)).table
for ci, cw in enumerate(col_ws7): tbl7.columns[ci].width = I(cw)
for ci, h in enumerate(hdrs7):
    cell = tbl7.cell(0, ci)
    set_cell_bg(cell, '3B82F6'); set_cell_text(cell, h, sz=10, bold=True, color='FFFFFF')
for ri, row in enumerate(proj7):
    is_total = ri == len(proj7)-1
    bg = '1E1E2E' if is_total else ('EEF2FF' if ri % 2 == 0 else 'FFFFFF')
    tc = 'FFFFFF' if is_total else '1E1E2E'
    for ci, val in enumerate(row):
        cell = tbl7.cell(ri+1, ci)
        set_cell_bg(cell, bg)
        set_cell_text(cell, val, sz=10, bold=is_total or ci==0, color=tc)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8  Exp 5 — Bing / Microsoft Ads
# ══════════════════════════════════════════════════════════════════════════════
s = new_slide(prs)
set_bg(s)
std_header(s, 'Experiment 5 — Bing / Microsoft Ads',
           'August 2026  |  Budget: $150–$200/month  |  Platform: Microsoft Advertising')
std_footer(s, 8)

rect(s, 0.55, 1.05, 1.60, 0.34, INDIGO)
txb(s, 'EXPERIMENT 5', 0.62, 1.09, 1.48, 0.26, sz=10, bold=True, clr=WHITE)
txb(s, 'Bing / Microsoft Ads', 2.28, 1.02, 8.0, 0.45, sz=20, bold=True, clr=INDIGO, font='Arial Black')

rect(s, 0.55, 1.55, 6.10, 0.30, INDIGO)
txb(s, 'WHAT IT IS', 0.70, 1.58, 6.00, 0.25, sz=10, bold=True, clr=WHITE)
rect(s, 0.55, 1.85, 6.10, 2.10, WHITE)
txb(s, 'Run the same keywords as current Google Search campaigns on Microsoft\'s Bing search engine. Setup takes ~30 minutes via the Google Ads import tool — no new copy or keyword research needed.\n\nBing holds 6–8% of US search market share nationally but over-indexes for 45+ users in suburban Michigan — aligning closely with Wellspring\'s commercially insured target demographic.',
    0.72, 1.95, 5.78, 1.90, sz=11, clr=DARK)

rect(s, 6.90, 1.55, 5.95, 0.30, INDIGO)
txb(s, 'WHY WE\'RE TESTING IT', 7.05, 1.58, 5.80, 0.25, sz=10, bold=True, clr=WHITE)
rect(s, 6.90, 1.85, 5.95, 2.10, WHITE)
why8 = [
    'CPCs typically 30–50% lower than Google for the same keywords',
    '45+ demographic skew = higher commercial insurance prevalence in audience',
    'Lowest-effort experiment — import from Google Ads in one click',
    'Bing users are less price-sensitive, less likely to be on Medicaid',
]
for i, pt in enumerate(why8):
    oval(s, 7.05, 1.98 + i*0.46 + 0.12, 0.12, 0.12, INDIGO)
    txb(s, pt, 7.28, 1.98 + i*0.46 + 0.02, 5.45, 0.40, sz=11, clr=DARK)

rect(s, 0.55, 4.10, 12.25, 0.32, DARK)
txb(s, 'PROJECTED ENGAGEMENT AT $175/MONTH',
    0.70, 4.14, 12.00, 0.26, sz=11, bold=True, clr=WHITE)

proj8 = [
    ('Search (Bing)',           '$3–5 CPC (40% lower than Google)',  '35–58 clicks / month', '700–1,400 impressions'),
    ('Demographic skew',        '45+ suburban Michigan',             'Commercially insured',  'Lower Medicaid overlap than Google'),
    ('TOTAL',                   '$4 avg CPC',                        '35–58 clicks',         '700–1,400 impressions'),
]
hdrs8 = ['Channel', 'Cost Basis', 'Est. Clicks', 'Est. Impressions']
col_ws8 = [2.50, 3.62, 2.62, 3.51]
tbl8 = s.shapes.add_table(len(proj8)+1, 4, I(0.55), I(4.45), I(12.25), I(2.72)).table
for ci, cw in enumerate(col_ws8): tbl8.columns[ci].width = I(cw)
for ci, h in enumerate(hdrs8):
    cell = tbl8.cell(0, ci)
    set_cell_bg(cell, '6366F1'); set_cell_text(cell, h, sz=10, bold=True, color='FFFFFF')
for ri, row in enumerate(proj8):
    is_total = ri == len(proj8)-1
    bg = '1E1E2E' if is_total else ('EEF2FF' if ri % 2 == 0 else 'FFFFFF')
    tc = 'FFFFFF' if is_total else '1E1E2E'
    for ci, val in enumerate(row):
        cell = tbl8.cell(ri+1, ci)
        set_cell_bg(cell, bg)
        set_cell_text(cell, val, sz=10, bold=is_total or ci==0, color=tc)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9  3-Month Timeline (Gantt)
# ══════════════════════════════════════════════════════════════════════════════
s = new_slide(prs)
set_bg(s)
std_header(s, '3-Month Experiment Timeline',
           'When each experiment launches, runs, and produces readable data')
std_footer(s, 9)

# Month headers
months = ['JUNE 2026', 'JULY 2026', 'AUGUST 2026']
month_colors = ['4B3BC8','3B82F6','6366F1']
col_start = 4.10
col_w = 2.90
for i, (m, mc) in enumerate(zip(months, month_colors)):
    l = col_start + i * col_w
    rect(s, l, 1.05, col_w - 0.08, 0.42, hc(mc))
    txb(s, m, l+0.10, 1.09, col_w-0.20, 0.32, sz=12, bold=True, clr=WHITE, align=PP_ALIGN.CENTER)

# Experiment rows
exps = [
    (PRIMARY,  'Exp 1 — Performance Max',       [True,  True,  True ]),  # Jun-Aug (learning Jun, read Aug)
    (PRIMARY,  'Exp 2 — Local Service Ads',      [True,  True,  True ]),  # Jun-Aug
    (BLUE,     'Exp 3 — Competitor Conquest',    [False, True,  True ]),  # Jul-Aug
    (BLUE,     'Exp 4 — Display Remarketing',    [False, True,  True ]),  # Jul-Aug
    (INDIGO,   'Exp 5 — Bing / Microsoft Ads',   [False, False, True ]),  # Aug only
]
notes = [
    'Learning mode Jun–Jul. First read: Aug.',
    'Start verification in June. Go live: June or when 15+ reviews reached.',
    'Launch after conquest keyword list is finalised.',
    'Requires ~300 users in pixel pool. Confirm site traffic first.',
    'Import from Google Ads. 30-min setup.',
]
for i, ((clr, name, active), note) in enumerate(zip(exps, notes)):
    top = 1.58 + i * 1.02
    # Row label
    rect(s, 0.30, top, 3.72, 0.56, LIGHT if i % 2 == 0 else WHITE)
    rect(s, 0.30, top, 0.10, 0.56, clr)
    txb(s, name, 0.52, top + 0.10, 3.40, 0.36, sz=11, bold=True, clr=DARK)
    # Month bars
    for j, is_active in enumerate(active):
        l = col_start + j * col_w
        if is_active:
            bar_clr = clr
            label = 'LEARNING' if (name == 'Exp 1 — Performance Max' and j == 0) else 'ACTIVE'
            rect(s, l+0.08, top+0.10, col_w-0.22, 0.36, bar_clr)
            txb(s, label, l+0.08, top+0.12, col_w-0.22, 0.30,
                sz=9, bold=True, clr=WHITE, align=PP_ALIGN.CENTER)
        else:
            rect(s, l+0.08, top+0.10, col_w-0.22, 0.36, DGRAY)
    # Note below bar
    txb(s, note, 0.52, top + 0.62, 12.55, 0.28, sz=9, italic=True, clr=GRAY)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10  Budget Summary & Projected Engagement
# ══════════════════════════════════════════════════════════════════════════════
s = new_slide(prs)
set_bg(s)
std_header(s, 'Budget Ask & Projected Engagement Impact',
           'Incremental investment on top of current campaigns — Q3 total ask and expected engagement output')
std_footer(s, 10)

# Current vs proposed
rect(s, 0.55, 1.05, 5.80, 0.35, GRAY)
txb(s, 'CURRENT MONTHLY SPEND (EXISTING CAMPAIGNS)', 0.70, 1.09, 5.55, 0.28, sz=10, bold=True, clr=WHITE)
rect(s, 0.55, 1.40, 5.80, 1.20, WHITE)
txb(s, '~$1,800–$2,000', 0.72, 1.52, 5.40, 0.62, sz=28, bold=True, clr=DARK, font='Arial Black')
txb(s, 'Generic Search + DSA + Regional Search', 0.72, 2.12, 5.40, 0.35, sz=11, clr=GRAY)

rect(s, 6.90, 1.05, 5.95, 0.35, PRIMARY)
txb(s, 'PROPOSED Q3 EXPERIMENT ADD-ON', 7.05, 1.09, 5.72, 0.28, sz=10, bold=True, clr=WHITE)
rect(s, 6.90, 1.40, 5.95, 1.20, WHITE)
txb(s, '+$1,100–$1,450 / mo', 7.08, 1.52, 5.60, 0.62, sz=26, bold=True, clr=PRIMARY, font='Arial Black')
txb(s, 'June (PMax + LSAs)  |  +$350–$450 July  |  +$150–$200 Aug', 7.08, 2.12, 5.60, 0.35, sz=10, clr=GRAY)

# Q3 total engagement projection
rect(s, 0.55, 2.80, 12.25, 0.35, DARK)
txb(s, 'CUMULATIVE Q3 PROJECTED ENGAGEMENT (ALL 5 EXPERIMENTS)',
    0.70, 2.84, 12.00, 0.28, sz=11, bold=True, clr=WHITE)

kpis10 = [
    (PRIMARY, '130K–220K',  'Incremental Impressions'),
    (BLUE,    '1,200–1,800','Incremental Clicks'),
    (INDIGO,  '36–70',      'LSA Leads (pay-per-lead)'),
    (GREEN,   '3 months',   'Time to First Read'),
]
for i, (clr, val, label) in enumerate(kpis10):
    l = 0.55 + i * 3.08
    rect(s, l, 3.20, 2.85, 0.38, clr)
    txb(s, label.upper(), l+0.12, 3.22, 2.62, 0.32, sz=9, bold=True, clr=WHITE)
    rect(s, l, 3.58, 2.85, 0.88, WHITE)
    txb(s, val, l+0.12, 3.65, 2.62, 0.76, sz=22, bold=True, clr=clr, font='Arial Black')

# Month-by-month table
rect(s, 0.55, 4.60, 12.25, 0.32, DARK)
txb(s, 'MONTH-BY-MONTH BUDGET RAMP',
    0.70, 4.64, 12.00, 0.26, sz=11, bold=True, clr=WHITE)

budget_rows = [
    ('June 2026',    'PMax ($550) + LSAs ($350)',                                  '$900–$1,000',  '$2,700–$3,000'),
    ('July 2026',    '+ Competitor Conquest ($225) + Display Retargeting ($175)',  '$1,300–$1,450','$3,100–$3,450'),
    ('August 2026',  '+ Bing / Microsoft Ads ($175)',                              '$1,450–$1,650','$3,250–$3,650'),
    ('Q3 TOTAL',     '5 experiments across 3 months',                             '$4,650–$5,100 (test)',  '~$9,050–$10,100 (combined)'),
]
hdrs10 = ['Month', 'Experiments Running', 'Test Budget', 'Total Monthly Spend']
col_ws10 = [1.60, 5.40, 2.00, 3.25]
tbl10 = s.shapes.add_table(len(budget_rows)+1, 4, I(0.55), I(4.95), I(12.25), I(2.22)).table
for ci, cw in enumerate(col_ws10): tbl10.columns[ci].width = I(cw)
for ci, h in enumerate(hdrs10):
    cell = tbl10.cell(0, ci)
    set_cell_bg(cell, '4B3BC8'); set_cell_text(cell, h, sz=10, bold=True, color='FFFFFF')
for ri, row in enumerate(budget_rows):
    is_total = ri == len(budget_rows)-1
    bg = '1E1E2E' if is_total else ('EEF2FF' if ri % 2 == 0 else 'FFFFFF')
    tc = 'FFFFFF' if is_total else '1E1E2E'
    for ci, val in enumerate(row):
        cell = tbl10.cell(ri+1, ci)
        set_cell_bg(cell, bg)
        set_cell_text(cell, val, sz=10, bold=is_total or ci==0, color=tc)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 11  Next Steps
# ══════════════════════════════════════════════════════════════════════════════
s = new_slide(prs)
set_bg(s)
std_header(s, 'Next Steps',
           'What needs to happen in the next two weeks to keep the Q3 roadmap on track')
std_footer(s, 11)

nsteps = [
    (PRIMARY, '1', 'Approve Q3 Experiment Budget',       'Damco + Client', 'This week',
     'Confirm $1,100–$1,450/month incremental budget for June experiments (PMax + LSAs). This allows campaign setup to begin immediately. July and August add-ons can be approved monthly based on early results.'),
    (BLUE,    '2', 'Start LSA Account Verification',     'Damco',          'This week',
     'Create LSA account and upload verification documents. Approval takes 2–4 weeks — starting now ensures the account is live before July.'),
    (INDIGO,  '3', 'Launch Google Review Programme',     'Wellspring',     'This week',
     'Activate post-appointment SMS/email review outreach. Target: 15+ reviews before LSA go-live. This is the single action that determines LSA rank quality — cannot be substituted by ad spend.'),
]
for i, (clr, num, title, owner, timing, body) in enumerate(nsteps):
    top = 1.05 + i * 1.98
    rect(s, 0.55, top, 0.65, 1.78, clr)
    txb(s, num, 0.55, top + 0.48, 0.65, 0.82, sz=32, bold=True, clr=WHITE,
        align=PP_ALIGN.CENTER, font='Arial Black')
    rect(s, 1.25, top, 11.55, 1.78, WHITE)
    rect(s, 9.55, top + 0.14, 1.45, 0.28, LIGHT)
    txb(s, f'Owner: {owner}', 9.55, top + 0.15, 1.45, 0.26, sz=9, bold=True,
        clr=clr, align=PP_ALIGN.CENTER)
    rect(s, 11.08, top + 0.14, 1.60, 0.28, LIGHT)
    txb(s, timing, 11.08, top + 0.15, 1.60, 0.26, sz=9, bold=True,
        clr=clr, align=PP_ALIGN.CENTER)
    txb(s, title, 1.42, top + 0.14, 8.00, 0.40, sz=14, bold=True, clr=clr)
    txb(s, body,  1.42, top + 0.57, 11.22, 1.10, sz=11, clr=DARK)

# ─────────────────────────────────────────────────────────────────────────────
out = Path(__file__).parent / '01_Reports' / 'Wellspring_Q3_Experiment_Roadmap_v2.pptx'
prs.save(out)
print(f'Saved: {out}')
