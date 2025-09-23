from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import MyPagination
from materials.serializers import (CourseSerializer, LessonSerializer,
                                   SubscriptionSerializer)
from users.permissions import IsModerator, IsOwner


# Будет использоваться ViewSet
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MyPagination

    def perform_create(self, serializer):
        """Создание курса и сохранение владельца в поле owner"""
        course = serializer.save()
        course.owner = self.request.user  # сохранение владельца курса в поле owner
        course.save()

    def get_permissions(self):
        if self.action == "create":
            # если создание объекта, то разрешаем всем аутентифицированным пользователям, кроме модераторов
            self.permission_classes = [IsAuthenticated & ~IsModerator]
        elif self.action == "list":
            # если просмотр списка объектов, то разрешаем всем
            self.permission_classes = [AllowAny]
        elif self.action in ["update", "partial_update", "retrieve"]:
            # если изменение, просмотр деталей объекта, то разрешаем модераторам или владельцу
            self.permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]
        elif self.action == "destroy":
            # если удаление объекта, то разрешаем только владельцу объекта
            self.permission_classes = [IsAuthenticated & IsOwner]
        else:
            # Для остальных действий используем глобальные разрешения
            self.permission_classes = [IsAuthenticated]

        return [
            permission() for permission in self.permission_classes
        ]  # возвращаем разрешения в виде списка объектов


# Будет использоваться GenericAPIView
class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated & ~IsModerator
    ]  # разрешение всем аутентифицированным пользователям, кроме модераторов

    def perform_create(self, serializer):
        """Создание урока и сохранение владельца в поле owner"""
        lesson = serializer.save()
        lesson.owner = self.request.user  # сохранение владельца урока в поле owner
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    pagination_class = MyPagination


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsOwner]


class SubscriptionAPIView(APIView):
    """APIView для управления подпиской пользователя на курс"""

    def post(self, request, *args, **kwargs):
        """Переопределение метода POST для создания или удаления подписки"""
        user = request.user  # Получаем текущего пользователя
        course_id = request.data.get("course_id")  # Получаем ID курса из запроса

        # Проверяем обязательный параметр course_id
        if not course_id:
            return Response(
                {"error": "Параметр course_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course_item = get_object_or_404(Course, id=course_id)  # Получаем курс по ID

        # Проверяем и управляем подпиской
        subscription, created = Subscription.objects.get_or_create(
            user=user,
            course=course_item
        )

        if not created:
            # Если подписка существовала - удаляем
            subscription.delete()
            return Response(
                {
                    "message": f'Подписка на курс "{course_item.name}" удалена',
                    "subscribed": False
                },
                status=status.HTTP_200_OK
            )
        else:
            # Если подписка была создана - возвращаем через сериализатор
            serializer = SubscriptionSerializer(subscription)
            return Response(
                {
                    "message": f'Подписка на курс "{course_item.name}" добавлена',
                    "subscribed": True,
                    "subscription": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
