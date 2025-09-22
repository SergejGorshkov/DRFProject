from rest_framework.routers import DefaultRouter

from payments.apps import PaymentsConfig
from payments.views import PaymentViewSet

app_name = PaymentsConfig.name  # Извлечение имени приложения из модуля payments/apps.py

router = DefaultRouter()  # Создание экземпляра DefaultRouter для регистрации ViewSet
router.register(
    r"payments", PaymentViewSet, basename="payments"
)  # Регистрация ViewSet с именем payments

urlpatterns = [] + router.urls  # Добавление URL для ViewSet
