from rest_framework import serializers
from .models import *

class PriceSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.full_name')

    class Meta:
        model = Prices
        fields = ['id', 'product', 'title', 'price']