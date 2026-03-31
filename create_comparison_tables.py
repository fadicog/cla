import pandas as pd
import numpy as np
from datetime import datetime
import sys

# Set stdout encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Load the dataset
df = pd.read_csv(r'D:\cluade\sharing_transactions_sample.csv')
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
    'required_count': 'first',
    'required_docs': 'first'
}).rename(columns={'status_ts': 'start_ts'})

# Merge to create request-level summary
request_summary = request_start.join(request_terminal, how='left')
request_summary['completed'] = ~request_summary['terminal_status'].isna()
request_summary['journey_time_sec'] = (request_summary['terminal_ts'] - request_summary['start_ts']).dt.total_seconds()
request_summary['success'] = request_summary['terminal_status'] == 'S40'

# ============================================================================
# TABLE 1: Channel Performance Comparison
# ============================================================================
print("="*100)
print("TABLE 1: CHANNEL PERFORMANCE COMPARISON")
print("="*100)
print()

channel_comparison = []
for channel in ['notification', 'redirect', 'qr']:
    channel_data = request_summary[request_summary['channel'] == channel]
    total = len(channel_data)
    success = channel_data['success'].sum()
    success_rate = (success / total * 100) if total > 0 else 0

    tech_error = (channel_data['terminal_status'] == 'S41').sum()
    expired = (channel_data['terminal_status'] == 'S42').sum()
    aborted = (channel_data['terminal_status'] == 'S43').sum()
    not_eligible = (channel_data['terminal_status'] == 'S44').sum()

    avg_time = channel_data[channel_data['success']]['journey_time_sec'].median()
    avg_docs = channel_data['required_count'].mean()

    # Get key funnel metrics
    if channel == 'notification':
        s01 = df[(df['channel'] == channel) & (df['status_code'] == 'S01')]['request_id'].nunique()
        s02 = df[(df['channel'] == channel) & (df['status_code'] == 'S02')]['request_id'].nunique()
        s03 = df[(df['channel'] == channel) & (df['status_code'] == 'S03')]['request_id'].nunique()
        delivery_rate = (s02 / s01 * 100) if s01 > 0 else 0
        open_rate = (s03 / s02 * 100) if s02 > 0 else 0
        key_metric = f"Delivery: {delivery_rate:.1f}%, Open: {open_rate:.1f}%"
    elif channel == 'qr':
        s06 = df[(df['channel'] == channel) & (df['status_code'] == 'S06')]['request_id'].nunique()
        s07 = df[(df['channel'] == channel) & (df['status_code'] == 'S07')]['request_id'].nunique()
        scan_rate = (s07 / s06 * 100) if s06 > 0 else 0
        key_metric = f"Scan Rate: {scan_rate:.1f}%"
    else:  # redirect
        s04 = df[(df['channel'] == channel) & (df['status_code'] == 'S04')]['request_id'].nunique()
        s05 = df[(df['channel'] == channel) & (df['status_code'] == 'S05')]['request_id'].nunique()
        s08 = df[(df['channel'] == channel) & (df['status_code'] == 'S08')]['request_id'].nunique()
        s20 = df[(df['channel'] == channel) & (df['status_code'] == 'S20')]['request_id'].nunique()
        land_rate = (s05 / s04 * 100) if s04 > 0 else 0
        view_to_consent = (s20 / s08 * 100) if s08 > 0 else 0
        key_metric = f"Land: {land_rate:.1f}%, View->Consent: {view_to_consent:.1f}%"

    channel_comparison.append({
        'Channel': channel.upper(),
        'Total Requests': total,
        'Success': success,
        'Success Rate': f"{success_rate:.1f}%",
        'Tech Errors': tech_error,
        'Expired': expired,
        'Aborted': aborted,
        'Not Eligible': not_eligible,
        'Median Time (s)': f"{avg_time:.1f}" if not pd.isna(avg_time) else 'N/A',
        'Avg Docs': f"{avg_docs:.1f}",
        'Key Metric': key_metric
    })

channel_df = pd.DataFrame(channel_comparison)
print(channel_df.to_string(index=False))

# ============================================================================
# TABLE 2: Document Type Combinations - Success Rate
# ============================================================================
print("\n" + "="*100)
print("TABLE 2: MOST COMMON DOCUMENT COMBINATIONS - SUCCESS RATES")
print("="*100)
print()

doc_combo_stats = []
for docs in request_summary['required_docs'].value_counts().head(15).index:
    combo_data = request_summary[request_summary['required_docs'] == docs]
    total = len(combo_data)
    success = combo_data['success'].sum()
    success_rate = (success / total * 100) if total > 0 else 0

    # Check if docs were ready
    requests_with_combo = combo_data.index
    docs_ready = df[(df['request_id'].isin(requests_with_combo)) & (df['status_code'] == 'S10')]['request_id'].nunique()
    docs_missing = df[(df['request_id'].isin(requests_with_combo)) & (df['status_code'] == 'S11')]['request_id'].nunique()
    readiness = (docs_ready / (docs_ready + docs_missing) * 100) if (docs_ready + docs_missing) > 0 else 0

    avg_time = combo_data[combo_data['success']]['journey_time_sec'].median()

    doc_combo_stats.append({
        'Document Combination': docs,
        'Total': total,
        'Success': success,
        'Success Rate': f"{success_rate:.1f}%",
        'Readiness Rate': f"{readiness:.1f}%",
        'Median Time (s)': f"{avg_time:.1f}" if not pd.isna(avg_time) else 'N/A'
    })

doc_combo_df = pd.DataFrame(doc_combo_stats)
print(doc_combo_df.to_string(index=False))

# ============================================================================
# TABLE 3: SP Performance by Channel
# ============================================================================
print("\n" + "="*100)
print("TABLE 3: SERVICE PROVIDER PERFORMANCE BY CHANNEL")
print("="*100)
print()

sp_channel_stats = []
for sp in request_summary['sp_id'].unique():
    for channel in request_summary['channel'].unique():
        sp_channel_data = request_summary[(request_summary['sp_id'] == sp) & (request_summary['channel'] == channel)]
        total = len(sp_channel_data)
        if total >= 5:  # Only include if sufficient sample size
            success = sp_channel_data['success'].sum()
            success_rate = (success / total * 100) if total > 0 else 0

            sp_channel_stats.append({
                'Service Provider': sp,
                'Channel': channel,
                'Total': total,
                'Success': success,
                'Success Rate': f"{success_rate:.1f}%"
            })

sp_channel_df = pd.DataFrame(sp_channel_stats)
sp_channel_df = sp_channel_df.sort_values(['Service Provider', 'Channel'])
print(sp_channel_df.to_string(index=False))

# ============================================================================
# TABLE 4: Platform Performance by Channel
# ============================================================================
print("\n" + "="*100)
print("TABLE 4: PLATFORM PERFORMANCE BY CHANNEL")
print("="*100)
print()

platform_channel_stats = []
for platform in ['ios', 'android']:
    for channel in ['notification', 'redirect', 'qr']:
        platform_channel_data = request_summary[(request_summary['platform'] == platform) & (request_summary['channel'] == channel)]
        total = len(platform_channel_data)
        if total > 0:
            success = platform_channel_data['success'].sum()
            success_rate = (success / total * 100) if total > 0 else 0
            tech_error = (platform_channel_data['terminal_status'] == 'S41').sum()
            aborted = (platform_channel_data['terminal_status'] == 'S43').sum()
            avg_time = platform_channel_data[platform_channel_data['success']]['journey_time_sec'].median()

            platform_channel_stats.append({
                'Platform': platform.upper(),
                'Channel': channel.upper(),
                'Total': total,
                'Success': success,
                'Success Rate': f"{success_rate:.1f}%",
                'Tech Errors': tech_error,
                'Aborted': aborted,
                'Median Time (s)': f"{avg_time:.1f}" if not pd.isna(avg_time) else 'N/A'
            })

platform_channel_df = pd.DataFrame(platform_channel_stats)
print(platform_channel_df.to_string(index=False))

# ============================================================================
# TABLE 5: Error Analysis by Channel and Status
# ============================================================================
print("\n" + "="*100)
print("TABLE 5: ERROR DISTRIBUTION BY CHANNEL")
print("="*100)
print()

error_df = df[df['error_code'].notna() & (df['error_code'] != '')].copy()

if len(error_df) > 0:
    error_channel_stats = []
    for channel in ['notification', 'redirect', 'qr']:
        channel_errors = error_df[error_df['channel'] == channel]
        total_errors = len(channel_errors)

        issuer_errors = channel_errors[channel_errors['error_source'] == 'issuer'].shape[0]
        network_errors = channel_errors[channel_errors['error_source'] == 'network'].shape[0]
        user_errors = channel_errors[channel_errors['error_source'] == 'user_cancel'].shape[0]
        dv_errors = channel_errors[channel_errors['error_source'] == 'dv'].shape[0]

        # Most common error
        if total_errors > 0:
            most_common = channel_errors['error_code'].value_counts().iloc[0] if len(channel_errors) > 0 else 'N/A'
            most_common_name = channel_errors['error_code'].value_counts().index[0] if len(channel_errors) > 0 else 'N/A'
        else:
            most_common = 0
            most_common_name = 'N/A'

        error_channel_stats.append({
            'Channel': channel.upper(),
            'Total Errors': total_errors,
            'Issuer': issuer_errors,
            'Network': network_errors,
            'User': user_errors,
            'DV': dv_errors,
            'Most Common': f"{most_common_name} ({most_common})"
        })

    error_channel_df = pd.DataFrame(error_channel_stats)
    print(error_channel_df.to_string(index=False))

# ============================================================================
# TABLE 6: Time-to-Success by Document Count
# ============================================================================
print("\n" + "="*100)
print("TABLE 6: JOURNEY TIME BY NUMBER OF DOCUMENTS REQUESTED")
print("="*100)
print()

doc_count_stats = []
for doc_count in sorted(request_summary['required_count'].unique()):
    doc_count_data = request_summary[request_summary['required_count'] == doc_count]
    total = len(doc_count_data)
    success = doc_count_data['success'].sum()
    success_rate = (success / total * 100) if total > 0 else 0

    successful_data = doc_count_data[doc_count_data['success']]
    if len(successful_data) > 0:
        median_time = successful_data['journey_time_sec'].median()
        p90_time = successful_data['journey_time_sec'].quantile(0.9)
    else:
        median_time = np.nan
        p90_time = np.nan

    # Check abandonment rate
    aborted = (doc_count_data['terminal_status'] == 'S43').sum()
    abort_rate = (aborted / total * 100) if total > 0 else 0

    doc_count_stats.append({
        'Docs Requested': int(doc_count),
        'Total Requests': total,
        'Success': success,
        'Success Rate': f"{success_rate:.1f}%",
        'Aborted': aborted,
        'Abort Rate': f"{abort_rate:.1f}%",
        'Median Time (s)': f"{median_time:.1f}" if not pd.isna(median_time) else 'N/A',
        'P90 Time (s)': f"{p90_time:.1f}" if not pd.isna(p90_time) else 'N/A'
    })

doc_count_df = pd.DataFrame(doc_count_stats)
print(doc_count_df.to_string(index=False))

# ============================================================================
# TABLE 7: Hourly Performance Analysis (if data available)
# ============================================================================
print("\n" + "="*100)
print("TABLE 7: PERFORMANCE BY HOUR OF DAY")
print("="*100)
print()

request_summary_with_hour = request_summary.copy()
request_summary_with_hour['hour'] = request_summary_with_hour['start_ts'].dt.hour

hourly_stats = []
for hour in sorted(request_summary_with_hour['hour'].unique()):
    hour_data = request_summary_with_hour[request_summary_with_hour['hour'] == hour]
    total = len(hour_data)
    success = hour_data['success'].sum()
    success_rate = (success / total * 100) if total > 0 else 0

    aborted = (hour_data['terminal_status'] == 'S43').sum()
    abort_rate = (aborted / total * 100) if total > 0 else 0

    avg_time = hour_data[hour_data['success']]['journey_time_sec'].median()

    hourly_stats.append({
        'Hour (24h)': f"{hour:02d}:00",
        'Total': total,
        'Success': success,
        'Success Rate': f"{success_rate:.1f}%",
        'Aborted': aborted,
        'Abort Rate': f"{abort_rate:.1f}%",
        'Median Time (s)': f"{avg_time:.1f}" if not pd.isna(avg_time) else 'N/A'
    })

hourly_df = pd.DataFrame(hourly_stats)
print(hourly_df.to_string(index=False))

# ============================================================================
# TABLE 8: App Version Performance
# ============================================================================
print("\n" + "="*100)
print("TABLE 8: PERFORMANCE BY APP VERSION")
print("="*100)
print()

# Get app version for each request
request_versions = df[df['status_code'] == 'S00'][['request_id', 'app_version']].set_index('request_id')
request_summary_with_version = request_summary.join(request_versions, how='left')

version_stats = []
for version in request_summary_with_version['app_version'].value_counts().head(10).index:
    version_data = request_summary_with_version[request_summary_with_version['app_version'] == version]

    total = len(version_data)
    if total >= 5:
        success = version_data['success'].sum()
        success_rate = (success / total * 100) if total > 0 else 0

        tech_error = (version_data['terminal_status'] == 'S41').sum()
        aborted = (version_data['terminal_status'] == 'S43').sum()

        avg_time = version_data[version_data['success']]['journey_time_sec'].median()

        version_stats.append({
            'App Version': version,
            'Total': total,
            'Success': success,
            'Success Rate': f"{success_rate:.1f}%",
            'Tech Errors': tech_error,
            'Aborted': aborted,
            'Median Time (s)': f"{avg_time:.1f}" if not pd.isna(avg_time) else 'N/A'
        })

version_df = pd.DataFrame(version_stats)
version_df = version_df.sort_values('Total', ascending=False)
print(version_df.to_string(index=False))

print("\n" + "="*100)
print("COMPARISON TABLES COMPLETE")
print("="*100)
