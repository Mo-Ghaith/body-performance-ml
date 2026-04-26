"""
Page 1: Individual Prediction — Input form with sliders and ML prediction
"""
import streamlit as st
import os
import sys
import pandas as pd
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.preprocessing import preprocess_single
from utils.model import predict_class, get_class_info, load_models, get_custom_model, predict_custom_class
from utils.recommendations import get_diet_plan, get_exercise_plan, get_motivational_message
from utils.charts import create_radar_chart, create_gauge_chart, create_probability_bar, create_distribution_chart

st.set_page_config(page_title="Predict | Body Performance AI", page_icon="🏋️", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'style.css')
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-container" style="padding: 1.5rem;">
    <div class="hero-title" style="font-size: 2rem;">🏋️ Performance Prediction</div>
    <div class="hero-subtitle" style="font-size: 1rem;">
        Enter your body metrics below and get an instant AI-powered fitness analysis with personalized recommendations.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Input Form ───
st.markdown("### 📝 Enter Your Body Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("🎂 Age", 18, 70, 28, help="Your current age in years")
    gender = st.radio("⚧ Gender", ["M", "F"], horizontal=True, help="Biological sex")
    height_cm = st.slider("📏 Height (cm)", 130, 210, 170, help="Height in centimeters")
    weight_kg = st.slider("⚖️ Weight (kg)", 30, 150, 70, help="Body weight in kilograms")

with col2:
    body_fat = st.slider("📊 Body Fat (%)", 5.0, 50.0, 22.0, 0.5, help="Body fat as percentage of total weight")
    grip_force = st.slider("✊ Grip Force (kg)", 5.0, 80.0, 38.0, 0.5, help="Hand grip strength measurement")
    flexibility = st.slider("🤸 Sit & Bend Forward (cm)", -30.0, 50.0, 15.0, 0.5, 
                           help="Flexibility test — distance past/before toes")
    
with col3:
    sit_ups = st.slider("🏋️ Sit-ups Count", 0, 80, 40, help="Number of sit-ups completed")
    broad_jump = st.slider("🦘 Broad Jump (cm)", 50, 290, 200, help="Standing broad jump distance")
    diastolic = st.slider("💓 Diastolic BP (mmHg)", 20, 120, 75, help="Blood pressure during heart relaxation")
    systolic = st.slider("💗 Systolic BP (mmHg)", 80, 200, 130, help="Blood pressure during heart contraction")

# Auto-compute BMI preview
bmi = weight_kg / (height_cm / 100) ** 2

st.markdown(f"""
<div class="glass-card" style="text-align: center; padding: 1rem;">
    <span style="color: #94A3B8;">Calculated BMI: </span>
    <span style="color: #8B5CF6; font-weight: 700; font-size: 1.3rem;">{bmi:.1f}</span>
    <span style="color: #94A3B8; margin-left: 1rem;">
        {'🟢 Normal' if 18.5 <= bmi <= 25 else '🟡 Overweight' if bmi <= 30 else '🔴 Obese' if bmi > 30 else '🔵 Underweight'}
    </span>
</div>
""", unsafe_allow_html=True)

# Model selection
MODELS = ['XGBoost', 'MLP', 'KNN', 'Decision Tree', 'SVM (Linear)', 'SVM (RBF)']
model_choice = st.selectbox("🤖 Choose ML Model", MODELS, index=0, help="Pick from 6 available models.")

hparams = {}
with st.expander(f"⚙️ Edit {model_choice} Hyperparameters", expanded=True):
    st.markdown(f"Fine-tune the **{model_choice}** model before making your prediction. The model will be dynamically trained on the latest complete dataset.")
    
    if model_choice == 'KNN':
        hparams['n_neighbors'] = st.slider("Number of Neighbors (k)", 1, 30, 7)
    elif model_choice == 'Decision Tree':
        hparams['max_depth'] = st.slider("Max Depth", 1, 30, 9)
    elif model_choice == 'SVM (Linear)':
        hparams['C'] = st.slider("Regularization (C)", 0.1, 100.0, 1.0, 0.1)
    elif model_choice == 'SVM (RBF)':
        hparams['C'] = st.slider("Regularization (C)", 0.1, 100.0, 10.0, 0.1)
        hparams['gamma'] = st.slider("Gamma (0 = 'scale')", 0.0, 1.0, 0.0, 0.01)
        st.caption("If Gamma is 0, 'scale' is used automatically.")
    elif model_choice == 'MLP':
        hparams['hidden_layer_1'] = st.slider("Hidden Layer 1 Neurons", 32, 256, 128, 32)
        hparams['hidden_layer_2'] = st.slider("Hidden Layer 2 Neurons", 0, 128, 64, 16)
        hparams['max_iter'] = st.slider("Max Iterations", 100, 1000, 200, 100)
    elif model_choice == 'XGBoost':
        hparams['n_estimators'] = st.slider("Number of Trees", 50, 500, 100, 50)
        hparams['max_depth'] = st.slider("Max Depth", 3, 15, 6, 1)
        hparams['learning_rate'] = st.slider("Learning Rate", 0.01, 0.5, 0.1, 0.01)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── Predict ───
if st.button("🚀 Analyze My Performance", use_container_width=True):
    # Prepare input
    input_data = {
        'age': age, 'gender': gender, 'heightCm': height_cm, 'weightKg': weight_kg,
        'bodyFatPercent': body_fat, 'diastolic': diastolic, 'systolic': systolic,
        'gripForce': grip_force, 'sitAndBendForwardCm': flexibility,
        'sitUpsCounts': sit_ups, 'broadJumpCm': broad_jump,
    }
    
    with st.spinner(f"🔬 Training {model_choice} & generating analysis..."):
        try:
            X_scaled = preprocess_single(input_data)
            
            # Dynamically train and predict using the chosen model and hyperparameters
            custom_model = get_custom_model(model_choice, **hparams)
            class_label, proba_dict, class_idx = predict_custom_class(X_scaled, custom_model)
            
            class_info = get_class_info(class_label)
            _, _, _, stats = load_models()
            
            # ─── Results ───
            motivational = get_motivational_message(class_label)
            
            st.markdown(f"""
            <div class="result-card">
                <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">{class_info['emoji']}</div>
                <div class="class-badge class-{class_label}" style="font-size: 1.3rem; padding: 0.8rem 2rem;">
                    Class {class_label} — {class_info['name']}
                </div>
                <p style="color: #94A3B8; margin-top: 1rem; font-size: 1rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                    {class_info['description']}
                </p>
                <p style="color: #E2E8F0; font-size: 1.1rem; margin-top: 1rem; font-weight: 500;">
                    {motivational}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Confidence bars
            st.markdown("#### 📊 Prediction Confidence")
            st.plotly_chart(create_probability_bar(proba_dict), use_container_width=True)
            
            # Radar chart
            st.markdown("#### 🎯 Your Profile vs Class Average")
            user_vals = {
                'gripForce': grip_force, 'sitAndBendForwardCm': flexibility,
                'sitUpsCounts': sit_ups, 'broadJumpCm': broad_jump, 'bodyFatPercent': body_fat,
            }
            class_means = stats.get('class_means', {})
            st.plotly_chart(create_radar_chart(user_vals, class_means, class_label), use_container_width=True)
            
            # Gauge charts
            st.markdown("#### 📈 Metric Gauges")
            g1, g2, g3, g4 = st.columns(4)
            with g1:
                st.plotly_chart(create_gauge_chart(bmi, 14, 45, "BMI", ""), use_container_width=True)
            with g2:
                st.plotly_chart(create_gauge_chart(grip_force, 0, 80, "Grip", "kg"), use_container_width=True)
            with g3:
                st.plotly_chart(create_gauge_chart(flexibility, -30, 50, "Flexibility", "cm"), use_container_width=True)
            with g4:
                st.plotly_chart(create_gauge_chart(sit_ups, 0, 80, "Sit-ups", ""), use_container_width=True)
            
            # ─── AI Explainer (SHAP) ───
            if model_choice in ['XGBoost', 'Decision Tree']:
                st.markdown("#### 🧠 AI Explainability (SHAP)")
                st.caption(f"This waterfall chart shows exactly which metrics pushed your prediction toward Class {class_label} and which held it back.")
                try:
                    import shap
                    import matplotlib
                    matplotlib.use('Agg')
                    import matplotlib.pyplot as plt
                    import joblib
                    from utils.model import MODELS_DIR
                    
                    explainer = shap.TreeExplainer(custom_model)
                    feature_cols = joblib.load(os.path.join(MODELS_DIR, 'feature_cols.pkl'))
                    
                    shap_values = explainer(X_scaled)
                    
                    if len(shap_values.shape) == 3:
                        exp = shap_values[0, :, class_idx]
                    else:
                        exp = shap_values[0]
                        
                    exp.feature_names = feature_cols
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    shap.plots.waterfall(exp, show=False)
                    st.pyplot(fig)
                    plt.close(fig)
                except Exception as e:
                    st.error(f"Could not generate SHAP visualization: {e}")

            # Distribution comparison
            try:
                cleaned_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'cleaned_data.csv')
                if os.path.exists(cleaned_path):
                    df_pop = pd.read_csv(cleaned_path)
                    st.markdown("#### 📊 Where You Stand in the Population")
                    dc1, dc2 = st.columns(2)
                    with dc1:
                        st.plotly_chart(create_distribution_chart(df_pop['gripForce'], grip_force, "Grip Force Distribution", "#8B5CF6"), use_container_width=True)
                    with dc2:
                        st.plotly_chart(create_distribution_chart(df_pop['broadJumpCm'], broad_jump, "Broad Jump Distribution", "#3B82F6"), use_container_width=True)
            except Exception:
                pass
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # ─── Recommendations Links ───
            st.markdown("## 📋 Your Next Steps")
            
            # Save metrics to session state for other pages
            st.session_state['user_metrics'] = {
                'class_label': class_label,
                'bmi': bmi,
                'body_fat': body_fat,
                'gender': gender,
                'age': age,
                'grip_force': grip_force,
                'flexibility': flexibility,
                'sit_ups': sit_ups,
                'broad_jump': broad_jump
            }
            
            st.info("We've generated specialized diet and exercise content based on your results. Go check them out!")
            
            c1, c2 = st.columns(2)
            with c1:
                # Use page_link for navigation
                st.page_link("pages/5_🥗_Diet_Plans.py", label="View Personalized Diet Plan", icon="🥗", use_container_width=True)
            with c2:
                st.page_link("pages/6_💪_Exercise_Programs.py", label="View Custom Exercise Program", icon="💪", use_container_width=True)
            
            # PDF Export Download Button
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            try:
                from utils.pdf_generator import create_report_pdf
                # Generate background plans for the PDF
                m = st.session_state['user_metrics']
                pdf_diet = get_diet_plan(class_label, m['bmi'], m['body_fat'], m['gender'])
                pdf_exercise = get_exercise_plan(class_label, m['age'], m['grip_force'], m['flexibility'], m['sit_ups'], m['broad_jump'])
                
                pdf_bytes = create_report_pdf(st.session_state['user_metrics'], pdf_diet, pdf_exercise)
                
                st.download_button(
                    label="📥 Download Full Assessment Report (PDF)",
                    data=pdf_bytes,
                    file_name="BodyPerformance_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as e:
                st.error(f"Could not generate PDF Report: {e}")
    
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
            st.info("Make sure you've run `python train_and_export.py` first to generate the model files.")
