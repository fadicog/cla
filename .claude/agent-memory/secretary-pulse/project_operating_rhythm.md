---
name: DV Operating Rhythm and Tools
description: Sprint cadence, approval workflows, tools, and file structure for the DV PM workspace
type: project
---

**Why:** Understanding the cadence helps set realistic timelines and flag when approvals or reviews need to be initiated early.

**How to apply:** When estimating timelines, factor in DDA's 2-4 week review cycles for UX changes and App Store release cycles of 1-2 weeks. Sprint reviews happen on Fridays; refinement mid-week.

## Sprint Cadence
- Bi-weekly (2-week sprints)
- Mid-week: Backlog refinement
- Friday: Sprint review
- Current sprint range: Sprint 70-72 active as of early 2026

## Tools
| Tool | Purpose |
|------|---------|
| Jira | "DV Product" board — sprint tracking, epics, tickets |
| Figma | "DV Refresh 2024/25" — design source of truth |
| SharePoint | Slides, roadmaps, presentations |
| Firebase | Push notifications, Remote Config (feature flags) |
| Metabase | BI / reporting dashboards (referenced in reporting stack) |
| ELK Stack | Log analysis (ELK AI Upgrade planned) |

## Key Files in Workspace (D:\claude\)
| File | Purpose |
|------|---------|
| `uae_pass_knowledge_base.md` | Source of truth — 17 sections covering product, tech, UX |
| `pm_dv_working_doc.md` | Living PM working document — priorities, decisions, backlog |
| `roadmap_2026_dv.md` | Full 2026 roadmap (v1.1, draft pending stakeholder review) |
| `features_prioritization_2026_v2_summary.md` | 37-feature prioritized backlog with scoring |
| `roadmap-builder/` | Interactive React roadmap tool |
| `roadmap-light/roadmap-light.html` | Single-file PowerPoint-ready Gantt export tool |
| `UAE_PASS_DV_2026_Roadmap.pptx` | 10-slide stakeholder roadmap deck |
| `research_qr_verification_benchmarking.md` | 63-page QR competitive analysis |
| `presentation_qr_verification_strategy.md` | 19-slide QR strategy stakeholder deck |
| `document_sharing_analysis_report.md` | 350K+ sharing request data analysis |
| `key_insights_summary.md` | Executive one-page summary of sharing analysis |
| `session_sharing_request_status_tracking.md` | 23-status-code system design |
| `sharing_request_status_codes.csv` | Status code lookup table |
| `uaepass_dashboard_report.html` | Interactive visualization dashboard |

## Documentation Conventions
- All user-facing content: bilingual EN/AR with RTL support
- Avoid "vault" — use "Documents" / «المستندات»
- Placeholders in PM doc: `_[TO BE FILLED]_`, `_[?]_`, `_[TO BE CLARIFIED]_`
- Decisions logged in Decision Log table with date, rationale, stakeholders, status
- Numbered sections: `## N) Feature Name`
- Timestamps on knowledge base updates

## Decision-Making
- Major features: DDA design approval + TDRA policy alignment (both required)
- Legal changes: TDRA legal team sign-off
- PM authority scope: `_[TO BE CLARIFIED]_`
