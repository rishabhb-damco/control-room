# KodaCars — Claude Code Workspace

> Account Lead: Rishabh B | Damco Digital
> Function: Digital Marketing Strategy (SEO, Content, LinkedIn, Meta, AEO)
> Last configured: 2026-05-12

---

## Client Identity

| Field | Detail |
|---|---|
| Client | KodaCars |
| Industry | Airport P2P Car Sharing / Parking Tech / InsurTech |
| Market | USA (airport-focused) |
| Stage | Pre-launch / fundraising ($5M raise in progress) |
| Project codenames | Project Velocity, Project LincUp |
| Platforms | LinkedIn (primary B2B), Meta (lot owners + travellers), SEO/AEO, Google Ads (planned) |
| Meeting cadence | TBD |
| Reports on | Organic rankings, LinkedIn impressions/CTR, DA growth, leads/demo bookings |
| Contact | executives@kodacars.com |

## Key Contacts

| Name | Role | Side |
|---|---|---|
| Brahm Sharma | CEO & Co-Founder | KodaCars |
| Rohan Sharma | CTO | KodaCars |
| Richard Piotrowski | Advisor & CMO | KodaCars |
| Rishabh B | Account Lead | Damco Digital |

---

## Files in This Folder

| File | Purpose |
|---|---|
| `Kodacars_Claude.md` | Living brief — business model, GTM, digital strategy |
| `action_tracker.md` | All open and closed actions |
| `deliverables.md` | Deliverable log |
| `transcripts/` | Drop zone for meeting transcripts |
| `01_Reports/` | Generated HTML/PDF reports, strategy decks |
| `02_Copy/` | LinkedIn copy, Meta copy, landing page copy |
| `03_Research/` | Competitor analysis, keyword lists, SEO research |
| `04_Data/` | CSVs, raw exports, GSC data |

---

## Workflow Commands

### "process transcript" or "process this transcript"
When I receive a transcript (pasted or saved in `transcripts/`):
1. Read `Kodacars_Claude.md` for context
2. Read `action_tracker.md` for current open items
3. Generate all 5 outputs:
   - Client MOM email (professional, B2B tone — CEO-level audience)
   - Internal team briefing (honest, flag any pivots or risks)
   - Action tracker additions
   - Brief update suggestions (especially GTM updates, fundraising signals, partner news)
   - Linear-ready paste
4. Ask: "Shall I update the files now?"
5. On confirmation: update files

### "where are we?" or "account status"
```
KODACARS — ACCOUNT STATUS [today's date]

FUNDRAISING: [status if known]
DIGITAL MARKETING: [SEO / LinkedIn / Meta status]
OPEN ACTIONS: [count] — [top 3]
NEXT DELIVERABLE: [what + when]
TOP PRIORITY THIS WEEK: [one thing]
WATCH: [competitor activity or risk]
```

### "what's pending?" or "open actions"
Read `action_tracker.md` and list all Open items sorted by Priority.

### "draft email about [topic]"
Read `Kodacars_Claude.md`. Draft B2B executive-level client email.
- Tone: strategic, confident, startup-aware, no fluff
- Audience: C-suite (Brahm/Rohan/Richard)
- Sign off as: Rishabh | Damco Digital

### "log deliverable: [name]"
Add new row to `deliverables.md`. Confirm when done.

### "linear update"
Format all Open `action_tracker.md` items as Linear-ready paste.

### "update brief"
Ask what to add, then update `Kodacars_Claude.md`.

### "seo check"
Run through SEO/AEO status from `Kodacars_Claude.md`. Report: DA progress, spam score, rankings, blogs published, AEO citations. Flag red items.

### "content ideas"
Based on the 4 LinkedIn pillars and 3 Meta pillars in `Kodacars_Claude.md`, generate 5 ready-to-post content ideas for this week.

---

## Style Rules (KodaCars-Specific)

- Currency: USD ($)
- Tone: B2B strategic, startup-aware, data-backed — speak to investors and operators
- Never use consumer language in LinkedIn content (no "check it out!", no emojis in strategy docs)
- Meta content can be human and visual — emotional, travel-adjacent
- Always differentiate from Turo and AirGarage when writing positioning copy
- When discussing SEO/AEO: always tie back to demo bookings as the conversion goal

---

## Report Password Gate (all HTML reports)

Every HTML report published to GitHub Pages must include a full-screen password gate before content loads.
- Password: `Kodacars123` (pattern: `{ClientName}123`, capital first letter)
- Uses `sessionStorage` so it's entered once per browser session; Enter key submits (not just the button)
- Embed gate CSS in the main `<style>` block, gate HTML + JS immediately after `<body>`
- Reason: prevents data leaks if a report URL is shared or indexed — client data is confidential

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
| HTML/PDF reports, strategy decks, PPTX | `01_Reports/` |
| LinkedIn copy, Meta copy, landing page copy | `02_Copy/` |
| Competitor analysis, keyword lists, SEO research | `03_Research/` |
| CSVs, raw exports, GSC data | `04_Data/` |
| Meeting transcripts | `transcripts/` |

Never save files to the root client folder — always route to a subfolder.

### On task completion
1. Mark the session log entry Completed in `action_tracker.md`
2. If a deliverable was produced: add a row to `deliverables.md`
3. If a new open action was identified: add it to the Open Actions table in `action_tracker.md`

---

## Critical Context (Read Before Every Session)

- KodaCars is pre-launch — no live campaigns, no ROAS metrics yet
- Domain Authority ~8, Spam score 56% — technical SEO is Month 1 priority
- Tracking (GA + GSC + GTM) already live on the site
- GBP category corrected to Software Company; video verification pending
- LinkedIn audience: hospitality GMs, lot owners, investors — NOT consumers
- Meta audience: everyday lot owners + airport travellers
- No competitor combines parking marketplace + P2P rental + shuttle — that is KodaCars' white space
- AEO: Parkable already showing on Google AI Overview — KodaCars must get there before more competitors
- $5M raise is active — all content and strategy should support investor confidence signals
