# "Continue with UAE PASS" Button — Risk, Benchmarking & Recommendation

---

## Slide 1: What's Changing & Why

### Current Flow: QR Code Scan
1. SP displays QR code on screen
2. User opens UAE PASS app and scans QR
3. Sharing request appears in-app
4. User approves and documents are shared

**Built-in safety:** Strong user intent (scanning is explicit), proximity signal (user is physically present), smaller remote attack surface.

### New Flow: "Continue with UAE PASS" Button
1. User clicks "Continue with UAE PASS" on SP website
2. SP backend creates sharing request via API
3. Push notification sent to user's phone
4. User approves in UAE PASS app and documents are shared

**UX gain:** No app switching, no camera needed, works on any device, faster flow. Reduces QR tampering risk flagged by Dubai Electronic Security Center.

**Trade-off:** Enables remote initiation of a sharing request using only knowledge of identifiers (phone + Emirates ID). This shifts the attack surface from physical proximity to remote initiation.

---

## Slide 2: Seven Risks Identified

### High Severity

**1. Push Fatigue / Notification Spam**
- Attacker floods a user with repeated sharing requests until they tap "Approve" by mistake or out of frustration
- This is the #1 attack vector that led Microsoft and Okta to enforce number matching globally in 2023
- Likelihood: High | Impact: High

**2. Impersonation via Known Identifiers**
- Attacker uses leaked or guessed Emirates ID + phone number to trigger a legitimate-looking sharing request
- Victim sees a real UAE PASS notification and may be coerced to approve ("push-to-approve fraud")
- Previously required victim to actively scan a QR at the right moment
- Likelihood: Medium | Impact: High

### Medium Severity

**3. Identity / Account Enumeration**
- API endpoint may reveal whether an Emirates ID + phone matches a UAE PASS user through error messages or response timing
- Attackers can confirm valid identity pairs at scale
- Likelihood: Medium | Impact: Medium

**4. Wrong-Person Delivery**
- Mistyped phone number or Emirates ID, or a recycled/reassigned phone number, sends the sharing request to the wrong person
- Results in a privacy incident and trust damage
- Likelihood: Medium | Impact: Medium

**5. Automated Bot / DoS Abuse**
- Bots flood the "create sharing request" endpoint using leaked identity lists
- UAE PASS users get spammed; integration quotas blow up; reputational damage
- Likelihood: Medium | Impact: Medium

**6. Social Engineering / Phishing Adjacency**
- Users become trained to approve push notifications. Attackers call pretending to be helpdesk: "Please approve the UAE PASS request now"
- Success rate of social engineering increases with push-based flows
- Likelihood: Medium | Impact: Medium

**7. Privacy & Compliance Risk (Data Collection)**
- The new flow requires collecting and processing Emirates ID + phone number, which are higher-sensitivity identifiers
- Increases obligations under UAE PDPL for data minimization, retention limits, security controls, and breach readiness
- Likelihood: Low | Impact: High

---

## Slide 3: Global Benchmarking — The World Is Moving This Way

### UAE: CBUAE Notice 2025/3057 (First in the World)

| Detail | Value |
|--------|-------|
| Issued | May 2025 |
| Mandate | All UAE-licensed banks must eliminate SMS and email OTP |
| Deadline | March 31, 2026 |
| Scope | Retail banks, card issuers, payment providers, e-wallet providers, neobanks |
| Approved replacements | In-app push authentication, biometrics, FIDO2/passkeys, Emirates Face Recognition |
| Liability shift | Already in effect — banks reimburse customers for OTP-related fraud losses |
| Early movers | Emirates NBD, ADIB, FAB already moved customers to app-based auth by end of 2025 |

The UAE is the first country globally to completely ban SMS OTP for financial services. This creates natural demand for the "Continue with UAE PASS" pattern from every bank, insurer, and payment provider.

### Singapore: MAS SMS OTP Phase-Out (July 2024)

| Detail | Value |
|--------|-------|
| Announced | July 9, 2024 |
| Replacement | Device-bound digital tokens (in-app authentication) |
| Adoption rate | 60%–90% of customers at DBS, OCBC, UOB already activated digital tokens |
| Early mover | Citibank Singapore phased out SMS OTP in 2023 |
| Additional layer | Singpass Face Verification added September 2024 for token setup |
| Phishing losses before mandate | S$14.2 million in 2023 alone |

### European Union: PSD2 Strong Customer Authentication

| Detail | Value |
|--------|-------|
| In force | January 2021 (full enforcement) |
| Requirement | Two-factor authentication using knowledge + possession + inherence |
| Coverage | 300+ million ecommerce shoppers across EEA |
| Frictionless rate | 60%+ of transactions authenticated without direct customer involvement |
| Direction | PSD3 in draft — further strengthening app-based, device-bound MFA |

### Microsoft & Okta: Number Matching Enforcement (May 2023)

| Detail | Value |
|--------|-------|
| Microsoft | Enforced number matching for all Authenticator push notifications from May 8, 2023 |
| Okta | Number Challenge available with risk-based triggers (never / high-risk only / always) |
| Problem solved | MFA fatigue attacks (Lapsus$ breached Microsoft, Cisco, Uber using push bombing) |
| How it works | SP displays a 2-digit code; user must type the same code in authenticator app to approve |
| Vendors supporting | Microsoft, Okta, Duo (Cisco), and others |
| Limitation | Does not fully protect against real-time phishing with man-in-the-middle |

### Global Push Authentication Adoption (2025–2026)

| Metric | Value |
|--------|-------|
| Banks with passwordless auth (top 50 global) | 78% launched for at least one segment |
| Customer adoption rate | 60%–85% within 18 months of launch |
| Fraud loss reduction | 42%–68% after implementation |
| Authentication success rate (passkeys) | 93% |
| Notable: HSBC | 41M passkey users in 6 months (60% adoption rate across 14 markets) |
| Notable: Nordea Bank | 73% digital banking customer adoption (highest regional rate globally) |
| Banking customers using passkeys globally | 340+ million as of Q1 2026 |
| Biometric auth among mobile banking users | 77% |
| Unauthorized access reduction from biometrics | 52.7% |

---

## Slide 4: Required Mitigations — Must-Have Controls

### Launch Blockers (Non-Negotiable)

**1. Number Matching / Challenge Code**
- Display a short code on the SP website; user must confirm the same code in UAE PASS app before approval
- Industry standard since Microsoft/Okta mandate (May 2023)
- Prevents fully remote push-to-approve attacks
- Proven to stop MFA fatigue attacks that breached Microsoft, Cisco, and Uber

**2. Aggressive Rate Limiting**
- Maximum 3 requests per Emirates ID per hour, 5 per day
- Cool-down timer + CAPTCHA after repeated failures
- Per-IP and per-device fingerprint throttling
- Allow users to temporarily mute requests from a specific service provider

**3. Generic Responses (Anti-Enumeration)**
- Always return: "If the details are correct, you will receive a request"
- Same response for valid and invalid identity pairs
- Constant-time API responses to prevent timing-based enumeration
- Monitor for high-volume probe attempts; graylist sources

**4. Short TTL + Single-Use Tokens**
- Sharing requests expire in 3–5 minutes
- Non-reusable correlation IDs (already enforced via DB unique constraint)
- Auto-expire requests quickly to minimize approval window

### Should-Have Controls (Post-Launch)

**5. Data Minimization & Retention Policy**
- Hash Emirates ID + phone after linking is complete
- Delete raw identifier data within 24 hours
- Encrypted at rest with strict access controls and audit trails
- Privacy notice with clear purpose limitation (UAE PDPL compliance)

**6. Bot Protection & Abuse Monitoring**
- WAF rules, device attestation, anomaly scoring by IP/ASN/geo mismatch
- Real-time alerting dashboard for abuse detection
- Per-user daily caps on sharing requests

**7. User Reporting & In-App Transparency**
- "Report Suspicious Request" button in UAE PASS approval screen
- In-app copy: "We will never call and ask you to approve"
- Show exact data being requested, the requesting SP identity, and the channel (e.g., "initiated from web form")
- Make "Deny" prominent alongside "Approve"

---

## Slide 5: Assessment & Recommendation

### Verdict

The "Continue with UAE PASS" button is **strategically sound** and aligns with a clear global trend:
- **CBUAE Notice 3057** mandates SMS OTP elimination by March 2026 — push auth is the approved replacement
- **Singapore, EU, and major global banks** have already moved to app-based push authentication
- **Microsoft and Okta** enforce number matching as the standard defense against push fatigue
- The new flow **eliminates QR tampering risk** flagged by Dubai Electronic Security Center
- **340M+ banking customers** globally already use push/passkey authentication

### The Risk Is Manageable

All 7 identified risks are **mitigatable with industry-standard controls** that are already widely deployed:
- Number matching (Microsoft/Okta standard since 2023)
- Rate limiting (standard for any API-exposed service)
- Anti-enumeration (security best practice)
- Short TTL tokens (already part of existing UAE PASS architecture)

### What We Reduce

| Risk | Current (QR) | New (Button + Mitigations) |
|------|--------------|---------------------------|
| QR tampering / overlay scams | Exposed (physical) | Eliminated |
| Push fatigue attacks | N/A | Mitigated by number matching |
| Remote impersonation | Low (requires proximity) | Mitigated by rate limiting + number matching |
| Identity enumeration | N/A | Mitigated by generic responses |
| User friction / drop-off | Higher (app switch + camera) | Lower (single tap) |

### Recommendation

**Go with Mitigations** — Implement the 4 must-have controls (number matching, rate limiting, anti-enumeration, short TTL) as launch gates. Conduct security review and pen test before pilot. Roll out initially with 2–3 SPs in a controlled pilot, then expand to general availability.

Not proceeding risks missing the CBUAE compliance window and allowing SPs to build proprietary alternatives outside the UAE PASS ecosystem.

---

## Sources & References

- CBUAE Notice 2025/3057: UAE Central Bank SMS OTP Phase-Out Directive
- Microsoft: Number Matching Enforcement (May 2023) — BleepingComputer
- Okta: Number Challenge for Okta Verify — Okta Documentation
- MAS: Banks in Singapore to Phase Out OTPs (July 2024) — MAS Media Release
- Singapore: Singpass Face Verification (September 2024) — MAS Media Release
- EU PSD2: Strong Customer Authentication — Stripe Guide
- Push Authentication Fraud Risks — ServiceNow Security Lab
- Passwordless Progress Report 2026 — UseIDeem
- Dubai Electronic Security Center: QR Code Tampering Warnings
- UAE PDPL: Data Protection Obligations for Identifier Collection
