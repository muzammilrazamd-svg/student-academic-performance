"""
Create PowerPoint presentation for Student Academic Performance Analysis project
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# Create presentation
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

def add_title_slide(prs, title, subtitle):
    """Add title slide"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(1))
    title_frame = title_box.text_frame
    title_frame.text = title
    p = title_frame.paragraphs[0]
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)
    p.alignment = PP_ALIGN.CENTER

    # Add subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.8), Inches(9), Inches(0.8))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = subtitle
    p = subtitle_frame.paragraphs[0]
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(100, 100, 100)
    p.alignment = PP_ALIGN.CENTER

    return slide

def add_content_slide(prs, title, bullet_points):
    """Add content slide with title and bullets"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content

    # Set title
    title_shape = slide.shapes.title
    title_shape.text = title
    title_shape.text_frame.paragraphs[0].font.size = Pt(32)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 51, 102)

    # Add content
    content = slide.placeholders[1]
    text_frame = content.text_frame
    text_frame.clear()

    for point in bullet_points:
        p = text_frame.add_paragraph()
        p.text = point
        p.level = 0
        p.font.size = Pt(18)
        p.space_after = Pt(12)

    return slide

def add_table_slide(prs, title, headers, rows):
    """Add slide with table"""
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title only

    # Set title
    title_shape = slide.shapes.title
    title_shape.text = title
    title_shape.text_frame.paragraphs[0].font.size = Pt(32)
    title_shape.text_frame.paragraphs[0].font.bold = True

    # Add table
    table = slide.shapes.add_table(
        len(rows) + 1, len(headers),
        Inches(1), Inches(2),
        Inches(8), Inches(4)
    ).table

    # Set header row
    for col_idx, header in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = header
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(14)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0, 51, 102)
        cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Set data rows
    for row_idx, row_data in enumerate(rows):
        for col_idx, cell_text in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = str(cell_text)
            cell.text_frame.paragraphs[0].font.size = Pt(12)

    return slide

# Slide 1: Title
add_title_slide(
    prs,
    "Student Academic Performance\nAnalysis and Prediction",
    "Using Data Analytics and Machine Learning\nDAV Lab Mini-Project"
)

# Slide 2: Project Overview
add_content_slide(prs, "Project Overview", [
    "📊 Objective: Predict student final exam scores using ML regression models",
    "🎯 Domain: Educational Data Analytics",
    "💡 Approach: Complete data science pipeline from generation to deployment",
    "🔧 Tech Stack: Python, Pandas, NumPy, Scikit-learn, Streamlit, Plotly",
    "✅ Outcome: Interactive web application with 70.41% prediction accuracy (R²)"
])

# Slide 3: Dataset Overview
add_content_slide(prs, "Dataset Overview", [
    "📁 Size: 1,200 student records with 16 attributes",
    "🔬 Source: Synthetically generated (NumPy, seed=42)",
    "📈 Features: 9 numerical + 2 categorical + 1 target variable",
    "🎲 Rationale: Ensures originality, reproducibility, controlled quality issues",
    "🧪 Quality Issues: 157 missing values, 15 duplicate rows (intentional)"
])

# Slide 4: Dataset Features
add_content_slide(prs, "Dataset Features (16 Attributes)", [
    "Academic: attendance %, study hours, assignment score, internal exam, lab score",
    "Historical: previous semester GPA (0-10 scale)",
    "Lifestyle: extracurricular hours, sleep hours, internet usage",
    "Demographic: gender, department (CSE/ECE/EEE/MECH/CIVIL/IT), year",
    "Target: final_exam_score (0-100) → regression problem"
])

# Slide 5: Data Quality Issues
add_table_slide(prs, "Data Quality Treatment",
    ["Column", "Missing Values", "Treatment"],
    [
        ["attendance_percentage", "36", "Median: 69.55%"],
        ["study_hours_per_week", "30", "Median: 19.75 hrs"],
        ["assignment_score", "48", "Median: 59.00"],
        ["previous_semester_gpa", "42", "Median: 5.96"],
        ["Duplicate Rows", "15", "Removed"]
    ]
)

# Slide 6: Data Cleaning Pipeline
add_content_slide(prs, "Data Cleaning Pipeline", [
    "1️⃣ Duplicate Detection: Identified and removed 15 duplicate rows",
    "2️⃣ Missing Value Imputation: Median imputation for 4 columns (157 values)",
    "3️⃣ Range Validation: Clipped values to valid ranges (attendance 0-100, etc.)",
    "4️⃣ Categorical Standardization: Ensured consistent category values",
    "✅ Result: Clean dataset of 1,200 records ready for analysis"
])

# Slide 7: Exploratory Data Analysis
add_content_slide(prs, "Exploratory Data Analysis (EDA)", [
    "📊 Visualizations: Histograms, pie charts, scatter plots, box plots, heatmaps",
    "🔍 Key Findings:",
    "   • Positive correlation: attendance, study hours, assignments → final score",
    "   • Previous GPA strongest predictor (weight: 2.5)",
    "   • Adequate sleep positively impacts performance",
    "   • Excessive internet usage negatively impacts scores",
    "📈 Pass Rate: 18.75% scored ≥60 (challenging assessment)"
])

# Slide 8: Machine Learning Models
add_content_slide(prs, "Machine Learning Approach", [
    "🤖 Models: Linear Regression vs Random Forest Regressor",
    "📊 Train-Test Split: 80% training (960) / 20% testing (240)",
    "🎲 Random State: 42 (reproducibility)",
    "🔢 Features: 11 (9 numerical + 2 encoded categorical)",
    "🎯 Target: final_exam_score (continuous variable)",
    "📏 Evaluation: MAE, RMSE, R² Score"
])

# Slide 9: Model Performance
add_table_slide(prs, "Model Performance Comparison",
    ["Model", "MAE", "RMSE", "R² Score"],
    [
        ["Linear Regression ✅", "4.2269", "5.3535", "0.7041"],
        ["Random Forest", "4.8110", "6.0471", "0.6225"]
    ]
)

# Slide 10: Best Model Analysis
add_content_slide(prs, "Best Model: Linear Regression 🏆", [
    "📊 R² = 0.7041 → Explains 70.41% of variance in final exam scores",
    "📏 MAE = 4.23 points → Average prediction error on 0-100 scale",
    "📐 RMSE = 5.35 points → Typical deviation from actual scores",
    "💡 Why Linear Regression Won:",
    "   • Data generated with weighted linear relationships + Gaussian noise",
    "   • Academic features have proportional relationships with outcomes",
    "   • Simpler model, more interpretable for educational context"
])

# Slide 11: Feature Importance
add_content_slide(prs, "Feature Importance (Weights)", [
    "1️⃣ Previous Semester GPA: 2.5 (strongest predictor)",
    "2️⃣ Internal Exam Score: 0.18",
    "3️⃣ Study Hours per Week: 0.15",
    "4️⃣ Assignment Score: 0.15",
    "5️⃣ Attendance Percentage: 0.12",
    "6️⃣ Lab Score: 0.10",
    "➕ Positive: Sleep hours | ➖ Negative: Internet usage"
])

# Slide 12: Streamlit Web Application
add_content_slide(prs, "Interactive Web Application", [
    "🌐 Framework: Streamlit (Python web framework)",
    "🔐 Authentication: Session-based demo login",
    "📄 5 Pages:",
    "   1. Overview Dashboard (KPIs, charts, dataset preview)",
    "   2. Dataset & Cleaning (workflow, comparison, reports)",
    "   3. Exploratory Analysis (filters, scatter, box plots, heatmap)",
    "   4. Model Comparison (metrics, performance chart)",
    "   5. Predict Performance (11-input form, real-time prediction)"
])

# Slide 13: Key Technologies
add_content_slide(prs, "Technologies & Libraries", [
    "🐍 Python 3.13.7 (base language)",
    "🔢 NumPy 2.2.5 (numerical arrays, random generation)",
    "📊 Pandas 3.0.6 (data manipulation, CSV handling)",
    "📈 Matplotlib 3.11.2 + Seaborn 0.13.2 (static visualizations)",
    "📉 Plotly 6.1.2 (interactive charts)",
    "🤖 Scikit-learn 1.9.1 (ML models, preprocessing, metrics)",
    "🌐 Streamlit 1.65.0 (web application deployment)"
])

# Slide 14: Project Structure
add_content_slide(prs, "Project Architecture", [
    "📁 src/ → 4 Python modules (generation, cleaning, visualization, training)",
    "📁 data/ → Raw + cleaned CSV files (1,215 → 1,200 records)",
    "📁 models/ → 4 trained model artifacts (.pkl files)",
    "📁 reports/ → Academic report, results summary, viva notes",
    "📄 app.py → Main Streamlit application (450+ lines)",
    "📋 requirements.txt → 58 pinned dependencies",
    "📖 README.md + QUICK_START.md → Complete documentation"
])

# Slide 15: Key Results Summary
add_content_slide(prs, "Key Results Summary", [
    "✅ Dataset: 1,200 cleaned records from 1,215 raw records",
    "✅ Data Quality: 157 missing values imputed, 15 duplicates removed",
    "✅ Best Model: Linear Regression (R² = 0.7041, MAE = 4.23)",
    "✅ Prediction Accuracy: ~4 points average error on 0-100 scale",
    "✅ Web App: Fully functional 5-page interactive dashboard",
    "✅ Documentation: 23-section report + viva preparation guide"
])

# Slide 16: Limitations (Honest Assessment)
add_content_slide(prs, "Project Limitations", [
    "🔬 Synthetic Data: Not real students; simplified relationships",
    "📊 Limited Features: Only 11 predictors; missing many real-world factors",
    "   (family background, mental health, teaching quality, motivation)",
    "⚠️ Linear Assumptions: Real relationships may be more complex",
    "⏰ No Temporal Modeling: Doesn't track improvement over semesters",
    "🔐 Demo Authentication: Session-based, not production-grade security"
])

# Slide 17: Future Enhancements
add_content_slide(prs, "Future Improvements", [
    "📊 Real Data: Partner with institution for anonymized historical data",
    "🧠 Advanced Models: XGBoost, neural networks, ensemble methods",
    "📈 More Features: Socioeconomic, psychological, teaching evaluations",
    "⏱️ Time-Series Analysis: Track performance changes across semesters",
    "☁️ Cloud Deployment: Streamlit Cloud, AWS for broader access",
    "🧪 A/B Testing: Evaluate intervention effectiveness",
    "🔍 Causal Inference: Understand WHY features matter (not just correlation)"
])

# Slide 18: Key Learnings
add_content_slide(prs, "What We Learned", [
    "✅ End-to-end data science pipeline: generation → deployment",
    "✅ Data quality is crucial: proper handling of missing values matters",
    "✅ Model selection: simpler models can outperform complex ones",
    "✅ Evaluation rigor: multiple metrics provide fuller picture",
    "✅ Reproducibility: fixed seeds + version control ensure consistency",
    "✅ Documentation: clear README and reports make projects accessible"
])

# Slide 19: DAV Lab Concepts Demonstrated
add_content_slide(prs, "DAV Lab Concepts Covered", [
    "📊 Data Analytics: NumPy arrays, Pandas DataFrames, statistical analysis",
    "🧹 Data Wrangling: Missing value imputation, duplicate removal, validation",
    "📈 Data Visualization: Matplotlib, Seaborn, Plotly (static + interactive)",
    "🔍 Exploratory Data Analysis: Correlation, distribution, trends",
    "🤖 Machine Learning: Supervised regression, train-test split, evaluation",
    "🌐 Deployment: Web application with Streamlit framework"
])

# Slide 20: How to Run the Project
slide = prs.slides.add_slide(prs.slide_layouts[5])
title_shape = slide.shapes.title
title_shape.text = "How to Run the Project"
title_shape.text_frame.paragraphs[0].font.size = Pt(32)
title_shape.text_frame.paragraphs[0].font.bold = True

# Add text box with code
text_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4))
text_frame = text_box.text_frame
text_frame.word_wrap = True

commands = [
    "Step 1: Navigate to project directory",
    'cd "C:\\Users\\MD.Mudassir Raza\\student-academic-performance"',
    "",
    "Step 2: Activate virtual environment",
    ".\\venv\\Scripts\\Activate.ps1",
    "",
    "Step 3: Run Streamlit application",
    "streamlit run app.py",
    "",
    "Step 4: Open browser at http://localhost:8501",
    "Login: demo@student.edu / demo123"
]

for cmd in commands:
    p = text_frame.add_paragraph()
    p.text = cmd
    if cmd.startswith("cd ") or cmd.startswith(".\\") or cmd.startswith("streamlit"):
        p.font.name = "Courier New"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(0, 100, 0)
    else:
        p.font.size = Pt(14)
    p.space_after = Pt(8)

# Slide 21: Conclusion
add_content_slide(prs, "Conclusion", [
    "✅ Successfully built complete data science project from scratch",
    "✅ Demonstrated full pipeline: data → cleaning → EDA → ML → deployment",
    "✅ Achieved 70.41% variance explanation (Linear Regression)",
    "✅ Delivered professional web application with 5 interactive pages",
    "✅ Comprehensive documentation: report, results, viva preparation",
    "🎓 Project Status: COMPLETE, TESTED, AND READY FOR SUBMISSION"
])

# Slide 22: Thank You
slide = prs.slides.add_slide(prs.slide_layouts[6])
title_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(1.5))
title_frame = title_box.text_frame
title_frame.text = "Thank You!\n\nQuestions?"
p = title_frame.paragraphs[0]
p.font.size = Pt(48)
p.font.bold = True
p.font.color.rgb = RGBColor(0, 51, 102)
p.alignment = PP_ALIGN.CENTER

# Add footer
footer_box = slide.shapes.add_textbox(Inches(1), Inches(5.5), Inches(8), Inches(1))
footer_frame = footer_box.text_frame
footer_frame.text = "Student Academic Performance Analysis & Prediction\nDAV Lab Mini-Project | October 2026"
p = footer_frame.paragraphs[0]
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(100, 100, 100)
p.alignment = PP_ALIGN.CENTER

# Save presentation
output_path = "Student_Performance_Analysis_Presentation.pptx"
prs.save(output_path)
print(f"✅ PowerPoint presentation created: {output_path}")
print(f"📊 Total slides: {len(prs.slides)}")
