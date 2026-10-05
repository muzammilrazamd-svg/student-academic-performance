# Student Academic Performance Analysis and Prediction Using Data Analytics and Machine Learning

**A Data Analytics and Visualization Laboratory Project**

---

## 1. Introduction

Data analytics has emerged as a transformative force in modern education, enabling institutions to make evidence-based decisions and provide targeted support to students. By leveraging statistical analysis, machine learning, and interactive visualization techniques, educators can identify at-risk students early, understand factors affecting academic success, and implement timely interventions. This project demonstrates the application of data analytics and machine learning to predict student academic performance, showcasing the complete data science pipeline from data generation and preprocessing through exploratory analysis, visualization, and predictive modeling.

---

## 2. Problem Statement

Educational institutions face significant challenges in identifying students who may struggle academically before their performance deteriorates. Traditional assessment methods often detect issues only after students have fallen behind, limiting the effectiveness of interventions. This project addresses the need for predictive analytics that can:

- Identify patterns and correlations in student data that influence academic outcomes
- Predict final exam scores based on demographic, behavioral, and performance indicators
- Enable proactive interventions by flagging at-risk students early in the academic term
- Provide interpretable insights to educators for personalized student support

---

## 3. Objectives

The primary objectives of this project are:

1. **Data Wrangling**: Generate a realistic synthetic dataset and demonstrate professional data cleaning and preprocessing techniques
2. **Exploratory Data Analysis**: Perform comprehensive statistical analysis to understand data distributions, central tendencies, and relationships between variables
3. **Data Visualization**: Create clear, informative visualizations using multiple libraries (Matplotlib, Seaborn, Plotly) to communicate insights effectively
4. **Machine Learning**: Implement and evaluate regression models to predict student performance
5. **Interactive Application**: Develop a user-friendly web application using Streamlit for data exploration and prediction
6. **Documentation**: Maintain comprehensive documentation following software engineering best practices

---

## 4. Scope

### In Scope:
- Synthetic dataset generation with realistic statistical relationships
- Data cleaning, preprocessing, and validation
- Exploratory data analysis with statistical summaries
- Multiple visualization techniques for univariate and multivariate analysis
- Implementation of Linear Regression and Random Forest regression models
- Model evaluation using industry-standard metrics
- Interactive Streamlit web application with authentication
- Real-time prediction interface with user input validation

### Out of Scope:
- Collection and analysis of real student data (due to privacy constraints)
- Deep learning models (neural networks, LSTMs)
- Production deployment with cloud infrastructure
- Advanced feature engineering techniques
- Time-series analysis of longitudinal student data
- Integration with learning management systems (LMS)

---

## 5. Technologies Used

### Core Programming:
- **Python 3.x**: Primary programming language for data science and machine learning

### Web Framework:
- **Streamlit**: Interactive web application framework for data science projects

### Data Manipulation and Analysis:
- **Pandas**: Data structures and data analysis tools
- **NumPy**: Numerical computing with multi-dimensional arrays

### Visualization Libraries:
- **Matplotlib**: Foundational plotting library for static visualizations
- **Seaborn**: Statistical data visualization built on Matplotlib
- **Plotly**: Interactive graphing library for dynamic visualizations

### Machine Learning:
- **Scikit-learn**: Machine learning algorithms, preprocessing, and model evaluation tools

### Development Tools:
- **Git**: Version control system for code management
- **VS Code**: Integrated development environment

---

## 6. Dataset Description

The dataset consists of **1,200 synthetic student records** generated using NumPy's random number generation capabilities with a fixed seed for reproducibility. The data simulates realistic patterns observed in educational settings, including:

- Correlations between study habits and academic performance
- Impact of attendance on exam scores
- Relationships between parental support and student outcomes
- Demographic factors affecting educational achievement

The synthetic nature of the data allows for demonstration of data analytics techniques while avoiding privacy concerns associated with real student information. The data generation process incorporates realistic distributions and inter-variable relationships based on educational research findings.

---

## 7. Dataset Attributes

The dataset includes 16 attributes capturing demographic, behavioral, and performance indicators:

| Attribute | Description | Data Type | Range/Values |
|-----------|-------------|-----------|--------------|
| **Student_ID** | Unique identifier for each student | Integer | 1001-2200 |
| **Age** | Student's age in years | Integer | 15-19 |
| **Gender** | Student's gender | Categorical | Male, Female |
| **Ethnicity** | Student's ethnic background | Categorical | Asian, African, Caucasian, Hispanic |
| **Parental_Education** | Highest education level of parents | Categorical | High School, Bachelor's, Master's, PhD |
| **Study_Hours_Per_Week** | Weekly study hours outside class | Float | 0-40 |
| **Absences** | Number of absences during term | Integer | 0-30 |
| **Tutoring** | Whether student receives tutoring | Categorical | Yes, No |
| **Parental_Support** | Level of parental involvement | Categorical | Low, Medium, High |
| **Extracurricular** | Participation in activities | Categorical | Yes, No |
| **Sports** | Participation in sports | Categorical | Yes, No |
| **Music** | Participation in music programs | Categorical | Yes, No |
| **Volunteering** | Participation in volunteering | Categorical | Yes, No |
| **Previous_Grade** | Grade from previous term | Float | 50-100 |
| **Midterm_Score** | Midterm examination score | Float | 40-100 |
| **Final_Score** | Final examination score (target) | Float | 35-100 |

---

## 8. Data Generation

The synthetic dataset was generated using Python's NumPy library with the following methodology:

### Generation Process:
1. **Fixed Random Seed**: `np.random.seed(42)` ensures reproducibility across runs
2. **Demographic Variables**: Generated using appropriate distributions
   - Age: Normal distribution centered around typical high school ages
   - Gender, Ethnicity: Random categorical assignment with realistic proportions
   - Parental Education: Weighted categorical distribution
3. **Behavioral Variables**: Generated with realistic constraints
   - Study Hours: Log-normal distribution (right-skewed, bounded)
   - Absences: Poisson distribution for count data
   - Categorical indicators: Bernoulli distributions with realistic probabilities
4. **Performance Variables**: Generated with correlations
   - Previous Grade: Normal distribution with controlled variance
   - Midterm Score: Correlated with study hours, previous grade, and attendance
   - Final Score: Strong correlation with midterm, influenced by study hours, tutoring, and behavioral factors

### Realistic Relationships:
- Students with higher study hours tend to score better
- Increased absences correlate negatively with performance
- Tutoring and parental support show positive associations with scores
- Previous academic performance is a strong predictor of future performance

---

## 9. Data Cleaning and Preprocessing

Professional data cleaning was applied to simulate real-world data quality issues:

### Missing Values:
- **Introduction**: 2-5% missing values randomly introduced in numerical columns (Study_Hours_Per_Week, Absences, Previous_Grade, Midterm_Score)
- **Detection**: Identified using `df.isnull().sum()`
- **Imputation Strategy**: Median imputation for numerical features to maintain distribution robustness against outliers
- **Justification**: Median preferred over mean for skewed distributions common in educational data

### Duplicate Records:
- **Detection**: Identified approximately 15 duplicate records using `df.duplicated()`
- **Removal**: Duplicates removed using `df.drop_duplicates()` to ensure data integrity
- **Validation**: Verified unique Student_ID values post-cleaning

### Data Validation:
- **Range Checks**: Verified all scores fall within expected ranges (0-100)
- **Type Consistency**: Ensured appropriate data types for each column
- **Categorical Integrity**: Validated categorical variables contain only expected values
- **Logical Consistency**: Checked for impossible combinations (e.g., Final_Score < Midterm_Score flagged for review)

### Feature Encoding:
- **Label Encoding**: Applied to ordinal categorical variables (Parental_Education, Parental_Support)
- **One-Hot Encoding**: Applied to nominal categorical variables (Gender, Ethnicity) for machine learning models
- **Binary Encoding**: Converted Yes/No variables to 1/0 for model compatibility

---

## 10. Exploratory Data Analysis

Comprehensive statistical analysis was performed to understand the dataset:

### Summary Statistics:
- **Descriptive Statistics**: Mean, median, standard deviation, quartiles for all numerical variables
- **Distribution Analysis**: Identified right-skewed study hours, normally distributed scores
- **Central Tendency**: Calculated measures of center for key performance indicators

### Grouping and Aggregation:
- **Performance by Demographics**: Average scores grouped by gender, ethnicity, parental education
- **Impact of Support Systems**: Mean scores compared across tutoring, parental support, and extracurricular participation levels
- **Behavioral Patterns**: Correlation between study hours, absences, and final scores

### Filtering and Segmentation:
- **At-Risk Identification**: Filtered students with Final_Score < 50
- **High Achievers**: Segmented students with Final_Score > 85
- **Attendance Analysis**: Examined performance differences between high vs. low attendance groups

### Key Findings:
- Strong positive correlation between study hours and final scores
- Significant negative impact of absences on academic performance
- Parental education level shows moderate positive association with student outcomes
- Tutoring demonstrates measurable positive effect on scores

---

## 11. Data Visualization

Multiple visualization techniques were employed to communicate insights:

### Univariate Analysis:
- **Histograms**: Distribution of continuous variables (Study_Hours_Per_Week, Final_Score)
- **Box Plots**: Outlier detection and quartile visualization for numerical features
- **Count Plots**: Frequency distribution of categorical variables (Gender, Tutoring, Parental_Support)

### Bivariate Analysis:
- **Scatter Plots**: Relationship between study hours and final scores, midterm vs. final scores
- **Box Plots by Category**: Final score distributions across different demographic groups
- **Bar Charts**: Average performance by categorical variables

### Multivariate Analysis:
- **Correlation Heatmap**: Pearson correlation coefficients between all numerical variables
- **Pair Plots**: Pairwise relationships between key performance indicators
- **Interactive Plotly Charts**: Allow zooming, hovering, and dynamic exploration

### Visualization Libraries:
- **Matplotlib**: Used for foundational static plots with full customization
- **Seaborn**: Applied for statistical visualizations with attractive default styling
- **Plotly**: Implemented for interactive charts in the Streamlit application

---

## 12. Machine Learning Methodology

### Problem Formulation:
- **Task Type**: Supervised regression (predicting continuous Final_Score)
- **Target Variable**: Final_Score (dependent variable)
- **Features**: All other attributes (independent variables)

### Data Splitting:
- **Training Set**: 80% of data (960 records) for model training
- **Testing Set**: 20% of data (240 records) for model evaluation
- **Random State**: Fixed seed for reproducible splits
- **Stratification**: Not applied (continuous target variable)

### Feature Preparation:
- **Encoding**: Categorical variables converted to numerical format
- **Scaling**: Not applied initially (tree-based models are scale-invariant; linear regression uses unscaled features for interpretability)
- **Feature Selection**: All available features included (no dimensionality reduction)

### Cross-Validation:
- K-fold cross-validation can be applied for robust performance estimation
- Hyperparameter tuning using GridSearchCV or RandomizedSearchCV

---

## 13. Linear Regression

### Model Description:
Linear Regression establishes a linear relationship between features and target variable using the equation:

```
Final_Score = β₀ + β₁X₁ + β₂X₂ + ... + βₙXₙ + ε
```

### Characteristics:
- **Interpretability**: High - coefficients show direct impact of each feature
- **Assumptions**: Linearity, independence, homoscedasticity, normality of residuals
- **Complexity**: Low - simple model with few parameters
- **Training Speed**: Fast - analytical solution using ordinary least squares

### Advantages:
- Easy to implement and interpret
- Computationally efficient
- Provides confidence intervals for predictions
- Suitable baseline model for regression tasks

### Limitations:
- Assumes linear relationships (may underfit complex patterns)
- Sensitive to outliers
- Cannot capture feature interactions without explicit engineering
- Poor performance on non-linear data

---

## 14. Random Forest Regression

### Model Description:
Random Forest is an ensemble learning method that constructs multiple decision trees and aggregates their predictions:

```
Final_Prediction = (1/N) Σ Tree_i(X)
```

### Characteristics:
- **Ensemble Method**: Combines predictions from multiple decision trees
- **Bagging**: Bootstrap aggregating reduces variance through averaging
- **Random Feature Selection**: Each split considers random subset of features
- **Hyperparameters**: Number of trees, max depth, min samples split, max features

### Advantages:
- Handles non-linear relationships effectively
- Robust to outliers and noise
- Provides feature importance rankings
- Requires minimal preprocessing (no scaling needed)
- Reduces overfitting through ensemble averaging

### Limitations:
- Less interpretable than linear models
- Computationally intensive (training and prediction)
- Larger model size (memory footprint)
- May overfit on very noisy data despite ensemble approach

---

## 15. Model Evaluation

### Evaluation Metrics:

#### Mean Absolute Error (MAE):
- Average absolute difference between predictions and actual values
- **Interpretation**: Average prediction error in same units as target variable
- **Range**: 0 to ∞ (lower is better)
- **Formula**: MAE = (1/n) Σ |yᵢ - ŷᵢ|

#### Root Mean Squared Error (RMSE):
- Square root of average squared differences
- **Interpretation**: Standard deviation of prediction errors
- **Sensitivity**: More sensitive to large errors than MAE
- **Formula**: RMSE = √[(1/n) Σ (yᵢ - ŷᵢ)²]

#### R² Score (Coefficient of Determination):
- Proportion of variance in target explained by model
- **Interpretation**: How well model fits data compared to baseline (mean)
- **Range**: -∞ to 1 (1 is perfect fit, 0 is baseline, negative is worse than baseline)
- **Formula**: R² = 1 - [Σ(yᵢ - ŷᵢ)² / Σ(yᵢ - ȳ)²]

### Performance Results:
See `results_summary.md` for actual model performance metrics on the test set. The results document contains:
- Training and testing scores for both models
- Comparative analysis of Linear Regression vs. Random Forest
- Feature importance rankings from Random Forest
- Residual analysis and error distribution
- Model selection recommendations

---

## 16. Results and Findings

### Model Performance:
Detailed performance metrics, including MAE, RMSE, and R² scores for both Linear Regression and Random Forest models, are documented in `results_summary.md`. The results file provides:
- Quantitative comparison of model accuracy
- Analysis of prediction errors and residuals
- Identification of scenarios where each model performs best

### Feature Importance:
The Random Forest model provides feature importance scores indicating which variables most strongly predict final exam scores. Key predictors typically include:
- Midterm_Score (strongest predictor of final performance)
- Study_Hours_Per_Week (positive correlation with achievement)
- Absences (negative correlation with performance)
- Previous_Grade (baseline academic capability)
- Parental_Support (environmental factor)

### Insights for Educators:
- Early midterm performance is highly predictive of final outcomes
- Study habits and attendance are modifiable factors that significantly impact results
- Support systems (tutoring, parental involvement) show measurable effects
- At-risk students can be identified based on behavioral and performance patterns

---

## 17. Streamlit Application

### Application Architecture:
The interactive web application is built using Streamlit and consists of five main pages with session-based authentication:

#### 1. Login Page (`app.py`):
- Simple username/password authentication (demo: admin/admin123)
- Session state management for user authorization
- Entry point to the application

#### 2. Home/Dashboard Page:
- Project overview and executive summary
- Key statistics and high-level insights
- Navigation guide to other pages
- Quick access to main features

#### 3. Data Overview Page:
- Display of raw dataset with pagination
- Interactive data table with sorting and filtering
- Summary statistics panel
- Data quality metrics (missing values, duplicates)
- Download capability for processed data

#### 4. Visualizations Page:
- Interactive Plotly charts with zoom and hover functionality
- Multiple visualization types:
  - Distribution plots for numerical features
  - Correlation heatmap with color-coded relationships
  - Scatter plots for bivariate analysis
  - Box plots for categorical comparisons
- Selectable chart options via sidebar controls
- Responsive design for different screen sizes

#### 5. Prediction Page:
- Interactive form for inputting student attributes
- Real-time prediction using trained Random Forest model
- Input validation and range checking
- User-friendly interface with helpful tooltips
- Prediction confidence intervals (if implemented)
- Suggestions for improvement based on modifiable factors

### Technical Features:
- **Session State**: Maintains user login status and preferences
- **Caching**: `@st.cache_data` decorator for loading data and models efficiently
- **Responsive Layout**: Adapts to different screen sizes
- **Error Handling**: Graceful handling of invalid inputs and missing data
- **Modular Design**: Clean separation of concerns across multiple Python files

---

## 18. Prediction Module

### User Interface:
The prediction page provides an intuitive form where users can input student characteristics:

#### Input Fields:
- **Demographics**: Age, Gender, Ethnicity
- **Family Background**: Parental Education, Parental Support level
- **Academic History**: Previous Grade, Midterm Score
- **Behavioral Factors**: Study Hours per Week, Number of Absences
- **Support Systems**: Tutoring (Yes/No)
- **Extracurricular Activities**: Extracurricular, Sports, Music, Volunteering participation

#### Validation:
- **Range Checks**: Ensures numerical inputs fall within realistic bounds
- **Type Validation**: Confirms correct data types for each field
- **Required Fields**: Alerts user if mandatory information is missing
- **Logical Checks**: Flags inconsistent combinations (e.g., unrealistic age-grade combinations)

#### Prediction Output:
- **Predicted Final Score**: Numerical prediction with confidence indication
- **Risk Assessment**: Categorization as Low Risk, Moderate Risk, or High Risk
- **Actionable Suggestions**: Personalized recommendations such as:
  - "Consider increasing study hours to improve performance"
  - "Attendance is critical - reducing absences could raise score by X points"
  - "Tutoring support recommended based on current performance trajectory"
  - "Strong midterm score indicates likely success - maintain current habits"

#### Interactive Features:
- **Real-time Prediction**: Updates immediately upon form submission
- **Scenario Testing**: Users can modify inputs to explore different scenarios
- **Clear Results Display**: Visual presentation with color-coded risk levels
- **Explanation**: Brief interpretation of prediction for non-technical users

---

## 19. Limitations

### Dataset Limitations:
1. **Synthetic Data**: Generated data may not capture all complexities of real-world student performance
2. **Limited Features**: Real educational data includes many more factors (socioeconomic status, learning disabilities, mental health, teacher quality, curriculum difficulty)
3. **Simplified Relationships**: Linear and ensemble models may not capture complex causal mechanisms
4. **No Temporal Dynamics**: Static snapshot rather than longitudinal tracking of student progress
5. **Missing Context**: Lacks school-level factors, peer influences, and broader environmental variables

### Technical Limitations:
1. **Authentication**: Simple session-based auth (not production-ready; no password hashing, no database)
2. **Model Deployment**: Single model in memory (not scalable for production)
3. **Scalability**: Streamlit not optimized for high-concurrency enterprise use
4. **Data Storage**: No persistent database integration for storing predictions or user data
5. **Model Updating**: No mechanism for retraining models with new data

### Methodological Limitations:
1. **Correlation vs. Causation**: Model identifies correlations but does not establish causal relationships
2. **Generalization**: Performance on synthetic data may not translate to real student populations
3. **Bias**: Potential biases in data generation may be learned by models
4. **Interpretability**: Random Forest provides limited insight into decision-making process
5. **Validation**: Lacks external validation on independent real-world datasets

---

## 20. Future Scope

### Enhanced Modeling:
1. **Deep Learning**: Implement neural networks (MLPs, LSTMs) for capturing complex non-linear patterns
2. **Ensemble Methods**: Combine predictions from multiple models (stacking, blending)
3. **Feature Engineering**: Automated feature creation and selection using domain knowledge
4. **Time-Series Analysis**: Longitudinal modeling of student progress over multiple terms
5. **Explainable AI**: SHAP values, LIME for interpretable predictions

### Real-World Deployment:
1. **Real Data Integration**: Partner with educational institutions to access anonymized real student data
2. **Privacy-Preserving ML**: Implement federated learning or differential privacy techniques
3. **Cloud Deployment**: Deploy on AWS/GCP/Azure with auto-scaling and load balancing
4. **API Development**: RESTful API for integration with existing learning management systems
5. **Continuous Learning**: Online learning algorithms that update models with new data

### Application Enhancements:
1. **Advanced Authentication**: Implement OAuth2, role-based access control (admin, teacher, student roles)
2. **Database Integration**: PostgreSQL/MongoDB for persistent storage of predictions and user interactions
3. **Mobile Application**: Native iOS/Android apps or progressive web app (PWA)
4. **Notification System**: Email/SMS alerts for at-risk students and teachers
5. **Recommendation Engine**: Personalized learning resource recommendations based on student profiles

### Analytical Expansions:
1. **Cohort Analysis**: Compare performance across different student cohorts over time
2. **Intervention Tracking**: Measure effectiveness of interventions on predicted at-risk students
3. **A/B Testing**: Experimental evaluation of different support strategies
4. **Natural Language Processing**: Analyze student feedback, essays, and teacher comments
5. **Multi-Target Prediction**: Predict multiple outcomes (dropout risk, course selection, career paths)

---

## 21. Conclusion

This project successfully demonstrates the end-to-end application of data analytics and machine learning techniques to the educational domain. Through systematic data generation, rigorous preprocessing, comprehensive exploratory analysis, and predictive modeling, we have illustrated how modern data science tools can provide actionable insights for educational stakeholders.

### Key Achievements:
1. **Complete Data Pipeline**: Demonstrated professional data handling from generation through preprocessing, analysis, and modeling
2. **Predictive Capability**: Developed regression models capable of predicting student final exam scores with quantifiable accuracy
3. **Interpretable Insights**: Generated visualizations and statistical summaries that clearly communicate patterns in student data
4. **Interactive Application**: Built a user-friendly web application enabling non-technical users to explore data and generate predictions
5. **Comprehensive Documentation**: Maintained thorough documentation following software engineering and academic standards

### Demonstrated Skills:
- Data wrangling and preprocessing with Pandas and NumPy
- Statistical analysis and hypothesis testing
- Data visualization using Matplotlib, Seaborn, and Plotly
- Machine learning model implementation and evaluation with Scikit-learn
- Web application development with Streamlit
- Version control and collaborative development with Git

### Impact and Applications:
While this project uses synthetic data for demonstration purposes, the methodologies and techniques employed are directly applicable to real educational analytics scenarios. Educational institutions can leverage similar approaches to:
- Identify at-risk students early for timely intervention
- Understand which factors most significantly impact student success
- Evaluate the effectiveness of support programs and interventions
- Optimize resource allocation for maximum educational impact
- Provide data-driven insights to inform policy decisions

### Learning Outcomes:
This project reinforces the value of data-driven decision-making in education and showcases the complete workflow of a data science project—from problem formulation through deployment of an interactive solution. The integration of multiple technologies and libraries demonstrates proficiency in the modern data science ecosystem and readiness for real-world analytical challenges.

---

## 22. References

### Documentation and Libraries:
1. **Streamlit Documentation**. (2026). *Streamlit: The fastest way to build and share data apps*. Retrieved from https://docs.streamlit.io/
2. **Scikit-learn Documentation**. (2026). *Machine Learning in Python*. Retrieved from https://scikit-learn.org/stable/documentation.html
3. **Pandas Documentation**. (2026). *pandas: powerful Python data analysis toolkit*. Retrieved from https://pandas.pydata.org/docs/
4. **NumPy Documentation**. (2026). *NumPy User Guide*. Retrieved from https://numpy.org/doc/stable/
5. **Matplotlib Documentation**. (2026). *Matplotlib: Visualization with Python*. Retrieved from https://matplotlib.org/stable/contents.html
6. **Seaborn Documentation**. (2026). *seaborn: statistical data visualization*. Retrieved from https://seaborn.pydata.org/
7. **Plotly Python Documentation**. (2026). *Plotly Graphing Libraries*. Retrieved from https://plotly.com/python/

### Academic References on Educational Data Mining:
8. Romero, C., & Ventura, S. (2020). *Educational data mining and learning analytics: An updated survey*. WIREs Data Mining and Knowledge Discovery, 10(3), e1355.
9. Baker, R. S., & Inventado, P. S. (2014). *Educational data mining and learning analytics*. In Learning Analytics (pp. 61-75). Springer, New York, NY.
10. Koedinger, K. R., D'Mello, S., McLaughlin, E. A., Pardos, Z. A., & Rosé, C. P. (2015). *Data mining and education*. WIREs Cognitive Science, 6(4), 333-353.

### Machine Learning References:
11. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer.
12. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning with Applications in Python*. Springer.
13. Breiman, L. (2001). *Random Forests*. Machine Learning, 45(1), 5-32.

### Educational Analytics:
14. Ferguson, R. (2012). *Learning analytics: Drivers, developments and challenges*. International Journal of Technology Enhanced Learning, 4(5-6), 304-317.
15. Siemens, G., & Long, P. (2011). *Penetrating the fog: Analytics in learning and education*. EDUCAUSE Review, 46(5), 30-40.

---

**Project Repository**: https://github.com/[username]/student-academic-performance  
**Project Date**: October 2026  
**Course**: Data Analytics and Visualization Laboratory  
**Institution**: [Your Institution Name]

---

*This report documents a demonstration project using synthetic data for educational purposes. All student records are artificially generated and do not represent real individuals.*
