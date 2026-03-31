# UAE PASS Digital Documents - Sharing Request Analysis
## Comprehensive Statistical Analysis Report

**Analysis Date:** 2026-01-09
**Dataset:** `sharing_transactions_new_sample.csv`
**Period:** November 1-28, 2025
**Total Requests:** 500 | **Total Events:** 5,068

---

## Executive Summary

### Key Performance Indicators

| Metric | Value | Status |
|--------|-------|--------|
| **Overall Success Rate** | **65.6%** | Moderate |
| **Technical Error Rate** | **4.8%** | Good |
| **User Abort Rate** | **17.8%** | Concerning |
| **Expiry Rate** | **9.4%** | High |
| **Not Eligible Rate** | **2.4%** | Low |
| **Avg Journey Time (Success)** | **63.5 seconds** | Acceptable |
| **Avg Journey Time (Failed)** | **290.7 seconds** | Very Poor |

### Critical Findings

1. **User Abandonment is the #1 Issue**: 17.8% of requests are user-aborted, with 41.6% abandoning after granting consent
2. **Redirect Channel Outperforms**: 83% success rate vs 65% (QR) and 60% (notification)
3. **Failed Requests Take 4.6x Longer**: 291 seconds vs 64 seconds for successful requests
4. **Document Retrieval Works Well**: 86.7% success rate when documents are missing
5. **iOS Slightly Better**: 68.3% success vs 62.9% on Android
6. **Consent & PIN Not the Problem**: 93.1% consent approval, 95.7% PIN success
7. **Expired Requests at 9.4%**: High expiry rate indicates slow user response or short TTL
8. **Service Provider Performance Varies Widely**: From 89% (DU) to 36% (ADIB)

---

## 1. Overall Performance Analysis

### Terminal Status Distribution

![Terminal Status Distribution](D:\cluade\visualizations\01_terminal_status_distribution.png)

| Terminal Status | Count | Percentage | Description |
|----------------|-------|------------|-------------|
| **S40 - Success** | 328 | **65.6%** | Documents successfully shared |
| **S43 - User Aborted** | 89 | **17.8%** | User cancelled the request |
| **S42 - Expired** | 47 | **9.4%** | Request expired before completion |
| **S41 - Technical Error** | 24 | **4.8%** | System/technical failure |
| **S44 - Not Eligible** | 12 | **2.4%** | Missing docs couldn't be retrieved |

### Journey Duration Analysis

**Successful Requests (S40)**:
- Mean: 63.5 seconds
- Median: 59.0 seconds
- Distribution: Consistent, most users complete in ~60 seconds

**Failed Requests (All Others)**:
- Mean: 290.7 seconds
- Median: 63.0 seconds
- Distribution: High variance, many requests timeout or expire

**Key Insight**: Failed requests take 4.6x longer than successful ones, primarily due to expiries (15-minute timeout) and user abandonment delays.

---

## 2. Channel Performance Analysis

### Channel Comparison

![Channel Performance](D:\cluade\visualizations\02_channel_performance.png)

| Channel | Requests | Success Rate | Avg Journey Time |
|---------|----------|-------------|------------------|
| **Redirect** | 100 | **83.0%** | 57.3s |
| **QR** | 112 | **65.2%** | 138.2s |
| **Notification** | 288 | **59.7%** | 147.5s |

### Key Insights

1. **Redirect is the Clear Winner**: 23% higher success rate than notification channel
2. **Notification Channel Struggles**: Lowest success rate (59.7%) despite highest volume (57.6% of requests)
3. **QR Channel Moderate**: Middle performance, but significantly slower journey time
4. **Speed Matters**: Redirect channel is 2.4x faster than notification

### Channel-Specific Failure Modes

**Notification Channel**:
- High expiry rate (9.7%)
- User abandonment at 20.1%
- Longer user engagement time required

**QR Channel**:
- Moderate expiry rate (8.9%)
- Highest average journey time (138s)
- Technical errors at 5.4%

**Redirect Channel**:
- Lowest failure rates across all metrics
- Best user experience (immediate app open)
- Minimal expiry (5.0%)

### Recommendation

**Priority**: Investigate why notification channel underperforms and consider promoting redirect/QR channels for critical transactions.

---

## 3. Status Transition Analysis

### Transition Heatmap

![Status Transition Heatmap](D:\cluade\visualizations\03_transition_heatmap.png)

### Top 10 Most Common Transitions

| From | To | Count | Transition |
|------|-----|-------|------------|
| S20 | S21 | 405 | Consent Screen Shown -> Consent Granted |
| S21 | S30 | 368 | Consent Granted -> PIN Required |
| S30 | S31 | 352 | PIN Required -> PIN Success |
| S08 | S10 | 343 | Request Loaded -> Documents Ready |
| S31 | S40 | 328 | PIN Success -> Success (Shared) |
| S10 | S20 | 318 | Documents Ready -> Consent Screen Shown |
| S00 | S01 | 288 | Request Created -> Notification Sent |
| S01 | S02 | 288 | Notification Sent -> Notification Delivered |
| S02 | S03 | 288 | Notification Delivered -> Notification Tapped |
| S03 | S08 | 288 | Notification Tapped -> Request Loaded |

### Critical Drop-off Points

![Critical Drop-offs](D:\cluade\visualizations\04_critical_dropoffs.png)

**Top Drop-off Transitions** (to terminal failure statuses):

1. **S21 -> S43 (37 requests)**: Users grant consent but then abandon - **HIGHEST PRIORITY**
2. **S10 -> S42 (25 requests)**: Expiry after documents ready - timeout issue
3. **S20 -> S43 (30 requests)**: Abandonment at consent screen
4. **S32 -> S43 (16 requests)**: PIN failure leads to abort
5. **S31 -> S41 (24 requests)**: Technical error after PIN success - **CRITICAL BUG**

### Key Insights

1. **S21 -> S43 is the Biggest Problem**: 37 users (41.6% of all abandonments) abort after granting consent
2. **PIN Success Technical Failure**: 24 requests fail with S41 immediately after successful PIN (S31) - this appears to be a backend issue
3. **Expiry After Doc Check**: 25 requests expire after documents are ready - users not responding fast enough or system delays
4. **Consent Screen Abandonment**: 30 requests (33.7% of abandonments) exit at consent screen despite no denial

### Critical Issues to Investigate

**Issue #1: Post-Consent Abandonment (S21 -> S43)**
- **Impact**: 37 requests (7.4% of total)
- **Hypothesis**: User confusion after consent granted, unclear next steps, or app background/crash
- **Recommendation**: Add loading indicator after consent, implement session recovery

**Issue #2: Technical Error After PIN Success (S31 -> S41)**
- **Impact**: 24 requests (4.8% of total)
- **Hypothesis**: Backend signing service failure, network timeout during document packaging
- **Recommendation**: Urgent investigation of backend logs, implement retry logic

**Issue #3: Expiry After Document Check (S10 -> S42)**
- **Impact**: 25 requests (5.0% of total)
- **Hypothesis**: 15-minute TTL too short, user distraction, or UI not prompting action
- **Recommendation**: Extend TTL for document-ready requests, add push notification reminder

---

## 4. Error Analysis

![Error Analysis](D:\cluade\visualizations\05_error_analysis.png)

### Error Code Distribution

| Error Code | Count | Percentage | Category |
|------------|-------|------------|----------|
| **issuer_not_found** | 24 | 34.3% | Issuer |
| **pin_incorrect** | 12 | 17.1% | User |
| **dv_5xx** | 11 | 15.7% | DV Backend |
| **signing_timeout** | 6 | 8.6% | DV Backend |
| **network_error** | 5 | 7.1% | Network |
| **pin_dismissed** | 4 | 5.7% | User |
| **issuer_5xx** | 3 | 4.3% | Issuer |
| **issuer_timeout** | 3 | 4.3% | Issuer |
| **dv_timeout** | 2 | 2.9% | DV Backend |

### Error Source Breakdown

| Source | Count | Percentage | Description |
|--------|-------|------------|-------------|
| **Issuer** | 30 | 42.9% | Document issuer errors |
| **DV (Digital Vault)** | 19 | 27.1% | UAE PASS backend errors |
| **User Cancel** | 16 | 22.9% | User-initiated errors |
| **Network** | 5 | 7.1% | Connectivity issues |

### Key Insights

1. **Issuer Errors Dominate**: 42.9% of errors originate from document issuers
   - `issuer_not_found` (24 errors): Document type not available from issuer
   - `issuer_5xx` (3 errors): Issuer server failures
   - `issuer_timeout` (3 errors): Issuer API timeouts

2. **DV Backend Issues**: 27.1% of errors are internal UAE PASS problems
   - `dv_5xx` (11 errors): Backend server errors
   - `signing_timeout` (6 errors): Document signing timeouts
   - `dv_timeout` (2 errors): General backend timeouts

3. **User-Driven Errors**: 22.9% are user cancellations
   - `pin_incorrect` (12 errors): Wrong PIN entry
   - `pin_dismissed` (4 errors): User closed PIN dialog

### Error Status Distribution

**Statuses with Most Errors**:
- **S32** (PIN Failed): 12 errors - all `pin_incorrect`
- **S15** (Retrieval Failed - Issuer): 12 errors - `issuer_not_found`, `issuer_5xx`, `issuer_timeout`
- **S41** (Technical Error): 24 errors - mix of `dv_5xx`, `signing_timeout`, `network_error`
- **S14** (Retrieval Failed - Network): 6 errors - all `network_error`

### Previous Status Leading to Errors

**Top 5**:
1. **S30** (PIN Required) -> 12 errors (`pin_incorrect`, `pin_dismissed`)
2. **S12** (Retrieval Started) -> 18 errors (issuer/network failures)
3. **S31** (PIN Success) -> 24 errors (`dv_5xx`, `signing_timeout`)
4. **S06** (QR Scanned) -> 5 errors (`network_error`)

### Recommendations

1. **Issuer Coordination**: Work with issuers to improve API reliability and document availability
2. **Backend Hardening**: Investigate `dv_5xx` and `signing_timeout` errors - implement retry logic and circuit breakers
3. **Network Resilience**: Add offline mode/retry for network errors during QR scans
4. **User Guidance**: Better PIN entry UI, show remaining attempts, offer PIN reset

---

## 5. Service Provider Performance Analysis

![Service Provider Performance](D:\cluade\visualizations\06_service_provider_performance.png)

### Top Performers (Success Rate)

| Service Provider | Requests | Success Rate | Successful |
|-----------------|----------|-------------|------------|
| **DU** | 19 | **89.5%** | 17 |
| **ENBD Tablet Banking** | 22 | **86.4%** | 19 |
| **Du Esim** | 21 | **85.7%** | 18 |
| **FAB Retail Banking** | 24 | **83.3%** | 20 |
| **ADNIC** | 26 | **76.9%** | 20 |
| **Lulu** | 24 | **75.0%** | 18 |
| **Noor Capital** | 22 | **72.7%** | 16 |
| **Botim** | 30 | **70.0%** | 21 |
| **Emirates Islamic** | 20 | **70.0%** | 14 |
| **CBD Mobile** | 21 | **66.7%** | 14 |

### Bottom Performers (Success Rate, min 5 requests)

| Service Provider | Requests | Success Rate | Successful |
|-----------------|----------|-------------|------------|
| **InsureOne** | 28 | **35.7%** | 10 |
| **ADIB** | 19 | **36.8%** | 7 |
| **National Bonds** | 26 | **53.8%** | 14 |
| **National Bank of Fujairah** | 22 | **54.5%** | 12 |
| **Baraka** | 23 | **56.5%** | 13 |

### Volume vs Success Rate Analysis

**High Volume + High Success**:
- **Botim** (30 requests, 70.0%) - Good overall performance
- **FAB Retail Banking** (24 requests, 83.3%) - Excellent
- **Lulu** (24 requests, 75.0%) - Good

**High Volume + Low Success**:
- **InsureOne** (28 requests, 35.7%) - **CRITICAL**: Needs immediate investigation
- **National Bonds** (26 requests, 53.8%) - Below average
- **ADIB** (19 requests, 36.8%) - **CRITICAL**: Needs immediate investigation

### Key Insights

1. **InsureOne & ADIB Are Outliers**: Success rates below 40% - likely requesting unavailable documents or integration issues
2. **Financial Services Vary Widely**: Banks range from 36.8% (ADIB) to 86.4% (ENBD)
3. **Telcos Perform Well**: DU (89.5%), Du Esim (85.7%), Etisalat Retail (65.5%)
4. **High Volume Doesn't Guarantee Success**: Etisalat Business (29 requests) only 65.5% success

### SP-Specific Failure Patterns

**InsureOne (35.7% success)**:
- Requesting: Emirates ID, Driving License
- Likely issue: Many users don't have driving license stored
- Recommendation: Implement document pre-check API

**ADIB (36.8% success)**:
- Requesting: Various financial documents
- Likely issue: Document availability or integration misconfiguration
- Recommendation: Audit ADIB integration, verify document type mappings

### Recommendations

1. **SP Onboarding Audit**: Review InsureOne and ADIB integrations
2. **Document Pre-check API**: Let SPs verify document availability before requesting
3. **Best Practices Sharing**: Share DU and ENBD success strategies with struggling SPs
4. **SP Dashboard**: Provide real-time success rate visibility to SPs

---

## 6. Platform Comparison (iOS vs Android)

![Platform Comparison](D:\cluade\visualizations\07_platform_comparison.png)

### Platform Performance Summary

| Platform | Requests | Success Rate | Avg Journey Time | Technical Error Rate |
|----------|----------|-------------|------------------|---------------------|
| **iOS** | 249 | **68.3%** | 146.2s | 4.0% |
| **Android** | 251 | **62.9%** | 137.2s | 5.6% |

### Key Insights

1. **iOS Outperforms Android by 5.4%**: 68.3% vs 62.9% success rate
2. **Android is Slightly Faster**: 137s vs 146s average journey time (but lower success)
3. **Android Has More Technical Errors**: 5.6% vs 4.0%
4. **User Abort Rates Similar**: iOS 16.9%, Android 18.7%

### Platform-Specific Failure Modes

**iOS**:
- Lower technical error rate (4.0%)
- Higher expiry rate (10.4%)
- Better overall reliability

**Android**:
- Higher technical error rate (5.6%)
- More user aborts (18.7%)
- Faster but less successful

### Terminal Status Distribution by Platform

**iOS**:
- Success (S40): 68.3%
- User Abort (S43): 16.9%
- Expired (S42): 10.4%
- Technical Error (S41): 4.0%
- Not Eligible (S44): 0.4%

**Android**:
- Success (S40): 62.9%
- User Abort (S43): 18.7%
- Expired (S42): 8.4%
- Technical Error (S41): 5.6%
- Not Eligible (S44): 4.4%

### Recommendations

1. **Android Performance Sprint**: Investigate why Android has 5.4% lower success rate
2. **Error Analysis**: Deep-dive into Android technical errors - app crashes, background restrictions?
3. **Background Handling**: Ensure Android app properly handles background/foreground transitions
4. **Testing**: Increase Android device/OS version test coverage

---

## 7. Missing Document Analysis

![Missing Document Analysis](D:\cluade\visualizations\08_missing_document_analysis.png)

### Document Availability Overview

| Status | Requests | Percentage |
|--------|----------|------------|
| **Documents Ready (S10)** | 343 | 68.6% |
| **Documents Missing (S11)** | 135 | 27.0% |
| No Document Check | 22 | 4.4% |

### Surprising Insight: Missing Documents Lead to HIGHER Success

| Scenario | Success Rate |
|----------|-------------|
| **Documents Ready (S10)** | 61.5% |
| **Documents Missing (S11)** | 86.7% |

**Why?** Users who need to retrieve missing documents are more engaged and committed to completing the flow. They've already invested time and effort, creating a "sunk cost" effect.

### Document Retrieval Performance

When documents are missing, the system attempts to retrieve them:

| Retrieval Outcome | Count | Percentage |
|------------------|-------|------------|
| **Success (S13)** | 117 | **86.7%** |
| **Failed - Issuer (S15)** | 12 | **8.9%** |
| **Failed - Network (S14)** | 6 | **4.4%** |

**Key Finding**: Document retrieval works very well (86.7% success rate).

### Missing Document Count Distribution

| Missing Count | Requests |
|--------------|----------|
| 1 document | 89 |
| 2 documents | 35 |
| 3+ documents | 11 |

**Insight**: Most users missing only 1 document (65.9%), which has high retrieval success.

### Key Insights

1. **Document Retrieval is NOT the Problem**: 86.7% success rate is excellent
2. **User Engagement Paradox**: Users who retrieve docs are more committed and have higher completion rates
3. **Retrieval Failures Are Rare**: Only 18 out of 135 (13.3%) retrieval attempts fail
4. **Issuer Issues Dominate Retrieval Failures**: 12 issuer failures vs 6 network failures

### Recommendations

1. **Don't Worry About Retrieval**: Current system works well
2. **Focus on User Abandonment**: The real problem is the 61.5% success rate when docs are ready
3. **Leverage Engagement**: Consider "progressive disclosure" - show users the doc retrieval process to build investment
4. **Issuer Coordination**: Work with issuers causing `issuer_not_found` errors

---

## 8. User Behavior Patterns

![User Behavior Patterns](D:\cluade\visualizations\09_user_behavior_patterns.png)

### Consent Screen Performance

**Consent shown (S20)**: 435 requests

| Outcome | Count | Percentage |
|---------|-------|------------|
| **Granted (S21)** | 405 | **93.1%** |
| **Denied (S22)** | 0 | **0.0%** |
| Abandoned at screen | 30 | **6.9%** |

**Key Insight**: Consent is NOT the problem. 93.1% approval rate is excellent. Zero explicit denials.

### PIN Entry Performance

**PIN required (S30)**: 368 requests

| Outcome | Count | Percentage |
|---------|-------|------------|
| **Success (S31)** | 352 | **95.7%** |
| **Failed (S32)** | 16 | **4.3%** |

**Key Insight**: PIN is NOT the problem. 95.7% success rate is excellent.

### User Abandonment Analysis

**Total User Aborts (S43)**: 89 requests (17.8% of all requests)

**Where Users Abandon**:

| Previous Status | Count | % of Abandonments |
|----------------|-------|-------------------|
| **After Consent Granted (S21)** | 37 | **41.6%** |
| **At Consent Screen (S20)** | 30 | **33.7%** |
| **After PIN Failed (S32)** | 16 | **18.0%** |
| **After Network Failure (S14)** | 6 | **6.7%** |

**Critical Finding**: 78% of abandonments happen around the consent screen (before or after granting consent).

### Time Spent at Critical Decision Points

| Status | Average Time | Description |
|--------|-------------|-------------|
| **S20** (Consent Screen) | **8.0 seconds** | Time user spends on consent screen |
| **S30** (PIN Entry) | **~7 seconds** | Time to enter PIN |

**Insight**: Users make quick decisions (8 seconds at consent), but then 41.6% abandon after granting consent - suggesting a post-consent UX issue, not consent hesitation.

### Key Insights

1. **Post-Consent Abandonment is the Real Problem**: 37 requests (41.6% of aborts) abandon after granting consent
2. **Consent Screen Itself is Fine**: 93.1% approval, only 30 (6.9%) abandon at screen
3. **PIN is Not a Barrier**: 95.7% success rate
4. **PIN Failure Cascade**: All 16 PIN failures lead to abandonment (100% conversion to S43)
5. **Fast Decision Making**: 8 seconds at consent screen indicates users are confident

### Hypothesis: Post-Consent Abandonment (S21 -> S43)

**Possible Causes**:
1. **App Backgrounding**: User switches apps/receives call after consent, app loses session
2. **Loading Screen Confusion**: No clear indication of progress after consent granted
3. **Network Issues**: Silent network failure causes user to give up
4. **Unexpected Delay**: User expects immediate completion after consent
5. **Missing Call-to-Action**: Unclear what happens next after consent

### Recommendations

**Priority 1: Fix Post-Consent Experience**
- Add prominent loading indicator after consent granted
- Show progress: "Preparing documents..." -> "Securing with PIN..." -> "Finalizing..."
- Implement session recovery if app backgrounds
- Set expectation: "This will take ~30 seconds"

**Priority 2: PIN Failure Recovery**
- Offer PIN reset/recovery flow instead of immediate abort
- Show remaining attempts (3 tries)
- Add biometric as backup authentication

**Priority 3: Consent Screen Improvements**
- While 93.1% is good, 30 abandonments is still 6.9%
- Add trust indicators (SP logo, data usage statement)
- Show document preview thumbnails

---

## 9. Journey Path Analysis

![Journey Path Analysis](D:\cluade\visualizations\10_journey_path_analysis.png)

### Most Common Successful Paths

**Path 1 (121 requests - 36.9% of successes)**: Standard Notification Flow
```
S00 -> S01 -> S02 -> S03 -> S08 -> S10 -> S20 -> S21 -> S30 -> S31 -> S40
(Request -> Notif -> Delivered -> Tapped -> Loaded -> Docs Ready -> Consent -> Granted -> PIN -> Success -> Share)
```
- **11 steps**, **~59 seconds**
- Ideal path: Documents ready, no retrieval needed

**Path 2 (51 requests - 15.5% of successes)**: Notification with Retrieval
```
S00 -> S01 -> S02 -> S03 -> S08 -> S11 -> S12 -> S13 -> S20 -> S21 -> S30 -> S31 -> S40
(Same as Path 1, but S11-S12-S13 for doc retrieval)
```
- **13 steps**, **~73 seconds**
- Requires document retrieval, still succeeds

**Path 3 (49 requests - 14.9% of successes)**: Redirect Flow
```
S00 -> S04 -> S05 -> S08 -> S10 -> S20 -> S21 -> S30 -> S31 -> S40
(Request -> Redirect -> App Open -> Loaded -> Docs Ready -> Consent -> Granted -> PIN -> Success -> Share)
```
- **10 steps**, **~48 seconds**
- Fastest path: Redirect channel, no retrieval

**Path 4 (41 requests - 12.5% of successes)**: QR Flow
```
S00 -> S06 -> S07 -> S08 -> S10 -> S20 -> S21 -> S30 -> S31 -> S40
(Request -> QR Scan -> Validated -> Loaded -> Docs Ready -> Consent -> Granted -> PIN -> Success -> Share)
```
- **10 steps**, **~55 seconds**
- QR channel, no retrieval

### Journey Length Statistics

**Successful Requests**:
- Mean: 11.2 steps
- Median: 11 steps
- Range: 10-13 steps

**Failed Requests**:
- Mean: 8.0 steps
- Median: 9 steps
- Range: 3-11 steps

**Key Insight**: Failed requests have shorter journeys because they exit early.

### Most Common Failure Paths

**Failure Path 1 (37 requests - 41.6% of S43 aborts)**: Post-Consent Abandonment
```
S00 -> S01 -> S02 -> S03 -> S08 -> S10 -> S20 -> S21 -> S43
(Notification flow, docs ready, consent granted, then ABORT)
```
- **9 steps**
- **THE BIGGEST PROBLEM**: Users abandon right after granting consent

**Failure Path 2 (25 requests - 53.2% of S42 expiries)**: Early Expiry After Doc Check
```
S00 -> S01 -> S02 -> S03 -> S08 -> S10 -> S42
(Notification flow, docs ready, but request EXPIRES before user acts)
```
- **7 steps**
- User doesn't respond within 15-minute TTL

**Failure Path 3 (22 requests - 46.8% of S42 expiries)**: QR Expiry
```
S00 -> S06 -> S42
(QR code generated but EXPIRES before being scanned)
```
- **3 steps**
- QR not scanned in time

**Failure Path 4 (17 requests)**: QR Flow Technical Error
```
S00 -> S06 -> S07 -> S08 -> S10 -> S20 -> S21 -> S30 -> S31 -> S41
(QR flow completes PIN successfully, then TECHNICAL ERROR)
```
- **10 steps**
- Backend failure after successful authentication

**Failure Path 5 (16 requests)**: PIN Failure -> Abort
```
S00 -> S01 -> S02 -> S03 -> S08 -> S10 -> S20 -> S21 -> S30 -> S32 -> S43
(Notification flow, PIN FAILS, user ABORTS)
```
- **11 steps**
- 100% of PIN failures lead to abort

**Failure Path 6 (12 requests)**: Document Not Found
```
S00 -> S01 -> S02 -> S03 -> S08 -> S11 -> S12 -> S15 -> S44
(Notification flow, docs missing, retrieval FAILS at issuer, NOT ELIGIBLE)
```
- **9 steps**
- Issuer can't provide requested document

### Last Status Before Terminal

**Top statuses leading to terminal outcomes**:
1. **S31** (352) -> S40: PIN success -> Share success ✓
2. **S21** (37) -> S43: Consent granted -> User abort ✗
3. **S20** (30) -> S43: Consent shown -> User abort ✗
4. **S10** (25) -> S42: Docs ready -> Expired ✗
5. **S32** (16) -> S43: PIN failed -> User abort ✗
6. **S15** (12) -> S44: Issuer retrieval fail -> Not eligible ✗

### Key Insights

1. **Successful Paths are Longer**: 11.2 steps vs 8.0 steps for failures
2. **Channel Affects Path**: Redirect (10 steps) faster than Notification (11 steps)
3. **Post-Consent Abort Dominates Failures**: 37 out of 89 aborts (41.6%)
4. **QR Expiry is Quick**: Only 3 steps - users never scan the code
5. **No "Dead End" Statuses**: Every status can lead to success if user continues

### Recommendations

1. **Session Recovery**: Implement recovery for S21 -> S43 path
2. **QR TTL Optimization**: Analyze QR expiry patterns, extend TTL if needed
3. **PIN Retry Flow**: Add retry/recovery for S32 instead of immediate S43
4. **Progress Indicators**: Show clear path progress to encourage completion
5. **Push Reminders**: Send push notification if user stalls at S10 or S20

---

## 10. Time-Based Analysis & Latency

![Time Latency Analysis](D:\cluade\visualizations\11_time_latency_analysis.png)

### Overall Latency Statistics

| Metric | Value |
|--------|-------|
| Mean step latency | 15.5 seconds |
| Median step latency | 5.0 seconds |
| 95th percentile | 18.0 seconds |
| Maximum | 900.0 seconds |

**Key Insight**: Median (5s) vs Mean (15.5s) shows right-skewed distribution - most steps are fast, but some are very slow (expiries).

### Top 10 Slowest Status Transitions (Bottlenecks)

| Status | Mean Latency | Median Latency | Count | Description |
|--------|-------------|----------------|-------|-------------|
| **S42** | **900.0s** | 900.0s | 47 | Expiry timeout (15 minutes) |
| **S20** | **16.7s** | 17.0s | 435 | Time from doc check to consent screen |
| **S12** | **13.8s** | 14.0s | 135 | Document retrieval start |
| **S43** | **13.7s** | 8.0s | 89 | Time before user abandonment |
| **S32** | **12.0s** | 12.0s | 16 | PIN failure (wrong entry) |
| **S07** | **11.1s** | 11.0s | 90 | QR validation |
| **S13** | **10.0s** | 10.0s | 117 | Document retrieval success |
| **S15** | **10.0s** | 10.0s | 12 | Document retrieval fail (issuer) |
| **S14** | **9.0s** | 9.0s | 6 | Document retrieval fail (network) |
| **S21** | **7.9s** | 8.0s | 405 | Consent granted |

### Bottleneck Analysis

**Bottleneck #1: S42 (Expiry) - 900 seconds**
- **Impact**: 47 requests (9.4%)
- **Cause**: 15-minute timeout threshold
- **Not fixable**: This is by design (timeout)
- **Mitigation**: Reduce S10 -> S42 and S06 -> S42 paths

**Bottleneck #2: S20 (Consent Screen Load) - 16.7 seconds**
- **Impact**: 435 requests (87% of requests reach this)
- **Cause**: Loading consent screen after document check
- **Potential**: Could be reduced by pre-loading consent screen data
- **Recommendation**: Optimize consent screen rendering, fetch SP metadata earlier

**Bottleneck #3: S12 (Retrieval Start) - 13.8 seconds**
- **Impact**: 135 requests (27%)
- **Cause**: Calling issuer APIs to retrieve missing documents
- **Note**: 13.8s is acceptable for external API calls
- **Recommendation**: Add loading indicator, set user expectation

**Bottleneck #4: S43 (Abandonment Time) - 13.7 seconds (mean) / 8.0s (median)**
- **Impact**: 89 requests (17.8%)
- **Insight**: Users wait average 8 seconds before abandoning
- **Interpretation**: Short wait time = confusion/frustration, not patience loss
- **Recommendation**: Fix UX issues causing abandonment, not timeout issues

**Bottleneck #5: S07 (QR Validation) - 11.1 seconds**
- **Impact**: 90 QR requests
- **Cause**: QR code validation and request lookup
- **Potential**: Could be optimized
- **Recommendation**: Optimize QR validation logic, use caching

### Journey Duration Comparison

**Successful Requests (S40)**:
- Mean: 63.5 seconds
- Median: 59.0 seconds
- Distribution: Tight, consistent

**Failed Requests (All Others)**:
- Mean: 290.7 seconds
- Median: 63.0 seconds
- Distribution: Wide variance (due to 900s expiries)

**Key Insight**: Excluding expiries, failed requests have similar duration to successful ones (median 63s both). The 290s mean is inflated by 47 expiries at 900s each.

### Average Latency Distribution by Outcome

**Successful Requests**: Average step latency ~6-8 seconds
**Failed Requests**: Average step latency ~6-8 seconds (excluding S42)

**Conclusion**: Latency doesn't predict success/failure (except for S42 expiries).

### Recommendations

**Priority 1: Optimize Consent Screen Load (S20)**
- Current: 16.7 seconds
- Target: <10 seconds
- Actions: Pre-fetch SP metadata, optimize rendering, reduce API calls

**Priority 2: Reduce Post-Consent Abandonment Time**
- Current: 8 seconds before abandonment
- Issue: Users don't wait long - they're confused, not impatient
- Actions: Fix UX, add loading indicators, show progress

**Priority 3: Optimize QR Validation (S07)**
- Current: 11.1 seconds
- Target: <5 seconds
- Actions: Cache QR request data, optimize lookup queries

**Priority 4: Reduce Expiry Rate**
- Current: 9.4% of requests expire (47 requests)
- Focus on paths: S10 -> S42 (25) and S06 -> S42 (22)
- Actions: Push notification reminders, extend TTL for document-ready requests

---

## 11. Conversion Funnel Analysis

![Conversion Funnel](D:\cluade\visualizations\12_conversion_funnel.png)

### Complete Conversion Funnel

| Stage | Status | Count | % of Total | Drop-off from Previous |
|-------|--------|-------|-----------|----------------------|
| **Request Created** | S00 | 500 | 100.0% | - |
| **Request Loaded** | S08 | 478 | 95.6% | **-4.4%** |
| **Doc Check Complete** | S10/S11 | 478 | 95.6% | -0.0% |
| **Consent Shown** | S20 | 435 | 87.0% | **-9.0%** |
| **Consent Granted** | S21 | 405 | 81.0% | **-6.9%** |
| **PIN Required** | S30 | 368 | 73.6% | **-9.1%** |
| **PIN Success** | S31 | 352 | 70.4% | -4.3% |
| **Success (Shared)** | S40 | 328 | 65.6% | **-6.8%** |

### Key Drop-off Points

**Drop-off #1: Request Created -> Request Loaded (-4.4%, 22 requests)**
- **Cause**: 22 QR codes expired before being scanned (S00 -> S06 -> S42)
- **Impact**: Small but indicates QR codes not being scanned
- **Recommendation**: Investigate QR code visibility, placement, TTL

**Drop-off #2: Doc Check -> Consent Shown (-9.0%, 43 requests)**
- **Cause**: 25 expiries after doc check (S10 -> S42), 18 errors during retrieval
- **Impact**: Moderate - users not moving forward after docs checked
- **Recommendation**: Push notification to prompt action, extend S10 TTL

**Drop-off #3: Consent Shown -> Consent Granted (-6.9%, 30 requests)**
- **Cause**: Users abandon at consent screen without denying (S20 -> S43, S20 -> S42)
- **Impact**: Moderate - consent screen UX or timing issue
- **Recommendation**: Optimize consent screen load time (16.7s), improve clarity

**Drop-off #4: Consent Granted -> PIN Required (-9.1%, 37 requests)**
- **Cause**: THE BIGGEST PROBLEM - S21 -> S43 abandonment
- **Impact**: High - users grant consent but don't reach PIN screen
- **Recommendation**: URGENT - investigate post-consent flow, add loading indicator, session recovery

**Drop-off #5: PIN Success -> Share Success (-6.8%, 24 requests)**
- **Cause**: Technical errors after PIN success (S31 -> S41)
- **Impact**: High - backend signing failures
- **Recommendation**: URGENT - investigate backend logs, add retry logic

### Funnel Efficiency

**Overall Conversion Rate**: 65.6% (328 out of 500)

**Stage-by-Stage Efficiency**:
- S00 -> S08: 95.6% ✓ (Good)
- S08 -> S20: 91.0% ✓ (Good)
- S20 -> S21: 93.1% ✓ (Excellent)
- S21 -> S30: 90.9% ✗ (Problem area)
- S30 -> S31: 95.7% ✓ (Excellent)
- S31 -> S40: 93.2% ✗ (Technical issue)

**Best Performing Stages**:
1. PIN success rate: 95.7%
2. Consent approval rate: 93.1%
3. Request load rate: 95.6%

**Worst Performing Stages**:
1. Consent granted -> PIN required: 90.9% (highest drop-off)
2. Doc check -> Consent shown: 91.0%

### Key Insights

1. **Post-Consent to PIN is the Weakest Link**: 9.1% drop-off (37 requests)
2. **Backend Technical Failures are Critical**: 6.8% drop-off after successful PIN
3. **Consent Itself is Not the Problem**: 93.1% approval rate
4. **PIN is Not the Problem**: 95.7% success rate
5. **Early QR Expiry Loses 4.4%**: Small but fixable

### Funnel Optimization Opportunities

**If we fix S21 -> S43 (post-consent abandonment)**:
- Recover 37 requests
- Success rate: 65.6% -> 73.0% (+7.4%)

**If we also fix S31 -> S41 (technical errors after PIN)**:
- Recover 24 requests
- Success rate: 73.0% -> 77.8% (+12.2% total)

**If we also reduce S10 -> S42 (expiries after doc check)**:
- Recover 25 requests
- Success rate: 77.8% -> 82.8% (+17.2% total)

**Potential Maximum Success Rate: ~83%** (if top 3 issues fixed)

### Recommendations

**Priority 1: Fix S21 -> S43 Post-Consent Abandonment (+7.4% success rate)**
- Implement: Loading indicators, session recovery, progress visibility
- Timeline: Immediate (high impact, UX fix)

**Priority 2: Fix S31 -> S41 Technical Errors After PIN (+4.8% success rate)**
- Implement: Backend hardening, retry logic, error handling
- Timeline: Urgent (high impact, backend fix)

**Priority 3: Reduce S10 -> S42 Expiries After Doc Check (+5.0% success rate)**
- Implement: Push reminders, extended TTL, in-app nudges
- Timeline: Medium (moderate impact, UX + config)

**Priority 4: Optimize S20 Load Time (-6.9% drop-off at consent)**
- Implement: Pre-fetch data, optimize rendering
- Timeline: Medium (moderate impact, performance optimization)

---

## 12. Top 10 Critical Insights

### 1. Post-Consent Abandonment is the #1 Problem
- **Impact**: 37 requests (7.4% of total) abort after granting consent
- **Why It Matters**: Users have already approved sharing but don't complete
- **Root Cause**: Likely UX confusion, app backgrounding, or unclear next steps
- **Action**: Implement loading indicators, session recovery, progress visibility

### 2. Technical Errors After PIN Success (Backend Failures)
- **Impact**: 24 requests (4.8% of total) fail with S41 after successful PIN
- **Why It Matters**: Users complete all steps correctly, system fails them
- **Root Cause**: Backend signing service failures, network timeouts
- **Action**: Investigate backend logs, implement retry logic, add circuit breakers

### 3. Redirect Channel is the Clear Winner
- **Performance**: 83% success rate vs 65% (QR) and 60% (notification)
- **Why It Matters**: 23% higher success than notification, fastest journey time
- **Root Cause**: Immediate app open, no notification dependency
- **Action**: Promote redirect channel for critical transactions, study best practices

### 4. Consent & PIN Are NOT the Problems
- **Consent Approval**: 93.1% (excellent)
- **PIN Success**: 95.7% (excellent)
- **Why It Matters**: Commonly assumed friction points are actually working well
- **Root Cause**: Good UX design at these stages
- **Action**: Don't over-optimize these areas, focus elsewhere

### 5. Failed Requests Take 4.6x Longer (290s vs 64s)
- **Impact**: Poor user experience for 34% of requests
- **Why It Matters**: Failed requests mostly timeout (900s) or users wait before abandoning
- **Root Cause**: 47 expiries at 900s inflate average, plus user confusion delays
- **Action**: Reduce expiry rate, fix abandonment triggers

### 6. Document Retrieval Works Excellently (86.7% success)
- **Performance**: 117 out of 135 retrieval attempts succeed
- **Why It Matters**: Commonly perceived as risky, actually very reliable
- **Root Cause**: Good issuer integration, robust retry logic
- **Action**: No changes needed, leverage as strength

### 7. User Engagement Paradox: Missing Docs = Higher Success
- **Unexpected**: 86.7% success when docs missing vs 61.5% when ready
- **Why It Matters**: Challenges assumption that doc availability is critical
- **Root Cause**: Users retrieving docs are more engaged and committed
- **Action**: Leverage retrieval process to build user investment

### 8. iOS Outperforms Android by 5.4%
- **Performance**: 68.3% (iOS) vs 62.9% (Android)
- **Why It Matters**: Significant platform disparity affects 50% of users
- **Root Cause**: Android technical errors (5.6% vs 4.0%), more abandons
- **Action**: Android performance sprint, investigate crashes/background handling

### 9. Service Provider Integration Quality Varies Wildly
- **Range**: 89.5% (DU) to 35.7% (InsureOne)
- **Why It Matters**: Poor SP integration ruins user experience, damages UAE PASS reputation
- **Root Cause**: InsureOne and ADIB likely requesting unavailable documents or misconfigured
- **Action**: SP audit, document pre-check API, integration best practices sharing

### 10. Expiry Rate at 9.4% is Too High
- **Impact**: 47 requests timeout before completion
- **Why It Matters**: 1 in 10 requests expire - indicates UX urgency issues or short TTL
- **Root Cause**: 25 expiries after S10 (doc check), 22 QR codes never scanned
- **Action**: Push reminders, extend TTL for doc-ready state, improve QR visibility

---

## 13. Prioritized Recommendations

### URGENT (Fix Immediately - High Impact)

#### 1. Fix Post-Consent Abandonment (S21 -> S43)
- **Impact**: +7.4% success rate (37 requests)
- **Effort**: Medium (UX changes)
- **Actions**:
  - Add loading indicator after consent granted: "Preparing your documents..."
  - Show progress bar with stages: Consent ✓ -> Preparing -> PIN -> Sharing
  - Implement session recovery if app backgrounds
  - Add timeout warning: "Please stay on this screen"
  - Track analytics: Where exactly does S21 -> S43 happen?

#### 2. Investigate & Fix Backend Failures After PIN (S31 -> S41)
- **Impact**: +4.8% success rate (24 requests)
- **Effort**: High (backend investigation)
- **Actions**:
  - Deep-dive into logs for S31 -> S41 failures
  - Identify failure patterns: signing_timeout, dv_5xx, network_error
  - Implement retry logic with exponential backoff
  - Add circuit breaker for signing service
  - Set up alerts for S31 -> S41 failures

#### 3. Audit InsureOne & ADIB Integrations
- **Impact**: +8 requests (InsureOne) + 7 requests (ADIB) = 15 requests
- **Effort**: Medium (SP collaboration)
- **Actions**:
  - Review document type requests vs user availability
  - Implement document pre-check API for SPs
  - Share best practices from DU (89.5% success)
  - Provide SP dashboard with real-time success rates

### HIGH PRIORITY (Plan & Implement - Significant Impact)

#### 4. Reduce Expiry Rate After Doc Check (S10 -> S42)
- **Impact**: +5.0% success rate (25 requests)
- **Effort**: Medium (push notifications + config)
- **Actions**:
  - Send push notification if user doesn't act within 5 minutes at S10
  - Extend TTL for document-ready requests (S10) from 15 min to 30 min
  - Add in-app nudge: "Your documents are ready! Tap to continue"
  - Track: How long do users typically wait at S10 before acting?

#### 5. Optimize Consent Screen Load Time (S20)
- **Impact**: Reduce 16.7s load time, improve 6.9% drop-off
- **Effort**: Medium (performance optimization)
- **Actions**:
  - Pre-fetch SP metadata during S08/S10
  - Optimize consent screen rendering (lazy load non-critical elements)
  - Cache SP logos and details
  - Add loading skeleton/spinner during S20 load

#### 6. Android Performance Sprint
- **Impact**: Close 5.4% iOS/Android gap = +13 requests
- **Effort**: High (comprehensive investigation)
- **Actions**:
  - Analyze Android-specific S41 technical errors
  - Test background/foreground transitions across Android versions
  - Improve Android app memory management
  - Increase test coverage for Android devices (Samsung, Xiaomi, etc.)

#### 7. Reduce QR Code Expiry (S00 -> S06 -> S42)
- **Impact**: +4.4% success rate (22 requests)
- **Effort**: Low (analytics + UX)
- **Actions**:
  - Analyze: How long between QR generation and scan attempts?
  - Extend QR TTL if scans happen >15 minutes after generation
  - Improve QR code visibility on SP websites/apps
  - Add QR refresh button: "Code expired? Generate new one"

### MEDIUM PRIORITY (Continuous Improvement)

#### 8. Implement PIN Retry/Recovery Flow
- **Impact**: Prevent 16 S32 -> S43 cascades (3.2% of requests)
- **Effort**: Medium (UX + backend)
- **Actions**:
  - Show remaining PIN attempts (3 tries)
  - Offer PIN reset/recovery after 3 failures
  - Add biometric fallback (Face ID / Fingerprint)
  - Don't auto-abort after 1 failure - give users 3 chances

#### 9. Improve Consent Screen Abandonment (S20 -> S43)
- **Impact**: +6% of 30 abandonments = ~2 requests
- **Effort**: Low (UX improvements)
- **Actions**:
  - Add trust indicators: SP logo, "Secure by UAE PASS"
  - Show document preview thumbnails
  - Add data usage statement: "Your data is encrypted and only shared with [SP]"
  - A/B test: Consent screen layout changes

#### 10. Optimize QR Validation Time (S07)
- **Impact**: Reduce 11.1s to <5s
- **Effort**: Medium (backend optimization)
- **Actions**:
  - Cache QR request data in Redis
  - Optimize database lookups (add indexes)
  - Pre-validate QR parameters
  - Add loading indicator during S07

### LOW PRIORITY (Monitor & Maintain)

#### 11. Service Provider Dashboard
- **Impact**: Long-term SP performance improvement
- **Effort**: High (dashboard development)
- **Actions**:
  - Real-time success rate by SP
  - Document availability insights
  - Error code breakdown
  - Best practices recommendations

#### 12. Document Pre-check API
- **Impact**: Prevent 27% of requests from requesting unavailable docs
- **Effort**: High (new API development)
- **Actions**:
  - API: Check user document availability before creating request
  - SPs call pre-check, only request available documents
  - Reduce S11 rate from 27% to <10%
  - Prevent "dead on arrival" requests

#### 13. Enhanced Analytics & Monitoring
- **Impact**: Better visibility into future issues
- **Effort**: Medium (analytics setup)
- **Actions**:
  - Real-time dashboard for status transitions
  - Alerts for anomalies (sudden S31 -> S41 spike)
  - Cohort analysis (iOS vs Android, channel, SP)
  - User journey recordings (with consent)

---

## 14. Potential Impact Summary

### If Top 3 Recommendations Implemented:

| Fix | Current Success | After Fix | Improvement |
|-----|----------------|-----------|-------------|
| **Baseline** | 65.6% | - | - |
| + Fix S21 -> S43 | 65.6% | 73.0% | +7.4% |
| + Fix S31 -> S41 | 73.0% | 77.8% | +4.8% |
| + Reduce S10 -> S42 | 77.8% | 82.8% | +5.0% |
| **Total Impact** | **65.6%** | **82.8%** | **+17.2%** |

### Estimated Weekly Impact (assuming 10,000 requests/week):

| Metric | Current | After Fixes | Improvement |
|--------|---------|-------------|-------------|
| Successful Shares | 6,560 | 8,280 | **+1,720/week** |
| User Aborts | 1,780 | 820 | **-960/week** |
| Technical Errors | 480 | 240 | **-240/week** |
| Expiries | 940 | 440 | **-500/week** |

---

## 15. Key Questions Answered

### 1. What is the biggest drop-off point in the journey?
**Answer**: Post-consent abandonment (S21 -> S43) with 37 requests (7.4% of total). Users grant consent but abandon before reaching PIN screen.

### 2. Which channel performs best and why?
**Answer**: Redirect channel (83% success) outperforms QR (65%) and notification (60%). Redirect is faster (57s vs 138s/148s), has immediate app open, and no notification dependency.

### 3. What percentage of failures are user-driven vs technical?
**Answer**:
- User-driven: 54.7% (89 aborts + 6 PIN failures + 0 consent denials = 95 / 172 failures)
- Technical: 14.0% (24 technical errors / 172 failures)
- System timeouts: 27.3% (47 expiries / 172 failures)
- Issuer issues: 7.0% (12 not eligible / 172 failures)

### 4. Which service providers need immediate attention?
**Answer**:
- **InsureOne** (35.7% success) - requesting unavailable documents
- **ADIB** (36.8% success) - integration misconfiguration
- Both need SP audit and document pre-check API.

### 5. How much does document availability impact success?
**Answer**: Surprisingly, the opposite of expected:
- **Documents ready (S10)**: 61.5% success
- **Documents missing (S11)**: 86.7% success
- Missing docs lead to HIGHER success due to user engagement/commitment.

### 6. Are there any unexpected status transitions?
**Answer**: Yes, several:
- **S21 -> S43** (37): Users abandon AFTER granting consent (unexpected)
- **S31 -> S41** (24): Technical error AFTER successful PIN (critical bug)
- **S10 -> S42** (25): Expiry despite docs being ready (UX urgency issue)
- **S11 -> Higher Success**: Missing docs correlate with higher completion (paradox)

### 7. What error codes are most common and fixable?
**Answer**:
- **issuer_not_found** (24 errors, 34.3%): Fixable via document pre-check API
- **dv_5xx** (11 errors, 15.7%): Fixable via backend hardening
- **signing_timeout** (6 errors, 8.6%): Fixable via retry logic
- **pin_incorrect** (12 errors, 17.1%): Fixable via PIN retry/recovery UX

### 8. How do iOS and Android compare across all metrics?
**Answer**:
| Metric | iOS | Android | Difference |
|--------|-----|---------|------------|
| Success Rate | 68.3% | 62.9% | iOS +5.4% |
| Journey Time | 146s | 137s | Android 6% faster |
| Technical Errors | 4.0% | 5.6% | Android 40% higher |
| User Aborts | 16.9% | 18.7% | Android 11% higher |

### 9. What is the average time to success vs failure?
**Answer**:
- **Success (S40)**: 63.5 seconds (median: 59s)
- **Failure (Non-S40)**: 290.7 seconds (median: 63s)
- **Key Insight**: Median is similar (59s vs 63s), but mean is inflated by 47 expiries at 900s each. Excluding expiries, failures are ~65-70 seconds.

### 10. Which status transitions have the highest failure rate?
**Answer**:
1. **S21 -> S43** (37 failures out of 405 S21s = 9.1% failure rate)
2. **S31 -> S41** (24 failures out of 352 S31s = 6.8% failure rate)
3. **S10 -> S42** (25 failures out of 343 S10s = 7.3% failure rate)
4. **S32 -> S43** (16 out of 16 = 100% failure rate - all PIN failures cascade)
5. **S12 -> S15** (12 failures out of 135 S12s = 8.9% failure rate)

---

## 16. Conclusion

This comprehensive analysis of 500 sharing requests (5,068 events) reveals that **UAE PASS Digital Documents sharing functionality achieves a 65.6% success rate**, with clear opportunities for improvement.

### Core Strengths
- Consent approval: 93.1% (excellent)
- PIN success: 95.7% (excellent)
- Document retrieval: 86.7% (excellent)
- Redirect channel: 83% success (strong)

### Critical Weaknesses
- Post-consent abandonment: 7.4% of all requests (fixable UX issue)
- Backend technical failures: 4.8% after successful PIN (critical bug)
- Expiry rate: 9.4% (UX urgency issue)
- Platform disparity: iOS 5.4% better than Android
- SP integration quality: 89% (DU) to 36% (InsureOne)

### Realistic Improvement Potential
By addressing the top 3 issues (post-consent abandonment, backend failures, expiries), success rate can improve from **65.6% to ~83%** (+17.2 percentage points), representing **+1,720 successful shares per week** (assuming 10K requests/week).

### Immediate Actions Required
1. Fix post-consent user experience (S21 -> S43)
2. Investigate and resolve backend failures after PIN (S31 -> S41)
3. Audit InsureOne and ADIB integrations
4. Implement document pre-check API
5. Reduce expiry rate through push notifications and TTL extension

This analysis provides a data-driven roadmap for improving UAE PASS Digital Documents sharing success rate and user experience.

---

## Appendix: Visualizations

All visualizations are saved in `D:\cluade\visualizations\`:

1. `01_terminal_status_distribution.png` - Terminal status pie and bar charts
2. `02_channel_performance.png` - Channel success rates and comparisons
3. `03_transition_heatmap.png` - Status transition heatmap
4. `04_critical_dropoffs.png` - Top drop-off points
5. `05_error_analysis.png` - Error code and source analysis
6. `06_service_provider_performance.png` - SP success rates and rankings
7. `07_platform_comparison.png` - iOS vs Android comparison
8. `08_missing_document_analysis.png` - Document availability impact
9. `09_user_behavior_patterns.png` - Consent, PIN, and abandonment analysis
10. `10_journey_path_analysis.png` - Journey patterns and lengths
11. `11_time_latency_analysis.png` - Latency and bottleneck analysis
12. `12_conversion_funnel.png` - Complete conversion funnel

---

**Report Generated**: 2026-01-09
**Analysis Tool**: Python (pandas, matplotlib, seaborn, plotly)
**Dataset**: `sharing_transactions_new_sample.csv` (500 requests, 5,068 events)
