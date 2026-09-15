# eSprinto — Claude Code Workspace

> Account Lead: Rishabh B | Damco Digital
> Function: Paid Ads + Social Media (Instagram, LinkedIn)
> Last configured: 2026-05-12

---

## Client Identity

| Field | Detail |
|---|---|
| Client | e-Sprinto |
| Industry | Electric Vehicles — EV Scooter |
| Market | India |
| Current focus | Bangalore (hyper-local) |
| Expansion target | Delhi, Pune, Jaipur, Lucknow (low competition) |
| Platforms | Instagram (active), Google Ads (planned), LinkedIn (planned) |
| Meeting cadence | TBD |
| Reports on | Reach, Engagement, CPF, Profile visits, Follower growth, Leads |

## Key Contacts

| Name | Role | Side |
|---|---|---|
| TBD | Client contact | eSprinto |
| Rishabh B | Account Lead / Paid Ads | Damco Digital |

---

## Files in This Folder

| File | Purpose |
|---|---|
| `eSprinto_Claude.md` | Living brief — competitor research, campaign data, strategy |
| `paid_ads_playbook.md` | Shared Paid Ads function module (output templates, health check, benchmarks) — local copy, previously `control room/modules/paid_ads.md` |
| `action_tracker.md` | All open and closed actions |
| `deliverables.md` | Deliverable log |
| `transcripts/` | Drop zone for meeting transcripts |
| `01_Reports/` | Generated HTML/PDF reports, campaign decks |
| `02_Copy/` | Ad copy, captions, hooks, scripts |
| `03_Research/` | Competitor notes, keyword lists, market research |
| `04_Data/` | CSVs, raw exports, data files |

---

## Workflow Commands

### "process transcript" or "process this transcript"
When I receive a transcript (pasted or saved in `transcripts/`):
1. Read `eSprinto_Claude.md` for context
2. Read `action_tracker.md` for current open items
3. Generate all 5 outputs (from `paid_ads_playbook.md`):
   - Client MOM email
   - Internal team briefing
   - Action tracker additions
   - Brief update suggestions
   - Linear-ready paste
4. Ask: "Shall I update the files now?"
5. On confirmation: update `action_tracker.md` and `eSprinto_Claude.md`

### "where are we?" or "account status"
Read all files and return:
```
eSPRINTO — ACCOUNT STATUS [today's date]

CHANNELS ACTIVE: [list]
LATEST CAMPAIGN: [summary]
OPEN ACTIONS: [count] — [top 3]
NEXT DELIVERABLE: [what + when]
TOP PRIORITY THIS WEEK: [one thing]
WATCH: [competitor activity or risk]
```

### "what's pending?" or "open actions"
Read `action_tracker.md` and list all Open items sorted by Priority.

### "draft email about [topic]"
Read `eSprinto_Claude.md` for context. Draft client email.
- Tone: energetic, forward-thinking (EV startup vibe), professional
- Currency: INR (₹)
- Sign off as: Rishabh | Damco Digital

### "log deliverable: [name]"
Add new row to `deliverables.md`. Confirm when done.

### "linear update"
Format all Open `action_tracker.md` items as Linear-ready paste.

### "update brief"
Ask what to add, then update `eSprinto_Claude.md`.

### "competitor check [brand]"
Read competitor sections in `eSprinto_Claude.md` and give a quick intelligence summary on that brand + any tactical gaps eSprinto can exploit.

### "campaign health check"
Run Instagram + paid media health check using data in `eSprinto_Claude.md`. Flag anything in red.

---

## Style Rules (eSprinto-Specific)

- Currency: INR (₹)
- Tone: confident, energetic, data-backed — EV startup energy
- Always frame messaging around real commuter savings (₹/month) not tech specs
- Competitor intel: always translate into "here's what eSprinto should do about it"
- City-specific framing: Bangalore first, then expand — never generic "India" messaging

---

## Report Password Gate (all HTML reports)

Every HTML report published to GitHub Pages must include a full-screen password gate before content loads.
- Password: `ESprinto123` (pattern: `{ClientName}123`, capital first letter)
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
| HTML/PDF reports, PPTX decks | `01_Reports/` |
| Ad copy, captions, hooks, scripts | `02_Copy/` |
| Competitor research, keyword lists, market research | `03_Research/` |
| CSVs, raw exports, data files | `04_Data/` |
| Meeting transcripts | `transcripts/` |

Never save files to the root client folder — always route to a subfolder.

### On task completion
1. Mark the session log entry Completed in `action_tracker.md`
2. If a deliverable was produced: add a row to `deliverables.md`
3. If a new open action was identified: add it to the Open Actions table in `action_tracker.md`

---

## Critical Context (Read Before Every Session)

- April 2026 Instagram boost: ₹499, 39,986 reach, 3 followers — giveaway attracted spectators not loyalists
- Profile drop-off is the main issue — people visit profile but don't follow
- Static creative tested; Reels not yet tested — this is the next experiment
- CTA was too direct (physical visit) for cold audience — need softer mid-step first
- Competitor white space: BGauss (no paid search), Sokudo (dark outside Diwali), Simple Energy (no North India) — all open for conquest
- LinkedIn files in eSprinto folder are actually KodaCars-targeted (hospitality B2B)
- Google Ads not yet launched — still to be set up
