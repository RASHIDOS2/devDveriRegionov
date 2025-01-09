from rest_framework import viewsets, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from catalogs.models import Products, Characteristics
from .serializers import PriceSerializer
from .models import Prices

from .permissions import isAdminOrReadOnly
import django_filters
from django.db.models import Q


class PriceFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='my_custom_filter')
    price = django_filters.RangeFilter()
    group = django_filters.UUIDFilter(field_name='product__group')

    class Meta:
        model = Prices
        fields = ['search', 'price', 'group']

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(product__full_name__contains=value) |
            Q(characteristic__name__contains=value)
        )


class StandartResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'per_page': self.page.paginator.per_page,
            'result': data
        })


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Prices.objects.all()
    serializer_class = PriceSerializer
    pagination_classes = [isAdminOrReadOnly]
    pagination_class = StandartResultSetPagination
    filterset_class = PriceFilter

    def create(self, request, *args, **kwargs):
        try:
            product = Products.objects.filter(pk=request.data['product'])
            if not product:
                return Response({'results': None, 'errors': 'Номенклатуры нет на портале'},
                                status=status.HTTP_400_BAD_REQUEST)
            characteristic = Characteristics.objects.filter(pk=request.data['characteristic'])
            price = request.data['price']

            obj_product = product.get()
            if len(characteristic) > 0:
                obj_characteristic = characteristic.get()
            else:
                obj_characteristic = None

            if price == 0:
                self.queryset.filter(product=obj_product, characteristic=obj_characteristic).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                product_price = self.queryset.filter(product=obj_product, characteristic=obj_characteristic)
                if product_price:
                    obj = product_price.get()
                    obj.price = price
                    obj.save()
                    return Response(status=status.HTTP_206_PARTIAL_CONTENT)
                else:
                    obj = self.queryset.create(product=obj_product, characteristic=obj_characteristic, price=price)
                    obj.save()
                    return Response(status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(data={'error': ex.__str__}, status=status.HTTP_400_BAD_REQUEST)

