from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from users.models import User


class Command(BaseCommand):
    help = 'Создание группы модераторов и добавление пользователей в нее'

    def handle(self, *args, **options):
        # Создание или получение группы "Moderators"
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Moderators" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Moderators" уже существует'))

        # Добавление прав для модераторов (просмотр и редактирование курсов или уроков)
        try:
            moderators_permissions = Permission.objects.filter(
                codename__in=['view_lesson', 'change_lesson', 'view_course', 'change_course']
            )
            moderators_group.permissions.set(moderators_permissions)
            self.stdout.write(self.style.SUCCESS('Права для группы "Moderators" настроены'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при настройке прав группы "Moderators": {e}'))

        # Создание или получение пользователей-модераторов
        moderators_data = [
            {
                'email': 'moderator1@example.com',
                'password': 'mod1pass123',
                'is_staff': True  # Для доступа к админке
            },
            {
                'email': 'moderator2@example.com',
                'password': 'mod2pass123',
                'is_staff': True
            }
        ]

        for moderator_data in moderators_data:
            email = moderator_data['email']

            # Проверка, существует ли пользователь
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'is_staff': moderator_data['is_staff'],
                    'is_active': True
                }
            )

            if created:
                # Установка хешированного пароля для нового пользователя
                user.set_password(moderator_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Создан пользователь: {email}'))
            else:
                self.stdout.write(self.style.WARNING(f'Пользователь уже существует: {email}'))

            # Добавление пользователя в группу модераторов
            user.groups.add(moderators_group)
            self.stdout.write(self.style.SUCCESS(f'Пользователь {email} добавлен в группу модераторов'))
