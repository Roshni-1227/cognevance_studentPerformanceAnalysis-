"""
01_data_cleaning.py
--------------------
Loads the raw dataset, profiles data-quality issues, cleans them, engineers
derived columns (average_score, grade), and writes the cleaned dataset to
data/student_data_clean.csv.
"""

import pandas as pd

RAW_PATH = "data/student_data.csv"
CLEAN_PATH = "data/student_data_clean.csv"


def load_raw(path: str = RAW_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def profile(df: pd.DataFrame) -> None:
    print("Shape:", df.shape)
    print("\nMissing values per column:\n", df.isna().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    print("\nDuplicate student_id:", df["student_id"].duplicated().sum())


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1. Drop exact duplicate rows and duplicate student IDs (keep first).
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset="student_id", keep="first")

    # 2. Impute missing numeric values with the column median (robust to outliers).
    numeric_cols = ["attendance_percentage", "study_hours_per_week",
                     "math_score", "reading_score", "writing_score"]
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # 3. Clip any out-of-range values into valid bounds.
    df["attendance_percentage"] = df["attendance_percentage"].clip(0, 100)
    for col in ["math_score", "reading_score", "writing_score"]:
        df[col] = df[col].clip(0, 100)

    # 4. Normalize categorical text formatting.
    for col in ["gender", "parental_education", "lunch", "test_preparation"]:
        df[col] = df[col].str.strip().str.lower()

    # 5. Feature engineering.
    df["average_score"] = df[["math_score", "reading_score", "writing_score"]].mean(axis=1).round(1)

    def grade(score: float) -> str:
        if score >= 90:
            return "A"
        elif score >= 75:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 40:
            return "D"
        return "F"

    df["grade"] = df["average_score"].apply(grade)

    def attendance_band(pct: float) -> str:
        if pct >= 90:
            return "Excellent (90-100%)"
        elif pct >= 75:
            return "Good (75-89%)"
        elif pct >= 60:
            return "Average (60-74%)"
        return "Low (<60%)"

    df["attendance_band"] = df["attendance_percentage"].apply(attendance_band)

    return df.reset_index(drop=True)


if __name__ == "__main__":
    raw = load_raw()
    print("=== BEFORE CLEANING ===")
    profile(raw)

    cleaned = clean(raw)
    print("\n=== AFTER CLEANING ===")
    profile(cleaned)

    cleaned.to_csv(CLEAN_PATH, index=False)
    print(f"\nSaved cleaned dataset -> {CLEAN_PATH} ({len(cleaned)} rows)")
