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


class CounterPartySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = CounterParty
        fields = ['id', 'partner', 'name', 'full_name', 'status', 'inn', 'kpp']


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

    def save(self, *args, **kwargs):
        if self.instance:
            if self.instance.image:
                self.instance.image.delete()
        return super().save(*args, **kwargs)



class CharacteristicsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4,)

    class Meta:
        model = Characteristics
        fields = ['id', 'name', 'product', 'type_of_product']


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4,)

    class Meta:
        model = Organizations
        fields = ['id', 'name']


class AgreementSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = Agreement
        fields = ['id', 'name', 'number', 'date', 'partner', 'counterparty']


class ContractSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = Contract
        fields = ['id', 'name', 'number', 'date', 'partner', 'counterparty', 'organization', 'default']


class ProductsGroupTreeSerializer(serializers.Serializer):
    id = serializers.CharField()
    parent = serializers.CharField()
    title = serializers.CharField()
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        nodes = []
        if len(obj.children) > 0:
            for node in obj.children:
                result = ProductsGroupTreeSerializer(node)
                nodes.append(result.data)
        return nodes


class PriceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image']