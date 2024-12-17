from rest_framework import viewsets, permissions
from .serializers import *
from .models import *
# Create your views here.


class ProductViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class ProductsGroupViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = ProductGroup.objects.all()
    serializer_class = ProductsGroupSerializer


class TypesOfProductsViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = TypesOfProducts.objects.all()
    serializer_class = TypesOfProductsSerializer


class ImageViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class CharacteristicsViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = Characteristics.objects.all()
    serializer_class = CharacteristicsSerializer


class OrganizationViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class CounterpartyViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = Counterparty.objects.all()
    serializer_class = CounterpartySerializer


class AgreementViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer


class ContractViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
