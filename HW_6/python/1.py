import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# З'єднання з базою даних
conn = sqlite3.connect('database/study.db')
cursor = conn.cursor()

# Запит для вибору перших п'яти рядків з кожної таблиці
tables = ['groups', 'students', 'teachers', 'subjects', 'scores']
for table in tables:
    print(f"Перші 6 рядків з таблиці '{table}':")
    cursor.execute(f"SELECT * FROM {table} LIMIT 6")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()

# Закриття підключення до бази даних
conn.close()
