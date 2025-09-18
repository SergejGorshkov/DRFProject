from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson

class LessonSerializer(ModelSerializer):
    """ Сериализатор для урока """

    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(ModelSerializer):
    """ Сериализатор для курса """
    lessons_count = SerializerMethodField()  # Поле для количества уроков
    lessons_in_course = LessonSerializer(source='lessons', many=True, read_only=True) # Поле для уроков в курсе

    def get_lessons_count(self, course):
        """ Подсчет количества уроков в курсе """
        return Lesson.objects.filter(course=course).count()


    class Meta:
        model = Course
        fields = ("id", "name", "description", "lessons_count", "lessons_in_course",)

