# Feature Analysis: Fill with UAE PASS
**Date**: 2026-02-26 | **Analyst**: Feature Benchmark Analyser | **Status**: Draft — Ready for TDRA Product Review

---

## 1) Feature Summary

**One-line description (EN):** A standardised UX pattern that allows users to auto-populate SP forms with verified, eSeal-authenticated data from their UAE PASS digital documents, replacing manual field entry.

**One-line description (AR):** نمط UX معياري يتيح للمستخدمين ملء نماذج مزودي الخدمة تلقائيًا باستخدام البيانات الموثقة من مستنداتهم الرقمية في UAE PASS، بديلاً عن الإدخال اليدوي.

**Feature category:** Product (citizen-facing capability) — with significant Design, SP, and Technical sub-components

**Proposer / source:** DV Product Team — derived from MyInfo by Singpass benchmark analysis (2026-02-26) and 2026 roadmap Form Filler initiative

**Date of analysis:** 2026-02-26

**Distinction from "Continue with UAE PASS":** "Continue with UAE PASS" is an authentication/SSO pattern — it establishes identity. "Fill with UAE PASS" is a data delivery pattern — it populates specific form fields with verified attribute values from eSeal-authenticated documents. The two may co-exist in the same SP flow but serve distinct purposes and involve different data models.

---

## 2) Problem Statement & User Need

### The Problem

When onboarding with a bank, insurer, telecom provider, or government portal, users are currently required to manually transcribe personal data — name, Emirates ID number, date of birth, nationality, visa expiry, address — from physical or digital documents into web or mobile forms. This creates:

1. **Transcription errors** — incorrect data leads to failed KYC checks, application rejections, and support escalations at the SP.
2. **Friction and drop-off** — high cognitive load during onboarding correlates with form abandonment, particularly on mobile.
3. **Trust deficit** — manually entered data lacks cryptographic provenance; SPs cannot verify its authenticity at point of entry.
4. **Repeated data entry** — the same identity attributes are re-entered for every new SP, even though UAE PASS already holds verified equivalents.

From the UAE PASS DV data (November 2025): 16.9% of sharing requests are abandoned at the consent screen — the highest single drop-off point in the funnel. Form friction is a known contributor to this abandonment. Additionally, 20.6% of sharing requests are "dead on arrival" (SP requests a document the user lacks) — Form Filler with a pre-check mechanism could eliminate a significant portion of these dead requests by scoping to attributes the user actually holds.

### Who Is Affected

| Persona | Pain |
|---------|------|
| UAE resident / citizen applying for a bank account | Must manually enter 10–15 fields from Emirates ID and Visa |
| Expat applying for telecom SIM registration | Must type passport data and visa details from physical documents |
| User completing insurance application | Must enter health card and EID data repeatedly across fields |
| SP KYC officer (bank/insurer) | Receives manually entered data with transcription errors; re-verification adds cost |
| SP developer | No standard API for attribute-level data ingestion; SP builds its own form + validation logic |

### User Stories

**Primary:**
As a UAE resident applying for a bank account online, I want to click "Fill with UAE PASS" and have my Emirates ID and Visa details auto-populate the required form fields, so that I can complete the application without manual transcription errors and in significantly less time.

**Secondary:**
As a service provider integrating with UAE PASS, I want to receive verified, eSeal-authenticated attribute data for specific form fields, so that my KYC checks pass first time and my onboarding conversion rate improves.

**Tertiary:**
As a user, I want to see exactly which fields will be shared with the SP before I approve, so that I feel in control of my personal data and give informed consent.

### Evidence of Need

- MyInfo benchmark (2026-02-26): Singapore's equivalent delivers an 80% reduction in application time and processes ~300K transactions/day across 1,000+ services — demonstrating strong, proven demand.
- UAE PASS DV funnel data: 16.9% consent screen abandonment is partly attributable to form friction; pre-filled data reduces decision fatigue.
- Competitive analysis (2025-12-29): UAE PASS DV identified as lacking selective attribute-level disclosure — "Fill with UAE PASS" is the citizen-facing manifestation of this capability.
- SP feedback (qualitative): SPs (banks, telcos) consistently raise KYC cost reduction and onboarding friction as top integration pain points. _[TO BE CONFIRMED with formal SP survey]_

---

## 3) Stakeholder Impact Matrix

### TDRA
| Dimension | Assessment |
|-----------|------------|
| Policy alignment | **Strong alignment.** "Fill with UAE PASS" directly supports UAE digital government goals (paperless services, national identity utility). Consistent with UAE Digital Economy Strategy and PASS platform mandate. |
| Regulatory considerations | **TDRA must define the approved attribute access policy** — specifically, which attribute categories SPs in each sector (banking, insurance, government, telecom) are permitted to request. This is a policy decision, not a product decision. UAE PDPL (Personal Data Protection Law) consent model must be verified: per-session, per-SP, revocable consent is the assumed model. |
| Approval required | Yes — attribute access scope policy must be ratified by TDRA before SP onboarding guidance is published. |

### DDA
| Dimension | Assessment |
|-----------|------------|
| Design approval required | **Yes — critical path.** Three new screen types require DDA design approval: (1) "Fill with UAE PASS" button specification and placement guidance for SPs, (2) in-app attribute consent review screen (which fields, from which document, to which SP), (3) post-fill confirmation or error state. |
| UX impact | High. The consent screen design for "Fill with UAE PASS" is a net-new UX pattern distinct from the existing document sharing consent flow. RTL layout, bilingual copy, and accessibility must be reviewed. |
| Estimated DDA review cycle | 2–4 weeks per the established sprint dependency constraint. |

### ICP
| Dimension | Assessment |
|-----------|------------|
| Document issuance impact | **Direct impact.** The feature relies on attribute extraction from ICP-issued documents: Emirates ID, Residence Visa, and Passport are the three highest-value source documents. |
| Schema publication required | **ICP must formally publish and maintain a versioned attribute schema** for each supported document type (field names, data types, validation rules, update cadence). This is a prerequisite — without it, SP API integration cannot be standardised. |
| Coordination level | High. ICP schema agreement is the single longest-lead dependency. Must be initiated in parallel with design and engineering. |
| ICP eSeal transition relevance | As ICP moves to self-signing HSM, the eSeal provenance chain for extracted attributes must be validated against the new certificate chain. No DV code change expected, but attribute-level eSeal binding must be confirmed during transition. |

### Service Providers (SPs)
| Dimension | Assessment |
|-----------|------------|
| Integration changes | **New API required.** SPs must implement a new API endpoint pattern to: (a) declare which attributes they are requesting (Attribute Request Object), (b) receive the attribute payload from UAE PASS, and (c) validate eSeal provenance on received attributes. This is distinct from the existing document-level sharing API. |
| API impact | Medium-High. A new attribute-level API resource is required. Existing document-sharing API is not retired — both patterns will coexist for different SP use cases. |
| Onboarding implications | The SP integration guide, DDA-approved SP portal, and onboarding documentation must all be updated. SPs must complete a new attribute access approval process scoped by TDRA policy. |
| Receptiveness | **High.** KYC cost reduction is a well-established SP pain point. Banking and insurance SPs are the most likely early adopters. _[Confirmed as pattern from SP stakeholder notes.]_ |

### End Users
| Dimension | Assessment |
|-----------|------------|
| Direct UX impact | **Highly positive.** Eliminates 10–15 field manual entries in common SP onboarding flows. Reduces risk of application failure due to transcription error. |
| Consent implications | Explicit per-session consent is mandatory. The user must see a granular attribute list (field name + source document) before approving. No persistent or background data sharing. |
| Trust implications | Showing "this data comes from your Emirates ID, verified by ICP" materially increases user trust in the accuracy of the submitted data. |
| Risk | Users who decline "Fill with UAE PASS" must retain the option to enter data manually — the feature must degrade gracefully. |

### Engineering (FE/BE/QA)
| Dimension | Assessment |
|-----------|------------|
| FE effort | **High.** New consent screen (attribute-level), new button integration pattern, SP SDK or web component, RTL/bilingual screen variants, accessibility testing. |
| BE effort | **High.** Attribute extraction service (parse Verifiable Presentation → individual attributes), attribute-level eSeal provenance binding, new API resource (attribute request/response), schema validation layer, per-attribute consent audit log. |
| QA effort | **High.** Cross-document schema testing (EID, Visa, Passport, Driving License), SP API integration testing across sectors, eSeal provenance validation, edge cases (missing fields, expired documents, partial attribute sets), bilingual and RTL regression. |
| Overall effort estimate | **High** — this is a new capability layer, not an extension of an existing pattern. |
| Technical risk | **Medium-High.** Primary risk is attribute schema misalignment across ICP document versions. Secondary risk is eSeal provenance chain integrity at attribute level (vs. document level, which is well-established). |

---

## 4) Technical Feasibility

### Architecture Overview

"Fill with UAE PASS" is architecturally a **selective attribute disclosure layer** built on top of the existing Verifiable Presentation sharing infrastructure. The request-consent-deliver pattern is preserved; the payload granularity changes from document-level to attribute-level.

```
SP Form → Attribute Request (correlation ID + field list) → UAE PASS backend
→ Attribute Extraction from Verifiable Presentation
→ User Consent (attribute-level review)
→ Attribute Response Payload (field values + eSeal provenance references)
→ SP Form Auto-Population
```

### Dependencies on Existing Systems

| System | Dependency Type | Notes |
|--------|----------------|-------|
| Verifiable Presentation sharing flow | Extension — attribute extraction layer on top of existing flow | Core request-consent-deliver pattern reused |
| eSeal validation (CAdES/PAdES) | Critical — attribute provenance must reference source document eSeal | No change to eSeal validation logic itself; new binding metadata required |
| QR code / correlation ID hygiene | Reused — same uniqueness, TTL, and one-time-use rules apply | No changes required to QR infrastructure |
| Firebase Remote Config | Used for phased rollout and feature flag management | No new infrastructure needed |
| Notification system | Notification for "Fill with UAE PASS" request may use existing actionable notification type | Copy update required; no new notification type |

### New Infrastructure Required

| Component | Description | Risk |
|-----------|-------------|------|
| Attribute Extraction Service | Parses Verifiable Presentation for a given document type and extracts named fields per the published schema | Medium — depends on ICP schema publication |
| Attribute Catalogue / Schema Registry | Central registry of supported document types, field names, data types, and issuer mapping | High — cross-issuer coordination required; ICP ownership TBC |
| Attribute Request Object (API) | New API resource: SP declares required fields by document type | Medium — new API design, backward compatible |
| Per-Attribute Consent Audit Log | Audit trail of which attributes were shared, with which SP, at what timestamp | Low — extension of existing sharing audit model |
| SP Attribute Response SDK/Spec | Documentation and sample code for SPs to receive, parse, and validate attribute payloads | Low — documentation effort |

### Security and Privacy Implications

1. **Consent model**: Per-session, per-SP, field-level consent. No persistent or stored consent. User must explicitly approve each Fill request. This is non-negotiable.
2. **No PII in QR codes**: The attribute request is initiated via the existing correlation ID pattern. No attribute names or values appear in the QR payload.
3. **eSeal provenance chain**: Every returned attribute value must carry a reference to its source document and the eSeal that authenticates that document. SPs must be able to verify this chain independently (offline, without a UAE PASS API call) — this preserves the architectural differentiator vs. MyInfo-style API-trust models.
4. **Minimum necessary principle**: SPs may only request attributes they are authorised to receive under TDRA-approved policy. A request for unauthorised attributes must be rejected server-side before presenting to the user.
5. **Attribute-level logging**: All fill events must be logged in the sharing audit trail, including which attributes were shared, not only which documents.
6. **Data retention at SP**: UAE PASS delivers the attribute payload; SP-side data retention is governed by TDRA/PDPL policy and is outside DV's control. The SP onboarding agreement must codify this. _[TO BE CLARIFIED with TDRA legal.]_

### Risk Register

| Risk | Level | Mitigation |
|------|-------|------------|
| ICP schema not published on time | High | Begin ICP coordination in Sprint 71; treat schema publication as a hard dependency gate |
| Attribute schema version drift (ICP updates EID format) | Medium | Version the Attribute Catalogue; include document version in eSeal provenance reference |
| SP API adoption slower than expected | Medium | Provide reference implementation and sandbox environment; target 3 pilot SPs before GA |
| eSeal provenance integrity at attribute level | Medium | Validate during ICP eSeal transition testing (already in Q1 2026 plan) |
| PDPL consent model ambiguity | Medium | Engage TDRA legal before design begins; do not assume per-session model is sufficient |
| User confusion: "Fill" vs "Share" vs "Continue" | Low-Medium | Requires DDA to define clear button hierarchy and naming standard across all UAE PASS entry points |

### Technical Red Flags / Blockers

- **Blocker**: Attribute Catalogue does not currently exist as a formal artefact. It must be created and ratified with ICP before attribute extraction can be implemented. This is the single most critical pre-scoping action.
- **Blocker**: ICP schema agreement requires formal cross-agency coordination — this cannot be assumed or estimated without an active engagement track.

---

## 5) UX & Design Considerations

### New Screens and Flows Required

**Flow 1 — SP Side (Web/App)**
- New "Fill with UAE PASS" button (DDA-designed, standardised asset provided to SPs)
- Button triggers attribute request creation on UAE PASS backend (server-to-server) and surfaces as a deep link or QR for mobile

**Flow 2 — UAE PASS App (User Side)**
- Attribute Consent Review Screen: lists each requested field, its value (masked or clear, per TDRA policy), and the source document (e.g., "Emirates ID — issued by ICP")
- Primary CTA: "Share" / «مشاركة»
- Secondary CTA: "Enter manually instead" / «الإدخال اليدوي بدلاً من ذلك» (graceful degradation)
- Tertiary: "Decline" — cancels the fill request without sharing

**Flow 3 — SP Side (Post-Fill)**
- Form fields auto-populated
- Success state: visual indicator that fields were filled via UAE PASS (trust signal for user)
- Error state: if a requested field is unavailable (e.g., document missing), SP must display a user-friendly fallback message

### Bilingual Copy Pairs (EN/AR)

All copy follows RTL formatting rules. Arabic text uses the Arabic UI font (Cairo). Numbers are presented RTL per existing conventions.

| English | Arabic |
|---------|--------|
| Fill with UAE PASS | «أكمل بـ UAE PASS» |
| The following information will be shared with [SP Name]: | «سيتم مشاركة المعلومات التالية مع [اسم مزود الخدمة]:» |
| Share | «مشاركة» |
| Enter manually instead | «الإدخال اليدوي بدلاً من ذلك» |
| Requested fields | «الحقول المطلوبة» |
| Source | «المصدر» |
| Emirates ID number | «رقم الهوية الإماراتية» |
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

### RTL Considerations

- The attribute list on the consent screen must render in RTL column order: Value (right) | Field Label | Source (left).
- The "Fill with UAE PASS" button asset must have an AR-text variant with right-to-left visual weight.
- Icon placement (UAE PASS logo) must be mirrored for AR direction.
- Test truncation: "أكمل بـ UAE PASS" is shorter than "Fill with UAE PASS" — button sizing should accommodate the English version as the maximum-width constraint.

### Arabic Pluralisation Edge Cases

- The attribute list count is non-user-facing in this flow (no counter is displayed), so pluralisation is not a primary concern on the consent screen itself.
- If a summary notification is shown (e.g., "3 fields shared with [SP]"), pluralisation rules apply:
  - 1 field: «حقل واحد»
  - 2 fields: «حقلان»
  - 3–10 fields: «حقول»
  - 11+ fields: «حقلاً»

### DDA Design Approval Required

**Yes — required for:**
1. "Fill with UAE PASS" button visual specification (logo usage, colour, sizing) — to be provided to SPs as a design asset
2. In-app attribute consent review screen template
3. Post-fill success/error state treatments
4. Button hierarchy guidelines (Fill vs Continue vs Share vs Sign — four distinct UAE PASS entry points must be differentiated)

**Recommended action:** Initiate DDA design brief in Sprint 71, targeting design approval by Sprint 73 to avoid blocking engineering.

### Accessibility

- All consent screen elements must meet WCAG 2.1 AA minimum.
- Field values on the consent screen must support screen reader description in both languages.
- The "Enter manually instead" escape path must be keyboard-accessible and visually prominent.

---

## 6) Prioritisation Scoring

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Priority** | **8 (High)** | "Fill with UAE PASS" is the citizen-facing manifestation of the Form Filler initiative, which is explicitly listed as a 2026 roadmap High priority. It directly addresses the 16.9% consent screen drop-off (highest funnel leak) and the recurring SP pain point of KYC onboarding friction. The feature unlocks new SP integration value and strengthens the UAE PASS national identity utility proposition. |
| **Complexity** | **3 (High complexity)** | A new capability layer — not an extension of an existing pattern. Requires: (1) net-new Attribute Catalogue with ICP coordination, (2) new attribute extraction service, (3) new SP API resource, (4) per-attribute eSeal provenance binding, (5) DDA consent screen design approval, (6) TDRA attribute access policy definition, (7) multi-sector SP onboarding. Any one of the six dependencies (ICP, DDA, TDRA policy, SP API, attribute service, audit log) can delay delivery independently. |
| **Total** | **11** | Consistent with the Foundational schema/capability scoring precedent established in MEMORY.md. High priority, high complexity — merits a dedicated discovery sprint and phased delivery approach before backlog entry as a single deliverable. |

**Scoring rationale note:** A score of 11 reflects a feature that is strategically essential but requires significant upfront prerequisite work. Delivering it in parts (Attribute Catalogue first, then Fill UX) would produce two items: Catalogue at 11, Fill UX at 13 (once catalogue dependency is resolved) — consistent with the MyInfo benchmark analysis precedent.

---

## 7) Roadmap Alignment

### Alignment with 2026 Roadmap

| Roadmap Initiative | Relationship to "Fill with UAE PASS" |
|-------------------|--------------------------------------|
| Form Filler (High priority, 2026 roadmap) | **Direct alignment** — "Fill with UAE PASS" IS the Form Filler feature, named and scoped here |
| Consent Screen Redesign (Q2 2026, Initiative 5) | **Dependency** — the attribute-level consent screen for Fill is a net-new design; the Consent Screen Redesign workstream should incorporate Fill consent patterns to avoid double design work |
| Status-Based Reporting (Q1 Sprint 70, P0) | **Indirect dependency** — Fill conversion metrics cannot be baselined without accurate reporting; do not launch Fill without the measurement layer in place |
| ICP eSeal Transition Completion (Q1 2026) | **Critical dependency** — attribute-level eSeal provenance must be validated against the new ICP self-signing certificates before Fill is released |
| Auto-Add Documents (Q2 2026, pending legal) | **Complementary, not prerequisite** — Fill operates on existing documents; Auto-Add improves document availability. Fill should not be blocked by Auto-Add legal review. |
| Dual Citizenship GA (Sprint 72) | **Dependency for dual citizens** — Fill must correctly resolve Primary EID (UAE) vs Secondary EID for dual citizenship users per existing sharing logic |
| SP Quality Scoring Program (Q3 2026) | **Downstream beneficiary** — Fill adoption rate per SP becomes a natural quality signal in SP scoring |

### Sprint Readiness Assessment

| Phase | Earliest Sprint | Prerequisite |
|-------|----------------|-------------|
| Discovery & ICP Schema Engagement | Sprint 71 (next quarter) | None — start immediately |
| DDA Design Brief | Sprint 71 | None — start in parallel |
| Attribute Catalogue Definition | Sprint 72–73 | ICP schema agreement |
| BE: Attribute Extraction Service | Sprint 74+ | Attribute Catalogue ratified |
| FE: Consent Screen (Fill flow) | Sprint 74+ | DDA design approval |
| SP API Spec + Pilot Integration | Sprint 74–76 | BE service, SP partner commitment |
| QA + eSeal provenance validation | Sprint 76–77 | All above complete |
| GA (initial 2 sectors) | Q3 2026 earliest | All above + TDRA policy approval |

**Assessment:** "Fill with UAE PASS" cannot enter the next sprint as a delivery item. It can — and should — enter the next sprint as a discovery and stakeholder engagement workstream. Full delivery is realistically Q3 2026, assuming ICP engagement begins in Sprint 71.

---

## 8) Recommended Document Fields per Use Case

The following field sets represent the minimum viable attribute scope per sector. TDRA must approve which fields each SP category is authorised to request. These are product recommendations, not policy decisions.

### 8.1 Banking / Account Opening (KYC)

| Field | Source Document | Data Type | Notes |
|-------|----------------|-----------|-------|
| Full name (EN) | Emirates ID | String | As printed on EID |
| Full name (AR) | Emirates ID | String | Arabic name field |
| Emirates ID number | Emirates ID | String (15-digit) | National ID number |
| Date of birth | Emirates ID | Date (DD/MM/YYYY) | |
| Gender | Emirates ID | Enum (M/F) | |
| Nationality | Emirates ID / Passport | Enum (country code) | Primary nationality |
| Passport number | Passport | String | For non-citizen accounts |
| Passport expiry date | Passport | Date | For residency-linked products |
| Visa type / category | Residence Visa | Enum | Employment / Family / Investor etc. |
| Visa expiry date | Residence Visa | Date | For residency-linked products |
| Home emirate / address | Emirates ID | String | If address field is present on EID record |
| EID expiry date | Emirates ID | Date | For AML/CDD document validity checks |

**Sectors:** Retail banking, digital-only banks, investment accounts, credit card applications

### 8.2 Insurance (Health, Motor, Life)

| Field | Source Document | Data Type | Notes |
|-------|----------------|-----------|-------|
| Full name (EN/AR) | Emirates ID | String | |
| Emirates ID number | Emirates ID | String | For policy binding |
| Date of birth | Emirates ID | Date | Age-rating for premiums |
| Gender | Emirates ID | Enum | Actuarial inputs |
| Nationality | Emirates ID | Enum | |
| Visa status / expiry | Residence Visa | Enum / Date | Coverage period alignment |
| Health Insurance Card number | Health Insurance Card | String | For health insurance renewals / portability |
| Health Insurance Card expiry | Health Insurance Card | Date | |
| Vehicle registration number | Vehicle Registration | String | For motor insurance |
| Vehicle make / model / year | Vehicle Registration | String / Integer | For motor insurance |
| Driving License number | Driving License | String | For motor insurance |
| Driving License expiry | Driving License | Date | |

**Sectors:** Health insurers, motor insurers, life / term insurers

### 8.3 Telecom (SIM Registration / KYC)

| Field | Source Document | Data Type | Notes |
|-------|----------------|-----------|-------|
| Full name (EN) | Emirates ID | String | TRA SIM registration requirement |
| Emirates ID number | Emirates ID | String | |
| Date of birth | Emirates ID | Date | Age verification |
| Nationality | Emirates ID | Enum | |
| Visa type / expiry | Residence Visa | Enum / Date | For residency-linked plans |
| Passport number | Passport | String | For visitors / short-stay SIM registration |
| Passport expiry | Passport | Date | |

**Sectors:** Etisalat (e&), du, MVNO operators. Note: TRA (Telecom Regulatory Authority) imposes specific SIM registration field mandates — Fill attribute scope for telecom must align with TRA requirements. _[TO BE CLARIFIED: confirm TRA-mandated fields are covered by UAE PASS DV document catalogue.]_

### 8.4 Government Services / Portals

| Field | Source Document | Data Type | Notes |
|-------|----------------|-----------|-------|
| Full name (EN/AR) | Emirates ID | String | |
| Emirates ID number | Emirates ID | String | Primary citizen identifier |
| Date of birth | Emirates ID | Date | |
| Gender | Emirates ID | Enum | |
| Nationality | Emirates ID | Enum | |
| Emirates of residence | Emirates ID | Enum | For emirate-specific services |
| Visa type / status | Residence Visa | Enum | For services restricted by residency type |
| Passport number | Passport | String | For services involving international travel |
| Driving License number | Driving License | String | For RTA, traffic fines, vehicle services |
| Vehicle registration | Vehicle Registration | String | For municipal / RTA services |

**Sectors:** MOHRE (work permits), ICA (visa services), RTA (driving / vehicle), DEWA (utility connections), municipal portals

### 8.5 Cross-Sector Field Prioritisation Summary

| Field | Banking | Insurance | Telecom | Government | Priority |
|-------|---------|-----------|---------|------------|----------|
| Full name (EN) | Yes | Yes | Yes | Yes | P1 — universal |
| Emirates ID number | Yes | Yes | Yes | Yes | P1 — universal |
| Date of birth | Yes | Yes | Yes | Yes | P1 — universal |
| Nationality | Yes | Yes | Yes | Yes | P1 — universal |
| Gender | Yes | Yes | No | Yes | P1 — near-universal |
| Visa expiry date | Yes | Yes | Yes | Yes | P1 — universal |
| Full name (AR) | Yes | No | No | Yes | P2 — government/banking |
| Passport number | Yes | Yes | Yes | Yes | P2 — cross-sector |
| EID expiry date | Yes | No | No | Yes | P2 — banking/government |
| Health Insurance Card | No | Yes | No | No | P3 — insurance-specific |
| Vehicle registration | No | Yes | No | Yes | P3 — motor/government |
| Driving License | No | Yes | No | Yes | P3 — motor/government |

**Recommended minimum viable attribute set for v1 launch:** P1 fields only (Full name EN, EID number, Date of birth, Nationality, Gender, Visa expiry). These are present on Emirates ID and Residence Visa — the two highest-availability documents in the UAE PASS catalogue.

---

## 9) Competitive Benchmarking

### 9.1 Singapore MyInfo (Singpass) — Closest Analogue

**Maturity:** GA since 2016 (government), 2018 (private sector)
**Scale:** 300K transactions/day, 1,000+ integrated services, 4.5M users (97% eligible population)
**Key capability:** Government-to-SP attribute sharing with per-transaction user consent; 80% reduction in application time

**Architectural comparison with UAE PASS:**

| Dimension | MyInfo (Singapore) | UAE PASS Fill (Proposed) |
|-----------|-------------------|--------------------------|
| Trust model | API-trust (GovTech asserts data accuracy) | **eSeal-trust (ICP eSeal attached to attribute payload; SP can verify independently — offline)** |
| Data source | Government database at point of request | eSeal-authenticated document stored in DV |
| SP verification | Must call MyInfo API to validate | Can validate eSeal offline — no UAE PASS API call needed |
| Consent model | Per-transaction | Per-session (proposed) |
| Attribute catalogue | Published, versioned | **Does not yet exist — prerequisite gap** |
| Offline capable | No (API-dependent) | **Yes (eSeal provenance) — UAE PASS architectural differentiator** |
| Sector coverage | Banking, insurance, telco, government, property | Banking, insurance, telco, government (proposed v1) |

**UAE PASS advantage:** The eSeal provenance model is architecturally stronger than MyInfo's API-trust model for independent verification. UAE PASS should lead with this differentiator in SP onboarding materials.

**UAE PASS gap vs MyInfo:** MyInfo has a formally published, versioned attribute catalogue with clear field schemas for all supported document types. UAE PASS does not. This is the most critical gap to close before delivery.

### 9.2 EU eIDAS Wallet (European Digital Identity Wallet)

**Status:** Regulation in force (2024); member states deploying 2025–2026
**Key capability:** Selective disclosure of identity attributes from government-issued credentials; zero-knowledge proof support in roadmap

**Relevance to UAE PASS:**
- eIDAS Wallet mandates attribute-level selective disclosure — confirming this is the global regulatory direction.
- The consent model (user selects specific attributes to share) is directionally aligned with "Fill with UAE PASS."
- eIDAS uses W3C Verifiable Credentials and SD-JWT formats — UAE PASS uses CAdES/PAdES eSeal. Interoperability is not a near-term requirement, but monitoring for future cross-border scenarios (UAE-EU) is advisable.

**Key differentiator:** eIDAS Wallet requires offline verification support — UAE PASS's eSeal model already supports this, giving UAE PASS a head start vs. identity systems that are API-dependent.

### 9.3 India DigiLocker

**Scale:** 500M+ users, 6B+ documents issued
**Key capability:** Document sharing between government issuers and verifiers; URI-based document references; limited form-fill through Digilocker-integrated services

**Relevance to UAE PASS:**
- DigiLocker operates at a scale that validates the government-to-citizen document utility model.
- DigiLocker's consent model is document-level (share the whole document), not attribute-level — UAE PASS "Fill with UAE PASS" would be more granular and therefore more privacy-preserving.
- DigiLocker lacks eSeal-equivalent provenance at attribute level — UAE PASS's model is technically superior.

**UAE PASS advantage:** UAE PASS's attribute-level sharing with eSeal provenance is materially more privacy-preserving and verifier-friendly than DigiLocker's document-blob model.

### 9.4 Sign in with Apple — AutoFill

**Key capability:** Apple uses PassKit and the Contacts framework to pre-fill forms with user-stored data (name, address, email, phone). No government-verified provenance; data comes from the device address book.

**Relevance to UAE PASS:**
- Apple AutoFill establishes the UX convention users already understand: "one button to fill the form."
- Critical gap vs. UAE PASS Fill: Apple data has no cryptographic provenance. A bank cannot verify that the name entered via Apple AutoFill matches a government-issued document.
- UAE PASS Fill is directly superior for KYC-grade use cases because it provides eSeal-authenticated, issuer-verified attribute values — not self-asserted user data.

**UX takeaway:** Adopt Apple AutoFill's button placement convention (prominent, near form entry point) and single-tap approval pattern. Match the interaction simplicity while delivering verified data that Apple cannot.

### 9.5 Germany BundID / ELSTER (eID)

**Key capability:** German national eID (nPA chip) used for government service authentication and form pre-fill; attribute disclosure via AusweisApp2 SDK.

**Relevance to UAE PASS:**
- BundID demonstrates the government portal use case: citizens use their national eID to authenticate AND pre-fill government service applications in one flow.
- The AusweisApp2 SDK model (a standardised native app SDK that SPs integrate) is analogous to what UAE PASS might deliver as an SP integration SDK for "Fill with UAE PASS."
- BundID's chip-based architecture is more constrained than UAE PASS's cloud-based model — UAE PASS can support a broader range of SPs and use cases.

### 9.6 Competitive Benchmarking Summary Table

| Platform | Attribute-Level Sharing | eSeal/Cryptographic Provenance | Offline Verifiable | Consent Model | Attribute Catalogue Published |
|----------|------------------------|-------------------------------|-------------------|---------------|------------------------------|
| MyInfo (SG) | Yes | No (API trust) | No | Per-transaction | Yes |
| eIDAS Wallet (EU) | Yes | Yes (SD-JWT/mdoc) | Yes | Per-transaction | Yes (in progress) |
| DigiLocker (IN) | No (document-level) | No | No | Per-document | No |
| Apple AutoFill | Partial (address book) | No | N/A | Per-app setting | No |
| BundID (DE) | Yes (limited fields) | Yes (chip-based) | Partial | Per-transaction | Partial |
| **UAE PASS Fill (proposed)** | **Yes** | **Yes (CAdES/PAdES eSeal)** | **Yes** | **Per-session** | **Not yet — prerequisite gap** |

**Conclusion:** UAE PASS Fill's proposed architecture is competitive with or superior to all five benchmarked platforms on the dimension that matters most for SP trust — cryptographic provenance. The single structural gap (Attribute Catalogue) is solvable and must be the first delivery milestone.

---

## 10) Acceptance Criteria

The following acceptance criteria are written for the minimum viable implementation of "Fill with UAE PASS" covering the P1 attribute set (EID and Residence Visa fields) with two pilot SP integrations.

**AC-01 — Attribute Request Initiation**
Given an SP has integrated the "Fill with UAE PASS" API and the user is on the SP's form, when the user taps the "Fill with UAE PASS" button, then the UAE PASS app is launched (or a deep link is followed) and an attribute consent review screen is displayed within 3 seconds showing the SP's name and the list of requested fields.

**AC-02 — Attribute Consent Screen Content**
Given the consent review screen is displayed, when the user reviews the screen, then each requested field must show: (a) the field name in both EN and AR, (b) the source document name (e.g., "Emirates ID") and issuer (e.g., "ICP"), and (c) the attribute value (masked or clear per TDRA policy). No fields outside the TDRA-approved attribute scope for this SP category may appear.

**AC-03 — Per-Session Consent Confirmation**
Given the user reviews the attribute consent screen, when the user taps "Share" / «مشاركة», then (a) the attribute payload is delivered to the SP within the session, (b) a consent event is written to the per-attribute audit log with SP ID, timestamp, and list of shared field names, and (c) the user is returned to the SP form with the approved fields auto-populated.

**AC-04 — Manual Entry Escape Path**
Given the consent review screen is displayed, when the user taps "Enter manually instead" / «الإدخال اليدوي بدلاً من ذلك», then the user is returned to the SP form with no data shared, no audit log entry written, and all form fields remaining empty for manual entry.

**AC-05 — Decline / Cancel Handling**
Given the consent review screen is displayed, when the user taps "Decline" or dismisses the screen, then (a) no attributes are shared, (b) no audit log entry is written for the declined request, (c) the SP receives a standardised decline response code, and (d) the SP form remains available for manual entry.

**AC-06 — Missing Document Handling**
Given an SP requests an attribute from a document the user does not hold in their DV (e.g., a Driving License field requested but user has no Driving License), when the consent screen is generated, then the missing field is displayed with a clear indicator (e.g., "Not available — document not in your UAE PASS") and the user may still approve sharing of available fields. The SP receives the partial payload with null values for unavailable fields, flagged as unavailable rather than incorrect.

**AC-07 — Expired Document Handling**
Given an SP requests an attribute from a document that is present but expired, when the consent screen is generated, then the expired document and its fields are shown with an expiry warning. The user may still share the fields, and the SP receives the payload with an expiry status flag on the relevant attributes.

**AC-08 — eSeal Provenance Integrity**
Given an attribute payload is delivered to an SP, when the SP validates the payload, then each attribute value must carry a reference to its source document's eSeal signature, enabling the SP to independently verify the attribute's authenticity without an online call to UAE PASS. This validation must pass for all P1 attribute fields from Emirates ID and Residence Visa.

**AC-09 — RTL and Bilingual Rendering**
Given the user's device is set to Arabic locale, when the consent review screen is displayed, then all text renders in RTL layout, all Arabic field labels and copy are displayed per the approved bilingual copy list, and the "Fill with UAE PASS" button displays its Arabic variant «أكمل بـ UAE PASS».

**AC-10 — Unauthorized Attribute Request Rejection**
Given an SP submits an attribute request containing a field not authorised for that SP category under TDRA policy, when the request is processed by the UAE PASS backend, then the request is rejected server-side before presentation to the user, and the SP receives a standardised error code indicating an unauthorised attribute was requested. No partial or filtered consent screen is shown.

---

## 11) Open Questions & Risks

| # | Question / Risk | Owner | Priority |
|---|----------------|-------|----------|
| 1 | _[TO BE CLARIFIED]_ — Which SP categories are authorised to request which attribute sets under TDRA policy? This is a policy decision that gates the SP onboarding guide, API design, and consent screen content. | TDRA | Critical |
| 2 | _[TO BE CLARIFIED]_ — Will ICP formally publish and maintain a versioned attribute schema for Emirates ID, Residence Visa, and Passport? If so, on what timeline, and who owns schema change communication to SPs? | ICP | Critical |
| 3 | _[TO BE CLARIFIED]_ — Does the UAE PDPL (Personal Data Protection Law) require any specific consent mechanism beyond per-session explicit approval? E.g., right to withdraw previously shared data at SP, minimum retention window at SP, or specific consent record format? | TDRA Legal | Critical |
| 4 | _[TO BE CLARIFIED]_ — What is the attribute value presentation policy? Should the consent screen show the actual attribute value to the user before sharing (full transparency), or mask it (privacy-first)? Different SPs may have different security implications. | TDRA / DDA | High |
| 5 | _[TO BE CLARIFIED]_ — Does the Driving License (RTA-issued) attribute schema differ materially from ICP-issued documents? If so, RTA coordination is needed in addition to ICP for the P3 attribute set. | RTA / Engineering | Medium |
| 6 | **Known risk**: DDA design approval for the consent screen is the most likely schedule risk. If not initiated in Sprint 71, Q3 2026 delivery is at risk. | DDA / DV PM | High |
| 7 | **Known risk**: SPs must update their API integration to receive and validate attribute payloads. SP migration timelines are historically 4–8 weeks. Pilot SP selection and pre-engagement should begin no later than Sprint 73. | SP Partnerships | High |
| 8 | **Known risk**: The existing "Continue with UAE PASS" button and the new "Fill with UAE PASS" button will co-exist on SP pages. Without a clear DDA-defined button hierarchy, SPs will place them inconsistently, creating user confusion about which button does what. | DDA | High |
| 9 | _[TO BE CLARIFIED]_ — For the TRA telecom SIM registration use case, are there mandatory field formats or validation rules mandated by TRA that may differ from the field format in the UAE PASS attribute payload? | TRA (Telecom) | Medium |
| 10 | **Assumption to validate**: The existing Verifiable Presentation sharing infrastructure can be extended to support attribute-level extraction without a full re-architecture. This assumption should be validated by the BE lead in Sprint 71 discovery. | Engineering BE | Medium |

---

## 12) Recommendation

**Verdict: Recommend — with phased delivery and prerequisite gate**

"Fill with UAE PASS" is a strategically essential feature that directly addresses the two most significant problems in the UAE PASS DV ecosystem: SP onboarding friction (KYC cost and form drop-off) and the absence of a citizen-facing, government-verified data utility. The eSeal provenance model gives UAE PASS a genuine architectural differentiator over every comparable global platform, including Singapore's MyInfo. The feature has clear demand from both citizens and SPs, strong roadmap alignment, and a proven commercial model at scale internationally.

However, the feature cannot be scoped into a single delivery sprint. It has six independent prerequisite gates — ICP attribute schema agreement, TDRA attribute access policy, DDA consent screen design approval, PDPL legal review of consent model, BE attribute extraction service, and SP API migration — any one of which can delay delivery independently. Treating this as a monolithic feature and attempting to deliver it in a single sprint cycle is the primary delivery risk.

**Recommended phased approach:**

| Phase | Scope | Target | Gate |
|-------|-------|--------|------|
| 0 — Prerequisites | ICP schema engagement, TDRA policy brief, DDA design brief, PDPL review | Sprint 71–72 | All gates must pass before Phase 1 begins |
| 1 — Attribute Catalogue | Define, publish, and ratify the formal attribute schema for EID and Residence Visa | Sprint 72–73 | ICP sign-off required |
| 2 — Core Fill (P1 attributes) | BE attribute extraction, FE consent screen, SP API spec, 2 pilot SPs (1 bank, 1 telecom) | Sprint 74–77 | DDA design approval + ICP schema |
| 3 — Expanded attribute set | P2 fields (Passport, EID expiry), additional sectors (insurance, government) | Q4 2026 | Phase 2 GA + SP adoption data |
| 4 — Advanced capabilities | ZKP / selective disclosure, offline attribute pack, cross-border considerations | 2027 | Phase 3 adoption baseline |

**Suggested next actions:**

1. **This sprint**: Brief TDRA on feature concept; request initiation of attribute access policy definition process.
2. **Sprint 71**: Open formal engagement track with ICP on attribute schema publication timeline.
3. **Sprint 71**: Submit DDA design brief for consent screen and button specification.
4. **Sprint 71**: Assign BE lead to complete technical feasibility validation (attribute extraction from Verifiable Presentation; eSeal provenance at attribute level).
5. **Sprint 72**: Identify 2 pilot SP partners (target: 1 bank, 1 telecom); begin pre-integration alignment.
6. **Sprint 72**: Engage TDRA Legal on PDPL consent model requirements.

---

_Document prepared for TDRA product review. All `_[TO BE CLARIFIED]_` items require stakeholder input before delivery scoping can be finalised._
