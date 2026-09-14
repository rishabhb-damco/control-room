# eSprinto Dealership Campaign — Meta Ads Performance Log

> This file is the running record for the B2B EV dealership recruitment Meta campaign (Delhi NCR). Every time new performance data is shared, an entry gets appended below so analysis builds on prior days rather than starting fresh each time. This is separate from the B2C Bangalore scooter-sales work in `eSprinto_Claude.md`.

## Campaign setup (baseline, 2026-08-06)

- **Objective:** Lead generation (Meta Instant Form)
- **Live creatives:** Concept 1 (English, direct-offer), Concept 2 (B2B EV leadership, "Apply Now"), Concept 1 Hindi variant
- **Ad sets (ABO):** Ad Set 1 = EV-interested audience; Ad Set 2 = investment/franchise-interested audience (non-EV-specific). All 3 creatives run as separate ads in both ad sets.
- **Full copy deck:** `../02_Copy/eSprinto_Dealership_Meta_Ad_Copy_28Jul2026.xlsx`

---

## Daily Entries

<!-- Append new entries below this line, most recent first. Each entry: date, raw metrics shared, diagnosis, recommendation, expected impact, what to monitor next. -->

### 2026-08-07 — First lead-level data (leads export, 2026-08-06 to 2026-08-07, no spend data yet)

**Data received:** Raw Meta lead export, 37 completed leads, with full qualifying-question answers (business background, commercial space status + area, investment capacity, timeline). No spend/impressions/CPL numbers in this file — that gap limits how far this analysis can go; cost-efficiency conclusions are NOT possible yet.

**What happened**
- 37 leads in under 24 hours across 3 live creatives and 2 ad sets.
- Ad-set split: Investment_Seekers 22, EV_Interest 15.
- Platform split: Instagram 22, Facebook 15.
- Creative split: "Static Ad 1 - English" 14, "Static Ad 1 - Hindi" 13, "Static Ad 1 - English_Futuristic" 10.
- Self-reported answers skew strongly toward the "ideal" option on every question: 24/37 already in automobile/EV dealership, 18/37 own commercial space outright, 30/37 say they can start immediately. 13/37 (35%) hit all three ideal answers simultaneously.
- Lead Quality Tracker created: `04_Data/eSprinto_Dealership_Lead_Quality_Tracker_MASTER.csv` (append future days here — see "Tracker convention" below).

**Why (evidence-backed)**
1. **Facebook leads are qualifying stronger than Instagram leads.** FB: 12/15 (80%) own their commercial space, 0 leads in the weakest "no space, willing to arrange" bucket, 13/15 ready immediately. IG: only 6/22 (27%) own space, 3/22 in the weakest space bucket, and IG is the only platform producing a 3-6-month (low urgency) lead. This is a real, evidence-backed platform gap, not a hunch — worth acting on.
2. **The audience segmentation is not clearly differentiating who applies.** The whole point of splitting Investment_Seekers vs EV_Interest was to reach two different psychographics. But business-background mix is nearly identical: 59% automobile/EV background in Investment_Seekers vs 73% in EV_Interest, both dominated by the same segment. Hypothesis, not yet confirmed: Meta's audience targeting for "investment/franchise interest" in India may not be precise enough to exclude EV-interested people, or the creative message itself (not the audience) is doing all the self-selection. Cannot confirm root cause without audience overlap/reach data from Ads Manager.
3. **2 of 37 leads (5.4%) are clearly non-genuine**: one full name is literally "Test," another is "Hidden man." Small in volume, but confirms some junk is getting through the form, worth a manual call-verification pass on a sample before trusting the "35% triple-ideal" number at face value.
4. **Found a typo in your own lead form**: the area dropdown has an option decoded as "15000-2000 sq. ft." — almost certainly meant to be "1,500-2,000 sq. ft." (it sits between the 1,000-1,500 and above-2,000 tiers). 5 leads selected this option. Recommend fixing this in the form directly; it's a credibility issue for anyone who reads their own submission back.

**What I can't conclude yet**
- Whether 37 leads/day is *good* — impossible to judge without spend. A ₹15-30L B2B decision producing 37 form-fills in a day is unusually high volume for a considered purchase; that alone is a reason to check CPL and lead-to-call-connect rate before assuming this is a win, not a reason to assume it's fake either (35% did give fully consistent, plausible answers).
- Whether the audience split is worth keeping as-is, worth continuing to run both ad sets for another few days before touching budget, since one week of data won't be enough to call this.

**Recommended next actions (prioritized)**
1. **Get spend/CPL data for this same window** — nothing below matters more; CPL is the number that turns "37 leads" into "good or bad."
2. **Manually call/verify a sample of ~10 leads** (mix of Hot-tier and the 2 flagged junk names) to check real-world answer-to-reality match. This calibrates whether the self-reported "Hot" tier can be trusted going forward.
3. **Pull Ads Manager audience overlap report** for Investment_Seekers vs EV_Interest to check if they're actually reaching distinct people or heavily overlapping.
4. **Fix the "15000-2000 sq. ft." typo** in the lead form, low effort, removes a credibility/data-quality issue.
5. **Consider shifting incremental budget toward Facebook** if the space-ownership and timeline gap holds up over a second day of data, it's currently the stronger-qualifying platform by a wide margin on this one day of evidence.

**Expected impact:** Can't quantify without spend data (see gap above). Directionally: fixing the form typo and re-verifying a lead sample are near-zero-cost, low-risk actions; shifting budget toward Facebook is the only recommendation here with real budget risk, and should wait for a second day of data before acting, one day is not enough to shift spend on.

**What to monitor next:** (a) CPL and spend by ad set and by platform once available, (b) whether the FB > IG qualification gap persists on day 2, (c) whether Investment_Seekers vs EV_Interest backgrounds stay similar or diverge with more volume, (d) call-connect rate on the "Hot" tier leads.

**Tracker convention going forward:** `04_Data/eSprinto_Dealership_Lead_Quality_Tracker_MASTER.csv` is the single running file, append new leads to it (don't create a new dated file each day) so the tracker stays queryable as one dataset. A dated snapshot of today's leads is also saved separately as `eSprinto_Dealership_Lead_Quality_Tracker_2026-08-06.csv` for reference. Scoring rubric used (documented so it's auditable, not a black box): Business background (automobile/EV=3, other dealership=2, other business=1, salaried=0) + Space (owned=2, rented=1, none=0) + Timeline (immediate=2, 1-3mo=1, 3-6mo=0) + flat 1 point for any stated investment capacity. Score >=6/8 = Hot, 3-5 = Warm, 0-2 = Cold; any obviously fake name overrides to "REVIEW." This rubric is based on self-reported form answers only, it is not verified intent, treat "Hot" as "worth calling first," not "confirmed serious."
