"""
data_cleaning.py
Cleans the raw student dataset: handles missing values, duplicates,
and validates ranges.
"""

import pandas as pd
import numpy as np
import os


def load_raw_data(path="data/students_raw.csv"):
    """Load the raw dataset from CSV."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Raw data file not found at '{path}'. "
            "Run data_generator.py first."
        )
    return pd.read_csv(path)


def get_cleaning_report(df):
    """Return a dict summarising data-quality issues before cleaning."""
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "total_missing": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "columns_with_missing": [
            col for col in df.columns if df[col].isnull().any()
        ],
    }
    return report


def clean_dataset(df):
    """
    Clean the dataset:
    1. Remove duplicate rows.
    2. Impute numerical missing values with column median.
    3. Validate numerical ranges (clamp out-of-range values).
    4. Ensure categorical consistency.
    Returns cleaned DataFrame and a list of actions taken.
    """
    actions = []
    cleaned = df.copy()

    # --- Step 1: Remove duplicates ---
    n_dups = cleaned.duplicated().sum()
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    actions.append(f"Removed {n_dups} duplicate rows.")

    # --- Step 2: Median imputation for numerical columns ---
    num_cols_to_impute = [
        "attendance_percentage",
        "study_hours_per_week",
        "assignment_score",
        "previous_semester_gpa",
    ]
    for col in num_cols_to_impute:
        if col in cleaned.columns and cleaned[col].isnull().any():
            median_val = cleaned[col].median()
            n_filled = int(cleaned[col].isnull().sum())
            cleaned[col] = cleaned[col].fillna(median_val)
            actions.append(
                f"Filled {n_filled} missing values in '{col}' with median ({median_val:.2f})."
            )

    # --- Step 3: Validate numerical ranges ---
    range_rules = {
        "age": (18, 24),
        "attendance_percentage": (0, 100),
        "study_hours_per_week": (0, 40),
        "assignment_score": (0, 100),
        "internal_exam_score": (0, 100),
        "lab_score": (0, 100),
        "previous_semester_gpa": (0, 10),
        "extracurricular_hours": (0, 20),
        "sleep_hours": (4, 10),
        "internet_usage_hours": (0, 12),
        "final_exam_score": (0, 100),
    }
    for col, (lo, hi) in range_rules.items():
        if col in cleaned.columns:
            out = ((cleaned[col] < lo) | (cleaned[col] > hi)).sum()
            if out > 0:
                cleaned[col] = cleaned[col].clip(lo, hi)
                actions.append(
                    f"Clamped {out} out-of-range values in '{col}' to [{lo}, {hi}]."
                )

    # --- Step 4: Categorical consistency ---
    if "gender" in cleaned.columns:
        cleaned["gender"] = cleaned["gender"].str.strip().str.title()
    if "department" in cleaned.columns:
        cleaned["department"] = cleaned["department"].str.strip().str.upper()
    actions.append("Standardised categorical columns (gender, department).")

    return cleaned, actions


def save_cleaned_dataset(df, path="data/students_cleaned.csv"):
    """Save the cleaned dataset to CSV."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Cleaned dataset saved: {path}  ({len(df)} rows)")


def run_cleaning_pipeline(raw_path="data/students_raw.csv",
                          clean_path="data/students_cleaned.csv"):
    """Full pipeline: load → report → clean → save."""
    raw = load_raw_data(raw_path)
    report = get_cleaning_report(raw)
    cleaned, actions = clean_dataset(raw)
    save_cleaned_dataset(cleaned, clean_path)
    return raw, cleaned, report, actions


if __name__ == "__main__":
    raw, cleaned, report, actions = run_cleaning_pipeline()
    print(f"\nCleaning Report:")
    print(f"  Raw rows      : {report['total_rows']}")
    print(f"  Missing values: {report['total_missing']}")
    print(f"  Duplicates    : {report['duplicate_rows']}")
    print(f"  Cleaned rows  : {len(cleaned)}")
    print(f"\nActions:")
    for a in actions:
        print(f"  - {a}")
