from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from users.models import Payment, User
from users.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']  # Поля для фильтрации
    ordering_fields = ['payment_date']  # Поле для сортировки
