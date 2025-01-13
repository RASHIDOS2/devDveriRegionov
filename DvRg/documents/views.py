from .serializers import OrderSerializer, ExchangeNodeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from .models import Orders, ExchangeNode, SiteOrderStatus
from catalogs.mixins import MyModelViewSet
from .tasks import upload_orders
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        results = {
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'per_page': self.page.paginator.per_page,
            'results': data,
        }
        return my_response(results)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Order.objects.all().order_by('-date')
        elif self.request.request.user:
            return Orders.objects.filter(partner=self.request.user).order_by('-date')

    def create(self, request, *args, **kwargs):
        new_order = Orders.objects.filter(partner=self.request.user, site_status=SideOrderStatus.CREATE)
        if new_order:
            return my_response(errors='В базе есть созданный необработанный заказ', status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return my_response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        partner = self.request.data.get('partner', None)
        if partner is None:
            serializer.save(partner=self.request.user)


class ExchangeNodeViewSet(MyModelViewSet, viewsets.ModelViewSet):
    serializer_class = ExchangeNodeSerializer
    permission_classes = [IsAdminUser]
    queryset = ExchangeNode.objects.all()


def test_task(request):
    upload_orders.delay()
    return HttpResponse('<h1>Запуск задачи</h1>')

