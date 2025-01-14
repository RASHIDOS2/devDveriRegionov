from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'backend/api/v1/price', PriceViewSet, basename='products')


urlpatterns = [
    path('', include(router.urls)),
    path('backend/api/v1/price_detail', ProductDetailViewSet.as_view(), name='price_detail')
]