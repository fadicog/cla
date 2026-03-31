# Report Implementation Guide: UAE PASS Document Sharing Analytics
**Version:** 1.0
**Last Updated:** 2026-01-09
**Target Audience:** Backend Engineers, Data Engineers, BI/Analytics Team, Operations

---

## Table of Contents

1. [Data Source & Schema](#1-data-source--schema)
2. [Overall Performance Metrics](#2-overall-performance-metrics)
3. [Channel Performance Reports](#3-channel-performance-reports)
4. [Status Flow & Funnel Reports](#4-status-flow--funnel-reports)
5. [Error Analysis Reports](#5-error-analysis-reports)
6. [Service Provider Performance Reports](#6-service-provider-performance-reports)
7. [User Behavior Reports](#7-user-behavior-reports)
8. [Document Readiness Reports](#8-document-readiness-reports)
9. [Time & Latency Reports](#9-time--latency-reports)
10. [Platform Comparison Reports](#10-platform-comparison-reports)
11. [Advanced SP-Specific Reports](#11-advanced-sp-specific-reports)
12. [Implementation Best Practices](#12-implementation-best-practices)

---

## 1. Data Source & Schema

### 1.1 Primary Table: sharing_transactions

**Table Structure:**
```sql
CREATE TABLE sharing_transactions (
    request_id VARCHAR(20),          -- Unique request identifier (REQ000001)
    sp_id VARCHAR(100),              -- Service Provider name
    channel VARCHAR(20),             -- notification | qr | redirect
    platform VARCHAR(20),            -- android | ios
    app_version VARCHAR(20),         -- Application version (e.g., "6.4.0")
    required_docs TEXT,              -- JSON array: ["Emirates ID Card", "Passport"]
    required_count INTEGER,          -- Number of required documents
    status_code VARCHAR(10),         -- S00-S44 (journey status codes)
    previous_status VARCHAR(10),     -- Previous status in the journey
    status_ts TIMESTAMP,             -- Timestamp: "2025-11-01 12:34:56"
    step_latency_ms INTEGER,         -- Milliseconds since previous status
    missing_count INTEGER,           -- Count of missing documents
    error_code VARCHAR(50),          -- Error identifier (issuer_timeout, pin_incorrect, etc.)
    error_source VARCHAR(20),        -- issuer | network | dv | user_cancel
    status_history TEXT,             -- JSON array: ["S00", "S01", ..., "S40"]
    PRIMARY KEY (request_id, status_code, status_ts)
);
```

### 1.2 Status Code Reference

**Terminal Statuses:**
- `S40`: Success (documents shared)
- `S41`: Technical Error
- `S42`: Expired
- `S43`: User Aborted
- `S44`: Not Eligible

**Journey Statuses:**
- `S00`: Request Created
- `S01-S03`: Notification flow (sent, delivered, opened)
- `S04-S05`: Redirect flow
- `S06-S07`: QR flow (scanned, verified)
- `S08`: Request Viewed
- `S10`: Documents Ready (all available)
- `S11`: Documents Missing (some unavailable)
- `S12-S15`: Missing document retrieval flow
- `S20`: Awaiting Consent
- `S21`: Consent Given
- `S30`: PIN Requested
- `S31`: PIN Verified
- `S32`: PIN Failed

### 1.3 Key Data Points

**Understanding Request-Level vs Event-Level:**
- Each row is a **status event** (one request can have 5-15 events)
- A **request** is identified by unique `request_id`
- A **terminal request** has reached S40, S41, S42, S43, or S44
- The **final status** is the last terminal status for each request_id

---

## 2. Overall Performance Metrics

### 2.1 Report: Overall Success Rate

#### Business Purpose
Measures the percentage of all sharing requests that successfully complete (S40). This is the primary KPI for system performance and user satisfaction.

#### Data Source
Table: `sharing_transactions`
Join: None (single table query)

#### Calculation Logic

**SQL Implementation:**
```sql
-- Overall Success Rate
WITH terminal_requests AS (
    SELECT
        request_id,
        status_code,
        status_ts,
        ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
    FROM sharing_transactions
    WHERE status_code IN ('S40', 'S41', 'S42', 'S43', 'S44')
),
final_statuses AS (
    SELECT request_id, status_code
    FROM terminal_requests
    WHERE rn = 1
)
SELECT
    COUNT(*) as total_requests,
    SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as successful_shares,
    ROUND(100.0 * SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate_pct
FROM final_statuses;
```

**Step-by-Step Algorithm:**
1. Identify all requests that have reached a terminal status (S40-S44)
2. For each request_id, take the LAST terminal status (highest timestamp)
3. Count total unique requests
4. Count requests where final status = S40
5. Calculate: (S40 count / Total requests) × 100

**Formula:**
```
Success Rate = (Number of S40 requests / Total unique requests) × 100
```

#### Example Calculation

**Sample Data:**
```
Request ID | Final Status
REQ001     | S40
REQ002     | S40
REQ003     | S43
REQ004     | S40
REQ005     | S41
```

**Calculation:**
- Total Requests: 5
- Successful (S40): 3
- Success Rate: (3 / 5) × 100 = **60.0%**

#### Filters & Segmentation

```sql
-- By Date Range
WHERE status_ts BETWEEN '2025-11-01' AND '2025-11-30'

-- By Channel
WHERE channel = 'notification'

-- By Platform
WHERE platform = 'ios'

-- By Service Provider
WHERE sp_id = 'Botim'

-- By App Version
WHERE app_version >= '6.0.0'

-- Combined Example
WHERE status_ts >= CURRENT_DATE - INTERVAL '7 days'
  AND channel = 'notification'
  AND platform = 'android'
```

#### Visualization Recommendation
- **Chart Type:** Large number tile + trend line
- **Primary Display:** 67.4% (current value)
- **Trend:** 7-day moving average line chart
- **Comparison:** Target line at 75%

#### Key Thresholds & Benchmarks
- **Target:** 75%+
- **Good:** 65-75%
- **Needs Attention:** <65%
- **Current Baseline:** 67.4%

#### Implementation Notes
- **Performance:** Index on `status_code` and `status_ts` for fast filtering
- **Edge Cases:**
  - Handle requests with no terminal status (exclude from denominator)
  - Requests with multiple terminal statuses (take latest by timestamp)
  - Null status_code values (exclude)
- **Refresh Frequency:** Real-time (1-minute updates) for operational dashboards
- **Aggregation:** Pre-aggregate by hour for historical trend analysis

#### Sample Output

```
Metric                    | Value
--------------------------|-------
Total Requests            | 350,802
Successful Shares (S40)   | 236,426
Success Rate              | 67.40%
Failed (S41)              | 12,133
Expired (S42)             | 25,689
User Aborted (S43)        | 62,515
Not Eligible (S44)        | 14,039
```

---

### 2.2 Report: Conversion Rate (Overall)

#### Business Purpose
Measures the percentage of all requests (including those still in progress) that result in successful sharing. More conservative than success rate because it includes incomplete journeys.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Conversion Rate (All Requests)
WITH all_requests AS (
    SELECT DISTINCT request_id
    FROM sharing_transactions
),
successful_requests AS (
    SELECT DISTINCT request_id
    FROM sharing_transactions
    WHERE status_code = 'S40'
)
SELECT
    (SELECT COUNT(*) FROM all_requests) as total_requests,
    (SELECT COUNT(*) FROM successful_requests) as successful_shares,
    ROUND(100.0 * (SELECT COUNT(*) FROM successful_requests) /
          (SELECT COUNT(*) FROM all_requests), 2) as conversion_rate_pct
;
```

**Step-by-Step Algorithm:**
1. Count all unique request_ids (regardless of status)
2. Count unique request_ids that have at least one S40 status
3. Calculate: (S40 requests / All requests) × 100

**Formula:**
```
Conversion Rate = (Requests with S40 status / All unique requests) × 100
```

#### Example Calculation

**Sample Data:**
```
Request ID | Statuses
REQ001     | S00, S01, S08, S20, S21, S30, S31, S40
REQ002     | S00, S01, S08
REQ003     | S00, S01, S08, S20, S43
```

**Calculation:**
- Total Requests: 3
- Completed with S40: 1
- Conversion Rate: (1 / 3) × 100 = **33.33%**

#### Filters & Segmentation
Same as Section 2.1 (Overall Success Rate)

#### Visualization Recommendation
- **Chart Type:** Gauge chart with target indicator
- **Range:** 0-100%
- **Zones:** Red (<60%), Yellow (60-70%), Green (70%+)

#### Key Thresholds & Benchmarks
- **Target:** 70%+
- **Good:** 60-70%
- **Needs Attention:** <60%
- **Current Baseline:** 67.4%

#### Implementation Notes
- **Difference from Success Rate:** Conversion includes in-progress requests; Success Rate only includes terminal statuses
- **Use Case:** Conversion Rate is better for real-time monitoring; Success Rate is better for completed journey analysis
- **Performance:** Simple DISTINCT count, very fast
- **Refresh Frequency:** Every 5 minutes for near-real-time tracking

#### Sample Output

```
Metric                    | Value
--------------------------|-------
Total Requests            | 350,802
Successful Shares         | 236,426
Conversion Rate           | 67.40%
In Progress (No Terminal) | 0
```

---

### 2.3 Report: Terminal Status Distribution

#### Business Purpose
Shows the breakdown of all completed requests by final outcome. Helps identify primary failure modes and success patterns.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Terminal Status Distribution
WITH terminal_requests AS (
    SELECT
        request_id,
        status_code,
        status_ts,
        ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
    FROM sharing_transactions
    WHERE status_code IN ('S40', 'S41', 'S42', 'S43', 'S44')
),
final_statuses AS (
    SELECT request_id, status_code
    FROM terminal_requests
    WHERE rn = 1
)
SELECT
    status_code,
    CASE
        WHEN status_code = 'S40' THEN 'Success (Shared)'
        WHEN status_code = 'S41' THEN 'Technical Error'
        WHEN status_code = 'S42' THEN 'Expired'
        WHEN status_code = 'S43' THEN 'User Aborted'
        WHEN status_code = 'S44' THEN 'Not Eligible'
    END as status_description,
    COUNT(*) as request_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage
FROM final_statuses
GROUP BY status_code
ORDER BY request_count DESC;
```

**Step-by-Step Algorithm:**
1. Filter to terminal statuses (S40-S44)
2. For each request, get the final (latest) terminal status
3. Group by status_code
4. Count requests in each status
5. Calculate percentage of each status

**Formula:**
```
Status Percentage = (Requests in Status X / Total Terminal Requests) × 100
```

#### Example Calculation

**Sample Data:**
```
Request ID | Final Status
REQ001     | S40
REQ002     | S40
REQ003     | S40
REQ004     | S43
REQ005     | S41
```

**Calculation:**
```
S40: 3 requests → (3/5) × 100 = 60%
S43: 1 request  → (1/5) × 100 = 20%
S41: 1 request  → (1/5) × 100 = 20%
```

#### Filters & Segmentation
Apply filters before the terminal_requests CTE:
- Date range: `WHERE status_ts BETWEEN ...`
- Channel/Platform/SP: `WHERE channel = '...' AND platform = '...'`

#### Visualization Recommendation
- **Chart Type:** Pie chart or horizontal bar chart
- **Colors:**
  - S40 (Success): Green
  - S41 (Technical Error): Red
  - S42 (Expired): Orange
  - S43 (User Aborted): Yellow
  - S44 (Not Eligible): Gray

#### Key Thresholds & Benchmarks
- **Healthy Distribution:**
  - S40: >70%
  - S41: <5%
  - S42: <10%
  - S43: <10%
  - S44: <10%

#### Implementation Notes
- **Use Case:** Identify if failures are technical (S41) or user-driven (S43)
- **Actionability:**
  - High S41: Infrastructure issues
  - High S43: UX/engagement issues
  - High S44: SP requesting wrong documents
  - High S42: Timeout/expiry issues
- **Performance:** Fast with proper indexes on status_code and status_ts

#### Sample Output

```
Status Code | Description        | Count   | Percentage
------------|-------------------|---------|------------
S40         | Success (Shared)  | 236,426 | 67.40%
S43         | User Aborted      | 62,515  | 17.82%
S42         | Expired           | 25,689  | 7.32%
S44         | Not Eligible      | 14,039  | 4.00%
S41         | Technical Error   | 12,133  | 3.46%
```

---

### 2.4 Report: Request Volume Trends

#### Business Purpose
Tracks request volume over time to identify growth trends, peak usage periods, and anomalies.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Daily Request Volume
WITH first_events AS (
    SELECT
        request_id,
        MIN(status_ts) as created_ts
    FROM sharing_transactions
    GROUP BY request_id
)
SELECT
    DATE(created_ts) as request_date,
    COUNT(*) as total_requests,
    COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY DATE(created_ts)) as day_over_day_change,
    ROUND(100.0 * (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY DATE(created_ts))) /
          LAG(COUNT(*)) OVER (ORDER BY DATE(created_ts)), 2) as pct_change
FROM first_events
WHERE created_ts >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(created_ts)
ORDER BY request_date;
```

**Hourly Breakdown (for operational monitoring):**
```sql
-- Hourly Request Volume
WITH first_events AS (
    SELECT
        request_id,
        MIN(status_ts) as created_ts
    FROM sharing_transactions
    GROUP BY request_id
)
SELECT
    DATE_TRUNC('hour', created_ts) as request_hour,
    COUNT(*) as total_requests,
    ROUND(AVG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('hour', created_ts)
          ROWS BETWEEN 23 PRECEDING AND CURRENT ROW), 2) as moving_avg_24h
FROM first_events
WHERE created_ts >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE_TRUNC('hour', created_ts)
ORDER BY request_hour;
```

**Step-by-Step Algorithm:**
1. For each request, find the first status event (S00 or earliest timestamp)
2. Extract the date/hour from the timestamp
3. Group by date/hour and count requests
4. Calculate day-over-day or hour-over-hour change
5. Calculate moving average for trend smoothing

**Formula:**
```
Day-over-Day Change % = ((Today's Volume - Yesterday's Volume) / Yesterday's Volume) × 100
Moving Average (7-day) = SUM(Volume for last 7 days) / 7
```

#### Example Calculation

**Sample Data:**
```
Date       | Request Count
2025-11-01 | 48,500
2025-11-02 | 52,300
2025-11-03 | 49,800
```

**Calculation:**
```
Nov 2 Change: (52,300 - 48,500) / 48,500 × 100 = +7.84%
Nov 3 Change: (49,800 - 52,300) / 52,300 × 100 = -4.78%
3-Day Avg: (48,500 + 52,300 + 49,800) / 3 = 50,200
```

#### Filters & Segmentation
```sql
-- By Channel
WHERE channel = 'notification'

-- By Platform
WHERE platform IN ('ios', 'android')

-- By Service Provider
WHERE sp_id = 'Botim'

-- Weekday vs Weekend
SELECT
    CASE WHEN EXTRACT(DOW FROM created_ts) IN (0,6)
         THEN 'Weekend' ELSE 'Weekday' END as day_type,
    COUNT(*) as requests
FROM first_events
GROUP BY day_type;
```

#### Visualization Recommendation
- **Chart Type:** Line chart (time series)
- **Multiple Lines:**
  - Daily volume (solid line)
  - 7-day moving average (dashed line)
  - Target volume (horizontal line)
- **X-Axis:** Date
- **Y-Axis:** Request count
- **Annotations:** Mark significant events (releases, campaigns)

#### Key Thresholds & Benchmarks
- **Baseline:** 50,000 requests/day (establish from historical data)
- **Alert Triggers:**
  - Volume drops >20% day-over-day
  - Volume spikes >50% day-over-day (capacity alert)
  - No requests for 1+ hour during business hours

#### Implementation Notes
- **Performance:** Pre-aggregate to daily/hourly granularity
- **Storage:** Keep raw data for 90 days, aggregated data for 2+ years
- **Refresh Frequency:**
  - Real-time dashboard: Every 5 minutes
  - Executive dashboard: Daily at midnight
- **Edge Cases:**
  - Handle timezone conversion (display in UAE time)
  - Account for daylight saving time changes
  - Mark partial days (e.g., "Today so far")

#### Sample Output

**Daily Trend:**
```
Date       | Requests | Change vs Prior Day | 7-Day Moving Avg
-----------|----------|---------------------|------------------
2025-11-12 | 48,234   | -                   | -
2025-11-13 | 52,108   | +8.03%              | -
2025-11-14 | 49,876   | -4.28%              | -
2025-11-15 | 51,234   | +2.72%              | 50,363
2025-11-16 | 50,891   | -0.67%              | 50,469
2025-11-17 | 49,123   | -3.47%              | 50,244
2025-11-18 | 48,667   | -0.93%              | 50,019
```

---

## 3. Channel Performance Reports

### 3.1 Report: Success Rate by Channel

#### Business Purpose
Compares success rates across different channels (notification, QR, redirect) to identify which channel performs best and optimize user flows.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Success Rate by Channel
WITH terminal_requests AS (
    SELECT
        request_id,
        channel,
        status_code,
        status_ts,
        ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
    FROM sharing_transactions
    WHERE status_code IN ('S40', 'S41', 'S42', 'S43', 'S44')
),
final_statuses AS (
    SELECT request_id, channel, status_code
    FROM terminal_requests
    WHERE rn = 1
)
SELECT
    channel,
    COUNT(*) as total_requests,
    SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as successful_shares,
    ROUND(100.0 * SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate_pct,
    SUM(CASE WHEN status_code = 'S41' THEN 1 ELSE 0 END) as technical_failures,
    SUM(CASE WHEN status_code = 'S43' THEN 1 ELSE 0 END) as user_aborted,
    ROUND(100.0 * SUM(CASE WHEN status_code = 'S43' THEN 1 ELSE 0 END) / COUNT(*), 2) as abort_rate_pct
FROM final_statuses
GROUP BY channel
ORDER BY success_rate_pct DESC;
```

**Step-by-Step Algorithm:**
1. Get final terminal status for each request
2. Group by channel
3. Calculate success rate for each channel
4. Calculate failure rates by type
5. Sort by success rate descending

**Formula:**
```
Channel Success Rate = (S40 count for channel / Total requests for channel) × 100
Channel Abort Rate = (S43 count for channel / Total requests for channel) × 100
```

#### Example Calculation

**Sample Data:**
```
Request ID | Channel      | Final Status
REQ001     | notification | S40
REQ002     | notification | S40
REQ003     | qr           | S40
REQ004     | qr           | S43
REQ005     | redirect     | S41
```

**Calculation:**
```
Notification: 2 requests, 2 S40 → 100% success
QR:           2 requests, 1 S40 → 50% success
Redirect:     1 request,  0 S40 → 0% success
```

#### Filters & Segmentation
```sql
-- By Date Range
WHERE status_ts >= '2025-11-01'

-- By Platform
WHERE platform = 'ios'

-- By Service Provider
WHERE sp_id IN ('Botim', 'Lulu')

-- Exclude low-volume channels
HAVING COUNT(*) >= 100
```

#### Visualization Recommendation
- **Chart Type:** Grouped bar chart
- **Bars per Channel:**
  - Success Rate (green)
  - Abort Rate (yellow)
  - Technical Failure Rate (red)
- **Sort:** By success rate descending
- **Data Labels:** Show percentages on bars

#### Key Thresholds & Benchmarks
- **Expected Performance:**
  - Notification: 70-75% (highest, user-initiated)
  - QR: 65-70% (in-person, good)
  - Redirect: 60-65% (lowest, web-based)
- **Alert If:**
  - Any channel drops >5% from baseline
  - Notification < 65%
  - QR < 60%

#### Implementation Notes
- **Channel Definitions:**
  - `notification`: Push notification flow (S01-S03)
  - `qr`: QR code scan flow (S06-S07)
  - `redirect`: Web redirect flow (S04-S05)
- **Edge Cases:**
  - Requests that switch channels mid-journey (rare, use first channel)
  - Null channel values (categorize as "Unknown")
- **Performance:** Index on `channel` for fast filtering
- **Refresh Frequency:** Hourly for operations, daily for executive

#### Sample Output

```
Channel      | Total Requests | Successful | Success Rate | Aborted | Abort Rate | Tech Failures
-------------|----------------|------------|--------------|---------|------------|---------------
notification | 245,678        | 178,234    | 72.5%        | 42,156  | 17.2%      | 8,234
qr           | 89,456         | 52,891     | 59.1%        | 18,567  | 20.8%      | 3,456
redirect     | 15,668         | 5,301      | 33.8%        | 1,792   | 11.4%      | 443
```

---

### 3.2 Report: Channel-Specific Journey Funnel

#### Business Purpose
Shows the step-by-step journey for each channel to identify where users drop off in channel-specific flows.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Notification Channel Funnel
WITH request_statuses AS (
    SELECT
        request_id,
        MAX(CASE WHEN status_code = 'S00' THEN 1 ELSE 0 END) as reached_s00,
        MAX(CASE WHEN status_code = 'S01' THEN 1 ELSE 0 END) as reached_s01,
        MAX(CASE WHEN status_code = 'S02' THEN 1 ELSE 0 END) as reached_s02,
        MAX(CASE WHEN status_code = 'S03' THEN 1 ELSE 0 END) as reached_s03,
        MAX(CASE WHEN status_code = 'S08' THEN 1 ELSE 0 END) as reached_s08,
        MAX(CASE WHEN status_code = 'S20' THEN 1 ELSE 0 END) as reached_s20,
        MAX(CASE WHEN status_code = 'S21' THEN 1 ELSE 0 END) as reached_s21,
        MAX(CASE WHEN status_code = 'S30' THEN 1 ELSE 0 END) as reached_s30,
        MAX(CASE WHEN status_code = 'S31' THEN 1 ELSE 0 END) as reached_s31,
        MAX(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as reached_s40
    FROM sharing_transactions
    WHERE channel = 'notification'
    GROUP BY request_id
)
SELECT
    'S00 - Request Created' as funnel_step,
    SUM(reached_s00) as requests,
    100.0 as pct_of_s00,
    0 as drop_off
FROM request_statuses
UNION ALL
SELECT
    'S01 - Notification Sent',
    SUM(reached_s01),
    ROUND(100.0 * SUM(reached_s01) / NULLIF(SUM(reached_s00), 0), 2),
    SUM(reached_s00) - SUM(reached_s01)
FROM request_statuses
UNION ALL
SELECT
    'S03 - Notification Opened',
    SUM(reached_s03),
    ROUND(100.0 * SUM(reached_s03) / NULLIF(SUM(reached_s00), 0), 2),
    SUM(reached_s01) - SUM(reached_s03)
FROM request_statuses
UNION ALL
SELECT
    'S08 - Request Viewed',
    SUM(reached_s08),
    ROUND(100.0 * SUM(reached_s08) / NULLIF(SUM(reached_s00), 0), 2),
    SUM(reached_s03) - SUM(reached_s08)
FROM request_statuses
UNION ALL
SELECT
    'S20 - Consent Screen',
    SUM(reached_s20),
    ROUND(100.0 * SUM(reached_s20) / NULLIF(SUM(reached_s00), 0), 2),
    SUM(reached_s08) - SUM(reached_s20)
FROM request_statuses
UNION ALL
SELECT
    'S21 - Consent Given',
    SUM(reached_s21),
    ROUND(100.0 * SUM(reached_s21) / NULLIF(SUM(reached_s00), 0), 2),
    SUM(reached_s20) - SUM(reached_s21)
FROM request_statuses
UNION ALL
SELECT
    'S30 - PIN Screen',
    SUM(reached_s30),
    ROUND(100.0 * SUM(reached_s30) / NULLIF(SUM(reached_s00), 0), 2),
    SUM(reached_s21) - SUM(reached_s30)
FROM request_statuses
UNION ALL
SELECT
    'S31 - PIN Verified',
    SUM(reached_s31),
    ROUND(100.0 * SUM(reached_s31) / NULLIF(SUM(reached_s00), 0), 2),
    SUM(reached_s30) - SUM(reached_s31)
FROM request_statuses
UNION ALL
SELECT
    'S40 - Successfully Shared',
    SUM(reached_s40),
    ROUND(100.0 * SUM(reached_s40) / NULLIF(SUM(reached_s00), 0), 2),
    SUM(reached_s31) - SUM(reached_s40)
FROM request_statuses
ORDER BY requests DESC;
```

**For QR Channel (S06-S07):**
```sql
-- Replace S01-S03 with S06-S07 in the above query
-- S06: QR Scanned
-- S07: QR Verified
-- Then continues to S08...
```

**Step-by-Step Algorithm:**
1. For each request, create binary flags for each status reached
2. Sum flags across all requests to get counts
3. Calculate percentage of S00 (starting point)
4. Calculate drop-off between consecutive steps
5. Present as funnel visualization

**Formula:**
```
Step Retention = (Requests reaching Step N / Requests reaching Step 0) × 100
Step Drop-off = Requests at Step N-1 - Requests at Step N
Drop-off Rate = (Drop-off / Requests at Step N-1) × 100
```

#### Example Calculation

**Sample Data:**
```
Request ID | Reached Statuses
REQ001     | S00, S01, S03, S08, S20, S21, S30, S31, S40
REQ002     | S00, S01, S03, S08, S20
REQ003     | S00, S01, S03, S08, S20, S21, S30, S31, S40
```

**Calculation:**
```
S00 (Created):       3 requests (100%)
S01 (Sent):          3 requests (100%) - Drop: 0
S03 (Opened):        3 requests (100%) - Drop: 0
S08 (Viewed):        3 requests (100%) - Drop: 0
S20 (Consent):       3 requests (100%) - Drop: 0
S21 (Gave Consent):  2 requests (67%)  - Drop: 1 (33% drop-off)
S30 (PIN):           2 requests (67%)  - Drop: 0
S31 (PIN Verified):  2 requests (67%)  - Drop: 0
S40 (Success):       2 requests (67%)  - Drop: 0
```

#### Filters & Segmentation
```sql
-- By Platform
WHERE platform = 'android'

-- By Date Range
WHERE status_ts BETWEEN '2025-11-01' AND '2025-11-30'

-- By Service Provider
WHERE sp_id = 'Botim'
```

#### Visualization Recommendation
- **Chart Type:** Funnel chart (trapezoid shapes stacked vertically)
- **Width:** Proportional to request count
- **Labels:** Show count and percentage
- **Highlight:** Largest drop-off steps in red
- **Interactive:** Click to drill down into specific step

#### Key Thresholds & Benchmarks
- **Critical Drop-off Points to Monitor:**
  - S01→S03 (notification not opened): Should be <15% drop
  - S20→S21 (consent not given): Should be <20% drop
  - S30→S31 (PIN failed): Should be <10% drop
- **Alert If:**
  - Any single step has >30% drop-off
  - Total funnel conversion <60%

#### Implementation Notes
- **Channel-Specific Statuses:**
  - Notification: S01-S03
  - QR: S06-S07
  - Redirect: S04-S05
  - All channels converge at S08
- **Edge Cases:**
  - Users who skip steps (e.g., go from S00 to S08 directly) - count in both
  - Multiple passes through same status - count as reached
- **Performance:** Pre-calculate funnel daily, cache results
- **Refresh Frequency:** Daily for trends, hourly for monitoring

#### Sample Output

```
Funnel Step               | Requests | % of Start | Drop-off | Drop-off %
--------------------------|----------|------------|----------|------------
S00 - Request Created     | 100,000  | 100.0%     | -        | -
S01 - Notification Sent   | 99,500   | 99.5%      | 500      | 0.5%
S03 - Notification Opened | 88,000   | 88.0%      | 11,500   | 11.6%
S08 - Request Viewed      | 87,000   | 87.0%      | 1,000    | 1.1%
S20 - Consent Screen      | 75,000   | 75.0%      | 12,000   | 13.8% ← HIGH DROP
S21 - Consent Given       | 65,000   | 65.0%      | 10,000   | 13.3% ← HIGH DROP
S30 - PIN Screen          | 64,000   | 64.0%      | 1,000    | 1.5%
S31 - PIN Verified        | 60,000   | 60.0%      | 4,000    | 6.3%
S40 - Successfully Shared | 58,000   | 58.0%      | 2,000    | 3.3%
```

---

### 3.3 Report: Average Journey Time by Channel

#### Business Purpose
Measures how long it takes users to complete sharing requests on each channel. Identifies slow channels and opportunities for performance optimization.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Average Journey Time by Channel
WITH request_timestamps AS (
    SELECT
        request_id,
        channel,
        MIN(status_ts) as start_ts,
        MAX(CASE WHEN status_code = 'S40' THEN status_ts END) as success_ts
    FROM sharing_transactions
    GROUP BY request_id, channel
    HAVING MAX(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) = 1
)
SELECT
    channel,
    COUNT(*) as successful_requests,
    ROUND(AVG(EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as avg_duration_seconds,
    ROUND(AVG(EXTRACT(EPOCH FROM (success_ts - start_ts))) / 60, 2) as avg_duration_minutes,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (success_ts - start_ts))) as median_duration_seconds,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (success_ts - start_ts))) as p90_duration_seconds
FROM request_timestamps
GROUP BY channel
ORDER BY avg_duration_seconds;
```

**Alternative using step_latency_ms:**
```sql
-- Sum of all step latencies for successful requests
WITH request_journey_time AS (
    SELECT
        request_id,
        channel,
        SUM(step_latency_ms) / 1000.0 as total_duration_seconds
    FROM sharing_transactions
    WHERE request_id IN (
        SELECT DISTINCT request_id
        FROM sharing_transactions
        WHERE status_code = 'S40'
    )
    GROUP BY request_id, channel
)
SELECT
    channel,
    COUNT(*) as successful_requests,
    ROUND(AVG(total_duration_seconds), 2) as avg_duration_seconds,
    ROUND(AVG(total_duration_seconds) / 60, 2) as avg_duration_minutes,
    ROUND(MIN(total_duration_seconds), 2) as fastest_seconds,
    ROUND(MAX(total_duration_seconds), 2) as slowest_seconds
FROM request_journey_time
GROUP BY channel
ORDER BY avg_duration_seconds;
```

**Step-by-Step Algorithm:**
1. Filter to successful requests (S40)
2. Calculate time difference between first status and S40
3. Group by channel
4. Calculate average, median, and percentiles
5. Sort by fastest to slowest

**Formula:**
```
Journey Time = Timestamp(S40) - Timestamp(S00)
Average Journey Time = SUM(Journey Times) / COUNT(Requests)
```

#### Example Calculation

**Sample Data:**
```
Request ID | Channel      | Start Time | End Time (S40) | Duration
REQ001     | notification | 10:00:00   | 10:02:30       | 150 sec
REQ002     | notification | 11:00:00   | 11:03:00       | 180 sec
REQ003     | qr           | 12:00:00   | 12:01:45       | 105 sec
```

**Calculation:**
```
Notification Average: (150 + 180) / 2 = 165 seconds = 2.75 minutes
QR Average:           105 / 1 = 105 seconds = 1.75 minutes
```

#### Filters & Segmentation
```sql
-- By Platform
WHERE platform = 'ios'

-- By Time of Day
WHERE EXTRACT(HOUR FROM start_ts) BETWEEN 9 AND 17

-- Exclude outliers (>30 minutes)
WHERE EXTRACT(EPOCH FROM (success_ts - start_ts)) <= 1800

-- By Document Count
WHERE required_count = 1 -- Single document requests only
```

#### Visualization Recommendation
- **Chart Type:** Box plot or violin plot
- **X-Axis:** Channel
- **Y-Axis:** Duration (seconds or minutes)
- **Show:** Median, Q1, Q3, outliers
- **Comparison:** Target line at 120 seconds (2 minutes)

#### Key Thresholds & Benchmarks
- **Target:** <120 seconds (2 minutes) average
- **Good:** 120-180 seconds (2-3 minutes)
- **Needs Attention:** >180 seconds (3+ minutes)
- **Expected by Channel:**
  - QR: 90-120 seconds (fastest, in-person)
  - Notification: 120-180 seconds
  - Redirect: 180-240 seconds (slowest, web)

#### Implementation Notes
- **User Time vs System Time:**
  - User time: Includes think time, consent review
  - System time: Pure processing (sum of latencies excluding user steps)
  - Report both separately
- **Edge Cases:**
  - Requests that span days (user left app open) - cap at 30 minutes
  - Very fast completions (<10 seconds) - may indicate testing/automation
- **Performance:** Pre-calculate for popular dimensions
- **Refresh Frequency:** Hourly for monitoring, daily for trending

#### Sample Output

```
Channel      | Successful | Avg Duration | Median | P90  | Fastest | Slowest
             | Requests   | (seconds)    | (sec)  | (sec)| (sec)   | (sec)
-------------|------------|--------------|--------|------|---------|----------
qr           | 52,891     | 98.5         | 85     | 165  | 23      | 1,245
notification | 178,234    | 156.3        | 132    | 287  | 31      | 1,789
redirect     | 5,301      | 223.7        | 198    | 412  | 67      | 1,834
```

---

## 4. Status Flow & Funnel Reports

### 4.1 Report: Complete Journey Funnel (All Channels)

#### Business Purpose
Shows the universal journey all requests follow regardless of channel, identifying the critical drop-off points across the entire flow.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Universal Journey Funnel (All Channels Combined)
WITH request_progress AS (
    SELECT
        request_id,
        MAX(CASE WHEN status_code = 'S00' THEN 1 ELSE 0 END) as reached_s00,
        MAX(CASE WHEN status_code IN ('S03','S07','S05') THEN 1 ELSE 0 END) as reached_channel_entry,
        MAX(CASE WHEN status_code = 'S08' THEN 1 ELSE 0 END) as reached_s08,
        MAX(CASE WHEN status_code IN ('S10','S11') THEN 1 ELSE 0 END) as reached_doc_check,
        MAX(CASE WHEN status_code = 'S10' THEN 1 ELSE 0 END) as docs_ready,
        MAX(CASE WHEN status_code = 'S11' THEN 1 ELSE 0 END) as docs_missing,
        MAX(CASE WHEN status_code = 'S20' THEN 1 ELSE 0 END) as reached_s20,
        MAX(CASE WHEN status_code = 'S21' THEN 1 ELSE 0 END) as reached_s21,
        MAX(CASE WHEN status_code = 'S30' THEN 1 ELSE 0 END) as reached_s30,
        MAX(CASE WHEN status_code = 'S31' THEN 1 ELSE 0 END) as reached_s31,
        MAX(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as reached_s40,
        MAX(CASE WHEN status_code IN ('S41','S42','S43','S44') THEN 1 ELSE 0 END) as reached_terminal_failure
    FROM sharing_transactions
    GROUP BY request_id
)
SELECT
    stage_number,
    stage_name,
    requests,
    ROUND(100.0 * requests / FIRST_VALUE(requests) OVER (ORDER BY stage_number), 2) as pct_of_start,
    requests - LAG(requests) OVER (ORDER BY stage_number) as drop_off,
    ROUND(100.0 * (requests - LAG(requests) OVER (ORDER BY stage_number)) /
          LAG(requests) OVER (ORDER BY stage_number), 2) as drop_off_pct
FROM (
    SELECT 1 as stage_number, 'Request Created (S00)' as stage_name,
           SUM(reached_s00) as requests FROM request_progress
    UNION ALL
    SELECT 2, 'Channel Entry (S03/S05/S07)',
           SUM(reached_channel_entry) FROM request_progress
    UNION ALL
    SELECT 3, 'Request Viewed (S08)',
           SUM(reached_s08) FROM request_progress
    UNION ALL
    SELECT 4, 'Document Check (S10/S11)',
           SUM(reached_doc_check) FROM request_progress
    UNION ALL
    SELECT 5, 'Consent Screen (S20)',
           SUM(reached_s20) FROM request_progress
    UNION ALL
    SELECT 6, 'Consent Given (S21)',
           SUM(reached_s21) FROM request_progress
    UNION ALL
    SELECT 7, 'PIN Screen (S30)',
           SUM(reached_s30) FROM request_progress
    UNION ALL
    SELECT 8, 'PIN Verified (S31)',
           SUM(reached_s31) FROM request_progress
    UNION ALL
    SELECT 9, 'Successfully Shared (S40)',
           SUM(reached_s40) FROM request_progress
) stages
ORDER BY stage_number;
```

**Step-by-Step Algorithm:**
1. Create binary flags for each major stage in the journey
2. Aggregate flags across all requests
3. Calculate cumulative retention from start
4. Calculate step-by-step drop-off
5. Present as ordered funnel stages

**Formula:**
```
Retention at Stage N = (Requests at Stage N / Requests at Stage 0) × 100
Drop-off between Stages = Requests at Stage N - Requests at Stage N+1
Drop-off Rate = (Drop-off / Requests at Stage N) × 100
```

#### Example Calculation

**Sample Data:**
```
Stage                   | Requests
------------------------|----------
S00 (Created)           | 1,000
S08 (Viewed)            | 900
S20 (Consent Screen)    | 850
S21 (Consent Given)     | 700
S30 (PIN)               | 695
S31 (PIN Verified)      | 650
S40 (Success)           | 640
```

**Calculation:**
```
S08: 900/1000 = 90% retention, 100 drop-off (10%)
S20: 850/1000 = 85% retention, 50 drop-off (5.6% from S08)
S21: 700/1000 = 70% retention, 150 drop-off (17.6% from S20) ← CRITICAL
S30: 695/1000 = 69.5% retention, 5 drop-off (0.7% from S21)
S31: 650/1000 = 65% retention, 45 drop-off (6.5% from S30)
S40: 640/1000 = 64% retention, 10 drop-off (1.5% from S31)
```

#### Filters & Segmentation
```sql
-- By Date Range
WHERE status_ts >= '2025-11-01'

-- By Platform
WHERE platform IN ('ios', 'android')

-- By Channel
WHERE channel = 'notification'

-- By Document Availability
WHERE (docs_ready = 1 OR docs_missing = 1) -- Only those who reached doc check
```

#### Visualization Recommendation
- **Chart Type:** Funnel chart (wide to narrow)
- **Colors:** Gradient from blue (start) to green (success)
- **Annotations:** Label largest drop-offs
- **Interactive:** Click stage to see details of drop-off reasons

#### Key Thresholds & Benchmarks
- **Expected Drop-offs:**
  - S00→S08: <12% (notification/channel engagement)
  - S08→S20: <15% (document check and prep)
  - S20→S21: <20% (consent - biggest user decision)
  - S21→S30: <5% (technical transition)
  - S30→S31: <10% (PIN entry)
  - S31→S40: <5% (final processing)
- **Alert If:**
  - Any stage drops >30%
  - Overall S00→S40 <60%

#### Implementation Notes
- **Collapsed Stages:** Combine channel-specific statuses (S03/S05/S07) into single "Channel Entry"
- **Document Split:** Can split S10/S11 into separate stages to show impact of missing docs
- **Progressive Profiling:** Track which stage users first abandon (create cohorts)
- **Performance:** Materialized view, refresh hourly
- **Refresh Frequency:** Real-time for operations, daily for executive

#### Sample Output

```
Stage | Stage Name              | Requests | % of Start | Drop-off | Drop-off %
------|-------------------------|----------|------------|----------|------------
1     | Request Created (S00)   | 350,802  | 100.0%     | -        | -
2     | Channel Entry           | 338,129  | 96.4%      | 12,673   | 3.6%
3     | Request Viewed (S08)    | 311,074  | 88.7%      | 27,055   | 8.0%
4     | Document Check          | 303,586  | 86.5%      | 7,488    | 2.4%
5     | Consent Screen (S20)    | 270,525  | 77.1%      | 33,061   | 10.9% ← HIGH
6     | Consent Given (S21)     | 258,759  | 73.8%      | 11,766   | 4.3%
7     | PIN Screen (S30)        | 247,114  | 70.4%      | 11,645   | 4.5%
8     | PIN Verified (S31)      | 239,857  | 68.4%      | 7,257    | 2.9%
9     | Successfully Shared     | 236,426  | 67.4%      | 3,431    | 1.4%
```

**Key Insight:** Biggest drops are at Consent Screen (10.9%) and Channel Entry (8.0%)

---

### 4.2 Report: Status Transition Matrix

#### Business Purpose
Shows the flow of requests from one status to another, identifying unexpected paths and common failure transitions.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Status Transition Matrix
WITH transitions AS (
    SELECT
        previous_status,
        status_code as next_status,
        COUNT(*) as transition_count
    FROM sharing_transactions
    WHERE previous_status IS NOT NULL
    GROUP BY previous_status, status_code
),
totals AS (
    SELECT
        previous_status,
        SUM(transition_count) as total_from_status
    FROM transitions
    GROUP BY previous_status
)
SELECT
    t.previous_status,
    t.next_status,
    t.transition_count,
    ROUND(100.0 * t.transition_count / tt.total_from_status, 2) as pct_of_status,
    CASE
        WHEN t.next_status IN ('S40','S41','S42','S43','S44') THEN 'Terminal'
        ELSE 'In Progress'
    END as transition_type
FROM transitions t
JOIN totals tt ON t.previous_status = tt.previous_status
WHERE t.transition_count >= 100  -- Filter noise
ORDER BY t.previous_status, t.transition_count DESC;
```

**Heatmap Version (for visualization):**
```sql
-- Pivot for heatmap
SELECT
    previous_status,
    SUM(CASE WHEN status_code = 'S08' THEN 1 ELSE 0 END) as to_s08,
    SUM(CASE WHEN status_code = 'S10' THEN 1 ELSE 0 END) as to_s10,
    SUM(CASE WHEN status_code = 'S11' THEN 1 ELSE 0 END) as to_s11,
    SUM(CASE WHEN status_code = 'S20' THEN 1 ELSE 0 END) as to_s20,
    SUM(CASE WHEN status_code = 'S21' THEN 1 ELSE 0 END) as to_s21,
    SUM(CASE WHEN status_code = 'S30' THEN 1 ELSE 0 END) as to_s30,
    SUM(CASE WHEN status_code = 'S31' THEN 1 ELSE 0 END) as to_s31,
    SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as to_s40,
    SUM(CASE WHEN status_code = 'S41' THEN 1 ELSE 0 END) as to_s41,
    SUM(CASE WHEN status_code = 'S42' THEN 1 ELSE 0 END) as to_s42,
    SUM(CASE WHEN status_code = 'S43' THEN 1 ELSE 0 END) as to_s43,
    SUM(CASE WHEN status_code = 'S44' THEN 1 ELSE 0 END) as to_s44
FROM sharing_transactions
WHERE previous_status IS NOT NULL
GROUP BY previous_status
ORDER BY previous_status;
```

**Step-by-Step Algorithm:**
1. For each status event, capture the previous_status and current status_code
2. Group by (previous_status, status_code) pair
3. Count transitions for each pair
4. Calculate percentage of each transition from source status
5. Sort by volume or anomaly score

**Formula:**
```
Transition % = (Count of A→B transitions / Total transitions from A) × 100
Expected Transition = Based on happy path (e.g., S20→S21 should be ~80%)
Anomaly Score = |Actual % - Expected %|
```

#### Example Calculation

**Sample Data:**
```
Previous | Next | Count
---------|------|-------
S20      | S21  | 800
S20      | S43  | 150
S20      | S42  | 50
```

**Calculation:**
```
Total from S20: 800 + 150 + 50 = 1,000
S20→S21: 800/1000 = 80% (expected - good)
S20→S43: 150/1000 = 15% (user abort - acceptable)
S20→S42: 50/1000 = 5% (expired - needs attention)
```

#### Filters & Segmentation
```sql
-- By Channel
WHERE channel = 'notification'

-- By Platform
WHERE platform = 'android'

-- Focus on specific status
WHERE previous_status = 'S20'

-- Only failures
WHERE status_code IN ('S41','S42','S43','S44')
```

#### Visualization Recommendation
- **Chart Type:** Sankey diagram or heatmap
- **Sankey:**
  - Nodes: Status codes
  - Links: Transitions (width = volume)
  - Color: Green (success path), Red (failure path)
- **Heatmap:**
  - Rows: Previous status
  - Columns: Next status
  - Cell color: Transition volume (darker = more)

#### Key Thresholds & Benchmarks
- **Expected Happy Path Transitions:**
  - S20→S21: >75%
  - S21→S30: >95%
  - S30→S31: >85%
  - S31→S40: >95%
- **Acceptable Failure Transitions:**
  - Any→S43: <20% (user abort)
  - Any→S42: <10% (expired)
  - Any→S41: <5% (technical error)
- **Alert If:**
  - Happy path transition drops >10%
  - Unexpected transition appears (e.g., S21→S41 >5%)

#### Implementation Notes
- **Use Cases:**
  - Identify broken flows (e.g., S08 directly to S40 - skipped consent?)
  - Find most common failure points (which status leads to S41 most?)
  - Optimize journey (eliminate unnecessary transitions)
- **Edge Cases:**
  - Loops (e.g., S30→S32→S30 for PIN retry) - count each instance
  - Null previous_status (first event) - exclude or label as "START"
- **Performance:** Can be large matrix (44 × 44), filter to common transitions
- **Refresh Frequency:** Daily for analysis, on-demand for deep dives

#### Sample Output

**Top 20 Transitions:**
```
From Status | To Status | Count   | % of From | Type      | Notes
------------|-----------|---------|-----------|-----------|------------------
S21         | S30       | 247,114 | 95.5%     | Progress  | Expected - good
S20         | S21       | 258,759 | 95.6%     | Progress  | High consent rate
S30         | S31       | 239,857 | 97.1%     | Progress  | High PIN success
S31         | S40       | 236,426 | 98.6%     | Terminal  | Final step reliable
S20         | S43       | 11,766  | 4.4%      | Terminal  | Consent decline
S08         | S20       | 270,525 | 87.0%     | Progress  | Doc check passed
S08         | S42       | 25,689  | 8.3%      | Terminal  | Expired at view
S30         | S32       | 7,257   | 2.9%      | Progress  | PIN failed (retry)
S21         | S43       | 11,645  | 4.5%      | Terminal  | Post-consent abort
S10         | S20       | 236,426 | 84.9%     | Progress  | Docs ready → consent
```

---

### 4.3 Report: Most Common Successful Paths

#### Business Purpose
Identifies the typical sequence of statuses for successful requests, helping understand optimal user journeys and detect variations.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Most Common Successful Paths (Full Journey)
WITH successful_requests AS (
    SELECT DISTINCT request_id
    FROM sharing_transactions
    WHERE status_code = 'S40'
),
request_paths AS (
    SELECT
        st.request_id,
        ARRAY_AGG(st.status_code ORDER BY st.status_ts) as status_path
    FROM sharing_transactions st
    INNER JOIN successful_requests sr ON st.request_id = sr.request_id
    GROUP BY st.request_id
)
SELECT
    ARRAY_TO_STRING(status_path, ' → ') as journey_path,
    COUNT(*) as request_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as pct_of_successful
FROM request_paths
GROUP BY status_path
ORDER BY request_count DESC
LIMIT 20;
```

**Simplified Version (Key Milestones Only):**
```sql
-- Simplified Path (Major Milestones)
WITH successful_requests AS (
    SELECT DISTINCT request_id
    FROM sharing_transactions
    WHERE status_code = 'S40'
),
request_milestones AS (
    SELECT
        st.request_id,
        MAX(CASE WHEN st.status_code IN ('S01','S04','S06') THEN st.status_code END) as channel_entry,
        MAX(CASE WHEN st.status_code = 'S10' THEN 'S10'
                 WHEN st.status_code = 'S11' THEN 'S11' END) as doc_status,
        MAX(CASE WHEN st.status_code = 'S12' THEN 'S12' END) as doc_retrieval,
        'S20' as consent_screen,
        'S30' as pin_screen
    FROM sharing_transactions st
    INNER JOIN successful_requests sr ON st.request_id = sr.request_id
    GROUP BY st.request_id
)
SELECT
    CONCAT_WS(' → ', channel_entry, 'S08', doc_status,
              CASE WHEN doc_retrieval IS NOT NULL THEN doc_retrieval END,
              'S20', 'S21', 'S30', 'S31', 'S40') as simplified_path,
    COUNT(*) as request_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as pct_of_successful,
    ROUND(AVG(EXTRACT(EPOCH FROM (MAX(st.status_ts) - MIN(st.status_ts)))), 2) as avg_duration_seconds
FROM request_milestones rm
JOIN sharing_transactions st ON rm.request_id = st.request_id
GROUP BY simplified_path
ORDER BY request_count DESC;
```

**Step-by-Step Algorithm:**
1. Filter to requests that reached S40
2. For each request, concatenate status_code sequence (ordered by timestamp)
3. Group identical sequences together
4. Count frequency of each unique path
5. Calculate percentage of successful requests
6. Sort by most common paths

**Formula:**
```
Path Frequency = (Requests following Path X / Total successful requests) × 100
```

#### Example Calculation

**Sample Data:**
```
Request ID | Status Sequence
REQ001     | S00 → S01 → S03 → S08 → S10 → S20 → S21 → S30 → S31 → S40
REQ002     | S00 → S01 → S03 → S08 → S10 → S20 → S21 → S30 → S31 → S40
REQ003     | S00 → S06 → S07 → S08 → S11 → S12 → S13 → S20 → S21 → S30 → S31 → S40
REQ004     | S00 → S01 → S03 → S08 → S10 → S20 → S21 → S30 → S31 → S40
```

**Calculation:**
```
Path 1 (Notification + Docs Ready): 3 requests (75%)
Path 2 (QR + Docs Missing/Retrieved): 1 request (25%)
```

#### Filters & Segmentation
```sql
-- By Channel
WHERE channel = 'notification'

-- By Date Range
WHERE status_ts >= '2025-11-01'

-- Exclude edge cases (too fast or too slow)
HAVING AVG(duration_seconds) BETWEEN 30 AND 600
```

#### Visualization Recommendation
- **Chart Type:**
  - Horizontal bar chart (top 10 paths)
  - Sankey diagram (flow visualization)
- **Labels:** Show path and percentage
- **Interactive:** Click path to see example request_ids

#### Key Thresholds & Benchmarks
- **Typical Successful Paths:**
  1. **Notification + Docs Ready (75%):** S00→S01→S03→S08→S10→S20→S21→S30→S31→S40
  2. **QR + Docs Ready (15%):** S00→S06→S07→S08→S10→S20→S21→S30→S31→S40
  3. **Notification + Doc Retrieval (8%):** S00→S01→S03→S08→S11→S12→S13→S20→S21→S30→S31→S40
  4. **Redirect + Docs Ready (2%):** S00→S04→S05→S08→S10→S20→S21→S30→S31→S40

#### Implementation Notes
- **Full Path vs Simplified:** Full path creates too many unique combinations; use simplified (milestones only) for analysis
- **Use Cases:**
  - Identify optimal journey for onboarding
  - Detect inefficient paths (too many steps)
  - Find variations by channel/platform
- **Edge Cases:**
  - Very long paths (retry loops) - cap at 20 statuses
  - Duplicate statuses (e.g., S30 twice for PIN retry) - deduplicate or mark
- **Performance:** ARRAY_AGG can be slow on large datasets; limit to recent data or sample
- **Refresh Frequency:** Weekly for trend analysis

#### Sample Output

```
Rank | Journey Path                                        | Requests | % of Success | Avg Duration
-----|-----------------------------------------------------|----------|--------------|---------------
1    | S00→S01→S03→S08→S10→S20→S21→S30→S31→S40            | 152,341  | 64.4%        | 142 sec
2    | S00→S06→S07→S08→S10→S20→S21→S30→S31→S40            | 42,567   | 18.0%        | 98 sec
3    | S00→S01→S03→S08→S11→S12→S13→S20→S21→S30→S31→S40   | 18,234   | 7.7%         | 187 sec
4    | S00→S04→S05→S08→S10→S20→S21→S30→S31→S40            | 5,123    | 2.2%         | 223 sec
5    | S00→S01→S03→S08→S10→S20→S21→S30→S32→S30→S31→S40   | 4,891    | 2.1%         | 201 sec
     | (with PIN retry)                                    |          |              |
6    | S00→S06→S07→S08→S11→S12→S13→S20→S21→S30→S31→S40   | 3,456    | 1.5%         | 165 sec
...
```

**Key Insights:**
- 64% follow "perfect" notification path with docs ready
- 18% use QR (faster by 44 seconds average)
- 7.7% require document retrieval (adds 45 seconds)
- 2.1% have PIN retry (adds 59 seconds)

---

### 4.4 Report: Most Common Failure Paths

#### Business Purpose
Identifies where and how requests fail, revealing problematic user journeys and technical bottlenecks.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Most Common Failure Paths
WITH failed_requests AS (
    SELECT
        request_id,
        status_code as terminal_status
    FROM (
        SELECT
            request_id,
            status_code,
            ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
        FROM sharing_transactions
        WHERE status_code IN ('S41', 'S42', 'S43', 'S44')
    ) t
    WHERE rn = 1
),
request_paths AS (
    SELECT
        fr.request_id,
        fr.terminal_status,
        ARRAY_AGG(st.status_code ORDER BY st.status_ts) as status_path
    FROM sharing_transactions st
    INNER JOIN failed_requests fr ON st.request_id = fr.request_id
    GROUP BY fr.request_id, fr.terminal_status
)
SELECT
    terminal_status,
    CASE
        WHEN terminal_status = 'S41' THEN 'Technical Error'
        WHEN terminal_status = 'S42' THEN 'Expired'
        WHEN terminal_status = 'S43' THEN 'User Aborted'
        WHEN terminal_status = 'S44' THEN 'Not Eligible'
    END as failure_type,
    ARRAY_TO_STRING(status_path, ' → ') as journey_path,
    COUNT(*) as request_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(PARTITION BY terminal_status), 2) as pct_of_failure_type
FROM request_paths
GROUP BY terminal_status, status_path
ORDER BY terminal_status, request_count DESC;
```

**Last Step Before Failure:**
```sql
-- What was the last status before failure?
WITH failed_requests AS (
    SELECT
        request_id,
        status_code as terminal_status,
        previous_status as last_step_before_failure
    FROM (
        SELECT
            request_id,
            status_code,
            previous_status,
            ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
        FROM sharing_transactions
        WHERE status_code IN ('S41', 'S42', 'S43', 'S44')
    ) t
    WHERE rn = 1
)
SELECT
    terminal_status,
    CASE
        WHEN terminal_status = 'S41' THEN 'Technical Error'
        WHEN terminal_status = 'S42' THEN 'Expired'
        WHEN terminal_status = 'S43' THEN 'User Aborted'
        WHEN terminal_status = 'S44' THEN 'Not Eligible'
    END as failure_type,
    last_step_before_failure,
    COUNT(*) as failure_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(PARTITION BY terminal_status), 2) as pct_of_failure_type
FROM failed_requests
GROUP BY terminal_status, last_step_before_failure
ORDER BY terminal_status, failure_count DESC;
```

**Step-by-Step Algorithm:**
1. Identify all requests with terminal failure status (S41-S44)
2. Get the complete journey path for each failed request
3. Group identical paths by failure type
4. Count frequency and calculate percentages
5. Sort by most common failure paths

**Formula:**
```
Failure Path Frequency = (Requests with Path X ending in SXX / Total failures of type SXX) × 100
```

#### Example Calculation

**Sample Data:**
```
Request ID | Path                                      | Terminal
REQ001     | S00 → S01 → S03 → S08 → S20 → S43        | S43
REQ002     | S00 → S01 → S03 → S08 → S20 → S43        | S43
REQ003     | S00 → S01 → S03 → S08 → S11 → S44        | S44
REQ004     | S00 → S01 → S03 → S08 → S20 → S21 → S41  | S41
```

**Calculation:**
```
S43 Failures: 2 total
  - Path "...S08→S20→S43": 2 (100% of S43 failures)

S44 Failures: 1 total
  - Path "...S08→S11→S44": 1 (100% of S44 failures)

S41 Failures: 1 total
  - Path "...S20→S21→S41": 1 (100% of S41 failures)
```

#### Filters & Segmentation
```sql
-- By Failure Type
WHERE terminal_status = 'S43'

-- By Channel/Platform
WHERE channel = 'notification' AND platform = 'android'

-- Include Error Details
SELECT
    fr.terminal_status,
    fr.last_step_before_failure,
    st.error_code,
    st.error_source,
    COUNT(*) as failure_count
FROM failed_requests fr
JOIN sharing_transactions st ON fr.request_id = st.request_id
    AND st.status_code = fr.terminal_status
WHERE st.error_code IS NOT NULL
GROUP BY fr.terminal_status, fr.last_step_before_failure, st.error_code, st.error_source;
```

#### Visualization Recommendation
- **Chart Type:**
  - Grouped bar chart (by failure type, showing top paths)
  - Sankey diagram (flow to failure)
- **Colors:** Red spectrum (darker = more common)
- **Annotations:** Show last step before failure

#### Key Thresholds & Benchmarks
- **Common Failure Patterns:**
  - **S43 (User Abort):**
    - S20→S43: 50%+ (consent declined) - Expected
    - S08→S43: 20%+ (abandoned at view) - UX issue
    - S21→S43: 10%+ (post-consent abandon) - Process issue
  - **S42 (Expired):**
    - S08→S42: 60%+ (expired while viewing) - Timeout too short?
    - S20→S42: 30%+ (expired during consent) - User taking too long
  - **S41 (Technical Error):**
    - S31→S41: 40%+ (failed after PIN) - Backend issue
    - S21→S41: 30%+ (failed after consent) - Signing issue
  - **S44 (Not Eligible):**
    - S11→S44: 80%+ (missing docs) - Expected

#### Implementation Notes
- **Use Cases:**
  - Prioritize UX fixes (high S43 from S08 = improve onboarding)
  - Identify technical issues (S41 patterns)
  - Adjust timeouts (S42 patterns)
- **Actionability:**
  - Each failure path suggests specific fix
  - Track over time to measure improvement
- **Performance:** Can generate many unique paths; limit to top 50
- **Refresh Frequency:** Daily for monitoring, weekly for deep analysis

#### Sample Output

**S43 (User Aborted) - Top 10 Paths:**
```
Last Step | Full Path (Simplified)                  | Count  | % of S43
----------|----------------------------------------|--------|----------
S20       | ... → S08 → S20 → S43                  | 28,156 | 45.0%
S08       | ... → S08 → S43                        | 18,234 | 29.2%
S21       | ... → S20 → S21 → S43                  | 11,645 | 18.6%
S30       | ... → S21 → S30 → S43                  | 3,456  | 5.5%
S10       | ... → S10 → S43                        | 1,024  | 1.6%
```

**S41 (Technical Error) - Top 10 Paths:**
```
Last Step | Error Code         | Count | % of S41
----------|-------------------|-------|----------
S31       | signing_timeout   | 2,378 | 19.6%
S21       | server_error      | 2,474 | 20.4%
S15       | issuer_timeout    | 3,167 | 26.1%
S30       | pin_invalid       | 1,537 | 12.7%
S13       | doc_fetch_failed  | 1,249 | 10.3%
```

**Key Insights:**
- 45% of user aborts happen at consent screen - highest priority UX fix
- 29% never get past initial view - notification/messaging issue
- 26% of technical failures are issuer timeouts - need retry logic
- 20% fail at signing step - backend optimization needed

---

## 5. Error Analysis Reports

### 5.1 Report: Error Frequency by Error Code

#### Business Purpose
Identifies the most common technical errors to prioritize engineering efforts and improve system reliability.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Error Frequency by Error Code
WITH error_events AS (
    SELECT
        request_id,
        status_code,
        error_code,
        error_source,
        status_ts
    FROM sharing_transactions
    WHERE error_code IS NOT NULL
)
SELECT
    error_code,
    error_source,
    COUNT(*) as error_count,
    COUNT(DISTINCT request_id) as affected_requests,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as pct_of_total_errors,
    MIN(status_ts) as first_seen,
    MAX(status_ts) as last_seen
FROM error_events
GROUP BY error_code, error_source
ORDER BY error_count DESC;
```

**Error Impact Analysis:**
```sql
-- How many errors lead to S41 (Technical Failure)?
WITH error_requests AS (
    SELECT DISTINCT request_id, error_code, error_source
    FROM sharing_transactions
    WHERE error_code IS NOT NULL
),
request_outcomes AS (
    SELECT
        er.request_id,
        er.error_code,
        er.error_source,
        MAX(CASE WHEN st.status_code = 'S41' THEN 1 ELSE 0 END) as ended_in_s41,
        MAX(CASE WHEN st.status_code = 'S40' THEN 1 ELSE 0 END) as ended_in_s40
    FROM error_requests er
    JOIN sharing_transactions st ON er.request_id = st.request_id
    WHERE st.status_code IN ('S40', 'S41', 'S42', 'S43', 'S44')
    GROUP BY er.request_id, er.error_code, er.error_source
)
SELECT
    error_code,
    error_source,
    COUNT(*) as total_errors,
    SUM(ended_in_s41) as led_to_s41,
    SUM(ended_in_s40) as recovered_to_s40,
    ROUND(100.0 * SUM(ended_in_s41) / COUNT(*), 2) as s41_rate,
    ROUND(100.0 * SUM(ended_in_s40) / COUNT(*), 2) as recovery_rate
FROM request_outcomes
GROUP BY error_code, error_source
ORDER BY led_to_s41 DESC;
```

**Step-by-Step Algorithm:**
1. Filter to rows where error_code IS NOT NULL
2. Group by error_code and error_source
3. Count total occurrences and unique requests affected
4. Calculate percentage of total errors
5. Determine impact (how many lead to S41 vs recover to S40)
6. Sort by most frequent errors

**Formula:**
```
Error Frequency = (Count of Error X / Total error events) × 100
Impact Rate = (Requests with Error X that end in S41 / Requests with Error X) × 100
Recovery Rate = (Requests with Error X that end in S40 / Requests with Error X) × 100
```

#### Example Calculation

**Sample Data:**
```
Request ID | Error Code        | Final Status
REQ001     | issuer_timeout    | S41
REQ002     | issuer_timeout    | S41
REQ003     | pin_incorrect     | S40 (recovered)
REQ004     | issuer_timeout    | S41
REQ005     | network_error     | S41
```

**Calculation:**
```
issuer_timeout: 3 occurrences (60% of errors), 3 led to S41 (100% impact), 0 recovered
pin_incorrect:  1 occurrence (20% of errors), 0 led to S41 (0% impact), 1 recovered (100% recovery)
network_error:  1 occurrence (20% of errors), 1 led to S41 (100% impact), 0 recovered
```

#### Filters & Segmentation
```sql
-- By Date Range
WHERE status_ts >= CURRENT_DATE - INTERVAL '7 days'

-- By Error Source
WHERE error_source = 'issuer'

-- By Service Provider (join if sp_id is needed)
WHERE sp_id = 'Botim'

-- By Platform
WHERE platform = 'android'

-- Only Fatal Errors (led to S41)
WHERE request_id IN (
    SELECT request_id FROM sharing_transactions WHERE status_code = 'S41'
)
```

#### Visualization Recommendation
- **Chart Type:**
  - Horizontal bar chart (error count)
  - Pie chart (error source distribution)
  - Stacked bar (error + recovery rate)
- **Colors:**
  - Red: High impact errors (>80% S41 rate)
  - Orange: Medium impact (40-80% S41 rate)
  - Yellow: Low impact (<40% S41 rate)
- **Data Labels:** Show count and percentage

#### Key Thresholds & Benchmarks
- **Error Volume Targets:**
  - Total Errors: <5% of all status events
  - Fatal Errors (leading to S41): <3% of all requests
- **Top Error Codes (Expected):**
  1. `issuer_timeout`: Issuer system slow/unavailable
  2. `signing_timeout`: eSeal signing too slow
  3. `pin_incorrect`: User enters wrong PIN
  4. `network_error`: Connectivity issues
  5. `server_error`: DV backend issues
- **Alert Thresholds:**
  - Any error >500 occurrences/hour
  - New error code appears
  - Error spike >2x baseline

#### Implementation Notes
- **Error Code Taxonomy:**
  - `issuer_*`: Issuer system issues (ICP, SP)
  - `pin_*`: PIN authentication issues
  - `signing_*`: eSeal/signature issues
  - `network_*`: Connectivity issues
  - `server_*`: DV backend issues
  - `timeout_*`: Generic timeouts
  - `validation_*`: Data validation failures
- **Use Cases:**
  - Prioritize engineering sprints (fix highest impact errors first)
  - SLA monitoring with issuers
  - Capacity planning (network/server errors)
- **Edge Cases:**
  - Multiple errors per request (count each, but flag repeated errors)
  - Null error_source (categorize as "unknown")
- **Performance:** Index on error_code and status_ts
- **Refresh Frequency:** Real-time (1-minute) for critical error monitoring

#### Sample Output

```
Error Code              | Source  | Count | Affected | % of Errors | Impact | Recovery | First Seen | Last Seen
                        |         |       | Requests |             | (S41%) | (S40%)   |            |
------------------------|---------|-------|----------|-------------|--------|----------|------------|------------
issuer_timeout          | issuer  | 3,167 | 3,089    | 26.1%       | 97.2%  | 1.8%     | 2025-11-12 | 2025-11-18
server_error            | dv      | 2,474 | 2,401    | 20.4%       | 94.5%  | 3.1%     | 2025-11-12 | 2025-11-18
signing_timeout         | dv      | 2,378 | 2,312    | 19.6%       | 96.8%  | 1.2%     | 2025-11-12 | 2025-11-18
pin_incorrect           | user    | 1,537 | 1,498    | 12.7%       | 2.8%   | 94.2%    | 2025-11-12 | 2025-11-18
document_fetch_failed   | issuer  | 1,249 | 1,217    | 10.3%       | 89.3%  | 8.7%     | 2025-11-12 | 2025-11-18
network_timeout         | network | 789   | 768      | 6.5%        | 78.9%  | 18.2%    | 2025-11-12 | 2025-11-18
issuer_not_found        | issuer  | 345   | 345      | 2.8%        | 100.0% | 0.0%     | 2025-11-12 | 2025-11-18
validation_error        | dv      | 194   | 189      | 1.6%        | 67.2%  | 29.8%    | 2025-11-13 | 2025-11-17
```

**Key Insights:**
- Top 3 errors account for 66% of all errors
- `issuer_timeout` and `signing_timeout` have >96% impact - critical to address
- `pin_incorrect` has 94% recovery rate - users can retry successfully
- `issuer_not_found` has 100% fatality - need better SP validation at request creation

---

### 5.2 Report: Error Source Distribution

#### Business Purpose
Attributes errors to responsible systems (issuer, network, DV backend, user) to assign accountability and focus fixes.

#### Data Source
Table: `sharing_transactions`

#### Calculation Logic

**SQL Implementation:**
```sql
-- Error Source Distribution
SELECT
    error_source,
    CASE
        WHEN error_source = 'issuer' THEN 'External - Issuer Systems'
        WHEN error_source = 'network' THEN 'Infrastructure - Network'
        WHEN error_source = 'dv' THEN 'Internal - DV Backend'
        WHEN error_source = 'user_cancel' THEN 'User Action'
        ELSE 'Unknown'
    END as source_category,
    COUNT(*) as error_count,
    COUNT(DISTINCT request_id) as affected_requests,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as pct_of_total_errors,
    COUNT(DISTINCT error_code) as unique_error_types
FROM sharing_transactions
WHERE error_code IS NOT NULL
GROUP BY error_source
ORDER BY error_count DESC;
```

**Error Source by Channel/Platform:**
```sql
-- Which channels/platforms have most errors from each source?
SELECT
    error_source,
    channel,
    platform,
    COUNT(*) as error_count,
    COUNT(DISTINCT request_id) as affected_requests,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(PARTITION BY error_source), 2) as pct_within_source
FROM sharing_transactions
WHERE error_code IS NOT NULL
GROUP BY error_source, channel, platform
ORDER BY error_source, error_count DESC;
```

**Step-by-Step Algorithm:**
1. Filter to error events (error_code IS NOT NULL)
2. Group by error_source
3. Count occurrences and affected requests
4. Calculate percentage distribution
5. Sort by most problematic source

**Formula:**
```
Source Distribution = (Errors from Source X / Total errors) × 100
```

#### Example Calculation

**Sample Data:**
```
Request ID | Error Source | Error Code
REQ001     | issuer       | issuer_timeout
REQ002     | issuer       | doc_fetch_failed
REQ003     | dv           | server_error
REQ004     | network      | network_timeout
REQ005     | issuer       | issuer_timeout
```

**Calculation:**
```
Issuer:  3 errors (60%)
DV:      1 error (20%)
Network: 1 error (20%)
```

#### Filters & Segmentation
```sql
-- By Date Range
WHERE status_ts >= CURRENT_DATE - INTERVAL '30 days'

-- By Service Provider
WHERE sp_id = 'Botim'

-- Exclude User-Caused Errors
WHERE error_source != 'user_cancel'

-- Only Fatal Errors
WHERE request_id IN (SELECT request_id FROM sharing_transactions WHERE status_code = 'S41')
```

#### Visualization Recommendation
- **Chart Type:**
  - Pie chart (source distribution)
  - Stacked bar chart (source × channel/platform)
  - Treemap (source → error codes)
- **Colors:**
  - Issuer: Orange (external dependency)
  - Network: Yellow (infrastructure)
  - DV: Red (internal - high priority)
  - User: Gray (expected behavior)

#### Key Thresholds & Benchmarks
- **Expected Distribution (Healthy System):**
  - Issuer: 40-50% (external, harder to control)
  - Network: 20-30% (infrastructure, partially controllable)
  - DV: 10-20% (internal, should be lowest)
  - User: 10-20% (expected user behavior)
- **Alert If:**
  - DV errors >25% (internal quality issue)
  - Any source >70% (single point of failure)
  - New source category appears

#### Implementation Notes
- **Error Source Definitions:**
  - `issuer`: Errors from ICP or SP issuer systems (timeouts, not found, fetch failures)
  - `network`: Connectivity, DNS, firewall, TLS errors
  - `dv`: DV backend errors (server errors, database, signing service)
  - `user_cancel`: User-initiated actions (PIN incorrect, manual cancel)
- **Use Cases:**
  - Accountability: Track SLAs with issuers
  - Prioritization: Fix DV errors first (controllable)
  - Capacity: Network errors may indicate scaling issues
- **Edge Cases:**
  - Cascading errors (network failure → issuer timeout) - attribute to root cause
  - Null error_source - investigate and categorize
- **Performance:** Very fast query with index on error_source
- **Refresh Frequency:** Real-time for operational dashboards

#### Sample Output

```
Error Source | Category                    | Error Count | Affected Requests | % of Errors | Unique Types
-------------|----------------------------|-------------|-------------------|-------------|---------------
issuer       | External - Issuer Systems  | 4,761       | 4,651             | 39.2%       | 8
dv           | Internal - DV Backend      | 4,852       | 4,713             | 39.9%       | 12
network      | Infrastructure - Network   | 1,845       | 1,798             | 15.2%       | 5
user_cancel  | User Action                | 685         | 672               | 5.6%        | 3
```

**Trend Over Time:**
```
Week of     | Issuer % | DV %   | Network % | User %
------------|----------|--------|-----------|--------
2025-11-04  | 42.3%    | 35.1%  | 17.2%     | 5.4%
2025-11-11  | 39.2%    | 39.9%  | 15.2%     | 5.7%
2025-11-18  | 37.8%    | 41.2%  | 14.9%     | 6.1%
```

**Alert:** DV error percentage increasing week-over-week - investigate backend issues

---

(Continuing with remaining sections...)

Due to length constraints, I'll now create the complete files with all sections. Let me continue with the comprehensive documentation.
