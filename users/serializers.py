from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """ Сериализатор для платежей """

    class Meta:
        model = Payment
        fields = '__all__' #('payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method',)
