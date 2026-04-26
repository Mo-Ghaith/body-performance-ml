"""
utils/charts.py — Plotly chart helpers for the Streamlit dashboard.
"""
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd


# Color scheme
CLASS_COLORS = {'A': '#10B981', 'B': '#3B82F6', 'C': '#F59E0B', 'D': '#EF4444'}
GENDER_COLORS = {'M': '#3B82F6', 'F': '#EC4899'}


def create_radar_chart(user_values, class_means, class_label):
    """Create a radar chart comparing user metrics to class averages."""
    categories = ['Grip Force', 'Flexibility', 'Sit-ups', 'Broad Jump', 'Body Fat %']
    raw_keys = ['gripForce', 'sitAndBendForwardCm', 'sitUpsCounts', 'broadJumpCm', 'bodyFatPercent']

    user_vals = [user_values.get(k, 0) for k in raw_keys]
    # Normalize for radar
    all_class_vals = {}
    for cls in ['A', 'B', 'C', 'D']:
        if cls in class_means.get('gripForce', {}):
            all_class_vals[cls] = [class_means[k].get(cls, 0) for k in raw_keys]

    # Find max across all classes and user for each category for normalization
    all_vals = [user_vals] + list(all_class_vals.values())
    max_vals = [max(abs(v[i]) for v in all_vals) if max(abs(v[i]) for v in all_vals) > 0 else 1 for i in range(len(raw_keys))]

    user_norm = [v / m * 100 for v, m in zip(user_vals, max_vals)]
    # For body fat, invert (lower is better)
    user_norm[4] = 100 - user_norm[4]

    fig = go.Figure()

    # Add class average
    if class_label in all_class_vals:
        cls_norm = [v / m * 100 for v, m in zip(all_class_vals[class_label], max_vals)]
        cls_norm[4] = 100 - cls_norm[4]
        fig.add_trace(go.Scatterpolar(
            r=cls_norm + [cls_norm[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=f'Class {class_label} Avg',
            line=dict(color=CLASS_COLORS.get(class_label, '#888'), width=2),
            opacity=0.3,
        ))

    # Add user
    fig.add_trace(go.Scatterpolar(
        r=user_norm + [user_norm[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Your Profile',
        line=dict(color='#8B5CF6', width=3),
        opacity=0.6,
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 110], showticklabels=False),
            bgcolor='rgba(0,0,0,0)',
        ),
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        margin=dict(t=30, b=30, l=60, r=60),
        height=400,
    )
    return fig


def create_gauge_chart(value, min_val, max_val, title, unit='', thresholds=None):
    """Create a gauge chart for a single metric."""
    if thresholds is None:
        r = max_val - min_val
        thresholds = [
            (min_val + r * 0.25, '#EF4444'),
            (min_val + r * 0.5, '#F59E0B'),
            (min_val + r * 0.75, '#3B82F6'),
            (max_val, '#10B981'),
        ]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 14, 'color': '#E2E8F0'}},
        number={'suffix': f' {unit}', 'font': {'color': '#E2E8F0'}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickcolor': '#94A3B8'},
            'bar': {'color': '#8B5CF6'},
            'bgcolor': 'rgba(30,41,59,0.5)',
            'borderwidth': 0,
            'steps': [
                {'range': [min_val, thresholds[0][0]], 'color': 'rgba(239,68,68,0.2)'},
                {'range': [thresholds[0][0], thresholds[1][0]], 'color': 'rgba(245,158,11,0.2)'},
                {'range': [thresholds[1][0], thresholds[2][0]], 'color': 'rgba(59,130,246,0.2)'},
                {'range': [thresholds[2][0], max_val], 'color': 'rgba(16,185,129,0.2)'},
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        height=220,
        margin=dict(t=40, b=10, l=20, r=20),
    )
    return fig


def create_probability_bar(proba_dict):
    """Create a horizontal bar chart showing class probabilities."""
    classes = ['A', 'B', 'C', 'D']
    probs = [proba_dict.get(c, 0) * 100 for c in classes]
    colors = [CLASS_COLORS[c] for c in classes]

    fig = go.Figure(go.Bar(
        x=probs,
        y=[f'Class {c}' for c in classes],
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        text=[f'{p:.1f}%' for p in probs],
        textposition='outside',
        textfont=dict(color='#E2E8F0'),
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 105], title='Confidence (%)', color='#94A3B8'),
        yaxis=dict(color='#E2E8F0'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        height=200,
        margin=dict(t=10, b=30, l=80, r=40),
    )
    return fig


def create_distribution_chart(data_col, user_value, title, color='#8B5CF6'):
    """Create a distribution chart with user's position highlighted."""
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data_col,
        nbinsx=40,
        marker=dict(color=color, opacity=0.6, line=dict(width=0)),
        name='Population',
    ))
    fig.add_vline(
        x=user_value, line=dict(color='#F59E0B', width=3, dash='dash'),
        annotation_text=f'You: {user_value:.1f}',
        annotation_font=dict(color='#F59E0B', size=12),
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color='#E2E8F0')),
        xaxis=dict(color='#94A3B8'),
        yaxis=dict(title='Count', color='#94A3B8'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        height=280,
        margin=dict(t=40, b=30, l=50, r=20),
        showlegend=False,
    )
    return fig


def create_correlation_heatmap(df, columns):
    """Create an interactive correlation heatmap."""
    corr = df[columns].corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=columns,
        y=columns,
        colorscale='RdBu_r',
        zmid=0,
        text=np.round(corr.values, 2),
        texttemplate='%{text}',
        textfont=dict(size=9),
    ))
    fig.update_layout(
        title=dict(text='Feature Correlation Matrix', font=dict(size=16, color='#E2E8F0')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        height=500,
        margin=dict(t=40, b=80, l=80, r=20),
    )
    return fig


def create_class_distribution(df, class_col='performanceClass'):
    """Create a donut chart for class distribution."""
    counts = df[class_col].value_counts().sort_index()
    fig = go.Figure(data=[go.Pie(
        labels=[f'Class {c}' for c in counts.index],
        values=counts.values,
        hole=0.55,
        marker=dict(colors=[CLASS_COLORS.get(c, '#888') for c in counts.index]),
        textinfo='label+percent',
        textfont=dict(color='white'),
    )])
    fig.update_layout(
        title=dict(text='Performance Class Distribution', font=dict(size=16, color='#E2E8F0')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        height=350,
        margin=dict(t=40, b=20, l=20, r=20),
        showlegend=True,
    )
    return fig
