from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    image = models.ImageField(
        upload_to="materials/photo",
        blank=True,
        null=True,
        verbose_name="Превью курса",
        help_text="Загрузите изображение в формате JPEG или PNG (макс. 5 МБ)",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Введите описание курса",
    )
    owner = models.ForeignKey(  # связь с моделью User
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="courses",
        verbose_name="Владелец",
        help_text="Введите владельца курса",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Введите описание урока",
    )
    image = models.ImageField(
        upload_to="materials/photo",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Загрузите изображение в формате JPEG или PNG (макс. 5 МБ)",
    )
    video = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Введите ссылку на видео",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        help_text="Выберите курс",
    )
    owner = models.ForeignKey(  # связь с моделью User
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="lessons",
        verbose_name="Владелец",
        help_text="Введите владельца урока",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(  # связь с моделью User
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Курс",
    )
    subscribed_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата подписки"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = [
            "user",
            "course",
        ]  # уникальное сочетание полей (один пользователь не может подписаться дважды)

    def __str__(self):
        return f"Пользователь {self.user.email} подписан на {self.course.name}"
