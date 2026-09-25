"""
src_05_risk_analysis.py
--------------------------
Flags students whose combination of low average score, low attendance,
and/or low weekly study hours matches project-defined analytical risk
indicators.

IMPORTANT: These are descriptive, rule-based indicators derived from
fixed thresholds on this dataset. They are NOT predictions, forecasts,
or diagnostic classifications, and should not be interpreted as such.

Thresholds (chosen from this dataset's own distribution):
    Low score           : average_score < 40   (below the 25th percentile)
    Low attendance        : attendance_percentage < 75  (below the 25th percentile)
    Low study hours        : study_hours_per_week < 3     (below the 25th percentile)

Risk level assignment (in order of precedence):
    High Risk           : low score AND low attendance AND low study hours
    Medium Risk           : low score AND (low attendance OR low study hours)
    Watch                : low score only (attendance and study hours are not low)
    No Risk Indicated    : score is not low
"""

import pandas as pd

CLEAN_PATH = "data/student_data_clean.csv"
OUTPUT_PATH = "data/risk_analysis.csv"

SCORE_THRESHOLD = 40
ATTENDANCE_THRESHOLD = 75
STUDY_HOURS_THRESHOLD = 3


def load() -> pd.DataFrame:
    return pd.read_csv(CLEAN_PATH)


def flag_risk_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["low_score_flag"] = df["average_score"] < SCORE_THRESHOLD
    df["low_attendance_flag"] = df["attendance_percentage"] < ATTENDANCE_THRESHOLD
    df["low_study_hours_flag"] = df["study_hours_per_week"] < STUDY_HOURS_THRESHOLD

    def risk_level(row) -> str:
        if not row["low_score_flag"]:
            return "No Risk Indicated"
        if row["low_attendance_flag"] and row["low_study_hours_flag"]:
            return "High Risk"
        if row["low_attendance_flag"] or row["low_study_hours_flag"]:
            return "Medium Risk"
        return "Watch"

    df["risk_level"] = df.apply(risk_level, axis=1)
    df["risk_level"] = pd.Categorical(
        df["risk_level"],
        categories=["High Risk", "Medium Risk", "Watch", "No Risk Indicated"],
        ordered=True,
    )
    return df


def risk_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("risk_level", observed=True)
        .agg(
            student_count=("student_id", "count"),
            avg_score=("average_score", "mean"),
            avg_attendance=("attendance_percentage", "mean"),
            avg_study_hours=("study_hours_per_week", "mean"),
        )
        .round(1)
        .reindex(["High Risk", "Medium Risk", "Watch", "No Risk Indicated"])
        .reset_index()
    )
    summary["share_of_students_pct"] = (
        summary["student_count"] / summary["student_count"].sum() * 100
    ).round(1)
    return summary


if __name__ == "__main__":
    df = load()
    flagged = flag_risk_indicators(df)
    summary = risk_summary(flagged)

    print("=== Risk Level Summary ===")
    print(summary.to_string(index=False))

    output_cols = [
        "student_id", "gender", "average_score", "attendance_percentage",
        "study_hours_per_week", "test_preparation",
        "low_score_flag", "low_attendance_flag", "low_study_hours_flag",
        "risk_level",
    ]
    flagged[output_cols].to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved risk analysis output -> {OUTPUT_PATH}")
