import streamlit as st
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.recommendations import get_exercise_plan

st.set_page_config(page_title="Exercise Programs | Body Performance AI", page_icon="💪", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'style.css')
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<div style="position: relative; border-radius: 16px; overflow: hidden; margin-bottom: 2.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(to right, rgba(220, 38, 38, 0.95), rgba(220, 38, 38, 0.4)); z-index: 1;"></div>
    <img src="https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=1200&q=80" style="width: 100%; height: 350px; object-fit: cover; display: block;">
    <div style="position: absolute; top: 50%; left: 5%; transform: translateY(-50%); z-index: 2; max-width: 650px; padding: 2rem;">
        <h1 style="color: white; font-size: 3.5rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.2;">💪 Custom <span style="color: #FECACA;">Training</span></h1>
        <p style="color: #F8FAFC; font-size: 1.2rem; line-height: 1.6;">Train smarter with targeted workout routines designed specifically for your fitness tier and physical baseline.</p>
    </div>
</div>
""", unsafe_allow_html=True)

metrics = st.session_state.get('user_metrics')

if not metrics:
    st.warning("⚠️ No prediction found. Please analyze your body metrics first to get a personalized exercise program.")
    st.page_link("pages/1_🏋️_Predict.py", label="Go to Predict Page", icon="🏋️")
else:
    class_label = metrics['class_label']
    age = metrics['age']
    grip_force = metrics['grip_force']
    flexibility = metrics['flexibility']
    sit_ups = metrics['sit_ups']
    broad_jump = metrics['broad_jump']
    
    exercise = get_exercise_plan(class_label, age, grip_force, flexibility, sit_ups, broad_jump)
    
    st.markdown(f"<h2 style='text-align: center; color: #EF4444; margin-top: 2rem;'>{exercise['title']}</h2>", unsafe_allow_html=True)
    
    # PDF Export
    try:
        from utils.pdf_generator import create_report_pdf
        from utils.recommendations import get_diet_plan
        pdf_diet = get_diet_plan(class_label, metrics['bmi'], metrics['body_fat'], metrics['gender'])
        pdf_bytes = create_report_pdf(metrics, pdf_diet, exercise)
        
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

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**🗓️ Frequency:** {exercise['weekly_sessions']}")
    with c2:
        st.markdown(f"**⚡ Intensity:** {exercise['intensity']}")
        
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    for cat in exercise['categories']:
        st.markdown(f"<h3 style='color: #F8FAFC;'>{cat['icon']} {cat['name']}</h3>", unsafe_allow_html=True)
        
        # Build attractive cards for each exercise
        cols = st.columns(3)
        for i, ex in enumerate(cat['exercises']):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2); padding: 1.5rem; margin-bottom: 1rem; border-radius: 8px; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔥</div>
                    <div style="color: #F1F5F9; font-weight: 600; font-size: 1.1rem;">{ex}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
                
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.info(f"🛌 **Recovery:** {exercise['recovery']}")
