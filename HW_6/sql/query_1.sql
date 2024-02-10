-- query_1.sql Знайти 5 студентів із найбільшим середнім балом з усіх предметів.

SELECT students.student_name, AVG(scores.score) AS average_score
FROM students
JOIN scores ON students.id = scores.student_id
GROUP BY students.student_name
ORDER BY average_score DESC
LIMIT 5;
