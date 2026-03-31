# Status Flow Mapping: Old vs New System

**Document Version**: 1.0
**Last Updated**: 2025-11-26
**Purpose**: Detailed mapping between existing 23 status codes and proposed refined 21-status flow

---

## 1) Overview

This document provides the authoritative mapping between:
- **Old System**: 23 status codes (current implementation)
- **New System**: 21 status codes (refined single-status flow)

### Key Changes Summary

| Change Type | Count | Description |
|-------------|-------|-------------|
| **Direct Mapping** | 11 | Status codes retained with same/similar meaning |
| **Renamed** | 7 | Status codes retained but renamed for clarity |
| **Split** | 3 | One old status split into multiple new statuses |
| **Merged** | 2 | Multiple old statuses consolidated into one |
| **Deprecated** | 1 | Removed from new system |
| **New** | 5 | Added to capture missing states |

---

## 2) Complete Mapping Table

| Old Code | Old Name | New Code | New Name | Mapping Type | Notes |
|----------|----------|----------|----------|--------------|-------|
| 100 | REQUEST_CREATED | 100 | REQUEST_CREATED | **Direct** | No change |
| 110 | REDIRECTING_TO_APP | 110 | OPENED | **Renamed** | Clarified to mean "user successfully viewed screen" |
| 200 | PENDING_DOCUMENTS | 200 | DOCUMENTS_NOT_IN_VAULT | **Renamed** | More specific name; same meaning |
| 210 | DOCUMENTS_BEING_REQUESTED | 210 | DOCUMENTS_REQUEST_INITIATED | **Renamed** | Clearer action-oriented name |
| 220 | DOCUMENTS_REQUEST_PARTIAL_FAILURE | 220 | DOCUMENTS_PARTIALLY_AVAILABLE | **Renamed** | Reframed as "partially available" vs "partial failure" |
| 230 | DOCUMENTS_REQUEST_FAILED | 230 | DOCUMENTS_REQUEST_FAILED | **Direct** | No change |
| 240 | DOCUMENTS_UNAVAILABLE_FOR_USER | 240 | DOCUMENTS_UNAVAILABLE_FOR_USER | **Direct** | No change |
| 300 | READY_FOR_REVIEW | **Split** → 300, 310 | 300: DOCUMENTS_AVAILABLE<br>310: READY_TO_CONSENT | **Split** | Old 300 conflated "docs ready" + "consent screen" - now separated |
| 310 | CONSENT_UNDER_REVIEW | 310 | READY_TO_CONSENT | **Merged/Renamed** | Merged with part of old 300; clearer name |
| 320 | CONSENT_GIVEN_AWAITING_SHARE | 320 | CONSENT_GIVEN | **Renamed** | Simplified name; next state is new 330 |
| 330 | AWAITING_PIN_ENTRY | **Merged** → 340 | PIN_REQUESTED | **Merged** | Consolidated with old 340 to avoid redundancy |
| 340 | PIN_VERIFICATION_IN_PROGRESS | **Split** → 340, 350 | 340: PIN_REQUESTED<br>350: PIN_ENTERED_CORRECTLY | **Split** | Separated PIN request from successful entry |
| N/A | *(missing)* | 330 | SHARE_INITIATED | **New** | Tracks "Share My Documents" button press |
| N/A | *(missing)* | 370 | SHARING_IN_PROGRESS | **New** | Tracks eSeal validation + SP API transmission |
| 400 | COMPLETED_SUCCESS | 400 | SHARING_SUCCESSFUL | **Renamed** | Clearer terminal name |
| 500 | COMPLETED_FAILURE | **DEPRECATED** | *(use specific 510-560)* | **Deprecated** | Generic failure code removed; use specific codes |
| 510 | FAILURE_CONSENT_DECLINED | 510 | CONSENT_DECLINED | **Renamed** | Removed "FAILURE_" prefix for consistency |
| 520 | FAILURE_EXPIRED_BEFORE_CONSENT | 520 | EXPIRED_BEFORE_CONSENT | **Renamed** | Removed "FAILURE_" prefix |
| 530 | FAILURE_EXPIRED_AFTER_CONSENT | 530 | EXPIRED_AFTER_CONSENT | **Renamed** | Removed "FAILURE_" prefix |
| 540 | FAILURE_PIN_INCORRECT | 360 | PIN_ENTERED_INCORRECTLY | **Renumbered + Renamed** | Moved to 360 range for logical grouping with PIN flow |
| 550 | FAILURE_SERVICE_ERROR | 550 | SERVICE_ERROR | **Renamed** | Removed "FAILURE_" prefix |
| 560 | FAILURE_DOCUMENTS_NOT_AVAILABLE | **Merged** → 240 | DOCUMENTS_UNAVAILABLE_FOR_USER | **Merged** | Redundant with 240; consolidated |
| 600 | ABANDONED_BY_USER | 600 | ABANDONED_BY_USER | **Direct** | No change |

---

## 3) Detailed Mapping by Change Type

### 3.1) Direct Mapping (No Change)

These status codes transfer directly with same code and meaning:

| Code | Name | Notes |
|------|------|-------|
| 100 | REQUEST_CREATED | Entry point - no changes needed |
| 230 | DOCUMENTS_REQUEST_FAILED | Terminal failure - well-defined |
| 240 | DOCUMENTS_UNAVAILABLE_FOR_USER | Terminal failure - clear meaning |
| 600 | ABANDONED_BY_USER | Terminal state - well-defined |

**Migration Action**: No code changes; update documentation only.

---

### 3.2) Renamed (Same Code, Clearer Name)

Status codes retained with improved naming for clarity:

| Old Code | Old Name | New Name | Rationale |
|----------|----------|----------|-----------|
| 110 | REDIRECTING_TO_APP | OPENED | "Opened" is clearer than "redirecting" - confirms user saw screen |
| 200 | PENDING_DOCUMENTS | DOCUMENTS_NOT_IN_VAULT | "Not in vault" is more specific than "pending" |
| 210 | DOCUMENTS_BEING_REQUESTED | DOCUMENTS_REQUEST_INITIATED | "Initiated" is clearer action verb |
| 220 | DOCUMENTS_REQUEST_PARTIAL_FAILURE | DOCUMENTS_PARTIALLY_AVAILABLE | Reframes as "what user has" vs "what failed" |
| 320 | CONSENT_GIVEN_AWAITING_SHARE | CONSENT_GIVEN | Shorter, clearer; next state handles "awaiting share" |
| 400 | COMPLETED_SUCCESS | SHARING_SUCCESSFUL | More descriptive terminal state name |
| 510-550 | FAILURE_* | *(no prefix)* | Removed "FAILURE_" prefix - terminal type indicates failure |

**Migration Action**:
1. Update status name in database enum/constants
2. Update application code references
3. Create alias view for analytics queries (3-month transition period)
4. Update dashboard labels

---

### 3.3) Split Transitions (1 Old → Multiple New)

Old statuses that combined multiple states, now separated:

#### Split 1: Old 300 READY_FOR_REVIEW → New 300 + 310

**Old Behavior**:
- 300 READY_FOR_REVIEW encompassed:
  - All docs available ✓
  - User viewing consent screen ✓
  - Ambiguous boundary between these two states

**New Behavior**:
- 300 DOCUMENTS_AVAILABLE: All mandatory docs confirmed in vault
- 310 READY_TO_CONSENT: User has reached consent screen

**Transition Logic**:
```
Old: 110 OPENED → 300 READY_FOR_REVIEW → 320 CONSENT_GIVEN

New: 110 OPENED → 300 DOCUMENTS_AVAILABLE → 310 READY_TO_CONSENT → 320 CONSENT_GIVEN
```

**Migration Action**:
- Analyze existing requests with old 300 status:
  - If timestamp is recent (< 5 min): migrate to 310 (likely viewing consent)
  - If older: keep as 300 (docs available, not yet at consent)
- Update transition triggers:
  - Set 300 when document availability check completes
  - Set 310 when consent screen renders

---

#### Split 2: Old 340 PIN_VERIFICATION_IN_PROGRESS → New 340 + 350

**Old Behavior**:
- 340 PIN_VERIFICATION_IN_PROGRESS encompassed:
  - User entering PIN
  - Backend validating PIN
  - No distinction between entry vs validation success

**New Behavior**:
- 340 PIN_REQUESTED: PIN entry screen shown, awaiting user input
- 350 PIN_ENTERED_CORRECTLY: PIN validated successfully, ready for transmission

**Transition Logic**:
```
Old: 330 AWAITING_PIN_ENTRY → 340 PIN_VERIFICATION_IN_PROGRESS → 400 COMPLETED_SUCCESS
                                                                 → 540 FAILURE_PIN_INCORRECT

New: 330 SHARE_INITIATED → 340 PIN_REQUESTED → 350 PIN_ENTERED_CORRECTLY → 370 SHARING_IN_PROGRESS
                                              → 360 PIN_ENTERED_INCORRECTLY (terminal)
```

**Migration Action**:
- Analyze existing requests with old 340 status:
  - Check backend logs for PIN validation result
  - If validated successfully: migrate to 350
  - If still validating or failed: migrate to 340
- Update PIN validation endpoint to set 350 on success

---

### 3.4) Merged Transitions (Multiple Old → 1 New)

Old statuses consolidated for simplicity:

#### Merge 1: Old 330 + 340 → New 340 PIN_REQUESTED

**Old Behavior**:
- 330 AWAITING_PIN_ENTRY: Waiting for user to start typing
- 340 PIN_VERIFICATION_IN_PROGRESS: User typing + backend validating

**Issue**: Redundant - user doesn't distinguish "awaiting entry" from "verifying"

**New Behavior**:
- 340 PIN_REQUESTED: Single state for entire PIN interaction until success/failure

**Transition Logic**:
```
Old: 320 CONSENT_GIVEN → 330 AWAITING_PIN_ENTRY → 340 PIN_VERIFICATION → [success/fail]

New: 320 CONSENT_GIVEN → 330 SHARE_INITIATED → 340 PIN_REQUESTED → [350 success / 360 fail]
```

**Migration Action**:
- All existing requests with 330 or old 340 → migrate to new 340

---

#### Merge 2: Old 560 + 240 → New 240 DOCUMENTS_UNAVAILABLE_FOR_USER

**Old Behavior**:
- 240 DOCUMENTS_UNAVAILABLE_FOR_USER: User not eligible
- 560 FAILURE_DOCUMENTS_NOT_AVAILABLE: Terminal state for missing docs

**Issue**: Redundant terminal states for same outcome

**New Behavior**:
- 240 DOCUMENTS_UNAVAILABLE_FOR_USER: Single terminal state

**Migration Action**:
- All existing requests with 560 → migrate to 240

---

### 3.5) Deprecated (Removed from New System)

#### Deprecated 1: Old 500 COMPLETED_FAILURE

**Old Behavior**:
- Generic failure code for any terminal failure
- Lost granularity - couldn't distinguish PIN failure from network error

**New Behavior**:
- Removed; all failures must use specific codes:
  - 230: Document request failed
  - 240: Documents unavailable
  - 360: PIN incorrect
  - 510: Consent declined
  - 520: Expired before consent
  - 530: Expired after consent
  - 550: Service/technical error
  - 600: Abandoned by user

**Migration Action**:
- Analyze all existing requests with 500 status
- Re-categorize based on error logs:
  - Check for PIN errors → migrate to 360
  - Check for SP API errors → migrate to 550
  - Check for expiry → migrate to 520 or 530
  - Check for user decline → migrate to 510
  - Default: migrate to 550 (service error)
- After migration, deprecate 500 from codebase

---

### 3.6) New Status Codes (Added)

States added to capture missing journey stages:

| New Code | New Name | Rationale | Metrics Unlocked |
|----------|----------|-----------|------------------|
| 300 | DOCUMENTS_AVAILABLE | Distinguish "had docs" vs "requested docs" (Branch A vs B) | % of users with pre-existing docs |
| 330 | SHARE_INITIATED | Track "Share My Documents" button press | Button press abandonment rate |
| 350 | PIN_ENTERED_CORRECTLY | Track successful PIN before transmission | PIN success rate independent of transmission |
| 370 | SHARING_IN_PROGRESS | Track eSeal validation + SP API call stage | eSeal failure rate, SP API latency |

**Migration Action**:
- No migration needed (new statuses start applying to new requests only)
- Update application code to set these statuses at appropriate triggers
- Update analytics dashboards to track new funnel stages

---

## 4) Renumbering Changes

Some statuses changed numerical codes for logical grouping:

| Old Code | Old Name | New Code | New Name | Reason for Renumber |
|----------|----------|----------|----------|---------------------|
| 540 | FAILURE_PIN_INCORRECT | 360 | PIN_ENTERED_INCORRECTLY | Grouped with PIN flow (340-360) |

**Migration Action**:
- Update all database records: `UPDATE sharing_requests SET status = 360 WHERE status = 540`
- Update application constants
- Update analytics queries

---

## 5) Migration Strategy

### 5.1) Data Migration Plan

**Phase 1: Analysis (Week 1)**
- [ ] Query all existing sharing requests by status code
- [ ] Identify requests in intermediate states (need careful migration)
- [ ] Identify requests in terminal states (safe to migrate)

**Phase 2: Mapping Script (Week 1)**
- [ ] Create SQL migration script with logic:
  ```sql
  -- Example migrations
  UPDATE sharing_requests SET status = 110, status_name = 'OPENED' WHERE status = 110;
  UPDATE sharing_requests SET status = 240 WHERE status = 560;
  UPDATE sharing_requests SET status = 360 WHERE status = 540;

  -- Complex migration: old 300 → new 300 or 310
  UPDATE sharing_requests
  SET status = 310, status_name = 'READY_TO_CONSENT'
  WHERE status = 300 AND updated_at > NOW() - INTERVAL '5 minutes';

  UPDATE sharing_requests
  SET status = 300, status_name = 'DOCUMENTS_AVAILABLE'
  WHERE status = 300 AND updated_at <= NOW() - INTERVAL '5 minutes';

  -- Categorize old 500
  UPDATE sharing_requests SET status = 550, status_name = 'SERVICE_ERROR'
  WHERE status = 500; -- default; refine with error log analysis
  ```

**Phase 3: Dual-Write Period (Week 2-3)**
- [ ] Deploy application code that writes BOTH old and new status codes
- [ ] Validate data consistency
- [ ] Monitor for discrepancies

**Phase 4: Cutover (Week 4)**
- [ ] Run final migration script on production database
- [ ] Switch application to read/write new status codes only
- [ ] Keep old status columns for 30 days as backup

**Phase 5: Cleanup (Week 8)**
- [ ] Drop old status columns from database
- [ ] Remove old status constants from codebase
- [ ] Archive migration scripts

---

### 5.2) Code Migration Checklist

#### Backend Changes
- [ ] Update database schema (add new status enum values, deprecate old)
- [ ] Update status transition validation logic
- [ ] Update API response models (return new status names)
- [ ] Update status update triggers (set new statuses at correct points)
- [ ] Add backward compatibility layer for old API consumers (3-month deprecation period)

#### Frontend Changes
- [ ] Update status display labels in UI
- [ ] Update status icons/colors (e.g., intermediate vs terminal)
- [ ] Update push notification templates (use new status-based copy)
- [ ] Update user-facing error messages

#### Analytics Changes
- [ ] Create view layer aliasing old → new status names
- [ ] Update PowerBI/Tableau dashboards with new status codes
- [ ] Update funnel reports to include new intermediate states
- [ ] Create new dwell time reports for granular states

---

### 5.3) Rollback Plan

**If migration fails**:
1. Revert database schema changes (restore old status column)
2. Revert application code to old status logic
3. Analyze failure root cause
4. Fix and retry migration

**Safe Rollback Window**: 30 days (while old status columns retained)

---

## 6) Impact Analysis

### 6.1) Stakeholder Impact

| Stakeholder | Impact | Mitigation |
|-------------|--------|------------|
| **Service Providers (SPs)** | Low - SPs consume delivery webhooks (400/550), not intermediate statuses | No SP API changes required; inform of deprecation of 500 code |
| **Engineering Team** | Medium - Code changes across FE/BE/Analytics | Provide migration guide, hold training session, 2-week dual-write buffer |
| **Product/Analytics Team** | Medium - Dashboard updates, new metrics available | Update dashboards during dual-write period; validate accuracy before cutover |
| **TDRA/Stakeholders** | Low - More granular reporting (positive impact) | Present new funnel metrics in next sprint review |
| **End Users** | None - Status codes are backend-only | No user-facing changes |

---

### 6.2) System Impact

| System Component | Change Required | Complexity | Risk |
|------------------|-----------------|------------|------|
| Database | Add new enum values, migrate data | Medium | Low (tested in staging) |
| Backend API | Update status update logic | Medium | Medium (thorough testing needed) |
| Frontend App | Update UI labels | Low | Low (cosmetic changes) |
| Analytics Pipeline | Update dashboards, create alias views | Medium | Low (dual-write validates accuracy) |
| Push Notifications | Update templates | Low | Low (A/B test new copy) |
| SP Integration | None (API contract unchanged) | None | None |

---

## 7) Validation & Testing

### 7.1) Validation Queries

**After migration, run these queries to validate**:

```sql
-- Check no requests have old deprecated statuses
SELECT COUNT(*) FROM sharing_requests WHERE status IN (500, 540, 560);
-- Expected: 0

-- Check all terminal states are valid
SELECT status, COUNT(*) FROM sharing_requests
WHERE status IN (230, 240, 360, 400, 510, 520, 530, 550, 600)
GROUP BY status;
-- Expected: Positive counts, sum matches total terminal requests

-- Check no intermediate states are stuck (>24 hours old)
SELECT status, COUNT(*) FROM sharing_requests
WHERE status IN (110, 200, 210, 220, 300, 310, 320, 330, 340, 350, 370)
AND created_at < NOW() - INTERVAL '24 hours';
-- Expected: 0 or very low (investigate stuck requests)

-- Validate transition logic (no invalid transitions)
SELECT r1.status AS from_status, r2.status AS to_status, COUNT(*)
FROM sharing_request_transitions r1
JOIN sharing_request_transitions r2 ON r1.request_id = r2.request_id
WHERE r2.created_at > r1.created_at
GROUP BY r1.status, r2.status
HAVING COUNT(*) > 0;
-- Review: Ensure all transitions match allowed transitions matrix
```

---

### 7.2) Test Scenarios

| Scenario | Old Flow | New Flow | Validation |
|----------|----------|----------|------------|
| Happy path (user has docs) | 100→110→300→320→330→340→400 | 100→110→300→310→320→330→340→350→370→400 | End-to-end test passes |
| Missing docs path | 100→110→200→210→300→320→330→340→400 | 100→110→200→210→300→310→320→330→340→350→370→400 | Document request succeeds |
| PIN failure | 100→110→300→320→330→340→540 | 100→110→300→310→320→330→340→360 | Terminal state 360 reached |
| Consent declined | 100→110→300→310→510 | 100→110→300→310→510 | Terminal state 510 reached |
| Service error | 100→110→300→320→330→340→500 | 100→110→300→310→320→330→340→350→370→550 | Terminal state 550 reached |

---

## 8) Timeline & Milestones

| Week | Milestone | Owner | Deliverable |
|------|-----------|-------|-------------|
| 1 | Data analysis & migration script | Backend Team | SQL script + validation queries |
| 2-3 | Dual-write deployment | Backend + QA | Feature flagged code in production |
| 4 | Analytics validation | Analytics Team | Dashboard accuracy report |
| 4 | Cutover | Backend Team | New system live, old system backup |
| 5-7 | Monitoring & bug fixes | All Teams | Incident response, hotfixes |
| 8 | Cleanup | Backend Team | Old columns dropped, migration complete |

---

## 9) Appendix: Quick Reference

### Old → New Status Code Lookup

| Old | New | Change |
|-----|-----|--------|
| 100 | 100 | Same |
| 110 | 110 | Renamed |
| 200 | 200 | Renamed |
| 210 | 210 | Renamed |
| 220 | 220 | Renamed |
| 230 | 230 | Same |
| 240 | 240 | Same |
| 300 | 300/310 | Split |
| 310 | 310 | Merged |
| 320 | 320 | Renamed |
| 330 | 340 | Merged |
| 340 | 340/350 | Split |
| 400 | 400 | Renamed |
| 500 | *varied* | Deprecated |
| 510 | 510 | Renamed |
| 520 | 520 | Renamed |
| 530 | 530 | Renamed |
| 540 | 360 | Renumbered |
| 550 | 550 | Renamed |
| 560 | 240 | Merged |
| 600 | 600 | Same |

### New Status Codes Summary

```
100 - REQUEST_CREATED (Initial)
110 - OPENED (Intermediate)
200 - DOCUMENTS_NOT_IN_VAULT (Intermediate)
210 - DOCUMENTS_REQUEST_INITIATED (Intermediate)
220 - DOCUMENTS_PARTIALLY_AVAILABLE (Intermediate)
230 - DOCUMENTS_REQUEST_FAILED (Terminal - Failure)
240 - DOCUMENTS_UNAVAILABLE_FOR_USER (Terminal - Failure)
300 - DOCUMENTS_AVAILABLE (Intermediate)
310 - READY_TO_CONSENT (Intermediate)
320 - CONSENT_GIVEN (Intermediate)
330 - SHARE_INITIATED (Intermediate) [NEW]
340 - PIN_REQUESTED (Intermediate)
350 - PIN_ENTERED_CORRECTLY (Intermediate) [NEW]
360 - PIN_ENTERED_INCORRECTLY (Terminal - Failure)
370 - SHARING_IN_PROGRESS (Intermediate) [NEW]
400 - SHARING_SUCCESSFUL (Terminal - Success)
510 - CONSENT_DECLINED (Terminal - Failure)
520 - EXPIRED_BEFORE_CONSENT (Terminal - Failure)
530 - EXPIRED_AFTER_CONSENT (Terminal - Failure)
550 - SERVICE_ERROR (Terminal - Failure)
600 - ABANDONED_BY_USER (Terminal - Failure)
```

---

**Document Owner**: Data Insights Analyst
**Reviewers**: Backend Lead, QA Lead, Product Manager
**Approval Required**: Engineering Director, Product Director
**Next Review**: Post-migration (Week 8)
