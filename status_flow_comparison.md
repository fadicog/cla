# UAE PASS DV - Status Flow v1 vs v2 Comparison

**Document Version:** 1.0
**Last Updated:** 2025-11-26
**Purpose:** Side-by-side comparison of v1 (21 states) vs v2 (23 states)

---

## Executive Summary

**v2 introduces 3 new statuses** to address critical gaps in granularity:

| New Status | Code | Purpose | Impact |
|-----------|------|---------|--------|
| ✅ CHECKING_DOCUMENT_AVAILABILITY | 115 | Auto-check at opening | Measure doc availability rate |
| ✅ USER_TRIGGERED_DOCUMENT_REQUEST | 210 | Capture user intent | Track request conversion rate |
| ✅ DOCUMENTS_REQUEST_IN_PROGRESS | 215 | Track fetch duration | Monitor issuer SLAs |

**Result:** +2 states (21 → 23), +3 new metrics capabilities, 0 breaking changes

---

## 1. State Count Comparison

### v1 (Original Flow)

```
Total States: 21

Initial/Opening:     2 states (100, 110)
Document Flow:       4 states (200, 210/220, 230, 300)
Consent Flow:        3 states (310, 320, 330)
PIN Flow:            4 states (340, 350, 360, 370)
Success:             1 state  (400)
Failures:            7 states (510, 520, 530, 540, 550, 560, 600)
```

### v2 (Revised Flow)

```
Total States: 23 (+2 from v1)

Initial/Opening:     3 states (100, 110, 115) ← +1 NEW
Document Flow:       5 states (200, 210, 215, 220, 230, 300) ← +2 NEW
Consent Flow:        3 states (310, 320, 330)
PIN Flow:            4 states (340, 350, 360, 370)
Success:             1 state  (400)
Failures:            7 states (510, 520, 530, 540, 550, 560, 600)
```

**Change:** +3 new states, but status 210 was revised (not net new), so **+2 net new states**

---

## 2. Flow Diagrams Comparison

### v1 Flow (Opening Sequence)

```
100 REQUEST_CREATED
  ↓
110 OPENED
  ↓
[Implicit document check - not tracked]
  ↓
200 DOCUMENTS_NOT_IN_VAULT  OR  300 DOCUMENTS_AVAILABLE
```

**Problem:** Cannot tell if docs were present at opening time

---

### v2 Flow (Opening Sequence)

```
100 REQUEST_CREATED
  ↓
110 OPENED
  ↓
115 CHECKING_DOCUMENT_AVAILABILITY ← NEW (explicit tracking)
  ↓
  ├─→ 300 DOCUMENTS_AVAILABLE (tracked: docs present at opening)
  └─→ 200 DOCUMENTS_NOT_IN_VAULT (tracked: docs missing at opening)
```

**Solution:** Explicit status 115 captures availability at opening moment

---

### v1 Flow (Document Request Sequence)

```
200 DOCUMENTS_NOT_IN_VAULT
  ↓
[User action implicit - when did user request?]
  ↓
210 DOCUMENTS_REQUEST_INITIATED
  ↓
[Fetch duration not measured]
  ↓
220 PARTIAL_SUCCESS  OR  230 REQUEST_FAILED
```

**Problem:** Cannot measure fetch duration or user intent timing

---

### v2 Flow (Document Request Sequence)

```
200 DOCUMENTS_NOT_IN_VAULT
  ↓
210 USER_TRIGGERED_DOCUMENT_REQUEST ← NEW (explicit user action)
  ↓
215 DOCUMENTS_REQUEST_IN_PROGRESS ← NEW (fetch duration tracking)
  ↓
  ├─→ 300 DOCUMENTS_ALL_AVAILABLE_POST_REQUEST
  ├─→ 220 DOCUMENTS_REQUEST_PARTIAL_SUCCESS
  └─→ 230 DOCUMENTS_REQUEST_FAILED
```

**Solution:** Explicit statuses 210 and 215 capture user intent and fetch duration

---

## 3. Metrics Comparison

### v1 Metrics (What We Could Measure)

| Metric | v1 Capability | Limitation |
|--------|--------------|------------|
| Document availability rate | ❌ **Cannot measure** | No checkpoint at opening time |
| Request conversion rate | ❌ **Cannot measure** | No explicit user action tracking |
| Issuer fetch duration | ❌ **Cannot measure** | No in-progress state |
| Partial success handling | ⚠️ **Partial** | Could count 220, but not context |
| Consent rejection rate | ✅ **Can measure** | Status 510 tracked |
| PIN failure rate | ✅ **Can measure** | Status 370, 520 tracked |
| Completion rate | ✅ **Can measure** | Status 400 tracked |

**Total Capabilities:** 3/7 metrics (**43%**)

---

### v2 Metrics (What We Can Measure)

| Metric | v2 Capability | How |
|--------|--------------|-----|
| Document availability rate | ✅ **Can measure** | Status 115 → 300 vs 115 → 200 |
| Request conversion rate | ✅ **Can measure** | Status 200 → 210 conversion |
| Issuer fetch duration | ✅ **Can measure** | Timestamp delta: 215 → 300/220/230 |
| Partial success handling | ✅ **Can measure** | Status 220 with full context |
| Consent rejection rate | ✅ **Can measure** | Status 510 tracked |
| PIN failure rate | ✅ **Can measure** | Status 370, 520 tracked |
| Completion rate | ✅ **Can measure** | Status 400 tracked |

**Total Capabilities:** 7/7 metrics (**100%**) ✅

**Improvement:** +4 new metrics capabilities (+57%)

---

## 4. Detailed State Changes

### 4.1 New State: 115 CHECKING_DOCUMENT_AVAILABILITY

**v1 Behavior:**
- Implicit check happened after 110 OPENED
- No status code assigned
- No timestamp recorded
- No analytics event

**v2 Behavior:**
```
Status: 115 CHECKING_DOCUMENT_AVAILABILITY
Trigger: Automatic after 110 OPENED
Duration: <1 second (DB query)
Next States: 300 (all present) OR 200 (missing)
Analytics: Track documents_available_at_opening (boolean)
```

**Business Impact:**
```sql
-- NEW query in v2:
SELECT
  COUNT(*) FILTER (WHERE status_115_to_300 = TRUE) / COUNT(*) * 100
  AS pct_docs_ready_at_opening
FROM sharing_requests;

-- Example result: 62% of requests have docs ready at opening
-- → Indicates good issuer coverage
```

---

### 4.2 Revised State: 210 USER_TRIGGERED_DOCUMENT_REQUEST

**v1 Behavior:**
```
Status: 210 DOCUMENTS_REQUEST_INITIATED
Trigger: [Ambiguous - auto after 200? User action?]
Purpose: Document request started
Next: 220/230
```

**v2 Behavior:**
```
Status: 210 USER_TRIGGERED_DOCUMENT_REQUEST
Trigger: User explicitly taps "Request Missing Documents" button
Purpose: Capture user intent timestamp
Next: 215 DOCUMENTS_REQUEST_IN_PROGRESS
Analytics: Track request_conversion_rate (200→210)
```

**Business Impact:**
```sql
-- NEW funnel analysis in v2:
SELECT
  COUNT(*) FILTER (WHERE last_status = 200 AND final_status = 600) AS abandoned_at_200,
  COUNT(*) FILTER (WHERE status = 210) AS triggered_request,
  COUNT(*) FILTER (WHERE status = 210) / COUNT(*) FILTER (WHERE status = 200) * 100 AS conversion_rate
FROM sharing_requests;

-- Example result: 30% of users at 200 abandon without requesting
-- → Redesign "Request Documents" CTA
```

---

### 4.3 New State: 215 DOCUMENTS_REQUEST_IN_PROGRESS

**v1 Behavior:**
- No intermediate state between 210 and 220/230
- Fetch duration not measured
- No loading state for user
- Cannot identify slow issuers

**v2 Behavior:**
```
Status: 215 DOCUMENTS_REQUEST_IN_PROGRESS
Trigger: Automatic after 210
Duration: 5-30 seconds (issuer API calls)
Next States: 300 (all received) OR 220 (partial) OR 230 (failed)
Analytics: Track issuer_fetch_duration_ms
```

**Business Impact:**
```sql
-- NEW issuer SLA monitoring in v2:
SELECT
  issuer_id,
  AVG(timestamp_300 - timestamp_215) AS avg_fetch_seconds,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY timestamp_300 - timestamp_215) AS p95_fetch_seconds
FROM sharing_requests
WHERE status_215 IS NOT NULL
GROUP BY issuer_id
HAVING avg_fetch_seconds > 10;

-- Example result:
-- Issuer A: avg 3.2s, p95 5.1s (good)
-- Issuer B: avg 18.7s, p95 29.3s (slow - negotiate SLA)
```

---

## 5. Flow Path Comparison

### Happy Path (Docs Already Available)

**v1 Flow:**
```
100 → 110 → [implicit check] → 300 → 310 → 320 → 330 → 400
(7 states, 1 implicit)
```

**v2 Flow:**
```
100 → 110 → 115 → 300 → 310 → 320 → 330 → 400
(8 states, all explicit)
```

**Change:** +1 state (115), **no behavioral change for user**, +analytics

---

### Happy Path (Need to Request Docs)

**v1 Flow:**
```
100 → 110 → [implicit check] → 200 → 210 → [implicit fetch] → 220/230 → ...
(Unknown fetch duration)
```

**v2 Flow:**
```
100 → 110 → 115 → 200 → 210 → 215 → 220/230/300 → ...
(Measured fetch duration: timestamp_215 to timestamp_220/230/300)
```

**Change:** +2 states (115, 215), +fetch duration tracking

---

### Failure Path (User Rejects Consent)

**v1 Flow:**
```
100 → 110 → 300 → 310 → 510
```

**v2 Flow:**
```
100 → 110 → 115 → 300 → 310 → 510
```

**Change:** +1 state (115), no other changes

---

## 6. Analytics Query Comparison

### Query 1: Document Availability Rate

**v1 Query:**
```sql
-- CANNOT MEASURE (no checkpoint at opening)
-- Workaround: Infer from presence of status 200
SELECT
  COUNT(*) FILTER (WHERE status IN (200, 210, 220, 230)) AS missing_docs_count,
  COUNT(*) AS total_requests
FROM sharing_requests;

-- Problem: Doesn't tell us if docs were missing at opening or became available later
```

**v2 Query:**
```sql
-- PRECISE MEASUREMENT
SELECT
  COUNT(*) FILTER (WHERE status_115_next = 300) AS docs_ready_at_opening,
  COUNT(*) FILTER (WHERE status_115_next = 200) AS docs_missing_at_opening,
  COUNT(*) AS total_requests,
  COUNT(*) FILTER (WHERE status_115_next = 300) / COUNT(*) * 100 AS availability_rate_pct
FROM sharing_requests
WHERE status_115_timestamp IS NOT NULL;

-- Example result: 62% availability at opening
```

---

### Query 2: Request Conversion Rate

**v1 Query:**
```sql
-- CANNOT MEASURE (no explicit user action tracking)
-- Workaround: Count status 210 presence
SELECT
  COUNT(*) FILTER (WHERE status = 210) AS initiated_requests,
  COUNT(*) FILTER (WHERE status = 200) AS missing_docs_cases
FROM sharing_requests;

-- Problem: Doesn't tell us if user actively requested or system auto-triggered
```

**v2 Query:**
```sql
-- PRECISE MEASUREMENT
SELECT
  COUNT(*) FILTER (WHERE status = 210) AS user_triggered_requests,
  COUNT(*) FILTER (WHERE status = 200) AS missing_docs_cases,
  COUNT(*) FILTER (WHERE status = 210) / COUNT(*) FILTER (WHERE status = 200) * 100 AS conversion_rate_pct
FROM sharing_requests;

-- Example result: 68% of users at 200 tap "Request Documents"
-- → 32% abandon without requesting (opportunity to improve UX)
```

---

### Query 3: Issuer Performance

**v1 Query:**
```sql
-- CANNOT MEASURE (no in-progress state, no timestamps)
-- No workaround available
```

**v2 Query:**
```sql
-- PRECISE MEASUREMENT
SELECT
  issuer_id,
  AVG(EXTRACT(EPOCH FROM (timestamp_300 - timestamp_215))) AS avg_fetch_seconds,
  COUNT(*) AS request_count
FROM sharing_requests
WHERE status_215_timestamp IS NOT NULL AND status_300_timestamp IS NOT NULL
GROUP BY issuer_id
ORDER BY avg_fetch_seconds DESC;

-- Example result:
-- ICP: 3.2 seconds (fast)
-- Bank A: 18.7 seconds (slow - negotiate SLA)
```

---

## 7. Breaking Changes Assessment

### Database Schema

**v1 Schema:**
```sql
CREATE TABLE sharing_requests (
  id UUID PRIMARY KEY,
  correlation_id TEXT UNIQUE,
  current_status INTEGER,
  status_timestamps JSONB,
  -- ... other fields
);
```

**v2 Schema:**
```sql
CREATE TABLE sharing_requests (
  id UUID PRIMARY KEY,
  correlation_id TEXT UNIQUE,
  current_status INTEGER,
  status_timestamps JSONB,

  -- NEW COLUMNS (backwards compatible - nullable)
  status_115_timestamp TIMESTAMP,
  status_210_timestamp TIMESTAMP,
  status_215_timestamp TIMESTAMP,
  documents_available_at_opening BOOLEAN,
  user_triggered_request BOOLEAN,
  issuer_fetch_duration_ms INTEGER,

  -- ... other fields
);
```

**Breaking Changes:** ❌ **NONE** (new columns are nullable, default NULL)

**Migration Strategy:** Add columns, backfill with inferred values

---

### API Endpoints

**v1 Endpoints:**
```
POST /api/sharing-requests/{id}/status/110
POST /api/sharing-requests/{id}/status/200
POST /api/sharing-requests/{id}/status/210
POST /api/sharing-requests/{id}/status/220
```

**v2 Endpoints:**
```
POST /api/sharing-requests/{id}/status/110
POST /api/sharing-requests/{id}/status/115  ← NEW (auto-triggered by backend)
POST /api/sharing-requests/{id}/status/200
POST /api/sharing-requests/{id}/status/210  ← REVISED (user-triggered button)
POST /api/sharing-requests/{id}/status/215  ← NEW (auto-triggered by backend)
POST /api/sharing-requests/{id}/status/220
```

**Breaking Changes:** ❌ **NONE** (new endpoints, existing endpoints unchanged)

**Client Changes Required:**
- Frontend: Add button click handler for 210
- Frontend: Show loading state during 215
- Backend: Auto-trigger 115 after 110
- Backend: Auto-trigger 215 after 210

---

### Frontend UI

**v1 UI:**
```
[User opens request]
  ↓
[Show loading...]
  ↓
IF docs missing:
  [Show "Missing Documents" screen with "Request" button]
  [On button click → 210]
  [Show loading...]
  [Show result: success/partial/failed]
```

**v2 UI:**
```
[User opens request]
  ↓
[Show brief loading during 115 (<1s)] ← NEW
  ↓
IF docs missing:
  [Show "Missing Documents" screen with "Request" button]
  [On button click → 210] ← Track analytics event
  [Show loading during 215 (5-30s)] ← NEW (explicit loading state)
  [Show result: success/partial/failed]
```

**Breaking Changes:** ❌ **NONE** (enhanced UX, not breaking)

---

## 8. Migration Path

### Step 1: Database Migration

```sql
-- Add new columns (backwards compatible)
ALTER TABLE sharing_requests ADD COLUMN status_115_timestamp TIMESTAMP;
ALTER TABLE sharing_requests ADD COLUMN status_210_timestamp TIMESTAMP;
ALTER TABLE sharing_requests ADD COLUMN status_215_timestamp TIMESTAMP;
ALTER TABLE sharing_requests ADD COLUMN documents_available_at_opening BOOLEAN;
ALTER TABLE sharing_requests ADD COLUMN user_triggered_request BOOLEAN;
ALTER TABLE sharing_requests ADD COLUMN issuer_fetch_duration_ms INTEGER;

-- Backfill historical data (inferred values)
UPDATE sharing_requests
SET
  status_115_timestamp = status_110_timestamp + INTERVAL '0.5 seconds',
  documents_available_at_opening = (status_200_timestamp IS NULL)
WHERE status_110_timestamp IS NOT NULL AND status_115_timestamp IS NULL;

UPDATE sharing_requests
SET
  status_210_timestamp = status_220_timestamp - INTERVAL '1 second',
  user_triggered_request = TRUE
WHERE status_220_timestamp IS NOT NULL AND status_210_timestamp IS NULL;

UPDATE sharing_requests
SET
  status_215_timestamp = status_210_timestamp + INTERVAL '0.5 seconds',
  issuer_fetch_duration_ms = EXTRACT(EPOCH FROM (status_220_timestamp - status_210_timestamp)) * 1000
WHERE status_210_timestamp IS NOT NULL AND status_220_timestamp IS NOT NULL AND status_215_timestamp IS NULL;
```

---

### Step 2: Backend Code Migration

**Add new status handlers:**

```javascript
// NEW: Auto-triggered after 110 OPENED
async function handleStatus110(requestId) {
  await updateStatus(requestId, 110);

  // Auto-trigger 115
  await handleStatus115(requestId);
}

// NEW: Check document availability
async function handleStatus115(requestId) {
  const request = await getRequest(requestId);
  const mandatoryDocs = request.mandatoryDocuments;
  const userDocs = await getUserDocuments(request.userId);

  const allPresent = mandatoryDocs.every(doc =>
    userDocs.some(ud => ud.type === doc.type && !ud.expired)
  );

  await updateStatus(requestId, 115, {
    documents_available_at_opening: allPresent
  });

  // Auto-transition
  if (allPresent) {
    await handleStatus300(requestId);
  } else {
    await handleStatus200(requestId);
  }
}

// REVISED: User-triggered (not automatic)
async function handleStatus210(requestId) {
  await updateStatus(requestId, 210, {
    user_triggered_request: true
  });

  // Auto-trigger 215
  await handleStatus215(requestId);
}

// NEW: Fetch documents from issuers
async function handleStatus215(requestId) {
  const startTime = Date.now();
  await updateStatus(requestId, 215);

  const request = await getRequest(requestId);
  const results = await fetchDocumentsFromIssuers(request);

  const duration = Date.now() - startTime;

  if (results.allSuccess) {
    await handleStatus300(requestId, { issuer_fetch_duration_ms: duration });
  } else if (results.partialSuccess) {
    await handleStatus220(requestId, { issuer_fetch_duration_ms: duration });
  } else {
    await handleStatus230(requestId, { issuer_fetch_duration_ms: duration });
  }
}
```

---

### Step 3: Frontend Migration

**Update button handler:**

```javascript
// REVISED: Explicit tracking
async function onRequestDocumentsClick() {
  // Track analytics event
  analytics.track('user_clicked_request_documents', {
    request_id: requestId,
    timestamp: Date.now()
  });

  // Trigger status 210 (user action)
  await api.updateStatus(requestId, 210);

  // Show loading state (status 215 in progress)
  showLoading('Requesting documents from issuers...');

  // Backend will auto-transition 210 → 215 → 220/230/300
  await pollStatusUntil(requestId, [220, 230, 300]);

  hideLoading();
  showResult();
}
```

---

## 9. Rollback Plan

If v2 causes issues, rollback is simple:

**Step 1: Disable new status transitions**
```javascript
// Revert to v1 behavior (skip 115, 210, 215)
async function handleStatus110(requestId) {
  await updateStatus(requestId, 110);

  // SKIP 115, go directly to 200/300
  const docsAvailable = await checkDocuments(requestId);
  if (docsAvailable) {
    await handleStatus300(requestId);
  } else {
    await handleStatus200(requestId);
  }
}
```

**Step 2: Keep database columns** (no data loss)
```sql
-- New columns remain, but are not populated
-- No breaking changes, existing v1 queries still work
```

**Result:** v2 → v1 rollback has **zero data loss**, **zero downtime**

---

## 10. Recommendation Matrix

| Criteria | v1 | v2 | Winner |
|----------|----|----|--------|
| **Metrics Granularity** | 43% | 100% | ✅ v2 |
| **Analytics Capabilities** | Limited | Comprehensive | ✅ v2 |
| **Implementation Complexity** | Simple | Moderate | v1 |
| **Database Schema Changes** | None | +6 columns | v1 |
| **Breaking Changes** | N/A | None | ✅ Tie |
| **Rollback Complexity** | N/A | Simple | ✅ v2 |
| **Business Value** | Baseline | High | ✅ v2 |
| **User Experience Impact** | Baseline | Enhanced | ✅ v2 |
| **Technical Debt** | Growing | Resolved | ✅ v2 |

**Overall Winner:** ✅ **v2**

---

## 11. Decision Recommendation

### Approve v2 Flow (23 States) ✅

**Rationale:**
1. **+4 new metrics capabilities** (57% improvement)
2. **Zero breaking changes** (backwards compatible)
3. **Simple rollback path** (no data loss)
4. **High business value** (issuer SLA monitoring, conversion tracking)
5. **Enhanced UX** (explicit loading states, better feedback)
6. **Resolves technical debt** (implicit checks now explicit)

**Implementation Priority:** **HIGH**

**Timeline:**
- Week 1: Database migration + backfill
- Week 2: Backend status handlers (115, 210, 215)
- Week 3: Frontend UI updates + analytics
- Week 4: QA + production rollout

**Risk Level:** **LOW** (backwards compatible, simple rollback)

---

## Appendix: Full State List Side-by-Side

| Code | v1 Status Name | v2 Status Name | Change |
|------|---------------|----------------|--------|
| 100 | REQUEST_CREATED | REQUEST_CREATED | Same |
| 110 | OPENED | OPENED | Same |
| 115 | ❌ Not present | ✅ CHECKING_DOCUMENT_AVAILABILITY | **NEW** |
| 200 | DOCUMENTS_NOT_IN_VAULT | DOCUMENTS_NOT_IN_VAULT | Same |
| 210 | DOCUMENTS_REQUEST_INITIATED | USER_TRIGGERED_DOCUMENT_REQUEST | **REVISED** |
| 215 | ❌ Not present | ✅ DOCUMENTS_REQUEST_IN_PROGRESS | **NEW** |
| 220 | DOCUMENTS_REQUEST_PARTIAL_SUCCESS | DOCUMENTS_REQUEST_PARTIAL_SUCCESS | Same |
| 230 | DOCUMENTS_REQUEST_FAILED | DOCUMENTS_REQUEST_FAILED | Same |
| 300 | DOCUMENTS_AVAILABLE | DOCUMENTS_AVAILABLE | Same |
| 310 | READY_TO_CONSENT | READY_TO_CONSENT | Same |
| 320 | CONSENT_GIVEN | CONSENT_GIVEN | Same |
| 330 | SHARING_INITIATED | SHARING_INITIATED | Same |
| 340 | PIN_REQUIRED | PIN_REQUIRED | Same |
| 350 | PIN_ENTERED | PIN_ENTERED | Same |
| 360 | PIN_VALIDATION_SUCCESS | PIN_VALIDATION_SUCCESS | Same |
| 370 | PIN_VALIDATION_FAILED | PIN_VALIDATION_FAILED | Same |
| 400 | SHARED_SUCCESSFULLY | SHARED_SUCCESSFULLY | Same |
| 510 | FAILURE_CONSENT_REJECTED | FAILURE_CONSENT_REJECTED | Same |
| 520 | FAILURE_PIN_ATTEMPTS_EXCEEDED | FAILURE_PIN_ATTEMPTS_EXCEEDED | Same |
| 530 | FAILURE_SESSION_EXPIRED | FAILURE_SESSION_EXPIRED | Same |
| 540 | FAILURE_TECHNICAL_ERROR | FAILURE_TECHNICAL_ERROR | Same |
| 550 | FAILURE_ISSUER_ERROR | FAILURE_ISSUER_ERROR | Same |
| 560 | FAILURE_DOCUMENTS_NOT_AVAILABLE | FAILURE_DOCUMENTS_NOT_AVAILABLE | Same |
| 600 | ABANDONED_BY_USER | ABANDONED_BY_USER | Same |

**Summary:**
- ✅ 3 new/revised statuses (115, 210, 215)
- ✅ 20 unchanged statuses
- ✅ 0 removed statuses
- ✅ **Total: 23 states**

---

**Document Version:** 1.0
**Author:** Product Management / Engineering
**Review Status:** Ready for stakeholder review
**Next Steps:** Approve v2 for implementation
