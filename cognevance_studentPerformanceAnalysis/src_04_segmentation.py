"""
src_04_segmentation.py
------------------------
Segments students into four score-based performance categories and
produces per-segment summary statistics.

Segmentation is based solely on `average_score` and is a descriptive
grouping for reporting purposes — it is not a predictive or diagnostic
classification.

Category thresholds (average_score, 0-100 scale):
    At Risk           : score <  35
    Needs Attention    : 35 <= score <  45
    Moderate           : 45 <= score <  60
    High Performer     : score >= 60

These cut points were set using the dataset's own score distribution
(10th percentile ≈ 35, 25th percentile ≈ 41, 75th percentile ≈ 55) so that
each category represents a meaningfully distinct part of the distribution
rather than an arbitrary split.
"""

import pandas as pd

CLEAN_PATH = "data/student_data_clean.csv"
OUTPUT_PATH = "data/student_data_segmented.csv"
SUMMARY_PATH = "data/segment_summary.csv"

SEGMENT_BINS = [-1, 35, 45, 60, 200]
SEGMENT_LABELS = ["At Risk", "Needs Attention", "Moderate", "High Performer"]
SEGMENT_ORDER = SEGMENT_LABELS  # display / sort order, worst to best


def load() -> pd.DataFrame:
    return pd.read_csv(CLEAN_PATH)


def segment(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["performance_segment"] = pd.cut(
        df["average_score"], bins=SEGMENT_BINS, labels=SEGMENT_LABELS
    )
    df["performance_segment"] = pd.Categorical(
        df["performance_segment"], categories=SEGMENT_ORDER, ordered=True
    )
    return df


def segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("performance_segment", observed=True)
        .agg(
            student_count=("student_id", "count"),
            avg_score=("average_score", "mean"),
            avg_attendance=("attendance_percentage", "mean"),
            avg_study_hours=("study_hours_per_week", "mean"),
            test_prep_completion_rate_pct=(
                "test_preparation", lambda s: (s == "completed").mean() * 100
            ),
        )
        .round(1)
        .reindex(SEGMENT_ORDER)
        .reset_index()
    )
    summary["share_of_students_pct"] = (
        summary["student_count"] / summary["student_count"].sum() * 100
    ).round(1)
    return summary


if __name__ == "__main__":
    df = load()
    segmented = segment(df)
    summary = segment_summary(segmented)

    print("=== Performance Segment Summary ===")
    print(summary.to_string(index=False))

    segmented.to_csv(OUTPUT_PATH, index=False)
    summary.to_csv(SUMMARY_PATH, index=False)
    print(f"\nSaved segmented dataset -> {OUTPUT_PATH}")
    print(f"Saved segment summary -> {SUMMARY_PATH}")
