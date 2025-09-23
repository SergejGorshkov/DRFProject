import re

from rest_framework import serializers


class LessonVideoUrlValidator:
    """Валидатор для проверки ссылки на видео урока"""

    def __call__(self, attrs):
        video_url = attrs.get("video")

        if not video_url:  # Если поле пустое - пропускаем
            return

        youtube_regex = r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+"

        if not re.match(youtube_regex, video_url):
            raise serializers.ValidationError("Урок должен быть ссылкой на YouTube")
