from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    """ Команда для создания администратора """
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@mail.com',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password('123qwe')  # Хеширование пароля
        user.save()
