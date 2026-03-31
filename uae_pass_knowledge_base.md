
# UAE PASS & Digital Documents (DV) — Knowledge Transfer
_Last updated: 2025-11-12T13:55:09Z_

## 1) What UAE PASS is (and how DV fits)
UAE PASS is the national digital identity platform. In our work, we operate two tightly connected domains:

- **UAE PASS (DDA-owned)**: user onboarding (registration & identity proofing), authentication/SSO, qualified electronic signature.
- **Digital Documents / “Documents” (DV)**: document request (from issuers), storage in the app, and consent-based **document sharing** with service providers (SPs).

### Key stakeholders
- **TDRA** (regulator / product owner) and **DDA** (design/UX / some services).
- **ICP** — high-volume document **issuer** (EID, Residency/Visa, Passport).
- **Service Providers (SPs)** — consumers of user documents (banks, telcos, insurers, etc.).

### Governance & cadence (working model)
- Bi‑weekly sprints; backlog refinement mid‑week; sprint review on Fridays.
- Major features require DDA design approval and TDRA policy alignment.
- Tools: Jira (“DV Product”), Figma (“DV Refresh 2024/25”), SharePoint for slides, Firebase for push/RC.

---

## 2) Core capabilities
### 2.1 Authentication & SSO
- Web/app SSO via QR or deep link: SP shows a QR; user scans with UAE PASS; short‑lived token, no PII inside the QR.
- Session established server‑to‑server after successful authentication.

### 2.2 Qualified eSignature
- User signs transactions or forms; signature attests **a natural person** consent.
- Used in flows that need non‑repudiation at the person level.

### 2.3 Documents (DV)
- **Issued documents**: official docs pulled from issuers (e.g., ICP). They carry issuer authenticity (eSeal) and status (Active/Expired/Revoked).
- **Uploaded documents**: user‑uploaded PDFs self-signed; generally lower trust for SPs.

### 2.4 Document lifecycle (DV)
- **Request** → **Availability** → **Storage** → **Updates** → **Revocation/Expiry**.
- **Issuance/Availability**: DV polls/requests from issuer via secure backend API.
- **Revocation**: issuer revokes; DV reflects state; user receives notification.
- **Updated version**: if a newer version exists, DV prompts: “Would you like to request an updated version?”
- **Expiry**: reminders at D‑30/15/7/5/3/1 (configurable).

### 2.5 Document sharing (“Presentation”)
- Initiated by SP (web/branch/app). SP creates a **sharing request** (correlation ID), optionally exposed as a QR.
- User gets **actionable** notification in UAE PASS and approves per‑transaction consent.
- DV prepares a **verifiable presentation** containing requested documents/attributes, preserves issuer signatures, and delivers to SP.
- SP is responsible for validating authenticity (e.g., **eSeal** validation) and consuming attributes.

---

## 3) eSeal in our context
- **What**: cryptographic **organization** stamp (issuer, not a person) proving origin + integrity of a document (e.g., CAdES/PAdES).
- **Today**: ICP traditionally used **DDA eSeal service** to sign a hash of the encoded credential. DV **validates** eSeal via DSS and passes to SPs.
- **Change (2025)**: ICP to **self-sign** (own HSM/certs), keeping **same structure**. Certificates will roll; DDA validator compatibility is being aligned.
- **Impact on DV**: no DV code change; expected **improvement** in reliability for ICP flows (less dependency on DDA eSeal uptime).
- **SP Impact**: SPs using **DDA’s validation API** may need to confirm compatibility; most SPs validate locally.

**Actions we planned**
1) Survey SPs for validation approach (local vs DDA API).  
2) Lower‑env tests with ICP test vectors.  
3) Update onboarding guide & cutover comms.  

---

## 4) QR code usage & hygiene
- **Login/SSO**: SP web/app displays a time‑boxed QR; user scans with UAE PASS.
- **Start sharing**: SP displays a QR carrying a **unique** correlation/request ID; scan opens sharing in the app.
- **Document verification**: some PDFs/screens include a QR pointing to issuer verification.
- **Hygiene**: unique IDs, short TTL, one‑time use, idempotent SP backend, clear error codes (expired/used/invalid).

**Operational issue we addressed**: duplicate correlation IDs from some SPs (e.g., telcos/banks) causing duplicate requests and noisy notifications.  
**Fix**: DB unique constraint on `unique_correlation_id`; service throws `PRESENTATION_REQUEST_DUPLICATE_CORRELATION_ID` to SP; staged rollout after SP comms.

---

## 5) Notifications taxonomy
### Actionable (user must act)
- **Document Sharing Request**: approve/decline SP request to access specific docs.

### Informational (non-actionable)
- **Document Issuance**: requested doc is available (Active/Expired).  
- **Document Expiry**: reminders at D‑30/15/7/5/3/1.  
- **Document Revocation**: issuer revoked a stored doc.  
- **Document Removed**: user removed a stored doc.  
- **Custom**: DDA‑defined; rarely used in production.

**UX notes**
- Keep bilingual (EN/AR), avoid “vault” term; say **“Documents”**.  
- When app is foreground, supplement OS banner with **in‑app cues** (badge, snackbar, inbox).  
- For missed notifications: provide **in‑app alerts** (e.g., “bell” inbox, banners).

---

## 6) Document UX — current and enhancements
### 6.1 Documents tab (as‑is)
- Tabs: **Issued** and **Uploaded** (currently equal visual weight).  
- Global search across both; sort by name/issuer; view modes (list, type‑based).  
- Categories: All / Personal / Professional / Legal / Property / Other.

**Identified weaknesses**
- Equal weight for Issued vs Uploaded despite different SP value.  
- Type view useful only for one‑to‑many cases; grid missing.  
- Inconsistent empty states and copy.

### 6.2 Enhancements we defined
- **New landing** with two primary CTAs: **Request Document** / **Upload Document**.  
- **Grid view** (common mental model from file apps) in addition to list.  
- **Issuer/logo chips** on doc cards: Issued → issuer logo; One‑to‑many & Uploaded → **document type** logo.  
- **More actions** menu cleanup (View Details, View/Download/Share PDF, QR verification, Remove).  
- **Copy-any-field** affordance on Document Details (tap/long‑press; toast “is copied”).  
- **Consistent PDF rendering** (native viewer; fit‑to‑width; snap to page; unified padding).  
- **Bilingual microcopy** refresh; **no “vault”** in user text.

**Empty-state examples (EN/AR)**
- “Add your first document” / «أضف أول مستند لك».  
- “Tap **Request Document** to request your first document.” / «اضغط على **اطلب مستند** لطلب أول مستند لك.»

---

## 7) Plurals & counters (Arabic rules)
**English**: `"0 issued document(s), 1 uploaded document(s)"`  
**Arabic (RTL number-first)**:  
- 0 → omit segment.  
- 1 → `"0 مستند صادر"`; 2 → `"0 مستندان صادران"`; 3–10 → `"0 مستندات صادرة"`; 11+ → `"0 مستند صادر"`.  
- Same pattern for uploaded: `"مستند محمّل / مستندان محمّلان / مستندات محمّلة / مستند محمّل"`.

---

## 8) Dual Citizenship — Primary/Secondary EID
**Goal**: support users granted “Special Emirati Citizenship” while retaining their original residency/nationality.

### Detection & state
- Server flag from DDA auth API: `isDualUser`.
- One‑time flag: `welcomePopupShown`.
- Inventory: `hasPrimaryEID`, `hasSecondaryEID`.

### Document addition
- **Visibility**: show **“Secondary EID (2nd nationality)”** only if `isDualUser = true`.  
- **First‑time (no EIDs)**: show welcome; allow requesting **Primary** and **Secondary**.  
- **Migration (existing EID)**: reclassify existing to **Secondary**; CTA to **request Primary EID (UAE)**.  
- **Chips** on cards: “Primary EID (UAE)” / “Secondary EID (2nd nationality)”.

### Sharing
- On first dual detection within a share flow, show **Welcome** pop‑up **before** “missing documents.”  
- **Default** to **Primary EID (UAE)** for sharing; Secondary not allowed by ICP instruction.  
- If Primary missing: prompt to request.

**AC highlights**
- Welcome shows once (Documents or Sharing), tracked via `welcomePopupShown`.  
- Deep links pass doc type IDs.  
- Full EN/AR/RTL accessibility.

---

## 9) One‑time consent (“Auto Add Documents”)
**Concept**: with explicit, revocable consent, DV **periodically checks** with issuers and **auto‑adds** new/updated documents for the user. **Sharing** remains **per‑transaction** consent.

### Naming
- **Auto Add Documents** / «الإضافة التلقائية للمستندات».  
- Helper: “We’ll check with issuers and add new documents for you.”

### UX outline
- Settings toggle + “Check now” button.  
- Consent sheet explaining scope, revocation, and audit logging.  
- Discovery limits per issuer; backoff; failure surfacing.

### Legal/policy considerations
- Verify fit with UAE data protection law and sectoral exceptions.  
- Consent lifetime, scope, and revocation UX; audit retention.

### Value
- Proactive updates; fewer failed shares due to missing/expired docs.  
- “Before you start” pre‑checks in sharing flows (no additional taps).

---

## 10) Analytics & KPIs
- **Lost requests**: break down by issuer/SP/network; top 3 causes; owners.  
- **“Successful combos %”**: percentage of SP‑requested doc sets fully satisfied on first attempt.  
- **“No document requested”**: analyze drop at the request screen; design nudges (copy, layout, defaults).  
- **Notification open rate**: foreground vs background; in‑app cue coverage.

---

## 11) SP onboarding essentials
- **Correlation IDs**: must be unique, time‑boxed, one‑time; DV enforces uniqueness.  
- **Validation**: SP should validate eSeal locally (sample code provided) or ensure DDA validator accepts ICP‑signed objects post‑change.  
- **Error handling**: present DV error codes (e.g., duplicate correlation) in SP channels with user‑friendly copy.  
- **Security**: never embed PII in QR; use opaque IDs; HTTPS/TLS pinning as per guidelines.

---

## 12) Copy guidelines (EN/AR)
- Avoid “vault” in user strings; use **Documents** / «المستندات».  
- Keep actionable labels short: “Request Document”, “Upload Document”.  
- Bilingual parity and glossary alignment; test truncation in both languages.  
- Provide system messages for key states: **Saved**, **Unsaved changes**, **Updating your document**, **Issue fetching document**.

**Common EN → AR pairs**
- “Quick Tip” → «تلميح سريع»  
- “Got it” → «حسنًا»  
- “Document Information” → «معلومات المستند»  
- “Document Details” → «تفاصيل المستند»  
- “Tap any field to copy its value instantly.” → «اضغط على أي حقل لنسخ قيمته فورًا.»

---

## 13) PDF viewer revamp — user story (summary)
**As a** user, **I want** PDFs to open directly in a native viewer with consistent fit/paging, **so that** I can read without manual zoom/pan friction.  
**Acceptance**: fit‑to‑width default, snap‑to‑page, pinch‑to‑zoom, toolbar actions respect issuer flags, RTL/EN accessibility, telemetry events.

---

## 14) Sprint quick‑win backlog (sample)
- Guided journey pop‑up copy refresh (EN/AR).  
- Document upload error/inline copy update (EN/AR).  
- Android dialog navigation bar transparency fix (select document type).  
- iOS collapsing header title on document selection (parity).  
- Document Details: copy‑to‑clipboard for fields (both).  
- “Consent & add” micro‑experiment (remote‑config).  
- SP comms: duplicate correlation enforcement & eSeal heads‑up.

---

## 15) Open questions / follow‑ups
- DDA validator compatibility with ICP‑signed eSeals.  
- One‑time consent legal retention windows (TDRA legal).  
- Final EN/AR labels for Dual EID chips and onboarding copy.  
- Notification UX changes for foreground sessions.

---

## 16) Glossary
- **eSeal**: organization cryptographic seal proving origin/integrity.  
- **Verifiable presentation**: package of user documents/attributes prepared for SP.  
- **Correlation ID**: unique request identifier from SP used to initiate sharing.  
- **Primary/Secondary EID**: citizen (UAE) vs resident/second‑nationality EID classification for dual-citizenship users.

---

## 17) Contact & ownership
- **Product**: Fadi / DV Product Team  
- **Engineering**: FE/BE/QA  
- **QA/Ops**: DV Ops  
- **UX/Design**: DDA liaison + in‑house

---

> This document is a working knowledge base to onboard teammates and guide execution. Link out to Jira epics, Figma files, and SharePoint decks for full detail.
