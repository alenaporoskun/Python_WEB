-- query_8.sql Знайти середній бал, який ставить певний викладач зі своїх предметів.

SELECT AVG(s.score) AS avg_score
FROM subjects sub
JOIN scores s ON sub.id = s.subject_id
JOIN teachers t ON sub.teacher_id = t.id
WHERE t.name_teacher = 'Jenna Bennett';
