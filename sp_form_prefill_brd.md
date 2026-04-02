# Business Requirements Document (BRD)
# SP Form Pre-Fill via Issuer Claims

| Field | Value |
|---|---|
| **Feature Name** | SP Form Pre-Fill via Issuer Claims |
| **Feature Code** | DV-PREFILL-2026 |
| **Version** | 1.0 |
| **Date** | 2026-04-01 |
| **Author** | Feature Benchmark Analyser |
| **Status** | Draft |
| **Stakeholders** | TDRA, DDA, ICP, MoHRE, DLD, Engineering (FE/BE/QA), Legal/Compliance, Service Providers |

---

## 1) Executive Summary

SP Form Pre-Fill via Issuer Claims enables UAE PASS Digital Documents (DV) to automatically populate SP onboarding and registration forms using verified, eSeal-authenticated data extracted from the user's government-issued documents — eliminating manual data entry and reducing SP KYC friction. The feature delivers a two-layer value proposition: (a) a visible-field pre-fill layer that improves user experience at onboarding touchpoints across banking, telecoms, insurance, and government, and (b) a hidden claims layer that provides SPs with issuer-signed data they cannot obtain through any other automated channel — effectively positioning UAE PASS DV as a verified data API, not merely a document wallet.

**Key Metrics Targets**

| Metric | Baseline | Target |
|---|---|---|
| SP onboarding form completion rate | _[TO BE FILLED]_ | +25% |
| Average onboarding form fill time | _[TO BE FILLED]_ | -60% |
| SP-reported KYC data quality error rate | _[TO BE FILLED]_ | -40% |
| SPs live with pre-fill capability | 0 | 6 (by end Phase 2) |
| Pilot SP live | None confirmed | 1 (gate for Phase 1 GA) |

---

## 2) Document Catalogue with Inferred Claims

All 66 documents currently live in UAE PASS DV are assessed below for pre-fill value. Claims listed are inferred from known document fields; structured payload availability is **unconfirmed** for all issuers and must be validated by DV Engineering in Phase 0.

### 2.1) Core Identity — HIGH Value

| Document Name | Issuer | Integration Type | Key Extractable Claims | Hidden Claims (inferred) | Pre-fill Value |
|---|---|---|---|---|---|
| Emirates ID | ICP | API / VP payload | Full name EN/AR, EID number, date of birth, gender, nationality, card expiry, photo | Pfile number, residency status code, sponsor relationship code | HIGH |
| Passport | ICP | API / VP payload | Full name EN, passport number, nationality, date of birth, gender, issue date, expiry date | _[TO BE CLARIFIED]_ | HIGH |
| Residence Visa | ICP | API / VP payload | Visa number, visa type, sponsor name, expiry date, profession/occupation label | Labour category code, entry permit number, sponsor entity type, port of entry | HIGH |

**Phase 1 universal attribute set (MVP):** Full name EN, EID number, date of birth, nationality, gender, visa expiry. These six fields are sufficient to satisfy SIM registration (TRA mandate) and core banking KYC fields.

### 2.2) Employment and Labour — HIGH Value

| Document Name | Issuer | Integration Type | Key Extractable Claims | Hidden Claims (inferred) | Pre-fill Value |
|---|---|---|---|---|---|
| Labour Card | MoHRE | API / VP payload | Employer name, job title, work permit number, work permit expiry | ISCO occupation code, WPS employer registration status, work permit category, establishment number | HIGH |
| Labour Contract | MoHRE | API / VP payload | Employer name, job title, contract type, contract start date | Salary (BLOCKED — TDRA gate) | MEDIUM-HIGH |
| Employee Work Contract (FAHR) | FAHR | API / VP payload | Federal employer name, job title, grade, contract start date | Salary (BLOCKED — TDRA gate) | MEDIUM |

**Note:** Salary is excluded from all phases. Labour Card fields (employer, title, work permit number) are viable without salary. FAHR covers federal government employees only.

### 2.3) Education and Academic — MEDIUM Value

| Document Name | Issuer | Integration Type | Key Extractable Claims | Hidden Claims (inferred) | Pre-fill Value |
|---|---|---|---|---|---|
| Degree Certificate | MoE / UAEU / HCT / ZU / MoHESR | VP payload | Institution name, degree type, field of study, graduation date, student name | _[TO BE CLARIFIED]_ | MEDIUM |
| Academic Attestation | MoE | VP payload | Degree confirmed, institution, country of origin degree | _[TO BE CLARIFIED]_ | MEDIUM |
| Academic Equivalency Certificate | MoHESR | VP payload | UAE equivalent qualification level, institution | _[TO BE CLARIFIED]_ | MEDIUM |
| Secondary School Certificate | MoE / Emirate MOEs | VP payload | School name, graduation year, stream | _[TO BE CLARIFIED]_ | LOW |
| EmSAT Score Certificate | MoE | VP payload | Subject scores, test date | _[TO BE CLARIFIED]_ | LOW |
| Academic Transcript | UAEU / HCT / ZU | VP payload | GPA, credits, academic standing | _[TO BE CLARIFIED]_ | LOW |

### 2.4) Property and Real Estate — MEDIUM Value (partial emirate coverage)

| Document Name | Issuer | Integration Type | Key Extractable Claims | Hidden Claims (inferred) | Pre-fill Value |
|---|---|---|---|---|---|
| Tenancy Contract (Dubai / EJARI) | DLD | API / VP payload | Full address, EJARI registration number, landlord name, annual rent, contract start/end dates | EJARI unified number, property type classification, MAKANI geocode | HIGH (Dubai only) |
| Tenancy Contract (Fujairah) | Fujairah Municipality | VP payload | Full address, contract dates, landlord details | _[TO BE CLARIFIED]_ | MEDIUM (Fujairah only) |
| Title Deed (DLD) | DLD | VP payload | Owner name, property address, area (sq ft), registration date | _[TO BE CLARIFIED]_ | MEDIUM |
| Title Deed (Ajman) | Ajman Land Department | VP payload | Owner name, property address, area | _[TO BE CLARIFIED]_ | MEDIUM |
| Title Deed (Sharjah) | Sharjah Real Estate | VP payload | Owner name, property address, area | _[TO BE CLARIFIED]_ | MEDIUM |

**Coverage note:** Tenancy Contract address pre-fill covers Dubai and Fujairah only (~37–41% of UAE residents). Abu Dhabi (Tawtheeq), Sharjah (RERA), Ajman, RAK, and UAQ are not onboarded. See Section 7 for full emirate coverage analysis and phasing.

### 2.5) Vehicle and Transport — MEDIUM Value

| Document Name | Issuer | Integration Type | Key Extractable Claims | Hidden Claims (inferred) | Pre-fill Value |
|---|---|---|---|---|---|
| Vehicle Registration / License | MoI / RTA | VP payload | Make, model, year, plate number, VIN, engine number, registration expiry, insurance expiry | _[TO BE CLARIFIED]_ | MEDIUM |
| Driving Licence | MoI / RTA | VP payload | Licence number, categories, expiry, date of birth, blood group (sensitive — DDA consent design required) | Traffic file number, traffic points balance at issuance, medical clearance date | MEDIUM |
| Pleasure Boat Licence | MoI | VP payload | Vessel details | _[TO BE CLARIFIED]_ | LOW |
| Small Boat Licence | MoI | VP payload | Vessel details | _[TO BE CLARIFIED]_ | LOW |

**Note on blood group:** Classified as sensitive. Requires prominent consent emphasis and DDA review before enabling as a pre-fill claim.

### 2.6) Health and Professional Licences — MEDIUM Value

| Document Name | Issuer | Integration Type | Key Extractable Claims | Hidden Claims (inferred) | Pre-fill Value |
|---|---|---|---|---|---|
| Medical Practitioner Licence (DHA) | DHA Dubai | VP payload | Speciality, licence number, expiry, practitioner name | _[TO BE CLARIFIED]_ | MEDIUM |
| Medical Practitioner Licence (DOH) | DOH Abu Dhabi | VP payload | Speciality, licence number, expiry, practitioner name | _[TO BE CLARIFIED]_ | MEDIUM |
| Health Insurance Card | HAAD / DHA / SEHA | VP payload | Policy number, insurer name, coverage type, expiry | _[TO BE CLARIFIED]_ | MEDIUM |
| People of Determination Card | MOFAIC / GDFCL | VP payload | Card holder name, determination category | Disability classification (PDPL-sensitive) | LOW (sensitive) |
| Covid Vaccination Card | MoHAP | VP payload | Vaccination dates, vaccine type | _[TO BE CLARIFIED]_ | LOW (post-pandemic relevance minimal) |

**Note on People of Determination Card:** Disability classification data is PDPL-sensitive. A separate DDA consent design is required before this document's claims can be used for pre-fill. Excluded from all MVP phases.

### 2.7) Legal and Civil Status — LOW-MEDIUM Value

| Document Name | Issuer | Integration Type | Key Extractable Claims | Hidden Claims (inferred) | Pre-fill Value |
|---|---|---|---|---|---|
| Marriage Certificate (MoJ) | MoJ | VP payload | Marital status signal, both parties' names, marriage date | _[TO BE CLARIFIED]_ | MEDIUM (insurance, banking relationship) |
| Marriage Certificate (ADJD) | ADJD | VP payload | Marital status signal, both parties' names | _[TO BE CLARIFIED]_ | MEDIUM |
| Marriage Certificate (RAK) | RAK Courts | VP payload | Marital status signal | _[TO BE CLARIFIED]_ | LOW |
| Divorce Certificate (MoJ) | MoJ | VP payload | Marital status signal (sensitive) | _[TO BE CLARIFIED]_ | LOW (sensitive) |
| Divorce Certificate (RAK) | RAK Courts | VP payload | Marital status signal (sensitive) | _[TO BE CLARIFIED]_ | LOW (sensitive) |
| Power of Attorney (MoJ) | MoJ | VP payload | Delegator name, delegate name, scope of authority | _[TO BE CLARIFIED]_ | MEDIUM (assisted channel/B2B) |
| Power of Attorney (ADJD) | ADJD | VP payload | Delegator name, delegate name | _[TO BE CLARIFIED]_ | MEDIUM |
| Police Clearance Certificate | MoI | VP payload | Status field (clear/flagged) | _[TO BE CLARIFIED]_ | LOW (TDRA policy instrument required) |
| Social Aid Card | MOFAIC / MoCD | VP payload | Beneficiary name | Financial vulnerability data (TDRA gate) | LOW (sensitive) |
| Productive Families Card | MoCD | VP payload | Beneficiary name, programme | Financial vulnerability data (TDRA gate) | LOW (sensitive) |

### 2.8) Business and Trade — MEDIUM Value

| Document Name | Issuer | Integration Type | Key Extractable Claims | Hidden Claims (inferred) | Pre-fill Value |
|---|---|---|---|---|---|
| Trade Licence (ADRA) | ADRA | VP payload | Business name EN/AR, licence number, activity, owner name, address, expiry | _[TO BE CLARIFIED]_ | HIGH (B2B onboarding) |
| Trade Licence (UAQ) | UAQ Municipality | VP payload | Business name EN/AR, licence number, activity, owner name, address, expiry | _[TO BE CLARIFIED]_ | HIGH (B2B onboarding) |
| Trade Licence (Fujairah) | Fujairah Municipality | VP payload | Business name EN/AR, licence number, activity, owner name, address, expiry | _[TO BE CLARIFIED]_ | HIGH (B2B onboarding) |
| Tax Residence Certificate | FTA | VP payload | TRN, country of tax residence, validity period | FATCA/CRS classification code | HIGH (investment platforms) |

### 2.9) Out of Scope — No Applicable Pre-Fill Claims

The following 9 documents are excluded from all pre-fill phases. Either the claims are non-attributable to a user identity form field, or the documents are decommissioned / instrument-only.

| Document | Issuer | Reason for Exclusion |
|---|---|---|
| CITES Import Certificate | MoCCE | Point-of-entry instrument; no personal attribute claims |
| Aircraft Maintenance Licence | GCAA | No applicable form field in consumer/SP onboarding |
| Air Traffic Controller Licence | GCAA | As above |
| Pilot Licence | GCAA | As above |
| Unmanned Aircraft Registration Certificate | GCAA | Decommissioned |
| MoJ Confession Document | MoJ | Transactional legal instrument; exclude from MVP |
| MoJ Contract Document | MoJ | Transactional legal instrument; exclude from MVP |
| ADJD Contract Document | ADJD | As above |
| _[Additional decommissioned/placeholder documents]_ | _[?]_ | _[TO BE CLARIFIED]_ |

---

## 3) Use Cases

### 3.1) Use Case Groups

| # | Use Case Group | Primary Documents | Applicable SP Sectors |
|---|---|---|---|
| 1 | SIM card registration (TRA-mandated KYC) | EID, Residence Visa | Telecoms (Etisalat, DU, Virgin, DU IGNITE) |
| 2 | Retail bank account opening | EID, Visa, Passport, Labour Card | Banking (Al Maryah, ADIB, ruya, FAB, CBD, Botim, Ziina, Lulu) |
| 3 | Investment / brokerage account opening | EID, Visa, Passport, Tax Residence Certificate | Investment (ADSS, Al Ramz, eToro, Baraka) |
| 4 | Motor insurance application | EID, Vehicle License, Driving Licence | Insurance (ADNIC Motor, GIG, Sukoon) |
| 5 | Health / life insurance application | EID, Visa, Labour Card | Insurance (Takaful Emarat, Orient, ADNIC) |
| 6 | Utility connection / move-in | EID, Tenancy Contract | Utilities (DEWA, ADDC, AADC) |
| 7 | Government service form pre-fill | EID, Visa, all relevant docs | Government portals, DED, RTA |
| 8 | Remittance / wallet KYC (CBUAE-mandated) | EID, Visa, Passport | Remittance (GCC Exchange, Hubpay, Al Ansari) |

### 3.2) Detailed Use Cases — Top 3

---

#### Use Case 1: SIM Registration Pre-Fill (Telecoms)

**User Persona:** UAE resident or citizen purchasing a new SIM card at a retail outlet or via an app.

**Problem today:** The customer must present physical EID, which the agent manually enters into TRA's SIM registration system. Errors are common; the process takes 3–7 minutes.

**User Story:**
As a UAE resident, I want my UAE PASS verified identity data to auto-populate the SIM registration form, so that I can complete SIM activation without manual data entry or document presentation.

**Pre-fill User Flow:**

1. User opens Etisalat / DU app or arrives at a retail kiosk.
2. SP app presents a "Fill with UAE PASS" / «أكمل بـ UAE PASS» button on the registration form.
3. User taps the button; the UAE PASS app opens (or a UAE PASS deep link is triggered).
4. UAE PASS DV displays the consent screen: "The following information will be shared with [SP Name]" / «سيتم مشاركة المعلومات التالية مع [اسم مزود الخدمة]».
5. Listed fields: Full name (EN), EID number, nationality, date of birth — each labelled "Verified by ICP" / «موثق من قِبل الهيئة الاتحادية للهوية».
6. User taps "Share" / «مشاركة» or "Decline" / «رفض».
7. On confirmation, a Verifiable Presentation is delivered to the SP backend via the existing DV sharing API.
8. SP form fields are auto-populated. A confirmation banner appears: "Your information was filled using verified UAE PASS data." / «تم ملء معلوماتك باستخدام بيانات موثقة من UAE PASS.»
9. User reviews and submits the form.

**Gate:** TRA field alignment required before any telecom SP can be onboarded for SIM registration pre-fill.

---

#### Use Case 2: Retail Bank Account Opening

**User Persona:** UAE expatriate applying for a current account or credit card digitally.

**Problem today:** Banks require document uploads (EID front/back, Visa, salary certificate, address proof). OCR-based extraction has high error rates; customers must re-upload rejected documents. Average digital onboarding takes 8–15 minutes.

**User Story:**
As a UAE resident, I want my bank account application form to be pre-filled with verified data from my Emirates ID, Residence Visa, and Labour Card, so that I can complete onboarding in under 3 minutes without uploading documents.

**Pre-fill User Flow:**

1. User opens the bank's app and selects "Open Account" or "Apply for Credit Card."
2. Bank app presents "Fill with UAE PASS" / «أكمل بـ UAE PASS» on the KYC data entry screen.
3. UAE PASS app opens; consent screen lists:
   - From Emirates ID: Name, EID number, date of birth, gender, nationality, EID expiry — "Verified by ICP"
   - From Residence Visa: Visa type, sponsor name, visa expiry, profession — "Verified by ICP"
   - From Labour Card: Employer name, job title, work permit number, work permit expiry — "Verified by MoHRE"
   - Address: EID registered address (Phase 1, caveated) OR Tenancy Contract address (Phase 2, Dubai/Fujairah)
4. User reviews fields, taps "Share" / «مشاركة».
5. Verifiable Presentation delivered to bank backend.
6. Form auto-populated. Bank's system validates eSeal provenance independently.
7. User reviews pre-filled form, corrects any fields that require updating, and submits.

**Phase dependency:** Labour Card fields are Phase 2. EID + Visa fields only in Phase 1.

---

#### Use Case 3: Government Service Form Pre-Fill (mGovernment / DED)

**User Persona:** UAE business owner applying for a trade licence renewal via DED Dubai portal or mGovernment.

**Problem today:** Applicant must re-enter business details, owner details, and address across multiple government forms — even when all data exists in their issued documents.

**User Story:**
As a UAE business owner, I want my trade licence and EID data to pre-fill DED renewal forms automatically, so that I can complete government service requests without re-entering data that authorities already hold.

**Pre-fill User Flow:**

1. Business owner accesses DED Dubai portal (or mGovernment app — candidate SP not yet onboarded).
2. Portal presents "Fill with UAE PASS" / «أكمل بـ UAE PASS» on the licence renewal form.
3. UAE PASS DV consent screen lists:
   - From Trade Licence (ADRA/UAQ/Fujairah): Business name EN/AR, licence number, activity, owner name, address, expiry
   - From Emirates ID: Owner name, EID number, nationality
4. User reviews and shares.
5. Form pre-filled. User makes any corrections and submits.

**Note:** DED Dubai and mGovernment are Tier 1 candidate SPs (not yet onboarded). This use case is the most commercially impactful but requires SP onboarding as a prerequisite.

---

## 4) Existing SP Use Case Mapping

The following table covers onboarded SPs as of 2026-04-01. Volume figures are monthly sharing interactions (from sharing request data). Priority reflects pre-fill onboarding priority, not overall SP commercial priority.

| SP Name | Sector | Vol/mo (est.) | Primary Documents for Pre-fill | Pre-fill Use Case | Pre-fill Priority |
|---|---|---|---|---|---|
| Etisalat Retail | Telecoms | 8,896 | EID, Visa | SIM registration: EID name, number, nationality | HIGH |
| Al Maryah | Banking | 7,383 | EID, Visa, Labour Card, Tenancy Contract | Account opening + credit KYC | HIGH |
| DU | Telecoms | 4,605 | EID, Visa | SIM registration | HIGH |
| Botim | Digital Wallet | 4,371 | EID | Wallet onboarding: identity fields | HIGH |
| ADIB | Banking | 3,997 | EID, Visa, Labour Card | Account + credit product KYC | HIGH |
| Etisalat Business | Telecoms (B2B) | 3,765 | Trade Licence, EID | B2B SIM: trade licence pre-fill | HIGH |
| ruya | Banking (Islamic) | _[TO BE FILLED]_ | EID, Visa, Labour Card | Account opening KYC | MEDIUM-HIGH |
| FAB | Banking | _[TO BE FILLED]_ | EID, Visa, Passport | Retail + credit KYC | MEDIUM-HIGH |
| Ziina | Fintech / Wallet | _[TO BE FILLED]_ | EID | Wallet onboarding | MEDIUM |
| CBD | Banking | _[TO BE FILLED]_ | EID, Visa, Labour Card | Account + credit KYC | MEDIUM |
| CBD Assisted | Banking (Assisted Channel) | _[TO BE FILLED]_ | EID, Visa | Agent-assisted onboarding (separate consent UX required) | MEDIUM — DDA flag |
| Lulu Financial | Fintech / Retail Banking | _[TO BE FILLED]_ | EID, Visa | Account opening | MEDIUM |
| ADNIC Motor | Insurance | _[TO BE FILLED]_ | EID, Vehicle License | Motor insurance KYC; vehicle pre-fill | HIGH |
| GIG Insurance | Insurance | _[TO BE FILLED]_ | EID, Visa, Labour Card | Health / life insurance KYC | MEDIUM |
| ADNIC | Insurance (Health) | _[TO BE FILLED]_ | EID, Visa, Labour Card | Health insurance KYC | MEDIUM |
| Sukoon | Insurance | _[TO BE FILLED]_ | EID | General insurance KYC | MEDIUM |
| ADSS | Investment | _[TO BE FILLED]_ | EID, Passport, TRC | FATCA/CRS account opening | HIGH |
| Al Ramz | Investment | _[TO BE FILLED]_ | EID, Passport, TRC | Securities account opening | HIGH |
| eToro | Investment (International) | _[TO BE FILLED]_ | EID, Passport, TRC | FATCA/CRS; cross-border KYC | HIGH |
| Baraka | Investment (Digital) | _[TO BE FILLED]_ | EID, Passport, TRC | Zero-paper account opening | HIGH |
| GCC Exchange | Remittance | _[TO BE FILLED]_ | EID, Visa, Passport | CBUAE KYC mandate — compliance as feature | HIGH |
| Hubpay | Remittance / Wallet | _[TO BE FILLED]_ | EID, Visa, Passport | CBUAE KYC compliance | HIGH |
| Virgin Mobile | Telecoms | _[TO BE FILLED]_ | EID, Visa | SIM registration | MEDIUM |
| DU IGNITE | Telecoms | _[TO BE FILLED]_ | EID, Visa | SIM registration | MEDIUM |
| Etisalat Direct | Telecoms | _[TO BE FILLED]_ | EID, Visa | SIM registration | MEDIUM |

_Note: 29 additional onboarded SPs are not individually listed as volume data was unavailable at time of analysis. Full 54-SP list should be extracted from the Jira SP onboarding registry and appended as an annex._

**Sector patterns:**
- **Telecoms:** Simplest use case (EID fields only); requires TRA field alignment before any pre-fill onboarding.
- **Banking — retail:** Labour Card is the high-value add-on beyond EID/Visa; address is secondary (Phase 2 dependency).
- **Investment:** Tax Residence Certificate (TRC) is the specialist high-value claim for FATCA/CRS automation.
- **Insurance:** Vehicle License is the specialist claim for motor; Labour Card for health/life.
- **Remittance:** CBUAE KYC mandate creates a compliance imperative — pre-fill is a regulatory enabler.
- **Assisted channel (CBD Assisted):** Requires a separate consent UX where the customer consents and the agent views the data. Flag to DDA as a distinct screen design requirement.

---

## 5) New Candidate SPs (Not Yet Onboarded)

The following 15 SPs are not yet onboarded to UAE PASS DV but represent high-value targets for pre-fill commercialisation. Their onboarding would unlock new sectors (utilities, government, e-commerce) and new document categories (Trade Licence, Tenancy Contract, Vehicle License at scale).

| SP / Sector | Use Case | Primary Documents | Value Rating |
|---|---|---|---|
| DED Dubai / Government — Business | Trade licence renewal pre-fill; owner KYC for new licence applications | Trade Licence, EID | VERY HIGH |
| Emirates NBD (main app) / Banking | Full digital account opening; credit card application | EID, Visa, Passport, Labour Card | VERY HIGH |
| mGovernment portals / Government | Universal government form pre-fill across all federal services | Full catalogue | VERY HIGH |
| RTA Dubai / Government — Transport | Vehicle registration renewal; driving licence renewal | EID, Vehicle License, Driving Licence | HIGH |
| DOH Abu Dhabi / Healthcare Regulation | Medical practitioner licence renewal pre-fill | Medical Practitioner Licence, EID | HIGH |
| DHA Dubai / Healthcare Regulation | Medical practitioner licence renewal; healthcare worker onboarding | Medical Practitioner Licence, EID | HIGH |
| DEWA / Utilities | New utility connection; move-in address verification | EID, Tenancy Contract | HIGH |
| ADDC / AADC / Utilities | New utility connection; move-in for Abu Dhabi residents | EID, Tenancy Contract | HIGH |
| Takaful Emarat / Insurance | Life and health insurance KYC | EID, Visa, Labour Card | HIGH |
| Orient Insurance / Insurance | Home and motor insurance KYC; address and vehicle pre-fill | Tenancy Contract, Vehicle License, EID | HIGH |
| Mashreq Bank / Banking | Digital account opening; SME banking | EID, Visa, Passport, Labour Card | HIGH |
| Al Ansari Exchange / Remittance | CBUAE KYC compliance; transfer limit verification | EID, Visa, Passport | HIGH |
| Zand Bank / Banking (Digital) | Zero-paper account opening; SME onboarding | EID, Visa, Labour Card, Trade Licence | MEDIUM-HIGH |
| MAF / Carrefour — Retail / Loyalty | Loyalty programme enrolment; age verification | EID (date of birth, name) | MEDIUM |
| Noon / Talabat / E-commerce | Account creation; delivery address pre-fill | EID, Tenancy Contract | MEDIUM |

**Untapped B2B/SME segment:** The current onboarded SP list is entirely consumer-facing. Trade Licences (ADRA, UAQ, Fujairah) are live in DV with no SME-oriented SPs onboarded. DED Dubai, DEWA (business accounts), and Zand Bank (SME) represent an entirely new SP segment that would significantly broaden the DV commercial footprint.

**Recommended pilot outreach (immediate):**
- One telecom: Etisalat Retail (highest volume; simplest use case — EID fields only)
- One bank: Al Maryah or ADIB (highest banking volume; broadest document use case)

---

## 6) Hidden Claims — Strategic Opportunity

### 6.1) What Hidden Claims Are

Hidden claims are fields included in the structured payload of an issuer-signed document that are **not rendered on the visible document face** in UAE PASS DV. They carry full eSeal provenance — identical cryptographic trust to visible fields — but are invisible to the user during normal document browsing. They exist within the Verifiable Presentation payload but are currently unexposed to either users or SPs.

### 6.2) Why They Are Strategically Significant

Hidden claims shift the feature value proposition from "user convenience for form-filling" to "verified data API for service providers." SPs gain access to issuer-signed data they cannot currently obtain through any automated channel — not from document inspection, not from user self-declaration, and not from third-party data bureaus. This is data that only the issuing authority holds, now shareable with SP consent and user consent, with full eSeal provenance. This repositions UAE PASS DV from a document wallet to a sovereign verified data infrastructure.

### 6.3) The Three Most Commercially Powerful Hidden Claims

| Claim | Source Document | SP Use Case | Commercial Impact |
|---|---|---|---|
| WPS employer registration status | Labour Card (MoHRE) | Credit scoring proxy — banks use WPS-registered employer as income verification signal when salary cannot be shared. Replaces paper salary certificate in loan underwriting. | VERY HIGH — banking sector; credit product underwriting |
| ISCO occupation code | Labour Card (MoHRE) | Enables income band estimation by occupation category. Used in insurance pricing, credit underwriting, and banking risk classification without salary disclosure. | HIGH — banking + insurance |
| EJARI unified number | Tenancy Contract (DLD) | Enables utility providers (DEWA) and insurers to verify address and property classification at connection/application without manual document submission. | HIGH — utilities + insurance |

**Additional high-value hidden claims:**

| Claim | Source Document | SP Use Case |
|---|---|---|
| Residency status code | Emirates ID (ICP) | Banking risk tier; government eligibility |
| Labour category / skill level code | Residence Visa (ICP) | Employment verification; banking credit products; fraud detection |
| Entry permit number | Residence Visa (ICP) | Cross-referencing for employment and immigration compliance |
| FATCA/CRS classification code | Tax Residence Certificate (FTA) | Investment platform compliance automation — eliminates paper W-8/W-9 equivalent process |
| Traffic file number | Driving Licence | Motor insurance underwriting |
| Traffic points balance at issuance | Driving Licence | Motor insurance risk rating |
| MAKANI number / property geocode | Tenancy Contract (DLD) | Address geocoding for utilities, insurance, delivery |
| Sponsor entity type | Residence Visa | Banking risk classification (individual vs corporate sponsor) |

### 6.4) Why This Requires a Separate TDRA Policy Conversation

Each hidden claim category represents a new data access instrument. TDRA's current sharing policy covers document-level sharing (the whole document). Attribute-level sharing of non-visible fields — especially those that function as financial signals (WPS status, ISCO code) — requires:

1. A formal TDRA policy instrument per claim category, specifying which SP sectors may access which claims.
2. Issuer schema disclosure agreements (MoHRE, ICP, FTA must confirm which fields exist in their signed payloads).
3. A legal/PDPL review for each claim category, particularly for financial and occupational data.
4. A new DDA-approved consent UX pattern (see 6.5 below).

**Recommendation:** Present hidden claims to TDRA as a SEPARATE strategic initiative, distinct from the Form Pre-Fill feature. Frame it as a new product category — Verified Data API / B2G data infrastructure — that may warrant its own roadmap item and commercial model. Do not bundle into Form Pre-Fill MVP or Phase 1/2.

### 6.5) New Consent UX Requirement for Hidden Claims

The standard document-share consent screen (which shows the document name and visible fields) does NOT cover non-visible data. Sharing hidden claims without explicit, informed consent likely violates PDPL Article 4 (lawfulness and transparency of processing).

Required UX elements for hidden claims consent:
- The consent screen must surface hidden fields explicitly, under a distinct section labelled "Additional verified information from this document" / «معلومات موثقة إضافية من هذا المستند:»
- Each hidden field must be labelled "Not shown on document face — verified by [Issuer]" / «غير ظاهر على وجه المستند — موثق من قِبل [الجهة]»
- An explanatory line must read: "This information comes from your document's issuer and is not visible in your UAE PASS Documents view." / «هذه المعلومات صادرة عن جهة إصدار مستندك ولا تظهر في عرض مستنداتك في UAE PASS.»
- eSeal provenance chain must accompany every hidden claim in the Verifiable Presentation (source issuer + document version + signing timestamp).
- DDA must design this as a new consent screen primitive — it cannot be adapted from the existing document-share consent screen.

### 6.6) Architecture Implications

**Path A — Payload-inclusive (fastest):** Hidden claims already exist in the Verifiable Presentation payload SPs receive today. SPs extract them from the existing payload with schema disclosure. No new DV API required. Requires: issuer schema disclosure, TDRA policy per claim, updated consent screen, SP API migration to consume new fields.

**Path B — Attribute extraction API (correct long-term architecture):** New DV backend endpoint extracts named hidden claims from issuer payloads on demand and returns structured JSON with eSeal provenance reference. Requires: full API design, security review, TDRA approval, SP API migration. This is the correct architecture for a productised Verified Data API.

**Critical action:** DV Engineering must inspect existing Verifiable Presentation payloads to determine whether Path A applies. This is hours of work, not weeks, and determines the entire architecture and timeline of the hidden claims initiative.

---

## 7) Address Pre-Fill — Emirates Coverage

### 7.1) Coverage by Emirate

| Emirate | Tenancy Contract in DV | Issuer | Pre-fill Status |
|---|---|---|---|
| Dubai | Yes | DLD / EJARI | Available — Phase 2 (pending DLD structured payload confirmation) |
| Fujairah | Yes | Fujairah Municipality | Available — Phase 2 (pending payload confirmation) |
| Abu Dhabi | No | Tawtheeq (not onboarded) | Not available — future issuer onboarding workstream |
| Sharjah | No | Sharjah RERA (not onboarded) | Not available — future issuer onboarding workstream |
| Ajman | No | Ajman (not onboarded) | Not available |
| Ras Al Khaimah | No | RAK (not onboarded) | Not available |
| Umm Al Quwain | No | UAQ (not onboarded) | Not available |

**Addressable population via Tenancy Contract:** ~37–41% of UAE residents (Dubai-heavy). Practical reach is lower due to DV document penetration gaps.

### 7.2) Phased Address Pre-Fill Approach

**Phase 1 — EID Registered Address (Nationwide, Best-Effort)**
Source: Emirates ID (ICP). Nationwide coverage; all UAE residents and citizens.
Limitation: The ICP-registered address reflects the address at the time of EID issuance. It may not reflect current residence, particularly for residents who have moved since their last EID renewal.
Display with mandatory caveat label (see EN/AR copy below).

**Phase 2 — Tenancy Contract Address Overlay (Dubai + Fujairah)**
Where a valid Tenancy Contract exists in the user's DV, offer the Tenancy Contract address as a higher-confidence alternative. Present both options; let the user select the more current address.
Prerequisite: DLD structured payload confirmation (Phase 0 gate).

**Future — Tawtheeq (Abu Dhabi) and Sharjah RERA**
Onboarding Tawtheeq and Sharjah RERA as DV issuers is a separate workstream, not within the Form Pre-Fill feature scope. Recommend flagging to TDRA as a future issuer expansion priority.

### 7.3) Address Caveat Label — Bilingual Copy

| Context | English | Arabic |
|---|---|---|
| Phase 1 address field label | Address on file with ICP (may not reflect current residence) | «العنوان المسجل لدى الهيئة الاتحادية للهوية (قد لا يعكس محل إقامتك الحالي)» |
| Phase 2 Tenancy Contract address label | Residential address — verified by [DLD / Fujairah Municipality] | «عنوان الإقامة — موثق من قِبل [هيئة الأراضي والأملاك / بلدية الفجيرة]» |
| Address auto-fill failure | Your residential address could not be filled automatically. Please enter it manually. | «تعذّر ملء عنوان إقامتك تلقائيًا. يُرجى إدخاله يدويًا.» |

---

## 8) Scope

### 8.1) In Scope — Phase 1 (MVP)

- Pre-fill of visible Emirates ID fields: full name EN, EID number, date of birth, gender, nationality, EID expiry.
- Pre-fill of visible Residence Visa fields: visa type, sponsor name, visa expiry, profession label.
- Pre-fill of EID registered address with caveat label.
- "Fill with UAE PASS" / «أكمل بـ UAE PASS» button integration pattern (SP-side trigger).
- Consent screen listing individual fields with issuer attribution (DDA design required).
- Verifiable Presentation delivery to SP backend via existing DV sharing API (document-level; no new API).
- SP-side confirmation banner after successful pre-fill.
- Bilingual consent screen and field labels (EN/AR, RTL).
- Phase 1 pilot with 1 confirmed telecom SP and 1 confirmed banking SP.
- Firebase Remote Config feature flag for phased rollout.

### 8.2) In Scope — Phase 2

- Pre-fill of Labour Card visible fields: employer name, job title, work permit number, work permit expiry.
- Pre-fill of Tenancy Contract address (Dubai/Fujairah) as optional overlay — user selects which address to use.
- Vehicle License pre-fill: make, model, plate number, registration expiry, insurance expiry.
- Driving Licence pre-fill: licence number, categories, expiry (blood group excluded from auto-pre-fill; requires DDA separate consent design).
- Tax Residence Certificate pre-fill: TRN, country of tax residence, validity period.
- Trade Licence pre-fill (ADRA, UAQ, Fujairah) for B2B/SME SP segment.
- Expansion to additional SPs post-pilot: target 6 SPs live by Phase 2 GA.
- Assisted channel consent UX (CBD Assisted pattern, DDA design).

### 8.3) Out of Scope / Future

- Salary field (all documents) — BLOCKED until TDRA policy instrument confirmed. No timeline.
- Police Clearance Certificate status — requires separate TDRA policy instrument. No timeline.
- Social Aid Card / Productive Families Card financial data — TDRA gate required. No timeline.
- People of Determination Card disability classification — PDPL-sensitive; requires separate PDPL assessment and DDA consent design. No timeline.
- Blood group (Driving Licence) — sensitive; separate DDA consent design required. Phase 3 at earliest.
- Hidden claims / Verified Data API — separate strategic initiative (Phase 3 / separate roadmap item).
- Tawtheeq (Abu Dhabi), Sharjah RERA, Ajman, RAK, UAQ address pre-fill — future issuer onboarding workstream.
- Attribute-level selective disclosure (sharing individual fields without sharing the full document) — architectural extension; not in current DV API model.
- Real-time data freshness checking (querying issuer APIs at pre-fill time to refresh data) — future enhancement.
- Academic certificate pre-fill — insufficient SP demand in onboarding context to justify Phase 1/2 scoping.
- Marriage / Divorce certificate pre-fill — sensitive; low commercial SP demand; flagged for future review.

---

## 9) Functional Requirements

| ID | Requirement | Priority | Notes |
|---|---|---|---|
| FR-01 | The SP must be able to trigger a pre-fill request by presenting a "Fill with UAE PASS" entry point in their application UI. | Must Have | SP-side implementation; DDA must approve button specification. |
| FR-02 | The UAE PASS app must display a consent screen listing each individual field to be shared, the issuer source for each field, and the requesting SP name. | Must Have | New screen; DDA design approval required. |
| FR-03 | The consent screen must include both "Share" and "Decline" actions; sharing must not proceed without affirmative user action. | Must Have | Consent model; no pre-selected or default-share state. |
| FR-04 | All consent screen copy must render in both English and Arabic, with correct RTL layout in Arabic mode. | Must Have | Bilingual requirement; follow CLAUDE.md Arabic guidelines. |
| FR-05 | Upon user consent, a Verifiable Presentation containing the consented fields must be delivered to the SP backend via the existing DV sharing API. | Must Have | No new backend API required for Phase 1; uses existing VP delivery. |
| FR-06 | The Verifiable Presentation must include the eSeal provenance chain for each field: source document, issuer identity, signing timestamp. | Must Have | Security requirement; do not strip eSeal metadata. |
| FR-07 | The SP app must display a confirmation to the user that fields have been pre-filled with verified UAE PASS data. | Must Have | Post-fill UX confirmation; EN/AR copy required. |
| FR-08 | Pre-filled fields must remain editable by the user before form submission. | Must Have | User may have more current data; pre-fill is not binding. |
| FR-09 | If a field cannot be pre-filled (document not in DV, payload not available, user declines), the SP form must fall back to manual entry for that field only. | Must Have | Graceful degradation; partial pre-fill is acceptable. |
| FR-10 | The address field (Phase 1) must be accompanied by a caveat label indicating the address may not reflect current residence. | Must Have | ICP address limitation; DDA must approve caveat label design. |
| FR-11 | The sharing request must use a unique correlation ID per pre-fill session (SP-generated, time-boxed, one-time use). | Must Have | QR hygiene requirement; existing DV constraint. |
| FR-12 | No personally identifiable information must be included in the correlation ID, QR code, or deep link parameter. | Must Have | Privacy by design; existing DV QR hygiene rule. |
| FR-13 | The pre-fill feature must be controlled by a Firebase Remote Config feature flag to enable phased rollout and SP-specific enablement. | Must Have | Phased rollout control; aligns with existing Firebase pattern. |
| FR-14 | Phase 2: The consent screen must present Tenancy Contract address alongside EID address when both are available, allowing the user to select which to share. | Should Have | User agency for address source selection. |
| FR-15 | Phase 2: Labour Card fields (employer, title, work permit number, expiry) must be available as an additional consent section separate from EID/Visa fields. | Should Have | Document-level grouping in consent screen; user can decline Labour Card while sharing EID. |
| FR-16 | The SP must be able to specify which documents or fields they are requesting in their pre-fill trigger, so users only see relevant fields. | Should Have | Reduces consent screen noise; requires SP-side field specification in API request. |
| FR-17 | Phase 3 / separate initiative: The consent screen must present hidden claims in a distinct section labelled as not visible on the document face. | Could Have | Requires TDRA policy instrument and DDA new consent pattern before implementation. |
| FR-18 | The assisted channel consent pattern (agent-assisted KYC) must display consent to the customer, not the agent, and must not expose PII to the agent's screen without customer authorisation. | Could Have | CBD Assisted use case; distinct DDA screen design required. |

---

## 10) Non-Functional Requirements

| ID | Requirement | Target | Notes |
|---|---|---|---|
| NFR-01 | Performance — consent screen load time | < 2 seconds from SP trigger to consent screen displayed | Measured on 4G connection; median device |
| NFR-02 | Performance — VP delivery to SP backend | < 3 seconds from user consent to SP form populated | End-to-end; includes VP generation and SP API acknowledgement |
| NFR-03 | Availability | 99.9% uptime for pre-fill API endpoints | Aligned with existing DV sharing API SLA |
| NFR-04 | eSeal validation | 100% of VPs delivered must include valid eSeal metadata | SP may independently validate; no eSeal-less delivery permitted |
| NFR-05 | Encryption | All data in transit must use TLS 1.2+ with certificate pinning | Existing DV SP integration requirement |
| NFR-06 | Session security | Pre-fill sessions must expire after 5 minutes if user does not act | Prevent stale consent screens being reused |
| NFR-07 | Accessibility | Consent screen must meet WCAG 2.1 AA | Including screen reader support for EN and AR |
| NFR-08 | RTL rendering | All Arabic UI elements must pass RTL layout QA on iOS and Android | Including field labels, caveat text, buttons |
| NFR-09 | Offline behaviour | If user device has no connectivity at consent time, display error state and prompt user to retry | Do not silently fail or cache stale consent |
| NFR-10 | Audit logging | All pre-fill sharing events must be logged with: SP ID, correlation ID, documents shared, fields shared, timestamp | Feeds into Status-Based Reporting infrastructure (Sprint 70 dependency) |
| NFR-11 | PDPL compliance | PII handling must comply with UAE PDPL; consent records must be retained per TDRA retention policy | Legal/Compliance review required before Phase 1 GA |
| NFR-12 | ICP eSeal transition compatibility | Pre-fill attribute scope must be validated against ICP's new self-signing HSM certificates before Phase 1 GA | ICP eSeal Transition initiative in progress; coordinate with ICP team |

---

## 11) Bilingual Requirements

All user-facing copy must be provided in English and Arabic. Arabic must follow RTL formatting, Arabic numeral conventions where applicable, and the pluralisation rules in CLAUDE.md. DDA must approve all final copy pairs.

### 11.1) Consent Screen Copy

| Context | English | Arabic |
|---|---|---|
| Consent screen title | The following information will be shared with [SP Name]: | «سيتم مشاركة المعلومات التالية مع [اسم مزود الخدمة]:» |
| Field section header (EID) | From your Emirates ID | «من بطاقة هويتك الإماراتية» |
| Field section header (Visa) | From your Residence Visa | «من تصريح إقامتك» |
| Field section header (Labour Card) | From your Labour Card | «من بطاقة عملك» |
| Field section header (Tenancy Contract) | From your Tenancy Contract | «من عقد الإيجار الخاص بك» |
| Field source attribution | Verified by [Issuer Name] | «موثق من قِبل [اسم الجهة المُصدِرة]» |
| Requested fields label | Requested fields | «الحقول المطلوبة» |
| Source label | Source | «المصدر» |
| Primary action button | Share | «مشاركة» |
| Secondary action button | Decline | «رفض» |
| Manual entry fallback link | Enter manually instead | «الإدخال اليدوي بدلاً من ذلك» |

### 11.2) Pre-Fill Trigger (SP-Side, UAE PASS Branding Guidelines Apply)

| Context | English | Arabic |
|---|---|---|
| Pre-fill button label | Fill with UAE PASS | «أكمل بـ UAE PASS» |
| Button sublabel (optional) | Auto-fill your details instantly | «أكمل بياناتك فوراً» |

### 11.3) Post-Fill Confirmation Banner

| Context | English | Arabic |
|---|---|---|
| Success banner | Your information was filled using verified UAE PASS data. | «تم ملء معلوماتك باستخدام بيانات موثقة من UAE PASS.» |
| Partial fill notice | Some fields could not be filled automatically. Please complete them manually. | «تعذّر ملء بعض الحقول تلقائيًا. يُرجى إكمالها يدويًا.» |
| Single field failure | This field could not be filled automatically. Please enter it manually. | «تعذّر ملء هذا الحقل تلقائيًا. يُرجى إدخاله يدويًا.» |

### 11.4) Field Labels

| English | Arabic |
|---|---|
| Full name | «الاسم الكامل» |
| Emirates ID number | «رقم الهوية الإماراتية» |
| Date of birth | «تاريخ الميلاد» |
| Nationality | «الجنسية» |
| Gender | «الجنس» |
| Card expiry date | «تاريخ انتهاء صلاحية البطاقة» |
| Passport number | «رقم جواز السفر» |
| Visa type | «نوع التأشيرة» |
| Visa expiry date | «تاريخ انتهاء صلاحية التأشيرة» |
| Sponsor name | «اسم الكفيل» |
| Employer name | «اسم صاحب العمل» |
| Job title | «المسمى الوظيفي» |
| Work permit number | «رقم تصريح العمل» |
| Address | «العنوان» |

### 11.5) Address Caveat Labels

| Context | English | Arabic |
|---|---|---|
| EID address caveat | Address on file with ICP (may not reflect current residence) | «العنوان المسجل لدى الهيئة الاتحادية للهوية (قد لا يعكس محل إقامتك الحالي)» |
| Tenancy Contract address label | Residential address — verified by [Issuer] | «عنوان الإقامة — موثق من قِبل [الجهة]» |
| Address fill failure | Your residential address could not be filled automatically. Please enter it manually. | «تعذّر ملء عنوان إقامتك تلقائيًا. يُرجى إدخاله يدويًا.» |

### 11.6) Hidden Claims Consent (Phase 3 / Separate Initiative)

| Context | English | Arabic |
|---|---|---|
| Hidden claims section header | Additional verified information from this document: | «معلومات موثقة إضافية من هذا المستند:» |
| Hidden field provenance label | Not shown on document face — verified by [Issuer] | «غير ظاهر على وجه المستند — موثق من قِبل [الجهة]» |
| Hidden claims explanatory line | This information comes from your document's issuer and is not visible in your UAE PASS Documents view. | «هذه المعلومات صادرة عن جهة إصدار مستندك ولا تظهر في عرض مستنداتك في UAE PASS.» |

---

## 12) Dependencies

### 12.1) Internal Dependencies

| Dependency | Owner | Status | Phase |
|---|---|---|---|
| DDA design approval — consent screen (individual field listing with issuer attribution) | DDA | Not started | Phase 0 → gates Phase 1 |
| DDA design approval — "Fill with UAE PASS" button specification and SP implementation guide | DDA | Not started | Phase 0 → gates Phase 1 |
| DDA design approval — address caveat label UI pattern | DDA | Not started | Phase 0 → gates Phase 1 |
| DDA design approval — Tenancy Contract address selector (user chooses between EID and Tenancy Contract address) | DDA | Not started | Phase 2 |
| DDA design approval — assisted channel consent pattern (CBD Assisted) | DDA | Not started | Phase 2 |
| DDA design approval — hidden claims consent screen primitive | DDA | Not started | Phase 3 / Separate |
| TDRA attribute access policy — which SP sectors may access which EID/Visa attributes | TDRA | _[TO BE CLARIFIED]_ | Phase 0 → gates Phase 1 |
| TDRA attribute access policy — employment fields (Labour Card: employer, title, permit) | TDRA | _[TO BE CLARIFIED]_ | Phase 0 → gates Phase 2 |
| TDRA attribute access policy — address fields (Tenancy Contract, EID registered address) | TDRA | _[TO BE CLARIFIED]_ | Phase 0 → gates Phase 2 |
| TDRA attribute access policy — hidden claims (separate instrument per claim category) | TDRA | Not started | Phase 3 / Separate |
| Engineering — structured payload audit of all existing VP payloads | DV Engineering (BE) | Not started | Phase 0 (urgent) |
| Engineering — consent screen FE implementation | DV Engineering (FE) | Not started | Phase 1 |
| Engineering — VP field extraction service (BE) | DV Engineering (BE) | Not started | Phase 1 |
| Engineering — SP integration guide update and API documentation | DV Engineering + SP Relations | Not started | Phase 1 |
| Status-Based Reporting data layer (Sprint 70) | DV Engineering | In progress (Sprint 70) | Required for audit logging (NFR-10) |
| Firebase Remote Config — feature flag setup for pre-fill | DV Engineering | Not started | Phase 1 |
| ICP eSeal Transition compatibility check | ICP + DV Engineering | In progress | Must complete before Phase 1 GA |
| Legal/Compliance — PDPL review for attribute-level sharing | Legal | Not started | Phase 0 → gates Phase 1 GA |

### 12.2) External Dependencies

| Dependency | External Party | Status | Phase |
|---|---|---|---|
| ICP — confirmation of structured field payload availability in VP (EID, Visa, Passport) | ICP | Unconfirmed | Phase 0 (critical gate) |
| ICP — formal publication of attribute schema for EID, Visa, Passport fields | ICP | Not started | Phase 0 → gates Phase 1 |
| ICP — hidden claims schema disclosure (Pfile number, residency status code, sponsor relationship code) | ICP | Not started | Phase 3 / Separate |
| MoHRE — confirmation of structured Labour Card payload availability in VP | MoHRE | Unconfirmed | Phase 0 (critical gate for Phase 2) |
| MoHRE — hidden claims schema disclosure (ISCO code, WPS status, establishment number) | MoHRE | Not started | Phase 3 / Separate |
| DLD — confirmation of structured Tenancy Contract payload availability in VP | DLD | Unconfirmed | Phase 0 (critical gate for Phase 2) |
| DLD — hidden claims schema disclosure (EJARI unified number, MAKANI) | DLD | Not started | Phase 3 / Separate |
| FTA — Tax Residence Certificate structured payload confirmation | FTA | Unconfirmed | Phase 2 gate |
| TRA — field alignment for SIM registration pre-fill (which EID/Visa fields satisfy TRA KYC mandate) | TRA (Telecom Regulator) | Not started | Phase 1 gate for telecom SPs |
| Etisalat Retail — pilot SP confirmation and integration commitment | Etisalat | Not started (outreach required) | Phase 1 gate |
| Al Maryah / ADIB — pilot SP confirmation and integration commitment | Al Maryah / ADIB | Not started (outreach required) | Phase 1 gate |

---

## 13) Risks and Mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Structured data payload unconfirmed for all issuers — entire feature may be limited to PDF-only documents with no extractable fields | High | Critical | Phase 0 Engineering audit of existing VP payloads is the fastest resolution path (hours). If payloads are PDF-only, the feature scope collapses to Phase 3 (new attribute extraction API), significantly extending timeline. |
| ICP declines to publish formal attribute schemas or rejects third-party attribute sharing model | Medium | Critical | Escalate to TDRA immediately if ICP raises objections — TDRA is the regulatory authority over ICP for this purpose. Do not allow ICP technical hesitance to block product without TDRA arbitration. |
| Salary claim remains permanently blocked — reduces banking SP enthusiasm for Labour Card integration | Low (for Phase 1/2) | Medium | Reframe Labour Card value proposition around employer identity, WPS registration status, and work permit validity — all bankable signals without salary. Maintain salary as a future item pending TDRA decision. |
| Tenancy Contract address coverage gap (62–63% of residents in non-Dubai/Fujairah emirates have no Tenancy Contract in DV) — SPs in Abu Dhabi-heavy user bases may see low pre-fill success for address | High | Medium | Phase 1 EID registered address provides nationwide fallback. Manage SP expectations with pre-fill success rate estimates by emirate before onboarding. Escalate Tawtheeq onboarding as separate issuer workstream. |
| No pilot SP confirmed by Phase 0 gate — Phase 1 sprint work cannot begin without a committed SP integration partner | High | High | PM must initiate outreach to Etisalat Retail and Al Maryah/ADIB immediately. A letter of intent or verbal commitment is sufficient to begin Phase 1 sprint planning. |
| User trust deficit for consent screen — users may decline pre-fill if consent screen is unclear or looks like data exfiltration | Medium | Medium | DDA consent screen design is critical path. Run usability testing with 5–10 users before Phase 1 GA. Ensure "Decline" is always prominent; never default to sharing. |
| Hidden claims consent violates PDPL if deployed without explicit per-field consent | High (if not addressed) | Critical | Hidden claims are scoped to Phase 3 / Separate initiative with mandatory PDPL review as a gate. Do not ship any hidden claims disclosure in Phase 1 or 2 VP payloads to SPs. |
| ICP eSeal Transition (HSM migration) breaks eSeal validation for pre-fill VPs | Low | High | Coordinate with ICP team to ensure new HSM certificates are distributed to SP eSeal validation endpoints before Phase 1 GA. Add as explicit Phase 1 gate item. |
| SP API migration burden reduces SP adoption — existing SP integrations do not expect attribute-level field metadata in VP | Medium | Medium | Provide SP integration guide and testing sandbox. Offer SP engineering support for Phase 1 pilot. Phase 1 uses existing document-level VP delivery — no new API format. |
| Assisted channel consent (CBD Assisted) creates a regulatory grey area — agent sees customer data | Medium | Medium | Exclude assisted channel from Phase 1. Flag to TDRA and DDA explicitly. Design separate consent flow for Phase 2 with full DDA approval. |
| Bilingual parity gaps cause UX inconsistency — Arabic copy approved later than English | Low | Low | Require EN/AR copy pairs to be approved by DDA simultaneously. Arabic copy should not be a post-launch localisation task. |

---

## 14) Phase 0 Discovery Gate

Phase 1 sprint work cannot begin until the following five questions are answered. Each has a designated owner and urgency level.

| # | Open Question | Owner | Urgency | Resolution Path |
|---|---|---|---|---|
| 1 | Do existing Verifiable Presentation payloads for ICP documents (EID, Visa, Passport) contain structured field data, or PDF-only content? | DV Engineering (BE) | CRITICAL — hours of work | Inspect existing VP payloads against a sample of live ICP-issued VPs. Answer within 5 business days. |
| 2 | Has TDRA confirmed that attribute-level sharing of EID and Visa visible fields with commercial SPs is authorised under the current sharing policy? If not, what policy instrument is needed? | PM → TDRA | CRITICAL | Schedule TDRA product alignment meeting. Do not assume existing document-share policy covers attribute-level extraction. |
| 3 | Has DDA received the consent screen brief and confirmed they can design and approve in time for Phase 1? What is DDA's estimated design-to-approval timeline? | PM → DDA | HIGH | Provide DDA with this BRD and the consent screen requirements (Section 11.1). Get DDA timeline commitment. |
| 4 | Has at least one SP (Etisalat Retail or Al Maryah/ADIB) confirmed pilot participation and committed engineering resource for integration? | PM → SP Relations | HIGH | Initiate outreach immediately. A verbal commitment from SP product lead is sufficient to proceed to Phase 1 sprint planning. |
| 5 | Has Legal/Compliance confirmed that the PDPL consent model for attribute-level sharing (user-initiated, field-listed, eSeal-provenance-maintained) is compliant, and that no additional consent instrument is required before Phase 1 GA? | PM → Legal | HIGH | Provide Legal with Section 10 (NFR-11) and the consent flow description (Section 3). Target: written confirmation within 2 weeks. |

---

## 15) Phasing and Roadmap

| Phase | Sprints (est.) | Scope | Gate Conditions |
|---|---|---|---|
| **Phase 0 — Discovery and Prerequisites** | Sprint 71–72 | Structured payload audit; TDRA policy engagement; DDA consent screen design brief; SP pilot outreach; Legal/PDPL review; ICP schema request; TRA field alignment | No gate — begins immediately. All five Phase 0 questions (Section 14) must be answered before Phase 1 sprint kickoff. |
| **Phase 1 — Core Pre-Fill MVP** | Sprint 73–75 | EID + Visa visible fields only; EID registered address with caveat; "Fill with UAE PASS" button; consent screen; VP delivery via existing DV API; 1 telecom pilot SP; 1 banking pilot SP; Firebase feature flag | ICP structured payload confirmed; TDRA EID/Visa sharing authorisation confirmed; DDA consent screen approved; 1 pilot SP confirmed; Legal PDPL clearance; ICP eSeal Transition compatibility validated |
| **Phase 2 — Employment, Address, and Vehicle Expansion** | Sprint 76–79 | Labour Card fields; Tenancy Contract address overlay (Dubai/Fujairah); Vehicle License; Driving Licence (excluding blood group); Tax Residence Certificate; Trade Licence (B2B); assisted channel consent pattern; 4 additional SPs | Phase 1 pilot complete with positive pre-fill success rate; MoHRE Labour Card payload confirmed; DLD Tenancy Contract payload confirmed; TDRA employment and address policy confirmed; DDA Phase 2 screen designs approved |
| **Phase 3 / Separate Initiative — Verified Data API (Hidden Claims)** | _[TO BE PLANNED]_ | Hidden claims primitive; attribute extraction API; new consent screen pattern; issuer schema integration; hidden claim sharing events in audit log | Presented to TDRA as separate initiative and approved; issuer schema disclosure completed (ICP, MoHRE, DLD, FTA); TDRA policy instrument per claim category; DDA hidden claims consent screen approved; PDPL assessment per claim; security review; separate commercial model defined (if applicable) |

---

## 16) Success Metrics

### 16.1) North Star Metric

**Pre-fill share rate:** The percentage of SP form-fill sessions where the user taps "Fill with UAE PASS" and the consent screen appears, who then complete the pre-fill (tap "Share") and successfully receive a populated form. Target: 70%+ consent-to-completion rate by end of Phase 2.

### 16.2) Per-Phase Metrics

**Phase 1 — MVP Pilot**

| Metric | Target |
|---|---|
| Pre-fill sessions initiated (pilot SPs) | > 500 in first month |
| Consent-to-completion rate | > 65% |
| SP-reported form completion time reduction | > 40% vs manual baseline |
| SP-reported KYC data quality error rate | < 5% (vs typical OCR error rate of ~15%) |
| User-reported pre-fill satisfaction (in-app NPS on consent screen) | > 60 NPS |

**Phase 2 — Expanded Documents and SPs**

| Metric | Target |
|---|---|
| SPs live with pre-fill capability | 6 |
| Monthly pre-fill sessions | > 10,000 |
| Consent-to-completion rate | > 70% |
| Labour Card pre-fill success rate (where Labour Card exists in DV) | > 60% |
| Tenancy Contract address pre-fill success rate (Dubai users) | > 50% |

**Phase 3 / Separate — Verified Data API**

| Metric | Target |
|---|---|
| SP integrations consuming hidden claims | > 3 |
| Hidden claims consent acceptance rate | > 55% (lower expected due to sensitivity) |
| SP NPS for hidden claims data quality | > 70 NPS |
| New SP onboardings driven by hidden claims value proposition | > 5 in first 6 months |

---

## 17) Open Questions and Decision Log

| # | Question | Type | Owner | Status |
|---|---|---|---|---|
| OQ-01 | Do existing VP payloads contain structured field data for ICP documents? | Technical | DV Engineering | OPEN — Phase 0 gate |
| OQ-02 | Does TDRA's current sharing policy authorise attribute-level extraction of EID/Visa fields for commercial SP pre-fill? | Policy | TDRA via PM | OPEN — Phase 0 gate |
| OQ-03 | What TDRA policy instrument is required to authorise residential address sharing from EID registered address with commercial SPs? | Policy | TDRA via PM | OPEN — Phase 0 gate |
| OQ-04 | What TDRA policy instrument is required to authorise employment field sharing (employer, title, permit number) from Labour Card with commercial SPs? | Policy | TDRA via PM | OPEN — Phase 2 gate |
| OQ-05 | Will TDRA ever authorise salary sharing with commercial SPs? If yes, under what conditions? | Policy | TDRA | OPEN — no timeline; exclude from all phases until resolved |
| OQ-06 | Has ICP formally agreed to publish structured attribute schemas for EID, Visa, and Passport? | External | ICP via PM | OPEN — Phase 0 gate |
| OQ-07 | Which specific EID and Visa fields satisfy the TRA SIM registration KYC mandate? | Regulatory | TRA via PM | OPEN — Phase 1 gate for telecoms |
| OQ-08 | What is DDA's estimated timeline from consent screen design brief to approved designs? | Design | DDA | OPEN — Phase 0 gate |
| OQ-09 | Has Etisalat Retail confirmed pilot participation? | Commercial | SP Relations | OPEN — Phase 1 gate |
| OQ-10 | Has Al Maryah or ADIB confirmed pilot participation? | Commercial | SP Relations | OPEN — Phase 1 gate |
| OQ-11 | Has Legal/Compliance confirmed PDPL compliance of the proposed attribute-level consent model? | Legal | Legal/Compliance | OPEN — Phase 1 gate |
| OQ-12 | Do MoHRE Labour Card VP payloads contain structured field data (employer, title, permit)? | Technical | DV Engineering / MoHRE | OPEN — Phase 2 gate |
| OQ-13 | Do DLD Tenancy Contract VP payloads contain structured field data (address, EJARI number, dates)? | Technical | DV Engineering / DLD | OPEN — Phase 2 gate |
| OQ-14 | What is the consent model for the assisted channel (CBD Assisted) use case — specifically, who initiates consent and who views the pre-filled data? | Design / Policy | DDA + TDRA | OPEN — Phase 2 gate |
| OQ-15 | Should hidden claims be presented to TDRA as a separate strategic initiative with its own BRD, or as a Phase 3 extension of this BRD? | Strategic | PM + TDRA | OPEN — recommend separate initiative; requires PM decision |
| OQ-16 | What is the ICP eSeal Transition status and expected completion date? Does it affect Phase 1 VP validity? | Technical | ICP + DV Engineering | OPEN — Phase 1 gate |

---

## 18) Glossary

| Term | Definition |
|---|---|
| DV | Digital Documents — the UAE PASS component for storing and sharing government-issued documents. Avoid the term "vault." |
| eSeal | Cryptographic organisational stamp applied by an issuer to authenticate a document or attribute. CAdES/PAdES standard. Not to be confused with eSignature (a person-level signing act). |
| Verifiable Presentation (VP) | A package of one or more documents or attributes, bundled and signed for delivery to a Service Provider. The existing mechanism for document sharing in DV. |
| SP | Service Provider — any organisation integrated with UAE PASS DV to consume shared documents or attributes (banks, telcos, insurers, government portals). |
| ICP | Federal Authority for Identity, Citizenship, Customs and Ports Security — the primary issuer of EID, Residence Visa, and Passport in DV. |
| MoHRE | Ministry of Human Resources and Emiratisation — issuer of Labour Card and Labour Contract in DV. |
| DLD | Dubai Land Department — issuer of Tenancy Contract (EJARI) and Title Deeds for Dubai. |
| TDRA | Telecommunications and Digital Government Regulatory Authority — the regulatory authority and product owner for UAE PASS. Policy decisions on attribute sharing are made by TDRA. |
| DDA | Design Authority — the design and UX approval partner. Any new screen or UX pattern requires DDA review and approval. |
| FAHR | Federal Authority for Government Human Resources — issuer of Employee Work Contracts for federal government employees. |
| FTA | Federal Tax Authority — issuer of Tax Residence Certificates. |
| TRA | Telecommunications Regulatory Authority — regulates telecoms SPs and mandates specific fields for SIM registration KYC. Distinct from TDRA. |
| Hidden Claims | Fields included in the structured payload of an issuer-signed document that are not rendered on the visible document face in DV. They carry full eSeal provenance but are not currently exposed to users or SPs. |
| Correlation ID | A unique, time-boxed, one-time identifier generated by the SP to initiate a sharing or pre-fill request. Must contain no PII. |
| EJARI | Dubai's mandatory tenancy registration system, operated by DLD. The EJARI number uniquely identifies a registered tenancy contract. |
| ISCO | International Standard Classification of Occupations — a UN standard occupation taxonomy used in Labour Card payloads to classify job categories. |
| WPS | Wage Protection System — a UAE Ministry of Finance system that monitors salary payment compliance for private sector employers. WPS registration status of an employer is a bankable signal of payroll stability. |
| PDPL | UAE Personal Data Protection Law — the primary data protection legislation governing PII handling, consent, and data subject rights in the UAE. |
| FATCA/CRS | US Foreign Account Tax Compliance Act / Common Reporting Standard — international tax transparency regimes requiring financial institutions to classify account holders by tax residency. |
| MAKANI | Dubai Municipality's geographic addressing system assigning unique numeric addresses to all buildings and units in Dubai. |
| Attribute Catalogue | A formally defined register of all attributes extractable from DV documents, their source documents, issuers, and data types. A prerequisite for the Form Pre-Fill feature. Currently does not exist as a formal artefact. |
| Path A | Pre-fill architecture path where hidden claims already exist in existing VP payloads and SPs can extract them with schema disclosure. Requires no new DV API. |
| Path B | Pre-fill architecture path where a new DV backend endpoint extracts hidden claims from issuer payloads on demand. The correct long-term architecture for a Verified Data API. |
| QR Hygiene | The set of rules governing QR code usage in DV sharing flows: unique correlation IDs, short TTL, one-time use, no PII embedded. |
| Firebase Remote Config | Google Firebase feature used in DV for remote feature flag management, enabling phased rollout and SP-specific feature enablement without app releases. |
| RTL | Right-to-left — the text directionality used for Arabic content in the DV app. |

---

_Last updated: 2026-04-01 | Author: Feature Benchmark Analyser | Version: 1.0 | Status: Draft_

_For DDA design engagement, refer to the consent screen requirements in Sections 9, 11, and 14._
_For TDRA policy alignment, refer to Sections 6.4, 8.3, 13, and 17._
_For Engineering sprint planning, refer to Sections 14, 15, and the Phase 0 gate in Section 14._
