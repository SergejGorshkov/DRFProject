from users.apps import UsersConfig
from users.views import PaymentViewSet
from rest_framework.routers import DefaultRouter

app_name = (
    UsersConfig.name
)  # Извлечение имени приложения из модуля users/apps.py

router = DefaultRouter()  # Создание экземпляра DefaultRouter для регистрации ViewSet
router.register(
    r"payments", PaymentViewSet, basename="payments")
urlpatterns = [

] + router.urls  # Добавление URL для ViewSet
