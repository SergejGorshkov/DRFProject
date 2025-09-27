from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.services import (create_stripe_price, create_stripe_product,
                               create_stripe_session)
from users.permissions import IsModerator, IsOwner


class PaymentViewSet(ModelViewSet):
    """CRUD для платежей"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        "owner",
        "payment_date",
        "paid_course",
        "paid_lesson",
        "amount",
        "payment_method",
    ]
    ordering_fields = ["payment_date"]  # Поле для сортировки

    def get_permissions(self):
        """Права доступа для действий с платежами"""

        if self.action == "create":
            # если создание объекта, то разрешаем всем аутентифицированным пользователям, кроме модераторов
            self.permission_classes = [IsAuthenticated & ~IsModerator]
        elif self.action == "list":
            # если просмотр списка объектов, то разрешаем всем
            self.permission_classes = [AllowAny]
        elif self.action in ["update", "partial_update", "retrieve"]:
            # если изменение, просмотр деталей объекта, то разрешаем модераторам или владельцу
            self.permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]
        elif self.action == "destroy":
            # если удаление объекта, то разрешаем только владельцу объекта
            self.permission_classes = [IsAuthenticated & IsOwner]
        else:
            # Для остальных действий используем глобальные разрешения
            self.permission_classes = [IsAuthenticated]

        return [
            permission() for permission in self.permission_classes
        ]  # возвращаем разрешения в виде списка объектов

    def perform_create(self, serializer):
        """Создание платежа и сохранение владельца в поле owner"""
        validated_data = (
            serializer.validated_data
        )  # Получаем данные о платеже из запроса после валидации

        # Получаем данные о платеже из запроса после валидации
        name = (
            validated_data["paid_course"]["name"]
            if validated_data.get("paid_course")
            else validated_data["paid_lesson"]["name"]
        )
        description = (
            validated_data["paid_course"]["description"]
            if validated_data.get("paid_course")
            else validated_data["paid_lesson"]["description"]
        )
        amount = validated_data["amount"]

        # Создаем продукт, цену и сессию в Stripe
        product = create_stripe_product(name, description)  # Создаем продукт в Stripe
        price = create_stripe_price(product, amount)  # Создаем цену в Stripe
        session_id, payment_link = create_stripe_session(
            price
        )  # Создаем сессию в Stripe

        # Сохраняем данные в БД
        payment = serializer.save()  # Сохранение платежа в БД
        payment.owner = self.request.user  # Сохранение владельца платежа в поле owner
        payment.session_id = session_id  # Сохранение ID сессии в поле session_id
        payment.payment_link = (
            payment_link  # Сохранение ссылки на оплату в поле payment_link
        )
        payment.save()
