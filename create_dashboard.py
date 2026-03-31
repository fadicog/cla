"""
Create Interactive HTML Dashboard for UAE PASS Sharing Transactions
Combines all visualizations into a single interactive dashboard
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# UAE PASS brand colors
BRAND_COLORS = {
    'primary': '#0066CC',
    'secondary': '#00A3A1',
    'success': '#00C853',
    'warning': '#FFA000',
    'error': '#D32F2F',
    'neutral': '#757575',
    'light_blue': '#64B5F6',
    'light_teal': '#4DB6AC',
    'dark_blue': '#003D7A'
}

STATUS_DEFINITIONS = {
    'S00': 'Request Created', 'S01': 'Notification Sent', 'S02': 'Notification Delivered',
    'S03': 'Notification Opened', 'S04': 'Redirect Launched', 'S05': 'Redirect Landed',
    'S06': 'QR Rendered', 'S07': 'QR Scanned', 'S08': 'Request Viewed',
    'S10': 'Docs Ready at Open', 'S11': 'Docs Missing at Open',
    'S12': 'Missing Doc Request Initiated', 'S13': 'Missing Doc Request Success',
    'S14': 'Missing Doc Request Error', 'S15': 'Missing Doc Not Found',
    'S20': 'Awaiting Consent', 'S21': 'Consent Given', 'S30': 'PIN Requested',
    'S31': 'PIN Verified', 'S32': 'PIN Failed', 'S40': 'Share Success',
    'S41': 'Share Tech Error', 'S42': 'Expired', 'S43': 'User Aborted', 'S44': 'Not Eligible'
}

TERMINAL_STATUSES = ['S40', 'S41', 'S42', 'S43', 'S44']

def load_data(filepath):
    """Load and prepare data"""
    df = pd.read_csv(filepath)
    df['status_ts'] = pd.to_datetime(df['status_ts'])
    df = df.sort_values(['request_id', 'status_ts'])
    return df

def get_summary(df):
    """Create request-level summary"""
    terminal_status = df[df['status_code'].isin(TERMINAL_STATUSES)].groupby('request_id').agg({
        'status_code': 'first',
        'status_ts': 'first'
    }).rename(columns={'status_code': 'terminal_status', 'status_ts': 'terminal_ts'})

    first_status = df.groupby('request_id').agg({
        'sp_id': 'first',
        'channel': 'first',
        'platform': 'first',
        'status_ts': 'first',
        'required_count': 'first'
    }).rename(columns={'status_ts': 'start_ts'})

    summary = first_status.join(terminal_status, how='left')
    summary['journey_time_ms'] = (summary['terminal_ts'] - summary['start_ts']).dt.total_seconds() * 1000

    docs_ready = df[df['status_code'] == 'S10'].groupby('request_id').size()
    docs_missing = df[df['status_code'] == 'S11'].groupby('request_id').size()

    summary['docs_ready_at_open'] = summary.index.isin(docs_ready.index)
    summary['docs_missing_at_open'] = summary.index.isin(docs_missing.index)

    for status in ['S08', 'S20', 'S21', 'S30', 'S31']:
        summary[f'reached_{status}'] = summary.index.isin(
            df[df['status_code'] == status]['request_id'].unique()
        )

    return summary

def create_dashboard(df, summary):
    """Create comprehensive interactive dashboard"""

    # Create HTML structure
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UAE PASS Sharing Transactions Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            color: #333;
        }

        .dashboard-container {
            max-width: 1800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            padding: 30px;
        }

        .header {
            text-align: center;
            padding: 20px 0 40px 0;
            border-bottom: 3px solid #0066CC;
            margin-bottom: 40px;
        }

        .header h1 {
            color: #0066CC;
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            color: #666;
            font-size: 1.1em;
        }

        .metrics-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 12px;
            color: white;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px);
        }

        .metric-card.success {
            background: linear-gradient(135deg, #00C853 0%, #00A000 100%);
        }

        .metric-card.warning {
            background: linear-gradient(135deg, #FFA000 0%, #FF6F00 100%);
        }

        .metric-card.error {
            background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%);
        }

        .metric-card.info {
            background: linear-gradient(135deg, #0066CC 0%, #003D7A 100%);
        }

        .metric-label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            line-height: 1;
        }

        .chart-section {
            margin-bottom: 50px;
        }

        .section-title {
            color: #0066CC;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
            font-weight: 600;
        }

        .chart-container {
            background: #fafafa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
        }

        .insight-box {
            background: #e3f2fd;
            border-left: 4px solid #0066CC;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 5px;
        }

        .insight-box h4 {
            color: #0066CC;
            margin-bottom: 8px;
            font-size: 1.1em;
        }

        .insight-box p {
            color: #555;
            line-height: 1.6;
        }

        .footer {
            text-align: center;
            padding: 30px 0;
            margin-top: 50px;
            border-top: 2px solid #e0e0e0;
            color: #666;
        }

        @media (max-width: 768px) {
            .chart-grid {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 1.8em;
            }

            .metric-value {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <h1>UAE PASS Digital Documents</h1>
            <p>Sharing Transactions Analysis Dashboard</p>
        </div>

        <!-- Key Metrics -->
        <div class="metrics-row" id="metrics">
            <!-- Metrics will be inserted here -->
        </div>

        <!-- Channel Funnels -->
        <div class="chart-section">
            <h2 class="section-title">Channel Performance Funnels</h2>
            <div class="insight-box">
                <h4>Key Insight</h4>
                <p>Compare how users progress through different channels (Notification, QR, Redirect).
                Identify drop-off points and optimize the user journey for each channel.</p>
            </div>
            <div class="chart-grid">
                <div class="chart-container" id="funnel-notification"></div>
                <div class="chart-container" id="funnel-qr"></div>
                <div class="chart-container" id="funnel-redirect"></div>
            </div>
        </div>

        <!-- Terminal Status Analysis -->
        <div class="chart-section">
            <h2 class="section-title">Terminal Status Analysis</h2>
            <div class="chart-grid">
                <div class="chart-container" id="terminal-overall"></div>
                <div class="chart-container" id="terminal-channel"></div>
            </div>
        </div>

        <!-- Document Readiness Impact -->
        <div class="chart-section">
            <h2 class="section-title">Document Readiness Impact</h2>
            <div class="insight-box">
                <h4>Critical Factor</h4>
                <p>Document availability at first view is THE critical success factor.
                Requests where docs are ready have significantly higher success rates.</p>
            </div>
            <div class="chart-grid">
                <div class="chart-container" id="doc-readiness-success"></div>
                <div class="chart-container" id="doc-missing-outcomes"></div>
            </div>
        </div>

        <!-- Channel & Platform Comparison -->
        <div class="chart-section">
            <h2 class="section-title">Channel & Platform Performance</h2>
            <div class="chart-grid">
                <div class="chart-container" id="channel-success"></div>
                <div class="chart-container" id="platform-success"></div>
            </div>
        </div>

        <!-- Service Provider Analysis -->
        <div class="chart-section">
            <h2 class="section-title">Service Provider Analysis</h2>
            <div class="chart-grid">
                <div class="chart-container" id="sp-success"></div>
                <div class="chart-container" id="sp-volume"></div>
            </div>
        </div>

        <!-- Time Analysis -->
        <div class="chart-section">
            <h2 class="section-title">Time-to-Complete Analysis</h2>
            <div class="chart-grid">
                <div class="chart-container" id="time-distribution"></div>
                <div class="chart-container" id="time-by-channel"></div>
            </div>
        </div>

        <!-- Error Analysis -->
        <div class="chart-section">
            <h2 class="section-title">Error Analysis</h2>
            <div class="chart-grid">
                <div class="chart-container" id="error-types"></div>
                <div class="chart-container" id="error-sources"></div>
            </div>
        </div>

        <div class="footer">
            <p><strong>UAE PASS Digital Documents - Sharing Transactions Dashboard</strong></p>
            <p>Generated on: """ + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        </div>
    </div>

    <script>
        // Configuration for all Plotly charts
        const config = {
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
        };

        const layout_template = {
            font: {family: 'Segoe UI', size: 12},
            plot_bgcolor: '#fafafa',
            paper_bgcolor: '#fafafa',
            margin: {l: 60, r: 40, t: 60, b: 60}
        };
"""

    # Calculate metrics
    total_requests = len(summary)
    successful = (summary['terminal_status'] == 'S40').sum()
    success_rate = successful / total_requests * 100
    docs_ready_pct = summary['docs_ready_at_open'].sum() / total_requests * 100
    median_time = summary[summary['terminal_status'] == 'S40']['journey_time_ms'].median() / 1000

    # Add metrics to HTML
    html_content += f"""
        // Insert metrics
        const metricsHTML = `
            <div class="metric-card info">
                <div class="metric-label">Total Requests</div>
                <div class="metric-value">{total_requests:,}</div>
            </div>
            <div class="metric-card success">
                <div class="metric-label">Success Rate</div>
                <div class="metric-value">{success_rate:.1f}%</div>
            </div>
            <div class="metric-card warning">
                <div class="metric-label">Docs Ready at Open</div>
                <div class="metric-value">{docs_ready_pct:.1f}%</div>
            </div>
            <div class="metric-card info">
                <div class="metric-label">Median Time (Success)</div>
                <div class="metric-value">{median_time:.1f}s</div>
            </div>
        `;
        document.getElementById('metrics').innerHTML = metricsHTML;
"""

    # Create channel funnels
    for channel in df['channel'].unique():
        channel_requests = summary[summary['channel'] == channel]
        total = len(channel_requests)

        if channel == 'notification':
            stages = ['S00', 'S01', 'S02', 'S03', 'S08', 'S10', 'S21', 'S30', 'S31', 'S40']
        elif channel == 'redirect':
            stages = ['S00', 'S04', 'S05', 'S08', 'S10', 'S21', 'S30', 'S31', 'S40']
        else:  # qr
            stages = ['S00', 'S06', 'S07', 'S08', 'S10', 'S21', 'S30', 'S31', 'S40']

        counts = []
        channel_df = df[df['channel'] == channel]

        for status in stages:
            if status == 'S00':
                count = total
            elif status == 'S10':
                count = summary[(summary['channel'] == channel) & (summary['reached_S08'] == True)]['docs_ready_at_open'].sum()
                s13_count = len(df[(df['channel'] == channel) & (df['status_code'] == 'S13')]['request_id'].unique())
                count += s13_count
            else:
                count = len(channel_df[channel_df['status_code'] == status]['request_id'].unique())
            counts.append(count)

        labels = [STATUS_DEFINITIONS.get(s, s) for s in stages]

        html_content += f"""
        // {channel.capitalize()} Funnel
        Plotly.newPlot('funnel-{channel}', [{{
            type: 'funnel',
            y: {labels},
            x: {counts},
            textposition: 'inside',
            textinfo: 'value+percent initial',
            marker: {{
                color: '#0066CC',
                line: {{width: 2, color: 'white'}}
            }},
            connector: {{
                line: {{color: '#757575', width: 1, dash: 'dot'}}
            }}
        }}], {{
            ...layout_template,
            title: '{channel.capitalize()} Channel Funnel<br><sub>Total: {total:,} requests</sub>',
            height: 500
        }}, config);
"""

    # Terminal status overall
    terminal_counts = summary['terminal_status'].value_counts()
    terminal_labels = [STATUS_DEFINITIONS.get(s, s) for s in terminal_counts.index]
    colors_map = {
        'S40': BRAND_COLORS['success'], 'S41': BRAND_COLORS['error'],
        'S42': BRAND_COLORS['warning'], 'S43': BRAND_COLORS['neutral'],
        'S44': BRAND_COLORS['error']
    }
    terminal_colors = [colors_map.get(s, BRAND_COLORS['neutral']) for s in terminal_counts.index]

    html_content += f"""
        // Terminal Status Overall
        Plotly.newPlot('terminal-overall', [{{
            type: 'pie',
            labels: {terminal_labels},
            values: {terminal_counts.values.tolist()},
            marker: {{colors: {terminal_colors}}},
            textinfo: 'label+percent',
            textposition: 'outside',
            hole: 0.4
        }}], {{
            ...layout_template,
            title: 'Terminal Status Distribution',
            height: 450
        }}, config);
"""

    # Terminal by channel
    channel_terminal = summary.groupby(['channel', 'terminal_status']).size().unstack(fill_value=0)
    html_content += """
        // Terminal by Channel
        const terminalByChannel = {
            data: [
"""

    for status in TERMINAL_STATUSES:
        if status in channel_terminal.columns:
            html_content += f"""
                {{
                    x: {channel_terminal.index.tolist()},
                    y: {channel_terminal[status].tolist()},
                    name: '{STATUS_DEFINITIONS.get(status, status)}',
                    type: 'bar',
                    marker: {{color: '{colors_map.get(status, BRAND_COLORS["neutral"])}'}},
                }},
"""

    html_content += f"""
            ],
            layout: {{
                ...layout_template,
                title: 'Terminal Status by Channel',
                barmode: 'stack',
                height: 450,
                xaxis: {{title: 'Channel'}},
                yaxis: {{title: 'Count'}}
            }}
        }};
        Plotly.newPlot('terminal-channel', terminalByChannel.data, terminalByChannel.layout, config);
"""

    # Document readiness success rate
    docs_ready = summary[summary['docs_ready_at_open'] == True]
    docs_missing = summary[summary['docs_missing_at_open'] == True]
    ready_success_rate = (docs_ready['terminal_status'] == 'S40').sum() / len(docs_ready) * 100 if len(docs_ready) > 0 else 0
    missing_success_rate = (docs_missing['terminal_status'] == 'S40').sum() / len(docs_missing) * 100 if len(docs_missing) > 0 else 0

    html_content += f"""
        // Document Readiness Success Rate
        Plotly.newPlot('doc-readiness-success', [{{
            x: ['Docs Ready (S10)', 'Docs Missing (S11)'],
            y: [{ready_success_rate:.1f}, {missing_success_rate:.1f}],
            type: 'bar',
            text: ['{ready_success_rate:.1f}%', '{missing_success_rate:.1f}%'],
            textposition: 'outside',
            marker: {{
                color: ['{BRAND_COLORS["success"]}', '{BRAND_COLORS["warning"]}'],
                line: {{color: 'black', width: 2}}
            }}
        }}], {{
            ...layout_template,
            title: 'Success Rate: Docs Ready vs Missing at Open',
            yaxis: {{title: 'Success Rate (%)', range: [0, 100]}},
            height: 450
        }}, config);
"""

    # Missing doc outcomes
    s12_requests = df[df['status_code'] == 'S12']['request_id'].unique()
    s13_success = len(df[df['status_code'] == 'S13']['request_id'].unique())
    s14_error = len(df[df['status_code'] == 'S14']['request_id'].unique())
    s15_not_found = len(df[df['status_code'] == 'S15']['request_id'].unique())

    html_content += f"""
        // Missing Doc Outcomes
        Plotly.newPlot('doc-missing-outcomes', [{{
            labels: ['Success (S13)', 'Tech Error (S14)', 'Not Found (S15)'],
            values: [{s13_success}, {s14_error}, {s15_not_found}],
            type: 'pie',
            marker: {{
                colors: ['{BRAND_COLORS["success"]}', '{BRAND_COLORS["error"]}', '{BRAND_COLORS["warning"]}']
            }},
            textinfo: 'label+percent',
            textposition: 'outside',
            hole: 0.3
        }}], {{
            ...layout_template,
            title: 'Missing Doc Request Outcomes<br><sub>Total Requests: {len(s12_requests)}</sub>',
            height: 450
        }}, config);
"""

    # Channel success comparison
    channel_success = summary.groupby('channel').agg({
        'terminal_status': lambda x: (x == 'S40').sum(),
        'sp_id': 'count'
    })
    channel_success.rename(columns={'sp_id': 'total_count'}, inplace=True)
    channel_success['success_rate'] = channel_success['terminal_status'] / channel_success['total_count'] * 100

    html_content += f"""
        // Channel Success Rate
        Plotly.newPlot('channel-success', [{{
            x: {channel_success.index.tolist()},
            y: {channel_success['success_rate'].tolist()},
            type: 'bar',
            text: {[f'{v:.1f}%' for v in channel_success['success_rate'].tolist()]},
            textposition: 'outside',
            marker: {{color: '{BRAND_COLORS["primary"]}'}}
        }}], {{
            ...layout_template,
            title: 'Success Rate by Channel',
            xaxis: {{title: 'Channel'}},
            yaxis: {{title: 'Success Rate (%)', range: [0, 100]}},
            height: 450
        }}, config);
"""

    # Platform success comparison
    platform_success = summary.groupby('platform').agg({
        'terminal_status': lambda x: (x == 'S40').sum(),
        'channel': 'count'
    })
    platform_success.rename(columns={'channel': 'total_count'}, inplace=True)
    platform_success['success_rate'] = platform_success['terminal_status'] / platform_success['total_count'] * 100

    html_content += f"""
        // Platform Success Rate
        Plotly.newPlot('platform-success', [{{
            x: {[p.upper() for p in platform_success.index.tolist()]},
            y: {platform_success['success_rate'].tolist()},
            type: 'bar',
            text: {[f'{v:.1f}%' for v in platform_success['success_rate'].tolist()]},
            textposition: 'outside',
            marker: {{color: ['{BRAND_COLORS["primary"]}', '{BRAND_COLORS["success"]}']}}
        }}], {{
            ...layout_template,
            title: 'Success Rate: iOS vs Android',
            xaxis: {{title: 'Platform'}},
            yaxis: {{title: 'Success Rate (%)', range: [0, 100]}},
            height: 450
        }}, config);
"""

    # SP Success Rate
    sp_success = summary.groupby('sp_id').agg({
        'terminal_status': lambda x: (x == 'S40').sum(),
        'channel': 'count'
    })
    sp_success.rename(columns={'channel': 'total_count'}, inplace=True)
    sp_success['success_rate'] = sp_success['terminal_status'] / sp_success['total_count'] * 100
    sp_success = sp_success.sort_values('success_rate', ascending=True)

    html_content += f"""
        // SP Success Rate
        Plotly.newPlot('sp-success', [{{
            y: {sp_success.index.tolist()},
            x: {sp_success['success_rate'].tolist()},
            type: 'bar',
            orientation: 'h',
            text: {[f'{v:.1f}%' for v in sp_success['success_rate'].tolist()]},
            textposition: 'outside',
            marker: {{color: '{BRAND_COLORS["primary"]}'}}
        }}], {{
            ...layout_template,
            title: 'Success Rate by Service Provider',
            xaxis: {{title: 'Success Rate (%)', range: [0, 110]}},
            yaxis: {{title: ''}},
            height: 500
        }}, config);
"""

    # SP Volume
    sp_volume = summary['sp_id'].value_counts()

    html_content += f"""
        // SP Volume
        Plotly.newPlot('sp-volume', [{{
            y: {sp_volume.index.tolist()},
            x: {sp_volume.values.tolist()},
            type: 'bar',
            orientation: 'h',
            text: {[f'{v:,}' for v in sp_volume.values.tolist()]},
            textposition: 'outside',
            marker: {{color: '{BRAND_COLORS["secondary"]}'}}
        }}], {{
            ...layout_template,
            title: 'Request Volume by Service Provider',
            xaxis: {{title: 'Number of Requests'}},
            yaxis: {{title: ''}},
            height: 500
        }}, config);
"""

    # Time distribution for successful requests
    successful = summary[summary['terminal_status'] == 'S40'].copy()
    successful['journey_time_sec'] = successful['journey_time_ms'] / 1000

    html_content += f"""
        // Time Distribution
        Plotly.newPlot('time-distribution', [{{
            x: {successful['journey_time_sec'].tolist()},
            type: 'histogram',
            nbinsx: 30,
            marker: {{color: '{BRAND_COLORS["success"]}'}},
            name: 'Frequency'
        }}], {{
            ...layout_template,
            title: 'Time-to-Complete Distribution (Successful Requests)<br><sub>Median: {successful["journey_time_sec"].median():.1f}s | P90: {successful["journey_time_sec"].quantile(0.9):.1f}s</sub>',
            xaxis: {{title: 'Journey Time (seconds)'}},
            yaxis: {{title: 'Frequency'}},
            height: 450,
            shapes: [
                {{
                    type: 'line',
                    x0: {successful['journey_time_sec'].median():.1f},
                    x1: {successful['journey_time_sec'].median():.1f},
                    y0: 0,
                    y1: 1,
                    yref: 'paper',
                    line: {{color: '{BRAND_COLORS["dark_blue"]}', width: 2, dash: 'dash'}}
                }},
                {{
                    type: 'line',
                    x0: {successful['journey_time_sec'].quantile(0.9):.1f},
                    x1: {successful['journey_time_sec'].quantile(0.9):.1f},
                    y0: 0,
                    y1: 1,
                    yref: 'paper',
                    line: {{color: '{BRAND_COLORS["error"]}', width: 2, dash: 'dash'}}
                }}
            ]
        }}, config);
"""

    # Time by channel
    channel_times = {}
    for channel in successful['channel'].unique():
        channel_data = successful[successful['channel'] == channel]['journey_time_sec'].values
        channel_times[channel] = channel_data.tolist()

    html_content += """
        // Time by Channel
        const timeByChannel = {
            data: [
"""

    for channel, times in channel_times.items():
        html_content += f"""
                {{
                    y: {times},
                    type: 'box',
                    name: '{channel.capitalize()}',
                    boxmean: 'sd'
                }},
"""

    html_content += f"""
            ],
            layout: {{
                ...layout_template,
                title: 'Journey Time by Channel (Successful Requests)',
                yaxis: {{title: 'Journey Time (seconds)'}},
                height: 450
            }}
        }};
        Plotly.newPlot('time-by-channel', timeByChannel.data, timeByChannel.layout, config);
"""

    # Error analysis
    errors = df[df['error_code'].notna()].copy()

    if len(errors) > 0:
        error_counts = errors['error_code'].value_counts()
        source_counts = errors['error_source'].value_counts()

        html_content += f"""
        // Error Types
        Plotly.newPlot('error-types', [{{
            y: {error_counts.index.tolist()},
            x: {error_counts.values.tolist()},
            type: 'bar',
            orientation: 'h',
            text: {[f'{v:,}' for v in error_counts.values.tolist()]},
            textposition: 'outside',
            marker: {{color: '{BRAND_COLORS["error"]}'}}
        }}], {{
            ...layout_template,
            title: 'Error Type Distribution',
            xaxis: {{title: 'Count'}},
            yaxis: {{title: ''}},
            height: 450
        }}, config);

        // Error Sources
        Plotly.newPlot('error-sources', [{{
            labels: {source_counts.index.tolist()},
            values: {source_counts.values.tolist()},
            type: 'pie',
            marker: {{
                colors: ['{BRAND_COLORS["error"]}', '{BRAND_COLORS["warning"]}', '{BRAND_COLORS["neutral"]}', '{BRAND_COLORS["light_blue"]}']
            }},
            textinfo: 'label+percent',
            textposition: 'outside',
            hole: 0.3
        }}], {{
            ...layout_template,
            title: 'Error Source Distribution<br><sub>Total Errors: {len(errors)}</sub>',
            height: 450
        }}, config);
"""

    html_content += """
    </script>
</body>
</html>
"""

    return html_content

def main():
    print("Creating interactive dashboard...")

    # Load data
    df = load_data(r"D:\cluade\sharing_transactions_sample.csv")
    summary = get_summary(df)

    print(f"Loaded {len(df)} status records for {len(summary)} requests")

    # Create dashboard
    dashboard_html = create_dashboard(df, summary)

    # Save
    output_path = r"D:\cluade\visualizations\interactive_dashboard.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(dashboard_html)

    print(f"Dashboard created: {output_path}")
    print("\nOpen the file in a web browser to view the interactive dashboard!")

if __name__ == "__main__":
    main()
