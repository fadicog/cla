
# Feature KB — QR Code Verification (As‑Is)
Last updated: 2025-11-14T05:40:18Z

## 1. Summary
This document captures the **as‑is** behaviour of the **QR Code Verification** feature in UAE PASS for **issued documents** (e.g., Emirates ID, Residency, Passport). It also lists current limitations and **recommendations** to strengthen trust and usability.

## 2. Context
UAE PASS supports two document types in the app:
- **Issued**: official documents sourced from government issuers integrated with UAE PASS. These carry issuer authenticity and lifecycle (Active/Expired/Revoked).
- **Uploaded**: user‑uploaded, self‑signed documents. Lower trust for service providers.

**QR Code Verification** is available on **issued documents** via the document’s actions menu.

## 3. Scope (as‑is)
- Platforms: iOS & Android UAE PASS app.
- Surfaces: Document Details → More actions → “QR verification” (label may vary).
- Backend systems involved: Issuer systems, UAE PASS backend, **UAE Verify** verification portal.
- Out of scope here: document **sharing** flow and SSO login QR usage (separate features).

## 4. Actors & Systems
- **End User**: UAE PASS holder viewing their issued document.
- **Verifier**: a staff member or system scanning the QR to confirm document validity.
- **UAE PASS App**: renders document card/details and the verification QR after PIN entry.
- **UAE Verify Portal**: public verification page reached after scanning the QR.
- **Issuer**: authoritative source for the document and its status.

## 5. Preconditions
- User is logged in to UAE PASS.
- The document is an **issued** document present in the user’s Documents list.
- Device online; user knows their app PIN.

## 6. User Flow (as‑is)
1. User opens **Documents** and selects an **issued document**.
2. From the document’s actions menu, the user selects **QR verification**.
3. App prompts for **PIN** to authorise showing the QR.
4. App displays a **QR code** for this document.
5. A verifier scans the QR (any QR scanner supported).  
6. The scanner is redirected to **UAE Verify**, which displays:  
   - the **issuer** of the document,  
   - the **status** (e.g., Active/Revoked/Expired),  
   - and issuance/verification timestamps as available.  
7. The verifier uses this information to accept or reject the document.

## 7. Data & Behaviour (as‑is)
- The QR encodes a link/identifier for the specific document verification endpoint in **UAE Verify**.
- **No personal data** is embedded directly in the QR (by design).
- **Current limitation**: the **UAE Verify** page **does not display a reference that uniquely binds** the verification result to the **exact document instance** the user presented (e.g., masked Emirates ID number, document serial).  
  - Consequence: a copied/screenshot QR could still show “valid” without revealing whether it refers to the **same** document instance the user is presenting.

## 8. Error & Edge States (as‑is)
- Incorrect PIN → QR not shown.
- Network issues → QR may fail to load; retry prompt in app.
- If issuer marks the document Revoked/Expired, **UAE Verify** reflects that state when scanned.
- Other conditions (e.g., link expiry, throttling) depend on backend configuration and are not exposed in‑app.

## 9. Security & Privacy Notes (as‑is)
- **PIN gate** prevents casual display of verification QR.
- QR carries an opaque reference; primary checks occur on **UAE Verify**.
- The current verification page **does not** show document‑specific identifiers to bind the result to the user’s presented record.

## 10. Known Limitations / Risks
- **Not bound to document instance on screen**: Verifier cannot confirm, at a glance, that the QR corresponds to the **same** document (e.g., same Emirates ID number) the user is showing.
- **Replayability**: Static QR may be **reused** (e.g., screenshot) if there is no short lifetime or anti‑replay (app/portal behaviour varies; not surfaced to user).
- **Usability**: Verifier experience depends on their scanner/browser; inconsistent messaging may cause confusion.

## 11. Recommendations (enhancements — not yet implemented)
These are proposed improvements to address the above risks while preserving privacy and simplicity.

### 11.1 Bind verification to the presented document
- **Display minimal, privacy‑safe reference** on UAE Verify (and optionally in‑app) such as:
  - **Masked document number** (e.g., Emirates ID: `784-XXXX-XXXXXXX-X`),
  - **Last 4 digits** or **checksum** of the document number,
  - **Issuer + document type + masked holder name initials** (e.g., “ICP · Emirates ID · A.F.”).
- Add “**This verification refers to:** {masked‑reference}” on the verification page.

### 11.2 Reduce replayability
- Use **short‑lived**, signed verification links; show **“Valid at {time}”** with a gentle countdown.
- Optionally render a **dynamic QR** (rotating token) while the page is open.
- Add **anti‑replay** server checks (nonce + single active verification per token).

### 11.3 Improve verifier UX
- Clean, mobile‑first **UAE Verify** layout with clear status badges: **Valid / Revoked / Expired**.
- Prominent **issuer name/logo** and **verification timestamp**.
- Explicit **help text**: “Compare the masked reference with the document shown by the user.”
- Provide a **fallback short code/link** under the QR (copyable) for environments where camera scanning is restricted.

### 11.4 Telemetry & ops
- Log events: `qr_shown`, `qr_scanned`, `verify_view`, `verify_status`, `verify_error` (issuer, device class).
- Add dashboards for verification success vs. failures and replay detections.

### 11.5 Accessibility & localisation
- Ensure full EN/AR parity; RTL layout for Arabic.
- High‑contrast status indicators; screen‑reader labels for status and references.

## 12. Copy (draft)
- Action label: **QR verification** / «التحقق عبر رمز QR»
- PIN prompt body: “Enter your PIN to show the verification QR.” / «أدخل رقمك السري لعرض رمز التحقق.»
- Verification page helper: “Compare this masked reference with the document shown.” / «قارِن هذا المرجع المخفي بالمستند الذي يقدمه المستخدم.»
- Status labels: **Valid** / **Revoked** / **Expired**  → «سليم» / «مُلغى» / «منتهي الصلاحية»

## 13. Open Questions
- Should the verification link be **time‑limited**? If yes, what TTL is acceptable for field use?
- What is the **minimal** reference we can display that satisfies verifiers without exposing full PII?
- Do any current verifiers cache screenshots of the **UAE Verify** page? Do we need a visible timestamp/watermark?
- Should we provide an **offline verification hint** (e.g., hotline or code) for rare no‑connectivity scenarios?

## 14. Acceptance Criteria (for future change)
- UAE Verify displays a **masked reference** that binds the verification to the presented document instance.
- Short‑lived links prevent **replay** beyond the defined TTL.
- EN/AR localisation with proper RTL; accessible status semantics.
- Telemetry available for scans and outcomes; error rates monitored.

## 15. References & Ownership
- Owners: Product (Documents), FE/BE, Ops; DDA/TDRA for UX/policy alignment.
- Related features: Document Sharing QR (separate), SSO Login QR (separate).
- Contact: DV Product Team.
