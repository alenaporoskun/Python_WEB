# Використовуємо базовий образ Python
FROM python:3.10

# Переміщаємося до каталогу з проектом
WORKDIR /app

# Копіюємо файли проекту в контейнер
COPY . /app

# Встановлюємо залежності
RUN pip install -r /app/console_assistant/requirements.txt

# Вказуємо команду, яка виконається при запуску контейнера
CMD ["python", "/app/console_assistant/main.py"]