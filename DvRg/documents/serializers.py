import uuid
from rest_framework import serializers
from .models import Orders, OrdersDetail, ExchangeNode
from drf_writable_nested.serializers import WritableNestedModelSerializer
from catalogs.serializers import PriceImagesSerializer
from catalogs.models import Images


class OrdersDetailSerializer(serializers.ModelSerializer):
    product_full_name = serializers.CharField(source='product.full_name', read_only=True)
    characteristic_name = serializers.CharField(source='characteristic.name', read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_images(self, obj):
        images = Images.objects.filter(product=obj.product)
        if images:
            result = PriceImagesSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = OrdersDetail
        fields = ['pk', 'order', 'product', 'product_full_name', 'characteristic', 'characteristic_name', 'price', 'quantity', 'total', 'images']


class OrdersSerializer(WritableNestedModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)
    order_orders_detail = OrdersDetailSerializer(many=True, required=False)
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
        fields = ['id', 'date', 'number', 'site_status', 'partner', 'partner_full_name', 'counterparty', 'organization',
                  'organization_name', 'agreement', 'contract', 'order_orders_detail']


class ExchangeNodeSerializer(serializers.ModelSerializer):
    order = OrdersSerializer()

    class Meta:
        model = ExchangeNode
        fields = ['pk', 'updated_at', 'order']
