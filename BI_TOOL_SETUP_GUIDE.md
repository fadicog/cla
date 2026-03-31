# BI Tool Setup Guide: UAE PASS Document Sharing Analytics
**Version:** 1.0
**Last Updated:** 2026-01-09
**Purpose:** Step-by-step guides for implementing dashboards in Tableau, Power BI, Looker, and other BI platforms

---

## Table of Contents

1. [Data Connection Setup](#1-data-connection-setup)
2. [Tableau Implementation](#2-tableau-implementation)
3. [Power BI Implementation](#3-power-bi-implementation)
4. [Looker/Looker Studio Implementation](#4-lookerlooker-studio-implementation)
5. [Metabase Implementation](#5-metabase-implementation)
6. [Dashboard Design Best Practices](#6-dashboard-design-best-practices)
7. [Refresh Schedules](#7-refresh-schedules)
8. [Performance Optimization](#8-performance-optimization)

---

## 1. Data Connection Setup

### Database Connection Parameters

```
Connection Type: PostgreSQL (or your database type)
Host: your-database-host.com
Port: 5432
Database: uaepass_analytics
Schema: public
Table: sharing_transactions

Authentication:
  Username: [read-only user recommended]
  Password: [secure credential]
  SSL: Enabled (required)
```

### Required Permissions

```sql
-- Grant read-only access to analytics user
GRANT SELECT ON sharing_transactions TO analytics_user;
GRANT SELECT ON mv_terminal_request_summary TO analytics_user;
```

### Data Source Configuration

**Recommended Approach:**
1. **Option A (Live Connection):** Connect directly to database for real-time data
2. **Option B (Extract/Cache):** Create scheduled extracts for better performance
3. **Option C (Hybrid):** Use materialized views for heavy aggregations, live for detailed drill-downs

**Extract Configuration (if using extracts):**
- **Frequency:** Hourly for operational dashboards, daily for executive dashboards
- **Incremental Refresh:** Filter to last 7 days for faster updates
- **Full Refresh:** Weekly on weekends

---

## 2. Tableau Implementation

### 2.1 Data Source Setup

**Step 1: Connect to Database**
1. Open Tableau Desktop
2. Click "Connect to Data" → "PostgreSQL" (or your DB type)
3. Enter connection details (host, database, credentials)
4. Click "Sign In"

**Step 2: Select Table**
1. Drag `sharing_transactions` to the canvas
2. Click "Update Now" to preview data

**Step 3: Create Data Extract (Optional)**
1. Click "Extract" radio button (top right)
2. Click "Edit" to configure:
   - **Incremental Refresh:** Yes
   - **Refresh Field:** `status_ts`
   - **Filters:** `status_ts >= TODAY() - 7` (for incremental)
3. Click "OK"

### 2.2 Create Calculated Fields

**Terminal Status Flag:**
```tableau
// Terminal Status Flag
IF [Status Code] IN ('S40', 'S41', 'S42', 'S43', 'S44')
THEN [Status Code]
ELSE NULL
END
```

**Success Flag:**
```tableau
// Success Flag
[Status Code] = 'S40'
```

**Final Status per Request:**
```tableau
// Final Status (LOD Expression)
{ FIXED [Request Id]:
  MAX(IF [Status Code] IN ('S40','S41','S42','S43','S44')
      THEN [Status Code] END)
}
```

**Journey Duration (Seconds):**
```tableau
// Journey Duration
{ FIXED [Request Id]:
  DATEDIFF('second',
    MIN([Status Ts]),
    MAX(IF [Status Code]='S40' THEN [Status Ts] END))
}
```

**Document Status:**
```tableau
// Document Status
{ FIXED [Request Id]:
  MAX(IF [Status Code] = 'S10' THEN 'Docs Ready'
      ELSEIF [Status Code] = 'S11' THEN 'Docs Missing'
      ELSE 'No Check' END)
}
```

### 2.3 Create Parameters

**Date Range Parameter:**
1. Create Parameter: `Date Range Selection`
2. Data Type: String
3. Allowable Values: List
   - "Last 7 Days"
   - "Last 30 Days"
   - "This Month"
   - "Last Month"
   - "Custom"

**Date Filter Calculated Field:**
```tableau
// Date Filter
CASE [Date Range Selection]
  WHEN 'Last 7 Days' THEN [Status Ts] >= DATEADD('day', -7, TODAY())
  WHEN 'Last 30 Days' THEN [Status Ts] >= DATEADD('day', -30, TODAY())
  WHEN 'This Month' THEN MONTH([Status Ts]) = MONTH(TODAY())
  WHEN 'Last Month' THEN MONTH([Status Ts]) = MONTH(DATEADD('month', -1, TODAY()))
  ELSE TRUE
END
```

### 2.4 Dashboard Layout: Executive Overview

**Dashboard Size:** 1920 × 1080 (Full HD)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ UAE PASS Document Sharing - Executive Dashboard             │
│ [Date Range: Last 30 Days ▼]  [Platform: All ▼]            │
├──────────────┬──────────────┬──────────────┬───────────────┤
│  Total       │  Success     │  Success     │  Avg Journey  │
│  Requests    │  Count       │  Rate        │  Time         │
│  350,802     │  236,426     │  67.4%       │  2.4 min      │
│  +7.2% ↑     │  +8.1% ↑     │  +0.8% ↑     │  -0.3 min ↓   │
├──────────────┴──────────────┴──────────────┴───────────────┤
│ Terminal Status Distribution              │  Trend (7d MA) │
│ ┌────────────────────────────┐           │  ┌────────────┐ │
│ │ [Pie Chart]                │           │  │ [Line]     │ │
│ │ - S40: 67.4%              │           │  │ Success %  │ │
│ │ - S43: 17.8%              │           │  │            │ │
│ │ - S42: 7.3%               │           │  └────────────┘ │
│ └────────────────────────────┘           │                 │
├──────────────────────────────────────────┴─────────────────┤
│ Funnel Analysis                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ S00: 350K ████████████████████████████████████ 100%    │ │
│ │ S08: 311K ██████████████████████████████ 88.7%         │ │
│ │ S20: 270K ███████████████████████ 77.1%                │ │
│ │ S21: 258K ██████████████████████ 73.7%                 │ │
│ │ S40: 236K ████████████████████ 67.4%                   │ │
│ └─────────────────────────────────────────────────────────┘ │
├──────────────────────────────┬──────────────────────────────┤
│ Channel Performance          │ Platform Performance         │
│ ┌──────────────────────────┐ │ ┌──────────────────────────┐ │
│ │ [Grouped Bar]            │ │ │ [Bar Chart]              │ │
│ │ Notification: 72.5%      │ │ │ iOS: 77.8%               │ │
│ │ QR: 59.1%                │ │ │ Android: 67.7%           │ │
│ │ Redirect: 33.8%          │ │ └──────────────────────────┘ │
│ └──────────────────────────┘ │                              │
└──────────────────────────────┴──────────────────────────────┘
```

**Implementation Steps:**

1. **Create Metric Tiles (BANs - Big Ass Numbers):**
   - Drag "Request ID" to Text → Change to CNT(DISTINCT)
   - Format: Number (Custom) → `#,##0`
   - Add KPI indicator: Create calculated field for YoY/MoM change
   - Use ▲/▼ Unicode characters for trend arrows

2. **Create Pie Chart (Terminal Status):**
   - Drag "Final Status" to Color
   - Drag "CNT(Request ID)" to Angle
   - Right-click chart → Add → Reference Line → "Total" label

3. **Create Funnel Chart:**
   - Create calculated fields for each stage count
   - Use horizontal bar chart
   - Sort descending
   - Add % labels

4. **Create Trend Line:**
   - Drag "Status Ts" to Columns → Change to DAY(continuous)
   - Drag "Success Rate" calculated field to Rows
   - Add trend line: Analytics → Trend Line → Show Trend Line
   - Add 7-day moving average: Quick Table Calc → Moving Average (7)

5. **Add Filters:**
   - Create filter for "Channel" → Show as dropdown
   - Create filter for "Platform" → Show as dropdown
   - Create filter for "SP ID" → Show as search box
   - Apply filters to all sheets in dashboard

### 2.5 Dashboard: Operational Monitoring

**Purpose:** Real-time monitoring for operations team

**Key Visualizations:**

1. **Error Rate Over Time (Last 24 Hours):**
   - Line chart with hourly granularity
   - Y-axis: Error %
   - Reference line at 5% (alert threshold)
   - Color: Red if >5%, Green if ≤5%

2. **Top 10 Errors (Live):**
   - Bar chart
   - X-axis: Error count
   - Y-axis: Error code
   - Sort descending

3. **SP Performance Heatmap:**
   - Rows: Service Provider
   - Columns: Date (Day)
   - Color: Success Rate (diverging red-yellow-green)
   - Filter: Last 30 days

4. **Alert Table:**
   - Show requests with anomalies (>20 steps, >30 min duration, >3 errors)
   - Columns: Request ID, SP, Duration, Error Count, Current Status
   - Conditional formatting: Red for critical issues

**Refresh Frequency:** Every 5 minutes (live connection or extract)

### 2.6 Dashboard Actions

**Action 1: Drill-Down to Request Details**
1. Dashboard → Actions → Add Action → Filter
2. Source: Any chart
3. Target: Detail table sheet
4. Run On: Select
5. Clearing Selection: Show all values

**Action 2: Highlight Related Data**
1. Dashboard → Actions → Add Action → Highlight
2. Source: Terminal Status pie chart
3. Target: All sheets
4. Run On: Hover

**Action 3: URL Action (Open Request in Admin Panel)**
1. Dashboard → Actions → Add Action → URL
2. URL: `https://admin.uaepass.ae/requests/<Request ID>`
3. Run On: Menu (right-click)

### 2.7 Publishing to Tableau Server

**Step 1: Publish Workbook**
1. File → Publish Workbook → Tableau Server
2. Enter server URL and credentials
3. Select project/folder
4. Set permissions (Viewer, Interactor, Editor)

**Step 2: Schedule Extract Refresh**
1. On Tableau Server, navigate to published workbook
2. Click "..." → Schedule Extract Refresh
3. Set schedule: Hourly (Mon-Sun, 8am-8pm)
4. Incremental: Yes
5. Full refresh: Weekly (Sunday 2am)

**Step 3: Configure Alerts**
1. Create calculated field: `[Success Rate] < 0.65` (alert if <65%)
2. Right-click metric → Create Alert
3. Set threshold and recipients
4. Frequency: Hourly

---

## 3. Power BI Implementation

### 3.1 Data Connection

**Step 1: Connect to Database**
1. Open Power BI Desktop
2. Home → Get Data → PostgreSQL (or your DB)
3. Server: `your-database-host.com:5432`
4. Database: `uaepass_analytics`
5. Click "OK"
6. Select `sharing_transactions` table
7. Click "Load" (or "Transform Data" to edit first)

**Step 2: Configure Query (Power Query)**
1. Home → Transform Data
2. Add custom column for "Is Terminal":
   ```powerquery
   if List.Contains({"S40","S41","S42","S43","S44"}, [status_code])
   then [status_code] else null
   ```
3. Add custom column for "Is Success":
   ```powerquery
   if [status_code] = "S40" then 1 else 0
   ```
4. Change data types:
   - `status_ts` → Date/Time
   - `step_latency_ms` → Whole Number
   - `required_count` → Whole Number
5. Close & Apply

### 3.2 Create DAX Measures

**Total Requests:**
```dax
Total Requests = DISTINCTCOUNT(sharing_transactions[request_id])
```

**Success Count:**
```dax
Success Count =
CALCULATE(
    DISTINCTCOUNT(sharing_transactions[request_id]),
    sharing_transactions[status_code] = "S40"
)
```

**Success Rate:**
```dax
Success Rate % =
DIVIDE(
    [Success Count],
    CALCULATE(
        DISTINCTCOUNT(sharing_transactions[request_id]),
        sharing_transactions[status_code] IN {"S40","S41","S42","S43","S44"}
    ),
    0
) * 100
```

**Consent Conversion:**
```dax
Consent Conversion % =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(sharing_transactions[request_id]),
        sharing_transactions[status_code] = "S21"
    ),
    CALCULATE(
        DISTINCTCOUNT(sharing_transactions[request_id]),
        sharing_transactions[status_code] = "S20"
    ),
    0
) * 100
```

**Average Journey Time:**
```dax
Avg Journey Time (sec) =
AVERAGEX(
    FILTER(
        SUMMARIZE(
            sharing_transactions,
            sharing_transactions[request_id],
            "Start", MIN(sharing_transactions[status_ts]),
            "End", CALCULATE(MAX(sharing_transactions[status_ts]),
                   sharing_transactions[status_code] = "S40")
        ),
        NOT(ISBLANK([End]))
    ),
    DATEDIFF([Start], [End], SECOND)
)
```

**Final Status (Calculated Column):**
```dax
Final Status =
CALCULATE(
    MAX(sharing_transactions[status_code]),
    FILTER(
        sharing_transactions,
        sharing_transactions[request_id] = EARLIER(sharing_transactions[request_id]) &&
        sharing_transactions[status_code] IN {"S40","S41","S42","S43","S44"}
    ),
    ALLEXCEPT(sharing_transactions, sharing_transactions[request_id])
)
```

**Previous Period Success Rate (for comparison):**
```dax
Success Rate % PP =
CALCULATE(
    [Success Rate %],
    DATEADD('Date'[Date], -1, MONTH)  // Compare to previous month
)
```

**Success Rate Change:**
```dax
Success Rate Change =
[Success Rate %] - [Success Rate % PP]
```

### 3.3 Create Date Table

```dax
Date =
ADDCOLUMNS(
    CALENDAR(DATE(2025, 1, 1), DATE(2026, 12, 31)),
    "Year", YEAR([Date]),
    "Month", FORMAT([Date], "MMM YYYY"),
    "Month Number", MONTH([Date]),
    "Quarter", "Q" & QUARTER([Date]),
    "Day of Week", FORMAT([Date], "ddd"),
    "Day Number", DAY([Date]),
    "Week Number", WEEKNUM([Date])
)
```

**Create Relationship:**
1. Model view → Drag `Date[Date]` to `sharing_transactions[status_ts]`
2. Cardinality: Many to One (Date is on "One" side)
3. Cross-filter direction: Single

### 3.4 Dashboard Layout: Executive Report

**Page 1: Overview**

**Visuals:**

1. **Card Visuals (Top Row):**
   - Total Requests: `[Total Requests]`
   - Success Count: `[Success Count]`
   - Success Rate: `[Success Rate %]` (format as %)
   - Avg Journey Time: `[Avg Journey Time (sec)]` / 60 (display in minutes)

2. **Line Chart (Success Rate Trend):**
   - X-axis: `Date[Date]` (day level)
   - Y-axis: `[Success Rate %]`
   - Add constant line at 75% (target)
   - Add analytics → Trend line

3. **Donut Chart (Terminal Status Distribution):**
   - Legend: `Final Status`
   - Values: `DISTINCTCOUNT(request_id)`
   - Data labels: Category, Percentage

4. **Funnel Chart (Conversion Funnel):**
   - Group: Stage name
   - Values: Count of requests reaching each stage
   - Stages: S00, S08, S20, S21, S30, S31, S40

5. **Clustered Bar Chart (Channel Performance):**
   - Y-axis: `channel`
   - X-axis: `[Success Rate %]`
   - Color by channel
   - Sort descending

6. **Table (Top SPs):**
   - Columns: SP ID, Total Requests, Success Rate %
   - Sort by Total Requests descending
   - Conditional formatting: Color scale on Success Rate

**Page 2: Error Analysis**

1. **Line and Stacked Column Chart (Errors Over Time):**
   - X-axis: Date
   - Column Y-axis: Error Count
   - Line Y-axis: Error Rate %

2. **Matrix (Error Source × Error Code):**
   - Rows: `error_source`
   - Columns: `error_code`
   - Values: `COUNT(status_code)`
   - Conditional formatting: Heatmap

3. **Bar Chart (Top 10 Errors):**
   - Y-axis: `error_code`
   - X-axis: `COUNT(DISTINCT request_id)`
   - Top N filter: 10

### 3.5 Slicers (Filters)

**Add Slicers:**
1. Insert → Slicer
2. Field: `Date[Month]` → Style: Dropdown
3. Field: `channel` → Style: List (vertical)
4. Field: `platform` → Style: Buttons (horizontal)
5. Field: `sp_id` → Style: Dropdown with search

**Apply to Pages:**
- Edit interactions: Click slicer → Format → Edit interactions
- Disable filters for KPIs if you want all-time totals

### 3.6 Publishing to Power BI Service

**Step 1: Publish Report**
1. Home → Publish
2. Select workspace (create if needed)
3. Click "Select"

**Step 2: Configure Data Refresh**
1. In Power BI Service, go to Workspace
2. Find dataset → Click "..." → Settings
3. Data source credentials → Edit credentials → Enter DB credentials
4. Scheduled refresh:
   - Frequency: Daily
   - Time: 2:00 AM
   - Timezone: UTC+4 (UAE)
   - Send failure notification: Yes
5. Save

**Step 3: Create Dashboard**
1. Open published report
2. Pin visuals to new dashboard: Hover over visual → Pin icon
3. Name dashboard: "Document Sharing - Executive"

**Step 4: Set Up Alerts**
1. Pin "Success Rate" card to dashboard
2. In dashboard, click "..." on card → Manage alerts
3. Add alert: If "Success Rate %" goes below 65
4. Email notification: Yes
5. Frequency: At most once per hour

### 3.7 Row-Level Security (RLS)

**If SPs should only see their own data:**

```dax
[sp_id] = USERPRINCIPALNAME()
```

**Or for specific users:**
```dax
[sp_id] = "Botim" && USERPRINCIPALNAME() = "botim-user@example.com"
```

**Implementation:**
1. Modeling → Manage Roles
2. Create role: "SP User"
3. Add DAX filter on `sharing_transactions` table
4. Save
5. In Power BI Service → Dataset Settings → Security
6. Assign users to roles

---

## 4. Looker/Looker Studio Implementation

### 4.1 LookML Model (Looker)

**File: `sharing_transactions.view.lkml`**

```lookml
view: sharing_transactions {
  sql_table_name: public.sharing_transactions ;;

  dimension: request_id {
    type: string
    primary_key: yes
    sql: ${TABLE}.request_id ;;
  }

  dimension: sp_id {
    type: string
    sql: ${TABLE}.sp_id ;;
    link: {
      label: "SP Detail Dashboard"
      url: "/dashboards/sp_detail?sp_id={{ value }}"
    }
  }

  dimension: channel {
    type: string
    sql: ${TABLE}.channel ;;
  }

  dimension: platform {
    type: string
    sql: ${TABLE}.platform ;;
  }

  dimension: status_code {
    type: string
    sql: ${TABLE}.status_code ;;
  }

  dimension: is_terminal {
    type: yesno
    sql: ${status_code} IN ('S40', 'S41', 'S42', 'S43', 'S44') ;;
  }

  dimension: is_success {
    type: yesno
    sql: ${status_code} = 'S40' ;;
  }

  dimension_group: status {
    type: time
    timeframes: [
      raw,
      time,
      date,
      week,
      month,
      quarter,
      year,
      hour_of_day,
      day_of_week
    ]
    sql: ${TABLE}.status_ts ;;
  }

  dimension: step_latency_seconds {
    type: number
    sql: ${TABLE}.step_latency_ms / 1000.0 ;;
    value_format_name: decimal_2
  }

  dimension: error_code {
    type: string
    sql: ${TABLE}.error_code ;;
  }

  dimension: error_source {
    type: string
    sql: ${TABLE}.error_source ;;
  }

  measure: total_requests {
    type: count_distinct
    sql: ${request_id} ;;
    drill_fields: [detail*]
  }

  measure: success_count {
    type: count_distinct
    sql: ${request_id} ;;
    filters: [status_code: "S40"]
  }

  measure: success_rate {
    type: number
    sql: 100.0 * ${success_count} / NULLIF(${total_requests}, 0) ;;
    value_format_name: percent_2
  }

  measure: avg_journey_time_seconds {
    type: average
    sql: ${step_latency_seconds} ;;
    filters: [is_success: "yes"]
  }

  measure: consent_conversion {
    type: number
    sql: 100.0 *
      ${s21_count} / NULLIF(${s20_count}, 0) ;;
    value_format_name: percent_2
  }

  measure: s20_count {
    type: count_distinct
    sql: ${request_id} ;;
    filters: [status_code: "S20"]
    hidden: yes
  }

  measure: s21_count {
    type: count_distinct
    sql: ${request_id} ;;
    filters: [status_code: "S21"]
    hidden: yes
  }

  set: detail {
    fields: [
      request_id,
      sp_id,
      channel,
      platform,
      status_code,
      status_time
    ]
  }
}
```

**File: `sharing_analytics.model.lkml`**

```lookml
connection: "uaepass_production"

include: "/views/**/*.view.lkml"

datagroup: hourly_refresh {
  sql_trigger: SELECT FLOOR(EXTRACT(EPOCH FROM NOW()) / 3600) ;;
  max_cache_age: "1 hour"
}

explore: sharing_transactions {
  label: "Document Sharing Analytics"

  join: date_dimension {
    type: left_outer
    sql_on: ${sharing_transactions.status_date} = ${date_dimension.date} ;;
    relationship: many_to_one
  }

  persist_with: hourly_refresh
}
```

### 4.2 Looker Dashboard Configuration

**Dashboard: Executive Overview**

**Tiles:**

1. **Single Value: Success Rate**
   - Measure: `sharing_transactions.success_rate`
   - Comparison: Previous period
   - Visualization: Single value with comparison

2. **Line Chart: Trend**
   - Dimension: `sharing_transactions.status_date`
   - Measure: `sharing_transactions.success_rate`
   - Filters: Last 30 days

3. **Pie Chart: Terminal Status**
   - Dimension: `sharing_transactions.status_code`
   - Measure: `sharing_transactions.total_requests`
   - Filters: `is_terminal: yes`

4. **Bar Chart: Channel Performance**
   - Dimension: `sharing_transactions.channel`
   - Measure: `sharing_transactions.success_rate`
   - Sort: Descending

**Filters (Dashboard Level):**
- Date Range: Last 30 days (default)
- Channel: All
- Platform: All

### 4.3 Looker Studio (Google Data Studio)

**Step 1: Connect Data Source**
1. Create Report → Add Data
2. Select connector: PostgreSQL (or BigQuery if data is there)
3. Enter connection details
4. Authenticate

**Step 2: Create Calculated Fields**

**Success Rate:**
```
(COUNT_DISTINCT(CASE WHEN status_code = 'S40' THEN request_id END) /
 COUNT_DISTINCT(request_id)) * 100
```

**Is Terminal:**
```
CASE
  WHEN status_code IN ('S40','S41','S42','S43','S44') THEN 'Yes'
  ELSE 'No'
END
```

**Step 3: Add Charts**

1. **Scorecard (Success Rate):**
   - Metric: Success Rate (calculated field)
   - Comparison: Previous period
   - Sparkline: Enabled

2. **Time Series (Trend):**
   - Date Range Dimension: status_ts
   - Metric: Success Rate
   - Comparison: Previous period (shaded area)

3. **Pie Chart (Terminal Status):**
   - Dimension: status_code
   - Metric: Record Count
   - Filter: Is Terminal = "Yes"

4. **Bar Chart (SP Performance):**
   - Dimension: sp_id
   - Metric: Success Rate
   - Sort: Success Rate descending
   - Bars to show: 20

**Step 4: Add Filters**
- Date Range: Last 30 days
- Channel (Dropdown)
- Platform (Radio buttons)

**Step 5: Share Dashboard**
- Share → Get link → Copy
- Permissions: View or Edit
- Schedule email delivery: Daily at 8 AM

---

## 5. Metabase Implementation

### 5.1 Database Connection

1. Admin → Databases → Add Database
2. Database type: PostgreSQL
3. Name: UAE PASS Analytics
4. Host: your-database-host.com
5. Port: 5432
6. Database name: uaepass_analytics
7. Username: [read-only user]
8. Password: [secure]
9. Save

### 5.2 Create Questions (Saved Queries)

**Question 1: Success Rate**

1. New → Question → Simple Question
2. Pick data: sharing_transactions
3. Summarize: Custom Expression
   ```
   CountIf([Status Code] = "S40") / Count
   ```
4. Filter: Status Code is one of S40, S41, S42, S43, S44
5. Visualize: Number
6. Format: Percentage
7. Save as: "Overall Success Rate"

**Question 2: Success Trend**

1. New → Question → Simple Question
2. Pick data: sharing_transactions
3. Summarize: Same as above
4. Group by: Status Ts → by Day
5. Filter: Status Ts in the last 30 days
6. Visualize: Line
7. Save as: "Success Rate Trend"

**Question 3: Terminal Status Breakdown**

1. New → Question → Simple Question
2. Pick data: sharing_transactions
3. Summarize: Count of Request ID (distinct)
4. Group by: Status Code
5. Filter: Status Code is one of S40, S41, S42, S43, S44
6. Visualize: Pie
7. Save as: "Terminal Status Distribution"

### 5.3 Create Dashboard

1. New → Dashboard → "Executive Overview"
2. Add saved questions:
   - Success Rate (scorecard, size: 1×1)
   - Success Trend (line, size: 2×1)
   - Terminal Status (pie, size: 1×1)
   - Channel Performance (bar, size: 2×1)
3. Add filters:
   - Date: Last 30 days
   - Channel: All
   - Platform: All
4. Link filters to questions
5. Save

### 5.4 Alerts

1. Open saved question: "Overall Success Rate"
2. Click bell icon → Get alerts
3. Email me when: "Success Rate goes below 65%"
4. Check: Hourly
5. Save

---

## 6. Dashboard Design Best Practices

### 6.1 Visual Hierarchy

**Priority Levels:**
1. **Critical Metrics (Top):** Success rate, total volume (large, prominent)
2. **Trends (Middle):** Time series, comparisons (medium size)
3. **Details (Bottom):** Tables, detailed breakdowns (smaller)

**Layout Example:**
```
[Big Number] [Big Number] [Big Number] [Big Number]
[────────── Trend Chart ──────────────][Pie Chart]
[────────── Funnel ───────────────────────────────]
[─── Bar Chart ────][─── Table ───────────────────]
```

### 6.2 Color Palette

**Status Colors:**
- Success (S40): `#28A745` (Green)
- Technical Error (S41): `#DC3545` (Red)
- Expired (S42): `#FD7E14` (Orange)
- User Aborted (S43): `#FFC107` (Yellow)
- Not Eligible (S44): `#6C757D` (Gray)

**Channel Colors:**
- Notification: `#007BFF` (Blue)
- QR: `#17A2B8` (Cyan)
- Redirect: `#6F42C1` (Purple)

**Platform Colors:**
- iOS: `#000000` (Black)
- Android: `#3DDC84` (Green)

**Performance Indicators:**
- Above Target: `#28A745` (Green)
- On Target: `#FFC107` (Yellow)
- Below Target: `#DC3545` (Red)

### 6.3 Formatting Standards

**Numbers:**
- Integers: `#,##0` (e.g., 236,426)
- Decimals: `#,##0.00` (e.g., 1,234.56)
- Percentages: `0.00%` (e.g., 67.40%)
- Large numbers: `#,##0.0 K` (e.g., 236.4K) or `#,##0.0 M` (e.g., 1.2M)

**Time:**
- Seconds: `0.0 s` (e.g., 143.2 s)
- Minutes: `0.0 min` (e.g., 2.4 min)
- Duration: `hh:mm:ss` (e.g., 00:02:23)

**Dates:**
- Short: `MMM DD` (e.g., Nov 18)
- Medium: `MMM DD, YYYY` (e.g., Nov 18, 2025)
- Long: `MMMM DD, YYYY` (e.g., November 18, 2025)

### 6.4 Tooltips

**Standard Tooltip Format:**
```
[Metric Name]
Value: [formatted value]
vs. [comparison period]: [+/-X.X%]
Date: [date]
```

**Example:**
```
Success Rate
Value: 67.4%
vs. Last Month: +0.8%
Date: Nov 18, 2025
```

### 6.5 Interactivity

**Required Actions:**
1. **Filter:** Click any dimension to filter all visuals
2. **Drill-down:** Click bar/line to show detail table
3. **Highlight:** Hover to highlight related data across charts
4. **Tooltip:** Show detailed breakdown on hover

### 6.6 Accessibility

**Requirements:**
- Color blindness safe: Use patterns + colors
- High contrast: 4.5:1 minimum for text
- Keyboard navigable: All filters accessible via tab
- Screen reader friendly: Alt text on all visuals

---

## 7. Refresh Schedules

### 7.1 Recommended Refresh Frequencies

**By Dashboard Type:**

| Dashboard Type | Frequency | Time (UAE) | Method |
|----------------|-----------|------------|--------|
| Executive Overview | Daily | 6:00 AM | Full refresh |
| Operational Monitoring | Every 5 min | Real-time | Live connection |
| Weekly Review | Weekly | Mon 6:00 AM | Full refresh |
| Error Analysis | Hourly | Top of hour | Incremental |
| SP Performance | Daily | 2:00 AM | Full refresh |

**By Data Volume:**
- <1M rows: Live connection
- 1M-10M rows: Hourly incremental + daily full
- >10M rows: Use materialized views + hourly refresh

### 7.2 Incremental Refresh Configuration

**Tableau:**
```
Filter: status_ts >= DATEADD('day', -7, TODAY())
Refresh: Hourly
Full Refresh: Weekly (Sunday 2 AM)
```

**Power BI:**
```
RangeStart = DateTime.LocalNow() - #duration(7, 0, 0, 0)
RangeEnd = DateTime.LocalNow()
Filter: status_ts >= RangeStart AND status_ts < RangeEnd
```

**Looker:**
```
persist_for: "1 hour"
sql_trigger: SELECT MAX(status_ts) FROM sharing_transactions ;;
```

---

## 8. Performance Optimization

### 8.1 Database Optimization

**Indexes (see SQL_QUERY_TEMPLATES.md for details):**
```sql
CREATE INDEX idx_status_code ON sharing_transactions(status_code);
CREATE INDEX idx_request_id ON sharing_transactions(request_id);
CREATE INDEX idx_status_ts ON sharing_transactions(status_ts);
CREATE INDEX idx_request_status ON sharing_transactions(request_id, status_code, status_ts);
```

**Materialized Views:**
```sql
CREATE MATERIALIZED VIEW mv_daily_summary AS
SELECT
    DATE(status_ts) as summary_date,
    channel,
    platform,
    sp_id,
    COUNT(DISTINCT request_id) as total_requests,
    COUNT(DISTINCT CASE WHEN status_code = 'S40' THEN request_id END) as success_count
FROM sharing_transactions
GROUP BY DATE(status_ts), channel, platform, sp_id;

REFRESH MATERIALIZED VIEW mv_daily_summary;  -- Run hourly via cron
```

### 8.2 BI Tool Optimization

**Tableau:**
- Use extracts for large datasets (>1M rows)
- Enable "Incremental Refresh" to update only new data
- Use Context Filters for large dimension filters
- Limit data sources per dashboard (max 3-5)
- Use aggregated data sources for historical trends

**Power BI:**
- Enable Query Folding (ensure all transformations push to database)
- Use DirectQuery for real-time, Import for performance
- Create aggregation tables for large fact tables
- Disable auto date/time hierarchy if not needed
- Use variables for repeated DAX expressions

**Looker:**
- Use persistent derived tables for complex aggregations
- Enable caching with appropriate datagroups
- Use aggregate awareness for large explores
- Limit result rows with `sql_always_where`

### 8.3 Query Optimization

**Avoid:**
- `SELECT *` (specify columns)
- Unnecessary JOINs
- Functions in WHERE clause (prevents index use)
- OR conditions (use IN instead)

**Use:**
- WHERE filters on indexed columns
- LIMIT for testing
- EXPLAIN ANALYZE to check query plan
- CTEs for readability, subqueries for performance

### 8.4 Monitoring Dashboard Performance

**Metrics to Track:**
- Query execution time (target: <5 seconds)
- Dashboard load time (target: <10 seconds)
- Extract refresh time (target: <30 minutes)
- Data freshness (target: <1 hour lag)

**Alerts:**
- Extract refresh failures
- Query timeout (>60 seconds)
- Dashboard load time >15 seconds

---

## Summary Checklist

**Before Go-Live:**
- [ ] Data connection tested and secured (SSL, read-only user)
- [ ] All calculated fields validated against SQL queries
- [ ] Dashboards tested on target screen resolution
- [ ] Filters applied correctly across all visuals
- [ ] Refresh schedule configured and tested
- [ ] Alerts set up for critical metrics
- [ ] User permissions configured (RLS if needed)
- [ ] Documentation shared with users
- [ ] Training session conducted for operations team
- [ ] Backup/disaster recovery plan in place

---

**End of BI Tool Setup Guide**
**Ready for Implementation in Production**
