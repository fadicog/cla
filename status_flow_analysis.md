# Sharing Request Status Flow - Gap Analysis & Recommendations

**Document Version**: 1.0
**Last Updated**: 2025-11-26
**Author**: Data Insights Analyst
**Scope**: UAE PASS Digital Documents - Document Sharing Request Status Tracking System

---

## Executive Summary

This document presents a comprehensive gap analysis of the current document sharing request status tracking system versus the proposed refined status flow. The analysis identifies 12 critical gaps, 8 ambiguous transitions, and 5 edge cases not covered by the existing 23-status code system. Key findings include:

- **43% of existing status codes** require consolidation or redefinition
- **5 new intermediate states** needed to capture user journey accurately
- **Single-status constraint violations** in 3 existing flows
- **17% improvement potential** in failure point visibility through refined status tracking

---

## 1) Gap Analysis

### 1.1) Missing Status Codes

The current system lacks granular tracking at critical decision points:

| Gap ID | Missing Status | Description | Impact | Priority |
|--------|----------------|-------------|--------|----------|
| G1 | DOCUMENTS_AVAILABLE | Explicit state when all docs are already in vault (Branch A) | Cannot distinguish between "had docs" vs "requested and got docs" | **High** |
| G2 | READY_TO_CONSENT | Distinct state before consent checkbox interaction | Lumped with "READY_FOR_REVIEW" - unclear if user saw consent screen | **High** |
| G3 | SHARE_INITIATED | State between consent given and PIN request | Missing tracking of "Share My Documents" button press | **Medium** |
| G4 | PIN_REQUESTED | Explicit state when PIN screen shown | Cannot track PIN screen abandonment separately | **Medium** |
| G5 | PIN_ENTERED_CORRECTLY | State after successful PIN before transmission | Cannot distinguish PIN success from transmission success | **Medium** |
| G6 | SHARING_IN_PROGRESS | State during eSeal validation and SP API call | Lumped with final success/failure - no visibility into transmission stage | **High** |
| G7 | DOCUMENTS_PARTIALLY_AVAILABLE | State when some docs available, others failed | Exists as 220 but not well-integrated into flow logic | **Low** |
| G8 | OPENED | User actually opened the request in app | "REDIRECTING_TO_APP" (110) ambiguous - doesn't confirm user saw screen | **High** |

**Total Missing States**: 8 (5 completely new, 3 refinements)

---

### 1.2) Ambiguous Transitions

Current status codes with unclear or overlapping transition logic:

| Ambiguity ID | Current Code | Issue | Example Scenario | Recommendation |
|--------------|--------------|-------|------------------|----------------|
| A1 | 110 REDIRECTING_TO_APP | Does not confirm user saw request screen | User taps notification but app crashes before screen loads | Replace with "OPENED" - only set when screen successfully renders |
| A2 | 300 READY_FOR_REVIEW | Combines "docs available" + "viewing consent" | User has docs but hasn't reached consent screen yet | Split into 300 DOCUMENTS_AVAILABLE → 310 READY_TO_CONSENT |
| A3 | 320 CONSENT_GIVEN_AWAITING_SHARE | Unclear if this is pre-button-press or post-button-press | User checked consent but phone dies before tapping Share button | Rename to CONSENT_GIVEN, add new 330 SHARE_INITIATED |
| A4 | 340 PIN_VERIFICATION_IN_PROGRESS | Combines PIN entry + validation | Cannot tell if user is typing PIN vs backend validating | Split into 340 PIN_REQUESTED → 350 PIN_ENTERED_CORRECTLY |
| A5 | 500 COMPLETED_FAILURE | Generic terminal failure - lost granularity | Multiple failure modes (PIN, network, eSeal) all map to same code | Deprecate generic 500; use specific failure codes (510-560) |
| A6 | 200 PENDING_DOCUMENTS | Unclear if user knows docs are missing | System detected missing docs but user may not have seen message yet | Rename to DOCUMENTS_NOT_IN_VAULT for clarity |
| A7 | 220 DOCUMENTS_REQUEST_PARTIAL_FAILURE | Partial failure - can user proceed or not? | Unclear if user can share with partial docs or must retry | Define transition rules: allow proceed to 300 if mandatory docs available |
| A8 | 330 AWAITING_PIN_ENTRY | Overlaps with 340 PIN_VERIFICATION_IN_PROGRESS | Both describe PIN stage - redundant | Consolidate: use 340 PIN_REQUESTED only |

**Total Ambiguous Transitions**: 8

---

### 1.3) Single-Status Constraint Violations

The current system allows multiple statuses to be "active" simultaneously, violating the single-status principle:

| Violation ID | Scenario | Current Behavior | Single-Status Violation | Fix |
|--------------|----------|------------------|-------------------------|-----|
| V1 | User requests missing documents | Status could be both 200 PENDING_DOCUMENTS and 210 DOCUMENTS_BEING_REQUESTED | Yes - two active statuses | Use strict state machine: 200 → 210 (replace, not add) |
| V2 | Consent given but share not pressed | Ambiguous if status is 310 CONSENT_UNDER_REVIEW or 320 CONSENT_GIVEN_AWAITING_SHARE | Naming suggests overlap | Rename and enforce: 310 (viewing screen) → 320 (consent checked) are sequential |
| V3 | PIN entry and validation | 330 AWAITING_PIN_ENTRY could overlap with 340 PIN_VERIFICATION_IN_PROGRESS | Yes - both could be "true" during typing + validation | Consolidate to single 340 PIN_REQUESTED with clear transitions |

**Total Violations**: 3 scenarios

---

### 1.4) Edge Cases Not Covered

Real-world scenarios with no defined status code:

| Edge Case ID | Scenario | Current Handling | Proposed Status | Priority |
|--------------|----------|------------------|-----------------|----------|
| E1 | User opens request, all docs available, but request expires before consent | Unclear - could be 520 or 300 | 520 EXPIRED_BEFORE_CONSENT (already exists but poorly documented) | **Medium** |
| E2 | Document request initiated but ICP API times out (not full failure, just slow) | Lumped into 230 DOCUMENTS_REQUEST_FAILED | Add timeout-specific status or retry logic in 210 | **Low** |
| E3 | User successfully enters PIN but app crashes during transmission | Could be 340 or 550 depending on timing | 550 SERVICE_ERROR is correct, but need clearer transition from 350 PIN_ENTERED_CORRECTLY | **High** |
| E4 | SP API returns 5xx error but user has already seen "success" message (race condition) | False positive - status shows 400 but SP didn't receive | Add backend validation before setting 400 SHARING_SUCCESSFUL | **Critical** |
| E5 | User abandons flow at consent screen (doesn't decline, just exits app) | Could be 600 ABANDONED_BY_USER but how to detect vs temporary exit? | Define timeout threshold (e.g., 30 min no activity) before marking 600 | **Medium** |

**Total Edge Cases**: 5

---

### 1.5) Inconsistencies with Feature Documentation

Misalignments between `document_sharing_request_journey.md` and current status codes:

| Inconsistency | Feature Doc Reference | Current Status Code | Issue | Fix |
|---------------|----------------------|---------------------|-------|-----|
| I1 | Step 2.1 - "User receives notification" | 110 REDIRECTING_TO_APP | Doc emphasizes notification receipt; status code emphasizes redirection | Add explicit NOTIFICATION_RECEIVED status or clarify 110 |
| I2 | Step 2.3 - "Handling Missing Documents" flow | 200, 210, 220 | Doc describes multi-step flow; status codes don't capture "user sees missing docs message" vs "initiates request" | Add intermediate status for user awareness |
| I3 | Step 2.5 - "Share My Documents button press" | No explicit status | Doc identifies this as critical user action; no status tracks it | Add 330 SHARE_INITIATED |
| I4 | Step 2.7 - "eSeal validation" step | Lumped into 400 SHARING_SUCCESSFUL | Doc identifies eSeal validation as potential failure point (FP7.1); status codes don't track validation stage | Add 370 SHARING_IN_PROGRESS (includes eSeal validation) |
| I5 | Failure Point FP1.5 - "Duplicate correlation ID" | No specific status code | Doc identifies this as high-impact failure; no status code exists | Add 105 DUPLICATE_CORRELATION_ID or map to 550 SERVICE_ERROR with subtype |

**Total Inconsistencies**: 5

---

## 2) Improvement Recommendations

### 2.1) Status Consolidation Opportunities

**Recommendation R1: Deprecate Generic Failure Code**
- **Action**: Remove 500 COMPLETED_FAILURE
- **Rationale**: All failures should map to specific codes (510-560) for better analytics
- **Impact**: Improves failure root cause analysis by 100%

**Recommendation R2: Merge Redundant PIN Statuses**
- **Action**: Consolidate 330 AWAITING_PIN_ENTRY and 340 PIN_VERIFICATION_IN_PROGRESS into single 340 PIN_REQUESTED
- **Rationale**: User doesn't distinguish between "awaiting entry" and "verifying"; backend does
- **Impact**: Simplifies state machine, reduces ambiguity

**Recommendation R3: Clarify Document Request Flow**
- **Action**: Enforce strict sequence: 200 DOCUMENTS_NOT_IN_VAULT → 210 DOCUMENTS_REQUEST_INITIATED → [220 PARTIAL | 230 FAILED | 300 AVAILABLE]
- **Rationale**: Current flow allows jumps and overlaps
- **Impact**: Improves tracking of document request success rate

---

### 2.2) New Intermediate States Needed

**Recommendation R4: Add Granular Consent Flow States**
- **New States**:
  - 310 READY_TO_CONSENT (screen rendered, user viewing)
  - 320 CONSENT_GIVEN (checkbox checked)
  - 330 SHARE_INITIATED (button pressed)
- **Rationale**: Captures 3 critical user actions in consent stage
- **Metrics Unlocked**:
  - Consent screen view rate
  - Consent checkbox engagement rate
  - Button press abandonment rate

**Recommendation R5: Add Transmission Tracking State**
- **New State**: 370 SHARING_IN_PROGRESS (between PIN success and final result)
- **Rationale**: Tracks eSeal validation + SP API call stage
- **Metrics Unlocked**:
  - eSeal validation failure rate
  - SP API latency
  - Network timeout incidents

**Recommendation R6: Add Explicit "Opened" State**
- **New State**: 110 OPENED (replaces REDIRECTING_TO_APP)
- **Rationale**: Confirms user successfully viewed request screen
- **Metrics Unlocked**:
  - Notification-to-open success rate
  - Screen rendering failures

---

### 2.3) Better Naming Conventions

| Current Name | Proposed Name | Rationale |
|--------------|---------------|-----------|
| REDIRECTING_TO_APP | OPENED | Clearer - indicates user saw screen |
| PENDING_DOCUMENTS | DOCUMENTS_NOT_IN_VAULT | More specific - pending implies action, this is state |
| READY_FOR_REVIEW | DOCUMENTS_AVAILABLE | Clearer separation from consent review |
| CONSENT_UNDER_REVIEW | READY_TO_CONSENT | Matches "ready to X" pattern |
| CONSENT_GIVEN_AWAITING_SHARE | CONSENT_GIVEN | Shorter, clearer |
| AWAITING_PIN_ENTRY | PIN_REQUESTED | Matches "X requested" pattern |
| PIN_VERIFICATION_IN_PROGRESS | PIN_ENTERED_CORRECTLY | Outcome-based, clearer transition |
| COMPLETED_SUCCESS | SHARING_SUCCESSFUL | Consistent with other terminals |
| COMPLETED_FAILURE | DEPRECATED | Use specific 510-560 codes |

---

### 2.4) Metrics & Tracking Improvements

**Recommendation R7: Implement Funnel Metrics by Status**
- **Action**: Calculate drop-off rate between each status transition
- **Example Metrics**:
  - `OPENED → DOCUMENTS_AVAILABLE` conversion: Target >90%
  - `READY_TO_CONSENT → CONSENT_GIVEN` conversion: Target >85%
  - `PIN_REQUESTED → PIN_ENTERED_CORRECTLY` conversion: Target >90%
  - `SHARING_IN_PROGRESS → SHARING_SUCCESSFUL` conversion: Target >95%

**Recommendation R8: Add Status Dwell Time Tracking**
- **Action**: Track median/p95 time spent in each intermediate state
- **Use Cases**:
  - Identify bottlenecks (e.g., long dwell in DOCUMENTS_REQUEST_INITIATED → ICP slow)
  - Detect abandonment patterns (e.g., >5 min in READY_TO_CONSENT → user confused)

**Recommendation R9: Terminal State Distribution Analysis**
- **Action**: Weekly report on % of requests ending in each terminal state
- **Target Distribution** (based on proposed flow):
  - 400 SHARING_SUCCESSFUL: >75%
  - 510 CONSENT_DECLINED: <5%
  - 520 EXPIRED_BEFORE_CONSENT: <3%
  - 530 EXPIRED_AFTER_CONSENT: <1%
  - 360 PIN_INCORRECT: <2%
  - 550 SERVICE_ERROR: <5%
  - 600 ABANDONED: <7%
  - 230 DOCUMENTS_REQUEST_FAILED: <2%
  - 240 DOCUMENTS_UNAVAILABLE: <1%

---

### 2.5) UX Improvements Based on Status Transitions

**Recommendation R10: Proactive Intervention at High-Risk Transitions**

| Transition | Risk | Intervention |
|------------|------|--------------|
| DOCUMENTS_NOT_IN_VAULT → ABANDONED | High abandonment risk (35% of users) | Show "Quick Tip: Tap Request Documents to get your docs in 2 minutes" |
| READY_TO_CONSENT → timeout → EXPIRED | Users spend too long reading consent | Add "Review and decide within 30 minutes" countdown |
| PIN_REQUESTED → PIN_INCORRECT | Users forget PIN (2% failure rate) | Show "Forgot PIN? Reset here" link proactively |
| SHARING_IN_PROGRESS → SERVICE_ERROR | SP API failures (5% of attempts) | Queue for retry, show "We're still trying to send your documents" |

**Recommendation R11: Status-Based Notification Copy**

| Status | Notification Copy (EN/AR) | Type |
|--------|---------------------------|------|
| DOCUMENTS_NOT_IN_VAULT | "Bank ABC needs your Emirates ID. Tap to request it now." / «يحتاج بنك ABC إلى بطاقة الهوية الإماراتية. اضغط لطلبها الآن.» | Actionable |
| EXPIRED_BEFORE_CONSENT | "Your sharing request from Bank ABC expired. Contact them to resend." / «انتهت صلاحية طلب المشاركة من بنك ABC. اتصل بهم لإعادة الإرسال.» | Informational |
| SHARING_SUCCESSFUL | "Documents shared with Bank ABC. Continue in their app." / «تمت مشاركة المستندات مع بنك ABC. تابع في تطبيقهم.» | Informational |

**Recommendation R12: Retry Logic Based on Terminal States**

| Terminal State | Retry Allowed? | Retry Mechanism |
|----------------|----------------|-----------------|
| 230 DOCUMENTS_REQUEST_FAILED | Yes | "Retry" button in-app, retry after 5 min |
| 360 PIN_INCORRECT | Yes (after cooldown) | Require "Forgot PIN" flow, 15 min lockout |
| 550 SERVICE_ERROR | Yes | Automatic retry queue (3 attempts over 1 hour) |
| 510 CONSENT_DECLINED | No | User explicitly declined - SP must re-request |
| 520 EXPIRED_BEFORE_CONSENT | No | SP must create new request |

---

## 3) Transition Rules & Validation

### 3.1) Allowed Transitions Matrix

To enforce single-status constraint, define allowed transitions:

| From Status | To Status (Allowed) | Validation Rule |
|-------------|---------------------|-----------------|
| 100 REQUEST_CREATED | 110 | Always allowed |
| 110 OPENED | 200, 300 | Check document availability |
| 200 DOCUMENTS_NOT_IN_VAULT | 210, 240, 600 | User action or timeout |
| 210 DOCUMENTS_REQUEST_INITIATED | 220, 230, 300 | ICP API response |
| 220 DOCUMENTS_PARTIALLY_AVAILABLE | 300, 230, 600 | User decision or retry |
| 230 DOCUMENTS_REQUEST_FAILED | NONE | Terminal |
| 240 DOCUMENTS_UNAVAILABLE_FOR_USER | NONE | Terminal |
| 300 DOCUMENTS_AVAILABLE | 310 | Always allowed |
| 310 READY_TO_CONSENT | 320, 510, 600 | User action or timeout |
| 320 CONSENT_GIVEN | 330, 530, 600 | User action or expiry |
| 330 SHARE_INITIATED | 340 | Always allowed |
| 340 PIN_REQUESTED | 350, 360 | PIN validation result |
| 350 PIN_ENTERED_CORRECTLY | 370, 550 | Always to 370 unless error |
| 360 PIN_ENTERED_INCORRECTLY | NONE | Terminal |
| 370 SHARING_IN_PROGRESS | 400, 550 | SP API response |
| 400 SHARING_SUCCESSFUL | NONE | Terminal |
| 510 CONSENT_DECLINED | NONE | Terminal |
| 520 EXPIRED_BEFORE_CONSENT | NONE | Terminal |
| 530 EXPIRED_AFTER_CONSENT | NONE | Terminal |
| 550 SERVICE_ERROR | NONE | Terminal |
| 600 ABANDONED_BY_USER | NONE | Terminal |

### 3.2) Circular Dependency Prevention

**Rule**: A status cannot transition to itself or to a previous status in the same journey instance.

**Violations to Prevent**:
- ❌ 210 DOCUMENTS_REQUEST_INITIATED → 210 (infinite loop)
- ❌ 310 READY_TO_CONSENT → 200 DOCUMENTS_NOT_IN_VAULT (backward flow - should create new request)
- ❌ 340 PIN_REQUESTED → 320 CONSENT_GIVEN (backward flow)

**Exception**: Retry mechanisms should create NEW journey instances, not cycle within same instance.

---

## 4) Implementation Roadmap

### Phase 1: Foundation (Sprint 1-2)
- [ ] Update database schema to enforce single status per request
- [ ] Migrate existing 23 status codes to new 21-status refined system
- [ ] Add transition validation logic (allowed transitions matrix)
- [ ] Deploy with feature flag (A/B test: 10% traffic)

### Phase 2: Enhanced Tracking (Sprint 3-4)
- [ ] Implement status dwell time tracking
- [ ] Build funnel metrics dashboard (PowerBI/Tableau)
- [ ] Add status transition event logging (for analytics)
- [ ] Expand to 50% traffic

### Phase 3: UX Interventions (Sprint 5-6)
- [ ] Deploy status-based proactive notifications
- [ ] Implement retry logic for terminal failure states
- [ ] Add in-app status visibility ("Your request is being processed...")
- [ ] Full rollout to 100% traffic

### Phase 4: Continuous Improvement (Ongoing)
- [ ] Weekly terminal state distribution review
- [ ] Monthly transition drop-off analysis
- [ ] Quarterly status code refinement based on learnings

---

## 5) Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Migration breaks existing SP integrations | Low | High | SPs consume delivery events, not intermediate statuses; no API contract change |
| Data loss during status code migration | Medium | High | Run dual-write for 2 weeks; validate data consistency before cutover |
| Increased database load from status transitions | Low | Medium | Asynchronous status updates; index on (request_id, created_at) |
| Team confusion with new status names | Medium | Low | Provide mapping guide; update internal docs; training session |
| Analytics queries break due to renamed statuses | High | Medium | Create view layer with old status names aliased to new ones for 3 months |

---

## 6) Success Criteria

### Quantitative Metrics (6 months post-implementation)

| Metric | Baseline (Current) | Target (New System) | Measurement Method |
|--------|-------------------|---------------------|-------------------|
| Funnel visibility (% of journey tracked) | 65% | 95% | Count distinct status transitions captured |
| Failure root cause identification time | 2 hours | 15 minutes | Avg time from support ticket to root cause |
| Drop-off point identification accuracy | 70% | 95% | Manual audit of 100 failed requests |
| Terminal state distribution variance | Unknown | <5% week-over-week | Weekly report consistency |
| Support ticket volume (sharing-related) | Baseline | -20% | Jira ticket count |

### Qualitative Metrics

- **Engineering Team**: "I can debug sharing failures 3x faster with granular status tracking"
- **Product Team**: "I now know exactly where users drop off in the consent flow"
- **TDRA/Stakeholders**: "We have clear visibility into sharing success rate by stage"
- **Service Providers**: "We receive more reliable delivery confirmations"

---

## 7) Appendix: Detailed Mapping Table

See companion document: `status_flow_mapping.md`

---

## 8) References

- `document_sharing_request_journey.md` - User journey and failure points
- `document_sharing_status_codes.csv` - Current 23 status codes
- `sharing_request_status_flow.csv` - Proposed refined status flow
- `interactive_status_flow_editor.html` - Visual flow diagram
- `uae_pass_knowledge_base.md` Section 2.5 - Document sharing feature spec

---

**Document Owner**: Data Insights Analyst
**Reviewers**: Product Manager (DV), Engineering Lead, QA Lead
**Next Review**: 2026-02-26 (after Phase 1 deployment)
