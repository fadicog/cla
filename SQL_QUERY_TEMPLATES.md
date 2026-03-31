# SQL Query Templates: UAE PASS Document Sharing Analytics
**Version:** 1.0
**Last Updated:** 2026-01-09
**Purpose:** Copy-paste ready SQL queries for all sharing analytics reports

---

## Table of Contents

1. [Overall Performance Metrics](#1-overall-performance-metrics)
2. [Channel Performance](#2-channel-performance)
3. [Status Flow & Funnel](#3-status-flow--funnel)
4. [Error Analysis](#4-error-analysis)
5. [Service Provider Performance](#5-service-provider-performance)
6. [User Behavior](#6-user-behavior)
7. [Document Readiness](#7-document-readiness)
8. [Time & Latency](#8-time--latency)
9. [Platform Comparison](#9-platform-comparison)
10. [Advanced Analytics](#10-advanced-analytics)

---

## 1. Overall Performance Metrics

### 1.1 Overall Success Rate

```sql
-- Overall Success Rate
-- Returns: Total requests and success percentage
-- Use Case: Primary KPI for executive dashboard

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
    ROUND(100.0 * SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate_pct,
    SUM(CASE WHEN status_code = 'S41' THEN 1 ELSE 0 END) as technical_failures,
    SUM(CASE WHEN status_code = 'S42' THEN 1 ELSE 0 END) as expired,
    SUM(CASE WHEN status_code = 'S43' THEN 1 ELSE 0 END) as user_aborted,
    SUM(CASE WHEN status_code = 'S44' THEN 1 ELSE 0 END) as not_eligible
FROM final_statuses;
```

### 1.2 Overall Success Rate with Date Filter

```sql
-- Overall Success Rate (Date Range)
-- Parameters: @start_date, @end_date

WITH terminal_requests AS (
    SELECT
        request_id,
        status_code,
        status_ts,
        ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
    FROM sharing_transactions
    WHERE status_code IN ('S40', 'S41', 'S42', 'S43', 'S44')
      AND status_ts BETWEEN @start_date AND @end_date
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

### 1.3 Terminal Status Distribution

```sql
-- Terminal Status Distribution
-- Returns: Count and percentage for each terminal status

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

### 1.4 Daily Request Volume Trend

```sql
-- Daily Request Volume Trend (Last 30 Days)
-- Returns: Date, count, day-over-day change

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
          NULLIF(LAG(COUNT(*)) OVER (ORDER BY DATE(created_ts)), 0), 2) as pct_change,
    AVG(COUNT(*)) OVER (ORDER BY DATE(created_ts) ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d
FROM first_events
WHERE created_ts >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(created_ts)
ORDER BY request_date;
```

### 1.5 Hourly Request Volume (Last 7 Days)

```sql
-- Hourly Request Volume (Last 7 Days)
-- Use Case: Operational monitoring, identify peak hours

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
    EXTRACT(DOW FROM created_ts) as day_of_week,
    EXTRACT(HOUR FROM created_ts) as hour_of_day,
    ROUND(AVG(COUNT(*)) OVER (
        ORDER BY DATE_TRUNC('hour', created_ts)
        ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
    ), 2) as moving_avg_24h
FROM first_events
WHERE created_ts >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE_TRUNC('hour', created_ts)
ORDER BY request_hour;
```

---

## 2. Channel Performance

### 2.1 Success Rate by Channel

```sql
-- Success Rate by Channel
-- Returns: Performance breakdown for notification, QR, redirect

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
    SUM(CASE WHEN status_code = 'S42' THEN 1 ELSE 0 END) as expired,
    SUM(CASE WHEN status_code = 'S43' THEN 1 ELSE 0 END) as user_aborted,
    SUM(CASE WHEN status_code = 'S44' THEN 1 ELSE 0 END) as not_eligible,
    ROUND(100.0 * SUM(CASE WHEN status_code = 'S43' THEN 1 ELSE 0 END) / COUNT(*), 2) as abort_rate_pct
FROM final_statuses
GROUP BY channel
ORDER BY success_rate_pct DESC;
```

### 2.2 Notification Channel Funnel

```sql
-- Notification Channel Funnel
-- Returns: Step-by-step progression through notification flow

WITH request_statuses AS (
    SELECT
        request_id,
        MAX(CASE WHEN status_code = 'S00' THEN 1 ELSE 0 END) as reached_s00,
        MAX(CASE WHEN status_code = 'S01' THEN 1 ELSE 0 END) as reached_s01,
        MAX(CASE WHEN status_code = 'S02' THEN 1 ELSE 0 END) as reached_s02,
        MAX(CASE WHEN status_code = 'S03' THEN 1 ELSE 0 END) as reached_s03,
        MAX(CASE WHEN status_code = 'S08' THEN 1 ELSE 0 END) as reached_s08,
        MAX(CASE WHEN status_code IN ('S10','S11') THEN 1 ELSE 0 END) as reached_doc_check,
        MAX(CASE WHEN status_code = 'S20' THEN 1 ELSE 0 END) as reached_s20,
        MAX(CASE WHEN status_code = 'S21' THEN 1 ELSE 0 END) as reached_s21,
        MAX(CASE WHEN status_code = 'S30' THEN 1 ELSE 0 END) as reached_s30,
        MAX(CASE WHEN status_code = 'S31' THEN 1 ELSE 0 END) as reached_s31,
        MAX(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as reached_s40
    FROM sharing_transactions
    WHERE channel = 'notification'
    GROUP BY request_id
),
funnel_data AS (
    SELECT 1 as step, 'S00 - Request Created' as funnel_step, SUM(reached_s00) as requests FROM request_statuses
    UNION ALL SELECT 2, 'S01 - Notification Sent', SUM(reached_s01) FROM request_statuses
    UNION ALL SELECT 3, 'S03 - Notification Opened', SUM(reached_s03) FROM request_statuses
    UNION ALL SELECT 4, 'S08 - Request Viewed', SUM(reached_s08) FROM request_statuses
    UNION ALL SELECT 5, 'Document Check', SUM(reached_doc_check) FROM request_statuses
    UNION ALL SELECT 6, 'S20 - Consent Screen', SUM(reached_s20) FROM request_statuses
    UNION ALL SELECT 7, 'S21 - Consent Given', SUM(reached_s21) FROM request_statuses
    UNION ALL SELECT 8, 'S30 - PIN Screen', SUM(reached_s30) FROM request_statuses
    UNION ALL SELECT 9, 'S31 - PIN Verified', SUM(reached_s31) FROM request_statuses
    UNION ALL SELECT 10, 'S40 - Successfully Shared', SUM(reached_s40) FROM request_statuses
)
SELECT
    funnel_step,
    requests,
    ROUND(100.0 * requests / FIRST_VALUE(requests) OVER (ORDER BY step), 2) as pct_of_start,
    requests - LAG(requests) OVER (ORDER BY step) as drop_off,
    ROUND(100.0 * ABS(requests - LAG(requests) OVER (ORDER BY step)) /
          NULLIF(LAG(requests) OVER (ORDER BY step), 0), 2) as drop_off_pct
FROM funnel_data
ORDER BY step;
```

### 2.3 QR Channel Funnel

```sql
-- QR Channel Funnel
-- Returns: Step-by-step progression through QR scan flow

WITH request_statuses AS (
    SELECT
        request_id,
        MAX(CASE WHEN status_code = 'S00' THEN 1 ELSE 0 END) as reached_s00,
        MAX(CASE WHEN status_code = 'S06' THEN 1 ELSE 0 END) as reached_s06,
        MAX(CASE WHEN status_code = 'S07' THEN 1 ELSE 0 END) as reached_s07,
        MAX(CASE WHEN status_code = 'S08' THEN 1 ELSE 0 END) as reached_s08,
        MAX(CASE WHEN status_code IN ('S10','S11') THEN 1 ELSE 0 END) as reached_doc_check,
        MAX(CASE WHEN status_code = 'S20' THEN 1 ELSE 0 END) as reached_s20,
        MAX(CASE WHEN status_code = 'S21' THEN 1 ELSE 0 END) as reached_s21,
        MAX(CASE WHEN status_code = 'S30' THEN 1 ELSE 0 END) as reached_s30,
        MAX(CASE WHEN status_code = 'S31' THEN 1 ELSE 0 END) as reached_s31,
        MAX(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as reached_s40
    FROM sharing_transactions
    WHERE channel = 'qr'
    GROUP BY request_id
),
funnel_data AS (
    SELECT 1 as step, 'S00 - Request Created' as funnel_step, SUM(reached_s00) as requests FROM request_statuses
    UNION ALL SELECT 2, 'S06 - QR Scanned', SUM(reached_s06) FROM request_statuses
    UNION ALL SELECT 3, 'S07 - QR Verified', SUM(reached_s07) FROM request_statuses
    UNION ALL SELECT 4, 'S08 - Request Viewed', SUM(reached_s08) FROM request_statuses
    UNION ALL SELECT 5, 'Document Check', SUM(reached_doc_check) FROM request_statuses
    UNION ALL SELECT 6, 'S20 - Consent Screen', SUM(reached_s20) FROM request_statuses
    UNION ALL SELECT 7, 'S21 - Consent Given', SUM(reached_s21) FROM request_statuses
    UNION ALL SELECT 8, 'S30 - PIN Screen', SUM(reached_s30) FROM request_statuses
    UNION ALL SELECT 9, 'S31 - PIN Verified', SUM(reached_s31) FROM request_statuses
    UNION ALL SELECT 10, 'S40 - Successfully Shared', SUM(reached_s40) FROM request_statuses
)
SELECT
    funnel_step,
    requests,
    ROUND(100.0 * requests / FIRST_VALUE(requests) OVER (ORDER BY step), 2) as pct_of_start,
    requests - LAG(requests) OVER (ORDER BY step) as drop_off,
    ROUND(100.0 * ABS(requests - LAG(requests) OVER (ORDER BY step)) /
          NULLIF(LAG(requests) OVER (ORDER BY step), 0), 2) as drop_off_pct
FROM funnel_data
ORDER BY step;
```

### 2.4 Average Journey Time by Channel

```sql
-- Average Journey Time by Channel
-- Returns: Mean, median, and percentile journey durations

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
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as median_duration_seconds,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as p90_duration_seconds,
    ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as p95_duration_seconds,
    ROUND(MIN(EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as fastest_seconds,
    ROUND(MAX(EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as slowest_seconds
FROM request_timestamps
GROUP BY channel
ORDER BY avg_duration_seconds;
```

---

## 3. Status Flow & Funnel

### 3.1 Universal Journey Funnel (All Channels)

```sql
-- Universal Journey Funnel (All Channels Combined)
-- Returns: High-level funnel across all entry points

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
        MAX(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as reached_s40
    FROM sharing_transactions
    GROUP BY request_id
),
funnel_stages AS (
    SELECT 1 as stage_number, 'Request Created (S00)' as stage_name, SUM(reached_s00) as requests FROM request_progress
    UNION ALL SELECT 2, 'Channel Entry (S03/S05/S07)', SUM(reached_channel_entry) FROM request_progress
    UNION ALL SELECT 3, 'Request Viewed (S08)', SUM(reached_s08) FROM request_progress
    UNION ALL SELECT 4, 'Document Check (S10/S11)', SUM(reached_doc_check) FROM request_progress
    UNION ALL SELECT 5, 'Consent Screen (S20)', SUM(reached_s20) FROM request_progress
    UNION ALL SELECT 6, 'Consent Given (S21)', SUM(reached_s21) FROM request_progress
    UNION ALL SELECT 7, 'PIN Screen (S30)', SUM(reached_s30) FROM request_progress
    UNION ALL SELECT 8, 'PIN Verified (S31)', SUM(reached_s31) FROM request_progress
    UNION ALL SELECT 9, 'Successfully Shared (S40)', SUM(reached_s40) FROM request_progress
)
SELECT
    stage_number,
    stage_name,
    requests,
    ROUND(100.0 * requests / FIRST_VALUE(requests) OVER (ORDER BY stage_number), 2) as pct_of_start,
    requests - LAG(requests) OVER (ORDER BY stage_number) as drop_off,
    ROUND(100.0 * ABS(requests - LAG(requests) OVER (ORDER BY stage_number)) /
          NULLIF(LAG(requests) OVER (ORDER BY stage_number), 0), 2) as drop_off_pct
FROM funnel_stages
ORDER BY stage_number;
```

### 3.2 Status Transition Matrix

```sql
-- Status Transition Matrix
-- Returns: Count and percentage for each status-to-status transition

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

### 3.3 Most Common Successful Paths

```sql
-- Most Common Successful Paths (Simplified Milestones)
-- Returns: Top journey patterns for successful requests

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
        MAX(CASE WHEN st.status_code IN ('S12','S13') THEN 'DOC_RETRIEVAL' END) as doc_retrieval
    FROM sharing_transactions st
    INNER JOIN successful_requests sr ON st.request_id = sr.request_id
    GROUP BY st.request_id
),
journey_summary AS (
    SELECT
        st.request_id,
        CONCAT_WS(' → ',
            'S00',
            rm.channel_entry,
            'S08',
            rm.doc_status,
            CASE WHEN rm.doc_retrieval IS NOT NULL THEN rm.doc_retrieval END,
            'S20', 'S21', 'S30', 'S31', 'S40'
        ) as simplified_path,
        MAX(st.status_ts) - MIN(st.status_ts) as duration
    FROM request_milestones rm
    JOIN sharing_transactions st ON rm.request_id = st.request_id
    GROUP BY st.request_id, simplified_path
)
SELECT
    simplified_path,
    COUNT(*) as request_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as pct_of_successful,
    ROUND(AVG(EXTRACT(EPOCH FROM duration)), 2) as avg_duration_seconds,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM duration)), 2) as median_duration_seconds
FROM journey_summary
GROUP BY simplified_path
ORDER BY request_count DESC
LIMIT 20;
```

### 3.4 Most Common Failure Paths (Last Step Before Failure)

```sql
-- Most Common Failure Paths (Last Step Before Each Terminal Failure)
-- Returns: Where users drop off for each failure type

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

---

## 4. Error Analysis

### 4.1 Error Frequency by Error Code

```sql
-- Error Frequency by Error Code
-- Returns: Most common errors with impact analysis

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
    MAX(status_ts) as last_seen,
    DATEDIFF(day, MIN(status_ts), MAX(status_ts)) as days_active
FROM error_events
GROUP BY error_code, error_source
ORDER BY error_count DESC;
```

### 4.2 Error Impact Analysis (S41 Rate)

```sql
-- Error Impact Analysis: How many errors lead to S41?
-- Returns: Error codes with recovery vs failure rates

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
        MAX(CASE WHEN st.status_code = 'S40' THEN 1 ELSE 0 END) as ended_in_s40,
        MAX(CASE WHEN st.status_code = 'S43' THEN 1 ELSE 0 END) as ended_in_s43
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
    SUM(ended_in_s43) as user_aborted,
    ROUND(100.0 * SUM(ended_in_s41) / COUNT(*), 2) as s41_rate,
    ROUND(100.0 * SUM(ended_in_s40) / COUNT(*), 2) as recovery_rate,
    ROUND(100.0 * SUM(ended_in_s43) / COUNT(*), 2) as abort_rate
FROM request_outcomes
GROUP BY error_code, error_source
ORDER BY led_to_s41 DESC;
```

### 4.3 Error Source Distribution

```sql
-- Error Source Distribution
-- Returns: Errors grouped by responsible system

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

### 4.4 Error Rate by Service Provider

```sql
-- Error Rate by Service Provider
-- Returns: Which SPs experience most errors

WITH sp_requests AS (
    SELECT
        sp_id,
        COUNT(DISTINCT request_id) as total_requests
    FROM sharing_transactions
    GROUP BY sp_id
),
sp_errors AS (
    SELECT
        sp_id,
        COUNT(*) as error_count,
        COUNT(DISTINCT request_id) as requests_with_errors
    FROM sharing_transactions
    WHERE error_code IS NOT NULL
    GROUP BY sp_id
)
SELECT
    r.sp_id,
    r.total_requests,
    COALESCE(e.error_count, 0) as error_count,
    COALESCE(e.requests_with_errors, 0) as requests_with_errors,
    ROUND(100.0 * COALESCE(e.requests_with_errors, 0) / r.total_requests, 2) as error_rate_pct,
    ROUND(COALESCE(e.error_count, 0)::DECIMAL / r.total_requests, 2) as errors_per_request
FROM sp_requests r
LEFT JOIN sp_errors e ON r.sp_id = e.sp_id
WHERE r.total_requests >= 100  -- Filter low-volume SPs
ORDER BY error_rate_pct DESC;
```

### 4.5 Errors Over Time (Daily Trend)

```sql
-- Daily Error Trend
-- Returns: Error volume and rate over time

WITH daily_requests AS (
    SELECT
        DATE(status_ts) as request_date,
        COUNT(DISTINCT request_id) as total_requests
    FROM sharing_transactions
    WHERE status_ts >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY DATE(status_ts)
),
daily_errors AS (
    SELECT
        DATE(status_ts) as request_date,
        COUNT(*) as error_count,
        COUNT(DISTINCT request_id) as requests_with_errors
    FROM sharing_transactions
    WHERE error_code IS NOT NULL
      AND status_ts >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY DATE(status_ts)
)
SELECT
    r.request_date,
    r.total_requests,
    COALESCE(e.error_count, 0) as error_count,
    COALESCE(e.requests_with_errors, 0) as requests_with_errors,
    ROUND(100.0 * COALESCE(e.requests_with_errors, 0) / r.total_requests, 2) as error_rate_pct,
    ROUND(AVG(100.0 * COALESCE(e.requests_with_errors, 0) / r.total_requests)
          OVER (ORDER BY r.request_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) as moving_avg_7d
FROM daily_requests r
LEFT JOIN daily_errors e ON r.request_date = e.request_date
ORDER BY r.request_date;
```

---

## 5. Service Provider Performance

### 5.1 SP Success Rate Ranking

```sql
-- Service Provider Success Rate Ranking
-- Returns: Top and bottom performing SPs

WITH sp_terminal_requests AS (
    SELECT
        sp_id,
        request_id,
        status_code,
        status_ts,
        ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
    FROM sharing_transactions
    WHERE status_code IN ('S40', 'S41', 'S42', 'S43', 'S44')
),
sp_final_statuses AS (
    SELECT sp_id, request_id, status_code
    FROM sp_terminal_requests
    WHERE rn = 1
)
SELECT
    sp_id,
    COUNT(*) as total_requests,
    SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as successful_shares,
    ROUND(100.0 * SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate_pct,
    SUM(CASE WHEN status_code = 'S41' THEN 1 ELSE 0 END) as technical_failures,
    SUM(CASE WHEN status_code = 'S43' THEN 1 ELSE 0 END) as user_aborted,
    SUM(CASE WHEN status_code = 'S44' THEN 1 ELSE 0 END) as not_eligible,
    ROUND(100.0 * SUM(CASE WHEN status_code = 'S43' THEN 1 ELSE 0 END) / COUNT(*), 2) as abort_rate_pct
FROM sp_final_statuses
GROUP BY sp_id
HAVING COUNT(*) >= 100  -- Minimum volume threshold
ORDER BY success_rate_pct DESC;
```

### 5.2 SP Volume vs Performance Analysis

```sql
-- SP Volume vs Performance (Scatter Plot Data)
-- Returns: Volume and success rate for bubble chart

WITH sp_terminal_requests AS (
    SELECT
        sp_id,
        request_id,
        status_code,
        status_ts,
        ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
    FROM sharing_transactions
    WHERE status_code IN ('S40', 'S41', 'S42', 'S43', 'S44')
),
sp_final_statuses AS (
    SELECT sp_id, request_id, status_code
    FROM sp_terminal_requests
    WHERE rn = 1
),
sp_metrics AS (
    SELECT
        sp_id,
        COUNT(*) as total_requests,
        SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as successful_shares,
        ROUND(100.0 * SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate_pct
    FROM sp_final_statuses
    GROUP BY sp_id
    HAVING COUNT(*) >= 50
)
SELECT
    sp_id,
    total_requests,
    successful_shares,
    success_rate_pct,
    CASE
        WHEN total_requests >= 10000 THEN 'High Volume'
        WHEN total_requests >= 1000 THEN 'Medium Volume'
        ELSE 'Low Volume'
    END as volume_category,
    CASE
        WHEN success_rate_pct >= 75 THEN 'High Performance'
        WHEN success_rate_pct >= 60 THEN 'Medium Performance'
        ELSE 'Low Performance'
    END as performance_category
FROM sp_metrics
ORDER BY total_requests DESC;
```

### 5.3 SP Consent Conversion Rate

```sql
-- Service Provider Consent Conversion Rate
-- Returns: % of users who give consent after viewing for each SP

WITH sp_consent_flow AS (
    SELECT
        sp_id,
        request_id,
        MAX(CASE WHEN status_code = 'S20' THEN 1 ELSE 0 END) as reached_consent_screen,
        MAX(CASE WHEN status_code = 'S21' THEN 1 ELSE 0 END) as gave_consent
    FROM sharing_transactions
    GROUP BY sp_id, request_id
)
SELECT
    sp_id,
    SUM(reached_consent_screen) as reached_consent_screen,
    SUM(gave_consent) as gave_consent,
    ROUND(100.0 * SUM(gave_consent) / NULLIF(SUM(reached_consent_screen), 0), 2) as consent_conversion_pct,
    SUM(reached_consent_screen) - SUM(gave_consent) as consent_declined,
    ROUND(100.0 * (SUM(reached_consent_screen) - SUM(gave_consent)) /
          NULLIF(SUM(reached_consent_screen), 0), 2) as consent_decline_pct
FROM sp_consent_flow
WHERE reached_consent_screen > 0
GROUP BY sp_id
HAVING SUM(reached_consent_screen) >= 100  -- Minimum threshold
ORDER BY consent_conversion_pct DESC;
```

### 5.4 SP PIN Success Rate

```sql
-- Service Provider PIN Success Rate
-- Returns: % of users who successfully verify PIN for each SP

WITH sp_pin_flow AS (
    SELECT
        sp_id,
        request_id,
        MAX(CASE WHEN status_code = 'S30' THEN 1 ELSE 0 END) as reached_pin_screen,
        MAX(CASE WHEN status_code = 'S31' THEN 1 ELSE 0 END) as pin_verified,
        MAX(CASE WHEN status_code = 'S32' THEN 1 ELSE 0 END) as pin_failed
    FROM sharing_transactions
    GROUP BY sp_id, request_id
)
SELECT
    sp_id,
    SUM(reached_pin_screen) as reached_pin_screen,
    SUM(pin_verified) as pin_verified,
    SUM(pin_failed) as pin_failed_at_least_once,
    ROUND(100.0 * SUM(pin_verified) / NULLIF(SUM(reached_pin_screen), 0), 2) as pin_success_pct,
    ROUND(100.0 * SUM(pin_failed) / NULLIF(SUM(reached_pin_screen), 0), 2) as pin_failure_pct
FROM sp_pin_flow
WHERE reached_pin_screen > 0
GROUP BY sp_id
HAVING SUM(reached_pin_screen) >= 100  -- Minimum threshold
ORDER BY pin_success_pct DESC;
```

### 5.5 SP Document Availability Analysis

```sql
-- SP Document Availability Analysis
-- Returns: % of SP requests where users have required documents

WITH sp_doc_check AS (
    SELECT
        sp_id,
        request_id,
        MAX(CASE WHEN status_code = 'S10' THEN 1 ELSE 0 END) as docs_ready,
        MAX(CASE WHEN status_code = 'S11' THEN 1 ELSE 0 END) as docs_missing,
        MAX(CASE WHEN status_code IN ('S10','S11') THEN 1 ELSE 0 END) as reached_doc_check
    FROM sharing_transactions
    GROUP BY sp_id, request_id
)
SELECT
    sp_id,
    SUM(reached_doc_check) as requests_checked,
    SUM(docs_ready) as docs_available,
    SUM(docs_missing) as docs_missing,
    ROUND(100.0 * SUM(docs_ready) / NULLIF(SUM(reached_doc_check), 0), 2) as doc_availability_pct,
    ROUND(100.0 * SUM(docs_missing) / NULLIF(SUM(reached_doc_check), 0), 2) as doc_missing_pct
FROM sp_doc_check
WHERE reached_doc_check > 0
GROUP BY sp_id
HAVING SUM(reached_doc_check) >= 50
ORDER BY doc_missing_pct DESC;
```

---

## 6. User Behavior

### 6.1 Consent Conversion Rate (Overall)

```sql
-- Consent Conversion Rate (Overall)
-- Returns: % who give consent after reaching consent screen

WITH consent_flow AS (
    SELECT
        request_id,
        MAX(CASE WHEN status_code = 'S20' THEN 1 ELSE 0 END) as reached_s20,
        MAX(CASE WHEN status_code = 'S21' THEN 1 ELSE 0 END) as reached_s21
    FROM sharing_transactions
    GROUP BY request_id
)
SELECT
    SUM(reached_s20) as reached_consent_screen,
    SUM(reached_s21) as gave_consent,
    ROUND(100.0 * SUM(reached_s21) / NULLIF(SUM(reached_s20), 0), 2) as consent_conversion_pct,
    SUM(reached_s20) - SUM(reached_s21) as consent_declined_or_abandoned,
    ROUND(100.0 * (SUM(reached_s20) - SUM(reached_s21)) /
          NULLIF(SUM(reached_s20), 0), 2) as consent_decline_pct
FROM consent_flow
WHERE reached_s20 = 1;
```

### 6.2 PIN Success Rate (Overall)

```sql
-- PIN Success Rate (Overall)
-- Returns: % who successfully verify PIN

WITH pin_flow AS (
    SELECT
        request_id,
        MAX(CASE WHEN status_code = 'S30' THEN 1 ELSE 0 END) as reached_s30,
        MAX(CASE WHEN status_code = 'S31' THEN 1 ELSE 0 END) as reached_s31,
        MAX(CASE WHEN status_code = 'S32' THEN 1 ELSE 0 END) as had_pin_failure
    FROM sharing_transactions
    GROUP BY request_id
)
SELECT
    SUM(reached_s30) as reached_pin_screen,
    SUM(reached_s31) as pin_verified,
    SUM(had_pin_failure) as had_at_least_one_failure,
    ROUND(100.0 * SUM(reached_s31) / NULLIF(SUM(reached_s30), 0), 2) as pin_success_pct,
    SUM(reached_s30) - SUM(reached_s31) as pin_never_verified,
    ROUND(100.0 * (SUM(reached_s30) - SUM(reached_s31)) /
          NULLIF(SUM(reached_s30), 0), 2) as pin_failure_pct
FROM pin_flow
WHERE reached_s30 = 1;
```

### 6.3 User Abandonment Analysis (Where Do Users Quit?)

```sql
-- User Abandonment Analysis (S43 Breakdown)
-- Returns: At which stage users abandon (S43)

WITH abandoned_requests AS (
    SELECT
        request_id,
        previous_status as abandoned_at,
        status_ts as abandoned_ts
    FROM (
        SELECT
            request_id,
            status_code,
            previous_status,
            status_ts,
            ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
        FROM sharing_transactions
        WHERE status_code = 'S43'
    ) t
    WHERE rn = 1
)
SELECT
    abandoned_at,
    CASE
        WHEN abandoned_at IN ('S01','S02','S03') THEN 'Notification Flow'
        WHEN abandoned_at IN ('S06','S07') THEN 'QR Flow'
        WHEN abandoned_at = 'S08' THEN 'Initial View'
        WHEN abandoned_at IN ('S10','S11') THEN 'Document Check'
        WHEN abandoned_at = 'S20' THEN 'Consent Screen'
        WHEN abandoned_at = 'S21' THEN 'After Consent'
        WHEN abandoned_at = 'S30' THEN 'PIN Screen'
        WHEN abandoned_at = 'S31' THEN 'After PIN'
        ELSE 'Other'
    END as abandonment_stage,
    COUNT(*) as abandon_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as pct_of_total_abandons
FROM abandoned_requests
GROUP BY abandoned_at
ORDER BY abandon_count DESC;
```

### 6.4 Time Spent at Critical Stages

```sql
-- Time Spent at Critical Stages (Consent, PIN)
-- Returns: How long users take at decision points

WITH stage_latencies AS (
    SELECT
        request_id,
        status_code,
        previous_status,
        step_latency_ms / 1000.0 as step_latency_seconds
    FROM sharing_transactions
    WHERE previous_status IS NOT NULL
      AND step_latency_ms IS NOT NULL
      AND status_code IN ('S21', 'S31', 'S43')  -- Consent given, PIN verified, or abandoned
)
SELECT
    CASE
        WHEN status_code = 'S21' AND previous_status = 'S20' THEN 'Consent Screen → Consent Given'
        WHEN status_code = 'S31' AND previous_status = 'S30' THEN 'PIN Screen → PIN Verified'
        WHEN status_code = 'S43' AND previous_status = 'S20' THEN 'Consent Screen → Abandoned'
        WHEN status_code = 'S43' AND previous_status = 'S08' THEN 'Initial View → Abandoned'
    END as user_action,
    COUNT(*) as action_count,
    ROUND(AVG(step_latency_seconds), 2) as avg_time_seconds,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY step_latency_seconds), 2) as median_time_seconds,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY step_latency_seconds), 2) as p90_time_seconds,
    ROUND(MIN(step_latency_seconds), 2) as fastest_seconds,
    ROUND(MAX(step_latency_seconds), 2) as slowest_seconds
FROM stage_latencies
WHERE step_latency_seconds BETWEEN 1 AND 600  -- Filter unrealistic values
GROUP BY user_action
ORDER BY avg_time_seconds DESC;
```

---

## 7. Document Readiness

### 7.1 Document Ready vs Missing Distribution

```sql
-- Document Ready vs Missing Distribution
-- Returns: How many requests have all docs vs missing docs

WITH doc_check AS (
    SELECT
        request_id,
        MAX(CASE WHEN status_code = 'S10' THEN 1 ELSE 0 END) as docs_ready,
        MAX(CASE WHEN status_code = 'S11' THEN 1 ELSE 0 END) as docs_missing
    FROM sharing_transactions
    GROUP BY request_id
)
SELECT
    SUM(docs_ready) as requests_docs_ready,
    SUM(docs_missing) as requests_docs_missing,
    SUM(CASE WHEN docs_ready = 0 AND docs_missing = 0 THEN 1 ELSE 0 END) as never_reached_doc_check,
    ROUND(100.0 * SUM(docs_ready) / (SUM(docs_ready) + SUM(docs_missing)), 2) as doc_availability_pct,
    ROUND(100.0 * SUM(docs_missing) / (SUM(docs_ready) + SUM(docs_missing)), 2) as doc_missing_pct
FROM doc_check;
```

### 7.2 Success Rate: Docs Ready vs Docs Missing

```sql
-- Success Rate: Documents Ready vs Documents Missing
-- Returns: Completion rate comparison

WITH doc_status AS (
    SELECT
        request_id,
        MAX(CASE WHEN status_code = 'S10' THEN 1 ELSE 0 END) as docs_ready,
        MAX(CASE WHEN status_code = 'S11' THEN 1 ELSE 0 END) as docs_missing,
        MAX(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as shared_successfully
    FROM sharing_transactions
    GROUP BY request_id
)
SELECT
    CASE
        WHEN docs_ready = 1 THEN 'Documents Ready (S10)'
        WHEN docs_missing = 1 THEN 'Documents Missing (S11)'
        ELSE 'No Doc Check'
    END as document_status,
    COUNT(*) as total_requests,
    SUM(shared_successfully) as successful_shares,
    ROUND(100.0 * SUM(shared_successfully) / COUNT(*), 2) as success_rate_pct
FROM doc_status
GROUP BY document_status
ORDER BY success_rate_pct DESC;
```

### 7.3 Document Retrieval Success Rate

```sql
-- Document Retrieval Success Rate (S12 → S13)
-- Returns: How often missing doc retrieval succeeds

WITH doc_retrieval AS (
    SELECT
        request_id,
        MAX(CASE WHEN status_code = 'S12' THEN 1 ELSE 0 END) as attempted_retrieval,
        MAX(CASE WHEN status_code = 'S13' THEN 1 ELSE 0 END) as retrieval_succeeded,
        MAX(CASE WHEN status_code = 'S15' THEN 1 ELSE 0 END) as retrieval_failed
    FROM sharing_transactions
    GROUP BY request_id
)
SELECT
    SUM(attempted_retrieval) as attempted_retrieval,
    SUM(retrieval_succeeded) as retrieval_succeeded,
    SUM(retrieval_failed) as retrieval_failed,
    ROUND(100.0 * SUM(retrieval_succeeded) / NULLIF(SUM(attempted_retrieval), 0), 2) as retrieval_success_pct,
    ROUND(100.0 * SUM(retrieval_failed) / NULLIF(SUM(attempted_retrieval), 0), 2) as retrieval_failure_pct
FROM doc_retrieval
WHERE attempted_retrieval = 1;
```

### 7.4 Missing Document Count Distribution

```sql
-- Missing Document Count Distribution
-- Returns: How many docs are typically missing

WITH missing_docs AS (
    SELECT
        request_id,
        missing_count
    FROM (
        SELECT
            request_id,
            missing_count,
            ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
        FROM sharing_transactions
        WHERE status_code = 'S11'
          AND missing_count IS NOT NULL
    ) t
    WHERE rn = 1
)
SELECT
    missing_count,
    COUNT(*) as request_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage
FROM missing_docs
GROUP BY missing_count
ORDER BY missing_count;
```

---

## 8. Time & Latency

### 8.1 Average Journey Time to Success

```sql
-- Average Journey Time to Success (Overall)
-- Returns: Mean journey duration for successful requests

WITH successful_journeys AS (
    SELECT
        request_id,
        MIN(status_ts) as start_ts,
        MAX(CASE WHEN status_code = 'S40' THEN status_ts END) as success_ts
    FROM sharing_transactions
    GROUP BY request_id
    HAVING MAX(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) = 1
)
SELECT
    COUNT(*) as successful_requests,
    ROUND(AVG(EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as avg_duration_seconds,
    ROUND(AVG(EXTRACT(EPOCH FROM (success_ts - start_ts))) / 60, 2) as avg_duration_minutes,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as median_seconds,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as p90_seconds,
    ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as p95_seconds
FROM successful_journeys;
```

### 8.2 Step Latency Analysis (Average Time per Status)

```sql
-- Step Latency Analysis: Average time at each status
-- Returns: How long each step takes on average

SELECT
    previous_status,
    status_code,
    CASE
        WHEN previous_status = 'S20' AND status_code = 'S21' THEN 'User Consent Decision'
        WHEN previous_status = 'S30' AND status_code = 'S31' THEN 'PIN Entry'
        WHEN previous_status = 'S08' AND status_code = 'S10' THEN 'Document Check (Ready)'
        WHEN previous_status = 'S08' AND status_code = 'S11' THEN 'Document Check (Missing)'
        WHEN previous_status = 'S12' AND status_code = 'S13' THEN 'Document Retrieval'
        ELSE CONCAT(previous_status, ' → ', status_code)
    END as step_description,
    COUNT(*) as occurrence_count,
    ROUND(AVG(step_latency_ms) / 1000.0, 2) as avg_latency_seconds,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY step_latency_ms) / 1000.0, 2) as median_latency_seconds,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY step_latency_ms) / 1000.0, 2) as p90_latency_seconds
FROM sharing_transactions
WHERE previous_status IS NOT NULL
  AND step_latency_ms IS NOT NULL
  AND step_latency_ms BETWEEN 0 AND 600000  -- 0 to 10 minutes
GROUP BY previous_status, status_code
HAVING COUNT(*) >= 100
ORDER BY avg_latency_seconds DESC;
```

### 8.3 Bottleneck Identification (Slowest Steps)

```sql
-- Bottleneck Identification: Top 10 slowest steps
-- Returns: Steps with highest latency

WITH step_latencies AS (
    SELECT
        previous_status,
        status_code,
        step_latency_ms / 1000.0 as step_latency_seconds
    FROM sharing_transactions
    WHERE previous_status IS NOT NULL
      AND step_latency_ms IS NOT NULL
      AND step_latency_ms BETWEEN 1000 AND 600000  -- 1 sec to 10 min
)
SELECT
    CONCAT(previous_status, ' → ', status_code) as transition,
    COUNT(*) as occurrence_count,
    ROUND(AVG(step_latency_seconds), 2) as avg_latency_seconds,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY step_latency_seconds), 2) as p90_latency_seconds,
    CASE
        WHEN AVG(step_latency_seconds) > 30 THEN '🔴 Critical Bottleneck'
        WHEN AVG(step_latency_seconds) > 15 THEN '🟡 Moderate Bottleneck'
        ELSE '🟢 Normal'
    END as bottleneck_severity
FROM step_latencies
GROUP BY previous_status, status_code
HAVING COUNT(*) >= 100
ORDER BY avg_latency_seconds DESC
LIMIT 10;
```

### 8.4 Time-to-Failure Distribution

```sql
-- Time-to-Failure Distribution
-- Returns: How long before requests fail

WITH failed_journeys AS (
    SELECT
        request_id,
        status_code as failure_type,
        MIN(status_ts) as start_ts,
        MAX(status_ts) as failure_ts
    FROM sharing_transactions
    WHERE request_id IN (
        SELECT DISTINCT request_id
        FROM sharing_transactions
        WHERE status_code IN ('S41', 'S42', 'S43', 'S44')
    )
    GROUP BY request_id, status_code
    HAVING MAX(CASE WHEN status_code IN ('S41','S42','S43','S44') THEN 1 ELSE 0 END) = 1
)
SELECT
    failure_type,
    CASE
        WHEN failure_type = 'S41' THEN 'Technical Error'
        WHEN failure_type = 'S42' THEN 'Expired'
        WHEN failure_type = 'S43' THEN 'User Aborted'
        WHEN failure_type = 'S44' THEN 'Not Eligible'
    END as failure_description,
    COUNT(*) as failure_count,
    ROUND(AVG(EXTRACT(EPOCH FROM (failure_ts - start_ts))), 2) as avg_time_to_failure_seconds,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (failure_ts - start_ts))), 2) as median_seconds,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (failure_ts - start_ts))), 2) as p90_seconds
FROM failed_journeys
GROUP BY failure_type
ORDER BY failure_count DESC;
```

---

## 9. Platform Comparison

### 9.1 iOS vs Android Success Rate

```sql
-- iOS vs Android Success Rate Comparison

WITH platform_terminal_requests AS (
    SELECT
        platform,
        request_id,
        status_code,
        status_ts,
        ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
    FROM sharing_transactions
    WHERE status_code IN ('S40', 'S41', 'S42', 'S43', 'S44')
      AND platform IN ('ios', 'android')
),
platform_final_statuses AS (
    SELECT platform, request_id, status_code
    FROM platform_terminal_requests
    WHERE rn = 1
)
SELECT
    platform,
    COUNT(*) as total_requests,
    SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as successful_shares,
    ROUND(100.0 * SUM(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate_pct,
    SUM(CASE WHEN status_code = 'S41' THEN 1 ELSE 0 END) as technical_failures,
    SUM(CASE WHEN status_code = 'S43' THEN 1 ELSE 0 END) as user_aborted,
    ROUND(100.0 * SUM(CASE WHEN status_code = 'S41' THEN 1 ELSE 0 END) / COUNT(*), 2) as tech_failure_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN status_code = 'S43' THEN 1 ELSE 0 END) / COUNT(*), 2) as abort_rate_pct
FROM platform_final_statuses
GROUP BY platform
ORDER BY success_rate_pct DESC;
```

### 9.2 Platform Journey Time Comparison

```sql
-- Platform Journey Time Comparison

WITH platform_successful_journeys AS (
    SELECT
        platform,
        request_id,
        MIN(status_ts) as start_ts,
        MAX(CASE WHEN status_code = 'S40' THEN status_ts END) as success_ts
    FROM sharing_transactions
    WHERE platform IN ('ios', 'android')
    GROUP BY platform, request_id
    HAVING MAX(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) = 1
)
SELECT
    platform,
    COUNT(*) as successful_requests,
    ROUND(AVG(EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as avg_duration_seconds,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as median_seconds,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (success_ts - start_ts))), 2) as p90_seconds
FROM platform_successful_journeys
GROUP BY platform
ORDER BY avg_duration_seconds;
```

### 9.3 Platform Error Rate Comparison

```sql
-- Platform Error Rate Comparison

WITH platform_requests AS (
    SELECT
        platform,
        COUNT(DISTINCT request_id) as total_requests
    FROM sharing_transactions
    WHERE platform IN ('ios', 'android')
    GROUP BY platform
),
platform_errors AS (
    SELECT
        platform,
        COUNT(*) as error_count,
        COUNT(DISTINCT request_id) as requests_with_errors
    FROM sharing_transactions
    WHERE error_code IS NOT NULL
      AND platform IN ('ios', 'android')
    GROUP BY platform
)
SELECT
    r.platform,
    r.total_requests,
    COALESCE(e.error_count, 0) as error_count,
    COALESCE(e.requests_with_errors, 0) as requests_with_errors,
    ROUND(100.0 * COALESCE(e.requests_with_errors, 0) / r.total_requests, 2) as error_rate_pct
FROM platform_requests r
LEFT JOIN platform_errors e ON r.platform = e.platform
ORDER BY error_rate_pct DESC;
```

### 9.4 Platform Funnel Comparison

```sql
-- Platform Funnel Comparison (Side-by-Side)

WITH platform_progress AS (
    SELECT
        platform,
        request_id,
        MAX(CASE WHEN status_code = 'S00' THEN 1 ELSE 0 END) as reached_s00,
        MAX(CASE WHEN status_code = 'S08' THEN 1 ELSE 0 END) as reached_s08,
        MAX(CASE WHEN status_code = 'S20' THEN 1 ELSE 0 END) as reached_s20,
        MAX(CASE WHEN status_code = 'S21' THEN 1 ELSE 0 END) as reached_s21,
        MAX(CASE WHEN status_code = 'S30' THEN 1 ELSE 0 END) as reached_s30,
        MAX(CASE WHEN status_code = 'S31' THEN 1 ELSE 0 END) as reached_s31,
        MAX(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as reached_s40
    FROM sharing_transactions
    WHERE platform IN ('ios', 'android')
    GROUP BY platform, request_id
)
SELECT
    platform,
    SUM(reached_s00) as s00_created,
    ROUND(100.0 * SUM(reached_s00) / SUM(reached_s00), 2) as s00_pct,
    SUM(reached_s08) as s08_viewed,
    ROUND(100.0 * SUM(reached_s08) / SUM(reached_s00), 2) as s08_pct,
    SUM(reached_s20) as s20_consent_screen,
    ROUND(100.0 * SUM(reached_s20) / SUM(reached_s00), 2) as s20_pct,
    SUM(reached_s21) as s21_consent_given,
    ROUND(100.0 * SUM(reached_s21) / SUM(reached_s00), 2) as s21_pct,
    SUM(reached_s30) as s30_pin_screen,
    ROUND(100.0 * SUM(reached_s30) / SUM(reached_s00), 2) as s30_pct,
    SUM(reached_s31) as s31_pin_verified,
    ROUND(100.0 * SUM(reached_s31) / SUM(reached_s00), 2) as s31_pct,
    SUM(reached_s40) as s40_success,
    ROUND(100.0 * SUM(reached_s40) / SUM(reached_s00), 2) as s40_pct
FROM platform_progress
GROUP BY platform
ORDER BY platform;
```

---

## 10. Advanced Analytics

### 10.1 Cohort Analysis (Requests by Creation Date)

```sql
-- Cohort Analysis: Track request cohorts over time
-- Returns: Success rate by creation date cohort

WITH request_cohort AS (
    SELECT
        DATE(MIN(status_ts)) as cohort_date,
        request_id
    FROM sharing_transactions
    GROUP BY request_id
),
cohort_outcomes AS (
    SELECT
        rc.cohort_date,
        rc.request_id,
        MAX(CASE WHEN st.status_code = 'S40' THEN 1 ELSE 0 END) as succeeded,
        MAX(CASE WHEN st.status_code IN ('S40','S41','S42','S43','S44') THEN 1 ELSE 0 END) as terminal
    FROM request_cohort rc
    JOIN sharing_transactions st ON rc.request_id = st.request_id
    GROUP BY rc.cohort_date, rc.request_id
)
SELECT
    cohort_date,
    COUNT(*) as total_requests,
    SUM(terminal) as completed_requests,
    SUM(succeeded) as successful_requests,
    ROUND(100.0 * SUM(succeeded) / NULLIF(SUM(terminal), 0), 2) as success_rate_pct,
    ROUND(100.0 * SUM(terminal) / COUNT(*), 2) as completion_rate_pct
FROM cohort_outcomes
WHERE cohort_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY cohort_date
ORDER BY cohort_date;
```

### 10.2 User Segment Performance (by Document Count)

```sql
-- User Segment Performance by Required Document Count
-- Returns: Success rate based on complexity (# of docs)

WITH request_complexity AS (
    SELECT
        request_id,
        required_count,
        MAX(CASE WHEN status_code = 'S40' THEN 1 ELSE 0 END) as succeeded,
        MAX(CASE WHEN status_code IN ('S40','S41','S42','S43','S44') THEN 1 ELSE 0 END) as terminal
    FROM sharing_transactions
    WHERE required_count IS NOT NULL
    GROUP BY request_id, required_count
)
SELECT
    required_count as num_documents_required,
    COUNT(*) as total_requests,
    SUM(terminal) as completed_requests,
    SUM(succeeded) as successful_requests,
    ROUND(100.0 * SUM(succeeded) / NULLIF(SUM(terminal), 0), 2) as success_rate_pct
FROM request_complexity
WHERE terminal = 1
GROUP BY required_count
ORDER BY required_count;
```

### 10.3 Anomaly Detection (Unusual Patterns)

```sql
-- Anomaly Detection: Requests with unusual journey patterns
-- Returns: Requests that deviate from normal flow

WITH request_journey_stats AS (
    SELECT
        request_id,
        channel,
        platform,
        sp_id,
        COUNT(*) as total_status_events,
        COUNT(DISTINCT status_code) as unique_statuses,
        MAX(status_ts) - MIN(status_ts) as total_duration,
        SUM(CASE WHEN error_code IS NOT NULL THEN 1 ELSE 0 END) as error_count,
        MAX(CASE WHEN status_code = 'S32' THEN 1 ELSE 0 END) as had_pin_failure
    FROM sharing_transactions
    GROUP BY request_id, channel, platform, sp_id
)
SELECT
    request_id,
    channel,
    platform,
    sp_id,
    total_status_events,
    unique_statuses,
    EXTRACT(EPOCH FROM total_duration) as total_duration_seconds,
    error_count,
    CASE
        WHEN total_status_events > 20 THEN '🔴 Too Many Steps'
        WHEN EXTRACT(EPOCH FROM total_duration) > 1800 THEN '🔴 Took Too Long (>30min)'
        WHEN error_count >= 3 THEN '🔴 Multiple Errors'
        WHEN had_pin_failure = 1 THEN '🟡 PIN Retry'
        ELSE '🟢 Normal'
    END as anomaly_flag
FROM request_journey_stats
WHERE total_status_events > 20
   OR EXTRACT(EPOCH FROM total_duration) > 1800
   OR error_count >= 3
ORDER BY total_status_events DESC, total_duration DESC
LIMIT 100;
```

### 10.4 Predictive Failure Risk Score

```sql
-- Predictive Failure Risk Score
-- Returns: Requests with high likelihood of failure based on early signals

WITH request_early_signals AS (
    SELECT
        request_id,
        channel,
        platform,
        sp_id,
        required_count,
        MAX(CASE WHEN status_code = 'S11' THEN 1 ELSE 0 END) as docs_missing,
        MAX(CASE WHEN status_code = 'S32' THEN 1 ELSE 0 END) as pin_failed,
        COUNT(CASE WHEN error_code IS NOT NULL THEN 1 END) as early_error_count,
        MAX(CASE WHEN status_code IN ('S40','S41','S42','S43','S44') THEN 1 ELSE 0 END) as is_terminal
    FROM sharing_transactions
    GROUP BY request_id, channel, platform, sp_id, required_count
)
SELECT
    request_id,
    channel,
    platform,
    sp_id,
    required_count,
    (
        (CASE WHEN docs_missing = 1 THEN 40 ELSE 0 END) +
        (CASE WHEN pin_failed = 1 THEN 25 ELSE 0 END) +
        (CASE WHEN channel = 'redirect' THEN 15 ELSE 0 END) +
        (CASE WHEN platform = 'android' THEN 10 ELSE 0 END) +
        (early_error_count * 10) +
        (CASE WHEN required_count > 2 THEN 10 ELSE 0 END)
    ) as risk_score,
    CASE
        WHEN (
            (CASE WHEN docs_missing = 1 THEN 40 ELSE 0 END) +
            (CASE WHEN pin_failed = 1 THEN 25 ELSE 0 END) +
            (CASE WHEN channel = 'redirect' THEN 15 ELSE 0 END) +
            (CASE WHEN platform = 'android' THEN 10 ELSE 0 END) +
            (early_error_count * 10) +
            (CASE WHEN required_count > 2 THEN 10 ELSE 0 END)
        ) >= 50 THEN 'High Risk'
        WHEN (
            (CASE WHEN docs_missing = 1 THEN 40 ELSE 0 END) +
            (CASE WHEN pin_failed = 1 THEN 25 ELSE 0 END) +
            (CASE WHEN channel = 'redirect' THEN 15 ELSE 0 END) +
            (CASE WHEN platform = 'android' THEN 10 ELSE 0 END) +
            (early_error_count * 10) +
            (CASE WHEN required_count > 2 THEN 10 ELSE 0 END)
        ) >= 25 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as risk_category
FROM request_early_signals
WHERE is_terminal = 0  -- Only in-progress requests
ORDER BY risk_score DESC;
```

---

## Query Performance Optimization Tips

### Indexes to Create

```sql
-- Recommended indexes for query performance

CREATE INDEX idx_status_code ON sharing_transactions(status_code);
CREATE INDEX idx_request_id ON sharing_transactions(request_id);
CREATE INDEX idx_status_ts ON sharing_transactions(status_ts);
CREATE INDEX idx_channel ON sharing_transactions(channel);
CREATE INDEX idx_platform ON sharing_transactions(platform);
CREATE INDEX idx_sp_id ON sharing_transactions(sp_id);
CREATE INDEX idx_error_code ON sharing_transactions(error_code);
CREATE INDEX idx_error_source ON sharing_transactions(error_source);

-- Composite indexes for common filters
CREATE INDEX idx_status_ts_code ON sharing_transactions(status_ts, status_code);
CREATE INDEX idx_request_status ON sharing_transactions(request_id, status_code, status_ts);
CREATE INDEX idx_channel_platform ON sharing_transactions(channel, platform);
```

### Materialized Views for Heavy Queries

```sql
-- Materialized view for terminal request summary (refresh hourly)

CREATE MATERIALIZED VIEW mv_terminal_request_summary AS
WITH terminal_requests AS (
    SELECT
        request_id,
        status_code,
        status_ts,
        channel,
        platform,
        sp_id,
        ROW_NUMBER() OVER (PARTITION BY request_id ORDER BY status_ts DESC) as rn
    FROM sharing_transactions
    WHERE status_code IN ('S40', 'S41', 'S42', 'S43', 'S44')
)
SELECT
    request_id,
    status_code as final_status,
    status_ts as completed_ts,
    channel,
    platform,
    sp_id
FROM terminal_requests
WHERE rn = 1;

CREATE INDEX idx_mv_final_status ON mv_terminal_request_summary(final_status);
CREATE INDEX idx_mv_sp_id ON mv_terminal_request_summary(sp_id);

-- Refresh hourly
-- REFRESH MATERIALIZED VIEW mv_terminal_request_summary;
```

---

## Parameter Placeholders

When adapting these queries for BI tools or applications, replace these placeholders:

- `@start_date` → Start date filter (e.g., '2025-11-01')
- `@end_date` → End date filter (e.g., '2025-11-30')
- `@sp_id` → Service Provider ID filter
- `@channel` → Channel filter ('notification', 'qr', 'redirect')
- `@platform` → Platform filter ('ios', 'android')
- `@min_volume` → Minimum request threshold for filtering low-volume segments

---

**End of SQL Query Templates**
**Total Queries: 50+**
**Ready for Copy-Paste Implementation**
