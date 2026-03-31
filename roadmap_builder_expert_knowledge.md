# Roadmap Builder Expert -- Knowledge Base

> **Last updated**: 2026-02-19
> **Purpose**: Complete reference for the `roadmap-builder-expert` agent to maintain, update, and extend the UAE PASS Digital Vault roadmap builder application without guidance.

---

## 1. Project Overview

### What This Is

The **Roadmap Builder** is a React + TypeScript single-page application used to plan and visualize the UAE PASS Digital Vault (DV) 2026 product roadmap. It provides:

- A **pool** of backlog items (features/epics) with priority scoring
- A **timeline** view (vis-timeline) showing items across sprints or calendar dates
- **Filtering** by category, external visibility
- **Export** to PNG and PPTX
- **Epic detail editing** with objectives, acceptance criteria, owners, dependencies

### Technology Stack

| Layer | Technology |
|-------|-----------|
| Framework | React 18 + TypeScript |
| Build | Vite + tsc |
| State | Zustand 4 with `zundo` (undo/redo) and `persist` middleware |
| Timeline | vis-timeline 7 + vis-data 7 |
| Drag & Drop | @dnd-kit/core + @dnd-kit/sortable |
| Date Utils | date-fns 3 |
| Export | html2canvas (PNG), pptxgenjs (PPTX) |
| IDs | uuid v10 |
| Deploy | GitHub Pages (static files in `docs/` folder) |

### Product Context

This is part of the UAE PASS Digital Vault documentation repository. The DV is a government digital documents component where users store and share verified documents (EID, Visa, Passport, etc.) with Service Providers (banks, telcos, insurers). Key stakeholders include TDRA (regulator), DDA (design authority), ICP (document issuer), and Service Providers.

See `D:\claude\CLAUDE.md` for full product domain context.

---

## 2. Data Model Deep Dive

### PoolItem Interface

A `PoolItem` represents a feature/epic in the backlog pool. Defined in `D:\claude\roadmap-builder\src\types\index.ts`.

| Field | TypeScript Type | Purpose | UI Usage | Example Values | Notes |
|-------|----------------|---------|----------|----------------|-------|
| `number` | `number` | Unique identifier for the pool item | Displayed as "#N" badge, used as primary key | `1`, `35`, `52` | Auto-assigned as `max(existing) + 1` for new items |
| `category` | `string` | Feature category | Color-coded chip/badge, filtering | `'Product'`, `'Technical'`, `'UX'`, `'Design'`, `'SP'` | Must be one of the 5 categories |
| `tag` | `string` | Optional label | Displayed in pool list | `'New Feature'`, `'Reporting'`, `''` | |
| `priority` | `string` | Priority level | Sorting, badge color | `'High'`, `'Medium'`, `'Low'`, `'TBD'`, `'TBC'`, `''` | |
| `priorityScore` | `number` | Numeric priority score | Sorting, totalScore calculation | `8`, `5`, `3`, `0` | **Transformation**: High=8, Medium=5, Low=3, TBD/TBC/empty=0 |
| `relatesTo` | `string` | Related item number(s) | Informational display | `'1'`, `'2'`, `''` | References other pool item numbers |
| `complexity` | `string` | Implementation complexity | Badge, duration default | `'High'`, `'Medium'`, `'Low'`, `'TBD'`, `'TBC'`, `''` | |
| `complexityScore` | `number` | Numeric complexity score | Sorting, totalScore calculation | `8`, `5`, `3`, `0` | **Transformation**: Low=8, Medium=5, High=3, TBD/TBC/empty=0 (NOTE: inverted -- low complexity = high score) |
| `totalScore` | `number` | Combined priority + complexity | Primary sort key, displayed prominently | `16`, `13`, `11`, `10` | `priorityScore + complexityScore`. Max possible = 16 |
| `track` | `string` | Track/workstream label | Informational | `'SP track'`, `''` | Usually empty string |
| `ddaItem` | `boolean` | Requires DDA (Design Authority) approval | DDA badge in UI | `true`, `false` | |
| `featureName` | `string` | Human-readable feature name | Primary display text, matching key | `'Design Audit'`, `'Form Filler'` | **Primary match key** for updates (case-insensitive) |
| `summary` | `string` | Short description | Tooltip or secondary text | Full sentence describing the feature | |
| `toBePickedUp` | `boolean \| null` | Whether item is in scope | Pool visibility | `true`, `null` | All current items have `true` |
| `remarks` | `string` | Internal notes | Displayed in detail view | `'Pending Legal TDRA approval'`, `''` | |
| `alreadyPickedUp` | `boolean` | Whether work has started | Visual indicator (badge/styling) | `true`, `false` | **Must be kept in sync**: `true` if `startSprint !== null && startSprint <= CURRENT_SPRINT` |
| `startSprint` | `number \| null` | Sprint when work begins | Timeline placement, picked-up calculation | `70`, `73`, `74`, `null` | `null` means not yet scheduled |
| `endSprint` | `number \| null` (optional) | Sprint when work ends | Timeline bar end | `72`, `77`, `null` | `null` or undefined means not yet determined |
| `externalVisible` | `boolean` | Show in external/public roadmap | External filter toggle | `true`, `false` | Currently all items are `false` |
| `epicName` | `string` (optional) | Epic name from PPT (may differ from featureName) | Epic detail display | `'Design System Update (DDA Dependent)'` | **Secondary match key** |
| `objectives` | `string[]` (optional) | Epic objectives | Epic detail panel, bullets | Array of objective strings | From PPT slides |
| `description` | `string` (optional) | Epic description | Epic detail panel | Single paragraph | From PPT slides |
| `acceptanceCriteria` | `string[]` (optional) | Acceptance criteria | Epic detail panel, bullets | Array of criteria strings | From PPT slides |
| `owners` | `string[]` (optional) | Team owners | Epic detail panel, chips | `['Product Management', 'Backend Development']` | From PPT slides |
| `dependencies` | `string[]` (optional) | Dependencies | Epic detail panel, bullets | Array of dependency strings | From PPT slides |
| `targetAudience` | `string[]` (optional) | Who benefits | Epic detail panel, chips | `['UAE PASS users', 'Service Providers']` | From PPT slides |

### Scoring System

```
Priority Score:
  High   -> 8
  Medium -> 5
  Low    -> 3
  TBD    -> 0
  TBC    -> 0
  (empty)-> 0

Complexity Score (INVERTED - lower complexity = higher score):
  Low    -> 8
  Medium -> 5
  High   -> 3
  TBD    -> 0
  TBC    -> 0
  (empty)-> 0

Total Score = priorityScore + complexityScore
Maximum = 16 (High priority + Low complexity)
```

### RoadmapItem Interface

A `RoadmapItem` is a feature placed on the timeline. Created when a pool item is "added to roadmap." Defined in `D:\claude\roadmap-builder\src\types\index.ts`.

| Field | TypeScript Type | Purpose |
|-------|----------------|---------|
| `id` | `string` | UUID, primary key |
| `name` | `string` | Display name on timeline |
| `startSprint` | `number` (optional) | Start sprint for sprint-based items |
| `endSprint` | `number` (optional) | End sprint for sprint-based items |
| `startDate` | `string` (optional) | ISO date for date-based items |
| `endDate` | `string` (optional) | ISO date for date-based items |
| `subtasks` | `Subtask[]` | Auto-generated REQ_UX/DEV/QA phases |
| `createdAt` | `string` | ISO timestamp |
| `updatedAt` | `string` | ISO timestamp |
| `poolItemNumber` | `number` (optional) | Links back to PoolItem.number |
| `category` | `string` (optional) | Copied from pool item |
| `poolPriority` | `string` (optional) | Copied from pool item |
| `poolComplexity` | `string` (optional) | Copied from pool item |
| `ddaItem` | `boolean` (optional) | Copied from pool item |
| `externalVisible` | `boolean` (optional) | Copied from pool item |
| `epicName` | `string` (optional) | Copied from pool item |
| `objectives` | `string[]` (optional) | Copied from pool item |
| `description` | `string` (optional) | Copied from pool item |
| `acceptanceCriteria` | `string[]` (optional) | Copied from pool item |
| `owners` | `string[]` (optional) | Copied from pool item |
| `dependencies` | `string[]` (optional) | Copied from pool item |
| `targetAudience` | `string[]` (optional) | Copied from pool item |

### SprintConfig Interface

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `firstSprintNumber` | `number` | `71` | The sprint number that corresponds to `firstSprintStartDate` |
| `firstSprintStartDate` | `string` | `'2026-01-01'` | ISO date when sprint 71 starts |
| `workingDaysPerSprint` | `number` | `10` | Working days per sprint (2 weeks = 10 working days) |
| `weekendDays` | `number[]` | `[0, 6]` | 0=Sunday, 6=Saturday (UAE weekend) |

### Category Colors

```typescript
// Chip/badge colors (for pool list, filters)
CATEGORY_COLORS = {
  'Product':   { bg: '#dbeafe', text: '#1e40af', border: '#93c5fd' },
  'Technical': { bg: '#ffedd5', text: '#9a3412', border: '#fdba74' },
  'UX':        { bg: '#ede9fe', text: '#5b21b6', border: '#c4b5fd' },
  'Design':    { bg: '#fce7f3', text: '#9d174d', border: '#f9a8d4' },
  'SP':        { bg: '#d1fae5', text: '#065f46', border: '#6ee7b7' },
};

// Timeline bar colors
CATEGORY_BAR_COLORS = {
  'Design':    '#8b5cf6',  // Purple/Violet
  'Product':   '#3b82f6',  // Blue
  'Technical': '#22c55e',  // Green
  'UX':        '#f97316',  // Orange
  'SP':        '#06b6d4',  // Teal/Cyan
};
```

### Complexity-to-Sprint Duration Mapping

When adding a pool item to the roadmap, the default sprint duration is based on complexity:

```typescript
COMPLEXITY_TO_SPRINTS = {
  'High': 3,
  'Hight': 3,  // handles CSV typo
  'Medium': 2,
  'Low': 1,
  'TBD': 2,
  'TBC': 2,
  '': 2,
};
```

### POOL_ITEMS Array Sorting

The `POOL_ITEMS` array in `poolItems.ts` is sorted at export time using `.sort()`:

1. **Total score descending** (highest first)
2. **Priority order** (High=0, Medium=1, Low=2, TBD/TBC=3, empty=4)
3. **Item number ascending** (as tiebreaker)

**Do not manually reorder items in the array.** The `.sort()` call at the bottom handles ordering automatically.

---

## 3. How to Add/Update Pool Items

### Adding a New Pool Item

1. **Open** `D:\claude\roadmap-builder\src\data\poolItems.ts`
2. **Add a new object** anywhere in the `POOL_ITEMS` array (sorting is automatic)
3. **Required fields** (all of these must be present):

```typescript
{
  number: <next available integer>,  // Find max existing number, add 1
  category: 'Product',               // One of: Product, Technical, UX, Design, SP
  tag: '',                           // String, can be empty
  priority: 'High',                  // High, Medium, Low, TBD, TBC, or ''
  priorityScore: 8,                  // Computed from priority
  relatesTo: '',                     // String, can be empty
  complexity: 'Medium',              // High, Medium, Low, TBD, TBC, or ''
  complexityScore: 5,                // Computed from complexity
  totalScore: 13,                    // priorityScore + complexityScore
  track: '',                         // Usually empty
  ddaItem: false,                    // boolean
  featureName: 'My New Feature',     // Required, unique identifier
  summary: 'Description here',      // Short summary
  toBePickedUp: true,                // Always true for active items
  remarks: '',                       // String, can be empty
  alreadyPickedUp: false,           // true if startSprint <= 73
  startSprint: null,                 // number or null
  endSprint: null,                   // number or null
  externalVisible: false,            // boolean
}
```

4. **Optional epic detail fields** (add if available):

```typescript
{
  // ... required fields above ...
  epicName: 'My New Feature Epic Name',
  objectives: ['Objective 1', 'Objective 2'],
  description: 'Full description paragraph.',
  acceptanceCriteria: ['Criterion 1', 'Criterion 2'],
  owners: ['Product Management', 'Backend Development'],
  dependencies: ['Dependency 1'],
  targetAudience: ['UAE PASS users'],
}
```

5. **Score calculation checklist**:
   - Priority High -> priorityScore = 8
   - Priority Medium -> priorityScore = 5
   - Priority Low -> priorityScore = 3
   - Complexity Low -> complexityScore = 8
   - Complexity Medium -> complexityScore = 5
   - Complexity High -> complexityScore = 3
   - totalScore = priorityScore + complexityScore

6. **alreadyPickedUp calculation**:
   - If `startSprint` is `null`: set to `false`
   - If `startSprint <= 73` (current sprint): set to `true`
   - If `startSprint > 73`: set to `false`

### Updating an Existing Pool Item

1. **Find the item** by `number` or `featureName` in `poolItems.ts`
2. **Update only the fields that changed** -- preserve all other values
3. **Recalculate derived fields** if priority/complexity changed:
   - `priorityScore`, `complexityScore`, `totalScore`
4. **Recalculate `alreadyPickedUp`** if `startSprint` changed
5. **Do not change** the `number` field -- it is the stable identifier

### Matching Logic (for PPT extraction updates)

When updating pool items from extracted PPT data:

1. **Primary match**: `featureName` (case-insensitive, trimmed). Fuzzy matching acceptable for minor wording differences.
2. **Secondary match**: `epicName` against existing `epicName` values.
3. **Match found**: Update epic detail fields (`epicName`, `objectives`, `description`, `acceptanceCriteria`, `owners`, `dependencies`, `targetAudience`). Only overwrite with non-empty values.
4. **No match**: Create new item with `number = max(existing numbers) + 1`.

The PPT extraction uses `<!-- MATCH: number=N featureName="..." -->` comments to help identify matches.

---

## 4. Sprint System

### Current Sprint

**Current sprint is 73** (as of 2026-02-19).

### Sprint Cadence

- **Duration**: 2 weeks (10 working days)
- **Weekend days**: Saturday (6) and Sunday (0) -- UAE weekend
- **Bi-weekly sprints** with mid-week backlog refinement and Friday sprint reviews

### Sprint Configuration (Default)

```typescript
{
  firstSprintNumber: 71,
  firstSprintStartDate: '2026-01-01',  // Sprint 71 starts Jan 1, 2026
  workingDaysPerSprint: 10,
  weekendDays: [0, 6],  // Sunday, Saturday
}
```

### Sprint-to-Date Mapping

The app computes dates from sprint numbers using this algorithm:
1. Start from `firstSprintStartDate`
2. For each sprint offset, count `workingDaysPerSprint` working days (skipping weekends)
3. The sprint ends after 10 working days (approximately 2 calendar weeks)

Approximate sprint-to-date mapping for 2026:

| Sprint | Approximate Start |
|--------|------------------|
| 71 | 2026-01-01 |
| 72 | 2026-01-15 |
| 73 | 2026-01-29 |
| 74 | 2026-02-12 |
| 75 | 2026-02-26 |
| 76 | 2026-03-12 |
| 77 | 2026-03-26 |
| 78 | 2026-04-09 |
| 79 | 2026-04-23 |
| 80 | 2026-05-07 |
| 81 | 2026-05-21 |
| 82 | 2026-06-04 |
| 83 | 2026-06-18 |
| 84 | 2026-07-02 |
| 85 | 2026-07-16 |
| 86 | 2026-07-30 |
| 87 | 2026-08-13 |
| 88 | 2026-08-27 |
| 89 | 2026-09-10 |
| 90 | 2026-09-24 |
| 91 | 2026-10-08 |
| 92 | 2026-10-22 |
| 93 | 2026-11-05 |
| 94 | 2026-11-19 |
| 95 | 2026-12-03 |
| 96 | 2026-12-17 |

### `startSprint` vs `endSprint`

- `startSprint`: The sprint number when work on the feature begins. If `null`, the item is not yet scheduled.
- `endSprint`: The sprint number when work on the feature ends (inclusive). If `null`, the end date is undetermined.
- Both map to calendar dates via `sprintConfig`.

### `alreadyPickedUp` Calculation

```
alreadyPickedUp = (startSprint !== null) && (startSprint <= CURRENT_SPRINT)
```

Where `CURRENT_SPRINT = 73` as of 2026-02-19. This value must be updated as sprints advance.

Items with `alreadyPickedUp: true` are visually distinguished in the pool (typically grayed out or marked with a badge).

---

## 5. Build and Deploy Process

### Prerequisites

- Node.js installed (npm available)
- Python available at `C:\Users\fadib\AppData\Local\Programs\Python\Python311\python.exe` (may be needed for PPT processing)
- Git configured with SSH remote

### Build

```bash
cd D:\claude\roadmap-builder && npm run build
```

This runs `tsc -b && vite build`, producing output in `D:\claude\roadmap-builder\dist\`.

**Always run build after editing TypeScript files** to catch type errors before committing.

### Deploy to GitHub Pages

The app is served from the `docs/` folder. After building, copy the dist output:

```bash
xcopy /E /Y "D:\claude\roadmap-builder\dist\*" "D:\claude\roadmap-builder\docs\"
```

### Commit and Push

```bash
git -C "D:\claude\roadmap-builder" add src/data/poolItems.ts docs/
git -C "D:\claude\roadmap-builder" commit -m "your commit message"
git -C "D:\claude\roadmap-builder" push
```

The git remote uses SSH, so push should work without auth prompts.

### Full Update Workflow (end to end)

1. Edit `D:\claude\roadmap-builder\src\data\poolItems.ts`
2. Build: `cd D:\claude\roadmap-builder && npm run build`
3. Verify no errors
4. Deploy: `xcopy /E /Y "D:\claude\roadmap-builder\dist\*" "D:\claude\roadmap-builder\docs\"`
5. Stage: `git -C "D:\claude\roadmap-builder" add src/data/poolItems.ts docs/`
6. Commit: `git -C "D:\claude\roadmap-builder" commit -m "update: description"`
7. Push: `git -C "D:\claude\roadmap-builder" push`

---

## 6. PPT Extraction Workflow

### Pipeline Overview

```
ppt roadmap.pptx  -->  ppt_roadmap_extracted.md  -->  poolItems.ts
     (source)           (intermediate, extracted)       (final, code)
```

### Files Involved

| File | Path | Purpose |
|------|------|---------|
| Source PPT | `D:\claude\ppt roadmap.pptx` | The original PowerPoint with 34 slides, 29 epics |
| Structure spec | `D:\claude\ppt_roadmap_structure_request.md` | Defines the exact markdown format for extraction |
| Extracted data | `D:\claude\ppt_roadmap_extracted.md` | Markdown file with all epic details, produced by PPT extraction agent |
| Pool items code | `D:\claude\roadmap-builder\src\data\poolItems.ts` | TypeScript data file that gets updated |

### How to Parse `ppt_roadmap_extracted.md`

The extracted file contains:

1. **Summary Table** at the top with all epics: Pool Item #, Feature Name, Category, Priority, Complexity, DDA Item, Sprints, Start/End Dates.

2. **Individual Epic Sections** formatted as:
   ```
   ## Epic N -- Slide M: Epic Name

   **Pool Item #**: #<number>
   **Category**: <category>
   ...

   ### Objectives
   - bullet points

   ### Description
   paragraph

   ### Acceptance Criteria
   - bullet points

   ### Owners
   - bullet points

   ### Dependencies
   - bullet points

   ### Timeline
   - **Sprints**: NN-MM

   ### Target Audience
   - bullet points
   ```

### The MATCH Comment Convention

In the extraction markdown, each epic may include a match comment:

```markdown
<!-- MATCH: number=35 featureName="Design Audit" -->
```

This maps the extracted epic to an existing pool item by number. Use this to identify which pool item to update.

### Update Process from PPT Extraction

1. Read `D:\claude\ppt_roadmap_extracted.md`
2. For each epic section:
   a. Check for `<!-- MATCH: number=N ... -->` comment
   b. If found, find pool item with that number in `poolItems.ts`
   c. If not found, fuzzy-match on `featureName` (case-insensitive)
   d. Update matching pool item's epic fields (objectives, description, acceptanceCriteria, owners, dependencies, targetAudience, epicName)
   e. Update sprint ranges if the PPT has different/new sprint data
   f. Only overwrite with non-empty values
3. For unmatched epics, create new pool items with auto-assigned numbers
4. Build and deploy

### Sprint Data from PPT

The PPT summary table includes sprint ranges and calendar dates. Some items have sprints listed (e.g., "73-77"), while others only have dates. When sprint numbers are available, update `startSprint` and `endSprint`. When only dates are available, you can leave sprint fields as-is or calculate approximate sprint numbers using the sprint-to-date mapping.

---

## 7. Current Pool Items Reference Table

All 28 pool items as of 2026-02-19, sorted by totalScore descending:

| # | featureName | category | priority | complexity | totalScore | startSprint | endSprint | alreadyPickedUp |
|---|------------|----------|----------|-----------|------------|-------------|-----------|-----------------|
| 35 | Design Audit | Design | High | Low | 16 | 74 | 77 | false |
| 40 | Enable Download of All Issued Documents in DV | Product | High | Low | 16 | 87 | 88 | false |
| 10 | Auto-Add Documents Launch / One-Time Consent | Product | High | Low | 16 | 81 | 86 | false |
| 19 | Form Filler | SP | High | Low | 16 | 79 | 82 | false |
| 52 | UAEVerify SEO | SP | High | Low | 16 | 73 | 73 | true |
| 53 | Service Provider SDK | SP | High | Low | 16 | null | null | false |
| 54 | DR Automation | Technical | High | Low | 16 | null | null | false |
| 55 | SP Automation Testing Suite | SP | High | Low | 16 | 75 | 76 | false |
| 56 | Blockchain Upgrade | Technical | High | Low | 16 | null | null | false |
| 57 | CI/CD Pipeline Automation | Technical | High | Low | 16 | null | null | false |
| 58 | Operation Automation | Technical | High | Low | 16 | null | null | false |
| 28 | Infinite Loaders Detection and Resolution | Technical | High | Low | 16 | 70 | 75 | true |
| 29 | Firebase Configuration & Optimization | Technical | High | Low | 16 | null | null | false |
| 1 | Status-Based Reporting Implementation | Product | High | Medium | 13 | 70 | 72 | true |
| 17 | Home Page Revamp | UX | High | Medium | 13 | 74 | 76 | false |
| 16 | Design System Update | Design | High | Medium | 13 | 76 | 78 | false |
| 5 | User Behavior Analytics Tool Selection | Product | High | Medium | 13 | 82 | 84 | false |
| 7 | UX Enhancements Bundle - Revisit Documents List View | UX | High | Medium | 13 | 75 | 76 | false |
| 8 | Error-to-Status Code Linking System | Technical | High | Medium | 13 | null | 76 | false |
| 9 | Dual Citizenship GA | Product | High | Medium | 13 | 72 | 72 | true |
| 18 | UX/UI Enhancements Bundle 2 | UX | High | Medium | 13 | 87 | 94 | false |
| 37 | Enhancement/Revamp Document Request | UX | High | Medium | 13 | 77 | 80 | false |
| 38 | Revamp Document Sharing | UX | High | Medium | 13 | 81 | 86 | false |
| 47 | ELK Stack AI Upgrade | Technical | High | Medium | 13 | null | null | false |
| 51 | QR Code Simplification - Direct Sharing | SP | High | Medium | 13 | 73 | 77 | true |
| 26 | License QR Code Display Fix | Technical | Medium | Low | 13 | null | null | false |
| 20 | Consent Sharing (Third Party Data) | Product | High | High | 11 | 83 | 85 | false |
| 32 | Automated Testing | Technical | High | High | 11 | null | null | false |
| 36 | Accessibility Enhancement | Design | High | High | 11 | 79 | 82 | false |
| 41 | Physical Document Sharing | Product | High | High | 11 | 89 | 94 | false |
| 50 | SP Offboarding | SP | Medium | Medium | 10 | 73 | 76 | true |

**Items already picked up** (startSprint <= 73): #1, #9, #28, #50, #51, #52

---

## 8. Store Actions Reference

All actions are defined in `D:\claude\roadmap-builder\src\store\roadmapStore.ts`.

### Pool Item Actions

#### `addPoolItem(item: Omit<PoolItem, 'number'>)`
- **What**: Adds a new pool item, auto-assigning the next available `number`
- **When**: When a completely new feature is discovered that does not exist in the pool
- **Note**: Finds max number among existing items and adds 1

#### `updatePoolItem(number: number, updates: Partial<Omit<PoolItem, 'number'>>)`
- **What**: Updates fields of an existing pool item identified by `number`
- **When**: Updating sprint ranges, epic details, priority, etc.
- **Note**: Merges `updates` into existing item. Only provided fields are overwritten.

#### `deletePoolItem(number: number)`
- **What**: Removes a pool item by number
- **When**: Rarely used. Only if an item is permanently removed from scope.

#### `resetPoolItems()`
- **What**: Resets all pool items to the hardcoded defaults in `DEFAULT_POOL_ITEMS`
- **When**: To discard runtime edits and revert to the code-level data

### Roadmap Item Actions

#### `addItemBySprint(name: string, startSprint: number, endSprint: number)`
- **What**: Creates a new roadmap item using sprint numbers
- **When**: Adding a generic item (not from pool) by sprint range

#### `addItemByDate(name: string, startDate: string, endDate: string)`
- **What**: Creates a new roadmap item using ISO date strings
- **When**: Adding a generic item by date range

#### `addFromPool(name, startSprint, durationSprints, poolItemNumber, category, priority, complexity, ddaItem)`
- **What**: Adds a pool item to the roadmap timeline with all metadata
- **When**: User clicks "Add to Roadmap" from the pool panel
- **Note**: Copies epic detail fields from the pool item. `endSprint = startSprint + durationSprints - 1`

#### `updateItem(id: string, updates: Partial<Omit<RoadmapItem, 'id' | 'createdAt' | 'subtasks'>>)`
- **What**: Updates a roadmap item. Recalculates subtasks if sprint/date range changes.
- **When**: Editing item details or dragging items on the timeline

#### `deleteItem(id: string)`
- **What**: Removes a roadmap item from the timeline
- **When**: User removes item from roadmap

### Subtask Actions

#### `updateSubtaskOverride(itemId, subtaskId, startDate?, endDate?)`
- **What**: Sets override dates for a specific subtask (REQ_UX, DEV, or QA phase)
- **When**: Manually adjusting phase timing

#### `resetSubtaskOverride(itemId, subtaskId)`
- **What**: Clears override dates, reverting to auto-calculated dates
- **When**: Resetting a manually adjusted subtask

### Marker Actions

#### `addReleaseMarker(name: string, date: string)`
- **What**: Adds a vertical release marker on the timeline at a specific date

#### `updateReleaseMarker(id, updates)` / `deleteReleaseMarker(id)`
- **What**: Modify or remove release markers

#### `addCodeFreezeMarker(name: string, afterSprint: number)`
- **What**: Adds a code freeze marker at the end of a specific sprint

#### `updateCodeFreezeMarker(id, updates)` / `deleteCodeFreezeMarker(id)`
- **What**: Modify or remove code freeze markers

### Configuration Actions

#### `updateSprintConfig(updates: Partial<SprintConfig>)`
- **What**: Updates sprint configuration (first sprint number, start date, etc.)

#### `setDisplaySprintCount(count: number)`
- **What**: Sets how many sprints to show on timeline. Default: 26 (full year).

#### `setTimingUnit(unit: TimingUnit)`
- **What**: Switches between `'sprints'` and `'dates'` timing mode

#### `setShowSprintActivities(show: boolean)`
- **What**: Toggles visibility of subtask phases (REQ_UX/DEV/QA) on timeline

#### `setSelectedCategories(categories: CategoryType[])`
- **What**: Sets which categories to display. Empty array = show all.

#### `toggleCategory(category: CategoryType)`
- **What**: Toggles a single category in the filter

#### `setShowExternalOnly(show: boolean)`
- **What**: When true, only shows items with `externalVisible: true`

#### `setSnapMode(mode: 'day' | 'sprint')`
- **What**: Controls timeline drag snapping behavior

### Ordering Actions

#### `reorderItems(orderedIds: string[])`
- **What**: Reorders roadmap items to match the given ID sequence

#### `sortItemsByStartDate()`
- **What**: Sorts all roadmap items by their start date (earliest first)

### Sync Action

#### `syncEpicDetailsFromPool()`
- **What**: Copies epic detail fields from pool items to their corresponding roadmap items
- **When**: After updating pool item epic details, to propagate changes to the timeline
- **Note**: Only fills **empty** fields on the roadmap item. Does not overwrite existing values.

### Import/Export Actions

#### `exportData(): string`
- **What**: Returns JSON string of entire app state (config, items, markers, pool, settings)

#### `importData(jsonString: string): boolean`
- **What**: Replaces entire app state from a JSON string. Returns true on success.

#### `clearAllData()`
- **What**: Resets everything to defaults (empty roadmap, default pool items, default config)

### Selector Hooks

```typescript
useSprintConfig()         // SprintConfig
useItems()                // RoadmapItem[]
useReleaseMarkers()       // ReleaseMarker[]
useCodeFreezeMarkers()    // CodeFreezeMarker[]
useDisplaySprintCount()   // number
useTimingUnit()           // TimingUnit
useAddedPoolNumbers()     // Set<number> -- pool items already on roadmap
usePoolItems()            // PoolItem[]
useShowSprintActivities() // boolean
useSelectedCategories()   // CategoryType[]
useShowExternalOnly()     // boolean
useSnapMode()             // 'day' | 'sprint'
getTemporalStore()        // Undo/redo store (zundo)
```

---

## 9. Common Tasks and How to Do Them

### Task: Add Sprint Ranges to Pool Items from PPT Data

**Scenario**: The PPT roadmap has been updated with new sprint assignments. You need to update pool items.

1. Read `D:\claude\ppt_roadmap_extracted.md`
2. Look at the Summary Table for sprint ranges per epic
3. For each item with updated sprints:
   a. Find the item in `D:\claude\roadmap-builder\src\data\poolItems.ts` by `number`
   b. Update `startSprint` and `endSprint`
   c. Recalculate `alreadyPickedUp` based on whether `startSprint <= 73`
4. Build: `cd D:\claude\roadmap-builder && npm run build`
5. Deploy: `xcopy /E /Y "D:\claude\roadmap-builder\dist\*" "D:\claude\roadmap-builder\docs\"`
6. Commit and push

### Task: Add a Completely New Pool Item

**Scenario**: A new feature has been approved and needs to be added to the pool.

1. Open `D:\claude\roadmap-builder\src\data\poolItems.ts`
2. Find the current maximum `number` in the array (scan for highest number)
3. Create a new object with `number = max + 1`
4. Fill all required fields (see section 3)
5. Calculate scores: priorityScore, complexityScore, totalScore
6. Set `alreadyPickedUp` based on startSprint
7. Add epic detail fields if available
8. Place the object anywhere in the array (`.sort()` handles ordering)
9. Build, deploy, commit

### Task: Fix a Description Error in a Pool Item

1. Open `D:\claude\roadmap-builder\src\data\poolItems.ts`
2. Find the item by number or featureName
3. Update the `description`, `summary`, or other text field
4. Build, deploy, commit

### Task: Sync Epic Details from Pool to Roadmap Items

This happens at runtime in the browser:

1. The user updates pool item epic details (or the code is updated and deployed)
2. In the UI, trigger the "Sync Epic Details" action
3. Or programmatically: the `syncEpicDetailsFromPool()` store action copies empty fields from pool items to their corresponding roadmap items

**Important**: This action only fills empty fields on roadmap items. It does NOT overwrite existing values.

### Task: Export Roadmap Data

In the UI:
1. Open the Data Controls panel
2. Click "Export" to get a JSON string
3. The JSON contains the full app state

Programmatically, call `useRoadmapStore.getState().exportData()`.

---

## 10. File Structure Map

```
D:\claude\
|-- CLAUDE.md                                -- Project instructions and conventions
|-- roadmap_builder_expert_knowledge.md      -- THIS FILE
|-- ppt roadmap.pptx                         -- Source PowerPoint (34 slides)
|-- ppt_roadmap_extracted.md                 -- Extracted PPT data (29 epics)
|-- ppt_roadmap_structure_request.md         -- Extraction format specification
|-- roadmap_v5_scored.csv                    -- Original scoring spreadsheet
|
|-- roadmap-builder\                         -- React application root
    |-- package.json                         -- Dependencies and scripts
    |-- tsconfig.json                        -- TypeScript configuration
    |-- index.html                           -- Entry HTML
    |-- vite.config.ts                       -- Vite build configuration
    |
    |-- src\
    |   |-- App.tsx                          -- Root React component
    |   |-- main.tsx                         -- Entry point
    |   |-- vite-env.d.ts                    -- Vite type declarations
    |   |
    |   |-- types\
    |   |   |-- index.ts                     -- ALL type/interface definitions
    |   |
    |   |-- data\
    |   |   |-- poolItems.ts                 -- Pool items data + category colors + helpers
    |   |
    |   |-- store\
    |   |   |-- roadmapStore.ts              -- Zustand store (all state + actions)
    |   |
    |   |-- utils\
    |   |   |-- subtaskAllocation.ts         -- Subtask generation logic (REQ_UX/DEV/QA)
    |   |   |-- workingDays.ts               -- Working day calculations
    |   |   |-- pptxExport.ts                -- PPTX export logic
    |   |
    |   |-- components\
    |       |-- EditorPanel.tsx              -- Main editor sidebar
    |       |-- ItemPool.tsx                 -- Pool items list and filtering
    |       |-- ItemForm.tsx                 -- Add/edit item form
    |       |-- ItemList.tsx                 -- Roadmap items list
    |       |-- TimelineView.tsx             -- vis-timeline rendering
    |       |-- EpicsView.tsx                -- Epic detail cards view
    |       |-- EpicEditModal.tsx            -- Modal for editing epic details
    |       |-- SubtaskEditor.tsx            -- REQ_UX/DEV/QA phase editor
    |       |-- DataControls.tsx             -- Import/Export/Clear controls
    |       |-- ReleaseMarkerList.tsx        -- Release marker management
    |       |-- CodeFreezeMarkerList.tsx     -- Code freeze marker management
    |
    |-- dist\                                -- Build output (generated)
    |-- docs\                                -- GitHub Pages deploy target (copy of dist)
    |-- node_modules\                        -- Dependencies (not committed)
```

---

## 11. Gotchas and Common Mistakes

### Path Separators
- Use `\` in Windows shell commands and file paths
- Use `/` in TypeScript import statements
- Example: `import { PoolItem } from '../types';` (forward slash in TS)
- Example: `xcopy /E /Y "D:\claude\roadmap-builder\dist\*"` (backslash in shell)

### Shell Commands on Windows
- The environment uses bash on Windows. Standard Unix commands like `ls`, `cat`, `test` work.
- For file copying, `xcopy` is the reliable Windows option.

### Array Sorting
The `POOL_ITEMS` array has a `.sort()` call at the bottom of the array:
```typescript
].sort((a, b) => {
  if (a.totalScore !== b.totalScore) return b.totalScore - a.totalScore;
  const pa = getPriorityOrder(a.priority);
  const pb = getPriorityOrder(b.priority);
  if (pa !== pb) return pa - pb;
  return a.number - b.number;
});
```
**Never manually reorder items.** Just add them anywhere and the sort handles it.

### alreadyPickedUp Sync
This field must be manually kept in sync with `startSprint` and the current sprint number (73). There is no automatic recalculation. When updating `startSprint`, always update `alreadyPickedUp` accordingly.

### PPT Slides with Swapped Sections
Some PPT slides have Description and Acceptance Criteria sections swapped (slides 13, 14, 18 are known offenders). The extraction file notes these with `> Note:` comments. When consuming this data, use semantic meaning to assign content to the correct field.

### Build Before Commit
**Always run `npm run build`** after editing TypeScript files. The build step runs `tsc -b` first, which catches type errors. A successful build means the code is type-safe.

### Git Remote is SSH
The repository uses SSH for the git remote. Push operations should work without authentication prompts. If they fail, it is an SSH key issue, not a credentials issue.

### Zustand Persistence
The store uses `persist` middleware with `localStorage` key `'roadmap-builder-storage'`. This means:
- Changes to `POOL_ITEMS` in code will NOT automatically appear for users who have persisted state
- Users must click "Reset Pool Items" or "Clear All Data" to pick up code changes
- The `resetPoolItems()` action reloads from `DEFAULT_POOL_ITEMS` (the hardcoded array)

### Undo/Redo (zundo)
The store uses `zundo` temporal middleware for undo/redo, but it only tracks the `items` array (roadmap items), not pool items or settings. Limit is 50 states.

### Item Number Stability
Pool item `number` values are stable identifiers. Never reassign or renumber items. They are referenced by roadmap items (`poolItemNumber`) and in the PPT extraction (`MATCH` comments).

### Category Values
Category must be exactly one of: `'Product'`, `'Technical'`, `'UX'`, `'Design'`, `'SP'`. Case-sensitive. Any other value will not match colors or filters.

### PPT Extraction: Home Page Revamp Category
In the PPT extraction, Home Page Revamp is listed under "Design" category, but in the pool items code it is listed as "UX" category. The pool items code is the source of truth. When consuming PPT data, be aware of such discrepancies and prefer the existing pool item category unless there is an explicit request to change it.

### Display Sprint Count
Default is 26 sprints (covers full year 2026: Sprint 71 through 96). The timeline shows sprints from `firstSprintNumber` through `firstSprintNumber + displaySprintCount - 1`.

---

## Appendix A: PPT Summary Table Cross-Reference

The PPT extraction at `D:\claude\ppt_roadmap_extracted.md` contains a summary table with sprint ranges that may differ from the pool items code. When the PPT is the authoritative source for sprint scheduling, update pool items accordingly. Key differences to watch:

- Some PPT items show only dates without sprint numbers (e.g., Firebase Configuration, Service Provider SDK, DR Automation, etc.)
- Some PPT items have different category assignments than the pool (e.g., Home Page Revamp: PPT says "Design", pool says "UX"; QR Code Simplification: PPT says "Technical", pool says "SP"; Form Filler: PPT says "Product", pool says "SP")
- Error-to-Status Code Linking (#8): PPT shows startSprint=74 while pool has startSprint=null

Always verify with the team which source is authoritative before making bulk updates.

---

## Appendix B: Quick Score Calculator

```
Feature: ____________
Priority: High(8) / Medium(5) / Low(3) / TBD(0)  -> priorityScore = ___
Complexity: Low(8) / Medium(5) / High(3) / TBD(0) -> complexityScore = ___
                                            totalScore = priorityScore + complexityScore = ___
```

Remember: Low complexity = HIGH score (8). This is intentional -- easy-to-build features score higher.
