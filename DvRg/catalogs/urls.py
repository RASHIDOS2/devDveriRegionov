from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'api/v1/products', ProductViewSet, basename='products')
router.register(r'api/v1/products_group', ProductsGroupViewSet, basename='products_group')

urlpatterns = [
    path('', include(router.urls)),

]