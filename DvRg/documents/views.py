from .serializers import OrderSerializer, ExchangeNodeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from .models import Orders, ExchangeNode
from catalogs.mixins import MyModelViewSet
from .tasks import upload_orders
from django.http import HttpResponse

# Create your views here.
class OrderViewSet(MyModelViewSet, viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Order.objects.all()
        elif self.request.request.user:
            return Orders.objects.filter(partner=self.request.user)


class ExchangeNodeViewSet(MyModelViewSet, viewsets.ModelViewSet):
    serializer_class = ExchangeNodeSerializer
    permission_classes = [IsAdminUser]
    queryset = ExchangeNode.objects.all()


def test_task(request):
    upload_orders.delay()
    return HttpResponse('<h1>Запуск задачи</h1>')

