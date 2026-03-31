Here’s a clean requirements draft you can hand to Analytics/FE/BE to enhance reporting for sharing transactions. It captures channels, a unified status model with codes, transitions, and the reporting outputs (funnels, distributions, and KPIs).
Sharing Transactions – Status Model & Reporting Requirements
0. Purpose
Provide a structured, lifecycle-based view of every sharing request so we can see where users progress or drop off. Replace flat “transactions” counts with a status timeline and clear funnel metrics per channel (Notification, Redirection, QR).
1. In Scope
•	Three sharing channels:
1.	Notification (push → open in UAE PASS)
2.	App-to-app / Web-to-app redirection
3.	Web QR (QR rendered on SP web → scan in UAE PASS)
•	Status model that distinguishes:
o	Document availability at open (ready vs missing)
o	User action on requesting missing documents
o	Outcomes of document fetch (success / technical error / not found at issuer)
o	Consent given or not
o	PIN step outcomes (verified / failed)
o	Final result (success / expired / user aborted / technical error)
•	Reporting: funnel, distributions, and time-in-step across channels and service providers.
2. Core Entities & Keys
•	request_id (unique per sharing request; correlation ID)
•	sp_id (service provider)
•	channel ∈ {notification, redirect, qr}
•	platform ∈ {ios, android}
•	app_version (semantic string)
•	required_docs (array of types)
All events and status rows must be joinable by request_id.
3. Unified Status Dictionary (with Codes)
Terminal statuses are marked [T]. Channels listed where applicable.
Request ingress
•	S00_REQUEST_CREATED — request registered in DV (all channels)
•	S01_NOTIF_SENT — push notification sent (notification only)
•	S02_NOTIF_DELIVERED — push delivered by OS (notification only)
•	S03_NOTIF_OPENED — user opened push → landed on request (notification only)
•	S04_REDIRECT_LAUNCHED — SP triggered app/web-to-app redirect (redirection only)
•	S05_REDIRECT_LANDED — user landed on request via redirect (redirection only)
•	S06_QR_RENDERED — QR shown on SP web (qr only)
•	S07_QR_SCANNED — user scanned QR → landed on request (qr only)
•	S08_REQUEST_VIEWED — request screen viewed in UAE PASS (all channels; first stable “landed” state)
Document readiness
•	S10_DOCS_READY_AT_OPEN — all mandatory docs present at first view
•	S11_DOCS_MISSING_AT_OPEN — mandatory docs missing at first view
Missing-docs user action
•	S12_MISSING_DOC_REQUEST_INITIATED — user tapped “Request” for a required doc
•	S13_MISSING_DOC_REQUEST_SUCCESS — required doc retrieved and added
•	S14_MISSING_DOC_REQUEST_ERROR — user attempted; technical error from issuer/DV
•	S15_MISSING_DOC_NOT_FOUND_AT_ISSUER — user attempted; issuer reports “no such doc” (e.g., user doesn’t own vehicle)
Consent & share button
•	S20_AWAITING_CONSENT — docs ready but consent not yet checked
•	S21_CONSENT_GIVEN — user checked consent; “Share” enabled
PIN & authentication
•	S30_PIN_REQUESTED — app prompted for PIN
•	S31_PIN_VERIFIED — PIN entered correctly
•	S32_PIN_FAILED — PIN incorrect or aborted PIN screen
Final outcomes
•	S40_SHARE_SUCCESS [T] — documents shared successfully
•	S41_SHARE_TECH_ERROR [T] — technical failure after PIN (timeouts, 5xx, etc.)
•	S42_EXPIRED [T] — request expired (TTL reached without completion)
•	S43_USER_ABORTED [T] — user backed out / closed without completion
•	S44_NOT_ELIGIBLE [T] — cannot satisfy requirements (e.g., S15 persists)
Notes
•	S01–S03 apply only to notification flow.
•	S04–S05 for redirection; S06–S07 for QR.
•	Every request must have S08_REQUEST_VIEWED once the user lands in UAE PASS.
4. Allowed Transitions (simplified)
Ingress
•	Notification: S00 → S01 → S02 → S03 → S08
•	Redirection: S00 → S04 → S05 → S08
•	QR: S00 → S06 → S07 → S08
At first view (S08)
•	If docs ready: S08 → S10 → S20
•	If docs missing: S08 → S11 → (S12 or S43/S42)
Missing-doc branch
•	S11 → S12 → { S13 → S20, S14 → S11, S15 → S44[T] }
Consent & PIN
•	S20 → S21 → S30 → { S31 → { S40[T] or S41[T] }, S32 → S43[T] }
Expiry
•	Any non-terminal may transition to S42_EXPIRED[T] when TTL is reached.
5. Event Schema (analytics logging)
For every status transition, fire an event with:
•	event_name (e.g., “sharing_status_changed”)
•	request_id, sp_id, channel, platform, app_version
•	from_status_code, to_status_code
•	doc_context: { required_count, missing_count, missing_types[] }
•	error: { code, source } when applicable (issuer, DV, network, user_cancel)
•	timing: { event_ts, step_latency_ms (since previous status), total_age_ms (since S00) }
Additional per-channel properties:
•	notification: push_provider_status (sent/delivered), os_open_result
•	redirect: source (app/web), deep_link_ok (bool)
•	qr: qr_age_sec at scan, qr_expired (bool)
6. Data Model (storage for reporting)
•	sharing_requests (one row/request)
o	request_id, sp_id, channel, created_ts, required_docs[], platform, app_version
•	sharing_status_history (1..n rows/request)
o	request_id, status_code, status_ts, meta (JSONB), error_code, step_latency_ms
•	v_sharing_latest_status (view)
o	request_id, latest_status_code, latest_status_ts
•	daily_sharing_funnel (aggregated)
o	date, sp_id, channel, counts per status_code, conversion rates (see §7)
7. Reporting Outputs
A. Funnel by channel & SP (last 7/30 days)
•	Notification: S01→S02→S03→S08→(S10/S11)→…→S40
o	KPIs: Delivery rate (S02/S01), Open rate (S03/S02), Landed rate (S08/S03)
•	Redirection: S04→S05→S08→…→S40
o	KPIs: Redirect land rate (S05/S04), Landed-to-complete (S40/S08)
•	QR: S06→S07→S08→…→S40
o	KPIs: Scan rate (S07/S06)
B. Document readiness at first view
•	% S10_DOCS_READY_AT_OPEN vs S11_DOCS_MISSING_AT_OPEN, per SP/service/doc-type.
C. Missing-doc behavior
•	Initiation rate: S12/S11
•	Fetch success: S13/S12
•	Not found rate: S15/S12
•	Tech error rate: S14/S12
D. Consent step
•	% AWAITING_CONSENT dwell (time in S20)
•	Consent rate: S21/(S10+S13)
E. PIN failures
•	PIN fail rate: S32/(S31+S32) at the PIN step
•	Post-PIN tech fail: S41/S31
F. Terminals distribution
•	S40, S41, S42, S43, S44 as % of S00, segmented by SP, channel, platform.
G. Time-to-complete
•	Median and p90 from S00→S40, and step latencies (e.g., S08→S21).
8. Channel Differentiation Rules
•	Notification-only statuses: S01, S02, S03
•	Redirect-only: S04, S05
•	QR-only: S06, S07
•	All channels must include S08_REQUEST_VIEWED onward.
•	Reports must filter/slice by channel; aggregation must not mix channel-specific steps.
9. Acceptance Criteria
•	Every request has S00; if the user lands in UAE PASS, S08 is present.
•	Status transitions are append-only, time-ordered, and unique (no duplicates).
•	Channel-specific statuses appear only for that channel.
•	Missing-docs branch records whether the user initiated request (S12) and the outcome (S13/S14/S15).
•	Consent state is explicit (S20 vs S21).
•	PIN step has explicit outcomes (S31 or S32).
•	A single terminal status [T] per request.
•	Dashboards show: per-channel funnel, terminals distribution, missing-docs behavior, consent rate, PIN failure rate, time-to-complete.
•	All metrics segmentable by SP, service, doc-type, platform, app version.
10. Implementation Tasks (by team)
Analytics/BE
•	Add sharing_status_history table; create ingestion for status events.
•	Enforce unique (request_id, status_code, status_ts).
•	Compute step_latency_ms and total_age_ms on insert.
•	Build v_sharing_latest_status and daily_sharing_funnel.
FE (UAE PASS app)
•	Emit events for: S08, S10/S11, S12–S15, S20–S21, S30–S32, S40–S44 with required properties.
•	Ensure event emission on both iOS/Android, including edge cases (backgrounding, app kill).
SP/OPS (coordination)
•	Keep correlation IDs unique (separate initiative).
•	Validate that SPs using notification vs redirect vs QR are tagged correctly at request creation.
11. Examples (for clarity)
Notification flow — successful path
•	S00 → S01 → S02 → S03 → S08 → S10 → S20 → S21 → S30 → S31 → S40[T]
Redirection flow — missing doc then success
•	S00 → S04 → S05 → S08 → S11 → S12 → S13 → S20 → S21 → S30 → S31 → S40[T]
QR flow — doc request error then abandon
•	S00 → S06 → S07 → S08 → S11 → S12 → S14 → S43[T]
Notification flow — not found at issuer
•	S00 → S01 → S02 → S03 → S08 → S11 → S12 → S15 → S44[T]
12. Error Codes (examples)
•	issuer_timeout, issuer_5xx, issuer_not_found, dv_timeout, dv_5xx, network_error, user_cancel, pin_incorrect, pin_dismissed

