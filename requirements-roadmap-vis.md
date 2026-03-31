# Roadmap Builder (Sprint-based) — Requirements & Build Recommendation
Optimized for Claude Code (vibe coding)

## 1) Goal
Build a small interactive app that helps create and visualize a sprint-based roadmap similar to the attached example (timeline with dates, sprint boundaries, colored bars).  
User enters roadmap items with a start sprint + end sprint. The app auto-creates 3 subtasks per item:
1) Requirements & UX Finalization
2) Development
3) QA

The app:
- generates a calendar timeline with day numbers + dates
- shows sprint divisions (10 working days per sprint, Sat/Sun weekend)
- auto-distributes each item’s subtasks across the item’s sprint range
- allows manual override of each subtask start/end dates
- supports release-day markers (milestones)
- renders a right-side visual roadmap (Gantt-like) like the attached image

---

## 2) Core Concepts & Rules

### 2.1 Sprint definition
- Sprint length: **10 working days**
- Weekends: **Saturday + Sunday** (non-working)
- Sprint 71:
  - Starts: **01 Jan 2026**
  - Ends: **14 Jan 2026**
  - Explanation: 10 working days spread across calendar days (1–14 Jan, excluding Sat/Sun)

**Rule**: Sprint end date is the date of the 10th working day from the sprint start (inclusive), skipping weekends.

### 2.2 Roadmap item
A roadmap item is a high-level feature/initiative (e.g., “Documents tab refresh”).

Inputs (minimum):
- Item name
- Start sprint (e.g., 71)
- End sprint (e.g., 74)

Derived:
- Item start date (start date of start sprint)
- Item end date (end date of end sprint)

### 2.3 Subtasks (auto-created)
Each roadmap item automatically has 3 subtasks:
1) Requirements & UX Finalization
2) Development
3) QA

Default distribution across the item duration (configurable later, but start with fixed logic):
- Requirements & UX Finalization: **20%**
- Development: **60%**
- QA: **20%**

Distribution should be done over **working days** inside the item’s start/end date range.

**Auto allocation rule (v1)**:
- Compute total working days in item range.
- Allocate working days per subtask by percentages (rounded; ensure sum equals total).
- Assign each subtask to a continuous date range (working-day contiguous), in order:
  - Req/UX -> Dev -> QA
- Skip weekends automatically.

### 2.4 Manual override
User can override each subtask:
- set Start Date + End Date (calendar dates)
- app validates:
  - end >= start
  - subtask dates must stay within overall item date range (unless user explicitly chooses to “Allow overflow” — optional v2)
  - weekends allowed visually but **counting/validation** uses working days (v1: allow placing on weekend but warn; or snap to next working day)

### 2.5 Release days (milestones)
App supports “Release Day” markers shown as vertical lines/labels on the timeline.

Inputs:
- Release name (e.g., “March Release”)
- Release date (or “Release Sprint” which derives a date)

Display:
- Vertical line on timeline with a label at top (like attached).

---

## 3) User Experience (UI)

### 3.1 Layout
Two-pane layout:

**Left panel: Roadmap Editor**
- Sprint calendar configuration (read-only for v1 except start sprint/date)
- Item list (table)
- Add/Edit item form
- Subtask overrides (expand row to edit subtask date ranges)
- Release markers list (add/edit)

**Right panel: Roadmap Visualization**
- Timeline header: months + dates + day-of-week cues (optional)
- Sprint boundary lines + sprint labels (Sprint 71, Sprint 72…)
- Gantt bars for:
  - Items (optional as parent grouping row)
  - Subtasks (3 colored bars under each item)
- Release marker vertical lines
- Zoom / horizontal scroll

### 3.2 Left panel details

#### Items table fields (v1)
- Item Name
- Start Sprint (dropdown/number)
- End Sprint (dropdown/number)
- Auto Start Date (computed)
- Auto End Date (computed)
- Expand icon → shows subtasks

#### Subtask editor (inside expanded item)
For each subtask:
- Name (fixed)
- Auto Start / Auto End (computed)
- Override Start (date picker)
- Override End (date picker)
- “Reset to Auto” button
- Status indicator if override invalid

#### Add Item flow
- Click “+ Add Item”
- Enter name, start sprint, end sprint
- Save
- App generates subtasks + auto dates

#### Release markers
- “+ Add Release”
- Name + date (date picker)
- Save → vertical line in roadmap view

### 3.3 Visualization behavior
- Each item is rendered as a group with 3 subtask bars.
- Colors (example):
  - Req/UX: light purple
  - Dev: blue
  - QA: yellow
  (Exact palette not critical; must be distinct.)

- Sprint boundaries as vertical shaded bands or lines.
- Weekends optionally shaded.
- Hover on any bar shows tooltip:
  - item name
  - subtask name
  - start/end dates
  - working days count

---

## 4) Data Model (Local-first)

### 4.1 Entities

#### SprintConfig
- firstSprintNumber: number (71)
- firstSprintStartDate: ISO date string ("2026-01-01")
- workingDaysPerSprint: number (10)
- weekendDays: number[] (6,0) where 0=Sun, 6=Sat (JS convention)

#### RoadmapItem
- id: string (uuid)
- name: string
- startSprint: number
- endSprint: number
- subtasks: Subtask[]
- createdAt, updatedAt

#### Subtask
- id: string (uuid)
- type: "REQ_UX" | "DEV" | "QA"
- autoStartDate: ISO date
- autoEndDate: ISO date
- overrideStartDate?: ISO date
- overrideEndDate?: ISO date

#### ReleaseMarker
- id: string (uuid)
- name: string
- date: ISO date

### 4.2 Storage (v1)
- Use browser localStorage (simple).
- Export/Import JSON file for sharing.

Optional v2:
- Export to CSV or image/PDF.

---

## 5) Calculation Logic

### 5.1 Working day helpers
Implement:
- isWeekend(date): boolean
- nextWorkingDay(date): date
- addWorkingDays(date, n): date (n>=0)
- countWorkingDays(start, end): number (inclusive or exclusive — pick one and be consistent)

### 5.2 Sprint date generation
Given SprintConfig:
- sprintStartDate(sprintNumber) = compute by adding (sprintNumber - firstSprintNumber) * workingDaysPerSprint working days to the firstSprintStartDate (skipping weekends).
- sprintEndDate(sprintNumber) = addWorkingDays(sprintStartDate, workingDaysPerSprint - 1)

### 5.3 Item date range
- itemStartDate = sprintStartDate(startSprint)
- itemEndDate = sprintEndDate(endSprint)

### 5.4 Subtask auto allocation
- totalWD = working days between itemStartDate..itemEndDate
- reqWD = round(totalWD * 0.2)
- qaWD = round(totalWD * 0.2)
- devWD = totalWD - reqWD - qaWD

Assign contiguous blocks:
- reqStart = itemStartDate
- reqEnd = addWorkingDays(reqStart, reqWD - 1)
- devStart = nextWorkingDay(reqEnd + 1 calendar day)
- devEnd = addWorkingDays(devStart, devWD - 1)
- qaStart = nextWorkingDay(devEnd + 1 calendar day)
- qaEnd = addWorkingDays(qaStart, qaWD - 1)

Edge cases:
- If totalWD < 3, allocate minimum 1 day per stage if possible; otherwise shrink to available days.
- If rounding causes reqWD or qaWD = 0, set to 1 and adjust devWD accordingly (if totalWD allows).

### 5.5 Override precedence
Effective subtask dates:
- if overrideStartDate && overrideEndDate → use override
- else use auto

Validation:
- overrideStart <= overrideEnd
- effective subtask range must be within itemStart..itemEnd (v1)

---

## 6) Reporting & Export (v1)
- Export JSON (all config + items + releases)
- Import JSON to restore
- Optional: Export CSV of items + subtasks (flat rows)

CSV row example:
- item_id, item_name, subtask_type, start_date, end_date, start_sprint, end_sprint

---

## 7) Acceptance Criteria (v1)
1) App shows timeline with dates and sprint boundaries starting Sprint 71 (01 Jan 2026 → 14 Jan 2026).
2) Weekends are treated as non-working for calculations.
3) User can add an item with start/end sprint and see 3 auto-generated subtasks distributed across the duration.
4) User can override subtask start/end dates; visualization updates immediately.
5) App supports adding release markers displayed as vertical lines.
6) Data persists in localStorage and can be exported/imported via JSON.

---

## 8) Out of Scope (v1)
- Multi-user collaboration
- Authentication
- Backend storage
- Dependency mapping between items
- Resource capacity planning
- Printing-perfect export

---

## 9) Recommended Technology (best for Claude Code “vibe coding”)

### Option A (Recommended): Web app — React + TypeScript + Vite + vis-timeline
Why this is best:
- Fast to build, easy to iterate with Claude Code.
- Runs anywhere (no install for stakeholders).
- Supports interactive timeline/Gantt visuals with groups and items.
- Easy localStorage + import/export.
- Good control over sprint lines, weekend shading, and milestone markers.

Suggested stack:
- Frontend: React + TypeScript (Vite)
- Timeline/Gantt: `vis-timeline` (open-source timeline component)
- Styling: Tailwind or simple CSS
- State: Zustand or React state (v1)
- Date library: date-fns (for working-day utilities)

Deliverables:
- Single-page app with left editor + right timeline
- Local-first storage + JSON export/import

### Option B: Python Streamlit (Not recommended for this)
Pros: quick UI.
Cons: timeline/Gantt interactivity and drag/override UX is harder; you’ll end up fighting the framework.

### Option C: Desktop (Electron)
Overkill for v1 unless you need offline distribution as an executable.

**Final recommendation**: **Option A (React + Vite + vis-timeline)**.

---

## 10) Implementation Plan (Claude Code checklist)

### Phase 1 — Foundations
- Create Vite React TS project
- Implement SprintConfig and working-day functions
- Generate sprint timeline data (Sprint 71 onward for N sprints)

### Phase 2 — Data + Editor UI
- CRUD items
- Auto-generate subtasks
- Subtask override UI with date pickers
- LocalStorage persistence + JSON export/import

### Phase 3 — Timeline UI
- Render groups (items) and sub-items (subtasks)
- Render sprint boundaries and labels
- Render weekend shading
- Render release markers

### Phase 4 — Polish
- Validation messages
- Tooltips
- Zoom/scroll usability
- Basic export CSV

---

## 11) Questions to confirm before build
1) How many sprints should the timeline show by default (e.g., next 12 sprints / 6 months / 1 year)?
2) Do you want sprint labels to appear at the top or as a band (like “Sprint 56, 57…” in the sample)?
3) Should users be able to drag bars on the timeline (direct manipulation), or only edit via left panel (v1)?
4) Should the timeline show months as the top header row (like the attached) or keep it simpler in v1?
