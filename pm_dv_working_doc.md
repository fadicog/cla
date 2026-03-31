# Product Manager - Digital Vault (DV) Working Document
_Role: Product Manager for UAE PASS Digital Documents (DV) Component_
_Started: 2025-11-12_

---

## 1) My Role & Responsibilities
**Scope**: Digital Vault (DV) component of UAE PASS - document issuance, storage, sharing, and user experience.

**Key Stakeholders**:
- **TDRA**: Regulator / Product Owner (policy & priorities)
- **DDA**: Design/UX partner (approvals required for major features)
- **ICP**: High-volume issuer (EID, Visa, Passport)
- **Service Providers (SPs)**: Banks, telcos, insurers consuming user documents
- **Engineering Team**: FE/BE/QA delivering features
- **Ops Team**: Monitoring, support, reliability

**Decision Authority**: [TO BE CLARIFIED]

---

## 2) Product Overview (Baseline Knowledge)

### What is DV?
Digital Vault is the **document management** component of UAE PASS that enables:
1. **Document Request**: Users request official docs from issuers (e.g., ICP)
2. **Document Storage**: Secure storage of issued + uploaded documents
3. **Document Sharing**: Consent-based sharing with Service Providers
4. **Lifecycle Management**: Updates, expiry reminders, revocation notifications

### Document Types
- **Issued Documents**: Official docs from issuers (eSeal-protected, high trust)
- **Uploaded Documents**: User PDFs (self-signed, lower SP trust)

### Core Flows
1. **Authentication/SSO**: QR-based login to SP services
2. **Qualified eSignature**: Person-level consent for transactions
3. **Document Sharing**: SP creates request → User approves → Verifiable presentation delivered

---

## 3) Current Priorities (Top 3)

**North Star Goal**: **Reduce failure cases in document sharing flows**

1. **Improve "Successful Combos %" metric** - Increase % of SP-requested document sets fully satisfied on first share attempt
2. **Reduce friction in sharing flows** - Minimize missing documents, expired docs, and user drop-off
3. **Enable proactive document readiness** - Users have required docs before SP requests them

---

## 4) Success Metrics & KPIs

**Primary KPIs** (my accountability):
- _[TO BE CONFIRMED]_

**Current Performance**:
- MAU: _[?]_
- Successful Combos %: _[?]_ (target: _[?]_)
- Notification Open Rate: _[?]_
- Lost Requests Rate: _[?]_
- SP Satisfaction Score: _[?]_

---

## 5) User Pain Points & Opportunities

### PRIMARY PAIN POINT: Document Sharing Failures 🔴
**Problem**: Users fail to complete document sharing flows with SPs (banks, telcos, etc.)

**Root Causes**:
1. **Missing documents** - User hasn't requested required docs from issuers
2. **Expired documents** - User has outdated version; needs to request update
3. **Revoked documents** - Issuer revoked but user unaware
4. **User drop-off** - Friction during request/approval flow
5. **Notification failures** - User doesn't see sharing request (missed notification)

**Impact**:
- Poor "Successful Combos %" metric
- User frustration (failed transactions at bank/telco/etc.)
- SP dissatisfaction (low conversion rates)
- Support burden (users don't understand why sharing failed)

**How Roadmap Addresses This**:
- **One-Time Consent (Auto-Add)**: Proactively adds new/updated docs before user needs them
- **Dual Citizenship**: Ensures correct EID is available for sharing (no confusion)
- **QR Code Revamp**: Enables lightweight SP verification (hospitals, hotels, HR) without full Document Sharing flow → simpler alternative reduces friction and failures
- **UX Enhancements**: Grid view, empty states, better discovery → easier to find/request missing docs

### Secondary Issues (UX Quality):
1. **Equal weight for Issued vs Uploaded** - despite different SP value
2. **Missing grid view** - users expect it (mental model from file apps)
3. **Inconsistent empty states** - confusing copy
4. **Notification noise** - duplicate correlation IDs causing spam (fixed via DB constraint)

### User Segments:
- _[TO BE CLARIFIED]_

### Underserved Needs:
- _[TO BE DISCOVERED]_

---

## 6) Technical Landscape

### Architecture:
- **Backend**: DV service polls issuers, validates eSeals (DSS), delivers presentations
- **Mobile**: iOS + Android apps (React Native?)
- **Integrations**: ICP (issuer), DDA eSeal service, Firebase (push/RC), SPs (APIs)

### Key Technical Initiatives:
1. **ICP eSeal Transition (2025)**: ICP moving to self-signing (own HSM)
   - Risk: DDA validator compatibility
   - Action: Survey SPs, test in lower envs, update docs
2. **Duplicate Correlation ID Fix**: DB constraint enforced (staged rollout)
3. **PDF Viewer Revamp**: Native viewer, fit-to-width, snap-to-page

### Tech Debt:
- _[TO BE IDENTIFIED]_

---

## 7) Roadmap & Initiatives

### 2026 Roadmap Overview
The 2026 roadmap includes **16 features across 4 categories**, prioritized using a scoring system (Priority + Complexity = Total Score, max 16).

**Roadmap Tools**:
- **Roadmap Builder App**: `D:\claude\roadmap-builder\` - Interactive React app for roadmap planning
- **2026 Presentation**: `D:\claude\UAE_PASS_DV_2026_Roadmap.pptx` - 10-slide PowerPoint deck

#### PRODUCT Features (7 items)
| Score | Feature | Status | Notes |
|-------|---------|--------|-------|
| 16 | Enable Download of All Issued Documents | Planned | New feature |
| 16 | Auto-Add Documents / One-Time Consent | Planned | Pending Legal TDRA approval |
| 13 | Status-Based Reporting Implementation | In Progress | Sprint 70, 23-status-code tracking |
| 13 | User Behavior Analytics Tool Selection | Planned | DDA related, UXCam/Firebase Analytics |
| 13 | Dual Citizenship GA | In Progress | Sprint 72 |
| 11 | Consent Sharing (Third Party Data) | Planned | High complexity |
| 11 | Physical Document Sharing | Planned | High complexity |

#### DESIGN Features (3 items)
| Score | Feature | Status | Notes |
|-------|---------|--------|-------|
| 16 | Design Audit | Planned | To be discussed with Ahmed |
| 13 | Design System Update | Planned | DDA related |
| 11 | Accessibility Enhancement | Planned | DDA related, WCAG compliance |

#### SP Features (1 item)
| Score | Feature | Status | Notes |
|-------|---------|--------|-------|
| 16 | Form Filler | Planned | Auto-fill forms using stored document data |

#### UX Features (5 items)
| Score | Feature | Status | Notes |
|-------|---------|--------|-------|
| 13 | Home Page Revamp | Planned | DDA related |
| 13 | UX Enhancements Bundle - Documents List View | Planned | |
| 13 | UX/UI Enhancements Bundle 2 | Planned | Based on user feedback |
| 13 | Enhancement/Revamp Document Request | Planned | Improve request flow |
| 13 | Revamp Document Sharing | Planned | Increase sharing success |

#### TECHNICAL Features (4 items - not in presentation)
| Score | Feature | Status | Notes |
|-------|---------|--------|-------|
| 16 | Infinite Loaders Detection | In Progress | Sprint 70 |
| 16 | Firebase Configuration & Optimization | Planned | |
| 13 | Error-to-Status Code Linking System | Planned | Automated troubleshooting |
| 13 | ELK Stack AI Upgrade | Planned | Enhanced log analysis |

---

### 2025 Roadmap (Completed/In Progress)
Building the 2025 roadmap with focus on three major initiatives (in progress + pending) plus UX enhancements.

### In Progress (2025 H1):

**1. Dual Citizenship Support** ⚙️
- **Goal**: Support users with "Special Emirati Citizenship" while retaining original residency
- **Scope**:
  - Primary EID (UAE) vs Secondary EID (2nd nationality) classification
  - Welcome popup + migration flow for existing users
  - Default to Primary EID in sharing flows (ICP requirement)
  - Document request visibility based on `isDualUser` flag
- **Status**: In development (design approved, implementation in progress)
- **Launch**: _[Q1 2025 target?]_
- **Dependencies**: ICP backend support for dual EID requests, DDA design sign-off
- **Risks**: Migration complexity for users with existing EID

**2. One-Time Consent (Auto-Add Documents)** ⏳
- **Goal**: With explicit consent, DV periodically checks issuers and auto-adds new/updated docs
- **Scope**:
  - Settings toggle + "Check now" button
  - Consent sheet (scope, revocation, audit logging)
  - Discovery limits per issuer with backoff
  - **Sharing remains per-transaction consent** (unchanged)
- **Status**: Pending legal/policy review
- **Blocker**: UAE data protection law alignment + TDRA legal sign-off
- **Value**: Proactive updates, fewer failed shares due to missing/expired docs
- **Launch**: _[Pending legal clearance - Q2 2025?]_
- **Open Questions**:
  - Consent lifetime and scope?
  - Audit retention windows?
  - Failure surfacing UX?

**3. QR Code Verification Revamp** 🔄 ✅
- **Goal**: Fix critical security gaps in QR verification + enable high-value in-person use cases
- **Status**: Research complete; awaiting stakeholder decision (Week of 2025-11-14)
- **Current State**:
  - QR verification exists but has critical security gaps:
    - ❌ No document binding (verifier can't confirm QR matches specific document shown)
    - ❌ No anti-replay protection (screenshots work indefinitely)
    - ❌ No time limits (static QR, no expiration)
    - ❌ No telemetry (product team blind to usage/abuse)
  - **Impact**: Unusable for high-trust use cases (hospitals, hotels, HR, landlords)
- **Benchmarking Completed** (2025-11-14):
  - Analyzed 5 global leaders: Singapore Singpass, EU Digital Identity Wallet, Apple Wallet Digital ID, India DigiLocker, W3C VC standards
  - All leaders have secure, user-controlled QR verification with document binding + anti-replay
  - UAE PASS is behind global standards
- **Strategic Options Analyzed**:
  - ❌ Option 1: Remove feature (loses strategic value, competitive gap vs global leaders)
  - ✅ **Option 2: Revamp & Expand (RECOMMENDED)** - Fix security gaps, enable new use cases, match global leaders
  - ⚠️ Option 3: Enhance minimally (doesn't solve core problem, creates technical debt)
- **Recommended Solution** (Option 2):
  - **Phase 1 MVP (Q1 2025, 4-6 months)**:
    - Masked document reference (e.g., `784-XXXX-XXXXXXX-X`)
    - Time-limited QR (5 min TTL + visual countdown)
    - Anti-replay protection (nonce + timestamp validation)
    - Redesigned UAE Verify portal (mobile-first, clear status badges)
    - Telemetry + monitoring
  - **Phase 2 Advanced (Q2 2025, +3-4 months)**:
    - NFC tap-to-verify
    - Selective disclosure (choose attributes to share)
    - W3C Verifiable Credentials alignment
    - Lightweight SP onboarding (QR-Only SP tier)
- **Use Cases Unlocked**:
  - 🏥 Hospital/clinic check-in (patient identity verification)
  - 🏨 Hotel check-in (guest registration, no ID photocopy)
  - 💼 Employer verification (HR onboarding, credential fraud reduction)
  - 🏦 Bank branch verification
  - 🏡 Landlord verification (rental contracts)
- **Business Impact**:
  - 10x SP ecosystem growth (lightweight QR-Only SP onboarding)
  - 500,000+ verifications/month target (12 months post-launch)
  - Matches global leaders (Singpass, EU Wallet, Apple Digital ID)
  - Reduces document sharing failures (simpler alternative to full flow)
- **Documents**:
  - Research: `research_qr_verification_benchmarking.md` (63 pages, full competitive analysis)
  - Presentation: `presentation_qr_verification_strategy.md` (19 slides for stakeholder review)
  - As-is KB: `kb_qr_code_as_is.md` (current feature behavior)
- **Next Steps**:
  - Week 2: Stakeholder decision (TDRA, DDA, Engineering, Legal)
  - If approved: Detailed BRD, pilot partner identification (hospital, hotel, employer)
  - Sprint planning for Phase 1 MVP

### Additional UX Enhancements (2025):
- **Grid view** for documents (in addition to list/type views)
- **Copy-any-field** affordance on Document Details
- **New landing page** with primary CTAs: Request Document / Upload Document
- **PDF Viewer Revamp**: Native viewer, fit-to-width, snap-to-page
- **Issuer/logo chips** on document cards
- **Consistent empty states** and bilingual copy refresh

### Quick Wins Backlog:
- Guided journey copy refresh (EN/AR)
- Upload error messaging improvements (EN/AR)
- Android dialog transparency fix (select document type)
- iOS collapsing header parity

### Technical Initiatives (2025):
- **ICP eSeal Transition**: ICP self-signing with own HSM (from DDA eSeal service)
  - SP comms + validation compatibility checks
  - Lower-env testing with ICP test vectors

### Future Exploration (2025 H2+):
- _[TO BE BRAINSTORMED based on user feedback, SP needs, TDRA priorities]_

---

## 8) Service Provider (SP) Ecosystem

**Active SPs**: _[?]_

**SP Onboarding Essentials**:
- Unique, time-boxed, one-time correlation IDs (now enforced)
- eSeal validation (local or DDA API)
- Error handling for DV error codes
- Security: no PII in QRs, HTTPS/TLS pinning

**SP Tiers** (Proposed - pending QR revamp approval):
- **Full Integration SPs**: Banks, telcos, government services (API integration, Document Sharing flow)
- **QR-Only SPs**: Hospitals, hotels, SMEs (lightweight verification via QR scan, no API needed) — **NEW TIER**

**SP Pain Points**:
- **High integration cost**: Full API integration requires months + legal agreements (blocker for small SPs like clinics, hotels)
- **Lengthy onboarding**: Delays adoption for non-technical SPs

**Onboarding Opportunities** (QR Revamp):
- Lightweight QR-Only SP tier could unlock 10x ecosystem growth (small SPs vastly outnumber large enterprises)

---

## 9) Open Questions / Risks

### High Priority:
1. **QR Code Revamp Decision**: TDRA/DDA/Engineering approval for Option 2 (Revamp & Expand)? Budget approval for 4-6 month Phase 1?
2. **QR Masked Reference Privacy**: Legal review - is `784-XXXX-XXXXXXX-X` format acceptable? (minimal PII exposure vs security need)
3. **ICP eSeal Transition**: DDA validator compatibility with ICP-signed eSeals?
4. **Auto-Add Consent**: Legal retention windows? TDRA legal sign-off timeline?
5. **Dual EID Labels**: Final EN/AR copy approved by DDA?

### Medium Priority:
4. Notification UX for foreground sessions - in-app cues coverage?
5. SP survey results on eSeal validation approach?

### Low Priority:
6. _[TBD]_

---

## 10) Operating Rhythm

**Sprint Cadence**: Bi-weekly (2-week sprints)
- Mid-week: Backlog refinement
- Friday: Sprint review

**Tools**:
- **Jira**: DV Product board
- **Figma**: DV Refresh 2024/25
- **SharePoint**: Slides, roadmaps
- **Firebase**: Push notifications, Remote Config

**Approval Gates**:
- Major features: DDA design approval + TDRA policy alignment
- Timeline: _[TO BE CLARIFIED - how long?]_

---

## 11) Decision Log

| Date | Decision | Rationale | Stakeholders | Status |
|------|----------|-----------|--------------|--------|
| 2025-11-14 | QR Verification Revamp: Approve Option 2 (Revamp & Expand) | Fix critical security gaps, enable high-value use cases (hospitals, hotels, HR), match global leaders (Singpass, EU Wallet, Apple), unlock 10x SP ecosystem growth via lightweight onboarding | TDRA, DDA, Engineering, Legal | **Pending Decision** (Week 2) |

---

## 12) Learning Backlog (Questions to Research)

- [x] **QR Code Verification benchmarking** - Completed 2025-11-14 (5 global apps analyzed, recommendation: Option 2 Revamp & Expand)
- [ ] Review last 3 sprint retrospectives - what's slowing us down?
- [ ] Analyze user feedback from support tickets - top 5 complaints?
- [ ] Review SP feedback - integration pain points?
- [ ] Check analytics - where are users dropping off?
- [ ] Review Figma designs - what's next in DDA pipeline?
- [ ] Review Jira backlog - what's been deprioritized and why?

---

## 13) Key Contacts

- **Product**: Fadi / DV Product Team
- **Engineering**: FE/BE/QA _[names?]_
- **QA/Ops**: DV Ops _[names?]_
- **UX/Design**: DDA liaison + in-house _[names?]_
- **TDRA**: _[key contact?]_
- **ICP**: _[technical contact?]_

---

## 14) Notes & Insights

### Week of 2025-11-12:
- Taking over as PM for DV component
- Reviewing knowledge base and understanding current state
- Key insight: Product operates in **highly regulated** environment (TDRA oversight)
- Key insight: **Multi-stakeholder** coordination required (TDRA, DDA, ICP, SPs)
- Key insight: Strong focus on **bilingual UX** (EN/AR) and **accessibility**
- **2025 Roadmap Planning Session**:
  - Three major initiatives confirmed: Dual Citizenship, One-Time Consent, QR Code Revamp
  - Dual Citizenship: In development, targeting Q1 2025
  - One-Time Consent: Pending legal/policy review (blocker)
  - QR Code Revamp: In progress - **need to clarify scope and goals**
  - UX enhancements running in parallel (grid view, copy-field, PDF viewer, etc.)
- **North Star Confirmed**: **Reduce failure cases in document sharing**
  - Primary metric: "Successful Combos %" (% of SP requests fully satisfied on first attempt)
  - Root causes: missing docs, expired docs, revoked docs, user drop-off, notification failures
- **Agent Framework Created**:
  - **New Feature Agent** (`agent_new_feature.md`): Requirements gathering, benchmarking, BRD/user stories
  - **Existing Feature Agent** (`agent_existing_feature.md`): Feature knowledge management, query response, gap analysis
  - Agents collaborate to ensure consistency and avoid duplication
- **QR Code Revamp - Critical Discovery** 🔴:
  - **Problem**: Current QR verification is fundamentally broken (no binding to document/user)
  - **Impact**: Unusable for high-value use cases (hospital check-in, hotel registration, in-person verification)
  - **Proposed Solutions**: 3 approaches identified (Enhanced QR, Lightweight SP, Peer-to-Peer)
  - **Key Insight**: "Lightweight SP" model could unlock massive adoption (hospitals, hotels, clinics without full integration)
  - **Analysis Document**: Created `qr_verification_problem_analysis.md` with detailed breakdown
  - **Next**: Validate scope, research benchmarks, prioritize solutions

### Week of 2026-02-03:
- **2026 Roadmap Finalized** ✅:
  - Imported roadmap data from `roadmap_v5_scored.csv` (scored prioritization)
  - **16 features** selected for 2026 across 4 categories: Product (7), Design (3), SP (1), UX (5)
  - Technical items (4) tracked separately
  - Scoring system: Priority Score (High=8, Medium=5, Low=3) + Complexity Score (Low=8, Medium=5, High=3) = Total Score (max 16)
  - 4 items DDA related, 3 items already in progress (Sprints 70, 72)

- **Roadmap Builder Application Updated** ✅:
  - Location: `D:\claude\roadmap-builder\`
  - New features implemented:
    - **Category filtering** with multi-select chips
    - **Color coding** by category (Product=Blue, Design=Purple, Technical=Green, UX=Orange, SP=Teal)
    - **Export to image** for PowerPoint (1920x1080 PNG, quarter/sprint timeline options)
    - **Category selection** in export modal
  - Merged "Technical Team Suggestions" into "Technical" category
  - Changed "DDA required" label to "DDA related"

- **2026 Roadmap Presentation Created** ✅:
  - File: `D:\claude\UAE_PASS_DV_2026_Roadmap.pptx`
  - 10 slides: Title, Roadmap Overview, Product (3), Design, SP, UX (2), Summary
  - Color-coded by category, organized by quarters (Q1-Q4 2026)
  - Target audience: UAE PASS Users, Service Providers
  - Condensed brief format (no team ownership details)

### Week of 2025-11-14:
- **QR Code Verification — Research Completed** ✅:
  - Conducted comprehensive competitive benchmarking (5 global leaders):
    1. **Singapore Singpass** - 5M users, 41M transactions/month, QR+NFC verification at hospitals/age verification
    2. **EU Digital Identity Wallet** - W3C VC + ISO 18013-5 compliant, pilot 2024-2025
    3. **Apple Wallet Digital ID** - Launched Nov 2025, 250+ US airports, QR→BLE handover, biometric-gated
    4. **India DigiLocker** - 200M users, time-limited QR sharing, document-embedded QR codes
    5. **W3C Verifiable Credentials** - International standard (30-90 sec TTL, nonce+timestamp anti-replay)
  - **Gap Analysis**: UAE PASS lacks document binding, anti-replay protection, time limits, NFC support, telemetry
  - **Strategic Options**: Evaluated 3 options (Remove, Revamp, Enhance Minimally)
  - **Recommendation**: **Option 2 - Revamp & Expand** (4-6 months Phase 1, +3-4 months Phase 2)
  - **Business Impact**: 10x SP ecosystem growth (lightweight QR-Only SP tier), 500k+ verifications/month, match global leaders
  - **Use Cases Unlocked**: Hospital check-in, hotel registration, HR onboarding, bank verification, landlord verification
  - **Documents Created**:
    - `research_qr_verification_benchmarking.md` (63 pages - full competitive analysis, security best practices, gap analysis, user stories, bilingual copy, technical architecture)
    - `presentation_qr_verification_strategy.md` (19 slides - stakeholder presentation deck)
    - `kb_qr_code_as_is.md` (updated - current feature behavior + limitations)
  - **Next**: Stakeholder review (TDRA, DDA, Engineering, Legal) → Decision gate Week 2 → If approved: Detailed BRD + pilot partners
- **Key Insight**: All global digital identity leaders (Singpass, EU Wallet, Apple) have secure QR verification as core capability
- **Key Insight**: Lightweight SP onboarding (QR-Only tier) is massive opportunity - hospitals, hotels, SMEs can verify without full API integration
- **Strategic Alignment**: QR Verification directly supports North Star (reduce sharing failures) by providing simpler alternative to full Document Sharing flow

---

## 15) Glossary (Quick Reference)

- **DV**: Digital Vault / Digital Documents component
- **eSeal**: Cryptographic organization stamp (issuer authentication)
- **Verifiable Presentation**: Package of user docs/attributes for SP
- **Correlation ID**: Unique SP request identifier for sharing flow
- **Primary/Secondary EID**: Dual-citizenship classification (UAE vs 2nd nationality)
- **SP**: Service Provider (banks, telcos, insurers)
- **ICP**: High-volume document issuer (EID, Visa, Passport)
- **DDA**: Design Authority (design/UX partner)
- **TDRA**: Telecommunications and Digital Government Regulatory Authority (regulator)

---

_This is a living document. Updated as I learn more about the product, users, and stakeholders._
