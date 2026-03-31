"""
Interactive Dashboard for UAE PASS Sharing Request Analysis
Built with Plotly Dash

Run this file to launch the interactive dashboard in your browser.
Usage: python sharing_analysis_dashboard.py
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
import numpy as np

# Load data
print("Loading data...")
df = pd.read_csv(r'D:\cluade\sharing_transactions_new_sample.csv')
df['status_ts'] = pd.to_datetime(df['status_ts'])
df['required_docs_list'] = df['required_docs'].apply(lambda x: json.loads(x) if pd.notna(x) else [])
df['status_history_list'] = df['status_history'].apply(lambda x: json.loads(x) if pd.notna(x) else [])

# Terminal statuses
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

# Status definitions
STATUS_DEFINITIONS = {
    'S00': 'Request Created', 'S01': 'Notification Sent', 'S02': 'Notification Delivered',
    'S03': 'Notification Tapped', 'S04': 'Redirect Initiated', 'S05': 'App Opened (Redirect)',
    'S06': 'QR Scanned', 'S07': 'QR Validated', 'S08': 'Request Loaded',
    'S10': 'Documents Ready', 'S11': 'Documents Missing', 'S12': 'Retrieval Started',
    'S13': 'Retrieval Success', 'S14': 'Retrieval Failed (Network)', 'S15': 'Retrieval Failed (Issuer)',
    'S20': 'Consent Screen Shown', 'S21': 'Consent Granted', 'S22': 'Consent Denied',
    'S30': 'PIN Required', 'S31': 'PIN Success', 'S32': 'PIN Failed',
    'S40': 'Success (Shared)', 'S41': 'Technical Error', 'S42': 'Expired',
    'S43': 'User Aborted', 'S44': 'Not Eligible'
}

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define color scheme
COLORS = {
    'S40': '#2ecc71',  # Success - green
    'S41': '#e74c3c',  # Technical error - red
    'S42': '#f39c12',  # Expired - orange
    'S43': '#e67e22',  # User abort - dark orange
    'S44': '#95a5a6',  # Not eligible - gray
    'primary': '#3498db',
    'secondary': '#9b59b6',
    'background': '#ecf0f1',
    'text': '#2c3e50'
}

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("UAE PASS Digital Documents - Sharing Request Analysis Dashboard",
                style={'textAlign': 'center', 'color': COLORS['text'], 'marginBottom': 10}),
        html.P("Interactive analysis of 500 sharing requests (5,068 events) | November 1-28, 2025",
               style={'textAlign': 'center', 'color': COLORS['text'], 'fontSize': 14}),
    ], style={'backgroundColor': COLORS['background'], 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),

    # Filters
    html.Div([
        html.Div([
            html.Label("Channel:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='channel-filter',
                options=[{'label': 'All', 'value': 'all'}] + [{'label': c.title(), 'value': c} for c in df['channel'].unique()],
                value='all',
                style={'width': '200px'}
            ),
        ], style={'display': 'inline-block', 'marginRight': '20px'}),

        html.Div([
            html.Label("Platform:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='platform-filter',
                options=[{'label': 'All', 'value': 'all'}] + [{'label': p.upper(), 'value': p} for p in df['platform'].unique()],
                value='all',
                style={'width': '200px'}
            ),
        ], style={'display': 'inline-block', 'marginRight': '20px'}),

        html.Div([
            html.Label("Service Provider:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='sp-filter',
                options=[{'label': 'All', 'value': 'all'}] + [{'label': sp, 'value': sp} for sp in sorted(df['sp_id'].unique())],
                value='all',
                style={'width': '300px'}
            ),
        ], style={'display': 'inline-block'}),
    ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'marginBottom': '20px'}),

    # Key metrics cards
    html.Div(id='metrics-cards', style={'marginBottom': '20px'}),

    # Tabs for different analyses
    dcc.Tabs([
        dcc.Tab(label='Overview', children=[
            html.Div([
                html.Div([dcc.Graph(id='terminal-distribution')], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(id='channel-performance')], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '2%'}),
            ]),
            html.Div([
                html.Div([dcc.Graph(id='platform-comparison')], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(id='journey-duration')], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '2%'}),
            ]),
        ]),

        dcc.Tab(label='Status Transitions', children=[
            html.Div([
                dcc.Graph(id='transition-heatmap', style={'height': '800px'}),
            ]),
            html.Div([
                html.Div([dcc.Graph(id='top-transitions')], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(id='critical-dropoffs')], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '2%'}),
            ]),
        ]),

        dcc.Tab(label='Errors & Issues', children=[
            html.Div([
                html.Div([dcc.Graph(id='error-codes')], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(id='error-sources')], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '2%'}),
            ]),
            html.Div([
                html.Div([dcc.Graph(id='error-by-status')], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(id='abandonment-points')], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '2%'}),
            ]),
        ]),

        dcc.Tab(label='Service Providers', children=[
            html.Div([
                dcc.Graph(id='sp-performance', style={'height': '600px'}),
            ]),
            html.Div([
                html.Div([dcc.Graph(id='sp-volume-success')], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(id='sp-failure-modes')], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '2%'}),
            ]),
        ]),

        dcc.Tab(label='Conversion Funnel', children=[
            html.Div([
                dcc.Graph(id='conversion-funnel', style={'height': '600px'}),
            ]),
            html.Div([
                html.Div([dcc.Graph(id='funnel-dropoff-chart')], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(id='user-behavior')], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '2%'}),
            ]),
        ]),
    ]),
], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'})

# Helper function to filter data
def filter_data(df_input, channel, platform, sp):
    df_filtered = df_input.copy()
    if channel != 'all':
        df_filtered = df_filtered[df_filtered['channel'] == channel]
    if platform != 'all':
        df_filtered = df_filtered[df_filtered['platform'] == platform]
    if sp != 'all':
        df_filtered = df_filtered[df_filtered['sp_id'] == sp]
    return df_filtered

# Callbacks
@callback(
    Output('metrics-cards', 'children'),
    [Input('channel-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('sp-filter', 'value')]
)
def update_metrics(channel, platform, sp):
    filtered_terminal = filter_data(terminal_statuses, channel, platform, sp)

    total = len(filtered_terminal)
    success_rate = (filtered_terminal['terminal_status'] == 'S40').mean() * 100
    abort_rate = (filtered_terminal['terminal_status'] == 'S43').mean() * 100
    error_rate = (filtered_terminal['terminal_status'] == 'S41').mean() * 100
    expiry_rate = (filtered_terminal['terminal_status'] == 'S42').mean() * 100
    avg_time = filtered_terminal[filtered_terminal['terminal_status'] == 'S40']['journey_duration_ms'].mean() / 1000

    return html.Div([
        html.Div([
            html.H3(f"{total}", style={'color': COLORS['primary'], 'marginBottom': '5px'}),
            html.P("Total Requests", style={'color': COLORS['text'], 'fontSize': '14px'}),
        ], style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center',
                  'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'marginRight': '2%'}),

        html.Div([
            html.H3(f"{success_rate:.1f}%", style={'color': COLORS['S40'], 'marginBottom': '5px'}),
            html.P("Success Rate", style={'color': COLORS['text'], 'fontSize': '14px'}),
        ], style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center',
                  'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'marginRight': '2%'}),

        html.Div([
            html.H3(f"{abort_rate:.1f}%", style={'color': COLORS['S43'], 'marginBottom': '5px'}),
            html.P("User Abort", style={'color': COLORS['text'], 'fontSize': '14px'}),
        ], style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center',
                  'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'marginRight': '2%'}),

        html.Div([
            html.H3(f"{error_rate:.1f}%", style={'color': COLORS['S41'], 'marginBottom': '5px'}),
            html.P("Technical Error", style={'color': COLORS['text'], 'fontSize': '14px'}),
        ], style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center',
                  'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'marginRight': '2%'}),

        html.Div([
            html.H3(f"{expiry_rate:.1f}%", style={'color': COLORS['S42'], 'marginBottom': '5px'}),
            html.P("Expired", style={'color': COLORS['text'], 'fontSize': '14px'}),
        ], style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center',
                  'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'marginRight': '2%'}),

        html.Div([
            html.H3(f"{avg_time:.1f}s", style={'color': COLORS['primary'], 'marginBottom': '5px'}),
            html.P("Avg Time (Success)", style={'color': COLORS['text'], 'fontSize': '14px'}),
        ], style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center',
                  'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px'}),
    ])

@callback(
    Output('terminal-distribution', 'figure'),
    [Input('channel-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('sp-filter', 'value')]
)
def update_terminal_distribution(channel, platform, sp):
    filtered_terminal = filter_data(terminal_statuses, channel, platform, sp)
    counts = filtered_terminal['terminal_status'].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=[f"{status}<br>{STATUS_DEFINITIONS[status]}" for status in counts.index],
        values=counts.values,
        marker_colors=[COLORS.get(status, COLORS['primary']) for status in counts.index],
        hole=0.4,
        textinfo='percent+value'
    )])

    fig.update_layout(
        title="Terminal Status Distribution",
        height=400,
        showlegend=True
    )
    return fig

@callback(
    Output('channel-performance', 'figure'),
    [Input('channel-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('sp-filter', 'value')]
)
def update_channel_performance(channel, platform, sp):
    filtered_terminal = filter_data(terminal_statuses, channel, platform, sp)

    if channel != 'all':
        # If filtering by channel, show terminal status breakdown
        channel_data = filtered_terminal.groupby('terminal_status').size()
        fig = go.Figure(data=[go.Bar(
            x=channel_data.index,
            y=channel_data.values,
            marker_color=[COLORS.get(status, COLORS['primary']) for status in channel_data.index],
            text=channel_data.values,
            textposition='auto'
        )])
        fig.update_layout(
            title=f"{channel.title()} Channel - Terminal Status Breakdown",
            xaxis_title="Terminal Status",
            yaxis_title="Number of Requests",
            height=400
        )
    else:
        # Show channel comparison
        channel_perf = filtered_terminal.groupby('channel').agg({
            'request_id': 'count',
            'terminal_status': lambda x: (x == 'S40').sum()
        }).reset_index()
        channel_perf.columns = ['channel', 'total', 'successful']
        channel_perf['success_rate'] = channel_perf['successful'] / channel_perf['total'] * 100

        fig = go.Figure(data=[go.Bar(
            x=channel_perf['channel'],
            y=channel_perf['success_rate'],
            marker_color=[COLORS['S40'], COLORS['primary'], COLORS['secondary']],
            text=[f"{rate:.1f}%" for rate in channel_perf['success_rate']],
            textposition='auto'
        )])
        fig.update_layout(
            title="Success Rate by Channel",
            xaxis_title="Channel",
            yaxis_title="Success Rate (%)",
            height=400,
            yaxis_range=[0, 100]
        )
    return fig

@callback(
    Output('platform-comparison', 'figure'),
    [Input('channel-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('sp-filter', 'value')]
)
def update_platform_comparison(channel, platform, sp):
    filtered_terminal = filter_data(terminal_statuses, channel, platform, sp)

    if platform != 'all':
        # Show terminal status breakdown for selected platform
        platform_data = filtered_terminal.groupby('terminal_status').size()
        fig = go.Figure(data=[go.Bar(
            x=platform_data.index,
            y=platform_data.values,
            marker_color=[COLORS.get(status, COLORS['primary']) for status in platform_data.index],
            text=platform_data.values,
            textposition='auto'
        )])
        fig.update_layout(
            title=f"{platform.upper()} Platform - Terminal Status Breakdown",
            xaxis_title="Terminal Status",
            yaxis_title="Number of Requests",
            height=400
        )
    else:
        # Platform comparison
        platform_perf = filtered_terminal.groupby('platform').agg({
            'request_id': 'count',
            'terminal_status': lambda x: (x == 'S40').sum()
        }).reset_index()
        platform_perf.columns = ['platform', 'total', 'successful']
        platform_perf['success_rate'] = platform_perf['successful'] / platform_perf['total'] * 100

        fig = go.Figure(data=[go.Bar(
            x=platform_perf['platform'],
            y=platform_perf['success_rate'],
            marker_color=[COLORS['primary'], COLORS['S40']],
            text=[f"{rate:.1f}%" for rate in platform_perf['success_rate']],
            textposition='auto'
        )])
        fig.update_layout(
            title="Success Rate by Platform",
            xaxis_title="Platform",
            yaxis_title="Success Rate (%)",
            height=400,
            yaxis_range=[0, 100]
        )
    return fig

@callback(
    Output('journey-duration', 'figure'),
    [Input('channel-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('sp-filter', 'value')]
)
def update_journey_duration(channel, platform, sp):
    filtered_terminal = filter_data(terminal_statuses, channel, platform, sp)

    success_durations = filtered_terminal[filtered_terminal['terminal_status'] == 'S40']['journey_duration_ms'] / 1000
    failure_durations = filtered_terminal[filtered_terminal['terminal_status'] != 'S40']['journey_duration_ms'] / 1000

    fig = go.Figure()
    fig.add_trace(go.Box(
        y=success_durations,
        name='Success',
        marker_color=COLORS['S40'],
        boxmean='sd'
    ))
    fig.add_trace(go.Box(
        y=failure_durations,
        name='Failed',
        marker_color=COLORS['S41'],
        boxmean='sd'
    ))

    fig.update_layout(
        title="Journey Duration: Success vs Failure",
        yaxis_title="Duration (seconds)",
        height=400,
        showlegend=True
    )
    return fig

@callback(
    Output('transition-heatmap', 'figure'),
    [Input('channel-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('sp-filter', 'value')]
)
def update_transition_heatmap(channel, platform, sp):
    filtered_df = filter_data(df, channel, platform, sp)

    transitions = filtered_df[filtered_df['previous_status'].notna()][['previous_status', 'status_code']].copy()
    transition_counts = transitions.groupby(['previous_status', 'status_code']).size().reset_index(name='count')

    all_statuses = sorted(filtered_df['status_code'].unique())
    transition_matrix = pd.DataFrame(0, index=all_statuses, columns=all_statuses)
    for _, row in transition_counts.iterrows():
        transition_matrix.loc[row['previous_status'], row['status_code']] = row['count']

    fig = go.Figure(data=go.Heatmap(
        z=transition_matrix.values,
        x=transition_matrix.columns,
        y=transition_matrix.index,
        colorscale='YlOrRd',
        text=transition_matrix.values,
        texttemplate='%{text}',
        textfont={"size": 10},
        hovertemplate='From: %{y}<br>To: %{x}<br>Count: %{z}<extra></extra>'
    ))

    fig.update_layout(
        title="Status Transition Heatmap",
        xaxis_title="To Status",
        yaxis_title="From Status",
        height=800
    )
    return fig

@callback(
    Output('sp-performance', 'figure'),
    [Input('channel-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('sp-filter', 'value')]
)
def update_sp_performance(channel, platform, sp):
    filtered_terminal = filter_data(terminal_statuses, channel, platform, sp)

    sp_perf = filtered_terminal.groupby('sp_id').agg({
        'request_id': 'count',
        'terminal_status': lambda x: (x == 'S40').sum()
    }).reset_index()
    sp_perf.columns = ['sp_id', 'total', 'successful']
    sp_perf['success_rate'] = sp_perf['successful'] / sp_perf['total'] * 100
    sp_perf = sp_perf.sort_values('success_rate', ascending=True)

    colors = ['#2ecc71' if rate >= 70 else '#f39c12' if rate >= 50 else '#e74c3c' for rate in sp_perf['success_rate']]

    fig = go.Figure(data=[go.Bar(
        x=sp_perf['success_rate'],
        y=sp_perf['sp_id'],
        orientation='h',
        marker_color=colors,
        text=[f"{rate:.1f}% ({total} req)" for rate, total in zip(sp_perf['success_rate'], sp_perf['total'])],
        textposition='auto'
    )])

    fig.update_layout(
        title="Service Provider Performance (Success Rate)",
        xaxis_title="Success Rate (%)",
        yaxis_title="Service Provider",
        height=600,
        xaxis_range=[0, 100]
    )
    return fig

@callback(
    Output('conversion-funnel', 'figure'),
    [Input('channel-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('sp-filter', 'value')]
)
def update_conversion_funnel(channel, platform, sp):
    filtered_df = filter_data(df, channel, platform, sp)
    filtered_terminal = filter_data(terminal_statuses, channel, platform, sp)

    funnel_stages = {
        'S00': 'Request Created',
        'S08': 'Request Loaded',
        'S20': 'Consent Shown',
        'S21': 'Consent Granted',
        'S30': 'PIN Required',
        'S31': 'PIN Success',
        'S40': 'Success'
    }

    funnel_data = []
    for stage, label in funnel_stages.items():
        if stage == 'S40':
            count = (filtered_terminal['terminal_status'] == 'S40').sum()
        else:
            count = filtered_df[filtered_df['status_code'] == stage]['request_id'].nunique()
        funnel_data.append({'stage': label, 'count': count})

    funnel_df = pd.DataFrame(funnel_data)
    funnel_df['percentage'] = funnel_df['count'] / funnel_df['count'].iloc[0] * 100

    fig = go.Figure(go.Funnel(
        y=funnel_df['stage'],
        x=funnel_df['count'],
        textposition="inside",
        textinfo="value+percent initial",
        marker={"color": px.colors.sequential.Greens_r}
    ))

    fig.update_layout(
        title="Conversion Funnel (All Stages)",
        height=600
    )
    return fig

# Additional callbacks for other charts (simplified versions)
@callback(
    Output('error-codes', 'figure'),
    [Input('channel-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('sp-filter', 'value')]
)
def update_error_codes(channel, platform, sp):
    filtered_df = filter_data(df, channel, platform, sp)
    errors = filtered_df[filtered_df['error_code'].notna()]

    if len(errors) == 0:
        return go.Figure().add_annotation(text="No errors in filtered data", showarrow=False)

    error_counts = errors['error_code'].value_counts()
    fig = go.Figure(data=[go.Bar(
        x=error_counts.index,
        y=error_counts.values,
        marker_color=COLORS['S41'],
        text=error_counts.values,
        textposition='auto'
    )])
    fig.update_layout(
        title="Error Code Distribution",
        xaxis_title="Error Code",
        yaxis_title="Frequency",
        height=400
    )
    return fig

# Run the app
if __name__ == '__main__':
    print("\n" + "="*80)
    print("UAE PASS Sharing Request Analysis - Interactive Dashboard")
    print("="*80)
    print("\nStarting dashboard server...")
    print("Open your browser and navigate to: http://127.0.0.1:8050/")
    print("\nPress Ctrl+C to stop the server.")
    print("="*80 + "\n")

    app.run(debug=True, port=8050)
