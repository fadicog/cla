# Digital Vault (DV) Impact Measurement Framework
**Version**: 1.0
**Date**: 2025-11-18
**Owner**: DV Product Team
**Purpose**: Measure and report impact of 2025 features to management (TDRA, DDA stakeholders)

---

## Executive Summary

This framework provides a structured approach to measuring, analyzing, and reporting the impact of Digital Vault features released in 2025. It identifies the highest-impact features based on strategic value, defines specific KPIs and data requirements, and provides actionable templates for requesting data from the ops team and reporting to management.

**Key Outcomes**:
- 7 highest-impact features identified (covering performance, UX, technical debt, and strategic initiatives)
- Specific KPIs and success criteria defined for each feature
- Ops team data request templates ready for immediate use
- Management reporting structure designed for compelling storytelling

---

## Table of Contents

1. [Highest Impact Features (Top 7)](#1-highest-impact-features-top-7)
2. [Impact Measurement Framework by Feature](#2-impact-measurement-framework-by-feature)
3. [Management Reporting Template](#3-management-reporting-template)
4. [Ops Team Data Request Template](#4-ops-team-data-request-template)
5. [Additional Research Recommendations](#5-additional-research-recommendations)
6. [Appendix: All 17 Features Summary](#6-appendix-all-17-features-summary)

---

## 1. Highest Impact Features (Top 7)

### Selection Criteria
1. **User Reach**: Does it affect all users or a critical segment?
2. **Frequency of Use**: Does it impact core, high-frequency flows?
3. **Performance Impact**: Does it reduce latency, API calls, or improve reliability?
4. **Strategic Value**: Does it align with North Star (reduce sharing failures) or unlock new capabilities?
5. **User Satisfaction Potential**: Does it address known pain points or enhance perceived quality?

---

### Top 7 Features (Ranked)

#### RANK 1: Removal of Loaders + Real-Time Updates (Q1)
**Combined Impact of Two Features**:
- Removal of loaders in all screens
- Implemented local search and real-time updates instead of calling API

**Why Top Priority**:
- **User Reach**: 100% of users (affects every screen visit)
- **Frequency**: Every time user navigates to any listing screen (Documents, Sharing Requests, etc.)
- **Performance Impact**: Drastic reduction in API calls + perceived performance improvement
- **Technical Innovation**: Firestore real-time cloud updates = seamless experience without loaders
- **Strategic Value**: Core infrastructure improvement benefiting all future features

**Impact Potential**: HIGH - Transforms core app experience from slow/loader-heavy to instant/seamless

---

#### RANK 2: Documents Section Revamp (Q3)
**Feature**: Revamp of Documents section with new landing screen, grid view, updated listing screens

**Why High Priority**:
- **User Reach**: 100% of users (primary app screen)
- **Frequency**: Entry point for all document interactions (request, view, upload, share)
- **Strategic Value**: Directly supports North Star (reduce sharing failures) by improving document discoverability
- **UX Enhancement**: Landing screen with latest 5 document types + unified search = faster document access
- **User Satisfaction**: Addresses known pain points (inconsistent empty states, missing grid view, equal weight for Issued vs Uploaded)

**Impact Potential**: HIGH - Improves primary user journey for document management

---

#### RANK 3: Copy-Paste Feature in Document Details (Q3)
**Feature**: Implemented copy-paste feature for all fields in issued document details screen

**Why High Priority**:
- **User Reach**: High (all users viewing document details)
- **Frequency**: Every time user needs to share document data (EID number, passport number, visa details) with SPs via phone/chat
- **User Satisfaction**: Addresses major pain point (manual retyping, transcription errors)
- **Strategic Value**: Reduces friction in document usage beyond formal Sharing flows
- **Accessibility**: Critical for users with visual/motor impairments

**Impact Potential**: MEDIUM-HIGH - Small feature, massive usability improvement

---

#### RANK 4: Sharing Request - Missing Document Auto Request (Q3)
**Feature**: When user lands on sharing request screen, if mandatory documents unavailable, popup allows requesting all at once

**Why High Priority**:
- **Strategic Value**: Directly supports North Star (reduce sharing failures by minimizing missing documents)
- **User Reach**: Medium (affects users missing mandatory docs during sharing)
- **Frequency**: Every failed sharing attempt due to missing docs
- **User Satisfaction**: Reduces friction (one-tap vs manual individual requests)
- **Measurable Impact**: Should increase "Successful Combos %" metric

**Impact Potential**: MEDIUM-HIGH - Directly reduces primary user pain point (failed shares)

---

#### RANK 5: PDF Viewer Implementation (Q4)
**Feature**: Migration to PDF viewer for issued document evidence screen; HTML fallback if issuer doesn't support PDF

**Why High Priority**:
- **User Reach**: High (all users viewing issued document evidence)
- **Frequency**: Every document view (core user action)
- **User Satisfaction**: Consistent, native PDF experience (fit-to-width, snap-to-page, pinch-to-zoom)
- **Technical Quality**: Unified viewing experience (previously inconsistent rendering)
- **Strategic Value**: Improved document trustworthiness perception (professional PDF vs HTML)

**Impact Potential**: MEDIUM-HIGH - Core user experience improvement

---

#### RANK 6: Document Update Detection (Q4)
**Feature**: Implementing document request whenever document hash mismatches (in Documents landing, view details, view document, QR verification)

**Why High Priority**:
- **Strategic Value**: Directly supports North Star (reduce sharing failures due to outdated documents)
- **User Reach**: Medium (affects users with expired/revoked documents)
- **Frequency**: Ongoing (every time user accesses outdated document)
- **User Satisfaction**: Proactive detection = user doesn't fail sharing flow
- **Technical Innovation**: Hash mismatch detection across 4 screens

**Impact Potential**: MEDIUM - Prevents sharing failures before they happen

---

#### RANK 7: Push Notification Tracking (Q1)
**Feature**: Tracking whether user enabled push notifications or not (updated to backend)

**Why High Priority**:
- **Strategic Value**: Enables optimization of notification strategy (foreground vs background)
- **Data Foundation**: Critical for diagnosing sharing failures due to missed notifications
- **Product Intelligence**: No prior visibility into notification opt-in rates
- **User Reach**: 100% of users
- **Frequency**: One-time tracking, ongoing monitoring

**Impact Potential**: MEDIUM - Foundation for future notification improvements

---

### Features Not Selected (Rationale)

**Q1: Migration of Requested Document Details (Mustache to JSON)**
- **Why Not Top 7**: Technical migration with limited direct user impact (faster loading is covered by loader removal)
- **Impact**: Performance improvement, but overshadowed by loader removal feature

**Q1-Q2: UI Enhancements (Error Messages, Ghost Loaders)**
- **Why Not Top 7**: Incremental improvements, harder to isolate impact
- **Impact**: Quality improvements, but not transformational

**Q2: MockSP App Development**
- **Why Not Top 7**: Internal tooling, no direct user impact
- **Impact**: Testing efficiency (QA/Engineering benefit)

**Q2: UX Lab Testing**
- **Why Not Top 7**: Research activity, not a launched feature
- **Impact**: Insights fed into later features (indirect)

**Q3: Bulk Signing Document Upload**
- **Why Not Top 7**: Lower frequency (uploaded docs have lower SP trust)
- **Impact**: Nice-to-have for power users, not core flow

**Q3: MockSP App Enhancements**
- **Why Not Top 7**: Internal tooling enhancement
- **Impact**: Testing capabilities (internal)

**Q3: Consent Box UI Improvement**
- **Why Not Top 7**: Incremental UX polish based on UX lab feedback
- **Impact**: Usability improvement, but not measurable in isolation

**Q3: Document Opening Failure Tracker API**
- **Why Not Top 7**: Monitoring/telemetry (no user-facing impact)
- **Impact**: Ops visibility (internal)

**Q3: Document Details Language Segregation**
- **Why Not Top 7**: Niche use case (bilingual users)
- **Impact**: Convenience for bilingual users, but copy-paste feature is higher priority

**Q4: Loader Tracker Introduction**
- **Why Not Top 7**: Telemetry/monitoring (no user-facing impact)
- **Impact**: Performance monitoring (internal)

**Q4: Email/Mobile Mismatch Message**
- **Why Not Top 7**: Edge case UX improvement
- **Impact**: Transparency for users with profile mismatches

---

## 2. Impact Measurement Framework by Feature

For each of the 7 highest-impact features, this section defines:
- Primary KPIs (quantitative metrics)
- Secondary KPIs (supporting metrics)
- Before/After Comparison (specific stats to request from ops)
- Data Sources (where metrics come from)
- Measurement Period (how long to measure)
- Success Criteria (what "good" looks like)

---

### FEATURE 1: Removal of Loaders + Real-Time Updates (Q1)

#### Primary KPIs
1. **API Call Reduction** (Backend)
   - Metric: Number of API calls per user session (Documents listing screens)
   - Target: 70-90% reduction vs. Q4 2024 baseline

2. **Perceived Screen Load Time** (App Telemetry)
   - Metric: Time from screen navigation to first content visible (Documents listing)
   - Target: <500ms (from ~2-3 seconds baseline)

3. **Screen Revisit Frequency** (App Telemetry)
   - Metric: Average number of times user navigates to Documents listing per session
   - Hypothesis: Faster loading = more browsing behavior
   - Target: +20% increase vs. baseline

#### Secondary KPIs
1. **App Crash Rate** (Firebase Crashlytics)
   - Metric: Crashes per user session (Firestore integration risk)
   - Target: No increase vs. baseline

2. **Data Freshness Accuracy** (Backend)
   - Metric: % of screen views showing stale data (>60 seconds old)
   - Target: <5%

3. **Network Error Rate** (App Telemetry)
   - Metric: Failed Firestore sync operations per user session
   - Target: <1%

#### Before/After Comparison: Ops Team Data Request

**BEFORE (Baseline): Q4 2024**
- Date Range: 2024-10-01 to 2024-12-31
- Filters: All users, Documents listing screens (Issued, Uploaded, All Documents)
- Metrics:
  1. Average API calls per user session (Documents screens only)
  2. P50/P90 screen load time (navigation to first content visible)
  3. Average Documents screen visits per user session
  4. Crash rate (crashes per 1000 sessions)

**AFTER (Post-Launch): Q1 2025**
- Date Range: 2025-01-15 to 2025-03-31 (2 weeks post-launch + 2.5 months)
- Filters: Same as baseline
- Metrics: Same as baseline

**Format**: CSV export with daily aggregates + weekly summaries

#### Data Sources
1. **Backend API Logs**: API call counts (by endpoint, user, date)
2. **App Telemetry Events**: Screen load times, navigation events (Firebase Analytics or custom)
3. **Firebase Crashlytics**: Crash rates, error logs
4. **Backend Firestore Logs**: Real-time sync operations, failures

#### Measurement Period
- **Baseline**: 3 months (Q4 2024)
- **Post-Launch**: 2 weeks stabilization + 2.5 months monitoring (Q1 2025)
- **Long-Term**: Monthly tracking (ongoing KPI)

#### Success Criteria
- **API Calls**: ≥70% reduction (ideal: 85%+)
- **Screen Load Time**: P90 <1 second (ideal: P50 <500ms)
- **Screen Revisits**: +15% increase (ideal: +25%+)
- **Crash Rate**: No increase (ideal: stable or improved)
- **Data Freshness**: ≥95% accuracy (ideal: 98%+)

#### Reporting Narrative
**Before**: "Users experienced 2-3 second load times every time they navigated to Documents screens, triggering repeated API calls and loader friction."

**After**: "Real-time Firestore updates eliminated loaders entirely, reducing API calls by [X]% and improving perceived performance to sub-second screen loads. Users now browse Documents [X]% more frequently per session, indicating increased engagement."

---

### FEATURE 2: Documents Section Revamp (Q3)

#### Primary KPIs
1. **Time to Find Document** (App Telemetry)
   - Metric: Time from landing screen arrival to document detail view
   - Target: -40% reduction vs. pre-revamp baseline

2. **Document Request Success Rate** (Backend)
   - Metric: % of document request flows completed (from Documents screen)
   - Target: +15% increase vs. baseline

3. **Search Usage Rate** (App Telemetry)
   - Metric: % of users using unified search (Documents landing screen)
   - Target: ≥30% of active users per week

#### Secondary KPIs
1. **Grid View Adoption** (App Telemetry)
   - Metric: % of users switching to grid view (vs. list view)
   - Target: ≥40% adoption within 4 weeks

2. **Landing Screen Engagement** (App Telemetry)
   - Metric: % of users tapping "latest 5 document types" cards
   - Target: ≥60% engagement rate

3. **Empty State Exposure** (App Telemetry)
   - Metric: % of users seeing new empty states (first-time users, no documents)
   - Metric: Click-through rate on "Request Document" CTA from empty state
   - Target: ≥50% CTR

#### Before/After Comparison: Ops Team Data Request

**BEFORE (Baseline): Q2 2025**
- Date Range: 2025-04-01 to 2025-06-30
- Filters: All users, Documents tab interactions
- Metrics:
  1. Time from Documents tab open to document detail view (P50/P90)
  2. Document request completion rate (% started vs. completed)
  3. Search usage rate (% of users using search per week)
  4. Tab switching frequency (Issued vs. Uploaded tab)

**AFTER (Post-Launch): Q3 2025**
- Date Range: 2025-07-15 to 2025-09-30 (2 weeks post-launch + 2.5 months)
- Filters: Same as baseline
- Metrics:
  1. Time from landing screen to document detail view (P50/P90)
  2. Document request completion rate (from landing screen)
  3. Unified search usage rate
  4. Grid view vs. list view usage (new metric)
  5. Landing screen card engagement (new metric)
  6. Empty state CTR (new metric)

**Format**: CSV export with weekly aggregates + user cohort analysis (new users vs. existing)

#### Data Sources
1. **App Telemetry Events**: Screen navigation, search usage, view mode selection, card taps (Firebase Analytics or custom)
2. **Backend API Logs**: Document request flows (start, abandon, complete)
3. **A/B Test Results** (if applicable): Grid view vs. list view engagement

#### Measurement Period
- **Baseline**: 3 months (Q2 2025)
- **Post-Launch**: 2 weeks stabilization + 2.5 months monitoring (Q3 2025)
- **Long-Term**: Quarterly tracking

#### Success Criteria
- **Time to Find Document**: ≥30% reduction (ideal: 40%+)
- **Document Request Success**: +10% increase (ideal: +15%+)
- **Search Usage**: ≥25% of users per week (ideal: 35%+)
- **Grid View Adoption**: ≥35% of users (ideal: 45%+)
- **Landing Screen Engagement**: ≥55% tap rate (ideal: 65%+)
- **Empty State CTR**: ≥45% (ideal: 55%+)

#### Reporting Narrative
**Before**: "Users navigated through separate Issued/Uploaded tabs with no unified discovery. Document finding required multiple taps and switching between tabs."

**After**: "New landing screen with 'latest 5 document types' + unified search reduced time to find documents by [X]%. Grid view adoption reached [X]% of users, and [X]% of first-time users tapped 'Request Document' from empty state."

---

### FEATURE 3: Copy-Paste Feature in Document Details (Q3)

#### Primary KPIs
1. **Copy Action Usage Rate** (App Telemetry)
   - Metric: % of document detail views with ≥1 copy action
   - Target: ≥40% of detail views

2. **Fields Copied per Session** (App Telemetry)
   - Metric: Average number of fields copied per user session (when ≥1 copy action)
   - Target: ≥2.5 fields per session

3. **Copy Action by Document Type** (App Telemetry)
   - Metric: Top 5 document types with highest copy usage (EID, Passport, Visa, etc.)
   - Insight: Understand which documents users share most frequently

#### Secondary KPIs
1. **User Satisfaction (Indirect)** (Support Tickets)
   - Metric: Support tickets related to "can't copy document data" or similar
   - Target: -80% reduction vs. pre-launch

2. **Accessibility Usage** (App Telemetry)
   - Metric: Copy action usage among users with accessibility features enabled (VoiceOver, TalkBack)
   - Target: ≥30% adoption

3. **Time Spent on Document Details** (App Telemetry)
   - Metric: Average session duration on document detail screen
   - Hypothesis: May decrease (faster copy = less time) or increase (more exploration)
   - Target: Track directionally (no hard target)

#### Before/After Comparison: Ops Team Data Request

**BEFORE (Baseline): Q2 2025**
- Date Range: 2025-04-01 to 2025-06-30
- Filters: All users, Document detail screen views
- Metrics:
  1. Total document detail views (by document type)
  2. Average session duration on document detail screen
  3. Support tickets mentioning "copy", "share", "retyping", "transcription" keywords

**AFTER (Post-Launch): Q3 2025**
- Date Range: 2025-07-15 to 2025-09-30 (2 weeks post-launch + 2.5 months)
- Filters: Same as baseline
- Metrics:
  1. Total document detail views
  2. Copy action events (total, by document type, by field)
  3. % of detail views with ≥1 copy action
  4. Average fields copied per session (when ≥1 copy)
  5. Average session duration on document detail screen
  6. Support tickets mentioning "copy", "share", "retyping"

**Format**: JSON export with event-level data + weekly aggregates

#### Data Sources
1. **App Telemetry Events**: Copy action events (field name, document type, timestamp) (Firebase Analytics or custom)
2. **Support Ticket System**: Keyword search results (pre/post launch)
3. **Accessibility Analytics**: Usage among users with accessibility features enabled

#### Measurement Period
- **Baseline**: 3 months (Q2 2025)
- **Post-Launch**: 2 weeks stabilization + 2.5 months monitoring (Q3 2025)
- **Long-Term**: Monthly tracking

#### Success Criteria
- **Copy Usage Rate**: ≥35% of detail views (ideal: 45%+)
- **Fields Copied**: ≥2.0 fields per session (ideal: 3.0+)
- **Support Tickets**: ≥50% reduction (ideal: 80%+)
- **Accessibility Usage**: ≥25% adoption (ideal: 35%+)

#### Reporting Narrative
**Before**: "Users had to manually retype document data (EID numbers, passport numbers, etc.) when sharing with SPs via phone/chat, leading to transcription errors and support requests."

**After**: "Copy-paste feature used in [X]% of document views, with users copying an average of [X] fields per session. Support tickets related to data retyping dropped by [X]%. Top copied documents: [EID, Passport, Visa]."

---

### FEATURE 4: Sharing Request - Missing Document Auto Request (Q3)

#### Primary KPIs
1. **Successful Combos %** (Backend)
   - Metric: % of sharing requests fully satisfied on first attempt (all requested docs available + active)
   - Target: +10% absolute increase vs. pre-launch baseline
   - **THIS IS THE NORTH STAR METRIC**

2. **Missing Document Auto-Request Usage Rate** (App Telemetry)
   - Metric: % of sharing requests triggering auto-request popup
   - Metric: % of users accepting auto-request (vs. dismissing)
   - Target: ≥70% acceptance rate

3. **Time to Resolve Missing Documents** (Backend)
   - Metric: Time from sharing request arrival to all mandatory docs becoming available
   - Target: -50% reduction vs. baseline (manual individual requests)

#### Secondary KPIs
1. **Sharing Request Abandonment Rate** (Backend)
   - Metric: % of sharing requests abandoned (user exits without approving/declining)
   - Target: -20% reduction vs. baseline

2. **Document Request Success Rate** (Backend)
   - Metric: % of auto-triggered document requests successfully fulfilled by issuers
   - Target: ≥85%

3. **User Returns to Complete Sharing** (Backend)
   - Metric: % of users returning to complete sharing after auto-requesting missing docs
   - Target: ≥60%

#### Before/After Comparison: Ops Team Data Request

**BEFORE (Baseline): Q2 2025**
- Date Range: 2025-04-01 to 2025-06-30
- Filters: All sharing requests, all SPs
- Metrics:
  1. Total sharing requests (by SP, by doc type)
  2. Successful Combos % (docs fully satisfied on first attempt)
  3. Missing document scenarios (which docs were missing, frequency)
  4. Sharing request abandonment rate (user exits without action)
  5. Average time from sharing request to approval (when successful)
  6. Average time from sharing request to abandonment (when failed)

**AFTER (Post-Launch): Q3 2025**
- Date Range: 2025-07-15 to 2025-09-30 (2 weeks post-launch + 2.5 months)
- Filters: Same as baseline
- Metrics:
  1. Total sharing requests
  2. Successful Combos %
  3. Auto-request popup trigger rate (% of sharing requests)
  4. Auto-request acceptance rate (% of popups accepted)
  5. Auto-requested documents (which docs, frequency)
  6. Auto-request fulfillment success rate (% fulfilled by issuers)
  7. Sharing request abandonment rate
  8. Time from sharing request to approval (with auto-request)
  9. User return rate to complete sharing (after auto-request)

**Format**: CSV export with daily aggregates + cohort analysis (by SP, by doc type, by user segment)

#### Data Sources
1. **Backend API Logs**: Sharing request events (create, view, approve, decline, abandon, auto-request trigger)
2. **App Telemetry Events**: Auto-request popup (shown, accepted, dismissed)
3. **Issuer API Logs**: Document request fulfillment (success, failure, pending)

#### Measurement Period
- **Baseline**: 3 months (Q2 2025)
- **Post-Launch**: 2 weeks stabilization + 2.5 months monitoring (Q3 2025)
- **Long-Term**: Ongoing monthly tracking (North Star metric)

#### Success Criteria
- **Successful Combos %**: +8% absolute increase (ideal: +12%+)
- **Auto-Request Acceptance**: ≥65% (ideal: 75%+)
- **Time to Resolve**: ≥40% reduction (ideal: 60%+)
- **Abandonment Rate**: ≥15% reduction (ideal: 25%+)
- **Fulfillment Success**: ≥80% (ideal: 90%+)
- **User Returns**: ≥55% (ideal: 65%+)

#### Reporting Narrative
**Before**: "When users received sharing requests with missing mandatory documents, they had to manually navigate to Documents → Request Document → select each missing document individually. This led to high abandonment rates and low Successful Combos %."

**After**: "Auto-request popup triggered for [X]% of sharing requests with missing docs. [X]% of users accepted auto-request, reducing time to resolve missing docs by [X]%. Successful Combos % increased from [X]% to [X]% (+[X] absolute points)."

---

### FEATURE 5: PDF Viewer Implementation (Q4)

#### Primary KPIs
1. **PDF Viewer Adoption Rate** (App Telemetry)
   - Metric: % of document views using PDF viewer (vs. HTML fallback)
   - Target: ≥85% (depends on issuer support)

2. **Document View Duration** (App Telemetry)
   - Metric: Average session duration on document evidence screen
   - Hypothesis: Better viewer = longer engagement (more reading, less frustration)
   - Target: +15% increase vs. baseline

3. **PDF Viewer Error Rate** (App Telemetry)
   - Metric: % of PDF viewer loads failing (rendering errors, crashes)
   - Target: <2%

#### Secondary KPIs
1. **User Actions in PDF Viewer** (App Telemetry)
   - Metric: Pinch-to-zoom usage (% of viewers)
   - Metric: Page navigation (swipes, pagination)
   - Target: ≥60% of users interacting with viewer (zoom or navigate)

2. **Issuer Support Coverage** (Backend)
   - Metric: % of issued documents with PDF support (by issuer)
   - Insight: Identify issuers needing migration to PDF

3. **User Satisfaction (Indirect)** (Support Tickets)
   - Metric: Support tickets mentioning "can't read document", "zoom", "blurry" keywords
   - Target: -50% reduction vs. baseline

#### Before/After Comparison: Ops Team Data Request

**BEFORE (Baseline): Q3 2025**
- Date Range: 2025-07-01 to 2025-09-30
- Filters: All users, issued document evidence screen views
- Metrics:
  1. Total document evidence views (by document type, by issuer)
  2. Average session duration on evidence screen
  3. Rendering errors or crashes (if tracked)
  4. Support tickets mentioning "view document", "zoom", "blurry", "can't read"

**AFTER (Post-Launch): Q4 2025**
- Date Range: 2025-10-15 to 2025-12-31 (2 weeks post-launch + 2.5 months)
- Filters: Same as baseline
- Metrics:
  1. Total document evidence views
  2. PDF viewer usage rate (% of views)
  3. HTML fallback usage rate (% of views)
  4. Average session duration on PDF viewer screen
  5. PDF viewer error rate (rendering failures, crashes)
  6. User interactions (zoom events, page navigation events)
  7. Support tickets mentioning document viewing issues

**Format**: CSV export with weekly aggregates + issuer-level breakdown (PDF support coverage)

#### Data Sources
1. **App Telemetry Events**: PDF viewer events (load, render, zoom, navigate, error) (Firebase Analytics or custom)
2. **Backend Logs**: Document type and format (PDF vs. HTML) by issuer
3. **Firebase Crashlytics**: PDF viewer crashes
4. **Support Ticket System**: Keyword search results

#### Measurement Period
- **Baseline**: 3 months (Q3 2025)
- **Post-Launch**: 2 weeks stabilization + 2.5 months monitoring (Q4 2025)
- **Long-Term**: Quarterly tracking

#### Success Criteria
- **PDF Adoption**: ≥80% of views (ideal: 90%+)
- **View Duration**: +10% increase (ideal: +20%+)
- **Error Rate**: <3% (ideal: <1%)
- **User Interactions**: ≥55% (ideal: 65%+)
- **Support Tickets**: ≥40% reduction (ideal: 60%+)

#### Reporting Narrative
**Before**: "Document evidence screens rendered inconsistently (HTML format), with users unable to zoom, navigate pages naturally, or read documents comfortably on mobile screens."

**After**: "Native PDF viewer now handles [X]% of document views, with [X]% of users actively zooming or navigating pages. Average viewing time increased by [X]%, and support tickets related to document readability dropped by [X]%."

---

### FEATURE 6: Document Update Detection (Q4)

#### Primary KPIs
1. **Hash Mismatch Detection Rate** (Backend)
   - Metric: % of document views triggering hash mismatch detection
   - Insight: Understand scale of outdated document problem

2. **Update Request Acceptance Rate** (App Telemetry)
   - Metric: % of users accepting "Request Updated Version" prompt (vs. dismissing)
   - Target: ≥60%

3. **Proactive Update Success Rate** (Backend)
   - Metric: % of hash mismatch scenarios resolved (updated document obtained) before next sharing request
   - Target: ≥70%

#### Secondary KPIs
1. **Sharing Failure Prevention** (Backend)
   - Metric: Estimated % of sharing failures prevented (hash mismatch detected pre-sharing)
   - Method: Compare hash mismatch detections at QR verification screen vs. during sharing
   - Target: ≥50% detected before sharing attempt

2. **Update Notification Response Time** (Backend)
   - Metric: Time from hash mismatch detection to user requesting updated version
   - Target: <5 minutes (median)

3. **User Satisfaction (Indirect)** (Support Tickets)
   - Metric: Support tickets mentioning "document expired", "sharing failed", "outdated document"
   - Target: -40% reduction vs. pre-launch

#### Before/After Comparison: Ops Team Data Request

**BEFORE (Baseline): Q3 2025**
- Date Range: 2025-07-01 to 2025-09-30
- Filters: All users, sharing requests, document views
- Metrics:
  1. Sharing failures due to "document expired/revoked/hash mismatch" (by doc type)
  2. Total document views (by screen: landing, details, evidence, QR verification)
  3. Support tickets mentioning "expired", "outdated", "sharing failed"

**AFTER (Post-Launch): Q4 2025**
- Date Range: 2025-10-15 to 2025-12-31 (2 weeks post-launch + 2.5 months)
- Filters: Same as baseline
- Metrics:
  1. Hash mismatch detections (total, by screen, by doc type)
  2. Update request prompt events (shown, accepted, dismissed)
  3. Proactive updates completed (updated doc obtained before sharing)
  4. Sharing failures due to "document expired/revoked/hash mismatch" (should decrease)
  5. Time from hash mismatch detection to update request
  6. Support tickets mentioning document expiry/outdated issues

**Format**: CSV export with weekly aggregates + screen-level breakdown (Documents landing, view details, view document, QR verification)

#### Data Sources
1. **Backend API Logs**: Hash validation events, update request triggers, document updates
2. **App Telemetry Events**: Update prompt events (shown, accepted, dismissed)
3. **Issuer API Logs**: Update request fulfillment (success, failure)
4. **Support Ticket System**: Keyword search results

#### Measurement Period
- **Baseline**: 3 months (Q3 2025)
- **Post-Launch**: 2 weeks stabilization + 2.5 months monitoring (Q4 2025)
- **Long-Term**: Quarterly tracking

#### Success Criteria
- **Update Request Acceptance**: ≥55% (ideal: 65%+)
- **Proactive Update Success**: ≥65% (ideal: 75%+)
- **Sharing Failure Prevention**: ≥45% detected pre-sharing (ideal: 55%+)
- **Response Time**: <10 minutes median (ideal: <5 minutes)
- **Support Tickets**: ≥30% reduction (ideal: 50%+)

#### Reporting Narrative
**Before**: "Users only discovered document expiry/hash mismatch during sharing flows, causing failed transactions and SP dissatisfaction. No proactive detection mechanism existed."

**After**: "Hash mismatch detection now runs across 4 screens (Documents landing, view details, view document, QR verification), identifying [X] outdated documents. [X]% of users accepted update prompts, and [X]% of potential sharing failures were prevented proactively."

---

### FEATURE 7: Push Notification Tracking (Q1)

#### Primary KPIs
1. **Notification Opt-In Rate** (Backend)
   - Metric: % of users with push notifications enabled
   - Baseline: Unknown (no prior tracking)
   - Target: Establish baseline, aim for ≥70% opt-in

2. **Opt-In Rate by Platform** (Backend)
   - Metric: iOS vs. Android opt-in rate
   - Insight: Platform differences inform strategy

3. **Opt-In Rate by User Tenure** (Backend)
   - Metric: New users (first 7 days) vs. existing users opt-in rate
   - Insight: Onboarding effectiveness

#### Secondary KPIs
1. **Notification Delivery Success Rate** (Firebase)
   - Metric: % of notifications successfully delivered (opt-in users)
   - Target: ≥95%

2. **Notification Open Rate** (Firebase)
   - Metric: % of delivered notifications opened
   - Baseline: Unknown
   - Target: Establish baseline, aim for ≥40% for actionable notifications

3. **Foreground vs. Background Notification Reception** (Firebase)
   - Metric: % of notifications received while app foreground vs. background
   - Insight: Inform in-app cue strategy

#### Before/After Comparison: Ops Team Data Request

**BEFORE (Baseline): Q4 2024**
- No data available (tracking not implemented)

**AFTER (Post-Launch): Q1 2025**
- Date Range: 2025-01-15 to 2025-03-31 (2 weeks post-launch + 2.5 months)
- Filters: All users
- Metrics:
  1. Total users (active, by platform)
  2. Users with push notifications enabled (count, %)
  3. Users with push notifications disabled (count, %)
  4. Opt-in rate by platform (iOS vs. Android)
  5. Opt-in rate by user tenure (new vs. existing)
  6. Notification delivery success rate (Firebase)
  7. Notification open rate (Firebase)
  8. Foreground vs. background reception (Firebase)

**Format**: CSV export with weekly aggregates + cohort analysis (platform, tenure)

#### Data Sources
1. **Backend User Database**: Notification opt-in status (updated by app)
2. **Firebase Cloud Messaging (FCM)**: Delivery success, open rates, foreground/background reception
3. **App Telemetry Events**: Opt-in/opt-out actions (if user changes setting)

#### Measurement Period
- **Baseline**: N/A (no prior tracking)
- **Post-Launch**: 2 weeks stabilization + 2.5 months monitoring (Q1 2025)
- **Long-Term**: Ongoing monthly tracking (foundational KPI)

#### Success Criteria
- **Opt-In Rate**: ≥65% (ideal: 75%+) — benchmark against industry standards
- **Platform Parity**: <10% difference between iOS and Android
- **New User Opt-In**: ≥70% within first 7 days (ideal: 80%+)
- **Delivery Success**: ≥93% (ideal: 97%+)
- **Open Rate (Actionable)**: ≥35% (ideal: 45%+)

#### Reporting Narrative
**Before**: "Product team had no visibility into push notification opt-in rates. We couldn't diagnose sharing failures due to missed notifications or optimize notification strategy."

**After**: "Tracking now shows [X]% of users have notifications enabled ([X]% iOS, [X]% Android). Notification open rate for actionable notifications (sharing requests) is [X]%. This data enables targeted optimization of notification strategy and in-app cue design."

---

## 3. Management Reporting Template

### 3.1 Executive Summary Format (1-Page)

**Template Structure**:

```
DIGITAL VAULT (DV) — FEATURE IMPACT REPORT
Q[X] 2025 Released Features

────────────────────────────────────────────────────────────────────

EXECUTIVE SUMMARY

In Q[X] 2025, we released [N] features focused on [primary goal: performance, UX, strategic capability]. This report quantifies the impact of the top [N] highest-value features.

KEY OUTCOMES:
✓ Performance: [X]% reduction in API calls, [X]% improvement in screen load times
✓ User Experience: [X]% increase in document discoverability, [X]% adoption of new features
✓ North Star Metric: Successful Combos % increased from [X]% → [X]% (+[X] points)
✓ User Satisfaction: Support tickets related to [pain point] decreased by [X]%

────────────────────────────────────────────────────────────────────

TOP 3 IMPACT HIGHLIGHTS

1. [FEATURE NAME] — [Impact Category]
   Before: [Pain point description in 1 sentence]
   After: [Outcome description in 1 sentence]
   Key Metric: [Metric] improved by [X]% (from [baseline] to [current])

2. [FEATURE NAME] — [Impact Category]
   Before: [Pain point description in 1 sentence]
   After: [Outcome description in 1 sentence]
   Key Metric: [Metric] improved by [X]% (from [baseline] to [current])

3. [FEATURE NAME] — [Impact Category]
   Before: [Pain point description in 1 sentence]
   After: [Outcome description in 1 sentence]
   Key Metric: [Metric] improved by [X]% (from [baseline] to [current])

────────────────────────────────────────────────────────────────────

STRATEGIC ALIGNMENT

Our North Star Goal: **Reduce failure cases in document sharing flows**

Q[X] features contributed to this goal by:
→ [Mechanism 1]: [Feature] reduced missing document scenarios by [X]%
→ [Mechanism 2]: [Feature] improved document discoverability by [X]%
→ [Mechanism 3]: [Feature] prevented [X]% of sharing failures proactively

Result: Successful Combos % (first-attempt sharing success) improved by [X] absolute points.

────────────────────────────────────────────────────────────────────

NEXT STEPS

1. [Action Item 1]: Based on [Feature] adoption data, we will [next optimization]
2. [Action Item 2]: [Feature] uncovered [insight], informing [future initiative]
3. [Action Item 3]: Continue monitoring [long-term KPI] to validate sustained impact

────────────────────────────────────────────────────────────────────

Prepared by: [PM Name]
Date: [YYYY-MM-DD]
Full report available: [link to detailed deck]
```

---

### 3.2 Detailed Feature Impact Report Template

**Template Structure** (per feature, 1-2 slides/pages):

```
FEATURE: [Feature Name]
Release Quarter: Q[X] 2025
Impact Category: [Performance / UX / Strategic / Technical Debt]

────────────────────────────────────────────────────────────────────

PROBLEM STATEMENT

Before this feature:
→ [Pain point 1]
→ [Pain point 2]
→ [Pain point 3]

Impact on users: [User frustration, failed transactions, friction]
Impact on business: [Low conversion, support burden, SP dissatisfaction]

────────────────────────────────────────────────────────────────────

SOLUTION

What we built:
→ [Capability 1]
→ [Capability 2]
→ [Capability 3]

Design rationale: [Why this approach, DDA alignment, best practices]

────────────────────────────────────────────────────────────────────

QUANTITATIVE IMPACT

PRIMARY KPIS:

1. [KPI Name]
   Baseline (Pre-Launch): [Value]
   Current (Post-Launch): [Value]
   Change: [+/-X%] or [+/-X points]
   Status: [✓ Target Met] / [⚠ In Progress] / [✗ Below Target]

2. [KPI Name]
   Baseline: [Value]
   Current: [Value]
   Change: [+/-X%]
   Status: [✓/⚠/✗]

3. [KPI Name]
   Baseline: [Value]
   Current: [Value]
   Change: [+/-X%]
   Status: [✓/⚠/✗]

SECONDARY KPIS:

[Same format as primary]

────────────────────────────────────────────────────────────────────

QUALITATIVE IMPACT

User Feedback:
→ [Quote from user interview / UX lab / support ticket]
→ [Quote from user interview / UX lab / support ticket]

Support Ticket Analysis:
→ Tickets related to [pain point] decreased by [X]% (from [N] to [M] per week)
→ Top resolved issues: [Issue 1], [Issue 2], [Issue 3]

SP Feedback (if applicable):
→ [SP name] reported [positive outcome]
→ [SP name] requested [related enhancement]

────────────────────────────────────────────────────────────────────

ADOPTION & ENGAGEMENT

Feature Usage:
→ [X]% of users used [feature capability] in first [N] weeks
→ [X]% of [target user segment] adopted [feature] within [timeframe]
→ [Frequency metric]: Users interact with [feature] [X] times per [period]

User Segments:
→ New users: [adoption rate, usage pattern]
→ Existing users: [adoption rate, usage pattern]
→ Platform differences: iOS [X]%, Android [X]%

────────────────────────────────────────────────────────────────────

VISUALIZATIONS

[Include 1-3 charts]:
→ Before/After comparison (line chart or bar chart)
→ Adoption curve over time (line chart)
→ Breakdown by segment (pie chart or stacked bar)

────────────────────────────────────────────────────────────────────

LESSONS LEARNED

What went well:
→ [Success factor 1]
→ [Success factor 2]

Challenges:
→ [Challenge 1]: [How we addressed it]
→ [Challenge 2]: [How we addressed it]

Unexpected outcomes:
→ [Insight 1]: [Implication for future features]
→ [Insight 2]: [Implication for future features]

────────────────────────────────────────────────────────────────────

NEXT STEPS

Short-term (1-3 months):
→ [Optimization 1]: Based on [data/feedback]
→ [Optimization 2]: Based on [data/feedback]

Long-term (3-6 months):
→ [Enhancement 1]: Expand [feature] to [new capability]
→ [Enhancement 2]: Integrate [feature] with [other feature]

Monitoring:
→ Continue tracking [KPI] monthly to ensure sustained impact
→ A/B test [variation] to optimize [metric]

────────────────────────────────────────────────────────────────────

Prepared by: [PM Name]
Date: [YYYY-MM-DD]
Review stakeholders: [TDRA, DDA, Engineering]
```

---

### 3.3 Visualization Recommendations

**For Each Feature, Include 1-3 Charts**:

#### Chart Type 1: Before/After Comparison (Bar Chart)
- **Purpose**: Show clear improvement in primary KPI
- **Format**: Side-by-side bars (Before | After)
- **Example**:
  ```
  API Calls per User Session (Documents Screens)

  Before (Q4 2024):  ████████████████████ 8.2 calls
  After (Q1 2025):   ███ 1.1 calls

  Improvement: -87%
  ```

#### Chart Type 2: Adoption Curve (Line Chart)
- **Purpose**: Show feature adoption over time (post-launch)
- **Format**: Line chart with weeks/months on X-axis, adoption % on Y-axis
- **Example**:
  ```
  Grid View Adoption (% of Users)

  Week 1:   12%
  Week 2:   24%
  Week 4:   38%
  Week 8:   45%
  Week 12:  47%

  Target: 40% ✓ Achieved Week 4
  ```

#### Chart Type 3: Segmentation Breakdown (Pie Chart or Stacked Bar)
- **Purpose**: Show adoption/usage by user segment
- **Format**: Pie chart or stacked bar chart
- **Example**:
  ```
  Copy-Paste Feature Usage by Document Type

  EID:             35% ███████████████████████████
  Passport:        28% ██████████████████████
  Visa:            18% ██████████████
  Other:           19% ███████████████
  ```

#### Chart Type 4: Funnel Chart (for Multi-Step Features)
- **Purpose**: Show drop-off at each step
- **Example**:
  ```
  Sharing Request with Missing Docs (Auto-Request Flow)

  Sharing request received:        1000 users ███████████████████████
  Auto-request popup shown:         650 users ███████████████
  User accepted auto-request:       455 users ██████████
  Document request fulfilled:       387 users ████████
  User returned to complete share:  232 users █████

  Conversion: 23.2%
  ```

---

### 3.4 Storytelling Approach

**Framework: "Problem → Solution → Impact → Next"**

#### Stage 1: PROBLEM (Set Context)
- **Purpose**: Make stakeholders feel the pain
- **Format**:
  - "Before this feature, users experienced [pain point]..."
  - "This led to [negative outcome]: [quantified impact]..."
  - "Example: [user quote or support ticket]"

**Example**:
> "Before the Documents Section Revamp, users navigated through separate Issued/Uploaded tabs with no unified discovery. Finding a specific document required multiple taps, tab switching, and scrolling. Support tickets related to 'can't find my document' averaged 120 per month."

#### Stage 2: SOLUTION (Show What We Built)
- **Purpose**: Explain the feature clearly (even to non-technical stakeholders)
- **Format**:
  - "We designed [feature] to [goal]..."
  - "Key capabilities: [1], [2], [3]..."
  - "Design aligned with DDA guidelines and global best practices..."

**Example**:
> "We designed a new Documents landing screen with two primary CTAs (Request Document / Upload Document) and a 'latest 5 document types' section for quick access. We added grid view (in addition to list view) and unified search across all documents. Design approval from DDA completed in Q2 2025."

#### Stage 3: IMPACT (Quantify Results)
- **Purpose**: Prove value with data
- **Format**:
  - "After launch, we measured [KPI]: [Before] → [After] ([+/-X%])..."
  - "This means [business outcome]: [user benefit, SP benefit, ops benefit]..."
  - "User feedback: [quote]..."

**Example**:
> "After launch, time to find a document decreased by 42% (from 18 seconds to 10 seconds median). Grid view adoption reached 45% of users within 8 weeks. 68% of first-time users tapped 'Request Document' from the empty state. User feedback: 'Much easier to find my documents now!' Support tickets related to document discovery dropped by 55%."

#### Stage 4: NEXT (Show Forward Momentum)
- **Purpose**: Demonstrate ongoing optimization and learning
- **Format**:
  - "Based on this data, our next steps are [action 1], [action 2]..."
  - "We'll continue monitoring [KPI] to ensure sustained impact..."
  - "This feature unlocks future opportunities: [related initiative]..."

**Example**:
> "Based on grid view adoption data, we'll explore adding document sorting/filtering options (by date, by issuer). We'll A/B test the 'latest 5 document types' section (5 vs. 7 vs. 10 recent items) to optimize engagement. This revamp also sets the foundation for the Auto-Add Documents feature (Q2 2025), which will proactively populate the landing screen."

---

### 3.5 Reporting Cadence

#### Weekly (Internal Team)
- **Format**: Slack/email update (3-5 bullet points)
- **Content**:
  - Key metric movement (week-over-week)
  - Anomalies or issues (e.g., sudden drop in adoption)
  - User feedback highlights
- **Audience**: Engineering, QA, Ops

#### Monthly (Stakeholder Review)
- **Format**: Slide deck (5-10 slides)
- **Content**:
  - Executive summary (1 slide)
  - Top 3 feature impacts (1 slide each)
  - North Star metric trend (Successful Combos %)
  - Open questions / risks
- **Audience**: TDRA, DDA, Engineering Leadership

#### Quarterly (Strategic Review)
- **Format**: Comprehensive report (20-30 slides + appendix)
- **Content**:
  - All released features (detailed impact per feature)
  - Strategic alignment (North Star progress)
  - User satisfaction trends (support tickets, NPS)
  - SP ecosystem health (integration rates, feedback)
  - Roadmap implications (lessons learned → future priorities)
- **Audience**: TDRA Executive, DDA Executive, Product Leadership

---

## 4. Ops Team Data Request Template

### 4.1 General Request Format

**Subject**: [Feature Name] Impact Measurement — Data Request

**Priority**: [High / Medium / Low]

**Requestor**: [PM Name]

**Date**: [YYYY-MM-DD]

**Purpose**: Measure the impact of [Feature Name] released in Q[X] 2025 to quantify [primary goal: performance improvement, UX enhancement, strategic capability].

**Deadline**: [YYYY-MM-DD] (need [N] days for analysis and reporting)

---

#### DATA REQUEST SUMMARY

**Feature**: [Feature Name]

**Release Date**: [YYYY-MM-DD]

**Baseline Period**: [Start Date] to [End Date] (pre-launch)

**Post-Launch Period**: [Start Date] to [End Date] (post-launch)

**Filters**: [All users / Specific segment / Specific SP / Specific document type]

**Output Format**: [CSV / JSON / Excel] with [daily / weekly] aggregates

---

#### METRICS REQUESTED

| # | Metric Name | Data Source | Calculation | Filters | Granularity |
|---|-------------|-------------|-------------|---------|-------------|
| 1 | [Metric] | [Backend API Logs / Firebase / App Telemetry] | [Formula or query description] | [User segment, date range, platform] | [Daily / Weekly / Event-level] |
| 2 | [Metric] | [Data source] | [Formula] | [Filters] | [Granularity] |
| 3 | [Metric] | [Data source] | [Formula] | [Filters] | [Granularity] |

---

#### DETAILED METRIC SPECIFICATIONS

**METRIC 1: [Metric Name]**

- **Definition**: [Clear definition in plain English]
- **Data Source**: [System/table/log file]
- **Query Logic**:
  ```
  [Pseudo-query or description]
  Example: "Count of API calls to /documents/list endpoint per user session,
  where session is defined as continuous app usage with <5 min gaps"
  ```
- **Filters**:
  - Date Range: [YYYY-MM-DD to YYYY-MM-DD]
  - User Segment: [All users / iOS only / Android only]
  - Screen: [Specific screen if applicable]
  - Platform: [iOS / Android / Both]
- **Granularity**: [Daily aggregates / Weekly aggregates / Event-level data]
- **Output Columns**: [user_id, date, api_call_count, session_count, avg_calls_per_session]

**METRIC 2: [Metric Name]**

[Same format as Metric 1]

**METRIC 3: [Metric Name]**

[Same format as Metric 1]

---

#### COHORT ANALYSIS (if applicable)

**Cohort Definition**: [New users (first 7 days) vs. Existing users (8+ days)]

**Cohort Comparison**:
- Metric 1: Compare [metric] between cohorts
- Metric 2: Compare [metric] between cohorts
- Insight Goal: Understand if feature adoption differs by user tenure

---

#### SEGMENT BREAKDOWN (if applicable)

**Segment Dimensions**:
- Platform: iOS vs. Android
- Document Type: [EID, Passport, Visa, Other]
- SP: [SP1, SP2, SP3, Other]

**Segment Comparison**:
- Metric 1: Break down by segment
- Insight Goal: Identify high-performing segments and optimization opportunities

---

#### CONTEXT & BACKGROUND

**Why This Data?**
[Explain the "why" to help ops team prioritize and understand the request]

Example: "This feature was designed to reduce API call volume and improve perceived performance. We need API call counts to validate the performance improvement and screen load times to measure user experience impact."

**How We'll Use It**:
[Explain intended use]

Example: "This data will be used to: (1) Report impact to TDRA/DDA stakeholders, (2) Validate ROI for engineering investment, (3) Inform optimization priorities for Q[X] 2025."

---

#### PRIORITY & URGENCY

**Priority Ranking**: [High / Medium / Low]

**Justification**:
- High: [Stakeholder presentation scheduled, blockers to roadmap decisions]
- Medium: [Routine impact measurement, monthly reporting]
- Low: [Exploratory analysis, nice-to-have insights]

**Deadline**: [YYYY-MM-DD]

**Contact for Questions**: [PM Name, Email, Slack]

---

### 4.2 Feature-Specific Data Request Examples

Below are complete, ready-to-use data request templates for the 7 highest-impact features.

---

#### EXAMPLE 1: Loader Removal + Real-Time Updates (Q1)

**Subject**: Loader Removal & Real-Time Updates — Impact Measurement Data Request

**Priority**: High

**Requestor**: DV Product Team

**Date**: 2025-04-01

**Purpose**: Quantify performance improvement (API call reduction, screen load time) and user engagement (screen revisit frequency) for Q1 2025 loader removal feature.

**Deadline**: 2025-04-15

---

**DATA REQUEST SUMMARY**

**Feature**: Removal of Loaders + Real-Time Firestore Updates

**Release Date**: 2025-01-15

**Baseline Period**: 2024-10-01 to 2024-12-31 (Q4 2024, pre-launch)

**Post-Launch Period**: 2025-01-15 to 2025-03-31 (Q1 2025, post-launch)

**Filters**: All users, Documents listing screens (Issued, Uploaded, All Documents)

**Output Format**: CSV with daily aggregates + weekly summaries

---

**METRICS REQUESTED**

| # | Metric Name | Data Source | Calculation | Filters | Granularity |
|---|-------------|-------------|-------------|---------|-------------|
| 1 | API Calls per User Session | Backend API Logs | Count of API calls to /documents/list per session | Documents screens, all users | Daily aggregates |
| 2 | Screen Load Time (P50, P90) | App Telemetry | Time from screen navigation event to first content visible event | Documents screens, all users | Daily P50/P90 |
| 3 | Screen Revisits per Session | App Telemetry | Count of Documents screen visits per user session | Documents screens, all users | Daily aggregates |
| 4 | App Crash Rate | Firebase Crashlytics | Crashes per 1000 sessions | All screens, all users | Daily rate |
| 5 | Firestore Sync Errors | Backend Firestore Logs | Failed real-time sync operations per session | Documents screens, all users | Daily error count |

---

**DETAILED METRIC SPECIFICATIONS**

**METRIC 1: API Calls per User Session (Documents Screens)**

- **Definition**: Average number of API calls to Documents listing endpoints per user session, where session is defined as continuous app usage with <5 min gaps.
- **Data Source**: Backend API logs (endpoint: /documents/list, /documents/issued, /documents/uploaded)
- **Query Logic**:
  ```
  For each user session:
    Count API calls to Documents listing endpoints
    Calculate: total_api_calls / total_sessions
  Aggregate by day
  ```
- **Filters**:
  - Date Range (Baseline): 2024-10-01 to 2024-12-31
  - Date Range (Post-Launch): 2025-01-15 to 2025-03-31
  - User Segment: All users
  - Endpoints: /documents/list, /documents/issued, /documents/uploaded
  - Platform: iOS + Android
- **Granularity**: Daily aggregates (with weekly summaries)
- **Output Columns**: date, total_sessions, total_api_calls, avg_calls_per_session, platform (iOS/Android)

**METRIC 2: Screen Load Time (P50, P90)**

- **Definition**: Time from screen navigation event (user taps Documents tab) to first content visible event (first document card rendered), measured at 50th and 90th percentile.
- **Data Source**: App telemetry (Firebase Analytics or custom telemetry)
- **Query Logic**:
  ```
  For each Documents screen load event:
    Calculate: first_content_visible_timestamp - screen_navigation_timestamp
    Aggregate P50 and P90 by day
  ```
- **Filters**:
  - Date Range (Baseline): 2024-10-01 to 2024-12-31
  - Date Range (Post-Launch): 2025-01-15 to 2025-03-31
  - Screen: Documents (all tabs: Issued, Uploaded, All)
  - Platform: iOS + Android
- **Granularity**: Daily P50/P90 (with weekly summaries)
- **Output Columns**: date, p50_load_time_ms, p90_load_time_ms, total_load_events, platform

**METRIC 3: Screen Revisits per Session**

- **Definition**: Average number of times a user navigates to Documents screens within a single session.
- **Data Source**: App telemetry (screen navigation events)
- **Query Logic**:
  ```
  For each user session:
    Count Documents screen navigation events
    Calculate: total_documents_visits / total_sessions
  Aggregate by day
  ```
- **Filters**:
  - Date Range (Baseline): 2024-10-01 to 2024-12-31
  - Date Range (Post-Launch): 2025-01-15 to 2025-03-31
  - Screen: Documents (all tabs)
  - Platform: iOS + Android
- **Granularity**: Daily aggregates (with weekly summaries)
- **Output Columns**: date, total_sessions, total_documents_visits, avg_revisits_per_session, platform

**METRIC 4: App Crash Rate**

- **Definition**: Number of app crashes per 1000 user sessions.
- **Data Source**: Firebase Crashlytics
- **Query Logic**:
  ```
  Crashes per day / Total sessions per day * 1000
  ```
- **Filters**:
  - Date Range (Baseline): 2024-10-01 to 2024-12-31
  - Date Range (Post-Launch): 2025-01-15 to 2025-03-31
  - Platform: iOS + Android
- **Granularity**: Daily crash rate (with weekly summaries)
- **Output Columns**: date, total_crashes, total_sessions, crash_rate_per_1000, platform

**METRIC 5: Firestore Sync Errors**

- **Definition**: Count of failed real-time Firestore sync operations per user session (Documents screens only).
- **Data Source**: Backend Firestore logs (error events)
- **Query Logic**:
  ```
  For each user session:
    Count Firestore sync error events for Documents screens
    Calculate: total_errors / total_sessions
  Aggregate by day
  ```
- **Filters**:
  - Date Range (Baseline): N/A (feature not active)
  - Date Range (Post-Launch): 2025-01-15 to 2025-03-31
  - Screen: Documents (all tabs)
  - Platform: iOS + Android
- **Granularity**: Daily error count (with weekly summaries)
- **Output Columns**: date, total_sessions, total_sync_errors, avg_errors_per_session, platform

---

**CONTEXT & BACKGROUND**

**Why This Data?**
This feature represents the largest infrastructure improvement in Q1 2025, replacing synchronous API calls with real-time Firestore updates. We need to validate two hypotheses: (1) API call volume decreased drastically (70-90% reduction), and (2) perceived performance improved significantly (sub-second load times).

**How We'll Use It**:
- Report impact to TDRA/DDA stakeholders (quarterly review)
- Validate ROI for Firestore migration (engineering investment justification)
- Inform future optimization priorities (e.g., extend real-time updates to other screens)

**Priority**: High — Foundational feature for 2025 roadmap, critical for stakeholder reporting.

**Contact**: [PM Name], [Email], [Slack: @pm-dv]

---

#### EXAMPLE 2: Documents Section Revamp (Q3)

**Subject**: Documents Section Revamp — Impact Measurement Data Request

**Priority**: High

**Requestor**: DV Product Team

**Date**: 2025-09-01

**Purpose**: Measure UX improvement (time to find document, document request success rate, search usage) for Q3 2025 Documents revamp feature.

**Deadline**: 2025-09-15

---

**DATA REQUEST SUMMARY**

**Feature**: Documents Section Revamp (Landing Screen, Grid View, Unified Search)

**Release Date**: 2025-07-15

**Baseline Period**: 2025-04-01 to 2025-06-30 (Q2 2025, pre-launch)

**Post-Launch Period**: 2025-07-15 to 2025-09-30 (Q3 2025, post-launch)

**Filters**: All users, Documents tab interactions

**Output Format**: CSV with weekly aggregates + cohort analysis (new vs. existing users)

---

**METRICS REQUESTED**

| # | Metric Name | Data Source | Calculation | Filters | Granularity |
|---|-------------|-------------|-------------|---------|-------------|
| 1 | Time to Find Document | App Telemetry | Time from Documents tab arrival to document detail view | Documents tab, all users | Weekly P50/P90 |
| 2 | Document Request Success Rate | Backend API Logs | % of document request flows completed | Documents tab, all users | Weekly % |
| 3 | Search Usage Rate | App Telemetry | % of users using unified search per week | Documents landing, all users | Weekly % |
| 4 | Grid View Adoption | App Telemetry | % of users switching to grid view | Documents screens, all users | Weekly % |
| 5 | Landing Screen Card Engagement | App Telemetry | % of users tapping "latest 5 types" cards | Documents landing, all users | Weekly % |
| 6 | Empty State CTR | App Telemetry | % of users clicking "Request Document" from empty state | Documents landing, new users | Weekly % |

---

**DETAILED METRIC SPECIFICATIONS**

**METRIC 1: Time to Find Document**

- **Definition**: Time from Documents tab arrival (landing screen) to document detail view, measured at 50th and 90th percentile.
- **Data Source**: App telemetry (screen navigation events)
- **Query Logic**:
  ```
  For each user journey:
    Calculate: document_detail_view_timestamp - documents_landing_timestamp
    Exclude outliers (>5 minutes)
    Aggregate P50 and P90 by week
  ```
- **Filters**:
  - Date Range (Baseline): 2025-04-01 to 2025-06-30
  - Date Range (Post-Launch): 2025-07-15 to 2025-09-30
  - Journey: Documents tab arrival → Document detail view
  - Platform: iOS + Android
- **Granularity**: Weekly P50/P90
- **Output Columns**: week_start_date, p50_time_to_find_seconds, p90_time_to_find_seconds, total_journeys, platform

**METRIC 2: Document Request Success Rate**

- **Definition**: Percentage of document request flows that resulted in successful completion (document requested from issuer), initiated from Documents tab.
- **Data Source**: Backend API logs (document request flow events)
- **Query Logic**:
  ```
  For each week:
    Count: document_request_started (from Documents tab)
    Count: document_request_completed (successful)
    Calculate: (completed / started) * 100
  ```
- **Filters**:
  - Date Range (Baseline): 2025-04-01 to 2025-06-30
  - Date Range (Post-Launch): 2025-07-15 to 2025-09-30
  - Origin Screen: Documents tab (landing, Issued list, Uploaded list)
  - Platform: iOS + Android
- **Granularity**: Weekly %
- **Output Columns**: week_start_date, total_requests_started, total_requests_completed, success_rate_percent, platform

**METRIC 3: Search Usage Rate**

- **Definition**: Percentage of active users who used unified search (Documents landing screen) at least once during the week.
- **Data Source**: App telemetry (search interaction events)
- **Query Logic**:
  ```
  For each week:
    Count: users who triggered search event (Documents landing)
    Count: total active users (visited Documents tab)
    Calculate: (search_users / active_users) * 100
  ```
- **Filters**:
  - Date Range (Baseline): 2025-04-01 to 2025-06-30 (search may not exist; if not, report "N/A")
  - Date Range (Post-Launch): 2025-07-15 to 2025-09-30
  - Screen: Documents landing
  - Platform: iOS + Android
- **Granularity**: Weekly %
- **Output Columns**: week_start_date, total_active_users, users_using_search, search_usage_rate_percent, platform

**METRIC 4: Grid View Adoption**

- **Definition**: Percentage of users who switched to grid view (at least once) during the week.
- **Data Source**: App telemetry (view mode selection event)
- **Query Logic**:
  ```
  For each week:
    Count: users who selected grid view (Documents screens)
    Count: total active users (visited Documents tab)
    Calculate: (grid_users / active_users) * 100
  ```
- **Filters**:
  - Date Range (Baseline): N/A (feature not active)
  - Date Range (Post-Launch): 2025-07-15 to 2025-09-30
  - Screen: Documents (Issued, Uploaded)
  - Platform: iOS + Android
- **Granularity**: Weekly %
- **Output Columns**: week_start_date, total_active_users, users_selecting_grid, grid_adoption_rate_percent, platform

**METRIC 5: Landing Screen Card Engagement**

- **Definition**: Percentage of users who tapped at least one "latest 5 document types" card on Documents landing screen.
- **Data Source**: App telemetry (card tap event)
- **Query Logic**:
  ```
  For each week:
    Count: users who tapped landing screen cards
    Count: total users who viewed landing screen
    Calculate: (card_tap_users / landing_viewers) * 100
  ```
- **Filters**:
  - Date Range (Baseline): N/A (feature not active)
  - Date Range (Post-Launch): 2025-07-15 to 2025-09-30
  - Screen: Documents landing
  - Platform: iOS + Android
- **Granularity**: Weekly %
- **Output Columns**: week_start_date, total_landing_viewers, users_tapping_cards, engagement_rate_percent, platform

**METRIC 6: Empty State CTR (First-Time Users)**

- **Definition**: Percentage of first-time users (no documents) who clicked "Request Document" CTA from Documents landing empty state.
- **Data Source**: App telemetry (empty state CTA click event)
- **Query Logic**:
  ```
  For each week:
    Count: new users seeing empty state (no documents)
    Count: new users clicking "Request Document" CTA
    Calculate: (cta_clicks / empty_state_views) * 100
  ```
- **Filters**:
  - Date Range (Baseline): 2025-04-01 to 2025-06-30 (may have different empty state)
  - Date Range (Post-Launch): 2025-07-15 to 2025-09-30
  - User Segment: First-time users (account age <7 days, 0 documents)
  - Screen: Documents landing
  - Platform: iOS + Android
- **Granularity**: Weekly %
- **Output Columns**: week_start_date, total_empty_state_views, total_cta_clicks, ctr_percent, platform

---

**COHORT ANALYSIS**

**Cohort Definition**: New users (account created within 7 days) vs. Existing users (account 8+ days old)

**Cohort Comparison**:
- Metric 1 (Time to Find Document): Compare P50/P90 between cohorts
- Metric 2 (Document Request Success): Compare success rate between cohorts
- Metric 3 (Search Usage): Compare usage rate between cohorts
- Insight Goal: Understand if revamp benefits new users more (clearer onboarding) or existing users (faster discovery)

**Output Format**: Separate CSV with cohort breakdown (cohort, metric, baseline, post-launch, change)

---

**CONTEXT & BACKGROUND**

**Why This Data?**
Documents revamp is the most significant UX improvement in 2025, redesigning the primary user journey for document management. We need to validate UX improvements (faster document discovery, higher engagement with new features) and identify optimization opportunities (which features are most adopted).

**How We'll Use It**:
- Report UX impact to DDA (design validation) and TDRA (user satisfaction)
- Prioritize optimization (e.g., A/B test "latest 5 vs. 7 document types")
- Validate foundational improvements for future features (Auto-Add Documents depends on landing screen)

**Priority**: High — Flagship UX feature, critical for stakeholder reporting.

**Contact**: [PM Name], [Email], [Slack: @pm-dv]

---

#### EXAMPLE 3: Copy-Paste Feature (Q3)

**Subject**: Copy-Paste Feature — Impact Measurement Data Request

**Priority**: Medium

**Requestor**: DV Product Team

**Date**: 2025-09-01

**Purpose**: Quantify usage of copy-paste feature (adoption rate, fields copied, user satisfaction) for Q3 2025 release.

**Deadline**: 2025-09-15

---

**DATA REQUEST SUMMARY**

**Feature**: Copy-Paste Feature in Document Details

**Release Date**: 2025-07-15

**Baseline Period**: 2025-04-01 to 2025-06-30 (Q2 2025, pre-launch)

**Post-Launch Period**: 2025-07-15 to 2025-09-30 (Q3 2025, post-launch)

**Filters**: All users, Document detail screen interactions

**Output Format**: JSON with event-level data + weekly aggregates

---

**METRICS REQUESTED**

| # | Metric Name | Data Source | Calculation | Filters | Granularity |
|---|-------------|-------------|-------------|---------|-------------|
| 1 | Copy Action Usage Rate | App Telemetry | % of document detail views with ≥1 copy action | Document details, all users | Weekly % |
| 2 | Fields Copied per Session | App Telemetry | Average number of fields copied per session (when ≥1 copy) | Document details, all users | Weekly average |
| 3 | Copy Actions by Document Type | App Telemetry | Breakdown of copy actions by document type | Document details, all users | Weekly breakdown |
| 4 | Support Tickets (Copy-Related) | Support Ticket System | Count of tickets mentioning "copy", "share", "retyping" keywords | All users | Weekly count |

---

**DETAILED METRIC SPECIFICATIONS**

**METRIC 1: Copy Action Usage Rate**

- **Definition**: Percentage of document detail views that included at least one copy action (field copied to clipboard).
- **Data Source**: App telemetry (copy action event)
- **Query Logic**:
  ```
  For each week:
    Count: document detail views with ≥1 copy action
    Count: total document detail views
    Calculate: (views_with_copy / total_views) * 100
  ```
- **Filters**:
  - Date Range (Baseline): N/A (feature not active)
  - Date Range (Post-Launch): 2025-07-15 to 2025-09-30
  - Screen: Document details (issued documents only)
  - Platform: iOS + Android
- **Granularity**: Weekly %
- **Output Columns**: week_start_date, total_detail_views, views_with_copy_action, usage_rate_percent, platform

**METRIC 2: Fields Copied per Session**

- **Definition**: Average number of fields copied per user session, calculated only for sessions with ≥1 copy action.
- **Data Source**: App telemetry (copy action event with field identifier)
- **Query Logic**:
  ```
  For each user session with ≥1 copy action:
    Count: total fields copied
    Calculate: total_fields_copied / total_sessions_with_copy
  Aggregate by week
  ```
- **Filters**:
  - Date Range (Post-Launch): 2025-07-15 to 2025-09-30
  - Screen: Document details
  - Platform: iOS + Android
- **Granularity**: Weekly average
- **Output Columns**: week_start_date, total_sessions_with_copy, total_fields_copied, avg_fields_per_session, platform

**METRIC 3: Copy Actions by Document Type**

- **Definition**: Breakdown of copy actions by document type (EID, Passport, Visa, etc.), showing which documents users copy most frequently.
- **Data Source**: App telemetry (copy action event with document type)
- **Query Logic**:
  ```
  For each week:
    Count: copy actions by document type
    Calculate: % of total copy actions per document type
  ```
- **Filters**:
  - Date Range (Post-Launch): 2025-07-15 to 2025-09-30
  - Screen: Document details
  - Platform: iOS + Android
- **Granularity**: Weekly breakdown
- **Output Columns**: week_start_date, document_type, total_copy_actions, percent_of_total_copies, platform

**METRIC 4: Support Tickets (Copy-Related)**

- **Definition**: Count of support tickets mentioning keywords: "copy", "share", "retyping", "transcription", "can't copy", "need to share data".
- **Data Source**: Support ticket system (keyword search)
- **Query Logic**:
  ```
  For each week:
    Search tickets for keywords in title/description
    Count: matching tickets
  ```
- **Filters**:
  - Date Range (Baseline): 2025-04-01 to 2025-06-30
  - Date Range (Post-Launch): 2025-07-15 to 2025-09-30
  - Keywords: "copy", "share", "retyping", "transcription", "can't copy", "need to share data"
- **Granularity**: Weekly count
- **Output Columns**: week_start_date, total_tickets_matching_keywords, period (baseline / post-launch)

---

**CONTEXT & BACKGROUND**

**Why This Data?**
Copy-paste is a small feature with potentially high user satisfaction impact. We need to understand adoption (how many users use it), intensity (how many fields they copy), and pain point resolution (support ticket reduction).

**How We'll Use It**:
- Validate user satisfaction improvement (support ticket reduction)
- Inform future enhancements (e.g., copy entire document as text block)
- Report to DDA (UX quality improvement) and TDRA (accessibility benefit)

**Priority**: Medium — User satisfaction feature, nice-to-have for stakeholder reporting.

**Contact**: [PM Name], [Email], [Slack: @pm-dv]

---

### 4.3 Priority Ranking of Data Requests

When ops team has limited capacity, prioritize data requests in this order:

#### TIER 1 (Critical — Week 1-2)
1. **Loader Removal + Real-Time Updates** — Foundational performance improvement, highest engineering investment, executive visibility
2. **Sharing Request Missing Doc Auto-Request** — Directly impacts North Star metric (Successful Combos %), critical for strategic reporting

#### TIER 2 (High Priority — Week 3-4)
3. **Documents Section Revamp** — Major UX feature, DDA collaboration validation, user satisfaction measurement
4. **Push Notification Tracking** — Foundational data (no prior baseline), informs future notification strategy

#### TIER 3 (Medium Priority — Week 5-6)
5. **PDF Viewer Implementation** — UX quality improvement, support ticket reduction validation
6. **Document Update Detection** — Proactive failure prevention, North Star support (indirect)

#### TIER 4 (Lower Priority — Week 7-8)
7. **Copy-Paste Feature** — Small feature, nice-to-have user satisfaction data

---

## 5. Additional Research Recommendations

Beyond quantitative metrics, these qualitative and experimental approaches will provide deeper insights into feature impact and user satisfaction.

---

### 5.1 Qualitative Measurement Approaches

#### 5.1.1 User Interviews (Post-Feature Launch)

**Goal**: Understand how users perceive features in their own words, uncover unarticulated pain points, validate quantitative findings.

**Method**:
- **Recruitment**: Sample 15-20 users across segments (new users, power users, different document types, iOS/Android)
- **Format**: 30-minute semi-structured interviews (video call or in-person)
- **Topics**:
  - Documents Section Revamp: "Walk me through how you find a document today. How has this changed for you?"
  - Copy-Paste Feature: "Tell me about the last time you needed to share document information with someone. How did you do it?"
  - PDF Viewer: "Show me how you view a document. What do you like or dislike about this experience?"
  - Sharing Request Auto-Request: "Describe what happens when you receive a sharing request but don't have all the documents. How does that feel?"

**Output**:
- Thematic analysis report (top 5 themes, quotes, pain points)
- Feature-specific insights (unexpected use cases, unmet needs)
- Prioritized enhancement opportunities

**Cadence**: Quarterly (post-launch of major features)

---

#### 5.1.2 Net Promoter Score (NPS) Survey

**Goal**: Measure overall user satisfaction and loyalty, track sentiment trends over time.

**Method**:
- **Question**: "How likely are you to recommend UAE PASS Documents to a friend or colleague?" (0-10 scale)
- **Follow-up**: "What is the primary reason for your score?" (open text)
- **Timing**: In-app survey triggered after key moments:
  - Successful sharing request (actionable notification → approval → completion)
  - Document request completion (requested → received)
  - Monthly for random sample of active users
- **Sample Size**: 200-500 responses per month

**Segmentation**:
- By feature usage (e.g., users who used Copy-Paste vs. didn't)
- By document type (EID users vs. Passport users vs. Visa users)
- By sharing frequency (high-frequency vs. low-frequency sharers)

**Analysis**:
- Calculate NPS: % Promoters (9-10) - % Detractors (0-6)
- Thematic analysis of open text (top reasons for promotion/detraction)
- Track NPS trend over quarters (correlate with feature releases)

**Target**: NPS ≥50 (good), ≥70 (excellent) for digital identity apps

**Cadence**: Monthly survey, quarterly reporting

---

#### 5.1.3 Support Ticket Analysis (Deep Dive)

**Goal**: Identify pain points not captured by quantitative metrics, validate feature impact on support burden.

**Method**:
- **Keyword Tagging**: Manually tag support tickets by theme (e.g., "can't find document", "sharing failed", "document expired", "can't zoom PDF")
- **Root Cause Analysis**: For top 10 ticket themes, trace back to product gaps or UX friction
- **Before/After Comparison**: Compare ticket volume and themes pre/post feature launch
- **User Journey Mapping**: Reconstruct user journeys from ticket descriptions to identify friction points

**Output**:
- Monthly support ticket report (top 10 themes, volume trend, resolution time)
- Feature-specific impact analysis (e.g., "PDF viewer launch reduced 'can't zoom' tickets by 65%")
- Product backlog (prioritized enhancements based on support pain points)

**Cadence**: Monthly analysis, quarterly deep dive

---

#### 5.1.4 UX Lab Testing (Ongoing)

**Goal**: Observe real users interacting with features, identify usability issues, validate design decisions.

**Method**:
- **Recruitment**: 8-12 users per session (mix of new and existing users)
- **Format**: Moderated usability testing (30-45 min per user)
- **Tasks**:
  - "Find your EID document and copy the EID number"
  - "You received a sharing request from a bank. Show me how you'd respond"
  - "Request a new Passport document from ICP"
  - "Switch your Documents view to grid mode and find your Visa"
- **Observation**: Record screen + audio, note friction points, confusion, errors
- **Metrics**: Task success rate, time on task, error rate, user satisfaction (1-5 scale)

**Output**:
- Usability report (task success rates, friction points, recommendations)
- Video clips of key moments (for stakeholder presentations)
- Prioritized UX enhancements

**Cadence**: Quarterly (Q1: baseline, Q2: revamp validation, Q3: optimization, Q4: roadmap planning)

---

### 5.2 A/B Testing Opportunities

A/B testing allows us to validate hypotheses about feature variations and optimize for maximum impact.

---

#### 5.2.1 Documents Landing Screen: Latest 5 vs. 7 vs. 10 Document Types

**Hypothesis**: Showing more recent document types increases engagement, but too many creates clutter.

**Variants**:
- **Control**: Latest 5 document types (current design)
- **Variant A**: Latest 7 document types
- **Variant B**: Latest 10 document types

**Success Metric**: Landing screen card engagement rate (% of users tapping ≥1 card)

**Secondary Metrics**: Time to find document, screen scroll depth, user satisfaction (in-app survey)

**Sample Size**: 10,000 users per variant (30,000 total)

**Duration**: 2 weeks

**Decision Criteria**: If Variant A or B improves engagement by ≥10% without increasing scroll depth significantly, roll out winner.

---

#### 5.2.2 Sharing Request Auto-Request Popup: One-Tap vs. Two-Tap Confirmation

**Hypothesis**: Simplifying auto-request confirmation (one-tap "Request All" vs. two-tap "Request All" → "Confirm") increases acceptance rate.

**Variants**:
- **Control**: Two-tap (current: "Request All" button → confirmation dialog)
- **Variant A**: One-tap (single "Request All Missing Documents" button, no confirmation)

**Success Metric**: Auto-request acceptance rate (% of popups accepted)

**Secondary Metrics**: Sharing request abandonment rate, time to complete sharing

**Sample Size**: 5,000 sharing requests per variant (10,000 total)

**Duration**: 3 weeks (longer to accumulate sharing requests)

**Decision Criteria**: If Variant A improves acceptance by ≥15% without increasing accidental taps (measured by immediate abandonment), roll out one-tap.

---

#### 5.2.3 PDF Viewer: Default Zoom (Fit-to-Width vs. Fit-to-Page)

**Hypothesis**: Fit-to-width provides better readability on mobile screens than fit-to-page.

**Variants**:
- **Control**: Fit-to-page (shows entire page, may require pinch-to-zoom to read)
- **Variant A**: Fit-to-width (page width matches screen width, requires vertical scroll)

**Success Metric**: Average viewing duration (longer = more engagement/readability)

**Secondary Metrics**: Pinch-to-zoom usage (lower for fit-to-width), user satisfaction (in-app survey)

**Sample Size**: 8,000 document views per variant (16,000 total)

**Duration**: 2 weeks

**Decision Criteria**: If Variant A increases viewing duration by ≥10% and reduces zoom usage by ≥20%, roll out fit-to-width.

---

#### 5.2.4 Copy-Paste Feature: Toast Message Variations

**Hypothesis**: More descriptive toast messages (e.g., "EID Number copied" vs. generic "Copied") increase user confidence and satisfaction.

**Variants**:
- **Control**: Generic toast ("Copied")
- **Variant A**: Field-specific toast ("[Field Name] copied", e.g., "EID Number copied")
- **Variant B**: Field-specific + action hint ("[Field Name] copied. Paste it wherever you need.")

**Success Metric**: Repeat copy actions per session (higher = more confidence)

**Secondary Metrics**: User satisfaction (in-app survey), time spent on document details

**Sample Size**: 6,000 users per variant (18,000 total)

**Duration**: 2 weeks

**Decision Criteria**: If Variant A or B increases repeat copy actions by ≥10% and improves satisfaction, roll out winner.

---

#### 5.2.5 Empty State CTA: "Request Document" vs. "Get Started"

**Hypothesis**: Action-oriented CTA ("Request Document") performs better than generic CTA ("Get Started") for first-time users.

**Variants**:
- **Control**: "Request Document" (current)
- **Variant A**: "Get Started"
- **Variant B**: "Add Your First Document"

**Success Metric**: Empty state CTA click-through rate (% of first-time users clicking)

**Secondary Metrics**: Document request completion rate (after clicking CTA)

**Sample Size**: 3,000 first-time users per variant (9,000 total)

**Duration**: 4 weeks (longer to accumulate first-time users)

**Decision Criteria**: If Control outperforms variants by ≥5%, validate current design. If Variant A or B improves CTR by ≥15%, roll out winner.

---

### 5.3 Cohort Analysis Suggestions

Cohort analysis reveals how different user segments experience features differently, informing targeted optimizations.

---

#### 5.3.1 New Users vs. Existing Users

**Question**: Do new users adopt new features faster than existing users (who may have ingrained habits)?

**Cohorts**:
- **New Users**: Account created within 7 days of feature launch
- **Existing Users**: Account created 8+ days before feature launch

**Features to Analyze**:
- Grid View Adoption: Do new users prefer grid view (no prior list view habit)?
- Copy-Paste Usage: Do existing users discover copy-paste (no onboarding nudge)?
- Search Usage: Do new users use unified search more (clearer entry point)?

**Metrics**:
- Feature adoption rate (% of cohort using feature within 4 weeks)
- Time to first use (days from feature launch to first use)
- Usage frequency (interactions per week)

**Insight Goal**: If new users adopt faster, invest in onboarding nudges for existing users. If existing users adopt slower, consider in-app education (tooltips, banners).

---

#### 5.3.2 High-Frequency Sharers vs. Low-Frequency Sharers

**Question**: Do users who share documents frequently (power users) benefit more from sharing-related features?

**Cohorts**:
- **High-Frequency Sharers**: ≥3 sharing requests per month
- **Low-Frequency Sharers**: <3 sharing requests per month

**Features to Analyze**:
- Sharing Request Auto-Request: Do high-frequency sharers accept auto-request more (proactive document readiness)?
- Document Update Detection: Do high-frequency sharers update documents faster (risk awareness)?

**Metrics**:
- Auto-request acceptance rate (by cohort)
- Proactive update success rate (by cohort)
- Successful Combos % (by cohort)

**Insight Goal**: If high-frequency sharers benefit more, prioritize features for this segment (e.g., bulk sharing, SP-specific document presets). If low-frequency sharers struggle, invest in education/guidance.

---

#### 5.3.3 iOS Users vs. Android Users

**Question**: Do platform differences (OS design conventions, performance) impact feature adoption?

**Cohorts**:
- **iOS Users**: iPhone/iPad
- **Android Users**: Android devices

**Features to Analyze**:
- PDF Viewer: Do iOS users interact more with native PDF viewer (platform advantage)?
- Push Notification Opt-In: Do iOS users opt-in less (stricter OS permissions)?
- Grid View Adoption: Do Android users prefer grid view (Files app familiarity)?

**Metrics**:
- Feature adoption rate (by platform)
- Performance metrics (screen load time, crash rate by platform)
- User satisfaction (NPS by platform)

**Insight Goal**: Identify platform-specific optimization opportunities. If iOS lags, investigate design/performance issues. If Android lags, test Android-specific UX patterns.

---

#### 5.3.4 Document Type Segmentation (EID Users vs. Passport Users vs. Visa Users)

**Question**: Do users with different document types have different needs/behaviors?

**Cohorts**:
- **EID Users**: Users with Emirates ID stored
- **Passport Users**: Users with Passport stored
- **Visa Users**: Users with Visa/Residency stored

**Features to Analyze**:
- Copy-Paste Usage: Which document fields are copied most (EID number, passport number, visa number)?
- Sharing Frequency: Which document type is shared most often (informs priority for features)?
- Document Update Detection: Which document type has highest hash mismatch rate (expiry/revocation frequency)?

**Metrics**:
- Feature usage rate (by document type)
- Sharing request volume (by document type)
- Update request volume (by document type)

**Insight Goal**: Prioritize features for high-usage document types. For example, if EID users copy-paste most frequently, optimize EID detail screen layout.

---

### 5.4 Additional Data Sources to Explore

Beyond app telemetry and backend logs, these data sources can provide complementary insights.

---

#### 5.4.1 Service Provider (SP) Feedback

**Goal**: Understand how features impact SP experience (integration ease, data quality, conversion rates).

**Method**:
- Quarterly SP surveys (5-10 questions, 10-15 min)
- Topics:
  - Document Sharing experience: "How satisfied are you with document data quality from UAE PASS?"
  - Integration feedback: "What challenges did you face during integration?"
  - Feature requests: "What capabilities would improve your users' experience?"
- One-on-one SP interviews (for top 5 SPs by volume)

**Output**:
- SP satisfaction score (1-10 scale, trend over quarters)
- Top SP pain points (ranked by frequency)
- SP-driven feature requests (inform roadmap)

**Cadence**: Quarterly survey, bi-annual interviews

---

#### 5.4.2 Issuer (ICP) Feedback

**Goal**: Understand how features impact issuer operations (request volume, error rates, data freshness).

**Method**:
- Monthly sync meetings with ICP technical team
- Topics:
  - Document request volume trends (impact of auto-request feature)
  - Error rates (failed requests, hash mismatches)
  - Data freshness (how often documents are updated)

**Output**:
- Issuer health report (request volume, success rate, latency)
- Identified bottlenecks (e.g., ICP downtime causing failed requests)
- Collaboration opportunities (e.g., real-time push updates instead of polling)

**Cadence**: Monthly sync meetings

---

#### 5.4.3 App Store Reviews

**Goal**: Understand user sentiment in public forums, identify pain points mentioned in reviews.

**Method**:
- Weekly scraping of App Store (iOS) and Google Play (Android) reviews
- Keyword tagging: "documents", "sharing", "copy", "PDF", "loader", "slow", "crash", "can't find"
- Sentiment analysis: Positive, Neutral, Negative
- Thematic analysis: Top 5 themes in 1-star reviews, top 5 themes in 5-star reviews

**Output**:
- Weekly review report (average rating, sentiment breakdown, top themes)
- Feature-specific feedback (e.g., "Users love copy-paste feature: mentioned in 12 reviews this week")
- Response strategy (prioritize reviews mentioning bugs or UX issues)

**Cadence**: Weekly monitoring, monthly analysis

---

#### 5.4.4 Social Media Listening

**Goal**: Identify user conversations about UAE PASS Documents on social platforms (Twitter, Instagram, forums).

**Method**:
- Monitor hashtags: #UAEPASS, #DigitalDocuments, #EmiratesID
- Track mentions: "@UAEPASS", "UAE PASS app"
- Manual review of forums (Reddit, expat Facebook groups)

**Output**:
- Monthly social listening report (mention volume, sentiment, top topics)
- Crisis detection (sudden spike in negative mentions = potential bug/outage)
- Feature awareness (are users discovering new features organically?)

**Cadence**: Monthly review

---

### 5.5 Long-Term Impact Tracking (6-12 Months)

Some features have delayed or compounding impact that requires long-term monitoring.

---

#### 5.5.1 Sustained Performance Improvements

**Question**: Do performance improvements (loader removal, real-time updates) sustain over time as user base grows?

**Metrics to Track**:
- API call volume per user (monthly trend)
- Screen load time P90 (monthly trend)
- Crash rate (monthly trend)
- Firestore sync error rate (monthly trend)

**Analysis**: Plot 12-month trend lines. Identify degradation points (e.g., Month 6 shows 20% increase in load time → investigate scaling issues).

**Action**: If degradation detected, prioritize backend optimization (caching, indexing, scaling).

---

#### 5.5.2 Cumulative Impact on North Star Metric

**Question**: How do multiple features compound to improve Successful Combos % over time?

**Method**:
- Track Successful Combos % monthly (12-month trend)
- Annotate feature launches on trend line (e.g., "Q1: Loader Removal", "Q3: Documents Revamp", "Q3: Auto-Request")
- Calculate cumulative impact: Baseline (Q4 2024) → Current (Q4 2025)

**Target**: +15-20 absolute point improvement in Successful Combos % over 12 months.

**Action**: If target not met, conduct deep-dive analysis (which failure modes persist? which features underperformed?).

---

#### 5.5.3 User Retention and Engagement

**Question**: Do UX improvements increase user retention and engagement over time?

**Metrics to Track**:
- Monthly Active Users (MAU) trend
- Daily Active Users / Monthly Active Users (DAU/MAU ratio) — stickiness
- User retention rate (% of users active in Month N who return in Month N+1)
- Average sessions per user per month

**Analysis**: Plot 12-month trends. Correlate with feature launches (e.g., "MAU increased 8% in Q3 2025, coinciding with Documents Revamp").

**Target**: +10-15% MAU growth, +5-10% retention rate improvement (12 months).

---

### 5.6 Recommended Research Cadence

**Weekly**:
- Support ticket monitoring (flag critical issues)
- App Store review monitoring (flag 1-star reviews)

**Monthly**:
- Support ticket deep dive (top 10 themes)
- NPS survey analysis (sentiment trends)
- App Store review thematic analysis
- Social media listening report

**Quarterly**:
- User interviews (15-20 users, post-feature launch)
- UX lab testing (8-12 users, usability validation)
- SP satisfaction survey (top 5-10 SPs)
- Feature impact reports (detailed analysis for stakeholders)
- Cohort analysis (new vs. existing users, iOS vs. Android, etc.)

**Annually**:
- Comprehensive user research study (100+ users, mixed methods)
- Long-term impact review (12-month trends, North Star progress)
- Competitive benchmarking refresh (global digital identity apps)

---

## 6. Appendix: All 17 Features Summary

For reference, here is a summary of all 17 features released in 2025 (from the CSV), including the 7 highest-impact features analyzed above.

---

### Q1 2025 Features

| # | Feature Name | Description | Advantages | Impact Tier |
|---|--------------|-------------|------------|-------------|
| 1 | **Removal of Loaders in All Screens** | Removed loaders from listing screens; first-time users see loader, then data updates dynamically via Firestore real-time cloud updates | Drastic reduction in API calls; seamless experience with updated information without loaders | **TIER 1 (Highest Impact)** |
| 2 | **Local Search + Real-Time Updates** | Implemented real-time Firestore updates in listing screens; updated search logic at app side without calling API for every character | Drastic reduction in API calls; seamless experience | **TIER 1 (covered with Feature 1)** |
| 3 | Migration of Requested Document Details (Mustache to JSON) | Display issued document details in list format based on JSON response (instead of Mustache HTML) | Significantly faster loading time; more control for text size accessibility | TIER 2 (Performance) |
| 4 | UI Enhancements (Messages + Shadows/Chips) | Updated messages, removed shadows and chip designs | Enhanced look and feel; more contextual information | TIER 3 (Incremental) |
| 5 | **Push Notification Tracking** | Track whether user enabled notifications; update backend | Statistics on notification opt-in rates | **TIER 1 (Highest Impact)** |

---

### Q2 2025 Features

| # | Feature Name | Description | Advantages | Impact Tier |
|---|--------------|-------------|------------|-------------|
| 6 | UI Enhancements (Error Messages) | Updated error messages in Document Selection and Sharing screens | More contextual information | TIER 3 (Incremental) |
| 7 | UI Enhancements (Ghost Loaders) | Implemented ghost loaders to remove loaders in listing screens | Users can access features even during loading; enhanced look and feel | TIER 3 (Incremental) |
| 8 | MockSP App Development | Sample application for unit testing of SP integration features | Testing in all environments including production; debug SP issues; QA efficiency | TIER 4 (Internal Tooling) |
| 9 | UX Lab Testing | Connected with real users to get feedback on DV flows | Valuable user feedback; informed feature enhancements | TIER 4 (Research Activity) |

---

### Q3 2025 Features

| # | Feature Name | Description | Advantages | Impact Tier |
|---|--------------|-------------|------------|-------------|
| 10 | **Sharing Request - Missing Document Auto Request** | When user lands on sharing request, if mandatory docs unavailable, popup allows requesting all at once | Avoids manual intervention to request unavailable docs individually | **TIER 1 (Highest Impact)** |
| 11 | Bulk Signing Document Upload | Allow user to upload multiple self-signed documents from Home Screen in one flow | Upload multiple docs in one flow | TIER 3 (Nice-to-Have) |
| 12 | MockSP App Enhancements | Added custom QR feature to MockSP app | Create custom actionable notifications with different combinations | TIER 4 (Internal Tooling) |
| 13 | Consent Box UI Improvement | Based on UX lab feedback, made consent box more noticeable and user-friendly | Enhanced user experience | TIER 3 (Incremental) |
| 14 | **Documents Section Revamp** | New landing screen with latest 5 document types; updated Issued/Uploaded listing screens; search from landing screen | Enhanced user experience; faster document discovery | **TIER 1 (Highest Impact)** |
| 15 | Document Opening Failure Tracker API | Track errors when viewing issued document details | Ops visibility (telemetry) | TIER 4 (Monitoring) |
| 16 | Document Details Language Segregation | Display issued document details in both English and Arabic in one screen | User doesn't need to change app language to view details | TIER 3 (Niche Use Case) |
| 17 | **Copy-Paste Feature** | Allow user to copy any field from issued document details screen | Enhanced user experience; no manual retyping | **TIER 1 (Highest Impact)** |

---

### Q4 2025 Features

| # | Feature Name | Description | Advantages | Impact Tier |
|---|--------------|-------------|------------|-------------|
| 18 | **Document Update Detection** | Implement document request whenever hash mismatch detected (in Documents landing, view details, view document, QR verification) | Allow user to request new version on-the-go when hash mismatch detected | **TIER 1 (Highest Impact)** |
| 19 | Loader Tracker Introduction | Implement telemetry API in Documents landing, view details, view documents screens | Track API call time and display time | TIER 4 (Monitoring) |
| 20 | **PDF Viewer Implementation** | Display all issued documents in PDF; HTML fallback if issuer doesn't support PDF | Enhanced user experience; consistent viewing | **TIER 1 (Highest Impact)** |
| 21 | Email/Mobile Mismatch Message | Display personal details even if SP not requesting them | Enhanced user experience; transparency | TIER 3 (Edge Case) |

---

### Impact Tier Definitions

- **TIER 1 (Highest Impact)**: Features affecting core user journeys, high frequency of use, strategic value (North Star alignment), or foundational improvements (performance, data)
- **TIER 2 (Performance)**: Technical improvements with measurable performance impact but limited user-facing visibility
- **TIER 3 (Incremental)**: UX polish, nice-to-have improvements, niche use cases
- **TIER 4 (Internal/Research)**: Tooling, monitoring, research activities (no direct user impact)

---

## Summary

This framework provides a comprehensive, data-driven approach to measuring and reporting feature impact. It is designed to be immediately actionable:

1. **Ops Team**: Use Section 4 templates to request specific data with clear definitions and context
2. **Product Team**: Use Section 2 frameworks to analyze feature impact, validate success criteria, and inform optimization priorities
3. **Management Stakeholders**: Use Section 3 templates to report impact compellingly with quantitative results and storytelling
4. **Research Team**: Use Section 5 recommendations to complement quantitative analysis with qualitative insights and experiments

**Next Steps**:
1. Prioritize data requests using Tier 1-4 ranking (Section 4.3)
2. Submit top 3 data requests to ops team (Loader Removal, Sharing Auto-Request, Documents Revamp)
3. Conduct first round of user interviews (15 users, post-Documents Revamp launch)
4. Set up NPS in-app survey (trigger after successful sharing request)
5. Create monthly reporting cadence with TDRA/DDA stakeholders

---

**Document Owner**: DV Product Team
**Last Updated**: 2025-11-18
**Review Cadence**: Quarterly (update KPIs, success criteria, research recommendations)
