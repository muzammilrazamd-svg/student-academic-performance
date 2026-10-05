"""
data_generator.py
Generates a reproducible synthetic dataset of 1,200 student records.
Uses NumPy with a fixed seed so every run produces identical data.
"""

import numpy as np
import pandas as pd
import os

SEED = 42
NUM_STUDENTS = 1200

DEPARTMENTS = ["CSE", "ECE", "EEE", "MECH", "CIVIL", "IT"]
GENDERS = ["Male", "Female"]
YEARS = [1, 2, 3, 4]


def generate_dataset(seed=SEED, n=NUM_STUDENTS):
    """Generate a synthetic student academic performance dataset."""
    rng = np.random.RandomState(seed)

    student_ids = [f"STU{str(i + 1).zfill(4)}" for i in range(n)]
    ages = rng.randint(18, 25, size=n)
    genders = rng.choice(GENDERS, size=n)
    departments = rng.choice(DEPARTMENTS, size=n)
    years = rng.choice(YEARS, size=n)

    # Academic features with realistic distributions
    attendance = rng.uniform(40, 100, size=n).round(1)
    study_hours = rng.uniform(0, 40, size=n).round(1)
    assignment_score = rng.uniform(20, 100, size=n).round(1)
    internal_exam = rng.uniform(15, 100, size=n).round(1)
    lab_score = rng.uniform(20, 100, size=n).round(1)
    prev_gpa = rng.uniform(2.0, 10.0, size=n).round(2)

    # Lifestyle features
    extracurricular = rng.uniform(0, 20, size=n).round(1)
    sleep_hours = rng.uniform(4, 10, size=n).round(1)
    internet_hours = rng.uniform(0, 12, size=n).round(1)

    # --- Final exam score: realistic weighted combination + noise ---
    final_exam = (
        0.12 * attendance
        + 0.15 * study_hours
        + 0.15 * assignment_score
        + 0.18 * internal_exam
        + 0.10 * lab_score
        + 2.5 * prev_gpa
        + 0.3 * sleep_hours
        - 0.4 * internet_hours
        + rng.normal(0, 5, size=n)  # noise
    )
    # Clamp to 0-100
    final_exam = np.clip(final_exam, 0, 100).round(1)

    # Performance category based on final exam score
    def categorize(score):
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 60:
            return "Average"
        else:
            return "Needs Improvement"

    performance = [categorize(s) for s in final_exam]

    df = pd.DataFrame({
        "student_id": student_ids,
        "age": ages,
        "gender": genders,
        "department": departments,
        "year": years,
        "attendance_percentage": attendance,
        "study_hours_per_week": study_hours,
        "assignment_score": assignment_score,
        "internal_exam_score": internal_exam,
        "lab_score": lab_score,
        "previous_semester_gpa": prev_gpa,
        "extracurricular_hours": extracurricular,
        "sleep_hours": sleep_hours,
        "internet_usage_hours": internet_hours,
        "final_exam_score": final_exam,
        "performance_category": performance,
    })

    return df


def introduce_quality_issues(df, seed=SEED):
    """
    Introduce realistic data-quality problems into the dataset:
    - ~2-5% missing values in selected columns.
    - A small number of duplicate rows.
    """
    rng = np.random.RandomState(seed + 1)
    dirty = df.copy()

    # Columns to add missing values to, and percentage
    missing_spec = {
        "attendance_percentage": 0.03,
        "study_hours_per_week": 0.025,
        "assignment_score": 0.04,
        "previous_semester_gpa": 0.035,
    }

    for col, frac in missing_spec.items():
        n_missing = int(len(dirty) * frac)
        idx = rng.choice(dirty.index, size=n_missing, replace=False)
        dirty.loc[idx, col] = np.nan

    # Insert ~15 duplicate rows
    dup_idx = rng.choice(dirty.index, size=15, replace=False)
    duplicates = dirty.loc[dup_idx].copy()
    dirty = pd.concat([dirty, duplicates], ignore_index=True)

    return dirty


def save_raw_dataset(output_dir="data"):
    """Generate dataset, introduce quality issues, and save as CSV."""
    os.makedirs(output_dir, exist_ok=True)
    clean = generate_dataset()
    raw = introduce_quality_issues(clean)
    path = os.path.join(output_dir, "students_raw.csv")
    raw.to_csv(path, index=False)
    print(f"Raw dataset saved: {path}  ({len(raw)} rows)")
    return raw


if __name__ == "__main__":
    save_raw_dataset()
