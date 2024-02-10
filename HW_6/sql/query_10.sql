-- query_10.sql Список курсів, які певному студенту читає певний викладач.

SELECT DISTINCT sub.subject_name
FROM subjects sub
JOIN scores s ON sub.id = s.subject_id
JOIN students stu ON s.student_id = stu.id
JOIN teachers t ON sub.teacher_id = t.id
WHERE stu.student_name = 'Wanda Jenkins' AND t.name_teacher = 'Jenna Bennett';
