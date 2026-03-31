"""
UAE PASS Digital Documents - Sharing Transactions Visualization Suite
Creates comprehensive visualizations for sharing request analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# UAE PASS brand colors (blues/teals)
BRAND_COLORS = {
    'primary': '#0066CC',      # UAE PASS blue
    'secondary': '#00A3A1',    # Teal
    'success': '#00C853',      # Green
    'warning': '#FFA000',      # Amber
    'error': '#D32F2F',        # Red
    'neutral': '#757575',      # Gray
    'light_blue': '#64B5F6',
    'light_teal': '#4DB6AC',
    'dark_blue': '#003D7A'
}

# Status code definitions
STATUS_DEFINITIONS = {
    'S00': 'Request Created',
    'S01': 'Notification Sent',
    'S02': 'Notification Delivered',
    'S03': 'Notification Opened',
    'S04': 'Redirect Launched',
    'S05': 'Redirect Landed',
    'S06': 'QR Rendered',
    'S07': 'QR Scanned',
    'S08': 'Request Viewed',
    'S10': 'Docs Ready at Open',
    'S11': 'Docs Missing at Open',
    'S12': 'Missing Doc Request Initiated',
    'S13': 'Missing Doc Request Success',
    'S14': 'Missing Doc Request Error',
    'S15': 'Missing Doc Not Found',
    'S20': 'Awaiting Consent',
    'S21': 'Consent Given',
    'S30': 'PIN Requested',
    'S31': 'PIN Verified',
    'S32': 'PIN Failed',
    'S40': 'Share Success',
    'S41': 'Share Tech Error',
    'S42': 'Expired',
    'S43': 'User Aborted',
    'S44': 'Not Eligible'
}

TERMINAL_STATUSES = ['S40', 'S41', 'S42', 'S43', 'S44']

# Channel-specific status flows
CHANNEL_FLOWS = {
    'notification': ['S00', 'S01', 'S02', 'S03', 'S08', 'S10/S11', 'S20', 'S21', 'S30', 'S31', 'S40'],
    'redirect': ['S00', 'S04', 'S05', 'S08', 'S10/S11', 'S20', 'S21', 'S30', 'S31', 'S40'],
    'qr': ['S00', 'S06', 'S07', 'S08', 'S10/S11', 'S20', 'S21', 'S30', 'S31', 'S40']
}

def load_and_prepare_data(filepath):
    """Load and prepare the sharing transactions data"""
    print("Loading data...")
    df = pd.read_csv(filepath)

    # Convert timestamp to datetime
    df['status_ts'] = pd.to_datetime(df['status_ts'])

    # Sort by request_id and timestamp
    df = df.sort_values(['request_id', 'status_ts'])

    print(f"Loaded {len(df)} status records for {df['request_id'].nunique()} unique requests")
    print(f"Channels: {df['channel'].unique()}")
    print(f"Platforms: {df['platform'].unique()}")
    print(f"Service Providers: {df['sp_id'].unique()}")
    print(f"Status codes: {sorted(df['status_code'].unique())}")

    return df

def get_request_summary(df):
    """Create a request-level summary with terminal status and journey info"""

    # Get terminal status for each request
    terminal_status = df[df['status_code'].isin(TERMINAL_STATUSES)].groupby('request_id').agg({
        'status_code': 'first',  # Terminal status
        'status_ts': 'first'     # When it reached terminal
    }).rename(columns={'status_code': 'terminal_status', 'status_ts': 'terminal_ts'})

    # Get first status for each request
    first_status = df.groupby('request_id').agg({
        'sp_id': 'first',
        'channel': 'first',
        'platform': 'first',
        'status_ts': 'first',
        'required_count': 'first'
    }).rename(columns={'status_ts': 'start_ts'})

    # Merge
    summary = first_status.join(terminal_status, how='left')

    # Calculate total journey time for completed requests
    summary['journey_time_ms'] = (summary['terminal_ts'] - summary['start_ts']).dt.total_seconds() * 1000

    # Check if docs were ready at open
    docs_ready = df[df['status_code'] == 'S10'].groupby('request_id').size()
    docs_missing = df[df['status_code'] == 'S11'].groupby('request_id').size()

    summary['docs_ready_at_open'] = summary.index.isin(docs_ready.index)
    summary['docs_missing_at_open'] = summary.index.isin(docs_missing.index)

    # Check if reached key stages
    for status in ['S08', 'S20', 'S21', 'S30', 'S31']:
        summary[f'reached_{status}'] = summary.index.isin(
            df[df['status_code'] == status]['request_id'].unique()
        )

    return summary

def create_channel_funnel(df, summary, channel, save_path):
    """Create funnel diagram for a specific channel"""
    print(f"\nCreating funnel for {channel} channel...")

    # Filter to this channel
    channel_requests = summary[summary['channel'] == channel]
    total_requests = len(channel_requests)

    if total_requests == 0:
        print(f"No data for {channel} channel")
        return None

    # Define funnel stages based on channel
    if channel == 'notification':
        stages = [
            ('S00', 'Request Created'),
            ('S01', 'Notification Sent'),
            ('S02', 'Notification Delivered'),
            ('S03', 'Notification Opened'),
            ('S08', 'Request Viewed'),
            ('S10', 'Docs Ready'),
            ('S21', 'Consent Given'),
            ('S30', 'PIN Requested'),
            ('S31', 'PIN Verified'),
            ('S40', 'Share Success')
        ]
    elif channel == 'redirect':
        stages = [
            ('S00', 'Request Created'),
            ('S04', 'Redirect Launched'),
            ('S05', 'Redirect Landed'),
            ('S08', 'Request Viewed'),
            ('S10', 'Docs Ready'),
            ('S21', 'Consent Given'),
            ('S30', 'PIN Requested'),
            ('S31', 'PIN Verified'),
            ('S40', 'Share Success')
        ]
    else:  # qr
        stages = [
            ('S00', 'Request Created'),
            ('S06', 'QR Rendered'),
            ('S07', 'QR Scanned'),
            ('S08', 'Request Viewed'),
            ('S10', 'Docs Ready'),
            ('S21', 'Consent Given'),
            ('S30', 'PIN Requested'),
            ('S31', 'PIN Verified'),
            ('S40', 'Share Success')
        ]

    # Calculate counts for each stage
    counts = []
    percentages = []
    drop_offs = []

    channel_df = df[df['channel'] == channel]

    for i, (status_code, stage_name) in enumerate(stages):
        if status_code == 'S00':
            count = total_requests
        elif status_code == 'S10':
            # Docs ready (either S10 directly or after S13)
            count = summary[
                (summary['channel'] == channel) &
                (summary['reached_S08'] == True)
            ]['docs_ready_at_open'].sum()
            # Add those who got docs via S13
            s13_count = len(df[
                (df['channel'] == channel) &
                (df['status_code'] == 'S13')
            ]['request_id'].unique())
            count += s13_count
        else:
            count = len(channel_df[channel_df['status_code'] == status_code]['request_id'].unique())

        counts.append(count)
        percentages.append(count / total_requests * 100)

        if i > 0:
            drop_off = counts[i-1] - count
            drop_off_pct = (drop_off / counts[i-1] * 100) if counts[i-1] > 0 else 0
            drop_offs.append(f"-{drop_off} (-{drop_off_pct:.1f}%)")
        else:
            drop_offs.append("")

    # Create funnel visualization using Plotly
    fig = go.Figure()

    # Add funnel
    fig.add_trace(go.Funnel(
        y=[stage[1] for stage in stages],
        x=counts,
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(
            color=BRAND_COLORS['primary'],
            line=dict(width=2, color='white')
        ),
        connector=dict(
            line=dict(color=BRAND_COLORS['neutral'], width=1, dash='dot')
        )
    ))

    fig.update_layout(
        title=f"{channel.capitalize()} Channel Funnel<br><sub>Total Requests: {total_requests:,}</sub>",
        height=800,
        font=dict(size=12),
        showlegend=False
    )

    # Save as HTML
    html_path = save_path.replace('.png', '.html')
    fig.write_html(html_path)
    print(f"Saved interactive funnel to {html_path}")

    # Create static version with matplotlib for presentation
    fig_static, ax = plt.subplots(figsize=(12, 10))

    y_pos = np.arange(len(stages))
    max_width = max(counts)

    # Draw bars
    bars = ax.barh(y_pos, counts, color=BRAND_COLORS['primary'], alpha=0.8, edgecolor='white', linewidth=2)

    # Add labels
    for i, (bar, count, pct, drop) in enumerate(zip(bars, counts, percentages, drop_offs)):
        # Stage name and count
        ax.text(5, i, f"{stages[i][1]}: {count:,} ({pct:.1f}%)",
                va='center', fontsize=11, fontweight='bold', color='white')

        # Drop-off annotation
        if drop and i > 0:
            ax.text(max_width * 1.02, i - 0.3, drop,
                    va='center', fontsize=9, color=BRAND_COLORS['error'], style='italic')

    ax.set_yticks([])
    ax.set_xlabel('Number of Requests', fontsize=12, fontweight='bold')
    ax.set_title(f'{channel.capitalize()} Channel Funnel\nTotal Requests: {total_requests:,}',
                 fontsize=14, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved static funnel to {save_path}")

    return {
        'channel': channel,
        'total_requests': total_requests,
        'stages': stages,
        'counts': counts,
        'percentages': percentages,
        'conversion_rate': (counts[-1] / counts[0] * 100) if counts[0] > 0 else 0
    }

def create_terminal_status_charts(summary, save_path):
    """Create terminal status distribution charts"""
    print("\nCreating terminal status distribution charts...")

    # Overall distribution
    terminal_counts = summary['terminal_status'].value_counts()

    # Create subplot: overall + by channel + by platform
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Overall Terminal Status', 'By Channel', 'By Platform'),
        specs=[[{'type': 'pie'}, {'type': 'bar'}, {'type': 'bar'}]]
    )

    # Overall pie chart
    colors = {
        'S40': BRAND_COLORS['success'],
        'S41': BRAND_COLORS['error'],
        'S42': BRAND_COLORS['warning'],
        'S43': BRAND_COLORS['neutral'],
        'S44': BRAND_COLORS['error']
    }

    fig.add_trace(
        go.Pie(
            labels=[STATUS_DEFINITIONS.get(s, s) for s in terminal_counts.index],
            values=terminal_counts.values,
            marker=dict(colors=[colors.get(s, BRAND_COLORS['neutral']) for s in terminal_counts.index]),
            textinfo='label+percent',
            textposition='outside'
        ),
        row=1, col=1
    )

    # By channel
    channel_terminal = summary.groupby(['channel', 'terminal_status']).size().unstack(fill_value=0)

    for status in TERMINAL_STATUSES:
        if status in channel_terminal.columns:
            fig.add_trace(
                go.Bar(
                    name=STATUS_DEFINITIONS.get(status, status),
                    x=channel_terminal.index,
                    y=channel_terminal[status],
                    marker_color=colors.get(status, BRAND_COLORS['neutral']),
                    text=channel_terminal[status],
                    textposition='auto'
                ),
                row=1, col=2
            )

    # By platform
    platform_terminal = summary.groupby(['platform', 'terminal_status']).size().unstack(fill_value=0)

    for status in TERMINAL_STATUSES:
        if status in platform_terminal.columns:
            fig.add_trace(
                go.Bar(
                    name=STATUS_DEFINITIONS.get(status, status),
                    x=platform_terminal.index,
                    y=platform_terminal[status],
                    marker_color=colors.get(status, BRAND_COLORS['neutral']),
                    text=platform_terminal[status],
                    textposition='auto',
                    showlegend=False
                ),
                row=1, col=3
            )

    fig.update_layout(
        title_text="Terminal Status Distribution Analysis",
        height=500,
        barmode='stack',
        showlegend=True
    )

    html_path = save_path.replace('.png', '.html')
    fig.write_html(html_path)

    # Static version
    fig_static, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Overall pie
    axes[0].pie(
        terminal_counts.values,
        labels=[STATUS_DEFINITIONS.get(s, s) for s in terminal_counts.index],
        autopct='%1.1f%%',
        colors=[colors.get(s, BRAND_COLORS['neutral']) for s in terminal_counts.index],
        startangle=90
    )
    axes[0].set_title('Overall Terminal Status', fontweight='bold', fontsize=12)

    # By channel
    channel_terminal_pct = channel_terminal.div(channel_terminal.sum(axis=1), axis=0) * 100
    channel_terminal_pct.plot(kind='bar', stacked=True, ax=axes[1],
                              color=[colors.get(s, BRAND_COLORS['neutral']) for s in channel_terminal_pct.columns])
    axes[1].set_title('Terminal Status by Channel', fontweight='bold', fontsize=12)
    axes[1].set_ylabel('Percentage (%)')
    axes[1].set_xlabel('Channel')
    axes[1].legend(title='Status', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    axes[1].tick_params(axis='x', rotation=0)

    # By platform
    platform_terminal_pct = platform_terminal.div(platform_terminal.sum(axis=1), axis=0) * 100
    platform_terminal_pct.plot(kind='bar', stacked=True, ax=axes[2],
                               color=[colors.get(s, BRAND_COLORS['neutral']) for s in platform_terminal_pct.columns])
    axes[2].set_title('Terminal Status by Platform', fontweight='bold', fontsize=12)
    axes[2].set_ylabel('Percentage (%)')
    axes[2].set_xlabel('Platform')
    axes[2].legend(title='Status', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    axes[2].tick_params(axis='x', rotation=0)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved to {save_path} and {html_path}")

def create_document_readiness_analysis(df, summary, save_path):
    """Create document readiness impact analysis"""
    print("\nCreating document readiness analysis...")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Success rate: S10 vs S11
    docs_ready = summary[summary['docs_ready_at_open'] == True]
    docs_missing = summary[summary['docs_missing_at_open'] == True]

    ready_success_rate = (docs_ready['terminal_status'] == 'S40').sum() / len(docs_ready) * 100 if len(docs_ready) > 0 else 0
    missing_success_rate = (docs_missing['terminal_status'] == 'S40').sum() / len(docs_missing) * 100 if len(docs_missing) > 0 else 0

    bars = axes[0, 0].bar(
        ['Docs Ready\n(S10)', 'Docs Missing\n(S11)'],
        [ready_success_rate, missing_success_rate],
        color=[BRAND_COLORS['success'], BRAND_COLORS['warning']],
        alpha=0.8,
        edgecolor='black'
    )

    for bar in bars:
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom', fontweight='bold', fontsize=12)

    axes[0, 0].set_ylabel('Success Rate (%)', fontweight='bold')
    axes[0, 0].set_title('Success Rate: Docs Ready vs Docs Missing at Open', fontweight='bold', fontsize=12)
    axes[0, 0].set_ylim(0, 100)
    axes[0, 0].grid(axis='y', alpha=0.3)

    # 2. Missing doc request outcomes
    s12_requests = df[df['status_code'] == 'S12']['request_id'].unique()
    s13_success = df[df['status_code'] == 'S13']['request_id'].unique()
    s14_error = df[df['status_code'] == 'S14']['request_id'].unique()
    s15_not_found = df[df['status_code'] == 'S15']['request_id'].unique()

    outcomes = {
        'Success (S13)': len(s13_success),
        'Tech Error (S14)': len(s14_error),
        'Not Found (S15)': len(s15_not_found)
    }

    wedges, texts, autotexts = axes[0, 1].pie(
        outcomes.values(),
        labels=outcomes.keys(),
        autopct='%1.1f%%',
        colors=[BRAND_COLORS['success'], BRAND_COLORS['error'], BRAND_COLORS['warning']],
        startangle=90
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    axes[0, 1].set_title(f'Missing Doc Request Outcomes\n(Total Requests: {len(s12_requests)})',
                         fontweight='bold', fontsize=12)

    # 3. Document readiness by channel
    channel_readiness = summary.groupby('channel').agg({
        'docs_ready_at_open': 'sum',
        'docs_missing_at_open': 'sum'
    })

    x = np.arange(len(channel_readiness.index))
    width = 0.35

    bars1 = axes[1, 0].bar(x - width/2, channel_readiness['docs_ready_at_open'], width,
                           label='Docs Ready', color=BRAND_COLORS['success'], alpha=0.8)
    bars2 = axes[1, 0].bar(x + width/2, channel_readiness['docs_missing_at_open'], width,
                           label='Docs Missing', color=BRAND_COLORS['warning'], alpha=0.8)

    axes[1, 0].set_xlabel('Channel', fontweight='bold')
    axes[1, 0].set_ylabel('Number of Requests', fontweight='bold')
    axes[1, 0].set_title('Document Readiness by Channel', fontweight='bold', fontsize=12)
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(channel_readiness.index)
    axes[1, 0].legend()
    axes[1, 0].grid(axis='y', alpha=0.3)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                                f'{int(height)}',
                                ha='center', va='bottom', fontsize=9)

    # 4. Document readiness by SP
    sp_readiness = summary.groupby('sp_id').agg({
        'docs_ready_at_open': 'sum',
        'docs_missing_at_open': 'sum'
    })
    sp_readiness['total'] = sp_readiness.sum(axis=1)
    sp_readiness['ready_pct'] = sp_readiness['docs_ready_at_open'] / sp_readiness['total'] * 100
    sp_readiness = sp_readiness.sort_values('ready_pct', ascending=False)

    bars = axes[1, 1].barh(sp_readiness.index, sp_readiness['ready_pct'],
                           color=BRAND_COLORS['primary'], alpha=0.8)

    for i, (idx, row) in enumerate(sp_readiness.iterrows()):
        axes[1, 1].text(row['ready_pct'] + 1, i, f"{row['ready_pct']:.1f}%",
                        va='center', fontweight='bold')

    axes[1, 1].set_xlabel('Percentage Ready (%)', fontweight='bold')
    axes[1, 1].set_ylabel('Service Provider', fontweight='bold')
    axes[1, 1].set_title('Document Readiness Rate by Service Provider', fontweight='bold', fontsize=12)
    axes[1, 1].set_xlim(0, 110)
    axes[1, 1].grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved to {save_path}")

def create_channel_performance_comparison(summary, save_path):
    """Create channel performance comparison"""
    print("\nCreating channel performance comparison...")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Overall success rate by channel
    channel_success = summary.groupby('channel').agg({
        'terminal_status': lambda x: (x == 'S40').sum(),
        'sp_id': 'count'  # Use sp_id as a proxy for counting rows
    })
    channel_success.rename(columns={'sp_id': 'total_count'}, inplace=True)
    channel_success['success_rate'] = channel_success['terminal_status'] / channel_success['total_count'] * 100
    channel_success = channel_success.sort_values('success_rate', ascending=False)

    bars = axes[0, 0].bar(channel_success.index, channel_success['success_rate'],
                          color=BRAND_COLORS['primary'], alpha=0.8, edgecolor='black')

    for bar in bars:
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom', fontweight='bold', fontsize=12)

    axes[0, 0].set_ylabel('Success Rate (%)', fontweight='bold')
    axes[0, 0].set_xlabel('Channel', fontweight='bold')
    axes[0, 0].set_title('Success Rate by Channel', fontweight='bold', fontsize=12)
    axes[0, 0].set_ylim(0, 100)
    axes[0, 0].grid(axis='y', alpha=0.3)

    # 2. Average journey time by channel (for successful requests)
    successful = summary[summary['terminal_status'] == 'S40']
    channel_time = successful.groupby('channel')['journey_time_ms'].agg(['median', 'mean'])
    channel_time = channel_time / 1000  # Convert to seconds

    x = np.arange(len(channel_time.index))
    width = 0.35

    bars1 = axes[0, 1].bar(x - width/2, channel_time['median'], width,
                           label='Median', color=BRAND_COLORS['success'], alpha=0.8)
    bars2 = axes[0, 1].bar(x + width/2, channel_time['mean'], width,
                           label='Mean', color=BRAND_COLORS['light_blue'], alpha=0.8)

    axes[0, 1].set_ylabel('Time (seconds)', fontweight='bold')
    axes[0, 1].set_xlabel('Channel', fontweight='bold')
    axes[0, 1].set_title('Journey Time by Channel (Successful Requests)', fontweight='bold', fontsize=12)
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(channel_time.index)
    axes[0, 1].legend()
    axes[0, 1].grid(axis='y', alpha=0.3)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                                f'{height:.1f}s',
                                ha='center', va='bottom', fontsize=9)

    # 3. Platform performance within each channel
    channel_platform = summary.groupby(['channel', 'platform']).agg({
        'terminal_status': lambda x: (x == 'S40').sum(),
        'sp_id': 'count'
    })
    channel_platform.rename(columns={'sp_id': 'total_count'}, inplace=True)
    channel_platform['success_rate'] = channel_platform['terminal_status'] / channel_platform['total_count'] * 100
    channel_platform = channel_platform.reset_index()

    channels = channel_platform['channel'].unique()
    x = np.arange(len(channels))
    width = 0.35

    ios_rates = []
    android_rates = []

    for channel in channels:
        ios_data = channel_platform[(channel_platform['channel'] == channel) &
                                     (channel_platform['platform'] == 'ios')]
        android_data = channel_platform[(channel_platform['channel'] == channel) &
                                        (channel_platform['platform'] == 'android')]

        ios_rates.append(ios_data['success_rate'].values[0] if len(ios_data) > 0 else 0)
        android_rates.append(android_data['success_rate'].values[0] if len(android_data) > 0 else 0)

    bars1 = axes[1, 0].bar(x - width/2, ios_rates, width,
                           label='iOS', color=BRAND_COLORS['primary'], alpha=0.8)
    bars2 = axes[1, 0].bar(x + width/2, android_rates, width,
                           label='Android', color=BRAND_COLORS['success'], alpha=0.8)

    axes[1, 0].set_ylabel('Success Rate (%)', fontweight='bold')
    axes[1, 0].set_xlabel('Channel', fontweight='bold')
    axes[1, 0].set_title('Success Rate by Platform within Channel', fontweight='bold', fontsize=12)
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(channels)
    axes[1, 0].legend()
    axes[1, 0].set_ylim(0, 100)
    axes[1, 0].grid(axis='y', alpha=0.3)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                                f'{height:.0f}%',
                                ha='center', va='bottom', fontsize=9)

    # 4. Request volume by channel
    channel_volume = summary['channel'].value_counts()

    wedges, texts, autotexts = axes[1, 1].pie(
        channel_volume.values,
        labels=[f'{c.capitalize()}\n({v:,})' for c, v in zip(channel_volume.index, channel_volume.values)],
        autopct='%1.1f%%',
        colors=[BRAND_COLORS['primary'], BRAND_COLORS['secondary'], BRAND_COLORS['light_teal']],
        startangle=90
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    axes[1, 1].set_title('Request Volume by Channel', fontweight='bold', fontsize=12)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved to {save_path}")

def create_sp_analysis(summary, save_path):
    """Create service provider analysis"""
    print("\nCreating service provider analysis...")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Success rate by SP
    sp_success = summary.groupby('sp_id').agg({
        'terminal_status': lambda x: (x == 'S40').sum(),
        'channel': 'count'
    })
    sp_success.rename(columns={'channel': 'total_count'}, inplace=True)
    sp_success['success_rate'] = sp_success['terminal_status'] / sp_success['total_count'] * 100
    sp_success = sp_success.sort_values('success_rate', ascending=True)

    bars = axes[0, 0].barh(sp_success.index, sp_success['success_rate'],
                           color=BRAND_COLORS['primary'], alpha=0.8)

    for i, (idx, row) in enumerate(sp_success.iterrows()):
        axes[0, 0].text(row['success_rate'] + 1, i, f"{row['success_rate']:.1f}%",
                        va='center', fontweight='bold')

    axes[0, 0].set_xlabel('Success Rate (%)', fontweight='bold')
    axes[0, 0].set_ylabel('Service Provider', fontweight='bold')
    axes[0, 0].set_title('Success Rate by Service Provider', fontweight='bold', fontsize=12)
    axes[0, 0].set_xlim(0, 110)
    axes[0, 0].grid(axis='x', alpha=0.3)

    # 2. Request volume by SP
    sp_volume = summary['sp_id'].value_counts()

    bars = axes[0, 1].barh(sp_volume.index, sp_volume.values,
                           color=BRAND_COLORS['secondary'], alpha=0.8)

    for i, (idx, val) in enumerate(sp_volume.items()):
        axes[0, 1].text(val + max(sp_volume) * 0.02, i, f"{val:,}",
                        va='center', fontweight='bold')

    axes[0, 1].set_xlabel('Number of Requests', fontweight='bold')
    axes[0, 1].set_ylabel('Service Provider', fontweight='bold')
    axes[0, 1].set_title('Request Volume by Service Provider', fontweight='bold', fontsize=12)
    axes[0, 1].grid(axis='x', alpha=0.3)

    # 3. SP vs Channel heatmap
    sp_channel = summary.groupby(['sp_id', 'channel']).size().unstack(fill_value=0)

    # Calculate success rates
    sp_channel_success = summary[summary['terminal_status'] == 'S40'].groupby(['sp_id', 'channel']).size().unstack(fill_value=0)
    sp_channel_rate = (sp_channel_success / sp_channel * 100).fillna(0)

    im = axes[1, 0].imshow(sp_channel_rate.values, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)

    axes[1, 0].set_xticks(np.arange(len(sp_channel_rate.columns)))
    axes[1, 0].set_yticks(np.arange(len(sp_channel_rate.index)))
    axes[1, 0].set_xticklabels(sp_channel_rate.columns)
    axes[1, 0].set_yticklabels(sp_channel_rate.index)

    # Add text annotations
    for i in range(len(sp_channel_rate.index)):
        for j in range(len(sp_channel_rate.columns)):
            value = sp_channel_rate.iloc[i, j]
            count = sp_channel.iloc[i, j]
            text = axes[1, 0].text(j, i, f'{value:.0f}%\n({count})',
                                   ha="center", va="center", color="black", fontsize=9)

    axes[1, 0].set_title('Success Rate Heatmap: SP vs Channel', fontweight='bold', fontsize=12)
    axes[1, 0].set_xlabel('Channel', fontweight='bold')
    axes[1, 0].set_ylabel('Service Provider', fontweight='bold')

    # Add colorbar
    cbar = plt.colorbar(im, ax=axes[1, 0])
    cbar.set_label('Success Rate (%)', fontweight='bold')

    # 4. Terminal status distribution by SP
    sp_terminal = summary.groupby(['sp_id', 'terminal_status']).size().unstack(fill_value=0)
    sp_terminal_pct = sp_terminal.div(sp_terminal.sum(axis=1), axis=0) * 100

    colors_list = [BRAND_COLORS['success'], BRAND_COLORS['error'],
                   BRAND_COLORS['warning'], BRAND_COLORS['neutral'], BRAND_COLORS['error']]

    sp_terminal_pct.plot(kind='barh', stacked=True, ax=axes[1, 1],
                         color=colors_list[:len(sp_terminal_pct.columns)])

    axes[1, 1].set_xlabel('Percentage (%)', fontweight='bold')
    axes[1, 1].set_ylabel('Service Provider', fontweight='bold')
    axes[1, 1].set_title('Terminal Status Distribution by SP', fontweight='bold', fontsize=12)
    axes[1, 1].legend(title='Status', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    axes[1, 1].grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved to {save_path}")

def create_time_analysis(df, summary, save_path):
    """Create time analysis visualizations"""
    print("\nCreating time analysis...")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Box plot of step latencies for key stages
    key_statuses = ['S08', 'S20', 'S21', 'S30', 'S31', 'S40']
    latency_data = []
    labels = []

    for status in key_statuses:
        status_df = df[df['status_code'] == status]
        if len(status_df) > 0:
            latencies = status_df['step_latency_ms'].values / 1000  # Convert to seconds
            latencies = latencies[latencies > 0]  # Remove zeros
            if len(latencies) > 0:
                latency_data.append(latencies)
                labels.append(f"{status}\n{STATUS_DEFINITIONS[status]}")

    bp = axes[0, 0].boxplot(latency_data, labels=labels, patch_artist=True,
                            boxprops=dict(facecolor=BRAND_COLORS['light_blue'], alpha=0.7),
                            medianprops=dict(color=BRAND_COLORS['dark_blue'], linewidth=2),
                            whiskerprops=dict(color=BRAND_COLORS['primary']),
                            capprops=dict(color=BRAND_COLORS['primary']))

    axes[0, 0].set_ylabel('Step Latency (seconds)', fontweight='bold')
    axes[0, 0].set_xlabel('Status Code', fontweight='bold')
    axes[0, 0].set_title('Step Latency Distribution for Key Stages', fontweight='bold', fontsize=12)
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(axis='y', alpha=0.3)

    # 2. Journey time distribution for successful requests
    successful = summary[summary['terminal_status'] == 'S40'].copy()
    successful['journey_time_sec'] = successful['journey_time_ms'] / 1000

    axes[0, 1].hist(successful['journey_time_sec'], bins=30,
                    color=BRAND_COLORS['success'], alpha=0.7, edgecolor='black')

    median_time = successful['journey_time_sec'].median()
    p90_time = successful['journey_time_sec'].quantile(0.9)

    axes[0, 1].axvline(median_time, color=BRAND_COLORS['dark_blue'], linestyle='--',
                       linewidth=2, label=f'Median: {median_time:.1f}s')
    axes[0, 1].axvline(p90_time, color=BRAND_COLORS['error'], linestyle='--',
                       linewidth=2, label=f'P90: {p90_time:.1f}s')

    axes[0, 1].set_xlabel('Journey Time (seconds)', fontweight='bold')
    axes[0, 1].set_ylabel('Frequency', fontweight='bold')
    axes[0, 1].set_title('Time-to-Complete Distribution (Successful Requests)', fontweight='bold', fontsize=12)
    axes[0, 1].legend()
    axes[0, 1].grid(axis='y', alpha=0.3)

    # 3. Journey time by channel
    channel_times = []
    channel_labels = []

    for channel in successful['channel'].unique():
        channel_data = successful[successful['channel'] == channel]['journey_time_sec'].values
        if len(channel_data) > 0:
            channel_times.append(channel_data)
            channel_labels.append(channel.capitalize())

    bp2 = axes[1, 0].boxplot(channel_times, labels=channel_labels, patch_artist=True,
                             boxprops=dict(facecolor=BRAND_COLORS['secondary'], alpha=0.7),
                             medianprops=dict(color=BRAND_COLORS['dark_blue'], linewidth=2))

    axes[1, 0].set_ylabel('Journey Time (seconds)', fontweight='bold')
    axes[1, 0].set_xlabel('Channel', fontweight='bold')
    axes[1, 0].set_title('Journey Time by Channel (Successful Requests)', fontweight='bold', fontsize=12)
    axes[1, 0].grid(axis='y', alpha=0.3)

    # 4. Median step times for critical path
    critical_steps = ['S08', 'S20', 'S21', 'S30', 'S31', 'S40']
    step_medians = []
    step_labels = []

    for status in critical_steps:
        status_df = df[df['status_code'] == status]
        if len(status_df) > 0:
            median_latency = status_df[status_df['step_latency_ms'] > 0]['step_latency_ms'].median() / 1000
            if not np.isnan(median_latency):
                step_medians.append(median_latency)
                step_labels.append(status)

    bars = axes[1, 1].bar(step_labels, step_medians,
                          color=BRAND_COLORS['primary'], alpha=0.8, edgecolor='black')

    for bar in bars:
        height = bar.get_height()
        axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}s',
                        ha='center', va='bottom', fontweight='bold')

    axes[1, 1].set_ylabel('Median Latency (seconds)', fontweight='bold')
    axes[1, 1].set_xlabel('Status Code', fontweight='bold')
    axes[1, 1].set_title('Median Step Latency for Critical Path', fontweight='bold', fontsize=12)
    axes[1, 1].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved to {save_path}")

def create_error_analysis(df, save_path):
    """Create error distribution analysis"""
    print("\nCreating error analysis...")

    # Filter to error records
    errors = df[df['error_code'].notna()].copy()

    if len(errors) == 0:
        print("No error data found")
        return

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Error types distribution
    error_counts = errors['error_code'].value_counts()

    bars = axes[0, 0].barh(error_counts.index, error_counts.values,
                           color=BRAND_COLORS['error'], alpha=0.8)

    for i, (idx, val) in enumerate(error_counts.items()):
        axes[0, 0].text(val + max(error_counts) * 0.02, i, f"{val:,}",
                        va='center', fontweight='bold')

    axes[0, 0].set_xlabel('Count', fontweight='bold')
    axes[0, 0].set_ylabel('Error Code', fontweight='bold')
    axes[0, 0].set_title('Error Type Distribution', fontweight='bold', fontsize=12)
    axes[0, 0].grid(axis='x', alpha=0.3)

    # 2. Error source distribution
    source_counts = errors['error_source'].value_counts()

    wedges, texts, autotexts = axes[0, 1].pie(
        source_counts.values,
        labels=source_counts.index,
        autopct='%1.1f%%',
        colors=[BRAND_COLORS['error'], BRAND_COLORS['warning'],
                BRAND_COLORS['neutral'], BRAND_COLORS['light_blue']],
        startangle=90
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    axes[0, 1].set_title(f'Error Source Distribution\n(Total Errors: {len(errors)})',
                         fontweight='bold', fontsize=12)

    # 3. Errors by status code
    error_status = errors.groupby(['status_code', 'error_source']).size().unstack(fill_value=0)

    error_status.plot(kind='bar', stacked=True, ax=axes[1, 0],
                      color=[BRAND_COLORS['error'], BRAND_COLORS['warning'],
                             BRAND_COLORS['neutral'], BRAND_COLORS['light_blue']])

    axes[1, 0].set_xlabel('Status Code', fontweight='bold')
    axes[1, 0].set_ylabel('Error Count', fontweight='bold')
    axes[1, 0].set_title('Errors by Status Code and Source', fontweight='bold', fontsize=12)
    axes[1, 0].legend(title='Error Source', bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(axis='y', alpha=0.3)

    # 4. Technical vs User-driven failures
    tech_errors = errors[errors['error_source'].isin(['issuer', 'dv', 'network'])]
    user_errors = errors[errors['error_source'].isin(['user_cancel', 'pin_incorrect'])]

    failure_types = {
        'Technical Errors': len(tech_errors),
        'User-Driven Failures': len(user_errors)
    }

    wedges, texts, autotexts = axes[1, 1].pie(
        failure_types.values(),
        labels=failure_types.keys(),
        autopct='%1.1f%%',
        colors=[BRAND_COLORS['error'], BRAND_COLORS['neutral']],
        startangle=90
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)

    axes[1, 1].set_title('Technical vs User-Driven Failures', fontweight='bold', fontsize=12)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved to {save_path}")

def create_platform_comparison(df, summary, save_path):
    """Create iOS vs Android platform comparison"""
    print("\nCreating platform comparison...")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Success rate comparison
    platform_success = summary.groupby('platform').agg({
        'terminal_status': lambda x: (x == 'S40').sum(),
        'channel': 'count'
    })
    platform_success.rename(columns={'channel': 'total_count'}, inplace=True)
    platform_success['success_rate'] = platform_success['terminal_status'] / platform_success['total_count'] * 100

    bars = axes[0, 0].bar(platform_success.index, platform_success['success_rate'],
                          color=[BRAND_COLORS['primary'], BRAND_COLORS['success']],
                          alpha=0.8, edgecolor='black')

    for bar in bars:
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom', fontweight='bold', fontsize=12)

    axes[0, 0].set_ylabel('Success Rate (%)', fontweight='bold')
    axes[0, 0].set_xlabel('Platform', fontweight='bold')
    axes[0, 0].set_title('Success Rate: iOS vs Android', fontweight='bold', fontsize=12)
    axes[0, 0].set_ylim(0, 100)
    axes[0, 0].grid(axis='y', alpha=0.3)

    # 2. Terminal status distribution by platform
    platform_terminal = summary.groupby(['platform', 'terminal_status']).size().unstack(fill_value=0)
    platform_terminal_pct = platform_terminal.div(platform_terminal.sum(axis=1), axis=0) * 100

    colors_list = {
        'S40': BRAND_COLORS['success'],
        'S41': BRAND_COLORS['error'],
        'S42': BRAND_COLORS['warning'],
        'S43': BRAND_COLORS['neutral'],
        'S44': BRAND_COLORS['error']
    }

    platform_terminal_pct.plot(kind='bar', stacked=True, ax=axes[0, 1],
                               color=[colors_list.get(s, BRAND_COLORS['neutral'])
                                      for s in platform_terminal_pct.columns])

    axes[0, 1].set_xlabel('Platform', fontweight='bold')
    axes[0, 1].set_ylabel('Percentage (%)', fontweight='bold')
    axes[0, 1].set_title('Terminal Status Distribution by Platform', fontweight='bold', fontsize=12)
    axes[0, 1].legend(title='Terminal Status', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    axes[0, 1].tick_params(axis='x', rotation=0)
    axes[0, 1].grid(axis='y', alpha=0.3)

    # 3. Journey time comparison
    successful = summary[summary['terminal_status'] == 'S40'].copy()
    successful['journey_time_sec'] = successful['journey_time_ms'] / 1000

    platform_times = []
    platform_labels = []

    for platform in successful['platform'].unique():
        platform_data = successful[successful['platform'] == platform]['journey_time_sec'].values
        if len(platform_data) > 0:
            platform_times.append(platform_data)
            platform_labels.append(platform.upper())

    bp = axes[1, 0].boxplot(platform_times, labels=platform_labels, patch_artist=True,
                            boxprops=dict(facecolor=BRAND_COLORS['light_blue'], alpha=0.7),
                            medianprops=dict(color=BRAND_COLORS['dark_blue'], linewidth=2))

    axes[1, 0].set_ylabel('Journey Time (seconds)', fontweight='bold')
    axes[1, 0].set_xlabel('Platform', fontweight='bold')
    axes[1, 0].set_title('Journey Time Comparison (Successful Requests)', fontweight='bold', fontsize=12)
    axes[1, 0].grid(axis='y', alpha=0.3)

    # 4. Request volume and conversion funnel
    x = np.arange(2)
    width = 0.35

    total_requests = [platform_success.loc[p, 'total_count'] for p in ['ios', 'android']]
    successful_requests = [platform_success.loc[p, 'terminal_status'] for p in ['ios', 'android']]

    bars1 = axes[1, 1].bar(x - width/2, total_requests, width,
                           label='Total Requests', color=BRAND_COLORS['primary'], alpha=0.8)
    bars2 = axes[1, 1].bar(x + width/2, successful_requests, width,
                           label='Successful', color=BRAND_COLORS['success'], alpha=0.8)

    axes[1, 1].set_ylabel('Number of Requests', fontweight='bold')
    axes[1, 1].set_xlabel('Platform', fontweight='bold')
    axes[1, 1].set_title('Request Volume and Success Count', fontweight='bold', fontsize=12)
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(['iOS', 'Android'])
    axes[1, 1].legend()
    axes[1, 1].grid(axis='y', alpha=0.3)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height):,}',
                            ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved to {save_path}")

def main():
    """Main execution function"""
    print("="*80)
    print("UAE PASS Digital Documents - Sharing Transactions Visualization Suite")
    print("="*80)

    # Load data
    data_path = r"D:\cluade\sharing_transactions_sample.csv"
    df = load_and_prepare_data(data_path)

    # Create request summary
    summary = get_request_summary(df)

    print(f"\nRequest Summary:")
    print(f"  Total unique requests: {len(summary)}")
    print(f"  Requests with terminal status: {summary['terminal_status'].notna().sum()}")
    print(f"  Success rate: {(summary['terminal_status'] == 'S40').sum() / len(summary) * 100:.1f}%")

    # Create output directory
    import os
    output_dir = r"D:\cluade\visualizations"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nCreating visualizations in: {output_dir}")
    print("="*80)

    # 1. Channel funnels
    print("\n[1/9] Creating channel funnel diagrams...")
    funnel_results = []
    for channel in df['channel'].unique():
        result = create_channel_funnel(
            df, summary, channel,
            os.path.join(output_dir, f"funnel_{channel}.png")
        )
        if result:
            funnel_results.append(result)

    # 2. Terminal status distribution
    print("\n[2/9] Creating terminal status distribution...")
    create_terminal_status_charts(
        summary,
        os.path.join(output_dir, "terminal_status_distribution.png")
    )

    # 3. Document readiness analysis
    print("\n[3/9] Creating document readiness analysis...")
    create_document_readiness_analysis(
        df, summary,
        os.path.join(output_dir, "document_readiness_analysis.png")
    )

    # 4. Channel performance comparison
    print("\n[4/9] Creating channel performance comparison...")
    create_channel_performance_comparison(
        summary,
        os.path.join(output_dir, "channel_performance_comparison.png")
    )

    # 5. Service provider analysis
    print("\n[5/9] Creating service provider analysis...")
    create_sp_analysis(
        summary,
        os.path.join(output_dir, "service_provider_analysis.png")
    )

    # 6. Time analysis
    print("\n[6/9] Creating time analysis...")
    create_time_analysis(
        df, summary,
        os.path.join(output_dir, "time_analysis.png")
    )

    # 7. Error analysis
    print("\n[7/9] Creating error analysis...")
    create_error_analysis(
        df,
        os.path.join(output_dir, "error_analysis.png")
    )

    # 8. Platform comparison
    print("\n[8/9] Creating platform comparison...")
    create_platform_comparison(
        df, summary,
        os.path.join(output_dir, "platform_comparison.png")
    )

    print("\n" + "="*80)
    print("Visualization suite completed!")
    print(f"All files saved to: {output_dir}")
    print("="*80)

if __name__ == "__main__":
    main()
