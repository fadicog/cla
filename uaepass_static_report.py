"""
UAE PASS Digital Documents - Static HTML Report Generator

This script generates a standalone HTML report with all visualizations
that can be viewed in any web browser without running a server.

Requirements:
- pip install plotly pandas

Run: python uaepass_static_report.py
Output: uaepass_dashboard_report.html
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime

# Load and prepare data
print("Loading data from D:\\cluade\\csvdata-2.csv...")
df = pd.read_csv('D:\\cluade\\csvdata-2.csv')

# Clean column names (remove BOM and spaces)
df.columns = df.columns.str.replace('\ufeff', '').str.strip()

# Convert date column
df['CREATED_AT'] = pd.to_datetime(df['CREATED_AT'], format='%d-%b-%y')

# Expand rows based on COUNT column
print("Processing data...")
df_expanded = df.loc[df.index.repeat(df['COUNT'])].reset_index(drop=True)

# Define color scheme
COLORS = {
    'success': '#28a745',
    'failure': '#dc3545',
    'in_progress': '#ffc107',
    'abandoned': '#6c757d',
    'primary': '#007bff',
}

# Calculate key metrics
total_requests = len(df_expanded)
success_count = len(df_expanded[df_expanded['STATUS'] == 'Shared'])
failure_count = len(df_expanded[df_expanded['STATUS'] == 'Failed'])
rejected_count = len(df_expanded[df_expanded['STATUS'] == 'User Rejected'])
success_rate = (success_count / total_requests * 100) if total_requests > 0 else 0

print(f"\nData Summary:")
print(f"  Total requests: {total_requests:,}")
print(f"  Success rate: {success_rate:.1f}%")
print(f"  Date range: {df['CREATED_AT'].min()} to {df['CREATED_AT'].max()}")

# Create all visualizations
print("\nGenerating visualizations...")

# 1. FUNNEL CHART
print("  - Funnel chart...")
total = len(df_expanded)
docs_available = len(df_expanded[df_expanded['MANDATORY_DOCS_AVAILABLE'] == 'Yes'])
notification_read = len(df_expanded[df_expanded['NOTIFICATION_STATE'] == 'Read'])
consent_given = len(df_expanded[df_expanded['CONSENT_GIVEN'] == 'Yes'])
pin_entered = len(df_expanded[df_expanded['PIN_GIVEN'] == 'Yes'])
successful = len(df_expanded[df_expanded['STATUS'] == 'Shared'])

funnel_data = {
    'stage': ['1. Request Created', '2. Docs Available', '3. Notification Read',
              '4. Consent Given', '5. PIN Entered', '6. Successfully Shared'],
    'count': [total, docs_available, notification_read, consent_given, pin_entered, successful],
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
    title={
        'text': f"<b>Sharing Request Funnel</b><br><sub>Total: {total:,} requests | Success Rate: {(successful/total*100):.1f}%</sub>",
        'x': 0.5,
        'xanchor': 'center'
    },
    height=700,
    width=1200,
    font=dict(size=14),
    margin=dict(l=50, r=200, t=100, b=50)
)

# Add conversion rates as annotations
conversion_rates = []
for i in range(1, len(funnel_data['count'])):
    prev_count = funnel_data['count'][i-1]
    curr_count = funnel_data['count'][i]
    if prev_count > 0:
        drop_rate = ((prev_count - curr_count) / prev_count * 100)
        conversion_rates.append(f"Drop-off: {drop_rate:.1f}% ({prev_count - curr_count:,} users)")

# 2. OUTCOME PIE CHART
print("  - Outcome distribution...")
outcome_counts = df_expanded['STATUS'].value_counts()

outcome_fig = go.Figure(data=[go.Pie(
    labels=outcome_counts.index,
    values=outcome_counts.values,
    hole=0.4,
    textinfo='label+percent+value',
    marker=dict(colors=[
        COLORS['success'] if 'Shared' in str(label)
        else COLORS['failure'] if 'Failed' in str(label)
        else COLORS['abandoned'] if 'Rejected' in str(label)
        else COLORS['in_progress']
        for label in outcome_counts.index
    ])
)])

outcome_fig.update_layout(
    title={
        'text': f"<b>Final Outcome Distribution</b><br><sub>{total:,} total requests</sub>",
        'x': 0.5,
        'xanchor': 'center'
    },
    height=600,
    width=1200,
    font=dict(size=14),
    margin=dict(l=50, r=50, t=100, b=50)
)

# 3. DOCUMENT AVAILABILITY IMPACT
print("  - Document availability analysis...")
docs_avail_grouped = df_expanded.groupby(['DOC_AVAILIBILITY', 'STATUS']).size().reset_index(name='count')

doc_avail_fig = px.bar(
    docs_avail_grouped,
    x='DOC_AVAILIBILITY',
    y='count',
    color='STATUS',
    barmode='group',
    text='count',
    color_discrete_map={
        'Shared': COLORS['success'],
        'Failed': COLORS['failure'],
        'User Rejected': COLORS['abandoned'],
        'No Action Taken': COLORS['in_progress'],
        'Saved For Later': COLORS['in_progress']
    }
)

doc_avail_fig.update_traces(texttemplate='%{text:,}', textposition='outside')
doc_avail_fig.update_layout(
    title={
        'text': "<b>Impact of Document Availability on Success</b>",
        'x': 0.5,
        'xanchor': 'center'
    },
    height=600,
    width=1200,
    xaxis_title="Document Availability Status",
    yaxis_title="Number of Requests",
    font=dict(size=14),
    margin=dict(l=50, r=50, t=100, b=100)
)

# Calculate success rates by doc availability
for doc_status in df_expanded['DOC_AVAILIBILITY'].unique():
    subset = df_expanded[df_expanded['DOC_AVAILIBILITY'] == doc_status]
    success_subset = len(subset[subset['STATUS'] == 'Shared'])
    success_rate_subset = (success_subset / len(subset) * 100) if len(subset) > 0 else 0
    print(f"    {doc_status}: {success_rate_subset:.1f}% success rate ({success_subset}/{len(subset)})")

# 4. FAILURE BREAKDOWN
print("  - Failure analysis...")
failed_df = df_expanded[df_expanded['STATUS'] == 'Failed']
rejected_df = df_expanded[df_expanded['STATUS'] == 'User Rejected']

# Combine failures and rejections
failure_categories = []

if len(failed_df) > 0:
    failure_reasons = failed_df['FAILURE_REASON'].value_counts()
    for reason, count in failure_reasons.items():
        failure_categories.append({'Category': f'System Failure: {reason}', 'Count': count, 'Type': 'System'})

if len(rejected_df) > 0:
    failure_categories.append({'Category': 'User Rejected', 'Count': len(rejected_df), 'Type': 'User'})

failure_df_plot = pd.DataFrame(failure_categories)

if len(failure_df_plot) > 0:
    failure_fig = go.Figure(data=[go.Bar(
        y=failure_df_plot['Category'],
        x=failure_df_plot['Count'],
        orientation='h',
        text=failure_df_plot['Count'],
        texttemplate='%{text:,}',
        textposition='auto',
        marker=dict(color=[
            COLORS['failure'] if row['Type'] == 'System' else COLORS['abandoned']
            for _, row in failure_df_plot.iterrows()
        ])
    )])
    failure_fig.update_layout(
        title={
            'text': f"<b>Failure & Rejection Breakdown</b><br><sub>{len(failed_df) + len(rejected_df):,} unsuccessful requests</sub>",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Count",
        yaxis_title="",
        height=max(500, len(failure_df_plot) * 50),
        width=1200,
        font=dict(size=14),
        margin=dict(l=350, r=50, t=100, b=50)
    )
else:
    failure_fig = go.Figure()
    failure_fig.add_annotation(
        text="No failures in data",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=20)
    )
    failure_fig.update_layout(height=400)

# 5. TIME SERIES
print("  - Time series analysis...")
daily_counts = df_expanded.groupby('CREATED_AT').size().reset_index(name='count')
daily_success = df_expanded[df_expanded['STATUS'] == 'Shared'].groupby('CREATED_AT').size().reset_index(name='success_count')
daily_merged = daily_counts.merge(daily_success, on='CREATED_AT', how='left').fillna(0)
daily_merged['success_rate'] = (daily_merged['success_count'] / daily_merged['count'] * 100).round(1)

time_series_fig = make_subplots(specs=[[{"secondary_y": True}]])

time_series_fig.add_trace(
    go.Bar(x=daily_merged['CREATED_AT'], y=daily_merged['count'], name="Total Requests",
           marker_color=COLORS['primary'], text=daily_merged['count'],
           texttemplate='%{text}', textposition='outside'),
    secondary_y=False,
)

time_series_fig.add_trace(
    go.Scatter(x=daily_merged['CREATED_AT'], y=daily_merged['success_rate'],
               name="Success Rate %", mode='lines+markers+text',
               text=[f"{v:.0f}%" for v in daily_merged['success_rate']],
               textposition='top center',
               line=dict(color=COLORS['success'], width=3),
               marker=dict(size=10)),
    secondary_y=True,
)

time_series_fig.update_xaxes(title_text="Date")
time_series_fig.update_yaxes(title_text="Request Count", secondary_y=False)
time_series_fig.update_yaxes(title_text="Success Rate (%)", secondary_y=True, range=[0, 110])
time_series_fig.update_layout(
    title={
        'text': "<b>Daily Request Volume & Success Rate Trend</b>",
        'x': 0.5,
        'xanchor': 'center'
    },
    height=600,
    width=1200,
    font=dict(size=14),
    margin=dict(l=50, r=50, t=100, b=100)
)

# 6. CONSENT & PIN COMPLETION FUNNEL
print("  - Consent and PIN analysis...")
consent_pin_data = {
    'Stage': ['Notification\nRead', 'Consent\nGiven', 'PIN\nEntered', 'Successfully\nShared'],
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
           name="Absolute Count", marker_color=COLORS['primary'],
           text=consent_pin_data['Count'],
           texttemplate='%{text:,}', textposition='outside'),
    secondary_y=False,
)

consent_pin_fig.add_trace(
    go.Scatter(x=consent_pin_data['Stage'], y=consent_pin_data['Conversion %'],
               name="Stage Conversion %", mode='lines+markers+text',
               text=[f"{v:.1f}%" for v in consent_pin_data['Conversion %']],
               textposition='top center',
               line=dict(color=COLORS['success'], width=4),
               marker=dict(size=12)),
    secondary_y=True,
)

consent_pin_fig.update_xaxes(title_text="Funnel Stage")
consent_pin_fig.update_yaxes(title_text="Count", secondary_y=False)
consent_pin_fig.update_yaxes(title_text="Stage-to-Stage Conversion Rate (%)", secondary_y=True, range=[0, 120])
consent_pin_fig.update_layout(
    title={
        'text': "<b>User Journey Conversion Rates</b>",
        'x': 0.5,
        'xanchor': 'center'
    },
    height=600,
    width=1200,
    font=dict(size=14),
    margin=dict(l=80, r=80, t=100, b=100)
)

# 7. SERVICE PROVIDER PERFORMANCE
print("  - Service provider analysis...")
sp_performance = df_expanded.groupby('ALIAS_NAME').agg({
    'STATUS': 'count',
}).rename(columns={'STATUS': 'Total'}).reset_index()

sp_success = df_expanded[df_expanded['STATUS'] == 'Shared'].groupby('ALIAS_NAME').size().reset_index(name='Success')
sp_performance = sp_performance.merge(sp_success, on='ALIAS_NAME', how='left').fillna(0)
sp_performance['Success Rate'] = (sp_performance['Success'] / sp_performance['Total'] * 100).round(1)
sp_performance = sp_performance.sort_values('Total', ascending=True)

sp_fig = go.Figure()

sp_fig.add_trace(go.Bar(
    y=sp_performance['ALIAS_NAME'],
    x=sp_performance['Total'],
    name='Total Requests',
    orientation='h',
    marker_color=COLORS['primary'],
    text=sp_performance['Total'],
    texttemplate='%{text:,}',
    textposition='auto'
))

sp_fig.add_trace(go.Bar(
    y=sp_performance['ALIAS_NAME'],
    x=sp_performance['Success'],
    name='Successful',
    orientation='h',
    marker_color=COLORS['success'],
    text=[f"{sr:.1f}%" for sr in sp_performance['Success Rate']],
    textposition='auto'
))

sp_fig.update_layout(
    title={
        'text': "<b>Performance by Service Provider</b>",
        'x': 0.5,
        'xanchor': 'center'
    },
    barmode='overlay',
    xaxis_title="Number of Requests",
    yaxis_title="Service Provider",
    height=max(600, len(sp_performance) * 40),
    width=1200,
    font=dict(size=14),
    margin=dict(l=250, r=50, t=100, b=50)
)

# 8. PLATFORM COMPARISON
print("  - Platform analysis...")
platform_data = df_expanded.groupby(['USER_AGENT', 'STATUS']).size().reset_index(name='count')

platform_fig = px.bar(
    platform_data,
    x='USER_AGENT',
    y='count',
    color='STATUS',
    barmode='group',
    text='count',
    color_discrete_map={
        'Shared': COLORS['success'],
        'Failed': COLORS['failure'],
        'User Rejected': COLORS['abandoned'],
        'No Action Taken': COLORS['in_progress'],
        'Saved For Later': COLORS['in_progress']
    }
)

platform_fig.update_traces(texttemplate='%{text:,}', textposition='outside')
platform_fig.update_layout(
    title={
        'text': "<b>Performance by Platform</b>",
        'x': 0.5,
        'xanchor': 'center'
    },
    height=600,
    width=1200,
    xaxis_title="Platform",
    yaxis_title="Number of Requests",
    font=dict(size=14),
    margin=dict(l=50, r=50, t=100, b=100)
)

# Create HTML report
print("\nGenerating HTML report...")

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>UAE PASS DV - Sharing Request Analytics</title>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .header {{
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 700;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .kpi-card {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .kpi-card h3 {{
            margin: 0;
            color: #6c757d;
            font-size: 1em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .kpi-card .kpi-value {{
            margin: 15px 0 0 0;
            font-size: 2.5em;
            font-weight: 700;
        }}
        .kpi-card.success .kpi-value {{ color: #28a745; }}
        .kpi-card.primary .kpi-value {{ color: #007bff; }}
        .kpi-card.danger .kpi-value {{ color: #dc3545; }}
        .kpi-card.warning .kpi-value {{ color: #ffc107; }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .insights {{
            background: #e7f3ff;
            border-left: 4px solid #007bff;
            padding: 20px;
            border-radius: 5px;
            margin: 30px 0;
        }}
        .insights h2 {{
            margin-top: 0;
            color: #007bff;
        }}
        .insights ul {{
            line-height: 1.8;
        }}
        .footer {{
            text-align: center;
            color: #6c757d;
            margin-top: 50px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>UAE PASS Digital Documents</h1>
        <p>Sharing Request Analytics Report</p>
        <p style="font-size: 0.9em; margin-top: 15px;">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="kpi-container">
        <div class="kpi-card primary">
            <h3>Total Requests</h3>
            <div class="kpi-value">{total_requests:,}</div>
        </div>
        <div class="kpi-card success">
            <h3>Success Rate</h3>
            <div class="kpi-value">{success_rate:.1f}%</div>
        </div>
        <div class="kpi-card success">
            <h3>Successful Shares</h3>
            <div class="kpi-value">{success_count:,}</div>
        </div>
        <div class="kpi-card danger">
            <h3>Failed/Rejected</h3>
            <div class="kpi-value">{failure_count + rejected_count:,}</div>
        </div>
    </div>

    <div class="insights">
        <h2>Key Insights</h2>
        <ul>
            <li><strong>Overall Success Rate:</strong> {success_rate:.1f}% of all sharing requests result in successful document sharing</li>
            <li><strong>Document Availability Impact:</strong> Requests with all required documents available have significantly higher success rates</li>
            <li><strong>Funnel Drop-off:</strong> Major drop-offs occur at:
                <ul>
                    <li>Document availability check ({(total - docs_available)/total*100:.1f}% lost)</li>
                    <li>Consent stage ({(notification_read - consent_given)/notification_read*100 if notification_read > 0 else 0:.1f}% of readers don't consent)</li>
                    <li>PIN entry ({(consent_given - pin_entered)/consent_given*100 if consent_given > 0 else 0:.1f}% don't complete PIN)</li>
                </ul>
            </li>
            <li><strong>Date Range:</strong> {df['CREATED_AT'].min().strftime('%Y-%m-%d')} to {df['CREATED_AT'].max().strftime('%Y-%m-%d')}</li>
            <li><strong>Service Providers:</strong> {df['ALIAS_NAME'].nunique()} different SPs in dataset</li>
        </ul>
    </div>

    <div class="chart-container">
        {funnel_fig.to_html(include_plotlyjs='cdn', div_id='funnel')}
    </div>

    <div class="chart-container">
        {consent_pin_fig.to_html(include_plotlyjs=False, div_id='consent_pin')}
    </div>

    <div class="chart-container">
        {outcome_fig.to_html(include_plotlyjs=False, div_id='outcome')}
    </div>

    <div class="chart-container">
        {doc_avail_fig.to_html(include_plotlyjs=False, div_id='doc_avail')}
    </div>

    <div class="chart-container">
        {failure_fig.to_html(include_plotlyjs=False, div_id='failure')}
    </div>

    <div class="chart-container">
        {time_series_fig.to_html(include_plotlyjs=False, div_id='timeseries')}
    </div>

    <div class="chart-container">
        {sp_fig.to_html(include_plotlyjs=False, div_id='sp')}
    </div>

    <div class="chart-container">
        {platform_fig.to_html(include_plotlyjs=False, div_id='platform')}
    </div>

    <div class="footer">
        <p>UAE PASS Digital Documents - Document Sharing Analytics</p>
        <p>This report analyzes {total_requests:,} sharing requests across {df['ALIAS_NAME'].nunique()} service providers</p>
    </div>
</body>
</html>
"""

output_file = 'D:\\cluade\\uaepass_dashboard_report.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n{'='*60}")
print("SUCCESS! Report generated successfully")
print(f"{'='*60}")
print(f"\nOutput file: {output_file}")
print(f"\nOpen this file in your web browser to view the dashboard.")
print(f"\nReport Summary:")
print(f"  - {total_requests:,} total requests analyzed")
print(f"  - {success_rate:.1f}% overall success rate")
print(f"  - {df['ALIAS_NAME'].nunique()} service providers")
print(f"  - Date range: {df['CREATED_AT'].min().strftime('%Y-%m-%d')} to {df['CREATED_AT'].max().strftime('%Y-%m-%d')}")
print(f"\n{'='*60}\n")
