# Student Performance Analysis — Project Report

**Author:** Roshni Kumari
**Program:** Cognevance Technologies — Data Science & Data Analytics (Level 1)

## 1. Objective
Analyze student academic performance data to identify the factors most
strongly associated with higher scores.

## 2. Dataset
- **Records analyzed:** 500 students (after cleaning)
- **Fields:** demographics, parental education, lunch type, test
  preparation status, attendance %, weekly study hours, and scores in
  math, reading, and writing.
- **Data quality steps applied:** removed duplicate records, imputed
  missing numeric values with the column median, clipped out-of-range
  values, and standardized categorical text formatting.

## 3. Key Findings

| Metric                                      | Value |
|-----------------------------------------------|-------|
| Overall average score                          | 48.4 |
| Correlation: attendance % ↔ average score        | 0.414 |
| Correlation: weekly study hours ↔ average score  | 0.515 |
| Pass rate (grade above F)                      | 78.0% |

**By attendance band (average score):**
- Average (60-74%): 43.7
- Excellent (90-100%): 55.3
- Good (75-89%): 48.7
- Low (<60%): 38.5

**By test preparation status (average score):**
- completed: 53.6
- none: 45.4

**By gender (average score):**
- female: 49.0
- male: 47.8

**Grade distribution:**
- Grade B: 4 students
- Grade C: 66 students
- Grade D: 320 students
- Grade F: 110 students

## 4. Conclusions
1. **Attendance matters.** Students in the "Excellent" attendance band
   (90–100%) score noticeably higher on average than those in the "Low"
   band, and the correlation between attendance and average score is
   moderate (0.414).
2. **Study hours are the strongest driver** of average score among the
   variables tested (correlation 0.515),
   ahead of attendance.
3. **Test preparation has a measurable effect** — students who completed
   a test-prep course averaged
   8.2
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
