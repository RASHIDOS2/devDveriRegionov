from rest_framework import viewsets, permissions
from .serializers import *
from .models import *
from .mixins import MyModelViewSet


class ProductViewSet(MyModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class ProductsGroupViewSet(MyModelViewSet):
    queryset = ProductGroup.objects.all()
    serializer_class = ProductsGroupSerializer


class TypesOfProductsViewSet(MyModelViewSet):
    queryset = TypesOfProducts.objects.all()
    serializer_class = TypesOfProductsSerializer


class ImageViewSet(MyModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class CharacteristicsViewSet(MyModelViewSet):
    queryset = Characteristics.objects.all()
    serializer_class = CharacteristicsSerializer


class OrganizationViewSet(MyModelViewSet):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationSerializer


class CounterPartyViewSet(MyModelViewSet):
    queryset = CounterParty.objects.all()
    serializer_class = CounterPartySerializer


class AgreementViewSet(MyModelViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer


class ContractViewSet(MyModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


