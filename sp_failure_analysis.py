"""
Service Provider (SP) Specific Failure Pattern Analysis
========================================================
Analyzes sharing transaction data to identify SP-specific bottlenecks,
failure patterns, and performance issues.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory
output_dir = Path(r"D:\cluade\visualizations\sp_analysis")
output_dir.mkdir(parents=True, exist_ok=True)

print("Loading data...")
df = pd.read_csv(r"D:\cluade\sharing_transactions_new_sample.csv")

print(f"Total rows: {len(df):,}")
print(f"Columns: {list(df.columns)}")

# Get terminal statuses for each request
terminal_df = df.sort_values(['request_id', 'status_ts']).groupby('request_id').last().reset_index()

print(f"\nTotal unique requests: {len(terminal_df):,}")
print(f"Terminal status distribution:\n{terminal_df['status_code'].value_counts()}")

# Calculate SP-level metrics
sp_metrics = []

for sp_id in terminal_df['sp_id'].unique():
    sp_data = terminal_df[terminal_df['sp_id'] == sp_id].copy()

    total = len(sp_data)
    success = len(sp_data[sp_data['status_code'] == 'S40'])
    s41 = len(sp_data[sp_data['status_code'] == 'S41'])
    s42 = len(sp_data[sp_data['status_code'] == 'S42'])
    s43 = len(sp_data[sp_data['status_code'] == 'S43'])
    s44 = len(sp_data[sp_data['status_code'] == 'S44'])

    # Calculate journey times for failures only
    failed = sp_data[sp_data['status_code'] != 'S40']

    # Get most common stuck status (previous_status before terminal failure)
    if len(failed) > 0:
        stuck_at = failed['previous_status'].mode()[0] if not failed['previous_status'].isna().all() else 'Unknown'
    else:
        stuck_at = 'N/A'

    # Error source distribution
    error_sources = sp_data[sp_data['error_source'].notna()]['error_source'].value_counts().to_dict()

    sp_metrics.append({
        'sp_id': sp_id,
        'total_requests': total,
        'success_count': success,
        'success_rate': success / total * 100 if total > 0 else 0,
        's41_count': s41,
        's41_rate': s41 / total * 100 if total > 0 else 0,
        's42_count': s42,
        's42_rate': s42 / total * 100 if total > 0 else 0,
        's43_count': s43,
        's43_rate': s43 / total * 100 if total > 0 else 0,
        's44_count': s44,
        's44_rate': s44 / total * 100 if total > 0 else 0,
        'failure_count': total - success,
        'failure_rate': (total - success) / total * 100 if total > 0 else 0,
        'most_common_stuck_status': stuck_at,
        'avg_time_to_failure': failed['status_ts'].apply(pd.to_datetime).max() - failed['status_ts'].apply(pd.to_datetime).min() if len(failed) > 0 else pd.Timedelta(0),
        'issuer_errors': error_sources.get('issuer', 0),
        'network_errors': error_sources.get('network', 0),
        'dv_errors': error_sources.get('dv', 0),
        'user_cancel_errors': error_sources.get('user_cancel', 0)
    })

sp_metrics_df = pd.DataFrame(sp_metrics)
sp_metrics_df = sp_metrics_df.sort_values('total_requests', ascending=False)

print("\n" + "="*80)
print("SP METRICS SUMMARY")
print("="*80)
print(sp_metrics_df.to_string())

# Save SP metrics
sp_metrics_df.to_csv(output_dir / 'sp_metrics_summary.csv', index=False)
print(f"\nSaved: {output_dir / 'sp_metrics_summary.csv'}")

# ============================================================================
# VISUALIZATION 1: SP Failure Mode Heatmap
# ============================================================================
print("\n\nGenerating Visualization 1: SP Failure Mode Heatmap...")

failure_cols = ['s41_count', 's42_count', 's43_count', 's44_count']
heatmap_data = sp_metrics_df[['sp_id'] + failure_cols].set_index('sp_id')
heatmap_data.columns = ['S41 Tech Error', 'S42 Expired', 'S43 User Abort', 'S44 Not Eligible']

# Sort by total failures
heatmap_data['total'] = heatmap_data.sum(axis=1)
heatmap_data = heatmap_data.sort_values('total', ascending=False).drop('total', axis=1)

fig, ax = plt.subplots(figsize=(12, max(8, len(heatmap_data) * 0.4)))
sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='Reds',
            cbar_kws={'label': 'Failure Count'}, ax=ax, linewidths=0.5)
ax.set_title('SP Failure Mode Heatmap\n(Sorted by Total Failures - Worst at Top)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Failure Type', fontsize=12, fontweight='bold')
ax.set_ylabel('Service Provider', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(output_dir / 'sp_failure_heatmap.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / 'sp_failure_heatmap.png'}")
plt.close()

# ============================================================================
# VISUALIZATION 2: SP Abandonment Analysis - Stacked Bar Chart
# ============================================================================
print("\nGenerating Visualization 2: SP Abandonment Stacked Bar Chart...")

# Sort by user abort rate
sp_metrics_sorted = sp_metrics_df.sort_values('s43_rate', ascending=True)

fig, ax = plt.subplots(figsize=(14, max(8, len(sp_metrics_sorted) * 0.4)))

# Create stacked bar
y_pos = np.arange(len(sp_metrics_sorted))
s40 = sp_metrics_sorted['success_count'].values
s43 = sp_metrics_sorted['s43_count'].values
s42 = sp_metrics_sorted['s42_count'].values
s41 = sp_metrics_sorted['s41_count'].values
s44 = sp_metrics_sorted['s44_count'].values

p1 = ax.barh(y_pos, s40, label='S40 Success', color='#2ecc71')
p2 = ax.barh(y_pos, s43, left=s40, label='S43 User Abort', color='#e74c3c')
p3 = ax.barh(y_pos, s42, left=s40+s43, label='S42 Expired', color='#f39c12')
p4 = ax.barh(y_pos, s41, left=s40+s43+s42, label='S41 Tech Error', color='#9b59b6')
p5 = ax.barh(y_pos, s44, left=s40+s43+s42+s41, label='S44 Not Eligible', color='#95a5a6')

# Add percentage annotations for user abort
for i, (sp, abort_rate) in enumerate(zip(sp_metrics_sorted['sp_id'], sp_metrics_sorted['s43_rate'])):
    if abort_rate > 5:  # Only annotate significant abort rates
        ax.text(sp_metrics_sorted.iloc[i]['total_requests'] + 50, i,
                f"{abort_rate:.1f}% abort",
                va='center', fontsize=8, color='red', fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(sp_metrics_sorted['sp_id'])
ax.set_xlabel('Request Count', fontsize=12, fontweight='bold')
ax.set_ylabel('Service Provider', fontsize=12, fontweight='bold')
ax.set_title('SP Request Outcomes - Stacked View\n(Sorted by User Abort Rate - Highest at Bottom)',
             fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='lower right', fontsize=10)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'sp_abandonment_stacked.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / 'sp_abandonment_stacked.png'}")
plt.close()

# ============================================================================
# VISUALIZATION 3: Critical Drop-off Points by SP
# ============================================================================
print("\nGenerating Visualization 3: Critical Drop-off Points by SP...")

# Get top 10 SPs by volume
top_sps = sp_metrics_df.nlargest(10, 'total_requests')['sp_id'].values

fig, axes = plt.subplots(2, 5, figsize=(20, 10))
axes = axes.flatten()

for idx, sp_id in enumerate(top_sps):
    sp_terminal = terminal_df[terminal_df['sp_id'] == sp_id]
    failed = sp_terminal[sp_terminal['status_code'] != 'S40']

    if len(failed) > 0:
        # Get distribution of last status before failure
        stuck_dist = failed['previous_status'].value_counts().head(8)

        axes[idx].barh(range(len(stuck_dist)), stuck_dist.values, color='coral')
        axes[idx].set_yticks(range(len(stuck_dist)))
        axes[idx].set_yticklabels(stuck_dist.index, fontsize=9)
        axes[idx].set_xlabel('Failure Count', fontsize=9)
        axes[idx].set_title(f'{sp_id}\n({len(failed)} failures)',
                           fontsize=11, fontweight='bold')
        axes[idx].grid(axis='x', alpha=0.3)
    else:
        axes[idx].text(0.5, 0.5, 'No failures', ha='center', va='center',
                      transform=axes[idx].transAxes, fontsize=12)
        axes[idx].set_title(f'{sp_id}\n(No failures)', fontsize=11, fontweight='bold')
        axes[idx].axis('off')

plt.suptitle('Where Do Users Get Stuck? (Last Status Before Failure)\nTop 10 SPs by Volume',
             fontsize=16, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig(output_dir / 'sp_dropoff_points.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / 'sp_dropoff_points.png'}")
plt.close()

# ============================================================================
# VISUALIZATION 4: SP Journey Completion Funnel Comparison
# ============================================================================
print("\nGenerating Visualization 4: SP Journey Funnel Comparison...")

# Calculate funnel conversion for each SP
funnel_stages = ['S00', 'S08', 'S20', 'S21', 'S30', 'S31', 'S40']
sp_funnels = []

for sp_id in terminal_df['sp_id'].unique():
    sp_all_data = df[df['sp_id'] == sp_id]

    funnel_counts = []
    for stage in funnel_stages:
        count = sp_all_data[sp_all_data['status_code'] == stage]['request_id'].nunique()
        funnel_counts.append(count)

    sp_funnels.append({
        'sp_id': sp_id,
        'success_rate': sp_metrics_df[sp_metrics_df['sp_id'] == sp_id]['success_rate'].values[0],
        'funnel': funnel_counts
    })

sp_funnels_df = pd.DataFrame(sp_funnels)
sp_funnels_df = sp_funnels_df.sort_values('success_rate', ascending=False)

# Get top 5 best and worst
top_5_best = sp_funnels_df.head(5)
top_5_worst = sp_funnels_df.tail(5)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Plot best performers
for idx, row in top_5_best.iterrows():
    # Normalize to percentages
    funnel = np.array(row['funnel'])
    if funnel[0] > 0:
        funnel_pct = (funnel / funnel[0]) * 100
    else:
        funnel_pct = funnel
    ax1.plot(funnel_stages, funnel_pct, marker='o', linewidth=2,
             label=f"{row['sp_id']} ({row['success_rate']:.1f}%)", markersize=8)

ax1.set_xlabel('Journey Stage', fontsize=12, fontweight='bold')
ax1.set_ylabel('Retention Rate (%)', fontsize=12, fontweight='bold')
ax1.set_title('Top 5 Best Performers\n(Journey Completion Funnel)',
              fontsize=14, fontweight='bold', color='green')
ax1.legend(fontsize=9, loc='lower left')
ax1.grid(True, alpha=0.3)
ax1.set_ylim([0, 105])

# Plot worst performers
for idx, row in top_5_worst.iterrows():
    funnel = np.array(row['funnel'])
    if funnel[0] > 0:
        funnel_pct = (funnel / funnel[0]) * 100
    else:
        funnel_pct = funnel
    ax2.plot(funnel_stages, funnel_pct, marker='o', linewidth=2,
             label=f"{row['sp_id']} ({row['success_rate']:.1f}%)", markersize=8)

ax2.set_xlabel('Journey Stage', fontsize=12, fontweight='bold')
ax2.set_ylabel('Retention Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title('Top 5 Worst Performers\n(Journey Completion Funnel)',
              fontsize=14, fontweight='bold', color='red')
ax2.legend(fontsize=9, loc='lower left')
ax2.grid(True, alpha=0.3)
ax2.set_ylim([0, 105])

plt.suptitle('SP Journey Funnel Comparison: Best vs Worst',
             fontsize=16, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig(output_dir / 'sp_funnel_comparison.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / 'sp_funnel_comparison.png'}")
plt.close()

# ============================================================================
# VISUALIZATION 5: SP Error Source Matrix
# ============================================================================
print("\nGenerating Visualization 5: SP Error Source Matrix...")

error_cols = ['issuer_errors', 'network_errors', 'dv_errors', 'user_cancel_errors']
error_matrix = sp_metrics_df[['sp_id'] + error_cols].set_index('sp_id')
error_matrix.columns = ['Issuer', 'Network', 'DV Backend', 'User Cancel']

# Sort by total errors
error_matrix['total'] = error_matrix.sum(axis=1)
error_matrix = error_matrix[error_matrix['total'] > 0].sort_values('total', ascending=False).drop('total', axis=1)

fig, ax = plt.subplots(figsize=(10, max(8, len(error_matrix) * 0.4)))
sns.heatmap(error_matrix, annot=True, fmt='g', cmap='YlOrRd',
            cbar_kws={'label': 'Error Count'}, ax=ax, linewidths=0.5)
ax.set_title('SP Error Source Matrix\n(Root Cause: Where Are Errors Coming From?)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Error Source', fontsize=12, fontweight='bold')
ax.set_ylabel('Service Provider', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(output_dir / 'sp_error_source_matrix.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / 'sp_error_source_matrix.png'}")
plt.close()

# ============================================================================
# VISUALIZATION 6: SP Performance Scatter Plot
# ============================================================================
print("\nGenerating Visualization 6: SP Performance Scatter Plot...")

fig, ax = plt.subplots(figsize=(14, 10))

# Calculate average journey time per SP (approximate using terminal status timestamp range)
sp_journey_times = []
for sp_id in terminal_df['sp_id'].unique():
    sp_data = df[df['sp_id'] == sp_id]
    # Group by request and calculate journey duration
    journey_times = []
    for req_id in sp_data['request_id'].unique():
        req_data = sp_data[sp_data['request_id'] == req_id]
        if len(req_data) > 1:
            start = pd.to_datetime(req_data['status_ts'].min())
            end = pd.to_datetime(req_data['status_ts'].max())
            duration = (end - start).total_seconds()
            journey_times.append(duration)

    avg_time = np.mean(journey_times) if journey_times else 0
    sp_journey_times.append({'sp_id': sp_id, 'avg_journey_time_sec': avg_time})

journey_df = pd.DataFrame(sp_journey_times)
sp_metrics_with_time = sp_metrics_df.merge(journey_df, on='sp_id')

# Create scatter plot
scatter = ax.scatter(sp_metrics_with_time['total_requests'],
                     sp_metrics_with_time['success_rate'],
                     s=sp_metrics_with_time['total_requests'] * 0.5,  # Bubble size
                     c=sp_metrics_with_time['avg_journey_time_sec'],
                     cmap='coolwarm', alpha=0.6, edgecolors='black', linewidth=1)

# Add SP labels
for idx, row in sp_metrics_with_time.iterrows():
    ax.annotate(row['sp_id'],
                (row['total_requests'], row['success_rate']),
                fontsize=9, fontweight='bold',
                xytext=(5, 5), textcoords='offset points')

# Add quadrant lines
ax.axhline(y=sp_metrics_with_time['success_rate'].median(),
           color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.axvline(x=sp_metrics_with_time['total_requests'].median(),
           color='gray', linestyle='--', alpha=0.5, linewidth=1)

# Quadrant labels
ax.text(0.98, 0.98, 'High Volume\nHigh Success\n(IDEAL)',
        transform=ax.transAxes, ha='right', va='top',
        fontsize=10, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
ax.text(0.02, 0.98, 'Low Volume\nHigh Success\n(Niche Good)',
        transform=ax.transAxes, ha='left', va='top',
        fontsize=10, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
ax.text(0.98, 0.02, 'High Volume\nLow Success\n(CRITICAL)',
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=10, bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
ax.text(0.02, 0.02, 'Low Volume\nLow Success\n(Investigate)',
        transform=ax.transAxes, ha='left', va='bottom',
        fontsize=10, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))

ax.set_xlabel('Request Volume (Total Requests)', fontsize=12, fontweight='bold')
ax.set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('SP Performance Matrix\n(Bubble Size = Volume, Color = Avg Journey Time)',
             fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Avg Journey Time (seconds)', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / 'sp_performance_scatter.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / 'sp_performance_scatter.png'}")
plt.close()

# ============================================================================
# VISUALIZATION 7: Time-to-Failure by SP
# ============================================================================
print("\nGenerating Visualization 7: Time-to-Failure by SP...")

# Calculate time to failure for each request
failure_times = []

for req_id in terminal_df[terminal_df['status_code'] != 'S40']['request_id']:
    req_data = df[df['request_id'] == req_id].sort_values('status_ts')
    if len(req_data) > 1:
        start = pd.to_datetime(req_data['status_ts'].iloc[0])
        end = pd.to_datetime(req_data['status_ts'].iloc[-1])
        duration_sec = (end - start).total_seconds()

        terminal_status = req_data['status_code'].iloc[-1]
        sp_id = req_data['sp_id'].iloc[0]

        failure_times.append({
            'request_id': req_id,
            'sp_id': sp_id,
            'terminal_status': terminal_status,
            'time_to_failure_sec': duration_sec
        })

failure_times_df = pd.DataFrame(failure_times)

# Get top SPs by failure count
top_failure_sps = sp_metrics_df.nlargest(10, 'failure_count')['sp_id'].values
failure_times_subset = failure_times_df[failure_times_df['sp_id'].isin(top_failure_sps)]

if len(failure_times_subset) > 0:
    fig, ax = plt.subplots(figsize=(14, 10))

    # Create violin plot
    sns.violinplot(data=failure_times_subset, y='sp_id', x='time_to_failure_sec',
                   hue='terminal_status', ax=ax, inner='box', cut=0)

    ax.set_xlabel('Time to Failure (seconds)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Service Provider', fontsize=12, fontweight='bold')
    ax.set_title('Time-to-Failure Distribution by SP and Failure Type\n(Top 10 SPs by Failure Count)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(title='Failure Type', fontsize=9, title_fontsize=10, loc='upper right')
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'sp_time_to_failure.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir / 'sp_time_to_failure.png'}")
    plt.close()
else:
    print("No failure time data available for visualization 7")

# ============================================================================
# VISUALIZATION 8: SP Missing Document Handling Performance
# ============================================================================
print("\nGenerating Visualization 8: SP Missing Document Handling...")

# Identify requests with missing documents (S11 status)
missing_doc_requests = df[df['status_code'] == 'S11']['request_id'].unique()

sp_missing_doc_perf = []

for sp_id in terminal_df['sp_id'].unique():
    sp_missing = terminal_df[
        (terminal_df['sp_id'] == sp_id) &
        (terminal_df['request_id'].isin(missing_doc_requests))
    ]

    if len(sp_missing) > 0:
        total_missing = len(sp_missing)
        successful_retrieval = len(sp_missing[sp_missing['status_code'] == 'S40'])
        gave_up = len(sp_missing[sp_missing['status_code'] == 'S44'])
        other_failures = len(sp_missing[~sp_missing['status_code'].isin(['S40', 'S44'])])

        sp_missing_doc_perf.append({
            'sp_id': sp_id,
            'total_missing_starts': total_missing,
            'successful_retrieval': successful_retrieval,
            'gave_up_s44': gave_up,
            'other_failures': other_failures,
            'success_rate': successful_retrieval / total_missing * 100 if total_missing > 0 else 0
        })

if sp_missing_doc_perf:
    missing_doc_df = pd.DataFrame(sp_missing_doc_perf)
    missing_doc_df = missing_doc_df[missing_doc_df['total_missing_starts'] >= 5]  # Min 5 cases
    missing_doc_df = missing_doc_df.sort_values('success_rate', ascending=True)

    if len(missing_doc_df) > 0:
        fig, ax = plt.subplots(figsize=(12, max(6, len(missing_doc_df) * 0.4)))

        x = np.arange(len(missing_doc_df))
        width = 0.25

        p1 = ax.bar(x - width, missing_doc_df['successful_retrieval'], width,
                   label='Successful Retrieval (S40)', color='#2ecc71')
        p2 = ax.bar(x, missing_doc_df['gave_up_s44'], width,
                   label='Gave Up (S44)', color='#e74c3c')
        p3 = ax.bar(x + width, missing_doc_df['other_failures'], width,
                   label='Other Failures', color='#f39c12')

        ax.set_ylabel('Request Count', fontsize=12, fontweight='bold')
        ax.set_xlabel('Service Provider', fontsize=12, fontweight='bold')
        ax.set_title('Missing Document Handling Performance by SP\n(Requests Starting with S11 - Missing Docs)',
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(missing_doc_df['sp_id'], rotation=45, ha='right')
        ax.legend(fontsize=10)
        ax.grid(axis='y', alpha=0.3)

        # Add success rate labels
        for i, (sp, rate) in enumerate(zip(missing_doc_df['sp_id'], missing_doc_df['success_rate'])):
            ax.text(i, missing_doc_df.iloc[i]['total_missing_starts'] + 1,
                   f"{rate:.1f}%", ha='center', va='bottom', fontsize=8, fontweight='bold')

        plt.tight_layout()
        plt.savefig(output_dir / 'sp_missing_doc_handling.png', dpi=300, bbox_inches='tight')
        print(f"Saved: {output_dir / 'sp_missing_doc_handling.png'}")
        plt.close()
    else:
        print("No SPs with sufficient missing doc cases for visualization 8")
else:
    print("No missing document data found for visualization 8")

# ============================================================================
# VISUALIZATION 9: Top 10 Worst SP Deep Dive Dashboard
# ============================================================================
print("\nGenerating Visualization 9: Top 10 Worst SP Deep Dive...")

worst_10_sps = sp_metrics_df.nsmallest(10, 'success_rate')

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 5, hspace=0.4, wspace=0.3)

for idx, (_, sp_row) in enumerate(worst_10_sps.iterrows()):
    row = idx // 5
    col = idx % 5

    # Create 2 subplots per SP (pie chart + bar chart)
    ax_pie = fig.add_subplot(gs[row*2//3:row*2//3+1, col])

    sp_id = sp_row['sp_id']
    sp_data = terminal_df[terminal_df['sp_id'] == sp_id]

    # Failure breakdown pie chart
    failure_breakdown = {
        'S41 Tech': sp_row['s41_count'],
        'S42 Expire': sp_row['s42_count'],
        'S43 Abort': sp_row['s43_count'],
        'S44 Inelig': sp_row['s44_count']
    }

    colors_pie = ['#9b59b6', '#f39c12', '#e74c3c', '#95a5a6']
    sizes = [v for v in failure_breakdown.values() if v > 0]
    labels = [k for k, v in failure_breakdown.items() if v > 0]

    if sizes:
        ax_pie.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90,
                  colors=colors_pie[:len(sizes)], textprops={'fontsize': 7})
    ax_pie.set_title(f"{sp_id}\n{sp_row['success_rate']:.1f}% success\n({sp_row['total_requests']} reqs)",
                    fontsize=10, fontweight='bold')

plt.suptitle('Top 10 Worst Performing SPs - Failure Breakdown',
             fontsize=18, fontweight='bold', y=0.98)

plt.savefig(output_dir / 'sp_top10_worst_dashboard.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / 'sp_top10_worst_dashboard.png'}")
plt.close()

# ============================================================================
# VISUALIZATION 10: SP Consent & PIN Success Rates
# ============================================================================
print("\nGenerating Visualization 10: SP Consent & PIN Success Rates...")

sp_consent_pin = []

for sp_id in df['sp_id'].unique():
    sp_data = df[df['sp_id'] == sp_id]

    # Consent conversion: reached S20 → completed S21
    reached_s20 = sp_data[sp_data['status_code'] == 'S20']['request_id'].nunique()
    completed_s21 = sp_data[sp_data['status_code'] == 'S21']['request_id'].nunique()
    consent_rate = (completed_s21 / reached_s20 * 100) if reached_s20 > 0 else np.nan

    # PIN success: reached S30 → completed S31
    reached_s30 = sp_data[sp_data['status_code'] == 'S30']['request_id'].nunique()
    completed_s31 = sp_data[sp_data['status_code'] == 'S31']['request_id'].nunique()
    pin_rate = (completed_s31 / reached_s30 * 100) if reached_s30 > 0 else np.nan

    sp_consent_pin.append({
        'sp_id': sp_id,
        'consent_conversion_rate': consent_rate,
        'pin_success_rate': pin_rate,
        'combined_score': np.nanmean([consent_rate, pin_rate]) if not np.isnan([consent_rate, pin_rate]).all() else 0,
        'reached_s20': reached_s20,
        'reached_s30': reached_s30
    })

consent_pin_df = pd.DataFrame(sp_consent_pin)
# Filter SPs with at least 10 consent attempts and 10 PIN attempts
consent_pin_df = consent_pin_df[
    (consent_pin_df['reached_s20'] >= 10) &
    (consent_pin_df['reached_s30'] >= 10)
].sort_values('combined_score', ascending=True)

if len(consent_pin_df) > 0:
    fig, ax = plt.subplots(figsize=(14, max(8, len(consent_pin_df) * 0.4)))

    x = np.arange(len(consent_pin_df))
    width = 0.35

    p1 = ax.barh(x - width/2, consent_pin_df['consent_conversion_rate'], width,
                label='Consent Conversion (S20→S21)', color='#3498db')
    p2 = ax.barh(x + width/2, consent_pin_df['pin_success_rate'], width,
                label='PIN Success (S30→S31)', color='#e67e22')

    # Add overall average lines
    overall_consent = consent_pin_df['consent_conversion_rate'].mean()
    overall_pin = consent_pin_df['pin_success_rate'].mean()
    ax.axvline(overall_consent, color='#3498db', linestyle='--', alpha=0.5, linewidth=2,
              label=f'Avg Consent: {overall_consent:.1f}%')
    ax.axvline(overall_pin, color='#e67e22', linestyle='--', alpha=0.5, linewidth=2,
              label=f'Avg PIN: {overall_pin:.1f}%')

    ax.set_yticks(x)
    ax.set_yticklabels(consent_pin_df['sp_id'])
    ax.set_xlabel('Success Rate (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Service Provider', fontsize=12, fontweight='bold')
    ax.set_title('SP Consent & PIN Success Rate Comparison\n(Sorted by Combined Score - Lowest at Bottom)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=10, loc='lower right')
    ax.grid(axis='x', alpha=0.3)
    ax.set_xlim([0, 105])

    plt.tight_layout()
    plt.savefig(output_dir / 'sp_consent_pin_comparison.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir / 'sp_consent_pin_comparison.png'}")
    plt.close()
else:
    print("No SPs with sufficient consent/PIN data for visualization 10")

print("\n" + "="*80)
print("ALL VISUALIZATIONS COMPLETED")
print("="*80)
print(f"Output directory: {output_dir}")
print("\nGenerated files:")
for f in sorted(output_dir.glob('*.png')):
    print(f"  - {f.name}")
print(f"  - sp_metrics_summary.csv")
