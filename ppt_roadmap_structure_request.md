# PPT Roadmap Extraction -- Markdown Structure Specification

This document defines the exact markdown format that the pptx-to-markdown agent must produce when extracting epic details from `ppt roadmap.pptx`. The output will be consumed programmatically to update the roadmap builder app's `poolItems.ts` data file.

---

## Output File

Write the extracted data to: `D:\claude\ppt_roadmap_extracted.md`

---

## Overall Document Structure

```markdown
# PPT Roadmap Extracted Epics

> Extracted from: ppt roadmap.pptx
> Extraction date: YYYY-MM-DD

---

## Epic: <Epic Name>

| Field | Value |
|-------|-------|
| Feature Name | <exact feature name as shown on the slide> |
| Category | <one of: Product, Technical, UX, Design, SP> |
| Priority | <one of: High, Medium, Low, TBD> |
| Complexity | <one of: High, Medium, Low, TBD> |
| DDA Item | <Yes or No> |
| Start Sprint | <number or empty> |
| End Sprint | <number or empty> |
| External Visible | <Yes or No> |
| Tag | <e.g. "New Feature", "Reporting", or empty> |
| Relates To | <item number(s) or empty> |

### Objectives
- <objective 1>
- <objective 2>
- <objective 3>

### Description
<single paragraph or short multi-line description>

### Acceptance Criteria
- <criterion 1>
- <criterion 2>
- <criterion 3>

### Owners
- <owner/team 1>
- <owner/team 2>

### Dependencies
- <dependency 1>
- <dependency 2>

### Target Audience
- <audience 1>
- <audience 2>

### Remarks
<any remarks, notes, or empty if none>

---

(repeat for each epic slide)
```

---

## Field-by-Field Mapping to TypeScript PoolItem

The table below shows how each markdown field maps to the `PoolItem` interface in `src/types/index.ts`.

| Markdown Field | PoolItem Property | Type | Transformation Rule |
|---|---|---|---|
| Feature Name | `featureName` | `string` | Verbatim text. Also used as `summary` if no separate summary exists. |
| Epic Name (H2 heading after "Epic: ") | `epicName` | `string` | Verbatim from H2 heading. May differ slightly from Feature Name (e.g., "Design System Update (DDA Dependent)"). |
| Category | `category` | `string` | Must be exactly one of: `Product`, `Technical`, `UX`, `Design`, `SP`. |
| Priority | `priority` | `string` | Must be exactly one of: `High`, `Medium`, `Low`, `TBD`, `TBC`. |
| Priority (derived) | `priorityScore` | `number` | Compute: High=8, Medium=5, Low=3, TBD=0, TBC=0. |
| Complexity | `complexity` | `string` | Must be exactly one of: `High`, `Medium`, `Low`, `TBD`, `TBC`. |
| Complexity (derived) | `complexityScore` | `number` | Compute: Low=8, Medium=5, High=3, TBD=0, TBC=0. |
| (derived) | `totalScore` | `number` | `priorityScore + complexityScore`. |
| DDA Item | `ddaItem` | `boolean` | "Yes" -> `true`, "No" -> `false`. |
| Start Sprint | `startSprint` | `number \| null` | Parse integer. If empty or not mentioned, use `null`. |
| End Sprint | `endSprint` | `number \| null` | Parse integer. If empty or not mentioned, use `null`. |
| External Visible | `externalVisible` | `boolean` | "Yes" -> `true`, "No" -> `false`. Default `false` if not present. |
| Tag | `tag` | `string` | Verbatim. Empty string if none. |
| Relates To | `relatesTo` | `string` | Item number(s) as string. Empty string if none. |
| Objectives (bullet list) | `objectives` | `string[]` | Each bullet becomes one array element. Strip leading "- ". |
| Description (paragraph) | `description` | `string` | Full paragraph as single string. Collapse multiple lines into one. |
| Acceptance Criteria (bullet list) | `acceptanceCriteria` | `string[]` | Each bullet becomes one array element. Strip leading "- ". |
| Owners (bullet list) | `owners` | `string[]` | Each bullet becomes one array element. Strip leading "- ". |
| Dependencies (bullet list) | `dependencies` | `string[]` | Each bullet becomes one array element. Strip leading "- ". |
| Target Audience (bullet list) | `targetAudience` | `string[]` | Each bullet becomes one array element. Strip leading "- ". |
| Remarks | `remarks` | `string` | Verbatim. Empty string if none. |

**Additional derived fields** (not extracted, set by the consuming agent):
- `number`: Auto-assigned integer. See "Matching Rules" section below.
- `track`: Set to empty string `''` unless slide explicitly mentions a track (e.g., "SP track").
- `toBePickedUp`: Default `true` for all extracted items.
- `alreadyPickedUp`: `true` if `startSprint` is not null and sprint is <= current sprint (73), otherwise `false`.
- `summary`: Use `description` field value, or `featureName` if description is empty.

---

## Matching Rules: New Items vs Existing Items

The consuming agent will match extracted epics to existing pool items using this logic:

1. **Primary match key**: `featureName` (case-insensitive, trimmed). Fuzzy match is acceptable for minor wording differences.
2. **Secondary match key**: `epicName` against existing `epicName` values.
3. **If a match is found**: Update the existing pool item's epic detail fields (`epicName`, `objectives`, `description`, `acceptanceCriteria`, `owners`, `dependencies`, `targetAudience`). Keep the existing `number`. Only overwrite fields that are non-empty in the extraction (do not clear existing data with empty values).
4. **If no match is found**: Create a new pool item entry. The `number` will be auto-assigned as `max(existing numbers) + 1`.

To help the consuming agent match items, include this comment in the markdown for any epic that clearly corresponds to an existing item:

```markdown
<!-- MATCH: number=35 featureName="Design Audit" -->
```

Place this comment immediately after the `## Epic:` heading if you can identify the match. If unsure, omit the comment and the consuming agent will fuzzy-match.

---

## Handling Special Cases

### Empty Sections
If a slide does not contain objectives, acceptance criteria, dependencies, etc., use:
```markdown
### Objectives
(none)
```

The consuming agent will treat "(none)" as an empty array `[]`.

### Sprint Ranges
If the slide shows a sprint range like "Sprint 73-77", extract as:
- Start Sprint: 73
- End Sprint: 77

If only one sprint is shown (e.g., "Sprint 73"), set both Start Sprint and End Sprint to that value.

If no sprint information is present, leave both empty.

### Multiple Categories or Ambiguous Category
If a slide does not clearly state a category, infer from context:
- Infrastructure, DevOps, CI/CD, monitoring, testing frameworks -> `Technical`
- User-facing design, accessibility, design system -> `Design`
- UI/UX improvements, screen revamps, flow redesigns -> `UX`
- Service Provider integrations, SDK, onboarding -> `SP`
- Everything else (features, reporting, consent, documents) -> `Product`

### DDA Dependency
Mark `DDA Item: Yes` if the slide mentions DDA approval, DDA dependency, or "DDA Dependent" in the title.

### Slides That Are Not Epics
Skip slides that are title slides, table of contents, summary/overview slides, or timeline/gantt chart slides. Only extract individual epic detail slides.

---

## Example: Fully Populated Epic

```markdown
## Epic: Design Audit

<!-- MATCH: number=35 featureName="Design Audit" -->

| Field | Value |
|-------|-------|
| Feature Name | Design Audit |
| Category | Design |
| Priority | High |
| Complexity | Low |
| DDA Item | No |
| Start Sprint | |
| End Sprint | 77 |
| External Visible | No |
| Tag | |
| Relates To | |

### Objectives
- Review core screens and journeys and capture pain points with evidence (screenshots, examples).
- Identify quick wins vs larger redesign candidates and propose sequencing.
- Align priorities with Product and Engineering so the backlog is implementation-ready.

### Description
UI/UX designer reviews the current screens to identify room for improvement and the biggest pain points (usability, clarity, consistency). Output is a prioritized backlog with recommended fixes.

### Acceptance Criteria
- Audit report delivered with issues grouped by severity/impact and linked to screens.
- Prioritized improvement backlog created (with effort sizing placeholders).
- Top quick wins have clear specs and acceptance criteria ready for development.

### Owners
- Product Design (UX/UI)
- Product Management
- Frontend/Mobile Development
- Quality Assurance

### Dependencies
- Agreed scope of screens/flows to audit.
- Access to current designs/build, and top support ticket themes (if available).
- Review workshop with key stakeholders to finalize priorities.

### Target Audience
- UAE PASS users

### Remarks
To be discussed with Ahmed
```

---

## Example: Minimal Epic (sparse slide)

```markdown
## Epic: Blockchain Upgrade

<!-- MATCH: number=56 featureName="Blockchain Upgrade" -->

| Field | Value |
|-------|-------|
| Feature Name | Blockchain Upgrade |
| Category | Technical |
| Priority | High |
| Complexity | Low |
| DDA Item | No |
| Start Sprint | |
| End Sprint | |
| External Visible | No |
| Tag | |
| Relates To | |

### Objectives
- Upgrade the Digital Vault blockchain infrastructure.

### Description
The Blockchain Upgrade project aims to enhance the current blockchain infrastructure by selecting the most suitable blockchain technology, validating feasibility, and ensuring future scalability.

### Acceptance Criteria
- Fully functional DV app with new blockchain.

### Owners
- Product Management
- Backend Development
- Quality Assurance

### Dependencies
(none)

### Target Audience
- UAE PASS users
- Service Providers

### Remarks

```

---

## Reference: Existing Pool Item Numbers and Feature Names

Use this list to populate the `<!-- MATCH -->` comments where possible:

| Number | Feature Name |
|--------|-------------|
| 1 | Status-Based Reporting Implementation |
| 5 | User Behavior Analytics Tool Selection |
| 7 | UX Enhancements Bundle - Revisit Documents List View |
| 8 | Error-to-Status Code Linking System |
| 9 | Dual Citizenship GA |
| 10 | Auto-Add Documents Launch / One-Time Consent |
| 16 | Design System Update |
| 17 | Home Page Revamp |
| 18 | UX/UI Enhancements Bundle 2 |
| 19 | Form Filler |
| 20 | Consent Sharing (Third Party Data) |
| 26 | License QR Code Display Fix |
| 28 | Infinite Loaders Detection and Resolution |
| 29 | Firebase Configuration & Optimization |
| 32 | Automated Testing |
| 35 | Design Audit |
| 36 | Accessibility Enhancement |
| 37 | Enhancement/Revamp Document Request |
| 38 | Revamp Document Sharing |
| 40 | Enable Download of All Issued Documents in DV |
| 41 | Physical Document Sharing |
| 47 | ELK Stack AI Upgrade |
| 50 | SP Offboarding |
| 51 | QR Code Simplification - Direct Sharing |
| 52 | UAEVerify SEO |
| 53 | Service Provider SDK |
| 54 | DR Automation |
| 55 | SP Automation Testing Suite |
| 56 | Blockchain Upgrade |
| 57 | CI/CD Pipeline Automation |
| 58 | Operation Automation |

---

## Final Notes

- Preserve the exact wording from slides whenever possible. Do not paraphrase objectives or acceptance criteria.
- If a slide contains information that does not fit any field above, include it in the Remarks section.
- Maintain consistent markdown formatting (no extra blank lines within sections, consistent bullet style with `-`).
- Use UTF-8 encoding for the output file.
