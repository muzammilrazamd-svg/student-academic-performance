# Student Academic Performance Analysis and Prediction

A complete Data Analytics and Visualization (DAV) lab project that demonstrates end-to-end data science workflows using synthetic student academic data. This project showcases data generation, cleaning, exploratory analysis, visualization, and machine learning prediction through an interactive Streamlit web application.

## Description

This project provides a comprehensive analysis of student academic performance using a synthetic dataset of 1200 student records. It demonstrates the complete data analytics pipeline from data generation and cleaning to advanced visualization and predictive modeling. The project serves as an educational tool for understanding how various factors like study hours, attendance, and extracurricular activities impact student performance.

## Objectives

- Demonstrate data analytics and visualization techniques on educational data
- Implement data cleaning and preprocessing workflows
- Create interactive visualizations to explore relationships in student data
- Build and compare machine learning models for performance prediction
- Provide an intuitive web interface for exploring insights and making predictions

## Tech Stack

**Core Technologies:**
- Python 3.8+
- Streamlit (Web application framework)

**Data Processing & Analysis:**
- Pandas (Data manipulation)
- NumPy (Numerical computing)

**Visualization:**
- Matplotlib (Static plots)
- Seaborn (Statistical visualizations)
- Plotly (Interactive charts)

**Machine Learning:**
- Scikit-learn (ML algorithms and evaluation)

## Dataset

The project uses a synthetic dataset of **1200 student records** with **16 attributes**:

### Columns

| Column | Description | Type |
|--------|-------------|------|
| `student_id` | Unique identifier for each student | Integer |
| `age` | Student age (18-25 years) | Integer |
| `gender` | Gender (Male/Female/Other) | Categorical |
| `department` | Academic department (CS, EE, ME, Civil, ECE) | Categorical |
| `year` | Year of study (1-4) | Integer |
| `attendance_percentage` | Class attendance percentage (0-100) | Float |
| `study_hours_per_week` | Weekly study hours | Float |
| `assignment_score` | Assignment scores (0-100) | Float |
| `internal_exam_score` | Internal examination scores (0-100) | Float |
| `lab_score` | Laboratory work scores (0-100) | Float |
| `previous_semester_gpa` | GPA from previous semester (0-10) | Float |
| `extracurricular_hours` | Weekly hours in extracurricular activities | Float |
| `sleep_hours` | Average daily sleep hours | Float |
| `internet_usage_hours` | Daily internet usage hours | Float |
| `final_exam_score` | Final examination score (target variable) | Float |
| `performance_category` | Performance classification (Excellent/Good/Average/Poor) | Categorical |

## Data Cleaning

The project implements robust data cleaning procedures:

- **Missing Value Imputation**: Median imputation for numerical features
- **Duplicate Removal**: Identification and removal of duplicate records
- **Data Validation**: Range checks and consistency validation
- **Outlier Detection**: Statistical methods to identify and handle outliers

## Visualizations

The application provides comprehensive visualizations including:

### Static Plots
- Scatter plots (study hours vs. final exam scores)
- Histograms (distribution of key metrics)
- Box plots (performance analysis by department)
- Heatmaps (correlation analysis)

### Interactive Plotly Charts
- Dynamic scatter plots with hover information
- Interactive bar charts for categorical analysis
- Customizable filtering and exploration

## Machine Learning Models

Two regression models are implemented to predict final exam scores:

### 1. Linear Regression
- Simple, interpretable baseline model
- Assumes linear relationships between features and target

### 2. Random Forest Regressor
- Ensemble learning method
- Captures non-linear relationships and feature interactions

### Evaluation Metrics

Models are evaluated using:
- **MAE (Mean Absolute Error)**: Average prediction error magnitude
- **RMSE (Root Mean Squared Error)**: Penalizes larger errors more heavily
- **R² Score**: Proportion of variance explained by the model

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. Clone or download the repository

2. Navigate to the project directory:
```bash
cd student-academic-performance
```

3. Create a virtual environment:
```bash
python -m venv venv
```

4. Activate the virtual environment:

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
.\venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

5. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit web application:

```bash
streamlit run app.py
```

The application will open automatically in your default web browser at `http://localhost:8501`

## Project Structure

```
student-academic-performance/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── src/                            # Source code modules
│   ├── __init__.py
│   ├── data_generator.py          # Synthetic data generation
│   ├── data_cleaning.py           # Data preprocessing and cleaning
│   ├── visualization.py           # Visualization functions
│   └── model_training.py          # ML model training and evaluation
│
├── data/                          # Data storage directory
│   └── (generated CSV files)
│
├── models/                        # Trained model artifacts
│   └── (saved model files)
│
├── reports/                       # Generated analysis reports
│   └── (report files)
│
└── screenshots/                   # Application screenshots
    └── README.md
```

## Application Pages

The Streamlit application consists of five main pages:

### 1. Overview
- Project introduction and objectives
- Dataset summary statistics
- Quick insights and key findings

### 2. Dataset & Cleaning
- View raw and cleaned data
- Data quality metrics
- Missing value analysis
- Data cleaning operations log

### 3. Exploratory Analysis
- Statistical summaries
- Distribution analysis
- Correlation heatmaps
- Feature relationships
- Interactive filtering and exploration

### 4. Model Comparison
- Model training interface
- Performance metrics comparison
- Feature importance analysis
- Model selection recommendations

### 5. Predict Performance
- Interactive prediction tool
- Input student features
- Get predicted final exam score
- Model confidence intervals

## Key Features

- **Interactive Dashboard**: User-friendly web interface built with Streamlit
- **Real-time Predictions**: Instant performance predictions based on student attributes
- **Comprehensive Analytics**: Multiple visualization types for deep insights
- **Model Comparison**: Side-by-side evaluation of multiple ML algorithms
- **Data Quality Focus**: Robust data cleaning and validation workflows
- **Reproducible Results**: Consistent data generation with seeded randomness

## Limitations

- **Synthetic Data**: The dataset is artificially generated and may not fully represent real-world student performance patterns
- **Simple Authentication**: Demo authentication is for illustration purposes only and is not production-grade
- **Model Scope**: Current models use basic features and may not capture all factors affecting academic performance
- **Scalability**: Designed for educational purposes with limited dataset size
- **No Production Deployment**: Application runs locally and is not configured for production deployment

## Future Improvements

- **Real Data Integration**: Connect to actual student information systems
- **Advanced Models**: Implement deep learning models (neural networks, gradient boosting)
- **Feature Engineering**: Create derived features (engagement scores, time-based trends)
- **Time Series Analysis**: Track performance changes over multiple semesters
- **Recommendation System**: Suggest personalized study strategies based on predictions
- **Production Deployment**: Deploy to cloud platforms (AWS, Azure, Heroku)
- **User Authentication**: Implement secure login system for multi-user access
- **Real-time Updates**: Enable live data streaming and automatic model retraining
- **Mobile Responsiveness**: Optimize UI for mobile devices
- **Export Functionality**: Add PDF report generation and data export features

## License

This project is created for educational purposes as part of a Data Analytics and Visualization lab assignment.

## Author

Created as a comprehensive DAV lab project demonstrating data science workflows and machine learning applications in educational data analysis.

---

**Note**: This is an academic project using synthetic data. Any resemblance to actual student data is purely coincidental.
