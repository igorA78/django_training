from django.urls import path

from subscriptions.apps import SubscriptionsConfig
from subscriptions.views import SubscriptionCreateAPIView, SubscriptionDestroyAPIView, SubscriptionListAPIView

app_name = SubscriptionsConfig.name

urlpatterns = [
    path('', SubscriptionListAPIView.as_view(), name='list'),
    path('create/', SubscriptionCreateAPIView.as_view(), name='create'),
    path('delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='delete'),
]