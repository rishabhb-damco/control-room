# Wellspring — Standing Notes

> Folded in from Claude Code's local memory store on 10 July 2026, so these carry over to any machine (not just this Windows install). Add new learnings here going forward instead of relying on local memory alone.

---

## Call Assets, not Call-Only campaigns

Google has sunsetted Call-Only campaigns — do not recommend them as a standalone campaign type. The replacement is a **Call Asset** (formerly Call Extension) added to existing Search/DSA campaigns, combined with a Call conversion goal.

**Status:** Call Assets are already live on both the DSA campaign and Generic Search (Zendrik) campaign as of May 2026 — confirmed by Rishabh during June 2026 experiment planning. Do not propose "add call assets" as a new open action; frame it as an existing setup to leverage.

---

## Therapy focus only — Medication Management out of scope

As of 18 May 2026 (confirmed by Rishabh during Q3 experiment planning), Wellspring campaign planning, copy, and targeting focus on **therapy/counselling services only**. Medication Management, NP services, ADHD medication, and prescribing-related angles are out of scope.

Applies to: decks, briefs, ad copy, keyword recommendations, audience targeting. No reason was given for the decision — treat it as a fixed strategic call, not something to revisit unprompted.

---

## Section 1 KPI card sourcing (Google Ads Performance section)

The 6 KPI cards in every weekly report's Google Ads Performance section must consistently use **Google-attributed data only** — not total CRM data:

| KPI Card | Metric Source |
|---|---|
| Total Platform Conversions | Google-attributed CRM leads (7-rule classification) |
| Total Spend | Google Ads platform data (sum of all campaigns) |
| Blended CPL | Spend ÷ Google CRM leads |
| DSA CPA | Google Ads pixel data, DSA campaign only |
| Avg. CTR | Google Ads platform data |
| Google Leads Scheduled | Google CRM leads scheduled ÷ total Google CRM leads (NOT total CRM leads across all sources) |

Total CRM scheduling rate (e.g. 12/19 = 63.2%) belongs in **Section 2 — Overall Lead Analysis**, never in the Section 1 grid.

---

## Already codified in `CLAUDE.md` — no need to re-derive

- **Anomaly detection checklist** (missing days, uneven spend, budget over/under-delivery, campaign dominance, WoW spend drops, zero conversions) — see `CLAUDE.md` Step 4.
- **Week definition (Sunday–Saturday, not Monday–Sunday)** — see `CLAUDE.md` under "create weekly report."
- **Password gate pattern** (`Wellspring123`) — see `CLAUDE.md` Step 5. This pattern is shared across all clients; the full cross-client convention lives in the root `control room/memory_notes.md`.
