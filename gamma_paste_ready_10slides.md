# TDRA Business-First Briefing — Gamma paste-ready (10 cards)

> **HOW TO USE THIS FILE**
> 1. In Gamma, choose **Paste in text** mode.
> 2. Set **Number of cards** to **10**.
> 3. Set **Text content / Card style** to **Preserve** (so Gamma keeps the wording).
> 4. Paste the block under **SECTION A** into the main text area. **Stop copying when you see the `═══ END OF SECTION A ═══` line — do not include it.**
> 5. Paste the block under **SECTION B** into the **Additional instructions** field.
> 6. Pick a clean editorial theme → **Generate**.

---

## SECTION A — Paste this into Gamma's main text area

## What we actually deliver — and why it matters

Digital Vault, Verifiable Credentials, and how UAE Verify completes the picture.

A briefing for the TDRA onboarding track · 30 minutes · May 2026.

---

## One idea, before everything else

What flows through Digital Vault is **not** a document.

It's a **verifiable credential** — a cryptographically sealed *claim*, signed by the source authority, consented to by the citizen, and delivered to the service provider with proof of origin, integrity, and intent.

- Source-signed — the issuer's seal makes it real.
- Citizen-consented — the citizen's tap makes it shared.
- Verifier-confirmable — the service provider can prove it on its own.

---

## A document is not a credential. The difference is structural.

| A PDF copy | A Verifiable Credential |
|---|---|
| Can be altered, photocopied, replayed | Tamper-evident — any change breaks the seal |
| No proof of origin once it leaves the issuer | Cryptographically tied to the issuing authority |
| No expiry, revocation, or status awareness | Status check is part of every verification |
| No record of consent — it can be reused at will | Consent is captured per share, on the record |
| No legal weight without a wet signature | Legally binding — eIDAS-aligned |

A credential *can* carry a PDF inside it as a visual companion. But the credential is the proof; the PDF is just a picture of it.

---

## Three roles, one trust model

A simple cast of three. UAE PASS is the rails — not a fourth actor.

The whole platform rests on three players, each with a clear job. No middleman holds the citizen's data.

*Triangle of Trust diagram — three glowing nodes on a dark panel: gold Issuer lower-left, green Holder top, teal Verifier lower-right.*

- **Issuer · Government authority.** Holds the original record. Stamps the credential with an unforgeable digital seal.
- **Holder · The Citizen.** Receives the credential into UAE PASS. Decides who sees it, when, and for how long.
- **Verifier · Service Provider.** Bank, telco, insurer. Confirms the credential is real — in seconds, on its own, no callback needed.

UAE PASS is the rails. It does not store the personal data being shared.

---

## From request to receipt — what actually happens

A single share, end to end. The citizen is in the driving seat throughout.

*End-to-end flow diagram — four pillars (Issuer · Citizen · UAE PASS DV · Service Provider) on a dark panel, with a tamper-proof ledger band beneath.*

1. **Service provider asks.** A bank or government desk asks UAE PASS for a verified credential.
2. **The ask is logged anonymously.** A record is added to the tamper-proof ledger. No personal data.
3. **Citizen approves on their phone.** They see who's asking, why, and exactly what's being shared.
4. **Live credential, from the source.** UAE PASS pulls a fresh, signed credential from the issuing authority.
5. **Sealed package travels.** Forwarded to the service provider, signed and tamper-evident.
6. **Service provider verifies — on its own.** Seals checked locally. If anything is off, the share is rejected. A receipt is logged anonymously.

The personal data passes *through* UAE PASS. It is never stored there.

---

## "PDF in a shared drive" — what actually changes

A simpler-sounding alternative has been raised. Let's walk through what changes.

The proposal: let citizens collect a PDF from the issuer, drop it on a shared drive, and let the service provider pick it up. Here's what's different — not from a tech standpoint, but from a *guarantee* standpoint.

| What the platform gives you today | What "PDF on a shared drive" gives you |
|---|---|
| **Consent** captured per share, with the citizen's approval and a legal signature | None — no record the citizen ever agreed to this share |
| **Revocation** — status checked on every verification | None — once the file is out, it's out forever |
| **Tamper detection** — mathematical; the seal breaks on any change | Trust the file hash, easily replayed or substituted |
| **Legal weight** — eIDAS-aligned, non-repudiable | None — disputes fall back to phone calls with the issuer |
| **Audit trail** — anonymous proof on-chain for every share | A drive log, at best — and only if it isn't deleted |

The choice isn't between *simple* and *complex*. It's between a system designed for the next decade and one we'd be reverting to from 2015.

---

## ICP documents — what's different, and the fix already built

Most credentials are issued once and held many times. ICP works the opposite way — and we've built the answer.

**Part 1 — Why ICP looks different**

Most credentials in Digital Vault — a degree, a marriage certificate, an insurance card — are **issued once, held many times.**

ICP credentials (Emirates ID, passport, visa) work differently. ICP **re-issues a fresh version every time it's requested.** That means:

- There is no single, durable artefact to "download and keep."
- Each retrieval is a new act of issuance.
- Digital Vault treats these as **visualisation documents** today — viewable in the app, but not downloadable, because anything saved on disk would no longer match what's live at the source.

**Part 2 — The downloadable + verifiable fix**

Digital Vault has built a mechanism that closes the gap **without sacrificing verifiability.**

- Each downloadable PDF carries an embedded reference to its underlying Verifiable Credential.
- The citizen can save it, share it, print it.
- Anyone can re-verify it later through UAE Verify — because the proof travels with the file.

✅ **Production-ready in Digital Vault.**

⏳ **Awaiting alignment with ICP** to enable for ICP-issued documents.

The thing the alternative proposal is trying to deliver — a downloadable PDF the citizen can keep — is *already on the way*, without breaking the credential model.

---

## UAE Verify — and how it fits with Digital Vault

Two services, two purposes — both needed.

**Part 1 — What UAE Verify is**

Documents *do* leave the secure channel. They get emailed, printed, shared on WhatsApp. **UAE Verify** is the national service that lets anyone confirm a UAE-issued document is authentic — after the fact.

Two ways to verify today:

1. **Upload the file** to uaeverify.gov.ae — UAE Verify checks the embedded proof and reports back.
2. **Scan the document's QR code** with the UAE PASS app — verification on the spot.

The QR-scan flow is being studied for revamp; direction not yet locked.

**Part 2 — Digital Vault vs UAE Verify**

| Digital Vault | UAE Verify |
|---|---|
| Direct, consented credential delivery to a known service provider | Authenticity check for documents already in circulation |
| The SP pulls from the issuer via UAE PASS, with citizen consent, for a defined purpose | The document owner pushes the file; anyone can verify it later |
| Cryptographic proof at delivery, plus on-chain consent record | Confirms authenticity, but not the purpose or who it was shared with |
| Bound to a specific share, a specific SP, a specific purpose | Stand-alone authenticity confirmation |

They're *complementary*, not interchangeable. Don't bypass Digital Vault because UAE Verify exists. Don't stretch UAE Verify to do Digital Vault's job.

---

## Where the UAE actually stands

The UAE is **one of the first nations** to operationalise W3C Verifiable Credentials at population scale.

The architecture is aligned with **eIDAS** — the European framework for electronic identity and trust services that the rest of the world has been benchmarking against since 2014.

The same foundations let us add new credentials, new service providers, and new verification surfaces — *without re-doing the trust model each time*.

The right question isn't *"can we make it simpler?"* It's *"can we hold the standard while making integration easier?"* — and that's exactly what the lightweight onboarding track is for.

---

## A shared picture

Not asking for approvals today — asking that we leave with the same mental model.

**One.** What flows through Digital Vault to service providers is a *Verifiable Credential* — not a stand-alone PDF. That distinction is what gives the platform its legal, security, and audit posture.

**Two.** The downloadable-document gap for ICP credentials *has* a fix. The mechanism is built, sitting in production, ready for alignment with ICP.

**Three.** For service providers that genuinely cannot take a full integration, the right answer is the lightweight onboarding tier — not bypassing the credential model. We can keep that work moving together.

*The credential follows the citizen. The trust follows the credential. The platform protects both.*

═══ END OF SECTION A — STOP COPYING HERE ═══

## SECTION B — Paste this into Gamma's "Additional instructions" field (≤500 chars)

```
Audience: new TDRA onboarding-track members, non-technical. Tone: inviting and educational, never defensive. Theme: cream bg, deep gold + teal accents, italic serif on key phrases, clean sans body. On slides 4 and 5, italic placeholder lines mark diagram images — leave space on a dark panel. Slides 7 and 8 need two-column or top/bottom splits. Slide 6 is a calm comparison table — no alarm icons, no jewel blues, no clip art.
```

---

## Notes for the user (NOT pasted into Gamma)

- **Card count:** 10 cards · 9 `---` separators in Section A — verified.
- **textMode recommended:** `preserve` (your wording is locked).
- **Diagram slides (4 and 5):** the italic line on each acts as a placeholder. After Gamma generates, replace it with your actual Triangle and Flow images from the simplified explainer site (`vc-explainer-simplified/index.html`). They live on a dark gallery panel — Section B asks Gamma to reserve that space.
- **Two-part slides (7 and 8):** flagged in Section B for a two-column or top/bottom split. If Gamma renders them single-column, click into each card and use `/columns` in the editor to split.
- **What was dropped during conversion:**
  - All `**TITLE**` / `**SUBTITLE**` / `**BODY**` / `**VISUAL HINT**` / `**SPEAKER NOTE**` scaffolding labels.
  - The optional appendix slide (kept the deck at exactly 10).
  - Speaker notes — Gamma generates its own; edit them in the card menu after generation.
  - The `> Brief for the slide generator` blockquote at the top of the source file (would have rendered as bullets on slide 1).
- **If Gamma still gives you fewer than 10 cards** — it sometimes merges adjacent short slides under `condense`. Force `Preserve` and re-generate.
- **If Gamma gives you more than 10** — your slide-count dropdown isn't set; double-check it's at 10 before clicking Generate.
