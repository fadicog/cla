# Session Summary - 2025-11-12
_PM for UAE PASS Digital Vault (DV) Component_

---

## Session Overview

**Duration**: 2025-11-12 (initial PM onboarding session)
**Role Assumed**: Product Manager for Digital Vault component of UAE PASS
**Status**: Active - awaiting user input on QR Code Revamp prioritization

---

## What We Accomplished This Session

### 1. Created Core Documentation Framework ✅

**Files Created**:
1. **`CLAUDE.md`** - Guide for future Claude instances
   - Documentation conventions (bilingual EN/AR, terminology)
   - Product domain context (stakeholders, flows, patterns)
   - Operating rhythm, tools, Arabic content guidelines

2. **`pm_dv_working_doc.md`** - PM working document (living doc)
   - Role & responsibilities
   - North Star goal: **Reduce document sharing failures**
   - 2025 roadmap: Dual Citizenship, One-Time Consent, QR Code Revamp
   - Success metrics, user pain points, technical landscape
   - Decision log, learning backlog, notes & insights

3. **`agent_new_feature.md`** - New Feature Agent specification
   - Requirements gathering with clarification templates
   - Competitive benchmarking process
   - BRD (Business Requirements Document) template
   - User Story template with acceptance criteria

4. **`agent_existing_feature.md`** - Existing Feature Agent specification
   - Feature catalog (12 current DV features documented)
   - Query response templates
   - Gap analysis templates
   - Integration guidance

5. **`qr_verification_problem_analysis.md`** - Critical problem discovery
   - Current QR verification weakness identified (no binding to document/user)
   - 3 proposed solutions analyzed
   - Use case validation (hospitals, hotels, peer-to-peer)
   - Comparison matrix and recommendations

---

## Key Insights & Decisions Made

### 1. North Star Goal Confirmed 🎯
**Goal**: **Reduce failure cases in document sharing flows**

**Primary Metric**: "Successful Combos %" (% of SP-requested document sets fully satisfied on first share attempt)

**Root Causes of Sharing Failures**:
1. Missing documents (user hasn't requested from issuers)
2. Expired documents (user has outdated version)
3. Revoked documents (issuer revoked but user unaware)
4. User drop-off (friction during request/approval)
5. Notification failures (user doesn't see sharing request)

---

### 2. 2025 Roadmap Structure Defined

**Three Major Initiatives** (in progress + pending):

**Initiative 1: Dual Citizenship Support** ⚙️
- **Status**: In development
- **Target**: Q1 2025
- **Goal**: Support users with "Special Emirati Citizenship" + original residency
- **Scope**: Primary EID (UAE) vs Secondary EID (2nd nationality) classification
- **Dependencies**: ICP backend support, DDA design sign-off

**Initiative 2: One-Time Consent (Auto-Add Documents)** ⏳
- **Status**: Pending legal/policy review
- **Blocker**: UAE data protection law alignment + TDRA legal sign-off
- **Target**: Q2 2025 (pending legal clearance)
- **Goal**: Periodic issuer checks to auto-add new/updated docs (with explicit consent)
- **Value**: Proactive updates → fewer failed shares due to missing/expired docs

**Initiative 3: QR Code Functionality Revamp** 🔄
- **Status**: Problem discovery phase → **AWAITING USER INPUT**
- **Critical Discovery**: Current QR verification is fundamentally broken
  - No binding to original document or user identity
  - Shows "Valid EID from ICP" but not whose EID or which specific document
  - Unusable for in-person verification (hospitals, hotels, etc.)
- **Proposed Solutions**: 3 approaches identified (see below)

**Additional**: UX Enhancements (grid view, copy-field, PDF viewer, new landing page, etc.)

---

### 3. QR Code Revamp - Critical Problem Discovery 🔴

**Problem Identified**:
Current QR verification flow is broken:
- User opens document in app → taps "QR Code" → QR displayed
- Verifier scans QR → redirects to uaeverify.ae → shows "Valid EID from ICP"
- **BUT**: No reference to which document, whose document, or when verified
- **Attack vector**: User can show friend's QR, screenshot, or reused old QR

**Impact**:
- Unusable for high-value in-person verification use cases
- Hospitals, hotels, clinics, banks (reception verification) cannot rely on this

---

### 4. Three Proposed Solutions for QR Revamp

**Solution 1: Enhanced QR Verification** (Quick Fix)
- Bind QR to specific document + user (dynamic QR with hash + timestamp)
- Show user photo, name, ID number, validation status
- Clear instruction: "Match photo to person in front of you"
- **Pros**: Quick win, fixes broken flow
- **Cons**: Privacy concern (PII exposed), still manual verification
- **Effort**: Low (2-3 sprints)
- **Recommended Phase**: Phase 1 (Q1 2025)

**Solution 2: Lightweight SP / On-Counter Sharing** ⭐ **HIGH PRIORITY**
- User's preferred solution: "QR at hospital reception → patient scans → approves → data flows to SP storage"
- Simplified SP onboarding (self-service portal, no complex backend integration)
- DV-managed storage (S3 bucket with SP-specific folders)
- SP system polls folder and fetches encrypted data
- **Pros**: Scalable, secure, unlocks huge market (hospitals, hotels, clinics)
- **Cons**: SP needs basic tech capability (poll S3/SFTP), legal/policy review
- **Effort**: Medium-High (6-8 sprints)
- **Recommended Phase**: Phase 2 (Q2 2025)

**Solution 3: Peer-to-Peer Sharing** (Lower Priority)
- User A generates QR → User B scans with UAE PASS → A approves → doc shared to B's app
- Use cases: Landlords, employers, individual verification
- **Pros**: Covers individual use cases
- **Cons**: Both need UAE PASS app, privacy risks, lower demand
- **Effort**: Medium (4-6 sprints)
- **Recommended Phase**: Phase 3 (Q3 2025+) if demand validated

---

## Open Questions - AWAITING USER RESPONSE ⏳

### Critical Questions for QR Code Revamp Scoping

**On Lightweight SP (User's Preferred Solution)**:
1. **Target SPs**: Hospitals/hotels/banks/all of above?
2. **Onboarding**: Self-service (instant) or approval-based?
3. **Data Delivery**: DV-managed S3? SP-managed SFTP? Email/SMS? Real-time API?
4. **Data Access Window**: 15 min? 1 hour? 24 hours? Custom per SP type?
5. **Data Fields**: Full EID? Core fields only? SP-requested fields?

**On Enhanced QR Verification**:
6. **Privacy Tradeoff**: Is showing photo + name acceptable? Needs explicit consent?
7. **Verifier Display**: Full details? Minimal (photo + "Valid")? Redacted?

**On Peer-to-Peer Sharing**:
8. **Demand Validation**: Real user need? What are top 3 use cases?
9. **Recipient Requirements**: UAE PASS users only? Or anyone via link?

---

## Current State of Roadmap

### Confirmed (In Progress):
- ✅ Dual Citizenship Support (Q1 2025)
- ✅ UX Enhancements (grid view, copy-field, PDF viewer, etc.)
- ✅ ICP eSeal Transition (technical initiative, 2025)
- ✅ Duplicate Correlation ID Fix (deployed)

### Pending (Blockers):
- ⏳ One-Time Consent / Auto-Add Documents (legal/policy review)
- ⏳ QR Code Revamp (awaiting scope/prioritization decision)

### Backlog:
- Quick wins: Guided journey copy refresh, upload error messaging, Android/iOS fixes

---

## Agent Framework Created

**Purpose**: Enable specialized, autonomous agents to support PM work.

**Agent 1: New Feature Agent** (`agent_new_feature.md`)
- **Responsibilities**: Requirements gathering, benchmarking, BRD creation, user stories
- **Templates**: Clarification template, competitive analysis, BRD, user stories
- **Research Sources**: Singpass, DigiLocker, EU Wallet, Apple Wallet, W3C standards

**Agent 2: Existing Feature Agent** (`agent_existing_feature.md`)
- **Responsibilities**: Feature knowledge management, query response, gap analysis
- **Feature Catalog**: 12 current DV features documented (auth, docs, sharing, notifications, etc.)
- **Templates**: Feature overview, integration query, gap analysis

**Collaboration Model**:
```
Main PM (You) → Coordinates
  ├─→ New Feature Agent: "Design QR revamp, benchmark industry"
  └─→ Existing Feature Agent: "How does current QR work?"
       └─→ Agents collaborate to ensure consistency
```

---

## Technical Context

### Product Overview (DV Component)
**What**: Digital Vault (DV) is the document management component of UAE PASS
- Document request (from issuers like ICP)
- Document storage (issued + uploaded)
- Document sharing (consent-based with SPs)
- Lifecycle management (updates, expiry, revocation)

**Key Stakeholders**:
- **TDRA**: Regulator / Product Owner (policy & priorities)
- **DDA**: Design Authority (UX approvals required)
- **ICP**: High-volume issuer (EID, Visa, Passport)
- **SPs**: Service Providers (banks, telcos, hospitals, hotels)

**Operating Rhythm**:
- Bi-weekly sprints (2-week cycles)
- Mid-week backlog refinement
- Friday sprint reviews
- Tools: Jira, Figma, SharePoint, Firebase

---

## Files & Documentation Created

### Primary Documentation
| File | Purpose | Status |
|------|---------|--------|
| `uae_pass_knowledge_base.md` | Original knowledge base (17 sections) | Existing |
| `pm_dv_working_doc.md` | PM working document (roadmap, metrics, notes) | Created & Updated |
| `CLAUDE.md` | Guide for future Claude instances | Created |
| `agent_new_feature.md` | New Feature Agent specification | Created |
| `agent_existing_feature.md` | Existing Feature Agent specification | Created |
| `qr_verification_problem_analysis.md` | QR problem analysis + 3 solutions | Created |
| `session_summary_2025-11-12.md` | This file (session snapshot) | Created |

### Key Sections in PM Working Doc
- **Section 3**: Current Priorities (North Star: reduce sharing failures)
- **Section 5**: Primary Pain Point (document sharing failures - root causes)
- **Section 7**: Roadmap & Initiatives (2025 H1 focus)
- **Section 9**: Open Questions / Risks (prioritized)
- **Section 14**: Notes & Insights (week of 2025-11-12)

---

## Next Steps (When Session Resumes)

### Immediate (Awaiting User Input)
1. **Get QR Code Revamp scope clarification** (answer 9 critical questions above)
2. **Prioritize solutions** (Enhanced QR vs Lightweight SP vs Peer-to-Peer)
3. **Define success metrics** for chosen solution

### Once Scope is Clear
4. **Task New Feature Agent** to research industry benchmarks (Singpass, Apple Wallet, etc.)
5. **Create BRDs** for prioritized solutions
6. **Draft User Stories** with acceptance criteria
7. **Engage TDRA Legal** on privacy/policy questions (PII in QR, data residency, consent)
8. **Engage Engineering** on technical feasibility (dynamic QR, S3 storage, SP portal)

### Ongoing
9. **Fill placeholders** in PM working doc (metrics, KPIs, user segments, contacts)
10. **Track decisions** in Decision Log as scope is finalized
11. **Update roadmap** based on prioritization outcome

---

## Key Metrics to Track (Currently Unknown)

These are placeholders in PM working doc - need to populate:
- MAU (Monthly Active Users): _[?]_
- Successful Combos %: _[?]_ (baseline + target)
- Notification Open Rate: _[?]_
- Lost Requests Rate: _[?]_
- SP Satisfaction Score: _[?]_
- Active SPs: _[?]_
- User segments breakdown: _[?]_

---

## Important Context for Next Session

### Bilingual Requirements (EN/AR)
- All user-facing content must be bilingual
- Arabic follows RTL (right-to-left) formatting
- Arabic plural rules: 0 (omit), 1 (singular), 2 (dual), 3-10 (plural-1), 11+ (plural-2)
- Avoid "vault" terminology → use "Documents" / «المستندات»
- Test for truncation in both languages

### Product Governance
- Major features require **DDA design approval** + **TDRA policy alignment**
- Approval timeline: _[TO BE CLARIFIED]_
- Legal/policy reviews can block features (e.g., Auto-Add Documents)

### Security & Privacy Principles
- Consent-based sharing (per-transaction, even with Auto-Add)
- No PII in QR codes (opaque correlation IDs only)
- eSeal validation (all issued documents cryptographically verified)
- Unique correlation IDs (enforced via DB constraint)
- HTTPS/TLS pinning for SP integrations

---

## Glossary (Quick Reference)

- **DV**: Digital Vault / Digital Documents component
- **eSeal**: Cryptographic organization stamp (issuer authentication, not eSignature)
- **SP**: Service Provider (banks, telcos, hospitals, hotels)
- **ICP**: High-volume document issuer (EID, Visa, Passport)
- **TDRA**: Telecommunications and Digital Government Regulatory Authority (regulator)
- **DDA**: Design Authority (design/UX partner)
- **Verifiable Presentation**: Package of user docs/attributes for SP
- **Correlation ID**: Unique SP request identifier for sharing flows
- **Successful Combos %**: % of SP-requested doc sets fully satisfied on first share attempt

---

## Current Todo List Status

- [x] Document current QR verification weakness
- [ ] Validate QR revamp scope with user (AWAITING RESPONSE)
- [ ] Explore peer-to-peer document sharing use case
- [ ] Explore on-counter sharing use case (hospital, hotel)
- [ ] Research industry solutions for in-person verification
- [ ] Define lightweight SP onboarding for reception use cases

---

## Recommended Reading Order for Next Session

1. **Start here**: `session_summary_2025-11-12.md` (this file)
2. **PM context**: `pm_dv_working_doc.md` (your working doc)
3. **QR problem**: `qr_verification_problem_analysis.md` (critical discovery)
4. **Product knowledge**: `uae_pass_knowledge_base.md` (17 sections)
5. **How to operate**: `CLAUDE.md` (guide for Claude instances)
6. **Agent specs**: `agent_new_feature.md` + `agent_existing_feature.md`

---

## Session Status: ⏸️ PAUSED

**Reason**: Awaiting user input on QR Code Revamp scope and prioritization.

**Next Action**: User to answer 9 critical questions in "Open Questions" section above, then PM will:
1. Finalize roadmap prioritization
2. Task New Feature Agent to research benchmarks
3. Create BRDs and user stories
4. Engage stakeholders (TDRA Legal, Engineering, DDA)

---

_Session saved. All context preserved for next Claude instance._
_Resume by reading this file first, then `pm_dv_working_doc.md`._
