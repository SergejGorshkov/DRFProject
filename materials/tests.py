from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonCRUDTestCase(APITestCase):
    """Тесты для проверки CRUD операций для Lesson"""

    def setUp(self):
        """Настройка тестовых данных"""

        # Создание группы модераторов
        self.moderators_group, created = Group.objects.get_or_create(name="Moderators")

        # Создание пользователей с разными правами
        self.owner_user = User.objects.create(  # Владелец
            email="owner@test.com", password="testpass123", is_staff=False
        )

        self.moderator_user = User.objects.create(  # Модератор
            email="moderator@test.com", password="testpass123", is_staff=True
        )
        self.moderator_user.groups.add(
            self.moderators_group
        )  # Добавление moderator_user в группу модераторов

        self.other_user = User.objects.create(  # Другой пользователь
            email="other@test.com", password="testpass123", is_staff=False
        )

        # Создание курса
        self.course = Course.objects.create(
            name="Test Course", description="Test Description", owner=self.owner_user
        )

        # Создание урока
        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Test Lesson Description",
            course=self.course,
            owner=self.owner_user,
            video="https://www.youtube.com/test",
        )

        # URL для тестирования
        self.lesson_list_url = reverse("materials:lessons_list")
        self.lesson_detail_url = reverse(
            "materials:lesson_retrieve", kwargs={"pk": self.lesson.pk}
        )
        self.lesson_update_url = reverse(
            "materials:lesson_update", kwargs={"pk": self.lesson.pk}
        )
        self.lesson_delete_url = reverse(
            "materials:lesson_delete", kwargs={"pk": self.lesson.pk}
        )

    # ТЕСТЫ ДЛЯ LessonListApiView (доступ для всех)
    def test_lesson_list_allowed_for_anyone(self):
        """Тест: список уроков доступен всем пользователям"""
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_list_contains_lesson(self):
        """Тест: список содержит созданный урок"""
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Test Lesson")

    # ТЕСТЫ ДЛЯ LessonRetrieveApiView (только модератор или владелец)
    def test_lesson_retrieve_by_owner(self):
        """Тест: владелец может просматривать урок"""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Lesson")

    def test_lesson_retrieve_by_moderator(self):
        """Тест: модератор может просматривать урок"""
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_retrieve_by_other_user_denied(self):
        """Тест: другой пользователь не может просматривать урок"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_retrieve_unauthenticated_denied(self):
        """Тест: неаутентифицированный пользователь не может просматривать урок"""
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ТЕСТЫ ДЛЯ LessonUpdateApiView (только модератор или владелец)
    def test_lesson_update_by_owner(self):
        """Тест: владелец может обновлять урок"""
        self.client.force_authenticate(user=self.owner_user)
        update_data = {"name": "Updated Lesson Name"}
        response = self.client.patch(self.lesson_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Updated Lesson Name")

    def test_lesson_update_by_moderator(self):
        """Тест: модератор может обновлять урок"""
        self.client.force_authenticate(user=self.moderator_user)
        update_data = {"name": "Updated by Moderator"}
        response = self.client.patch(self.lesson_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update_by_other_user_denied(self):
        """Тест: другой пользователь не может обновлять урок"""
        self.client.force_authenticate(user=self.other_user)
        update_data = {"name": "Unauthorized Update"}
        response = self.client.patch(self.lesson_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ТЕСТЫ ДЛЯ LessonDestroyApiView (только владелец)
    def test_lesson_delete_by_owner(self):
        """Тест: владелец может удалять урок"""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())

    def test_lesson_delete_by_moderator_denied(self):
        """Тест: модератор не может удалять урок"""
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Lesson.objects.filter(pk=self.lesson.pk).exists())

    def test_lesson_delete_by_other_user_denied(self):
        """Тест: другой пользователь не может удалять урок"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        """Настройка тестовых данных для подписок"""

        self.user = User.objects.create(email="user@test.com", password="testpass123")

        self.course = Course.objects.create(
            name="Test Course for Subscription",
            description="Test Description",
            owner=self.user,
        )

        self.subscription_url = reverse("materials:subscription")

    def test_subscription_create(self):
        """Тест: создание подписки"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.subscription_url, {"course_id": self.course.id}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["message"],
            'Подписка на курс "Test Course for Subscription" добавлена',
        )
        self.assertTrue(response.data["subscribed"])
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_delete(self):
        """Тест: удаление подписки"""
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.subscription_url, {"course_id": self.course.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            'Подписка на курс "Test Course for Subscription" удалена',
        )
        self.assertFalse(response.data["subscribed"])
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_without_course_id(self):
        """Тест: ошибка при отсутствии course_id"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.subscription_url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Параметр course_id обязателен")

    def test_subscription_with_invalid_course_id(self):
        """Тест: ошибка при неверном course_id"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.subscription_url, {"course_id": 999})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscription_unauthenticated_denied(self):
        """Тест: неаутентифицированный пользователь не может управлять подписками"""
        response = self.client.post(
            self.subscription_url, {"course_id": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
