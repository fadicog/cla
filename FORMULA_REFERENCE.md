# Formula Reference: UAE PASS Document Sharing Analytics
**Version:** 1.0
**Last Updated:** 2026-01-09
**Purpose:** Quick lookup for all calculation formulas

---

## Core Success Metrics

### 1. Overall Success Rate
```
Success Rate = (S40 Count / Total Terminal Requests) × 100

Where:
  S40 Count = Number of requests with final status S40
  Total Terminal Requests = Requests with final status in {S40, S41, S42, S43, S44}
```

**Example:** 236,426 S40 / 350,802 Total = **67.40%**

---

### 2. Conversion Rate
```
Conversion Rate = (S40 Count / Total Requests) × 100

Where:
  S40 Count = Number of requests that reached S40
  Total Requests = All unique request_ids (including in-progress)
```

**Example:** 236,426 S40 / 350,802 Total = **67.40%**

**Note:** Conversion Rate ≤ Success Rate (includes incomplete journeys)

---

### 3. Terminal Status Distribution
```
Status Percentage = (Count of Status X / Total Terminal Requests) × 100

For each status X in {S40, S41, S42, S43, S44}
```

**Example:**
- S40: 236,426 / 350,802 = 67.40%
- S43: 62,515 / 350,802 = 17.82%
- S42: 25,689 / 350,802 = 7.32%

---

## Channel Performance Metrics

### 4. Channel Success Rate
```
Channel Success Rate = (S40 Count for Channel C / Total Requests for Channel C) × 100

Where:
  Channel C ∈ {notification, qr, redirect}
```

**Example (Notification):** 178,234 S40 / 245,678 Total = **72.5%**

---

### 5. Channel Volume Distribution
```
Channel Volume % = (Requests on Channel C / Total Requests) × 100
```

**Example:**
- Notification: 245,678 / 350,802 = 70.0%
- QR: 89,456 / 350,802 = 25.5%
- Redirect: 15,668 / 350,802 = 4.5%

---

## Funnel Metrics

### 6. Stage Retention Rate
```
Stage Retention = (Requests Reaching Stage N / Requests Reaching Stage 0) × 100

Where:
  Stage 0 = S00 (Request Created)
  Stage N = Any subsequent status
```

**Example (Consent Screen):**
270,525 reached S20 / 350,802 reached S00 = **77.1% retention**

---

### 7. Step Drop-off Count
```
Drop-off Count = Requests at Stage N - Requests at Stage N+1
```

**Example (Consent → Consent Given):**
270,525 (S20) - 258,759 (S21) = **11,766 dropped off**

---

### 8. Step Drop-off Rate
```
Drop-off Rate = (Drop-off Count / Requests at Stage N) × 100
           = ((Stage N - Stage N+1) / Stage N) × 100
```

**Example (Consent → Consent Given):**
11,766 drop-off / 270,525 at S20 = **4.35% drop-off rate**

---

## User Behavior Metrics

### 9. Consent Conversion Rate
```
Consent Conversion = (S21 Count / S20 Count) × 100

Where:
  S21 Count = Requests that reached "Consent Given"
  S20 Count = Requests that reached "Consent Screen"
```

**Example:** 258,759 S21 / 270,525 S20 = **95.65%**

---

### 10. PIN Success Rate
```
PIN Success Rate = (S31 Count / S30 Count) × 100

Where:
  S31 Count = Requests with "PIN Verified"
  S30 Count = Requests that reached "PIN Screen"
```

**Example:** 239,857 S31 / 247,114 S30 = **97.06%**

---

### 11. User Abort Rate
```
User Abort Rate = (S43 Count / Total Terminal Requests) × 100

Alternatively (for specific stage):
Stage Abort Rate = (S43 from Stage X / Requests at Stage X) × 100
```

**Example (Overall):** 62,515 S43 / 350,802 Total = **17.82%**

**Example (Consent Screen):** 11,766 S43 from S20 / 270,525 at S20 = **4.35%**

---

### 12. Consent Decline Rate
```
Consent Decline Rate = ((S20 Count - S21 Count) / S20 Count) × 100
                     = 100% - Consent Conversion Rate
```

**Example:** (270,525 - 258,759) / 270,525 = **4.35%**

---

## Document Readiness Metrics

### 13. Document Availability Rate
```
Doc Availability Rate = (S10 Count / (S10 Count + S11 Count)) × 100

Where:
  S10 = Documents Ready
  S11 = Documents Missing
```

**Example:** 278,604 S10 / (278,604 + 72,198) = **79.4%**

---

### 14. Document Missing Rate
```
Doc Missing Rate = (S11 Count / (S10 Count + S11 Count)) × 100
                 = 100% - Doc Availability Rate
```

**Example:** 72,198 S11 / 350,802 = **20.6%**

---

### 15. Success Rate When Docs Ready
```
Success Rate (Docs Ready) = (S40 Count where S10 in history / S10 Count) × 100
```

**Example:** 236,426 S40 / 278,604 S10 = **84.9%**

---

### 16. Success Rate When Docs Missing
```
Success Rate (Docs Missing) = (S40 Count where S11 in history / S11 Count) × 100
```

**Example (from analysis):** 0 S40 / 72,198 S11 = **0.0%**

---

### 17. Document Retrieval Success Rate
```
Retrieval Success Rate = (S13 Count / S12 Count) × 100

Where:
  S13 = Document Retrieved Successfully
  S12 = Document Retrieval Attempted
```

**Example (typical):** 18,234 S13 / 24,567 S12 = **74.2%**

---

## Error Analysis Metrics

### 18. Technical Error Rate
```
Technical Error Rate = (S41 Count / Total Terminal Requests) × 100
```

**Example:** 12,133 S41 / 350,802 Total = **3.46%**

---

### 19. Error Frequency
```
Error Frequency = (Count of Error X / Total Error Events) × 100
```

**Example (issuer_timeout):**
3,167 issuer_timeout / 12,133 total errors = **26.1%**

---

### 20. Error Impact Rate (S41 Rate)
```
Error Impact Rate = (Requests with Error X that end in S41 / Requests with Error X) × 100
```

**Example (issuer_timeout):**
3,089 ended in S41 / 3,167 had error = **97.5% impact rate**

---

### 21. Error Recovery Rate
```
Recovery Rate = (Requests with Error X that end in S40 / Requests with Error X) × 100
              = 100% - Impact Rate (if only S40 or S41 outcomes)
```

**Example (pin_incorrect):**
1,448 ended in S40 / 1,537 had error = **94.2% recovery rate**

---

### 22. Error Source Distribution
```
Source Distribution = (Errors from Source Y / Total Errors) × 100

Where Source Y ∈ {issuer, network, dv, user_cancel}
```

**Example (issuer):** 4,761 issuer errors / 12,133 total = **39.2%**

---

## Service Provider Metrics

### 23. SP Success Rate
```
SP Success Rate = (S40 Count for SP / Total Requests for SP) × 100
```

**Example (Botim):** 45,123 S40 / 62,891 Total = **71.7%**

---

### 24. SP Error Rate
```
SP Error Rate = (Requests with Errors for SP / Total Requests for SP) × 100
```

**Example:** 3,456 error requests / 62,891 total = **5.5%**

---

### 25. SP Consent Conversion
```
SP Consent Conversion = (S21 Count for SP / S20 Count for SP) × 100
```

**Example:** 48,567 S21 / 52,341 S20 = **92.8%**

---

### 26. SP Document Availability
```
SP Doc Availability = (S10 Count for SP / (S10 + S11) Count for SP) × 100
```

**Example:** 52,341 S10 / (52,341 + 10,550) = **83.2%**

---

## Time & Latency Metrics

### 27. Average Journey Time
```
Avg Journey Time = AVG(Success Timestamp - Created Timestamp)
                 = SUM(Individual Journey Times) / Count of Journeys

For each request:
  Journey Time = Timestamp(S40) - Timestamp(S00)
```

**Example:** Total 33,845,678 seconds / 236,426 requests = **143.2 seconds avg**

---

### 28. Median Journey Time
```
Median Journey Time = PERCENTILE_CONT(0.5) of all journey times
```

**Example:** 50th percentile = **125 seconds**

---

### 29. P90 Journey Time
```
P90 Journey Time = PERCENTILE_CONT(0.90) of all journey times

(90% of requests complete faster than this)
```

**Example:** 90th percentile = **287 seconds**

---

### 30. Step Latency
```
Step Latency = Timestamp(Status N) - Timestamp(Status N-1)
             = step_latency_ms / 1000 (convert to seconds)
```

**Example (S20 → S21):**
Individual: 8,000 ms = 8 seconds
Average: 8.5 seconds across all requests

---

### 31. Time-to-Failure
```
Time-to-Failure = Timestamp(Terminal Failure Status) - Timestamp(S00)

Where Terminal Failure ∈ {S41, S42, S43, S44}
```

**Example (S43 - User Abort):**
Average time before user aborts = 112 seconds

---

## Platform Comparison Metrics

### 32. Platform Success Rate Difference
```
Platform Gap = iOS Success Rate - Android Success Rate
```

**Example:** 77.8% (iOS) - 67.7% (Android) = **+10.1 percentage points**

---

### 33. Platform Relative Performance
```
Relative Performance = (Platform X Success Rate / Best Platform Success Rate) × 100
```

**Example (Android vs iOS):**
67.7% / 77.8% = **87.0% relative performance**
(Android performs at 87% of iOS level)

---

## Advanced Metrics

### 34. Completion Rate (Terminal Rate)
```
Completion Rate = (Terminal Requests / Total Requests) × 100

Where Terminal = Requests with final status in {S40, S41, S42, S43, S44}
```

**Example:** 350,802 terminal / 350,802 total = **100%**
(In real-time data, may be <100% due to in-progress requests)

---

### 35. Day-over-Day Change
```
DoD Change = Today's Metric - Yesterday's Metric
DoD Change % = ((Today - Yesterday) / Yesterday) × 100
```

**Example (Volume):**
52,300 today - 48,500 yesterday = +3,800 requests
(+3,800 / 48,500) × 100 = **+7.8% increase**

---

### 36. Moving Average (7-Day)
```
Moving Avg (7-day) = SUM(Last 7 Days) / 7
```

**Example:**
(48,500 + 52,300 + 49,800 + 51,200 + 50,900 + 49,100 + 48,600) / 7 = **50,057 avg**

---

### 37. Conversion Funnel Efficiency
```
Funnel Efficiency = (S40 Count / S08 Count) × 100

(Success rate from "Request Viewed" to "Shared")
```

**Example:** 236,426 S40 / 311,074 S08 = **76.0%**

---

### 38. Transaction Success Rate (Terminal Success)
```
Transaction Success = (S40 Count / (S40 + S41 + S44) Count) × 100

(Excludes user-driven outcomes: S42 expired, S43 aborted)
```

**Example:**
236,426 / (236,426 + 12,133 + 14,039) = **90.0% transaction success**

---

### 39. Operational Failure Rate
```
Operational Failure = ((S41 + S42) Count / Total Terminal) × 100

(System-caused failures: technical + expired)
```

**Example:** (12,133 + 25,689) / 350,802 = **10.8%**

---

### 40. User-Driven Failure Rate
```
User-Driven Failure = ((S43 + S44) Count / Total Terminal) × 100

(User-caused: aborted + not eligible)
```

**Example:** (62,515 + 14,039) / 350,802 = **21.8%**

---

## Composite Metrics

### 41. Engagement Rate
```
Engagement Rate = (S08 Count / S00 Count) × 100

(% who view request after it's created/notified)
```

**Example:** 311,074 S08 / 350,802 S00 = **88.7%**

---

### 42. Completion Rate from Engagement
```
Completion from Engagement = (S40 Count / S08 Count) × 100

(Success rate among engaged users)
```

**Example:** 236,426 S40 / 311,074 S08 = **76.0%**

---

### 43. End-to-End Consent-to-Share
```
Consent-to-Share Rate = (S40 Count / S21 Count) × 100

(% who successfully share after giving consent)
```

**Example:** 236,426 S40 / 258,759 S21 = **91.4%**

---

### 44. PIN-to-Share Success
```
PIN-to-Share = (S40 Count / S31 Count) × 100

(% who successfully share after PIN verification)
```

**Example:** 236,426 S40 / 239,857 S31 = **98.6%**

---

## Statistical Measures

### 45. Standard Deviation
```
StdDev = SQRT(SUM((X - Mean)²) / N)

Where:
  X = Individual value
  Mean = Average of all values
  N = Number of observations
```

**Use Case:** Measure variability in journey times, identify outliers

---

### 46. Variance
```
Variance = SUM((X - Mean)²) / N
```

---

### 47. Coefficient of Variation
```
CV = (Standard Deviation / Mean) × 100

(Relative variability as percentage)
```

**Example:** If StdDev = 45 sec, Mean = 143 sec
CV = (45 / 143) × 100 = **31.5%**

---

### 48. Percentile Calculation
```
Pth Percentile = Value where P% of data falls below

Common percentiles:
  P25 (Q1) = 25th percentile (1st quartile)
  P50 (Q2) = Median (2nd quartile)
  P75 (Q3) = 75th percentile (3rd quartile)
  P90 = 90th percentile
  P95 = 95th percentile
  P99 = 99th percentile
```

---

## Ratio Metrics

### 49. Errors per Request
```
Errors per Request = Total Error Events / Total Requests
```

**Example:** 12,133 errors / 350,802 requests = **0.035 errors/request**

---

### 50. Average Steps per Request
```
Avg Steps = Total Status Events / Total Requests
```

**Example:** 3,508,020 status events / 350,802 requests = **10 steps/request**

---

### 51. Success-to-Failure Ratio
```
Success-to-Failure = S40 Count / (S41 + S42 + S43 + S44) Count
```

**Example:** 236,426 / (12,133 + 25,689 + 62,515 + 14,039) = **2.07:1**
(For every 1 failure, there are 2.07 successes)

---

## Trend Metrics

### 52. Growth Rate
```
Growth Rate = ((Current Period - Previous Period) / Previous Period) × 100
```

**Example (Week-over-Week):**
This week: 350,802 | Last week: 328,456
Growth = ((350,802 - 328,456) / 328,456) × 100 = **+6.8%**

---

### 53. Compound Growth Rate (CAGR)
```
CAGR = ((Ending Value / Beginning Value)^(1/N) - 1) × 100

Where N = Number of periods
```

**Example (3 months):**
End: 350,802 | Start: 280,000 | N = 3
CAGR = ((350,802 / 280,000)^(1/3) - 1) × 100 = **+7.8% per month**

---

### 54. Trend Slope (Linear Regression)
```
Slope = (N × SUM(XY) - SUM(X) × SUM(Y)) / (N × SUM(X²) - (SUM(X))²)

Where:
  X = Time period (day number)
  Y = Metric value
  N = Number of data points
```

**Use Case:** Determine if success rate is trending up or down over time

---

## Benchmark Comparisons

### 55. Index Score (vs Baseline)
```
Index = (Current Value / Baseline Value) × 100
```

**Example:**
Current success rate: 67.4% | Baseline: 65.0%
Index = (67.4 / 65.0) × 100 = **103.7**
(Performing 3.7% above baseline)

---

### 56. Gap to Target
```
Gap to Target = Target Value - Current Value
Gap % = ((Target - Current) / Current) × 100
```

**Example:**
Target: 75% | Current: 67.4%
Gap = 75 - 67.4 = **+7.6 percentage points needed**
Gap % = ((75 - 67.4) / 67.4) × 100 = **+11.3% improvement needed**

---

## Quick Reference: Key Formulas Summary

| Metric | Formula | Example |
|--------|---------|---------|
| Success Rate | (S40 / Terminal) × 100 | 67.4% |
| Conversion Rate | (S40 / All Requests) × 100 | 67.4% |
| Consent Conversion | (S21 / S20) × 100 | 95.6% |
| PIN Success | (S31 / S30) × 100 | 97.1% |
| Doc Availability | (S10 / (S10+S11)) × 100 | 79.4% |
| Error Rate | (S41 / Terminal) × 100 | 3.5% |
| Abort Rate | (S43 / Terminal) × 100 | 17.8% |
| Avg Journey Time | AVG(S40_ts - S00_ts) | 143 sec |
| Step Drop-off | Stage_N - Stage_N+1 | 11,766 |
| Drop-off % | (Drop / Stage_N) × 100 | 4.35% |

---

## Formula Notation Guide

**Symbols Used:**
- `×` = Multiply
- `/` = Divide
- `AVG()` = Average/Mean
- `SUM()` = Sum total
- `COUNT()` = Count of items
- `MAX()` = Maximum value
- `MIN()` = Minimum value
- `SQRT()` = Square root
- `∈` = "is an element of" (belongs to set)
- `{...}` = Set notation
- `^` = Power/exponent
- `≤` = Less than or equal to
- `≥` = Greater than or equal to

**Rounding:**
- Percentages: Round to 2 decimal places (67.40%)
- Time (seconds): Round to 2 decimal places (143.25 sec)
- Time (minutes): Round to 2 decimal places (2.39 min)
- Counts: No decimals (236,426 requests)
- Ratios: Round to 2 decimal places (2.07:1)

---

**End of Formula Reference**
**Total Formulas: 56**
**Quick Lookup for All Calculations**
