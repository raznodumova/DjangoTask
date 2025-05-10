# Версия python
FROM python:3.11-slim

# Установка Poetry
RUN pip install --no-cache-dir poetry==1.7.0

WORKDIR /app

# Копируем ТОЛЬКО файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копируем весь проект
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]