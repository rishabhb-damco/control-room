# eSprinto B2B Dealership Campaign — Lead Quality Analysis
**Source:** Google Sheet "eSprinto_Lead_Quality_Tracker" (raw Meta Lead Ads export, 339 rows, 06 Aug – 03 Sep 2026)
**Campaign:** Damco_B2B_Dealership_050826 · Form: eSprinto_Dealership_Delhi-NCR_050826
**Prepared:** 17 Sep 2026 · **Updated:** 17 Sep 2026 (qualification baseline changed — see below)

---

## 0. Method note

The sheet has **no explicit "booked meeting" column**. Outcome was inferred from the free-text `Remarks` field and `Date of call`, using rule-based keyword classification (reproducible, not manual per-row judgment). A small share of remarks (4–5%) are ambiguous and grouped as "Other/Unclassified." No spend/CPL data exists in this sheet, so this remains a lead-quality/funnel report, not a cost-efficiency one (still Open Action #11).

## 0.5 Baseline change (effective 17 Sep 2026)

**Rishabh's instruction:** leads that stated an investment capacity below ₹25 lakh are no longer being pursued and should be excluded from the working analysis. The form's "₹20–25 lakh" bucket straddles that line — per Rishabh, it is **excluded from the main baseline** but reported **separately** below so its performance stays visible.

This changes the qualified base dramatically:

| Segment | Leads | % of total 339 | Status |
|---|---|---|---|
| **₹25–30 lakh + ₹30 lakh+ ("Qualified")** | **30** | **8.8%** | **New main baseline — used in §1–§6 below** |
| ₹20–25 lakh | 24 | 7.1% | Reported separately in §7 — not part of the baseline |
| ₹15–20 lakh | 285 | 84.1% | Excluded entirely from consideration |

**The size of that last row is itself the headline finding.** Under the new ₹25L threshold, **91% of all leads this campaign has produced (309/339) are no longer relevant.** If ₹25L+ is genuinely the investment level eSprinto wants to recruit at, the current campaign — form, creative, and targeting alike — is overwhelmingly attracting the wrong applicant profile. That is a targeting/qualification design problem, not just a follow-up problem, and it's addressed directly in §2 and §8.

All findings from §1 onward use the **30-lead qualified base** unless stated otherwise. Sample sizes at this level are small — most creative/ad-set cells contain single digits — so read directional patterns as early signal to monitor, not as a basis for immediate budget reallocation. Where a pattern isn't reliable at n=30, that's stated explicitly rather than forced into a conclusion.

---

## 1. Lead Quality Analysis (Qualified base, n=30)

| Stage | Count | % of total (30) | % of contacted (16) |
|---|---|---|---|
| Not contacted yet | 14 | 46.7% | — |
| Interested for meeting | 3 | 10.0% | 18.8% |
| Info-stalled (asking for company details/specs first) | 3 | 10.0% | 18.8% |
| Other/unclassified | 3 | 10.0% | 18.8% |
| Disqualified — already has a dealership | 2 | 6.7% | 12.5% |
| Timing deferred | 2 | 6.7% | 12.5% |
| Unreachable | 2 | 6.7% | 12.5% |
| Interested but also info-stalled | 1 | 3.3% | 6.3% |

**Summary of contacted (16):** positive intent 43.8% (7/16) · unreachable 12.5% (2/16) · disqualified 12.5% (2/16).

### Biggest reason qualified leads don't convert into meetings

1. **They're not being called — and this segment is your most valuable one.** 14 of 30 qualified leads (46.7%) have zero recorded follow-up — proportionally worse than the 42.2% no-contact rate across the full dataset. These are your highest-investment-capacity applicants and nearly half sit untouched.
2. **Once contacted, quality is genuinely decent and cleaner than the general pool.** Disqualification is only 12.5% of contacted qualified leads (vs 8.4% of contacted leads across the whole dataset — comparable), and notably **zero budget-mismatch or wrong-need disqualifications** appear in this segment (both categories were present in the broader pool). The two disqualifications here are both "already has a dealership" — *"Not Dealership required. Already discussed with owner sir required in bulk but pricing did not matched so purchased from another Supplier"* and *"Already taken the dealership from Noida"* — i.e., lost to a competitor's follow-up speed, not a bad-fit lead.
3. **The same "asking for company details first" stall shows up here too** — *"Asking company details with EV specification afterthat he will decide," "Asking company details," "Asking company details with product specification," "Interested for meeting company details required."* This confirms the collateral-gap finding from the full dataset isn't specific to lower-tier leads — it's a universal follow-up process gap.
4. Two of the highest-quality individual remarks in the entire dataset sit in this segment: *"Interested for meeting/he is distributor of 6 company"* and *"Interested for meeting"* paired with ₹30L+ capacity — genuinely strong prospects that should be prioritised first once follow-up capacity is addressed.

### Trend over time (qualified leads)

| Week (Sun start) | Qualified leads in | Contacted |
|---|---|---|
| 02 Aug | 7 | 7 (100%) |
| 09 Aug | 12 | 2 (17%) |
| 16 Aug | 4 | 0 (0%) |
| 23 Aug | 5 | 5 (100%) |
| 30 Aug | 2 | 2 (100%) |

Same pattern as the full dataset: the 9–16 Aug volume spike is where qualified leads went uncalled (16 of the 30 qualified leads' 2-week window), and contact rate recovered to 100% afterward. **This means the highest-value leads generated during that spike are very likely still sitting uncalled today** — worth pulling and actioning immediately, separate from any process fix.

---

## 2. Top Priorities (revised for the ≥₹25L baseline)

1. **Investigate why 91% of leads fall below the ₹25L threshold before touching follow-up or creative.** This is a targeting/form design question, not a funnel-execution one: either the audience being reached skews toward smaller operators, or the form's investment-capacity options and ad messaging (₹15–20L is the default/most-selected bucket) are self-selecting for exactly the segment no longer wanted. Pulling Ads Manager audience composition and re-examining whether the ad copy's financial framing (see `02_Copy/eSprinto_Dealership_Meta_Ad_Copy_28Jul2026.xlsx`) implicitly targets a lower investment tier is the highest-leverage next step.
2. **Immediately work the backlog of uncalled qualified leads**, especially the ~12 still-uncalled from the 9–16 Aug spike — these are scarce (only 30 total) and high-value; losing them to a competitor's faster follow-up (as already happened twice in this segment) is a direct, avoidable revenue loss.
3. **Build the WhatsApp-ready company profile / price / spec sheet and send it on first contact** — the "asking company details first" stall appears in this segment too, so it isn't a lower-tier-lead problem; it's worth fixing regardless of which tier ends up mattering most.
4. **Don't reallocate creative or ad-set budget off the qualified segment yet** — n=30 (16 contacted) is too small to read reliably; see §3–§5 caveats. Let it accumulate for 2–3 more weeks post-fix before making a creative call on this basis alone.
5. **Use the ₹20–25L bucket (§7, n=24) as an early-warning signal only**, not a decision basis — it shows some concerning divergence (e.g. Hindi + EV_Interest unreachable rate of 75%) worth watching as more ₹25L+ volume comes in, since it's adjacent to the new baseline.
6. **Re-run this analysis in 2–4 weeks** once qualified volume grows past ~60–80 leads — that's roughly the minimum needed before creative/ad-set splits stop being single-digit-cell noise.

---

## 3. Creative Analysis (Qualified base, n=30 — small sample, read directionally only)

| Creative | Total | Contacted | Positive % | Unreachable % | Disqualified % |
|---|---|---|---|---|---|
| Static Ad 1 - English | 14 | 9 | 33.3% (3) | 22.2% (2) | 11.1% (1) |
| Static Ad 1 - Hindi | 11 | 6 | 66.7% (4) | 0% (0) | 16.7% (1) |
| Static Ad 1 - English_Futuristic | 5 | 1 | 0% (0) | 0% (0) | 0% (0) |

**Caveat:** English_Futuristic has only 1 contacted lead in this segment — no conclusion is possible there. Hindi's 66.7% positive rate is based on 4 of 6 contacted leads — directionally consistent with its strong performance in the full dataset (47% positive at n=180), but not statistically reliable on its own at this size. English remains the comparatively weaker performer here too, consistent with the full-dataset finding.

No creative-level cost or delivery data exists to compute efficiency (§0 method note applies here as well).

---

## 4. Ad Set Analysis (Qualified base, n=30)

| Ad set | Total | Contacted | Positive % | Unreachable % | Disqualified % |
|---|---|---|---|---|---|
| EV_Interest | 15 | 6 | 50.0% (3) | 0% (0) | 16.7% (1) |
| Investment_Seekers | 15 | 10 | 40.0% (4) | 20.0% (2) | 10.0% (1) |

Evenly split by volume (15/15) — interesting on its own, since it suggests neither ad set is inherently better at surfacing ₹25L+ applicants specifically. Outcome quality is close between the two (50% vs 40% positive) but n is far too small (6 and 10 contacted) to call a winner.

---

## 5. Cross-Analysis: Ad Set × Creative (Qualified base, n=30 — indicative only)

| Ad set | Creative | Total | Contacted | Positive | Unreachable | Disqualified |
|---|---|---|---|---|---|---|
| Investment_Seekers | English | 9 | 6 | 2 (33.3%) | 2 (33.3%) | 1 (16.7%) |
| EV_Interest | Hindi | 6 | 3 | 2 (66.7%) | 0 | 1 (33.3%) |
| EV_Interest | English | 5 | 3 | 1 (33.3%) | 0 | 0 |
| Investment_Seekers | Hindi | 5 | 3 | 2 (66.7%) | 0 | 0 |
| EV_Interest | English_Futuristic | 4 | 0 | — | — | — |
| Investment_Seekers | English_Futuristic | 1 | 1 | 0 | 0 | 0 |

Every cell here has 6 or fewer leads (many with 3 or fewer contacted) — **no combination in this table is large enough to act on.** The one pattern worth flagging as "watch, don't act": Hindi looks strong in both ad sets again at this tier (consistent with §3 and the full dataset), while English_Futuristic simply hasn't produced enough qualified volume yet to say anything.

---

## 6. Action Plan (Qualified/≥₹25L baseline)

### Do Now
- Pull and call the ~12 uncalled qualified leads from the 9–16 Aug backlog immediately — small in number, high value, time-sensitive (already lost 2 of 30 to competitors in this tier).
- Investigate the 91%-below-threshold finding with the media/targeting team — this is now the single biggest lever, bigger than any creative or ad-set tweak.
- Build and start sending the WhatsApp company profile / price / spec sheet on first contact for all tiers, qualified included.

### Test Next
- Once targeting/audience adjustments are made in response to the ₹25L finding, watch whether the *mix* of investment-capacity responses shifts (i.e., does the ₹15–20L share actually shrink).
- Re-test creative allocation only after qualified volume reaches roughly 60–80 leads (currently 30) — not before.

### Monitor
- Weekly qualified-lead contact rate — re-check this after any volume spike, since the 9–16 Aug backlog pattern would recur in the same way for high-value leads too.
- ₹20–25 lakh bucket (§7) as a leading indicator of how the ≥25L pool may behave once it's larger.

### Stop/Reduce
- Stop making creative or ad-set budget decisions based on the qualified segment alone until volume grows — every table in §3–§5 is currently single-digit-cell territory.

---

## 7. ₹20–25 Lakh Bucket — Reference Breakout (n=24, NOT part of the qualified baseline)

Kept visible per Rishabh's request, since this bucket sits just under the new ₹25L line and may be informative even though it's excluded from the main analysis.

**Funnel:** 24 total, 18 contacted (75.0%) — a notably higher contact rate than the qualified segment (53.3%) or full dataset (57.8%).

| Stage | Count | % of contacted (18) |
|---|---|---|
| Unreachable | 5 | 27.8% |
| Interested for meeting | 3 | 16.7% |
| Other/unclassified | 3 | 16.7% |
| Timing deferred | 2 | 11.1% |
| Info-stalled | 2 | 11.1% |
| Disqualified — wrong need | 2 | 11.1% |
| Disqualified — already has dealership | 1 | 5.6% |

Positive 27.8% (5/18) · unreachable 27.8% (5/18) · disqualified 16.7% (3/18) — **noticeably weaker outcome quality than the qualified (≥25L) segment's 43.8% positive rate**, which is a reasonable sanity check that the ₹25L cutoff is doing real qualification work, not an arbitrary line.

**By creative:**

| Creative | Total | Contacted | Positive % | Unreachable % |
|---|---|---|---|---|
| Static Ad 1 - Hindi | 8 | 6 | 0% | 50.0% |
| Static Ad 1 - English_Futuristic | 8 | 6 | 50.0% | 0% |
| Static Ad 1 - English | 7 | 6 | 33.3% | 33.3% |

**Notable divergence from the full-dataset pattern:** Hindi — the strongest creative overall and in the qualified segment — has a **0% positive rate and 50% unreachable rate** in this bucket specifically, driven largely by EV_Interest pairing (*EV_Interest + Hindi: 3 of 4 contacted unreachable*). English_Futuristic, weak in EV_Interest at the full-population level, looks comparatively better here (50% positive) and is strongest paired with Investment_Seekers (2 of 3 contacted positive). This is a single 24-lead bucket, so treat it as a flag to watch as the ≥25L segment grows, not a standalone conclusion.

---

## Appendix: Full unfiltered dataset (all 339 leads, reference only — includes the now-excluded <₹25L leads)

This is the original analysis run before the 17 Sep 2026 baseline change, kept for context on overall Meta funnel behaviour (contact-rate discipline, collateral gaps, unreachability) since those process issues apply across all tiers, not just the qualified one.

### A.1 Full-dataset funnel (n=339)

| Stage | Count | % of total | % of contacted (196) |
|---|---|---|---|
| Not contacted yet | 143 | 42.2% | — |
| Unreachable | 54 | 15.9% | 27.6% |
| Interested for meeting | 40 | 11.8% | 20.4% |
| Info-stalled | 30 | 8.8% | 15.3% |
| Interested + info-stalled | 13 | 3.8% | 6.6% |
| Timing deferred | 13 | 3.8% | 6.6% |
| Disqualified — not required | 12 | 3.5% | 6.1% |
| Disqualified — already has dealership | 8 | 2.4% | 4.1% |
| Disqualified — wrong need | 8 | 2.4% | 4.1% |
| Meeting confirmed | 2 | 0.6% | 1.0% |
| Disqualified — budget | 1 | 0.3% | 0.5% |
| Other/unclassified | 15 | 4.4% | 7.7% |

### A.2 Full-dataset weekly trend

| Week | Leads in | Contacted | Not contacted |
|---|---|---|---|
| 02 Aug | 73 | 67 | 6 |
| 09 Aug | 116 | 32 | 84 |
| 16 Aug | 72 | 19 | 53 |
| 23 Aug | 40 | 40 | 0 |
| 30 Aug | 38 | 38 | 0 |

### A.3 Full-dataset creative performance (n=339)

| Creative | Total | Contacted | Positive % | Unreachable % | Disqualified % |
|---|---|---|---|---|---|
| Static Ad 1 - Hindi | 180 | 103 | 47% | 31% | 12% |
| Static Ad 1 - English | 85 | 52 | 37% | 25% | 19% |
| Static Ad 1 - English_Futuristic | 73 | 41 | 44% | 22% | 17% |

### A.4 Full-dataset ad set performance (n=339)

| Ad set | Total | Contacted | Positive % | Unreachable % | Disqualified % |
|---|---|---|---|---|---|
| EV_Interest | 179 | 98 | 42% | 30% | 15% |
| Investment_Seekers | 159 | 98 | 45% | 26% | 14% |

### A.5 Full-dataset ad set × creative cross-tab (n=339)

| Ad set | Creative | Total | Contacted | Positive % | Unreachable % | Disqualified % |
|---|---|---|---|---|---|---|
| Investment_Seekers | English_Futuristic | 27 | 20 | 55% | 15% | 10% |
| EV_Interest | Hindi | 87 | 52 | 48% | 31% | 12% |
| Investment_Seekers | Hindi | 93 | 51 | 45% | 31% | 12% |
| Investment_Seekers | English | 39 | 27 | 37% | 22% | 22% |
| EV_Interest | English | 46 | 25 | 36% | 28% | 16% |
| EV_Interest | English_Futuristic | 46 | 21 | 33% | 29% | 24% |

### A.6 Other full-dataset observations (unchanged from original analysis)

- Space ownership is the strongest quality signal: 50% positive for "owns space" vs 23% for "no space, willing to arrange" (which also has the worst unreachable rate, 41%).
- 5 leads flagged "repeated lead" (duplicate submissions); 4 leads clearly outside Delhi-NCR (Andhra Pradesh, Hyderabad) plus 1 Telugu-language call; at least 5 leads want bulk/fleet vehicle purchase rather than a dealership.
- The "15000–2000 sq. ft." area-field typo (Open Action #14) affects 26 rows of the area column dataset-wide.

*This appendix is retained for process-level insight only. For qualification and prioritization decisions going forward, use §1–§7 above, which reflect the ≥₹25L baseline.*
