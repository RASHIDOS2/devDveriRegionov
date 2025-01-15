from rest_framework import serializers
from .models import Prices
from catalogs.serializers import PriceImagesSerializer
from catalogs.models import Images


class PricesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.full_name', read_only=True)
    title_characteristic = serializers.CharField(source='characteristic.name', read_only=True)
    count = serializers.IntegerField(default=0)
    images = serializers.SerializerMethodField(read_only=True)

    def get_images(self, obj):
        images = Images.objects.filter(product=obj.product)
        if images:
            result = PriceImagesSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = Prices
        fields = ['id', 'product', 'characteristic', 'title', 'title_characteristic', 'price', 'count', 'images']


class PriceDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.full_name', read_only=True)
    title_characteristic = serializers.CharField(source='characteristic.name', read_only=True)
    count = serializers.IntegerField(default=0, read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    description = serializers.CharField(source='product.description', read_only=True, default='')

    def get_images(self, obj):
        images = Images.objects.filter(product=obj.product)
        if images:
            result = PriceImagesSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = Prices
        fields = ['id', 'product', 'characteristic', 'title', 'title_characteristic', 'price', 'count', 'images', 'description']
