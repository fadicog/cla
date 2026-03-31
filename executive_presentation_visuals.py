"""
UAE PASS Digital Documents - Executive Presentation Visuals
2025 Performance Features Impact Analysis

Generates 7 professional charts for C-level executive presentation.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path

# UAE PASS Brand Colors
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'neutral': '#6c757d',
    'light_gray': '#f8f9fa',
    'dark_gray': '#343a40'
}

# Chart styling configuration
CHART_CONFIG = {
    'font_family': 'Segoe UI, Arial, sans-serif',
    'title_size': 24,
    'label_size': 14,
    'annotation_size': 12,
    'width': 1280,  # 16:9 aspect ratio
    'height': 720
}

def create_slide1_dashboard():
    """
    Slide 1: Executive Summary - KPI Dashboard
    3-column card layout with key metrics
    """
    fig = go.Figure()

    # Create three KPI cards using annotations and shapes
    cards_data = [
        {
            'title': 'Feature 1<br>Loader Reduction',
            'metric1': '16,650 hrs',
            'metric1_label': 'saved',
            'metric2': '$425K',
            'metric2_label': 'value',
            'x': 0.17
        },
        {
            'title': 'Feature 2<br>Mock SP App',
            'metric1': '80%',
            'metric1_label': 'fewer defects',
            'metric2': '$74K',
            'metric2_label': 'savings',
            'x': 0.5
        },
        {
            'title': 'Feature 3<br>Ghost Loader',
            'metric1': '31%',
            'metric1_label': 'anxiety reduction',
            'metric2': '$53K',
            'metric2_label': 'benefit',
            'x': 0.83
        }
    ]

    colors = [COLORS['primary'], COLORS['secondary'], COLORS['success']]

    for i, card in enumerate(cards_data):
        # Card background
        fig.add_shape(
            type="rect",
            x0=card['x']-0.13, y0=0.2, x1=card['x']+0.13, y1=0.8,
            fillcolor=colors[i],
            opacity=0.1,
            line=dict(color=colors[i], width=2)
        )

        # Title
        fig.add_annotation(
            x=card['x'], y=0.72,
            text=card['title'],
            showarrow=False,
            font=dict(size=16, color=colors[i], family=CHART_CONFIG['font_family']),
            xanchor='center'
        )

        # Metric 1
        fig.add_annotation(
            x=card['x'], y=0.55,
            text=f"<b>{card['metric1']}</b>",
            showarrow=False,
            font=dict(size=32, color=colors[i], family=CHART_CONFIG['font_family']),
            xanchor='center'
        )

        # Metric 1 Label
        fig.add_annotation(
            x=card['x'], y=0.45,
            text=card['metric1_label'],
            showarrow=False,
            font=dict(size=14, color=COLORS['neutral'], family=CHART_CONFIG['font_family']),
            xanchor='center'
        )

        # Metric 2
        fig.add_annotation(
            x=card['x'], y=0.32,
            text=f"<b>{card['metric2']}</b>",
            showarrow=False,
            font=dict(size=28, color=colors[i], family=CHART_CONFIG['font_family']),
            xanchor='center'
        )

        # Metric 2 Label
        fig.add_annotation(
            x=card['x'], y=0.24,
            text=card['metric2_label'],
            showarrow=False,
            font=dict(size=14, color=COLORS['neutral'], family=CHART_CONFIG['font_family']),
            xanchor='center'
        )

    # Main title
    fig.add_annotation(
        x=0.5, y=0.95,
        text="<b>2025 Performance & Quality Transformation</b>",
        showarrow=False,
        font=dict(size=28, color=COLORS['dark_gray'], family=CHART_CONFIG['font_family']),
        xanchor='center'
    )

    # Subtitle
    fig.add_annotation(
        x=0.5, y=0.88,
        text="Three Features | $635K Impact | 11-13× ROI",
        showarrow=False,
        font=dict(size=18, color=COLORS['neutral'], family=CHART_CONFIG['font_family']),
        xanchor='center'
    )

    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    fig.update_layout(
        width=CHART_CONFIG['width'],
        height=CHART_CONFIG['height'],
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=80, b=40),
        showlegend=False
    )

    return fig

def create_slide2_loader_reduction():
    """
    Slide 2: Loader Reduction - Before/After Comparison
    Horizontal bar chart showing loading time reduction
    """
    stages = ['Document Check', 'Consent Review', 'Post-PIN', '<b>TOTAL SESSION</b>']
    before = [2.5, 1.8, 1.2, 5.5]
    after = [0.8, 0.5, 0.3, 1.6]
    reduction_pct = [68, 72, 75, 71]

    fig = go.Figure()

    # Before bars
    fig.add_trace(go.Bar(
        y=stages,
        x=before,
        name='Before',
        orientation='h',
        marker=dict(color=COLORS['danger'], opacity=0.7),
        text=[f'{val}s' for val in before],
        textposition='inside',
        textfont=dict(size=14, color='white'),
        hovertemplate='%{y}<br>Before: %{x}s<extra></extra>'
    ))

    # After bars
    fig.add_trace(go.Bar(
        y=stages,
        x=after,
        name='After',
        orientation='h',
        marker=dict(color=COLORS['success'], opacity=0.9),
        text=[f'{val}s (-{reduction_pct[i]}%)' for i, val in enumerate(after)],
        textposition='inside',
        textfont=dict(size=14, color='white', family=CHART_CONFIG['font_family']),
        hovertemplate='%{y}<br>After: %{x}s<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': '<b>User Journey Loading Time Reduction</b>',
            'font': {'size': CHART_CONFIG['title_size'], 'family': CHART_CONFIG['font_family']},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Loading Time (seconds)',
        yaxis_title='',
        barmode='group',
        width=CHART_CONFIG['width'],
        height=CHART_CONFIG['height'],
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=CHART_CONFIG['label_size'], family=CHART_CONFIG['font_family']),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=14)
        ),
        margin=dict(l=150, r=80, t=120, b=80)
    )

    # Add annotation for key insight
    fig.add_annotation(
        x=4.5, y=3.5,
        text="<b>71% reduction in loading friction</b><br>16,650 hours saved annually",
        showarrow=True,
        arrowhead=2,
        arrowcolor=COLORS['success'],
        ax=-100,
        ay=-50,
        font=dict(size=16, color=COLORS['success'], family=CHART_CONFIG['font_family']),
        bgcolor='white',
        bordercolor=COLORS['success'],
        borderwidth=2,
        borderpad=10
    )

    fig.update_xaxes(showgrid=True, gridcolor='#e0e0e0')
    fig.update_yaxes(showgrid=False)

    return fig

def create_slide3_mock_sp():
    """
    Slide 3: Mock SP App - Shift-Left Quality
    Side-by-side comparison with flow visualization
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('<b>Before Mock Tool</b>', '<b>After Mock Tool</b>'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}]]
    )

    categories = ['Dev/QA', 'Staging', 'Production']
    before_values = [65, 20, 15]
    after_values = [85, 12, 3]

    colors_before = [COLORS['warning'], COLORS['warning'], COLORS['danger']]
    colors_after = [COLORS['success'], COLORS['success'], COLORS['success']]

    # Before chart
    fig.add_trace(go.Bar(
        x=categories,
        y=before_values,
        name='Before',
        marker=dict(color=colors_before, opacity=0.8),
        text=[f'{val}%' for val in before_values],
        textposition='outside',
        textfont=dict(size=16, family=CHART_CONFIG['font_family']),
        showlegend=False,
        hovertemplate='%{x}<br>%{y}% of defects caught<extra></extra>'
    ), row=1, col=1)

    # After chart
    fig.add_trace(go.Bar(
        x=categories,
        y=after_values,
        name='After',
        marker=dict(color=colors_after, opacity=0.8),
        text=[f'{val}%' for val in after_values],
        textposition='outside',
        textfont=dict(size=16, family=CHART_CONFIG['font_family']),
        showlegend=False,
        hovertemplate='%{x}<br>%{y}% of defects caught<extra></extra>'
    ), row=1, col=2)

    fig.update_layout(
        title={
            'text': '<b>Shift-Left Quality: Defect Detection Rate</b>',
            'font': {'size': CHART_CONFIG['title_size'], 'family': CHART_CONFIG['font_family']},
            'x': 0.5,
            'xanchor': 'center'
        },
        width=CHART_CONFIG['width'],
        height=CHART_CONFIG['height'],
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=CHART_CONFIG['label_size'], family=CHART_CONFIG['font_family']),
        margin=dict(l=80, r=80, t=150, b=120)
    )

    fig.update_yaxes(title_text='% of Defects Caught', range=[0, 100], row=1, col=1)
    fig.update_yaxes(title_text='% of Defects Caught', range=[0, 100], row=1, col=2)

    # Add key insight annotation
    fig.add_annotation(
        x=0.5, y=-0.15,
        text="<b>KEY IMPACT: 80% reduction in production escapes</b> (15% → 3%)<br>QA cycle time reduced 36% (35h → 22.5h per sprint)",
        showarrow=False,
        font=dict(size=16, color=COLORS['success'], family=CHART_CONFIG['font_family']),
        xref='paper',
        yref='paper',
        xanchor='center',
        bgcolor=COLORS['light_gray'],
        bordercolor=COLORS['success'],
        borderwidth=2,
        borderpad=10
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#e0e0e0')

    return fig

def create_slide4_ghost_loader():
    """
    Slide 4: Ghost Loader - UX Enhancement
    Before/After mockup with metric cards
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('', '', '', ''),
        specs=[
            [{'type': 'xy', 'rowspan': 1}, {'type': 'xy', 'rowspan': 1}],
            [{'type': 'indicator'}, {'type': 'indicator'}]
        ],
        row_heights=[0.5, 0.5],
        vertical_spacing=0.15,
        horizontal_spacing=0.15
    )

    # Visual mockups using shapes (simplified representation)
    # Before: blank screen with spinner
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=1, y1=1,
        fillcolor='white',
        line=dict(color=COLORS['neutral'], width=2),
        row=1, col=1
    )
    fig.add_annotation(
        x=0.5, y=0.5,
        text="⟳",
        showarrow=False,
        font=dict(size=60, color=COLORS['neutral']),
        xref='x1', yref='y1',
        row=1, col=1
    )
    fig.add_annotation(
        x=0.5, y=-0.1,
        text="<b>BEFORE: Blank Screen</b>",
        showarrow=False,
        font=dict(size=16, color=COLORS['danger'], family=CHART_CONFIG['font_family']),
        xref='x1', yref='y1'
    )

    # After: skeleton screen
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=1, y1=1,
        fillcolor='white',
        line=dict(color=COLORS['success'], width=2),
        row=1, col=2
    )
    # Skeleton bars
    skeleton_positions = [0.8, 0.65, 0.5, 0.35, 0.2]
    for pos in skeleton_positions:
        fig.add_shape(
            type="rect",
            x0=0.1, y0=pos-0.03, x1=0.9, y1=pos+0.03,
            fillcolor=COLORS['light_gray'],
            line=dict(color=COLORS['neutral'], width=1),
            row=1, col=2
        )
    fig.add_annotation(
        x=0.5, y=-0.1,
        text="<b>AFTER: Skeleton Screen</b>",
        showarrow=False,
        font=dict(size=16, color=COLORS['success'], family=CHART_CONFIG['font_family']),
        xref='x2', yref='y2'
    )

    # Metric indicators
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=25,
        delta={'reference': 0, 'relative': False, 'suffix': '%'},
        title={'text': "<b>Perceived Speed<br>Improvement</b>", 'font': {'size': 14}},
        number={'suffix': '%', 'font': {'size': 40, 'color': COLORS['success']}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=2, col=1)

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=2.4,
        delta={'reference': 3.5, 'relative': False, 'suffix': '%', 'decreasing': {'color': COLORS['success']}},
        title={'text': "<b>Bounce Rate<br>Reduction</b>", 'font': {'size': 14}},
        number={'suffix': '%', 'font': {'size': 40, 'color': COLORS['success']}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=2, col=2)

    fig.update_layout(
        title={
            'text': '<b>Ghost Loader: Zero-Infrastructure UX Enhancement</b>',
            'font': {'size': CHART_CONFIG['title_size'], 'family': CHART_CONFIG['font_family']},
            'x': 0.5,
            'xanchor': 'center'
        },
        width=CHART_CONFIG['width'],
        height=CHART_CONFIG['height'],
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family=CHART_CONFIG['font_family']),
        margin=dict(l=80, r=80, t=120, b=100),
        showlegend=False
    )

    # Add cost comparison annotation
    fig.add_annotation(
        x=0.5, y=-0.08,
        text="<b>Development Cost: $8K</b> (vs $100K+ for backend optimization)<br>31% bounce reduction with zero infrastructure investment",
        showarrow=False,
        font=dict(size=14, color=COLORS['primary'], family=CHART_CONFIG['font_family']),
        xref='paper',
        yref='paper',
        xanchor='center',
        bgcolor=COLORS['light_gray'],
        bordercolor=COLORS['primary'],
        borderwidth=2,
        borderpad=10
    )

    # Hide axes for mockup sections
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False, row=1, col=2)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False, row=1, col=2)

    return fig

def create_slide5_benchmarking():
    """
    Slide 5: Competitive Benchmarking
    Scatter plot with table overlay
    """
    platforms_data = {
        'Platform': ['UAE PASS 2024', 'UAE PASS 2025', 'SingPass', 'India Stack'],
        'Load Time (s)': [5.5, 1.6, 1.5, 4.0],
        'QA Maturity (%)': [65, 85, 80, 60],
        'UX Score': [1, 3, 4, 1],
        'Color': [COLORS['danger'], COLORS['success'], COLORS['primary'], COLORS['neutral']]
    }

    df = pd.DataFrame(platforms_data)

    fig = go.Figure()

    # Add scatter points
    for idx, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Load Time (s)']],
            y=[row['QA Maturity (%)']],
            mode='markers+text',
            name=row['Platform'],
            marker=dict(
                size=row['UX Score']*15 + 20,
                color=row['Color'],
                opacity=0.7,
                line=dict(color='white', width=2)
            ),
            text=row['Platform'],
            textposition='top center',
            textfont=dict(size=12, family=CHART_CONFIG['font_family']),
            hovertemplate=f"<b>{row['Platform']}</b><br>" +
                         f"Load Time: {row['Load Time (s)']}s<br>" +
                         f"QA Maturity: {row['QA Maturity (%)']}%<br>" +
                         f"UX Score: {row['UX Score']}/4<extra></extra>"
        ))

    # Add arrow showing progression
    fig.add_annotation(
        x=5.5, y=65,
        ax=1.6, ay=85,
        xref='x', yref='y',
        axref='x', ayref='y',
        showarrow=True,
        arrowhead=3,
        arrowsize=1.5,
        arrowwidth=3,
        arrowcolor=COLORS['success']
    )
    fig.add_annotation(
        x=3.5, y=75,
        text="<b>2025<br>Transformation</b>",
        showarrow=False,
        font=dict(size=14, color=COLORS['success'], family=CHART_CONFIG['font_family'])
    )

    fig.update_layout(
        title={
            'text': '<b>Global Platform Benchmarking: UAE PASS Position</b>',
            'font': {'size': CHART_CONFIG['title_size'], 'family': CHART_CONFIG['font_family']},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='<b>Load Time (seconds) - Lower is Better</b>',
        yaxis_title='<b>QA Maturity (%) - Higher is Better</b>',
        width=CHART_CONFIG['width'],
        height=CHART_CONFIG['height'],
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=CHART_CONFIG['label_size'], family=CHART_CONFIG['font_family']),
        showlegend=False,
        margin=dict(l=100, r=100, t=150, b=120)
    )

    # Invert x-axis (lower load time is better)
    fig.update_xaxes(autorange='reversed', showgrid=True, gridcolor='#e0e0e0')
    fig.update_yaxes(showgrid=True, gridcolor='#e0e0e0', range=[50, 90])

    # Add quadrant labels
    fig.add_annotation(
        x=0.5, y=87,
        text="<b>🎯 WORLD-CLASS</b>",
        showarrow=False,
        font=dict(size=16, color=COLORS['success'], family=CHART_CONFIG['font_family']),
        bgcolor=COLORS['light_gray'],
        opacity=0.7
    )

    # Add summary note
    fig.add_annotation(
        x=0.5, y=-0.15,
        text="<b>Bubble size</b> = UX sophistication score | <b>UAE PASS 2025</b> now competitive with world-class platforms",
        showarrow=False,
        font=dict(size=14, color=COLORS['neutral'], family=CHART_CONFIG['font_family']),
        xref='paper',
        yref='paper',
        xanchor='center'
    )

    return fig

def create_slide6_roi():
    """
    Slide 6: ROI Waterfall Chart
    Investment → benefits → net ROI visualization
    """
    categories = ['Investment', 'Loader<br>Benefit', 'Mock SP<br>Benefit',
                  'Ghost<br>Benefit', 'Synergy<br>Bonus', 'Net ROI']
    values = [-50, 425, 74, 53, 83, 585]

    # Calculate cumulative for waterfall
    cumulative = [0]
    for i in range(len(values)-1):
        cumulative.append(sum(values[:i+1]))

    colors = [COLORS['danger'], COLORS['success'], COLORS['success'],
              COLORS['success'], COLORS['primary'], COLORS['secondary']]

    fig = go.Figure()

    # Waterfall chart
    fig.add_trace(go.Waterfall(
        name='ROI Components',
        orientation='v',
        measure=['relative', 'relative', 'relative', 'relative', 'relative', 'total'],
        x=categories,
        y=values,
        text=[f'${abs(v)}K' for v in values],
        textposition='outside',
        textfont=dict(size=16, family=CHART_CONFIG['font_family']),
        connector={'line': {'color': COLORS['neutral'], 'width': 2, 'dash': 'dot'}},
        increasing={'marker': {'color': COLORS['success']}},
        decreasing={'marker': {'color': COLORS['danger']}},
        totals={'marker': {'color': COLORS['secondary']}},
        hovertemplate='%{x}<br>Value: $%{y}K<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': '<b>ROI Waterfall: Investment to Returns</b>',
            'font': {'size': CHART_CONFIG['title_size'], 'family': CHART_CONFIG['font_family']},
            'x': 0.5,
            'xanchor': 'center'
        },
        yaxis_title='Value ($K)',
        width=CHART_CONFIG['width'],
        height=CHART_CONFIG['height'],
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=CHART_CONFIG['label_size'], family=CHART_CONFIG['font_family']),
        showlegend=False,
        margin=dict(l=100, r=100, t=150, b=120)
    )

    # Add ROI calculation annotation
    fig.add_annotation(
        x=5, y=650,
        text="<b>11.7× ROI</b><br>Payback < 2 months",
        showarrow=True,
        arrowhead=2,
        ax=-80,
        ay=-60,
        font=dict(size=20, color=COLORS['secondary'], family=CHART_CONFIG['font_family']),
        bgcolor='white',
        bordercolor=COLORS['secondary'],
        borderwidth=3,
        borderpad=10
    )

    # Add breakdown note
    fig.add_annotation(
        x=0.5, y=-0.15,
        text="<b>Total Investment: $50K</b> | <b>Total Benefit: $635K</b> (direct benefits + synergies) | <b>Net Gain: $585K in Year 1</b>",
        showarrow=False,
        font=dict(size=14, color=COLORS['neutral'], family=CHART_CONFIG['font_family']),
        xref='paper',
        yref='paper',
        xanchor='center',
        bgcolor=COLORS['light_gray'],
        bordercolor=COLORS['primary'],
        borderwidth=2,
        borderpad=10
    )

    fig.update_yaxes(showgrid=True, gridcolor='#e0e0e0')
    fig.update_xaxes(showgrid=False)

    return fig

def create_slide7_roadmap():
    """
    Slide 7: Roadmap Timeline
    Horizontal timeline with quarterly phases
    """
    quarters = ['Q1 2026', 'Q2 2026', 'Q3 2026', 'Q4 2026']
    phases = [
        {
            'name': 'Validate',
            'items': ['User surveys', 'Metrics baseline', 'Refinement']
        },
        {
            'name': 'Expand',
            'items': ['Auth module', 'eSign flows', 'SP scenarios']
        },
        {
            'name': 'Monitor',
            'items': ['Quarterly UX review', 'NPS tracking', 'A/B testing']
        },
        {
            'name': 'Sustain',
            'items': ['Maintain SP app', 'Iterate features', 'Document learnings']
        }
    ]

    fig = go.Figure()

    # Create timeline bars
    for i, (quarter, phase) in enumerate(zip(quarters, phases)):
        # Phase bar
        fig.add_trace(go.Bar(
            x=[1],
            y=[quarter],
            orientation='h',
            name=phase['name'],
            marker=dict(
                color=[COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['warning']][i],
                opacity=0.7
            ),
            text=f"<b>{phase['name']}</b>",
            textposition='inside',
            textfont=dict(size=18, color='white', family=CHART_CONFIG['font_family']),
            hoverinfo='skip',
            showlegend=False
        ))

        # Add phase items as annotations
        items_text = '<br>'.join([f"• {item}" for item in phase['items']])
        fig.add_annotation(
            x=1.05, y=i,
            text=items_text,
            showarrow=False,
            font=dict(size=11, color=COLORS['dark_gray'], family=CHART_CONFIG['font_family']),
            xanchor='left',
            align='left'
        )

    fig.update_layout(
        title={
            'text': '<b>2026 Roadmap: Sustaining Momentum</b>',
            'font': {'size': CHART_CONFIG['title_size'], 'family': CHART_CONFIG['font_family']},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='',
        yaxis_title='',
        width=CHART_CONFIG['width'],
        height=CHART_CONFIG['height'],
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=CHART_CONFIG['label_size'], family=CHART_CONFIG['font_family']),
        barmode='overlay',
        showlegend=False,
        margin=dict(l=120, r=400, t=120, b=80)
    )

    # Add key message
    fig.add_annotation(
        x=0.5, y=-0.12,
        text="<b>Continue prioritizing performance</b> — Expand successful patterns to all user flows",
        showarrow=False,
        font=dict(size=16, color=COLORS['primary'], family=CHART_CONFIG['font_family']),
        xref='paper',
        yref='paper',
        xanchor='center',
        bgcolor=COLORS['light_gray'],
        bordercolor=COLORS['primary'],
        borderwidth=2,
        borderpad=10
    )

    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False)

    return fig

def generate_all_charts():
    """
    Generate all 7 charts and save as HTML files
    """
    output_dir = Path('D:/cluade/presentation_charts')
    output_dir.mkdir(exist_ok=True)

    charts = {
        'slide1_executive_summary': create_slide1_dashboard(),
        'slide2_loader_reduction': create_slide2_loader_reduction(),
        'slide3_mock_sp_quality': create_slide3_mock_sp(),
        'slide4_ghost_loader': create_slide4_ghost_loader(),
        'slide5_benchmarking': create_slide5_benchmarking(),
        'slide6_roi_waterfall': create_slide6_roi(),
        'slide7_roadmap': create_slide7_roadmap()
    }

    # Save individual HTML files
    for name, fig in charts.items():
        fig.write_html(output_dir / f'{name}.html')
        print(f"[OK] Generated: {name}.html")

    # Create combined HTML report
    create_html_report(charts, output_dir)

    print(f"\n[OK] All charts generated in: {output_dir}")
    print(f"[OK] Open 'executive_presentation_visuals.html' to view all slides")

def create_html_report(charts, output_dir):
    """
    Create a single HTML file with all charts embedded
    """
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>UAE PASS - Executive Presentation Visuals</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 32px;
        }
        .header p {
            margin: 0;
            font-size: 18px;
            opacity: 0.9;
        }
        .slide {
            background: white;
            margin-bottom: 30px;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .slide h2 {
            color: #667eea;
            margin-top: 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        .chart-container {
            margin-top: 20px;
        }
        .footer {
            text-align: center;
            padding: 20px;
            color: #6c757d;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>UAE PASS Digital Documents</h1>
        <p>2025 Performance Features - Executive Presentation Visuals</p>
        <p style="margin-top: 10px; font-size: 14px;">Generated for TDRA C-Level Leadership</p>
    </div>
"""

    slide_titles = [
        'Slide 1: Executive Summary Dashboard',
        'Slide 2: Loader Reduction Impact',
        'Slide 3: Mock Service Provider App - Quality Shift',
        'Slide 4: Ghost Loader - UX Enhancement',
        'Slide 5: Global Platform Benchmarking',
        'Slide 6: ROI Waterfall Analysis',
        'Slide 7: 2026 Roadmap'
    ]

    for (name, fig), title in zip(charts.items(), slide_titles):
        html_content += f"""
    <div class="slide">
        <h2>{title}</h2>
        <div class="chart-container">
            {fig.to_html(include_plotlyjs='cdn', full_html=False, div_id=name)}
        </div>
    </div>
"""

    html_content += """
    <div class="footer">
        <p><strong>UAE PASS Digital Documents - Product Management</strong></p>
        <p>Visualizations generated using Plotly | For internal executive presentation use</p>
    </div>
</body>
</html>
"""

    with open(output_dir / 'executive_presentation_visuals.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    print("UAE PASS Executive Presentation Visuals Generator")
    print("=" * 60)
    generate_all_charts()
    print("\n" + "=" * 60)
    print("USAGE INSTRUCTIONS:")
    print("1. Open 'executive_presentation_visuals.html' in your browser")
    print("2. Each chart can be exported as PNG by clicking the camera icon")
    print("3. Right-click charts to copy/save for PowerPoint insertion")
    print("4. Individual slide HTML files available in 'presentation_charts' folder")
