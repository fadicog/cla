# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Repository Purpose

This is a **documentation-only repository** for UAE PASS Digital Documents (DV) component. It contains no executable code - only knowledge base and product management documentation.

**Primary Files**:
- `uae_pass_knowledge_base.md` - Comprehensive knowledge transfer document (17 sections covering product capabilities, technical architecture, UX guidelines, and operational procedures)
- `pm_dv_working_doc.md` - Living PM working document (metrics, roadmap, decision log, learning backlog)

---

## Working with This Repository

### No Build/Test Commands
This repository has no build scripts, package.json, or test frameworks. Work consists entirely of documentation editing and knowledge management.

### Documentation Conventions

**1. Bilingual Content (EN/AR)**
All user-facing content must include both English and Arabic:
- Arabic uses RTL (right-to-left) formatting
- Follow Arabic plural rules: 0 (omit), 1 (singular), 2 (dual), 3-10 (plural form 1), 11+ (plural form 2)
- Avoid "vault" terminology - use "Documents" / «المستندات»

**2. Terminology (Glossary)**
- **DV** - Digital Vault / Digital Documents component
- **eSeal** - Cryptographic organization stamp (issuer authentication, not eSignature)
- **SP** - Service Provider (banks, telcos, insurers)
- **ICP** - High-volume document issuer (EID, Visa, Passport)
- **TDRA** - Telecommunications and Digital Government Regulatory Authority (regulator/product owner)
- **DDA** - Design Authority (design/UX partner)
- **Verifiable Presentation** - Package of user documents/attributes for SP
- **Correlation ID** - Unique SP request identifier for sharing flows

**3. Document Structure Standards**
- Use numbered sections (e.g., "## 2) Core capabilities")
- Separate major sections with `---`
- Include "Last updated" timestamps on knowledge documents
- Add glossary sections for technical terms
- Include contact/ownership sections

**4. Living Document Patterns**
The PM working doc uses placeholders for ongoing work:
- `_[TO BE FILLED]_` - awaiting information
- `_[?]_` - unknown/to be discovered
- `_[TO BE CLARIFIED]_` - needs stakeholder input
- Checkboxes `- [ ]` for learning backlogs
- Decision log tables for tracking key decisions

---

## Product Domain Context

### Multi-Stakeholder Environment
- **TDRA** - Sets policy, owns product priorities
- **DDA** - Design approval required for major features
- **ICP** - Primary document issuer (EID, Visa, Passport)
- **Service Providers (SPs)** - Integration partners consuming user documents
- **Engineering** - FE/BE/QA delivery teams

Major features require DDA design approval + TDRA policy alignment.

### Core Product Flows
1. **Authentication/SSO** - QR-based login to SP services
2. **Document Lifecycle** - Request → Availability → Storage → Updates → Revocation/Expiry
3. **Document Sharing** - Consent-based: SP creates request → User approves → Verifiable presentation delivered
4. **Qualified eSignature** - Person-level consent for transactions

### Technical Patterns
- **eSeal Validation** - Cryptographic verification of issuer authenticity (CAdES/PAdES)
- **QR Code Hygiene** - Unique IDs, short TTL, one-time use, no PII embedded
- **Notification Taxonomy** - Actionable (document sharing request) vs Informational (issuance, expiry, revocation)
- **Dual Citizenship** - Primary EID (UAE) vs Secondary EID (2nd nationality) classification

### Key Ongoing Initiatives (as of 2025-11-12)
- **ICP eSeal Transition** - ICP moving from DDA eSeal service to self-signing (own HSM)
- **Dual Citizenship Support** - Primary/Secondary EID handling
- **Auto-Add Documents** - One-time consent for periodic issuer checks (pending legal review)
- **UX Enhancements** - Grid view, copy-any-field, PDF viewer revamp
- **Duplicate Correlation ID Fix** - DB constraint to prevent duplicate QR requests

---

## Operating Rhythm

**Sprint Cadence**: Bi-weekly (2-week sprints)
- Mid-week: Backlog refinement
- Friday: Sprint review

**Tools**:
- Jira: "DV Product" board
- Figma: "DV Refresh 2024/25"
- SharePoint: Slides, roadmaps
- Firebase: Push notifications, Remote Config

---

## When Acting as Product Manager

If taking on the PM role for DV:

1. **Start with `pm_dv_working_doc.md`** - This is your living workspace
2. **Reference `uae_pass_knowledge_base.md`** - Source of truth for product/technical details
3. **Update timestamps** when making significant changes to knowledge base
4. **Fill placeholders** in PM doc as you learn (`[TO BE FILLED]`, `[?]`, etc.)
5. **Log decisions** in the Decision Log table with date, rationale, stakeholders, status
6. **Track learning** using checkboxes in Learning Backlog section
7. **Maintain bilingual parity** for any user-facing copy examples (EN/AR)
8. **Cross-reference sections** using format like "See section 2.3" or file references

---

## Security & Privacy Principles

- **Consent-based sharing** - Every document share requires explicit user approval
- **No PII in QR codes** - Use opaque correlation IDs only
- **eSeal validation** - All issued documents must be cryptographically verified
- **Unique correlation IDs** - SPs must generate unique, time-boxed, one-time IDs (enforced via DB constraint)
- **HTTPS/TLS pinning** - Required for SP integrations

---

## Common Tasks

### Adding New Feature Documentation
1. Determine section in knowledge base (authentication, documents, UX, etc.)
2. Follow numbered section format: `## N) Feature Name`
3. Include user stories if applicable: "As a [user], I want [goal], so that [benefit]"
4. Add bilingual copy examples (EN/AR) for user-facing text
5. Document acceptance criteria, technical implementation, and stakeholder approvals
6. Update glossary if introducing new terms
7. Add timestamp to "Last updated" line

### Updating PM Working Doc
1. Keep "Notes & Insights" section chronological (by week)
2. Update KPI/metrics section with actual values as discovered
3. Move items from "Learning Backlog" to "Notes & Insights" when completed
4. Add rows to Decision Log table for significant product decisions
5. Update "Current Priorities" section based on sprint planning

### Documenting Stakeholder Feedback
1. Capture in "Notes & Insights" section with date + source
2. If impacts roadmap, update "Roadmap & Initiatives" section
3. If decision required, add to Decision Log after resolution
4. If new risk/question, add to "Open Questions / Risks" section

---

## Arabic Content Guidelines

When adding Arabic translations:

**Pluralization Rules**:
- 0 items: Omit segment
- 1 item: `مستند صادر` (singular)
- 2 items: `مستندان صادران` (dual)
- 3-10 items: `مستندات صادرة` (plural form 1)
- 11+ items: `مستند صادر` (plural form 2)

**Common EN → AR Pairs** (from knowledge base section 12):
- "Quick Tip" → «تلميح سريع»
- "Got it" → «حسنًا»
- "Document Information" → «معلومات المستند»
- "Document Details" → «تفاصيل المستند»
- "Documents" → «المستندات»

**RTL Formatting**:
- Numbers appear RTL: `0 مستند صادر` (number-first)
- Use Arabic quotation marks: « »
- Test for truncation in both languages

---

## Reference Sections in Knowledge Base

Quick navigation to key sections in `uae_pass_knowledge_base.md`:

- **Section 2**: Core capabilities (auth, eSignature, documents, sharing)
- **Section 3**: eSeal implementation and 2025 transition
- **Section 4**: QR code usage and hygiene
- **Section 5**: Notifications taxonomy (actionable vs informational)
- **Section 6**: Document UX enhancements
- **Section 7**: Arabic plurals and counters
- **Section 8**: Dual Citizenship (Primary/Secondary EID)
- **Section 9**: Auto-Add Documents (one-time consent)
- **Section 11**: SP onboarding essentials
- **Section 12**: Copy guidelines (EN/AR)
- **Section 16**: Glossary

---

## Session History & Key Artifacts

### Session: Sharing Request Status Tracking (2025-11-25)

**Full session documentation**: `session_sharing_request_status_tracking.md`

**Key Deliverables**:
- **Status tracking system design** with 23 status codes (100-600 range)
- **Data analysis** of 350K+ sharing requests (67.4% conversion rate)
- **Interactive dashboard** with 8 visualizations
- **CSV status reference** for database import

**Critical Findings**:
- Document availability is THE critical factor: 84.9% success when docs available vs 0% when missing
- 20.6% of requests are "dead on arrival" (SPs requesting docs users don't have)
- Consent screen is biggest drop-off point (16.9% abandonment)
- iOS outperforms Android by 10 percentage points (77.8% vs 67.7%)

**Quick Reference Files**:
- `sharing_request_status_codes.csv` - Status code lookup table
- `uaepass_dashboard_report.html` - Interactive visualization dashboard (ready to view)
- `document_sharing_analysis_report.md` - Comprehensive analysis report
- `key_insights_summary.md` - Executive one-page summary
- `QUICKSTART_DASHBOARD.md` - Dashboard setup guide

**Top Recommendations**:
1. Implement document pre-check API (eliminate 72K futile requests/week)
2. Redesign consent screen UX (reduce 16.9% drop-off)
3. Android optimization sprint (close 10% platform gap)
4. Issuer retry logic (reduce 26% of technical failures)

**Potential Impact**: +31,500 shares/week (+13.3% improvement) → Target: 76% conversion rate

---

### Session: 2026 Roadmap Planning & Visualization (2026-02-03)

**Key Deliverables**:
- **Roadmap Builder Application** - React app with filtering, color coding, export features
- **2026 Roadmap Data** - 16 features across 4 categories (Product, Design, SP, UX)
- **PowerPoint Presentation** - 10-slide stakeholder deck

**Roadmap Builder Features**:
- Category filtering with multi-select chips
- Color coding by category (Product=Blue, Design=Purple, Technical=Green, UX=Orange, SP=Teal)
- Export to PNG image (1920x1080) with timeline options (sprints/months/both)
- Category selection in export for filtered exports

**Quick Reference Files**:
- `roadmap-builder/` - Interactive roadmap planning application
- `roadmap_v5_scored.csv` - Source data with prioritization scores
- `UAE_PASS_DV_2026_Roadmap.pptx` - 10-slide presentation deck
- `slide format.md` - Reference format from previous year

**2026 Features by Category**:
| Category | Count | Top Score | DDA Related |
|----------|-------|-----------|-------------|
| Product | 7 | 16 | 1 |
| Design | 3 | 16 | 2 |
| SP | 1 | 16 | 0 |
| UX | 5 | 13 | 1 |
| Technical | 4 | 16 | 0 |

**Scoring System**: Priority (High=8, Medium=5, Low=3) + Complexity (Low=8, Medium=5, High=3) = Total Score (max 16)

**Items Already In Progress**:
- Status-Based Reporting Implementation - Sprint 70
- Dual Citizenship GA - Sprint 72
- Infinite Loaders Detection - Sprint 70

---

### Session: Roadmap Light — PowerPoint Export Tool (2026-02-23)

**Key Deliverable**:
- **`roadmap-light/roadmap-light.html`** — Single-file, zero-install roadmap tool purpose-built for exporting PowerPoint-ready slides

**Tool Design**:
- Layout: Rows = items, Columns = months (Gantt-style)
- No build step — open directly in any browser
- Multiple independent instances on the same page, each exportable separately

**Features**:
- Bilingual EN/AR with UAE Arabic month names (يناير، فبراير... ديسمبر); full RTL layout when Arabic active
- Font: Inter (EN) / Cairo (AR) via Google Fonts CDN
- Theme colors: Gold `#a89030`, Dark Green `#11a56f`, Teal `#3fcaa7` + custom hex per item
- Item input table: Name EN/AR, Start/End month (2025–2028 range), color picker
- PNG export via html2canvas CDN — sizes 1920×1080 / 2400×1350 / 2560×1440
- "Hide title in export" checkbox per instance (hides `.roadmap-title` div during html2canvas capture only)
- No categories rendered — items sorted by start date only (category field kept in data model but hidden)

**Preloaded Instances**:
1. **DV 2026 Roadmap** — 12 items: Product (gold `#a89030`), Design (dark green `#11a56f`), SP (teal `#3fcaa7`)
2. **DV 2025 Roadmap** — 12 items from `rd25.png` reference slide: Product (green `#5a9e6f`), DDA Joint (blue `#7ab0cc`), Analysis (navy `#2c3a55`)

**Quick Reference**:
- `roadmap-light/roadmap-light.html` — The tool (single file, ~960 lines)
