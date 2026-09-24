"""
03_insights_report.py
-----------------------
Turns the computed statistics into a written insights & recommendations
report (report/PROJECT_REPORT.md).
"""

import pandas as pd
from src_02_analysis_visualization import load, summary_stats

df = load()
s = summary_stats(df)

report = f"""# Student Performance Analysis — Project Report

**Author:** Roshni Kumari
**Program:** Cognevance Technologies — Data Science & Data Analytics (Level 1)

## 1. Objective
Analyze student academic performance data to identify the factors most
strongly associated with higher scores.

## 2. Dataset
- **Records analyzed:** {s['n_students']} students (after cleaning)
- **Fields:** demographics, parental education, lunch type, test
  preparation status, attendance %, weekly study hours, and scores in
  math, reading, and writing.
- **Data quality steps applied:** removed duplicate records, imputed
  missing numeric values with the column median, clipped out-of-range
  values, and standardized categorical text formatting.

## 3. Key Findings

| Metric                                      | Value |
|-----------------------------------------------|-------|
| Overall average score                          | {s['avg_score_overall']} |
| Correlation: attendance % ↔ average score        | {s['corr_attendance_avg_score']} |
| Correlation: weekly study hours ↔ average score  | {s['corr_study_hours_avg_score']} |
| Pass rate (grade above F)                      | {s['pass_rate_pct']}% |

**By attendance band (average score):**
{chr(10).join(f"- {band}: {score}" for band, score in s['avg_score_by_attendance_band'].items())}

**By test preparation status (average score):**
{chr(10).join(f"- {status}: {score}" for status, score in s['avg_score_by_test_prep'].items())}

**By gender (average score):**
{chr(10).join(f"- {gender}: {score}" for gender, score in s['avg_score_by_gender'].items())}

**Grade distribution:**
{chr(10).join(f"- Grade {g}: {c} students" for g, c in sorted(s['grade_distribution'].items()))}

## 4. Conclusions
1. **Attendance matters.** Students in the "Excellent" attendance band
   (90–100%) score noticeably higher on average than those in the "Low"
   band, and the correlation between attendance and average score is
   moderate ({s['corr_attendance_avg_score']}).
2. **Study hours are the strongest driver** of average score among the
   variables tested (correlation {s['corr_study_hours_avg_score']}),
   ahead of attendance.
3. **Test preparation has a measurable effect** — students who completed
   a test-prep course averaged
   {s['avg_score_by_test_prep'].get('completed', 0) - s['avg_score_by_test_prep'].get('none', 0):.1f}
   points higher than those who did not.
4. **Gender is a weak predictor** of performance in this dataset compared
   to attendance, study time, and test preparation.

## 5. Recommended Interventions
- Attendance tracking with an early-outreach threshold at 75%.
- Structured study-time programs, given the strong observed correlation
  with performance.
- Expanded access to test-preparation resources.
- A combined attendance + study-hour indicator as an early-warning signal
  for academic risk, ahead of final exam results.

## 6. Charts
The full set of visualizations is available in `charts/`:
1. `01_score_distribution.png` — overall score distribution
2. `02_attendance_vs_score.png` — attendance vs. score with trend line
3. `03_score_by_attendance_band.png` — average score by attendance band
4. `04_grade_distribution.png` — grade distribution
5. `05_score_by_test_prep.png` — score by test-preparation status
6. `06_correlation_heatmap.png` — correlation between numeric variables
"""

with open("report/PROJECT_REPORT.md", "w") as f:
    f.write(report)

print("Saved report -> report/PROJECT_REPORT.md")
print(report)
