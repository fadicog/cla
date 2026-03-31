---
name: DV Current Initiatives and Status
description: All active, in-progress, and recently completed initiatives as of March 2026
type: project
---

**Why:** The 2026 roadmap was finalized in January 2026. As of March 2026, Q1 work is underway. Initiatives are sequenced with Status-Based Reporting as the mandatory first step before any conversion optimization.

**How to apply:** When the PM asks about priority or sequencing, refer to this. No optimization work proceeds until accurate measurement infrastructure is live.

## Q1 2026 — Foundation & Measurement (current quarter as of 2026-03-17)

| Initiative | Status | Notes |
|------------|--------|-------|
| Status-Based Reporting Implementation (P0) | In Progress (Sprint 70) | 23-status-code system (100-600 range). MUST complete before optimization work. |
| Infinite Loaders Detection | In Progress (Sprint 70) | Technical reliability improvement. |
| Dual Citizenship GA | In Progress (Sprint 72) | Primary/Secondary EID handling. Design approved, implementation underway. |
| ICP eSeal Transition Completion | Planned Q1 | ICP self-signing with own HSM. DDA validator compatibility check needed. |
| Android Optimization Sprint | Planned Q1 | Close 10% iOS/Android conversion gap (15K lost shares/week). |
| Document Pre-Check API | Planned Q1 | Eliminate 72K futile requests/week (SPs requesting docs users don't have). |
| User Behavior Analytics Tool Selection | Planned Q1 (early) | UXCam vs Firebase Analytics decision. Must precede A/B testing. |
| Issuer Retry Logic | Planned Q1 | Backend improvement. +1,500 shares/week estimated. |

## Q2 2026 — Conversion Excellence

| Initiative | Status | Notes |
|------------|--------|-------|
| Consent Screen Redesign | Planned Q2 | Biggest funnel leak: 16.9% abandonment. Requires DDA approval. |
| Auto-Add Documents Launch | Planned Q2 (if legal cleared) | One-time consent for periodic issuer checks. Blocker: TDRA legal sign-off. |
| Smart Pending Request Reminder System | Planned Q2 | Reduce abandonment by redirecting pending requests. |
| UX Enhancements Bundle | Planned Q2 | Grid view, copy-any-field, PDF viewer revamp, empty states. |
| Status Chain/History Tracking | Planned Q2 | New: enables user journey reconstruction and analysis. |
| Error-to-Status Code Linking | Planned Q2 | New: automated troubleshooting. |

## Q3 2026 — Ecosystem Expansion

| Initiative | Status | Notes |
|------------|--------|-------|
| QR Verification Phase 1 MVP | Planned Q3 | Fix security gaps (no binding, no anti-replay, no TTL). Enable hospital/hotel/HR use cases. Requires TDRA/DDA/Legal approval. |
| SP Quality Scoring Program | Planned Q3 | Partner health metrics. |
| Advanced Reporting | Planned Q3 | Root cause dashboards. |

## Q4 2026 — Scale & Innovation

| Initiative | Status | Notes |
|------------|--------|-------|
| QR Verification Phase 2 | Planned Q4 | NFC tap, selective disclosure, W3C VC alignment. |
| Zero-Knowledge Proofs POC | Planned Q4 (research) | Privacy-first: verify attributes without revealing document data. 2027+ for production. |
| Predictive Document Availability | Planned Q4 | ML-based proactive notifications. |
| AI Chatbot Stage 1 | Planned Q4 | Support deflection. Not conversion-impacting. |

## Key Pending Decisions
- QR Verification Revamp (Option 2): Stakeholder decision still pending as of PM working doc (targeted Week 2 from Nov 2025). May already be resolved — confirm with PM.
- Auto-Add Documents legal clearance: TDRA legal sign-off timeline unknown.
- ICP eSeal Transition: DDA validator compatibility status unknown.

## 2025 Work Completed
- QR Verification benchmarking (5 global leaders analyzed — Nov 2025)
- Sharing request data analysis (350K+ requests, 67.4% conversion baseline)
- Status-based reporting system design (23 status codes)
- 2026 roadmap finalized and presented (16+ features, scored prioritization)
- Roadmap visualization tools built (roadmap-builder React app, roadmap-light HTML tool)
