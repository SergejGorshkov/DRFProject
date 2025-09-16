from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from materials.models import Lesson, Course
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    """Команда для загрузки тестовых данных"""
    help = 'Загрузка тестовых данных'

    def handle(self, *args, **kwargs):
        # Удаление существующих записей
        Payment.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        # Создание курса
        course, created = Course.objects.get_or_create(name='Курс 1', description="Какой-то курс1")
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Успешно добавлен курс: {course.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Курс "{course.name}" уже есть в БД.'))

        # Создание уроков
        lessons = [
            {'name': 'Урок 1', 'description': 'Какой-то урок1', 'course': course},
            {'name': 'Урок 2', 'description': 'Какой-то урок2', 'course': course},
            {'name': 'Урок 3', 'description': 'Какой-то урок3', 'course': course},
        ]

        created_lessons = []
        for lesson_data in lessons:
            lesson, created = Lesson.objects.get_or_create(**lesson_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Успешно добавлен урок: {lesson.name}'))
                created_lessons.append(lesson)
            else:
                self.stdout.write(self.style.WARNING(f'Урок "{lesson.name}" уже есть в БД.'))

        # Создание или получение пользователей
        users = [
            {'email': 'user1@mail.com'},
            {'email': 'user2@mail.com'},
            {'email': 'user3@mail.com'},
        ]

        created_users = []
        for user_data in users:
            user, created = User.objects.get_or_create(email=user_data['email'])
            if created:
                user.set_password('testpassword123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Успешно создан пользователь: {user.email}'))
            else:
                self.stdout.write(self.style.WARNING(f'Пользователь "{user.email}" уже есть в БД.'))
            created_users.append(user)

        # Создание платежей
        payments = [
            {"user": created_users[0], "payment_date": None,
             "paid_course": course, "paid_lesson": None, "amount": 10000, "payment_method": "cash"},

            {"user": created_users[1], "payment_date": None,
             "paid_course": None, "paid_lesson": created_lessons[2], "amount": 20000, "payment_method": "transfer"},

            {"user": created_users[2], "payment_date": None,
             "paid_course": course, "paid_lesson": None, "amount": 15000, "payment_method": "gift"},
        ]

        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Успешно добавлен платеж: {payment.user.email} - {payment.amount} руб.'))
            else:
                self.stdout.write(self.style.WARNING(f'Платеж для "{payment.user.email}" уже есть в БД.'))
