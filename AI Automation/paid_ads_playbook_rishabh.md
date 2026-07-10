# Paid Ads Operational Playbook — Rishabh B
> Contributed to: AI Automation Initiative
> Date: 27 May 2026
> Purpose: Decision rules, pre-flight checklist, and time SLAs for paid deliverables

---

## 1. Weekly Optimisation Decision Rules

### When to Pause an Ad

| Signal | Threshold | Action |
|---|---|---|
| High impressions, low CTR | 1,000+ impressions, CTR <0.4% | Pause. Rewrite headline — ad is not resonating |
| Clicks but no conversions | 15+ clicks, 0 conversions (same ad group has a converter) | Pause. Ad is attracting wrong intent |
| CTR drops suddenly | >35% drop week-over-week vs. same ad | Investigate — ad fatigue or competitor entered |
| Copy approved, still underperforming | Running 21+ days with stat sig volume, CTR still <0.5% | Pause, replace with fresh variant |

> **Rule of thumb:** Never pause an ad with fewer than 500 impressions. Insufficient data. Give it the week.

---

### When to Shift Budget

| Signal | Threshold | Action |
|---|---|---|
| Campaign outperforming on CPL | Campaign CPL <70% of target CPL, limited by budget | Increase daily budget 20–30%. Don't jump. |
| Campaign underperforming on CPL | Campaign CPL >150% of target CPL for 7+ consecutive days | Shift budget to the next-best campaign |
| DSA vs. Generic Search (Wellspring) | DSA CPL consistently 2x+ lower than Generic Search | Move 20% weekly budget from Generic → DSA until ratio is 70/30 |
| Campaign underpacing | Spending <70% of daily budget by mid-day consistently | Don't add budget. Investigate: bids too low, keywords too narrow, or audience exhausted |
| Campaign overpacing | Spending 100% budget before 6pm daily | Add 15–20% budget OR tighten ad scheduling to core hours |

---

### Alert Triggers (Flag Immediately — Don't Wait for Weekly Review)

| Trigger | Threshold | What It Usually Means |
|---|---|---|
| Conversion tracking gap | 0 conversions for 2+ consecutive days in an account that normally converts | Pixel broke, landing page changed, or URL mismatch |
| Spend anomaly — spike | Daily spend >200% of average | Budget cap removed, bid strategy switched to uncapped, or new campaign accidentally unlimited |
| Spend anomaly — drop | Daily spend <30% of average | Payment issue, account suspended, ads disapproved, scheduling error |
| Ad disapproval rate | >20% of active ads disapproved | Policy issue — check for restricted language (healthcare, finance, housing) |
| CTR cliff | Account-wide CTR drops >40% in a single week | Auction shift, landing page redirect broken, or headline stripped by platform |
| CPL spike | CPL increases >60% week-over-week with same spend | Competitor entered aggressively, landing page conversion dropped, or audience exhausted |

> **Wellspring-specific:** If conversions = 0 for 2 days — check Google Ads conversion tag on the "Thank You" page first. This has happened before.
> **eSprinto-specific:** If Meta spend spikes, check if audience size dropped (audience too narrow = delivery issues triggering broad spend bursts).

---

## 2. Pre-Flight Checklist — Top 7 Things That Have Bitten Us

In order of how often they cause silent failure (campaign goes live, looks fine, but doesn't actually work):

### ✓ 1. Conversion Tracking — Verify Before Going Live
- [ ] Pixel/tag installed on the correct page (thank you page, not the form page)
- [ ] Conversion action status shows "Active" (not "Unverified" or "No recent conversions")
- [ ] Test the conversion: use Google Tag Assistant or Meta Pixel Helper browser extension
- [ ] For Google: use "Test conversion" in the conversion action settings
- **Platform:** Google Ads + Meta | **Bite:** Campaign runs for a week, 0 reported conversions, wasted spend, client unhappy

### ✓ 2. UTM Parameters — On Every URL, Every Ad
- [ ] Every ad destination URL has UTM source, medium, campaign, content
- [ ] Format: `?utm_source=google&utm_medium=cpc&utm_campaign=[campaign-name]&utm_content=[ad-variant]`
- [ ] Test the URL — click it and check that UTM params appear in the browser bar (no redirect stripping them)
- [ ] Confirm they appear in GA4 / client analytics as expected
- **Platform:** All | **Bite:** Month-end reporting shows "direct" traffic instead of "paid" — client questions attribution

### ✓ 3. Landing Page — Does It Match the Ad?
- [ ] Ad headline matches landing page headline (or at least the same offer)
- [ ] CTA in ad ("Book a Free Consultation") matches CTA on page ("Schedule Now" is fine; "Contact Us" is not)
- [ ] Landing page loads in <3 seconds on mobile (test on Lighthouse or PageSpeed)
- [ ] Landing page form actually submits — fill it out and check that the thank-you page fires
- **Platform:** All | **Bite:** Good CTR, terrible conversion rate — mismatch between ad promise and page experience

### ✓ 4. Ad Scheduling — Default Is 24/7
- [ ] Confirm ad scheduling is set correctly (most clients want business hours, not 2am leads)
- [ ] For Wellspring: scheduling set to US Eastern timezone, not account default (which may be IST)
- [ ] For Meta: check timezone in Ad Account settings before setting schedule
- **Platform:** Google + Meta | **Bite:** Ads run overnight in the US, wasted budget on off-hours low-intent traffic

### ✓ 5. Audience Exclusions — Are They Set?
- [ ] Existing customers/leads excluded from prospecting campaigns
- [ ] For Meta: exclude Custom Audience of existing email list before running cold campaigns
- [ ] For Google Search: add negative keywords list before going live (not after first week of waste)
- [ ] For Wellspring specifically: add Medicaid, Medicare, HAP-related terms as negatives before launch
- **Platform:** All | **Bite:** Spend on audiences that would never convert, or worse — retargeting existing clients

### ✓ 6. Budget — Client vs. Platform Interpretation
- [ ] Confirm with client whether the quoted budget is weekly or monthly
- [ ] In Google Ads: daily budget × 30.4 = monthly max (platform can spend 2x daily on some days)
- [ ] In Meta: campaign budget vs. ad set budget — set at the right level
- [ ] Double-check: is this a test budget or the full launch budget?
- **Platform:** All | **Bite:** Client expects $500/week, but daily budget was set to $500 → $15,000 monthly. Serious.

### ✓ 7. Match Types — Especially on Google
- [ ] Confirm that no keywords are accidentally set to Broad Match when Phrase or Exact was intended
- [ ] Review the keyword list one more time before launch — check for duplicates across campaigns (keyword cannibalisation)
- [ ] Add a negative keyword list from day 1, not after seeing bad search terms week 2
- [ ] For new accounts: start with Exact + Phrase only. Never Broad Match without SKAG structure and solid negatives in place
- **Platform:** Google Ads | **Bite:** Broad match eats budget on irrelevant queries in week 1, burns client trust early

---

## 3. Time SLAs — Per Paid Deliverable

> These are working-day estimates. Client feedback/approval rounds are included. Internal-only tasks (no client approval loop) are faster — noted where relevant.

| Deliverable | SLA (Working Days) | What's Included | Bottleneck |
|---|---|---|---|
| **Single-platform campaign setup** (Google OR Meta, 1 campaign, 2–3 ad groups) | **3 working days** | Strategy brief → copy → targeting → build in platform → pre-flight checklist → QA → go-live | Client brief turnaround |
| **Multi-platform setup** (Google + Meta or Google + LinkedIn, coordinated launch) | **5–6 working days** | Same as above × 2 platforms, plus cross-platform audience logic and UTM consistency check | Platform account access + pixel setup at client end |
| **A/B test setup** (on an existing campaign — new variant only) | **1–2 working days** | New copy variant → new ad → set experiment or manual split → briefing on what to measure | Low — mostly internal |
| **Monthly performance report** | **Half day with automation (current state)** / **2–3 hours manually** | Data pull → analysis → PPT or HTML → review → send | Data access (Google Ads + sheets MCP) |
| **Weekly performance report** (Wellspring HTML) | **~5–10 minutes with skill** | Fully automated — data pulled, report generated, pushed to GitHub Pages | None currently |
| **Copy refresh** (rewriting headlines/descriptions in an existing campaign) | **1 working day** | Review current copy + performance → write 3–5 new variants → upload → QA | Approval if client reviews copy |
| **New keyword research** (for a new campaign or expansion) | **1 working day** | Keyword Planner pull → filtering → clustering → match type tagging → negative list | None — fully internal |
| **Search terms audit** (reviewing existing campaign search term reports for negatives + opportunities) | **2–3 hours** | Pull export → sort by spend → flag negatives → identify opportunities → formatted output | None — fully internal |
| **Campaign health audit** (structured review across all active campaigns) | **Half day** | Per-campaign CPL, CTR, quality score, budget pacing, disapproved ads, conversion tracking check | None — fully internal |
| **Lead quality analysis** (Wellspring / any consultation sheet) | **~5 minutes with skill** | Fully automated — classification + scheduling rate + source breakdown | None currently |

---

## Automation Opportunity Flags (For AI Automation Group)

| Rule / Item | Automation Potential | What to Build |
|---|---|---|
| Alert triggers (CPL spike, zero conversions, spend anomaly) | **High** | Claude Routine: daily check against Google Ads API / sheet data → flag if threshold breached |
| Pre-flight checklist | **High** | Skill: takes campaign brief as input → outputs checklist with yes/no for each item → blocks go-live until all checked |
| Weekly decision: pause / shift / hold | **Medium** | Skill: takes weekly performance table → runs decision rules → outputs recommended actions with rationale |
| SLA tracker | **Medium** | Add to action_tracker.md template — auto-calculate deadline from deliverable type + start date |

---

*Prepared by Rishabh B for the Damco Digital AI Automation Initiative | 27 May 2026*
