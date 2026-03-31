"""
Comprehensive Statistical Analysis and Visualization Suite
UAE PASS Digital Documents - Sharing Request Analysis

Dataset: sharing_transactions_new_sample.csv
- 500 unique requests
- 5,068 status events
- Status codes: S00-S44
- Terminal statuses: S40 (Success), S41 (Technical Error), S42 (Expired), S43 (User Aborted), S44 (Not Eligible)
"""

import sys
import io

# Set UTF-8 encoding for stdout to handle Unicode characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
import warnings
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory for visualizations
viz_dir = Path(r'D:\cluade\visualizations')
viz_dir.mkdir(exist_ok=True)

print("Loading data...")
df = pd.read_csv(r'D:\cluade\sharing_transactions_new_sample.csv')

# Parse timestamps
df['status_ts'] = pd.to_datetime(df['status_ts'])

# Parse JSON fields
df['required_docs_list'] = df['required_docs'].apply(lambda x: json.loads(x) if pd.notna(x) else [])
df['status_history_list'] = df['status_history'].apply(lambda x: json.loads(x) if pd.notna(x) else [])

# Get terminal status for each request (last status in journey)
terminal_statuses = df.groupby('request_id').agg({
    'status_code': 'last',
    'channel': 'first',
    'platform': 'first',
    'sp_id': 'first',
    'required_count': 'first',
    'status_ts': ['first', 'last'],
    'error_code': 'last',
    'error_source': 'last'
}).reset_index()

terminal_statuses.columns = ['request_id', 'terminal_status', 'channel', 'platform', 'sp_id',
                             'required_count', 'start_time', 'end_time', 'error_code', 'error_source']
terminal_statuses['journey_duration_ms'] = (terminal_statuses['end_time'] - terminal_statuses['start_time']).dt.total_seconds() * 1000

# Status code definitions
STATUS_DEFINITIONS = {
    'S00': 'Request Created',
    'S01': 'Notification Sent',
    'S02': 'Notification Delivered',
    'S03': 'Notification Tapped',
    'S04': 'Redirect Initiated',
    'S05': 'App Opened (Redirect)',
    'S06': 'QR Scanned',
    'S07': 'QR Validated',
    'S08': 'Request Loaded',
    'S10': 'Documents Ready',
    'S11': 'Documents Missing',
    'S12': 'Retrieval Started',
    'S13': 'Retrieval Success',
    'S14': 'Retrieval Failed (Network)',
    'S15': 'Retrieval Failed (Issuer)',
    'S20': 'Consent Screen Shown',
    'S21': 'Consent Granted',
    'S22': 'Consent Denied',
    'S30': 'PIN Required',
    'S31': 'PIN Success',
    'S32': 'PIN Failed',
    'S40': 'Success (Shared)',
    'S41': 'Technical Error',
    'S42': 'Expired',
    'S43': 'User Aborted',
    'S44': 'Not Eligible'
}

TERMINAL_STATUSES = ['S40', 'S41', 'S42', 'S43', 'S44']

print(f"\nDataset Overview:")
print(f"  Total events: {len(df):,}")
print(f"  Unique requests: {df['request_id'].nunique():,}")
print(f"  Date range: {df['status_ts'].min()} to {df['status_ts'].max()}")
print(f"  Channels: {df['channel'].unique().tolist()}")
print(f"  Platforms: {df['platform'].unique().tolist()}")
print(f"  Service Providers: {df['sp_id'].nunique()}")
print(f"  Status codes: {sorted(df['status_code'].unique())}")

# ============================================================================
# 1. OVERALL PERFORMANCE METRICS
# ============================================================================
print("\n" + "="*80)
print("1. OVERALL PERFORMANCE METRICS")
print("="*80)

overall_metrics = {
    'Total Requests': len(terminal_statuses),
    'Success Rate (S40)': f"{(terminal_statuses['terminal_status'] == 'S40').mean() * 100:.2f}%",
    'Technical Error (S41)': f"{(terminal_statuses['terminal_status'] == 'S41').mean() * 100:.2f}%",
    'Expired (S42)': f"{(terminal_statuses['terminal_status'] == 'S42').mean() * 100:.2f}%",
    'User Aborted (S43)': f"{(terminal_statuses['terminal_status'] == 'S43').mean() * 100:.2f}%",
    'Not Eligible (S44)': f"{(terminal_statuses['terminal_status'] == 'S44').mean() * 100:.2f}%",
    'Avg Journey Time (Successful)': f"{terminal_statuses[terminal_statuses['terminal_status'] == 'S40']['journey_duration_ms'].mean() / 1000:.2f}s",
    'Avg Journey Time (Failed)': f"{terminal_statuses[terminal_statuses['terminal_status'] != 'S40']['journey_duration_ms'].mean() / 1000:.2f}s"
}

print("\nOverall Metrics:")
for key, value in overall_metrics.items():
    print(f"  {key}: {value}")

# Terminal Status Distribution
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Pie chart
terminal_counts = terminal_statuses['terminal_status'].value_counts()
colors = {'S40': '#2ecc71', 'S41': '#e74c3c', 'S42': '#f39c12', 'S43': '#e67e22', 'S44': '#95a5a6'}
pie_colors = [colors.get(status, '#3498db') for status in terminal_counts.index]

axes[0].pie(terminal_counts.values, labels=[f"{status}\n({STATUS_DEFINITIONS[status]})" for status in terminal_counts.index],
            autopct='%1.1f%%', startangle=90, colors=pie_colors)
axes[0].set_title('Terminal Status Distribution', fontsize=14, fontweight='bold')

# Bar chart
bars = axes[1].bar(range(len(terminal_counts)), terminal_counts.values,
                    color=[colors.get(status, '#3498db') for status in terminal_counts.index])
axes[1].set_xticks(range(len(terminal_counts)))
axes[1].set_xticklabels([f"{status}\n{STATUS_DEFINITIONS[status]}" for status in terminal_counts.index], rotation=45, ha='right')
axes[1].set_ylabel('Number of Requests', fontsize=12)
axes[1].set_title('Terminal Status Distribution (Bar Chart)', fontsize=14, fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}\n({height/len(terminal_statuses)*100:.1f}%)',
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(viz_dir / '01_terminal_status_distribution.png', dpi=300, bbox_inches='tight')
print(f"\nSaved: {viz_dir / '01_terminal_status_distribution.png'}")
plt.close()

# ============================================================================
# 2. CHANNEL PERFORMANCE ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("2. CHANNEL PERFORMANCE ANALYSIS")
print("="*80)

channel_perf = terminal_statuses.groupby('channel').agg({
    'request_id': 'count',
    'terminal_status': lambda x: (x == 'S40').sum()
}).reset_index()
channel_perf.columns = ['channel', 'total_requests', 'successful_requests']
channel_perf['success_rate'] = channel_perf['successful_requests'] / channel_perf['total_requests'] * 100
channel_perf = channel_perf.sort_values('success_rate', ascending=False)

print("\nChannel Performance:")
print(channel_perf.to_string(index=False))

# Channel comparison visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Success rate by channel
ax = axes[0, 0]
bars = ax.bar(channel_perf['channel'], channel_perf['success_rate'], color=['#2ecc71', '#3498db', '#9b59b6'])
ax.set_ylabel('Success Rate (%)', fontsize=12)
ax.set_title('Success Rate by Channel', fontsize=14, fontweight='bold')
ax.set_ylim(0, 100)
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Volume by channel
ax = axes[0, 1]
bars = ax.bar(channel_perf['channel'], channel_perf['total_requests'], color=['#2ecc71', '#3498db', '#9b59b6'])
ax.set_ylabel('Number of Requests', fontsize=12)
ax.set_title('Request Volume by Channel', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Terminal status distribution by channel
ax = axes[1, 0]
channel_terminal = terminal_statuses.groupby(['channel', 'terminal_status']).size().unstack(fill_value=0)
channel_terminal_pct = channel_terminal.div(channel_terminal.sum(axis=1), axis=0) * 100
channel_terminal_pct.plot(kind='bar', stacked=True, ax=ax,
                          color=[colors.get(col, '#3498db') for col in channel_terminal_pct.columns])
ax.set_ylabel('Percentage (%)', fontsize=12)
ax.set_xlabel('Channel', fontsize=12)
ax.set_title('Terminal Status Distribution by Channel', fontsize=14, fontweight='bold')
ax.legend(title='Terminal Status', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.grid(axis='y', alpha=0.3)

# Average journey time by channel
ax = axes[1, 1]
channel_time = terminal_statuses.groupby('channel')['journey_duration_ms'].mean() / 1000
bars = ax.bar(channel_time.index, channel_time.values, color=['#2ecc71', '#3498db', '#9b59b6'])
ax.set_ylabel('Average Journey Time (seconds)', fontsize=12)
ax.set_title('Average Journey Time by Channel', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}s', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(viz_dir / '02_channel_performance.png', dpi=300, bbox_inches='tight')
print(f"Saved: {viz_dir / '02_channel_performance.png'}")
plt.close()

# ============================================================================
# 3. STATUS TRANSITION ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("3. STATUS TRANSITION ANALYSIS")
print("="*80)

# Get all transitions
transitions = df[df['previous_status'].notna()][['previous_status', 'status_code']].copy()
transition_counts = transitions.groupby(['previous_status', 'status_code']).size().reset_index(name='count')

# Create transition matrix
all_statuses = sorted(df['status_code'].unique())
transition_matrix = pd.DataFrame(0, index=all_statuses, columns=all_statuses)
for _, row in transition_counts.iterrows():
    transition_matrix.loc[row['previous_status'], row['status_code']] = row['count']

print(f"\nTotal transitions: {len(transitions):,}")
print(f"Unique transition pairs: {len(transition_counts)}")

# Top 10 transitions
print("\nTop 10 Most Common Transitions:")
top_transitions = transition_counts.nlargest(10, 'count')
for idx, row in top_transitions.iterrows():
    from_status = STATUS_DEFINITIONS.get(row['previous_status'], row['previous_status'])
    to_status = STATUS_DEFINITIONS.get(row['status_code'], row['status_code'])
    print(f"  {row['previous_status']} -> {row['status_code']}: {row['count']:,} ({from_status} -> {to_status})")

# Transition heatmap
fig, ax = plt.subplots(figsize=(20, 16))
sns.heatmap(transition_matrix, annot=True, fmt='g', cmap='YlOrRd', ax=ax,
            cbar_kws={'label': 'Number of Transitions'}, linewidths=0.5)
ax.set_title('Status Transition Heatmap', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('To Status', fontsize=12)
ax.set_ylabel('From Status', fontsize=12)
plt.tight_layout()
plt.savefig(viz_dir / '03_transition_heatmap.png', dpi=300, bbox_inches='tight')
print(f"Saved: {viz_dir / '03_transition_heatmap.png'}")
plt.close()

# Critical drop-off transitions (transitions to terminal failure statuses)
failure_transitions = transition_counts[transition_counts['status_code'].isin(['S41', 'S42', 'S43', 'S44'])]
failure_transitions = failure_transitions.sort_values('count', ascending=False).head(15)

fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.barh(range(len(failure_transitions)), failure_transitions['count'].values,
               color=['#e74c3c' if status in ['S41', 'S44'] else '#f39c12' if status == 'S42' else '#e67e22'
                      for status in failure_transitions['status_code']])
ax.set_yticks(range(len(failure_transitions)))
ax.set_yticklabels([f"{row['previous_status']} -> {row['status_code']}\n({STATUS_DEFINITIONS.get(row['previous_status'], '')} -> {STATUS_DEFINITIONS.get(row['status_code'], '')})"
                     for _, row in failure_transitions.iterrows()], fontsize=9)
ax.set_xlabel('Number of Transitions', fontsize=12)
ax.set_title('Top 15 Critical Drop-off Points (Transitions to Failure)', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, (bar, count) in enumerate(zip(bars, failure_transitions['count'].values)):
    ax.text(count, i, f' {count}', va='center', fontsize=10)
plt.tight_layout()
plt.savefig(viz_dir / '04_critical_dropoffs.png', dpi=300, bbox_inches='tight')
print(f"Saved: {viz_dir / '04_critical_dropoffs.png'}")
plt.close()

# ============================================================================
# 4. ERROR ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("4. ERROR ANALYSIS")
print("="*80)

errors = df[df['error_code'].notna()].copy()
print(f"\nTotal error events: {len(errors):,}")
print(f"Requests with errors: {errors['request_id'].nunique():,}")

if len(errors) > 0:
    # Error code distribution
    error_code_dist = errors['error_code'].value_counts()
    print("\nError Code Distribution:")
    for error, count in error_code_dist.items():
        print(f"  {error}: {count} ({count/len(errors)*100:.1f}%)")

    # Error source distribution
    error_source_dist = errors['error_source'].value_counts()
    print("\nError Source Distribution:")
    for source, count in error_source_dist.items():
        print(f"  {source}: {count} ({count/len(errors)*100:.1f}%)")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Error code frequency
    ax = axes[0, 0]
    error_code_dist.plot(kind='bar', ax=ax, color='#e74c3c')
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_xlabel('Error Code', fontsize=12)
    ax.set_title('Error Code Frequency', fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', alpha=0.3)
    for i, v in enumerate(error_code_dist.values):
        ax.text(i, v, f'{v}\n({v/len(errors)*100:.1f}%)', ha='center', va='bottom', fontsize=9)

    # Error source distribution
    ax = axes[0, 1]
    error_source_colors = {'issuer': '#e74c3c', 'network': '#f39c12', 'dv': '#3498db', 'user_cancel': '#e67e22'}
    pie_colors = [error_source_colors.get(source, '#95a5a6') for source in error_source_dist.index]
    ax.pie(error_source_dist.values, labels=error_source_dist.index, autopct='%1.1f%%',
           startangle=90, colors=pie_colors)
    ax.set_title('Error Source Distribution', fontsize=14, fontweight='bold')

    # Errors by status code
    ax = axes[1, 0]
    error_by_status = errors.groupby('status_code')['error_code'].count().sort_values(ascending=False)
    bars = ax.bar(range(len(error_by_status)), error_by_status.values, color='#e74c3c')
    ax.set_xticks(range(len(error_by_status)))
    ax.set_xticklabels([f"{status}\n{STATUS_DEFINITIONS.get(status, status)}" for status in error_by_status.index],
                       rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Number of Errors', fontsize=12)
    ax.set_title('Errors by Status Code', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)

    # Previous status leading to errors
    ax = axes[1, 1]
    error_previous = errors.groupby('previous_status')['error_code'].count().sort_values(ascending=False).head(10)
    bars = ax.barh(range(len(error_previous)), error_previous.values, color='#e74c3c')
    ax.set_yticks(range(len(error_previous)))
    ax.set_yticklabels([f"{status} - {STATUS_DEFINITIONS.get(status, status)}" for status in error_previous.index],
                       fontsize=9)
    ax.set_xlabel('Number of Errors', fontsize=12)
    ax.set_title('Top 10 Previous Statuses Leading to Errors', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    for i, (bar, count) in enumerate(zip(bars, error_previous.values)):
        ax.text(count, i, f' {count}', va='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(viz_dir / '05_error_analysis.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {viz_dir / '05_error_analysis.png'}")
    plt.close()

# ============================================================================
# 5. SERVICE PROVIDER PERFORMANCE
# ============================================================================
print("\n" + "="*80)
print("5. SERVICE PROVIDER PERFORMANCE")
print("="*80)

sp_perf = terminal_statuses.groupby('sp_id').agg({
    'request_id': 'count',
    'terminal_status': lambda x: (x == 'S40').sum()
}).reset_index()
sp_perf.columns = ['sp_id', 'total_requests', 'successful_requests']
sp_perf['success_rate'] = sp_perf['successful_requests'] / sp_perf['total_requests'] * 100
sp_perf = sp_perf.sort_values('success_rate', ascending=False)

print("\nService Provider Performance:")
print(sp_perf.to_string(index=False))

fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# Success rate ranking
ax = axes[0, 0]
top_sp = sp_perf.head(15)
bars = ax.barh(range(len(top_sp)), top_sp['success_rate'].values,
               color=['#2ecc71' if rate >= 70 else '#f39c12' if rate >= 50 else '#e74c3c'
                      for rate in top_sp['success_rate'].values])
ax.set_yticks(range(len(top_sp)))
ax.set_yticklabels(top_sp['sp_id'].values, fontsize=9)
ax.set_xlabel('Success Rate (%)', fontsize=12)
ax.set_title('Top 15 Service Providers by Success Rate', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, (bar, rate) in enumerate(zip(bars, top_sp['success_rate'].values)):
    ax.text(rate, i, f' {rate:.1f}%', va='center', fontsize=9)

# Volume vs Success Rate scatter
ax = axes[0, 1]
scatter = ax.scatter(sp_perf['total_requests'], sp_perf['success_rate'],
                    s=sp_perf['total_requests']*10, alpha=0.6, c=sp_perf['success_rate'],
                    cmap='RdYlGn', vmin=0, vmax=100)
ax.set_xlabel('Total Requests', fontsize=12)
ax.set_ylabel('Success Rate (%)', fontsize=12)
ax.set_title('Volume vs Success Rate by Service Provider', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)
plt.colorbar(scatter, ax=ax, label='Success Rate (%)')

# Top performers (volume)
ax = axes[1, 0]
top_volume = sp_perf.nlargest(10, 'total_requests')
bars = ax.bar(range(len(top_volume)), top_volume['total_requests'].values, color='#3498db')
ax.set_xticks(range(len(top_volume)))
ax.set_xticklabels(top_volume['sp_id'].values, rotation=45, ha='right', fontsize=9)
ax.set_ylabel('Number of Requests', fontsize=12)
ax.set_title('Top 10 Service Providers by Volume', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=9)

# Bottom performers (success rate with min 5 requests)
ax = axes[1, 1]
bottom_sp = sp_perf[sp_perf['total_requests'] >= 5].nsmallest(10, 'success_rate')
if len(bottom_sp) > 0:
    bars = ax.barh(range(len(bottom_sp)), bottom_sp['success_rate'].values, color='#e74c3c')
    ax.set_yticks(range(len(bottom_sp)))
    ax.set_yticklabels(bottom_sp['sp_id'].values, fontsize=9)
    ax.set_xlabel('Success Rate (%)', fontsize=12)
    ax.set_title('Bottom 10 Service Providers by Success Rate (min 5 requests)', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    for i, (bar, rate) in enumerate(zip(bars, bottom_sp['success_rate'].values)):
        ax.text(rate, i, f' {rate:.1f}%', va='center', fontsize=9)

plt.tight_layout()
plt.savefig(viz_dir / '06_service_provider_performance.png', dpi=300, bbox_inches='tight')
print(f"Saved: {viz_dir / '06_service_provider_performance.png'}")
plt.close()

# ============================================================================
# 6. PLATFORM COMPARISON (iOS vs Android)
# ============================================================================
print("\n" + "="*80)
print("6. PLATFORM COMPARISON (iOS vs Android)")
print("="*80)

platform_perf = terminal_statuses.groupby('platform').agg({
    'request_id': 'count',
    'terminal_status': lambda x: (x == 'S40').sum(),
    'journey_duration_ms': 'mean'
}).reset_index()
platform_perf.columns = ['platform', 'total_requests', 'successful_requests', 'avg_journey_time_ms']
platform_perf['success_rate'] = platform_perf['successful_requests'] / platform_perf['total_requests'] * 100

print("\nPlatform Performance:")
print(platform_perf.to_string(index=False))

# Platform error rates
platform_errors = terminal_statuses.groupby('platform').agg({
    'terminal_status': lambda x: (x.isin(['S41', 'S44'])).sum() / len(x) * 100
}).reset_index()
platform_errors.columns = ['platform', 'technical_error_rate']

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Success rate comparison
ax = axes[0, 0]
bars = ax.bar(platform_perf['platform'], platform_perf['success_rate'],
              color=['#3498db', '#2ecc71'])
ax.set_ylabel('Success Rate (%)', fontsize=12)
ax.set_title('Success Rate by Platform', fontsize=14, fontweight='bold')
ax.set_ylim(0, 100)
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

# Journey time comparison
ax = axes[0, 1]
bars = ax.bar(platform_perf['platform'], platform_perf['avg_journey_time_ms'] / 1000,
              color=['#3498db', '#2ecc71'])
ax.set_ylabel('Average Journey Time (seconds)', fontsize=12)
ax.set_title('Average Journey Time by Platform', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}s', ha='center', va='bottom', fontsize=12, fontweight='bold')

# Terminal status distribution by platform
ax = axes[1, 0]
platform_terminal = terminal_statuses.groupby(['platform', 'terminal_status']).size().unstack(fill_value=0)
platform_terminal_pct = platform_terminal.div(platform_terminal.sum(axis=1), axis=0) * 100
platform_terminal_pct.plot(kind='bar', stacked=True, ax=ax,
                           color=[colors.get(col, '#3498db') for col in platform_terminal_pct.columns])
ax.set_ylabel('Percentage (%)', fontsize=12)
ax.set_xlabel('Platform', fontsize=12)
ax.set_title('Terminal Status Distribution by Platform', fontsize=14, fontweight='bold')
ax.legend(title='Terminal Status', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.grid(axis='y', alpha=0.3)

# Error rate comparison
ax = axes[1, 1]
bars = ax.bar(platform_errors['platform'], platform_errors['technical_error_rate'],
              color=['#e74c3c', '#f39c12'])
ax.set_ylabel('Technical Error Rate (%)', fontsize=12)
ax.set_title('Technical Error Rate by Platform', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(viz_dir / '07_platform_comparison.png', dpi=300, bbox_inches='tight')
print(f"Saved: {viz_dir / '07_platform_comparison.png'}")
plt.close()

# ============================================================================
# 7. MISSING DOCUMENT ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("7. MISSING DOCUMENT ANALYSIS")
print("="*80)

# Requests that hit S11 (docs missing)
docs_missing_requests = df[df['status_code'] == 'S11']['request_id'].unique()
docs_ready_requests = df[df['status_code'] == 'S10']['request_id'].unique()
docs_missing_only = set(docs_missing_requests) - set(docs_ready_requests)

print(f"\nRequests hitting S11 (Documents Missing): {len(docs_missing_requests)} ({len(docs_missing_requests)/len(terminal_statuses)*100:.1f}%)")
print(f"Requests with S10 (Documents Ready): {len(docs_ready_requests)} ({len(docs_ready_requests)/len(terminal_statuses)*100:.1f}%)")

# Success rate comparison
s10_success = terminal_statuses[terminal_statuses['request_id'].isin(docs_ready_requests)]
s11_success = terminal_statuses[terminal_statuses['request_id'].isin(docs_missing_requests)]

s10_success_rate = (s10_success['terminal_status'] == 'S40').mean() * 100
s11_success_rate = (s11_success['terminal_status'] == 'S40').mean() * 100

print(f"\nSuccess rate when docs ready (S10): {s10_success_rate:.2f}%")
print(f"Success rate when docs missing (S11): {s11_success_rate:.2f}%")

# Document retrieval outcomes
retrieval_starts = df[df['status_code'] == 'S12']['request_id'].unique()
retrieval_success = df[df['status_code'] == 'S13']['request_id'].unique()
retrieval_fail_network = df[df['status_code'] == 'S14']['request_id'].unique()
retrieval_fail_issuer = df[df['status_code'] == 'S15']['request_id'].unique()

print(f"\nDocument Retrieval Started (S12): {len(retrieval_starts)}")
print(f"  Success (S13): {len(retrieval_success)} ({len(retrieval_success)/len(retrieval_starts)*100:.1f}%)")
print(f"  Failed - Network (S14): {len(retrieval_fail_network)} ({len(retrieval_fail_network)/len(retrieval_starts)*100:.1f}%)")
print(f"  Failed - Issuer (S15): {len(retrieval_fail_issuer)} ({len(retrieval_fail_issuer)/len(retrieval_starts)*100:.1f}%)")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Success rate: S10 vs S11
ax = axes[0, 0]
bars = ax.bar(['Documents Ready\n(S10)', 'Documents Missing\n(S11)'],
              [s10_success_rate, s11_success_rate],
              color=['#2ecc71', '#e74c3c'])
ax.set_ylabel('Success Rate (%)', fontsize=12)
ax.set_title('Success Rate: Documents Ready vs Missing', fontsize=14, fontweight='bold')
ax.set_ylim(0, 100)
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

# Document retrieval outcomes
ax = axes[0, 1]
retrieval_outcomes = {
    'Success\n(S13)': len(retrieval_success),
    'Network Fail\n(S14)': len(retrieval_fail_network),
    'Issuer Fail\n(S15)': len(retrieval_fail_issuer)
}
bars = ax.bar(retrieval_outcomes.keys(), retrieval_outcomes.values(),
              color=['#2ecc71', '#f39c12', '#e74c3c'])
ax.set_ylabel('Number of Requests', fontsize=12)
ax.set_title('Document Retrieval Outcomes', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    pct = height / len(retrieval_starts) * 100
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Missing document count distribution
ax = axes[1, 0]
missing_dist = df[df['status_code'] == 'S11'].groupby('missing_count').size()
if len(missing_dist) > 0:
    bars = ax.bar(missing_dist.index, missing_dist.values, color='#e67e22')
    ax.set_xlabel('Number of Missing Documents', fontsize=12)
    ax.set_ylabel('Number of Requests', fontsize=12)
    ax.set_title('Distribution of Missing Document Count', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=10)

# Document availability flow
ax = axes[1, 1]
flow_data = {
    'Total Requests': len(terminal_statuses),
    'Docs Ready (S10)': len(docs_ready_requests),
    'Docs Missing (S11)': len(docs_missing_requests),
    'Retrieval Started (S12)': len(retrieval_starts),
    'Retrieval Success (S13)': len(retrieval_success)
}
bars = ax.barh(list(flow_data.keys()), list(flow_data.values()),
               color=['#3498db', '#2ecc71', '#e67e22', '#f39c12', '#27ae60'])
ax.set_xlabel('Number of Requests', fontsize=12)
ax.set_title('Document Availability Flow', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, (bar, val) in enumerate(zip(bars, flow_data.values())):
    ax.text(val, i, f' {val}', va='center', fontsize=10)

plt.tight_layout()
plt.savefig(viz_dir / '08_missing_document_analysis.png', dpi=300, bbox_inches='tight')
print(f"Saved: {viz_dir / '08_missing_document_analysis.png'}")
plt.close()

# ============================================================================
# 8. USER BEHAVIOR PATTERNS
# ============================================================================
print("\n" + "="*80)
print("8. USER BEHAVIOR PATTERNS")
print("="*80)

# Consent conversion (S20 -> S21 vs S22)
consent_shown = df[df['status_code'] == 'S20']['request_id'].unique()
consent_granted = df[df['status_code'] == 'S21']['request_id'].unique()
consent_denied = df[df['status_code'] == 'S22']['request_id'].unique()

consent_grant_rate = len(consent_granted) / len(consent_shown) * 100 if len(consent_shown) > 0 else 0
consent_deny_rate = len(consent_denied) / len(consent_shown) * 100 if len(consent_shown) > 0 else 0

print(f"\nConsent Screen Shown (S20): {len(consent_shown)}")
print(f"  Granted (S21): {len(consent_granted)} ({consent_grant_rate:.1f}%)")
print(f"  Denied (S22): {len(consent_denied)} ({consent_deny_rate:.1f}%)")

# PIN success (S30 -> S31 vs S32)
pin_required = df[df['status_code'] == 'S30']['request_id'].unique()
pin_success = df[df['status_code'] == 'S31']['request_id'].unique()
pin_failed = df[df['status_code'] == 'S32']['request_id'].unique()

pin_success_rate = len(pin_success) / len(pin_required) * 100 if len(pin_required) > 0 else 0
pin_fail_rate = len(pin_failed) / len(pin_required) * 100 if len(pin_required) > 0 else 0

print(f"\nPIN Required (S30): {len(pin_required)}")
print(f"  Success (S31): {len(pin_success)} ({pin_success_rate:.1f}%)")
print(f"  Failed (S32): {len(pin_failed)} ({pin_fail_rate:.1f}%)")

# User abandonment by status
abandonment_by_status = terminal_statuses[terminal_statuses['terminal_status'] == 'S43'].copy()
# Get the last non-terminal status before S43
abandonment_statuses = []
for req_id in abandonment_by_status['request_id']:
    req_journey = df[df['request_id'] == req_id].sort_values('status_ts')
    non_terminal = req_journey[~req_journey['status_code'].isin(['S43'])]['status_code'].values
    if len(non_terminal) > 0:
        abandonment_statuses.append(non_terminal[-1])
    else:
        abandonment_statuses.append('Unknown')

abandonment_dist = pd.Series(abandonment_statuses).value_counts()

print(f"\nUser Aborted (S43): {len(abandonment_by_status)}")
print("\nAbandonment by previous status:")
for status, count in abandonment_dist.head(10).items():
    print(f"  After {status} ({STATUS_DEFINITIONS.get(status, status)}): {count} ({count/len(abandonment_by_status)*100:.1f}%)")

# Time spent at critical decision points
critical_statuses = ['S20', 'S30']  # Consent and PIN
time_spent = {}
for status in critical_statuses:
    status_events = df[df['status_code'] == status].copy()
    if len(status_events) > 0:
        # Get next event for each
        next_latencies = []
        for req_id in status_events['request_id'].unique():
            req_df = df[df['request_id'] == req_id].sort_values('status_ts')
            status_idx = req_df[req_df['status_code'] == status].index[0]
            if status_idx + 1 < len(req_df):
                next_latency = req_df.loc[status_idx + 1, 'step_latency_ms']
                if pd.notna(next_latency):
                    next_latencies.append(next_latency / 1000)
        if next_latencies:
            time_spent[status] = np.mean(next_latencies)
            print(f"\nAverage time at {status} ({STATUS_DEFINITIONS.get(status, status)}): {time_spent[status]:.2f}s")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Consent conversion
ax = axes[0, 0]
consent_data = {
    'Granted': len(consent_granted),
    'Denied': len(consent_denied),
    'Other': len(consent_shown) - len(consent_granted) - len(consent_denied)
}
colors_consent = ['#2ecc71', '#e74c3c', '#95a5a6']
ax.pie([v for v in consent_data.values() if v > 0],
       labels=[k for k, v in consent_data.items() if v > 0],
       autopct='%1.1f%%', startangle=90, colors=colors_consent)
ax.set_title(f'Consent Screen Outcomes (n={len(consent_shown)})', fontsize=14, fontweight='bold')

# PIN success rate
ax = axes[0, 1]
pin_data = {
    'Success': len(pin_success),
    'Failed': len(pin_failed),
    'Other': len(pin_required) - len(pin_success) - len(pin_failed)
}
colors_pin = ['#2ecc71', '#e74c3c', '#95a5a6']
ax.pie([v for v in pin_data.values() if v > 0],
       labels=[k for k, v in pin_data.items() if v > 0],
       autopct='%1.1f%%', startangle=90, colors=colors_pin)
ax.set_title(f'PIN Entry Outcomes (n={len(pin_required)})', fontsize=14, fontweight='bold')

# Abandonment points
ax = axes[1, 0]
top_abandonment = abandonment_dist.head(10)
bars = ax.barh(range(len(top_abandonment)), top_abandonment.values, color='#e67e22')
ax.set_yticks(range(len(top_abandonment)))
ax.set_yticklabels([f"{status}\n{STATUS_DEFINITIONS.get(status, status)}" for status in top_abandonment.index],
                   fontsize=9)
ax.set_xlabel('Number of Abandonments', fontsize=12)
ax.set_title('Top 10 Abandonment Points (Status Before S43)', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, (bar, count) in enumerate(zip(bars, top_abandonment.values)):
    pct = count / len(abandonment_by_status) * 100
    ax.text(count, i, f' {count} ({pct:.1f}%)', va='center', fontsize=9)

# Time at critical decision points
ax = axes[1, 1]
if time_spent:
    bars = ax.bar(list(time_spent.keys()), list(time_spent.values()),
                  color=['#3498db', '#9b59b6'])
    ax.set_ylabel('Average Time (seconds)', fontsize=12)
    ax.set_xlabel('Status', fontsize=12)
    ax.set_title('Time Spent at Critical Decision Points', fontsize=14, fontweight='bold')
    ax.set_xticklabels([f"{status}\n{STATUS_DEFINITIONS.get(status, status)}" for status in time_spent.keys()])
    ax.grid(axis='y', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}s', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(viz_dir / '09_user_behavior_patterns.png', dpi=300, bbox_inches='tight')
print(f"Saved: {viz_dir / '09_user_behavior_patterns.png'}")
plt.close()

# ============================================================================
# 9. JOURNEY PATH ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("9. JOURNEY PATH ANALYSIS")
print("="*80)

# Get complete journey paths
journey_paths = terminal_statuses.merge(
    df.groupby('request_id')['status_history_list'].last().reset_index(),
    on='request_id'
)

# Convert journey paths to strings for grouping
journey_paths['journey_string'] = journey_paths['status_history_list'].apply(lambda x: ' -> '.join(x))

# Most common successful paths
successful_paths = journey_paths[journey_paths['terminal_status'] == 'S40']['journey_string'].value_counts()
print(f"\nMost common successful paths (Top 10):")
for path, count in successful_paths.head(10).items():
    print(f"  {count} requests: {path}")

# Most common failure paths
failure_paths = journey_paths[journey_paths['terminal_status'] != 'S40']['journey_string'].value_counts()
print(f"\nMost common failure paths (Top 10):")
for path, count in failure_paths.head(10).items():
    terminal = path.split(' -> ')[-1]
    print(f"  {count} requests ({terminal}): {path}")

# Journey length analysis
journey_paths['journey_length'] = journey_paths['status_history_list'].apply(len)
successful_lengths = journey_paths[journey_paths['terminal_status'] == 'S40']['journey_length']
failure_lengths = journey_paths[journey_paths['terminal_status'] != 'S40']['journey_length']

print(f"\nJourney Length Statistics:")
print(f"  Successful (S40): Mean={successful_lengths.mean():.2f}, Median={successful_lengths.median():.0f}, Min={successful_lengths.min()}, Max={successful_lengths.max()}")
print(f"  Failed: Mean={failure_lengths.mean():.2f}, Median={failure_lengths.median():.0f}, Min={failure_lengths.min()}, Max={failure_lengths.max()}")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Journey length distribution
ax = axes[0, 0]
ax.hist([successful_lengths, failure_lengths], bins=20, label=['Successful', 'Failed'],
        color=['#2ecc71', '#e74c3c'], alpha=0.7)
ax.set_xlabel('Journey Length (Number of Statuses)', fontsize=12)
ax.set_ylabel('Number of Requests', fontsize=12)
ax.set_title('Journey Length Distribution', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)

# Top successful path patterns
ax = axes[0, 1]
top_success = successful_paths.head(5)
bars = ax.barh(range(len(top_success)), top_success.values, color='#2ecc71')
ax.set_yticks(range(len(top_success)))
# Truncate long paths for display
ax.set_yticklabels([path[:50] + '...' if len(path) > 50 else path for path in top_success.index],
                   fontsize=8)
ax.set_xlabel('Number of Requests', fontsize=12)
ax.set_title('Top 5 Successful Journey Patterns', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, (bar, count) in enumerate(zip(bars, top_success.values)):
    ax.text(count, i, f' {count}', va='center', fontsize=10)

# Top failure path patterns
ax = axes[1, 0]
top_failure = failure_paths.head(5)
bars = ax.barh(range(len(top_failure)), top_failure.values, color='#e74c3c')
ax.set_yticks(range(len(top_failure)))
# Truncate long paths for display
ax.set_yticklabels([path[:50] + '...' if len(path) > 50 else path for path in top_failure.index],
                   fontsize=8)
ax.set_xlabel('Number of Requests', fontsize=12)
ax.set_title('Top 5 Failure Journey Patterns', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, (bar, count) in enumerate(zip(bars, top_failure.values)):
    ax.text(count, i, f' {count}', va='center', fontsize=10)

# Terminal status reached from each status (funnel)
ax = axes[1, 1]
# Get last non-terminal status before terminal
pre_terminal_statuses = []
for req_id in journey_paths['request_id']:
    req_journey = df[df['request_id'] == req_id].sort_values('status_ts')
    non_terminal = req_journey[~req_journey['status_code'].isin(TERMINAL_STATUSES)]['status_code'].values
    if len(non_terminal) > 0:
        pre_terminal_statuses.append(non_terminal[-1])
    else:
        pre_terminal_statuses.append('Unknown')

pre_terminal_dist = pd.Series(pre_terminal_statuses).value_counts().head(10)
bars = ax.barh(range(len(pre_terminal_dist)), pre_terminal_dist.values, color='#3498db')
ax.set_yticks(range(len(pre_terminal_dist)))
ax.set_yticklabels([f"{status}\n{STATUS_DEFINITIONS.get(status, status)}" for status in pre_terminal_dist.index],
                   fontsize=9)
ax.set_xlabel('Number of Requests', fontsize=12)
ax.set_title('Last Status Before Terminal (Top 10)', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, (bar, count) in enumerate(zip(bars, pre_terminal_dist.values)):
    ax.text(count, i, f' {count}', va='center', fontsize=10)

plt.tight_layout()
plt.savefig(viz_dir / '10_journey_path_analysis.png', dpi=300, bbox_inches='tight')
print(f"Saved: {viz_dir / '10_journey_path_analysis.png'}")
plt.close()

# ============================================================================
# 10. TIME-BASED ANALYSIS & LATENCY
# ============================================================================
print("\n" + "="*80)
print("10. TIME-BASED ANALYSIS & LATENCY")
print("="*80)

# Filter out zero latencies (first event in each request)
latency_data = df[df['step_latency_ms'] > 0].copy()
latency_data['step_latency_s'] = latency_data['step_latency_ms'] / 1000

print(f"\nLatency Statistics (all statuses):")
print(f"  Mean: {latency_data['step_latency_s'].mean():.2f}s")
print(f"  Median: {latency_data['step_latency_s'].median():.2f}s")
print(f"  95th percentile: {latency_data['step_latency_s'].quantile(0.95):.2f}s")
print(f"  Max: {latency_data['step_latency_s'].max():.2f}s")

# Average latency by status
latency_by_status = latency_data.groupby('status_code')['step_latency_s'].agg(['mean', 'median', 'count']).sort_values('mean', ascending=False)
print(f"\nTop 10 slowest status transitions (by mean latency):")
print(latency_by_status.head(10).to_string())

# Bottleneck identification (slowest steps)
bottlenecks = latency_by_status[latency_by_status['count'] >= 10].head(10)  # Min 10 occurrences

# Journey duration by outcome
successful_duration = terminal_statuses[terminal_statuses['terminal_status'] == 'S40']['journey_duration_ms'] / 1000
failed_duration = terminal_statuses[terminal_statuses['terminal_status'] != 'S40']['journey_duration_ms'] / 1000

print(f"\nJourney Duration by Outcome:")
print(f"  Successful (S40): Mean={successful_duration.mean():.2f}s, Median={successful_duration.median():.2f}s")
print(f"  Failed: Mean={failed_duration.mean():.2f}s, Median={failed_duration.median():.2f}s")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Latency distribution
ax = axes[0, 0]
ax.hist(latency_data['step_latency_s'], bins=50, color='#3498db', alpha=0.7, edgecolor='black')
ax.set_xlabel('Step Latency (seconds)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Step Latency Distribution (All Transitions)', fontsize=14, fontweight='bold')
ax.axvline(latency_data['step_latency_s'].median(), color='red', linestyle='--',
           label=f"Median: {latency_data['step_latency_s'].median():.2f}s")
ax.axvline(latency_data['step_latency_s'].mean(), color='orange', linestyle='--',
           label=f"Mean: {latency_data['step_latency_s'].mean():.2f}s")
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.set_xlim(0, min(latency_data['step_latency_s'].quantile(0.99), 100))  # Cap at 99th percentile or 100s

# Top bottlenecks
ax = axes[0, 1]
bars = ax.barh(range(len(bottlenecks)), bottlenecks['mean'].values, color='#e74c3c')
ax.set_yticks(range(len(bottlenecks)))
ax.set_yticklabels([f"{status}\n{STATUS_DEFINITIONS.get(status, status)}" for status in bottlenecks.index],
                   fontsize=9)
ax.set_xlabel('Mean Latency (seconds)', fontsize=12)
ax.set_title('Top 10 Bottlenecks (Slowest Transitions)', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, (bar, latency) in enumerate(zip(bars, bottlenecks['mean'].values)):
    ax.text(latency, i, f' {latency:.1f}s', va='center', fontsize=9)

# Journey duration by outcome
ax = axes[1, 0]
bp = ax.boxplot([successful_duration, failed_duration], labels=['Successful\n(S40)', 'Failed'],
                patch_artist=True, showmeans=True)
bp['boxes'][0].set_facecolor('#2ecc71')
bp['boxes'][1].set_facecolor('#e74c3c')
ax.set_ylabel('Journey Duration (seconds)', fontsize=12)
ax.set_title('Journey Duration: Success vs Failure', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, min(terminal_statuses['journey_duration_ms'].quantile(0.99) / 1000, 200))

# Latency correlation with success/failure
ax = axes[1, 1]
# Get average latency per request
request_avg_latency = latency_data.groupby('request_id')['step_latency_s'].mean().reset_index()
request_avg_latency = request_avg_latency.merge(terminal_statuses[['request_id', 'terminal_status']], on='request_id')
request_avg_latency['outcome'] = request_avg_latency['terminal_status'].apply(lambda x: 'Success' if x == 'S40' else 'Failure')

success_latencies = request_avg_latency[request_avg_latency['outcome'] == 'Success']['step_latency_s']
failure_latencies = request_avg_latency[request_avg_latency['outcome'] == 'Failure']['step_latency_s']

ax.hist([success_latencies, failure_latencies], bins=30,
        label=['Successful', 'Failed'], color=['#2ecc71', '#e74c3c'], alpha=0.7)
ax.set_xlabel('Average Step Latency per Request (seconds)', fontsize=12)
ax.set_ylabel('Number of Requests', fontsize=12)
ax.set_title('Average Latency Distribution by Outcome', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.set_xlim(0, min(request_avg_latency['step_latency_s'].quantile(0.99), 50))

plt.tight_layout()
plt.savefig(viz_dir / '11_time_latency_analysis.png', dpi=300, bbox_inches='tight')
print(f"Saved: {viz_dir / '11_time_latency_analysis.png'}")
plt.close()

# ============================================================================
# 11. CONVERSION FUNNEL ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("11. CONVERSION FUNNEL ANALYSIS")
print("="*80)

# Define key funnel stages
funnel_stages = {
    'S00': 'Request Created',
    'S08': 'Request Loaded',
    'S10/S11': 'Doc Check Complete',
    'S20': 'Consent Shown',
    'S21': 'Consent Granted',
    'S30': 'PIN Required',
    'S31': 'PIN Success',
    'S40': 'Success (Shared)'
}

funnel_data = {}
for stage, label in funnel_stages.items():
    if '/' in stage:
        # Handle S10/S11 (either one)
        codes = stage.split('/')
        count = df[df['status_code'].isin(codes)]['request_id'].nunique()
    else:
        count = df[df['status_code'] == stage]['request_id'].nunique()
    funnel_data[label] = count

# Convert to list maintaining order
funnel_labels = list(funnel_data.keys())
funnel_values = list(funnel_data.values())
funnel_pct = [v / funnel_values[0] * 100 for v in funnel_values]

print("\nConversion Funnel:")
for label, value, pct in zip(funnel_labels, funnel_values, funnel_pct):
    drop_from_prev = ""
    if label != funnel_labels[0]:
        prev_idx = funnel_labels.index(label) - 1
        drop = (funnel_values[prev_idx] - value) / funnel_values[prev_idx] * 100
        drop_from_prev = f" (-{drop:.1f}% from previous)"
    print(f"  {label}: {value} ({pct:.1f}% of total){drop_from_prev}")

fig, ax = plt.subplots(figsize=(14, 8))

# Create funnel visualization
y_pos = np.arange(len(funnel_labels))
colors_funnel = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(funnel_labels)))

bars = ax.barh(y_pos, funnel_values, color=colors_funnel)
ax.set_yticks(y_pos)
ax.set_yticklabels(funnel_labels, fontsize=11)
ax.invert_yaxis()
ax.set_xlabel('Number of Requests', fontsize=12)
ax.set_title('Sharing Request Conversion Funnel', fontsize=16, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Add value and percentage labels
for i, (bar, value, pct) in enumerate(zip(bars, funnel_values, funnel_pct)):
    # Drop rate from previous
    drop_text = ""
    if i > 0:
        drop = (funnel_values[i-1] - value) / funnel_values[i-1] * 100
        if drop > 0:
            drop_text = f" (down{drop:.1f}%)"

    ax.text(value, i, f' {value} ({pct:.1f}%){drop_text}',
            va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(viz_dir / '12_conversion_funnel.png', dpi=300, bbox_inches='tight')
print(f"Saved: {viz_dir / '12_conversion_funnel.png'}")
plt.close()

# ============================================================================
# GENERATE KEY STATISTICS FOR REPORT
# ============================================================================
print("\n" + "="*80)
print("GENERATING SUMMARY STATISTICS FOR REPORT")
print("="*80)

# Calculate all key statistics
stats = {
    'dataset': {
        'total_events': len(df),
        'unique_requests': df['request_id'].nunique(),
        'unique_sps': df['sp_id'].nunique(),
        'date_range': f"{df['status_ts'].min()} to {df['status_ts'].max()}",
        'channels': df['channel'].unique().tolist(),
        'platforms': df['platform'].unique().tolist()
    },
    'overall_performance': {
        'success_rate': (terminal_statuses['terminal_status'] == 'S40').mean() * 100,
        'technical_error_rate': (terminal_statuses['terminal_status'] == 'S41').mean() * 100,
        'expired_rate': (terminal_statuses['terminal_status'] == 'S42').mean() * 100,
        'user_aborted_rate': (terminal_statuses['terminal_status'] == 'S43').mean() * 100,
        'not_eligible_rate': (terminal_statuses['terminal_status'] == 'S44').mean() * 100,
        'avg_journey_time_success_s': terminal_statuses[terminal_statuses['terminal_status'] == 'S40']['journey_duration_ms'].mean() / 1000,
        'avg_journey_time_failed_s': terminal_statuses[terminal_statuses['terminal_status'] != 'S40']['journey_duration_ms'].mean() / 1000
    },
    'channel_performance': channel_perf.to_dict('records'),
    'platform_performance': platform_perf.to_dict('records'),
    'document_availability': {
        'docs_ready_count': len(docs_ready_requests),
        'docs_missing_count': len(docs_missing_requests),
        'success_rate_docs_ready': s10_success_rate,
        'success_rate_docs_missing': s11_success_rate,
        'retrieval_success_rate': len(retrieval_success) / len(retrieval_starts) * 100 if len(retrieval_starts) > 0 else 0
    },
    'user_behavior': {
        'consent_grant_rate': consent_grant_rate,
        'consent_deny_rate': consent_deny_rate,
        'pin_success_rate': pin_success_rate,
        'pin_fail_rate': pin_fail_rate
    },
    'top_sps': sp_perf.nlargest(10, 'total_requests').to_dict('records'),
    'bottom_sps': sp_perf[sp_perf['total_requests'] >= 5].nsmallest(5, 'success_rate').to_dict('records')
}

print("\nAll statistics calculated and ready for report generation.")
print(f"\nTotal visualizations created: 12")
print(f"Output directory: {viz_dir}")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\nNext steps:")
print("1. Review visualizations in D:\\cluade\\visualizations\\")
print("2. Generate comprehensive markdown report")
print("3. Create interactive dashboard")
print("4. Generate insights document")
