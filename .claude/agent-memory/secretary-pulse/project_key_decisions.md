---
name: DV Decision Log Summary
description: Key decisions made and pending in the DV product, with rationale and stakeholders
type: project
---

**Why:** Decisions shape the roadmap and must not be re-litigated without clear reason. Knowing what was decided (and why) prevents contradictory work.

**How to apply:** When a discussion touches on these areas, reference the existing decision. Flag if context suggests a prior decision needs revisiting.

## Decisions Made

| Date | Decision | Rationale | Stakeholders | Status |
|------|----------|-----------|--------------|--------|
| 2025-11-14 | QR Verification: Pursue Option 2 — Revamp & Expand | Fix critical security gaps (no binding, no anti-replay, no TTL), enable high-value use cases (hospitals, hotels, HR), match global leaders (Singpass, EU Wallet, Apple), unlock 10x SP ecosystem growth via QR-Only SP tier | TDRA, DDA, Engineering, Legal | PENDING formal approval as of Nov 2025 — confirm current status |
| 2025-11-14 | QR Verification benchmarking: 5 global leaders analyzed | Singpass, EU Digital Identity Wallet, Apple Wallet Digital ID, India DigiLocker, W3C VC standards — all have secure QR with binding + anti-replay | Product | COMPLETED |
| 2026-01-07 | 2026 Roadmap: Status-Based Reporting is P0 — no optimization proceeds until live | Cannot optimize what cannot be accurately measured. Current metrics are estimates. | Product | ADOPTED |
| 2026-01-07 | ZKP deferred to 2027+ (POC in Q4 2026) | Too high effort without POC validation; requires talent acquisition; legal implications unclear | Product | ADOPTED |
| 2026-01-07 | User Behavior Analytics elevated to Q1 (early) | Must precede A/B testing of consent screen redesign | Product | ADOPTED |
| 2026-01-07 | AI Chatbot deferred to Q4 | Not conversion-impacting; not the right time | Product | ADOPTED |
| 2025-11-12 | North Star metric: "Successful Combos %" | Directly measures whether users can complete SP-initiated sharing flows | Product | ADOPTED |
| 2026-01-06 | 2026 roadmap scored using: Impact x 0.4 + (11-Effort) x 0.3 + Data_Confidence x 0.2 + (11-Risk) x 0.1 | Weighted multi-factor prioritization; max score 100 | Product | ADOPTED |

## Decisions NOT Made (still open)
- Auto-Add Documents: Legal clearance from TDRA not yet received
- QR masked reference privacy: Legal review of `784-XXXX-XXXXXXX-X` format not complete
- Final EN/AR copy for Dual EID chips: DDA approval pending
- Analytics tool selection: UXCam vs Firebase Analytics — decision needed Q1 2026
- PM decision authority scope: Still to be clarified

## Product Positions (established but informal)
- No "vault" in user-facing copy — always "Documents" / «المستندات»
- Sharing is always per-transaction consent (even with Auto-Add enabled, adding != sharing consent)
- QR codes must never contain PII — opaque correlation IDs only
- ICP eSeal transition: no DV code change expected; mainly SP comms and DDA validator alignment
