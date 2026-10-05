"""
model_training.py
Trains Linear Regression and Random Forest models to predict
final_exam_score from academic features.  Evaluates with MAE, RMSE, R².
"""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder


FEATURE_COLS = [
    "attendance_percentage",
    "study_hours_per_week",
    "assignment_score",
    "internal_exam_score",
    "lab_score",
    "previous_semester_gpa",
    "extracurricular_hours",
    "sleep_hours",
    "internet_usage_hours",
]

CATEGORICAL_COLS = ["gender", "department"]
TARGET = "final_exam_score"
MODEL_DIR = "models"
RANDOM_STATE = 42


def prepare_features(df):
    """
    Encode categorical columns and return feature matrix X and target y.
    Also returns the fitted label encoders for later use in prediction.
    """
    data = df.copy()
    encoders = {}
    for col in CATEGORICAL_COLS:
        if col in data.columns:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col].astype(str))
            encoders[col] = le

    all_features = FEATURE_COLS + [c for c in CATEGORICAL_COLS if c in data.columns]
    X = data[all_features]
    y = data[TARGET]
    return X, y, encoders


def train_models(df):
    """
    Train Linear Regression and Random Forest. Return models, metrics,
    and label encoders.
    """
    X, y, encoders = prepare_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE
    )

    # --- Linear Regression ---
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)

    # --- Random Forest ---
    rf = RandomForestRegressor(
        n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1
    )
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)

    # --- Evaluate ---
    def evaluate(y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        return {"MAE": round(mae, 4), "RMSE": round(rmse, 4), "R²": round(r2, 4)}

    lr_metrics = evaluate(y_test, lr_pred)
    rf_metrics = evaluate(y_test, rf_pred)

    results = pd.DataFrame([
        {"Model": "Linear Regression", **lr_metrics},
        {"Model": "Random Forest", **rf_metrics},
    ])

    return {
        "lr_model": lr,
        "rf_model": rf,
        "results": results,
        "lr_metrics": lr_metrics,
        "rf_metrics": rf_metrics,
        "encoders": encoders,
        "feature_columns": list(X.columns),
    }


def save_models(train_output, model_dir=MODEL_DIR):
    """Save trained models and encoders with joblib."""
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(train_output["lr_model"],
                os.path.join(model_dir, "linear_regression.pkl"))
    joblib.dump(train_output["rf_model"],
                os.path.join(model_dir, "random_forest.pkl"))
    joblib.dump(train_output["encoders"],
                os.path.join(model_dir, "encoders.pkl"))
    joblib.dump(train_output["feature_columns"],
                os.path.join(model_dir, "feature_columns.pkl"))
    print(f"Models saved to {model_dir}/")


def load_models(model_dir=MODEL_DIR):
    """Load previously saved models and encoders."""
    lr = joblib.load(os.path.join(model_dir, "linear_regression.pkl"))
    rf = joblib.load(os.path.join(model_dir, "random_forest.pkl"))
    encoders = joblib.load(os.path.join(model_dir, "encoders.pkl"))
    features = joblib.load(os.path.join(model_dir, "feature_columns.pkl"))
    return lr, rf, encoders, features


def predict_score(model, encoders, feature_columns, input_dict):
    """
    Predict final_exam_score for a single student.
    input_dict should have raw feature values (including categorical strings).
    """
    row = input_dict.copy()
    for col in CATEGORICAL_COLS:
        if col in row and col in encoders:
            val = str(row[col])
            le = encoders[col]
            if val in le.classes_:
                row[col] = le.transform([val])[0]
            else:
                row[col] = 0  # fallback for unseen labels

    df_input = pd.DataFrame([row])[feature_columns]
    prediction = model.predict(df_input)[0]
    return round(float(np.clip(prediction, 0, 100)), 2)


if __name__ == "__main__":
    from data_cleaning import run_cleaning_pipeline

    _, cleaned, _, _ = run_cleaning_pipeline()
    output = train_models(cleaned)
    save_models(output)
    print("\nModel Evaluation:")
    print(output["results"].to_string(index=False))
