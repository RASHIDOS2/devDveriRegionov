from rest_framework import serializers
from .models import *
from drf_writable_nested import WritableNestedModelSerializer

import uuid

from catalogs.serializers import PriceImageSerializer
from catalogs.models import Images


class OrderDetailSerializer(serializers.ModelSerializer):
    product_full_name = serializers.CharField(source='product.full_name', read_only=True)
    characteristic_name = serializers.CharField(source='characteristic.name', read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_images(self, obj):
        images = Images.objects.filter(product=obj.product)
        if images:
            result = PriceImageSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = OrderDetails
        fields = ['pk', 'order', 'product', 'product_full_name', 'characteristic', 'characteristic_name', 'price', 'quantity', 'total', 'image']


class OrderSerializer(WritableNestedModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4,)
    order_orders_detail = OrderDetailSerializer(many=True, required=False)
    partner_full_name = serializers.CharField(source='partner.full_name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)

    def create(self, validated_data):
        order = super().create(validated_data)
        if self.initial_data.get('from_ones') is None:
            order.fix_exchange()
        return order

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if self.initial_data.get('from_ones') is None:
            instance.fix_exchange()
        return instance

    class Meta:
        model = Orders
        fields = ['id', 'date', 'number', 'side_status', 'partner', 'counterparty', 'organization', 'agreement',
                  'contract', 'order_orders_detail', 'partner_full_name', 'organization_name']


class ExchangeNodeSerializer(serializers.ModelSerializer):
    model = OrderSerializer

    class Meta:
        model = ExchangeNode
        fields = ['pk', 'updated_at', 'order']



