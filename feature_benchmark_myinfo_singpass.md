# Feature Benchmark Analysis: MyInfo by Singpass

**Date**: 2026-02-26 | **Analyst**: Feature Benchmark Analyser | **Status**: Draft
**Prepared for**: UAE PASS DV Product Team — TDRA
**Purpose**: Inform roadmap decisions for Form Filler, Auto-Add Documents, and document sharing enhancements

---

## 1. Executive Summary

MyInfo is Singapore's government-operated "tell us once" personal data platform, built on top of the Singpass national digital identity infrastructure and operated by the Government Technology Agency (GovTech). It allows citizens to grant service providers (SPs) one-time, per-transaction access to their government-verified personal data — eliminating manual form entry and document submission. Since its private-sector opening in 2017, MyInfo has been integrated into over 1,000 digital services, with approximately 300,000 transactions processed daily across a user base of 4.5 million (97% of Singapore residents aged 15 and above).

For the UAE PASS DV product team, MyInfo represents the most mature, government-operated analogue to the capabilities currently in delivery or on the 2026 roadmap: Form Filler, Auto-Add Documents, and the Verifiable Presentation sharing flow. The benchmarking reveals both strong architectural alignment with UAE PASS's existing direction and specific capability gaps — most critically, a standardised attribute-level data catalogue and a structured SP data-access approval workflow — that UAE PASS should evaluate for adoption.

The overall recommendation is **Recommend with scoping**: three specific features derived from the MyInfo model are prioritised for UAE PASS DV in Section 13.3 and scored in Section 15.

---

## 2. Feature Overview

### 2.1 What MyInfo Is

MyInfo is a consent-based personal data sharing layer that sits between government data sources (immigration, tax, pension, employment agencies) and service providers (banks, insurers, telcos, government portals). It is a component of Singapore's National Digital Identity (NDI) programme.

**Core value proposition**: A citizen authenticates with Singpass once, selects which verified data fields to share, consents, and the SP's form is auto-populated with government-authoritative data — no document upload, no manual entry, no OCR fallback.

**Operator**: Government Technology Agency (GovTech), under the Ministry of Digital Development and Information (MDDI), Singapore.

**Variants**:
- **MyInfo (Personal)** — citizen data for individuals (KYC, onboarding, applications)
- **MyInfo Business** — corporate entity data via CorpPass (company registration, UEN, directors, shareholders from ACRA)
- **SGFinDex** — extension layer enabling citizens to share private-sector financial data (bank accounts, insurance policies, CPF) with participating institutions, authenticated via Singpass

### 2.2 Problem It Solves

| Problem | MyInfo Solution |
|---------|----------------|
| Citizens repeatedly submit the same identity documents across different services | Single consent per transaction; data pulled once from source |
| Document authenticity cannot be trusted by SPs (fakes, outdated copies) | Government-authoritative data; no document scanning required |
| SP onboarding takes days due to manual KYC verification | Near-instant approval; 80% reduction in onboarding time reported |
| Data entry errors cause rejection and re-application | Verified fields carry zero transcription error |
| KYC cost burden on financial institutions | Up to S$50 savings per customer acquisition online; 30% reduction in verification costs |

---

## 3. User Journey (Citizen)

The citizen-facing experience follows a consistent pattern across all integrated services:

**Step 1 — Service Initiation**
The citizen visits an SP's digital service (e.g., bank account opening, insurance application, government benefit claim). The SP presents a "Fill with Singpass" or "Retrieve MyInfo" button.

**Step 2 — Singpass Authentication**
The citizen is redirected to Singpass for authentication (password + OTP, or biometric via the Singpass app). This step is mandatory — MyInfo data is never released without authenticated identity.

**Step 3 — Consent Screen**
The citizen sees a structured consent screen listing exactly which data fields the SP has requested (e.g., Full Name, NRIC, Date of Birth, Address, Income). The citizen can review, deselect individual fields (data minimisation), or decline entirely and proceed manually.

**Step 4 — Data Return**
Upon consent, MyInfo pulls the requested fields from the relevant government agencies in real time and returns them to the SP. The SP's form is auto-populated. The citizen reviews the pre-filled form, makes any corrections, and submits.

**Step 5 — Audit Trail**
The citizen can view a log of all MyInfo data sharing transactions via the Singpass app ("Consent History"), enabling post-hoc review and trust management.

**Key UX principles**:
- The citizen is never redirected away from the SP context for longer than one Singpass authentication step
- Data field granularity is visible: the citizen sees "Full Name, Date of Birth, Nationality" not just "personal details"
- Manual fallback is always available — consent is voluntary, not mandatory for service access
- Consent is per-transaction: no persistent grants; each SP visit requires fresh consent

---

## 4. Service Provider Journey

**Step 1 — Discovery and Eligibility**
SPs browse the Singpass API Library (api.singpass.gov.sg) and review data categories, key principles, and use-case guidelines. Only Singapore-registered companies are eligible. Government agencies use a parallel pathway.

**Step 2 — User Journey Submission**
Before receiving sandbox access, the SP must submit a documented "user journey" — a structured walkthrough showing how MyInfo data will be used in their service, which fields will be requested, and for what purpose. GovTech reviews this to enforce data minimisation and appropriate use.

**Step 3 — Sandbox Access**
Upon approval, GovTech provisions an App ID and sandbox credentials. The SP integrates using the MyInfo v5 REST API (or legacy v3/v4 until decommission in September 2026). GovTech provides a mock Singpass environment (MockPass) and a reference implementation library.

**Step 4 — Production Approval**
After sandbox testing, the SP undergoes a production review. GovTech evaluates security posture, compliance with data handling obligations, and user journey quality before granting production access.

**Step 5 — Integration Architecture**
The SP's backend implements the OAuth 2.0 / OIDC flow with PKCE. The citizen consent redirect passes through Singpass, and upon consent, the SP's server calls the MyInfo Person API with the authorisation code to retrieve the granted data fields as a JSON payload. All calls are server-to-server; data does not pass through the SP's frontend.

**Step 6 — Ongoing Obligations**
SPs must comply with Singapore's PDPA for the data they receive, adhere to agreed use-case scope (no secondary use without separate consent), and migrate to new API versions per GovTech's published timelines.

---

## 5. Technical Architecture

### 5.1 Core Architecture Pattern

MyInfo uses a **federated, real-time pull** model, not a centralised data store:

```
[Government Agency DBs] ← pull at consent time → [MyInfo API Layer] → [SP Backend]
     ICA / CPF / IRAS / MOM / HDB                      (GovTech)
```

Critically, **MyInfo does not store user data in a persistent vault**. Each transaction triggers a fresh pull from the originating government agency. This eliminates stale data risk and reduces the attack surface of a centralised database.

### 5.2 Authentication & Authorisation Stack

- **Identity provider**: Singpass (OpenID Connect)
- **API security (current, v3/v4)**: OAuth 2.0, RS256 client assertions, X.509 certificates
- **API security (upcoming, v5/FAPI 2.0)**:
  - Pushed Authorization Requests (PAR) — auth parameters sent via secure back-channel, not URL
  - DPoP (Demonstration of Proof-of-Possession) — access tokens cryptographically bound to the requesting client
  - ID Token Encryption (JWE) — token payload encrypted end-to-end
  - PKCE enforced for all integrations
  - JWKS-based key management replaces X.509 certificates
- **API versioning**: v3 decommissioned 30 September 2026; v4 and v5 supported with v5 (FAPI 2.0) as the target state

### 5.3 Data Retrieval Flow

1. SP initiates authorisation request (PAR in v5)
2. Citizen authenticates via Singpass; consent screen presented
3. Singpass issues authorisation code to SP callback
4. SP backend exchanges code for access token (server-to-server, DPoP-bound)
5. SP backend calls MyInfo Person API with access token
6. MyInfo fetches real-time data from relevant agencies, assembles JSON response
7. Data returned to SP backend; never touches SP frontend

### 5.4 SP Integration Tooling

- REST API (JSON over HTTPS)
- Official reference implementation: `singpass-myinfo-oidc-helper` (open source, GitHub)
- MockPass sandbox for local development and CI testing
- Published OpenAPI specifications

### 5.5 SGFinDex Extension

SGFinDex extends the model into private-sector financial data: citizens can authorise the flow of their bank account, insurance, and investment data between participating financial institutions, also authenticated via Singpass. 15 financial institutions participate as of 2024. This is the "private-sector data" complement to MyInfo's "government data" scope.

---

## 6. Data Scope & Categories

MyInfo's data catalogue is the product's most distinctive characteristic. It spans seven primary categories sourced from multiple government agencies:

| Category | Key Data Fields | Primary Source Agency |
|----------|----------------|----------------------|
| **Personal Identity** | Full name (as on NRIC/FIN), NRIC/FIN number, date of birth, gender, nationality, race, religion, dialect group | ICA (Immigration & Checkpoints Authority) |
| **Contact** | Registered address (NRIC-linked), email, mobile number | ICA, Singpass profile |
| **Passport** | Passport number, issue/expiry date, country of issue | ICA |
| **Residency/Immigration Status** | Pass type, pass status, pass expiry, long-term visit pass details | ICA |
| **Employment & CPF** | Employer name, occupation, CPF contribution history (month, employer, amount), OA/SA/MA/RA balances | MOM (Ministry of Manpower), CPF Board |
| **Income & Tax** | Yearly assessable income (latest 2 years of assessment), Notice of Assessment details | IRAS (Inland Revenue Authority of Singapore) |
| **Education** | Highest qualification, field of study, name of institution | MOE / SkillsFuture |
| **Family** | Marital status, marriage date/place, spouse data, children (name, DOB, gender) | ROM (Registry of Marriages), ICA |
| **Property** | HDB flat ownership, address, flat type, number of owners | HDB (Housing Development Board) |
| **Vehicle & Driving Licence** | Driving licence class, expiry, demerit points, suspension dates; vehicle make, model, registration number | LTA (Land Transport Authority) |

**Total data fields available**: The MyInfo Business data catalogue lists over 40 distinct personal data fields across these categories, with sub-fields (e.g., CPF contribution records per month) expanding the count substantially.

**Field-level granularity**: SPs request specific fields, not whole categories. A bank opening a savings account might request Name, NRIC, DOB, Address, and Income only — not family status or vehicle data. GovTech enforces this via the user journey review process.

**Data accuracy**: All fields reflect the government's authoritative record. If a citizen's address registered with ICA is outdated, MyInfo returns the outdated address — it does not self-correct. This is both a trust guarantee and a limitation.

---

## 7. Consent & Privacy Model

### 7.1 Consent Design Principles

- **Per-transaction, explicit consent**: Every MyInfo data retrieval requires a fresh authentication and consent act. There are no persistent, standing grants to SPs.
- **Field-level transparency**: The consent screen displays exactly which fields will be shared, not a vague category like "personal information."
- **Field-level deselection**: Citizens can deselect individual fields before consenting. If the SP's service requires a field the citizen deselects, the SP must handle the missing data gracefully (e.g., fallback to manual input for that field).
- **Voluntary consent**: Declining MyInfo never blocks service access; manual form submission with document upload remains available.
- **Audit history**: The Singpass app provides a consent log showing date, SP name, and data fields shared for each past transaction.
- **Data minimisation enforcement**: GovTech's user journey review process requires SPs to justify every field requested. Fields deemed unnecessary for the stated use case are not approved.

### 7.2 Regulatory Basis

- Government agencies operating MyInfo are governed by Singapore's **Public Sector (Governance) Act 2018** and GovTech's internal IM8 (Infocomm Technology & Smart Systems Management) policies — not directly subject to PDPA.
- SPs receiving data via MyInfo are subject to **Singapore's Personal Data Protection Act 2012 (PDPA)**, administered by the Personal Data Protection Commission (PDPC). They must comply with obligations on purpose limitation, security safeguards, and retention limits.
- The platform aligns with PDPA's consent, notification, and data minimisation obligations for the private-sector leg of the data transfer.

### 7.3 Known Consent Model Limitations

- **Scope creep risk**: As MyInfo integrates into more services (dating apps, lifestyle platforms), the principle that "only necessary data should be shared" becomes harder to enforce through manual user journey reviews at GovTech's current scale.
- **Informed consent question**: Academic and privacy commentators (NTU Nanyang Business School, Privacy Ninja) have raised that users may not meaningfully understand which fields they are consenting to share, particularly for complex financial data.
- **No revocation of past shares**: Once data has been shared and received by an SP, the citizen cannot retroactively revoke the SP's copy. Revocation only prevents future sharing.
- **Dark web compromise risk**: By Q2 2024, over 2,300 compromised Singpass accounts were found on dark web marketplaces — a credential theft vector, not a MyInfo architectural flaw, but a systemic risk to the entire consent model.

---

## 8. Trust & Verification Model

### 8.1 Source of Truth Architecture

MyInfo's trustworthiness derives from a single principle: data is pulled directly from the originating government registry, not from the citizen's assertion or a document scan. The authoritative source for each field is contractually defined:

- Name and NRIC: ICA's national population register
- Income: IRAS's tax assessment database
- CPF balances: CPF Board's scheme records
- Employment: MOM's employer reporting system

This means MyInfo data is as fresh and accurate as the government's own records — and no more. If a government agency's records are incorrect, MyInfo propagates that error.

### 8.2 No Cryptographic Proof at Field Level

MyInfo does not provide verifiable credentials with cryptographic proofs at the field level in the W3C VC (Verifiable Credentials) or ISO mDL sense. The SP receives a signed JSON payload from the MyInfo API, where the signature attests that GovTech assembled this payload from its authoritative sources — but the individual field values do not carry issuer-level cryptographic seals (unlike UAE PASS DV's eSeal model on issued documents).

This is a significant architectural difference from UAE PASS DV. UAE PASS's approach — where each issued document carries an issuer eSeal (CAdES/PAdES) validatable by the SP independently — provides a stronger, decentralised trust model for individual fields.

### 8.3 SP Verification Responsibility

SPs are expected to trust the MyInfo API response as authoritative because it comes from a GovTech-operated endpoint over a mutually authenticated TLS channel. There is no equivalent to UAE PASS DV's eSeal that SPs can independently verify offline.

---

## 9. Adoption & Impact Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Singpass registered users | 4.5 million | ~97% of Singapore residents aged 15+ |
| Services integrated with MyInfo | 1,000+ | Government and private sector |
| Government/private organisations on Singpass | 800+ agencies / 460+ organisations | Total platform |
| Daily MyInfo transactions | ~300,000 | Approximate; as of 2024 |
| Annual transactions (full platform) | 350 million+ | Singpass total |
| Reduction in onboarding time | Up to 80% | Reported by major banks post-MyInfo |
| Reduction in verification costs | ~30% | Industry average reported |
| Increase in approval rates | ~15% | Due to better data quality |
| Cost savings per customer acquisition (financial sector) | Up to S$50 | Online channel, GovTech/MAS estimate |
| SGFinDex users | ~150,000 | 290,000 bank accounts connected |
| MyInfo v3 decommission deadline | 30 September 2026 | Migration to v5 (FAPI 2.0) required |

**Adoption trajectory**: MyInfo was opened to the private sector in 2017. It reached 1,000 integrated services faster than initially projected, driven primarily by the banking and insurance sectors' need to digitise KYC processes in compliance with MAS regulations.

---

## 10. Key UX Patterns & Design Principles

### 10.1 "Fill with Singpass" Button Standard

GovTech publishes mandatory design guidelines for how SPs must present the MyInfo entry point. A standardised "Fill with Singpass" button with defined dimensions, colours, and placement rules creates a uniform recognition pattern across all services — citizens know what to expect before clicking. This design consistency is enforced as a condition of integration approval.

### 10.2 Transparent Field-Level Consent Screen

The consent screen shows a structured list of fields with their current values (where pre-viewable), the source agency, and individual opt-out controls. This is not a generic "I agree" checkbox — the citizen sees:

```
Sharing with: [Bank Name]
- Full Name: TAN BOON KIAT (from ICA)
- NRIC: S1234567A (from ICA)
- Date of Birth: 15 Jan 1985 (from ICA)
- Registered Address: 123 Ang Mo Kio Avenue 3... (from ICA)
- Annual Assessable Income: S$72,000 (from IRAS)
[Confirm] [Cancel]
```

### 10.3 Single-Session Flow

The entire citizen journey — SP page → Singpass auth → consent → return to SP with pre-filled form — is designed to complete within a single browser or app session. The redirect chain is minimal and rehearsed. GovTech measures and optimises completion rate at each step.

### 10.4 Graceful Degradation

If a citizen declines MyInfo or if a required field is unavailable, the SP's form must fall back gracefully to manual input. SPs that make MyInfo mandatory without a fallback fail GovTech's integration review.

### 10.5 Consent History in Identity App

The Singpass app includes a dedicated "Transaction History" section where citizens can review every MyInfo consent event: date, SP name, fields shared. This post-hoc transparency reduces anxiety about data sharing and creates an audit mechanism accessible to the citizen — not just to the platform operator.

### 10.6 Data Freshness Enforcement

Every new transaction triggers a fresh data pull from the source agency. MyInfo explicitly prohibits SPs from caching retrieved data and re-using it in subsequent transactions. This is both a privacy protection and a data quality guarantee.

---

## 11. Limitations & Known Gaps

### 11.1 Government Data Quality Dependency

MyInfo is only as accurate as government registries. Citizens with incorrect records at ICA, IRAS, or CPF must first correct the source record before MyInfo returns accurate data. There is no correction mechanism within MyInfo itself.

### 11.2 Singapore-Resident Only

Only Singapore citizens, permanent residents, and foreigners with valid Singapore passes can use MyInfo. There is no cross-border equivalent — a UAE citizen transacting in Singapore cannot use MyInfo. This is a design constraint driven by legal jurisdiction; government data sources are bounded by territory.

### 11.3 No Persistent Consent or Standing Grants

Each transaction requires a fresh consent act. While this is a strong privacy protection, it creates friction for recurring transactions (e.g., a user updating their address with multiple SPs simultaneously would need to consent to each SP individually). There is no "update all my SPs" capability.

### 11.4 No Offline or Verifiable Credential Mode

MyInfo requires a live API call to GovTech's servers. There is no offline-capable mode, no downloadable verifiable credential, and no QR-based presentation that an SP could verify without calling the MyInfo API. This limits use cases such as in-person document presentation (e.g., at a counter) or offline KYC.

This is the most significant structural gap compared to UAE PASS DV, which issues eSeal-stamped documents that can be cryptographically verified by any SP independently without calling DV's servers.

### 11.5 Web-Only Integration (Historical)

MyInfo APIs currently only support web-based integration as the primary flow. Mobile-native deep link integration is possible but relies on the Singpass app. Pure SDK-based in-app integration without a web redirect has historically been limited, though the v5 FAPI 2.0 roadmap addresses some of these constraints.

### 11.6 Scope Creep and Consent Fatigue

As MyInfo integrates into more and more services, including lifestyle platforms and non-critical applications, the principle of data minimisation becomes harder to enforce through manual user-journey reviews. Critics from NTU and privacy advocacy groups have noted that highly sensitive fields (marital status, NRIC) are now being shared with commercial platforms well beyond the original financial services scope.

### 11.7 Credential Theft Systemic Risk

Since all MyInfo transactions are gated on Singpass authentication, credential compromise (infostealer malware, phishing) bypasses all field-level consent controls. In 2024, 2,300+ compromised Singpass accounts were found on dark web markets. A stolen account can be used to silently share a citizen's data with any integrated SP without the citizen's knowledge.

### 11.8 No Independent SP Verification

SPs cannot independently verify the authenticity of data received via MyInfo without trusting the GovTech-signed API response. There is no cryptographic proof at the field level that an SP can verify against a public key infrastructure independently. This creates a single point of trust (GovTech), which is appropriate in Singapore's governance context but would be a centralisation concern in a multi-authority federation like the UAE.

---

## 12. Regulatory Framework

### 12.1 Singapore Legal Basis

| Layer | Instrument | Applies To |
|-------|-----------|-----------|
| Government data management | Public Sector (Governance) Act 2018 | GovTech operating MyInfo |
| Data quality / registries | Agency-specific legislation (ICA Act, CPF Act, IRAS Act) | Source agencies |
| SP data handling | Personal Data Protection Act 2012 (PDPA) | Private-sector SPs receiving MyInfo data |
| Financial sector SPs | MAS Technology Risk Management Guidelines | Banks, insurers integrating MyInfo |
| Overall NDI framework | Smart Nation and Digital Government initiative (policy, not statute) | Entire Singpass/MyInfo programme |

### 12.2 PDPA Asymmetry

A critical nuance: the PDPA explicitly exempts public agencies from its provisions. GovTech is not bound by PDPA in operating MyInfo. However, private-sector SPs who receive data via MyInfo are fully subject to PDPA. This creates an asymmetric compliance landscape — the government side of the data flow operates under executive governance, while the private sector side operates under statutory regulation.

### 12.3 GovTech's Approval Gate as Regulatory Proxy

Because there is no specific statute governing MyInfo data access for private sector SPs, GovTech's user journey review and App ID approval process functions as a de facto regulatory gate. SPs cannot access MyInfo without GovTech's explicit, case-by-case approval. This makes GovTech simultaneously a product operator and a quasi-regulator of the data ecosystem it has created.

---

## 13. Relevance to UAE PASS DV

### 13.1 Direct Parallels — What UAE PASS Already Does

| MyInfo Capability | UAE PASS DV Equivalent | Parity Assessment |
|------------------|----------------------|------------------|
| Consent-based sharing with SPs | Document Sharing (Verifiable Presentation) | High parity — UAE PASS's per-transaction consent model is architecturally equivalent |
| Singpass authentication as gateway | UAE PASS SSO / QR authentication | High parity |
| Issuer-sourced document data | Issued documents from ICP (EID, Visa, Passport) | High parity |
| Cryptographic authenticity guarantee | eSeal validation (CAdES/PAdES) on issued documents | UAE PASS is stronger — eSeal enables independent offline verification; MyInfo does not |
| Notification of data sharing event | Actionable notifications for sharing requests | High parity |
| SP onboarding with approval gate | SP integration onboarding process | Moderate parity — UAE PASS has onboarding but user journey review process is less formalised |
| Audit log of sharing events | Sharing request history (in-progress) | Moderate parity — UAE PASS has correlation ID tracking; citizen-facing history view is _[TO BE CLARIFIED]_ |

**Key Insight**: UAE PASS DV's trust model is architecturally superior to MyInfo for the sharing of individual document data, because eSeal-stamped documents can be verified by any SP independently without calling DV servers. MyInfo requires trust in GovTech's signed API response with no field-level cryptographic proof. UAE PASS should preserve and communicate this competitive advantage.

### 13.2 Gaps — What UAE PASS Could Learn or Adopt

#### Gap 1: Structured Attribute-Level Data Catalogue
**MyInfo**: Offers 40+ named, field-level data attributes (Full Name, NRIC, DOB, Address, Income, CPF balances, etc.) as discrete, requestable units. SPs request specific fields via the API.

**UAE PASS DV**: Currently operates at the document level (share this EID, share this driving licence). Attribute extraction exists implicitly through the Verifiable Presentation, but there is no published, standardised attribute catalogue that SPs can browse and request individual fields from.

**Gap**: UAE PASS lacks a formal attribute-level data catalogue — a structured enumeration of every data field available from each issued document type, with field IDs, data types, and issuer source labels. This is the foundational missing piece that would enable Form Filler and selective attribute sharing.

#### Gap 2: "Fill with UAE PASS" — Standardised SP Form Fill UX
**MyInfo**: The "Fill with Singpass" button with enforced design guidelines creates a universal recognition pattern. Citizens know what to expect; SPs implement to a standard.

**UAE PASS DV**: The 2026 roadmap includes Form Filler (High priority), but there is no current public-facing design standard for how SPs should present UAE PASS form fill as an option to users — no equivalent to GovTech's button design and consent screen specifications.

**Gap**: UAE PASS lacks a standardised, SP-implemented "Fill with UAE PASS" UX pattern, including a defined consent screen template, button design specifications, and SP implementation guidelines for graceful degradation (fallback when user declines or field is unavailable).

#### Gap 3: Formalised User Journey Review for Data Access
**MyInfo**: Before any SP receives production access, GovTech reviews a documented user journey to enforce data minimisation. SPs cannot request fields they cannot justify.

**UAE PASS DV**: SP onboarding covers technical integration (correlation IDs, eSeal, security), but the current onboarding guide does not appear to include a structured review of which document attributes the SP will request and why.

**Gap**: UAE PASS lacks a formalised data access justification process as part of SP onboarding — analogous to GovTech's user journey review. This gap will become more significant as attribute-level sharing matures and the range of SPs requesting more sensitive fields expands.

#### Gap 4: Citizen-Facing Consent History Log
**MyInfo**: Every MyInfo transaction is logged and visible to the citizen in the Singpass app ("Transaction History"), enabling post-hoc review.

**UAE PASS DV**: The sharing request status tracking system (implemented via the correlation ID framework) provides operational tracking, but a citizen-facing, in-app log of "data you have shared, with whom, and when" is not confirmed as an available feature.

**Gap**: UAE PASS DV lacks a confirmed citizen-facing sharing history view — a log accessible within the app showing every consent-based sharing event, the SP name, the documents/attributes shared, and the timestamp.

#### Gap 5: Proactive "Freshness" Enforcement
**MyInfo**: Data freshness is enforced architecturally — every transaction pulls fresh data from the source agency; caching by SPs is prohibited.

**UAE PASS DV**: Auto-Add Documents (one-time consent for periodic issuer checks) addresses the document-availability freshness problem but does not address the SP-side question of whether SPs are re-using stale attribute data from old Verifiable Presentations.

**Gap**: UAE PASS DV does not currently have an SP-side data freshness policy — analogous to MyInfo's prohibition on SP caching — that would prevent SPs from re-using attribute data from a previous Verifiable Presentation in subsequent transactions without re-requesting.

---

### 13.3 Feature Recommendations for UAE PASS DV Roadmap

The following three feature recommendations are derived directly from the MyInfo benchmark. Each is framed as a user story and mapped to existing roadmap context.

---

#### Recommendation A: Formal Attribute Data Catalogue

**User Story (SP)**: "As a service provider, I want to browse a standardised catalogue of data attributes available from UAE PASS-issued documents (with field IDs, data types, and issuer labels), so that I can design my integration to request only the specific attributes my service needs."

**User Story (Citizen)**: "As a UAE resident, I want to see exactly which fields about me a service provider is requesting before I share my data, so that I can make an informed consent decision."

**Roadmap link**: Directly enables and defines the scope of Form Filler (2026, High priority). Without a formal attribute catalogue, Form Filler implementations will be ad hoc and inconsistent across SPs.

**Recommended content for catalogue** (derived from UAE PASS-issued document types):

| Document Type | Key Attributes | Issuer |
|--------------|---------------|--------|
| Emirates ID | Full name (EN/AR), EID number, DOB, gender, nationality, card expiry, PUID | ICP |
| Residency Visa | Visa type, visa number, entry permit, expiry, sponsor name | ICP |
| Passport | Passport number, issue/expiry date, place of birth, MRZ | ICP |
| Driving Licence | Licence number, categories, issue/expiry date | _[TO BE CLARIFIED — issuer agency]_ |

**Arabic copy pair**:
- "Attribute Catalogue" / «فهرس البيانات»
- "Requested fields" / «الحقول المطلوبة»
- "Source" / «المصدر»
- "Emirates ID number" / «رقم الهوية الإماراتية»

---

#### Recommendation B: "Fill with UAE PASS" — Standardised Form Fill UX Pattern

**User Story (Citizen)**: "As a UAE resident transacting with a bank or government portal, I want to tap 'Fill with UAE PASS' and see exactly which fields from my documents will be shared before I confirm, so that I can complete the form instantly without manual data entry or document upload."

**User Story (SP)**: "As a service provider, I want to implement a standardised 'Fill with UAE PASS' button and consent screen against UAE PASS's defined specifications, so that my users have a consistent, trusted experience that increases form completion rates."

**Roadmap link**: This is the citizen and SP UX manifestation of Form Filler. It converts Form Filler from a backend capability into a recognisable, consistent product pattern.

**Key design specifications to define** (DDA design review required):
1. "Fill with UAE PASS" button — UAE PASS brand-compliant, mandatory SP placement guidelines
2. Consent screen template — field list, source labels, per-field opt-out, EN/AR bilingual
3. Graceful degradation specification — behaviour when user declines or field is unavailable
4. SP implementation guide update — add Form Filler consent screen requirements

**Arabic copy pair**:
- "Fill with UAE PASS" / «أكمل بـ UAE PASS»
- "The following information will be shared with [SP Name]:" / «سيتم مشاركة المعلومات التالية مع [اسم مزود الخدمة]:»
- "Share" / «مشاركة»
- "Enter manually instead" / «الإدخال اليدوي بدلاً من ذلك»

---

#### Recommendation C: Citizen-Facing Sharing History Log

**User Story (Citizen)**: "As a UAE PASS user, I want to see a log of every time I have shared my documents or attributes with a service provider, so that I can review what was shared, with whom, and when — and build confidence in the platform."

**Roadmap link**: Complements the existing sharing request status tracking system (Status-Based Reporting initiative, Sprint 70). The operational data exists; this recommendation is to surface it as a citizen-facing feature in the DV interface.

**Suggested log entry content** (per sharing event):
- Date and time
- SP name (display name, not internal ID)
- Documents and/or attributes shared
- Correlation ID (for support reference, shown as human-readable reference number)
- Status (Approved / Declined / Expired)

**Arabic copy pair**:
- "Sharing History" / «سجل المشاركة»
- "Shared with" / «تمت المشاركة مع»
- "on [date]" / «في [التاريخ]»
- "You shared [document name]" / «شاركت [اسم المستند]»
- "No sharing history yet." / «لا يوجد سجل مشاركة حتى الآن.»

---

## 14. Feasibility Assessment for UAE PASS

### 14.1 Technical Feasibility

| Recommendation | Technical Feasibility | Key Dependencies | Risk |
|---------------|----------------------|-----------------|------|
| A — Attribute Catalogue | Medium | Requires structured extraction of attribute schemas from existing issued document types; alignment with ICP on published field definitions; API schema changes for field-level requests | Medium — schema standardisation is non-trivial across multiple issuers |
| B — "Fill with UAE PASS" UX Pattern | Medium | Depends on Attribute Catalogue (A) being defined first; DDA design approval; SP API update to support field-level requests in Verifiable Presentation; bilingual copy system | Medium — UX and SP coordination effort is high; core tech exists |
| C — Sharing History Log | Low–Medium | Status-Based Reporting data infrastructure is being built (Sprint 70); citizen-facing UI requires new screen design; SP display name mapping needed | Low — data exists; frontend work is the primary effort |

**No new external infrastructure is required** for any of the three recommendations. All three build on existing UAE PASS DV capabilities (document sharing, correlation ID tracking, Verifiable Presentation). The primary effort is in schema definition (A), UX design (B), and frontend development (C).

**eSeal compatibility**: All three recommendations are compatible with the existing eSeal validation model. Attribute-level data sharing (Recommendation A) should preserve eSeal provenance where possible — i.e., the Verifiable Presentation should indicate which eSeal-signed document each attribute was extracted from, enabling SPs to validate the source.

### 14.2 Legal/Regulatory Feasibility (UAE Context)

| Consideration | Assessment |
|--------------|-----------|
| UAE Personal Data Protection Law (Federal Decree-Law No. 45 of 2021) | Per-transaction consent model (Recommendations A–C) is compliant with UAE PDPL's consent and purpose limitation requirements — _[TO BE CLARIFIED with TDRA legal team]_ |
| Auto-Add Documents legal review (in progress) | Recommendations A–C do not depend on Auto-Add Documents; they operate within the per-transaction consent model already established |
| Data residency | All data processing remains within UAE PASS DV infrastructure; no cross-border transfer implied — _[TO BE CONFIRMED]_ |
| TDRA policy alignment | Per-transaction consent and attribute-level sharing aligns with TDRA's stated principle of consent-based sharing; no known policy conflicts — _[TO BE CONFIRMED with TDRA]_ |
| ICP data fields | ICP agreement to publish a formal attribute schema for EID, Visa, and Passport fields must be negotiated — _[TO BE CLARIFIED]_ |

**No direct analogues to Singapore's PDPA/GovTech governance asymmetry issue exist in UAE PASS DV**: TDRA operates as regulator and product owner, and ICP operates as issuer. The governance model is more integrated than Singapore's, which reduces the regulatory complexity of the private-sector data handoff.

### 14.3 Stakeholder Alignment

| Stakeholder | Position | Key Consideration |
|------------|----------|------------------|
| TDRA | Likely supportive — aligns with UAE digital transformation goals and consent-based data sharing principles | Attribute Catalogue requires TDRA policy decision on which fields SPs may access |
| DDA | DDA design review required for Recommendations A (consent screen template) and B (button design). DDA approval is on the critical path for B | Bilingual consent screen design is non-trivial; DDA engagement should start early |
| ICP | Agreement needed to publish formal attribute schemas for ICP-issued documents | ICP eSeal transition (self-signing HSM) should not conflict; this is a schema/metadata concern, not a signing infrastructure concern |
| SPs | High interest from banks, insurers, and telcos — equivalent to Singapore's banking sector adoption of MyInfo; reduces KYC cost and onboarding friction | SP API changes for field-level requests require migration guide and communication plan |
| Engineering (FE/BE/QA) | Medium effort for A and B; low–medium for C | API schema changes for field-level Verifiable Presentation are the highest-effort engineering item |

### 14.4 Estimated Complexity

| Recommendation | Complexity | Rationale |
|---------------|-----------|-----------|
| A — Attribute Catalogue | High | Requires cross-issuer schema alignment, API changes, SP migration, ICP coordination, policy decisions on field access scope |
| B — "Fill with UAE PASS" UX Pattern | Medium | Design-heavy; depends on A; SP coordination required; DDA approval on critical path; core tech (Verifiable Presentation) exists |
| C — Sharing History Log | Low–Medium | Data infrastructure in progress; primarily a frontend and SP display-name mapping task |

---

## 15. Prioritisation Score

Using the UAE PASS DV scoring model: Priority (High=8, Medium=5, Low=3) + Complexity (Low=8, Medium=5, High=3) = Total Score (max 16)

### 15.1 Attribute Catalogue (Recommendation A)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Priority | **8** (High) | Foundational enabler for Form Filler (already High priority on 2026 roadmap) and all future attribute-level sharing. Without this, Form Filler is ad hoc and unscalable. |
| Complexity | **3** (High) | Cross-issuer schema definition, API changes, ICP coordination, SP migration, and TDRA policy decisions make this the most complex of the three recommendations. |
| **Total** | **11** | |

**Verdict**: Recommend — add as a prerequisite work stream to Form Filler in the 2026 roadmap. Start with a discovery sprint to define the attribute schema for EID, Visa, and Passport with ICP.

---

### 15.2 "Fill with UAE PASS" UX Pattern (Recommendation B)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Priority | **8** (High) | Directly enables Form Filler's citizen-facing value proposition. Without a standardised UX pattern, Form Filler delivers inconsistent SP experiences that will undermine adoption. MyInfo's most powerful adoption driver was the standardised button and consent screen — not the underlying API. |
| Complexity | **5** (Medium) | Design work is substantial (DDA approval required) but core technology (Verifiable Presentation, consent flow) exists. SP coordination is manageable with a clear spec and migration guide. Depends on A being completed or in progress. |
| **Total** | **13** | |

**Verdict**: Recommend — schedule DDA design review for the consent screen template and "Fill with UAE PASS" button specifications in Q2 2026. Coordinate with Form Filler delivery. DDA approval is the critical path.

---

### 15.3 Sharing History Log (Recommendation C)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Priority | **5** (Medium) | High citizen trust value; directly reinforces UAE PASS's consent-based positioning. However, it does not unlock new sharing volume directly — it is a trust and transparency feature. Moderate priority relative to roadmap. |
| Complexity | **8** (Low) | Status-Based Reporting infrastructure (Sprint 70) is building the data layer. Frontend screen is the primary remaining work. No new backend infrastructure required. |
| **Total** | **13** | |

**Verdict**: Recommend — add to backlog as a Q3 2026 candidate. Low delivery risk given the data infrastructure already in progress. Pair with Status-Based Reporting delivery for efficiency.

---

### 15.4 Comparative Prioritisation Summary

| Recommendation | Priority Score | Complexity Score | Total | Sprint Readiness |
|---------------|---------------|-----------------|-------|-----------------|
| A — Attribute Catalogue | 8 | 3 | **11** | Discovery sprint Q1 2026; delivery Q2–Q3 |
| B — "Fill with UAE PASS" UX | 8 | 5 | **13** | DDA design review Q2 2026; delivery Q3 |
| C — Sharing History Log | 5 | 8 | **13** | Backlog entry now; delivery Q3 2026 |

**Note on Recommendation A's lower total score**: The lower total (11 vs 13) reflects high complexity, not lower priority. A must be initiated first because B depends on it. Treat A as a prerequisite, not as a lower-priority item.

---

## 16. Sources & References

- [Singpass MyInfo — Official Product Overview (Singpass Developer Docs)](https://docs.developer.singpass.gov.sg/docs/products/singpass-myinfo)
- [MyInfo — How It Works (Singapore Government Developer Portal)](https://www.developer.tech.gov.sg/products/categories/digital-identity/myinfo/how-it-works)
- [MyInfo — Getting Started (Singapore Government Developer Portal)](https://www.developer.tech.gov.sg/products/categories/digital-identity/myinfo/getting-started)
- [MyInfo Business — Data Items (Singpass)](https://www.singpass.gov.sg/main/myinfobusiness/data-items)
- [MyInfo Business — FAQ (Singpass)](https://www.singpass.gov.sg/main/myinfobusiness/faq)
- [MyInfo Data Catalog — Personal (Singpass Developer Docs)](https://docs.developer.singpass.gov.sg/docs/data-catalog-myinfo/catalog/personal)
- [MyInfo Data Catalog — Finance (Singpass Developer Docs)](https://docs.developer.singpass.gov.sg/docs/data-catalog-myinfo/catalog/finance)
- [MyInfo Data Catalog — Education and Employment (Singpass Developer Docs)](https://docs.developer.singpass.gov.sg/docs/data-catalog-myinfo/catalog/education-and-employment)
- [MyInfo Data Catalog — Vehicle and Driving Licence (Singpass Developer Docs)](https://docs.developer.singpass.gov.sg/docs/data-catalog-myinfo/catalog/vehicle-and-driving-licence)
- [MyInfo Data Catalog — Property (Singpass Developer Docs)](https://docs.developer.singpass.gov.sg/docs/data-catalog-myinfo/catalog/property)
- [FAPI 2.0 Authentication API — Singpass Developer Docs](https://docs.developer.singpass.gov.sg/docs/upcoming-changes/fapi-2.0-authentication-api)
- [MyInfo v3 Decommissioning Notice — May 2025 (Singpass Partner Support)](https://partnersupport.singpass.gov.sg/hc/en-sg/articles/46944126585753--15-May-2025-Agencies-Important-Updates-Myinfo-v3-Decommissioning-on-30-September-2026)
- [MyInfo v5 Migration Guide — Login/Myinfo Apps (Singpass Developer Docs)](https://docs.developer.singpass.gov.sg/docs/technical-specifications/migration-guides/login-myinfo-v5-apps)
- [Singpass API — Implementation Technical Requirements](https://api.singpass.gov.sg/library/myinfo/developers/implementation-technical-requirements)
- [SGFinDex — MAS Overview](https://www.mas.gov.sg/development/fintech/sgfindex)
- [GovTech Singapore — Singpass Product Page](https://www.tech.gov.sg/products-and-services/for-citizens/digital-services/singpass/)
- [Singpass — National Digital Identity Overview (MDDI Factsheet)](https://www.mddi.gov.sg/newsroom/singpass-factsheet-02032022/)
- [Singpass — OECD Observatory of Public Sector Innovation](https://oecd-opsi.org/innovations/singpass/)
- [World Bank — Singapore NDI and Government Data Sharing Case Study](https://blogs.worldbank.org/en/digital-development/how-singapores-national-digital-identity-and-government-digital-data-sharing)
- [What is MyInfo? — Sumsub Blog](https://sumsub.com/blog/singapore-my-info-singpass/)
- [MyInfo Business Edge — Adnovum Blog](https://www.adnovum.com/blog/verified-data-streamlined-processes-the-myinfo-business-edge-in-singapore)
- [Why Singpass MyInfo Still Matters — Adnovum Blog](https://www.adnovum.com/blog/what-is-singpass-myinfo-and-how-does-it-enhance-your-services)
- [Singpass Integration — WhooshPro](https://www.whooshpro.com/singpass-integration/)
- [Cybercriminals Targeting Singapore Citizens — Resecurity (2024)](https://www.resecurity.com/blog/article/cybercriminals-are-targeting-digital-identity-of-singapore-citizens)
- [MyInfo and Data Privacy — Privacy Ninja](https://www.privacy.com.sg/resources/myinfo-and-your-data-privacy/)
- [Users Should Scrutinise MyInfo Data Sharing — NTU Nanyang Business School](https://www.ntu.edu.sg/business/news-events/news/story-detail/users-need-to-scrutinise-what-data-is-shared-through-myinfo)
- [Personal Data Protection Act 2012 — Singapore Statutes Online](https://sso.agc.gov.sg/Act/PDPA2012)
- [Singapore National Digital Identity — Global DPI Network](https://www.dpi.global/globaldpi/singapore_sndi)
- [GitHub — singpass-myinfo-oidc-helper (GovTechSG)](https://github.com/GovTechSG/singpass-myinfo-oidc-helper)

---

*Document prepared by Feature Benchmark Analyser | UAE PASS DV — TDRA*
*Analysis date: 2026-02-26 | Review cycle: Quarterly or upon major MyInfo product update*
*Next review trigger: MyInfo v3 decommission (September 2026); UAE PASS Form Filler delivery milestone*
