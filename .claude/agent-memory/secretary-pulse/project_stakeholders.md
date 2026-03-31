---
name: DV Stakeholder Map
description: All stakeholders for the DV product, their roles, and decision authority
type: project
---

**Why:** DV operates in a multi-stakeholder environment. Features require alignment across multiple parties before delivery. Knowing who owns what prevents misdirected escalations.

**How to apply:** Tag tasks with the correct stakeholder. Flag when a task requires DDA design approval or TDRA policy alignment — these are mandatory gates for major features.

## Stakeholder Roles

| Shorthand | Full Name | Role |
|-----------|-----------|------|
| TDRA | Telecommunications and Digital Government Regulatory Authority | Regulator and product owner. Sets policy and priorities. Final authority on product direction. |
| DDA | Design Authority | Design/UX partner. Design approval required for all major features. Also runs the eSeal validation service (transitioning). |
| ICP | Identity and Citizenship Persons Authority | High-volume document issuer: EID, Visa, Passport. Transitioning to self-signing (own HSM) in 2025-2026. |
| SP | Service Providers | Banks, telcos, insurers. Consumers of user documents. Integration partners. |
| Engineering | DV Engineering Team | FE/BE/QA teams delivering features. Names TBD. |
| Ops | DV Ops Team | Monitoring, support, reliability. |
| Fadi | PM | Product Manager for DV. Primary contact. |

## Approval Gates
- Major features: DDA design approval + TDRA policy alignment (2-4 week review cycles)
- Legal changes (e.g., Auto-Add consent): TDRA legal sign-off required
- App releases: iOS/Android App Store cycles add 1-2 weeks

## Key External Contacts (as known)
- Product: Fadi (PM)
- Ahmed: UI/UX Designer on the DV team. Design audit lead. Produces Figma designs in "DV Refresh 2024/25" workspace. Confirmed active in Sprint 76 (Mar 12–25, 2026).
- Engineering, QA, TDRA, ICP contacts: TBD / to be clarified
