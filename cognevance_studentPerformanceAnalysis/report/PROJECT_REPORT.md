# Student Performance Analysis — Project Report

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
- **Records analyzed:** 500 students (after cleaning)
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
| Attendance % | 0.414 | < 0.001 | 0.385 | < 0.001 |
| Study hours/week | 0.515 | < 0.001 | 0.496 | < 0.001 |

Both correlations are statistically significant (p < 0.001) and indicate
a **moderate positive association** — students with higher attendance or
more weekly study hours tend to have higher average scores within this
dataset. Correlation describes association, not cause and effect.

### 3.2 Simple Linear Regression
Ordinary least-squares regression of `average_score` on each variable
individually:

| Model | Slope | Intercept | R² | p-value |
|---|---|---|---|---|
| average_score ~ attendance_percentage | 0.4718 | 10.204 | 0.1715 | < 0.001 |
| average_score ~ study_hours_per_week | 2.6776 | 37.412 | 0.2649 | < 0.001 |

Attendance alone explains about **17.2%** of the
variance in average score (R²); study hours alone explain about
**26.5%**. The majority of the variance in scores is
explained by factors outside these two variables. These are simple,
single-variable models fit to describe association within the dataset —
they are not used to predict individual student outcomes in this project.

### 3.3 Group-wise Comparison
| Group | Mean average_score | Std. dev. | n |
|---|---|---|---|
| Test prep — completed | 53.63 | 10.31 | 180 |
| Test prep — none | 45.44 | 9.52 | 320 |
| Gender — female | 48.98 | 9.84 | 244 |
| Gender — male | 47.83 | 11.19 | 256 |

A Welch's t-test comparing average scores between students who completed
test preparation and those who did not returned t = 8.76,
p < 0.001 — a statistically significant
difference. The gender difference (0.98-point gap) is small relative to
the within-group standard deviations and is not treated as a meaningful
finding in this report.

A one-way ANOVA comparing average scores across the six parental-education
categories returned F = 0.304,
p 0.911 (η² = 0.0031) —
no statistically significant difference between groups, and the effect
size is negligible.

## 4. Performance Segmentation
Students were grouped into four score-based segments (see
`src_04_segmentation.py` and `data_dictionary.md` for exact thresholds
and methodology):

```
performance_segment  student_count  avg_score  avg_attendance  avg_study_hours  test_prep_completion_rate_pct  share_of_students_pct
            At Risk             51       30.4            75.0              2.1                           11.8                   10.2
    Needs Attention            131       40.3            78.0              3.4                           20.6                   26.2
           Moderate            249       51.6            81.8              4.4                           39.0                   49.8
     High Performer             69       65.5            87.7              5.7                           72.5                   13.8
```

Segment averages increase consistently across attendance, study hours,
and test-preparation completion rate from "At Risk" to "High Performer,"
consistent with the correlation results above.

## 5. Risk Analysis
Students were flagged using project-defined rules combining low score
with low attendance and/or low study hours (see `src_05_risk_analysis.py`
for the exact thresholds and decision logic). This is a descriptive,
rule-based indicator — not a predictive or diagnostic classification.

- High Risk: 20 students
- Medium Risk: 65 students
- Watch: 25 students
- No Risk Indicated: 390 students

## 6. Key Findings
1. Attendance and weekly study hours are both **positively and
   significantly associated** with average score (Pearson r = 0.414
   and r = 0.515 respectively).
2. Study hours show a **stronger association** with score than attendance
   does, based on both correlation strength and regression R².
3. Students who completed test preparation scored significantly higher
   on average (53.63 vs.
   45.44, p < 0.001).
4. Parental education shows **no statistically significant association**
   with average score (one-way ANOVA, p 0.911, η² = 0.0031).
   The gender difference is small relative to within-group variation and
   is not treated as a meaningful finding.
5. Segmentation and risk analysis together identify a
   concentrated subgroup (20 students, "High Risk") combining low
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
