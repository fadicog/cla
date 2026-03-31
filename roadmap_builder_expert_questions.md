# roadmap-builder-expert Questions

## Q1: Sprint Number Anchoring and Date Calculation

The default sprint config has `firstSprintNumber: 71` and `firstSprintStartDate: '2026-01-01'`. The PPT extracted data shows Sprint 71–72 = Jan 1–28 2026, and the current date is 2026-02-19. What is the actual current sprint number as of today? The system prompt says items in progress are Sprint 70 and 72, but the store config starts at Sprint 71. Is Sprint 70 a past sprint that predates the roadmap window?

## Q2: Sprint Number vs Pool Item startSprint Discrepancy

The CSV shows `Status-Based Reporting Implementation` with `Start Sprint = 70`, and `Infinite Loaders Detection and Resolution` with `Start Sprint = 70`. But the default sprint config uses Sprint 71 as the first sprint (starting 2026-01-01). Sprint 70 would therefore be before the roadmap window. How should Sprint 70 items be displayed — are they treated as "already started" and pinned to the first visible sprint, or shown starting before the visible range?

## Q3: Pool Item Number Gaps and CSV vs poolItems.ts Divergence

The CSV (`roadmap_v5_scored.csv`) contains item numbers and feature names that differ from `poolItems.ts`. For example:
- CSV has item 43 "DR Automation (Disaster Recovery)" and 44 "Blockchain Upgrade" and 45 "CI/CD Pipeline Automation" and 53 "SP Integration through SDK" — these differ from `poolItems.ts` which has items 54 "DR Automation", 56 "Blockchain Upgrade", 57 "CI/CD Pipeline Automation", 53 "Service Provider SDK".
- The CSV appears to be an older version. Is `poolItems.ts` the authoritative source of truth for item numbers and data, or should the CSV be kept in sync?

## Q4: Category Assignment Discrepancy — Home Page Revamp

In `poolItems.ts`, item #17 "Home Page Revamp" has `category: 'UX'` but in the PPT extracted data (Epic 4), it is listed with `Category: Design`. The PPT summary table also shows it as Design. Which category is correct for this item?

## Q5: Category Assignment Discrepancy — QR Code Simplification

In `poolItems.ts`, item #51 "QR Code Simplification – Direct Sharing" has `category: 'SP'`, but in the PPT extracted data (Epic 18), it is listed as `Category: Technical`. Which is correct?

## Q6: Form Filler Category Discrepancy

In `poolItems.ts`, item #19 "Form Filler" has `category: 'SP'`, but in the PPT summary table (Epic 5), it is listed as `Category: Product`. Which is correct?

## Q7: alreadyPickedUp Flag Semantics

The `alreadyPickedUp` boolean in `PoolItem` indicates an item is in progress. But when a pool item is added to the roadmap via `addFromPool`, the roadmap item has its own sprint range. Does `alreadyPickedUp: true` on a pool item have any visible effect in the UI (e.g., badge, color, ordering)? Or is it purely informational metadata that tells the consuming agent the item is already in a sprint?

## Q8: Relationship Between PoolItem.startSprint and RoadmapItem.startSprint

When a pool item has a `startSprint` defined (e.g., item #9 Dual Citizenship has `startSprint: 72`), and a user clicks "Add to Roadmap" from the pool, does the app pre-populate the sprint fields with the pool item's `startSprint`/`endSprint`? Or does the user always specify these manually?

## Q9: The syncEpicDetailsFromPool Action

The store has `syncEpicDetailsFromPool()` which copies epic fields from pool items to roadmap items (for fields that are empty). Is this intended to be called manually by the user (via the "Sync Epic Details" button), or should it be called automatically when a pool item is updated? If a pool item's description is updated in `poolItems.ts` and the roadmap item already has a description, the sync will NOT overwrite it — is that the intended behavior?

## Q10: externalVisible Flag — Currently All False

All 31 pool items have `externalVisible: false`. The store has a `showExternalOnly` filter. Is the external visibility feature fully implemented and just not yet configured for any items, or is it a feature under development?

## Q11: Build and Deploy Workflow

The vite config has `base: '/roadmapbuilder/'` and `outDir: 'docs'`. The `docs/` directory is present. Is the app deployed to GitHub Pages (since docs/ is a common GitHub Pages target)? What is the exact deploy command — just `npm run build`? And is there a dev server command to preview changes locally before building?

## Q12: Temporal (Undo/Redo) Only Tracks Items

The temporal middleware in the store has `partialize: (state) => ({ items: (state as any).items })`, meaning only `items` array changes are tracked for undo/redo. Changes to `poolItems`, `sprintConfig`, `releaseMarkers`, and `codeFreezeMarkers` are NOT undoable. Is this intentional? Could updating `poolItems.ts` and triggering a resetPoolItems() cause unexpected undo behavior?

## Q13: Zustand persist — What Gets Persisted?

The store uses `persist` with `name: 'roadmap-builder-storage'`. Looking at the config, it appears the full state is persisted to localStorage (no `partialize` on the persist layer — only on temporal). This means poolItems from `poolItems.ts` are the initial values, but once the app runs, the localStorage-persisted state overrides `DEFAULT_POOL_ITEMS`. Does this mean that updating `poolItems.ts` in code will NOT reflect in the app unless the user clicks "Clear All" or manually resets? What is the correct workflow for propagating `poolItems.ts` changes to a running app?

## Q14: EpicsView Component — What Does It Display?

The `App.tsx` shows two tabs: "Timeline" and "Epics". The "Epics" tab renders `EpicsView`. What does this view show — the pool items' epic details, or the roadmap items' epic details? Is it used for PPT export (`pptxExport.ts` is in utils)?

## Q15: Missing ELK Stack AI Upgrade from PPT

The PPT extracted data has 29 epics but item #47 "ELK Stack AI Upgrade" appears in `poolItems.ts` but NOT in the `ppt_roadmap_extracted.md`. Was this item intentionally excluded from the PPT roadmap, or was it missed during extraction? If excluded, should it remain in the pool or be removed?

## Q16: Item Numbers — Are They Stable Identifiers?

The `number` field in `PoolItem` is used as the primary identifier to match pool items to roadmap items (`poolItemNumber` in `RoadmapItem`). If a pool item's number is changed (e.g., due to renumbering), existing roadmap items that reference the old number would lose their pool item association. Is the numbering scheme fixed/stable, or can numbers be reassigned?

## Q17: Complexity Score for TBD/TBC

The scoring spec says High=8, Medium=5, Low=3, TBD=0, TBC=0 (per the PPT structure spec). But in `poolItems.ts`, TBD complexity items have `complexityScore: 0` which would make their total score equal only their priority score. Is this the correct behavior? UAEVerify SEO has priority/complexity not specified — how should it be scored?

## Q18: Home Page Revamp Pool Item — Category Should Be UX or Design?

Specifically: in `poolItems.ts`, item #17 "Home Page Revamp" is in category `UX`, but `ddaItem: true`. Typically DDA items are in Design category. The PPT shows it in Design. Should the category in `poolItems.ts` be corrected to `Design`?
