Consider the followig, currently when a sharing request is created, the user needs to have the uae pass application opened, scans the qr code from the with the uae pass application, then the user gets the sharing request gets generated, the previous journey assumed that the user is already authenticated, now we take the information from the use in a form then get the phone number and eid and link it to the identifier in uae pass and notify that account with a sharing request as an improvement for the sharing process ux, i need to identify what might be the risks or room for fraud if we move to such a ux 
Thought for 1m 49s

You can absolutely improve UX by moving from “user opens UAE PASS → scans QR → request created” to “user enters phone + Emirates ID in your form → you map to UAE PASS identifier → push a sharing request to that account”. But it changes the trust model in a way that creates new fraud / abuse space.

This is very similar to the UAE PASS “identifier + push notification” pattern used in some authentication journeys (user provides email/mobile/Emirates ID, then gets a push notification in the UAE PASS app).

Below is a practical risk / fraud checklist your technical team can use.

What changes (and why it matters)
Current flow (QR scan inside UAE PASS)

Built-in safety properties

Strong “user intent” signal: scanning a QR is an explicit action.

Some “proximity/context”: user is looking at the relying party screen when they scan.

Smaller remote attack surface (harder to trigger at scale without the user present).

Proposed flow (form → server triggers push request)

New safety trade-off

You’ve enabled remote initiation of a push request to a person using only knowledge of identifiers (phone + Emirates ID).

That introduces:

impersonation attempts

request spamming

account/identity enumeration

push-fatigue social engineering

UAE PASS itself is built to integrate service providers and supports “Data & Document Sharing” as a capability, but the abuse surface depends on how you initiate requests.

Main fraud / abuse risks in the new UX
1) Impersonation by “known identifiers”

Scenario: Attacker knows (or guesses/leaks) a victim’s Emirates ID + phone number and submits your form.
Impact: Victim receives a legitimate-looking sharing request in UAE PASS; attacker may try to coerce them to approve (“push-to-approve fraud”).
Why new: Previously the attacker typically needed the victim to actively scan a QR at the right moment.

Mitigations

In the UAE PASS approval screen, show very clear relying-party identity (your org name, verified branding), purpose, and exactly what will be shared.

Add a challenge code: show a short code on your website/app and require the user to confirm the same code in-app before approval (prevents fully-remote initiation from being effective).

“First-time / high-risk share” → require step-up (stronger confirmation / biometric if available in your integration pattern).

2) Push notification fatigue / consent manipulation

Scenario: Attacker repeatedly triggers requests until the user taps “Approve” just to stop notifications (or during distraction).
Impact: Unauthorized sharing due to human factors, not crypto break.

Mitigations

Hard rate limits per Emirates ID, per phone, per IP/device fingerprint.

Cool-down timers and progressive friction (CAPTCHA, additional checks) after N attempts.

Make “Deny” prominent; add “Report suspicious request” path.

Auto-expire requests quickly (short TTL).

3) Wrong-person delivery (data quality + telecom realities)

Scenario: User mistypes phone or Emirates ID; phone numbers can also be recycled/reassigned.
Impact: You push a sharing request to the wrong person → privacy incident + trust damage.

Mitigations

Validate formatting strictly; confirm phone ownership (OTP) but don’t treat OTP as identity proof.

Avoid displaying “we found your account” vs “not found” (prevents enumeration) — always respond generically.

Consider requiring a second corroborating attribute (e.g., DOB) only if your risk model supports it (and you can protect it).

4) Account / identity enumeration

Scenario: Your endpoint reveals whether a given Emirates ID + phone matches a UAE PASS user (even indirectly via error messages or timing).
Impact: Attackers can confirm identity pairs at scale.

Mitigations

Always return the same generic response: “If the details are correct, you will receive a request.”

Constant-time-ish responses; avoid “not registered” branching visible to attackers.

Monitor for high-volume attempts; block/graylist sources.

5) Automated abuse / denial-of-service

Scenario: Bots flood your “create sharing request” endpoint using leaked ID lists.
Impact: UAE PASS users get spammed; your integration quotas/logs blow up; reputational damage.

Mitigations

Strong bot controls: WAF rules, CAPTCHA, device attestation where possible, throttling.

Abuse detection: anomaly scoring by IP ASN, velocity, geo mismatches.

Per-user daily caps; allow users to temporarily “mute requests from this service provider”.

6) Phishing adjacency and “trust transference”

Scenario: User is trained to approve pushes; attackers call pretending to be your helpdesk: “Approve the UAE PASS request now.”
Impact: Social engineering success increases.

Mitigations

In-app copy: “We will never call and ask you to approve.”

Show exact data requested and “why” in the approval screen.

Add “initiated from: channel / session type” (e.g., “initiated from web form”) to make out-of-context approvals feel suspicious.

7) Privacy + compliance risk (you now store/handle Emirates ID + phone)

You’re collecting and processing higher-sensitivity identifiers, which increases your obligations for data minimization, retention limits, security controls, and breach readiness under UAE data protection expectations. A widely used legal summary of the UAE PDPL highlights rights like access/correction/deletion and emphasizes minimizing data, not keeping it longer than needed, and stronger security/breach obligations.

Mitigations

Minimize what you store (ideally store only a transaction reference + hashed identifiers).

Encrypt at rest; strict access controls; audit trails.

Define retention: delete raw Emirates ID/phone quickly once linking is complete.

Privacy notice + purpose limitation (what you collect, why, with whom it’s shared).

One risk you reduce by moving away from QR-in-public

If today’s QR is displayed in public/physical contexts, QR tampering/overlay scams are a known issue (replace/overlay QR to redirect users). Dubai Electronic Security Center has explicitly warned about tampered QR codes used for phishing/malware/data capture.
Your new flow reduces that specific physical QR-tampering risk, but increases remote initiation risks above.

Recommended “minimum safe” version of the new UX

If you want the UX gain without taking on disproportionate fraud risk, implement at least these controls:

Request is always approved inside UAE PASS (no “silent sharing”).

Short TTL + single-use transaction tokens; auto-expire quickly.

Challenge code binding (website shows code X; UAE PASS approval screen must show the same X).

Generic responses to prevent enumeration.

Aggressive rate limiting + bot protection + abuse monitoring.

Data minimization + retention policy for Emirates ID/phone.

If you share what “sharing request” technically means in your integration (data fields requested, whether it’s document sharing via UAE PASS or via GSB/other channel, and whether you can show a challenge code in the UAE PASS consent screen), I can turn this into a concise risk register with severity/likelihood ratings and concrete acceptance criteria for security sign-off.