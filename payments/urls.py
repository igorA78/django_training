from rest_framework import routers

from payments.apps import PaymentsConfig
from payments.views import PaymentsAPIViewSet

app_name = PaymentsConfig.name

router = routers.DefaultRouter()
router.register(r'', PaymentsAPIViewSet, basename='payments')

urlpatterns = [

]+router.urls
