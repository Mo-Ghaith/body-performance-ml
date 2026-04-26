"""
Page 3: CSV Upload — Batch prediction from uploaded CSV files
"""
import streamlit as st
import os
import sys
import pandas as pd
import numpy as np
import io

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.preprocessing import preprocess_csv
from utils.model import predict_batch, get_class_info
from utils.recommendations import get_diet_plan, get_exercise_plan

st.set_page_config(page_title="CSV Upload | Body Performance AI", page_icon="📁", layout="wide")

css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'style.css')
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-container" style="padding: 1.5rem;">
    <div class="hero-title" style="font-size: 2rem;">📁 CSV Batch Prediction</div>
    <div class="hero-subtitle" style="font-size: 1rem;">
        Upload a CSV file with multiple body measurements and get predictions for all rows at once.
    </div>
</div>
""", unsafe_allow_html=True)

# Required columns info
st.markdown("""
<div class="glass-card">
    <strong style="color: #8B5CF6;">📋 Required CSV Columns:</strong>
    <p style="color: #CBD5E1; margin-top: 0.5rem; font-size: 0.9rem;">
        <code>age</code>, <code>gender</code> (M/F), <code>height_cm</code>, <code>weight_kg</code>, 
        <code>body fat_%</code>, <code>diastolic</code>, <code>systolic</code>, <code>gripForce</code>, 
        <code>sit and bend forward_cm</code>, <code>sit-ups counts</code>, <code>broad jump_cm</code>
    </p>
    <p style="color: #94A3B8; font-size: 0.8rem; margin-top: 0.3rem;">
        Both original Kaggle column names and camelCase format are accepted.
    </p>
</div>
""", unsafe_allow_html=True)

# Download sample CSV
sample_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_input.csv')
if os.path.exists(sample_path):
    with open(sample_path, 'rb') as f:
        st.download_button("📥 Download Sample CSV", f, "sample_input.csv", "text/csv")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=['csv'], 
                                  help="Upload a CSV with body measurement columns")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")
        
        # Preview
        with st.expander("👁️ Preview Uploaded Data", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)
        
        # Model selection
        model_choice = st.selectbox("🤖 Model:", ["xgboost", "mlp"],
                                    format_func=lambda x: "XGBoost (Recommended)" if x == "xgboost" else "MLP Neural Network")
        
        if st.button("🚀 Run Batch Predictions", use_container_width=True):
            with st.spinner("🔬 Processing all rows..."):
                try:
                    X_scaled, processed_df = preprocess_csv(df)
                    labels, probas = predict_batch(X_scaled, model_choice)
                    
                    # Build results dataframe
                    results = df.copy()
                    results['Predicted_Class'] = labels
                    results['Confidence'] = [f"{max(p) * 100:.1f}%" for p in probas]
                    results['Class_A_Prob'] = [f"{p[0]*100:.1f}%" for p in probas]
                    results['Class_B_Prob'] = [f"{p[1]*100:.1f}%" for p in probas]
                    results['Class_C_Prob'] = [f"{p[2]*100:.1f}%" for p in probas]
                    results['Class_D_Prob'] = [f"{p[3]*100:.1f}%" for p in probas]
                    
                    # Summary stats
                    st.markdown("### 📊 Batch Results Summary")
                    class_counts = pd.Series(labels).value_counts().sort_index()
                    
                    cols = st.columns(4)
                    for i, cls in enumerate(['A', 'B', 'C', 'D']):
                        count = class_counts.get(cls, 0)
                        info = get_class_info(cls)
                        with cols[i]:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div style="font-size: 1.5rem;">{info['emoji']}</div>
                                <div class="metric-value" style="color: {info['color']};">{count}</div>
                                <div class="metric-label">Class {cls}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                    
                    # Results table
                    st.markdown("### 📋 Detailed Results")
                    
                    def color_class(val):
                        colors = {'A': '#10B981', 'B': '#3B82F6', 'C': '#F59E0B', 'D': '#EF4444'}
                        return f'color: {colors.get(val, "#94A3B8")}; font-weight: bold'
                    
                    styled_results = results.style.applymap(color_class, subset=['Predicted_Class'])
                    st.dataframe(results, use_container_width=True, height=400)
                    
                    # Download results
                    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                    
                    csv_buffer = io.StringIO()
                    results.to_csv(csv_buffer, index=False)
                    st.download_button(
                        "📥 Download Results as CSV",
                        csv_buffer.getvalue(),
                        "prediction_results.csv",
                        "text/csv",
                        use_container_width=True,
                    )
                    
                    # Per-row recommendations (expandable)
                    st.markdown("### 📋 Per-Row Recommendations")
                    st.markdown("""
                    <div class="glass-card" style="padding: 1rem;">
                        <p style="color: #94A3B8; font-size: 0.9rem;">
                            Click on any row below to see personalized diet and exercise recommendations.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show first 10 rows with recommendations
                    for idx in range(min(10, len(results))):
                        row = results.iloc[idx]
                        cls = row['Predicted_Class']
                        info = get_class_info(cls)
                        
                        with st.expander(f"{info['emoji']} Row {idx+1} — Class {cls} ({info['name']}) — Confidence: {row['Confidence']}"):
                            # Get relevant values for recommendations
                            rename_map = {
                                'height_cm': 'heightCm', 'weight_kg': 'weightKg',
                                'body fat_%': 'bodyFatPercent',
                                'sit and bend forward_cm': 'sitAndBendForwardCm',
                                'sit-ups counts': 'sitUpsCounts',
                                'broad jump_cm': 'broadJumpCm',
                            }
                            row_data = {}
                            for orig, new in rename_map.items():
                                if orig in row:
                                    row_data[new] = row[orig]
                                elif new in row:
                                    row_data[new] = row[new]
                            
                            age_val = row.get('age', 30)
                            gender_val = row.get('gender', 'M')
                            weight_val = row_data.get('weightKg', 70)
                            height_val = row_data.get('heightCm', 170)
                            bf_val = row_data.get('bodyFatPercent', 22)
                            grip_val = row_data.get('gripForce', row.get('gripForce', 38))
                            flex_val = row_data.get('sitAndBendForwardCm', 15)
                            situps_val = row_data.get('sitUpsCounts', 40)
                            jump_val = row_data.get('broadJumpCm', 200)
                            
                            bmi_val = weight_val / (height_val / 100) ** 2 if height_val > 0 else 22
                            
                            dc, ec = st.columns(2)
                            with dc:
                                diet = get_diet_plan(cls, bmi_val, bf_val, gender_val)
                                st.markdown(f"**{diet['title']}**")
                                st.write(f"Calories: {diet['calories']}")
                                st.write(f"Protein: {diet['protein']}")
                            with ec:
                                exercise = get_exercise_plan(cls, age_val, grip_val, flex_val, situps_val, jump_val)
                                st.markdown(f"**{exercise['title']}**")
                                st.write(f"Frequency: {exercise['weekly_sessions']}")
                                st.write(f"Intensity: {exercise['intensity']}")
                    
                    if len(results) > 10:
                        st.info(f"ℹ️ Showing recommendations for first 10 of {len(results)} rows. Download the full CSV for all predictions.")
                    
                except Exception as e:
                    st.error(f"⚠️ Error during prediction: {str(e)}")
                    st.info("Ensure your CSV has the required columns. Check the column names above.")
    
    except Exception as e:
        st.error(f"⚠️ Error reading CSV: {str(e)}")
