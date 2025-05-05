FROM python:3.11-slim # версия python

WORKDIR /app # рабочая директория

COPY requirements.txt . # копирование зависимостей в корневую директорию

COPY . . # копирование всех данных из одной директории в другую

RUN pip install --no-cache-dir -r requirements.txt # запуск установки зависимостей

EXPOSE 8000 # использование восмитысячного порта

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"] # запуск миграций и сервера