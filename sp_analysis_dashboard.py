"""
Interactive Service Provider Analysis Dashboard
==============================================
Allows stakeholders to explore SP-specific performance, compare to average,
and drill down into specific failure patterns.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from pathlib import Path

print("Loading data...")
df = pd.read_csv(r"D:\cluade\sharing_transactions_new_sample.csv")

# Get terminal statuses
terminal_df = df.sort_values(['request_id', 'status_ts']).groupby('request_id').last().reset_index()

# Load SP metrics
sp_metrics_df = pd.read_csv(r"D:\cluade\visualizations\sp_analysis\sp_metrics_summary.csv")

# Calculate system-wide averages
overall_metrics = {
    'success_rate': terminal_df['status_code'].eq('S40').mean() * 100,
    's41_rate': terminal_df['status_code'].eq('S41').mean() * 100,
    's42_rate': terminal_df['status_code'].eq('S42').mean() * 100,
    's43_rate': terminal_df['status_code'].eq('S43').mean() * 100,
    's44_rate': terminal_df['status_code'].eq('S44').mean() * 100,
}

print("Creating interactive dashboard...")

# Create comprehensive dashboard with subplots
fig = make_subplots(
    rows=4, cols=2,
    subplot_titles=(
        '1. SP Success Rate vs System Average',
        '2. Failure Mode Distribution by SP',
        '3. SP Volume vs Success Rate',
        '4. User Abort Rate Ranking',
        '5. Technical Error Rate by SP',
        '6. Consent & PIN Performance',
        '7. Time-to-Failure Distribution',
        '8. Error Source Breakdown'
    ),
    specs=[
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "scatter"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "box"}, {"type": "bar"}]
    ],
    vertical_spacing=0.08,
    horizontal_spacing=0.12,
    row_heights=[0.25, 0.25, 0.25, 0.25]
)

# ============================================================================
# Plot 1: SP Success Rate vs System Average
# ============================================================================
sp_sorted = sp_metrics_df.sort_values('success_rate', ascending=False)

colors = ['green' if x > overall_metrics['success_rate'] else 'red'
          for x in sp_sorted['success_rate']]

fig.add_trace(
    go.Bar(
        x=sp_sorted['sp_id'],
        y=sp_sorted['success_rate'],
        marker_color=colors,
        name='Success Rate',
        text=[f"{x:.1f}%" for x in sp_sorted['success_rate']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Success: %{y:.1f}%<extra></extra>'
    ),
    row=1, col=1
)

# Add system average line
fig.add_hline(
    y=overall_metrics['success_rate'],
    line_dash="dash",
    line_color="blue",
    annotation_text=f"System Avg: {overall_metrics['success_rate']:.1f}%",
    annotation_position="top right",
    row=1, col=1
)

# ============================================================================
# Plot 2: Failure Mode Distribution (Stacked Bar)
# ============================================================================
sp_sorted2 = sp_metrics_df.sort_values('failure_rate', ascending=False).head(10)

fig.add_trace(
    go.Bar(
        x=sp_sorted2['sp_id'],
        y=sp_sorted2['s41_rate'],
        name='S41 Tech Error',
        marker_color='purple',
        hovertemplate='<b>%{x}</b><br>S41: %{y:.1f}%<extra></extra>'
    ),
    row=1, col=2
)

fig.add_trace(
    go.Bar(
        x=sp_sorted2['sp_id'],
        y=sp_sorted2['s42_rate'],
        name='S42 Expired',
        marker_color='orange',
        hovertemplate='<b>%{x}</b><br>S42: %{y:.1f}%<extra></extra>'
    ),
    row=1, col=2
)

fig.add_trace(
    go.Bar(
        x=sp_sorted2['sp_id'],
        y=sp_sorted2['s43_rate'],
        name='S43 User Abort',
        marker_color='red',
        hovertemplate='<b>%{x}</b><br>S43: %{y:.1f}%<extra></extra>'
    ),
    row=1, col=2
)

fig.add_trace(
    go.Bar(
        x=sp_sorted2['sp_id'],
        y=sp_sorted2['s44_rate'],
        name='S44 Not Eligible',
        marker_color='gray',
        hovertemplate='<b>%{x}</b><br>S44: %{y:.1f}%<extra></extra>'
    ),
    row=1, col=2
)

# ============================================================================
# Plot 3: Volume vs Success Rate Scatter
# ============================================================================
# Add quadrant lines
median_volume = sp_metrics_df['total_requests'].median()
median_success = sp_metrics_df['success_rate'].median()

fig.add_trace(
    go.Scatter(
        x=sp_metrics_df['total_requests'],
        y=sp_metrics_df['success_rate'],
        mode='markers+text',
        text=sp_metrics_df['sp_id'],
        textposition='top center',
        marker=dict(
            size=sp_metrics_df['total_requests'] * 0.8,
            color=sp_metrics_df['success_rate'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(x=0.46, y=0.5, len=0.2, title='Success %'),
            line=dict(width=1, color='black')
        ),
        hovertemplate='<b>%{text}</b><br>Volume: %{x}<br>Success: %{y:.1f}%<extra></extra>',
        showlegend=False
    ),
    row=2, col=1
)

# Add quadrant dividers
fig.add_vline(x=median_volume, line_dash="dash", line_color="gray", row=2, col=1)
fig.add_hline(y=median_success, line_dash="dash", line_color="gray", row=2, col=1)

# ============================================================================
# Plot 4: User Abort Rate Ranking
# ============================================================================
abort_sorted = sp_metrics_df.sort_values('s43_rate', ascending=True)

colors_abort = ['darkred' if x > 20 else 'orange' if x > 15 else 'yellow' if x > 10 else 'green'
                for x in abort_sorted['s43_rate']]

fig.add_trace(
    go.Bar(
        y=abort_sorted['sp_id'],
        x=abort_sorted['s43_rate'],
        orientation='h',
        marker_color=colors_abort,
        text=[f"{x:.1f}%" for x in abort_sorted['s43_rate']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Abort Rate: %{x:.1f}%<extra></extra>',
        showlegend=False
    ),
    row=2, col=2
)

# Add threshold lines
fig.add_vline(x=15, line_dash="dot", line_color="red",
              annotation_text="Critical", annotation_position="top",
              row=2, col=2)

# ============================================================================
# Plot 5: Technical Error Rate
# ============================================================================
error_sorted = sp_metrics_df.sort_values('s41_rate', ascending=True)

colors_error = ['darkred' if x > 10 else 'orange' if x > 5 else 'green'
                for x in error_sorted['s41_rate']]

fig.add_trace(
    go.Bar(
        y=error_sorted['sp_id'],
        x=error_sorted['s41_rate'],
        orientation='h',
        marker_color=colors_error,
        text=[f"{x:.1f}%" for x in error_sorted['s41_rate']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Tech Error: %{x:.1f}%<extra></extra>',
        showlegend=False
    ),
    row=3, col=1
)

fig.add_vline(x=5, line_dash="dot", line_color="orange",
              annotation_text="Target", annotation_position="top",
              row=3, col=1)

# ============================================================================
# Plot 6: Consent & PIN Performance
# ============================================================================
# Calculate consent and PIN rates
consent_pin_data = []

for sp_id in df['sp_id'].unique():
    sp_data = df[df['sp_id'] == sp_id]

    reached_s20 = sp_data[sp_data['status_code'] == 'S20']['request_id'].nunique()
    completed_s21 = sp_data[sp_data['status_code'] == 'S21']['request_id'].nunique()
    consent_rate = (completed_s21 / reached_s20 * 100) if reached_s20 > 0 else 0

    reached_s30 = sp_data[sp_data['status_code'] == 'S30']['request_id'].nunique()
    completed_s31 = sp_data[sp_data['status_code'] == 'S31']['request_id'].nunique()
    pin_rate = (completed_s31 / reached_s30 * 100) if reached_s30 > 0 else 0

    if reached_s20 >= 5 and reached_s30 >= 5:  # Min sample size
        consent_pin_data.append({
            'sp_id': sp_id,
            'consent_rate': consent_rate,
            'pin_rate': pin_rate
        })

consent_pin_df = pd.DataFrame(consent_pin_data).sort_values('consent_rate', ascending=True)

fig.add_trace(
    go.Bar(
        y=consent_pin_df['sp_id'],
        x=consent_pin_df['consent_rate'],
        orientation='h',
        name='Consent (S20→S21)',
        marker_color='steelblue',
        text=[f"{x:.0f}%" for x in consent_pin_df['consent_rate']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Consent: %{x:.1f}%<extra></extra>'
    ),
    row=3, col=2
)

fig.add_trace(
    go.Bar(
        y=consent_pin_df['sp_id'],
        x=consent_pin_df['pin_rate'],
        orientation='h',
        name='PIN (S30→S31)',
        marker_color='coral',
        text=[f"{x:.0f}%" for x in consent_pin_df['pin_rate']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>PIN: %{x:.1f}%<extra></extra>'
    ),
    row=3, col=2
)

# ============================================================================
# Plot 7: Time-to-Failure Distribution (Box Plot)
# ============================================================================
# Calculate journey times
journey_times = []

for req_id in terminal_df['request_id']:
    req_data = df[df['request_id'] == req_id].sort_values('status_ts')
    if len(req_data) > 1:
        start = pd.to_datetime(req_data['status_ts'].iloc[0])
        end = pd.to_datetime(req_data['status_ts'].iloc[-1])
        duration_sec = (end - start).total_seconds()

        sp_id = req_data['sp_id'].iloc[0]
        terminal_status = req_data['status_code'].iloc[-1]

        journey_times.append({
            'sp_id': sp_id,
            'terminal_status': terminal_status,
            'duration_sec': duration_sec
        })

journey_df = pd.DataFrame(journey_times)

# Get top SPs by volume
top_sps = sp_metrics_df.nlargest(8, 'total_requests')['sp_id'].values
journey_subset = journey_df[journey_df['sp_id'].isin(top_sps)]

for sp in top_sps:
    sp_journey = journey_subset[journey_subset['sp_id'] == sp]

    fig.add_trace(
        go.Box(
            y=sp_journey['duration_sec'] / 3600,  # Convert to hours
            name=sp,
            boxmean='sd',
            hovertemplate='<b>%{fullData.name}</b><br>Time: %{y:.1f} hours<extra></extra>',
            showlegend=False
        ),
        row=4, col=1
    )

# ============================================================================
# Plot 8: Error Source Breakdown (Stacked Bar)
# ============================================================================
error_source_data = sp_metrics_df[
    (sp_metrics_df['issuer_errors'] + sp_metrics_df['network_errors'] +
     sp_metrics_df['dv_errors'] + sp_metrics_df['user_cancel_errors']) > 0
].sort_values('failure_count', ascending=False).head(10)

fig.add_trace(
    go.Bar(
        x=error_source_data['sp_id'],
        y=error_source_data['issuer_errors'],
        name='Issuer',
        marker_color='#e74c3c',
        hovertemplate='<b>%{x}</b><br>Issuer Errors: %{y}<extra></extra>'
    ),
    row=4, col=2
)

fig.add_trace(
    go.Bar(
        x=error_source_data['sp_id'],
        y=error_source_data['network_errors'],
        name='Network',
        marker_color='#f39c12',
        hovertemplate='<b>%{x}</b><br>Network Errors: %{y}<extra></extra>'
    ),
    row=4, col=2
)

fig.add_trace(
    go.Bar(
        x=error_source_data['sp_id'],
        y=error_source_data['dv_errors'],
        name='DV Backend',
        marker_color='#9b59b6',
        hovertemplate='<b>%{x}</b><br>DV Errors: %{y}<extra></extra>'
    ),
    row=4, col=2
)

fig.add_trace(
    go.Bar(
        x=error_source_data['sp_id'],
        y=error_source_data['user_cancel_errors'],
        name='User Cancel',
        marker_color='#95a5a6',
        hovertemplate='<b>%{x}</b><br>User Cancel: %{y}<extra></extra>'
    ),
    row=4, col=2
)

# ============================================================================
# Layout Updates
# ============================================================================
fig.update_xaxes(title_text="Service Provider", row=1, col=1, tickangle=-45)
fig.update_yaxes(title_text="Success Rate (%)", row=1, col=1)

fig.update_xaxes(title_text="Service Provider", row=1, col=2, tickangle=-45)
fig.update_yaxes(title_text="Failure Rate (%)", row=1, col=2)

fig.update_xaxes(title_text="Request Volume", row=2, col=1)
fig.update_yaxes(title_text="Success Rate (%)", row=2, col=1)

fig.update_yaxes(title_text="Service Provider", row=2, col=2)
fig.update_xaxes(title_text="User Abort Rate (%)", row=2, col=2)

fig.update_yaxes(title_text="Service Provider", row=3, col=1)
fig.update_xaxes(title_text="Technical Error Rate (%)", row=3, col=1)

fig.update_yaxes(title_text="Service Provider", row=3, col=2)
fig.update_xaxes(title_text="Conversion Rate (%)", row=3, col=2)

fig.update_xaxes(title_text="Service Provider", row=4, col=1, tickangle=-45)
fig.update_yaxes(title_text="Journey Time (hours)", row=4, col=1)

fig.update_xaxes(title_text="Service Provider", row=4, col=2, tickangle=-45)
fig.update_yaxes(title_text="Error Count", row=4, col=2)

# Update barmode for stacked bars
fig.update_layout(
    barmode='stack',
    height=2000,
    width=1600,
    title_text="<b>Service Provider Analysis Dashboard</b><br>" +
               f"<sub>System Average: {overall_metrics['success_rate']:.1f}% success | " +
               f"Total Requests: {len(terminal_df)} | " +
               f"SPs Analyzed: {len(sp_metrics_df)}</sub>",
    title_font_size=20,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.05,
        xanchor="center",
        x=0.5
    ),
    template='plotly_white'
)

# Save interactive dashboard
output_path = Path(r"D:\cluade\sp_analysis_interactive_dashboard.html")
fig.write_html(str(output_path))

print(f"\n[SUCCESS] Interactive dashboard saved: {output_path}")
print(f"\nDashboard includes:")
print("  1. SP success rate comparison vs system average")
print("  2. Failure mode distribution (top 10 worst SPs)")
print("  3. Volume vs success scatter plot (quadrant analysis)")
print("  4. User abort rate ranking")
print("  5. Technical error rate by SP")
print("  6. Consent & PIN performance comparison")
print("  7. Time-to-failure distribution (top 8 SPs)")
print("  8. Error source breakdown (root cause analysis)")
print(f"\nOpen in browser to explore: {output_path}")

# ============================================================================
# Create SP-Specific Deep Dive (Individual SP Analysis)
# ============================================================================
print("\n\nGenerating individual SP analysis pages...")

output_dir = Path(r"D:\cluade\visualizations\sp_analysis\individual_reports")
output_dir.mkdir(parents=True, exist_ok=True)

for sp_id in sp_metrics_df['sp_id'].unique():
    sp_terminal = terminal_df[terminal_df['sp_id'] == sp_id]
    sp_all = df[df['sp_id'] == sp_id]
    sp_metrics = sp_metrics_df[sp_metrics_df['sp_id'] == sp_id].iloc[0]

    # Create SP-specific dashboard
    sp_fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f'{sp_id} - Status Distribution',
            f'{sp_id} - Journey Flow (Funnel)',
            f'{sp_id} - Stuck Points (Last Status Before Failure)',
            f'{sp_id} - Performance vs System Average'
        ),
        specs=[
            [{"type": "pie"}, {"type": "funnel"}],
            [{"type": "bar"}, {"type": "bar"}]
        ]
    )

    # Pie chart - terminal status distribution
    status_counts = sp_terminal['status_code'].value_counts()
    sp_fig.add_trace(
        go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            marker=dict(colors=['#2ecc71', '#9b59b6', '#f39c12', '#e74c3c', '#95a5a6']),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
        ),
        row=1, col=1
    )

    # Funnel - journey progression
    funnel_stages = ['S00', 'S08', 'S20', 'S21', 'S30', 'S31', 'S40']
    funnel_counts = []
    for stage in funnel_stages:
        count = sp_all[sp_all['status_code'] == stage]['request_id'].nunique()
        funnel_counts.append(count)

    sp_fig.add_trace(
        go.Funnel(
            y=funnel_stages,
            x=funnel_counts,
            textinfo="value+percent initial",
            marker=dict(color=['#3498db', '#5dade2', '#85c1e9', '#aed6f1',
                              '#d6eaf8', '#e8f6f3', '#2ecc71'])
        ),
        row=1, col=2
    )

    # Bar chart - stuck points
    failed = sp_terminal[sp_terminal['status_code'] != 'S40']
    if len(failed) > 0:
        stuck_dist = failed['previous_status'].value_counts().head(8)
        sp_fig.add_trace(
            go.Bar(
                x=stuck_dist.index,
                y=stuck_dist.values,
                marker_color='coral',
                text=stuck_dist.values,
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Failures: %{y}<extra></extra>'
            ),
            row=2, col=1
        )

    # Comparison bars
    comparison_data = {
        'Metric': ['Success Rate', 'Abort Rate', 'Tech Error', 'Expiry Rate'],
        f'{sp_id}': [
            sp_metrics['success_rate'],
            sp_metrics['s43_rate'],
            sp_metrics['s41_rate'],
            sp_metrics['s42_rate']
        ],
        'System Avg': [
            overall_metrics['success_rate'],
            overall_metrics['s43_rate'],
            overall_metrics['s41_rate'],
            overall_metrics['s42_rate']
        ]
    }

    sp_fig.add_trace(
        go.Bar(
            x=comparison_data['Metric'],
            y=comparison_data[f'{sp_id}'],
            name=sp_id,
            marker_color='steelblue',
            text=[f"{x:.1f}%" for x in comparison_data[f'{sp_id}']],
            textposition='outside'
        ),
        row=2, col=2
    )

    sp_fig.add_trace(
        go.Bar(
            x=comparison_data['Metric'],
            y=comparison_data['System Avg'],
            name='System Average',
            marker_color='lightgray',
            text=[f"{x:.1f}%" for x in comparison_data['System Avg']],
            textposition='outside'
        ),
        row=2, col=2
    )

    # Layout
    sp_fig.update_layout(
        height=800,
        width=1400,
        title_text=f"<b>{sp_id} - Detailed Analysis</b><br>" +
                   f"<sub>Total Requests: {sp_metrics['total_requests']} | " +
                   f"Success Rate: {sp_metrics['success_rate']:.1f}% | " +
                   f"Rank: #{sp_metrics_df[sp_metrics_df['success_rate'] >= sp_metrics['success_rate']].shape[0]}/{len(sp_metrics_df)}</sub>",
        title_font_size=18,
        showlegend=True,
        template='plotly_white'
    )

    sp_fig.update_xaxes(title_text="Status", row=2, col=1)
    sp_fig.update_yaxes(title_text="Failure Count", row=2, col=1)

    sp_fig.update_xaxes(title_text="Metric", row=2, col=2)
    sp_fig.update_yaxes(title_text="Rate (%)", row=2, col=2)

    # Save
    sp_output = output_dir / f"{sp_id.replace(' ', '_')}_analysis.html"
    sp_fig.write_html(str(sp_output))
    print(f"  [OK] Saved: {sp_output.name}")

print(f"\n[SUCCESS] Generated {len(sp_metrics_df)} individual SP reports in: {output_dir}")
print("\n" + "="*80)
print("INTERACTIVE DASHBOARD GENERATION COMPLETE")
print("="*80)
