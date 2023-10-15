from rest_framework import serializers

from payments.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserPartialSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', 'last_name']
