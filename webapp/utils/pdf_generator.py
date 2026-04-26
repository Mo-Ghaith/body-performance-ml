from fpdf import FPDF
import re

class PDFReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(139, 92, 246)
        self.set_x(10)
        self.cell(190, 10, "Body Performance AI - Assessment Report", align="C", ln=1)
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.set_x(10)
        self.cell(190, 10, f"Page {self.page_no()}", align="C", ln=1)

def create_report_pdf(metrics, diet_plan, exercise_plan):
    """Generate a formatted PDF report with the user's prediction, diet, and exercise plans."""
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    def clean_text(text):
        if not text:
            return ""
        # Remove emojis and strip HTML tags
        text = str(text)
        text = re.sub(r'<[^>]+>', '', text)
        # Convert to latin-1 acceptable string
        return text.encode('latin-1', 'replace').decode('latin-1')

    def safe_cell(txt_str, font_style="", font_size=12, h=8):
        pdf.set_font("Helvetica", font_style, font_size)
        pdf.set_x(10)
        pdf.cell(190, h, clean_text(str(txt_str)), ln=1)
        
    def safe_multi(txt_str, font_style="", font_size=11, h=6):
        pdf.set_font("Helvetica", font_style, font_size)
        pdf.set_x(10)
        pdf.multi_cell(190, h, clean_text(str(txt_str)))

    # 1. Prediction Section
    pdf.set_text_color(0, 0, 0)
    safe_cell("1. Performance Prediction", "B", 16, 10)
    
    class_label = metrics.get('class_label', 'Unknown')
    class_desc_map = {
        'A': 'Elite Performer',
        'B': 'Strong Performer',
        'C': 'Average Performer',
        'D': 'Needs Improvement'
    }
    class_desc = class_desc_map.get(class_label, '')
    
    safe_cell(f"Predicted Class: {class_label} ({class_desc})", "", 12)
    safe_cell(f"Age: {metrics.get('age')} | Gender: {metrics.get('gender')}", "", 12)
    bmi_val = metrics.get('bmi', 0)
    safe_cell(f"BMI: {bmi_val:.1f} | Body Fat: {metrics.get('body_fat')}%", "", 12)
    pdf.ln(5)

    # 2. Diet Plan
    if dict(diet_plan):
        safe_cell("2. Personalized Diet Plan", "B", 16, 10)
        
        title = diet_plan.get('title', 'Diet Plan')
        safe_cell(title, "B", 12)
        
        safe_cell(f"Calories: {diet_plan.get('calories', '')}", "", 11, 6)
        safe_cell(f"Protein: {diet_plan.get('protein', '')}", "", 11, 6)
        safe_cell(f"Carbs: {diet_plan.get('carbs', '')}", "", 11, 6)
        safe_cell(f"Hydration: {diet_plan.get('hydration', '')}", "", 11, 6)
        pdf.ln(3)
        
        safe_cell("Daily Meals:", "B", 12)
        for m_name, m_desc in diet_plan.get('meals', []):
            line = f"{m_name}: {m_desc}"
            safe_multi(line, "", 11)
        pdf.ln(3)
        
        safe_cell("Nutrition Tips:", "B", 12)
        for tip in diet_plan.get('tips', []):
            safe_multi(f"- {tip}", "", 11)
        pdf.ln(5)
        
    # 3. Exercise Plan
    if exercise_plan:
        safe_cell("3. Custom Exercise Program", "B", 16, 10)
        
        title = exercise_plan.get('title', 'Exercise Program')
        safe_cell(title, "B", 12)
        
        safe_cell(f"Frequency: {exercise_plan.get('weekly_sessions', '')}", "", 11, 6)
        safe_cell(f"Intensity: {exercise_plan.get('intensity', '')}", "", 11, 6)
        pdf.ln(3)
        
        for cat in exercise_plan.get('categories', []):
            cat_name = cat.get('name', '')
            safe_cell(cat_name, "B", 12)
            for ex in cat.get('exercises', []):
                safe_multi(f"- {ex}", "", 11)
            pdf.ln(2)
            
        safe_multi(f"Recovery: {exercise_plan.get('recovery', '')}", "B", 11)
        
    return bytes(pdf.output())
