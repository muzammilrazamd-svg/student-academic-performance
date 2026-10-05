"""
app.py — Student Academic Performance Analysis & Prediction
Main Streamlit application.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import hashlib

# ── Ensure the project root is on the Python path ──
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_generator import generate_dataset, introduce_quality_issues, save_raw_dataset
from src.data_cleaning import (
    load_raw_data, get_cleaning_report, clean_dataset, save_cleaned_dataset,
)
from src.model_training import (
    train_models, save_models, load_models, predict_score, FEATURE_COLS,
    CATEGORICAL_COLS,
)
from src.visualization import (
    plot_score_distribution, plot_performance_pie, plot_dept_avg_score,
    plot_scatter, plot_box_dept, plot_category_bar, plot_avg_by_year,
    plot_attendance_by_dept, plot_correlation_heatmap, plot_model_comparison,
)

# ── Page configuration ─────────────────────────────────────────────
st.set_page_config(
    page_title="Student Academic Performance Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .kpi-card h2 { margin: 0; font-size: 2rem; }
    .kpi-card p  { margin: 0.3rem 0 0; font-size: 0.95rem; opacity: 0.9; }
    .kpi-green  { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .kpi-blue   { background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%); }
    .kpi-orange { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); }
    .kpi-purple { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .workflow-step {
        background: #f0f2f6; padding: 0.8rem 1rem; border-radius: 8px;
        margin: 0.4rem 0; border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# DATA LOADING / CACHING
# ═══════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner="Generating dataset …")
def get_raw_data():
    """Generate (or load) the raw dataset."""
    raw_path = os.path.join(PROJECT_ROOT, "data", "students_raw.csv")
    if not os.path.exists(raw_path):
        save_raw_dataset(os.path.join(PROJECT_ROOT, "data"))
    return pd.read_csv(raw_path)


@st.cache_data(show_spinner="Cleaning dataset …")
def get_cleaned_data(_raw_df):
    """Clean the raw dataset and save a cleaned copy."""
    report = get_cleaning_report(_raw_df)
    cleaned, actions = clean_dataset(_raw_df)
    clean_path = os.path.join(PROJECT_ROOT, "data", "students_cleaned.csv")
    save_cleaned_dataset(cleaned, clean_path)
    return cleaned, report, actions


@st.cache_resource(show_spinner="Training models …")
def get_trained_models(_cleaned_df):
    """Train ML models (or load from disk)."""
    model_dir = os.path.join(PROJECT_ROOT, "models")
    try:
        lr, rf, encoders, features = load_models(model_dir)
        # Quick evaluation on current data
        output = train_models(_cleaned_df)
        output["lr_model"] = lr
        output["rf_model"] = rf
        return output
    except Exception:
        output = train_models(_cleaned_df)
        save_models(output, model_dir)
        return output


# ═══════════════════════════════════════════════════════════════════
# AUTHENTICATION  (simple session-state demo)
# ═══════════════════════════════════════════════════════════════════

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def init_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "user_store" not in st.session_state:
        # Pre-populate a demo account
        st.session_state.user_store = {
            "demo@student.edu": hash_password("demo123"),
        }


def auth_page():
    """Render login / create-account form. Returns True if authenticated."""
    init_auth()
    if st.session_state.authenticated:
        return True

    st.title("🎓 Student Academic Performance Analyzer")
    st.markdown("**Please log in to continue.**")
    st.caption(
        "This is a simple session-based login for demonstration purposes only. "
        "It is not production-grade authentication."
    )

    tab_login, tab_register = st.tabs(["Login", "Create Account"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pw")
        if st.button("Login", key="btn_login"):
            store = st.session_state.user_store
            if email in store and store[email] == hash_password(password):
                st.session_state.authenticated = True
                st.session_state.current_user = email
                st.rerun()
            else:
                st.error("Invalid email or password.")

    with tab_register:
        new_email = st.text_input("Email", key="reg_email")
        new_pw = st.text_input("Password", type="password", key="reg_pw")
        confirm_pw = st.text_input("Confirm Password", type="password",
                                   key="reg_pw2")
        if st.button("Create Account", key="btn_register"):
            if not new_email or not new_pw:
                st.error("Email and password are required.")
            elif new_pw != confirm_pw:
                st.error("Passwords do not match.")
            elif new_email in st.session_state.user_store:
                st.error("An account with this email already exists.")
            else:
                st.session_state.user_store[new_email] = hash_password(new_pw)
                st.success("Account created! You can now log in.")

    st.info("**Demo account:** demo@student.edu / demo123")
    return False


# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════

def sidebar_nav():
    with st.sidebar:
        st.markdown("## 🎓 Student Performance")
        st.markdown("---")

        if st.session_state.get("authenticated"):
            st.success(f"Logged in as: {st.session_state.current_user}")
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.current_user = None
                st.rerun()
            st.markdown("---")

        page = st.radio(
            "Navigation",
            ["📊 Overview", "📁 Dataset & Cleaning",
             "📈 Exploratory Analysis", "🤖 Model Comparison",
             "🔮 Predict Performance"],
            label_visibility="collapsed",
        )
    return page


# ═══════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════════════════════════

def page_overview(df):
    st.title("📊 Overview Dashboard")
    st.info(
        "📌 This project uses a **reproducible synthetic student dataset** "
        "created for academic demonstration of Data Analytics and "
        "Visualization techniques. It does not represent real students."
    )

    # KPI cards
    avg_score = df["final_exam_score"].mean()
    avg_att = df["attendance_percentage"].mean()
    avg_gpa = df["previous_semester_gpa"].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f'<div class="kpi-card kpi-purple"><h2>{len(df)}</h2>'
            f'<p>Total Students</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(
            f'<div class="kpi-card kpi-blue"><h2>{avg_score:.1f}</h2>'
            f'<p>Avg Final Score</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(
            f'<div class="kpi-card kpi-green"><h2>{avg_att:.1f}%</h2>'
            f'<p>Avg Attendance</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(
            f'<div class="kpi-card kpi-orange"><h2>{avg_gpa:.2f}</h2>'
            f'<p>Avg GPA</p></div>', unsafe_allow_html=True)

    st.markdown("")

    # Charts row 1
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_score_distribution(df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_performance_pie(df), use_container_width=True)

    # Charts row 2
    st.plotly_chart(plot_dept_avg_score(df), use_container_width=True)

    # Top 10 rows
    st.subheader("📋 Top 10 Student Records")
    st.dataframe(df.head(10), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════
# PAGE: DATASET & CLEANING
# ═══════════════════════════════════════════════════════════════════

def page_dataset(raw_df, cleaned_df, report, actions):
    st.title("📁 Dataset & Cleaning")

    # Workflow diagram
    st.subheader("🔄 Data Cleaning Workflow")
    steps = [
        "RAW DATA", "Missing Value Detection", "Duplicate Detection",
        "Median Imputation", "Validation", "CLEAN DATA",
    ]
    for i, step in enumerate(steps):
        st.markdown(f'<div class="workflow-step">{"↓ " if i > 0 else "⬤ "}'
                    f'<strong>{step}</strong></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Raw dataset info
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📄 Raw Dataset")
        st.metric("Total Rows", report["total_rows"])
        st.metric("Total Columns", report["total_columns"])
        st.metric("Duplicate Rows", report["duplicate_rows"])
        st.metric("Total Missing Values", report["total_missing"])
    with col2:
        st.subheader("✅ Cleaned Dataset")
        st.metric("Rows After Cleaning", len(cleaned_df))
        st.metric("Missing Values After Cleaning",
                  int(cleaned_df.isnull().sum().sum()))

    # Missing values detail
    st.subheader("🔍 Missing Values by Column")
    missing_df = pd.DataFrame({
        "Column": report["columns_with_missing"],
        "Missing Count": [report["missing_values"][c]
                          for c in report["columns_with_missing"]],
    })
    if len(missing_df):
        st.table(missing_df)
    else:
        st.success("No missing values detected.")

    # Data types
    with st.expander("📊 Data Types"):
        st.dataframe(
            pd.DataFrame(raw_df.dtypes, columns=["Type"]).reset_index()
            .rename(columns={"index": "Column"}),
            use_container_width=True,
        )

    # Cleaning actions
    st.subheader("🛠️ Cleaning Actions Performed")
    for action in actions:
        st.success(f"✔ {action}")

    # Previews
    with st.expander("👁️ Raw Dataset Preview (first 20 rows)"):
        st.dataframe(raw_df.head(20), use_container_width=True)
    with st.expander("👁️ Cleaned Dataset Preview (first 20 rows)"):
        st.dataframe(cleaned_df.head(20), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════
# PAGE: EXPLORATORY ANALYSIS
# ═══════════════════════════════════════════════════════════════════

def page_analysis(df):
    st.title("📈 Exploratory Data Analysis")

    # Interactive filters
    st.subheader("🎛️ Filters")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        dept_filter = st.multiselect(
            "Department", options=sorted(df["department"].unique()),
            default=sorted(df["department"].unique()))
    with fc2:
        year_filter = st.multiselect(
            "Year", options=sorted(df["year"].unique()),
            default=sorted(df["year"].unique()))
    with fc3:
        gender_filter = st.multiselect(
            "Gender", options=sorted(df["gender"].unique()),
            default=sorted(df["gender"].unique()))

    filtered = df[
        (df["department"].isin(dept_filter)) &
        (df["year"].isin(year_filter)) &
        (df["gender"].isin(gender_filter))
    ]
    st.caption(f"Showing **{len(filtered)}** of {len(df)} records.")

    if filtered.empty:
        st.warning("No records match the selected filters.")
        return

    # Summary stats
    st.subheader("📊 Summary Statistics")
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    sc1.metric("Avg Final Score", f"{filtered['final_exam_score'].mean():.1f}")
    sc2.metric("Avg Attendance", f"{filtered['attendance_percentage'].mean():.1f}%")
    sc3.metric("Avg Study Hours", f"{filtered['study_hours_per_week'].mean():.1f}")
    sc4.metric("Avg GPA", f"{filtered['previous_semester_gpa'].mean():.2f}")
    pass_pct = (filtered["final_exam_score"] >= 60).mean() * 100
    sc5.metric("Pass % (≥60)", f"{pass_pct:.1f}%")

    st.markdown("---")

    # Scatter plots
    tab1, tab2, tab3 = st.tabs([
        "Attendance vs Score", "Study Hours vs Score", "Internal vs Final"])
    with tab1:
        st.plotly_chart(
            plot_scatter(filtered, "attendance_percentage",
                         "final_exam_score"),
            use_container_width=True)
    with tab2:
        st.plotly_chart(
            plot_scatter(filtered, "study_hours_per_week",
                         "final_exam_score"),
            use_container_width=True)
    with tab3:
        st.plotly_chart(
            plot_scatter(filtered, "internal_exam_score",
                         "final_exam_score"),
            use_container_width=True)

    # Row of charts
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_box_dept(filtered), use_container_width=True)
    with col2:
        st.plotly_chart(plot_category_bar(filtered), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(plot_avg_by_year(filtered), use_container_width=True)
    with col4:
        st.plotly_chart(plot_attendance_by_dept(filtered),
                        use_container_width=True)

    st.plotly_chart(
        plot_score_distribution(filtered), use_container_width=True)

    # Correlation heatmap (matplotlib)
    st.subheader("🔥 Correlation Heatmap")
    st.pyplot(plot_correlation_heatmap(filtered))


# ═══════════════════════════════════════════════════════════════════
# PAGE: MODEL COMPARISON
# ═══════════════════════════════════════════════════════════════════

def page_models(cleaned_df, train_output):
    st.title("🤖 Model Comparison")

    results = train_output["results"]

    st.subheader("📋 Evaluation Metrics")
    st.table(results.set_index("Model"))

    # Identify better model
    best_idx = results["R²"].idxmax()
    best_model = results.loc[best_idx, "Model"]
    best_r2 = results.loc[best_idx, "R²"]
    st.success(f"🏆 **Best Model:** {best_model} (R² = {best_r2})")

    st.plotly_chart(plot_model_comparison(results), use_container_width=True)

    st.markdown("---")
    st.subheader("📖 Model Details")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Linear Regression")
        st.markdown(
            "A simple model that fits a straight-line relationship between "
            "features and the target score. It is easy to interpret and fast "
            "to train."
        )
        for k, v in train_output["lr_metrics"].items():
            st.metric(k, v)

    with col2:
        st.markdown("### Random Forest")
        st.markdown(
            "An ensemble of decision trees that captures non-linear "
            "relationships. Usually more accurate but harder to interpret."
        )
        for k, v in train_output["rf_metrics"].items():
            st.metric(k, v)

    st.markdown("---")
    st.subheader("🔧 Features Used")
    st.write(train_output["feature_columns"])


# ═══════════════════════════════════════════════════════════════════
# PAGE: PREDICT PERFORMANCE
# ═══════════════════════════════════════════════════════════════════

def page_predict(train_output):
    st.title("🔮 Predict Student Performance")
    st.markdown("Enter student details and click **Predict** to estimate the "
                "final exam score using the best trained model.")

    # Use the better model
    results = train_output["results"]
    best_idx = results["R²"].idxmax()
    best_name = results.loc[best_idx, "Model"]
    if "Random Forest" in best_name:
        model = train_output["rf_model"]
    else:
        model = train_output["lr_model"]

    st.info(f"Using **{best_name}** (R² = {results.loc[best_idx, 'R²']})")

    with st.form("prediction_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            department = st.selectbox("Department",
                                      ["CSE", "ECE", "EEE", "MECH",
                                       "CIVIL", "IT"])
            year = st.selectbox("Year", [1, 2, 3, 4])
            gender = st.selectbox("Gender", ["Male", "Female"])
            attendance = st.slider("Attendance (%)", 0, 100, 75)
        with c2:
            study_hours = st.slider("Study Hours / Week", 0, 40, 15)
            assignment = st.slider("Assignment Score", 0, 100, 70)
            internal = st.slider("Internal Exam Score", 0, 100, 65)
            lab = st.slider("Lab Score", 0, 100, 70)
        with c3:
            prev_gpa = st.slider("Previous Semester GPA", 0.0, 10.0, 7.0,
                                 step=0.1)
            extra = st.slider("Extracurricular Hours", 0, 20, 5)
            sleep = st.slider("Sleep Hours", 4, 10, 7)
            internet = st.slider("Internet Usage Hours", 0, 12, 3)

        submitted = st.form_submit_button("🚀 Predict Final Performance")

    if submitted:
        input_data = {
            "department": department,
            "gender": gender,
            "attendance_percentage": attendance,
            "study_hours_per_week": study_hours,
            "assignment_score": assignment,
            "internal_exam_score": internal,
            "lab_score": lab,
            "previous_semester_gpa": prev_gpa,
            "extracurricular_hours": extra,
            "sleep_hours": sleep,
            "internet_usage_hours": internet,
        }

        try:
            score = predict_score(
                model, train_output["encoders"],
                train_output["feature_columns"], input_data,
            )

            # Category
            if score >= 90:
                cat = "Excellent"
                color = "🟢"
            elif score >= 75:
                cat = "Good"
                color = "🔵"
            elif score >= 60:
                cat = "Average"
                color = "🟡"
            else:
                cat = "Needs Improvement"
                color = "🔴"

            st.markdown("---")
            st.subheader("📋 Prediction Result")

            rc1, rc2 = st.columns(2)
            with rc1:
                st.markdown(
                    f'<div class="kpi-card kpi-blue">'
                    f'<h2>{score} / 100</h2>'
                    f'<p>Predicted Final Exam Score</p></div>',
                    unsafe_allow_html=True)
            with rc2:
                st.markdown(
                    f'<div class="kpi-card kpi-green">'
                    f'<h2>{color} {cat}</h2>'
                    f'<p>Performance Category</p></div>',
                    unsafe_allow_html=True)

            st.markdown("")
            st.info(f"Your predicted score indicates **{cat.lower()}** "
                    f"academic performance.")

            # Improvement suggestions
            st.subheader("💡 Suggestions")
            suggestions = []
            if attendance < 70:
                suggestions.append(
                    "📌 **Attendance** is below 70%. Regular class "
                    "attendance is strongly correlated with better scores.")
            if study_hours < 10:
                suggestions.append(
                    "📖 **Study hours** are below 10/week. Consider "
                    "increasing dedicated study time.")
            if assignment < 60:
                suggestions.append(
                    "📝 **Assignment score** is below 60. Completing "
                    "assignments thoroughly can improve understanding.")
            if internal < 60:
                suggestions.append(
                    "📋 **Internal exam score** is below 60. Practice "
                    "with previous papers may help.")
            if sleep < 6:
                suggestions.append(
                    "😴 **Sleep hours** are below 6. Adequate sleep "
                    "improves concentration and memory.")
            if internet > 8:
                suggestions.append(
                    "🌐 **Internet usage** is above 8 hours. Consider "
                    "reducing non-academic screen time.")
            if prev_gpa < 5.0:
                suggestions.append(
                    "📉 **Previous GPA** is below 5.0. Focus on "
                    "strengthening fundamentals from earlier semesters.")
            if not suggestions:
                st.success("Great inputs! Keep up the good work.")
            else:
                for s in suggestions:
                    st.warning(s)

            st.caption(
                "⚠️ These predictions are based on a synthetic dataset "
                "and a machine-learning model trained for academic "
                "demonstration. They are not guaranteed outcomes.")

        except Exception as e:
            st.error(f"Prediction failed: {e}")


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    # Authentication gate
    if not auth_page():
        return

    page = sidebar_nav()

    # Load data
    try:
        raw_df = get_raw_data()
        cleaned_df, report, actions = get_cleaned_data(raw_df)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    # Train / load models (only needed for two pages, but cached)
    try:
        train_output = get_trained_models(cleaned_df)
    except Exception as e:
        st.error(f"Error training models: {e}")
        train_output = None

    # Routing
    if page == "📊 Overview":
        page_overview(cleaned_df)
    elif page == "📁 Dataset & Cleaning":
        page_dataset(raw_df, cleaned_df, report, actions)
    elif page == "📈 Exploratory Analysis":
        page_analysis(cleaned_df)
    elif page == "🤖 Model Comparison":
        if train_output:
            page_models(cleaned_df, train_output)
        else:
            st.error("Models could not be trained. Check the data.")
    elif page == "🔮 Predict Performance":
        if train_output:
            page_predict(train_output)
        else:
            st.error("Models could not be trained. Check the data.")


if __name__ == "__main__":
    main()
