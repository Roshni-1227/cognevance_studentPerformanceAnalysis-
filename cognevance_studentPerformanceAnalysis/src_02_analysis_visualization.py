"""
02_analysis_visualization.py
------------------------------
Runs exploratory data analysis on the cleaned dataset and saves all charts
to charts/. Also prints key statistics used in the final report.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
CLEAN_PATH = "data/student_data_clean.csv"
CHART_DIR = "charts"


def load() -> pd.DataFrame:
    return pd.read_csv(CLEAN_PATH)


def summary_stats(df: pd.DataFrame) -> dict:
    corr_attendance_avg = df["attendance_percentage"].corr(df["average_score"])
    corr_study_avg = df["study_hours_per_week"].corr(df["average_score"])
    by_gender = df.groupby("gender")["average_score"].mean().round(1)
    by_prep = df.groupby("test_preparation")["average_score"].mean().round(1)
    by_band = df.groupby("attendance_band")["average_score"].mean().round(1)
    grade_counts = df["grade"].value_counts().sort_index()

    stats = {
        "n_students": len(df),
        "avg_score_overall": round(df["average_score"].mean(), 1),
        "corr_attendance_avg_score": round(corr_attendance_avg, 3),
        "corr_study_hours_avg_score": round(corr_study_avg, 3),
        "avg_score_by_gender": by_gender.to_dict(),
        "avg_score_by_test_prep": by_prep.to_dict(),
        "avg_score_by_attendance_band": by_band.to_dict(),
        "grade_distribution": grade_counts.to_dict(),
        "pass_rate_pct": round((df["grade"] != "F").mean() * 100, 1),
    }
    return stats


def make_charts(df: pd.DataFrame) -> None:
    # 1. Histogram of average score distribution
    plt.figure(figsize=(7, 5))
    sns.histplot(df["average_score"], bins=20, kde=True, color="#4C72B0")
    plt.title("Distribution of Average Student Scores")
    plt.xlabel("Average Score")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/01_score_distribution.png", dpi=150)
    plt.close()

    # 2. Scatter: attendance vs average score (with regression line)
    plt.figure(figsize=(7, 5))
    sns.regplot(data=df, x="attendance_percentage", y="average_score",
                scatter_kws={"alpha": 0.4, "s": 20}, line_kws={"color": "red"})
    plt.title("Attendance % vs Average Score")
    plt.xlabel("Attendance (%)")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/02_attendance_vs_score.png", dpi=150)
    plt.close()

    # 3. Bar chart: average score by attendance band
    plt.figure(figsize=(7, 5))
    order = ["Low (<60%)", "Average (60-74%)", "Good (75-89%)", "Excellent (90-100%)"]
    sns.barplot(data=df, x="attendance_band", y="average_score", order=order,
            hue="attendance_band", legend=False, palette="viridis")
    plt.title("Average Score by Attendance Band")
    plt.xlabel("Attendance Band")
    plt.ylabel("Average Score")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/03_score_by_attendance_band.png", dpi=150)
    plt.close()

    # 4. Pie chart: grade distribution
    plt.figure(figsize=(6, 6))
    grade_counts = df["grade"].value_counts().sort_index()
    colors = sns.color_palette("Set2", len(grade_counts))
    plt.pie(grade_counts.values, labels=grade_counts.index, autopct="%1.1f%%",
            colors=colors, startangle=90)
    plt.title("Grade Distribution")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/04_grade_distribution.png", dpi=150)
    plt.close()

    # 5. Bar chart: average score by test preparation
    plt.figure(figsize=(6, 5))
    sns.barplot(data=df, x="test_preparation", y="average_score",
            hue="test_preparation", legend=False, palette="pastel")
    plt.title("Average Score: Test Preparation Completed vs Not")
    plt.xlabel("Test Preparation")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/05_score_by_test_prep.png", dpi=150)
    plt.close()

    # 6. Correlation heatmap
    plt.figure(figsize=(6, 5))
    num_cols = ["attendance_percentage", "study_hours_per_week",
                "math_score", "reading_score", "writing_score", "average_score"]
    sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/06_correlation_heatmap.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    df = load()
    stats = summary_stats(df)
    for k, v in stats.items():
        print(f"{k}: {v}")
    make_charts(df)
    print(f"\nSaved 6 charts to {CHART_DIR}/")
