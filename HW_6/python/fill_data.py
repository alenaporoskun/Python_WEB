import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# З'єднання з базою даних
conn = sqlite3.connect('database/study.db')
cursor = conn.cursor()

# Створення фальшивих даних за допомогою Faker
fake = Faker()

# Створення таблиць, які ви описали

# Функція для заповнення таблиці груп
def populate_groups():
    groups = [('Group A',), ('Group B',), ('Group C',)]
    cursor.executemany('INSERT INTO groups (name_group) VALUES (?)', groups)
    conn.commit()

# Функція для заповнення таблиці студентів
def populate_students():
    students = [(fake.name(), random.randint(1, 3)) for _ in range(30)]
    cursor.executemany('INSERT INTO students (student_name, group_id) VALUES (?, ?)', students)
    conn.commit()

# Функція для заповнення таблиці викладачів
def populate_teachers():
    teachers = [(fake.name(),) for _ in range(5)]
    cursor.executemany('INSERT INTO teachers (name_teacher) VALUES (?)', teachers)
    conn.commit()

# Функція для заповнення таблиці предметів
def populate_subjects():
    subjects = [(fake.word(), random.randint(1, 5)) for _ in range(8)]
    cursor.executemany('INSERT INTO subjects (subject_name, teacher_id) VALUES (?, ?)', subjects)
    conn.commit()

# Функція для заповнення таблиці оцінок
def populate_scores():
    # Отримуємо список всіх студентів і предметів
    cursor.execute('SELECT id FROM students')
    students = cursor.fetchall()
    cursor.execute('SELECT id FROM subjects')
    subjects = cursor.fetchall()

    # Заповнюємо таблицю оцінок для кожного студента і предмету
    for student in students:
        for subject in subjects:
            # Генеруємо випадкову оцінку та час її отримання
            score = random.randint(60, 100)
            time_score = fake.date_time_between(start_date='-1y', end_date='now')
            cursor.execute('INSERT INTO scores (student_id, subject_id, score, time_score) VALUES (?, ?, ?, ?)',
                           (student[0], subject[0], score, time_score))
    conn.commit()

# Викликаємо функції для заповнення таблиць
populate_groups()
populate_students()
populate_teachers()
populate_subjects()
populate_scores()

# Закриваємо з'єднання з базою даних
conn.close()
