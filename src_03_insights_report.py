"""
src_03_insights_report.py
-----------------------------
Compiles the statistical analysis, segmentation, and risk analysis outputs
into a written findings report (report/PROJECT_REPORT.md).

Language throughout is restricted to what the underlying methods support:
correlation and group-comparison results describe statistical association,
not causation, and are not framed as predictions.
"""

import pandas as pd

from src_02_analysis_visualization import (
    load, summary_stats, correlation_analysis, simple_linear_regression,
    group_wise_analysis,
)

df = load()
s = summary_stats(df)
corr = correlation_analysis(df)
reg_attendance = simple_linear_regression(df, "attendance_percentage")
reg_study = simple_linear_regression(df, "study_hours_per_week")
groups = group_wise_analysis(df)

segment_summary = pd.read_csv("data/segment_summary.csv")
risk_df = pd.read_csv("data/risk_analysis.csv")
risk_counts = risk_df["risk_level"].value_counts().reindex(
    ["High Risk", "Medium Risk", "Watch", "No Risk Indicated"]
)

def fmt_p(p: float) -> str:
    return "< 0.001" if p < 0.001 else f"{p:.3f}"

segment_table = segment_summary.to_string(index=False)
risk_table = "\n".join(f"- {level}: {count} students" for level, count in risk_counts.items())

report = f"""# Student Performance Analysis — Project Report

**Author:** Roshni Kumari
**Program:** Cognevance Technologies — Data Science & Data Analytics (Level 1)

## 1. Problem Statement
Educational institutions often need to understand which factors are
associated with academic performance in order to prioritize support
resources. This project analyzes a 500-student dataset to describe
patterns between attendance, study time, test preparation, and academic
outcomes, and to produce a rule-based segmentation of students for
reporting purposes.

## 2. Dataset
- **Records analyzed:** {s['n_students']} students (after cleaning)
- **Nature of the data:** This project uses a **synthetically generated
  dataset**, structured to match the schema of publicly available
  Kaggle student-performance datasets. It was generated for this project
  so the full pipeline could be built and demonstrated end-to-end; it is
  not observational data collected from a real institution. All
  statistics below describe patterns within this synthetic dataset only.
- **Fields:** demographics, parental education, lunch type, test
  preparation status, attendance %, weekly study hours, and scores in
  math, reading, and writing. See `data_dictionary.md` for full column
  definitions.
- **Data quality steps applied:** removed duplicate records, imputed
  missing numeric values with the column median, clipped out-of-range
  values, and standardized categorical text formatting.

## 3. Statistical Analysis

### 3.1 Correlation
Pearson (linear) and Spearman (monotonic, rank-based) correlation
coefficients between `average_score` and two numeric variables:

| Variable | Pearson r | Pearson p-value | Spearman r | Spearman p-value |
|---|---|---|---|---|
| Attendance % | {corr['attendance_percentage']['pearson_r']} | {fmt_p(corr['attendance_percentage']['pearson_p'])} | {corr['attendance_percentage']['spearman_r']} | {fmt_p(corr['attendance_percentage']['spearman_p'])} |
| Study hours/week | {corr['study_hours_per_week']['pearson_r']} | {fmt_p(corr['study_hours_per_week']['pearson_p'])} | {corr['study_hours_per_week']['spearman_r']} | {fmt_p(corr['study_hours_per_week']['spearman_p'])} |

Both correlations are statistically significant (p < 0.001) and indicate
a **moderate positive association** — students with higher attendance or
more weekly study hours tend to have higher average scores within this
dataset. Correlation describes association, not cause and effect.

### 3.2 Simple Linear Regression
Ordinary least-squares regression of `average_score` on each variable
individually:

| Model | Slope | Intercept | R² | p-value |
|---|---|---|---|---|
| average_score ~ attendance_percentage | {reg_attendance['slope']} | {reg_attendance['intercept']} | {reg_attendance['r_squared']} | {fmt_p(reg_attendance['p_value'])} |
| average_score ~ study_hours_per_week | {reg_study['slope']} | {reg_study['intercept']} | {reg_study['r_squared']} | {fmt_p(reg_study['p_value'])} |

Attendance alone explains about **{reg_attendance['r_squared']*100:.1f}%** of the
variance in average score (R²); study hours alone explain about
**{reg_study['r_squared']*100:.1f}%**. The majority of the variance in scores is
explained by factors outside these two variables. These are simple,
single-variable models fit to describe association within the dataset —
they are not used to predict individual student outcomes in this project.

### 3.3 Group-wise Comparison
| Group | Mean average_score | Std. dev. | n |
|---|---|---|---|
| Test prep — completed | {groups['by_test_prep'].loc['completed','mean']} | {groups['by_test_prep'].loc['completed','std']} | {int(groups['by_test_prep'].loc['completed','count'])} |
| Test prep — none | {groups['by_test_prep'].loc['none','mean']} | {groups['by_test_prep'].loc['none','std']} | {int(groups['by_test_prep'].loc['none','count'])} |
| Gender — female | {groups['by_gender'].loc['female','mean']} | {groups['by_gender'].loc['female','std']} | {int(groups['by_gender'].loc['female','count'])} |
| Gender — male | {groups['by_gender'].loc['male','mean']} | {groups['by_gender'].loc['male','std']} | {int(groups['by_gender'].loc['male','count'])} |

A Welch's t-test comparing average scores between students who completed
test preparation and those who did not returned t = {groups['test_prep_ttest']['t_stat']},
p {fmt_p(groups['test_prep_ttest']['p_value'])} — a statistically significant
difference. The gender difference (0.98-point gap) is small relative to
the within-group standard deviations and is not treated as a meaningful
finding in this report.

A one-way ANOVA comparing average scores across the six parental-education
categories returned F = {groups['parental_education_anova']['f_stat']},
p {fmt_p(groups['parental_education_anova']['p_value'])} (η² = {groups['parental_education_anova']['eta_squared']}) —
no statistically significant difference between groups, and the effect
size is negligible.

## 4. Performance Segmentation
Students were grouped into four score-based segments (see
`src_04_segmentation.py` and `data_dictionary.md` for exact thresholds
and methodology):

```
{segment_table}
```

Segment averages increase consistently across attendance, study hours,
and test-preparation completion rate from "At Risk" to "High Performer,"
consistent with the correlation results above.

## 5. Risk Analysis
Students were flagged using project-defined rules combining low score
with low attendance and/or low study hours (see `src_05_risk_analysis.py`
for the exact thresholds and decision logic). This is a descriptive,
rule-based indicator — not a predictive or diagnostic classification.

{risk_table}

## 6. Key Findings
1. Attendance and weekly study hours are both **positively and
   significantly associated** with average score (Pearson r = {corr['attendance_percentage']['pearson_r']}
   and r = {corr['study_hours_per_week']['pearson_r']} respectively).
2. Study hours show a **stronger association** with score than attendance
   does, based on both correlation strength and regression R².
3. Students who completed test preparation scored significantly higher
   on average ({groups['by_test_prep'].loc['completed','mean']} vs.
   {groups['by_test_prep'].loc['none','mean']}, p < 0.001).
4. Parental education shows **no statistically significant association**
   with average score (one-way ANOVA, p {fmt_p(groups['parental_education_anova']['p_value'])}, η² = {groups['parental_education_anova']['eta_squared']}).
   The gender difference is small relative to within-group variation and
   is not treated as a meaningful finding.
5. Segmentation and risk analysis together identify a
   concentrated subgroup ({int(risk_counts['High Risk'])} students, "High Risk") combining low
   score, low attendance, and low study hours — a natural candidate group
   for targeted review.

## 7. Recommended Areas of Focus
- Attendance monitoring, given its significant association with score.
- Structured study-time support, given the strongest observed association
  in this dataset.
- Continued or expanded test-preparation access.
- Prioritized review of the "High Risk" and "Medium Risk" segments
  identified in the risk analysis output (`data/risk_analysis.csv`).

## 8. Limitations
- **Synthetic data.** All findings describe patterns in a synthetically
  generated dataset built for this project, not real student records.
  Relationships were partly built into the data-generation process
  itself, so results should not be generalized to real institutions.
- **Correlation, not causation.** No causal claims are made or supported
  by this analysis. Observed associations may be explained by other,
  unmeasured factors.
- **No predictive modeling.** The regression models here are simple,
  single-variable, descriptive fits — they are not validated predictive
  models and are not used to forecast individual outcomes.
- **Segmentation and risk thresholds are project-defined**, not
  externally validated or benchmarked against an institutional standard.
- **Single snapshot.** The dataset represents one point in time; no
  trend or longitudinal analysis was performed.

## 9. Deliverables Reference
- `notebooks/student_performance_analysis.ipynb` — full executed workflow
- `charts/` — 9 exported visualizations
- `sql/` — KPI, relationship, and business-question SQL queries
- `data_dictionary.md` — full column documentation
- `data/student_data_segmented.csv`, `data/risk_analysis.csv` — Power BI–ready outputs
"""

with open("report/PROJECT_REPORT.md", "w") as f:
    f.write(report)

print("Saved report -> report/PROJECT_REPORT.md")
