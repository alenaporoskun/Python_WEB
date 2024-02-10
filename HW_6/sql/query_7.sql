-- query_7.sql Знайти оцінки студентів у окремій групі з певного предмета.

SELECT s.score
FROM students stu
JOIN scores s ON stu.id = s.student_id
WHERE stu.group_id = 1 AND s.subject_id = 6;
