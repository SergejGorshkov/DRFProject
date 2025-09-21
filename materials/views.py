from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated, AllowAny


# Будет использоваться ViewSet
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        """ Создание курса и сохранение владельца в поле owner """
        course = serializer.save()
        course.owner = self.request.user # сохранение владельца курса в поле owner
        course.save()


    def get_permissions(self):
        if self.action == 'create':
            # если создание объекта, то разрешаем всем аутентифицированным пользователям, кроме модераторов
            self.permission_classes = [IsAuthenticated & ~IsModerator]
        elif self.action == 'list':
            # если просмотр списка объектов, то разрешаем всем
            self.permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            # если изменение, просмотр деталей объекта, то разрешаем модераторам или владельцу
            self.permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]
        elif self.action == 'destroy':
            # если удаление объекта, то разрешаем только владельцу объекта
            self.permission_classes = [IsAuthenticated & IsOwner]
        else:
            # Для остальных действий используем глобальные разрешения
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes] # возвращаем разрешения в виде списка объектов


# Будет использоваться GenericAPIView
class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & ~IsModerator] # разрешение всем аутентифицированным пользователям, кроме модераторов


    def perform_create(self, serializer):
        """ Создание урока и сохранение владельца в поле owner """
        lesson = serializer.save()
        lesson.owner = self.request.user # сохранение владельца урока в поле owner
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]


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
