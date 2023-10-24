from rest_framework import serializers

from payments.models import Payment
from payments.services import create_payment_intent, retrieve_payment_intent


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.request = kwargs.get('context').get('request')

    def get_payment_stripe(self, instance):
        if self.request.method == 'POST':
            payment_stripe_id = create_payment_intent(instance.amount)
            obj_payment = Payment.objects.get(id=instance.id)
            obj_payment.payment_stripe_id = payment_stripe_id
            obj_payment.save()

            return retrieve_payment_intent(payment_stripe_id)

        if self.request.method == 'GET':
            if not instance.payment_stripe_id:
                return None
            return retrieve_payment_intent(instance.payment_stripe_id)

