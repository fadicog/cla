# UAE PASS Digital Vault - 2026 Roadmap

**Source**: `ppt roadmap.pptx`
**Slide Count**: 34
**Converted**: 2026-02-19
**Purpose**: 2026 product roadmap for UAE PASS Digital Vault (DV), covering 28 epics across Product, Design, UX, Technical, and SP categories with timelines, owners, dependencies, and acceptance criteria.

---

## Table of Contents

- [Summary Table](#summary-table)
- [Epic 1 — Slide 31: Dual Citizenship](#epic-1--slide-31-dual-citizenship)
- [Epic 2 — Slide 32: Status-Based Reporting Implementation](#epic-2--slide-32-status-based-reporting-implementation)
- [Epic 3 — Slide 33: SP Offboarding](#epic-3--slide-33-sp-offboarding)
- [Epic 4 — Slide 34: Home Page Revamp](#epic-4--slide-34-home-page-revamp)
- [Epic 5 — Slide 2: Form Filler](#epic-5--slide-2-form-filler)
- [Epic 6 — Slide 3: UX Enhancements Bundle - 1](#epic-6--slide-3-ux-enhancements-bundle---1)
- [Epic 7 — Slide 4: Document Request Revision](#epic-7--slide-4-document-request-revision)
- [Epic 8 — Slide 5: Auto-Add Documents Launch / One-Time Consent](#epic-8--slide-5-auto-add-documents-launch--one-time-consent)
- [Epic 9 — Slide 6: Document Sharing Revision](#epic-9--slide-6-document-sharing-revision)
- [Epic 10 — Slide 7: User Behavior Analytics Tool Selection](#epic-10--slide-7-user-behavior-analytics-tool-selection)
- [Epic 11 — Slide 8: Consent Sharing (Third Party Data)](#epic-11--slide-8-consent-sharing-third-party-data)
- [Epic 12 — Slide 9: Enable Download of All Issued Documents in DV](#epic-12--slide-9-enable-download-of-all-issued-documents-in-dv)
- [Epic 13 — Slide 10: UX/UI Enhancements Bundle 2](#epic-13--slide-10-uxui-enhancements-bundle-2)
- [Epic 14 — Slide 11: Design Audit](#epic-14--slide-11-design-audit)
- [Epic 15 — Slide 13: Design System Update](#epic-15--slide-13-design-system-update)
- [Epic 16 — Slide 14: Accessibility Enhancement](#epic-16--slide-14-accessibility-enhancement)
- [Epic 17 — Slide 15: Over the Counter Document Sharing](#epic-17--slide-15-over-the-counter-document-sharing)
- [Epic 18 — Slide 16: QR Code Simplification – Direct Sharing](#epic-18--slide-16-qr-code-simplification--direct-sharing)
- [Epic 19 — Slide 17: UAEVerify SEO](#epic-19--slide-17-uaeverify-seo)
- [Epic 20 — Slide 18: Error to Status Code Linking](#epic-20--slide-18-error-to-status-code-linking)
- [Epic 21 — Slide 19: Infinite Loader Detection and Resolution](#epic-21--slide-19-infinite-loader-detection-and-resolution)
- [Epic 22 — Slide 20: Firebase Configuration and Optimization](#epic-22--slide-20-firebase-configuration-and-optimization)
- [Epic 23 — Slide 21: Service Provider SDK](#epic-23--slide-21-service-provider-sdk)
- [Epic 24 — Slide 22: DR Automation](#epic-24--slide-22-dr-automation)
- [Epic 25 — Slide 24: SP Automation Testing Suite](#epic-25--slide-24-sp-automation-testing-suite)
- [Epic 26 — Slide 25: UAE Verify QR Code Scan vs Doc Upload](#epic-26--slide-25-uae-verify-qr-code-scan-vs-doc-upload)
- [Epic 27 — Slide 26: Blockchain Upgrade](#epic-27--slide-26-blockchain-upgrade)
- [Epic 28 — Slide 27: CI/CD Pipeline Automation](#epic-28--slide-27-cicd-pipeline-automation)
- [Epic 29 — Slide 28: Operation Automation](#epic-29--slide-28-operation-automation)
- [Presentation Summary](#presentation-summary)

---

## Summary Table

| Epic # | Slide | Pool Item # | Feature Name | Category | Priority | Complexity | DDA Item | Sprints | Start Date | End Date |
|--------|-------|-------------|--------------|----------|----------|------------|----------|---------|------------|----------|
| 1 | 31 | #9 | Dual Citizenship | Product | High | Medium | No | 71–72 | 01 Jan 2026 | 28 Jan 2026 |
| 2 | 32 | #1 | Status-Based Reporting Implementation | Product | High | Medium | No | 71–72 | 01 Jan 2026 | 28 Jan 2026 |
| 3 | 33 | #50 | SP Offboarding | SP | Medium | Medium | No | 73–76 | 29 Jan 2026 | 25 Mar 2026 |
| 4 | 34 | #17 | Home Page Revamp | Design | High | Medium | No | 74–76 | 12 Feb 2026 | 25 Mar 2026 |
| 5 | 2 | #19 | Form Filler | Product | High | Low | No | 79–82 | 23 Apr 2026 | 17 Jul 2026 |
| 6 | 3 | #7 | UX Enhancements Bundle - 1 | UX | High | Medium | No | 75–76 | 26 Feb 2026 | 25 Mar 2026 |
| 7 | 4 | #37 | Document Request Revision | UX | High | Medium | No | 77–80 | 26 Mar 2026 | 20 May 2026 |
| 8 | 5 | #10 | Auto-Add Documents Launch / One-Time Consent | Product | High | Low | No | 81–86 | 21 May 2026 | 12 Aug 2026 |
| 9 | 6 | #38 | Document Sharing Revision | UX | High | Medium | No | 81–86 | 21 May 2026 | 12 Aug 2026 |
| 10 | 7 | #5 | User Behavior Analytics Tool Selection | Product | High | Medium | Yes (DDA Dependent) | 82–84 | 04 Jun 2026 | 15 Jul 2026 |
| 11 | 8 | #20 | Consent Sharing (Third Party Data) | Product | High | High | No | 83–85 | 18 Jun 2026 | 29 Jul 2026 |
| 12 | 9 | #40 | Enable Download of All Issued Documents in DV | Product | High | Low | No | 87–88 | 13 Aug 2026 | 09 Sep 2026 |
| 13 | 10 | #18 | UX/UI Enhancements Bundle 2 | UX | High | Medium | No | 87–94 | 13 Aug 2026 | 03 Dec 2026 |
| 14 | 11 | #35 | Design Audit | Design | High | Low | No | 74–77 | 12 Feb 2026 | 08 Apr 2026 |
| 15 | 13 | #16 | Design System Update | Design | High | Medium | Yes (DDA Dependent) | 76–78 | 12 Mar 2026 | 22 Apr 2026 |
| 16 | 14 | #36 | Accessibility Enhancement | Design | High | High | Yes (DDA Dependent) | 79–82 | 23 Apr 2026 | 17 Jun 2026 |
| 17 | 15 | #41 | Over the Counter Document Sharing (Physical Document Sharing) | Product | High | High | No | 89–94 | 10 Sep 2026 | 03 Dec 2026 |
| 18 | 16 | #51 | QR Code Simplification – Direct Sharing | Technical | High | Medium | No | 73–77 | 29 Jan 2026 | 08 Apr 2026 |
| 19 | 17 | #52 | UAEVerify SEO | SP | — | — | No | 73 | 30 Jan 2026 | 10 Feb 2026 |
| 20 | 18 | #8 | Error to Status Code Linking | Technical | High | Low | No | 74–76 | 12 Feb 2026 | 15 Mar 2026 |
| 21 | 19 | #28 | Infinite Loader Detection and Resolution | Technical | High | Low | No | 71–75 | 31 Jan 2025 | 11 Mar 2026 |
| 22 | 20 | #29 | Firebase Configuration and Optimization | Technical | High | Low | No | — | 15 Jan 2026 | 15 Mar 2026 |
| 23 | 21 | #53 | Service Provider SDK | SP | High | Low | No | — | 01 Apr 2026 | 30 May 2026 |
| 24 | 22 | #54 | DR Automation | Technical | High | Low | No | — | 15 Mar 2026 | 30 Jun 2026 |
| 25 | 24 | #55 | SP Automation Testing Suite | SP | High | Low | No | 75–76 | 26 Feb 2026 | 25 Mar 2026 |
| 26 | 25 | #26 | UAE Verify QR Code Scan vs Doc Upload (License QR Fix) | Technical | High | Low | No | — | 15 Jul 2026 | 25 Sep 2026 |
| 27 | 26 | #56 | Blockchain Upgrade | Technical | High | Low | No | — | 01 Aug 2026 | 30 Jan 2027 |
| 28 | 27 | #57 | CI/CD Pipeline Automation | Technical | High | Low | No | — | 01 Oct 2026 | 30 Nov 2026 |
| 29 | 28 | #58 | Operation Automation | Technical | High | Low | No | — | 01 Oct 2026 | 30 Dec 2026 |

> Note: Slides 1, 12, 23, 29, and 30 are title/section divider slides with no epic content and are excluded from the epic list above.

---

## Epic 1 — Slide 31: Dual Citizenship

**Pool Item #**: #9
**Category**: Product
**Priority**: High
**Complexity**: Medium
**DDA Item**: No

### Epic Name
Dual Citizenship

### Objectives
- Finalize Primary/Secondary EID handling across all relevant flows.
- Complete EN/AR copy approval and validate edge cases to reduce user confusion and support load.
- Ensure downstream integrations behave correctly for both primary and secondary identifiers.

### Description
Complete Primary/Secondary EID handling with final EN/AR copy approval and edge case handling.

### Acceptance Criteria
- User can add/manage primary and secondary EID where applicable without breaking existing accounts.
- All impacted screens have approved EN/AR copy.
- Edge cases covered: switching primary, duplicate detection, and issuer retrieval using the correct identifier.
- No increase in authentication failure rate after release (tracked for first 2 weeks).

### Owners
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance
- Customer Support / Ops

### Dependencies
- ICP/DDA Dual citizenship flag availability.
- Backend validation rules for primary/secondary EID storage and retrieval.
- Regression coverage for authentication, profile, and document flows.

### Timeline
- **Dates**: 01 Jan 2026 – 28 Jan 2026
- **Sprints**: 71–72
- **Priority/Complexity**: High/Medium

### Target Audience
- UAE PASS users
- Support & Operations teams

---

## Epic 2 — Slide 32: Status-Based Reporting Implementation

**Pool Item #**: #1
**Category**: Product
**Priority**: High
**Complexity**: Medium
**DDA Item**: No

### Epic Name
Status-Based Reporting Implementation

### Objectives
- Introduce a consistent 23-status-code model for sharing requests so we can measure success/failure end-to-end.
- Store status transition history (previous status + timestamp) to enable journey analysis and operational reporting.
- Provide initial dashboards/reports that answer: volume, success rate, drop-off points, and top failure reasons.

### Description
Implement a consistent status model and status history for sharing requests to enable end-to-end reporting, diagnostics, and analytics.

### Acceptance Criteria
- Every sharing request is assigned exactly one current status from the agreed set.
- All status changes are persisted with timestamps and previous status.
- At least 3 core reports are available: overall success rate, drop-off by status, and top failure/error categories.
- Support team can map a user case to its latest status using a request identifier.

### Owners
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance
- Customer Support / Ops

### Dependencies
- Agreement on the canonical status model and definitions (product + support).
- Database schema update to store status transitions and history.
- Instrumentation updates in backend services and clients to emit status transitions.
- Report consumer (dashboard / export) decision and access control.

### Timeline
- **Dates**: 01 Jan 2026 – 28 Jan 2026
- **Sprints**: 71–72
- **Priority/Complexity**: High/Medium

### Target Audience
- UAE PASS users
- Service Providers
- Support & Operations teams
- Product & Analytics stakeholders

---

## Epic 3 — Slide 33: SP Offboarding

**Pool Item #**: #50
**Category**: SP
**Priority**: Medium
**Complexity**: Medium
**DDA Item**: No

### Epic Name
SP Offboarding

### Objectives
- Provide a controlled way to offboard Service Providers without breaking active user journeys.
- Remove stale integrations and reduce operational burden.

### Description
To create a process for offboarding already onboarded Service Providers, with the option of re-onboarding.

### Acceptance Criteria
- Provider can be disabled via configuration without a new app release (where possible).
- Offboarding is logged and auditable (who/when/why).
- No critical errors caused by disabled providers in production.

### Owners
- Service Provider Onboarding team
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Inventory of active Service Providers and their integration method.
- Backend flags/config to disable providers safely (with rollback).
- Support playbook and communications plan for affected providers/users.

### Timeline
- **Dates**: 29 Jan 2026 – 25 Mar 2026
- **Sprints**: 73–76
- **Priority/Complexity**: Medium/Medium

### Target Audience
- UAE PASS users
- Service Providers
- Support & Operations teams

---

## Epic 4 — Slide 34: Home Page Revamp

**Pool Item #**: #17
**Category**: Design
**Priority**: High
**Complexity**: Medium
**DDA Item**: No

### Epic Name
Home Page Revamp

### Objectives
- Redesign the DV home page to surface the most-used actions and recent items immediately.
- Reduce time-to-task for frequent journeys (share, request).
- Improve engagement by making status, alerts, and shortcuts visible and consistent.

### Description
Redesign the DV home page to prioritize top tasks and reduce navigation friction.

### Acceptance Criteria
- Home page highlights 3–5 primary actions and recent/important items without scrolling on common devices.
- Users can reach top tasks within 1–2 taps from home.
- Analytics events added for key home interactions (cards, shortcuts).

### Owners
- Product Design (UX/UI)
- Product Management
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Agreement on the primary jobs-to-be-done for the home screen.
- Analytics baseline for current home usage and drop-offs.
- Design system update alignment (components, spacing, typography).

### Timeline
- **Dates**: 12 Feb 2026 – 25 Mar 2026
- **Sprints**: 74–76
- **Priority/Complexity**: High/Medium

### Target Audience
- UAE PASS users

---

## Epic 5 — Slide 2: Form Filler

**Pool Item #**: #19
**Category**: Product
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
Form Filler

### Objectives
- Auto-fill Service Provider forms using existing document data to reduce manual typing.
- Support user review and edit before submission to avoid incorrect data.
- Improve completion rate for forms by reducing time and errors.

### Description
Auto-fill forms using stored document data to streamline user workflows. Note: Service Provider related.

### Acceptance Criteria
- Field mapping is versioned so form changes do not silently break auto-fill.
- Metrics tracked: time-to-complete and form submission success rate.

### Owners
- Service Provider Enablement/Partnerships
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Mapping between DV document fields and Service Provider form fields.
- Consent and data-sharing rules for populating third-party forms.
- SDK or integration method for Service Providers to adopt the feature.

### Timeline
- **Dates**: 23 Apr 2026 – 17 Jul 2026
- **Sprints**: 79–82
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Epic 6 — Slide 3: UX Enhancements Bundle - 1

**Pool Item #**: #7
**Category**: UX
**Priority**: High
**Complexity**: Medium
**DDA Item**: No

### Epic Name
UX Enhancements Bundle - 1

### Objectives
- Improve the documents list view so users can find, filter, and act on documents faster.
- Reduce cognitive load by clarifying document status, issuer, and last update at a glance.
- Support common actions directly from the list (view, share, download) with fewer taps.

### Description
This is a placeholder item to implement the outcomes of design audit and Design system epics.

### Acceptance Criteria
TBD

### Owners
- Product Design (UX/UI)
- Product Management
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Analytics/funnel data to prioritize list pain points (filter usage, search behavior).
- Design system components availability and alignment.
- Backend APIs support for filtering/sorting (if not already available).

### Timeline
- **Dates**: 26 Feb 2026 – 25 Mar 2026
- **Sprints**: 75–76
- **Priority/Complexity**: High/Medium

### Target Audience
- UAE PASS users

---

## Epic 7 — Slide 4: Document Request Revision

**Pool Item #**: #37
**Category**: UX
**Priority**: High
**Complexity**: Medium
**DDA Item**: No

### Epic Name
Document Request Revision

### Objectives
- Redesign the document request flow so users understand what is being requested and why.
- Reduce request abandonment by simplifying steps and clarifying expected outcomes.
- Improve request success rate and reduce support escalations.

### Description
Redesign the document request journey with clearer steps, better copy, and trackable outcomes aligned to the status model.

### Acceptance Criteria
- Request flow has clear steps: select provider/context → confirm scope → send → track outcome.
- User can track request status using the status model (e.g., sent, viewed, completed, failed).
- Error states include actionable recovery steps (retry, contact support, change provider).
- A/B or usability review indicates improved comprehension vs current flow.

### Owners
- Product Design (UX/UI)
- Product Management
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Service Provider requirements for request payload and response handling.
- Copywriting in EN/AR for key request states and error handling.
- Status model alignment so request states map cleanly to reporting.

### Timeline
- **Dates**: 26 Mar 2026 – 20 May 2026
- **Sprints**: 77–80
- **Priority/Complexity**: High/Medium

### Target Audience
- UAE PASS users
- Service Providers

---

## Epic 8 — Slide 5: Auto-Add Documents Launch / One-Time Consent

**Pool Item #**: #10
**Category**: Product
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
Auto-Add Documents Launch / One-Time Consent

### Objectives
- Introduce one-time consent allowing DV to periodically check for new/updated issued documents.
- Auto-add eligible documents to the user's vault with clear visibility and control.
- Reduce manual steps for users who frequently receive updated documents.

### Description
One-time consent for DV to periodically check and auto-add new/updated documents from issuers. Note: Pending Legal TDRA approval.

### Acceptance Criteria
- User can grant one-time consent and review what it enables (scope, frequency, revocation).
- System can detect and auto-add new/updated documents from participating issuers.
- User is notified (in-app and/or push) when a document is added/updated, with a link to view details.
- User can revoke consent and stop further checks; revocation takes effect within the stated window.

### Owners
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance
- Customer Support / Ops
- Legal/Compliance (approval gates)

### Dependencies
- Legal/TDRA approval for consent language and periodic checks (noted as a gate).
- Issuer availability and rules for which documents can be auto-added.
- Notification/UX design for new document events and opt-out controls.

### Timeline
- **Dates**: 21 May 2026 – 12 Aug 2026
- **Sprints**: 81–86
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Participating issuers / Service Providers
- Legal & Compliance

---

## Epic 9 — Slide 6: Document Sharing Revision

**Pool Item #**: #38
**Category**: UX
**Priority**: High
**Complexity**: Medium
**DDA Item**: No

### Epic Name
Document Sharing Revision

### Objectives
- Redesign the sharing flow to increase successful shares and reduce retries.
- Make selection, consent, and confirmation steps obvious and lightweight.
- Improve failure recovery: clear reasons, next steps, and support hooks.

### Description
Revamp the sharing flow across selection, consent, confirmation, and failure recovery, tied to status-based reporting for measurable improvements.

### Acceptance Criteria
- Share flow supports: select document(s) → select recipient/provider → confirm scope/consent → share → track result.
- Failures show the mapped status/error category and a recommended action (retry, switch channel, contact support).
- Share success rate baseline established and post-release tracked.
- Support can diagnose a failed share using request ID and status history.

### Owners
- Product Design (UX/UI)
- Product Management
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Status-based reporting to identify top failure states and where users drop off.
- Design system components for consistent share UI patterns.
- Backend support for retry-safe operations and better error messages.

### Timeline
- **Dates**: 21 May 2026 – 12 Aug 2026
- **Sprints**: 81–86
- **Priority/Complexity**: High/Medium

### Target Audience
- UAE PASS users
- Service Providers
- Support teams

---

## Epic 10 — Slide 7: User Behavior Analytics Tool Selection

**Pool Item #**: #5
**Category**: Product
**Priority**: High
**Complexity**: Medium
**DDA Item**: Yes (DDA Dependent)

### Epic Name
User Behavior Analytics Tool Selection

### Objectives
- Select a user-behavior analytics tool that supports session replay and key funnels for DV journeys.
- Instrument core flows to measure drop-offs and time-to-complete (home → select doc → share/request).
- Enable Real User Monitoring (RUM) signals to correlate performance issues with user impact.

### Description
Select and integrate analytics tool (UXCam/Firebase Analytics) to enable data-driven optimization, session replay, and Real User Monitoring (RUM) for user behavior patterns. Relates to: Epic 1.

### Acceptance Criteria
- Tool decision documented with reasons (capabilities, cost, privacy/security, integration effort).
- Event taxonomy defined for at least 10 key events + 3 funnels.
- Dashboards show funnel conversion + top screens with rage taps/crashes/performance issues.
- Session replay is enabled for approved users with PII masking rules.

### Owners
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance
- Customer Support / Ops

### Dependencies
- Security, privacy, and data retention review for candidate tools (e.g., Firebase Analytics vs UXCam).
- Mobile app instrumentation plan and event taxonomy aligned to the status model.
- Access model for who can view session replays (PII considerations).

### Timeline
- **Dates**: 04 Jun 2026 – 15 Jul 2026
- **Sprints**: 82–84
- **Priority/Complexity**: High/Medium

### Target Audience
- UAE PASS users
- Service Providers
- Support & Operations teams
- Product, UX, Engineering leads

---

## Epic 11 — Slide 8: Consent Sharing (Third Party Data)

**Pool Item #**: #20
**Category**: Product
**Priority**: High
**Complexity**: High
**DDA Item**: No

### Epic Name
Consent Sharing (Third Party Data)

### Objectives
- Enable sharing of third-party data through an explicit, user-controlled consent mechanism.
- Standardize consent capture (who, what, why, duration) to support audits and user trust.
- Support downstream APIs to verify consent before data is shared.

### Description
Sharing third party data via providing consent mechanism.

### Acceptance Criteria
- Before any third-party data is shared, the user is shown scope + purpose and must confirm.
- Consents are stored with timestamp, requester identity, scope, and expiry (if applicable).
- User can view and revoke active consents.
- APIs enforce consent checks and log consent reference IDs for audit.

### Owners
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance
- Customer Support / Ops
- Legal/Compliance (approval gates)

### Dependencies
- Consent model definition (data fields, TTL/expiry, revocation) and storage.
- UX patterns for clear disclosure and granular selection where needed.
- Legal/compliance review for consent wording and audit requirements.

### Timeline
- **Dates**: 18 Jun 2026 – 29 Jul 2026
- **Sprints**: 83–85
- **Priority/Complexity**: High/High

### Target Audience
- UAE PASS users
- Service Providers requesting third-party data
- Legal & Compliance
- Audit/Operations

---

## Epic 12 — Slide 9: Enable Download of All Issued Documents in DV

**Pool Item #**: #40
**Category**: Product
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
Enable Download of All Issued Documents Types in DV

### Objectives
- Allow users to download all issued documents available in DV.
- Reduce friction for users who need offline copies for personal record-keeping or external submissions.
- Ensure downloads respect issuer rules and user entitlements.

### Description
Enable downloading all issued documents in DV.

### Acceptance Criteria
- Enable the download of all the visualization based documents in Digital Vault.

### Owners
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance
- Customer Support / Ops

### Dependencies
- Backend support for bulk selection and secure file packaging.
- Rate limiting and security controls to prevent abuse.

### Timeline
- **Dates**: 13 Aug 2026 – 09 Sep 2026
- **Sprints**: 87–88
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Support & Operations teams

---

## Epic 13 — Slide 10: UX/UI Enhancements Bundle 2

**Pool Item #**: #18
**Category**: UX
**Priority**: High
**Complexity**: Medium
**DDA Item**: No

### Epic Name
UX/UI Enhancements Bundle 2

### Objectives
- Deliver the second bundle of UI/UX improvements based on feedback and observed behavior.
- Address the top 3 usability issues discovered after analytics tooling is in place.

### Description
Second bundle of UI/UX improvements based on design audit, design system update and accessibility findings.

### Acceptance Criteria
TBD

### Owners
- Product Design (UX/UI)
- Product Management
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Design Audit
- Design System Update
- Accessibility Reports

### Timeline
- **Dates**: 13 Aug 2026 – 03 Dec 2026
- **Sprints**: 87–94
- **Priority/Complexity**: High/Medium

### Target Audience
- UAE PASS users

---

## Epic 14 — Slide 11: Design Audit

**Pool Item #**: #35
**Category**: Design
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
Design Audit

### Objectives
- Review core screens and journeys and capture pain points with evidence (screenshots, examples).
- Identify quick wins vs larger redesign candidates and propose sequencing.
- Align priorities with Product and Engineering so the backlog is implementation-ready.

### Description
UI/UX designer reviews the current screens to identify room for improvement and the biggest pain points (usability, clarity, consistency). Output is a prioritized backlog with recommended fixes.

### Acceptance Criteria
- Audit report delivered with issues grouped by severity/impact and linked to screens.
- Prioritized improvement backlog created (with effort sizing placeholders).
- Top quick wins have clear specs and acceptance criteria ready for development.

### Owners
- Product Design (UX/UI)
- Product Management
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Agreed scope of screens/flows to audit.
- Access to current designs/build, and top support ticket themes (if available).
- Review workshop with key stakeholders to finalize priorities.

### Timeline
- **Dates**: 12 Feb 2026 – 08 Apr 2026
- **Sprints**: 74–77
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users

---

## Epic 15 — Slide 13: Design System Update

**Pool Item #**: #16
**Category**: Design
**Priority**: High
**Complexity**: Medium
**DDA Item**: Yes (DDA Dependent)

### Epic Name
Design System Update (DDA Dependent)

### Objectives
- Update and enhance the DV design system components and patterns based on current product needs.
- Align DV and DDA design standards where applicable to reduce divergence.
- Improve implementation consistency by publishing clear guidelines and reusable assets.

### Description
Joint effort with the DDA UI/UX team to update and enhance the DV design system so it stays up to date and supports consistent implementation across teams.

### Acceptance Criteria
- Updated design system published with versioning and change log.
- High-usage components are standardized and adopted in the app.
- New work uses updated components; legacy screens have a migration plan.

### Owners
- Product Design (UX/UI)
- DDA UX/UI Team (joint)
- Product Management
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Regular working sessions with DDA UI/UX team and agreement on standards.
- Component inventory and gap analysis (what exists vs what's missing).
- Engineering adoption plan for component library updates and migration.

### Timeline
- **Dates**: 12 Mar 2026 – 22 Apr 2026
- **Sprints**: 76–78
- **Priority/Complexity**: High/Medium

### Target Audience
- (Not explicitly stated on slide — internal design and engineering teams implied)

> Note: On slide 13 the Description and Acceptance Criteria text blocks appeared to be swapped in the source PowerPoint. The content above has been re-assigned to the correct sections based on semantic meaning.

---

## Epic 16 — Slide 14: Accessibility Enhancement

**Pool Item #**: #36
**Category**: Design
**Priority**: High
**Complexity**: High
**DDA Item**: Yes (DDA Dependent)

### Epic Name
Accessibility Enhancement (DDA Dependent)

### Objectives
- Improve accessibility compliance across priority screens and critical flows.
- Embed accessibility checks into design, development, and QA so issues don't regress.
- Reduce accessibility-related user friction and support cases.

### Description
Increase the level of accessibility support in the app across key DV screens and flows (screen reader, contrast, dynamic text, focus order, touch targets) and validate against an agreed WCAG target.

### Acceptance Criteria
- Priority flows meet the agreed accessibility checklist (labels, focus, scaling, contrast).
- Accessibility checklist is added to QA and release criteria.
- Remaining gaps are documented with owners and a mitigation plan.

### Owners
- Product Design (UX/UI)
- Product Management
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Define target WCAG level and priority flows in scope.
- Accessibility guidelines for designers and developers (components + content).
- Testing approach (manual + automated) for iOS/Android.

### Timeline
- **Dates**: 23 Apr 2026 – 17 Jun 2026
- **Sprints**: 79–82
- **Priority/Complexity**: High/High

### Target Audience
- (Not explicitly stated on slide — all UAE PASS users implied, particularly those using assistive technologies)

> Note: On slide 14 the Description and Acceptance Criteria text blocks appeared to be swapped in the source PowerPoint. The content above has been re-assigned to the correct sections based on semantic meaning.

---

## Epic 17 — Slide 15: Over the Counter Document Sharing

**Pool Item #**: #41
**Category**: Product
**Priority**: High
**Complexity**: High
**DDA Item**: No

### Epic Name
Over the Counter Document Sharing

### Objectives
- Enable sharing of documents over the counter through UAE PASS.

### Description
Enable sharing of Digital Vault documents over the counter.

### Acceptance Criteria
TBD

### Owners
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance
- Customer Support / Ops

### Dependencies
- Definition of 'verified copy' workflow and acceptable document types.
- Service Provider acceptance format and validation requirements.

### Timeline
- **Dates**: 10 Sep 2026 – 03 Dec 2026
- **Sprints**: 89–94
- **Priority/Complexity**: High/High

### Target Audience
- UAE PASS users
- Service Providers

---

## Epic 18 — Slide 16: QR Code Simplification – Direct Sharing

**Pool Item #**: #51
**Category**: Technical
**Priority**: High
**Complexity**: Medium
**DDA Item**: No

### Epic Name
QR Code Simplification – Direct Sharing

### Objectives
- Address SP feedback on the difficulty of scanning the current QR codes.
- Simplify the UX/UI for sharing.
- Make it easier for SPs to integrate the document sharing functionality.

### Description
Simplify the QR code generation logic and introduce a new way to trigger the sharing requests to the user from the SP channel.

### Acceptance Criteria
TBD

### Owners
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance
- Customer Support / Ops

### Dependencies
- DDA exposure of UDID identification services from email or mobile number or EID.
- Existing integrations with Service Providers.

### Timeline
- **Dates**: 29 Jan 2026 – 08 Apr 2026
- **Sprints**: 73–77
- **Priority/Complexity**: High/Med

### Target Audience
- UAE PASS users
- Service Providers

---

## Epic 19 — Slide 17: UAEVerify SEO

**Pool Item #**: #52
**Category**: SP
**Priority**: — (not specified)
**Complexity**: — (not specified)
**DDA Item**: No

### Epic Name
UAEVerify SEO

### Objectives
- Implement SEO for the UAEVerify portal.

### Description
Need to improve the SEO of the UAEVerify website by adding proper SEO metadata across key pages so the site can rank better in Google search results. This includes adding page-level meta tags and structured information that helps search engines understand the content and display rich previews.

### Acceptance Criteria
- The improved rank for UAEVerify website in Google search; ideally it should appear at the top.
- Meta data per page is as per approved copy.

### Owners
- Service Provider Enablement/Partnerships
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Google algorithm takes its time to improve the ranking (noted as an external dependency with no control).

### Timeline
- **Dates**: 30 Jan 2026 – 10 Feb 2026
- **Sprints**: 73
- **Priority/Complexity**: Not specified

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Epic 20 — Slide 18: Error to Status Code Linking

**Pool Item #**: #8
**Category**: Technical
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
Error to Status Code Linking

### Objectives
- Create the operational dashboard to track the state of the sharing request using the latest status model.

### Description
Auto-fill forms using stored document data to streamline user workflows. Note: Service Provider related.

> Note: The description text on this slide appears to be copied incorrectly from the Form Filler epic. The objectives indicate this epic is about an operational sharing request tracking dashboard linked to the error/status code system.

### Acceptance Criteria
- Should be able to track the sharing request using ID.
- Track the respective state for the sharing request.
- Updated funnel chart.

### Owners
- Service Provider Enablement/Partnerships
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- The data should be present in production in the agreed format; there might be some updates required to optimize the visualization at the DB side.

### Timeline
- **Dates**: 12 Feb 2026 – 15 Mar 2026
- **Sprints**: 74–76
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Epic 21 — Slide 19: Infinite Loader Detection and Resolution

**Pool Item #**: #28
**Category**: Technical
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
Infinite Loader Detection and Resolution

### Objectives
- Detect and resolve infinite loading states across the application.

### Description
Scoped screens and scenarios covered:
- Issuer list
- Download and Share
- QR verification
- Notification list
- Actionable and non-actionable notification details
- Document selection screen
- Include remaining scenarios above

### Acceptance Criteria
- Reduction of the loader (infinite loading states eliminated across covered screens).

### Owners
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
(Not specified)

### Timeline
- **Dates**: 31 Jan 2025 – 11 Mar 2026
- **Sprints**: 71–75
- **Priority/Complexity**: High/Low

> Note: The start date of "31 Jan 2025" appears to be a typo in the source PowerPoint; this epic is likely already in progress from early 2026, consistent with Sprint 71 start.

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Epic 22 — Slide 20: Firebase Configuration and Optimization

**Pool Item #**: #29
**Category**: Technical
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
Firebase Configuration and Optimization

### Objectives
- Create TTL-based document deletion.
- Timely deletion of anonymous users.

### Description
After the incident of 6th December, batch processes were stopped. These batch processors handled deletion of documents from the collection and deletion of anonymous users. As a result, TTL-based document deletion and Google Function-based scheduled deletion of anonymous users are now required.

### Acceptance Criteria
- The collection should have the latest document as per configuration; all older documents should be deleted from Firebase.

### Owners
- Service Provider Enablement/Partnerships
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Google Cloud.

### Timeline
- **Dates**: 15 Jan 2026 – 15 Mar 2026
- **Sprints**: Not specified
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Epic 23 — Slide 21: Service Provider SDK

**Pool Item #**: #53
**Category**: SP
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
Service Provider SDK

### Objectives
- Create a software development kit (SDK) for SPs to improve their implementation time.

### Description
Create a software development kit for Service Providers for Android and iOS app development. The SDK will include all API implementations required for DV integration. It will be easy to integrate — developers need only change the configuration.

### Acceptance Criteria
- Easy-to-integrate setup for app development.

### Owners
- Service Provider Enablement/Partnerships
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- iOS and Android development process SPs are following.

### Timeline
- **Dates**: 01 Apr 2026 – 30 May 2026
- **Sprints**: Not specified
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Epic 24 — Slide 22: DR Automation

**Pool Item #**: #54
**Category**: Technical
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
DR Automation

### Objectives
- Prepare for the automated DR drill which would happen mid-year.

### Description
- Create scripts for making apps live in one environment (DR) and stopped in other (PROD).
- Script to switch the primary DB.
- Script-based traffic switching.

### Acceptance Criteria
- Complete the DR under 20 minutes.

### Owners
- Service Provider Enablement/Partnerships
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- FEDNET

### Timeline
- **Dates**: 15 Mar 2026 – 30 Jun 2026
- **Sprints**: Not specified
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Epic 25 — Slide 24: SP Automation Testing Suite

**Pool Item #**: #55
**Category**: SP
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
SP Automation Testing Suite

### Objectives
- Create the automation testing suite for Service Providers.

### Description
Similar to the SDK for faster development, this testing suite complements development. After development is complete, a set of testing activities will be automated for Service Providers. These will produce results and speed up their testing with the Digital Vault backing.

### Acceptance Criteria
(Not specified)

### Owners
- Service Provider Enablement/Partnerships
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
(Not specified)

### Timeline
- **Dates**: 26 Feb 2026 – 25 Mar 2026
- **Sprints**: 75–76
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Epic 26 — Slide 25: UAE Verify QR Code Scan vs Doc Upload

**Pool Item #**: #26
**Category**: Technical
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
UAE Verify QR Code Scan vs Doc Upload

### Objectives
- Fix License Name and Number not showing when customer scans QR code from UAE Verify portal.

### Description
Fix License Name and Number not showing when customer scans QR code from UAE Verify portal.

### Acceptance Criteria
(Not specified)

### Owners
- Service Provider Enablement/Partnerships
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
(Not specified)

### Timeline
- **Dates**: 15 Jul 2026 – 25 Sep 2026
- **Sprints**: Not specified
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Epic 27 — Slide 26: Blockchain Upgrade

**Pool Item #**: #56
**Category**: Technical
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
Blockchain Upgrade

### Objectives
- Upgrade the Digital Vault blockchain.

### Description
The Blockchain Upgrade project aims to enhance the current blockchain infrastructure by selecting the most suitable blockchain technology, validating feasibility, and ensuring future scalability. The project will be executed in three phases.

### Acceptance Criteria
- Fully functional DV app with new blockchain.

### Owners
- Service Provider Enablement/Partnerships
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
(Not specified)

### Timeline
- **Dates**: 01 Aug 2026 – 30 Jan 2027
- **Sprints**: Not specified
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Epic 28 — Slide 27: CI/CD Pipeline Automation

**Pool Item #**: #57
**Category**: Technical
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
CI/CD Pipeline Automation

### Objectives
- Automate the deployment in respective environments.

### Description
Implement a branching strategy where code committed to a specific branch is automatically deployed to the corresponding environment. For example, code committed to the dev branch triggers deployment to the dev environment.

### Acceptance Criteria
(Not specified)

### Owners
- Service Provider Enablement/Partnerships
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
(Not specified)

### Timeline
- **Dates**: 01 Oct 2026 – 30 Nov 2026
- **Sprints**: Not specified
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Epic 29 — Slide 28: Operation Automation

**Pool Item #**: #58
**Category**: Technical
**Priority**: High
**Complexity**: Low
**DDA Item**: No

### Epic Name
Operation Automation

### Objectives
- Automate the operation tasks.

### Description
Automate the incident report generation.

### Acceptance Criteria
(Not specified)

### Owners
- Service Provider Enablement/Partnerships
- Product Management
- Backend Development
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
(Not specified)

### Timeline
- **Dates**: 01 Oct 2026 – 30 Dec 2026
- **Sprints**: Not specified
- **Priority/Complexity**: High/Low

### Target Audience
- UAE PASS users
- Service Providers (form owners)

---

## Presentation Summary

### Key Themes
- **User Experience Improvement**: Multiple epics (UX Bundle 1 & 2, Document Request Revision, Document Sharing Revision, Home Page Revamp) focus on reducing friction and improving task completion rates.
- **Data & Analytics Enablement**: Status-Based Reporting, Error-to-Status Code Linking, and User Behavior Analytics are foundational to measuring and improving the product.
- **Service Provider Ecosystem**: SP SDK, SP Automation Testing Suite, SP Offboarding, Form Filler, and QR Code Simplification reduce SP integration friction.
- **Design System & Standards**: Design Audit, Design System Update (DDA), and Accessibility Enhancement establish a consistent design foundation.
- **Infrastructure & Technical Debt**: Firebase Optimization, Blockchain Upgrade, CI/CD Automation, DR Automation, Infinite Loader Fixes, and Operation Automation address platform health.
- **Consent & Compliance**: Auto-Add Documents (pending TDRA legal approval) and Consent Sharing (Third Party Data) advance the consent architecture.
- **Dual Citizenship**: Completing primary/secondary EID support as a carry-over from 2025.

### Key Data Points
- 23-status-code model introduced for sharing request tracking (Epic 2).
- DR completion target: under 20 minutes (Epic 24).
- Analytics tool scope: minimum 10 key events + 3 funnels (Epic 10).
- Home page target: top tasks reachable in 1–2 taps (Epic 4).
- Session replay requires PII masking rules (Epic 10).
- Blockchain Upgrade spans into Q1 2027, making it the longest epic in the roadmap.
- Sprint range covered: 71 (Jan 2026) through 94 (Dec 2026).

### Action Items / Calls to Action
- Obtain Legal/TDRA approval for Auto-Add Documents consent language (gate for Epic 8).
- Finalize EN/AR copy approval for Dual Citizenship flows (Epic 1).
- Resolve description/content accuracy issues on slides 18, 13, and 14 (content appears copied from other epics or swapped between sections).
- Define WCAG target level and priority flows for Accessibility Enhancement (Epic 16).
- Confirm sprint assignments for epics currently missing sprint numbers (#22, #23, #24, #26, #27, #28, #29).
- Verify start date typo on Infinite Loaders epic (slide shows "31 Jan 2025" — likely 2026).

### Terminology and Acronyms

| Term | Definition |
|------|------------|
| DV | Digital Vault — UAE PASS component for storing and sharing issued documents |
| SP | Service Provider — banks, telcos, insurers integrating with UAE PASS |
| ICP | Identity and Citizenship Platform — primary document issuer (EID, Visa, Passport) |
| TDRA | Telecommunications and Digital Government Regulatory Authority — regulator and product owner |
| DDA | Design Authority — design/UX partner with approval authority on DDA-dependent epics |
| EID | Emirates ID |
| eSeal | Cryptographic organization stamp for issuer authentication |
| RUM | Real User Monitoring — performance and experience monitoring in production |
| UXCam | Third-party user behavior analytics and session replay tool (candidate for Epic 10) |
| WCAG | Web Content Accessibility Guidelines — target standard for Epic 16 |
| SDK | Software Development Kit — packaged integration library for SPs (Epic 23) |
| DR | Disaster Recovery |
| CI/CD | Continuous Integration / Continuous Deployment |
| TTL | Time To Live — used for Firebase document expiry configuration |
| FEDNET | UAE government network infrastructure (dependency for DR Automation) |
| UDID | Unique Device/User Identifier — used in QR simplification DDA dependency |
| QR | Quick Response code — used in sharing flows and SP integrations |
| PII | Personally Identifiable Information |
| TBD | To Be Determined — acceptance criteria placeholder used on several epics |
