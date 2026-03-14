# Data Tracking Templates for EDM Campaigns

## Why Data Tracking Matters

**"What gets measured gets managed"**

Without tracking:
- You don't know what worked
- You can't improve future campaigns
- You waste budget on ineffective strategies

With tracking:
- Optimize based on real data
- Prove ROI to stakeholders
- Build institutional knowledge

---

## UTM Parameter System

### Standard UTM Structure

```
?utm_source=email
&utm_medium=email
&utm_campaign=[campaign_name]
&utm_content=[email_number]_[variant]_[audience_segment]
```

### Campaign Naming Convention

```
[brand]_[campaign_type]_[month_year]

Examples:
- winbridge_springvoice_mar2026
- yatai_ramadan_mar2026
- acme_productlaunch_apr2026
```

### Content Naming Convention

```
[email_number]_[variant]_[audience]

Examples:
- edm1_a_teachers      (Email 1, Variant A, Teachers)
- edm1_b_teachers      (Email 1, Variant B, Teachers)
- edm2_control_all     (Email 2, No test, All audiences)
- edm3_a_fitness       (Email 3, Variant A, Fitness)
```

### Complete URL Examples

```
https://www.winbridge.com/products/voice-amplifier
?utm_source=email
&utm_medium=email
&utm_campaign=winbridge_springvoice_mar2026
&utm_content=edm1_a_teachers

Full URL:
https://www.winbridge.com/products/voice-amplifier?utm_source=email&utm_medium=email&utm_campaign=winbridge_springvoice_mar2026&utm_content=edm1_a_teachers
```

---

## KPI Tracking Dashboard

### Campaign Overview Sheet

```markdown
# Campaign: [Campaign Name]
Date Range: [Start] - [End]

## Executive Summary
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Total Revenue | $X | $___ | 🟡/🟢/🔴 |
| ROI | 3:1 | ___:1 | 🟡/🟢/🔴 |
| New Customers | X | ___ | 🟡/🟢/🔴 |
| AOV | $X | $___ | 🟡/🟢/🔴 |

## Email Performance by Send

| Email # | Send Date | Audience | Open Rate | Click Rate | Conv. Rate | Revenue |
|---------|-----------|----------|-----------|------------|------------|---------|
| EDM 1 | 3/4 | Teachers | ___% | ___% | ___% | $___ |
| EDM 2 | 3/11 | Fitness | ___% | ___% | ___% | $___ |
| EDM 3 | 3/18 | Guides | ___% | ___% | ___% | $___ |
| EDM 4 | 3/25 | All | ___% | ___% | ___% | $___ |

## Audience Performance

| Segment | Sent | Opened | Clicked | Converted | Revenue |
|---------|------|--------|---------|-----------|---------|
| Teachers | ___ | ___ | ___ | ___ | $___ |
| Fitness | ___ | ___ | ___ | ___ | $___ |
| Guides | ___ | ___ | ___ | ___ | $___ |
| Business | ___ | ___ | ___ | ___ | $___ |

## Key Insights
- Best performing email: [Which and why]
- Worst performing email: [Which and why]
- Best audience: [Which segment]
- Best subject line: [Which variant]
- Lessons for next campaign: [3-5 bullet points]
```

---

## A/B Test Results Log

### Test Results Template

```markdown
# A/B Test Results - [Campaign Name]

## Test 1: Subject Lines (EDM 1)

| Variant | Subject Line | Sent | Opened | Open Rate | Winner? |
|---------|--------------|------|--------|-----------|---------|
| A | "Save 20% on amplifiers" | 500 | 115 | 23% | |
| B | "Your voice is your career" | 500 | 140 | 28% | ✅ +22% |
| C | "Last chance: Sale ends" | 500 | 95 | 19% | |

**Winner: Variant B**
- Lift: +22% open rate vs. A
- Lift: +47% open rate vs. C
- Sent to remaining 80%: 2,000 recipients

**Insight:** Emotional resonance (career protection) outperformed discounts and urgency.

---

## Test 2: CTA Buttons (EDM 2)

| Variant | CTA Text | Clicks | Click Rate | Winner? |
|---------|----------|--------|------------|---------|
| A | "Shop Now" | 45 | 9% | |
| B | "Protect Your Voice" | 62 | 12.4% | ✅ +38% |

**Winner: Variant B**
- Lift: +38% click rate
- Benefit-focused CTA outperformed action-focused

---

## Test 3: Send Time (EDM 3)

| Variant | Send Time | Open Rate | Click Rate | Winner? |
|---------|-----------|-----------|------------|---------|
| A | 9:00 AM | 26% | 5.2% | ✅ |
| B | 3:00 PM | 21% | 4.1% | |

**Winner: Variant A (9:00 AM)**
- Morning sends performed 24% better
- Likely: Checking email before work

---

## Cumulative Learning

### What Works for Our Audience:
1. ✅ Emotional subject lines (career, health)
2. ✅ Benefit-focused CTAs
3. ✅ Morning send times (9 AM)
4. ✅ Customer testimonials
5. ✅ Problem-focused hero images

### What Doesn't Work:
1. ❌ Discount-only subject lines
2. ❌ Generic CTAs ("Click Here")
3. ❌ Evening sends
4. ❌ Product-only emails (no pain point)
5. ❌ Too many CTAs

### Next Campaign Recommendations:
- [ ] Start with emotional subject lines
- [ ] Always include customer testimonial
- [ ] Test: Long-form vs. short-form content
- [ ] Test: Video vs. static images
```

---

## Subject Line Performance Tracker

### Subject Line Database

```markdown
| Date | Subject Line | Type | Audience | Open Rate | Sentiment | Notes |
|------|--------------|------|----------|-----------|-----------|-------|
| 3/4 | "Save 20% today" | Discount | Teachers | 23% | 😐 | Weak |
| 3/4 | "Your voice is your career" | Emotional | Teachers | 28% | 😊 | Strong |
| 3/11 | "5 days left" | Urgency | Fitness | 19% | 😕 | Poor |
| 3/11 | "Lead without shouting" | Benefit | Fitness | 27% | 😊 | Strong |

**Top Patterns:**
1. Emotional/personal > Discount
2. Benefit-focused > Feature-focused
3. Specific > Generic
4. Question format performs well
```

---

## Revenue Attribution

### Revenue Tracking

```markdown
# Revenue Attribution - [Campaign]

## By Email
| Email | Direct Revenue | Assisted Revenue | Total |
|-------|----------------|------------------|-------|
| EDM 1 | $X | $X | $X |
| EDM 2 | $X | $X | $X |
| EDM 3 | $X | $X | $X |
| EDM 4 | $X | $X | $X |

## By Product
| Product | Units Sold | Revenue | % of Total |
|---------|------------|---------|------------|
| H5 | ___ | $___ | ___% |
| S97 | ___ | $___ | ___% |
| 40W | ___ | $___ | ___% |
| M31 | ___ | $___ | ___% |

## By Audience
| Segment | Revenue | AOV | Conversion Rate |
|---------|---------|-----|-----------------|
| Teachers | $___ | $___ | ___% |
| Fitness | $___ | $___ | ___% |
| Guides | $___ | $___ | ___% |

## ROI Calculation
- Campaign Cost: $___ (design, tools, time)
- Total Revenue: $___
- Net Profit: $___
- ROI: ___:1
```

---

## List Health Tracking

### Email List Metrics

```markdown
# List Health Report - [Month]

## Growth
| Metric | Start | End | Change |
|--------|-------|-----|--------|
| Total Subscribers | ___ | ___ | +___% |
| Active (90 days) | ___ | ___ | +___% |
| New Subscribers | ___ | ___ | |

## Engagement
| Metric | Rate | Benchmark | Status |
|--------|------|-----------|--------|
| Avg Open Rate | ___% | 25% | 🟡/🟢/🔴 |
| Avg Click Rate | ___% | 5% | 🟡/🟢/🔴 |
| Unsubscribe Rate | ___% | <0.5% | 🟡/🟢/🔴 |
| Bounce Rate | ___% | <2% | 🟡/🟢/🔴 |
| Complaint Rate | ___% | <0.1% | 🟡/🟢/🔴 |

## List Quality
- Inactive (>6 months): ___%
- Engaged (opened last 3 emails): ___%
- VIP (high value customers): ___%
- At-risk (declining engagement): ___%

## Actions Taken
- [ ] Cleaned inactive subscribers
- [ ] Re-engagement campaign sent
- [ ] Segmentation updated
- [ ] New signup forms deployed
```

---

## Automation & Tools

### Recommended Tools

**Email Platform:**
- Klaviyo (best for e-commerce)
- Mailchimp (good for beginners)
- HubSpot (all-in-one marketing)

**Analytics:**
- Google Analytics (UTM tracking)
- Email platform analytics
- Google Sheets (custom dashboards)

**A/B Testing:**
- Built-in platform tools
- Optimizely (advanced)
- Google Optimize (free)

### Dashboard Setup

**Weekly Dashboard (Auto-Generated):**
- Open rate trend (7-day)
- Revenue by email
- Top performing subject lines
- List growth rate

**Monthly Dashboard:**
- Campaign ROI summary
- Audience performance comparison
- A/B test results
- Competitive analysis updates

---

## Quick Reference: Benchmarks

### Industry Benchmarks (2026)

| Metric | B2B | B2C | Education | Fitness |
|--------|-----|-----|-----------|---------|
| Open Rate | 21% | 20% | 25% | 22% |
| Click Rate | 3% | 2.5% | 5% | 3.5% |
| Conversion | 1% | 2% | 2.5% | 2% |
| Unsubscribe | 0.2% | 0.3% | 0.2% | 0.3% |

### Your Goals Should Be:
- Open Rate: 25%+ (above industry)
- Click Rate: 5%+ (above industry)
- Conversion: 2%+ (at or above industry)
- Unsubscribe: <0.5% (healthy)

---

## Action Items by Phase

### Before Campaign
- [ ] Set up UTM parameters
- [ ] Configure tracking pixels
- [ ] Create tracking spreadsheet
- [ ] Define KPI targets

### During Campaign
- [ ] Monitor first hour metrics
- [ ] Check for deliverability issues
- [ ] A/B test variant performance

### After Campaign
- [ ] Compile final metrics
- [ ] Document A/B test results
- [ ] Write lessons learned
- [ ] Update best practices

---

## Data-Driven Optimization Framework

**Weekly:**
1. Review open rates by subject line
2. Identify patterns in top performers
3. Update subject line templates

**Monthly:**
1. Analyze full campaign ROI
2. Compare audience performance
3. Document A/B test learnings
4. Adjust segmentation strategy

**Quarterly:**
1. Review competitive landscape
2. Update customer personas
3. Refresh creative templates
4. Set new benchmark goals

---

*Remember: Data without action is just trivia. Use these insights to continuously improve.*