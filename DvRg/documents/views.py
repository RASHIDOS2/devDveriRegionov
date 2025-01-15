from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrdersSerializer, ExchangeNodeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from .models import Orders, ExchangeNode, OrdersDetail
from .tasks import upload_orders
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from catalogs.mixins import my_response, MyModelViewSet
from price.serializers import PricesSerializer


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


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Orders.objects.all().order_by('-date')
        elif self.request.user:
            return self.request.user.partner_order.all().order_by('-date')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return my_response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        partner = self.request.data.get("partner", None)
        if partner is None:
            serializer.save(partner=self.request.user)
        else:
            serializer.save()


class ExchangeNodeViewSet(MyModelViewSet, viewsets.ModelViewSet):
    serializer_class = ExchangeNodeSerializer
    permission_classes = [IsAdminUser]
    queryset = ExchangeNode.objects.all()


def test_task(request):
    upload_orders.delay()
    return HttpResponse('<h1>Запуск задачи</h1>')


class NewOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = Orders.objects.create(partner=request.user)
        for item in request.data:
            price_serializer = PricesSerializer(data=item)
            price_serializer.is_valid(raise_exception=True)
            data = price_serializer.validated_data

            OrdersDetail.objects.create(
                order=order,
                product=data['product'],
                characteristic=data['characteristic'],
                price=data['price'],
                quantity=data['count'],
                total=data['count'] * data['price']
            )

        serializer = OrdersSerializer(order)

        return my_response(serializer.data, status=status.HTTP_201_CREATED)
