import xlsxwriter
import os
from pathlib import Path

output_path = Path(__file__).parent / "AI_Automation_Task_Tracker.xlsx"

wb = xlsxwriter.Workbook(output_path)
ws = wb.add_worksheet("Task Tracker")

# ── Formats ──────────────────────────────────────────────────────────────────
base = {"font_name": "Calibri", "font_size": 10, "border": 1, "border_color": "#D0D0D0", "valign": "vcenter", "text_wrap": True}

def fmt(extra={}):
    return wb.add_format({**base, **extra})

hdr = fmt({"bold": True, "font_size": 11, "bg_color": "#1a3a3a", "font_color": "#FFFFFF", "align": "center", "border_color": "#1a3a3a"})
cat_hdr = fmt({"bold": True, "font_size": 10, "bg_color": "#2d5a5a", "font_color": "#FFFFFF", "border_color": "#2d5a5a"})

done_bg    = fmt({"bg_color": "#D6F4D6", "font_color": "#1a6b1a", "bold": True, "align": "center"})
high_bg    = fmt({"bg_color": "#FFF3CD", "font_color": "#7d5a00", "bold": True, "align": "center"})
medium_bg  = fmt({"bg_color": "#E8F4FD", "font_color": "#1a5276",  "bold": True, "align": "center"})
low_bg     = fmt({"bg_color": "#F8F9FA", "font_color": "#555555",  "bold": True, "align": "center"})
none_bg    = fmt({"bg_color": "#EFEFEF", "font_color": "#888888",  "bold": True, "align": "center"})

done_row   = fmt({"bg_color": "#EBF9EB"})
normal     = fmt({})
center     = fmt({"align": "center"})
bold_cell  = fmt({"bold": True})
italic     = fmt({"italic": True, "font_color": "#666666"})

# ── Column widths ─────────────────────────────────────────────────────────────
ws.set_column(0, 0, 4)   # #
ws.set_column(1, 1, 14)  # Category
ws.set_column(2, 2, 42)  # Task
ws.set_column(3, 3, 14)  # Avg Time
ws.set_column(4, 4, 18)  # Automation Potential
ws.set_column(5, 5, 14)  # Status
ws.set_column(6, 6, 44)  # Notes / Next Action

ws.set_default_row(18)

# ── Header row ────────────────────────────────────────────────────────────────
headers = ["#", "Category", "Task", "Avg Time", "Automation Potential", "Status", "Notes / Next Action"]
for col, h in enumerate(headers):
    ws.write(0, col, h, hdr)
ws.set_row(0, 22)

# ── Data ──────────────────────────────────────────────────────────────────────
# (category, task, avg_time, automation, status, notes)
rows = [
    # DAILY
    ("DAILY", "Check campaign dashboards (Google + Meta)", "15–20 min", "High",
     "Open", "Routine: pull anomalies, flag overspend, send daily summary"),
    ("DAILY", "Monitor spend pacing across clients", "10 min", "High",
     "Open", "Routine: compare daily spend vs. target, flag if >15% off"),
    ("DAILY", "Check for alerts (disapproved ads, policy issues)", "5 min", "High",
     "Open", "Routine: scan accounts, surface issues automatically"),
    ("DAILY", "Respond to client messages / queries", "10–20 min", "Low",
     "Open", "AI can draft replies — human approval required before sending"),

    # WEEKLY
    ("WEEKLY", "Weekly performance report (HTML)", "~~90 min~~ → 5 min", "Done ✓",
     "Done", "Wellspring live — skill built and running"),
    ("WEEKLY", "Lead quality classification + scheduling analysis", "~~30–45 min~~", "Done ✓",
     "Done", "Skill live — classifies leads, computes scheduling rate"),
    ("WEEKLY", "Search terms review → flag negatives + opportunities", "45–60 min", "High",
     "Open", "Paste CSV → auto-sort by spend, flag negatives, surface new keywords"),
    ("WEEKLY", "Budget pacing check (all clients)", "15 min", "High",
     "Open", "Input daily budget + spend to date → pacing status + recommendation"),
    ("WEEKLY", "Campaign optimisation (bid adjustments, budget shifts)", "30–45 min", "Medium",
     "Open", "AI surfaces recommendation — execution done by you"),
    ("WEEKLY", "MOM email after client call", "20–30 min", "High",
     "Open", "Transcript → MOM email skill — works across all clients"),
    ("WEEKLY", "Internal team briefing after call", "15 min", "High",
     "Open", "Same transcript → internal brief (separate from client email)"),
    ("WEEKLY", "Action tracker update from call", "10 min", "High",
     "Open", "Skill: transcript → action items formatted and appended"),
    ("WEEKLY", "Linear update", "10 min", "High",
     "Open", "Skill: read open actions → Linear-ready paste"),

    # MONTHLY
    ("MONTHLY", "Monthly performance report (PPTX)", "~~2–3 hrs~~", "Done ✓",
     "Done", "PPT auto-generated — skill built and running"),
    ("MONTHLY", "Competitor research (per client)", "60–90 min", "High",
     "Open", "Replace with Claude Routine — runs daily, saves to memory"),
    ("MONTHLY", "Search term audit (deep clean)", "60–90 min", "High",
     "Open", "Same as weekly skill but on full monthly export"),
    ("MONTHLY", "Account health audit checklist", "30–45 min", "High",
     "Open", "Checklist skill — auto-run against live account data"),
    ("MONTHLY", "Budget planning for next month", "20 min", "Medium",
     "Open", "AI models scenarios from current data — you approve"),
    ("MONTHLY", "A/B test review + recommendations", "20 min", "Medium",
     "Open", "Summarise test data + statistical significance + recommendation"),
    ("MONTHLY", "Keyword research (new campaigns / expansion)", "60–90 min", "Medium",
     "Open", "AI generates seed list and clusters — you refine and approve"),

    # OCCASIONAL
    ("OCCASIONAL", "New client onboarding brief", "60–90 min", "High",
     "Open", "Template skill: inputs → structured brief with all required fields"),
    ("OCCASIONAL", "Ad copy creation (headlines, descriptions, hooks)", "45–60 min", "High",
     "Open", "Skill: brief → 10+ copy variants per format, per platform"),
    ("OCCASIONAL", "Campaign setup (structure, keywords, ad groups)", "2–4 hrs", "Medium",
     "Open", "AI drafts full structure + keyword list — you build in platform"),
    ("OCCASIONAL", "QBR deck preparation", "3–4 hrs", "High",
     "Open", "Data pull + narrative → PPTX — extension of monthly report skill"),
    ("OCCASIONAL", "Strategy proposal for new client", "2–3 hrs", "Medium",
     "Open", "Template + competitor research → first draft for you to refine"),
    ("OCCASIONAL", "Landing page brief", "30 min", "High",
     "Open", "Inputs → structured brief ready for design team"),
    ("OCCASIONAL", "Google Ads account audit", "90 min", "High",
     "Open", "Structured checklist + data → formatted audit report"),

    # CANNOT AUTOMATE
    ("NO AUTOMATION", "Bid strategy decisions", "Varies", "None",
     "Manual", "Market conditions + client context — human judgment required"),
    ("NO AUTOMATION", "Client relationship and trust-building", "Ongoing", "None",
     "Manual", "Human only"),
    ("NO AUTOMATION", "Creative direction and brief sign-off", "Varies", "None",
     "Manual", "Human only"),
    ("NO AUTOMATION", "Final campaign go / no-go calls", "Varies", "None",
     "Manual", "Human only"),
    ("NO AUTOMATION", "Reading between the lines on client requests", "Varies", "None",
     "Manual", "Human only"),
]

auto_fmt = {
    "Done ✓": done_bg,
    "High":   high_bg,
    "Medium": medium_bg,
    "Low":    low_bg,
    "None":   none_bg,
}

row_bg = {
    "Done ✓": done_row,
    "High":   normal,
    "Medium": normal,
    "Low":    normal,
    "None":   fmt({"bg_color": "#F5F5F5", "font_color": "#888888"}),
}

current_cat = None
r = 1
task_num = 1

for (cat, task, avg_time, auto, status, notes) in rows:
    # Category header row
    if cat != current_cat:
        ws.set_row(r, 20)
        ws.merge_range(r, 0, r, 6, cat, cat_hdr)
        r += 1
        current_cat = cat

    tf = row_bg.get(auto, normal)
    af = auto_fmt.get(auto, normal)

    num_str = str(task_num) if cat != "NO AUTOMATION" else "—"
    ws.write(r, 0, num_str, center)
    ws.write(r, 1, cat,      tf)
    ws.write(r, 2, task,     tf)
    ws.write(r, 3, avg_time, center if cat != "NO AUTOMATION" else fmt({"align": "center", "bg_color": "#F5F5F5", "font_color": "#888888"}))
    ws.write(r, 4, auto,     af)
    ws.write(r, 5, status,   center)
    ws.write(r, 6, notes,    tf)

    ws.set_row(r, 28)
    if cat != "NO AUTOMATION":
        task_num += 1
    r += 1

# ── Legend ────────────────────────────────────────────────────────────────────
r += 1
ws.write(r, 0, "LEGEND", fmt({"bold": True, "font_size": 10}))
r += 1
legend = [
    ("Done ✓", "#D6F4D6", "#1a6b1a", "Skill already built and running"),
    ("High",   "#FFF3CD", "#7d5a00", "Strong automation candidate — build next"),
    ("Medium", "#E8F4FD", "#1a5276",  "Partial automation — AI assists, human finalises"),
    ("Low",    "#F8F9FA", "#555555",  "AI can draft — human must approve before action"),
    ("None",   "#EFEFEF", "#888888",  "Human judgment required — cannot automate"),
]
for (label, bg, fc, desc) in legend:
    lf = wb.add_format({"font_name": "Calibri", "font_size": 10, "bg_color": bg, "font_color": fc, "bold": True, "border": 1, "border_color": "#D0D0D0"})
    df = wb.add_format({"font_name": "Calibri", "font_size": 10, "border": 1, "border_color": "#D0D0D0"})
    ws.write(r, 4, label, lf)
    ws.write(r, 5, "", df)
    ws.merge_range(r, 5, r, 6, desc, df)
    r += 1

# ── Freeze panes + zoom ───────────────────────────────────────────────────────
ws.freeze_panes(1, 0)
ws.set_zoom(110)

wb.close()
print(f"Done: {output_path}")
