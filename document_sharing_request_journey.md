# Document Sharing Request Journey - Feature Documentation

**Last updated**: 2025-11-24

---

## 1) Overview

This document details the complete user journey for responding to document sharing requests from Service Providers (SPs) within the UAE PASS Digital Documents (DV) component. It includes step-by-step flow, failure points, and mitigation strategies.

### User Story
**As a** UAE PASS user
**I want to** respond to document sharing requests from Service Providers
**So that** I can complete services like opening bank accounts, applying for loans, or registering for telecom services

---

## 2) Complete User Journey Flow

### 2.1) Step 1: Receiving the Sharing Request

**User Action**: User receives a notification that a Service Provider has requested documents

**System Behavior**:
- Push notification sent to user's device (Firebase)
- In-app notification appears in notification center
- Notification type: Actionable (requires user response)
- Contains: SP name, document types requested, expiry time

**Bilingual Copy Examples**:
- EN: "Bank ABC requests your Emirates ID to open your account"
- AR: «يطلب بنك ABC بطاقة الهوية الإماراتية لفتح حسابك»

**Failure Points**:
- **FP1.1**: Push notification not received (device offline, notification permissions disabled)
- **FP1.2**: Notification delivered but user misses it (notification overload, expired before seen)
- **FP1.3**: Deep link from notification fails to open sharing request screen
- **FP1.4**: Sharing request expired before user opens it (short TTL)
- **FP1.5**: Duplicate correlation ID causes request rejection at database level

**Metrics to Track**:
- Notification delivery rate (sent vs received)
- Time from notification send to user opening request
- Expiration rate (requests expired before user response)

---

### 2.2) Step 2: Viewing Request Details

**User Action**: User taps notification or navigates to sharing requests section

**System Behavior**:
- Display SP name and logo
- List requested document types (e.g., Emirates ID, Visa, Passport)
- Show expiry countdown for request
- Display consent text and terms
- Show "Request Missing Documents" option if user lacks required documents

**Bilingual Copy Examples**:
- EN: "Bank ABC requests 2 documents"
- AR: «يطلب بنك ABC مستندين» (dual form)

**Failure Points**:
- **FP2.1**: Screen fails to load request details (API timeout, network error)
- **FP2.2**: SP logo or branding fails to load (broken asset reference)
- **FP2.3**: User cannot understand what documents are being requested (unclear naming)
- **FP2.4**: Consent text too long or complex (user skips reading)
- **FP2.5**: Request already processed/expired but still shown as active (sync issue)

**Metrics to Track**:
- Screen load success rate
- Time spent on request details screen (engagement)
- Drop-off rate at this step

---

### 2.3) Step 3: Handling Missing Documents

**User Action**: If user lacks required documents, taps "Request Missing Documents"

**System Behavior**:
- Identify which documents are missing
- Show option to request from issuer (ICP for EID/Visa/Passport)
- Redirect to document request flow
- Return to sharing request after document becomes available

**Bilingual Copy Examples**:
- EN: "You need to request your Emirates ID before sharing"
- AR: «تحتاج إلى طلب بطاقة الهوية الإماراتية قبل المشاركة»

**Failure Points**:
- **FP3.1**: User abandons flow when seeing missing documents (high friction)
- **FP3.2**: Document request to ICP fails (issuer unavailable, user ineligible)
- **FP3.3**: User requests document but does not return to complete sharing (broken journey)
- **FP3.4**: Document becomes available but sharing request has expired
- **FP3.5**: User confused about how long document request will take (no ETA shown)

**Metrics to Track**:
- % of sharing requests with missing documents
- Completion rate for "request then share" journeys
- Time from document request to availability
- Return rate after document issuance

---

### 2.4) Step 4: Providing Consent

**User Action**: User checks the consent checkbox

**System Behavior**:
- Display consent statement (legal text explaining data sharing)
- Checkbox must be explicitly checked (no pre-selection)
- "Share My Documents" button remains disabled until consent checked
- Log consent timestamp for audit trail

**Bilingual Copy Examples**:
- EN: "I consent to share my documents with Bank ABC for account opening"
- AR: «أوافق على مشاركة مستنداتي مع بنك ABC لفتح الحساب»

**Failure Points**:
- **FP4.1**: User does not read consent text (checkbox hunting behavior)
- **FP4.2**: Consent text unclear or too legalistic (user confusion)
- **FP4.3**: User checks consent accidentally (tap error on mobile)
- **FP4.4**: Consent checkbox tap does not register (UI responsiveness issue)
- **FP4.5**: User disagrees with consent terms but no "Decline" option clearly visible

**Metrics to Track**:
- Time from screen load to consent checked (proxy for text reading)
- Consent decline rate (if decline option exists)
- User support tickets about consent confusion

---

### 2.5) Step 5: Initiating Document Sharing

**User Action**: User taps "Share My Documents" button

**System Behavior**:
- Button enabled only after consent checked and documents available
- Trigger PIN entry screen
- Show summary of what will be shared (document types, SP name)

**Bilingual Copy Examples**:
- EN: "Share My Documents"
- AR: «مشاركة مستنداتي»

**Failure Points**:
- **FP5.1**: Button appears enabled but tap does nothing (state management bug)
- **FP5.2**: User taps button multiple times (double submission risk)
- **FP5.3**: Button tap triggers error before PIN entry (validation failure)
- **FP5.4**: User expects immediate sharing without PIN (expectation mismatch)
- **FP5.5**: User changes mind but no "Cancel" option after tapping button

**Metrics to Track**:
- Button tap success rate
- Double-tap incidents (duplicate request attempts)
- Time from consent to button tap

---

### 2.6) Step 6: PIN Authentication

**User Action**: User enters their UAE PASS PIN

**System Behavior**:
- Display secure PIN entry pad (masked input)
- Validate PIN against user's account
- Allow 3 attempts before lockout (standard security pattern)
- Show error message for incorrect PIN with remaining attempts

**Bilingual Copy Examples**:
- EN: "Enter your PIN to confirm sharing"
- AR: «أدخل رقم التعريف الشخصي لتأكيد المشاركة»
- EN: "Incorrect PIN. 2 attempts remaining"
- AR: «رقم التعريف الشخصي غير صحيح. محاولتان متبقيتان» (dual form)

**Failure Points**:
- **FP6.1**: User forgets PIN (high support cost)
- **FP6.2**: User reaches lockout threshold (account temporarily blocked)
- **FP6.3**: PIN validation API fails (backend unavailable)
- **FP6.4**: User cannot see PIN entry on screen (accessibility issue)
- **FP6.5**: Keyboard does not appear on PIN entry (mobile OS issue)
- **FP6.6**: User exits PIN screen accidentally (loses context, must restart)

**Metrics to Track**:
- PIN entry success rate (first attempt vs multiple attempts)
- Lockout incidents per day/week
- Average time spent on PIN entry screen
- "Forgot PIN" flow initiation rate

---

### 2.7) Step 7: Document Sharing Execution

**User Action**: After successful PIN entry, system executes sharing

**System Behavior**:
- Create verifiable presentation package (selected documents + user attributes)
- Apply eSeal validation (cryptographic verification of issuer authenticity)
- Send presentation to SP via secure API endpoint (HTTPS/TLS pinning)
- Log sharing event with: timestamp, SP ID, document types, correlation ID
- Mark sharing request as "Completed"
- Show success confirmation to user

**Bilingual Copy Examples**:
- EN: "Your documents have been shared with Bank ABC"
- AR: «تمت مشاركة مستنداتك مع بنك ABC»

**Failure Points**:
- **FP7.1**: eSeal validation fails (document integrity issue, revoked certificate)
- **FP7.2**: SP API endpoint unavailable (network error, SP downtime)
- **FP7.3**: Request times out during transmission (slow network, large payload)
- **FP7.4**: SP rejects presentation (schema mismatch, missing fields)
- **FP7.5**: Success confirmation shown but sharing actually failed (false positive)
- **FP7.6**: User closes app during transmission (interrupted flow, unclear state)

**Metrics to Track**:
- Sharing success rate (end-to-end)
- eSeal validation failure rate
- SP API error rate (by SP)
- Average transmission time
- Retry rate after failures

---

### 2.8) Step 8: Post-Sharing Confirmation

**User Action**: User sees success/failure message

**System Behavior**:
- **Success case**: Show confirmation screen with SP name and timestamp
- **Failure case**: Show error message with retry option or support contact
- Send informational push notification (non-actionable confirmation)
- Update sharing history in user's profile
- Remove completed request from pending requests list

**Bilingual Copy Examples**:
- EN: "Success! Continue with Bank ABC to complete your application"
- AR: «نجاح! تابع مع بنك ABC لإكمال طلبك»

**Failure Points**:
- **FP8.1**: Success message does not provide next steps (user confused about what to do)
- **FP8.2**: Error message too technical (user cannot self-resolve)
- **FP8.3**: No retry option after failure (user stuck)
- **FP8.4**: User unclear if SP received documents (lack of status visibility)
- **FP8.5**: Sharing history not updated (user cannot verify past shares)

**Metrics to Track**:
- User satisfaction score (post-sharing survey)
- Support ticket volume related to sharing
- Retry utilization rate
- Time from sharing to SP service completion (if measurable)

---

## 3) Critical Failure Point Summary

### High-Impact Failures (User Cannot Complete Flow)

| Failure Point | Impact | Likelihood | Mitigation Strategy |
|---------------|--------|------------|---------------------|
| FP1.5: Duplicate correlation ID | High - Request rejected at DB level | Medium | Enforce unique constraint + SP guidance on ID generation |
| FP3.2: Document request to ICP fails | High - User blocked from sharing | Low-Medium | Retry logic + clear error messaging + ICP SLA monitoring |
| FP6.2: PIN lockout | High - User locked out of account | Low | Self-service PIN reset + support escalation |
| FP7.1: eSeal validation fails | High - Document cannot be shared | Low | Pre-flight validation + issuer certificate monitoring |
| FP7.2: SP API unavailable | High - Sharing fails at final step | Medium | Retry queue + async delivery option |

### Medium-Impact Failures (User Experiences Friction)

| Failure Point | Impact | Likelihood | Mitigation Strategy |
|---------------|--------|------------|---------------------|
| FP1.4: Request expires before user opens | Medium - User must re-request from SP | Medium | Extend TTL + expiry warnings in notification |
| FP3.1: User abandons when seeing missing docs | Medium - Lost sharing opportunity | Medium | One-click document request + Auto-Add feature |
| FP4.1: User does not read consent | Medium - Uninformed consent (legal risk) | High | Progressive disclosure + summary before checkbox |
| FP6.1: User forgets PIN | Medium - Requires password reset flow | Medium | Biometric authentication option + PIN hints |
| FP8.2: Error message too technical | Medium - User cannot self-resolve | Low | User-friendly error copy + contextual help links |

### Low-Impact Failures (Minor UX Issues)

| Failure Point | Impact | Likelihood | Mitigation Strategy |
|---------------|--------|------------|---------------------|
| FP2.2: SP logo fails to load | Low - Aesthetic issue only | Low | Fallback to SP name text + asset CDN redundancy |
| FP4.4: Consent checkbox tap does not register | Low - User retaps | Low | Increase tap target size + haptic feedback |
| FP5.2: Double-tap submission | Low - Backend idempotency handles | Low | Button debouncing + loading state during processing |

---

## 4) Recommended Enhancements

### 4.1) Proactive Document Availability Check
- **Feature**: Before user opens sharing request, check if all documents are available
- **Benefit**: Surface missing document issue in notification ("1 document needs to be requested")
- **Priority**: High (reduces friction)

### 4.2) Auto-Add Documents Integration
- **Feature**: If user previously consented to Auto-Add, automatically fetch missing documents
- **Benefit**: Zero-touch sharing for repeat SPs
- **Priority**: High (pending legal review - see section 9 in knowledge base)

### 4.3) Biometric Authentication Option
- **Feature**: Allow Face ID / Fingerprint instead of PIN for sharing confirmation
- **Benefit**: Reduces PIN-related failures (FP6.1, FP6.2)
- **Priority**: Medium (requires security review)

### 4.4) Asynchronous Sharing with Status Tracking
- **Feature**: If SP API is slow/unavailable, queue sharing and notify user when complete
- **Benefit**: Prevents user waiting for transmission (FP7.2, FP7.3)
- **Priority**: Medium (improves reliability)

### 4.5) Pre-Flight Validation
- **Feature**: Validate eSeal, document expiry, SP endpoint before user enters PIN
- **Benefit**: Catches failures early, before user authentication (FP7.1, FP7.2)
- **Priority**: High (better error UX)

### 4.6) Sharing Request Dashboard
- **Feature**: Dedicated screen showing all pending/completed/expired requests with filters
- **Benefit**: User can easily manage multiple SP requests
- **Priority**: Low (nice-to-have for power users)

---

## 5) Key Metrics & Success Criteria

### Funnel Metrics (Track Drop-off at Each Step)

| Step | Metric | Target |
|------|--------|--------|
| 1. Notification received | Delivery rate | >95% |
| 2. Request opened | Open rate within 1 hour | >70% |
| 3. Missing docs handled | Request + return rate | >60% |
| 4. Consent provided | Consent rate (of opened requests) | >90% |
| 5. Share button tapped | Tap-through rate | >95% |
| 6. PIN entered successfully | Success rate (within 3 attempts) | >90% |
| 7. Sharing executed | End-to-end success rate | >95% |
| 8. User sees confirmation | Confirmation view rate | >99% |

### Quality Metrics

- **Time to Share**: Median time from notification received to documents shared (target: <2 minutes)
- **First-Time Success Rate**: % of users who complete sharing without errors (target: >85%)
- **Support Ticket Rate**: Sharing-related tickets per 1000 sharing requests (target: <5)
- **SP Satisfaction**: SP feedback on presentation quality and reliability (target: >4.5/5)

---

## 6) Stakeholder Considerations

### TDRA (Product Owner)
- Ensure consent flow meets legal requirements for data sharing
- Validate that failure handling protects user trust
- Approve any changes to consent language

### DDA (Design Authority)
- Design approval required for any UI changes to sharing flow
- Must review error message copy (EN/AR)
- Validate accessibility of PIN entry and consent screens

### ICP (Document Issuer)
- Coordinate on document request flow (step 3)
- Ensure eSeal validation compatibility
- Define SLAs for document issuance

### Service Providers (SPs)
- Provide guidance on correlation ID uniqueness (prevent FP1.5)
- Define acceptable TTLs for sharing requests
- Establish API SLAs and error handling contracts

---

## 7) Technical Implementation Notes

### API Endpoints Involved
- `POST /sharing-requests` (SP creates request)
- `GET /sharing-requests/:id` (User fetches request details)
- `POST /sharing-requests/:id/share` (Execute sharing with PIN)
- `GET /documents/:type` (Check document availability)
- `POST /documents/request` (Request missing document from ICP)

### Security Considerations
- All sharing requests must use unique correlation IDs (enforce via DB constraint)
- PIN entry must use secure input (no logging, masked display)
- eSeal validation required before presentation generation
- TLS pinning for SP API communication
- Audit log every sharing event with user ID, SP ID, timestamp, documents shared

### Firebase Remote Config Flags
- `sharing_request_ttl_seconds` (default: 3600)
- `max_pin_attempts` (default: 3)
- `enable_biometric_auth` (default: false)
- `enable_async_sharing` (default: false)

---

## 8) Glossary

- **Correlation ID**: Unique identifier for a sharing request, generated by SP
- **Verifiable Presentation**: Package of user documents and attributes cryptographically signed for SP
- **eSeal**: Cryptographic organization stamp for issuer authentication (not eSignature)
- **TTL**: Time-to-live for sharing request before expiration
- **ICP**: Issuer - high-volume document provider (EID, Visa, Passport)
- **SP**: Service Provider - bank, telco, insurer requesting user documents
- **FP**: Failure Point - identified location where user journey can break

---

## 9) Related Documentation

- See `uae_pass_knowledge_base.md` Section 2: Core capabilities (document sharing flow)
- See `uae_pass_knowledge_base.md` Section 4: QR code hygiene (correlation ID requirements)
- See `uae_pass_knowledge_base.md` Section 5: Notifications taxonomy (actionable vs informational)
- See `uae_pass_knowledge_base.md` Section 9: Auto-Add Documents (future enhancement)
- See `pm_dv_working_doc.md`: Current priorities and roadmap

---

**Document Owner**: Product Manager, UAE PASS Digital Vault
**Review Cadence**: Quarterly or after major feature releases
**Next Review Date**: 2026-02-24
