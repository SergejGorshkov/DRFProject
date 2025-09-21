from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentViewSet(ModelViewSet):
    """ CRUD для платежей """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['owner', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']  # Поля для фильтрации
    ordering_fields = ['payment_date']  # Поле для сортировки

    def perform_create(self, serializer):
        """ Создание платежа и сохранение владельца в поле owner """
        payment = serializer.save()
        payment.owner = self.request.user # сохранение владельца платежа в поле owner
        payment.save()
