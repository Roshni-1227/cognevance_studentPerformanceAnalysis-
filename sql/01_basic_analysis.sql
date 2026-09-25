-- =============================================================================
-- 01_basic_analysis.sql
-- Basic student-performance KPIs.
--
-- Target table: student_performance
-- Load data/student_data_clean.csv into a table of this name (column names
-- match the CSV headers) before running these queries. Written in standard
-- ANSI SQL and validated by execution against SQLite; expected to be
-- compatible with PostgreSQL and MySQL, though not independently tested
-- against those engines. The STDDEV() calls below are not supported by
-- SQLite and require PostgreSQL/MySQL (or an equivalent function) to run.
-- =============================================================================

-- 1. Total number of students
SELECT COUNT(*) AS total_students
FROM student_performance;

-- 2. Overall average score, attendance, and study hours
SELECT
    ROUND(AVG(average_score), 2)         AS avg_score,
    ROUND(AVG(attendance_percentage), 2) AS avg_attendance_pct,
    ROUND(AVG(study_hours_per_week), 2)  AS avg_study_hours
FROM student_performance;

-- 3. Score statistics: min, max, average, standard deviation
SELECT
    MIN(average_score)                AS min_score,
    MAX(average_score)                AS max_score,
    ROUND(AVG(average_score), 2)      AS mean_score,
    ROUND(STDDEV(average_score), 2)   AS stddev_score   -- MySQL/Postgres: STDDEV(); SQLite has no built-in STDDEV
FROM student_performance;

-- 4. Grade distribution (count and percentage of students per grade)
SELECT
    grade,
    COUNT(*)                                                    AS student_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM student_performance), 1) AS pct_of_students
FROM student_performance
GROUP BY grade
ORDER BY grade;

-- 5. Test-preparation completion rate
SELECT
    test_preparation,
    COUNT(*)                                                    AS student_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM student_performance), 1) AS pct_of_students
FROM student_performance
GROUP BY test_preparation;

-- 6. Attendance band distribution
SELECT
    attendance_band,
    COUNT(*)                          AS student_count,
    ROUND(AVG(average_score), 2)      AS avg_score
FROM student_performance
GROUP BY attendance_band
ORDER BY avg_score DESC;

-- 7. Subject-level score comparison (math vs reading vs writing)
SELECT
    ROUND(AVG(math_score), 2)    AS avg_math,
    ROUND(AVG(reading_score), 2) AS avg_reading,
    ROUND(AVG(writing_score), 2) AS avg_writing
FROM student_performance;
