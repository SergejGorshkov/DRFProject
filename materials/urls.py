from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateApiView,
                             LessonDestroyApiView, LessonListApiView,
                             LessonRetrieveApiView, LessonUpdateApiView,
                             SubscriptionAPIView)

app_name = (
    MaterialsConfig.name
)  # Извлечение имени приложения из модуля materials/apps.py

router = SimpleRouter()  # Создание экземпляра SimpleRouter для регистрации ViewSet
router.register("course", CourseViewSet, basename="courses")

urlpatterns = [
    path("lesson/", LessonListApiView.as_view(), name="lessons_list"),
    path("lesson/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson_retrieve"),
    path("lesson/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path(
        "lesson/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lesson_delete"
    ),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
] + router.urls  # Добавление URL для ViewSet
