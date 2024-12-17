import uuid

from rest_framework import serializers
from .models import *


class TypesOfProductsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4,)

    class Meta:
        model = TypesOfProducts
        fields = ['id', 'name']


class ProductsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4,)

    class Meta:
        model = Products
        fields = ['id', 'full_name', 'group', 'use_characteristics', 'type_of_product']


class ProductsGroupSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4,)

    class Meta:
        model = ProductGroup
        fields = ['id', 'title', 'parent']


class ImagesSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4,)

    class Meta:
        model = Images
        fields = ['id', 'product', 'image']


class CharacteristicsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4,)

    class Meta:
        model = Characteristics
        fields = ['id', 'name', 'product', 'type_of_product']


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4,)

    class Meta:
        model = Organization
        fields = ['id', 'name']


