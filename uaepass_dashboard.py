"""
UAE PASS Digital Documents - Sharing Request Tracking Dashboard

This interactive dashboard visualizes the document sharing request flow,
success/failure rates, and key performance metrics.

Requirements:
- pip install dash plotly pandas

Run: python uaepass_dashboard.py
Then open: http://127.0.0.1:8050/
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from datetime import datetime

# Load and prepare data
def load_data():
    """Load and preprocess the CSV data"""
    df = pd.read_csv('D:\\cluade\\csvdata-2.csv')

    # Clean column names (remove BOM and spaces)
    df.columns = df.columns.str.replace('\ufeff', '').str.strip()

    # Convert date column
    df['CREATED_AT'] = pd.to_datetime(df['CREATED_AT'], format='%d-%b-%y')

    # Expand rows based on COUNT column
    df_expanded = df.loc[df.index.repeat(df['COUNT'])].reset_index(drop=True)

    return df, df_expanded

df, df_expanded = load_data()

# Define status mappings
def categorize_status(row):
    """Categorize each record into funnel stages"""
    status = row['STATUS']
    consent_given = row['CONSENT_GIVEN']
    pin_given = row['PIN_GIVEN']
    docs_available = row['MANDATORY_DOCS_AVAILABLE']
    notification_state = row['NOTIFICATION_STATE']

    if status == 'Shared':
        return 'Success'
    elif status == 'Failed':
        return 'Failed'
    elif status == 'User Rejected':
        return 'User Rejected'
    elif status == 'No Action Taken':
        if pin_given == 'Yes':
            return 'PIN Entered - No Action'
        elif consent_given == 'Yes':
            return 'Consent Given - No Action'
        elif docs_available == 'Yes':
            return 'Ready for Review - No Action'
        else:
            return 'Missing Documents'
    elif status == 'Saved For Later':
        return 'Saved For Later'
    else:
        return 'Other'

df_expanded['STAGE'] = df_expanded.apply(categorize_status, axis=1)

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "UAE PASS DV - Sharing Request Analytics"

# Define color scheme
COLORS = {
    'success': '#28a745',
    'failure': '#dc3545',
    'in_progress': '#ffc107',
    'abandoned': '#6c757d',
    'primary': '#007bff',
    'background': '#f8f9fa'
}

# Calculate key metrics
total_requests = len(df_expanded)
success_count = len(df_expanded[df_expanded['STATUS'] == 'Shared'])
failure_count = len(df_expanded[df_expanded['STATUS'] == 'Failed'])
rejected_count = len(df_expanded[df_expanded['STATUS'] == 'User Rejected'])
success_rate = (success_count / total_requests * 100) if total_requests > 0 else 0

# Dashboard layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("UAE PASS Digital Documents", className="text-center mb-2"),
            html.H3("Sharing Request Analytics Dashboard", className="text-center text-muted mb-4")
        ])
    ]),

    # KPI Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Requests", className="text-muted"),
                    html.H2(f"{total_requests:,}", className="text-primary")
                ])
            ], className="shadow-sm")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Success Rate", className="text-muted"),
                    html.H2(f"{success_rate:.1f}%", className="text-success")
                ])
            ], className="shadow-sm")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Successful Shares", className="text-muted"),
                    html.H2(f"{success_count:,}", className="text-success")
                ])
            ], className="shadow-sm")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Failed/Rejected", className="text-muted"),
                    html.H2(f"{failure_count + rejected_count:,}", className="text-danger")
                ])
            ], className="shadow-sm")
        ], width=3),
    ], className="mb-4"),

    # Filters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Service Provider (SP):"),
                    dcc.Dropdown(
                        id='sp-filter',
                        options=[{'label': 'All', 'value': 'ALL'}] +
                                [{'label': sp, 'value': sp} for sp in df['ALIAS_NAME'].unique()],
                        value='ALL',
                        clearable=False
                    )
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Request Type:"),
                    dcc.Dropdown(
                        id='viz-type-filter',
                        options=[{'label': 'All', 'value': 'ALL'}] +
                                [{'label': vt, 'value': vt} for vt in df['VIZ_TYPE'].unique()],
                        value='ALL',
                        clearable=False
                    )
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Platform:"),
                    dcc.Dropdown(
                        id='platform-filter',
                        options=[{'label': 'All', 'value': 'ALL'},
                                {'label': 'Android', 'value': 'Android'},
                                {'label': 'IOS', 'value': 'IOS'}],
                        value='ALL',
                        clearable=False
                    )
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Date Range:"),
                    dcc.DatePickerRange(
                        id='date-filter',
                        start_date=df['CREATED_AT'].min(),
                        end_date=df['CREATED_AT'].max(),
                        display_format='DD-MMM-YY'
                    )
                ])
            ])
        ], width=3),
    ], className="mb-4"),

    # Main visualizations
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Sharing Request Funnel", className="card-title"),
                    dcc.Graph(id='funnel-chart', style={'height': '500px'})
                ])
            ], className="shadow-sm")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Outcome Distribution", className="card-title"),
                    dcc.Graph(id='outcome-pie', style={'height': '500px'})
                ])
            ], className="shadow-sm")
        ], width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Document Availability Impact", className="card-title"),
                    dcc.Graph(id='doc-availability-chart', style={'height': '400px'})
                ])
            ], className="shadow-sm")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Failure Breakdown", className="card-title"),
                    dcc.Graph(id='failure-breakdown', style={'height': '400px'})
                ])
            ], className="shadow-sm")
        ], width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Daily Request Volume", className="card-title"),
                    dcc.Graph(id='time-series', style={'height': '400px'})
                ])
            ], className="shadow-sm")
        ], width=12),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Status Distribution Details", className="card-title"),
                    dcc.Graph(id='status-distribution', style={'height': '400px'})
                ])
            ], className="shadow-sm")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Consent & PIN Completion Rate", className="card-title"),
                    dcc.Graph(id='consent-pin-chart', style={'height': '400px'})
                ])
            ], className="shadow-sm")
        ], width=6),
    ], className="mb-4"),

], fluid=True, style={'backgroundColor': COLORS['background']})

# Callbacks for interactivity
@app.callback(
    [Output('funnel-chart', 'figure'),
     Output('outcome-pie', 'figure'),
     Output('doc-availability-chart', 'figure'),
     Output('failure-breakdown', 'figure'),
     Output('time-series', 'figure'),
     Output('status-distribution', 'figure'),
     Output('consent-pin-chart', 'figure')],
    [Input('sp-filter', 'value'),
     Input('viz-type-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def update_charts(sp, viz_type, platform, start_date, end_date):
    # Filter data
    filtered_df = df_expanded.copy()

    if sp != 'ALL':
        filtered_df = filtered_df[filtered_df['ALIAS_NAME'] == sp]
    if viz_type != 'ALL':
        filtered_df = filtered_df[filtered_df['VIZ_TYPE'] == viz_type]
    if platform != 'ALL':
        filtered_df = filtered_df[filtered_df['USER_AGENT'] == platform]
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['CREATED_AT'] >= start_date) &
            (filtered_df['CREATED_AT'] <= end_date)
        ]

    # 1. FUNNEL CHART
    total = len(filtered_df)

    # Calculate funnel stages
    docs_available = len(filtered_df[filtered_df['MANDATORY_DOCS_AVAILABLE'] == 'Yes'])
    notification_read = len(filtered_df[filtered_df['NOTIFICATION_STATE'] == 'Read'])
    consent_given = len(filtered_df[filtered_df['CONSENT_GIVEN'] == 'Yes'])
    pin_entered = len(filtered_df[filtered_df['PIN_GIVEN'] == 'Yes'])
    successful = len(filtered_df[filtered_df['STATUS'] == 'Shared'])

    funnel_data = {
        'stage': ['Request Created', 'Docs Available', 'Notification Read',
                  'Consent Given', 'PIN Entered', 'Successfully Shared'],
        'count': [total, docs_available, notification_read, consent_given, pin_entered, successful],
        'percent': [100,
                   (docs_available/total*100) if total > 0 else 0,
                   (notification_read/total*100) if total > 0 else 0,
                   (consent_given/total*100) if total > 0 else 0,
                   (pin_entered/total*100) if total > 0 else 0,
                   (successful/total*100) if total > 0 else 0]
    }

    funnel_fig = go.Figure(go.Funnel(
        y=funnel_data['stage'],
        x=funnel_data['count'],
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=['#007bff', '#17a2b8', '#28a745', '#ffc107', '#fd7e14', '#28a745']),
        connector=dict(line=dict(color="royalblue", width=3))
    ))

    funnel_fig.update_layout(
        title_text=f"Request Flow (Total: {total:,} requests)",
        showlegend=False,
        height=500
    )

    # 2. OUTCOME PIE CHART
    outcome_counts = filtered_df['STATUS'].value_counts()

    outcome_fig = go.Figure(data=[go.Pie(
        labels=outcome_counts.index,
        values=outcome_counts.values,
        hole=0.4,
        marker=dict(colors=[
            COLORS['success'] if 'Shared' in str(label)
            else COLORS['failure'] if 'Failed' in str(label)
            else COLORS['abandoned'] if 'Rejected' in str(label)
            else COLORS['in_progress']
            for label in outcome_counts.index
        ])
    )])

    outcome_fig.update_layout(
        title_text=f"Final Outcomes ({total:,} requests)",
        height=500
    )

    # 3. DOCUMENT AVAILABILITY IMPACT
    docs_avail_grouped = filtered_df.groupby(['DOC_AVAILIBILITY', 'STATUS']).size().reset_index(name='count')

    doc_avail_fig = px.bar(
        docs_avail_grouped,
        x='DOC_AVAILIBILITY',
        y='count',
        color='STATUS',
        barmode='group',
        title="Success Rate by Document Availability",
        color_discrete_map={
            'Shared': COLORS['success'],
            'Failed': COLORS['failure'],
            'User Rejected': COLORS['abandoned'],
            'No Action Taken': COLORS['in_progress'],
            'Saved For Later': COLORS['in_progress']
        }
    )

    doc_avail_fig.update_layout(height=400, xaxis_title="Document Availability", yaxis_title="Count")

    # 4. FAILURE BREAKDOWN
    failed_df = filtered_df[filtered_df['STATUS'] == 'Failed']

    if len(failed_df) > 0:
        failure_reasons = failed_df['FAILURE_REASON'].value_counts()
        failure_fig = go.Figure(data=[go.Bar(
            y=failure_reasons.index,
            x=failure_reasons.values,
            orientation='h',
            marker=dict(color=COLORS['failure'])
        )])
        failure_fig.update_layout(
            title_text=f"Failure Reasons ({len(failed_df)} failures)",
            xaxis_title="Count",
            yaxis_title="Failure Reason",
            height=400
        )
    else:
        failure_fig = go.Figure()
        failure_fig.add_annotation(
            text="No failures in filtered data",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20)
        )
        failure_fig.update_layout(height=400)

    # 5. TIME SERIES
    daily_counts = filtered_df.groupby('CREATED_AT').size().reset_index(name='count')
    daily_success = filtered_df[filtered_df['STATUS'] == 'Shared'].groupby('CREATED_AT').size().reset_index(name='success_count')
    daily_merged = daily_counts.merge(daily_success, on='CREATED_AT', how='left').fillna(0)
    daily_merged['success_rate'] = (daily_merged['success_count'] / daily_merged['count'] * 100).round(1)

    time_series_fig = make_subplots(specs=[[{"secondary_y": True}]])

    time_series_fig.add_trace(
        go.Bar(x=daily_merged['CREATED_AT'], y=daily_merged['count'], name="Total Requests",
               marker_color=COLORS['primary']),
        secondary_y=False,
    )

    time_series_fig.add_trace(
        go.Scatter(x=daily_merged['CREATED_AT'], y=daily_merged['success_rate'],
                   name="Success Rate %", mode='lines+markers',
                   line=dict(color=COLORS['success'], width=3)),
        secondary_y=True,
    )

    time_series_fig.update_xaxes(title_text="Date")
    time_series_fig.update_yaxes(title_text="Request Count", secondary_y=False)
    time_series_fig.update_yaxes(title_text="Success Rate (%)", secondary_y=True)
    time_series_fig.update_layout(title_text="Request Volume & Success Rate Over Time", height=400)

    # 6. STATUS DISTRIBUTION
    stage_counts = filtered_df['STAGE'].value_counts()

    status_fig = go.Figure(data=[go.Bar(
        x=stage_counts.values,
        y=stage_counts.index,
        orientation='h',
        marker=dict(color=[
            COLORS['success'] if 'Success' in str(stage)
            else COLORS['failure'] if 'Failed' in str(stage)
            else COLORS['abandoned'] if 'Rejected' in str(stage)
            else COLORS['in_progress']
            for stage in stage_counts.index
        ])
    )])

    status_fig.update_layout(
        title_text=f"Current Status of All Requests ({total:,} total)",
        xaxis_title="Count",
        yaxis_title="Status",
        height=400
    )

    # 7. CONSENT & PIN COMPLETION
    consent_pin_data = {
        'Stage': ['Notification Read', 'Consent Given', 'PIN Entered', 'Success'],
        'Count': [notification_read, consent_given, pin_entered, successful],
        'Conversion %': [
            100,
            (consent_given/notification_read*100) if notification_read > 0 else 0,
            (pin_entered/consent_given*100) if consent_given > 0 else 0,
            (successful/pin_entered*100) if pin_entered > 0 else 0
        ]
    }

    consent_pin_fig = make_subplots(specs=[[{"secondary_y": True}]])

    consent_pin_fig.add_trace(
        go.Bar(x=consent_pin_data['Stage'], y=consent_pin_data['Count'],
               name="Absolute Count", marker_color=COLORS['primary']),
        secondary_y=False,
    )

    consent_pin_fig.add_trace(
        go.Scatter(x=consent_pin_data['Stage'], y=consent_pin_data['Conversion %'],
                   name="Stage Conversion %", mode='lines+markers+text',
                   text=[f"{v:.1f}%" for v in consent_pin_data['Conversion %']],
                   textposition='top center',
                   line=dict(color=COLORS['success'], width=3)),
        secondary_y=True,
    )

    consent_pin_fig.update_xaxes(title_text="Funnel Stage")
    consent_pin_fig.update_yaxes(title_text="Count", secondary_y=False)
    consent_pin_fig.update_yaxes(title_text="Conversion Rate (%)", secondary_y=True, range=[0, 110])
    consent_pin_fig.update_layout(title_text="User Journey Conversion Rates", height=400)

    return funnel_fig, outcome_fig, doc_avail_fig, failure_fig, time_series_fig, status_fig, consent_pin_fig

if __name__ == '__main__':
    print("\n" + "="*60)
    print("UAE PASS Digital Documents - Sharing Request Dashboard")
    print("="*60)
    print(f"\nTotal requests loaded: {len(df_expanded):,}")
    print(f"Date range: {df['CREATED_AT'].min().strftime('%Y-%m-%d')} to {df['CREATED_AT'].max().strftime('%Y-%m-%d')}")
    print(f"Service Providers: {df['ALIAS_NAME'].nunique()}")
    print(f"\nOverall Success Rate: {success_rate:.1f}%")
    print(f"  - Successful: {success_count:,}")
    print(f"  - Failed: {failure_count:,}")
    print(f"  - User Rejected: {rejected_count:,}")
    print("\nStarting dashboard server...")
    print("\nOpen http://127.0.0.1:8050/ in your web browser")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")

    app.run_server(debug=True, host='127.0.0.1', port=8050)
