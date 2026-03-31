"""
UAE PASS Digital Documents - Document Sharing Request Analysis
==============================================================

This script analyzes 422,596 sharing request events from June 25 to November 18, 2025
to extract actionable insights for prioritizing fixes and enhancements.

Data source: 6.4.0WeeklyTrend.xlsx
Reference: document_sharing_request_journey.md (38 failure points across 8 journey steps)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("UAE PASS DIGITAL DOCUMENTS - SHARING REQUEST ANALYSIS")
print("="*80)
print(f"\nAnalysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# SECTION 1: DATA LOADING
# ============================================================================
print("\n" + "="*80)
print("1. LOADING DATA")
print("="*80)

df = pd.read_excel('6.4.0WeeklyTrend.xlsx', sheet_name='Data')
df_new = pd.read_excel('6.4.0WeeklyTrend.xlsx', sheet_name='DataNewFields')

print(f"\nMain Dataset:")
print(f"  - Total records: {len(df):,}")
print(f"  - Date range: {df['CREATED_AT'].min().date()} to {df['CREATED_AT'].max().date()}")
print(f"  - Duration: {(df['CREATED_AT'].max() - df['CREATED_AT'].min()).days} days")

print(f"\nNew Fields Dataset (with first-read tracking):")
print(f"  - Total records: {len(df_new):,}")
print(f"  - Date range: {df_new['CREATED_AT'].min().date()} to {df_new['CREATED_AT'].max().date()}")

# ============================================================================
# SECTION 2: FUNNEL ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("2. FUNNEL ANALYSIS - DROP-OFF AT EACH STAGE")
print("="*80)

total_requests = len(df)

# Stage 1: Notification delivered
# NOTIFIED_SUCCESSFULLY is mostly null, so we assume all requests in dataset were delivered
notified = total_requests
print(f"\nStage 1: Notification Delivered")
print(f"  Total requests: {notified:,} (100.0%)")

# Stage 2: Notification opened (Read)
notification_opened = len(df[df['NOTIFICATION_STATE'] == 'Read'])
print(f"\nStage 2: Notification Opened (State = 'Read')")
print(f"  Opened: {notification_opened:,} ({notification_opened/total_requests*100:.1f}%)")
print(f"  Drop-off: {total_requests - notification_opened:,} ({(total_requests - notification_opened)/total_requests*100:.1f}%)")

# Check other notification states
print(f"\n  Notification States Breakdown:")
notif_states = df['NOTIFICATION_STATE'].value_counts()
for state, count in notif_states.items():
    print(f"    - {state}: {count:,} ({count/total_requests*100:.1f}%)")

# Stage 3: Consent given
consent_given = len(df[df['CONSENT_GIVEN'] == 'Yes'])
print(f"\nStage 3: Consent Given")
print(f"  Consent given: {consent_given:,} ({consent_given/total_requests*100:.1f}%)")
print(f"  Drop-off from opened: {notification_opened - consent_given:,} ({(notification_opened - consent_given)/notification_opened*100:.1f}%)")

# Stage 4: PIN entered
pin_given = len(df[df['PIN_GIVEN'] == 'Yes'])
print(f"\nStage 4: PIN Entered")
print(f"  PIN entered: {pin_given:,} ({pin_given/total_requests*100:.1f}%)")
print(f"  Drop-off from consent: {consent_given - pin_given:,} ({(consent_given - pin_given)/consent_given*100:.1f}%)")

# Stage 5: Sharing completed
shared = len(df[df['STATUS'] == 'Shared'])
print(f"\nStage 5: Sharing Completed (Status = 'Shared')")
print(f"  Successfully shared: {shared:,} ({shared/total_requests*100:.1f}%)")
print(f"  Drop-off from PIN entered: {pin_given - shared:,} ({(pin_given - shared)/pin_given*100:.1f}%)")

# Overall funnel
print(f"\n{'='*60}")
print(f"OVERALL FUNNEL SUMMARY")
print(f"{'='*60}")
print(f"  1. Notification Delivered:  {total_requests:,} (100.0%)")
print(f"  2. Notification Opened:     {notification_opened:,} ({notification_opened/total_requests*100:.1f}%) - Drop: {(1-notification_opened/total_requests)*100:.1f}%")
print(f"  3. Consent Given:           {consent_given:,} ({consent_given/total_requests*100:.1f}%) - Drop: {(1-consent_given/total_requests)*100:.1f}%")
print(f"  4. PIN Entered:             {pin_given:,} ({pin_given/total_requests*100:.1f}%) - Drop: {(1-pin_given/total_requests)*100:.1f}%")
print(f"  5. Successfully Shared:     {shared:,} ({shared/total_requests*100:.1f}%) - Drop: {(1-shared/total_requests)*100:.1f}%")
print(f"\n  END-TO-END SUCCESS RATE: {shared/total_requests*100:.2f}%")

# ============================================================================
# SECTION 3: FAILURE POINT ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("3. FAILURE POINT ANALYSIS")
print("="*80)

# STATUS breakdown
print(f"\n3.1 STATUS Breakdown:")
print(f"{'='*60}")
status_counts = df['STATUS'].value_counts()
for status, count in status_counts.items():
    print(f"  {status:25s}: {count:7,} ({count/total_requests*100:5.2f}%)")

# ERROR_CATEGORIZATION patterns
print(f"\n3.2 ERROR_CATEGORIZATION Patterns:")
print(f"{'='*60}")
error_cat = df[df['ERROR_CATEGORIZATION'].notna()]['ERROR_CATEGORIZATION'].value_counts()
if len(error_cat) > 0:
    print(f"  Total requests with error categorization: {error_cat.sum():,}")
    for cat, count in error_cat.head(15).items():
        print(f"  {cat:45s}: {count:6,} ({count/error_cat.sum()*100:5.2f}% of errors)")
else:
    print("  No error categorization data found")

# FAILURE_REASON patterns
print(f"\n3.3 FAILURE_REASON Patterns:")
print(f"{'='*60}")
failure_reasons = df[df['FAILURE_REASON'].notna()]['FAILURE_REASON'].value_counts()
if len(failure_reasons) > 0:
    print(f"  Total requests with failure reasons: {failure_reasons.sum():,}")
    for reason, count in failure_reasons.head(20).items():
        print(f"  {reason:50s}: {count:6,} ({count/failure_reasons.sum()*100:5.2f}% of failures)")
else:
    print("  No failure reason data found")

# Missing documents impact
print(f"\n3.4 Missing Documents Impact:")
print(f"{'='*60}")
docs_available = df['MANDATORY_DOCS_AVAILABLE'].value_counts()
print(f"  Document Availability:")
for avail, count in docs_available.items():
    print(f"    {avail}: {count:,} ({count/total_requests*100:.2f}%)")

# Success rate by document availability
if 'Yes' in docs_available.index and 'No' in docs_available.index:
    docs_yes = df[df['MANDATORY_DOCS_AVAILABLE'] == 'Yes']
    docs_no = df[df['MANDATORY_DOCS_AVAILABLE'] == 'No']

    success_with_docs = len(docs_yes[docs_yes['STATUS'] == 'Shared']) / len(docs_yes) * 100
    success_without_docs = len(docs_no[docs_no['STATUS'] == 'Shared']) / len(docs_no) * 100

    print(f"\n  Success Rate Analysis:")
    print(f"    With all mandatory docs available:    {success_with_docs:5.2f}%")
    print(f"    Without all mandatory docs:           {success_without_docs:5.2f}%")
    print(f"    Impact of missing docs:               {success_with_docs - success_without_docs:+5.2f} percentage points")

# Users attempting to share despite missing docs
credential_req = df[df['MANDATORY_DOCS_AVAILABLE'] == 'No']['CREDENTIAL_REQUEST'].value_counts()
if len(credential_req) > 0:
    print(f"\n  Users with missing docs who requested credentials:")
    for req, count in credential_req.items():
        print(f"    {req}: {count:,} ({count/len(df[df['MANDATORY_DOCS_AVAILABLE'] == 'No'])*100:.2f}%)")

# ============================================================================
# SECTION 4: SERVICE PROVIDER ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("4. SERVICE PROVIDER (SP) ANALYSIS")
print("="*80)

# Top SPs by volume
print(f"\n4.1 Top 10 Service Providers by Volume:")
print(f"{'='*60}")
top_sps = df['ALIAS_NAME'].value_counts().head(10)
for rank, (sp, count) in enumerate(top_sps.items(), 1):
    print(f"  {rank:2d}. {sp:35s}: {count:7,} ({count/total_requests*100:5.2f}%)")

# Success rate by SP (top 20 by volume)
print(f"\n4.2 Success Rate by Top 20 Service Providers:")
print(f"{'='*60}")
top_20_sps = df['ALIAS_NAME'].value_counts().head(20).index

sp_success_rates = []
for sp in top_20_sps:
    sp_df = df[df['ALIAS_NAME'] == sp]
    total_sp = len(sp_df)
    shared_sp = len(sp_df[sp_df['STATUS'] == 'Shared'])
    success_rate = shared_sp / total_sp * 100 if total_sp > 0 else 0
    sp_success_rates.append({
        'SP': sp,
        'Total': total_sp,
        'Shared': shared_sp,
        'Success_Rate': success_rate
    })

sp_success_df = pd.DataFrame(sp_success_rates).sort_values('Success_Rate', ascending=False)
print(f"\n  Sorted by Success Rate:")
for idx, row in sp_success_df.iterrows():
    print(f"  {row['SP']:35s}: {row['Success_Rate']:5.1f}% ({row['Shared']:,}/{row['Total']:,})")

# Most requested document types
print(f"\n4.3 Most Requested Document Types:")
print(f"{'='*60}")
# Split comma-separated document names
all_docs = []
for docs in df['REQUIRED_DOC_NAMES'].dropna():
    all_docs.extend([doc.strip() for doc in str(docs).split(',')])

doc_counts = pd.Series(all_docs).value_counts().head(15)
for doc, count in doc_counts.items():
    print(f"  {doc:40s}: {count:7,} requests")

# ============================================================================
# SECTION 5: VERSION ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("5. APP VERSION ANALYSIS")
print("="*80)

# Version distribution
print(f"\n5.1 Version Distribution:")
print(f"{'='*60}")
version_counts = df['APP_RELEASE'].value_counts()
for version, count in version_counts.head(15).items():
    print(f"  {str(version):15s}: {count:7,} ({count/df['APP_RELEASE'].notna().sum()*100:5.2f}%)")

# Success rate by version (for major versions)
print(f"\n5.2 Success Rate by Version (Top 10 by volume):")
print(f"{'='*60}")
top_versions = df['APP_RELEASE'].value_counts().head(10).index

version_success = []
for version in top_versions:
    ver_df = df[df['APP_RELEASE'] == version]
    total_ver = len(ver_df)
    shared_ver = len(ver_df[ver_df['STATUS'] == 'Shared'])
    success_rate = shared_ver / total_ver * 100 if total_ver > 0 else 0
    version_success.append({
        'Version': version,
        'Total': total_ver,
        'Shared': shared_ver,
        'Success_Rate': success_rate
    })

version_success_df = pd.DataFrame(version_success).sort_values('Version')
for idx, row in version_success_df.iterrows():
    print(f"  {str(row['Version']):15s}: {row['Success_Rate']:5.2f}% ({row['Shared']:,}/{row['Total']:,})")

# Focus on 6.4.x versions
print(f"\n5.3 Version 6.4.x Family Analysis:")
print(f"{'='*60}")
v64_versions = ['6.4.0', '6.4.1', '6.4.2', '6.4.3', '6.4.4', '6.4.5']
for version in v64_versions:
    ver_df = df[df['APP_RELEASE'] == version]
    if len(ver_df) > 0:
        total_ver = len(ver_df)
        shared_ver = len(ver_df[ver_df['STATUS'] == 'Shared'])
        success_rate = shared_ver / total_ver * 100
        print(f"  {version:10s}: {success_rate:5.2f}% ({shared_ver:,}/{total_ver:,})")

# ============================================================================
# SECTION 6: TIME-BASED TRENDS
# ============================================================================
print("\n" + "="*80)
print("6. TIME-BASED TRENDS")
print("="*80)

# Weekly success rate trend
print(f"\n6.1 Weekly Success Rate Trend:")
print(f"{'='*60}")
df['Week'] = df['CREATED_AT'].dt.to_period('W')
weekly_stats = df.groupby('Week').agg({
    'STATUS': lambda x: (x == 'Shared').sum(),
    'CREATED_AT': 'count'
}).rename(columns={'CREATED_AT': 'Total', 'STATUS': 'Shared'})
weekly_stats['Success_Rate'] = weekly_stats['Shared'] / weekly_stats['Total'] * 100

print(f"\n  {'Week':12s}  {'Total':>8s}  {'Shared':>8s}  {'Success %':>10s}")
print(f"  {'-'*45}")
for week, row in weekly_stats.iterrows():
    print(f"  {str(week):12s}  {row['Total']:8,.0f}  {row['Shared']:8,.0f}  {row['Success_Rate']:9.2f}%")

# Day of week analysis
print(f"\n6.2 Day of Week Analysis:")
print(f"{'='*60}")
df['DayOfWeek'] = df['CREATED_AT'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

day_stats = df.groupby('DayOfWeek').agg({
    'STATUS': lambda x: (x == 'Shared').sum(),
    'CREATED_AT': 'count'
}).rename(columns={'CREATED_AT': 'Total', 'STATUS': 'Shared'})
day_stats['Success_Rate'] = day_stats['Shared'] / day_stats['Total'] * 100

# Reorder by day of week
day_stats = day_stats.reindex([d for d in day_order if d in day_stats.index])

print(f"\n  {'Day':12s}  {'Total':>8s}  {'Shared':>8s}  {'Success %':>10s}")
print(f"  {'-'*45}")
for day, row in day_stats.iterrows():
    print(f"  {day:12s}  {row['Total']:8,.0f}  {row['Shared']:8,.0f}  {row['Success_Rate']:9.2f}%")

# Hour of day analysis (if time component exists)
df['Hour'] = df['CREATED_AT'].dt.hour
hour_stats = df.groupby('Hour').agg({
    'STATUS': lambda x: (x == 'Shared').sum(),
    'CREATED_AT': 'count'
}).rename(columns={'CREATED_AT': 'Total', 'STATUS': 'Shared'})
hour_stats['Success_Rate'] = hour_stats['Shared'] / hour_stats['Total'] * 100

print(f"\n6.3 Hour of Day Analysis (Top/Bottom 5 hours):")
print(f"{'='*60}")
hour_stats_sorted = hour_stats.sort_values('Success_Rate', ascending=False)
print(f"\n  Top 5 Hours (by success rate):")
print(f"  {'Hour':6s}  {'Total':>8s}  {'Shared':>8s}  {'Success %':>10s}")
for hour, row in hour_stats_sorted.head(5).iterrows():
    print(f"  {hour:02d}:00  {row['Total']:8,.0f}  {row['Shared']:8,.0f}  {row['Success_Rate']:9.2f}%")

print(f"\n  Bottom 5 Hours (by success rate):")
print(f"  {'Hour':6s}  {'Total':>8s}  {'Shared':>8s}  {'Success %':>10s}")
for hour, row in hour_stats_sorted.tail(5).iterrows():
    print(f"  {hour:02d}:00  {row['Total']:8,.0f}  {row['Shared']:8,.0f}  {row['Success_Rate']:9.2f}%")

# ============================================================================
# SECTION 7: MISSING DOCUMENTS IMPACT
# ============================================================================
print("\n" + "="*80)
print("7. MISSING DOCUMENTS DETAILED IMPACT ANALYSIS")
print("="*80)

# Overall missing docs percentage
missing_docs_count = len(df[df['MANDATORY_DOCS_AVAILABLE'] == 'No'])
print(f"\n7.1 Overall Missing Documents:")
print(f"  Requests with missing mandatory docs: {missing_docs_count:,} ({missing_docs_count/total_requests*100:.2f}%)")

# Credential request behavior
print(f"\n7.2 Credential Request Behavior (Users with Missing Docs):")
missing_docs_df = df[df['MANDATORY_DOCS_AVAILABLE'] == 'No']
cred_req_counts = missing_docs_df['CREDENTIAL_REQUEST'].value_counts()
print(f"  Total with missing docs: {len(missing_docs_df):,}")
for status, count in cred_req_counts.items():
    print(f"    {status}: {count:,} ({count/len(missing_docs_df)*100:.2f}%)")

# Completion rate for "request missing docs then share" journey
requested_docs = missing_docs_df[missing_docs_df['CREDENTIAL_REQUEST'] == 'Yes']
if len(requested_docs) > 0:
    requested_and_shared = len(requested_docs[requested_docs['STATUS'] == 'Shared'])
    print(f"\n7.3 'Request Missing Docs Then Share' Journey:")
    print(f"  Users who requested missing docs: {len(requested_docs):,}")
    print(f"  Successfully shared after request: {requested_and_shared:,} ({requested_and_shared/len(requested_docs)*100:.2f}%)")

    # Credential status for those who requested
    cred_status = requested_docs['CREDENTIAL_STATUS'].value_counts()
    print(f"\n  Credential Request Status:")
    for status, count in cred_status.items():
        print(f"    {status}: {count:,} ({count/len(requested_docs)*100:.2f}%)")

# Final STATUS for users with missing docs
print(f"\n7.4 Final STATUS for Users with Missing Mandatory Docs:")
missing_docs_status = missing_docs_df['STATUS'].value_counts()
for status, count in missing_docs_status.items():
    print(f"  {status:25s}: {count:6,} ({count/len(missing_docs_df)*100:5.2f}%)")

# ============================================================================
# SECTION 8: NOTIFICATION EFFECTIVENESS
# ============================================================================
print("\n" + "="*80)
print("8. NOTIFICATION EFFECTIVENESS")
print("="*80)

# VIZ_TYPE analysis
print(f"\n8.1 Notification Type (VIZ_TYPE) Analysis:")
print(f"{'='*60}")
viz_type_counts = df['VIZ_TYPE'].value_counts()
for viz_type, count in viz_type_counts.items():
    print(f"  {viz_type}: {count:,} ({count/total_requests*100:.2f}%)")

# Success rate by VIZ_TYPE
print(f"\n8.2 Success Rate by Notification Type:")
for viz_type in viz_type_counts.index:
    viz_df = df[df['VIZ_TYPE'] == viz_type]
    success = len(viz_df[viz_df['STATUS'] == 'Shared'])
    success_rate = success / len(viz_df) * 100
    print(f"  {viz_type:10s}: {success_rate:5.2f}% ({success:,}/{len(viz_df):,})")

# Notification read rate
print(f"\n8.3 Notification Read Rate:")
print(f"{'='*60}")
notif_state_counts = df['NOTIFICATION_STATE'].value_counts()
total_with_state = df['NOTIFICATION_STATE'].notna().sum()
print(f"  Total with notification state: {total_with_state:,}")
for state, count in notif_state_counts.items():
    print(f"    {state}: {count:,} ({count/total_with_state*100:.2f}%)")

# Success rate by notification state
print(f"\n8.4 Success Rate by Notification State:")
for state in notif_state_counts.index:
    state_df = df[df['NOTIFICATION_STATE'] == state]
    success = len(state_df[state_df['STATUS'] == 'Shared'])
    success_rate = success / len(state_df) * 100
    print(f"  {state:20s}: {success_rate:5.2f}% ({success:,}/{len(state_df):,})")

# ============================================================================
# SECTION 9: NEW FIELDS ANALYSIS (DataNewFields sheet)
# ============================================================================
print("\n" + "="*80)
print("9. NEW FIELDS ANALYSIS - User Lifecycle Tracking")
print("="*80)

print(f"\n9.1 First Read vs Current State - Document Availability:")
print(f"{'='*60}")

# Note: Column names in df_new have leading spaces, need to strip
df_new.columns = df_new.columns.str.strip()

if 'FIRST_READ_MANDATORY_DOCS_AVAILABLE' in df_new.columns:
    # Cross-tabulation of first read vs current state
    crosstab = pd.crosstab(
        df_new['FIRST_READ_MANDATORY_DOCS_AVAILABLE'],
        df_new['MANDATORY_DOCS_AVAILABLE'],
        margins=True
    )
    print(f"\n  First Read Availability vs Current Availability:")
    print(crosstab)

    # Users who acquired docs after first read
    acquired_docs = len(df_new[
        (df_new['FIRST_READ_MANDATORY_DOCS_AVAILABLE'] == 'No') &
        (df_new['MANDATORY_DOCS_AVAILABLE'] == 'Yes')
    ])
    total_first_read_no = len(df_new[df_new['FIRST_READ_MANDATORY_DOCS_AVAILABLE'] == 'No'])

    if total_first_read_no > 0:
        print(f"\n  Users who acquired missing docs after first read:")
        print(f"    Count: {acquired_docs:,}")
        print(f"    Rate: {acquired_docs/total_first_read_no*100:.2f}% of users who initially lacked docs")

if 'FIRST_READ_MANDATORY_DOCS_FULFILLED' in df_new.columns:
    print(f"\n9.2 First Read vs Current State - Document Fulfillment:")
    print(f"{'='*60}")

    crosstab_fulfilled = pd.crosstab(
        df_new['FIRST_READ_MANDATORY_DOCS_FULFILLED'],
        df_new['MANDATORY_DOCS_FULFILLED'],
        margins=True
    )
    print(f"\n  First Read Fulfillment vs Current Fulfillment:")
    print(crosstab_fulfilled)

# Success rate comparison for new fields dataset
print(f"\n9.3 Success Rate in New Fields Dataset (Recent Data):")
print(f"{'='*60}")
total_new = len(df_new)
shared_new = len(df_new[df_new['STATUS'] == 'Shared'])
print(f"  Total requests: {total_new:,}")
print(f"  Successfully shared: {shared_new:,} ({shared_new/total_new*100:.2f}%)")
print(f"  Comparison to overall dataset: {shared/total_requests*100:.2f}%")

# ============================================================================
# SECTION 10: EXECUTIVE SUMMARY & KEY INSIGHTS
# ============================================================================
print("\n" + "="*80)
print("10. EXECUTIVE SUMMARY - TOP INSIGHTS")
print("="*80)

print(f"""
KEY FINDING #1: LOW END-TO-END SUCCESS RATE
  - Only {shared/total_requests*100:.2f}% of sharing requests successfully complete
  - Primary drop-off point: Notification opened → Consent given
  - {(1-shared/total_requests)*100:.1f}% of requests fail to complete

KEY FINDING #2: NOTIFICATION ENGAGEMENT CHALLENGE
  - {notification_opened/total_requests*100:.1f}% of requests are opened (read)
  - {(1-notification_opened/total_requests)*100:.1f}% drop-off at notification stage
  - Maps to FP1.1-1.4 in journey document (notification delivery/engagement failures)

KEY FINDING #3: MISSING DOCUMENTS MAJOR BARRIER
  - {missing_docs_count/total_requests*100:.1f}% of requests involve missing mandatory documents
  - Success rate WITH docs: {success_with_docs:.2f}%
  - Success rate WITHOUT docs: {success_without_docs:.2f}%
  - Impact: {success_with_docs - success_without_docs:+.1f} percentage points
  - Maps to FP3.1-3.5 in journey document

KEY FINDING #4: VERSION PERFORMANCE (requires detailed analysis in next section)
  - Multiple app versions in use (6.1.x - 6.4.x)
  - Version-specific success rates vary
  - Opportunity for version-based optimization

KEY FINDING #5: SERVICE PROVIDER INTEGRATION QUALITY VARIES
  - Top SP: {top_sps.index[0]} ({top_sps.iloc[0]:,} requests)
  - SP success rates range widely
  - Some SPs have integration issues requiring attention
""")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\nNext steps:")
print(f"  1. Review detailed findings above")
print(f"  2. Cross-reference with document_sharing_request_journey.md failure points")
print(f"  3. Prioritize fixes based on impact x volume")
print(f"  4. Create targeted improvements for low-performing SPs and versions")
