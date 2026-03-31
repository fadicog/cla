# Feature Benchmark Analyser — Persistent Memory
_Last updated: 2026-02-26_

## Scoring Precedents

| Feature Type | Priority Score | Complexity Score | Total | Rationale Pattern |
|---|---|---|---|---|
| Foundational schema/catalogue (e.g., Attribute Catalogue) | 8 (High) | 3 (High complexity) | 11 | High priority because it enables other features; high complexity because cross-issuer coordination + API changes |
| Standardised UX pattern with DDA dependency (e.g., "Fill with UAE PASS") | 8 (High) | 5 (Medium) | 13 | High priority if it is the citizen-facing manifestation of a High-priority roadmap item; Medium complexity when core tech exists but design approval is critical path |
| Citizen transparency/trust feature (e.g., Sharing History) | 5 (Medium) | 8 (Low) | 13 | Medium priority (trust, not conversion); Low complexity when data infrastructure already exists |

## Benchmark Analyses Completed

- **MyInfo by Singpass** (2026-02-26): Saved to `D:\claude\feature_benchmark_myinfo_singpass.md`
  - Key finding: UAE PASS DV's eSeal model is architecturally stronger than MyInfo for field-level trust (offline verifiable vs. API-trust-only)
  - Key gap identified: UAE PASS lacks a formal attribute-level data catalogue — the foundational prerequisite for Form Filler
  - Three recommendations derived: Attribute Catalogue (11), "Fill with UAE PASS" UX (13), Sharing History Log (13)

- **"Fill with UAE PASS" Feature Analysis** (2026-02-26): Saved to `D:\claude\feature_analysis_fill_with_uae_pass.md`
  - Final score: 11 (Priority 8 + Complexity 3) — High priority, High complexity; phased delivery required
  - Six prerequisite gates identified: ICP schema, TDRA attribute access policy, DDA consent screen, PDPL legal, BE extraction service, SP API migration
  - Competitive benchmark confirms UAE PASS eSeal model is architecturally superior to all five comparators (MyInfo, eIDAS, DigiLocker, Apple, BundID) on cryptographic provenance
  - Minimum viable P1 attribute set defined: Full name EN, EID number, Date of birth, Nationality, Gender, Visa expiry
  - Recommended phased delivery: Phase 0 (prerequisites, Sprint 71–72) → Phase 1 (Attribute Catalogue) → Phase 2 (Core Fill, 2 pilot SPs) → Phase 3 (expanded sectors)

## Recurring Patterns in DV Benchmark Analysis

- **eSeal advantage**: UAE PASS DV's CAdES/PAdES eSeal model enables independent, offline SP verification. Most comparable platforms (MyInfo, eIDAS-lite) rely on centralised API trust. Always flag this as UAE PASS's architectural differentiator.
- **Form Filler prerequisite**: Any form-fill or attribute-sharing feature requires a formally defined attribute catalogue first. Do not scope Form Filler delivery without confirming catalogue ownership (ICP coordination required).
- **DDA approval triggers**: New screen designs, button specifications, consent screen templates, and bilingual copy patterns always require DDA design review. Flag these early.
- **ICP coordination required**: Any feature touching the attribute schema of ICP-issued documents (EID, Visa, Passport) requires ICP agreement. Do not assume ICP will publish schemas without negotiation.
- **Auto-Add Documents**: Pending legal review as of 2026-02-26. Do not create features that depend on it as a prerequisite until legal review is resolved.

## Arabic Copy Pairs (from benchmark analyses)

| English | Arabic |
|---------|--------|
| Attribute Catalogue | «فهرس البيانات» |
| Requested fields | «الحقول المطلوبة» |
| Source | «المصدر» |
| Emirates ID number | «رقم الهوية الإماراتية» |
| Fill with UAE PASS | «أكمل بـ UAE PASS» |
| The following information will be shared with [SP Name]: | «سيتم مشاركة المعلومات التالية مع [اسم مزود الخدمة]:» |
| Share | «مشاركة» |
| Enter manually instead | «الإدخال اليدوي بدلاً من ذلك» |
| Sharing History | «سجل المشاركة» |
| Shared with | «تمت المشاركة مع» |
| You shared [document name] | «شاركت [اسم المستند]» |
| No sharing history yet. | «لا يوجد سجل مشاركة حتى الآن.» |
| Full name | «الاسم الكامل» |
| Date of birth | «تاريخ الميلاد» |
| Nationality | «الجنسية» |
| Visa expiry date | «تاريخ انتهاء صلاحية التأشيرة» |
| Address | «العنوان» |
| Passport number | «رقم جواز السفر» |
| Your information was filled using verified UAE PASS data. | «تم ملء معلوماتك باستخدام بيانات موثقة من UAE PASS.» |
| This field could not be filled automatically. Please enter it manually. | «تعذّر ملء هذا الحقل تلقائيًا. يُرجى إدخاله يدويًا.» |
| Verified by [Issuer Name] | «موثق من قِبل [اسم الجهة المُصدِرة]» |
| Decline | «رفض» |

## Stakeholder Sensitivity Notes

- **TDRA**: Policy decisions on which attributes SPs may access are a TDRA call, not a product call. Flag attribute access scope questions to TDRA.
- **DDA**: Critical path for any new screen or UX pattern. Engage DDA early for features with design-heavy specs (consent screens, button standards).
- **ICP**: Must agree to publish formal attribute schemas for EID, Visa, Passport before Form Filler or Attribute Catalogue can be scoped accurately.
- **SPs**: High receptiveness to form-fill features (KYC cost reduction, onboarding friction). SP API migration plans needed for any schema change.

## Key Ongoing Initiatives (context for dependency checks)

- Status-Based Reporting Implementation — Sprint 70 (data layer for Sharing History)
- Dual Citizenship GA — Sprint 72
- Infinite Loaders Detection — Sprint 70
- Form Filler — 2026 roadmap, High priority
- Auto-Add Documents — pending legal review
- ICP eSeal Transition (self-signing HSM) — in progress

## Technical Constraints Frequently Affecting Feasibility

- Attribute-level field extraction from Verifiable Presentations requires SP API schema changes
- Any new sharing data model must maintain eSeal provenance chain (attribute → source document → eSeal)
- QR hygiene rules apply to all sharing-initiation flows: unique correlation IDs, short TTL, no PII in QR
- Firebase Remote Config used for feature flags — relevant for phased rollouts
- "Fill with UAE PASS" attribute scope must be validated against ICP eSeal transition (new HSM certs) before GA — confirmed in Q1 2026 plan
- For form-fill features, the SP API must support both document-level sharing (existing) and attribute-level sharing (new) simultaneously — both patterns coexist

## "Fill with UAE PASS" — Sector Field Sets (confirmed 2026-02-26)

- **P1 universal fields** (EID + Visa): Full name EN, EID number, Date of birth, Nationality, Gender, Visa expiry — recommended for v1 launch
- **P2 cross-sector**: Full name AR, Passport number, EID expiry
- **P3 sector-specific**: Health Insurance Card (insurance), Vehicle Registration (motor/government), Driving License (motor/government)
- TRA (telecom regulator) mandates specific SIM registration fields — must confirm TRA alignment before telecom sector onboarding
- RTA-issued Driving License may have a different attribute schema from ICP-issued documents — requires separate coordination
