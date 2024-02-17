import sys
from my_select import select_1, select_2, select_3, select_4, select_5, select_6, select_7, select_8, select_9, select_10
from models import Student, Subject, Teacher
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import random

# Підключення до бази даних
engine = create_engine('sqlite:///study.db')
Session = sessionmaker(bind=engine)
session = Session()

# Встановлюємо з'єднання з файлом для запису
with open('results.txt', 'w', encoding='utf-8') as file:
    # Використовуємо stdout для перенаправлення виводу
    original_stdout = sys.stdout
    sys.stdout = file

    # Виклик функцій select_1 до select_10 з використанням даних із бази даних

    # Функція select_1: Топ 5 студентів з найвищим середнім балом у всіх предметах
    top_students = select_1()
    print("Топ 5 студентів з найвищим середнім балом у всіх предметах:")
    for student in top_students:
        print(f"ID студента: {student.id}, Ім'я: {student.name}")

    # Функція select_2: Знайти студента з найвищим середнім балом з певного предмета
    subject_name = random.choice([subject.name for subject in session.query(Subject).all()])
    top_student_math = select_2(subject_name)
    if top_student_math:
        print(f"\nНайкращий студент з {subject_name}: {top_student_math.name}")

    # Функція select_3: Знайти середній бал у групах з певного предмету
    avg_scores_by_group_math = select_3(subject_name)
    print("\nСередній бал у групах з математики:")
    for group, avg_score in avg_scores_by_group_math:
        print(f"Група: {group}, Середній бал: {avg_score}")

    # Функція select_4: Знайти середній бал на потоці (по всій таблиці оцінок)
    avg_score_overall = select_4()
    print(f"\nЗагальний середній бал: {avg_score_overall}")

    # Функція select_5: Знайти курси, що читає певний викладач
    teacher_name = random.choice([teacher.name for teacher in session.query(Teacher).all()])
    courses_taught_by_john = select_5(teacher_name)
    print(f"\nКурси, які веде {teacher_name}:")
    for course in courses_taught_by_john:
        print(course)

    # Функція select_6: Знайти список студентів у певній групі
    group_name = random.choice(["Group A", "Group B", "Group C"])
    students_in_group_1 = select_6(group_name)
    print(f"\nСтуденти в {group_name}:")
    for student in students_in_group_1:
        print(f"ID студента: {student.id}, Ім'я: {student.name}")

    # Функція select_7: Знайти оцінки студентів у окремій групі з певного предмету
    scores_in_group_1_math = select_7(group_name, subject_name)
    print(f"\nОцінки студентів у {group_name} з {subject_name}:")
    for student, score in scores_in_group_1_math:
        print(f"Студент: {student}, Оцінка: {score}")

    # Функція select_8: Знайти середній бал, який ставить певний викладач зі своїх предметів
    avg_score_by_john = select_8(teacher_name)
    print(f"\nСередній бал, який ставить {teacher_name}: {avg_score_by_john}")

    # Функція select_9: Знайти список курсів, які відвідує певний студент
    student_name = random.choice([student.name for student in session.query(Student).all()])
    courses_attended_by_student = select_9(student_name)
    print(f"\nКурси, які відвідує {student_name}:")
    for course in courses_attended_by_student:
        print(course)

    # Функція select_10: Знайти список курсів, які певний студент відвідує, читані певним викладачем
    courses_taught_to_alice_by_john = select_10(student_name, teacher_name)
    print(f"\nКурси, які веде {teacher_name} і відвідує {student_name}:")
    for course in courses_taught_to_alice_by_john:
        print(course)

    # Відновлюємо оригінальний вивід
    sys.stdout = original_stdout

# Закриття сесії
session.close()
