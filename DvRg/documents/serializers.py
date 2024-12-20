from rest_framework import serializers
from .models import *
from drf_writable_nested import WritableNestedModelSerializer

import uuid

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ['pk', 'order', 'product', 'characteristic', 'price', 'quantity', 'total']


class OrderSerializer(WritableNestedModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4,)
    order_orders_detail = OrderDetailSerializer(many=True, required=False)

    class Meta:
        model = Orders
        fields = ['id', 'date', 'number', 'partner', 'counterparty', 'organization', 'agreement', 'contract', 'order_orders_detail']