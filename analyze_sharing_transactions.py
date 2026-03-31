import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import sys

# Set stdout encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Load the dataset
df = pd.read_csv(r'D:\cluade\sharing_transactions_sample.csv')

print("="*80)
print("SHARING TRANSACTIONS ANALYSIS REPORT")
print("="*80)
print(f"\nDataset Overview: {len(df):,} total status records")
print(f"Unique Requests: {df['request_id'].nunique():,}")
print(f"Date Range: {df['status_ts'].min()} to {df['status_ts'].max()}")
print(f"\nChannels: {', '.join(df['channel'].unique())}")
print(f"Platforms: {', '.join(df['platform'].unique())}")
print(f"Service Providers: {', '.join(df['sp_id'].unique())}")

# Parse timestamps
df['status_ts'] = pd.to_datetime(df['status_ts'])

# Get terminal status for each request
terminal_statuses = ['S40', 'S41', 'S42', 'S43', 'S44']
request_terminal = df[df['status_code'].isin(terminal_statuses)].groupby('request_id').agg({
    'status_code': 'first',
    'status_ts': 'first'
}).rename(columns={'status_code': 'terminal_status', 'status_ts': 'terminal_ts'})

# Get first status for each request
request_start = df[df['status_code'] == 'S00'].groupby('request_id').agg({
    'status_ts': 'first',
    'sp_id': 'first',
    'channel': 'first',
    'platform': 'first',
    'required_count': 'first'
}).rename(columns={'status_ts': 'start_ts'})

# Merge to create request-level summary
request_summary = request_start.join(request_terminal, how='left')
request_summary['completed'] = ~request_summary['terminal_status'].isna()
request_summary['journey_time_sec'] = (request_summary['terminal_ts'] - request_summary['start_ts']).dt.total_seconds()

print(f"\n{'='*80}")
print("1. FUNNEL ANALYSIS BY CHANNEL")
print(f"{'='*80}")

# Channel-level funnel
for channel in df['channel'].unique():
    channel_df = df[df['channel'] == channel]
    channel_requests = request_summary[request_summary['channel'] == channel]
    total_requests = channel_requests.shape[0]

    print(f"\n{channel.upper()} CHANNEL (n={total_requests:,} requests)")
    print("-" * 60)

    # Define funnel steps per channel
    if channel == 'notification':
        funnel_steps = [
            ('S00', 'Request Created'),
            ('S01', 'Notification Sent'),
            ('S02', 'Notification Delivered'),
            ('S03', 'Notification Opened'),
            ('S08', 'Request Viewed'),
            ('S20', 'Awaiting Consent'),
            ('S21', 'Consent Given'),
            ('S30', 'PIN Requested'),
            ('S31', 'PIN Verified'),
            ('S40', 'Share Success')
        ]
    elif channel == 'redirect':
        funnel_steps = [
            ('S00', 'Request Created'),
            ('S04', 'Redirect Launched'),
            ('S05', 'Redirect Landed'),
            ('S08', 'Request Viewed'),
            ('S20', 'Awaiting Consent'),
            ('S21', 'Consent Given'),
            ('S30', 'PIN Requested'),
            ('S31', 'PIN Verified'),
            ('S40', 'Share Success')
        ]
    else:  # qr
        funnel_steps = [
            ('S00', 'Request Created'),
            ('S06', 'QR Rendered'),
            ('S07', 'QR Scanned'),
            ('S08', 'Request Viewed'),
            ('S20', 'Awaiting Consent'),
            ('S21', 'Consent Given'),
            ('S30', 'PIN Requested'),
            ('S31', 'PIN Verified'),
            ('S40', 'Share Success')
        ]

    # Calculate funnel
    funnel_counts = {}
    for status_code, label in funnel_steps:
        count = channel_df[channel_df['status_code'] == status_code]['request_id'].nunique()
        funnel_counts[status_code] = count
        pct_of_total = (count / total_requests * 100) if total_requests > 0 else 0

        # Calculate conversion from previous step
        prev_idx = funnel_steps.index((status_code, label)) - 1
        if prev_idx >= 0:
            prev_status = funnel_steps[prev_idx][0]
            prev_count = funnel_counts.get(prev_status, 0)
            conversion = (count / prev_count * 100) if prev_count > 0 else 0
            print(f"{label:25} {count:6,} ({pct_of_total:5.1f}% of total, {conversion:5.1f}% conversion)")
        else:
            print(f"{label:25} {count:6,} ({pct_of_total:5.1f}% of total)")

    # Drop-off analysis
    print(f"\n  DROP-OFF POINTS:")
    for i in range(len(funnel_steps) - 1):
        curr_status, curr_label = funnel_steps[i]
        next_status, next_label = funnel_steps[i+1]
        curr_count = funnel_counts.get(curr_status, 0)
        next_count = funnel_counts.get(next_status, 0)
        drop_count = curr_count - next_count
        drop_pct = (drop_count / curr_count * 100) if curr_count > 0 else 0
        if drop_pct > 5:  # Only show significant drops
            print(f"    {curr_label} → {next_label}: {drop_count:,} users ({drop_pct:.1f}%)")

print(f"\n{'='*80}")
print("2. DOCUMENT READINESS IMPACT")
print(f"{'='*80}")

# Document readiness analysis
docs_ready = df[df['status_code'] == 'S10']['request_id'].unique()
docs_missing = df[df['status_code'] == 'S11']['request_id'].unique()

print(f"\nRequests with docs READY at open: {len(docs_ready):,}")
print(f"Requests with docs MISSING at open: {len(docs_missing):,}")
print(f"Readiness rate: {len(docs_ready)/(len(docs_ready)+len(docs_missing))*100:.1f}%")

# Success rates by readiness
docs_ready_success = request_summary[request_summary.index.isin(docs_ready) & (request_summary['terminal_status'] == 'S40')].shape[0]
docs_ready_total = request_summary[request_summary.index.isin(docs_ready)].shape[0]

docs_missing_success = request_summary[request_summary.index.isin(docs_missing) & (request_summary['terminal_status'] == 'S40')].shape[0]
docs_missing_total = request_summary[request_summary.index.isin(docs_missing)].shape[0]

print(f"\nSuccess rate when docs READY: {docs_ready_success}/{docs_ready_total} = {docs_ready_success/docs_ready_total*100:.1f}%")
print(f"Success rate when docs MISSING: {docs_missing_success}/{docs_missing_total} = {docs_missing_success/docs_missing_total*100:.1f}%")
print(f"Impact: {(docs_ready_success/docs_ready_total - docs_missing_success/docs_missing_total)*100:.1f} percentage point difference")

# Missing doc request flow
print(f"\nMISSING DOC REQUEST FLOW:")
s11_requests = df[df['status_code'] == 'S11']['request_id'].nunique()
s12_requests = df[df['status_code'] == 'S12']['request_id'].nunique()
s13_requests = df[df['status_code'] == 'S13']['request_id'].nunique()
s14_requests = df[df['status_code'] == 'S14']['request_id'].nunique()
s15_requests = df[df['status_code'] == 'S15']['request_id'].nunique()

print(f"  Users with missing docs (S11): {s11_requests:,}")
print(f"  Users who initiated doc request (S12): {s12_requests:,} ({s12_requests/s11_requests*100:.1f}% initiation rate)")
print(f"  Successful doc fetch (S13): {s13_requests:,} ({s13_requests/s12_requests*100:.1f}% of attempts)")
print(f"  Technical error (S14): {s14_requests:,} ({s14_requests/s12_requests*100:.1f}% of attempts)")
print(f"  Not found at issuer (S15): {s15_requests:,} ({s15_requests/s12_requests*100:.1f}% of attempts)")

# Document type analysis
print(f"\nDOCUMENT TYPE FAILURE ANALYSIS:")
doc_types = {}
for idx, row in df[df['status_code'].isin(['S11', 'S15'])].iterrows():
    docs = str(row['required_docs']).split('|')
    status = row['status_code']
    for doc in docs:
        if doc not in doc_types:
            doc_types[doc] = {'missing': 0, 'not_found': 0}
        if status == 'S11':
            doc_types[doc]['missing'] += 1
        elif status == 'S15':
            doc_types[doc]['not_found'] += 1

for doc, counts in sorted(doc_types.items(), key=lambda x: x[1]['missing'] + x[1]['not_found'], reverse=True):
    total = counts['missing'] + counts['not_found']
    print(f"  {doc:25} Missing: {counts['missing']:4}, Not Found: {counts['not_found']:4}, Total: {total:4}")

print(f"\n{'='*80}")
print("3. USER BEHAVIOR PATTERNS")
print(f"{'='*80}")

# Consent abandonment
s20_requests = df[df['status_code'] == 'S20']['request_id'].nunique()
s21_requests = df[df['status_code'] == 'S21']['request_id'].nunique()
consent_abandonment = s20_requests - s21_requests
consent_abandonment_rate = (consent_abandonment / s20_requests * 100) if s20_requests > 0 else 0

print(f"\nCONSENT STEP:")
print(f"  Reached consent screen (S20): {s20_requests:,}")
print(f"  Gave consent (S21): {s21_requests:,}")
print(f"  Abandonment: {consent_abandonment:,} users ({consent_abandonment_rate:.1f}%)")
print(f"  Consent conversion rate: {s21_requests/s20_requests*100:.1f}%")

# PIN analysis
s30_requests = df[df['status_code'] == 'S30']['request_id'].nunique()
s31_requests = df[df['status_code'] == 'S31']['request_id'].nunique()
s32_requests = df[df['status_code'] == 'S32']['request_id'].nunique()

print(f"\nPIN STEP:")
print(f"  PIN requested (S30): {s30_requests:,}")
print(f"  PIN verified (S31): {s31_requests:,}")
print(f"  PIN failed (S32): {s32_requests:,}")
print(f"  PIN success rate: {s31_requests/(s31_requests+s32_requests)*100:.1f}%" if (s31_requests+s32_requests) > 0 else "  PIN success rate: N/A")
print(f"  PIN failure rate: {s32_requests/(s31_requests+s32_requests)*100:.1f}%" if (s31_requests+s32_requests) > 0 else "  PIN failure rate: N/A")

# Most common exit points
print(f"\nMOST COMMON EXIT POINTS (requests that don't reach terminal status):")
incomplete_requests = request_summary[~request_summary['completed']]
if len(incomplete_requests) > 0:
    # Get last status for incomplete requests
    last_status_incomplete = df[df['request_id'].isin(incomplete_requests.index)].groupby('request_id')['status_code'].last()
    exit_points = last_status_incomplete.value_counts().head(10)
    for status, count in exit_points.items():
        pct = count / len(incomplete_requests) * 100
        print(f"  {status}: {count:,} requests ({pct:.1f}% of incomplete)")
else:
    print("  All requests reached terminal status")

print(f"\n{'='*80}")
print("4. SERVICE PROVIDER PERFORMANCE")
print(f"{'='*80}")

# SP performance
sp_stats = []
for sp in request_summary['sp_id'].unique():
    sp_data = request_summary[request_summary['sp_id'] == sp]
    total = len(sp_data)
    success = (sp_data['terminal_status'] == 'S40').sum()
    tech_error = (sp_data['terminal_status'] == 'S41').sum()
    expired = (sp_data['terminal_status'] == 'S42').sum()
    aborted = (sp_data['terminal_status'] == 'S43').sum()
    not_eligible = (sp_data['terminal_status'] == 'S44').sum()

    success_rate = (success / total * 100) if total > 0 else 0
    avg_time = sp_data[sp_data['completed']]['journey_time_sec'].median()

    sp_stats.append({
        'sp_id': sp,
        'total': total,
        'success': success,
        'success_rate': success_rate,
        'tech_error': tech_error,
        'expired': expired,
        'aborted': aborted,
        'not_eligible': not_eligible,
        'avg_time': avg_time
    })

sp_df = pd.DataFrame(sp_stats).sort_values('success_rate', ascending=False)
print(f"\nSERVICE PROVIDER SUCCESS RATES:")
print(f"{'SP':<20} {'Total':>7} {'Success':>7} {'Rate':>6} {'TechErr':>7} {'Expired':>7} {'Aborted':>7} {'NotElig':>7} {'AvgTime(s)':>10}")
print("-" * 100)
for _, row in sp_df.iterrows():
    print(f"{row['sp_id']:<20} {row['total']:>7,} {row['success']:>7,} {row['success_rate']:>5.1f}% {row['tech_error']:>7,} {row['expired']:>7,} {row['aborted']:>7,} {row['not_eligible']:>7,} {row['avg_time']:>10.1f}")

print(f"\n{'='*80}")
print("5. PLATFORM COMPARISON (iOS vs Android)")
print(f"{'='*80}")

# Platform comparison
platform_stats = []
for platform in request_summary['platform'].unique():
    platform_data = request_summary[request_summary['platform'] == platform]
    total = len(platform_data)
    success = (platform_data['terminal_status'] == 'S40').sum()
    tech_error = (platform_data['terminal_status'] == 'S41').sum()
    expired = (platform_data['terminal_status'] == 'S42').sum()
    aborted = (platform_data['terminal_status'] == 'S43').sum()
    not_eligible = (platform_data['terminal_status'] == 'S44').sum()

    success_rate = (success / total * 100) if total > 0 else 0
    avg_time = platform_data[platform_data['completed']]['journey_time_sec'].median()

    platform_stats.append({
        'platform': platform,
        'total': total,
        'success': success,
        'success_rate': success_rate,
        'tech_error': tech_error,
        'tech_error_rate': (tech_error / total * 100) if total > 0 else 0,
        'expired': expired,
        'aborted': aborted,
        'not_eligible': not_eligible,
        'avg_time': avg_time
    })

platform_df = pd.DataFrame(platform_stats)
print(f"\nPLATFORM OVERVIEW:")
print(f"{'Platform':<10} {'Total':>7} {'Success':>7} {'Rate':>6} {'TechErr':>7} {'ErrRate':>7} {'Aborted':>7} {'AvgTime(s)':>10}")
print("-" * 80)
for _, row in platform_df.iterrows():
    print(f"{row['platform']:<10} {row['total']:>7,} {row['success']:>7,} {row['success_rate']:>5.1f}% {row['tech_error']:>7,} {row['tech_error_rate']:>6.1f}% {row['aborted']:>7,} {row['avg_time']:>10.1f}")

# Platform differences at each stage
print(f"\nPLATFORM JOURNEY DIFFERENCES:")
key_stages = ['S08', 'S20', 'S21', 'S30', 'S31', 'S40']
for stage in key_stages:
    ios_count = df[(df['platform'] == 'ios') & (df['status_code'] == stage)]['request_id'].nunique()
    android_count = df[(df['platform'] == 'android') & (df['status_code'] == stage)]['request_id'].nunique()
    ios_total = request_summary[request_summary['platform'] == 'ios'].shape[0]
    android_total = request_summary[request_summary['platform'] == 'android'].shape[0]

    ios_rate = (ios_count / ios_total * 100) if ios_total > 0 else 0
    android_rate = (android_count / android_total * 100) if android_total > 0 else 0
    diff = ios_rate - android_rate

    print(f"  {stage}: iOS {ios_rate:5.1f}% vs Android {android_rate:5.1f}% (diff: {diff:+5.1f}pp)")

print(f"\n{'='*80}")
print("6. ERROR ANALYSIS")
print(f"{'='*80}")

# Error distribution
error_df = df[df['error_code'].notna() & (df['error_code'] != '')].copy()
print(f"\nTotal error events: {len(error_df):,}")

if len(error_df) > 0:
    print(f"\nERROR CODE DISTRIBUTION:")
    error_counts = error_df.groupby(['error_code', 'error_source']).size().sort_values(ascending=False)
    for (code, source), count in error_counts.head(15).items():
        pct = count / len(error_df) * 100
        print(f"  {code:<25} (source: {source:<10}) {count:5,} ({pct:5.1f}%)")

    # Errors by status
    print(f"\nERRORS BY STATUS CODE:")
    error_by_status = error_df.groupby('status_code')['request_id'].nunique().sort_values(ascending=False)
    for status, count in error_by_status.head(10).items():
        print(f"  {status}: {count:,} unique requests with errors")

# Terminal status distribution
print(f"\nTERMINAL STATUS DISTRIBUTION:")
terminal_dist = request_summary['terminal_status'].value_counts()
total_terminal = terminal_dist.sum()
status_labels = {
    'S40': 'Share Success',
    'S41': 'Technical Error',
    'S42': 'Expired',
    'S43': 'User Aborted',
    'S44': 'Not Eligible'
}
for status, count in terminal_dist.items():
    label = status_labels.get(status, status)
    pct = count / total_terminal * 100
    print(f"  {status} ({label:<20}): {count:5,} ({pct:5.1f}%)")

# Technical vs user-driven failures
tech_failures = (request_summary['terminal_status'].isin(['S41', 'S42'])).sum()
user_failures = (request_summary['terminal_status'].isin(['S43', 'S44'])).sum()
total_failures = tech_failures + user_failures
print(f"\nFAILURE BREAKDOWN:")
print(f"  Technical failures (S41, S42): {tech_failures:,} ({tech_failures/total_failures*100:.1f}%)")
print(f"  User-driven failures (S43, S44): {user_failures:,} ({user_failures/total_failures*100:.1f}%)")

print(f"\n{'='*80}")
print("7. TIME-BASED METRICS")
print(f"{'='*80}")

# Calculate step latencies
print(f"\nSTEP LATENCY ANALYSIS (median milliseconds):")
latency_by_status = df[df['step_latency_ms'] > 0].groupby('status_code')['step_latency_ms'].agg(['median', 'mean', 'std', 'count'])
latency_by_status = latency_by_status.sort_values('median', ascending=False)

print(f"{'Status':<8} {'Median(ms)':>10} {'Mean(ms)':>10} {'StdDev(ms)':>10} {'Samples':>8}")
print("-" * 60)
for status, row in latency_by_status.head(15).iterrows():
    print(f"{status:<8} {row['median']:>10.0f} {row['mean']:>10.0f} {row['std']:>10.0f} {row['count']:>8.0f}")

# Journey time for successful flows
successful_journeys = request_summary[request_summary['terminal_status'] == 'S40']['journey_time_sec'].dropna()
print(f"\nJOURNEY TIME FOR SUCCESSFUL SHARES (S40):")
if len(successful_journeys) > 0:
    print(f"  Median: {successful_journeys.median():.1f} seconds")
    print(f"  Mean: {successful_journeys.mean():.1f} seconds")
    print(f"  P90: {successful_journeys.quantile(0.9):.1f} seconds")
    print(f"  Min: {successful_journeys.min():.1f} seconds")
    print(f"  Max: {successful_journeys.max():.1f} seconds")

# Time at critical stages
print(f"\nTIME SPENT AT CRITICAL STAGES:")
critical_stages = [
    ('S08', 'S20', 'View to Consent'),
    ('S20', 'S21', 'Consent Decision'),
    ('S21', 'S30', 'Consent to PIN'),
    ('S30', 'S31', 'PIN Entry'),
    ('S31', 'S40', 'PIN to Success')
]

for from_status, to_status, label in critical_stages:
    # Find time difference for these transitions
    from_times = df[df['status_code'] == from_status][['request_id', 'status_ts']]
    to_times = df[df['status_code'] == to_status][['request_id', 'status_ts']]

    merged = from_times.merge(to_times, on='request_id', suffixes=('_from', '_to'))
    merged['duration_sec'] = (merged['status_ts_to'] - merged['status_ts_from']).dt.total_seconds()

    if len(merged) > 0:
        median_time = merged['duration_sec'].median()
        mean_time = merged['duration_sec'].mean()
        print(f"  {label:<25} Median: {median_time:>6.1f}s, Mean: {mean_time:>6.1f}s (n={len(merged):,})")

# Journey time by channel
print(f"\nJOURNEY TIME BY CHANNEL (successful flows only):")
for channel in request_summary['channel'].unique():
    channel_success = request_summary[(request_summary['channel'] == channel) &
                                     (request_summary['terminal_status'] == 'S40')]['journey_time_sec'].dropna()
    if len(channel_success) > 0:
        print(f"  {channel:12} Median: {channel_success.median():>6.1f}s, Mean: {channel_success.mean():>6.1f}s (n={len(channel_success):,})")

print(f"\n{'='*80}")
print("8. DATA QUALITY OBSERVATIONS")
print(f"{'='*80}")

# Check for data quality issues
print(f"\nDATA QUALITY CHECKS:")

# Missing terminal status
incomplete = request_summary[~request_summary['completed']].shape[0]
print(f"  Requests without terminal status: {incomplete:,} ({incomplete/len(request_summary)*100:.1f}%)")

# Null values
print(f"\nMISSING VALUES:")
null_counts = df.isnull().sum()
for col, count in null_counts[null_counts > 0].items():
    pct = count / len(df) * 100
    print(f"  {col}: {count:,} ({pct:.1f}%)")

# Check for status sequence anomalies
print(f"\nSTATUS SEQUENCE VALIDATION:")
# Count requests by status
status_reach = df.groupby('status_code')['request_id'].nunique().sort_index()
print(f"  Total unique requests: {df['request_id'].nunique():,}")
print(f"  Requests reaching S00: {status_reach.get('S00', 0):,}")
print(f"  Requests reaching S08: {status_reach.get('S08', 0):,}")
print(f"  Requests reaching S40 (success): {status_reach.get('S40', 0):,}")

# Check for duplicate status codes per request
duplicates = df.groupby(['request_id', 'status_code']).size()
duplicates = duplicates[duplicates > 1]
if len(duplicates) > 0:
    print(f"  WARNING: {len(duplicates):,} request-status combinations appear multiple times")
else:
    print(f"  ✓ No duplicate status codes per request")

print(f"\n{'='*80}")
print("ANALYSIS COMPLETE")
print(f"{'='*80}")
