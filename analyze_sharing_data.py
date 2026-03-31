"""
UAE PASS Digital Documents - Sharing Request Performance Analysis
Analyzes csvdata-2.csv to extract insights on document sharing funnel and failure patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import sys

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

warnings.filterwarnings('ignore')

# Read the CSV file
print("Loading data from csvdata-2.csv...")
df = pd.read_csv(r'D:\cluade\csvdata-2.csv')

# Strip whitespace from column names
df.columns = df.columns.str.strip()

print(f"Total rows loaded: {len(df):,}")
print(f"Date range: {df['CREATED_AT'].min()} to {df['CREATED_AT'].max()}")
print("\n" + "="*80 + "\n")

# Note: The COUNT column appears to represent aggregated counts of identical records
# We need to expand this for accurate calculations
print("Expanding aggregated records based on COUNT column...")
df_expanded = df.loc[df.index.repeat(df['COUNT'])].reset_index(drop=True)
print(f"Total individual sharing requests (expanded): {len(df_expanded):,}")
print("\n" + "="*80 + "\n")

# ============================================================================
# 1. FUNNEL ANALYSIS
# ============================================================================
print("="*80)
print("1. FUNNEL ANALYSIS - Drop-off at Each Stage")
print("="*80 + "\n")

total_requests = len(df_expanded)

# Stage 1: Notification Delivered -> Notification Opened (Read)
notif_delivered = total_requests
notif_read = len(df_expanded[df_expanded['NOTIFICATION_STATE'] == 'Read'])
notif_unread = len(df_expanded[df_expanded['NOTIFICATION_STATE'].isna()])
notif_rejected_at_notif = len(df_expanded[df_expanded['NOTIFICATION_STATE'] == 'Rejected'])

print(f"Stage 1: Notification Delivered -> Opened")
print(f"  Notifications delivered: {notif_delivered:,}")
print(f"  Notifications read: {notif_read:,} ({notif_read/notif_delivered*100:.2f}%)")
print(f"  Notifications unread: {notif_unread:,} ({notif_unread/notif_delivered*100:.2f}%)")
print(f"  Rejected at notification: {notif_rejected_at_notif:,} ({notif_rejected_at_notif/notif_delivered*100:.2f}%)")
print(f"  DROP-OFF: {(notif_delivered - notif_read)/notif_delivered*100:.2f}%\n")

# Stage 2: Request Opened -> Consent Given
opened_requests = notif_read
consent_given = len(df_expanded[(df_expanded['NOTIFICATION_STATE'] == 'Read') &
                                 (df_expanded['CONSENT_GIVEN'] == 'Yes')])

print(f"Stage 2: Request Opened -> Consent Given")
print(f"  Requests opened (read): {opened_requests:,}")
print(f"  Consent given: {consent_given:,} ({consent_given/opened_requests*100:.2f}%)")
print(f"  DROP-OFF: {(opened_requests - consent_given)/opened_requests*100:.2f}%\n")

# Stage 3: Consent Given -> PIN Entered
pin_given = len(df_expanded[(df_expanded['CONSENT_GIVEN'] == 'Yes') &
                             (df_expanded['PIN_GIVEN'] == 'Yes')])

print(f"Stage 3: Consent Given -> PIN Entered")
print(f"  Consent given: {consent_given:,}")
print(f"  PIN entered: {pin_given:,} ({pin_given/consent_given*100:.2f}%)")
print(f"  DROP-OFF: {(consent_given - pin_given)/consent_given*100:.2f}%\n")

# Stage 4: PIN Entered -> Sharing Completed
shared_success = len(df_expanded[(df_expanded['PIN_GIVEN'] == 'Yes') &
                                  (df_expanded['STATUS'] == 'Shared')])

print(f"Stage 4: PIN Entered -> Sharing Completed")
print(f"  PIN entered: {pin_given:,}")
print(f"  Successfully shared: {shared_success:,} ({shared_success/pin_given*100:.2f}%)")
print(f"  DROP-OFF: {(pin_given - shared_success)/pin_given*100:.2f}%\n")

# Overall End-to-End Success Rate
print(f"{'='*40}")
print(f"OVERALL END-TO-END SUCCESS RATE")
print(f"{'='*40}")
print(f"Total requests: {total_requests:,}")
print(f"Successfully shared: {shared_success:,}")
print(f"SUCCESS RATE: {shared_success/total_requests*100:.2f}%")
print(f"FAILURE RATE: {(total_requests - shared_success)/total_requests*100:.2f}%")
print("\n" + "="*80 + "\n")

# ============================================================================
# 2. FAILURE POINT ANALYSIS
# ============================================================================
print("="*80)
print("2. FAILURE POINT ANALYSIS")
print("="*80 + "\n")

# STATUS breakdown
print("Status Breakdown:")
print("-" * 60)
status_counts = df_expanded['STATUS'].value_counts()
for status, count in status_counts.items():
    print(f"  {status:.<40} {count:>10,} ({count/total_requests*100:>6.2f}%)")
print(f"  {'TOTAL':.<40} {total_requests:>10,} ({100:>6.2f}%)")
print()

# ERROR_CATEGORIZATION breakdown (for failed requests)
print("Error Categorization (for failed/error states):")
print("-" * 60)
error_data = df_expanded[df_expanded['ERROR_CATEGORIZATION'].notna()]
if len(error_data) > 0:
    error_counts = error_data['ERROR_CATEGORIZATION'].value_counts()
    for error, count in error_counts.items():
        print(f"  {error:.<40} {count:>10,} ({count/len(error_data)*100:>6.2f}%)")
    print(f"  {'TOTAL ERRORS':.<40} {len(error_data):>10,} ({100:>6.2f}%)")
else:
    print("  No error categorization data found")
print()

# FAILURE_REASON breakdown
print("Failure Reasons (top 10):")
print("-" * 60)
failure_data = df_expanded[df_expanded['FAILURE_REASON'].notna()]
if len(failure_data) > 0:
    failure_counts = failure_data['FAILURE_REASON'].value_counts().head(10)
    for reason, count in failure_counts.items():
        print(f"  {str(reason)[:50]:.<52} {count:>8,} ({count/len(failure_data)*100:>6.2f}%)")
    print(f"  {'TOTAL WITH FAILURE REASONS':.<52} {len(failure_data):>8,}")
else:
    print("  No failure reason data found")
print()

# Missing documents impact
print("Missing Documents Impact:")
print("-" * 60)
missing_docs = len(df_expanded[df_expanded['MANDATORY_DOCS_AVAILABLE'] == 'No'])
has_docs = len(df_expanded[df_expanded['MANDATORY_DOCS_AVAILABLE'] == 'Yes'])

print(f"  Requests with missing mandatory docs: {missing_docs:,} ({missing_docs/total_requests*100:.2f}%)")
print(f"  Requests with all docs available: {has_docs:,} ({has_docs/total_requests*100:.2f}%)")

# Success rate comparison
missing_docs_shared = len(df_expanded[(df_expanded['MANDATORY_DOCS_AVAILABLE'] == 'No') &
                                       (df_expanded['STATUS'] == 'Shared')])
has_docs_shared = len(df_expanded[(df_expanded['MANDATORY_DOCS_AVAILABLE'] == 'Yes') &
                                   (df_expanded['STATUS'] == 'Shared')])

print(f"\n  Success rate when docs missing: {missing_docs_shared/missing_docs*100 if missing_docs > 0 else 0:.2f}%")
print(f"  Success rate when docs available: {has_docs_shared/has_docs*100 if has_docs > 0 else 0:.2f}%")

# Users who attempt to request missing docs
attempted_request = len(df_expanded[(df_expanded['MANDATORY_DOCS_AVAILABLE'] == 'No') &
                                     (df_expanded['CREDENTIAL_REQUEST'] == 'Yes')])
print(f"\n  Users with missing docs who attempted credential request: {attempted_request:,} ({attempted_request/missing_docs*100 if missing_docs > 0 else 0:.2f}%)")

# Completion rate for request-then-share journeys
request_then_share = len(df_expanded[(df_expanded['CREDENTIAL_REQUEST'] == 'Yes') &
                                      (df_expanded['CREDENTIAL_STATUS'] == 'Success') &
                                      (df_expanded['STATUS'] == 'Shared')])
total_credential_requests = len(df_expanded[df_expanded['CREDENTIAL_REQUEST'] == 'Yes'])
print(f"  Request-then-share completion rate: {request_then_share/total_credential_requests*100 if total_credential_requests > 0 else 0:.2f}% ({request_then_share:,}/{total_credential_requests:,})")

print("\n" + "="*80 + "\n")

# ============================================================================
# 3. SERVICE PROVIDER ANALYSIS
# ============================================================================
print("="*80)
print("3. SERVICE PROVIDER ANALYSIS")
print("="*80 + "\n")

# Top 10 SPs by volume
print("Top 10 Service Providers by Volume:")
print("-" * 60)
sp_counts = df_expanded['ALIAS_NAME'].value_counts().head(10)
for sp, count in sp_counts.items():
    print(f"  {sp:.<40} {count:>10,} ({count/total_requests*100:>6.2f}%)")
print()

# Success rate by SP (top 10 by volume)
print("Success Rate by Service Provider (Top 10 by volume):")
print("-" * 60)
print(f"{'Service Provider':<35} {'Total':>10} {'Shared':>10} {'Success %':>12}")
print("-" * 60)

for sp in sp_counts.head(10).index:
    sp_total = len(df_expanded[df_expanded['ALIAS_NAME'] == sp])
    sp_shared = len(df_expanded[(df_expanded['ALIAS_NAME'] == sp) &
                                 (df_expanded['STATUS'] == 'Shared')])
    sp_success_rate = sp_shared/sp_total*100 if sp_total > 0 else 0
    print(f"{sp[:34]:<35} {sp_total:>10,} {sp_shared:>10,} {sp_success_rate:>11.2f}%")
print()

# Most requested document types
print("Most Requested Document Combinations (Top 10):")
print("-" * 60)
doc_counts = df_expanded['REQUIRED_DOC_NAMES'].value_counts().head(10)
for docs, count in doc_counts.items():
    print(f"  {str(docs)[:50]:.<52} {count:>8,} ({count/total_requests*100:>6.2f}%)")

print("\n" + "="*80 + "\n")

# ============================================================================
# 4. VERSION ANALYSIS
# ============================================================================
print("="*80)
print("4. APP VERSION ANALYSIS")
print("="*80 + "\n")

# Version distribution
print("Version Distribution (Top 10):")
print("-" * 60)
version_counts = df_expanded['APP_RELEASE'].value_counts().head(10)
for version, count in version_counts.items():
    print(f"  {str(version):.<20} {count:>10,} ({count/total_requests*100:>6.2f}%)")
print()

# Success rate by version (focus on 6.4.x)
print("Success Rate by App Version (6.4.x and others):")
print("-" * 60)
print(f"{'Version':<15} {'Total':>10} {'Shared':>10} {'Failed':>10} {'Success %':>12}")
print("-" * 60)

# Group versions
versions_of_interest = ['6.4.0', '6.4.1', '6.4.2', '6.3.0', '6.2.2', '6.2.1', '6.2.0', '6.1.3']

for version in versions_of_interest:
    v_total = len(df_expanded[df_expanded['APP_RELEASE'] == version])
    if v_total > 0:
        v_shared = len(df_expanded[(df_expanded['APP_RELEASE'] == version) &
                                    (df_expanded['STATUS'] == 'Shared')])
        v_failed = len(df_expanded[(df_expanded['APP_RELEASE'] == version) &
                                    (df_expanded['STATUS'] == 'Failed')])
        v_success_rate = v_shared/v_total*100
        print(f"{version:<15} {v_total:>10,} {v_shared:>10,} {v_failed:>10,} {v_success_rate:>11.2f}%")

# Compare 6.4.x vs pre-6.4
v64_total = len(df_expanded[df_expanded['APP_RELEASE'].isin(['6.4.0', '6.4.1', '6.4.2'])])
v64_shared = len(df_expanded[(df_expanded['APP_RELEASE'].isin(['6.4.0', '6.4.1', '6.4.2'])) &
                              (df_expanded['STATUS'] == 'Shared')])

pre64_total = len(df_expanded[~df_expanded['APP_RELEASE'].isin(['6.4.0', '6.4.1', '6.4.2']) &
                               df_expanded['APP_RELEASE'].notna()])
pre64_shared = len(df_expanded[~df_expanded['APP_RELEASE'].isin(['6.4.0', '6.4.1', '6.4.2']) &
                                df_expanded['APP_RELEASE'].notna() &
                                (df_expanded['STATUS'] == 'Shared')])

print("-" * 60)
print(f"{'6.4.x combined':<15} {v64_total:>10,} {v64_shared:>10,} {'':>10} {v64_shared/v64_total*100:>11.2f}%")
print(f"{'Pre-6.4':<15} {pre64_total:>10,} {pre64_shared:>10,} {'':>10} {pre64_shared/pre64_total*100 if pre64_total > 0 else 0:>11.2f}%")

print("\n" + "="*80 + "\n")

# ============================================================================
# 5. TIME-BASED TRENDS
# ============================================================================
print("="*80)
print("5. TIME-BASED TRENDS")
print("="*80 + "\n")

# Convert date column
df_expanded['date'] = pd.to_datetime(df_expanded['CREATED_AT'], format='%d-%b-%y')
df_expanded['week'] = df_expanded['date'].dt.isocalendar().week
df_expanded['day_of_week'] = df_expanded['date'].dt.day_name()
df_expanded['month'] = df_expanded['date'].dt.to_period('M')

# Weekly success rate trend
print("Weekly Success Rate Trend:")
print("-" * 80)
print(f"{'Week Starting':<20} {'Total':>10} {'Shared':>10} {'Failed':>10} {'Success %':>12}")
print("-" * 80)

weekly_data = df_expanded.groupby(df_expanded['date'].dt.to_period('W')).agg({
    'STATUS': ['count', lambda x: (x == 'Shared').sum(), lambda x: (x == 'Failed').sum()]
}).reset_index()

for idx, row in weekly_data.head(20).iterrows():
    week = row['date']
    total = row[('STATUS', 'count')]
    shared = row[('STATUS', '<lambda_0>')]
    failed = row[('STATUS', '<lambda_1>')]
    success_rate = shared/total*100 if total > 0 else 0
    print(f"{str(week):<20} {total:>10,} {shared:>10,} {failed:>10,} {success_rate:>11.2f}%")

print()

# Day of week patterns
print("Day of Week Patterns:")
print("-" * 60)
print(f"{'Day':<15} {'Total':>10} {'Shared':>10} {'Success %':>12}")
print("-" * 60)

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for day in day_order:
    day_total = len(df_expanded[df_expanded['day_of_week'] == day])
    if day_total > 0:
        day_shared = len(df_expanded[(df_expanded['day_of_week'] == day) &
                                      (df_expanded['STATUS'] == 'Shared')])
        day_success = day_shared/day_total*100
        print(f"{day:<15} {day_total:>10,} {day_shared:>10,} {day_success:>11.2f}%")

print("\n" + "="*80 + "\n")

# ============================================================================
# 6. NOTIFICATION EFFECTIVENESS
# ============================================================================
print("="*80)
print("6. NOTIFICATION EFFECTIVENESS")
print("="*80 + "\n")

# Push vs Pull
print("Push vs Pull Notification Success Rates:")
print("-" * 60)
print(f"{'Type':<15} {'Total':>10} {'Read':>10} {'Shared':>10} {'Read %':>10} {'Success %':>12}")
print("-" * 60)

for viz_type in ['Push', 'Pull']:
    vt_total = len(df_expanded[df_expanded['VIZ_TYPE'] == viz_type])
    if vt_total > 0:
        vt_read = len(df_expanded[(df_expanded['VIZ_TYPE'] == viz_type) &
                                   (df_expanded['NOTIFICATION_STATE'] == 'Read')])
        vt_shared = len(df_expanded[(df_expanded['VIZ_TYPE'] == viz_type) &
                                     (df_expanded['STATUS'] == 'Shared')])
        vt_read_rate = vt_read/vt_total*100
        vt_success_rate = vt_shared/vt_total*100
        print(f"{viz_type:<15} {vt_total:>10,} {vt_read:>10,} {vt_shared:>10,} {vt_read_rate:>9.2f}% {vt_success_rate:>11.2f}%")

print()

# Notification state breakdown
print("Notification State Breakdown:")
print("-" * 60)
notif_states = df_expanded['NOTIFICATION_STATE'].value_counts()
for state, count in notif_states.items():
    print(f"  {str(state):.<30} {count:>10,} ({count/total_requests*100:>6.2f}%)")
missing_state = df_expanded['NOTIFICATION_STATE'].isna().sum()
print(f"  {'No state (unread)':.<30} {missing_state:>10,} ({missing_state/total_requests*100:>6.2f}%)")

print("\n" + "="*80 + "\n")

# ============================================================================
# 7. DEVICE & PLATFORM ANALYSIS
# ============================================================================
print("="*80)
print("7. DEVICE & PLATFORM ANALYSIS")
print("="*80 + "\n")

# Platform success rates
print("Platform Success Rates:")
print("-" * 60)
print(f"{'Platform':<15} {'Total':>10} {'Shared':>10} {'Failed':>10} {'Success %':>12}")
print("-" * 60)

for platform in ['Android', 'IOS', 'iOS']:
    p_total = len(df_expanded[df_expanded['USER_AGENT'] == platform])
    if p_total > 0:
        p_shared = len(df_expanded[(df_expanded['USER_AGENT'] == platform) &
                                    (df_expanded['STATUS'] == 'Shared')])
        p_failed = len(df_expanded[(df_expanded['USER_AGENT'] == platform) &
                                    (df_expanded['STATUS'] == 'Failed')])
        p_success = p_shared/p_total*100
        print(f"{platform:<15} {p_total:>10,} {p_shared:>10,} {p_failed:>10,} {p_success:>11.2f}%")

missing_platform = len(df_expanded[df_expanded['USER_AGENT'].isna()])
print(f"{'Unknown':<15} {missing_platform:>10,} {'':>10} {'':>10} {'':>12}")

print("\n" + "="*80 + "\n")

# ============================================================================
# 8. CROSS-REFERENCE WITH FAILURE POINTS
# ============================================================================
print("="*80)
print("8. FAILURE POINT MAPPING (Cross-reference with Journey Document)")
print("="*80 + "\n")

print("FP1.1-1.2: Notification not received/missed:")
print(f"  Unread notifications: {missing_state:,} ({missing_state/total_requests*100:.2f}%)")
print()

print("FP1.5: Duplicate correlation ID:")
print("  [Cannot measure from this dataset - requires SP request logs]")
print()

print("FP2.x: Request details screen failures:")
print(f"  Read but no action taken: {len(df_expanded[(df_expanded['NOTIFICATION_STATE'] == 'Read') & (df_expanded['STATUS'] == 'No Action Taken')]):,}")
print()

print("FP3.x: Missing documents:")
print(f"  Total requests with missing docs: {missing_docs:,} ({missing_docs/total_requests*100:.2f}%)")
print(f"  Attempted to request docs: {attempted_request:,} ({attempted_request/missing_docs*100 if missing_docs > 0 else 0:.2f}%)")
print(f"  Request-then-share success: {request_then_share:,}")
print()

print("FP4.x: Consent failures:")
print(f"  Read but did not give consent: {len(df_expanded[(df_expanded['NOTIFICATION_STATE'] == 'Read') & (df_expanded['CONSENT_GIVEN'] != 'Yes')]):,}")
print()

print("FP5.x: PIN entry failures:")
print(f"  Consent given but PIN not entered: {len(df_expanded[(df_expanded['CONSENT_GIVEN'] == 'Yes') & (df_expanded['PIN_GIVEN'] != 'Yes')]):,}")
print()

print("FP6.x-FP8.x: Sharing completion failures:")
failed_before_pin = len(df_expanded[df_expanded['ERROR_CATEGORIZATION'] == 'Failed before PIN page'])
failed_after_pin = len(df_expanded[df_expanded['ERROR_CATEGORIZATION'] == 'Failed after PIN page'])
print(f"  Failed before PIN page: {failed_before_pin:,}")
print(f"  Failed after PIN page: {failed_after_pin:,}")
print()

print("="*80)
print("\nAnalysis complete. Results saved to console.")
print("="*80)
