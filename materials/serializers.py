from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import LessonVideoUrlValidator


class LessonSerializer(ModelSerializer):
    """Сериализатор для урока"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LessonVideoUrlValidator()]  # Валидатор для видео урока


class CourseSerializer(ModelSerializer):
    """Сериализатор для курса"""

    lessons_count = SerializerMethodField()  # Поле для количества уроков
    lessons_in_course = LessonSerializer(
        source="lessons", many=True, read_only=True
    )  # Поле для уроков в курсе
    is_subscribed = SerializerMethodField()  # Поле для проверки подписки на курс

    def get_lessons_count(self, course):
        """Подсчет количества уроков в курсе"""
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        """Проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get(
            "request"
        )  # Получаем объект запроса из контекста сериализатора

        # Если пользователь авторизован и есть запрос, проверяем, есть ли запись в подписках
        # для текущего пользователя и курса
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, course=course
            ).exists()
        return False

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "lessons_count",
            "lessons_in_course",
            "is_subscribed",
        )


class SubscriptionSerializer(ModelSerializer):
    """Сериализатор для подписки на курс"""

    class Meta:
        model = Subscription
        fields = ["id", "user", "course", "subscribed_at"]  # Поля для сериализации
        read_only_fields = [
            "id",
            "subscribed_at",
            "user",
        ]  # Поля, которые нельзя изменять
