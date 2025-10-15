# Используем официальный slim-образ Python 3.12
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY requirements.txt ./

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Создаем директории для медиафайлов и статики и назначаем права доступа
RUN mkdir -p /app/static /app/media
RUN chown -R www-data:www-data /app/static /app/media
RUN chmod -R 755 /app/static /app/media

# Открываем порт 8000 для взаимодействия с приложением Django
EXPOSE 8000

# Определяем команду для запуска приложения (для production)
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
