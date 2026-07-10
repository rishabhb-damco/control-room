# CSXAI — Claude Code Workspace

> Account Lead: Rishabh B | Damco Digital
> Function: Lead Generation Strategy + Email Campaigns + Paid Ads
> Last configured: 26 May 2026

---

## Client Identity

| Field | Detail |
|---|---|
| Client | CSX Intelligence (CSXAI) |
| Product | AI-powered voice agent for financial services + real estate |
| Location | US market |
| PM | Shaivi Tyagi |
| Platforms | Google Ads / Meta Ads / LinkedIn Ads (TBD) + Email (MailChimp) |
| Meeting cadence | TBD |
| Reports on | Leads, CPL, platform performance, email open/click rates |

---

## Files in This Folder

| File | Purpose |
|---|---|
| `CSXAI_Claude.md` | Living brief — full account context, tasks, learnings |
| `action_tracker.md` | All open and closed actions |
| `deliverables.md` | Deliverable log |
| `transcripts/` | Drop zone for meeting transcripts |
| `01_Reports/` | Generated reports, decks |
| `02_Copy/` | Ad copy, email copy, outreach templates |
| `03_Research/` | Competitor research, keyword lists, platform analysis |
| `04_Data/` | CSVs, raw exports, data files |

---

## Workflow Commands

### "where are we?" or "account status"
Read `CSXAI_Claude.md` + `action_tracker.md` + `deliverables.md` and return:
```
CSXAI — ACCOUNT STATUS [today's date]

CAMPAIGNS: [live / not live / in planning]
OPEN ACTIONS: [count] — [top 3 by priority]
NEXT DELIVERABLE: [what + when]
TOP PRIORITY THIS WEEK: [one thing]
WATCH: [any risk or flag]
```

### "what's pending?" or "open actions"
Read `action_tracker.md` and list all items with Status = Open, sorted by Priority (Critical → High → Medium → Low).

### "process transcript" or "process this transcript"
1. Read `CSXAI_Claude.md` for context
2. Read `action_tracker.md` for current open items
3. Generate:
   - Internal team briefing (honest, direct)
   - Action tracker additions
   - Brief update suggestions (what to add to `CSXAI_Claude.md`)
4. Ask: "Shall I update the files now?"
5. On confirmation: update `action_tracker.md` and `CSXAI_Claude.md`

### "competitor research [competitor name]"
Research the named competitor (or Altropy + Gila by default):
- Lead gen channels they use
- LinkedIn presence + post formats
- Estimated ad spend / activity signals
- Key messaging and positioning
Save output to `03_Research/`

### "draft email: [sequence / type]"
Draft email copy for the specified nurture sequence or outreach template.
- Financial institutions or real estate — specify which
- Save to `02_Copy/`

### "draft outreach template: [email / linkedin]"
Draft a cold/warm outreach template for the specified channel.
Save to `02_Copy/`

### "platform strategy"
Evaluate Google Ads, Meta Ads, and LinkedIn Ads for reaching financial institution and real estate decision-makers:
- Audience availability
- Estimated CPL
- Recommended channel + rationale
Output structured recommendation.

### "log deliverable: [name]"
Add a new row to `deliverables.md`:
`| [today's date] | [deliverable name] | Completed | — |`

### "update brief"
Ask: "What data or update would you like to add to the CSXAI brief?"
Then update the relevant section of `CSXAI_Claude.md`.

---

## Style Rules (CSXAI-Specific)

- B2B tone — professional, confident, credibility-first
- Lead all messaging with empathy + compliance differentiators
- Target personas: VP Operations / CTO / Head of Customer Service at financial institutions; Real estate firm principals
- Currency: USD ($)
- Internal briefs: fully honest, direct
- Emails to client: professional, no jargon

---

## Critical Context (Read Before Every Session)

- Product is brand new — zero existing leads database, everything being built from scratch
- LinkedIn organic is running (Simran + Tarun) — Rishabh's scope is paid ads + email
- Thursday 29 May 2026 deadline: competitor research slide + lead gen plan slide for Shaivi
- LinkedIn paid = expensive, Phase 2; first priority is identifying the right cold lead gen channel
- Lead magnets: 2 documents planned (finance + real estate) — to be created before June launch
- No email list yet — outreach and nurturing depend on first building a contact database
