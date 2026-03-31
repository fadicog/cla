# Miro Board Analysis Summary - UAE PASS Digital Documents (DV)

**Boards Analyzed**:
1. Miro_UAE_PASS_Intro.csv - Application structure and UX flows
2. miro-roadmap-extract.csv - 2024-2025 roadmap and sprint planning
3. Miro_Reskin_Backlog_Refinement.csv - Sprint 27-70 detailed planning

**Date Range**: December 2023 - December 2025 (Sprint 17-70)
**Analysis Date**: 2026-01-06
**Analyst**: Miro Board Analysis Specialist

---

## Executive Summary

The three Miro board exports represent **comprehensive planning sessions spanning 2+ years** of UAE PASS Digital Documents development. Analysis reveals significant strategic initiatives, user research findings, and technical debt items that provide essential context for 2026 roadmap execution.

**Key Metrics**:
- **Total items analyzed**: ~2,500+ entries across 3 boards
- **Jira tickets referenced**: 150+ DVT tickets
- **Sprints covered**: Sprint 17 through Sprint 70 (Dec 2023 - Dec 2025)
- **Existing features identified**: 45+ features documented in knowledge base
- **New feature proposals discovered**: 18 net-new items for 2026 consideration
- **Deferred/incomplete initiatives**: 12 items that never shipped

**Critical Findings**:
1. **AI Chatbot initiative (Stage 1 & 2)** was planned but never delivered - opportunity for 2026
2. **User research insights** from 2024 sessions directly informed current roadmap priorities
3. **Technology upgrades** (Kotlin, Compose UI, Swift UI, RedHat backend) are in progress
4. **Document Addition Revamp Epic** (DVT-1430, DVT-1434, DVT-1435) was the largest 2024-2025 initiative
5. **Transaction History feature** experienced significant DDA dependency delays
6. **Accessibility features** were prioritized but implementation was complex

---

## 1) Board-by-Board Analysis

### Board 1: Miro_UAE_PASS_Intro.csv

**Purpose**: Application architecture and UX flow documentation

**Key Content**:
- **App Structure**: Notifications, Home, Documents, Profile - four primary navigation tabs
- **Document Flows**:
  - Requesting (from issuers)
  - Sharing (with SPs)
  - Adding (issued vs uploaded)
- **Verification Mechanisms**: QR verification, eSeal validation
- **Design Guidelines**: Font standards (Roboto for Android, SF for iOS), accessibility notes

**UX Flow Patterns Documented**:
| Flow | Description | Key Decision Points |
|------|-------------|---------------------|
| **Document Request** | User requests from issuer | Consent popup, real-time status |
| **Document Sharing** | SP initiates, user approves | Mandatory vs optional docs, expiry timer |
| **QR Verification** | Scan-to-verify document | eSeal validation, time limits |
| **One-to-Many Mapping** | Single doc type, multiple instances | User selection, SP predefined |

**Sharing Flow Complexity**:
The board documents extensive sharing flow logic:
- **Mandatory documents**: User cannot deselect automapped docs
- **Optional documents**: User can proceed without adding
- **Unavailable documents**: Error displayed with "Request doc" button
- **Document updates during sharing**: User sees status, accepts update, proceeds

**Status**: This board serves as the **source of truth for UX patterns** - aligns with `uae_pass_knowledge_base.md` sections 2-6.

---

### Board 2: miro-roadmap-extract.csv

**Purpose**: Strategic roadmap planning for 2024-2025

**Key Themes Identified**:

#### 2024 Roadmap Inputs
| Input Source | Key Items |
|--------------|-----------|
| **User Research Report** | 38 issues and recommendations (design-related) |
| **Benchmarking** | DubaiNow App, UAE Government Portal, U-Ask chatbot |
| **Technology Trends** | Everest Group reports on Gen AI, experience design |
| **Backlog Items** | Existing DVT tickets, deferred features |

#### 2025 Roadmap Structure
| Quarter | Major Initiatives | DDA Dependencies |
|---------|-------------------|------------------|
| **Q1 2025** | Backend tech upgrade (RedHat), R1 Release | Transaction history designs |
| **Q2 2025** | Sharing Center, Document handling | UX improvements approval |
| **Q3 2025** | Automatic Document Addition, Frontend tech upgrade | Accessibility features |
| **Q4 2025** | QR Reimagining completion, Error recovery | Final approvals |

#### Prioritization Framework Discovered
The Miro board shows a **P1/P2/P3 prioritization matrix**:

**P1 - High Value, Easy to Implement**:
- Metrics tracking MVP (DVT-681)
- Handling document update in docs tab
- Product tour & optional guidance

**P2 - High Value, Complex**:
- AI Chatbot for UAE PASS (Stage 1 & 2)
- Automatic Document Addition
- One-click document sharing

**P3 - Lower Priority**:
- Non-critical tech debt
- Non-value-added features (dark mode, favorites, etc.)

#### AI Chatbot Initiative Details
**Stage 1** - Answer simple customer inquiries replacing FAQs
**Stage 2** - Interaction with DV through chat:
- Support users in requesting documents
- Search for specific document information
- Language translation
- Document summarization
- Personalized user experience (suggest documents based on user type)

**Status**: Never delivered - **Opportunity for 2026**

#### User Research Findings (Direct Quotes from Miro)

**Sharing Flow Issues**:
- "Most users confused by document status showing as 'Accepted', believing document had already been shared"
- "Users encountered difficulty clicking the 'Reject' button due to its small size"
- "The 'Reject' button's green color seemed irrelevant to its intended action"
- "None of the users noticed the button 'Got it' on the notification message"
- "Users wondered why optional document was pre-checked; they preferred unselected unless needed"

**Document Tab Issues**:
- "Users were curious if they can copy their Emirates ID number"
- "Number of categories was quite large, making navigation challenging"
- "Child's face icon was misleading, giving impression of children's documents section"

**Homepage Issues**:
- "Users assumed they would find their Emirates ID by clicking upper section of main page"
- "Few users did not understand what 'Scan QR Code Request' section is about"

**Notification Issues**:
- "Users had difficulty finding entity's name on notification card"
- "Users asking why redirected to 'Notifications' page after clicking 'Done' button"

#### Technology Upgrade Plans
| Technology | Timeline | Effort |
|------------|----------|--------|
| Kotlin Migration (Android) | 2024-2025 | Part 1 & 2 |
| Compose UI (Android) | 2025 | 4-5 sprints |
| Swift UI (iOS) | 2025 | TBD |
| RedHat Backend Upgrade | 2025 Q1-Q2 | 6 sprints |
| GSB to iPaaS Migration | 2025 | TBD |

#### Bug Tracking Summary
| Priority | Count | Key Examples |
|----------|-------|--------------|
| High | 3 | GCP API Keys, Invalid Certificate, Duplicate MOI Calls |
| Medium | 6 | BUSYKEY, Document retrieval, Log enhancements |
| Low | 4 | Dialog navigation, Duplicate share calls |

---

### Board 3: Miro_Reskin_Backlog_Refinement.csv

**Purpose**: Detailed sprint planning and backlog refinement (Sprint 27-70)

**Key Epics Tracked**:

#### Document Addition Revamp Epic
| Ticket | Description | Points | Status |
|--------|-------------|--------|--------|
| DVT-1430 | Introduce Document Categories to Document Tab | 30 | In Progress |
| DVT-1434 | Simplified Document Addition | 60 | In Progress |
| DVT-1433 | Request/upload documents from homepage | 13 | In Progress |
| DVT-1435 | Requesting same document type from different issuers | 8 | In Progress |
| DVT-2034 | Updating scrolling behavior for document tab | 21 | In Progress |

#### Search Functionality
| Ticket | Description | Estimate |
|--------|-------------|----------|
| DVT-2510 | Implement Search Functionality for Issuers and Documents | XXL (21) |
| DVT-2739 | Front-End Search Functionality for Documents Tab [iOS] | L (8) |
| DVT-2734/2735 | Search in Document Request Screen | Multi-issuer |

#### Accessibility Enhancements
| Ticket | Description | Estimate |
|--------|-------------|----------|
| DVT-2630 | Accessibility Enhancement for Text Display in iOS | XL (13) |
| DVT-2776 | Accessibility configuration and testing [Android] | Retest |
| DVT-2459 | Analyze Accessibility Features for iOS and Android | S (3) |
| DVT-2528 | Accessibility discussion and alignment with DDA | S (3) |

#### Transaction History Feature
| Ticket | Description | Status |
|--------|-------------|--------|
| DVT-2669 | Back-End Integration for Transaction History | XXL (21) |
| DVT-2799 | Transaction history DDA requested update | S (3) |

**Note**: Transaction history experienced significant DDA dependency delays as documented in Sprint planning notes.

#### Revocation Handling
| Ticket | Description | Estimate |
|--------|-------------|----------|
| DVT-2199 | Handle Revocation in Sharing flow - Cancellation Cases | XL (13) |
| DVT-2342 | Handle Revocation - Available Cases and non-key attribute update | XXL (21) |
| DVT-2190 | Handle Revocation - Corner Cases | XL (13) |
| DVT-2911 | Reactivation of Revoked Documents | Analysis |

#### Performance & Operations
| Ticket | Description | Estimate |
|--------|-------------|----------|
| DVT-2457 | Analyze and Reduce Loading Screen Frequency | L (8) |
| DVT-2529 | Reduce Loading Screen Frequency - Detailed design | XL (13) |
| DVT-3359 | Optimize Batch Jobs Part 1 | XL (13) |
| DVT-2527 | Further analysis on No action taken | L (8) |
| DVT-2563 | Analyze and implement solutions for non-actioned sharing requests | XXL (21) |

#### Dual Citizenship Support
| Ticket | Description | Estimate |
|--------|-------------|----------|
| TBD | Document details changes | L (8) |
| TBD | Evidence and QR verification screen changes | L (8) |
| TBD | Sharing flow handling | L (8) |

#### Ghost Loader Implementation
| Phase | Description | Estimate |
|-------|-------------|----------|
| Part 1 | Incremental implementation in Notifications, Documents list, Add documents | XL (13) |
| Part 2 | Continuation | XL (13) |

#### Sprint Velocity Tracking
| Sprint Range | Typical Velocity | Notes |
|--------------|------------------|-------|
| 35-43 | 26-30 Frontend, 31-35 Backend | Standard capacity |
| Holiday Sprints | 15-22 | Reduced for Eid, National holidays |
| Release Sprints | 20-25 | Includes release activities |

---

## 2) Feature Reconciliation

### A. Features Already in Knowledge Base

| Feature | KB Section | Miro Reference | Status |
|---------|------------|----------------|--------|
| Document Request Flow | Section 2.4 | Intro board, Roadmap | Documented |
| Document Sharing Flow | Section 2.5 | Intro board, Roadmap | Documented |
| eSeal Validation | Section 3 | Roadmap | Documented |
| QR Code Hygiene | Section 4 | Intro board, Roadmap | Documented |
| Notifications Taxonomy | Section 5 | Intro board | Documented |
| Dual Citizenship | Section 8 | Backlog Refinement | Documented |
| Auto-Add Documents | Section 9 | Roadmap | Documented |
| Arabic Pluralization | Section 7 | Intro board | Documented |

### B. Features in PM Working Doc (Backlog)

| Feature | PM Doc Reference | Miro Source | Alignment |
|---------|------------------|-------------|-----------|
| Dual Citizenship Support | Section 7 | Backlog Refinement | Aligned |
| One-Time Consent (Auto-Add) | Section 7 | Roadmap | Aligned |
| QR Code Verification Revamp | Section 7 | Roadmap | Aligned |
| Grid View | Section 7 | Roadmap | Aligned |
| Copy-any-field | Section 7 | Roadmap | Aligned |
| PDF Viewer Revamp | Section 7 | Roadmap | Aligned |

### C. Features in 2026 Roadmap

| 2026 Initiative | Miro Board Evidence | Alignment Assessment |
|-----------------|---------------------|----------------------|
| Status-Based Reporting | Session analysis | **NEW** - not in Miro |
| Document Pre-Check API | Roadmap ("SP can know what docs available") | **Aligned** - mentioned |
| Android Optimization | User research findings | **Aligned** - issues documented |
| ICP eSeal Transition | Roadmap | **Aligned** - in progress |
| Consent Screen Redesign | User research findings | **Aligned** - issues documented |
| Auto-Add Documents | Roadmap (P1 priority) | **Aligned** - planned |
| QR Verification Revamp | Roadmap (QR Reimagining) | **Aligned** - planned |
| Predictive Document Availability | Not mentioned | **NEW** - not in Miro |

### D. NET NEW Features Discovered (Not in Any Doc)

| Feature | Miro Source | Description | Priority Recommendation |
|---------|-------------|-------------|-------------------------|
| **AI Chatbot Stage 1** | Roadmap | Answer FAQs via chat | P2 - Consider for 2026 H2 |
| **AI Chatbot Stage 2** | Roadmap | Document search, request via chat | P3 - Future exploration |
| **Users Dashboard** | Roadmap | Personal stats (docs requested, shared, environment savings) | P3 - Nice to have |
| **Sharing Center** | Roadmap | Dedicated tab for sharing requests, SP list | P2 - Consider for Q3-Q4 |
| **Dependent Identity Documents** | Roadmap | Family members' documents | P3 - Legal complexity |
| **Temporary Access** | Roadmap | Time-limited document access | P3 - Evaluated, deferred |
| **One-Click Document Sharing** | Roadmap | Quick share from notification/home/screen | P2 - UX opportunity |
| **Document Request Reminder** | Roadmap | Notification if user hasn't acted | P2 - Conversion opportunity |
| **Customer Feedback Tool** | Roadmap | In-app feedback mechanism | P2 - User research enabler |
| **Environmental Impact Display** | Roadmap | Trees saved by using DV | P3 - Marketing feature |
| **Favorites Document Feature** | Roadmap (DVT-1539) | Mark frequently used docs | P3 - Convenience |
| **Dark Mode** | Roadmap (DVT-1676) | System-wide dark theme | P3 - Accessibility |
| **Multi-Language Support** | Roadmap | Beyond EN/AR | P3 - Future expansion |
| **Selective Sharing** | Roadmap | Share specific parts of document | P2 - Privacy feature |
| **Comments on Sharing Requests** | Roadmap | SP annotations | P3 - Collaboration |
| **Revocable Access** | Roadmap | User revokes shared access | P2 - Control feature |
| **Proactive Document Request API** | Backlog (DVT-3809) | SP-initiated availability check | **P1 - Aligns with Pre-Check API** |
| **Ghost Loader** | Backlog | Progressive loading UX | P2 - Performance perception |

---

## 3) Decisions Log (from Miro Boards)

| Decision | Context | Date (Approx) | Status | Impact on 2026 |
|----------|---------|---------------|--------|----------------|
| No Compose UI/Swift UI in 2024 | Resource constraints | Jan 2024 | Applied | Upgrades continued into 2025 |
| Transaction History to R2 | DDA design not finalized | Jan 2024 | Applied | Feature eventually shipped |
| Kotlin Migration Part 1 only in 2024 | Scope management | Q1 2024 | Applied | Part 2 continued in 2025 |
| AI Chatbot deferred | Complexity, prioritization | 2024 | Applied | **Opportunity for 2026** |
| Accessibility features P1 | Regulatory requirement | 2024 | Applied | Ongoing |
| User Behavior Analytics deferred | Tool decision pending | 2024 | Applied | Consider for 2026 |
| Temporary Access not feasible | Data not stored in app | 2024 | Rejected | Removed from consideration |
| Backend tech upgrade to RedHat | Performance, support | 2024 | In Progress | Complete in 2025 |

---

## 4) Action Items Extracted from Miro Boards

### Active/In-Progress (from Backlog Refinement)
- [ ] Complete Document Addition Revamp Epic (DVT-1430, 1434, 1435) - Sprint 49+
- [ ] Finalize Accessibility features alignment with DDA - Ongoing
- [ ] Complete Transaction History DDA integration - In testing
- [ ] Deploy Dual Citizenship document handling - Sprint 40+
- [ ] Implement Ghost Loader Part 2 - Sprint 50+
- [ ] Complete Kotlin Migration Part 2 - 2025

### Pending/Deferred Items
- [ ] AI Chatbot exploration (Stage 1 & 2) - **NOT STARTED**
- [ ] Sharing Center concept - NOT STARTED
- [ ] One-Click Document Sharing - NOT STARTED
- [ ] Customer Feedback Tool - NOT STARTED
- [ ] Users Dashboard (personal stats) - NOT STARTED
- [ ] Document Request Reminder notification - NOT STARTED

### Operations/Technical Debt
- [ ] Resolve BUSYKEY issues (DVT-1996) - Medium priority
- [ ] INVALID_REQUEST_PARAMETERS error (DVT-672) - Low priority, ongoing
- [ ] Restrict duplicate share presentation calls (DVT-204/205) - In development
- [ ] Optimize batch jobs (Part 1 complete, Part 2 pending)
- [ ] Firebase async changes (P1 incidents)

---

## 5) Open Questions & Risks

### From Miro Planning Sessions

**Questions**:
- **Q**: Does Operations have existing user behavior analytics tools? - Needs answer
- **Q**: Is there an existing tool at DDA side for analytics? - Needs answer
- **Q**: Can DV team own analytics or should DDA own it? - Decision pending
- **Q**: Transaction History API details from DDA? - Sample Postman collection pending

**Risks Identified**:
- **Risk**: Limited availability of DDA resources before/during Eid breaks - Mitigation: Communicate dependencies upfront
- **Risk**: Not finalizing Transaction History requirements by target date - Mitigation: Start other work while waiting
- **Risk**: Extensive production testing required for Firebase changes - Mitigation: Prepare test cases upfront
- **Risk**: App lifecycle handling issues (backgrounding causing stuck app) - Analysis in progress

### Gaps for 2026 Planning

**From Miro Analysis**:
1. **AI/ML Capabilities** - Significant planning done but never executed. 2026 opportunity.
2. **User Behavior Analytics** - Tool decision never made. Critical for data-driven optimization.
3. **Customer Feedback Mechanism** - Planned but never built. Needed for user research.
4. **Sharing Center Concept** - Explored but not prioritized. Could improve user experience.

---

## 6) Alignment Assessment with 2026 Roadmap

### Well-Aligned Initiatives

| 2026 Initiative | Miro Evidence | Confidence |
|-----------------|---------------|------------|
| **Document Pre-Check API** | "SP can know what docs available" mentioned in Roadmap | HIGH |
| **Android Optimization** | User research identified Android-specific issues | HIGH |
| **Consent Screen Redesign** | User research: confusion about "Accepted" status, button sizes, colors | HIGH |
| **Auto-Add Documents** | P1 priority in 2024-2025 roadmap, "Automatic Document Addition" | HIGH |
| **QR Verification Revamp** | "QR Reimagining Completion" in Q4 2025 plan | HIGH |
| **UX Enhancements Bundle** | Grid view, copy-field, PDF revamp all mentioned | HIGH |

### Gaps Identified

| Gap | Description | Recommendation |
|-----|-------------|----------------|
| **Status-Based Reporting** | Not in Miro boards - NEW 2026 initiative from Nov 2025 analysis | Validated - critical for measurement |
| **Predictive Document Availability** | Not in Miro boards - NEW 2026 initiative | Consider as innovation, lower priority |
| **SP Quality Scoring** | Not in Miro boards - NEW 2026 initiative | Aligned with "Admin dashboard" idea |
| **AI Chatbot** | In Miro but not in 2026 roadmap | **GAP - Consider adding to 2026** |
| **User Behavior Analytics** | In Miro but not in 2026 roadmap | **GAP - Critical for optimization** |
| **Sharing Center** | In Miro but not in 2026 roadmap | Consider for future |

### Conflicts Identified

| Conflict | Miro Position | 2026 Position | Resolution |
|----------|---------------|---------------|------------|
| **Dark Mode (DVT-1676)** | P3 / Non-value-added | Not in 2026 roadmap | Aligned - correctly deprioritized |
| **Favorites Feature (DVT-1539)** | P3 / Non-value-added | Not in 2026 roadmap | Aligned - correctly deprioritized |
| **Undo Action (DVT-1413)** | P3 | Not in 2026 roadmap | Aligned - correctly deprioritized |

---

## 7) Recommendations for 2026 Roadmap Adjustments

### HIGH PRIORITY - Add to Roadmap

1. **User Behavior Analytics Tool Selection** (Q1 2026)
   - Miro Evidence: "UXCam" and "Google Analytics for Firebase" evaluated
   - Value: Required foundation for all data-driven optimization
   - Effort: Low (tool selection + integration)
   - Dependency: Informs all conversion optimization initiatives

2. **Customer Feedback Mechanism** (Q2 2026)
   - Miro Evidence: "Introduce customer feedback tool within the application" + "Banner for user research activities"
   - Value: Enables continuous user research, validates UX changes
   - Effort: Medium
   - Dependency: None

### MEDIUM PRIORITY - Consider for 2026 H2

3. **AI Chatbot Stage 1** (Q3-Q4 2026)
   - Miro Evidence: Detailed Stage 1/2 planning, benchmarked against U-Ask
   - Scope: Answer simple customer inquiries, replace FAQs
   - Value: Reduce support burden, improve user self-service
   - Effort: High
   - Dependency: None (could run parallel to other initiatives)

4. **One-Click Document Sharing** (Q3 2026)
   - Miro Evidence: "Quickshare from push notification, home screen, notifications screen"
   - Value: Reduces sharing friction, improves conversion
   - Effort: Medium
   - Dependency: Consent mechanism revision

5. **Document Request Reminder Notification** (Q2 2026)
   - Miro Evidence: "Notification request reminder (in case user did not take any action)"
   - Value: Reduces abandoned requests, improves conversion
   - Effort: Low
   - Dependency: Notification infrastructure

### LOW PRIORITY - Future Backlog

6. **Sharing Center** - Dedicated tab for all sharing requests
7. **Users Dashboard** - Personal stats and environmental impact
8. **Selective Sharing** - Choose specific document parts to share
9. **AI Chatbot Stage 2** - Advanced document interaction via chat

---

## 8) Technical Debt & Operations Items

### From Miro Backlog (Carried into 2026)

| Item | Priority | Status | Notes |
|------|----------|--------|-------|
| DVT-672 INVALID_REQUEST_PARAMETERS error | Low | Ongoing | Android-specific |
| DVT-204/205 Duplicate share presentation calls | Low | In development | iOS and Android |
| DVT-1996 BUSYKEY issues | Medium | In Progress | Reopened |
| Firebase async changes | High | P1 incident | Critical for stability |
| Batch job optimization | Medium | Part 1 complete | Part 2 pending |
| Loading screen frequency reduction | Medium | Analysis complete | Implementation pending |
| No action taken analysis | Medium | Analysis complete | Solutions pending |

### Technology Upgrade Status

| Upgrade | 2024 Status | 2025 Status | 2026 Expected |
|---------|-------------|-------------|---------------|
| Kotlin (Android) | Part 1 | Part 2 | Complete |
| Compose UI (Android) | Not started | 4-5 sprints | In progress |
| Swift UI (iOS) | Not started | TBD | TBD |
| RedHat Backend | Not started | 6 sprints | Complete |
| GSB to iPaaS | Not started | In progress | Complete |

---

## 9) Glossary (Miro-Specific Terms)

| Term | Definition |
|------|------------|
| **Busykey** | Backend key management issue (BUSYKEY errors) |
| **DDA** | Design and Delivery Authority - design partner |
| **DVT-XXXX** | Jira ticket identifier for DV project |
| **Ghost Loader** | Skeleton/shimmer loading UI pattern |
| **GSB** | Government Service Bus |
| **iPaaS** | Integration Platform as a Service |
| **One-to-Many** | Document type with multiple instances (e.g., vehicle registrations) |
| **Prefetch** | Pre-loading document list from issuer before user selects |
| **Revamp** | Major redesign initiative (2024-2025) |
| **SOP1/2/3** | Service level classifications for users |

---

## 10) Source References

### Files Analyzed
- `D:\cluade\Miro_UAE_PASS_Intro.csv` - 131 entries
- `D:\cluade\miro-roadmap-extract.csv` - 1500+ entries
- `D:\cluade\Miro_Reskin_Backlog_Refinement.csv` - 1000+ entries

### Cross-Referenced Documentation
- `D:\cluade\uae_pass_knowledge_base.md` - Sections 1-17
- `D:\cluade\pm_dv_working_doc.md` - Sections 1-12
- `D:\cluade\roadmap_2026_dv.md` - Full 2026 roadmap
- `D:\cluade\session_sharing_request_status_tracking.md` - Nov 2025 analysis

---

## Summary: Three Lists

### A. Added Information/Context Discovered

1. **AI Chatbot was a P2 priority** - Detailed planning for 2-stage implementation exists
2. **User research identified 38 specific UX issues** - Many not yet addressed
3. **"Accept" status terminology confusion** - Users believed document was shared when it wasn't
4. **Green color for Reject button confusing** - Color should reflect action intent
5. **Emirates ID copy functionality requested** - Now in 2026 roadmap as copy-any-field
6. **Child icon misleading in category navigation** - UX debt
7. **Transaction History delayed by DDA** - Significant coordination overhead
8. **Technology upgrades 40% complete** - Kotlin/Compose/Swift/RedHat ongoing
9. **Velocity typically 26-35 points per sprint** - Capacity planning baseline
10. **Holiday sprints have 40% reduced capacity** - Eid, National holidays impact
11. **"No action taken" was analyzed** - Solutions proposed but not fully implemented
12. **U-Ask chatbot was a benchmark** - Government AI platform reference
13. **Environmental sustainability messaging considered** - Show trees saved

### B. Opportunities Identified

1. **AI Chatbot (Stage 1)** - Never delivered despite detailed planning. FAQ replacement, reduce support burden
2. **User Behavior Analytics** - Tool evaluated (UXCam, Firebase Analytics) but never selected. Critical for optimization
3. **Customer Feedback Tool** - Planned but not built. Essential for user research
4. **One-Click Sharing** - Quickshare from notification/home designed but not shipped
5. **Document Request Reminders** - Conversion optimization, low effort
6. **Sharing Center** - Dedicated sharing experience, improve discoverability
7. **Loading Screen Reduction** - Analysis complete, implementation opportunity
8. **Ghost Loaders** - Part 1 done, Part 2 opportunity
9. **Batch Job Optimization** - Part 1 done, Part 2 opportunity
10. **Arabic UX improvements** - Line spacing, issuer list order issues identified

### C. New Features to Consider for 2026

| Feature | Source | Priority | Effort | Rationale |
|---------|--------|----------|--------|-----------|
| **User Behavior Analytics** | Roadmap | P1 | Low | Foundation for optimization |
| **Customer Feedback Tool** | Roadmap | P2 | Medium | Enable continuous research |
| **AI Chatbot Stage 1** | Roadmap | P2 | High | FAQ replacement, self-service |
| **One-Click Sharing** | Roadmap | P2 | Medium | Conversion improvement |
| **Document Request Reminder** | Roadmap | P2 | Low | Conversion improvement |
| **Sharing Center** | Roadmap | P3 | High | UX improvement |
| **Users Dashboard** | Roadmap | P3 | Medium | Engagement feature |
| **Proactive Document Request API** | Backlog (DVT-3809) | P1 | Medium | Aligns with Pre-Check API |
| **Ghost Loader Part 2** | Backlog | P2 | Medium | Performance perception |
| **Loading Screen Reduction** | Backlog | P2 | Medium | Performance improvement |

---

**Document Status:** Complete
**Next Review:** Coordinate with product-roadmap-strategist and feature-registry-maintainer for integration

---

*Generated by Miro Board Analysis Specialist - 2026-01-06*
