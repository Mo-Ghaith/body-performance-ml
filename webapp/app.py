"""
app.py — Main Streamlit entry point for Body Performance AI
"""
import streamlit as st
import os

# Page config
st.set_page_config(
    page_title="Body Performance AI",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar branding
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 2.5rem;">🏋️</div>
        <div style="font-size: 1.3rem; font-weight: 700; 
                    background: linear-gradient(135deg, #8B5CF6, #3B82F6);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    margin-top: 0.5rem;">Body Performance AI</div>
        <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 0.3rem;">
            AI-Powered Fitness Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 0.5rem; font-size: 0.85rem; color: #94A3B8;">
        <p><strong style="color: #E2E8F0;">Navigate</strong></p>
        <p>🏋️ <strong>Predict</strong> — Individual analysis</p>
        <p>🥗 <strong>Diet Plans</strong> — Personalized nutrition</p>
        <p>💪 <strong>Exercise</strong> — Custom routines</p>
        <p>📊 <strong>Dashboard</strong> — Dataset insights</p>
        <p>📁 <strong>CSV Upload</strong> — Batch predictions</p>
        <p>🔬 <strong>Simulator</strong> — What-if scenarios</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Landing Page ───
st.markdown("""
<div style="position: relative; border-radius: 16px; overflow: hidden; margin-bottom: 3rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(to right, rgba(15, 23, 42, 0.95) 0%, rgba(15, 23, 42, 0.5) 100%); z-index: 1;"></div>
    <img src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=80" style="width: 100%; height: 400px; object-fit: cover; display: block; border-radius: 16px;">
    <div style="position: absolute; top: 50%; left: 5%; transform: translateY(-50%); z-index: 2; max-width: 650px; padding: 2rem;">
        <h1 style="color: white; font-size: 3.5rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.1;">Transform Your <span style="background: linear-gradient(135deg, #8B5CF6, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Fitness</span></h1>
        <p style="color: #E2E8F0; font-size: 1.2rem; margin-bottom: 2rem; line-height: 1.6;">Your intelligent fitness companion powered by machine learning. Get personalized performance analysis, tailored diet & exercise plans, and actionable insights — all in seconds.</p>
        <a href="Predict" target="_self" style="background: linear-gradient(135deg, #8B5CF6, #3B82F6); color: white; padding: 1rem 2.5rem; border-radius: 30px; text-decoration: none; font-weight: 600; font-size: 1.1rem; display: inline-block; box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4); transition: transform 0.2s;">🎯 Start Your Analysis</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Feature cards
st.markdown("""
<div class="feature-grid">
    <a href="Predict" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">AI Prediction</div>
            <div class="feature-desc">Enter your body metrics and get an instant performance classification powered by XGBoost & MLP neural networks.</div>
        </div>
    </a>
    <a href="Diet_Plans" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="feature-icon">🥗</div>
            <div class="feature-title">Personal Diet Plans</div>
            <div class="feature-desc">Receive custom nutrition guidance with calories, macros, and meal suggestions tailored to your fitness level.</div>
        </div>
    </a>
    <a href="Exercise_Programs" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="feature-icon">💪</div>
            <div class="feature-title">Exercise Programs</div>
            <div class="feature-desc">Get strength, flexibility, and cardio routines designed specifically for your current performance tier.</div>
        </div>
    </a>
    <a href="Dashboard" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Visual Analytics</div>
            <div class="feature-desc">Explore interactive charts showing how your metrics compare to 13,000+ athletes in our dataset.</div>
        </div>
    </a>
    <a href="CSV_Upload" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="feature-icon">📁</div>
            <div class="feature-title">CSV Batch Upload</div>
            <div class="feature-desc">Upload CSV files for batch predictions with downloadable results and per-row recommendations.</div>
        </div>
    </a>
    <a href="Simulator" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="feature-icon">🔬</div>
            <div class="feature-title">What-If Simulator</div>
            <div class="feature-desc">Adjust your metrics with interactive sliders and see how changes impact your predicted fitness class in real-time.</div>
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

# Quick stats
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h3 style="color: #F8FAFC; font-weight: 700;">Model & Dataset Overview</h3>
    <p style="color: #94A3B8; font-size: 1.1rem;">These metrics reflect our AI models trained exclusively on the Kaggle Body Performance dataset.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">13K+</div>
        <div class="metric-label">Athletes Analyzed</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">15</div>
        <div class="metric-label">Features Engineered</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">~73%</div>
        <div class="metric-label">Model Accuracy</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">4</div>
        <div class="metric-label">Fitness Classes</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 1rem;">
    <p style="color: #94A3B8; font-size: 0.85rem;">
        👈 Use the sidebar to navigate to different sections. Start with 
        <strong style="color: #8B5CF6;">Predict</strong> to analyze your body metrics!
    </p>
    <p style="color: #64748B; font-size: 0.75rem; margin-top: 1rem;">
        Built with Streamlit • Powered by XGBoost & MLP Neural Networks • Dataset: Kaggle Body Performance
    </p>
</div>
""", unsafe_allow_html=True)
