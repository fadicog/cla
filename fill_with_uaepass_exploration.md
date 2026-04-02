# Fill with UAE PASS — Exploratory Product Analysis
**Date**: 2026-04-01 | **Analyst**: Feature Benchmark Analyser | **Status**: Draft — Exploratory
**Scope**: Independent concept exploration; separate from SP Form Pre-Fill BRD

---

## Executive Summary

"Fill with UAE PASS" as a universal, consent-based form-filling product is architecturally feasible, strategically sound, and competitively differentiated — but it is not a single product. It is a product family of five distinct delivery form factors, each with different trust models, regulatory requirements, and go-to-market timelines.

The core differentiation from Google/Apple autofill is not convenience — it is cryptographic provenance. UAE PASS holds government-issued, eSeal-verified identity data. When a user fills a form with UAE PASS, the receiving party can independently verify that the data originated from ICP, MoHRE, or another authority. No consumer autofill product in the world offers this.

The recommended MVP is the JavaScript SDK ("Fill with UAE PASS" button) combined with a deep-link mobile trigger — the fastest path to broad reach without requiring full SP API integration. This is the form factor most analogous to "Continue with Google" and represents the largest addressable surface area.

---

## 1) Benchmark — Existing Form-Fill Products

### 1.1 Browser Built-In Autofill

| Product | Architecture | Data Types | Trust Level | UX Model | Limitations |
|---------|-------------|------------|-------------|----------|-------------|
| Chrome Autofill | Local storage + Google Account sync (optional) | Name, address, email, phone, payment card, password | Self-declared by user; no verification | Inline suggestion below field; yellow highlight | No issuer provenance; user can enter anything; no cryptographic proof |
| Safari AutoFill | iCloud Keychain sync; device-local fallback | Contact card fields, passwords, payment cards, passkeys | Self-declared; Apple Wallet cards have bank-level trust | Inline keyboard suggestion; Touch ID / Face ID confirmation | Contact card is user-curated; no government-verified source |
| Firefox | Local storage; no account sync by default | Name, address, email, phone; credit cards (optional) | Self-declared | Dropdown below field | No cloud sync without Firefox account; no verification layer |
| Edge | Microsoft account sync; Windows credential store | Similar to Chrome; tighter integration with Windows Hello | Self-declared; Microsoft account identity layer | Inline; Copilot sidebar integration emerging | Microsoft identity ≠ government identity; no issuer provenance |

**Trust model summary**: All browser built-ins operate on self-declaration. The user populates their own profile; the browser stores and replays it. There is zero issuer provenance, zero cryptographic verification, and zero mechanism for the receiving site to validate that the filled data is accurate. This is the fundamental gap UAE PASS can address.

---

### 1.2 "Fill with Google" / "Continue with Google"

**"Continue with Google" (OAuth/OpenID Connect)**
- Architecture: OAuth 2.0 authorisation flow; OpenID Connect identity layer. Google acts as Identity Provider (IdP). The website redirects to Google, user authenticates, Google returns an ID token (JWT) containing name, email, profile photo, and optionally phone number.
- Data: Email, name, profile photo. Not address, not national ID, not date of birth, not government-issued fields.
- Trust: Email is verified by Google (deliverability check). Name is self-declared on Google account. No government verification.
- UX: Standard OAuth redirect or popup. Widely adopted — 3+ billion Google accounts. Frictionless for users already signed in.
- Limitation for UAE PASS comparison: The data payload is thin (email + name only). It is primarily an authentication flow, not a form-fill flow. The user's Google profile is not government-sourced.

**"Fill with Google" / Google Autofill**
- Distinct from "Continue with Google". Uses Chrome's autofill engine backed by Google Account data (Contacts, Payments, addresses stored in Google Account settings).
- Architecture: Cloud-synced; address data comes from Google Account → synced to Chrome.
- Data: Full name, postal address, phone, email, payment cards. User-curated, not government-verified.
- Key insight: Google has introduced "Autofill with Google" prompts on checkout pages, which is the closest analogue to the "Fill with UAE PASS" concept — but the data is entirely self-declared and Google is not a government identity authority.

**"Sign in with Google" for government use**: Several countries have tested using Google as an IdP for government portals, but regulatory and sovereignty concerns have consistently blocked adoption at the identity tier. UAE PASS avoids this problem entirely — it is a sovereign IdP.

---

### 1.3 Apple AutoFill / Sign in with Apple

**Sign in with Apple**
- Architecture: OAuth 2.0 / OpenID Connect. Apple acts as IdP. Returns user identifier, name, email (with optional relay/private email). Requires Face ID / Touch ID confirmation.
- Data: Name (user-confirmed), email (may be private relay), and a stable user identifier. No address, no national ID, no date of birth in the base flow.
- Trust: Apple-verified Apple ID. Name is user-curated. Email relay means even the email may be synthetic.
- Privacy model: Apple's design philosophy is to share as little as possible. Sign in with Apple is deliberately data-minimising — the inverse of what "Fill with UAE PASS" needs to do.
- Hardware trust: Face ID / Touch ID biometric confirmation at point of use is a strong UX model. UAE PASS should match this pattern.

**iOS AutoFill (Contact Card + iCloud Keychain)**
- Architecture: Device-local; iCloud Keychain for sync. The "My Card" in Contacts populates name, address, phone, email fields.
- Data: Whatever the user has entered in their Contacts card. Can include address, phone, email, website, birthday.
- Trust: Zero — fully self-declared.
- iOS AutoFill Provider API (iOS 12+): Third-party apps (1Password, LastPass, Google Password Manager) can register as AutoFill providers via the `AutoFillCredentialProvider` extension point. This is the mechanism UAE PASS would use for iOS integration.

**Passkeys (iOS 16+ / Android 14+)**
- Not directly relevant to form-fill, but relevant to authentication layer. UAE PASS should track passkey adoption as it may change the authentication ceremony for "Fill with UAE PASS" flows.

---

### 1.4 Password Managers with Form-Fill

| Product | Architecture | Field Detection | Data Types | Trust Level |
|---------|-------------|----------------|------------|-------------|
| 1Password | AES-256 encrypted local vault + cloud sync | Heuristic field detection; custom field labelling; browser extension injects autofill UI | Passwords, TOTP, addresses, identities, payment cards, custom fields | Self-declared; zero issuer provenance; strong encryption |
| Dashlane | Similar to 1Password; stronger emphasis on web autofill UX; autofill confidence scoring | ML-based field classification; confidence threshold before suggestion | Same as 1Password + receipt/ID document photo storage | Self-declared; photo of ID ≠ verified ID data |
| Bitwarden | Open-source; self-hostable; browser extension + mobile app | Heuristic; URI matching | Passwords, identities, payment cards | Self-declared; zero issuer provenance |
| LastPass | Browser extension primary; mobile secondary | Heuristic field detection | Passwords, addresses, identities, secure notes | Self-declared |

**Form-fill field detection methodology** (shared across all password managers):
1. The extension scans the DOM for `<input>`, `<select>`, and `<textarea>` elements.
2. It classifies fields using a combination of: `autocomplete` attribute value, `name` attribute, `id` attribute, `placeholder` text, surrounding label text, and `type` attribute.
3. It maintains a heuristic scoring model to determine which vault item best matches the detected form context.
4. On match above threshold, it presents a fill suggestion (inline icon, dropdown, or overlay).

**Key insight for UAE PASS**: The field detection layer used by password managers is well-understood and implementable. UAE PASS does not need to invent this — it can adopt the same heuristic DOM analysis approach in a browser extension. The differentiator is not how UAE PASS detects fields; it is what data it fills them with (government-verified vs. self-declared).

**Dashlane ID document storage**: Dashlane allows photo uploads of passports and ID cards, and OCR-extracts fields for autofill. This is self-declared from a photo — not cryptographically verified. A user could upload a photo of anyone's ID. This is a qualitatively different trust model from UAE PASS eSeal-verified data.

---

### 1.5 Government Identity Wallets

#### Singapore Singpass MyInfo
- Architecture: Centralised government data API. Singpass acts as IdP and data broker. SPs call the MyInfo API after user authentication; Singpass retrieves data from government registries (ICA, CPF, LHLA, ACRA, etc.) and returns it in real-time.
- Data: Name, NRIC/FIN, date of birth, gender, nationality, address (registered + mailing), marital status, occupation, employment, income (CPF contributions), education level, vehicle ownership, HDB ownership, driving licence.
- Trust: Government registry data; highly accurate; updated in real-time by source agencies.
- Integration model: SPs must be registered and approved. No open-web model.
- UX: "Fill with Singpass" button on SP pages. User taps → Singpass app opens → biometric auth → consent screen listing requested fields → data returned to SP.
- Trust transmission: API-trust only. SP trusts Singpass's assertion. There is no cryptographic proof the SP can independently verify offline.
- Known limitation: If the Singpass API is unavailable, the fill fails. There is no offline fallback. UAE PASS's eSeal model is architecturally stronger here.

#### EU Digital Identity Wallet (eIDAS 2.0)
- Architecture: Decentralised wallet model. Member States issue wallets; users hold Verifiable Credentials (VCs) in their wallet. Relying parties (RPs) request presentations. Selective disclosure via W3C VC Data Model or ISO 18013-5 mdoc.
- Data: National ID data, professional qualifications, driving licence (mDL), health data, education credentials. Attribute-level selective disclosure.
- Trust: Issuer-signed VCs with PKI chain. RP can verify the credential offline against issuer public key — the same model as UAE PASS eSeal. This is the gold standard.
- Status: In deployment across EU member states as of 2025-2026. Large Reference Implementations (LRIs) active.
- Integration model: Open standard (ISO 18013-5, W3C VC, OpenID4VC). Any RP can integrate.
- Key insight: eIDAS 2.0 is the closest architectural parallel to what "Fill with UAE PASS" aspires to be. UAE PASS should monitor eIDAS 2.0's field adoption patterns, consent UX, and RP onboarding mechanics.

#### India DigiLocker
- Architecture: Government-backed document repository. Issuers push documents to DigiLocker; users share via API or QR. URI-addressable documents.
- Data: Academic certificates, driving licence, vehicle registration, insurance, national ID (Aadhaar-linked), COVID certificates, and 1,500+ issuer document types.
- Trust: Government-issued documents; not attribute-level eSeal — document-level trust. SP receives a link to a government-hosted document, not an extracted field payload.
- UX: "Pull Document from DigiLocker" flow; also share via QR on physical government counters.
- Integration model: SP must be registered with DigiLocker. Over 9,000 registered requesters as of 2025.
- Scale: 300M+ registered users; 6+ billion documents stored.
- Limitation: Field-level extraction is not the primary model. DigiLocker is primarily a document store and sharer, not an attribute extraction service. Form pre-fill requires SP-side parsing of returned documents.

#### Estonia e-ID / X-Road
- Architecture: e-ID (physical smart card + mobile ID) as authentication layer. X-Road data exchange layer connects government registries. Form pre-fill happens via X-Road queries at service login.
- Data: Residency, tax data, health data, company registry data — pulled from authoritative registries at point of use.
- Trust: Registry-authoritative; X-Road provides audit trail. Not VC-based but highly trusted.
- UX: Deeply integrated into every Estonian government service. Citizens expect forms to be pre-filled.
- Key insight: Estonia's model shows that government-mandated pre-fill (not opt-in) is achievable at population scale when the regulatory environment is supportive. UAE PASS operates in a similarly centralised regulatory environment under TDRA — this is an enabler, not a constraint.

---

### 1.6 Browser Extensions — Comparable Concepts

| Extension | Mechanism | Relevance |
|-----------|-----------|-----------|
| MetaMask | Injects `window.ethereum` into page; dApp detects and calls it; user signs transactions | Architecture analogy: injected script model. UAE PASS extension could inject a `window.uaepass` object for web integration. |
| LinkedIn AutoFill | Deprecated (2018). LinkedIn provided a button that filled name, email, phone, employer, job title from LinkedIn profile. Removed after security researchers showed cross-site data leakage risks. | Critical cautionary tale: the LinkedIn autofill button was exploited to exfiltrate user data to third-party sites without user knowledge. Any UAE PASS JS SDK must learn from this failure. |
| Honey / Capital One Shopping | Browser extension injects coupon-finding UI at checkout. Non-identity but shows extension overlay UX pattern at scale. | UX pattern reference for non-intrusive extension overlay design. |
| Okta FastPass / enterprise SSO extensions | Enterprise IdP extensions that detect SP login pages and inject SSO. | Architecture analogy for IdP-side extension detecting form context. |

**LinkedIn AutoFill post-mortem (2018)** — directly relevant to the JS SDK form factor:
- LinkedIn offered a `<button data-linkedin-autofill>` that websites embedded. LinkedIn's JS would fill name, email, phone, employer, title into form fields.
- Security researcher Jack Cable discovered that any website could invoke the button, and LinkedIn's `postMessage` implementation did not validate the origin of the receiving frame.
- Result: Third-party iframes could silently capture the autofilled data by embedding the LinkedIn button in an invisible iframe.
- Fix: LinkedIn restricted to whitelisted partner domains, then deprecated the feature entirely.
- UAE PASS lesson: Any JS SDK model must implement strict `postMessage` origin validation, CORS, and explicit user consent at the moment of fill — not pre-authorised fill. The LinkedIn failure is the canonical risk case for this form factor.

---

### 1.7 Mobile OS Autofill Frameworks

**iOS AutoFill Provider API (iOS 12+)**
- Any app can register as an AutoFill credential provider via an App Extension (`AutoFillCredentialProviderExtension`).
- When the user focuses a form field in any app or mobile browser, iOS presents a suggestion bar above the keyboard. Registered providers can inject suggestions.
- The extension runs in a sandboxed process; it receives the `ASCredentialServiceIdentifier` (the app bundle ID or website URL requesting fill) and returns `ASPasswordCredential` or `ASOneTimeCodeCredential`.
- iOS 17+ introduced `ASPasskeyCredential` for passkey-based autofill.
- For identity/address fields (not passwords): iOS presents the "My Card" contact card for name/address. Third-party providers cannot currently inject address/identity suggestions via the standard provider API — only passwords and one-time codes.
- UAE PASS implication: UAE PASS could register as a password/passkey provider on iOS. For address/identity field fill on iOS, the standard extension API is limited. A UAE PASS keyboard extension (more invasive) or a browser extension within Safari (feasible via Safari Web Extensions) are alternative paths.

**Android Autofill Framework (Android 8+)**
- `AutofillService` API: Apps register as autofill services in Settings > Accessibility > Autofill Service. Only one autofill service can be active at a time (system-level).
- The active service receives a `FillRequest` with `AssistStructure` (the view hierarchy of the current form) and returns a `FillResponse` with one or more `Dataset` objects.
- Android 11+ introduced `InlineSuggestionsRequest` for inline (keyboard-chip) suggestions.
- Unlike iOS, Android's autofill API fully supports identity/address fields — it is not limited to passwords.
- The active autofill service gets access to the full view hierarchy of any app requesting fill. This is a broad permission that must be prominently disclosed to users.
- UAE PASS implication: UAE PASS could register as the system autofill service on Android, giving it fill capability across all apps and browsers. This is technically feasible and architecturally powerful, but requires users to explicitly switch their autofill service from Google to UAE PASS — a significant adoption barrier.

---

## 2) The "Fill with UAE PASS" Product Concept

### Form Factor A: Browser Extension / Plugin

**Architecture**
The extension comprises three components:
1. **Content Script**: Injected into every web page. Scans the DOM for fillable form fields. Classifies fields using `autocomplete` attribute, field name/id heuristics, label text, and placeholder analysis. Adds a subtle UAE PASS icon inside or beside detected identity fields (similar to 1Password's inline icon).
2. **Background Service Worker**: Communicates with the UAE PASS backend (or locally cached data) to retrieve the user's verified attribute set. Manages session tokens and refresh.
3. **Popup UI**: The extension icon in the browser toolbar. Shows user identity status, recent fill history, and settings. Also used for initial authentication / linking of UAE PASS account.

**Authentication Model**
- First use: User opens extension popup → redirected to UAE PASS login (UAE PASS app QR scan or OTP). Returns an OAuth-style session token stored in extension's `chrome.storage.local` (encrypted).
- Subsequent use: Session token validates silently. If expired, re-authentication required.
- Biometric confirmation at fill (optional): Each fill action could require a biometric re-confirmation via the UAE PASS mobile app (push notification model). This is the highest-trust model but highest friction.

**Field Detection and Matching**
```
Field Classification Heuristic (illustrative):
  autocomplete="given-name" → Full Name (First)
  autocomplete="family-name" → Full Name (Last)
  autocomplete="name" → Full Name (EN)
  autocomplete="bday" → Date of Birth
  autocomplete="country" → Nationality
  autocomplete="tel" → Phone (not in DV scope)
  name/id contains "eid", "emirates", "id-number" → Emirates ID Number
  name/id contains "passport" → Passport Number
  name/id contains "visa", "residency" → Residence Visa fields
  name/id contains "expiry", "expiration" → Document expiry (context-dependent)
```

**Consent UX**
- On field click: UAE PASS icon appears inline. User clicks icon → mini popup shows "Fill with UAE PASS?" with the specific field to be filled and its source document (e.g., "Emirates ID — verified by ICP").
- User clicks "Fill" → field populates. A subtle "Verified" badge appears beside the filled field (optional, depends on website CSS compatibility).
- Alternative: Whole-form fill trigger. User clicks extension icon in toolbar → UAE PASS scans the entire page, shows all detected fields with proposed values, user reviews and confirms → all fields populate simultaneously.

**Browser Support**
| Browser | Extension API | Status |
|---------|--------------|--------|
| Chrome | Manifest V3 (MV3); Chrome Web Store distribution | Primary target; 65%+ global browser share |
| Edge | Chromium-based; same MV3 extension runs | Secondary; important for enterprise/government portals |
| Firefox | WebExtensions API (compatible with Chrome MV3 with minor adjustments); Firefox Add-ons Store | Tertiary; important for privacy-conscious users |
| Safari | Safari Web Extensions (macOS/iOS 15+); requires App Store distribution via macOS app wrapper | Important for UAE iPhone-dominant market; requires separate build and Apple review |
| Brave | Chromium-based; same MV3 extension runs | Bonus; no extra development |

**Safari note**: Safari Web Extensions require a native macOS app as the container. Distribution is via App Store, not a standalone extension store. This adds developer cost but is strategically important given UAE's high iPhone adoption rate.

**Trust and Security Model**
- Data stored: Extension stores user's verified attribute set locally (in `chrome.storage.local`, encrypted). Data is sourced from UAE PASS backend once per session and cached.
- Data never sent to the website's server by the extension directly. The extension fills HTML fields client-side. The website's own form submission sends the data — extension has no involvement post-fill.
- No persistent tracking: Extension must not log which websites the user visits or fills. This is a PDPL obligation and a user trust requirement.
- HTTPS-only operation: Extension should refuse to fill on HTTP pages (risk of MITM interception of filled data).
- Risk: A malicious website could attempt to read filled values from input fields before user submission. This is standard web behaviour — not an extension-specific risk — but UAE PASS branding means any data breach on a malicious site becomes a UAE PASS reputational incident. Mitigation: user education, website trust indicators.

**Comparable products**: 1Password browser extension (architecture reference), Bitwarden (open-source reference), Dashlane Web (UX reference for confidence scoring).

---

### Form Factor B: Mobile OS Autofill Integration

**iOS Implementation Path**

Option 1 — AutoFill Credential Provider Extension (Password/Passkey scope only):
- UAE PASS registers as a credential provider. On login forms, UAE PASS can suggest UAE PASS-linked passwords or passkeys. This does not cover identity/address fields.
- Effort: Low-Medium. Standard iOS 12+ API.
- Coverage: Password + passkey fields only. Limited for form-fill use case.

Option 2 — Safari Web Extension (iOS 15+):
- UAE PASS ships a Safari Web Extension within the UAE PASS iOS app. Provides the same content-script-based field detection as the desktop browser extension.
- User enables the extension in Safari Settings. Extension then injects into Safari pages.
- Effort: Medium-High. Separate extension codebase + Apple review cycle.
- Coverage: Safari on iOS only. Does not help with in-app WebViews or native app forms.

Option 3 — UAE PASS Keyboard Extension (most invasive):
- A custom iOS keyboard extension that has a "UAE PASS" quick-fill key. When focused on a compatible field, the keyboard shows UAE PASS suggestions.
- Effort: High. Keyboard extensions have strict performance requirements (must load in <12ms) and no network access in the keyboard process.
- Coverage: Any app, any field.
- Privacy concern: Keyboard extensions have "full access" permission which enables network calls — this triggers App Store review scrutiny and user trust concerns ("Why does my ID wallet need full keyboard access?").

**Recommended iOS path**: Option 2 (Safari Web Extension) for web forms as MVP, with Option 1 (Credential Provider) for password/passkey fields as a baseline. Option 3 is not recommended due to user trust and privacy perception risks.

**Android Implementation Path**

Option 1 — `AutofillService` API (System-Level):
- UAE PASS registers as the system autofill service. User must switch from Google Autofill to UAE PASS Autofill in Android Settings.
- Coverage: All apps, all browsers, native app forms.
- Data: UAE PASS can fill identity, address, and any field type — the Android API has no restrictions comparable to iOS.
- Effort: Medium. Well-documented API; 1Password, Bitwarden, and Dashlane have published open implementations.
- Adoption barrier: Users must actively switch their autofill service. Most users do not know this setting exists. Must be promoted within UAE PASS app onboarding.

Option 2 — Accessibility Service (not recommended):
- Some autofill apps historically used Android's Accessibility API as a fallback for older Android versions.
- As of Android 8+, the `AutofillService` API is the correct mechanism.
- Accessibility Service usage for autofill is against Google Play policy and should not be considered.

Option 3 — Chrome Custom Tab with Autofill:
- For web-only coverage, UAE PASS can provide a browser extension for Chrome on Android (same as desktop Chrome extension with minor adjustments).
- Coverage: Chrome browser only, not native app forms.
- Effort: Low (reuse desktop extension codebase).

**Recommended Android path**: Option 1 (AutofillService) as the strategic target. Option 3 (Chrome extension) as the interim/MVP while the AutofillService implementation matures.

**Field matching on mobile** follows the same heuristic model as the browser extension, but operating on `AssistStructure` (Android's view hierarchy representation) rather than DOM. Key field signals: `View.setAutofillHints()` (the Android equivalent of `autocomplete` HTML attribute), view `contentDescription`, view resource ID heuristics.

---

### Form Factor C: JavaScript SDK / Web Button ("Fill with UAE PASS")

This is the highest-reach, lowest-barrier form factor for website operators. It is the closest analogue to "Continue with Google."

**Architecture**

```
Website operator embeds:
<script src="https://sdk.uaepass.ae/fill/v1.js"></script>
<button class="uaepass-fill-btn" data-fields="name,eid,dob,nationality">
  Fill with UAE PASS
</button>
```

**Flow — Mobile (primary)**
1. User visits a website with the "Fill with UAE PASS" button (on their phone or desktop).
2. User taps the button.
3. On mobile: UAE PASS app opens via deep link (`uaepass://fill?session=<token>&fields=name,eid,dob`). The session token is generated server-side by the UAE PASS SDK backend and is a one-time, short-TTL opaque identifier (QR hygiene rules apply: no PII in token, unique per request, expires in 120 seconds).
4. UAE PASS app presents a consent screen listing the requested fields and their source documents.
5. User authenticates (biometric) and approves.
6. UAE PASS backend stores the approved attribute payload against the session token.
7. The website's JS polls or receives a webhook callback that the session is complete.
8. UAE PASS SDK JS retrieves the attribute payload from the UAE PASS backend using the session token.
9. SDK JS fills the website's form fields with the returned attributes.
10. SDK JS posts a `verified` event to the page so the website can show a trust badge.

**Flow — Desktop (cross-device)**
1. User visits a website on desktop.
2. User clicks "Fill with UAE PASS".
3. SDK generates a session token and renders a QR code in a modal.
4. User scans QR with UAE PASS app on their phone.
5. UAE PASS app presents consent screen → user approves.
6. SDK's polling loop detects session completion → fills the form.

**Architectural diagram**
```
[Website] → [UAE PASS SDK JS] → [UAE PASS SDK Backend]
                                      ↑ session init
                                      ↓ attribute payload
[UAE PASS App] ← deep link / QR ← [UAE PASS SDK Backend]
[UAE PASS App] → consent + biometric → [UAE PASS SDK Backend]
```

**Security architecture**

The LinkedIn AutoFill incident (2018) is the canonical risk for this model. The following controls are mandatory:

1. **Strict `postMessage` origin validation**: SDK JS must never relay attribute data via `postMessage` without validating the receiving window's origin against the session's registered domain.
2. **Session token binding**: Each session token is bound to the originating domain at creation time. The token cannot be redeemed by a different domain.
3. **No open-web model by default**: Despite the goal of "no full API integration required," the SDK must require domain registration (a lightweight process: email verification + domain confirmation, not the full SP onboarding). This prevents abuse by bad actors who could phish users into consenting to data extraction on spoofed sites.
4. **Attribute scope declaration**: The website declares which fields it wants at SDK initialisation time. The UAE PASS app shows exactly those fields in the consent screen. The backend enforces that only those fields are returned.
5. **HTTPS-only**: SDK refuses to load on HTTP origins.
6. **Rate limiting**: Session creation is rate-limited per domain to prevent enumeration or bulk extraction attempts.
7. **Audit log**: Every consent event is logged to the user's Sharing History in UAE PASS, regardless of form factor.

**"No full API integration" vs. lightweight registration**
The JS SDK model can lower the barrier dramatically compared to full SP API integration — but "zero registration" creates unacceptable fraud and phishing risks. The recommended model is a lightweight developer portal registration (similar to Google Cloud Console or Stripe dashboard):
- Developer provides: company name, domain(s), use case description, contact email.
- UAE PASS validates domain ownership (DNS TXT record or file upload).
- Developer receives a publishable API key embedded in their SDK snippet.
- No legal contract, no onboarding SLA, no integration testing required.
- Full SP API integration remains for SPs who want deeper integration, webhook callbacks, stored sharing consents, and access to the full document sharing flow.

**Returned data format**

```json
{
  "session_id": "opaque-uuid",
  "verified_at": "2026-04-01T09:00:00Z",
  "attributes": {
    "full_name_en": {
      "value": "Mohammed Al Rashidi",
      "source_document": "Emirates ID",
      "issuer": "ICP",
      "issuer_did": "did:uaepass:icp",
      "verified": true
    },
    "date_of_birth": {
      "value": "1988-03-15",
      "source_document": "Emirates ID",
      "issuer": "ICP",
      "verified": true
    },
    "nationality": {
      "value": "AE",
      "source_document": "Emirates ID",
      "issuer": "ICP",
      "verified": true
    }
  },
  "eseal_proof": "base64-encoded-CAdES-proof"
}
```

The `eseal_proof` field allows the website (if it chooses) to independently verify the data against the ICP public key — the same offline verification model as the full SP API. This is the trust differentiator that Google and Apple cannot replicate.

---

### Form Factor D: QR-Based Universal Filler

**Architecture**
- The website/app displays a static or dynamically-generated QR code labelled "Fill with UAE PASS" — «أكمل بـ UAE PASS».
- The QR encodes a UAE PASS deep link: `uaepass://fill?session=<token>` where the token is generated by either:
  - **Server-side** (preferred): The website's backend calls the UAE PASS SDK API to create a session and embed the resulting token in the QR.
  - **Client-side with no backend** (lowest barrier): A static QR that encodes a UAE PASS universal fill URL. The fill fields are declared in the URL parameters. This is the "no SDK, no registration" model — but with higher abuse risk.
- User scans QR → UAE PASS app opens → consent screen → user approves → UAE PASS app fills the originating form.

**On-device vs. cross-device fill**
- If the user scans on their phone while viewing the website on the same phone: deep link opens UAE PASS app, fill is completed within UAE PASS app, result returned via deep link callback or device clipboard injection.
- If the user scans on their phone while viewing on desktop: QR is the cross-device bridge (same as Form Factor C desktop flow).

**In-person use case**: A bank branch teller's screen displays a "Fill Application Form — Fill with UAE PASS" QR. Customer scans with their UAE PASS app. App shows consent screen for the bank's KYC fields. Customer approves. Bank's terminal receives the filled data. This eliminates paper form-filling entirely.

**No-SDK model (static QR)**
- A website could generate a QR encoding: `https://fill.uaepass.ae/?fields=name,eid,dob&callback=https://website.com/uaepass-callback&nonce=random`
- Advantage: Zero integration required — any website can render this QR manually.
- Disadvantage: Difficult to validate callback URL authenticity; phishing risk if the callback URL is not validated by UAE PASS backend.
- Mitigation: UAE PASS validates callback domains against a registered allowlist. Registration is still required, but the QR generation itself requires no server-side SDK.

**Comparison to WeChat / Asian super-app QR models**
- WeChat's "Scan to Fill" is a widely-adopted model in China: WeChat Mini Programs use QR-initiated flows for government service form pre-fill.
- Alipay, Grab, GovTech Singapore's Singpass app all use QR-initiated flows as the mobile bridge for web-to-app form fill.
- The QR model is well-understood by smartphone-first users in the UAE/GCC. Adoption friction is lower than asking users to install a browser extension.

---

### Form Factor E: NFC / Tap-to-Fill

**Architecture**
NFC tap-to-fill operates in two modes:

**Mode 1 — Phone-to-Terminal (in-person)**
- UAE PASS app holds a short-lived NFC Data Exchange Format (NDEF) record containing a session deep link.
- User taps their phone to an NFC-capable terminal (bank counter, government kiosk, hospital reception desk).
- Terminal reads the NDEF record, initiates a UAE PASS fill session, displays the consent confirmation screen to the user on their phone.
- Terminal receives the attribute payload.
- This is architecturally identical to the QR model but uses NFC as the transport instead of camera/QR.

**Mode 2 — Phone-to-Phone (peer-to-peer)**
- Less relevant for form-fill; more relevant for document sharing between individuals.

**ISO 18013-5 mDL (Mobile Driving Licence) relevance**
- ISO 18013-5 defines an NFC and BLE-based proximity presentation protocol for mobile driving licences.
- The protocol uses device engagement (QR or NFC), device retrieval (BLE or NFC data transfer), and selective disclosure.
- If UAE PASS adopts ISO 18013-5 for its Driving Licence document, the NFC tap infrastructure is effectively already defined by the standard.
- eIDAS 2.0 wallets are implementing ISO 18013-5 and OpenID4VP for proximity flows.
- UAE PASS should evaluate ISO 18013-5 adoption — it would make UAE PASS interoperable with global identity infrastructure (airports, hotels, rental car counters accepting mDL).

**In-person use cases**
| Setting | Field Required | Source Document |
|---------|---------------|-----------------|
| Bank branch KYC | Name, EID number, DOB, nationality | Emirates ID |
| Hospital registration | Name, DOB, insurance card, nationality | EID + Health Insurance |
| Government counter | Name, EID number, visa status | EID + Residence Visa |
| Hotel check-in | Name, passport number, nationality | Passport |
| Rental car | Driving licence number, categories, expiry | Driving Licence |
| SIM registration | Name, EID/passport, DOB | EID or Passport (TRA requirement) |

**Device requirements**
- UAE PASS app must support NFC (available on all modern iPhones [XS+] and Android [4.4+] with NFC chip).
- Terminal must have NFC reader hardware.
- For government counters and bank branches: terminal integration is a separate procurement and IT project.
- NFC tap-to-fill is the highest-value in-person form factor but requires physical infrastructure rollout, making it the longest timeline to scale.

---

## 3) Trust and Verification Differentiation

### The Core Differentiator: Cryptographic Provenance

The fundamental distinction between "Fill with UAE PASS" and every consumer autofill product is the answer to the question: **"Where did this data come from, and can you prove it?"**

| Autofill Product | Data Origin | Verifiability by Recipient | Cryptographic Proof |
|-----------------|-------------|---------------------------|---------------------|
| Chrome Autofill | User typed it | None | None |
| Apple AutoFill | User's Contacts card | None | None |
| 1Password / Dashlane | User typed or OCR'd from photo | None | None |
| Sign in with Google | Google Account (user-curated) | API trust (Google's word) | JWT signature (IdP trust only) |
| Sign in with Apple | Apple ID (user-curated) | API trust (Apple's word) | JWT signature (IdP trust only) |
| Singpass MyInfo | Government registry | API trust (Singpass's word) | None (no offline proof) |
| eIDAS 2.0 Wallet | Member State government issuer | Issuer public key (offline) | W3C VC / mdoc issuer signature |
| **UAE PASS DV** | **Government issuer (ICP, MoHRE, etc.)** | **Issuer eSeal (offline)** | **CAdES/PAdES eSeal — independently verifiable** |

UAE PASS's eSeal model enables a recipient SP to take the returned attribute payload, extract the eSeal proof, and independently verify it against the ICP public key — without calling any UAE PASS API. This is the same trust model as a physical stamp on a government letter: the recipient can verify the seal without calling the issuing authority.

No consumer autofill product offers this. Even Singpass MyInfo, which is government-sourced, relies on API trust — the SP must trust that Singpass returned genuine data, with no independent verification mechanism.

### Communicating Trust Differential to Users

**User-facing messaging (EN/AR pairs)**

| Context | English | Arabic |
|---------|---------|--------|
| Button label | Fill with UAE PASS | «أكمل بـ UAE PASS» |
| Trust badge (post-fill) | Verified by UAE Government | «موثق من قِبل حكومة الإمارات» |
| Consent screen subtitle | Government-verified data from your documents | «بيانات موثقة حكومياً من مستنداتك» |
| Data source label | Emirates ID — verified by ICP | «بطاقة الهوية — موثقة من قِبل الهيئة الاتحادية للهوية» |
| Trust explanation tooltip | This information was issued by [Issuer] and verified with a government eSeal. | «صدرت هذه المعلومات من [الجهة] وتم التحقق منها بخاتم إلكتروني حكومي.» |
| For website operators | Your user's identity is government-verified. No document checks required. | (B2B messaging; AR not required) |

### Communicating Trust to Website Operators

Three levels of trust signal for website operators:
1. **Basic**: UAE PASS SDK returns attribute payload with `"verified": true`. Website trusts UAE PASS's assertion (API trust model — same as Singpass MyInfo).
2. **Standard**: SDK payload includes issuer metadata (`issuer`, `issuer_did`, `verified_at`). Website can display "Verified by ICP" badge to the end user.
3. **Advanced (eSeal proof)**: SDK payload includes `eseal_proof` (CAdES/PAdES). Regulated industries (banks, telecoms) can independently verify the cryptographic proof against published issuer public keys — no UAE PASS API call required at verification time.

This tiered trust model means websites can adopt "Fill with UAE PASS" at the level of sophistication appropriate to their compliance requirements.

---

## 4) Go-to-Market Models

### Overview by Form Factor

| Form Factor | Primary User | Distribution Channel | Monetisation | Adoption Barrier | Regulatory Requirement |
|------------|-------------|---------------------|-------------|-----------------|----------------------|
| A. Browser Extension | UAE residents (power users) | Chrome Web Store, Firefox Add-ons, App Store (Safari) | Government-funded (no cost) | Install step; user inertia | TDRA product approval; DDA UX approval |
| B. Mobile OS Autofill | UAE residents (all smartphone users) | Pre-installed in UAE PASS app (no separate install) | Government-funded | Change system autofill service (Android); enable extension (iOS) | TDRA product approval; Apple / Google platform review |
| C. JS SDK / Web Button | Website operators | Developer portal (self-serve) | Freemium: free tier (X fills/month/domain), paid tier (volume, eSeal proof, analytics) | Domain registration; button integration | Lightweight registration; TDRA policy for data scope |
| D. QR Universal Filler | UAE residents at any website | Built into UAE PASS app (scan from camera) | Government-funded (citizen-side) | None — users already have UAE PASS app | TDRA policy; no separate approval needed if using existing QR infrastructure |
| E. NFC Tap-to-Fill | UAE residents at physical counters | UAE PASS app NFC feature | Government-funded or terminal operator fee | Terminal hardware; enterprise procurement | TDRA + site-specific authority approval |

### Monetisation Analysis

**Government-funded model (current DV posture)**
- UAE PASS is a sovereign infrastructure platform. The national interest argument for government-funded "Fill with UAE PASS" is strong: reducing KYC friction increases economic productivity, reduces fraud, and supports UAE's paperless government goals.
- Precedent: Singpass MyInfo is funded by the Singapore government and provided free to citizens and SPs.
- Risk: If TDRA funds the service, commercial SPs get a subsidised competitive advantage. This may create equity concerns for SPs who built their own KYC infrastructure.

**Transaction fee model**
- Charge SPs per successful fill (e.g., AED 0.50 per verified fill). Analogous to payment transaction fees.
- Advantage: Aligned incentives — UAE PASS earns only when value is delivered.
- Disadvantage: SPs will build around it (ask users to enter data manually if they have cheap manual data entry alternatives).
- Comparable: Stripe charges per payment transaction. DigiLocker charges for commercial requesters in India.

**Subscription / API tier model**
- Free tier: JS SDK with basic attributes (name, EID number, DOB, nationality) — lightweight registration required.
- Professional tier: Extended attributes (address, employer, education), eSeal proof, analytics dashboard, webhook callbacks — monthly subscription.
- Enterprise tier: Full SP API integration, custom attribute sets, SLA, dedicated support — annual contract.
- This model is closest to how Google Maps API, Twilio, and Stripe operate — a developer-friendly freemium funnel.

**Recommended model**: Hybrid. The QR-based fill and mobile OS autofill are government-funded (citizen value). The JS SDK follows a freemium subscription model for commercial operators. The full SP API remains on a contract basis as today. This creates a natural upgrade path: operator starts with free JS SDK → upgrades to professional tier as volume grows → graduates to full SP API integration when they need deep integration features.

---

## 5) Competitive Landscape in UAE / GCC

### UAE Current State

| Domain | Current Form-Fill Method | Gap |
|--------|------------------------|-----|
| UAE Government Portals (Federal: moi.gov.ae, u.ae, GDRFA) | UAE PASS SSO fills name and email from login; full form still requires manual entry | No attribute pre-fill beyond basic login identity |
| Dubai Smart Government portals (DubaiNow, etc.) | UAE PASS login; minimal pre-fill | No document-level field extraction |
| Banks (ENBD, ADCB, ADIB, FAB) | Manual entry; some mobile banking apps have address recall from previous applications | No government-verified pre-fill; KYC data is re-keyed |
| Telcos (Etisalat/e&, du) | Copy ID manually; some stores use staff-assisted scanning | No digital pre-fill; physical ID card scanning at point of sale |
| Insurance portals | Manual entry + document upload | No verified pre-fill |
| Hospital / clinic registration | Paper forms or manual digital entry | No identity pre-fill |
| e-Commerce checkout | Manual entry | No identity/address pre-fill from government source |

**Key finding**: No UAE-based organisation currently offers a cross-sector, government-verified form pre-fill product. The market gap is genuine and significant.

### GCC Regional Landscape

| Country | Platform | Comparable Feature | Status |
|---------|---------|-------------------|--------|
| Saudi Arabia | Absher / Nafath | Nafath provides authentication (SSO equivalent); no form pre-fill API for commercial SPs | Authentication-only; no attribute sharing layer |
| Saudi Arabia | Absher (for government services) | Some government portals auto-fill from GOSI / NIC data | Government-internal only; not available to commercial SPs |
| Bahrain | iDQ (National Digital Identity) | Authentication via Bahrain ID; limited attribute sharing | Early stage; authentication focus |
| Jordan | JISA (Jordan Identity and Security Authority) | National ID-based SSO; no commercial SP pre-fill | Government use only |
| Oman | Muscat Digital Government Authority | Oman ID / eGovernment SSO | Authentication-only |
| Qatar | Metrash2 | Government service app; no commercial SP pre-fill | Government-internal |
| Kuwait | No equivalent | Manual processes dominant | — |

**Regional conclusion**: UAE PASS is the most advanced national digital identity platform in the GCC. No GCC country has a government-verified, commercial-SP-facing form pre-fill product. "Fill with UAE PASS" would be the first in the region and could become a regional model.

**Global context**: Singapore (Singpass MyInfo) and Estonia (X-Road + e-ID) are the international benchmarks for government-verified form pre-fill at scale. UAE PASS's eSeal model is architecturally superior to Singpass in terms of cryptographic provenance. The opportunity is to build the world's most trusted government-backed form pre-fill product.

---

## 6) Recommended Product Strategy

### Priority Ranking of Form Factors

| Rank | Form Factor | Rationale | Timeline |
|------|------------|-----------|----------|
| 1 | C — JS SDK / Web Button | Highest reach; zero user install required; operator-controlled; fastest to demonstrate value; analogous to proven "Continue with Google" model | 6–9 months to MVP |
| 2 | D — QR Universal Filler | Leverages existing UAE PASS app and QR infrastructure; zero new user behaviour required; works on any website without operator integration; excellent for physical/in-person hybrid | 3–6 months (builds on Form Factor C infrastructure) |
| 3 | B — Mobile OS Autofill (Android AutofillService first) | Largest ambient surface area; no website operator action required; fills native app forms as well as web | 9–12 months |
| 4 | A — Browser Extension | High-value for power users; enables desktop web fill without SDK integration by operator; important for enterprise and B2B portals | 9–12 months (parallel with Android) |
| 5 | E — NFC Tap-to-Fill | Highest value per transaction (in-person KYC); longest infrastructure dependency; enterprise/government procurement cycle | 18–24 months |

### MVP Product Concept

**"Fill with UAE PASS" MVP = Form Factor C (JS SDK) + Form Factor D (QR, cross-device desktop)**

The MVP is not a browser extension, not an OS integration, and not an NFC solution. It is:

1. A lightweight JavaScript SDK (`fill.uaepass.ae/v1.js`) that any website can embed with a single `<script>` tag.
2. A "Fill with UAE PASS" button rendered by the SDK.
3. A deep link / QR flow that opens the UAE PASS app.
4. A consent screen inside UAE PASS app (bilingual EN/AR, eSeal provenance displayed).
5. A secure attribute payload returned to the website's form fields.
6. An audit entry in the user's Sharing History.

**MVP attribute scope** (aligned with existing Form Pre-Fill BRD Phase 1):
- Full name (EN)
- Emirates ID number
- Date of birth
- Nationality
- Gender

**Why this is the right MVP:**
- Zero new user behaviour: Users already have UAE PASS app installed (mandatory for UAE residents accessing government services).
- Minimal operator integration: One `<script>` tag + lightweight domain registration.
- Leverages existing DV infrastructure: Session management, consent screens, Sharing History, eSeal proof — all exist or are in development.
- Demonstrates the trust differentiation immediately: The consent screen shows "Verified by ICP" — something Google and Apple can never show.
- Creates a flywheel: More websites integrate the button → more citizens use it → UAE PASS becomes the identity layer for the UAE web.

### Relationship to SP Form Pre-Fill BRD

| Dimension | SP Form Pre-Fill (BRD) | "Fill with UAE PASS" (This Concept) |
|-----------|----------------------|--------------------------------------|
| Integration model | Full SP API contract; onboarding SLA | Lightweight domain registration; self-serve |
| Target audience | Existing registered SPs (banks, telecoms, insurers) | Any website operator globally |
| Attribute scope | Deep (employment, address, professional licences) | Progressive (basic identity MVP; expandable) |
| Trust depth | Full eSeal proof; legal data sharing agreement | Tiered (basic → eSeal proof on paid tier) |
| User consent | Per-sharing-request consent screen | Per-fill consent screen (same model) |
| Sharing History | Yes | Yes |
| Timeline | 2026 (phased delivery) | 6–9 months for MVP (partially parallel) |
| Dependency | Requires ICP structured payload confirmation | Same dependency (shared prerequisite) |

**Key relationship**: The SP Form Pre-Fill BRD and "Fill with UAE PASS" share the same foundational prerequisites:
- ICP structured payload confirmation (Phase 0 audit)
- TDRA attribute access policy
- DDA consent screen design
- Sharing History data model

They are not competing efforts — they serve different audience segments (deep-integrated SPs vs. the open web) using the same underlying infrastructure. Building them in parallel is feasible and strategically sound. The JS SDK can be a lightweight front-end on top of the same attribute extraction service being built for the SP API.

### Is This a Feature or a Standalone Product?

**Verdict: Standalone product, operated as a platform layer within UAE PASS.**

Arguments for "feature within UAE PASS app":
- Uses the same document store, consent model, and eSeal infrastructure.
- The citizen-facing consent screen is just another UAE PASS screen.
- The QR form factor is already how UAE PASS works.

Arguments for "standalone product":
- The JS SDK and developer portal are net-new infrastructure independent of the UAE PASS app.
- The target customer for the SDK is website operators, not citizens — a B2B product layer.
- Monetisation (if pursued) requires a separate product identity and billing infrastructure.
- The brand "Fill with UAE PASS" should be distinct from "UAE PASS" as the authentication product — analogous to how "Google Pay" and "Sign in with Google" are distinct even though they share Google account infrastructure.
- It has its own developer ecosystem, documentation, and go-to-market motion.

**Recommendation**: Position "Fill with UAE PASS" as a **platform product** — a product that UAE PASS (the citizen app) supports as a form factor, and that website operators/enterprises consume via a developer-facing SDK and portal. Create a separate product identity for the operator-facing layer while keeping the citizen UX within the UAE PASS app. This mirrors how Apple operates: "Sign in with Apple" is a platform product, but the citizen interaction happens within the iPhone's standard authentication flow.

### The 3 Biggest Risks

**Risk 1: The LinkedIn Autofill Problem**
Malicious websites embed the "Fill with UAE PASS" button and use it to phish government-verified identity data from users who are tricked into consenting. A single high-profile phishing incident using UAE PASS branding would cause severe reputational damage to the national identity platform.

Mitigation: Domain registration is non-negotiable (even if lightweight). `postMessage` origin validation is non-negotiable. HTTPS-only is non-negotiable. A trust indicator system that shows users the verified domain they are filling data into (similar to how browsers show HTTPS padlock + domain name) must be part of the consent screen design.

**Risk 2: TDRA Attribute Access Policy Fragmentation**
The current SP onboarding model has TDRA as the policy authority for which attributes SPs may access. Extending attribute access to thousands of website operators via a self-serve SDK could conflict with TDRA's desire to maintain policy control over attribute access. If TDRA requires each new website operator to go through the existing SP approval process, the SDK's "low-barrier integration" value proposition collapses.

Mitigation: Engage TDRA early to design a tiered policy framework. Basic attributes (name, EID number, DOB, nationality) could be approved for any domain-verified operator as a blanket policy instrument. Sensitive attributes (address, employer, salary) remain behind the full SP approval process. This mirrors how OAuth scopes work — public scopes vs. restricted scopes.

**Risk 3: ICP Structured Payload Dependency**
Both the SP Form Pre-Fill BRD and this concept depend on ICP confirming that its document payloads contain structured, machine-readable field data (not just PDF renderings). If the Phase 0 engineering audit reveals that ICP documents are PDF-only, the entire attribute extraction architecture requires renegotiating with ICP to add structured data fields to their issuance pipeline. This could add 6–12 months to the foundational work.

Mitigation: Accelerate the Phase 0 structured payload audit immediately (engineering inspection of existing VP payloads — this takes hours, not weeks). If PDF-only, initiate ICP negotiations in parallel with other workstreams rather than waiting for confirmation.

---

## 7) Clarifying Questions for PM

The following five questions would most significantly change the product direction if answered:

**Q1: What is TDRA's appetite for an open-web / self-serve SDK model?**

The most consequential policy question. If TDRA requires every website operator to go through the existing SP onboarding process, Form Factor C (JS SDK) is effectively killed. If TDRA is willing to create a tiered policy framework (blanket approval for basic attributes at domain-verified operators), the SDK model becomes viable at scale. PM should initiate a TDRA strategic conversation before committing engineering resources to SDK architecture.

**Q2: Does UAE PASS have a sovereign restriction on where attribute data can be processed, and does that affect a global JS SDK?**

The JS SDK would be accessible to websites globally (any website can embed the button). When a UAE resident fills a form on a UK e-commerce site or a US university application, the UAE PASS backend processes a consent transaction. Does UAE data sovereignty law (and PDPL) permit attribute data to be shared with non-UAE registered operators? The answer determines whether the SDK is a UAE-market product or a global product.

**Q3: Is there an existing or planned UAE PASS developer portal and SDK infrastructure?**

If a developer portal, API key management system, and webhook infrastructure already exist (even partially) for the current SP integration model, the JS SDK can reuse significant infrastructure. If these do not exist, the SDK requires building net-new developer tooling — which is a substantial engineering investment independent of the attribute extraction work. PM should establish current state with engineering before scoping SDK timelines.

**Q4: What is the target penetration metric for "Fill with UAE PASS" — usage by citizens or adoption by websites?**

These require different product strategies. Maximising citizen usage (fill events) favours the QR and mobile OS autofill form factors (reach existing UAE PASS users, no website action needed). Maximising website adoption favours the JS SDK (developer-facing marketing, documentation, community). Both matter, but the primary metric determines which form factor gets resourced first and how success is measured.

**Q5: Is UAE PASS willing to make the eSeal proof available to JS SDK operators (including non-SP-registered websites), or is the eSeal proof capability restricted to contracted SPs?**

The eSeal proof is UAE PASS's strongest trust differentiator. Making it available to any domain-registered JS SDK operator dramatically elevates the product's value proposition and competitive moat. However, the eSeal proof is the legal instrument for verified data transactions — making it available to non-contracted operators may create legal ambiguity about liability if a website misuses the proof. TDRA and legal team input is required. The answer determines whether the SDK is "trusted convenience" (like Singpass MyInfo) or "cryptographically verifiable identity infrastructure" (like eIDAS 2.0) — a significant positioning difference.

---

## Appendix A: Form Factor Comparison Matrix

| Dimension | A: Browser Extension | B: Mobile OS Autofill | C: JS SDK | D: QR Filler | E: NFC |
|-----------|---------------------|-----------------------|-----------|--------------|--------|
| User install required | Yes (extension) | No (in UAE PASS app) | No | No | No |
| Operator integration required | No | No | Yes (lightweight) | Optional | Yes (terminal) |
| Desktop web coverage | Yes | Chrome extension only | Yes | Yes (cross-device QR) | No |
| Mobile web coverage | Safari extension (iOS) | Yes | Yes | Yes | No |
| Native app coverage | No | Yes (Android) | No | Partial | Yes |
| In-person coverage | No | No | No | Partial | Yes |
| Trust level (citizen) | High | High | High | High | Highest |
| Trust level (operator verification) | Medium (API trust) | Medium | Tiered | Medium | High |
| Time to reach 1M users | 18–24 months | 12–18 months | 6–12 months | 6–9 months | 36+ months |
| Engineering complexity | Medium | High (Android) + Medium (iOS) | Medium | Low–Medium | High |
| Regulatory complexity | Medium | Medium | High (open-web policy) | Low | Medium |
| Recommended priority | 4 | 3 | 1 | 2 | 5 |

---

## Appendix B: Applicable Standards and References

| Standard / Protocol | Relevance |
|--------------------|-----------|
| W3C Verifiable Credentials Data Model (VC-DM) | Attribute packaging and proof format; UAE PASS should evaluate VC-DM for SDK payload format |
| ISO 18013-5 (mDL) | NFC/BLE proximity presentation for driving licence; standard for Form Factor E |
| OpenID4VP (OpenID for Verifiable Presentations) | Protocol for wallet-to-verifier presentation; relevant for eIDAS 2.0 interoperability |
| OpenID4VCI (OpenID for Verifiable Credential Issuance) | Credential issuance protocol; relevant if UAE PASS moves to VC-DM model |
| FIDO2 / WebAuthn | Passkey authentication; relevant to UAE PASS authentication ceremony in SDK flow |
| HTML `autocomplete` attribute (WHATWG Living Standard) | Field classification taxonomy for browser extension and SDK field matching |
| Android AutofillService API (API Level 26+) | Form Factor B Android implementation |
| iOS AutoFill Credential Provider Extension | Form Factor B iOS implementation |
| UAE PDPL (Federal Decree-Law No. 45 of 2021) | Personal data processing obligations; consent model; data minimisation; cross-border transfer restrictions |
| CAdES (ETSI EN 319 122) / PAdES (ETSI EN 319 132) | eSeal format used in UAE PASS DV — the proof format for SDK eSeal payload |

---

*End of exploratory analysis. File path: `C:\Users\2065726\mainclaude\fill_with_uaepass_exploration.md`*
