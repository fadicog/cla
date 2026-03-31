# Report Catalog: UAE PASS Document Sharing Analytics
**Version:** 1.0
**Last Updated:** 2026-01-09
**Purpose:** Complete index of all available reports with descriptions, use cases, and access information

---

## Table of Contents

1. [Executive Reports](#1-executive-reports)
2. [Operational Reports](#2-operational-reports)
3. [Product Management Reports](#3-product-management-reports)
4. [Service Provider Reports](#4-service-provider-reports)
5. [Engineering Reports](#5-engineering-reports)
6. [Ad-Hoc Analysis Queries](#6-ad-hoc-analysis-queries)
7. [Report Access Matrix](#7-report-access-matrix)
8. [Report Delivery Schedule](#8-report-delivery-schedule)

---

## 1. Executive Reports

### 1.1 Executive Dashboard (Real-Time)

**Description:** High-level overview of document sharing performance with key metrics and trends.

**Target Audience:** C-Suite, VPs, Product Directors

**Key Metrics:**
- Overall success rate (current + trend)
- Total request volume (current + YoY/MoM change)
- Terminal status distribution (S40, S41, S42, S43, S44)
- Success rate by channel (notification, QR, redirect)
- Success rate by platform (iOS, Android)
- 7-day moving average trend

**Visualizations:**
- 4 KPI cards (Total Requests, Success Count, Success Rate, Avg Journey Time)
- Line chart: Success rate trend (30 days)
- Pie chart: Terminal status distribution
- Horizontal bar: Channel performance comparison
- Horizontal bar: Platform performance comparison
- Funnel: Universal journey (S00 → S40)

**Refresh Frequency:** Daily at 6:00 AM UAE time

**Filters Available:**
- Date range (Last 7/30/90 days, Custom)
- Channel (All, Notification, QR, Redirect)
- Platform (All, iOS, Android)

**Access:**
- Dashboard URL: `/dashboards/executive-overview`
- Email Delivery: Daily summary to exec-team@uaepass.ae
- Mobile: Yes (responsive design)

**Use Cases:**
- Daily standup review
- Weekly leadership meetings
- Monthly board presentations
- Quarterly business reviews

---

### 1.2 Executive Weekly Summary (Automated Email)

**Description:** Weekly email report summarizing key performance indicators and notable changes.

**Target Audience:** Executives, Department Heads

**Contents:**
- Week-over-week comparison (success rate, volume, errors)
- Top 3 wins (improvements)
- Top 3 concerns (degradations)
- Channel and platform performance
- Top 5 service providers by volume and success rate
- Executive summary (2-3 bullet points)

**Format:** PDF attachment + inline HTML

**Delivery Schedule:** Every Monday at 8:00 AM UAE time

**Access:** Email subscription via admin panel

**Sample Structure:**
```
UAE PASS Document Sharing - Week of Nov 12-18, 2025

KEY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total Requests: 350,802 (+7.2% vs last week)
• Success Rate: 67.4% (+0.8 pp vs last week)
• Avg Journey Time: 2.4 min (-0.3 min vs last week)

TOP WINS
✓ iOS success rate reached 77.8% (+2.1%)
✓ Consent conversion improved to 95.6% (+1.3%)
✓ Error rate dropped to 3.5% (-0.7%)

TOP CONCERNS
⚠ Android success rate gap widened to -10.1 pp
⚠ Document unavailability at 20.6% (no improvement)
⚠ User abort rate still high at 17.8%

[View Full Dashboard →]
```

---

### 1.3 Monthly Business Review Report

**Description:** Comprehensive monthly report for business review meetings with deep analysis and recommendations.

**Target Audience:** Executive Leadership, Product Management, Operations

**Contents:**
- 30-day performance summary
- Month-over-month and year-over-year trends
- Funnel analysis with drop-off identification
- Channel and platform deep dive
- Service provider performance ranking
- Error analysis and root causes
- User behavior insights (consent, PIN, abandonment)
- Recommendations and action items

**Format:** PowerPoint + PDF

**Delivery Schedule:** 1st of each month

**Page Count:** 15-20 slides

**Access:** Shared via SharePoint + email

---

## 2. Operational Reports

### 2.1 Real-Time Monitoring Dashboard

**Description:** Live operational dashboard for monitoring system health and identifying issues immediately.

**Target Audience:** Operations Team, DevOps, Support

**Key Metrics:**
- Requests in last hour (vs. baseline)
- Error rate (last hour, current day)
- Success rate (last hour, current day)
- Top 5 active errors (live)
- Slow requests (>5 min duration)
- Stuck requests (no status change >10 min)
- SP error rate (live)

**Visualizations:**
- Line chart: Hourly request volume (last 24 hours)
- Gauge: Current error rate (with threshold indicators)
- Table: Active errors (sortable by count, last seen)
- Table: Anomalous requests (long duration, multiple errors, stuck)
- Heatmap: SP performance (last 6 hours)

**Refresh Frequency:** Every 1 minute (live connection)

**Alerts:**
- Error rate >5%: Alert operations team (Slack + email)
- Request volume drops >30%: Alert DevOps (PagerDuty)
- Any error count >100/hour: Alert engineering (Slack)
- SP success rate <50%: Alert SP relations team (email)

**Access:**
- Dashboard URL: `/dashboards/ops-monitoring`
- Display: Operations Center TV screens (1920×1080)
- Mobile: Yes (simplified view)

**Use Cases:**
- 24/7 operations monitoring
- Incident detection and triage
- Real-time system health check
- Customer support escalation

---

### 2.2 Daily Operations Report

**Description:** Daily snapshot of operational metrics for ops team daily standup.

**Target Audience:** Operations Team, Support Team

**Contents:**
- Yesterday's summary (vs. baseline)
- Errors breakdown (count, %, top 10)
- Service provider issues (SPs with errors >10%)
- Anomalies detected (unusual patterns)
- Follow-up items from previous day

**Format:** Email (HTML) + Slack channel post

**Delivery Schedule:** Daily at 7:00 AM UAE time

**Access:** Subscription-based (ops-team@uaepass.ae)

---

### 2.3 Hourly Error Alert Report

**Description:** Automated alert when error thresholds are breached.

**Target Audience:** On-Call Engineer, Operations Lead

**Trigger Conditions:**
- Total errors in last hour >500
- Error rate >5%
- Any single error code >100 occurrences
- New error code appears

**Contents:**
- Error summary (count, rate, %)
- Top 5 error codes (with counts)
- Affected service providers
- Sample request IDs for investigation
- Comparison to baseline (is this unusual?)

**Format:** Email + Slack alert

**Delivery:** Real-time (within 5 minutes of threshold breach)

---

## 3. Product Management Reports

### 3.1 Product Performance Dashboard

**Description:** Product-focused metrics for understanding user behavior and feature performance.

**Target Audience:** Product Managers, Product Owners, UX Designers

**Key Metrics:**
- Conversion funnel (S00 → S40)
- Stage-by-stage drop-off analysis
- Consent conversion rate (S20 → S21)
- PIN success rate (S30 → S31)
- Document availability rate (S10 vs S11)
- Document retrieval success (S12 → S13)
- User abandonment patterns (where users quit)
- Average time spent at each stage

**Visualizations:**
- Funnel chart: Universal journey with drop-off %
- Bar chart: Drop-off comparison by channel
- Line chart: Consent conversion trend (30 days)
- Table: Time spent at key stages (Consent, PIN, Doc retrieval)
- Sankey diagram: User journey flows (successful vs failed)

**Refresh Frequency:** Daily at 2:00 AM UAE time

**Filters:**
- Date range
- Channel
- Platform
- Service provider
- Document count (1, 2, 3+)

**Access:**
- Dashboard URL: `/dashboards/product-performance`
- PDF export: Weekly snapshot

**Use Cases:**
- Sprint planning
- Feature prioritization
- UX improvement identification
- A/B test result analysis

---

### 3.2 Funnel Optimization Report

**Description:** Deep dive into conversion funnel to identify optimization opportunities.

**Target Audience:** Product Managers, UX Team, Analytics Team

**Contents:**
- Complete funnel breakdown (all channels)
- Channel-specific funnels (notification, QR, redirect)
- Platform comparison (iOS vs Android funnels)
- Cohort analysis (success rate by creation date)
- Drop-off root cause analysis
- Time-in-stage analysis
- Abandonment point analysis (S43 breakdown)
- Recommendations with impact estimates

**Format:** PowerPoint presentation + interactive dashboard

**Delivery Schedule:** Bi-weekly (every 2 weeks)

**Use Cases:**
- Quarterly planning
- UX redesign prioritization
- Conversion rate optimization (CRO) initiatives
- Platform-specific improvement sprints

---

### 3.3 User Behavior Analysis Report

**Description:** Analysis of user interactions and behavior patterns to inform product decisions.

**Target Audience:** Product Managers, UX Researchers

**Contents:**
- Consent behavior (acceptance rate, time to decision)
- PIN behavior (success rate, retry patterns)
- Document interaction (view, download, share patterns)
- Abandonment analysis (when, why, patterns)
- Segmentation by user type (frequent vs infrequent)
- Time-of-day and day-of-week patterns
- Journey path analysis (most common successful/failed paths)

**Format:** PDF report + data export (CSV)

**Delivery Schedule:** Monthly

---

### 3.4 Feature Impact Analysis (Ad-Hoc)

**Description:** Before/after analysis to measure impact of product changes or new features.

**Target Audience:** Product Managers, Engineering Leads

**Use Cases:**
- Measure success of UX redesign
- Validate A/B test results
- Assess impact of new feature launch
- Evaluate platform-specific changes

**Contents:**
- Baseline metrics (pre-change)
- Post-change metrics
- Statistical significance testing
- Segmented analysis (by channel, platform, SP)
- User feedback correlation
- Recommendations (keep, iterate, rollback)

**Format:** Custom report (PDF/PPT)

**Delivery:** On-demand (requested via product-analytics@uaepass.ae)

---

## 4. Service Provider Reports

### 4.1 SP Performance Dashboard

**Description:** Service Provider-specific performance metrics and benchmarks.

**Target Audience:** Service Provider Relationship Managers, SP Integration Teams

**Key Metrics (Per SP):**
- Total requests (volume)
- Success rate (vs. platform average)
- Terminal status distribution
- Consent conversion rate
- PIN success rate
- Document availability rate
- Error rate and top errors
- Average journey time
- Performance ranking (vs other SPs)

**Visualizations:**
- Scorecard: SP success rate + platform average comparison
- Trend line: Success rate over time (30 days)
- Bar chart: SP vs Platform average (consent, PIN, doc availability)
- Table: Error breakdown (error code, count, %)
- Funnel: SP-specific journey

**Refresh Frequency:** Daily at 3:00 AM UAE time

**Filters:**
- Service Provider (dropdown)
- Date range
- Channel
- Platform

**Access:**
- Dashboard URL: `/dashboards/sp-performance?sp_id={SP_ID}`
- SP Portal: Each SP sees only their own data (RLS enabled)

**Use Cases:**
- SP performance reviews
- Identify integration issues
- Benchmark against peers
- Optimize SP-specific flows

---

### 4.2 SP Weekly Scorecard (Automated Email)

**Description:** Weekly performance report sent to each service provider.

**Target Audience:** Individual Service Providers (sent to SP technical contact)

**Contents:**
- This week's performance summary
- Week-over-week change
- Comparison to platform average
- Top issues (if any)
- Recommendations for improvement
- Support contact information

**Format:** Email (HTML)

**Delivery Schedule:** Every Monday at 9:00 AM UAE time

**Sample:**
```
Botim - Weekly Performance Report
Week of Nov 12-18, 2025

YOUR PERFORMANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Success Rate: 71.7% (Platform Avg: 67.4%) ✓
• Total Requests: 62,891 (+12% vs last week)
• Error Rate: 5.5% (Platform Avg: 3.5%) ⚠

AREAS FOR IMPROVEMENT
• Document availability: 76.2% (Platform: 79.4%)
  → Consider pre-checking document availability
• Android success: 65.3% (iOS: 78.9%)
  → Review Android-specific integration

[View Full Dashboard →]
[Contact Support: sp-support@uaepass.ae]
```

---

### 4.3 SP Onboarding Success Report

**Description:** Track performance of newly onboarded service providers during trial period.

**Target Audience:** SP Relationship Managers, Integration Team

**Contents:**
- Days since go-live
- Request volume trend (daily)
- Success rate trend (daily)
- Error rate and common errors
- Integration health checklist
- Red flags (if any)
- Recommendations for stabilization

**Format:** Email report + dashboard

**Delivery:** Daily for first 30 days after SP go-live

---

### 4.4 SP Benchmark Report (Quarterly)

**Description:** Comprehensive comparison of all service providers for internal review.

**Target Audience:** VP Product, SP Relationship Team, TDRA

**Contents:**
- SP ranking by success rate
- SP ranking by volume
- Volume vs performance scatter plot
- Top performers (success rate >75%, volume >10K)
- Underperformers (success rate <60%)
- SP-specific issues summary
- Best practices from top performers
- Recommendations for struggling SPs

**Format:** PDF report + Excel data export

**Delivery Schedule:** Quarterly (end of Q1, Q2, Q3, Q4)

---

## 5. Engineering Reports

### 5.1 Error Analysis Dashboard

**Description:** Deep dive into technical errors for engineering investigation and resolution.

**Target Audience:** Backend Engineers, DevOps, QA

**Key Metrics:**
- Total errors (count, rate, %)
- Error distribution by error_code
- Error distribution by error_source (issuer, network, dv, user)
- Error impact (% leading to S41 vs recovered to S40)
- Error trend over time
- Error rate by SP
- Error rate by platform
- Error correlation with time-of-day

**Visualizations:**
- Table: Top 20 errors (sortable by count, impact, recovery rate)
- Pie chart: Error source distribution
- Heatmap: Error code × Error source matrix
- Line chart: Error rate trend (7 days, hourly granularity)
- Bar chart: SP error rate ranking
- Table: Sample request IDs for each error (for debugging)

**Refresh Frequency:** Every 15 minutes

**Filters:**
- Date range (Last hour, 24 hours, 7 days, Custom)
- Error source
- Error code
- Service provider
- Platform

**Access:**
- Dashboard URL: `/dashboards/error-analysis`
- Slack integration: Auto-post to #engineering-alerts when error spike detected

**Use Cases:**
- Bug investigation
- Root cause analysis
- Error triage and prioritization
- SLA monitoring (issuer errors)
- Capacity planning (server errors)

---

### 5.2 Performance & Latency Dashboard

**Description:** Analysis of system performance and latency bottlenecks.

**Target Audience:** Backend Engineers, Performance Engineers

**Key Metrics:**
- Average journey time (overall, by channel, by platform)
- Step-by-step latency (S00→S01, S01→S03, etc.)
- P50, P90, P95, P99 latency percentiles
- Slow requests (>5 min)
- Very slow requests (>10 min)
- Timeout incidents (S42 breakdown)
- Latency by time-of-day (identify peak hours)

**Visualizations:**
- Box plot: Journey time distribution by channel
- Heatmap: Step latency matrix (previous_status × status_code)
- Line chart: P90 latency trend (7 days)
- Bar chart: Top 10 slowest steps (by average latency)
- Table: Slow request detail (request_id, duration, current status)

**Refresh Frequency:** Hourly

**Access:**
- Dashboard URL: `/dashboards/performance-latency`

**Use Cases:**
- Performance optimization
- Timeout threshold tuning
- Capacity planning
- Identify slow third-party integrations (issuer latency)

---

### 5.3 Data Quality Dashboard

**Description:** Monitor data quality issues and anomalies in the sharing_transactions table.

**Target Audience:** Data Engineers, QA Engineers

**Key Metrics:**
- Null value counts (by column)
- Unexpected value counts (e.g., status_code not in expected set)
- Duplicate request IDs
- Orphaned status events (no S00)
- Requests with missing terminal status
- Data freshness (max status_ts vs current time)
- Row count trend (detect data pipeline issues)

**Visualizations:**
- Table: Column null % (flag if >5%)
- Line chart: Row count by hour (detect gaps)
- Table: Anomalous requests (for investigation)

**Refresh Frequency:** Hourly

**Alerts:**
- Data freshness lag >2 hours
- Row count drops >50% hour-over-hour
- Null values >10% for critical columns

---

### 5.4 Weekly Engineering Summary

**Description:** Weekly summary of technical issues and resolutions for engineering team.

**Target Audience:** Engineering Team, Engineering Managers

**Contents:**
- Error summary (total, top 5, impact)
- New errors introduced this week
- Errors resolved this week
- Performance summary (latency trends)
- Data quality issues (if any)
- Production incidents (count, MTTR)
- Action items for next week

**Format:** Email + Confluence page

**Delivery Schedule:** Every Friday at 4:00 PM UAE time

---

## 6. Ad-Hoc Analysis Queries

### 6.1 Custom Date Range Analysis

**Description:** Generate performance report for any custom date range.

**Input Parameters:**
- Start date
- End date
- Comparison period (optional)
- Filters (channel, platform, SP)

**Output:** Full metrics suite for specified period

**Access:** Self-service query builder (`/reports/custom-analysis`)

---

### 6.2 Cohort Analysis

**Description:** Track performance of request cohorts over time.

**Use Cases:**
- Measure retention of requests created on specific date
- Identify if issues are isolated to specific time periods
- Validate fix effectiveness (compare pre/post cohorts)

**Output:** Cohort table (rows = creation date, columns = days since creation, values = success rate)

---

### 6.3 Correlation Analysis

**Description:** Identify correlations between variables.

**Examples:**
- Does required_doc_count correlate with success rate?
- Does app_version correlate with error rate?
- Does time-of-day correlate with journey time?

**Output:** Correlation matrix + scatter plots

---

### 6.4 Anomaly Detection

**Description:** Identify statistically unusual patterns.

**Detection Rules:**
- Requests with >20 status events
- Requests with duration >30 minutes
- Requests with >3 errors
- Requests with unexpected status sequences

**Output:** Flagged request IDs for investigation

---

### 6.5 Deep Dive: Single Request Journey

**Description:** Complete timeline and details for a specific request_id.

**Input:** request_id

**Output:**
- Full status sequence with timestamps
- Latency at each step
- Errors encountered (if any)
- Final outcome
- Comparison to average journey
- Visual timeline

**Access:** Search box on any dashboard → Enter request_id → View detail

---

## 7. Report Access Matrix

| Report | Executive | Product | Operations | Engineering | SPs | Public |
|--------|-----------|---------|------------|-------------|-----|--------|
| Executive Dashboard | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Executive Weekly Summary | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Monthly Business Review | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Real-Time Monitoring | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Daily Operations Report | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| Product Performance | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Funnel Optimization | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| User Behavior Analysis | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| SP Performance Dashboard | ✓ | ✓ | ✓ | ✗ | ✓* | ✗ |
| SP Weekly Scorecard | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| SP Benchmark Report | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Error Analysis Dashboard | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Performance Dashboard | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| Data Quality Dashboard | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |

**Notes:**
- ✓ = Full access
- ✓* = Row-Level Security (RLS) - SPs see only their own data
- ✗ = No access

---

## 8. Report Delivery Schedule

### Daily Reports

| Report | Time (UAE) | Recipients | Format |
|--------|-----------|------------|--------|
| Daily Operations Report | 7:00 AM | ops-team@uaepass.ae | Email (HTML) |
| SP Onboarding Report (new SPs only) | 8:00 AM | sp-integration@uaepass.ae | Email + Dashboard |

### Weekly Reports

| Report | Day | Time (UAE) | Recipients | Format |
|--------|-----|-----------|------------|--------|
| Executive Weekly Summary | Monday | 8:00 AM | exec-team@uaepass.ae | Email (PDF) |
| SP Weekly Scorecard | Monday | 9:00 AM | Each SP contact | Email (HTML) |
| Engineering Summary | Friday | 4:00 PM | engineering@uaepass.ae | Email + Confluence |
| Funnel Optimization Report | Every 2 weeks | Tuesday 10:00 AM | product-team@uaepass.ae | Email + PPT |

### Monthly Reports

| Report | Day | Time (UAE) | Recipients | Format |
|--------|-----|-----------|------------|--------|
| Monthly Business Review | 1st of month | 9:00 AM | leadership@uaepass.ae | Email (PPT + PDF) |
| User Behavior Analysis | 5th of month | 10:00 AM | product-team@uaepass.ae | Email (PDF + CSV) |

### Quarterly Reports

| Report | Timing | Recipients | Format |
|--------|--------|------------|--------|
| SP Benchmark Report | End of quarter | exec-team@uaepass.ae, TDRA | Email (PDF + Excel) |

### Real-Time Alerts

| Alert | Trigger | Recipients | Channel |
|-------|---------|------------|---------|
| High Error Rate | Error rate >5% | ops-oncall@uaepass.ae | Email + Slack |
| Volume Drop | Requests drop >30% hour-over-hour | devops-oncall@uaepass.ae | PagerDuty |
| Error Spike | Any error >100/hour | engineering-alerts (Slack) | Slack |
| SP Critical Issue | SP success rate <50% | sp-relations@uaepass.ae | Email |
| Data Freshness Lag | Data lag >2 hours | data-eng@uaepass.ae | Email + Slack |

---

## Report Request Process

### Standard Reports
Access via dashboard portal: `https://analytics.uaepass.ae/dashboards`

### Custom/Ad-Hoc Reports
1. Submit request via Jira: Project "Analytics Requests"
2. Provide:
   - Business question
   - Date range
   - Required filters/segments
   - Deadline
3. SLA: 3 business days for standard queries, 10 days for complex analysis

### Emergency Reports
- Contact: analytics-support@uaepass.ae
- Response time: 2 hours during business hours

---

## Report Feedback

**Submit feedback or request new reports:**
- Email: product-analytics@uaepass.ae
- Slack: #analytics-feedback
- Quarterly survey: Share your analytics needs

---

**End of Report Catalog**
**Total Reports: 25+ Standard Reports + Ad-Hoc Capability**
**Comprehensive Coverage for All Stakeholders**
