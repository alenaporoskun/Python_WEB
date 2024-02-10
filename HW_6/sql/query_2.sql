-- query_2.sql Знайти студента із найвищим середнім балом з певного предмета.

SELECT student_id, AVG(score) AS avg_score
FROM scores
WHERE subject_id = 6
GROUP BY student_id
ORDER BY avg_score DESC
LIMIT 1;
