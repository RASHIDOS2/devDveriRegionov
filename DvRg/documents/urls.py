from django.urls import path, include
from .views import OrderViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/v1/orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]