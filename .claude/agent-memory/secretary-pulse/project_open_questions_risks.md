---
name: DV Open Questions and Risks
description: Unresolved questions, blockers, and risks that may surface in PM discussions
type: project
---

**Why:** These are the live unknowns. When the PM brings up any of these topics, be ready to reference context and help drive toward resolution.

**How to apply:** Proactively flag if a task or discussion is blocked by one of these open items. Prompt for updates when relevant.

## High Priority Open Items

1. **QR Verification Revamp — Decision Gate**
   - Status: Pending (targeted Week 2 from 2025-11-14 — may be resolved by now)
   - What's needed: TDRA, DDA, Engineering, Legal approval for Option 2 (Revamp & Expand)
   - Risk if blocked: QR Phase 1 slips from Q3 2026

2. **Auto-Add Documents — Legal Clearance**
   - Status: Pending TDRA legal sign-off
   - What's needed: UAE data protection law alignment, consent lifetime/scope confirmation, audit retention windows
   - Risk if blocked: Q2 launch of Auto-Add slips; 68.5 priority score means it's still important

3. **ICP eSeal Transition — DDA Validator Compatibility**
   - Status: Planned Q1, compatibility check in progress
   - What's needed: Confirm DDA validator accepts ICP-signed eSeals; SP survey on local vs DDA validation
   - Risk if delayed: Reliability issues for ICP flows

4. **Status-Based Reporting — Baseline Validation**
   - Status: In Progress (Sprint 70)
   - Critical: All 2026 conversion targets (67.4% -> 80%) are estimates until this ships
   - Risk: Entire Q1-Q2 optimization work is on hold until accurate baselines established

5. **Dual Citizenship — Final EN/AR Copy**
   - Status: Implementation in progress; DDA copy approval status unknown
   - What's needed: Final label approval for "Primary EID (UAE)" / "Secondary EID (2nd nationality)" chips

6. **User Behavior Analytics Tool**
   - Decision needed: UXCam vs Firebase Analytics
   - Must be resolved Q1 to enable consent screen A/B testing in Q2

## Medium Priority

7. **QR Masked Reference Privacy**
   - Format proposed: `784-XXXX-XXXXXXX-X`
   - Legal review needed: Is minimal PII exposure acceptable for this security requirement?

8. **Notification UX for Foreground Sessions**
   - In-app cue coverage for when app is open (banner, snackbar, inbox) — status unclear

9. **SP Feedback on eSeal Validation**
   - SP survey on whether they use local validation or DDA API — results not captured yet

## Key Metrics to Establish
- MAU: unknown
- Successful Combos %: baseline ~67.4% (to be re-validated)
- Notification Open Rate: unknown
- Lost Requests Rate: unknown
- SP Satisfaction Score: unknown

## Platform Gaps
- iOS conversion 77.8% vs Android 67.7% — 10% gap = ~15K lost shares/week
- Android optimization sprint planned Q1 to close this
