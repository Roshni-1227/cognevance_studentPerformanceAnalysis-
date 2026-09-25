-- =============================================================================
-- 02_performance_analysis.sql
-- Relationships between performance and attendance, study hours, gender,
-- test preparation, and performance segments.
--
-- Target tables: student_performance, student_data_segmented
-- (student_data_segmented additionally has the performance_segment column
-- produced by src_04_segmentation.py)
-- =============================================================================

-- 1. Average score by attendance band
SELECT
    attendance_band,
    COUNT(*)                     AS student_count,
    ROUND(AVG(average_score), 2) AS avg_score,
    ROUND(AVG(attendance_percentage), 2) AS avg_attendance_pct
FROM student_performance
GROUP BY attendance_band
ORDER BY avg_score DESC;

-- 2. Average score by study-hours bracket
SELECT
    CASE
        WHEN study_hours_per_week < 3  THEN '0-3 hrs'
        WHEN study_hours_per_week < 6  THEN '3-6 hrs'
        ELSE '6+ hrs'
    END                            AS study_hours_bracket,
    COUNT(*)                       AS student_count,
    ROUND(AVG(average_score), 2)   AS avg_score
FROM student_performance
GROUP BY study_hours_bracket
ORDER BY avg_score DESC;

-- 3. Average score by gender
SELECT
    gender,
    COUNT(*)                     AS student_count,
    ROUND(AVG(average_score), 2) AS avg_score,
    ROUND(STDDEV(average_score), 2) AS stddev_score
FROM student_performance
GROUP BY gender;

-- 4. Average score by test-preparation status
SELECT
    test_preparation,
    COUNT(*)                     AS student_count,
    ROUND(AVG(average_score), 2) AS avg_score
FROM student_performance
GROUP BY test_preparation
ORDER BY avg_score DESC;

-- 5. Average score by parental education level
SELECT
    parental_education,
    COUNT(*)                     AS student_count,
    ROUND(AVG(average_score), 2) AS avg_score
FROM student_performance
GROUP BY parental_education
ORDER BY avg_score DESC;

-- 6. Performance segment summary (requires student_data_segmented)
SELECT
    performance_segment,
    COUNT(*)                              AS student_count,
    ROUND(AVG(average_score), 2)          AS avg_score,
    ROUND(AVG(attendance_percentage), 2)  AS avg_attendance_pct,
    ROUND(AVG(study_hours_per_week), 2)   AS avg_study_hours
FROM student_data_segmented
GROUP BY performance_segment
ORDER BY avg_score DESC;

-- 7. Cross-tab: performance segment by test-preparation status
SELECT
    performance_segment,
    test_preparation,
    COUNT(*) AS student_count
FROM student_data_segmented
GROUP BY performance_segment, test_preparation
ORDER BY performance_segment, test_preparation;

-- 8. Combined view: attendance AND study hours together against score
--    (simple two-way grouping, no aggregation function beyond AVG/COUNT)
SELECT
    attendance_band,
    CASE
        WHEN study_hours_per_week < 3 THEN 'Low study hours'
        ELSE 'Adequate study hours'
    END                             AS study_hours_group,
    COUNT(*)                        AS student_count,
    ROUND(AVG(average_score), 2)    AS avg_score
FROM student_performance
GROUP BY attendance_band, study_hours_group
ORDER BY attendance_band, study_hours_group;
