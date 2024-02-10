import sqlite3

def create_db():
    # Відкриваємо файл create_tables.sql для читання
    with open('sql/study.sql', 'r') as f:
        # Читаємо SQL запити з файлу
        sql = f.read()

    # Встановлюємо з'єднання з базою даних study.db
    with sqlite3.connect('database/study.db') as con:
        # Створюємо курсор для виконання SQL запитів
        cur = con.cursor()
        # Виконуємо SQL скрипт для створення таблиць
        cur.executescript(sql)

# Викликаємо функцію create_db, якщо файл виконується напряму (не імпортується)
if __name__ == "__main__":
    create_db()
