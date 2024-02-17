from faker import Faker
from faker.providers import person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Student, Teacher, Subject, Grade
from datetime import datetime
import random

# Ініціалізація Faker для генерації випадкових даних
fake = Faker()
fake.add_provider(person)

# Підключення до бази даних
engine = create_engine('sqlite:///study.db')
Session = sessionmaker(bind=engine)
session = Session()

# Створення таблиць у базі даних, якщо вони ще не існують
Base.metadata.create_all(engine)

# Генерація груп
group_names = ["Group A", "Group B", "Group C"]
groups = [Group(name=name) for name in group_names]
session.add_all(groups)
session.commit()

# Генерація викладачів
teacher_names = [fake.name() for _ in range(random.randint(3, 5))]
teachers = [Teacher(name=name) for name in teacher_names]
session.add_all(teachers)
session.commit()

# Генерація предметів
subject_names = ["Mathematics", "Physics", "Chemistry", "Biology", "History", "Literature", "Geography", "Computer Science"]
subjects = [Subject(name=name, teacher=random.choice(teachers)) for name in subject_names]
session.add_all(subjects)
session.commit()

# Генерація студентів
students = []
for _ in range(random.randint(30, 50)):
    student = Student(name=fake.name(), group=random.choice(groups))
    students.append(student)
session.add_all(students)
session.commit()

# Генерація оцінок для студентів
for student in students:
    for subject in subjects:
        for _ in range(random.randint(5, 20)):
            grade = Grade(
                value=random.randint(60, 100),
                date=fake.date_time_between(start_date='-1y', end_date='now'),
                student=student,
                subject=subject
            )
            session.add(grade)
session.commit()

# Закриття сесії
session.close()
