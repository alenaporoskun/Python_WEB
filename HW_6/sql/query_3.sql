-- query_3.sql Знайти середній бал у групах з певного предмета.

SELECT g.name_group, AVG(s.score) AS avg_score
FROM groups g
JOIN students stu ON g.id = stu.group_id
JOIN scores s ON stu.id = s.student_id
WHERE s.subject_id = 6
GROUP BY g.name_group;
