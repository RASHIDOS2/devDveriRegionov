from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from .models import Orders
from catalogs.mixins import MyModelViewSet


# Create your views here.
class OrderViewSet(MyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Order.objects.all()
        elif self.request.request.user:
            return Orders.objects.filter(partner=self.request.user)
