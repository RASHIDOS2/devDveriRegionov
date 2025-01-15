from rest_framework import serializers
from .models import *
from price.models import Prices


class TypesOfProductsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = TypesOfProducts
        fields = ['id', 'name']


class ProductsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = Products
        fields = ['id', 'full_name', 'group', 'use_characteristics', 'type_of_product', 'description']


class ProductDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)
    images = serializers.SerializerMethodField(read_only=True)
    count = serializers.IntegerField(default=0, read_only=True)

    def get_images(self, obj):
        images = Images.objects.filter(product=obj.id)
        if images:
            result = PriceImagesSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = Products
        fields = ['id', 'full_name', 'description', 'images', 'count']


class CharacteristicsDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4, source='product.id')
    full_name = serializers.CharField(source='product.full_name')
    description = serializers.CharField(source='product.description')
    images = serializers.SerializerMethodField(read_only=True)
    title_characteristic = serializers.CharField(source='name')
    characteristic = serializers.UUIDField(default=uuid.uuid4, source='id')

    def get_images(self, obj):
        images = Images.objects.filter(product=obj.product)
        if images:
            result = PriceImagesSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = Characteristics
        fields = ['id', 'full_name', 'description', 'images', 'title_characteristic', 'characteristic']


class ProductsGroupSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = ProductsGroup
        fields = ['id', 'title', 'parent']


class ImagesSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = Images
        fields = ['id', 'product', 'image']

    def save(self, *args, **kwargs):
        if self.instance:
            if self.instance.image:
                self.instance.image.delete()
        return super().save(*args, **kwargs)


class CharacteristicsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = Characteristics
        fields = ['id', 'name', 'product', 'type_of_product']


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = Organization
        fields = ['id', 'name']


class CounterpartySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = Counterparty
        fields = ['id', 'partner', 'name', 'full_name', 'status', 'inn', 'kpp']


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


class PriceImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image']


