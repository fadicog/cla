"""
Generate data for advanced chart visualizations from sharing transactions sample data.
This script produces JSON data structures ready for Chart.js embedding.
"""

import pandas as pd
import json
from collections import Counter, defaultdict
import numpy as np

# Load data
df = pd.read_csv(r'D:\claude\sharing_transactions_new_sample.csv')

# Get terminal status for each request
terminal_statuses = ['S40', 'S41', 'S42', 'S43', 'S44']
request_outcomes = df[df['status_code'].isin(terminal_statuses)].groupby('request_id').last()

print("=== DATASET OVERVIEW ===")
print(f"Total records: {len(df)}")
print(f"Unique requests: {df['request_id'].nunique()}")
print(f"Requests with outcomes: {len(request_outcomes)}")

# =============================================================================
# 1. MULTI-STAGE FUNNEL CHART
# =============================================================================
print("\n=== 1. MULTI-STAGE FUNNEL ===")

# Define funnel stages
funnel_stages = ['S00', 'S08', 'S20', 'S21', 'S30', 'S31', 'S40']
stage_labels = {
    'S00': 'Request Created',
    'S08': 'Request Opened',
    'S20': 'Consent Screen',
    'S21': 'Reviewing Docs',
    'S30': 'Docs Collected',
    'S31': 'Verification Complete',
    'S40': 'Success'
}

funnel_data = []
previous_count = None
for stage in funnel_stages:
    count = df[df['status_code'] == stage]['request_id'].nunique()
    drop_off_pct = 0 if previous_count is None else ((previous_count - count) / previous_count * 100)
    funnel_data.append({
        'stage': stage,
        'label': stage_labels[stage],
        'count': int(count),
        'drop_off_pct': round(drop_off_pct, 1)
    })
    previous_count = count
    print(f"{stage_labels[stage]}: {count} ({drop_off_pct:.1f}% drop-off)")

# =============================================================================
# 2. SP PERFORMANCE BY CHANNEL
# =============================================================================
print("\n=== 2. SP PERFORMANCE BY CHANNEL ===")

# Get top 10 SPs by volume
top_sps = request_outcomes['sp_id'].value_counts().head(10).index.tolist()

sp_channel_data = defaultdict(lambda: {'notification': 0, 'qr': 0, 'redirect': 0})
for sp in top_sps:
    sp_requests = request_outcomes[request_outcomes['sp_id'] == sp]
    for channel in ['notification', 'qr', 'redirect']:
        channel_requests = sp_requests[sp_requests['channel'] == channel]
        success_rate = (channel_requests['status_code'] == 'S40').sum() / len(channel_requests) * 100 if len(channel_requests) > 0 else 0
        sp_channel_data[sp][channel] = round(success_rate, 1)

sp_performance_data = []
for sp in top_sps:
    sp_performance_data.append({
        'sp': sp,
        'notification': sp_channel_data[sp]['notification'],
        'qr': sp_channel_data[sp]['qr'],
        'redirect': sp_channel_data[sp]['redirect']
    })
    print(f"{sp}: Notif={sp_channel_data[sp]['notification']}%, QR={sp_channel_data[sp]['qr']}%, Redirect={sp_channel_data[sp]['redirect']}%")

# =============================================================================
# 3. ERROR DISTRIBUTION
# =============================================================================
print("\n=== 3. ERROR DISTRIBUTION ===")

error_statuses = ['S41', 'S42', 'S43', 'S44']
error_labels = {
    'S41': 'Technical Error',
    'S42': 'Expired',
    'S43': 'User Aborted',
    'S44': 'Not Eligible'
}

error_counts = {}
for status in error_statuses:
    count = (request_outcomes['status_code'] == status).sum()
    error_counts[status] = int(count)
    print(f"{error_labels[status]}: {count}")

error_data = [
    {'label': error_labels[status], 'count': error_counts[status]}
    for status in error_statuses
]

# =============================================================================
# 4. STEP LATENCY ANALYSIS
# =============================================================================
print("\n=== 4. STEP LATENCY ANALYSIS ===")

# Key status transitions
key_transitions = [
    ('S00', 'S08', 'App Opened'),
    ('S08', 'S20', 'Loading Consent'),
    ('S20', 'S21', 'Review Docs'),
    ('S21', 'S30', 'Collecting Docs'),
    ('S30', 'S31', 'Verification'),
    ('S31', 'S40', 'Final Submit')
]

latency_data = []
for prev_status, curr_status, label in key_transitions:
    transitions = df[(df['previous_status'] == prev_status) & (df['status_code'] == curr_status)]
    if len(transitions) > 0:
        avg_latency = transitions['step_latency_ms'].mean() / 1000  # Convert to seconds
        latency_data.append({
            'transition': label,
            'avg_seconds': round(avg_latency, 2)
        })
        print(f"{label}: {avg_latency:.2f}s")

# =============================================================================
# 5. PLATFORM x CHANNEL MATRIX
# =============================================================================
print("\n=== 5. PLATFORM x CHANNEL MATRIX ===")

platform_channel_data = []
for platform in ['ios', 'android']:
    platform_data = {'platform': platform}
    for channel in ['notification', 'qr', 'redirect']:
        subset = request_outcomes[(request_outcomes['platform'] == platform) & (request_outcomes['channel'] == channel)]
        success_rate = (subset['status_code'] == 'S40').sum() / len(subset) * 100 if len(subset) > 0 else 0
        platform_data[channel] = round(success_rate, 1)
        print(f"{platform.upper()} x {channel.capitalize()}: {success_rate:.1f}% (n={len(subset)})")
    platform_channel_data.append(platform_data)

# =============================================================================
# 6. DOCUMENT COMPLEXITY IMPACT
# =============================================================================
print("\n=== 6. DOCUMENT COMPLEXITY IMPACT ===")

doc_complexity_data = []
for doc_count in [1, 2, 3, 4]:
    if doc_count < 4:
        subset = request_outcomes[request_outcomes['required_count'] == doc_count]
        label = f"{doc_count} doc" if doc_count == 1 else f"{doc_count} docs"
    else:
        subset = request_outcomes[request_outcomes['required_count'] >= 4]
        label = "4+ docs"

    success_rate = (subset['status_code'] == 'S40').sum() / len(subset) * 100 if len(subset) > 0 else 0
    doc_complexity_data.append({
        'label': label,
        'success_rate': round(success_rate, 1),
        'count': int(len(subset))
    })
    print(f"{label}: {success_rate:.1f}% (n={len(subset)})")

# =============================================================================
# 7. WEEKLY TREND (SIMULATED)
# =============================================================================
print("\n=== 7. WEEKLY TREND ===")

# Convert to datetime
df['status_ts'] = pd.to_datetime(df['status_ts'])
request_outcomes['status_ts'] = pd.to_datetime(request_outcomes['status_ts'])

# Group by date
daily_success = request_outcomes.groupby(request_outcomes['status_ts'].dt.date).agg({
    'status_code': lambda x: (x == 'S40').sum() / len(x) * 100
}).reset_index()
daily_success.columns = ['date', 'success_rate']

weekly_trend_data = []
for _, row in daily_success.iterrows():
    weekly_trend_data.append({
        'date': str(row['date']),
        'success_rate': round(row['success_rate'], 1)
    })
    print(f"{row['date']}: {row['success_rate']:.1f}%")

# =============================================================================
# 8. PATH ANALYSIS (TOP 5 COMMON PATHS)
# =============================================================================
print("\n=== 8. PATH ANALYSIS ===")

# Extract complete paths from status_history
def extract_path(status_history_str):
    """Extract path from status_history string."""
    try:
        # Remove brackets and quotes, split by comma
        clean = status_history_str.strip('[]"').replace('"', '').replace(' ', '')
        return clean
    except:
        return ""

request_outcomes['path'] = request_outcomes['status_history'].apply(extract_path)

# Get top 5 most common paths
path_counts = request_outcomes['path'].value_counts().head(5)

path_data = []
for path, count in path_counts.items():
    # Determine outcome
    if 'S40' in path:
        outcome = 'Success'
    elif 'S43' in path:
        outcome = 'Aborted'
    elif 'S42' in path:
        outcome = 'Expired'
    elif 'S41' in path:
        outcome = 'Tech Error'
    elif 'S44' in path:
        outcome = 'Not Eligible'
    else:
        outcome = 'Other'

    # Create readable path
    path_steps = path.split(',')
    readable_path = ' > '.join(path_steps[:5]) + ('...' if len(path_steps) > 5 else '')

    path_data.append({
        'path': readable_path,
        'outcome': outcome,
        'count': int(count),
        'percentage': round(count / len(request_outcomes) * 100, 1)
    })
    print(f"{readable_path} ({outcome}): {count} ({count / len(request_outcomes) * 100:.1f}%)")

# =============================================================================
# 9. BOTTLENECK WATERFALL (WHERE FAILURES OCCURRED)
# =============================================================================
print("\n=== 9. BOTTLENECK WATERFALL ===")

# Get failed requests (not S40)
failed_requests = request_outcomes[request_outcomes['status_code'] != 'S40']

# Get the previous status before failure (last non-terminal status)
def get_bottleneck_stage(row):
    """Get the last status before terminal failure status."""
    prev = row['previous_status']
    # Map to stage categories
    if prev in ['S00', 'S01', 'S02', 'S03', 'S04', 'S05']:
        return 'Pre-Open'
    elif prev in ['S06', 'S07', 'S08']:
        return 'Opening'
    elif prev in ['S10', 'S11', 'S12', 'S13', 'S14', 'S15']:
        return 'Doc Availability Check'
    elif prev in ['S20', 'S21']:
        return 'Consent Screen'
    elif prev in ['S30', 'S31', 'S32']:
        return 'Collection & Verification'
    else:
        return 'Other'

failed_requests['bottleneck'] = failed_requests.apply(get_bottleneck_stage, axis=1)

bottleneck_counts = failed_requests.groupby(['bottleneck', 'status_code']).size().reset_index(name='count')

bottleneck_data = []
for stage in ['Pre-Open', 'Opening', 'Doc Availability Check', 'Consent Screen', 'Collection & Verification']:
    stage_data = bottleneck_counts[bottleneck_counts['bottleneck'] == stage]
    total = stage_data['count'].sum()
    if total > 0:
        bottleneck_data.append({
            'stage': stage,
            'count': int(total)
        })
        print(f"{stage}: {total} failures")

# =============================================================================
# EXPORT ALL DATA AS JSON
# =============================================================================

output = {
    'funnel': funnel_data,
    'sp_performance': sp_performance_data,
    'error_distribution': error_data,
    'step_latency': latency_data,
    'platform_channel': platform_channel_data,
    'doc_complexity': doc_complexity_data,
    'weekly_trend': weekly_trend_data,
    'path_analysis': path_data,
    'bottleneck': bottleneck_data
}

# Save to JSON file
with open(r'D:\claude\advanced_charts_data.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n=== EXPORT COMPLETE ===")
print("Data saved to: D:\\claude\\advanced_charts_data.json")
print(f"\nData structure keys: {list(output.keys())}")
