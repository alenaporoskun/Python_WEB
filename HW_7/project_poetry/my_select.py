from sqlalchemy import func
from connect_db import session
from models import Student, Group, Subject, Teacher, Grade

def select_1():
    # Знайти 5 студентів із найвищим середнім балом по всіх предметах
    top_students = session.query(Student).\
        join(Grade, Student.id == Grade.student_id).\
        group_by(Student.id).\
        order_by(func.avg(Grade.value).desc()).\
        limit(5).all()
    return top_students

def select_2(subject_name):
    # Знайти студента з найвищим середнім балом з певного предмета
    top_student = session.query(Student).\
        join(Grade, Student.id == Grade.student_id).\
        join(Subject, Grade.subject_id == Subject.id).\
        filter(Subject.name == subject_name).\
        group_by(Student.id).\
        order_by(func.avg(Grade.value).desc()).\
        first()
    return top_student

def select_3(subject_name):
    # Знайти середній бал у групах з певного предмету
    avg_score_by_group = session.query(Group.name, func.avg(Grade.value)).\
        join(Student, Student.group_id == Group.id).\
        join(Grade, Student.id == Grade.student_id).\
        join(Subject, Grade.subject_id == Subject.id).\
        filter(Subject.name == subject_name).\
        group_by(Group.id).all()
    return avg_score_by_group

def select_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок)
    avg_score_overall = session.query(func.avg(Grade.value)).scalar()
    return avg_score_overall

def select_5(teacher_name):
    # Знайти курси, що читає певний викладач
    courses_taught = session.query(Subject.name).\
        join(Teacher, Subject.teacher_id == Teacher.id).\
        filter(Teacher.name == teacher_name).all()
    return courses_taught

def select_6(group_name):
    # Знайти список студентів у певній групі
    students_in_group = session.query(Student).\
        join(Group, Student.group_id == Group.id).\
        filter(Group.name == group_name).all()
    return students_in_group

def select_7(group_name, subject_name):
    # Знайти оцінки студентів у окремій групі з певного предмету
    scores_in_group = session.query(Student.name, Grade.value).\
        join(Group, Student.group_id == Group.id).\
        join(Grade, Student.id == Grade.student_id).\
        join(Subject, Grade.subject_id == Subject.id).\
        filter(Group.name == group_name, Subject.name == subject_name).all()
    return scores_in_group

def select_8(teacher_name):
    # Знайти середній бал, який ставить певний викладач зі своїх предметів
    avg_score_by_teacher = session.query(func.avg(Grade.value)).\
        join(Subject, Grade.subject_id == Subject.id).\
        join(Teacher, Subject.teacher_id == Teacher.id).\
        filter(Teacher.name == teacher_name).scalar()
    return avg_score_by_teacher

def select_9(student_name):
    # Знайти список унікальних курсів, які відвідує певний студент
    courses_attended = session.query(Subject.name).\
        join(Grade, Subject.id == Grade.subject_id).\
        join(Student, Grade.student_id == Student.id).\
        filter(Student.name == student_name).\
        distinct().all()
    return courses_attended

def select_10(student_name, teacher_name):
    # Знайти список унікальних курсів, які певний студент відвідує, читані певним викладачем
    courses_taught_to_student = session.query(Subject.name).\
        join(Teacher, Subject.teacher_id == Teacher.id).\
        join(Grade, Subject.id == Grade.subject_id).\
        join(Student, Grade.student_id == Student.id).\
        filter(Student.name == student_name, Teacher.name == teacher_name).\
        distinct().all()
    return courses_taught_to_student
