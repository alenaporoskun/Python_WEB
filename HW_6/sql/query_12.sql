-- query_12.sql Оцінки студентів у певній групі з певного предмета на останньому занятті.

SELECT students.student_name, scores.score
FROM students
JOIN scores ON students.id = scores.student_id
JOIN subjects ON scores.subject_id = subjects.id
WHERE students.group_id = 2 AND subjects.id = 6
ORDER BY scores.time_score DESC
LIMIT 1;

