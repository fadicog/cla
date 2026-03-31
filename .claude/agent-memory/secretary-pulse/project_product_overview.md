---
name: DV Product Overview
description: What UAE PASS Digital Documents (DV) is, its core flows, and how it fits into the UAE PASS ecosystem
type: project
---

UAE PASS is the national digital identity platform of the UAE. The DV (Digital Documents / "Digital Vault") component is responsible for document issuance, storage, consent-based sharing, and lifecycle management.

**Why:** DV is the document management layer that enables SPs (banks, telcos, insurers) to request and verify documents held by users. The PM role owns the entire DV product surface.

**How to apply:** When the PM asks about features, scope, or strategy, frame everything in terms of the three core DV goals: document availability, sharing success, and user trust.

## Core Flows
1. Authentication/SSO — QR-based login to SP services (not strictly DV but tightly coupled)
2. Document Lifecycle — Request from issuer -> Availability -> Storage -> Updates -> Revocation/Expiry
3. Document Sharing — SP creates sharing request (correlation ID) -> User approves -> Verifiable presentation delivered to SP
4. Qualified eSignature — Person-level consent for transactions

## Document Types
- Issued Documents: Official docs from issuers (e.g., ICP: EID, Visa, Passport). Carry eSeal (cryptographic org stamp proving origin). High SP trust.
- Uploaded Documents: User PDFs, self-signed. Lower SP trust.

## North Star Metric
"Successful Combos %" — percentage of SP-requested document sets fully satisfied on first sharing attempt. Current baseline: ~67.4% conversion (to be re-validated after Status-Based Reporting goes live).

## Key Technical Notes
- eSeal: CAdES/PAdES cryptographic org stamp from issuer. Not an eSignature.
- Correlation ID: Unique, time-boxed, one-time SP request ID. DB uniqueness constraint now enforced.
- Verifiable Presentation: Package of user docs/attributes prepared for SP, preserving issuer signatures.
- QR codes must never contain PII — opaque IDs only.
- DDA validator compatibility must be maintained for eSeal validation.
