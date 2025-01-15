from django.urls import path, include
from .views import OrdersViewSet, ExchangeNodeViewSet, test_task, NewOrderView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'backend/api/v1/orders', OrdersViewSet, basename='orders')
router.register(r'backend/api/v1/exchange', ExchangeNodeViewSet, basename='exchange')

urlpatterns = [
    path('', include(router.urls)),
    path('backend/test_task/', test_task),
    path('backend/api/v1/create_new_order/', NewOrderView.as_view(), name='create_new_order')

]