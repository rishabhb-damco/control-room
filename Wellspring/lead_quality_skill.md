# Wellspring — Lead Quality Classification Skill

> Source: `wellspring-lead-classification.skill` (ZIP archive at `C:\Users\Rishabhb\Downloads\`)
> Purpose: Classify consultation sheet leads by source, score scheduling quality, surface Google vs non-Google splits
> Google Sheet: https://docs.google.com/spreadsheets/d/1OCsKgpQ-crR5rtrGTpSK0slRyhlGpqtC5QIi_4Gl_Vc/edit?usp=sharing

---

## Column Mappings (Consultation Sheet)

| Internal Key | Column Header in Sheet |
|---|---|
| `HEAR` | "How did you hear about us?" |
| `SOURCE` | "Lead Source" (CRM-set field) |
| `DATE` | Consultation / Appointment Date |
| `NAME` | Client name |
| `STATUS` | Scheduled / No-show / Cancelled / Completed |
| `THERAPIST` | Assigned provider |

---

## 8-Rule Classification Logic (Priority Order)

```
Rule 0: if HEAR contains AI search tools → SEO        ← NEW: organic AI discovery ≠ paid ads
         ('gemini', 'google gemini',
          'chatgpt', 'chat gpt',
          'bard', 'perplexity',
          'copilot', 'bing ai')
Rule 1: if SOURCE == "internal"         → Internal
Rule 2: if SOURCE == "google ads"       → Google
         OR "google" in HEAR
Rule 3: if HEAR in ('', '-', 'other',   → Google   ← implicit / unknown = Google
         'online', 'internet', 'web',
         'search', 'online search',
         'searched online')
Rule 4: if "psychology today" in HEAR   → Psychology Today
Rule 5: if SOURCE in ('external',       → Referral
         'referral')
Rule 6: if HEAR is any named person     → Referral
         or practice
Rule 7: fallback                        → Google
```

**Rule 0 rationale:** Leads from Google Gemini, ChatGPT, Bing AI etc. discovered Wellspring through organic AI-generated answers — not through a paid ad click. These belong to SEO/organic, not Google Ads.

---

## Python Implementation

```python
AI_TOOLS = ('gemini', 'google gemini', 'chatgpt', 'chat gpt', 'bard', 'perplexity', 'copilot', 'bing ai')

def classify_source(row, col_map):
    hear   = str(row[col_map['HEAR']]   or '').strip().lower()
    source = str(row[col_map['SOURCE']] or '').strip().lower()

    if any(t in hear for t in AI_TOOLS):                return 'SEO'   # Rule 0 — AI search tools
    if source == 'internal':                            return 'Internal'
    if source == 'google ads' or 'google' in hear:      return 'Google'
    if hear in ('', '-', 'other', 'online', 'internet',
                'web', 'search', 'online search',
                'searched online'):                     return 'Google'
    if 'psychology today' in hear:                      return 'Psychology Today'
    if source in ('external', 'referral'):              return 'Referral'
    if hear:                                            return 'Referral'
    return 'Google'  # fallback
```

---

## JavaScript Implementation

```javascript
const AI_TOOLS = ['gemini','google gemini','chatgpt','chat gpt','bard','perplexity','copilot','bing ai'];

function classifySource(hear, source) {
  hear   = (hear   || '').trim().toLowerCase();
  source = (source || '').trim().toLowerCase();

  if (AI_TOOLS.some(t => hear.includes(t)))               return 'SEO';  // Rule 0
  if (source === 'internal')                               return 'Internal';
  if (source === 'google ads' || hear.includes('google'))  return 'Google';
  const implicit = ['', '-', 'other', 'online', 'internet',
                    'web', 'search', 'online search', 'searched online'];
  if (implicit.includes(hear))                             return 'Google';
  if (hear.includes('psychology today'))                   return 'Psychology Today';
  if (['external','referral'].includes(source))            return 'Referral';
  if (hear)                                                return 'Referral';
  return 'Google';
}
```

---

## Scheduling Analysis Output Format

When running lead quality analysis, produce this output:

```
WELLSPRING — LEAD QUALITY REPORT [date range]

TOTAL LEADS: [N]
SCHEDULED:   [N] ([%])
NO-SHOW:     [N] ([%])
CANCELLED:   [N] ([%])

--- BY SOURCE ---
Source            Leads  Sched  Sched%
Internal          [N]    [N]    [%]
Google            [N]    [N]    [%]
Referral          [N]    [N]    [%]
Psychology Today  [N]    [N]    [%]
Other             [N]    [N]    [%]

--- SCHEDULING QUALITY NOTES ---
[Flag any source with scheduling rate below 30%]
[Flag any source with 0 scheduled out of 3+ leads]
[Note if Internal leads are below 50% scheduling rate]

--- VS BENCHMARK ---
[Compare to March 2026 reference benchmarks below]
```

---

## Reference Benchmarks — March 2026

> **Methodology:** All metrics derived using CRM-based 7-rule classification (consultation sheet data). Google metrics use Google-attributed CRM leads only (not pixel/platform conversions). This ensures benchmarks are consistent and comparable with how weekly reports are built.

### Section 1 — Google Ads Performance Benchmarks

| Metric | Benchmark Value | Definition |
|---|---|---|
| Google CRM Leads / Month | 49 | Google-attributed leads (7-rule logic) from consultation sheet |
| Blended CPL | $44 | Total Google Ads spend ÷ Google CRM leads ($2,147 ÷ 49) |
| Conversion Rate | 9.4% | Google CRM leads ÷ total clicks (49 ÷ 520) |
| Avg CTR | 6.49% | Weighted CTR across all campaigns |
| Avg CPC | $4.13 | Total spend ÷ total clicks ($2,147 ÷ 520) |
| DSA Platform CPA | $20.43 | DSA spend ÷ DSA pixel conversions ($510.86 ÷ 25) |
| Google Scheduling Rate | 38.8% | Google CRM leads scheduled ÷ Google CRM leads (19 ÷ 49) |
| Cost per Scheduled Appointment | $113 | Total spend ÷ Google CRM scheduled leads ($2,147 ÷ 19) |

### Section 2 — Overall Lead Analysis Benchmarks

| Metric | Benchmark Value | Definition |
|---|---|---|
| Total CRM Leads / Month | 81 | All leads from consultation sheet (all sources) |
| Overall Scheduling Rate | 53.1% | All leads scheduled ÷ all leads (43 ÷ 81) |
| Internal Scheduling Rate | 71.4% | Internal leads scheduled ÷ Internal leads (15 ÷ 21) |
| Referral Scheduling Rate | 88.9% | Referral leads scheduled ÷ Referral leads (8 ÷ 9) |
| Psychology Today Scheduling Rate | 50.0% | PT leads scheduled ÷ PT leads (1 ÷ 2) |

### Source Mix — March 2026

| Source | Leads | Scheduled | Scheduling Rate |
|---|---|---|---|
| Google | 49 | 19 | 38.8% |
| Internal | 21 | 15 | 71.4% |
| Referral | 9 | 8 | 88.9% |
| Psychology Today | 2 | 1 | 50.0% |
| **TOTAL** | **81** | **43** | **53.1%** |

### Google Ads Spend — March 2026

| Campaign | Impressions | Clicks | CTR | CPC | Spend |
|---|---|---|---|---|---|
| Generic Search | 5,555 | 307 | 5.53% | $5.33 | $1,636.34 |
| DSA | 2,461 | 213 | 8.66% | $2.40 | $510.86 |
| **TOTAL** | **8,016** | **520** | **6.49%** | **$4.13** | **$2,147.20** |

---

## How to Run Lead Quality Analysis

### Option A — Manual Paste (available now)
1. Open the Google Sheet linked above
2. Export as CSV: File → Download → CSV
3. Say: `analyse lead quality` and paste the CSV data
4. Claude will classify each row and generate the report

### Option B — Google Sheets MCP (when configured)
If the Google Sheets MCP server is connected to Claude Code:
1. Say: `run lead quality report for [date range]`
2. Claude fetches the sheet directly, classifies, and reports
3. Setup: `claude mcp add google-sheets-mcp` (requires Google OAuth)

### Option C — Google Sheets → CSV auto-export via Script
Add a Google Apps Script to the sheet that:
- Exports a date-filtered CSV to a watched folder on your machine
- Claude Code picks it up on next `create weekly report` command

---

## Reason Buckets (for no-show / not-scheduled analysis)

| Bucket | Description |
|---|---|
| Capacity | No therapist available for client's availability |
| Insurance | Doesn't accept client's insurance plan |
| Price | Private pay cost too high |
| No response | Client didn't answer follow-up calls |
| Found elsewhere | Client chose another provider |
| Medical fit | Not a clinical fit |
| Unknown | No data captured |
