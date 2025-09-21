from users.apps import UsersConfig
from payments.views import PaymentViewSet
from rest_framework.routers import DefaultRouter


app_name = (
    UsersConfig.name
)  # Извлечение имени приложения из модуля payments/apps.py

router = DefaultRouter()  # Создание экземпляра DefaultRouter для регистрации ViewSet
router.register(r"payments", PaymentViewSet, basename="payments")  # Регистрация ViewSet с именем payments

urlpatterns = [

] + router.urls  # Добавление URL для ViewSet
