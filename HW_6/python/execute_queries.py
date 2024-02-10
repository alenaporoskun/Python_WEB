import sqlite3
import os

# Відкриття підключення до бази даних
conn = sqlite3.connect('database/study.db')
cursor = conn.cursor()

# Шлях до папки з файлами SQL
sql_folder = 'sql'

# Цикл для виконання запитів з кожного файлу SQL
for i in range(1, 13):
    filename = os.path.join(sql_folder, f'query_{i}.sql')  # Формування шляху до файлу запиту
    print(f'Виконання запиту з файлу {filename}:')

    with open(filename, 'r') as file:
        sql_query = file.read()  # Зчитування SQL-запиту з файлу
        cursor.execute(sql_query)  # Виконання SQL-запиту
        results = cursor.fetchall()  # Отримання результатів запиту

    # Виведення результатів на екран
    for row in results:
        print(row)

    print()  # Друк порожнього рядка для відділення результатів від різних запитів

# Закриття підключення
conn.close()

print("Запити виконано.")
