-- =============================================================================
-- 03_business_questions.sql
-- Queries that directly answer this project's core business questions and
-- identify students or groups that may warrant academic attention.
--
-- Target tables: student_performance, student_data_segmented, risk_analysis
-- =============================================================================

-- Q1. Is attendance associated with academic performance?
--     (Descriptive evidence only — see report for the correlation coefficient.)
SELECT
    attendance_band,
    COUNT(*)                     AS student_count,
    ROUND(AVG(average_score), 2) AS avg_score
FROM student_performance
GROUP BY attendance_band
ORDER BY avg_score DESC;

-- Q2. Is weekly study time associated with academic performance?
SELECT
    CASE
        WHEN study_hours_per_week < 3  THEN '0-3 hrs/week'
        WHEN study_hours_per_week < 6  THEN '3-6 hrs/week'
        ELSE '6+ hrs/week'
    END                            AS study_hours_bracket,
    COUNT(*)                       AS student_count,
    ROUND(AVG(average_score), 2)   AS avg_score
FROM student_performance
GROUP BY study_hours_bracket
ORDER BY avg_score DESC;

-- Q3. Does completing test preparation relate to higher scores?
SELECT
    test_preparation,
    COUNT(*)                     AS student_count,
    ROUND(AVG(average_score), 2) AS avg_score
FROM student_performance
GROUP BY test_preparation;

-- Q4. How many students fall into each performance segment?
SELECT
    performance_segment,
    COUNT(*) AS student_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM student_data_segmented), 1) AS pct_of_students
FROM student_data_segmented
GROUP BY performance_segment
ORDER BY student_count DESC;

-- Q5. Which students are flagged as High Risk or Medium Risk?
--     (Project-defined indicators — see risk_analysis for full methodology.)
SELECT
    student_id,
    average_score,
    attendance_percentage,
    study_hours_per_week,
    risk_level
FROM risk_analysis
WHERE risk_level IN ('High Risk', 'Medium Risk')
ORDER BY risk_level, average_score ASC;

-- Q6. How many students are at each risk level, and what do they look like on average?
SELECT
    risk_level,
    COUNT(*)                              AS student_count,
    ROUND(AVG(average_score), 2)          AS avg_score,
    ROUND(AVG(attendance_percentage), 2)  AS avg_attendance_pct,
    ROUND(AVG(study_hours_per_week), 2)   AS avg_study_hours
FROM risk_analysis
GROUP BY risk_level
ORDER BY avg_score ASC;

-- Q7. Within the "Needs Attention" and "At Risk" segments, how many have
--     also NOT completed test preparation? (a candidate group for outreach)
SELECT
    performance_segment,
    COUNT(*) AS student_count
FROM student_data_segmented
WHERE performance_segment IN ('At Risk', 'Needs Attention')
  AND test_preparation = 'none'
GROUP BY performance_segment;

-- Q8. Top 10 lowest-scoring students with their contributing attendance and
--     study-hour figures, for manual review.
SELECT
    student_id,
    average_score,
    attendance_percentage,
    study_hours_per_week,
    test_preparation
FROM student_performance
ORDER BY average_score ASC
LIMIT 10;
