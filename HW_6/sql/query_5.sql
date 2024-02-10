-- query_5.sql Знайти які курси читає певний викладач.

SELECT DISTINCT sub.subject_name
FROM subjects sub
JOIN scores s ON sub.id = s.subject_id
JOIN teachers t ON sub.teacher_id = t.id
WHERE t.name_teacher = 'Jenna Bennett';
