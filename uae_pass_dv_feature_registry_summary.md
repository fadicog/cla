# UAE PASS DV Feature Registry - Executive Summary

**Last Updated**: 2025-12-25T12:00:00Z
**Version**: 2.0 (Corrected Scope)
**Registry Version**: 2.0

---

## Quick Stats

- **Total Features**: 10
- **Active Features**: 8
- **In Development**: 1
- **Pending Legal Review**: 1
- **Deprecated**: 0

---

## Feature Categories

### 1) Digital Signature Features (1 feature)
- **Qualified eSignature (for Uploaded Documents)** - Active
  - Self-sign user-uploaded PDFs in the "Uploaded" tab
  - Person-level cryptographic signature for attestation
  - Legally binding electronic signature

### 2) Document Lifecycle Features (3 features)
- **Document Request (from Issuers)** - Active
  - Request official documents from ICP, RTA, MOH, MOE, etc.
  - Support for Issued Documents (eSeal-protected) and Uploaded Documents (user PDFs)

- **Document Storage** - Active
  - Secure encrypted storage with cloud sync
  - Two tabs: Issued Documents (high trust) / Uploaded Documents (self-signed)
  - Two active views: List View, Type-based View (Grid View planned for 2025)

- **Document Lifecycle Management** - Active
  - Automated expiry reminders (D-30, D-15, D-7, D-5, D-3, D-1)
  - Revocation notifications (issuer action)
  - Document removal by user (user action)
  - Updated version prompts

### 3) Document Sharing Features (2 features)
- **Consent-Based Document Sharing** - Active
  - Per-transaction explicit user consent
  - 67.4% overall conversion rate (350K+ requests analyzed)
  - Verifiable presentation with issuer eSeals
  - Status tracking system with 23 status codes
  - Major insights: 20.6% failures due to missing docs, 16.9% consent abandonment

- **QR Code for Sharing Initiation** - Active
  - In-person, web-to-mobile, and kiosk flows
  - Unique correlation IDs (DB constraint enforced)
  - Short TTL, one-time use, no PII

### 4) Notification Features (2 features)
- **Push Notifications for Document Events** - Active
  - Actionable: Document sharing requests
  - Informational: Issuance, expiry reminders, revocation, removal
  - Firebase Cloud Messaging (FCM)
  - Full bilingual support (EN/AR)

- **In-App Alerts and Banners** - Partial (Beta)
  - Badge indicators, snackbar alerts, banner overlays
  - Bell inbox concept not fully implemented

### 5) UX Enhancement Features (1 feature)
- **Document Details and Actions** - Active
  - View PDF, Download, Share (external), Remove
  - PDF viewer with pinch-to-zoom, page navigation
  - Copy-any-field planned for 2025

### 6) Advanced User Features (2 features)
- **Dual Citizenship Support (Primary/Secondary EID)** - In Development (Q1 2025)
  - Primary EID (UAE) vs Secondary EID (2nd nationality) classification
  - Detection via `isDualUser` API flag
  - Always use Primary EID for sharing (ICP requirement)

- **Auto-Add Documents (One-Time Consent)** - Pending Legal Review (Q2 2025)
  - One-time consent for daily automated issuer checks
  - Auto-add new documents, auto-update expired documents
  - Manual "Check now" option
  - Sharing still requires per-transaction consent (unchanged)
  - BLOCKER: Legal/policy review needed

---

## Scope Boundaries (CRITICAL)

### What IS Part of DV
✅ Document request, storage, lifecycle management
✅ Consent-based sharing with SPs
✅ Qualified eSignature for uploaded documents
✅ Push notifications for document events
✅ Document details and actions

### What IS NOT Part of DV
❌ **Authentication/SSO** - Owned by DDA (QR-Based Login, Deep Link Authentication)
❌ **Platform/Infrastructure** - Backend capabilities (eSeal validation, cloud sync, analytics)
❌ **Security/Privacy** - Underlying capabilities (consent management, encryption, audit logging)
❌ **Support/Operational** - Cross-cutting tools (error handling, remote config/A/B testing)
❌ **DDA Sharing Consent Feature** - External to DV, managed by DDA for third-party SP document sharing

### Features NOT Existing
❌ QR Code Document Verification - NOT active
❌ Grid View - Planned for 2025, not existing
❌ Empty States/Onboarding - Not a distinct feature
❌ Arabic Plurals/RTL - Not a feature (cross-cutting capability)
❌ Bilingual Copy - Not a feature (cross-cutting standard)

---

## Top Priorities & Known Issues

### Critical Issues (Blocking User Success)
1. **Document Sharing Failures (20.6%)** - SPs requesting docs users don't have → Need document pre-check API
2. **Consent Screen Abandonment (16.9%)** - High drop-off at consent review → UX redesign needed

### High Priority Issues
3. **Expired Documents (2.1% of failures)** - Auto-Add Documents feature will address (pending legal)
4. **Android Performance Gap (10 points)** - iOS 77.8% vs Android 67.7% conversion → Optimization needed
5. **Inconsistent Empty States** - Copy and design vary across screens → Redesign in progress

### Improvement Opportunities (from Data Analysis)
1. **Document Pre-Check API** - Eliminate 72K futile requests/week
2. **Consent Screen Redesign** - Reduce 16.9% drop-off
3. **Android Optimization** - Close 10% platform gap
4. **Issuer Retry Logic** - Reduce 26% of technical failures

**Potential Impact**: +31,500 shares/week (+13.3% improvement) → Target: 76% conversion rate

---

## Key Terminology

- **Revocation** - Issuer-side action to invalidate document
- **Removal** - User-side action to remove document from Digital Vault
- **eSignature** - Person-level signature for uploaded documents (Qualified eSignature)
- **eSeal** - Issuer-level cryptographic stamp for issued documents
- **DV** - Digital Vault / Digital Documents component
- **DDA** - Design Authority (owns authentication/SSO, external sharing consent)
- **ICP** - High-volume issuer (EID, Visa, Passport)
- **SP** - Service Provider (banks, telcos, government services)

---

## Recent Changes

### Version 2.0 (2025-12-25) - Major Scope Correction
- **REMOVED Authentication/SSO** (DDA responsibility): QR-Based Login, Deep Link Authentication
- **REMOVED Platform/Infrastructure**: eSeal Validation, Cloud Sync, Analytics
- **REMOVED Security/Privacy**: Consent Management, Data Encryption, Audit Logging
- **REMOVED Support/Operational**: Error Handling, Remote Config
- **REMOVED Non-Existing Features**: QR Code Verification, Grid View, Empty States, Arabic Plurals, Bilingual Copy
- **CLARIFIED** eSignature scope: Uploaded documents only (not issued documents)
- **CLARIFIED** Revocation vs Removal: Issuer action vs user action
- **CLARIFIED** DDA sharing consent feature: External to DV
- **Corrected feature count**: From 35+ to 10 actual DV features

---

## Dependencies

### External Systems
- **ICP** - EID, Visa, Passport issuance
- **DDA** - Authentication (external to DV), eSeal service, design authority, external sharing consent
- **TDRA** - Policy, regulatory compliance, approvals
- **Service Providers** - Document consumers (banks, telcos, government, etc.)
- **Other Issuers** - RTA, MOH, MOE, etc.

### Internal Systems
- **UAE PASS Auth** - User authentication (managed by DDA, external to DV)
- **Firebase** - Push notifications, Remote Config, Analytics
- **DV Backend** - Document storage, sharing orchestration, issuer polling
- **DSS** - Digital Signature Service (eSeal validation)
- **Cloud Storage** - Encrypted document backup

---

## Quick Reference

**Full Registry**: `uae_pass_dv_feature_registry.md`
**Knowledge Base**: `uae_pass_knowledge_base.md`
**PM Working Doc**: `pm_dv_working_doc.md`

**For Questions**:
- "What does DV do?" → This summary + full registry
- "What's the status of [feature]?" → Full registry
- "What's on the roadmap?" → PM Working Doc
- "How does [feature] work?" → Knowledge Base

---

**End of Summary**

*Last updated: 2025-12-25T12:00:00Z by Feature Registry Expert*
