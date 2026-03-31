# UAE PASS Digital Vault (DV) Feature Registry

**Last Updated**: 2026-02-16T10:45:00Z
**Version**: 2.2 (Share with UAE PASS Button Added)
**Maintained by**: Feature Registry Expert
**Purpose**: Single source of truth for all existing features in the UAE PASS Digital Documents component

---

## Overview

This registry catalogs every feature in the UAE PASS Digital Vault (DV) application. It serves as the authoritative reference for:
- Feature descriptions, capabilities, and user flows
- Current status (Active, Beta, In Development, Pending Review, Deprecated)
- Release information and version tracking
- Technical implementation details
- Bilingual support status (EN/AR)
- Known issues and limitations
- Stakeholder approvals (TDRA, DDA)
- Cross-references to knowledge base and documentation

**Scope**: Document request, storage, lifecycle management, sharing, and qualified eSignature (for uploaded documents) within the DV component of UAE PASS.

**IMPORTANT BOUNDARIES**:
- **Authentication/SSO**: Owned by DDA, NOT part of DV
- **Platform/Infrastructure**: Backend capabilities, not user-facing DV features
- **Security/Privacy**: Underlying capabilities, not standalone DV features
- **DDA Sharing Consent Feature**: External to DV, managed by DDA for third-party SP document sharing

**Related Documentation**:
- Knowledge Base: `uae_pass_knowledge_base.md` (Sections 1-17)
- PM Working Doc: `pm_dv_working_doc.md` (roadmap, metrics, decision log)
- Session Artifacts: Various analysis and design documents

---

## 1) Digital Signature Features

### 1.1) Qualified eSignature (for Uploaded Documents)

**Status**: Active
**Release Date**: Pre-2025 (core feature)
**Version**: Stable

**Description**:
- **EN**: Legally binding electronic signature specifically for user-uploaded documents in the "Uploaded" tab
- **AR**: التوقيع الإلكتروني الملزم قانونياً خصيصاً للمستندات المحملة من قبل المستخدم في تبويب "المحملة"

**User Story**:
As a UAE PASS user, I want to self-sign documents I upload to my Documents, so that I can add a qualified eSignature to my own PDFs for transactions requiring my personal attestation.

**Scope**:
- **Uploaded Documents Tab ONLY**: Users can upload their own PDFs and self-sign them
- **NOT for Issued Documents**: Issued documents (EID, Visa, Passport) come with issuer eSeal, not user eSignature
- **Person-level signature**: Cryptographic proof of user consent/attestation

**Use Cases**:
- User uploads contract and self-signs it
- User uploads personal declaration and signs it
- User uploads form and adds qualified eSignature
- Any transaction requiring person-level non-repudiation

**Key Capabilities**:
- Person-level cryptographic signature
- Non-repudiation (legally binding)
- Attestation of natural person consent
- Timestamp and certificate chain

**Technical Implementation**:
- Cryptographic signature using user's private key
- PKI (Public Key Infrastructure) certificate validation
- Timestamp authority integration
- eSignature standard compliance (UAE regulations)

**Bilingual Support**: Full (EN/AR)

**Known Issues**: None currently documented

**Dependencies**:
- UAE PKI infrastructure
- User's digital certificate
- Timestamp authority

**Stakeholders**:
- TDRA (regulatory compliance)
- Federal and local government entities
- Service Providers requiring eSignatures on user-uploaded docs

**Documentation**: KB Section 2.2

---

## 2) Document Lifecycle Features

### 2.1) Document Request (from Issuers)

**Status**: Active
**Release Date**: Pre-2025 (core DV feature)
**Version**: 4.x

**Description**:
- **EN**: Request official documents from authorized issuers (ICP, government entities)
- **AR**: طلب المستندات الرسمية من الجهات المصدرة المعتمدة

**User Story**:
As a UAE PASS user, I want to request my official documents (EID, Visa, Passport, licenses) from government issuers, so that I can store them securely in my Documents and share them with service providers.

**User Flow**:
1. User navigates to Documents tab
2. Taps "Request Document" button
3. Selects issuer from list (e.g., ICP, RTA, MOH)
4. Selects document type (e.g., Emirates ID, Driver License)
5. Confirms request
6. DV polls issuer backend for document availability
7. User receives notification when document is available
8. Document appears in Issued Documents tab

**Document Types Supported**:

**Issued Documents** (official, eSeal-protected):
- Emirates ID (EID) - from ICP
- Residency Visa - from ICP
- Passport - from ICP
- Driver License - from RTA
- Vehicle Registration - from RTA
- Health Records - from MOH
- Education Certificates - from MOE
- Other government-issued credentials

**Uploaded Documents** (user PDFs, self-signed):
- Any user PDF (lower trust for SPs, can be self-signed via qualified eSignature)

**Key Capabilities**:
- Multi-issuer support
- Real-time and asynchronous document retrieval
- eSeal validation on retrieval
- Status tracking (Available, Pending, Failed)
- Notification on availability

**Technical Implementation**:
- DV backend polls issuer APIs via secure channels
- Issuer returns document with eSeal (CAdES/PAdES format)
- DV validates eSeal via DSS (Digital Signature Service)
- Document stored encrypted on device + cloud sync
- Status: Active / Expired / Revoked tracked

**Security & Privacy**:
- End-to-end encryption
- eSeal validation ensures authenticity
- User consent required for document request
- Audit logging of all requests

**Bilingual Support**: Full (EN/AR)

**Known Issues**:
- Some issuers have slower response times (polling delays)
- Limited error messaging when issuer unavailable
- Users unaware which documents are available from which issuers

**Dependencies**:
- Issuer backend APIs (ICP, RTA, MOH, etc.)
- DDA eSeal validation service (transitioning to ICP self-signing in 2025)
- Firebase push notifications

**Stakeholders**:
- TDRA (policy, governance)
- ICP (primary issuer for EID/Visa/Passport)
- Other government issuers (RTA, MOH, MOE, etc.)

**Documentation**: KB Section 2.3, 2.4

---

### 2.2) Document Storage

**Status**: Active
**Release Date**: Pre-2025
**Version**: 4.x

**Description**:
- **EN**: Secure storage of issued and uploaded documents in the mobile app
- **AR**: التخزين الآمن للمستندات الصادرة والمحملة في التطبيق

**User Story**:
As a UAE PASS user, I want to securely store all my official documents in one place, so that I can access them anytime and share them with service providers when needed.

**Storage Structure**:

**Tabs**:
- **Issued Documents**: Official docs from issuers (high trust, eSeal-protected)
- **Uploaded Documents**: User PDFs (self-signed, lower SP trust)

**Views**:
- **List View**: Default chronological list (ACTIVE)
- **Type-based View**: Group by document type (one-to-many documents) (ACTIVE)
- **Grid View**: NOT EXISTING - Planned for 2025

**Categories** (filter/organize):
- All
- Personal
- Professional
- Legal
- Property
- Other

**Key Capabilities**:
- Local device storage (encrypted)
- Cloud sync (backup and multi-device access)
- Search across all documents (global search)
- Sort by name, issuer, date
- Filter by category
- Document cards show: issuer logo, document type, status, expiry

**Technical Implementation**:
- Encrypted storage on device (iOS Keychain, Android Keystore)
- Cloud backup (encrypted)
- eSeal validation on retrieval (issued docs)
- Real-time sync across user devices
- Revocation/expiry status checks

**Security & Privacy**:
- AES-256 encryption at rest
- Secure enclave/keystore for keys
- Biometric or PIN unlock required
- No cloud storage without user consent
- Audit logging of access

**Bilingual Support**: Full (EN/AR)

**Known Issues**:
- Equal visual weight for Issued vs Uploaded tabs (despite different SP value)
- Type view only useful for one-to-many cases
- Inconsistent empty states
- No grid view (users expect from file managers)

**UX Enhancements Planned (2025)**:
- Grid view (in addition to list/type)
- New landing page with primary CTAs: "Request Document" / "Upload Document"
- Issuer/logo chips on doc cards
- Consistent empty states (EN/AR parity)
- Bilingual microcopy refresh (remove "vault" term)

**Dependencies**:
- Device storage APIs
- Cloud sync service
- eSeal validation service

**Documentation**: KB Section 2.3, 6.1

---

### 2.3) Document Lifecycle Management

**Status**: Active
**Release Date**: Pre-2025
**Version**: 4.x

**Description**:
- **EN**: Automated tracking and management of document updates, expiry, and revocation
- **AR**: التتبع والإدارة التلقائية لتحديثات المستندات وانتهاء الصلاحية والإلغاء

**User Story**:
As a UAE PASS user, I want to be notified when my documents are expiring or have been updated, so that I can keep my documents current and avoid failed sharing attempts.

**Lifecycle Stages**:
1. **Request** - User initiates document request
2. **Availability** - Issuer makes document available
3. **Storage** - Document stored in app
4. **Updates** - Issuer provides updated version
5. **Revocation** - Issuer revokes document (issuer action)
6. **Expiry** - Document reaches expiration date
7. **Removal** - User removes document from digital vault (user action)

**Key Features**:

**Updated Version Prompt**:
- DV detects when newer version exists
- Prompts user: "Would you like to request an updated version?"
- User can tap to initiate request flow
- Replaces old version when new one arrives

**Expiry Reminders** (Informational Notifications):
- Timeline: D-30, D-15, D-7, D-5, D-3, D-1 (configurable)
- Channel: Push notification via Firebase
- Bilingual: EN/AR
- Non-actionable (informational only)
- Example: "Your Emirates ID expires in 7 days. Request an updated version to avoid service disruptions."

**Revocation Notifications**:
- Issuer revokes document (issuer-side action, e.g., replacement issued, fraud detected)
- User receives informational notification
- Document status updated to "Revoked"
- Document card shows revoked status
- User prompted to request new version if available

**Document Removal by User**:
- User can manually remove stored documents from Digital Vault (user action)
- Confirmation dialog before removal
- Cannot be undone (must re-request)
- Removal tracked in audit log

**Document Status Tracking**:
- **Active**: Valid, current document
- **Expired**: Past expiration date
- **Revoked**: Issuer revoked (issuer action)
- **Pending**: Request in progress
- **Failed**: Request failed

**Technical Implementation**:
- Backend monitors document expiry dates
- Scheduled jobs trigger notifications
- Real-time revocation updates from issuers
- Status reflected in UI (badges, colors)
- Version comparison logic

**Bilingual Support**: Full (EN/AR)

**Known Issues**:
- No centralized dashboard showing all expiring documents
- No one-tap bulk renewal (users must request individually)
- No proactive pre-request before SP asks for sharing

**Improvement Opportunities**:
- Expiry dashboard (see all documents expiring in next 30 days)
- Bulk renewal for multiple expiring documents
- Integration with Auto-Add Documents feature (future)

**Dependencies**:
- Issuer backend APIs (status updates)
- Firebase Cloud Messaging (notifications)
- DV backend (scheduling, monitoring)

**Documentation**: KB Section 2.4, 5

---

## 3) Document Sharing Features

### 3.1) Consent-Based Document Sharing

**Status**: Active
**Release Date**: Pre-2025 (core DV feature)
**Version**: 4.1 (latest: duplicate correlation ID fix deployed 2025-01-15)

**Description**:
- **EN**: Share documents with Service Providers (banks, telcos, government) after explicit user consent
- **AR**: مشاركة المستندات مع مزودي الخدمة بعد موافقة المستخدم الصريحة

**User Story**:
As a UAE PASS user, I want to securely share my official documents with service providers (bank, telecom, employer) when they need them, so that I can complete transactions without submitting physical copies.

**IMPORTANT NOTE**:
- DDA recently added a "sharing consent" feature for sharing documents with third-party service providers
- This DDA feature is OUTSIDE Digital Vault but related to document sharing ecosystem
- DV's consent-based sharing is a separate, DV-native feature

**User Flow** (Standard):
1. **SP Initiates**: Service Provider creates sharing request with unique correlation ID
2. **User Receives Request** (via one of three channels):
   - **Push Notification**: Actionable notification in UAE PASS app (most common)
   - **QR Code**: SP displays QR code; user scans with UAE PASS app (in-person/web flows)
   - **Deep Link**: SP sends deep link; user taps to open in UAE PASS app (mobile flows)
3. **User Opens Request**: Views sharing request details in app
4. **User Reviews**: Sees which documents SP is requesting + SP identity
5. **User Approves/Declines**: Explicit per-transaction consent
6. **DV Prepares Presentation**: If approved, DV packages requested documents with issuer signatures
7. **DV Delivers**: Verifiable presentation sent to SP backend
8. **SP Validates**: SP validates eSeal authenticity and consumes attributes

**Key Capabilities**:
- Per-transaction consent (every share requires user approval)
- Verifiable presentation (includes issuer eSeals)
- Selective disclosure (user can decline specific documents)
- SP identity transparency (user sees who's requesting)
- Audit trail of all shares
- QR code and deep link support
- Time-limited requests (expiry after X minutes)

**Technical Implementation**:

**Correlation ID**:
- Unique identifier for each sharing request
- SP-generated, time-boxed, one-time use
- Database unique constraint enforced (as of 2025-01-15)
- Prevents duplicate requests and notification spam

**Verifiable Presentation**:
- JSON package containing:
  - Requested documents/attributes
  - Issuer eSeals (cryptographic signatures)
  - Timestamps
  - Request context
- Delivered to SP callback URL
- SP validates eSeal before trusting data

**Security**:
- No PII in QR codes (opaque correlation ID only)
- HTTPS/TLS pinning for SP communication
- User PIN verification before sensitive shares
- Per-transaction consent (cannot auto-share)
- Audit logging of all shares

**Sharing Request Status Tracking** (comprehensive system designed 2025-11-25):

**Status Codes** (23 total):
- **100-199**: Initial/Redirect states
  - `REQUEST_CREATED` (100)
  - `REDIRECTING_TO_APP` (110)
- **200-299**: Document acquisition phase
  - `PENDING_DOCUMENTS` (200)
  - `DOCUMENTS_BEING_REQUESTED` (210)
  - `DOCUMENTS_REQUEST_PARTIAL_FAILURE` (220)
  - `DOCUMENTS_REQUEST_FAILED` (230)
  - `DOCUMENTS_UNAVAILABLE_FOR_USER` (240)
- **300-399**: User interaction/consent phase
  - `READY_FOR_REVIEW` (300)
  - `CONSENT_UNDER_REVIEW` (310)
  - `CONSENT_GIVEN_AWAITING_SHARE` (320)
  - `AWAITING_PIN_ENTRY` (330)
  - `PIN_VERIFICATION_IN_PROGRESS` (340)
- **400-499**: Success states
  - `COMPLETED_SUCCESS` (400)
- **500-599**: Failure states
  - `COMPLETED_FAILURE` (500)
  - `FAILURE_CONSENT_DECLINED` (510)
  - `FAILURE_EXPIRED_BEFORE_CONSENT` (520)
  - `FAILURE_EXPIRED_AFTER_CONSENT` (530)
  - `FAILURE_PIN_INCORRECT` (540)
  - `FAILURE_SERVICE_ERROR` (550)
  - `FAILURE_DOCUMENTS_NOT_AVAILABLE` (560)
- **600-699**: Abandonment states
  - `ABANDONED_BY_USER` (600)

**Data Analysis Findings** (350K+ requests analyzed, 2025-11-25):

**Overall Conversion Rate**: 67.4% (237,000 successes / 351,000 requests)

**Critical Insights**:
1. **Document availability is THE critical factor**:
   - 84.9% success when docs available
   - 0% success when docs missing
   - 20.6% of requests "dead on arrival" (SP requesting docs user doesn't have)

2. **Consent screen is biggest drop-off point**:
   - 16.9% abandonment at consent review
   - Suggests UX friction or trust concerns

3. **Platform performance gap**:
   - iOS: 77.8% conversion
   - Android: 67.7% conversion
   - 10 percentage point gap needs investigation

4. **Time-based patterns**:
   - Business hours (9am-5pm): 72.3% conversion
   - Off-hours: 58.1% conversion
   - Suggests context and urgency affect completion

**Top Failure Reasons**:
1. **Missing documents** (20.6%): User hasn't requested docs from issuer
2. **Consent declined** (16.9%): User rejects share at consent screen
3. **Request expired** (8.2%): User doesn't act within time window
4. **Service errors** (4.3%): Backend/issuer failures
5. **Expired documents** (2.1%): User has outdated version

**Bilingual Support**: Full (EN/AR)

**Known Issues**:

**Fixed**:
- ✅ Duplicate correlation IDs causing notification spam (FIXED 2025-01-15 via DB constraint)

**Active**:
- Missing documents cause 20.6% of sharing failures
- Expired documents cause 2.1% of failures
- High consent screen abandonment (16.9%)
- Android performance gap (10 points below iOS)
- No document pre-check API (SPs request docs users don't have)

**Improvement Opportunities** (from data analysis):

**High Impact**:
1. **Document Pre-Check API**: Allow SPs to verify document availability before creating request → Eliminate 72K futile requests/week
2. **Consent Screen Redesign**: Reduce 16.9% drop-off through UX improvements
3. **Android Optimization**: Close 10% platform gap
4. **Issuer Retry Logic**: Reduce 26% of technical failures

**Potential Impact**: +31,500 shares/week (+13.3% improvement) → Target: 76% conversion rate

**Dependencies**:
- SP integration (API, correlation ID generation)
- Issuer backend (document availability)
- Firebase push notifications
- DDA eSeal validation service
- DV backend (presentation preparation)

**Stakeholders**:
- TDRA (policy, consent requirements)
- DDA (design approval for UX, external sharing consent feature)
- Service Providers (integration partners)
- Issuers (document sources)

**QR Code Hygiene Principles** (when using QR channel):
- Unique correlation IDs (enforced via DB constraint)
- Short TTL (time-to-live, typically 5-15 minutes)
- One-time use (QR invalidated after scan)
- No PII embedded (opaque IDs only)
- Clear error codes (expired, used, invalid)
- Idempotent SP backend (handle retries)
- QR format: `uaepass://share?correlationId={unique-id}`

**Documentation**:
- KB Section 2.5, 4, 11
- Session artifact: `session_sharing_request_status_tracking.md`
- Analysis reports: `document_sharing_analysis_report.md`, `key_insights_summary.md`
- Dashboard: `uaepass_dashboard_report.html`

---

### 3.2) "Share with UAE PASS" Button (User-Initiated Push Notification Sharing)

**Status**: In Development
**Release Date**: Q1 2026 (target)
**Version**: TBD

**Description**:
- **EN**: User-initiated document sharing flow where users click a button on SP website to trigger push notification for consent
- **AR**: تدفق مشاركة المستندات الذي يبدأه المستخدم حيث ينقر المستخدمون على زر على موقع مزود الخدمة لتشغيل إشعار فوري للموافقة

**User Story**:
As a user completing a transaction on a Service Provider's website, I want to click a "Share with UAE PASS" button to approve document sharing on my phone, so that I can complete my transaction without scanning QR codes or switching contexts.

**Key Difference from Existing Flow**:

**Existing (SP-Initiated)**:
1. SP creates sharing request
2. Push notification sent to user
3. User opens app and approves
4. SP polls/receives completion

**New (User-Initiated via Button)**:
1. User clicks "Share with UAE PASS" button on SP website
2. SP creates sharing request + sends push notification
3. User receives push notification on phone
4. User approves sharing in UAE PASS app
5. SP website detects completion and continues user journey

**User Flow**:
1. **SP Website Journey**: User is on SP website (e.g., bank account opening)
2. **Document Request Point**: SP shows "Share with UAE PASS" button when Emirates ID needed
3. **User Clicks Button**: Triggers SP backend to create sharing request
4. **Push Notification Sent**: UAE PASS app receives actionable notification
5. **User Reviews on Phone**: Opens notification, sees document request details
6. **User Approves**: Gives consent in UAE PASS app
7. **Sharing Completes**: DV delivers verifiable presentation to SP
8. **SP Website Updates**: SP detects completion, user continues on website

**Use Cases**:
- Bank account opening (web journey requiring Emirates ID)
- Insurance policy application (document sharing without QR scan)
- Government service application (seamless web-to-mobile flow)
- Hotel check-in (user on hotel website shares ID via button)
- Any SP web flow requiring document verification

**Key Capabilities**:
- **User-initiated**: User controls when to trigger the sharing request
- **Button-based UX**: Simple, clear call-to-action on SP website
- **Cross-device flow**: User acts on website, approves on phone
- **Real-time completion detection**: SP website knows when sharing is complete
- **No QR scanning required**: Eliminates QR code display/scan step
- **Same security model**: Maintains per-transaction consent and correlation ID hygiene
- **Fallback to QR**: SP can offer both button and QR for user preference

**Technical Implementation**:

**SP Website**:
- "Share with UAE PASS" button displayed at document request point
- Button click triggers SP backend API to create sharing request
- SP frontend polls or receives webhook when sharing completes
- UI updates to show success/failure state

**SP Backend**:
- Creates sharing request with unique correlation ID (same as existing)
- Calls UAE PASS API to send push notification to user
- Provides callback URL or polling endpoint for completion status
- Handles timeout scenarios (user doesn't respond)

**UAE PASS Backend**:
- Receives sharing request from SP
- Sends push notification to user's device
- Tracks completion status for SP polling/webhook
- Enforces same correlation ID uniqueness constraint

**UAE PASS App**:
- Receives actionable push notification (same as existing)
- Opens sharing consent screen (same UX as existing)
- User approves/declines (same flow)
- Delivers verifiable presentation to SP (same mechanism)

**Demo Context**:
- Initial demo with mock bank website
- Account creation journey requiring Emirates ID sharing
- Demonstrates button click → push notification → approval → completion flow

**Comparison with Existing Channels**:

| Channel | Initiation | Use Case | UX Pattern |
|---------|-----------|----------|------------|
| **QR Code** | SP displays QR | In-person, web flows | User scans → Opens app |
| **Deep Link** | SP sends link | Mobile-first flows | User taps link → Opens app |
| **Push (SP-initiated)** | SP triggers push | SP knows user identity | Notification arrives → Opens app |
| **Push (User-initiated button)** | User clicks button | Web flows, user control | User clicks → Notification → Opens app |

**Advantages**:
- **User control**: User decides when to start the flow
- **No QR complexity**: No need to display/scan QR codes
- **Familiar pattern**: Button clicking is intuitive
- **Cross-device friendly**: Works naturally for desktop web + mobile app
- **Maintains consent**: Per-transaction approval still required

**Considerations**:
- **Device identification**: SP must know which user/device to send notification to (requires user session)
- **Timeout handling**: Clear UX if user doesn't respond to push notification
- **Fallback options**: Offer QR code as alternative if push fails
- **Completion detection**: SP website needs real-time or near-real-time status updates

**Bilingual Support**: Full (EN/AR)

**Known Issues**: None (in development)

**Dependencies**:
- SP integration (button implementation, backend API)
- UAE PASS backend (push notification endpoint, status tracking)
- Same dependencies as existing consent-based sharing (Firebase, issuer APIs, etc.)

**Stakeholders**:
- TDRA (policy approval for new sharing initiation pattern)
- DDA (design approval if authentication/session impacts)
- Service Providers (integration partners adopting button pattern)

**Open Questions**:
1. **User authentication requirement**: Does user need to be authenticated with SP before clicking button?
2. **Multi-device scenarios**: How to handle users with multiple UAE PASS devices?
3. **Timeout duration**: How long should SP wait for user response before showing fallback?
4. **Analytics tracking**: What metrics to capture for button vs QR channel comparison?
5. **Rollout strategy**: Pilot SPs for initial deployment?

**Related Features**:
- Section 3.1: Consent-Based Document Sharing (core sharing mechanism)
- Section 4.1: Push Notifications (delivery channel)

**Documentation**: TBD (pending feature release)

---

## 4) Notification Features

### 4.1) Push Notifications for Document Events

**Status**: Active
**Release Date**: Pre-2025
**Version**: Stable

**Description**:
- **EN**: Real-time push notifications for document and sharing events
- **AR**: إشعارات فورية لأحداث المستندات والمشاركة

**User Story**:
As a UAE PASS user, I want to receive timely notifications about document availability, expiry, and sharing requests, so that I can take action when needed and keep my documents current.

**Notification Taxonomy**:

**Actionable Notifications** (user must act):
1. **Document Sharing Request**:
   - Triggered when: SP creates sharing request
   - User action: Approve or decline share
   - Example (EN): "Bank ABC is requesting your Emirates ID. Tap to review."
   - Example (AR): «يطلب بنك ABC بطاقة هويتك الإماراتية. اضغط للمراجعة.»

**Informational Notifications** (non-actionable):
1. **Document Issuance**:
   - Triggered when: Requested document becomes available
   - Example (EN): "Your Emirates ID is now available in Documents."
   - Example (AR): «بطاقة هويتك الإماراتية متوفرة الآن في المستندات.»

2. **Document Expiry Reminders**:
   - Timeline: D-30, D-15, D-7, D-5, D-3, D-1 (configurable)
   - Example (EN): "Your Emirates ID expires in 7 days. Request an updated version."
   - Example (AR): «تنتهي صلاحية بطاقة هويتك الإماراتية خلال 7 أيام. اطلب نسخة محدثة.»

3. **Document Revocation**:
   - Triggered when: Issuer revokes stored document (issuer action)
   - Example (EN): "Your Driver License has been revoked. Contact RTA for details."
   - Example (AR): «تم إلغاء رخصة القيادة الخاصة بك. اتصل بهيئة الطرق والمواصلات للحصول على التفاصيل.»

4. **Document Removed**:
   - Triggered when: User removes document from storage (user action)
   - Example (EN): "Your Passport has been removed from Documents."
   - Example (AR): «تمت إزالة جواز سفرك من المستندات.»

**UX Guidelines**:
- **Bilingual**: All notifications EN/AR
- **Terminology**: Use "Documents" (never "vault")
- **Foreground**: Supplement OS banner with in-app cues (badge, snackbar, inbox)
- **Missed notifications**: Provide in-app alerts (bell inbox, banners)
- **Clear CTAs**: Actionable notifications have clear action buttons
- **Truncation**: Test in both languages to avoid cutoff

**Technical Implementation**:
- **Platform**: Firebase Cloud Messaging (FCM)
- **Channels**: iOS (APNs), Android (FCM)
- **Payload**: Contains notification type, document details, deep link
- **Deep linking**: Opens relevant screen in app (sharing request, document details, etc.)
- **Remote Config**: A/B testing notification copy and timing
- **Retry logic**: Handle delivery failures

**Bilingual Support**: Full (EN/AR)

**Known Issues**:
- Duplicate notifications from duplicate correlation IDs (FIXED via DB constraint 2025-01-15)
- Limited error messaging when notification delivery fails

**Improvement Opportunities**:
- In-app notification center (persistent inbox)
- Notification preferences (user controls timing and types)
- Rich notifications (images, action buttons)
- Notification analytics (delivery rate, open rate, action rate)

**Dependencies**:
- Firebase Cloud Messaging
- iOS APNs / Android FCM
- DV backend (notification triggering)
- Remote Config (A/B testing)

**Documentation**: KB Section 5

---

### 4.2) In-App Alerts and Banners

**Status**: Partial (in development)
**Release Date**: Ongoing enhancements
**Version**: Beta

**Description**:
In-app visual cues to supplement push notifications when app is in foreground.

**Key Capabilities**:
- **Badge indicators**: Unread notification count on Documents tab
- **Snackbar alerts**: Temporary toast-style messages at bottom of screen
- **Banner overlays**: Full-screen or partial overlays for critical alerts

**User Story**:
As a UAE PASS user, I want to see important alerts even when the app is open, so that I don't miss critical sharing requests or document updates.

**Bilingual Support**: Full (EN/AR)

**Known Issues**:
- Bell inbox concept not fully implemented
- Inconsistent alert styling across screens
- No persistence for missed in-app alerts

**Documentation**: KB Section 5

---

## 5) UX Enhancement Features

### 5.1) Document Details and Actions

**Status**: Active
**Release Date**: Pre-2025
**Version**: 4.x

**Description**:
Detailed view of individual documents with actions menu.

**Document Details Screen**:
- **Header**: Document type, issuer logo, status badge
- **Metadata**: Issue date, expiry date, document number, issuer
- **Preview**: PDF thumbnail or embedded viewer
- **Actions menu**: View PDF, Download, Share, Remove

**Actions Available**:

**View PDF**:
- Opens full PDF viewer (native)
- Pinch-to-zoom
- Page navigation

**Download PDF**:
- Saves PDF to device storage
- User selects location
- Requires storage permission

**Share PDF** (external):
- System share sheet
- Can share via email, messaging apps, etc.
- Not the same as DV Document Sharing (to SPs)

**Remove Document**:
- Confirmation dialog
- Cannot be undone
- Must re-request to restore

**Bilingual Support**: Full (EN/AR)

**Known Issues**:
- Inconsistent PDF rendering across devices

**UX Enhancements Planned (2025)**:
- PDF Viewer Revamp: Native viewer, fit-to-width, snap-to-page, unified padding
- Copy-any-field affordance (tap to copy field values)
- More actions menu cleanup
- Consistent iconography

**Documentation**: KB Section 6.2, 13

---

## 6) Advanced User Features (In Development / Pending)

### 6.1) Dual Citizenship Support (Primary/Secondary EID)

**Status**: In Development
**Release Date**: Q1 2025 (target)
**Version**: TBD

**Description**:
- **EN**: Support for users granted "Special Emirati Citizenship" while retaining original residency
- **AR**: دعم المستخدمين الحاصلين على "الجنسية الإماراتية الخاصة" مع الاحتفاظ بالإقامة الأصلية

**User Story**:
As a user with dual citizenship (UAE + another nationality), I want to store both my Primary EID (UAE) and Secondary EID (2nd nationality), so that I can use the correct ID for different purposes while avoiding confusion.

**Goal**: Primary EID (UAE) vs Secondary EID (2nd nationality) classification

**Detection & State**:
- **Server flag**: `isDualUser` from DDA auth API
- **One-time flag**: `welcomePopupShown` (tracks if welcome shown)
- **Inventory**: `hasPrimaryEID`, `hasSecondaryEID`

**Document Addition Flow**:

**Visibility**:
- Show "Secondary EID (2nd nationality)" option ONLY if `isDualUser = true`
- Regular users see only standard "Emirates ID" option

**First-Time User (no EIDs)**:
1. User with `isDualUser = true` opens Documents
2. Welcome popup explains Primary vs Secondary EID
3. User can request both Primary and Secondary
4. Cards show chips: "Primary EID (UAE)" / "Secondary EID (2nd nationality)"

**Migration Flow (existing EID)**:
1. User has existing EID stored
2. System detects `isDualUser = true`
3. Reclassify existing EID as "Secondary EID (2nd nationality)"
4. Show CTA: "Request your Primary EID (UAE)"
5. User taps to request Primary EID from ICP
6. Both EIDs now stored with clear labels

**Sharing Flow**:
- **Default**: Always use Primary EID (UAE) for sharing (ICP requirement)
- **Secondary not allowed**: ICP instruction - Secondary cannot be shared
- **If Primary missing**: Prompt user to request Primary EID before sharing
- **Welcome popup**: Shows once (Documents or Sharing screen), tracked via `welcomePopupShown`

**Visual Design**:
- **Chips on cards**: "Primary EID (UAE)" / "Secondary EID (2nd nationality)"
- **Color coding**: Primary (blue), Secondary (gray) - TBD by DDA
- **Icons**: Different icons for clarity

**Key Capabilities**:
- Detect dual citizenship users via API flag
- Store and manage two EIDs with clear labels
- Default to Primary EID for sharing
- One-time welcome popup with clear explanation
- Migration flow for existing users
- Deep links support doc type IDs
- Full EN/AR/RTL accessibility

**Technical Implementation**:
- Backend API returns `isDualUser` flag in auth response
- App stores `welcomePopupShown` flag locally
- Document request API supports Primary vs Secondary parameter
- Sharing logic enforces Primary EID default
- Card rendering shows appropriate chips

**Bilingual Support**: Full (EN/AR)

**Known Issues**: None (in development)

**Dependencies**:
- ICP backend support for dual EID requests
- DDA design sign-off on visual design
- Backend API changes (auth flag, document request)

**Stakeholders**:
- TDRA (policy - who qualifies for dual citizenship)
- ICP (issuer - must support dual EID issuance)
- DDA (design approval)

**Open Questions**:
- Final EN/AR labels for chips (pending DDA approval)
- Welcome popup copy finalization
- Migration flow UX details

**Documentation**: KB Section 8

---

### 6.2) Auto-Add Documents (One-Time Consent)

**Status**: Pending Legal/Policy Review
**Release Date**: Q2 2025 (pending legal clearance)
**Version**: TBD

**Description**:
- **EN**: With explicit consent, DV periodically checks issuers and auto-adds new/updated documents
- **AR**: الإضافة التلقائية للمستندات - بموافقة صريحة، يقوم DV بالتحقق دورياً من الجهات المصدرة وإضافة المستندات الجديدة/المحدثة تلقائياً

**Key Principle**: **Sharing remains per-transaction consent** (unchanged - every share still requires explicit approval)

**User Story**:
As a UAE PASS user, I want to enable automatic document updates from issuers, so that my Documents are always current and I don't fail sharing requests due to missing or expired documents.

**Naming**:
- **EN**: "Auto Add Documents"
- **AR**: «الإضافة التلقائية للمستندات»
- **Helper text**: "We'll check with issuers and add new documents for you."

**User Flow**:

**Initial Setup**:
1. User navigates to Settings
2. Finds "Auto Add Documents" toggle (off by default)
3. Taps toggle
4. Consent sheet appears explaining:
   - What: DV will periodically check issuers for new/updated docs
   - Why: Keep documents current, reduce failed shares
   - Scope: Only from trusted issuers (ICP, RTA, MOH, etc.)
   - Frequency: Daily checks (configurable)
   - Privacy: No sharing with SPs without consent
   - Revocation: Can disable anytime in Settings
   - Audit: All checks logged for transparency
5. User consents (or declines)
6. If consented, toggle enabled

**Ongoing Operation**:
1. DV backend runs daily check (scheduled job)
2. Polls each issuer for new/updated docs for user
3. If new doc found:
   - Auto-adds to Documents (no user action needed)
   - User receives informational notification: "New document added: [Doc Name]"
4. If updated version found:
   - Auto-replaces old version
   - User receives notification: "Document updated: [Doc Name]"

**"Check Now" Button**:
- In Settings, below toggle
- User can trigger manual check anytime
- Shows loading state while checking
- Shows result: "X new documents added" or "No new documents"

**Consent Management**:
- User can revoke consent anytime (toggle off in Settings)
- Revocation takes effect immediately
- Audit log retained per legal requirements

**Key Capabilities**:
- One-time consent for ongoing document discovery
- Daily automated checks with issuers
- Auto-add new documents
- Auto-update expired documents
- Manual "Check now" option
- Revocable consent (toggle off anytime)
- Audit logging of all checks
- Failure notifications
- **Sharing still requires per-transaction consent** (unchanged)

**Value Proposition**:
- **Proactive updates**: Users always have current documents
- **Fewer failed shares**: Reduces 20.6% of failures due to missing docs + 2.1% due to expired docs
- **User convenience**: No manual requests for updates

**Legal/Policy Considerations** (BLOCKER):
- ✅ Verify fit with UAE data protection law
- ✅ Sectoral exceptions (government data)
- ⏳ Consent lifetime and scope (legal review needed)
- ⏳ Revocation UX requirements
- ⏳ Audit retention windows (how long to keep logs?)
- ⏳ TDRA legal sign-off timeline

**Technical Implementation**:
- Backend scheduled jobs (daily checks)
- Issuer polling APIs (same as manual request)
- Consent flag stored per user (`autoAddEnabled`)
- Audit logging table (user ID, timestamp, issuer, result)
- Rate limiting and backoff logic
- Notification triggers for new/updated docs

**Bilingual Support**: Full (EN/AR)

**Known Issues**: None (not yet implemented)

**Dependencies**:
- Legal clearance (BLOCKER)
- TDRA policy approval
- Issuer backend APIs (same as manual request)
- Backend scheduled job infrastructure

**Stakeholders**:
- TDRA (policy approval, legal sign-off)
- Legal team (UAE data protection law compliance)
- Issuers (API rate limits, SLAs)
- DDA (design approval for Settings UI)

**Open Questions** (HIGH PRIORITY):
1. Consent lifetime and scope? (Legal review needed)
2. Audit retention windows? (Legal review needed)
3. Failure surfacing UX? (How to notify user of persistent failures?)
4. TDRA legal sign-off timeline? (Blocks launch date)

**Documentation**: KB Section 9

---

## Feature Status Summary

| Feature | Status | Release Date | Version | Priority |
|---------|--------|--------------|---------|----------|
| **1) Digital Signature** | | | | |
| Qualified eSignature (Uploaded Docs) | Active | Pre-2025 | Stable | High |
| **2) Document Lifecycle** | | | | |
| Document Request | Active | Pre-2025 | 4.x | High |
| Document Storage | Active | Pre-2025 | 4.x | High |
| Document Lifecycle Mgmt | Active | Pre-2025 | 4.x | High |
| **3) Document Sharing** | | | | |
| Consent-Based Sharing (via push/QR/deep link) | Active | Pre-2025 | 4.1 | High |
| "Share with UAE PASS" Button (User-Initiated Push) | In Development | Q1 2026 | TBD | Medium |
| **4) Notifications** | | | | |
| Push Notifications | Active | Pre-2025 | Stable | High |
| In-App Alerts | Partial | Ongoing | Beta | Medium |
| **5) UX Enhancements** | | | | |
| Document Details & Actions | Active | Pre-2025 | 4.x | High |
| **6) Advanced Features** | | | | |
| Dual Citizenship | In Development | Q1 2025 | TBD | High |
| Auto-Add Documents | Pending Legal | Q2 2025 | TBD | High |

**Total Active Features**: 7
**Total In Development**: 2
**Total Pending Review**: 1
**Total Features**: 10

---

## Feature Status Definitions

- **Active**: Live in production, fully supported, stable
- **Partial**: Partially implemented, some capabilities missing
- **Beta**: Released with limited availability or ongoing refinement
- **In Development**: Currently being built, not yet released
- **Pending Review**: Awaiting legal, policy, or design approval
- **Pending Legal**: Blocked by legal/compliance review
- **Deprecated**: No longer recommended, will be removed
- **Sunset**: Removed from production

---

## Features REMOVED from Registry (Not DV Features)

### Authentication/SSO (DDA Responsibility)
- ❌ QR-Based Login (SSO) - Owned by DDA, not DV
- ❌ Deep Link Authentication - Owned by DDA, not DV

### Not Standalone Features (Part of Other Features)
- ❌ QR Code for Sharing Initiation - NOT a standalone feature, merely one of three channels (push/QR/deep link) for triggering Consent-Based Document Sharing
- ❌ Document Views and Navigation - NOT a standalone feature, part of Document Storage
- ❌ Empty States and Onboarding - NOT a standalone feature, UX element across multiple features
- ❌ Arabic Plurals and RTL Support - NOT a standalone feature, cross-cutting UX capability
- ❌ Bilingual Copy and Microcopy - NOT a standalone feature, cross-cutting UX capability

### Not Existing Features (Planned or Broken)
- ❌ QR Code Document Verification - NOT an active feature (described as broken/problematic in problem analysis docs, pending revamp)
- ❌ Grid View - NOT existing (planned for 2025)

### Platform & Infrastructure (Not User-Facing DV Features)
- ❌ eSeal Validation - Backend capability, not user-facing DV feature
- ❌ Cloud Sync and Backup - Infrastructure, not user-facing DV feature
- ❌ Analytics and Telemetry - Internal tooling, not user-facing DV feature

### Security & Privacy (Not Standalone DV Features)
- ❌ Consent Management - Part of Consent-Based Sharing, not standalone
- ❌ Data Encryption - Underlying security, not standalone DV feature
- ❌ Audit Logging - Backend capability, not user-facing DV feature

### Support & Operational (Not Standalone DV Features)
- ❌ Error Handling and User Messaging - Cross-cutting capability, not standalone feature
- ❌ Remote Configuration (A/B Testing) - Internal tooling, not user-facing DV feature

---

## Known Issues & Limitations (Consolidated)

### Critical Issues (Blocking User Success):
1. **Document Sharing Failures (20.6%)**: SPs requesting docs users don't have → Need document pre-check API
2. **Consent Screen Abandonment (16.9%)**: High drop-off at consent review → UX redesign needed

### High Priority Issues:
3. **Expired Documents (2.1% of failures)**: Users unaware docs expired → Auto-Add Documents feature addresses
4. **Android Performance Gap (10 points)**: iOS 77.8% vs Android 67.7% conversion → Optimization sprint needed
5. **Inconsistent Empty States**: Copy and design vary across screens → Redesign in progress

### Medium Priority Issues:
6. **No Document Pre-Check API**: SPs cannot verify availability before request → 72K futile requests/week
7. **No Centralized Expiry Dashboard**: Users cannot see all expiring docs → Gap identified
8. **Limited Error Messaging**: Some errors too technical or missing → Ongoing refinement
9. **Equal Weight Issued/Uploaded Tabs**: Despite different SP value → UX enhancement planned

### Low Priority Issues:
10. **Type View Limited Usefulness**: Only good for one-to-many docs → Grid view will address (when implemented)
11. **No Selective Disclosure**: All-or-nothing sharing → Future enhancement
12. **Truncation in Arabic**: Some screens cut off long text → Ongoing fixes
13. **Legacy "Vault" Terminology**: Some screens still use old term → Copy refresh in progress

---

## Dependencies & Integration Points

### External Systems:
- **ICP** (Issuer): EID, Visa, Passport issuance
- **DDA**: Authentication service (external to DV), eSeal service (transitioning), design authority, external sharing consent feature
- **TDRA**: Policy, regulatory compliance, approvals
- **Service Providers**: Document consumers (banks, telcos, government, hospitals, hotels, etc.)
- **Other Issuers**: RTA (driving/vehicle), MOH (health), MOE (education), etc.

### Internal Systems:
- **UAE PASS Auth**: User authentication and identity (managed by DDA)
- **Firebase**: Push notifications, Remote Config, Analytics
- **DV Backend**: Document storage, sharing orchestration, issuer polling
- **DSS** (Digital Signature Service): eSeal validation
- **Cloud Storage**: Encrypted document backup

### APIs:
- **Issuer APIs**: Document request and retrieval
- **SP APIs**: Callback for verifiable presentation delivery
- **DDA APIs**: Authentication (external to DV), eSeal validation
- **Firebase APIs**: FCM, Remote Config, Analytics

---

## Glossary (Quick Reference)

- **DV**: Digital Vault / Digital Documents component
- **eSeal**: Cryptographic organization stamp (issuer authentication, not eSignature)
- **eSignature**: Person-level cryptographic signature (qualified electronic signature for uploaded documents)
- **Verifiable Presentation**: Package of user documents/attributes for SP, includes issuer eSeals
- **Correlation ID**: Unique SP request identifier for sharing flow (time-boxed, one-time use)
- **Primary EID**: Emirates ID for UAE citizenship (dual citizenship users)
- **Secondary EID**: Emirates ID for 2nd nationality (dual citizenship users)
- **Revocation**: Issuer-side action to invalidate document
- **Removal**: User-side action to remove document from Digital Vault
- **SP**: Service Provider (banks, telcos, insurers, government services)
- **ICP**: High-volume document issuer (EID, Visa, Passport)
- **DDA**: Design Authority (design/UX partner, service provider, manages authentication/SSO and external sharing consent)
- **TDRA**: Telecommunications and Digital Government Regulatory Authority (regulator, product owner)
- **MAU**: Monthly Active Users
- **Successful Combos %**: Percentage of SP-requested document sets fully satisfied on first share attempt
- **TTL**: Time-to-live (expiration time for QR codes, requests, etc.)
- **CAdES**: CMS Advanced Electronic Signatures (eSeal standard)
- **PAdES**: PDF Advanced Electronic Signatures (eSeal standard)
- **DSS**: Digital Signature Service (eSeal validation)
- **FCM**: Firebase Cloud Messaging (push notifications)
- **RTL**: Right-to-left (Arabic text direction)

---

## Change Log

| Date | Change | Description | Updated By |
|------|--------|-------------|------------|
| 2025-12-25 | Registry Created | Initial comprehensive feature registry created from knowledge base, agent specs, and session artifacts | Feature Registry Expert |
| 2025-12-25 | Major Scope Correction | Removed Authentication/SSO (DDA), Platform/Infrastructure, Security/Privacy, Support features. Clarified DV vs DDA boundaries. Corrected feature count to 10 active/in-development DV features. | Feature Registry Expert |
| 2025-12-25 | QR Code Correction | Removed "QR Code for Sharing Initiation" as standalone feature (Section 3.2). QR code is merely one of three channels for triggering Consent-Based Document Sharing, not a feature itself. Updated registry to show QR/push/deep link as delivery channels within Consent-Based Sharing feature. Feature count corrected to 9. | Feature Registry Expert |
| 2026-02-16 | New Feature Added | Added Section 3.2: "Share with UAE PASS" Button (User-Initiated Push Notification Sharing). Status: In Development, Q1 2026 target. This is a new sharing initiation pattern where users click a button on SP website to trigger push notification for consent, complementing existing QR/deep link/SP-initiated push channels. Feature count updated to 10. | Feature Registry Expert |

---

## Next Steps & Maintenance

### Immediate Actions:
1. **Stakeholder Review**: Share corrected registry with TDRA, DDA, Engineering for validation
2. **Gap Filling**: Identify missing information (metrics, dates, stakeholders)
3. **Cross-Reference**: Validate against Jira, Figma, and SharePoint sources
4. **Bilingual Audit**: Ensure all user-facing features have EN/AR descriptions

### Ongoing Maintenance:
1. **Weekly Updates**: Review sprint deliverables and update feature status
2. **Quarterly Audits**: Full registry review for accuracy and completeness
3. **Deprecation Tracking**: Mark features as deprecated when superseded
4. **New Feature Intake**: Add features as they launch or enter development
5. **Metrics Refresh**: Update KPIs and analytics data monthly

### Integration with Workflow:
- **New Feature Agent**: Consults registry before designing new features (avoid duplication)
- **PM Working Doc**: Registry status feeds into roadmap planning
- **Stakeholder Queries**: Registry is first point of reference for "what does DV do?" questions
- **Onboarding**: New team members start with registry as orientation

---

**End of Feature Registry**

*This document is the single source of truth for UAE PASS Digital Vault features. For detailed technical/operational information, consult `uae_pass_knowledge_base.md`. For roadmap and metrics, see `pm_dv_working_doc.md`.*
