# Wellspring — Claude Code Workspace

> Account Lead: Rishabh B | Damco Digital
> Function: Paid Ads (Google Ads + Meta Ads)
> Last configured: 2026-05-12

---

## Client Identity

| Field | Detail |
|---|---|
| Client | Wellspring Therapeutic Partners |
| Industry | Mental Health / Private Practice |
| Location | Troy + Clinton Township, Michigan, USA |
| Services | Therapy + Medication Management (NP-led) |
| Insurance | Private pay — BCBS, BCN, Aetna, Priority Health, McLaren, Tricare, UHC |
| NOT accepted | Medicaid, Medicare, HAP (under review) |
| Platforms | Google Ads + Meta Ads |
| Meeting cadence | Weekly |
| Reports on | Leads, CPL, CTR, CPC, Scheduling rate, Funnel quality |

## Key Contacts

| Name | Role | Side |
|---|---|---|
| TBD | Client contact | Wellspring |
| Rishabh B | Account Lead / Paid Ads | Damco Digital |

---

## Files in This Folder

| File | Purpose |
|---|---|
| `Wellspring_Claude.md` | Living brief — full account history, performance, strategy |
| `action_tracker.md` | All open and closed actions |
| `deliverables.md` | Deliverable log |
| `lead_quality_skill.md` | Lead classification logic, skill reference, analysis format |
| `paid_ads_playbook.md` | Shared Paid Ads function module (output templates, health check, benchmarks) — local copy, previously `control room/modules/paid_ads.md` |
| `transcripts/` | Drop zone for meeting transcripts |
| `01_Reports/` | Generated HTML/PDF reports, monthly decks |
| `02_Copy/` | Ad copy, headlines, hooks, scripts |
| `03_Research/` | Search terms, competitor notes, keyword lists |
| `04_Data/` | CSVs, raw exports, data files |

## Connected Data Sources

| Source | Sheet ID / Path | Access Method |
|---|---|---|
| Consultation Sheet (lead quality) | `1OCsKgpQ-crR5rtrGTpSK0slRyhlGpqtC5QIi_4Gl_Vc` | Composio → `GOOGLESHEETS_BATCH_GET` |
| Google Ads Data Sheet | `1ZPXuyGP35wKhp7RBSUgoFOkfbnpfq1vmLPtchThacO4` | Composio → `GOOGLESHEETS_BATCH_GET` |
| Lead Classification Skill | `lead_quality_skill.md` | Always available |
| Weekly Report Repo | Windows: `C:\Users\Rishabhb\Downloads\Wellspring-Weekly-Report\` · Mac: `~/Downloads/Wellspring-Weekly-Report/` | git push → GitHub Pages |

**Consultation Sheet tabs:** Weekly date-range tabs (e.g. `May 3 - May 9`). Columns: Date, Name, DOB, Phone, Email, Insurance, Service Type, Source (`col_map['SOURCE']`), How did you hear (`col_map['HEAR']`), Scheduled (Yes/No), Reason Not Scheduled.

**Google Ads Sheet tabs:** `Performance Report` — daily rows with Date, Campaign, Impressions, Clicks, CTR, Avg CPC, Cost, Conversions, Conv. Rate, Cost/Conv.

**GitHub Pages base URL:** `https://rishabhb-damco.github.io/Wellspring-Weekly-Report/`
**Report naming:** `wellspring-report-[mon]-[d]-[yyyy]-[mon]-[d]-[yyyy].html` (e.g. `wellspring-report-may-3-2026-may-9-2026.html`)

---

## Workflow Commands

### "process transcript" or "process this transcript"
When I receive a transcript (pasted or saved in `transcripts/`):
1. Read `Wellspring_Claude.md` for context
2. Read `action_tracker.md` for current open items
3. Generate all 5 outputs (from `paid_ads_playbook.md`):
   - Client MOM email (professional, warm, no jargon)
   - Internal team briefing (honest, flagging risks)
   - Action tracker additions (formatted for `action_tracker.md`)
   - Brief update suggestions (what to add to `Wellspring_Claude.md`)
   - Linear-ready paste
4. Ask: "Shall I update the files now?"
5. On confirmation: update `action_tracker.md` and `Wellspring_Claude.md`

### "where are we?" or "account status"
Read `Wellspring_Claude.md` + `action_tracker.md` + `deliverables.md` and return:
```
WELLSPRING — ACCOUNT STATUS [today's date]

CAMPAIGNS: [active / paused / issues]
LAST WEEK: [key metric summary]
OPEN ACTIONS: [count] — [top 3]
NEXT DELIVERABLE: [what + when]
TOP PRIORITY THIS WEEK: [one thing]
WATCH: [any risk or flag]
```

### "what's pending?" or "open actions"
Read `action_tracker.md` and list all items with Status = Open, sorted by Priority (Critical → High → Medium → Low).

### "draft email about [topic]"
Read `Wellspring_Claude.md` for client context, then draft a professional client email.
- Tone: warm, professional, no jargon
- Sign off as: Rishabh | Damco Digital
- Keep subject line clear and specific

### "log deliverable: [name]"
Add a new row to `deliverables.md`:
`| [today's date] | [deliverable name] | Completed | — |`
Confirm when done.

### "linear update"
Read all Open items in `action_tracker.md` and format as Linear-ready paste (title, assignee, priority, description per item).

### "update brief"
Ask: "What data or update would you like to add to the Wellspring brief?"
Then update the relevant section of `Wellspring_Claude.md`.

### "weekly report"
Using latest data from `Wellspring_Claude.md`, generate a weekly performance summary in the Paid Ads report format (from `paid_ads_playbook.md`).

### "create weekly report" or "create last weekly report"
Full fused report: pulls live data from both Google Sheets via Composio, classifies leads, generates a styled HTML report, publishes it to GitHub Pages.

**Step 1 — Confirm date range**
Ask: "What week? (e.g. Jun 7 – Jun 13)" — OR if user said "last weekly report", auto-calculate as **Sun–Sat of the previous calendar week** (e.g. if today is Mon Jun 15, last week = Sun Jun 7 – Sat Jun 13). Week always runs Sunday to Saturday.

**Step 2 — Pull Google Ads data**
Use Composio `GOOGLESHEETS_BATCH_GET` on sheet `1ZPXuyGP35wKhp7RBSUgoFOkfbnpfq1vmLPtchThacO4`, tab `Performance Report`.
Filter rows where Date falls within the date range.
Campaigns to track:
- `Damco_WS_Generic_Search_041125` → label "Generic Search"
- `Damco_DSA_Wellspring_Ad_270226` → label "DSA"
- `Damco_WS_Regional_Search_060525` → label "Regional Search"

Aggregate per campaign: Impressions, Clicks, CTR, Avg CPC, Cost (Spend), Conversions, Conv. Rate, Cost/Conv. (CPL).
Also compute totals across all campaigns.

For prior-week comparison: fetch the week immediately before the target range from the same sheet and compute % change for Spend, Conversions, CPL, CTR.

**Step 3 — Pull consultation / lead quality data**
Use Composio `GOOGLESHEETS_BATCH_GET` on sheet `1OCsKgpQ-crR5rtrGTpSK0slRyhlGpqtC5QIi_4Gl_Vc`.
First use `GOOGLESHEETS_GET_SHEET_NAMES` to find the tab matching the date range (e.g. `May 10 - May 16`).
Fetch all rows from that tab.

**Step 4 — Anomaly detection (run before building the report)**
Before aggregating or writing any numbers, scan the raw daily Google Ads rows for irregular patterns. Flag any of the following as amber/rust insight cards in the Key Observations section:

- **Missing days:** Count distinct dates per campaign. If any active campaign has fewer rows than the number of days in the period, flag which dates are missing and how many.
- **Uneven spend distribution:** If any single day = >40% of weekly total, or if spend is $0 for 2+ consecutive mid-week days, flag as possible budget exhaustion or front-loading.
- **Budget over/under-delivery:** DSA daily budget = $15. Days >$20 = over-delivery (Google 2× rule). Multiple days <$5 = under-serving.
- **Campaign dominance:** If one campaign absorbs >90% of total spend when both are active, flag the imbalance explicitly.
- **WoW spend drop >50%:** Flag any week where total spend drops more than 50% vs prior week without a confirmed reason (holiday, intentional pause).
- **Zero platform conversions:** If the whole week has 0 forms + 0 phone calls, flag separately from CRM-based conversions.
- **Full campaign absence:** If an expected active campaign (DSA, Generic Search) has zero rows for the entire week, flag as potentially paused.
- **Acceleration-then-drop pattern:** Heavy spend early in week followed by abrupt zero → likely budget exhaustion or smart bidding throttle. Note suspected cause.

Output format: `"⚠️ [Campaign] had no recorded spend on [dates] (X of 7 days active). Possible cause: [hypothesis]. Recommend pulling change history for [date range]."`

**Step 4a — Send anomaly alert email (if any anomalies found)**
If Step 4 detected ANY anomaly, send an email immediately via Composio `GMAIL_SEND_EMAIL` before building the report.

- **To:** rishabhb@damcogroup.com
- **Subject:** `⚠️ Wellspring Google Ads — Anomaly Alert [Week: DATE_RANGE]`
- **Body format:**

```
Hi Rishabh,

While pulling data for the [DATE_RANGE] Wellspring report, the following anomalies were detected in the Google Ads account. Action may be required before or alongside reviewing the published report.

────────────────────────────
🔴 HIGH PRIORITY
────────────────────────────
[List each high-priority anomaly]
• [Campaign] had zero spend on [dates] — possible pause or budget exhaustion
• Zero platform conversions (0 forms + 0 calls) entire week

────────────────────────────
🟡 MEDIUM PRIORITY
────────────────────────────
[List each medium-priority anomaly]
• [Campaign] absorbed X% of total spend — Generic Search near-absent
• Spend front-loaded on [dates], zero on [dates]

────────────────────────────
🟢 LOW PRIORITY / WATCH
────────────────────────────
[List each low-priority anomaly]
• CTR dropped X% vs prior week — monitor next week

────────────────────────────
The full weekly report will be published shortly at:
[GitHub Pages URL]

— Damco Digital (automated alert)
```

Priority classification:
- 🔴 HIGH: Campaign absent 3+ days · WoW spend drop >70% · Zero platform conversions all week · Possible account suspension
- 🟡 MEDIUM: 1–2 missing campaign days · Spend drop 50–70% · One campaign >90% of spend · Acceleration-then-drop pattern
- 🟢 LOW: Single-day over/under-delivery · CTR drop >20% vs prior week · Minor WoW variation

If no anomalies are found, skip this step — do not send a blank alert.

**Step 4c — Fetch Google Trends context (on request only)**
Only include Market Context / Google Trends section if the user explicitly asks for it. It is NOT part of the default weekly report template.
If requested, use pytrends to fetch "Therapist Near Me" interest and include a panel between Section 1 and Section 2.

**Step 4b — Classify leads and compute metrics**
Apply the 7-rule logic from `lead_quality_skill.md` to every row.
Compute:
- Total leads, total scheduled, overall scheduling rate
- Per-source: Google, Internal, Referral, Psychology Today — lead count + scheduled count + scheduling rate
- Per service type: Psychotherapy, Medication Management, ADHD Testing, Couples, Other — lead count
- Scheduling breakdown: Scheduled vs Not Scheduled (for donut chart)
- Reason not scheduled: count by reason bucket (Insurance, No response, Cost, Capacity, Other)
- Unqualified leads: rows where insurance = Medicaid/Medicare/HAP and not accepted

**Step 5 — Generate HTML report**
Build an HTML file that exactly matches the format of `wellspring-report-may-3-2026-may-9-2026.html` in the Weekly Report Repo (Windows: `C:\Users\Rishabhb\Downloads\Wellspring-Weekly-Report\` · Mac: `~/Downloads/Wellspring-Weekly-Report/`).
Key elements:
- Fonts: Cormorant Garamond (serif headings) + DM Sans (body) from Google Fonts
- CSS variables color system (dark teal `#1a3a3a`, gold `#c9a84c`, off-white `#f5f0e8`)
- KPI cards row: Total Leads | Scheduling Rate | Total Spend | CPL | CTR | Total Conversions
- Each KPI shows value + vs-prior-week delta badge (↑/↓ with % change, green/red)
**Standard report section order (do NOT deviate without being asked):**
1. Header + anomaly banner (if anomalies found)
2. Section 1 KPI cards (6 cards)
3. Campaign performance table + 4-week trend chart (two-col)
4. Section 2 divider → Lead Analysis KPI cards
5. Scheduling by Source (donut + table) + Service Mix & Decline Reasons (two-col)
6. Recommended Actions (full-width, 2-column grid)
7. Key Observations (full-width panel with 3 insight cards — placed LAST before footer)
8. Footer

**Sections NOT included by default (include only if user asks):**
- Prior week campaign comparison table — removed from standard template
- Market Context / Google Trends — removed from standard template; fetch only on request
- Benchmark vs Current Performance section — removed from standard template; include on request

**Password gate — REQUIRED on every report**
Every HTML report MUST include a full-screen password gate before the report content loads.
- Password: `Wellspring123` (pattern: `{ClientName}123` — capitalise first letter)
- Gate blocks the entire page until correct password is entered
- Uses `sessionStorage` so the user only enters it once per browser session
- Enter key should submit the password (not just the button)
- Embed the gate CSS in the main `<style>` block and the gate HTML + JS immediately after `<body>`
- Reference implementation: `wellspring-report-may-10-2026-may-15-2026.html` — copy the `#pw-gate` block exactly

Save the file as:
`wellspring-report-[date-range].html` inside the Weekly Report Repo (Windows: `C:\Users\Rishabhb\Downloads\Wellspring-Weekly-Report\` · Mac: `~/Downloads/Wellspring-Weekly-Report/`)
where `[date-range]` = e.g. `may-10-2026-may-16-2026`

**Step 6 — Push to GitHub**
Use the Weekly Report Repo path for the current OS (see above).
```
cd [Weekly Report Repo path for current OS]
git add wellspring-report-[date-range].html
git commit -m "Add weekly report [date range]"
git push origin main
```
Wait for push to succeed. If push fails, report the error — do NOT force-push.

**Step 7 — Return the live URL**
Report back:
```
Report published:
https://rishabhb-damco.github.io/Wellspring-Weekly-Report/wellspring-report-[date-range].html

(GitHub Pages typically goes live within 1–2 minutes)
```

**Step 8 — Offer to update weekly log**
Ask: "Add this week's data to the weekly log in Wellspring_Claude.md?"
If yes, append a new row to the weekly performance log section in `Wellspring_Claude.md`.

### "analyse lead quality" or "run lead quality"
1. Ask: "Paste CSV data from the consultation sheet (or specify date range if MCP connected)"
2. Classify each row using the 7-rule logic in `lead_quality_skill.md`
3. Output the scheduling analysis in the format defined in `lead_quality_skill.md`
4. Compare against March 2026 benchmarks
5. Flag sources below 30% scheduling rate

### "campaign health check"
Run through the Google Ads + Meta Ads health checklist from `paid_ads_playbook.md` using current data in `Wellspring_Claude.md`. Flag anything in red.

### "paste search terms [data]"
User pastes Google Ads Search Terms report. Claude will:
1. Sort by spend (high → low)
2. Flag irrelevant terms as negatives with suggested match type
3. Identify 3–5 new keyword opportunities
4. Output: negative list (ready to add) + keyword opportunities table

### "check budget pacing"
User provides: daily budget + spend so far this month + days remaining.
Calculate: on-pace / over-pace / under-pace. Recommend adjustment if >15% off-pace.

### "log optimization [action]"
Append to `optimization_log.md`:
`| [today's date] | [campaign] | [action taken] | [expected impact] | Pending |`
Create `optimization_log.md` if it doesn't exist yet.

### "diagnose [metric] drop" or "why did [metric] drop?"
Read `Wellspring_Claude.md` weekly log. Cross-reference the metric drop with:
- Campaign change history
- Seasonality (month/week patterns from historical data)
- Known Wellspring-side issues (capacity, insurance)
Output structured diagnosis: likely cause, supporting evidence, recommended fix.

### "test idea: [hypothesis]"
Log a new A/B test idea to `test_tracker.md`:
`| [today's date] | [campaign/ad group] | [hypothesis] | [metric to watch] | Not started |`
Create `test_tracker.md` if it doesn't exist yet.

---

## Style Rules (Wellspring-Specific)

- Client emails: compassionate, professional tone (mental health client — sensitivity matters)
- Currency: USD ($)
- Do NOT use clinical jargon in client emails (no "conversion rate", "CPL" — say "cost per lead", "leads generated")
- Internal briefs: fully honest, direct, no softening
- Always note if a campaign issue is Wellspring-side (capacity, insurance) vs agency-side

---

## Session Behaviour

### Auto-task logging
At the start of every session, append a new row to the **Session Log** section of `action_tracker.md`:

| Date | Task | Status |
|---|---|---|
| [today's date] | [user's first request, one line] | In Progress |

Update status to **Completed** when the task is done. If a deliverable file was produced, also add a row to `deliverables.md`.

### Git sync
This folder is its own git repo, synced to GitHub so it's accessible across machines. Only run `git push`/`git pull` when explicitly asked — never proactively sync in the background.

### File routing — always save to a subfolder
| File type | Save to |
|---|---|
| HTML/PDF reports, PPTX decks | `01_Reports/` |
| Ad copy, headlines, hooks, scripts | `02_Copy/` |
| Competitor research, keyword lists, search terms | `03_Research/` |
| CSVs, raw exports, data files | `04_Data/` |
| Meeting transcripts | `transcripts/` |

Never save files to the root client folder — always route to a subfolder.

### On task completion
1. Mark the session log entry Completed in `action_tracker.md`
2. If a deliverable was produced: add a row to `deliverables.md`
3. If a new open action was identified: add it to the Open Actions table in `action_tracker.md`

---

## Critical Context (Read Before Every Session)

- Meta leads have 0% scheduling rate — Meta is remarketing only, NOT cold lead gen
- DSA outperforms Generic Search by 2–4x on CPA every week — priority campaign
- HAP insurance status is unresolved — ~20-28% of lost leads, awaiting client confirmation
- Grief Search campaign is paused — relaunch when grief counselor capacity confirmed
- Google Healthcare certificate needed to unlock YouTube + Medication Management ads
- Psychotherapy = 53-61% of inbound — need to push ADHD/MedMgt copy
- Scheduling rate is partly a Wellspring capacity issue, not just campaign quality
