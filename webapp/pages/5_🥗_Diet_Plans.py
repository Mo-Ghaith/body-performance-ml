import streamlit as st
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.recommendations import get_diet_plan

st.set_page_config(page_title="Diet Plans | Body Performance AI", page_icon="🥗", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'style.css')
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<div style="position: relative; border-radius: 16px; overflow: hidden; margin-bottom: 2.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(to right, rgba(16, 185, 129, 0.95), rgba(16, 185, 129, 0.4)); z-index: 1;"></div>
    <img src="https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=1200&q=80" style="width: 100%; height: 350px; object-fit: cover; display: block;">
    <div style="position: absolute; top: 50%; left: 5%; transform: translateY(-50%); z-index: 2; max-width: 600px; padding: 2rem;">
        <h1 style="color: white; font-size: 3.5rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.2;">🥗 Nutrition <span style="color: #A7F3D0;">Plans</span></h1>
        <p style="color: #F8FAFC; font-size: 1.2rem; line-height: 1.6;">Fuel your body for peak performance with science-backed meal plans tailored to your AI-predicted fitness profile.</p>
    </div>
</div>
""", unsafe_allow_html=True)

metrics = st.session_state.get('user_metrics')

if not metrics:
    st.warning("⚠️ No prediction found. Please analyze your body metrics first to get a personalized diet plan.")
    st.page_link("pages/1_🏋️_Predict.py", label="Go to Predict Page", icon="🏋️")
else:
    class_label = metrics['class_label']
    bmi = metrics['bmi']
    body_fat = metrics['body_fat']
    gender = metrics['gender']
    
    diet = get_diet_plan(class_label, bmi, body_fat, gender)
    
    st.markdown(f"<h2 style='text-align: center; color: #10B981; margin-top: 2rem;'>{diet['title']}</h2>", unsafe_allow_html=True)
    
    # PDF Export
    try:
        from utils.pdf_generator import create_report_pdf
        from utils.recommendations import get_exercise_plan
        pdf_exercise = get_exercise_plan(class_label, metrics['age'], metrics['grip_force'], metrics['flexibility'], metrics['sit_ups'], metrics['broad_jump'])
        pdf_bytes = create_report_pdf(metrics, diet, pdf_exercise)
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.download_button(
                label="📥 Download Full Assessment Report (PDF)",
                data=pdf_bytes,
                file_name=f"BodyPerformance_Report_{class_label}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
    except Exception as e:
        st.error(f"PDF Generation failed: {e}")

    # Render stats
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.metric("🔥 Calories", diet['calories'])
    with mc2:
        st.metric("🍗 Protein", diet['protein'])
    with mc3:
        st.metric("🍞 Carbs", diet['carbs'])
    with mc4:
        st.metric("💧 Hydration", diet['hydration'])
        
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Render meals
    st.markdown("### 🍽️ Daily Meal Plan")
    for meal_name, meal_desc in diet['meals']:
        # Extract meal icon if any
        icon = '🌅' if 'Breakfast' in meal_name else '🥗' if 'Lunch' in meal_name else '🍎' if 'Snack' in meal_name else '🥘' if 'Dinner' in meal_name else '🌙'
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.05); border-left: 4px solid #10B981; padding: 1.5rem; margin-bottom: 1rem; border-radius: 4px;">
            <div style="font-size: 1.3rem; font-weight: 700; color: #10B981; margin-bottom: 0.5rem;">{meal_name}</div>
            <div style="font-size: 1.1rem; color: #E2E8F0;">{meal_desc}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Render tips
    st.markdown("### 💡 Nutrition Tips")
    for tip in diet['tips']:
        st.markdown(f"""
        <div style="display: flex; align-items: start; margin-bottom: 1rem; background: #1E293B; padding: 1rem; border-radius: 8px;">
            <div style="margin-right: 1rem; font-size: 1.5rem;">✨</div>
            <div style="color: #F8FAFC; font-size: 1.1rem; padding-top: 0.2rem;">{tip}</div>
        </div>
        """, unsafe_allow_html=True)
