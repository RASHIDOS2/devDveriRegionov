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

    def create(self, validated_data):
        order = super().create(validated_data)
        if self.initial_data['from_frontend']:
            order.fix_exchange()
        return order

    def update(self, instance, validated_data):
        if self.initial_data['from_frontend']:
            instance.fix_exchange()
        return instance

    class Meta:
        model = Orders
        fields = ['id', 'date', 'number', 'partner', 'counterparty', 'organization', 'agreement', 'contract', 'order_orders_detail']


class ExchangeNodeSerializer(serializers.ModelSerializer):
    model = OrderSerializer

    class Meta:
        model = ExchangeNode
        fields = ['pk', 'updated_at', 'order']



