"""
Generate Wellspring LSA Experiment Proposal deck.
Matches QBR Q1 2026 visual style: F5F6FA bg, 4B3BC8 purple, Arial Black headings.
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

# ── Palette ──────────────────────────────────────────────────────────────────
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

def hc(hex_str):
    """Hex string to RGBColor."""
    r, g, b = int(hex_str[0:2],16), int(hex_str[2:4],16), int(hex_str[4:6],16)
    return RGBColor(r, g, b)

# ── Low-level helpers ─────────────────────────────────────────────────────────

def set_bg(slide, color=None):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color or BG

def rect(slide, l, t, w, h, color, line_color=None):
    shp = slide.shapes.add_shape(MSO.RECTANGLE, I(l), I(t), I(w), I(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    if line_color:
        shp.line.color.rgb = line_color
    else:
        shp.line.fill.background()
    return shp

def oval(slide, l, t, w, h, color):
    shp = slide.shapes.add_shape(MSO.OVAL, I(l), I(t), I(w), I(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return shp

def txb(slide, text, l, t, w, h, sz=12, bold=False, clr=None,
        align=PP_ALIGN.LEFT, font='Calibri', italic=False):
    box = slide.shapes.add_textbox(I(l), I(t), I(w), I(h))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(sz)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = clr or DARK
    return box

def set_cell_bg(cell, color_hex):
    tc = cell._tc
    tcPr = tc.find(qn('a:tcPr'))
    if tcPr is None:
        tcPr = etree.SubElement(tc, qn('a:tcPr'))
    for tag in ['a:solidFill','a:gradFill','a:noFill','a:pattFill','a:blipFill']:
        for elem in tcPr.findall(qn(tag)):
            tcPr.remove(elem)
    sf = etree.SubElement(tcPr, qn('a:solidFill'))
    sc = etree.SubElement(sf, qn('a:srgbClr'))
    sc.set('val', color_hex)

def set_cell_text(cell, text, sz=11, bold=False, color='1E1E2E',
                  align=PP_ALIGN.LEFT, font='Calibri'):
    tf = cell.text_frame
    # clear existing paragraphs after first
    for para in tf.paragraphs[1:]:
        para._p.getparent().remove(para._p)
    p = tf.paragraphs[0]
    for run in p.runs:
        run._r.getparent().remove(run._r)
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(sz)
    run.font.bold = bold
    run.font.color.rgb = hc(color)

# ── Slide chrome ──────────────────────────────────────────────────────────────

def std_header(slide, title, subtitle=None):
    rect(slide, 0.0, 0.0, 13.33, 0.82, PRIMARY)
    txb(slide, title, 0.55, 0.10, 10.5, 0.62, sz=22, bold=True, clr=WHITE, font='Arial Black')
    if subtitle:
        txb(slide, subtitle, 0.55, 0.60, 12.00, 0.28, sz=10, clr=LIGHT2)

def std_footer(slide, page_num):
    rect(slide, 12.72, 7.10, 0.50, 0.34, PRIMARY)
    txb(slide, str(page_num), 12.72, 7.10, 0.50, 0.34, sz=11, bold=True, clr=WHITE,
        align=PP_ALIGN.CENTER)
    txb(slide, 'Copyright © 2025 Damco Group. All Rights Reserved.',
        0.30, 7.24, 11.0, 0.22, sz=9, clr=GRAY)

def new_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])  # blank

# ── Build presentation ────────────────────────────────────────────────────────

prs = Presentation()
prs.slide_width  = I(13.33)
prs.slide_height = I(7.50)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 1  Cover
# ─────────────────────────────────────────────────────────────────────────────
s = new_slide(prs)
set_bg(s)

# Decorative background circles (match QBR cover)
for (l, t, sz_c, col) in [(7.8, -1.2, 5.0, 'EEF0FF'), (9.3, 0.6, 6.2, 'C9CBF0')]:
    shp = s.shapes.add_shape(MSO.OVAL, I(l), I(t), I(sz_c), I(sz_c))
    shp.fill.solid(); shp.fill.fore_color.rgb = hc(col); shp.line.fill.background()

txb(s, 'Damco Digital × Wellspring', 1.5, 1.95, 10.3, 0.62, sz=18, bold=True, clr=DARK)
txb(s, 'Local Service Ads', 1.5, 2.60, 10.3, 1.20, sz=54, bold=True, clr=PRIMARY, font='Arial Black')
txb(s, 'Q3 2026 Experiment Proposal', 1.5, 3.90, 10.3, 0.60, sz=20, clr=GRAY)
txb(s, 'Wellspring Therapeutic Partners  |  May 2026', 1.5, 4.52, 10.3, 0.48, sz=15, clr=GRAY)
txb(s, 'Copyright © 2025 Damco Group. All Rights Reserved.',
    0.30, 7.24, 11.0, 0.22, sz=9, clr=GRAY)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 2  What Are LSAs? — 3 pillars
# ─────────────────────────────────────────────────────────────────────────────
s = new_slide(prs)
set_bg(s)
std_header(s, 'What Are Local Service Ads?',
           'A Google product built specifically for service businesses — completely separate from regular Search Ads')
std_footer(s, 2)

pillars = [
    (PRIMARY,  'POSITION',
     'Appear ABOVE all regular Search Ads and organic results.\nTrue position zero — the first thing a user sees.'),
    (BLUE,     'PAYMENT MODEL',
     'Pay per lead (call or message received), not per click.\nNo budget wasted on people who click and leave.'),
    (INDIGO,   'TRUST SIGNAL',
     '"Google Screened" badge shown on the profile.\nGoogle verifies business licence, insurance, and practitioner background.'),
]
for i, (clr, label, body) in enumerate(pillars):
    l = 0.55 + i * 4.25
    rect(s, l, 1.10, 4.00, 0.45, clr)
    txb(s, label, l+0.15, 1.13, 3.72, 0.40, sz=13, bold=True, clr=WHITE)
    rect(s, l, 1.55, 4.00, 4.30, WHITE)
    txb(s, body, l+0.18, 1.75, 3.66, 3.80, sz=14, clr=DARK)

# Bottom insight
rect(s, 0.0, 6.55, 13.33, 0.60, LIGHT)
rect(s, 0.0, 6.55, 0.10, 0.60, PRIMARY)
txb(s, 'Key difference from what you run today: Wellspring pays only when someone actually calls or messages — not just for ad impressions or clicks.',
    0.28, 6.63, 12.85, 0.40, sz=12, bold=True, clr=PRIMARY)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 3  LSAs vs Current Campaigns — comparison table
# ─────────────────────────────────────────────────────────────────────────────
s = new_slide(prs)
set_bg(s)
std_header(s, 'LSAs vs. Your Current Google Campaigns',
           'How Local Service Ads differ from the Generic Search and DSA campaigns running now')
std_footer(s, 3)

rows_data = [
    ('',                  'Generic Search + DSA (current)',       'Local Service Ads'),
    ('You pay for',       'Every click',                          'Calls + messages only'),
    ('Ad position',       'Below LSAs on the page',               'Above everything — position 0'),
    ('Keyword control',   'Full — you bid on specific keywords',  'None — Google matches by category'),
    ('Ad creative',       'Headlines, descriptions, URL',         'Your business profile (name, reviews, phone)'),
    ('Budget structure',  'Daily budget, full CPC control',       'Weekly budget, no CPC bidding'),
    ('Managed in',        'Google Ads dashboard',                 'Separate LSA app / dashboard'),
    ('Trust signal',      'None',                                 '"Google Screened" badge'),
    ('Invalid leads',     'Cannot dispute',                       'Dispute within 30 days for credit'),
]

col_ws = [2.75, 4.75, 4.75]
tbl_obj = s.shapes.add_table(len(rows_data), 3, I(0.55), I(1.00), I(12.25), I(6.10))
tbl = tbl_obj.table
for ci, cw in enumerate(col_ws):
    tbl.columns[ci].width = I(cw)

for ri, row in enumerate(rows_data):
    for ci, val in enumerate(row):
        cell = tbl.cell(ri, ci)
        if ri == 0:
            bgs = ['F5F6FA', '4B3BC8', '3B82F6']
            set_cell_bg(cell, bgs[ci])
            clr_t = 'F5F6FA' if ci == 0 else 'FFFFFF'
            set_cell_text(cell, val, sz=12, bold=True, color=clr_t, align=PP_ALIGN.CENTER)
        else:
            bg = 'EEF2FF' if ri % 2 == 1 else 'FFFFFF'
            set_cell_bg(cell, bg)
            if ci == 0:
                set_cell_text(cell, val, sz=11, bold=True, color='4B3BC8')
            else:
                set_cell_text(cell, val, sz=11, color='1E1E2E')

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 4  Setup Process — 5 steps
# ─────────────────────────────────────────────────────────────────────────────
s = new_slide(prs)
set_bg(s)
std_header(s, 'How to Set It Up',
           'Five steps from account creation to first live lead — allow 2–4 weeks for verification')
std_footer(s, 4)

steps = [
    (PRIMARY, '1', 'Create the LSA Account',
     'Go to ads.google.com/local-services-ads. Separate from Google Ads but linked. Takes ~15 minutes to register.'),
    (PRIMARY, '2', 'Build the Business Profile',
     'Set business name, addresses (Troy + Clinton Twp), phone, hours, and service category: "Therapist" or "Mental Health Counselor".'),
    (BLUE,    '3', 'Complete Verification  (2–4 weeks)',
     'Upload business licence, professional liability insurance, and submit practitioners for background checks. Google uses a third-party verifier.'),
    (BLUE,    '4', 'Set Weekly Budget & Hours',
     'Set a weekly lead volume target or spend cap. Also set your lead acceptance hours (e.g. Mon–Fri 9am–6pm). Leads outside hours are not charged.'),
    (INDIGO,  '5', 'Go Live — Manage Leads Daily',
     'Calls arrive via Google forwarding number (recorded). Messages via the LSA app. Mark each lead: Booked / Not a Fit. Dispute invalid leads within 30 days.'),
]

for i, (clr, num, title, body) in enumerate(steps):
    top = 1.02 + i * 1.16
    oval(s, 0.55, top + 0.22, 0.40, 0.40, clr)
    txb(s, num, 0.55, top + 0.20, 0.40, 0.40, sz=12, bold=True, clr=WHITE, align=PP_ALIGN.CENTER)
    if i < len(steps) - 1:
        rect(s, 0.72, top + 0.62, 0.06, 0.56, LIGHT2)
    txb(s, title, 1.10, top + 0.10, 11.80, 0.38, sz=13, bold=True, clr=DARK)
    txb(s, body,  1.10, top + 0.48, 11.80, 0.60, sz=11, clr=GRAY)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 5  Eligibility
# ─────────────────────────────────────────────────────────────────────────────
s = new_slide(prs)
set_bg(s)
std_header(s, 'Eligibility for Wellspring',
           'What qualifies, what does not, and what needs confirmation before launch')
std_footer(s, 5)

# Left: Eligible
rect(s, 0.55, 1.05, 5.90, 0.40, PRIMARY)
txb(s, '✓  ELIGIBLE FOR LSAs', 0.72, 1.09, 5.60, 0.34, sz=13, bold=True, clr=WHITE)
elig = [
    ('Therapy & Counselling', 'Both "Mental Health Counselor" and "Therapist" are supported LSA categories in Michigan.'),
    ('Troy + Clinton Township', 'Both Michigan metro service areas are fully covered by LSA geo-targeting.'),
    ('Private practice model', 'Appointment-based service businesses are the exact use case LSAs were built for.'),
    ('"Google Screened" badge', 'Available after licence + insurance + background check verification is complete.'),
]
for i, (title, body) in enumerate(elig):
    top = 1.55 + i * 1.22
    rect(s, 0.55, top, 5.90, 1.10, LIGHT)
    rect(s, 0.55, top, 0.10, 1.10, PRIMARY)
    txb(s, title, 0.82, top + 0.10, 5.45, 0.35, sz=12, bold=True, clr=PRIMARY)
    txb(s, body,  0.82, top + 0.45, 5.45, 0.55, sz=11, clr=DARK)

# Right: Grey area
rect(s, 7.00, 1.05, 5.90, 0.40, INDIGO)
txb(s, '⚠  GREY AREA / LIMITATIONS', 7.17, 1.09, 5.60, 0.34, sz=13, bold=True, clr=WHITE)
grey = [
    ('Medication Management', 'Prescribing/NP services sit in a restricted healthcare sub-category. LSA profile should be set under therapy only.'),
    ('No keyword control', 'Cannot exclude terms the way you do in Search. Google decides which queries trigger the LSA profile.'),
    ('Reviews are critical', 'LSA ranking is heavily review-driven. Wellspring currently has near-zero reviews. This is the biggest launch risk.'),
]
amber_red = [INDIGO, AMBER, RED]
for i, (title, body) in enumerate(grey):
    top = 1.55 + i * 1.62
    bg_col = hc('FFF3EE') if i > 0 else LIGHT
    rect(s, 7.00, top, 5.90, 1.50, bg_col)
    rect(s, 7.00, top, 0.10, 1.50, amber_red[i])
    txb(s, title, 7.25, top + 0.12, 5.45, 0.35, sz=12, bold=True, clr=amber_red[i])
    txb(s, body,  7.25, top + 0.50, 5.45, 0.88, sz=11, clr=DARK)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 6  Budget & Engagement Projections
# ─────────────────────────────────────────────────────────────────────────────
s = new_slide(prs)
set_bg(s)
std_header(s, 'Budget & Engagement Projections',
           'Estimated impact at $350/month — framed as engagement (impressions + leads), not conversions')
std_footer(s, 6)

# KPI cards
kpis = [
    (PRIMARY, '$350',       'Monthly Budget'),
    (BLUE,    '4K–8K', 'Impressions / Month'),
    (INDIGO,  '$15–$30', 'Cost Per Lead (LSA avg)'),
    (GREEN,   '12–23', 'Leads / Month'),
]
for i, (clr, val, label) in enumerate(kpis):
    l = 0.55 + i * 3.08
    rect(s, l, 1.05, 2.85, 0.40, clr)
    txb(s, label.upper(), l+0.12, 1.08, 2.62, 0.35, sz=10, bold=True, clr=WHITE)
    rect(s, l, 1.45, 2.85, 1.00, WHITE)
    txb(s, val, l+0.12, 1.55, 2.62, 0.85, sz=26, bold=True, clr=clr, font='Arial Black')

# Comparison table
rect(s, 0.55, 2.65, 12.25, 0.35, DARK)
txb(s, 'Impressions & Reach: LSAs vs Current Campaigns',
    0.70, 2.69, 12.00, 0.28, sz=12, bold=True, clr=WHITE)

comp_rows = [
    ('Generic Search',           '$363–$699 / week', '~800–1,400 impr. / week', 'Pay per click',             '4–6% CTR'),
    ('DSA Campaign',              'Included above',        '~700–1,100 impr. / week', 'Pay per click',             '6–9% CTR'),
    ('LSAs (projected at $350/mo)', '$87.50 / week',       '~1,000–2,000 impr. / week', 'Pay per lead (no CPC)', 'N/A'),
]
hdrs = ['Campaign', 'Weekly Budget', 'Est. Impressions / Week', 'Cost Model', 'CTR']
col_ws2 = [2.75, 2.10, 2.90, 2.50, 2.00]

tbl2 = s.shapes.add_table(len(comp_rows)+1, 5, I(0.55), I(3.10), I(12.25), I(3.65)).table
for ci, cw in enumerate(col_ws2):
    tbl2.columns[ci].width = I(cw)
for ci, h in enumerate(hdrs):
    cell = tbl2.cell(0, ci)
    set_cell_bg(cell, '4B3BC8')
    set_cell_text(cell, h, sz=11, bold=True, color='FFFFFF')
for ri, row in enumerate(comp_rows):
    bg = 'EEF2FF' if ri % 2 == 0 else 'FFFFFF'
    for ci, val in enumerate(row):
        cell = tbl2.cell(ri+1, ci)
        set_cell_bg(cell, bg)
        bold = ci == 0
        clr_t = '4B3BC8' if ci == 0 else '1E1E2E'
        set_cell_text(cell, val, sz=11, bold=bold, color=clr_t)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 7  The Reviews Problem
# ─────────────────────────────────────────────────────────────────────────────
s = new_slide(prs)
set_bg(s)
std_header(s, 'The Key Limitation: Reviews',
           'LSA ranking is driven by Google review count and rating — this is where Wellspring has a structural gap')
std_footer(s, 7)

# Warning banner
rect(s, 0.55, 1.02, 12.25, 0.75, hc('FFF3CD'))
rect(s, 0.55, 1.02, 0.14, 0.75, AMBER)
txb(s, '⚠  LSAs without reviews are structurally weak. A user scans profile cards in under 3 seconds. If your card shows no reviews next to RCBM\'s 4.7★ / 2,273 reviews, they click RCBM.',
    0.88, 1.10, 11.80, 0.58, sz=12, clr=DARK)

# Competitor comparison
rect(s, 0.55, 1.95, 12.25, 0.38, DARK)
txb(s, 'What a user sees when comparing LSA profiles searching for a therapist in Troy, MI',
    0.70, 1.99, 12.00, 0.30, sz=12, bold=True, clr=WHITE)

comps = [
    (PRIMARY, 'Rochester Ctr for Behavioral Medicine (RCBM)',    '4.7 ★', '2,273 reviews', 'STRONG'),
    (BLUE,    'Helios Psychiatry & Counseling',                   '4.3 ★', '205 reviews',   'GOOD'),
    (RED,     'Wellspring (current state)',                        'No rating',  '0 reviews',     'CRITICAL GAP'),
]
for i, (clr, name, rating, reviews, status) in enumerate(comps):
    top = 2.48 + i * 1.50
    rect(s, 0.55, top, 12.25, 1.32, WHITE)
    rect(s, 0.55, top, 0.12, 1.32, clr)
    txb(s, name,    0.82, top + 0.14, 6.00, 0.40, sz=14, bold=True, clr=DARK)
    txb(s, rating,  7.00, top + 0.14, 2.00, 0.40, sz=14, bold=True, clr=clr)
    txb(s, reviews, 9.20, top + 0.14, 2.20, 0.40, sz=14, clr=GRAY)
    rect(s, 11.55, top + 0.18, 1.10, 0.30, clr)
    txb(s, status, 11.55, top + 0.18, 1.10, 0.30, sz=9, bold=True, clr=WHITE, align=PP_ALIGN.CENTER)
    note = ('Reviews are the #1 LSA ranking and trust signal.' if i == 2
            else 'Well-established review presence — strong LSA competitor.')
    txb(s, note, 0.82, top + 0.72, 12.00, 0.45, sz=11, italic=True, clr=GRAY)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 8  Phased Recommendation
# ─────────────────────────────────────────────────────────────────────────────
s = new_slide(prs)
set_bg(s)
std_header(s, 'Recommended Phased Approach',
           'Build the review foundation first, then activate LSAs at full strength')
std_footer(s, 8)

phases = [
    (PRIMARY, 'PHASE 1', 'June – July 2026', 'Build the Review Foundation',
     ['Launch Google Review SMS/email programme (25 reviews in 90 days)',
      'Target: 15–20 reviews before LSA go-live',
      'Focus: post-appointment outreach by Wellspring front desk',
      'In parallel: Create LSA account + begin verification (takes 2–4 weeks)',
      'Pre-approve $350/month LSA budget, conditional on review milestone']),
    (BLUE, 'PHASE 2', 'August 2026  (or when 15+ reviews reached)', 'Go Live on LSAs',
     ['Activate LSA campaign at $350/month',
      'Service areas: Troy, MI + Clinton Township, MI',
      'Category: Therapist / Mental Health Counselor',
      'Manage leads via LSA app daily — dispute invalid leads within 30 days',
      'Measure vs benchmark: 12–23 leads/month at $15–$30 CPL']),
]
for i, (clr, label, timing, title, bullets) in enumerate(phases):
    l = 0.55 + i * 6.45
    rect(s, l, 1.05, 6.15, 0.44, clr)
    txb(s, f'{label}  |  {timing}', l+0.15, 1.10, 5.85, 0.36, sz=12, bold=True, clr=WHITE)
    rect(s, l, 1.49, 6.15, 5.40, WHITE)
    txb(s, title, l+0.18, 1.62, 5.82, 0.42, sz=15, bold=True, clr=clr)
    for j, b in enumerate(bullets):
        top = 2.15 + j * 0.84
        oval(s, l+0.18, top + 0.14, 0.14, 0.14, clr)
        txb(s, b, l+0.42, top + 0.05, 5.62, 0.70, sz=11, clr=DARK)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 9  Next Steps
# ─────────────────────────────────────────────────────────────────────────────
s = new_slide(prs)
set_bg(s)
std_header(s, 'Next Steps',
           'Three actions to progress this week — one Damco-owned, two Wellspring-owned')
std_footer(s, 9)

actions = [
    (PRIMARY, '1', 'Start LSA Verification Now', 'Damco', 'This week',
     'Create the LSA account at ads.google.com/local-services-ads. Begin uploading business licence and insurance documents. Verification takes 2–4 weeks — start the clock now regardless of review count, so the account is approved when Phase 2 is ready.'),
    (BLUE, '2', 'Launch Google Review Programme', 'Wellspring', 'This week',
     'Activate post-appointment SMS/email outreach to collect reviews. Target: 25 reviews in 90 days, 15+ before LSA go-live. This is the single highest-impact action Wellspring can take right now — LSAs cannot rank competitively without it.'),
    (INDIGO, '3', 'Set the Go-Live Trigger (Budget Approval)', 'Joint', 'Agree in next call',
     'Agree a milestone: when Wellspring reaches 15 Google reviews, go live on LSAs at $350/month. Document this as a conditional budget approval so there is no delay when the milestone is hit.'),
]
for i, (clr, num, title, owner, timing, body) in enumerate(actions):
    top = 1.05 + i * 1.98
    # Number block
    rect(s, 0.55, top, 0.65, 1.78, clr)
    txb(s, num, 0.55, top + 0.48, 0.65, 0.82, sz=32, bold=True, clr=WHITE,
        align=PP_ALIGN.CENTER, font='Arial Black')
    # Content block
    rect(s, 1.25, top, 11.55, 1.78, WHITE)
    # Owner + Timing badges
    rect(s, 9.90, top + 0.14, 1.30, 0.28, LIGHT)
    txb(s, f'Owner: {owner}', 9.90, top + 0.15, 1.30, 0.26, sz=9, bold=True,
        clr=clr, align=PP_ALIGN.CENTER)
    rect(s, 11.28, top + 0.14, 1.40, 0.28, LIGHT)
    txb(s, timing, 11.28, top + 0.15, 1.40, 0.26, sz=9, bold=True,
        clr=clr, align=PP_ALIGN.CENTER)
    txb(s, title, 1.42, top + 0.14, 8.35, 0.40, sz=14, bold=True, clr=clr)
    txb(s, body,  1.42, top + 0.55, 11.22, 1.12, sz=11, clr=DARK)

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────
out = Path(__file__).parent / '01_Reports' / 'Wellspring_LSA_Proposal_Q3_2026.pptx'
prs.save(out)
print(f'Saved: {out}')
