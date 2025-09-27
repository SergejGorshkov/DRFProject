from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Course, Subscription


@shared_task
def send_course_update_notification(course_id):
    """Отправка уведомления об обновлении курса подписчикам"""
    course = Course.objects.get(id=course_id)  # Получение курса по его ID
    subscribers = Subscription.objects.filter(
        course=course
    )  # Получение подписчиков курса

    for subscription in subscribers:
        try:
            send_mail(
                subject=f"Обновление курса: {course.name}",
                message=f'Дорогой подписчик! Произошло обновление курса "{course.name}".',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    subscription.user.email
                ],  # Получение списка email подписчиков
                fail_silently=False,  # Если отправка не удалась, не выбрасывать исключение
            )

            return f"Уведомления отправлены {subscribers.count()} подписчикам"
        except Exception as e:
            return f"Ошибка отправки уведомления: {str(e)}"
