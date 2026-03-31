# Jira User Story: Sharing Transactions Status Model & Funnel Reporting

## User Story

**As a** Product Manager
**I want** a lifecycle-based status tracking system for document sharing requests
**So that** we can identify where users drop off and optimize conversion rates across all channels

---

## Epic / Component
Digital Vault (DV) - Analytics & Reporting

---

## Description

Replace flat "transactions" counts with a detailed status lifecycle model that tracks every sharing request through 25+ status codes from creation to terminal outcome. Enable funnel analysis, drop-off identification, and performance metrics across 3 channels (Notification, Redirect, QR).

**Current State**: Basic transaction counts without visibility into user journey
**Desired State**: Detailed funnel reporting with drop-off points, conversion rates, and time-to-complete metrics

---

## Acceptance Criteria

### Backend / Analytics
- [ ] Create `sharing_status_history` table with schema: `request_id`, `status_code`, `status_ts`, `step_latency_ms`, `error_code`, `meta`
- [ ] Implement 25 status codes (S00-S44) covering request ingress, doc readiness, consent, PIN, terminals
- [ ] Enforce unique constraint: `(request_id, status_code, status_ts)`
- [ ] Build view `v_sharing_latest_status` for current request states
- [ ] Create aggregated table `daily_sharing_funnel` with conversion rates per channel/SP

### Frontend (UAE PASS App)
- [ ] Emit status events for: S08 (viewed), S10/S11 (docs ready/missing), S12-S15 (missing doc flow), S20-S21 (consent), S30-S32 (PIN), S40-S44 (terminals)
- [ ] Include metadata: `request_id`, `sp_id`, `channel`, `platform`, `required_docs[]`, `missing_count`, `error_code`
- [ ] Ensure events fire on iOS and Android with correct timestamps

### Reporting Dashboards
- [ ] **Funnel by channel**: Show S00 → S08 → S10/S11 → S20 → S21 → S30 → S31 → S40 with drop-off %
- [ ] **Document readiness**: % S10 vs S11 at first view, segmented by SP/doc-type
- [ ] **Missing-doc behavior**: Initiation rate (S12/S11), success rate (S13/S12), error rate (S14/S12)
- [ ] **Consent metrics**: Conversion rate (S21/S20), average dwell time in S20
- [ ] **PIN failures**: Fail rate (S32/(S31+S32)), post-PIN tech failures (S41/S31)
- [ ] **Terminal distribution**: S40/S41/S42/S43/S44 as % of S00, by channel/platform/SP
- [ ] **Time-to-complete**: Median and P90 from S00 → S40, step latency breakdown

### Data Quality
- [ ] Every request has S00 (request created)
- [ ] If user lands in app, S08 is present
- [ ] Status transitions are append-only, time-ordered, no duplicates
- [ ] Channel-specific statuses (S01-S03, S04-S05, S06-S07) only appear for correct channel
- [ ] Exactly one terminal status [T] per request

---

## Technical Notes

**Status Model**: Lifecycle-based with clear transitions (see §4 in requirements)

**Channels**:
- **Notification**: S00 → S01 → S02 → S03 → S08
- **Redirect**: S00 → S04 → S05 → S08
- **QR**: S00 → S06 → S07 → S08

**Terminal Statuses** [T]:
- S40: Share success
- S41: Technical error
- S42: Expired
- S43: User aborted
- S44: Not eligible (missing docs can't be retrieved)

**Event Schema** (minimum fields):
```json
{
  "event_name": "sharing_status_changed",
  "request_id": "REQ001234",
  "sp_id": "ADIB",
  "channel": "notification",
  "platform": "ios",
  "from_status": "S20",
  "to_status": "S21",
  "status_ts": "2025-11-28T10:15:30Z",
  "step_latency_ms": 4500,
  "doc_context": {
    "required_count": 2,
    "missing_count": 0
  },
  "error": {
    "code": "issuer_timeout",
    "source": "issuer"
  }
}
```

---

## Definition of Done

- [ ] Status tracking implemented for all 3 channels (iOS + Android)
- [ ] All 7 reporting dashboards deployed and accessible
- [ ] Data quality checks pass (100% S00, unique statuses, correct terminals)
- [ ] Metrics segmentable by: SP, channel, platform, app version, doc type
- [ ] Documentation updated with status dictionary and event schema
- [ ] Sample data validated against expected funnel patterns
- [ ] Stakeholder demo completed (PM, TDRA, DDA)

---

## Team Instructions: Using Sample Data & Visualizations

### 📁 Attached Resources

**Location**: `D:\cluade\`

1. **Requirements**: `Here.docx` - Full status model & reporting spec
2. **Sample Data**: `sharing_transactions_sample.csv` - 300 realistic requests (2,995 status records)
3. **Visualizations**: `visualizations/` folder - Interactive dashboard + 10 charts
4. **Analysis Reports**: Multiple `.md` files with insights

### 🚀 Quick Start (5 mins)

#### View the Dashboard
1. Open `D:\cluade\visualizations\interactive_dashboard.html` in browser
2. Explore funnel diagrams, conversion rates, drop-off points
3. Understand what "good" looks like (70% success baseline)

#### Understand the Data
```bash
# View sample data structure
head sharing_transactions_sample.csv

# Key fields:
# - request_id: Unique per sharing request
# - status_code: S00 through S44
# - channel: notification | redirect | qr
# - platform: ios | android
# - sp_id: Service provider
# - status_ts: Timestamp of status change
# - step_latency_ms: Time since previous status
```

#### Use for Development

**Backend Team**:
- Import `sharing_transactions_sample.csv` to test database schema
- Validate status transitions against requirements (§4)
- Test aggregation queries for funnel metrics

**Frontend Team**:
- Review status codes you need to emit (S08, S10/S11, S20-S21, S30-S32, S40-S44)
- Use sample data to validate event payloads
- Check channel-specific statuses (notification: S01-S03, redirect: S04-S05, qr: S06-S07)

**Analytics Team**:
- Load CSV into your BI tool (Tableau/PowerBI/Looker)
- Recreate funnel charts using Python scripts: `create_visualizations.py`, `create_dashboard.py`
- Reference `ANALYSIS_QUICK_START.md` for key metrics to track

**QA Team**:
- Use sample data as test cases (12 realistic scenarios included)
- Validate status transition rules (no S01 in QR flow, etc.)
- Check data quality: unique statuses, one terminal per request

### 📊 Key Metrics to Validate

From the sample data (baseline targets):
- **Overall Success Rate**: 70% (target: 75-80%)
- **Consent Rate**: 92% (S21/S20)
- **PIN Success**: 95% (S31/(S31+S32))
- **Median Journey Time**: 33 seconds
- **Channel Success**: Notification 75.6%, Redirect 64.5%, QR 63.2%

### 📖 Read These First

1. **Requirements**: `Here.docx` (sections 3-7 are critical)
2. **Quick Analysis**: `ANALYSIS_QUICK_START.md` (15 min read)
3. **Visualization Guide**: `QUICKSTART_VISUALIZATIONS.md` (how to read funnels)

### ⚠️ Important Notes

- **Status codes are sequential but not all appear in every flow** (e.g., S01-S03 only for notification)
- **Terminal statuses are exclusive**: Each request ends with exactly ONE of S40/S41/S42/S43/S44
- **S08 is universal**: All channels converge at "request viewed" - use this as primary funnel anchor
- **Timestamps must be ordered**: Validate `status_ts` increases monotonically per `request_id`

### 🎯 Success Criteria

Your implementation is correct when:
1. You can recreate the funnel diagrams from sample data
2. Terminal distribution matches: ~70% S40, ~16% S43, ~10% S42, ~3% S41, ~1% S44
3. Every request has S00 and exactly one terminal status
4. Channel-specific statuses only appear for correct channel

---

## Story Points
**Estimate**: 13 points

**Breakdown**:
- Backend schema + events (5 pts)
- Frontend instrumentation (3 pts)
- Reporting dashboards (3 pts)
- Testing + validation (2 pts)

---

## Priority
**High** - Enables data-driven optimization of 70% → 85%+ success rate

---

## Dependencies
- DB migration approval
- Analytics platform access (Tableau/PowerBI/Firebase)
- Coordination with SPs for correlation ID uniqueness (separate initiative)

---

## Related Stories
- DV-XXX: Fix duplicate correlation ID issue
- DV-XXX: Document pre-check API (depends on this story's insights)
- DV-XXX: Consent screen UX improvements (informed by drop-off data)

---

## Attachments
- `Here.docx` - Full requirements specification
- `sharing_transactions_sample.csv` - Sample dataset (300 requests)
- `visualizations/` - Interactive dashboard + charts
- `ANALYSIS_QUICK_START.md` - Key insights from sample data
- `QUICKSTART_VISUALIZATIONS.md` - How to read the reports

---

**Questions?** Contact: Product Manager (DV) or check `README_ANALYSIS.md` for full documentation
