# Data Dictionary

This document describes every column produced across the project's data
pipeline: the raw dataset, the cleaned dataset, and the two derived outputs
(segmentation and risk analysis).

## 1. Raw / Cleaned Dataset — `data/student_data.csv`, `data/student_data_clean.csv`

| Column | Type | Origin | Expected Range / Values | Description |
|---|---|---|---|---|
| `student_id` | string | Original | `S1000`–`S1499` | Unique student identifier |
| `gender` | categorical (string) | Original | `male`, `female` | Student gender |
| `parental_education` | categorical (string) | Original | `some high school`, `high school`, `some college`, `associate's degree`, `bachelor's degree`, `master's degree` | Highest education level attained by a parent/guardian |
| `lunch` | categorical (string) | Original | `standard`, `free/reduced` | Lunch program type, a common proxy for household income |
| `test_preparation` | categorical (string) | Original | `none`, `completed` | Whether the student completed a test-preparation course |
| `attendance_percentage` | float | Original | 0–100 | Attendance rate over the analyzed period |
| `study_hours_per_week` | float | Original | 0–24 (observed 0–9.5) | Self-reported weekly study hours |
| `math_score` | float | Original | 0–100 | Math exam score |
| `reading_score` | float | Original | 0–100 | Reading exam score |
| `writing_score` | float | Original | 0–100 | Writing exam score |
| `average_score` | float | **Engineered** | 0–100 | Mean of `math_score`, `reading_score`, `writing_score` |
| `grade` | categorical (string) | **Engineered** | `A`, `B`, `C`, `D`, `F` | Letter grade derived from `average_score` (A ≥ 90, B ≥ 75, C ≥ 60, D ≥ 40, F < 40) |
| `attendance_band` | categorical (string) | **Engineered** | `Low (<60%)`, `Average (60-74%)`, `Good (75-89%)`, `Excellent (90-100%)` | Attendance bucketed into four bands |

**Cleaning applied to raw → clean:** duplicate rows and duplicate `student_id` values removed; missing numeric values imputed with the column median; scores and attendance clipped to a valid 0–100 range; categorical text lower-cased and stripped.

## 2. Segmented Dataset — `data/student_data_segmented.csv`

All columns from the cleaned dataset, plus:

| Column | Type | Origin | Expected Range / Values | Description |
|---|---|---|---|---|
| `performance_segment` | categorical (string), ordered | **Engineered** | `At Risk`, `Needs Attention`, `Moderate`, `High Performer` | Score-based segment; see `src_04_segmentation.py` for exact thresholds |

## 3. Segment Summary — `data/segment_summary.csv`

One row per `performance_segment`, with `student_count`, `avg_score`, `avg_attendance`, `avg_study_hours`, `test_prep_completion_rate_pct`, and `share_of_students_pct` (all **engineered**, aggregated from the segmented dataset).

## 4. Risk Analysis Output — `data/risk_analysis.csv`

| Column | Type | Origin | Expected Range / Values | Description |
|---|---|---|---|---|
| `student_id` | string | Original | — | Unique student identifier |
| `gender` | categorical (string) | Original | `male`, `female` | Student gender |
| `average_score` | float | Engineered (carried over) | 0–100 | Mean subject score |
| `attendance_percentage` | float | Original | 0–100 | Attendance rate |
| `study_hours_per_week` | float | Original | 0–24 | Weekly study hours |
| `test_preparation` | categorical (string) | Original | `none`, `completed` | Test-prep completion status |
| `low_score_flag` | boolean | **Engineered** | `True`/`False` | `average_score` below the project-defined threshold (< 40) |
| `low_attendance_flag` | boolean | **Engineered** | `True`/`False` | `attendance_percentage` below the project-defined threshold (< 75) |
| `low_study_hours_flag` | boolean | **Engineered** | `True`/`False` | `study_hours_per_week` below the project-defined threshold (< 3) |
| `risk_level` | categorical (string), ordered | **Engineered** | `High Risk`, `Medium Risk`, `Watch`, `No Risk Indicated` | Rule-based combination of the three flags above; see `src_05_risk_analysis.py` for the exact decision logic |

**Note:** `risk_level` is a project-defined, rule-based analytical indicator built from fixed thresholds on this dataset. It is not a predictive or diagnostic classification and should not be interpreted as one.
