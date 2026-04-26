"""
Page 4: What-If Simulator — Interactive sliders for real-time prediction changes
"""
import streamlit as st
import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.preprocessing import preprocess_single
from utils.model import predict_class, get_class_info, load_models
from utils.charts import create_radar_chart, create_probability_bar

st.set_page_config(page_title="Simulator | Body Performance AI", page_icon="🔬", layout="wide")

css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'style.css')
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-container" style="padding: 1.5rem;">
    <div class="hero-title" style="font-size: 2rem;">🔬 What-If Simulator</div>
    <div class="hero-subtitle" style="font-size: 1rem;">
        Adjust your metrics in real-time and see how changes impact your predicted fitness class. 
        Try questions like: "What if I increase my grip strength by 10kg?"
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Baseline vs Adjusted ───
st.markdown("### 🎛️ Adjust Your Metrics")
st.markdown("""
<div class="glass-card" style="padding: 1rem;">
    <p style="color: #94A3B8; font-size: 0.9rem;">
        💡 <strong>How to use:</strong> Start with your current metrics on the left. 
        Then adjust the "simulated" values on the right to see the impact on your prediction.
    </p>
</div>
""", unsafe_allow_html=True)

col_base, col_sim = st.columns(2)

with col_base:
    st.markdown("#### 📍 Current Values")
    b_age = st.slider("Age", 18, 70, 28, key="b_age")
    b_gender = st.radio("Gender", ["M", "F"], horizontal=True, key="b_gender")
    b_height = st.slider("Height (cm)", 130, 210, 170, key="b_h")
    b_weight = st.slider("Weight (kg)", 30, 150, 70, key="b_w")
    b_bf = st.slider("Body Fat (%)", 5.0, 50.0, 22.0, 0.5, key="b_bf")
    b_grip = st.slider("Grip Force (kg)", 5.0, 80.0, 38.0, 0.5, key="b_grip")
    b_flex = st.slider("Flexibility (cm)", -30.0, 50.0, 15.0, 0.5, key="b_flex")
    b_sit = st.slider("Sit-ups", 0, 80, 40, key="b_sit")
    b_jump = st.slider("Broad Jump (cm)", 50, 290, 200, key="b_jump")
    b_dia = st.slider("Diastolic (mmHg)", 20, 120, 75, key="b_dia")
    b_sys = st.slider("Systolic (mmHg)", 80, 200, 130, key="b_sys")

with col_sim:
    st.markdown("#### 🔮 Simulated Values")
    s_age = st.slider("Age", 18, 70, b_age, key="s_age")
    s_gender = st.radio("Gender", ["M", "F"], horizontal=True, key="s_gender",
                       index=0 if b_gender == "M" else 1)
    s_height = st.slider("Height (cm)", 130, 210, b_height, key="s_h")
    s_weight = st.slider("Weight (kg)", 30, 150, b_weight, key="s_w")
    s_bf = st.slider("Body Fat (%)", 5.0, 50.0, b_bf, 0.5, key="s_bf")
    s_grip = st.slider("Grip Force (kg)", 5.0, 80.0, b_grip, 0.5, key="s_grip")
    s_flex = st.slider("Flexibility (cm)", -30.0, 50.0, b_flex, 0.5, key="s_flex")
    s_sit = st.slider("Sit-ups", 0, 80, b_sit, key="s_sit")
    s_jump = st.slider("Broad Jump (cm)", 50, 290, b_jump, key="s_jump")
    s_dia = st.slider("Diastolic (mmHg)", 20, 120, b_dia, key="s_dia")
    s_sys = st.slider("Systolic (mmHg)", 80, 200, b_sys, key="s_sys")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── Compare ───
try:
    base_data = {
        'age': b_age, 'gender': b_gender, 'heightCm': b_height, 'weightKg': b_weight,
        'bodyFatPercent': b_bf, 'diastolic': b_dia, 'systolic': b_sys,
        'gripForce': b_grip, 'sitAndBendForwardCm': b_flex,
        'sitUpsCounts': b_sit, 'broadJumpCm': b_jump,
    }
    sim_data = {
        'age': s_age, 'gender': s_gender, 'heightCm': s_height, 'weightKg': s_weight,
        'bodyFatPercent': s_bf, 'diastolic': s_dia, 'systolic': s_sys,
        'gripForce': s_grip, 'sitAndBendForwardCm': s_flex,
        'sitUpsCounts': s_sit, 'broadJumpCm': s_jump,
    }
    
    X_base = preprocess_single(base_data)
    X_sim = preprocess_single(sim_data)
    
    b_label, b_proba, _ = predict_class(X_base, 'xgboost')
    s_label, s_proba, _ = predict_class(X_sim, 'xgboost')
    
    b_info = get_class_info(b_label)
    s_info = get_class_info(s_label)
    
    _, _, _, stats = load_models()
    
    st.markdown("### ⚡ Comparison Results")
    
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"""
        <div class="result-card" style="padding: 1.5rem;">
            <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem;">CURRENT</div>
            <div style="font-size: 2.5rem;">{b_info['emoji']}</div>
            <div class="class-badge class-{b_label}" style="margin-top: 0.5rem;">
                Class {b_label} — {b_info['name']}
            </div>
            <p style="color: #94A3B8; margin-top: 0.5rem; font-size: 0.85rem;">
                Confidence: {max(b_proba.values()) * 100:.1f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(create_probability_bar(b_proba), use_container_width=True, key="chart_base")
    
    with r2:
        changed = b_label != s_label
        border_style = "border: 2px solid #10B981;" if changed and s_info['level'] > b_info['level'] else \
                       "border: 2px solid #EF4444;" if changed and s_info['level'] < b_info['level'] else ""
        
        st.markdown(f"""
        <div class="result-card" style="padding: 1.5rem; {border_style}">
            <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.5rem;">SIMULATED</div>
            <div style="font-size: 2.5rem;">{s_info['emoji']}</div>
            <div class="class-badge class-{s_label}" style="margin-top: 0.5rem;">
                Class {s_label} — {s_info['name']}
            </div>
            <p style="color: #94A3B8; margin-top: 0.5rem; font-size: 0.85rem;">
                Confidence: {max(s_proba.values()) * 100:.1f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(create_probability_bar(s_proba), use_container_width=True, key="chart_sim")
    
    # Change summary
    if changed:
        if s_info['level'] > b_info['level']:
            st.success(f"🎉 Your simulated changes **improved** your class from **{b_label}** to **{s_label}**!")
        else:
            st.warning(f"⚠️ Your simulated changes **decreased** your class from **{b_label}** to **{s_label}**.")
    else:
        st.info(f"ℹ️ No class change detected. You remain in Class **{b_label}**. Try larger adjustments!")
    
    # Show what changed
    changes = []
    labels = {
        'age': 'Age', 'heightCm': 'Height', 'weightKg': 'Weight', 'bodyFatPercent': 'Body Fat',
        'gripForce': 'Grip Force', 'sitAndBendForwardCm': 'Flexibility', 'sitUpsCounts': 'Sit-ups',
        'broadJumpCm': 'Broad Jump', 'diastolic': 'Diastolic', 'systolic': 'Systolic',
    }
    for key in labels:
        if base_data[key] != sim_data[key]:
            diff = sim_data[key] - base_data[key]
            sign = "+" if diff > 0 else ""
            changes.append(f"**{labels[key]}**: {base_data[key]} → {sim_data[key]} ({sign}{diff:.1f})")
    
    if changes:
        st.markdown("#### 📝 Changes Applied")
        for c in changes:
            st.markdown(f"- {c}")
    
    # Radar comparison
    st.markdown("#### 🎯 Profile Comparison")
    class_means = stats.get('class_means', {})
    
    r1, r2 = st.columns(2)
    with r1:
        base_vals = {k: base_data.get(k, 0) for k in ['gripForce', 'sitAndBendForwardCm', 'sitUpsCounts', 'broadJumpCm', 'bodyFatPercent']}
        st.plotly_chart(create_radar_chart(base_vals, class_means, b_label), use_container_width=True, key="radar_base")
    with r2:
        sim_vals = {k: sim_data.get(k, 0) for k in ['gripForce', 'sitAndBendForwardCm', 'sitUpsCounts', 'broadJumpCm', 'bodyFatPercent']}
        st.plotly_chart(create_radar_chart(sim_vals, class_means, s_label), use_container_width=True, key="radar_sim")

except Exception as e:
    st.error(f"⚠️ Error: {str(e)}")
    st.info("Make sure you've run `python train_and_export.py` first to generate the model files.")
