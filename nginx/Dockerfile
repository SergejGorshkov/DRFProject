# Используем официальный образ Nginx
FROM nginx:latest

# Создание директории для статических файлов приложения
RUN mkdir -p /app/static

# Копирование файла конфигурации Nginx в контейнер
COPY nginx.conf /etc/nginx/nginx.conf

# Открытие порта 80 для HTTP-трафика
EXPOSE 80
