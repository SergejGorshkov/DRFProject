from rest_framework.serializers import ModelSerializer
from payments.models import Payment


class PaymentSerializer(ModelSerializer):
    """ Сериализатор для платежей """

    class Meta:
        model = Payment
        fields = '__all__'
