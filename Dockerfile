FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменные окружения
ENV FLASK_APP_PORT=5001

# Открываем порт
EXPOSE $FLASK_APP_PORT

# Команда для запуска Flask приложения
CMD ["python", "app.py"]
