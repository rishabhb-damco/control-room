# Paid Ads Function Module

> Role: Paid Ads Manager / Account Lead
> Platforms: Google Ads, Meta Ads, LinkedIn Ads, Instagram
> This module is loaded by all client CLAUDE.md files.

---

## Weekly Reporting Format

When generating a weekly performance report, always include:

```
WEEKLY REPORT — [Client Name] — [Date Range]

PLATFORM SUMMARY
Google Ads:   Spend | Leads | CPL | CTR | CPC | Top campaign
Meta Ads:     Spend | Leads | CPL | CTR | Top audience
[Other]:      Spend | relevant KPIs

THIS WEEK vs LAST WEEK
↑ / ↓ / → for each key metric with % change

KEY WINS THIS WEEK
- [1-2 things that clearly worked]

KEY CONCERNS
- [1-2 things to flag]

ACTIONS TAKEN THIS WEEK
- [Optimisations made]

RECOMMENDED NEXT ACTIONS
1. [Highest priority]
2. [Second priority]
3. [Third priority]
```

---

## Transcript Processing — Paid Ads Output Format

When processing a meeting transcript for a Paid Ads account, generate all 5 outputs:

### Output 1: Client MOM Email
```
Subject: Meeting Notes — [Client Name] | [Date]

Hi [Client Contact],

Thank you for your time today. Here's a summary of what we covered:

KEY DISCUSSION POINTS
• [Point 1]
• [Point 2]

DECISIONS MADE
• [Decision 1]
• [Decision 2]

ACTION ITEMS
| Action | Owner | Due |
|--------|-------|-----|
| [action] | [who] | [when] |

Please confirm if we've captured everything correctly.

Best regards,
Rishabh
Damco Digital
```

### Output 2: Internal Team Briefing
```
INTERNAL BRIEF — [Client Name] — [Date]
NOT FOR CLIENT DISTRIBUTION

WHAT WAS DISCUSSED
- [Raw honest summary]

WHAT THE CLIENT IS THINKING
- [Signals, concerns, priorities they revealed]

WHAT WE COMMITTED TO
- [Exact commitments made]

RISK FLAGS
- [Anything that could become a problem]

WHAT RISHABH NEEDS FROM THE TEAM
- [Internal actions]
```

### Output 3: Action Tracker Update
```
NEW ACTIONS TO ADD TO action_tracker.md:
| Date | Action | Owner | Priority | Due | Status |
|------|--------|-------|----------|-----|--------|
| [date] | [action] | [owner] | [High/Med/Low] | [date] | Open |
```

### Output 4: Client Brief Update
```
SECTIONS TO UPDATE IN [ClientName_Claude.md]:
- Section: [which section]
  Add: [what to add]
```

### Output 5: Linear-Ready Paste
```
LINEAR UPDATE — [Client Name] — [Date]

[ACTION 1]
Assignee: [name]
Due: [date]
Priority: [High/Medium/Low]
Description: [one line]

[ACTION 2]
...
```

---

## Campaign Health Check Template

When asked to review campaign health, check:

**Google Ads:**
- [ ] CPL vs target — trending up or down?
- [ ] CTR by campaign — any below 2%?
- [ ] Quality Score on top keywords
- [ ] Negative keyword gaps (new wasted spend?)
- [ ] DSA vs Search CPA comparison
- [ ] Phone call conversion rate
- [ ] Scheduling rate (if tracked downstream)

**Meta Ads:**
- [ ] CPL vs target
- [ ] Frequency — above 3x = creative fatigue risk
- [ ] Audience overlap between ad sets
- [ ] Creative performance by format (Reel vs Static vs Carousel)
- [ ] Lead quality signals (scheduling rate, form completion rate)

---

## Email Templates

### Reporting Email (weekly/monthly)
Subject: [Client] — [Platform] Performance Report | [Month/Week]

### Escalation Email (budget/issue)
Subject: [Client] — [Issue] — Action Required

### Approval Request Email
Subject: [Client] — [Asset/Campaign] — Approval Needed Before [Date]

### Deliverable Handoff Email
Subject: [Client] — [Deliverable Name] Delivered | [Date]

---

## Performance Benchmarks by Platform

| Metric | Google Search | Google DSA | Meta (Lead Gen) | LinkedIn |
|---|---|---|---|---|
| Good CTR | >4% | >6% | >1.5% | >0.5% |
| Target CPL | Client-specific | 30-50% below Search | Below Search CPL | 3-5x Search CPL |
| CPC range | varies | lower than Search | varies | $5-15 B2B |
| Frequency cap | N/A | N/A | <3x | <4x |

---

## Red Flags to Always Escalate

- CPL spike >30% week-on-week without explanation
- CTR drop >25% on a previously stable campaign
- Zero conversions for 3+ days on a live campaign
- Ad account flagged or disapproved
- Budget pacing off by >15% from target
- Meta frequency above 4x with declining CTR
- Scheduling rate drops below 15% for a lead gen account
