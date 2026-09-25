"""
src_02_analysis_visualization.py
------------------------------------
Exploratory data analysis on the cleaned dataset: descriptive statistics,
Pearson and Spearman correlation, group-wise performance comparisons, and
a simple linear regression of average_score on attendance and on study
hours. Saves all charts to charts/ and prints the statistics used in the
final report.

All correlation and regression results describe association within this
dataset only. They do not establish causation and are not used to predict
outcomes for individual students.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

sns.set_theme(style="whitegrid")
CLEAN_PATH = "data/student_data_clean.csv"
CHART_DIR = "charts"


def load() -> pd.DataFrame:
    return pd.read_csv(CLEAN_PATH)


def descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = ["attendance_percentage", "study_hours_per_week",
                "math_score", "reading_score", "writing_score", "average_score"]
    desc = df[num_cols].describe().T
    desc["skew"] = df[num_cols].skew()
    return desc.round(2)


def correlation_analysis(df: pd.DataFrame) -> dict:
    """Pearson (linear) and Spearman (monotonic, rank-based) correlations,
    each with its two-sided p-value, between average_score and the two
    numeric predictors of interest."""
    results = {}
    for col in ["attendance_percentage", "study_hours_per_week"]:
        pearson_r, pearson_p = stats.pearsonr(df[col], df["average_score"])
        spearman_r, spearman_p = stats.spearmanr(df[col], df["average_score"])
        results[col] = {
            "pearson_r": round(pearson_r, 3),
            "pearson_p": round(pearson_p, 5),
            "spearman_r": round(spearman_r, 3),
            "spearman_p": round(spearman_p, 5),
        }
    return results


def simple_linear_regression(df: pd.DataFrame, predictor: str, target: str = "average_score") -> dict:
    """Ordinary least-squares simple linear regression of `target` on a
    single `predictor`, returning slope, intercept, R^2, and p-value.
    Reported as an association model, not a predictive/causal claim."""
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[predictor], df[target])
    return {
        "predictor": predictor,
        "slope": round(slope, 4),
        "intercept": round(intercept, 3),
        "r_squared": round(r_value ** 2, 4),
        "p_value": round(p_value, 6),
        "std_err": round(std_err, 4),
    }


def group_wise_analysis(df: pd.DataFrame) -> dict:
    by_gender = df.groupby("gender")["average_score"].agg(["mean", "std", "count"]).round(2)
    by_prep = df.groupby("test_preparation")["average_score"].agg(["mean", "std", "count"]).round(2)
    by_band = df.groupby("attendance_band")["average_score"].agg(["mean", "std", "count"]).round(2)
    by_parent_edu = df.groupby("parental_education")["average_score"].agg(["mean", "std", "count"]).round(2)

    # Welch's t-test: test-prep completed vs none (unequal variance assumed)
    prep_completed = df.loc[df["test_preparation"] == "completed", "average_score"]
    prep_none = df.loc[df["test_preparation"] == "none", "average_score"]
    t_stat, t_p = stats.ttest_ind(prep_completed, prep_none, equal_var=False)

    # One-way ANOVA: average_score across parental_education categories (6 groups)
    edu_groups = [g["average_score"].values for _, g in df.groupby("parental_education")]
    anova_f, anova_p = stats.f_oneway(*edu_groups)
    grand_mean = df["average_score"].mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in edu_groups)
    ss_total = ((df["average_score"] - grand_mean) ** 2).sum()
    eta_squared = ss_between / ss_total

    return {
        "by_gender": by_gender,
        "by_test_prep": by_prep,
        "by_attendance_band": by_band,
        "by_parental_education": by_parent_edu,
        "test_prep_ttest": {"t_stat": round(t_stat, 3), "p_value": round(t_p, 6)},
        "parental_education_anova": {
            "f_stat": round(anova_f, 3),
            "p_value": round(anova_p, 6),
            "eta_squared": round(eta_squared, 4),
        },
    }


def summary_stats(df: pd.DataFrame) -> dict:
    """Retained for backward compatibility with src_03_insights_report.py."""
    corr = correlation_analysis(df)
    by_gender = df.groupby("gender")["average_score"].mean().round(1)
    by_prep = df.groupby("test_preparation")["average_score"].mean().round(1)
    by_band = df.groupby("attendance_band")["average_score"].mean().round(1)
    grade_counts = df["grade"].value_counts().sort_index()

    stats_dict = {
        "n_students": len(df),
        "avg_score_overall": round(df["average_score"].mean(), 1),
        "corr_attendance_avg_score": corr["attendance_percentage"]["pearson_r"],
        "corr_study_hours_avg_score": corr["study_hours_per_week"]["pearson_r"],
        "avg_score_by_gender": by_gender.to_dict(),
        "avg_score_by_test_prep": by_prep.to_dict(),
        "avg_score_by_attendance_band": by_band.to_dict(),
        "grade_distribution": grade_counts.to_dict(),
        "pass_rate_pct": round((df["grade"] != "F").mean() * 100, 1),
    }
    return stats_dict


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------

def make_charts(df: pd.DataFrame) -> None:
    # --- Existing charts (unchanged) ---------------------------------------

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

    # 6. Correlation heatmap (Pearson)
    plt.figure(figsize=(6, 5))
    num_cols = ["attendance_percentage", "study_hours_per_week",
                "math_score", "reading_score", "writing_score", "average_score"]
    sns.heatmap(df[num_cols].corr(method="pearson"), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap (Pearson)")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/06_correlation_heatmap.png", dpi=150)
    plt.close()

    # --- New charts ----------------------------------------------------------

    # 7. Scatter: study hours vs average score (with regression line)
    plt.figure(figsize=(7, 5))
    sns.regplot(data=df, x="study_hours_per_week", y="average_score",
                scatter_kws={"alpha": 0.4, "s": 20, "color": "#55A868"},
                line_kws={"color": "darkorange"})
    plt.title("Weekly Study Hours vs Average Score")
    plt.xlabel("Study Hours per Week")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/07_study_hours_vs_score.png", dpi=150)
    plt.close()

    # 8. Boxplot: average score by parental education level
    edu_order = ["some high school", "high school", "some college",
                 "associate's degree", "bachelor's degree", "master's degree"]
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df, x="parental_education", y="average_score",
                order=edu_order, hue="parental_education", legend=False, palette="crest")
    plt.title("Average Score by Parental Education Level")
    plt.xlabel("Parental Education")
    plt.ylabel("Average Score")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/08_score_by_parental_education.png", dpi=150)
    plt.close()

    # 9. Spearman correlation heatmap (rank-based, complements Pearson)
    plt.figure(figsize=(6, 5))
    sns.heatmap(df[num_cols].corr(method="spearman"), annot=True, cmap="BrBG", fmt=".2f")
    plt.title("Correlation Heatmap (Spearman)")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/09_spearman_correlation_heatmap.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    df = load()

    print("=== Descriptive Statistics ===")
    print(descriptive_statistics(df).to_string())

    print("\n=== Correlation Analysis (Pearson & Spearman) ===")
    corr = correlation_analysis(df)
    for col, res in corr.items():
        print(f"{col}: {res}")

    print("\n=== Simple Linear Regression ===")
    reg_attendance = simple_linear_regression(df, "attendance_percentage")
    reg_study = simple_linear_regression(df, "study_hours_per_week")
    print("average_score ~ attendance_percentage:", reg_attendance)
    print("average_score ~ study_hours_per_week :", reg_study)

    print("\n=== Group-wise Analysis ===")
    groups = group_wise_analysis(df)
    for name, table in groups.items():
        print(f"\n-- {name} --")
        print(table)

    stats_summary = summary_stats(df)
    print("\n=== Summary (for report) ===")
    for k, v in stats_summary.items():
        print(f"{k}: {v}")

    make_charts(df)
    print(f"\nSaved 9 charts to {CHART_DIR}/")
