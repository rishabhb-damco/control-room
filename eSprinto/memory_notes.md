# eSprinto — Standing Notes

> Folded in from Claude Code's local memory store on 10 July 2026, so these carry over to any machine (not just this Windows install). Add new learnings here going forward instead of relying on local memory alone.

---

## Meta Campaign Creative Plan (as of June 2026)

**Campaign overview**
- Objective: acquire 25–30 signed dealership partners
- Period: July – October 2026 (4 months)
- Primary channel: Meta Ads (Lead objective, CBO)
- Confirmed audience: 9.54 lakh – 17 lakh (verified in Meta Ads Manager)
- 28 cities across 3 regions (South 12, West 11, North 5)
- Monthly budget: INR 1.31 lakh | Total: INR 5.22 lakh
- CTR: 2.5% | Click-to-Lead: 5% | CPL: INR 560

**Final creative structure — 17 creatives total**

*Static creatives — 11 (one per state)* — state name appears in visual and copy:

| Region | State | Cities Covered |
|---|---|---|
| South | Andhra Pradesh | Vijaywada · Guntur |
| South | Telangana | Hyderabad · Nizamabad |
| South | Karnataka | Bangalore · Mysuru · Mangalore |
| South | Tamil Nadu | Chennai · Coimbatore |
| South | Kerala | Kochi · Calicut · Trivandrum |
| West | Gujarat | Ahmedabad · Surat · Vadodara |
| West | Maharashtra | Pune · Nagpur · Nashik · Aurangabad · Mumbai |
| West | Goa | All Cities |
| West | Madhya Pradesh | Indore · Bhopal |
| North | Delhi NCR | Ghaziabad · Noida |
| North | Rajasthan | Jaipur · Jodhpur · Udaipur |

*Reel creatives — 6 (two per region, two different concepts each)* — region-level, one creative covers all states in the region:

| Region | Coverage | Concepts |
|---|---|---|
| South | AP · Telangana · Karnataka · Tamil Nadu · Kerala | 2 reels (2 concepts) |
| North | Delhi NCR · Rajasthan | 2 reels (2 concepts) |
| West | Gujarat · Maharashtra · Goa · MP | 2 reels (2 concepts) |

**Why 6 reels, not 3:** each region needs 2 concept variations to test which angle (territory vs timing vs trust) performs best per region.

**Tracker file:** `eSprinto_Meta_Creative_Tracker_v3.xlsx` — Windows: `C:\Users\Rishabhb\Downloads\eSprinto_Meta_Creative_Tracker_v3.xlsx` · Mac: `~/Downloads/eSprinto_Meta_Creative_Tracker_v3.xlsx`
- Sheet: single sheet "Creative Planner"
- Columns: Campaign, Region, State, Cities Covered, Creative Type, Creative Concept, Creative Copy, Hook/Opening Line, Primary Text, Chars, Headline, Chars, Description, Chars, CTA, Status, Owner, Notes
- All copy columns blank — to be filled by content writer

**Key creative angles (priority order):**
1. Territory exclusivity — "You would be the only dealer in your state"
2. Market timing — "EV sales grew 150% in Tier 2 India"
3. Fleet trust / commercial proof — "Fleet operators depend on this daily"
4. Investment clarity — "INR 5.22 lakh, exclusive territory"

**Campaign structure:** 2 ad sets (Entrepreneurs/Owners, EV + Investors) × 4 creative concepts (Territory, Numbers, Fleet Trust, Market Timing). Funnel: YouTube awareness → Meta lead capture → WhatsApp conversion.

**Live status (as of 6 Aug 2026):** only 3 of the 5 drafted concepts are actually running — Concept 1 (English direct-offer, no rupee figure, CTA "Apply for Dealership"), Concept 2 (B2B EV leadership positioning, CTA "Apply Now"), and a Hindi variant of Concept 1. Ad sets run ABO (manual budget per ad set), split by audience (EV-interested vs. investment/franchise-interested) rather than by creative — all 3 live creatives run as separate ads within both ad sets. Full ad copy deck (all 5 concepts, English + Hindi, character-limit-validated): `02_Copy/eSprinto_Dealership_Meta_Ad_Copy_28Jul2026.xlsx` + matching `.md`.

**Compliance notes:** Meta requires SEBI/AMFI disclosure for this account; correctly declared NOT registered since dealership recruitment isn't a securities offering (triggers a public "not registered" disclosure in Meta's Ad Library). Ad copy avoids "invest/ROI/returns" framing in favor of "business/margins" framing. The "#1 player in B2B EV" ranking claim is only on the creative image, not restated as fact in copy text, since unsubstantiated superiority claims are commonly challenged under India's ASCI code.

**Lead Quality Tracker:** `04_Data/eSprinto_Dealership_Lead_Quality_Tracker_MASTER.csv` is the single running file for lead-level data — append new leads here, don't create new dated files each day. Scoring rubric: business background + commercial space status + timeline + investment capacity, self-reported only, not verified intent. First pull (7 Aug 2026, 37 leads): Facebook leads qualify meaningfully stronger than Instagram leads; the Investment_Seekers vs EV_Interest ad-set split isn't clearly differentiating who applies; a typo in the lead form's area dropdown ("15000-2000 sq. ft."); 2/37 leads with clearly fake names.

Daily metrics/analysis for this campaign should be logged to `04_Data/meta_dealership_ads_performance_log.md` so future sessions build on historical trends rather than analyzing each day in isolation. This is a distinct workstream from the B2C Bangalore scooter-sales Instagram work above — don't conflate audiences or learnings between the two.

---

## Meta Ads Performance Consultant mode

When the user shares eSprinto Meta Ads campaign data (metrics, creatives, ad copy, CTR/CPC/CPM/CPL, frequency, conversion rates, landing page performance) — for either the B2C Bangalore campaign or the B2B dealership campaign above — respond as a 15+ year veteran Meta Ads performance marketer running an ongoing consulting engagement, not as someone giving one-off generic advice:

- Diagnose root causes, not symptoms. Cover: what happened, why (with evidence), what to do next, expected impact, what to monitor afterward.
- Prioritize recommendations by expected business impact, not by how easy they are to explain.
- Challenge the user's assumptions when the data suggests a different conclusion — don't validate a take just because it was offered as a question.
- Distinguish explicitly between fact, hypothesis, and assumption; say so if there isn't enough data to conclude something.
- Propose specific next tests with a clear hypothesis and expected outcome, covering structure, budget/bidding, audience, creative (hook, fatigue, visual hierarchy, CTA), copy, placements, learning phase, frequency, funnel/landing page, lead quality, scaling.
- Build cumulative, longitudinal analysis — reference prior days' data and trends rather than evaluating each new data drop in isolation.

**Why:** User set this up as a standing engagement (not a single task) on 6 Aug 2026, to maximize qualified lead gen and profitability through rigorous analysis — explicitly not just validating assumptions or repeating generic best practices. Apply automatically, without needing to be re-established each session.

---

## Shared conventions

Report password gate pattern (`ESprinto123`) — full-screen gate before content loads, `sessionStorage` so it's entered once per browser session, Enter key submits. See `CLAUDE.md` → Report Password Gate.
