-- query_11.sql Середній бал, який певний викладач ставить певному студентові.

SELECT AVG(score) AS avg_score
FROM scores
WHERE student_id = 1 AND subject_id IN (
    SELECT id
    FROM subjects
    WHERE teacher_id = 2
);
