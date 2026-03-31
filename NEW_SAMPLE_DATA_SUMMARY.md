# New Sample Data Summary

**Generated**: 2026-01-09
**File**: `sharing_transactions_new_sample.csv`
**Status Events**: 5,068
**Unique Requests**: 500
**Date Range**: November 1-28, 2025

---

## Key Changes from Previous Sample

### 1. New Columns Added ✅

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `previous_status` | String | The status code that came immediately before this one | `"S20"` |
| `status_history` | JSON Array | Complete ordered list of all statuses for this request | `["S00", "S01", "S02", "S08", "S10", "S20", "S21", "S30", "S31", "S40"]` |

### 2. Real Service Providers from csvdata-1.csv ✅

Uses actual SP names found in your production data:
- AAE, ADCB, ADIB, ADNIC, Arab Bank, Baraka, Beyon Money
- Botim, Commercial Bank of Dubai - Mobile, DU, Du Esim
- Emirates Islamic, ENBD Tablet Banking, Etisalat Retail/Business
- FAB Retail Banking, GIG, Lulu, National Bank of Fujairah
- National Bonds Corporation, Noor Capital, InsureOne

### 3. Channel-Specific Status Transitions ✅

**Notification Channel** (57.6% of requests):
```
S00 → S01 → S02 → S03 → S08 → ...
```

**QR Channel** (22.4% of requests):
```
S00 → S06 → S07 → S08 → ...
```

**Redirect Channel** (20.0% of requests):
```
S00 → S04 → S05 → S08 → ...
```

---

## Data Distribution

### Success Rate: 65.6%

| Terminal Status | Count | Percentage | Description |
|----------------|-------|------------|-------------|
| **S40** | 328 | **65.6%** | Success - Documents shared |
| S43 | 89 | 17.8% | User Aborted |
| S42 | 47 | 9.4% | Expired |
| S41 | 24 | 4.8% | Technical Error |
| S44 | 12 | 2.4% | Not Eligible |

### Channel Distribution

| Channel | Requests | Percentage |
|---------|----------|------------|
| Notification | 288 | 57.6% |
| QR | 112 | 22.4% |
| Redirect | 100 | 20.0% |

### Platform Distribution

| Platform | Requests | Percentage |
|----------|----------|------------|
| Android | 251 | 50.2% |
| iOS | 249 | 49.8% |

---

## Sample Journey Examples

### 1. Notification Channel - User Abandoned
```
REQ000001 - GIG
S00 (START)       @ 2025-11-23 04:09:00
S01 (S00)         @ 2025-11-23 04:09:03  [+3s]
S02 (S01)         @ 2025-11-23 04:09:07  [+4s]
S03 (S02)         @ 2025-11-23 04:09:12  [+5s]
S08 (S03)         @ 2025-11-23 04:09:19  [+7s]
S10 (S08)         @ 2025-11-23 04:09:21  [+2s]  - Docs ready
S20 (S10)         @ 2025-11-23 04:09:39  [+18s] - Awaiting consent
S21 (S20)         @ 2025-11-23 04:09:47  [+8s]  - Consent given
S43 (S21)         @ 2025-11-23 04:10:12  [+25s] - User aborted

Journey: S00 → S01 → S02 → S03 → S08 → S10 → S20 → S21 → S43
```

### 2. QR Channel - Success with Missing Docs
```
REQ000005 - Lulu
S00 (START)       @ 2025-11-18 08:25:00
S06 (S00)         @ 2025-11-18 08:25:02  [+2s]  - QR rendered
S07 (S06)         @ 2025-11-18 08:25:12  [+10s] - QR scanned
S08 (S07)         @ 2025-11-18 08:25:17  [+5s]  - Request viewed
S11 (S08)         @ 2025-11-18 08:25:19  [+2s]  - Docs missing
S12 (S11)         @ 2025-11-18 08:25:31  [+12s] - Doc request initiated
S13 (S12)         @ 2025-11-18 08:25:40  [+9s]  - Doc retrieved
S20 (S13)         @ 2025-11-18 08:25:54  [+14s] - Awaiting consent
S21 (S20)         @ 2025-11-18 08:26:01  [+7s]  - Consent given
S30 (S21)         @ 2025-11-18 08:26:03  [+2s]  - PIN requested
S31 (S30)         @ 2025-11-18 08:26:09  [+6s]  - PIN verified
S40 (S31)         @ 2025-11-18 08:26:12  [+3s]  - Success!

Journey: S00 → S06 → S07 → S08 → S11 → S12 → S13 → S20 → S21 → S30 → S31 → S40
```

### 3. Redirect Channel - Success
```
REQ000007 - Botim
S00 (START)       @ 2025-11-05 03:41:00
S04 (S00)         @ 2025-11-05 03:41:02  [+2s]  - Redirect launched
S05 (S04)         @ 2025-11-05 03:41:05  [+3s]  - Redirect landed
S08 (S05)         @ 2025-11-05 03:41:10  [+5s]  - Request viewed
S10 (S08)         @ 2025-11-05 03:41:11  [+1s]  - Docs ready
S20 (S10)         @ 2025-11-05 03:41:28  [+17s] - Awaiting consent
S21 (S20)         @ 2025-11-05 03:41:36  [+8s]  - Consent given
S30 (S21)         @ 2025-11-05 03:41:38  [+2s]  - PIN requested
S31 (S30)         @ 2025-11-05 03:41:45  [+7s]  - PIN verified
S40 (S31)         @ 2025-11-05 03:41:48  [+3s]  - Success!

Journey: S00 → S04 → S05 → S08 → S10 → S20 → S21 → S30 → S31 → S40
```

---

## Journey Pattern Types Included

The data includes 16 different realistic journey patterns:

### Success Paths (65.6%)
1. **notification_success_ready** - Notification, docs available
2. **notification_success_missing** - Notification, docs retrieved
3. **qr_success** - QR, docs available
4. **qr_success_missing** - QR, docs retrieved
5. **redirect_success** - Redirect, docs available
6. **redirect_success_missing** - Redirect, docs retrieved

### User-Driven Failures (20.2%)
7. **notification_abandoned** - User exits before completion
8. **redirect_abandoned** - User exits during redirect flow
9. **consent_rejected** - User declines consent
10. **qr_not_scanned** - QR rendered but never scanned

### Technical Failures (4.8%)
11. **tech_error** - Backend/network error after PIN
12. **qr_tech_error** - QR-specific technical failure

### PIN Failures (varies)
13. **pin_failed** - Wrong PIN or dismissed

### Missing Document Failures (2.4%)
14. **missing_not_found** - Document not at issuer
15. **missing_tech_error** - Error retrieving document

### Timeout Failures (9.4%)
16. **expired_before_consent** - Request TTL expired

---

## Data Quality Features

✅ **Realistic Latencies**: Step times match real-world patterns
✅ **Error Codes**: Proper error codes for S14, S15, S32, S41, S44
✅ **Error Sources**: issuer, network, dv, user_cancel
✅ **Missing Counts**: Accurate missing document counts in S11/S12
✅ **Platform Split**: Near 50/50 iOS/Android distribution
✅ **App Versions**: Real version numbers from production data
✅ **Document Types**: Realistic document combinations
✅ **Timestamps**: Full month of November 2025, realistic times

---

## Schema

```csv
request_id         - Unique request identifier (REQ000001 - REQ000500)
sp_id              - Service Provider name (from csvdata-1.csv)
channel            - notification | qr | redirect
platform           - android | ios
app_version        - e.g., "6.4.0", "6.3.0", "6.2.1"
required_docs      - JSON array: ["Emirates ID Card", "Passport"]
required_count     - Number of required documents (1-3)
status_code        - S00-S44
previous_status    - Previous status code in journey (empty for S00)
status_ts          - Timestamp: "2025-11-01 12:34:56"
step_latency_ms    - Milliseconds since previous status (0 for S00)
missing_count      - Count of missing docs (0-2)
error_code         - Error code (empty if no error)
error_source       - Error source: issuer | network | dv | user_cancel
status_history     - JSON array: ["S00", "S01", "S02", ..., "S40"]
```

---

## Usage Examples

### Query 1: Get Complete Journey for a Request
```python
import pandas as pd
import json

df = pd.read_csv('sharing_transactions_new_sample.csv')
request = df[df['request_id'] == 'REQ000001']

for _, row in request.iterrows():
    prev = row['previous_status'] if row['previous_status'] else 'START'
    print(f"{row['status_code']} <- {prev} @ {row['status_ts']}")
```

### Query 2: Success Rate by Channel
```python
df = pd.read_csv('sharing_transactions_new_sample.csv')

# Get last status for each request
last_statuses = df.groupby('request_id').last()

success_by_channel = last_statuses.groupby('channel').apply(
    lambda x: (x['status_code'] == 'S40').sum() / len(x) * 100
)
print(success_by_channel)
```

### Query 3: Find All Requests with Missing Docs
```python
df = pd.read_csv('sharing_transactions_new_sample.csv')

missing_doc_requests = df[df['status_code'] == 'S11']['request_id'].unique()
print(f"Requests with missing docs: {len(missing_doc_requests)}")
```

### Query 4: Average Journey Time to Success
```python
df = pd.read_csv('sharing_transactions_new_sample.csv')

successful = df[df.groupby('request_id')['status_code'].transform('last') == 'S40']
journey_times = successful.groupby('request_id')['step_latency_ms'].sum() / 1000

print(f"Average journey time: {journey_times.mean():.1f} seconds")
print(f"Median journey time: {journey_times.median():.1f} seconds")
```

---

## Files Generated

1. **sharing_transactions_new_sample.csv** (5,068 rows) - Main data file
2. **generate_new_sample_data.py** - Generation script (reusable)
3. **NEW_SAMPLE_DATA_SUMMARY.md** - This document

---

## Next Steps

1. ✅ Sample data created with new columns
2. ⏭️ Update analysis scripts to use new columns
3. ⏭️ Update dashboard to visualize status_history
4. ⏭️ Test reporting queries with new schema
5. ⏭️ Share with engineering teams as reference for implementation

---

## Regenerating Data

To create a new sample with different parameters:

```bash
python generate_new_sample_data.py
```

You can modify:
- Number of requests (default: 500)
- Journey pattern weights
- Service providers list
- Document types
- Date range
- App versions

---

**Questions or Issues?**
The generation script is fully documented and can be modified to suit your specific needs.
