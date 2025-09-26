from django.db import models

from materials.models import Course, Lesson
from users.models import User


class Payment(models.Model):
    """Модель для хранения информации о платежах"""

    # способ платежа
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
        ("gift", "Подарочный сертификат"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="payments",
        verbose_name="Плательщик",
        help_text="Укажите плательщика",
        null=True,
        blank=True,
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
        related_name="payments",
        verbose_name="Оплаченный курс",
        help_text="Курс, за который произведена оплата",
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный урок",
        help_text="Урок, за который произведена оплата",
    )
    amount = models.PositiveIntegerField(
        default=0, verbose_name="Сумма оплаты", help_text="Укажите сумму оплаты в рублях"
    )
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Идентификатор сессии",
        help_text="Укажите идентификатор сессии платежа",
    )
    payment_link = models.URLField(
        max_length=400,
        null=True,
        blank=True,
        verbose_name="Ссылка на оплату",
        help_text=("Ссылка для оплаты (для платежа через платежную систему)"),
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        what_is_paid_for = self.paid_course or self.paid_lesson or "не указано"
        return f"Платеж {self.owner} - {self.amount} руб. ({what_is_paid_for})"
