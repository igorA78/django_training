from rest_framework import generics

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()


class SubscriptionListAPIView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
