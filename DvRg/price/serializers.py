from rest_framework import serializers
from .models import *

class PriceSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.full_name')
    title_characteristic = serializers.CharField(source='characteristic.name', read_only=True)

    class Meta:
        model = Prices
        fields = ['id', 'product', 'characteristic', 'title', 'price', 'title_characteristic']
