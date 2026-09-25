"""
generate_dataset.py
--------------------
Generates the student performance dataset used for this analysis: 500
records covering demographics, attendance, study hours, and scores in
math, reading, and writing, with realistic data-quality issues (missing
values, duplicate records) for the cleaning stage to resolve.
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
N_STUDENTS = 500

genders = RNG.choice(["male", "female"], size=N_STUDENTS)
parent_education = RNG.choice(
    ["some high school", "high school", "some college",
     "associate's degree", "bachelor's degree", "master's degree"],
    size=N_STUDENTS,
    p=[0.15, 0.22, 0.22, 0.20, 0.15, 0.06],
)
test_prep = RNG.choice(["none", "completed"], size=N_STUDENTS, p=[0.64, 0.36])
lunch = RNG.choice(["standard", "free/reduced"], size=N_STUDENTS, p=[0.65, 0.35])

# Attendance & study hours drive scores (with noise) to create a realistic,
# analyzable relationship rather than pure randomness.
attendance = np.clip(RNG.normal(82, 10, N_STUDENTS), 40, 100)
study_hours = np.clip(RNG.normal(4, 2, N_STUDENTS), 0, 12)

base = (
    0.55 * attendance
    + 3.2 * study_hours
    + RNG.normal(0, 8, N_STUDENTS)
)
prep_bonus = np.where(test_prep == "completed", 6, 0)
lunch_bonus = np.where(lunch == "standard", 4, 0)

math_score = np.clip(base * 0.75 + prep_bonus + lunch_bonus + RNG.normal(0, 5, N_STUDENTS), 0, 100)
reading_score = np.clip(base * 0.80 + prep_bonus * 1.2 + RNG.normal(0, 5, N_STUDENTS), 0, 100)
writing_score = np.clip(base * 0.78 + prep_bonus * 1.3 + RNG.normal(0, 5, N_STUDENTS), 0, 100)

df = pd.DataFrame({
    "student_id": [f"S{1000+i}" for i in range(N_STUDENTS)],
    "gender": genders,
    "parental_education": parent_education,
    "lunch": lunch,
    "test_preparation": test_prep,
    "attendance_percentage": attendance.round(1),
    "study_hours_per_week": study_hours.round(1),
    "math_score": math_score.round(1),
    "reading_score": reading_score.round(1),
    "writing_score": writing_score.round(1),
})

# Inject a few realistic data-quality issues so the cleaning step has real work to do.
dirty_idx = RNG.choice(N_STUDENTS, size=15, replace=False)
df.loc[dirty_idx[:5], "attendance_percentage"] = np.nan
df.loc[dirty_idx[5:10], "math_score"] = np.nan
df = pd.concat([df, df.iloc[[3, 17]]], ignore_index=True)  # duplicate rows

df.to_csv("data/student_data.csv", index=False)
print(f"Generated data/student_data.csv with {len(df)} rows (includes injected nulls/duplicates).")
