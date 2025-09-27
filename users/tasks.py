from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from users.models import User


@shared_task
def send_deactivation_notification(user_email):
    """Отправка уведомления о деактивации аккаунта."""
    try:
        subject = "Ваш аккаунт был деактивирован"
        message = """
        Уважаемый пользователь!

        Ваш аккаунт был автоматически деактивирован из-за длительного отсутствия активности
        (более 31 дня без входа в систему).

        Для восстановления доступа обратитесь в поддержку.

        С уважением,
        Команда сервиса
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )

        return f"Уведомление о деактивации отправлено пользователю {user_email}"

    except Exception as e:
        return f"Ошибка отправки уведомления о деактивации пользователя: {str(e)}"


@shared_task
def deactivate_inactive_users():
    """Задача для деактивации пользователей, которые не заходили более 1 месяца."""
    try:
        # Вычисление даты (31 день назад)
        month_ago = timezone.now() - timedelta(days=31)

        # Поиск пользователей, которые не заходили более 1 месяца и еще активны
        inactive_users = User.objects.filter(
            last_login__lt=month_ago,  # последний вход раньше, чем 31 день назад
            is_active=True,  # только активные пользователи
        )

        user_count = (
            inactive_users.count()
        )  # Получение количества пользователей для деактивации

        if user_count == 0:
            return "Не найдено пользователей для деактивации."

        # Деактивация пользователей
        deactivated_emails = []
        for user in inactive_users:
            user.is_active = False
            user.save()
            deactivated_emails.append(user.email)

            # Отправка уведомления пользователю
            send_deactivation_notification.delay(user.email)

        return f"Успешно деактивировано {user_count} пользователей"

    except Exception as e:
        return f"Ошибка: {str(e)}"
