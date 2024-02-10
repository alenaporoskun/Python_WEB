-- query_9.sql Знайти список курсів, які відвідує студент.

SELECT DISTINCT sub.subject_name
FROM subjects sub
JOIN scores s ON sub.id = s.subject_id
JOIN students stu ON s.student_id = stu.id
WHERE stu.student_name = 'Wanda Jenkins';
