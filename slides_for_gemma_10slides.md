# Digital Vault & Verifiable Credentials — A business-first briefing for the TDRA onboarding track (10-slide version)

> **Brief for the slide generator**
> - Audience: new TDRA members on the onboarding track. Mostly non-technical. Some have proposed a "PDF in a shared drive" alternative; this deck addresses it without making them defensive.
> - Tone: inviting and collaborative. We're walking through it together, not defending a fortress.
> - Format: 10 slides, ~30-minute online session, leaving 5–7 minutes for discussion.
> - Visual style: cream / off-white background, deep gold (#9c7820) and teal (#14826d) accents, an italic serif (Instrument Serif or Georgia italic) for editorial accents on key phrases, clean sans for body. Diagrams sit on a dark "gallery panel" inside the cream layout.
> - No JSON, no code, no signature taxonomies in the body. Anything technical goes in an optional appendix.
> - Each slide below has: **TITLE**, optional **SUBTITLE**, **BODY**, and a short **VISUAL HINT** for the slide generator. Speaker notes are included on the load-bearing slides.
> - Two slides are denser than the rest by design (Slide 7 merges the ICP problem + fix; Slide 8 merges UAE Verify + the DV-vs-UAE-Verify comparison). Use a two-column or top/bottom layout so neither feels crowded.

---

## Slide 1 — Cover

**TITLE**
What we actually deliver — and why it matters

**SUBTITLE**
Digital Vault, Verifiable Credentials, and how UAE Verify completes the picture

**BODY (footer line)**
A briefing for the TDRA onboarding track · 30 minutes · May 2026

**VISUAL HINT**
Cover slide — large title in deep ink, italic serif for "actually deliver", a single soft gold gradient orb in the corner. UAE PASS DV mark top-left. No imagery in the body.

---

## Slide 2 — One idea, before everything else

**TITLE**
One idea, before everything else

**BODY (large editorial statement)**
What flows through Digital Vault is **not** a document.
It's a **verifiable credential** — a cryptographically sealed *claim*, signed by the source authority, consented to by the citizen, and delivered to the service provider with proof of origin, integrity, and intent.

**THREE ANCHOR PILLS (left to right, equal weight)**
- Source-signed — the issuer's seal makes it real.
- Citizen-consented — the citizen's tap makes it shared.
- Verifier-confirmable — the service provider can prove it on its own.

**VISUAL HINT**
Big editorial typography. The three anchor pills sit on a thin horizontal line beneath the statement, divided by faint vertical hairlines.

**SPEAKER NOTE**
Hold on this slide. Everything that follows depends on this one frame: a credential is a *claim with a proof*, not a file.

---

## Slide 3 — A document is not a credential

**TITLE**
A document is not a credential. The difference is structural.

**BODY (two-column comparison)**

| A PDF copy | A Verifiable Credential |
|---|---|
| Can be altered, photocopied, replayed | Tamper-evident — any change breaks the seal |
| No proof of origin once it leaves the issuer | Cryptographically tied to the issuing authority |
| No expiry, revocation, or status awareness | Status check is part of every verification |
| No record of consent — it can be reused at will | Consent is captured per share, on the record |
| No legal weight without a wet signature | Legally binding — eIDAS-aligned |

**FOOTNOTE (smaller, below the table)**
A credential *can* carry a PDF inside it as a visual companion. But the credential is the proof; the PDF is just a picture of it.

**VISUAL HINT**
Clean two-column table. Left column on a soft cream tint with a subtle red dot per row; right column slightly brighter with a teal check per row. No icons inside the cells.

---

## Slide 4 — Three roles, one trust model

**TITLE**
Three roles, one trust model

**SUBTITLE**
A simple cast of three. UAE PASS is the rails — not a fourth actor.

**DIAGRAM CAPTION**
The whole platform rests on three players, each with a clear job. No middleman holds the citizen's data.

**THREE ROLE CAPTIONS (one paragraph each, beside or below the diagram)**

- **Issuer · Government authority.** Holds the original record. Stamps the credential with an unforgeable digital seal.
- **Holder · The Citizen.** Receives the credential into UAE PASS. Decides who sees it, when, and for how long.
- **Verifier · Service Provider.** Bank, telco, insurer. Confirms the credential is real — in seconds, on its own, no callback needed.

**BOTTOM LINE (centred)**
UAE PASS is the rails. It does not store the personal data being shared.

**VISUAL HINT**
Lift the **Triangle of Trust** from the simplified explainer site. Three glowing circle nodes (gold ISSUER lower-left, green HOLDER top, teal VERIFIER lower-right), thin gradient edges between them, a faint dashed "shared trust register" line across the bottom. The whole diagram lives on a dark gallery panel (deep navy / near-black) so it sits like artwork inside the cream layout.

---

## Slide 5 — From request to receipt

**TITLE**
From request to receipt — what actually happens

**SUBTITLE**
A single share, end to end. The citizen is in the driving seat throughout.

**BODY (six numbered steps, plain language)**

1. **Service provider asks.** A bank or government desk asks UAE PASS for a verified credential.
2. **The ask is logged anonymously.** A record of the request is added to the tamper-proof ledger. No personal data.
3. **Citizen approves on their phone.** They see who's asking, why, and exactly what's being shared.
4. **Live credential, from the source.** UAE PASS pulls a fresh, signed credential straight from the issuing authority.
5. **Sealed package travels.** Forwarded to the service provider, signed and tamper-evident.
6. **Service provider verifies — on its own.** All seals checked locally. If anything is off, the share is rejected. A receipt is logged anonymously.

**BOTTOM LINE (italic, centred)**
The personal data passes *through* UAE PASS. It is never stored there.

**VISUAL HINT**
Lift the **end-to-end flow diagram** from the simplified explainer site — four pillars (Issuer, Citizen, UAE PASS DV, Service Provider) connected by curved dashed paths, with a "tamper-proof ledger" band underneath. Keep the dark gallery treatment. The six numbered steps run as a list to one side or below.

---

## Slide 6 — What changes if we step back to PDFs

**TITLE**
"PDF in a shared drive" — what actually changes

**SUBTITLE**
A simpler-sounding alternative has been raised. Let's walk through what changes.

**INTRO (one line above the table)**
The proposal: let citizens collect a PDF from the issuer, drop it on a shared drive, and let the service provider pick it up. Here's what's different about that model — not from a tech standpoint, but from a *guarantee* standpoint.

**BODY (five-row comparison)**

| What the platform gives you today | What "PDF on a shared drive" gives you |
|---|---|
| **Consent** captured per share, with the citizen's approval and a legal signature | None — no record the citizen ever agreed to this share |
| **Revocation** — status checked on every verification | None — once the file is out, it's out forever |
| **Tamper detection** — mathematical, the seal breaks on any change | Trust the file hash, easily replayed or substituted |
| **Legal weight** — eIDAS-aligned, non-repudiable | None — disputes fall back to phone calls with the issuer |
| **Audit trail** — anonymous proof on-chain for every share | A drive log, at best — and only if it isn't deleted |

**CLOSING LINE (centred, italic accent)**
The choice isn't between *simple* and *complex*. It's between a system designed for the next decade and one we'd be reverting to from 2015.

**VISUAL HINT**
Five-row comparison table. Left column subtle teal accent (current state), right column subtle red accent (the alternative). Avoid loaded icons (no skull, no warning sign) — the words carry the weight. Calm and factual.

**SPEAKER NOTE**
This is the slide that earns the rest of the meeting. Don't rush. Walk row-by-row. The point is that each row is a *property* the platform delivers — and each one disappears in the alternative. Not because the alternative is "bad", but because it isn't the same thing.

---

## Slide 7 — ICP documents: what's different, and the fix already built

**TITLE**
ICP documents — what's different, and the fix already built

**SUBTITLE**
Most credentials are issued once and held many times. ICP works the opposite way — and we've built the answer.

**BODY — TWO PARTS, SIDE-BY-SIDE OR TOP/BOTTOM**

**Part 1 — Why ICP looks different**

Most credentials in Digital Vault — a degree, a marriage certificate, an insurance card — are **issued once, held many times.**

ICP credentials (Emirates ID, passport, visa) work differently. ICP **re-issues a fresh version every time it's requested.** That means:

- There is no single, durable artefact to "download and keep."
- Each retrieval is a *new act of issuance*.
- Today, Digital Vault treats these as **visualisation documents** — viewable in the app, but not downloadable, because anything saved on disk would no longer match what's live at the source.

**Part 2 — The downloadable + verifiable fix**

Digital Vault has built a mechanism that closes the gap **without sacrificing verifiability.**

- Each downloadable PDF carries an embedded **reference to its underlying Verifiable Credential.**
- The citizen can save it, share it, print it.
- Anyone can re-verify it later through UAE Verify — because the proof travels with the file.

**Status:**
- ✅ **Production-ready in Digital Vault.**
- ⏳ **Awaiting alignment with ICP** to enable for ICP-issued documents.

**CLOSING LINE (italic, full width)**
The thing the alternative proposal is trying to deliver — a downloadable PDF the citizen can keep — is *already on the way*, without breaking the credential model.

**VISUAL HINT**
Two-column or split layout. Left/top: a small "issued once → held many" vs "re-issued every time" icon-pair. Right/bottom: a stylised PDF with a small embedded "VC reference" tag in the corner, plus the green-check / amber-clock status row. Keep the colour palette restrained — green for ready, soft amber for pending, no alarm colours.

**SPEAKER NOTE**
This slide answers two questions in one breath: "why can't I just download my Emirates ID?" and "wait, you said you fixed it — what's the holdup?" Be specific that the implementation is *already in production*; the gap is policy alignment with ICP, not engineering.

---

## Slide 8 — UAE Verify, and how it fits with Digital Vault

**TITLE**
UAE Verify — and how it fits with Digital Vault

**SUBTITLE**
Two services, two purposes — both needed.

**BODY — TWO PARTS, SIDE-BY-SIDE OR TOP/BOTTOM**

**Part 1 — What UAE Verify is**

Documents *do* leave the secure channel. They get emailed, printed, shared on WhatsApp. **UAE Verify** is the national service that lets anyone confirm a UAE-issued document is authentic — after the fact.

**Two ways to verify today:**
1. **Upload the file** to `uaeverify.gov.ae` — UAE Verify checks the embedded proof and reports back.
2. **Scan the document's QR code** with the UAE PASS app — verification on the spot.

The QR-scan flow is being studied for revamp; direction not yet locked.

**Part 2 — Digital Vault vs UAE Verify**

| Digital Vault | UAE Verify |
|---|---|
| Direct, consented credential delivery to a known service provider | Authenticity check for documents already in circulation |
| The SP pulls from the issuer via UAE PASS, with citizen consent, for a defined purpose | The document owner pushes the file; anyone can verify it later |
| Cryptographic proof at delivery, plus on-chain consent record | Confirms authenticity, but not the purpose or who it was shared with |
| Bound to a specific share, a specific SP, a specific purpose | Stand-alone authenticity confirmation |

**CLOSING LINE (italic)**
They're *complementary*, not interchangeable. Don't bypass Digital Vault because UAE Verify exists. Don't stretch UAE Verify to do Digital Vault's job.

**VISUAL HINT**
Two-column layout. Left/top column has a clean "UAE Verify" wordmark/icon and the two verification methods (file-upload card + phone-with-QR card). Right/bottom column is the Digital Vault vs UAE Verify comparison table — gold tones on the DV side, teal tones on the UAE Verify side, rows aligned across the divider for direct comparison.

**SPEAKER NOTE**
The audience often conflates these. The 30-second mental model: Digital Vault is the *secure delivery rail* for known purposes; UAE Verify is the *authenticity check surface* for documents that have left the rail. Both are needed because both situations exist in the real world.

---

## Slide 9 — The bigger picture

**TITLE**
Where the UAE actually stands

**BODY (three short paragraphs)**

The UAE is **one of the first nations** to operationalise W3C Verifiable Credentials at population scale.

The architecture is aligned with **eIDAS** — the European framework for electronic identity and trust services that the rest of the world has been benchmarking against since 2014.

The same foundations let us add new credentials, new service providers, and new verification surfaces — *without re-doing the trust model each time*.

**CLOSING LINE (italic accent, centred)**
The right question isn't *"can we make it simpler?"* It's *"can we hold the standard while making integration easier?"* — and that's exactly what the lightweight onboarding track is for.

**VISUAL HINT**
Restrained editorial layout. Maybe a faint world map or stylised globe in the background at very low opacity, with a small UAE marker. Otherwise just text.

---

## Slide 10 — A shared picture

**TITLE**
A shared picture

**SUBTITLE**
Not asking for approvals today — asking that we leave with the same mental model.

**BODY (three short paragraphs, no bullet points)**

**One.** What flows through Digital Vault to service providers is a *Verifiable Credential* — not a stand-alone PDF. That distinction is what gives the platform its legal, security, and audit posture.

**Two.** The downloadable-document gap for ICP credentials *has* a fix. The mechanism is built, sitting in production, ready for alignment with ICP.

**Three.** For service providers that genuinely cannot take a full integration, the right answer is the lightweight onboarding tier — not bypassing the credential model. We can keep that work moving together.

**CLOSING LINE (large, italic accent)**
*The credential follows the citizen. The trust follows the credential. The platform protects both.*

**VISUAL HINT**
Editorial closing slide. Large italic serif for the closing line. The three numbered points sit cleanly above. UAE PASS DV mark in the corner. No image — let the words land.

---

## Optional Appendix Slide — For the engineering reviewers in the room

**TITLE**
For the engineering reviewers in the room

**SUBTITLE**
Where the cryptography, signature taxonomy, and verification chain are documented.

**BODY (no detail — just a pointer)**

Everything below is intentionally outside the main flow of this briefing — it's the reference layer for the integration teams.

- **W3C Verifiable Credentials Data Model 2.0** — the international standard our credentials follow.
- **SP Integration Guide v2.4** — sections 2.4, 2.6, 2.7, 5.2 cover sharing, verification, evidence/visualisation, and the Receive Presentation flow end to end.
- **SP Use Case Guidelines v1.1** — sections 2.1–2.7 are the non-negotiable rules every service provider integration must respect.
- **Internal:** the existing technical deck (`TDRA-_DocumentValidation_v1`) carries the full signature chain, on-chain/off-chain data taxonomy, and verification step-by-step.

**VISUAL HINT**
Plain reference card. Four bulleted document references on a cream background, no other ornament.

---

## Generator notes (please respect)

- **No JSON anywhere on slides.** No `did:eth:…`, no signature payloads.
- **No alarmist language or icons** on Slide 6 (no warning triangles, no skulls, no fire). The comparison should feel like adult math, not propaganda.
- **Triangle of Trust** (Slide 4) and **End-to-end flow diagram** (Slide 5) — if you can render them as actual diagrams, do. If not, leave a clean placeholder titled "Triangle of Trust diagram — three glowing nodes on dark gallery panel" / "End-to-end flow diagram — four pillars + ledger band on dark gallery panel" so the design team can drop the SVG in afterwards.
- **Slides 7 and 8 are two-part slides by design.** Use a clear top/bottom or left/right split so each half breathes. Don't crush them into one block.
- **Type pairing.** Headings: clean sans (Inter / Arial). Editorial accent words ("actually deliver", "structural", "shared picture"): an italic serif (Instrument Serif / Georgia italic). Body: clean sans, 14–16pt.
- **Colour discipline.** Primary cream `#faf6ec`, ink `#1a1d28`, deep gold `#9c7820`, teal `#14826d`, warning red used sparingly `#b94545`. Avoid jewel-tone blues and synthetic greens.
- **One image per slide max** (the comparison tables and Triangle/Flow diagrams *are* "the image" — don't add stock photography on top).
