# UAE PASS DV - Status Flow Migration Mapping (v1 → v2)

**Version:** 1.0
**Last Updated:** 2025-11-26
**Purpose:** Complete migration guide for upgrading from v1 (21 states) to v2 (23 states)

---

## Executive Summary

This document provides detailed mapping for migrating from v1 to v2 status flow system.

**Migration Summary:**
- **Total v1 states:** 21
- **Total v2 states:** 23
- **Net new states:** +2 (actually +3 new, -1 revised)
- **Breaking changes:** 0
- **Data loss risk:** None
- **Rollback difficulty:** Easy

---

## 1. Complete State Mapping

| v1 Code | v1 Name | v2 Code | v2 Name | Change Type |
|---------|---------|---------|---------|-------------|
| 100 | REQUEST_CREATED | 100 | REQUEST_CREATED | ✅ No change |
| 110 | OPENED | 110 | OPENED | ✅ No change |
| ❌ N/A | ❌ N/A | **115** | **CHECKING_DOCUMENT_AVAILABILITY** | ✅ NEW |
| 200 | DOCUMENTS_NOT_IN_VAULT | 200 | DOCUMENTS_NOT_IN_VAULT | ✅ No change |
| 210 | DOCUMENTS_REQUEST_INITIATED | **210** | **USER_TRIGGERED_DOCUMENT_REQUEST** | ⚠️ REVISED (semantics) |
| ❌ N/A | ❌ N/A | **215** | **DOCUMENTS_REQUEST_IN_PROGRESS** | ✅ NEW |
| 220 | DOCUMENTS_REQUEST_PARTIAL_SUCCESS | 220 | DOCUMENTS_REQUEST_PARTIAL_SUCCESS | ✅ No change |
| 230 | DOCUMENTS_REQUEST_FAILED | 230 | DOCUMENTS_REQUEST_FAILED | ✅ No change |
| 300 | DOCUMENTS_AVAILABLE | 300 | DOCUMENTS_AVAILABLE | ✅ No change |
| 310 | READY_TO_CONSENT | 310 | READY_TO_CONSENT | ✅ No change |
| 320 | CONSENT_GIVEN | 320 | CONSENT_GIVEN | ✅ No change |
| 330 | SHARING_INITIATED | 330 | SHARING_INITIATED | ✅ No change |
| 340 | PIN_REQUIRED | 340 | PIN_REQUIRED | ✅ No change |
| 350 | PIN_ENTERED | 350 | PIN_ENTERED | ✅ No change |
| 360 | PIN_VALIDATION_SUCCESS | 360 | PIN_VALIDATION_SUCCESS | ✅ No change |
| 370 | PIN_VALIDATION_FAILED | 370 | PIN_VALIDATION_FAILED | ✅ No change |
| 400 | SHARED_SUCCESSFULLY | 400 | SHARED_SUCCESSFULLY | ✅ No change |
| 510 | FAILURE_CONSENT_REJECTED | 510 | FAILURE_CONSENT_REJECTED | ✅ No change |
| 520 | FAILURE_PIN_ATTEMPTS_EXCEEDED | 520 | FAILURE_PIN_ATTEMPTS_EXCEEDED | ✅ No change |
| 530 | FAILURE_SESSION_EXPIRED | 530 | FAILURE_SESSION_EXPIRED | ✅ No change |
| 540 | FAILURE_TECHNICAL_ERROR | 540 | FAILURE_TECHNICAL_ERROR | ✅ No change |
| 550 | FAILURE_ISSUER_ERROR | 550 | FAILURE_ISSUER_ERROR | ✅ No change |
| 560 | FAILURE_DOCUMENTS_NOT_AVAILABLE | 560 | FAILURE_DOCUMENTS_NOT_AVAILABLE | ✅ No change |
| 600 | ABANDONED_BY_USER | 600 | ABANDONED_BY_USER | ✅ No change |

**Summary:**
- ✅ **20 states unchanged**
- ⚠️ **1 state revised** (210: name + semantics change)
- ✅ **2 states added** (115, 215)
- **Total: 23 states in v2**

---

## 2. New Status Details

### 2.1 Status 115: CHECKING_DOCUMENT_AVAILABILITY

**Position:** Between 110 (OPENED) and 200/300

**v1 Behavior (Implicit):**
```
110 OPENED
  ↓ [implicit document check - not tracked]
200 DOCUMENTS_NOT_IN_VAULT OR 300 DOCUMENTS_AVAILABLE
```

**v2 Behavior (Explicit):**
```
110 OPENED
  ↓ [automatic trigger]
115 CHECKING_DOCUMENT_AVAILABILITY
  ↓
  ├→ 300 DOCUMENTS_AVAILABLE (all present)
  └→ 200 DOCUMENTS_NOT_IN_VAULT (missing)
```

**Migration Strategy:**
```sql
-- Add new column
ALTER TABLE sharing_requests ADD COLUMN status_115_timestamp TIMESTAMP;
ALTER TABLE sharing_requests ADD COLUMN documents_available_at_opening BOOLEAN;

-- Backfill historical data
UPDATE sharing_requests
SET
  status_115_timestamp = status_110_timestamp + INTERVAL '0.5 seconds',
  documents_available_at_opening = (status_200_timestamp IS NULL AND status_300_timestamp IS NOT NULL)
WHERE
  status_110_timestamp IS NOT NULL
  AND status_115_timestamp IS NULL;
```

**Code Changes:**
```javascript
// v1 (old):
async function handleStatus110(requestId) {
  await updateStatus(requestId, 110);
  const docsAvailable = await checkDocuments(requestId);
  if (docsAvailable) {
    await handleStatus300(requestId);
  } else {
    await handleStatus200(requestId);
  }
}

// v2 (new):
async function handleStatus110(requestId) {
  await updateStatus(requestId, 110);
  await handleStatus115(requestId); // Auto-trigger
}

async function handleStatus115(requestId) {
  const docsAvailable = await checkDocuments(requestId);
  await updateStatus(requestId, 115, { documents_available_at_opening: docsAvailable });
  if (docsAvailable) {
    await handleStatus300(requestId);
  } else {
    await handleStatus200(requestId);
  }
}
```

---

### 2.2 Status 210: USER_TRIGGERED_DOCUMENT_REQUEST (Revised)

**Change:** Name + semantics clarification

**v1 Behavior (Ambiguous):**
```
210 DOCUMENTS_REQUEST_INITIATED
Trigger: [Unclear - automatic or user-initiated?]
```

**v2 Behavior (Explicit):**
```
210 USER_TRIGGERED_DOCUMENT_REQUEST
Trigger: User explicitly taps "Request Missing Documents" button
```

**Migration Strategy:**
```sql
-- Add flag to track user action
ALTER TABLE sharing_requests ADD COLUMN user_triggered_request BOOLEAN;

-- Backfill: Assume all v1 status 210 records were user-triggered
UPDATE sharing_requests
SET user_triggered_request = TRUE
WHERE status_210_timestamp IS NOT NULL
  AND user_triggered_request IS NULL;
```

**Code Changes:**
```javascript
// v1 (old - ambiguous):
async function requestDocuments(requestId) {
  await updateStatus(requestId, 210);
  await fetchDocuments(requestId);
}

// v2 (new - explicit):
async function onUserClickRequestDocuments(requestId) {
  // Track analytics: user clicked button
  analytics.track('user_clicked_request_documents', { request_id: requestId });

  // Update status (user action)
  await updateStatus(requestId, 210, { user_triggered_request: true });

  // Auto-trigger status 215
  await handleStatus215(requestId);
}
```

---

### 2.3 Status 215: DOCUMENTS_REQUEST_IN_PROGRESS

**Position:** Between 210 (USER_TRIGGERED_REQUEST) and 220/230/300

**v1 Behavior (Implicit):**
```
210 DOCUMENTS_REQUEST_INITIATED
  ↓ [implicit fetch - duration not measured]
220/230/300 (outcome)
```

**v2 Behavior (Explicit):**
```
210 USER_TRIGGERED_DOCUMENT_REQUEST
  ↓ [automatic trigger]
215 DOCUMENTS_REQUEST_IN_PROGRESS
  ↓ [5-30 seconds - measured]
  ├→ 300 DOCUMENTS_ALL_AVAILABLE_POST_REQUEST
  ├→ 220 DOCUMENTS_REQUEST_PARTIAL_SUCCESS
  └→ 230 DOCUMENTS_REQUEST_FAILED
```

**Migration Strategy:**
```sql
-- Add new columns
ALTER TABLE sharing_requests ADD COLUMN status_215_timestamp TIMESTAMP;
ALTER TABLE sharing_requests ADD COLUMN issuer_fetch_duration_ms INTEGER;

-- Backfill historical data
UPDATE sharing_requests
SET
  status_215_timestamp = status_210_timestamp + INTERVAL '0.5 seconds'
WHERE
  status_210_timestamp IS NOT NULL
  AND status_215_timestamp IS NULL;

-- Calculate fetch duration
UPDATE sharing_requests
SET
  issuer_fetch_duration_ms = EXTRACT(EPOCH FROM (
    COALESCE(status_220_timestamp, status_230_timestamp, status_300_timestamp) - status_215_timestamp
  )) * 1000
WHERE
  status_215_timestamp IS NOT NULL
  AND (status_220_timestamp IS NOT NULL OR status_230_timestamp IS NOT NULL OR status_300_timestamp IS NOT NULL)
  AND issuer_fetch_duration_ms IS NULL;
```

**Code Changes:**
```javascript
// v1 (old):
async function handleStatus210(requestId) {
  await updateStatus(requestId, 210);
  const results = await fetchDocumentsFromIssuers(requestId);
  if (results.allSuccess) {
    await handleStatus300(requestId);
  } else if (results.partialSuccess) {
    await handleStatus220(requestId);
  } else {
    await handleStatus230(requestId);
  }
}

// v2 (new):
async function handleStatus210(requestId) {
  await updateStatus(requestId, 210, { user_triggered_request: true });
  await handleStatus215(requestId); // Auto-trigger
}

async function handleStatus215(requestId) {
  const startTime = Date.now();
  await updateStatus(requestId, 215);

  const results = await fetchDocumentsFromIssuers(requestId);
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

## 3. Flow Path Migration

### 3.1 Happy Path (Docs Ready at Opening)

**v1 Flow:**
```
100 REQUEST_CREATED
  ↓
110 OPENED
  ↓ [implicit check]
300 DOCUMENTS_AVAILABLE
  ↓
310 READY_TO_CONSENT
  ↓
320 CONSENT_GIVEN
  ↓
330 SHARING_INITIATED
  ↓
400 SHARED_SUCCESSFULLY
```

**v2 Flow:**
```
100 REQUEST_CREATED
  ↓
110 OPENED
  ↓
115 CHECKING_DOCUMENT_AVAILABILITY ← NEW
  ↓
300 DOCUMENTS_AVAILABLE
  ↓
310 READY_TO_CONSENT
  ↓
320 CONSENT_GIVEN
  ↓
330 SHARING_INITIATED
  ↓
400 SHARED_SUCCESSFULLY
```

**Migration:** Insert status 115 with inferred timestamp

---

### 3.2 Happy Path (Need to Request Docs)

**v1 Flow:**
```
100 → 110 → [implicit] → 200 → 210 → [implicit] → 300 → 310 → 320 → 330 → 400
```

**v2 Flow:**
```
100 → 110 → 115 → 200 → 210 → 215 → 300 → 310 → 320 → 330 → 400
         ↑              ↑       ↑
       NEW           REVISED   NEW
```

**Migration:** Insert statuses 115 and 215 with inferred timestamps

---

## 4. Database Migration Scripts

### 4.1 Schema Changes

```sql
-- Step 1: Add new columns (backwards compatible)
ALTER TABLE sharing_requests ADD COLUMN status_115_timestamp TIMESTAMP DEFAULT NULL;
ALTER TABLE sharing_requests ADD COLUMN status_210_timestamp TIMESTAMP DEFAULT NULL;
ALTER TABLE sharing_requests ADD COLUMN status_215_timestamp TIMESTAMP DEFAULT NULL;
ALTER TABLE sharing_requests ADD COLUMN documents_available_at_opening BOOLEAN DEFAULT NULL;
ALTER TABLE sharing_requests ADD COLUMN user_triggered_request BOOLEAN DEFAULT NULL;
ALTER TABLE sharing_requests ADD COLUMN issuer_fetch_duration_ms INTEGER DEFAULT NULL;

-- Step 2: Add indexes for performance
CREATE INDEX idx_sr_status_115 ON sharing_requests(status_115_timestamp) WHERE status_115_timestamp IS NOT NULL;
CREATE INDEX idx_sr_status_210 ON sharing_requests(status_210_timestamp) WHERE status_210_timestamp IS NOT NULL;
CREATE INDEX idx_sr_status_215 ON sharing_requests(status_215_timestamp) WHERE status_215_timestamp IS NOT NULL;
CREATE INDEX idx_sr_docs_avail ON sharing_requests(documents_available_at_opening);
```

---

### 4.2 Data Backfill

```sql
-- Backfill status 115 (after 110, before 200/300)
UPDATE sharing_requests
SET
  status_115_timestamp = status_110_timestamp + INTERVAL '0.5 seconds',
  documents_available_at_opening = (
    status_200_timestamp IS NULL AND status_300_timestamp IS NOT NULL
  )
WHERE
  status_110_timestamp IS NOT NULL
  AND status_115_timestamp IS NULL;

-- Backfill status 210 timestamp (before 220/230/300 in doc request flow)
UPDATE sharing_requests
SET
  status_210_timestamp = COALESCE(
    status_220_timestamp,
    status_230_timestamp,
    status_300_timestamp
  ) - INTERVAL '1 second',
  user_triggered_request = TRUE
WHERE
  status_200_timestamp IS NOT NULL
  AND (status_220_timestamp IS NOT NULL OR status_230_timestamp IS NOT NULL)
  AND status_210_timestamp IS NULL;

-- Backfill status 215 (between 210 and 220/230/300)
UPDATE sharing_requests
SET
  status_215_timestamp = status_210_timestamp + INTERVAL '0.5 seconds'
WHERE
  status_210_timestamp IS NOT NULL
  AND status_215_timestamp IS NULL;

-- Calculate issuer fetch duration
UPDATE sharing_requests
SET
  issuer_fetch_duration_ms = EXTRACT(EPOCH FROM (
    COALESCE(status_220_timestamp, status_230_timestamp, status_300_timestamp) - status_215_timestamp
  )) * 1000
WHERE
  status_215_timestamp IS NOT NULL
  AND (status_220_timestamp IS NOT NULL OR status_230_timestamp IS NOT NULL OR status_300_timestamp IS NOT NULL)
  AND issuer_fetch_duration_ms IS NULL;
```

---

### 4.3 Validation

```sql
-- Check backfill completeness
SELECT
  COUNT(*) AS total_requests,
  COUNT(status_115_timestamp) AS has_115,
  COUNT(status_210_timestamp) AS has_210,
  COUNT(status_215_timestamp) AS has_215,
  COUNT(documents_available_at_opening) AS has_doc_flag,
  COUNT(issuer_fetch_duration_ms) AS has_duration
FROM sharing_requests
WHERE status_110_timestamp IS NOT NULL;

-- Check for timestamp ordering issues
SELECT COUNT(*) AS invalid_order
FROM sharing_requests
WHERE
  status_115_timestamp IS NOT NULL
  AND status_110_timestamp IS NOT NULL
  AND status_115_timestamp < status_110_timestamp;
-- Expected: 0

-- Sample check
SELECT
  id,
  status_110_timestamp,
  status_115_timestamp,
  status_200_timestamp,
  status_300_timestamp,
  documents_available_at_opening
FROM sharing_requests
WHERE status_115_timestamp IS NOT NULL
ORDER BY RANDOM()
LIMIT 10;
```

---

## 5. Code Migration Examples

### 5.1 Backend (Node.js/Express)

**Before (v1):**
```javascript
// Status 110 handler
app.post('/api/requests/:id/status/110', async (req, res) => {
  const { id } = req.params;

  await db.sharing_requests.update(id, {
    current_status: 110,
    status_110_timestamp: new Date()
  });

  // Implicit check
  const docsAvailable = await checkDocuments(id);

  if (docsAvailable) {
    await db.sharing_requests.update(id, {
      current_status: 300,
      status_300_timestamp: new Date()
    });
  } else {
    await db.sharing_requests.update(id, {
      current_status: 200,
      status_200_timestamp: new Date()
    });
  }

  res.json({ success: true });
});
```

**After (v2):**
```javascript
// Status 110 handler
app.post('/api/requests/:id/status/110', async (req, res) => {
  const { id } = req.params;

  await db.sharing_requests.update(id, {
    current_status: 110,
    status_110_timestamp: new Date()
  });

  // Auto-trigger status 115
  await triggerStatus115(id);

  res.json({ success: true });
});

// NEW: Status 115 handler
async function triggerStatus115(requestId) {
  const docsAvailable = await checkDocuments(requestId);

  await db.sharing_requests.update(requestId, {
    current_status: 115,
    status_115_timestamp: new Date(),
    documents_available_at_opening: docsAvailable
  });

  if (docsAvailable) {
    await triggerStatus300(requestId);
  } else {
    await triggerStatus200(requestId);
  }
}
```

---

### 5.2 Frontend (React)

**Before (v1):**
```javascript
async function onOpenRequest(requestId) {
  await api.updateStatus(requestId, 110);

  // Poll for 200/300
  const status = await pollStatus(requestId, [200, 300]);

  if (status === 200) {
    showMissingDocsScreen();
  } else {
    showConsentScreen();
  }
}
```

**After (v2):**
```javascript
async function onOpenRequest(requestId) {
  await api.updateStatus(requestId, 110);

  // Optional: Show brief loading (<1s)
  showLoading('Loading...');

  // Backend auto-triggers 115 → 200/300
  const status = await pollStatus(requestId, [200, 300]);

  hideLoading();

  if (status === 200) {
    showMissingDocsScreen();
  } else {
    showConsentScreen();
  }
}

async function onRequestDocumentsClick(requestId) {
  // Track analytics
  analytics.track('user_clicked_request_documents', { request_id: requestId });

  // Trigger status 210
  await api.updateStatus(requestId, 210);

  // Show loading during status 215 (5-30s)
  showLoading('Requesting documents...');

  // Backend auto-triggers 215 → 220/230/300
  const status = await pollStatus(requestId, [220, 230, 300]);

  hideLoading();

  if (status === 300) {
    showConsentScreen();
  } else if (status === 220) {
    showPartialSuccessScreen();
  } else {
    showFailureScreen();
  }
}
```

---

## 6. Analytics Migration

### 6.1 New Metrics Available

**Metric 1: Document Availability Rate**
```sql
-- v1: NOT AVAILABLE
-- v2: AVAILABLE
SELECT
  COUNT(*) FILTER (WHERE documents_available_at_opening = TRUE) * 100.0 / COUNT(*) AS pct_ready_at_opening
FROM sharing_requests
WHERE status_115_timestamp IS NOT NULL;
```

**Metric 2: Request Conversion Rate**
```sql
-- v1: NOT AVAILABLE
-- v2: AVAILABLE
SELECT
  COUNT(*) FILTER (WHERE user_triggered_request = TRUE) * 100.0 / COUNT(*) AS conversion_rate
FROM sharing_requests
WHERE status_200_timestamp IS NOT NULL;
```

**Metric 3: Issuer Fetch Duration**
```sql
-- v1: NOT AVAILABLE
-- v2: AVAILABLE
SELECT
  issuer_id,
  AVG(issuer_fetch_duration_ms) / 1000.0 AS avg_fetch_seconds,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY issuer_fetch_duration_ms) / 1000.0 AS p95_seconds
FROM sharing_requests
WHERE issuer_fetch_duration_ms IS NOT NULL
GROUP BY issuer_id;
```

---

### 6.2 Dashboard Updates

**Update PowerBI/Tableau queries:**

```sql
-- Before (v1):
SELECT
  status,
  COUNT(*) AS request_count
FROM sharing_requests
GROUP BY status;

-- After (v2):
SELECT
  status,
  COUNT(*) AS request_count,
  -- NEW COLUMNS
  AVG(CASE WHEN documents_available_at_opening THEN 1 ELSE 0 END) AS pct_docs_ready,
  AVG(issuer_fetch_duration_ms) / 1000.0 AS avg_fetch_seconds
FROM sharing_requests
GROUP BY status;
```

---

## 7. Rollback Procedure

### 7.1 Disable v2 (Feature Flag)

```javascript
// config.js
const ENABLE_V2_FLOW = process.env.ENABLE_V2_FLOW === 'true';

// usage:
if (ENABLE_V2_FLOW) {
  await handleStatus110_v2(requestId);
} else {
  await handleStatus110_v1(requestId);
}
```

### 7.2 Rollback Impact

**Safe:** v2 → v1 rollback is safe because:
- All v1 statuses exist in v2 (no removed statuses)
- New columns are nullable (no breaking changes)
- No data loss (new columns remain)

**Steps:**
1. Set `ENABLE_V2_FLOW=false` in environment
2. Restart services
3. Monitor for issues
4. Keep new columns for future retry

---

## 8. Timeline

| Week | Phase | Activities |
|------|-------|-----------|
| 1 | Preparation | Schema changes, backfill, validation |
| 2 | Deployment | Deploy v2 code with feature flag OFF |
| 3 | Rollout | Enable v2 for 10% → 50% → 100% |
| 4 | Monitoring | Monitor metrics, fix bugs |
| 5+ | Cleanup | Remove feature flag, finalize |

---

## Appendix: Quick Reference

**New statuses in v2:**
- 115 CHECKING_DOCUMENT_AVAILABILITY
- 215 DOCUMENTS_REQUEST_IN_PROGRESS

**Revised status:**
- 210 USER_TRIGGERED_DOCUMENT_REQUEST (was: DOCUMENTS_REQUEST_INITIATED)

**New columns:**
- status_115_timestamp
- status_210_timestamp (exists but semantics changed)
- status_215_timestamp
- documents_available_at_opening
- user_triggered_request
- issuer_fetch_duration_ms

**Breaking changes:** None ✅

---

**Document Status:** Ready for Implementation
**Approval Required:** Backend Lead, QA Lead, DBA
**Next Steps:** Execute migration checklist
