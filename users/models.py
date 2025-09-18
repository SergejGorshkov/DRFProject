from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings
from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите ваш email"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите ваш телефон",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите ваш город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите ваш аватар",
    )

    USERNAME_FIELD = (
        "email"  # означает, что мы хотим использовать email в качестве логина
    )
    REQUIRED_FIELDS = (
        []
    )  # означает, что мы не хотим использовать username в качестве обязательного поля

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Модель для хранения информации о платежах"""
    # способ платежа
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
        ("gift", "Подарочный сертификат"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # связь с пользователем, который оплатил курс или урок (имя - из settings.py)
        related_name="payments",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, оплативший курс или урок",
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name="Дата платежа",
        help_text="Дата и время совершения платежа",
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Оплаченный курс',
        help_text='Курс, за который произведена оплата'
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Оплаченный урок',
        help_text='Урок, за который произведена оплата'
    )
    amount = models.PositiveIntegerField(
        default=0,
        verbose_name='Сумма оплаты',
        help_text='Сумма платежа в рублях'
    )
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ['-payment_date']

    def __str__(self):
        what_is_paid_for = self.paid_course or self.paid_lesson or "не указано"
        return f"Платеж {self.user} - {self.amount} руб. ({what_is_paid_for})"
