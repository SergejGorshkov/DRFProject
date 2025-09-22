from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Регистрация модели User в админке """
    list_filter = ('id', 'email',)
