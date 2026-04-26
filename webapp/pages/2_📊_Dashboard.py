"""
Page 2: Dashboard — Dataset visualizations and EDA insights
"""
import streamlit as st
import os
import sys
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.charts import CLASS_COLORS, GENDER_COLORS, create_correlation_heatmap, create_class_distribution

st.set_page_config(page_title="Dashboard | Body Performance AI", page_icon="📊", layout="wide")

css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'style.css')
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-container" style="padding: 1.5rem;">
    <div class="hero-title" style="font-size: 2rem;">📊 Analytics Dashboard</div>
    <div class="hero-subtitle" style="font-size: 1rem;">
        Explore interactive visualizations from 13,000+ body performance records.
    </div>
</div>
""", unsafe_allow_html=True)

# Load data
cleaned_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'cleaned_data.csv')
if not os.path.exists(cleaned_path):
    st.error("⚠️ Cleaned dataset not found. Please run `python train_and_export.py` first.")
    st.stop()

@st.cache_data
def load_data():
    return pd.read_csv(cleaned_path)

df = load_data()

# Quick Stats
st.markdown("### 📈 Dataset Overview")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Total Records", f"{len(df):,}")
with c2:
    st.metric("Features", f"{df.shape[1]}")
with c3:
    st.metric("Male %", f"{(df['gender'] == 'M').mean() * 100:.1f}%")
with c4:
    st.metric("Avg Age", f"{df['age'].mean():.1f}")
with c5:
    st.metric("Classes", "4 (A-D)")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Distributions", "🔗 Correlations", "👤 Gender Analysis", "⏳ Age Analysis"])

with tab1:
    st.markdown("### Feature Distributions")
    
    # Class distribution
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_class_distribution(df), use_container_width=True)
    with col2:
        # Gender distribution
        gc = df['gender'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=['Male', 'Female'], values=gc.values, hole=0.55,
            marker=dict(colors=['#3B82F6', '#EC4899']),
            textinfo='label+percent', textfont=dict(color='white'),
        )])
        fig.update_layout(
            title=dict(text='Gender Distribution', font=dict(size=16, color='#E2E8F0')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E2E8F0'), height=350, margin=dict(t=40, b=20, l=20, r=20),
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Histograms
    num_cols = ['age', 'heightCm', 'weightKg', 'bodyFatPercent', 'gripForce', 'sitAndBendForwardCm', 'sitUpsCounts', 'broadJumpCm']
    selected_feature = st.selectbox("Select feature to explore:", num_cols, index=4)
    
    fig = px.histogram(df, x=selected_feature, color='performanceClass',
                       color_discrete_map=CLASS_COLORS, nbins=50,
                       barmode='overlay', opacity=0.6,
                       title=f'{selected_feature} Distribution by Performance Class')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'), height=400,
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Box plots
    fig = px.box(df, x='performanceClass', y=selected_feature,
                 color='performanceClass', color_discrete_map=CLASS_COLORS,
                 title=f'{selected_feature} by Performance Class',
                 category_orders={'performanceClass': ['A', 'B', 'C', 'D']})
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'), height=400, showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Correlation Analysis")
    corr_cols = ['age', 'heightCm', 'weightKg', 'bodyFatPercent', 'diastolic', 'systolic',
                 'gripForce', 'sitAndBendForwardCm', 'sitUpsCounts', 'broadJumpCm']
    st.plotly_chart(create_correlation_heatmap(df, corr_cols), use_container_width=True)
    
    # Scatter plot
    st.markdown("### Scatter Explorer")
    sc1, sc2 = st.columns(2)
    with sc1:
        x_var = st.selectbox("X-axis:", corr_cols, index=6)
    with sc2:
        y_var = st.selectbox("Y-axis:", corr_cols, index=8)
    
    fig = px.scatter(df, x=x_var, y=y_var, color='performanceClass',
                     color_discrete_map=CLASS_COLORS, opacity=0.4, size_max=6,
                     title=f'{x_var} vs {y_var}',
                     category_orders={'performanceClass': ['A', 'B', 'C', 'D']})
    fig.update_traces(marker=dict(size=4))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'), height=450,
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Gender-Based Analysis")
    
    # Grip strength by gender
    fig = px.violin(df, x='gender', y='gripForce', color='gender',
                    color_discrete_map=GENDER_COLORS, box=True,
                    title='Grip Strength Distribution by Gender')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'), height=400, showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Class distribution by gender
    ct = pd.crosstab(df['gender'], df['performanceClass'], normalize='index') * 100
    fig = go.Figure()
    for cls in ['A', 'B', 'C', 'D']:
        fig.add_trace(go.Bar(name=f'Class {cls}', x=['Male', 'Female'],
                            y=[ct.loc['M', cls], ct.loc['F', cls]],
                            marker_color=CLASS_COLORS[cls]))
    fig.update_layout(
        barmode='stack', title='Performance Class Distribution by Gender (%)',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'), height=400,
        yaxis_title='Percentage (%)',
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Body fat comparison
    fig = px.histogram(df, x='bodyFatPercent', color='gender',
                       color_discrete_map=GENDER_COLORS, nbins=50,
                       barmode='overlay', opacity=0.6, marginal='box',
                       title='Body Fat Distribution by Gender')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'), height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("### Age & Aging Effects")
    
    # Create age groups
    df_age = df.copy()
    df_age['ageGroup'] = pd.cut(df_age['age'], bins=[20, 30, 40, 50, 65],
                                 labels=['21-30', '31-40', '41-50', '51-64'])
    
    # Grip vs age
    fig = px.scatter(df, x='age', y='gripForce', color='gender',
                     color_discrete_map=GENDER_COLORS, opacity=0.3,
                     trendline='lowess', title='Grip Strength Decline with Age')
    fig.update_traces(marker=dict(size=3))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'), height=400,
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Class by age group heatmap
    ct2 = pd.crosstab(df_age['ageGroup'], df_age['performanceClass'], normalize='index') * 100
    fig = go.Figure(data=go.Heatmap(
        z=ct2[['A', 'B', 'C', 'D']].values,
        x=['A', 'B', 'C', 'D'],
        y=ct2.index.astype(str).tolist(),
        colorscale='RdYlGn', text=np.round(ct2[['A', 'B', 'C', 'D']].values, 1),
        texttemplate='%{text}%', textfont=dict(size=12),
    ))
    fig.update_layout(
        title='Performance Class (%) by Age Group',
        xaxis_title='Performance Class', yaxis_title='Age Group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'), height=350,
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # All metrics by age group
    metric_choice = st.selectbox("Select metric:", 
                                  ['gripForce', 'sitUpsCounts', 'broadJumpCm', 'sitAndBendForwardCm', 'bodyFatPercent'])
    fig = px.box(df_age.dropna(subset=['ageGroup']), x='ageGroup', y=metric_choice,
                 color='ageGroup', color_discrete_sequence=['#3B82F6', '#8B5CF6', '#F59E0B', '#EF4444'],
                 title=f'{metric_choice} by Age Group')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'), height=400, showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
