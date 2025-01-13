from django.urls import path, include
from .views import OrderViewSet, ExchangeNodeViewSet, test_task
from rest_framework import routers

router = routers.DefaultRouter()
router.register('backend/api/v1/orders', OrderViewSet, basename='orders')
router.register(r'backend/api/v1/exchange', ExchangeNodeViewSet, basename='exchange')

urlpatterns = [
    path('', include(router.urls)),
    path('test_task/', test_task, name='test_task'),
]