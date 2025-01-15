from rest_framework import viewsets, status

from .serializers import *
from .models import *
from .mixins import MyModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView


class ProductsViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class ProductsGroupViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = ProductsGroup.objects.all()
    serializer_class = ProductsGroupSerializer


class TypesOfProductsViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = TypesOfProducts.objects.all()
    serializer_class = TypesOfProductsSerializer


class ImagesViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class CharacteristicsViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = Characteristics.objects.all()
    serializer_class = CharacteristicsSerializer


class OrganizationViewSet(MyModelViewSet, viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class CounterpartyViewSet(MyModelViewSet, viewsets.ModelViewSet):
    serializer_class = CounterpartySerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Counterparty.objects.all()
        elif self.request.user:
            return Counterparty.objects.filter(partner=self.request.user)


class AgreementViewSet(MyModelViewSet, viewsets.ModelViewSet):
    serializer_class = AgreementSerializer

    def get_queryset(self):
        return Agreement.objects.all()
        # Надо смотреть как ведется учет в 1С, так как есть индивидуальные и общие соглашения, пока показываем все
        # if self.request.user and self.request.user.is_staff:
        #     return Agreement.objects.all()
        # elif self.request.user:
        #     return Agreement.objects.filter(partner=self.request.user)


class ContractViewSet(MyModelViewSet, viewsets.ModelViewSet):
    serializer_class = ContractSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Contract.objects.all()
        elif self.request.user:
            return Contract.objects.filter(partner=self.request.user)


class Node(object):
    def __init__(self, node):
        self.id = node.id
        self.title = node.title
        if node.parent:
            self.parent = node.parent.title
            self.parent_id = node.parent.id
        else:
            self.parent = None
            self.parent_id = None
        self.children = []

    def __str__(self):
        return f'{self.title} - {self.parent} - {self.children}'


def add_nodes(product_groups):
    tree_nodes = {}

    for group in product_groups:
        node = Node(group)
        tree_nodes[node.id] = node

    for key, item in tree_nodes.items():
        if item.parent is None:
            continue
        if item.parent_id in tree_nodes.keys():
            children = tree_nodes[item.parent_id].children
            children.append(item)

    return tree_nodes


class ProductsGroupTree(APIView):
    def get(self, request):
        products_group = ProductsGroup.objects.all()
        tree_nodes = add_nodes(products_group)
        root_nodes = [node for id, node in tree_nodes.items() if (node.parent is None)]

        result = []
        for node in root_nodes:
            group_sr = ProductsGroupTreeSerializer(node)
            result.append(group_sr.data)

        return Response({'results': result, 'errors': ''}, status=status.HTTP_200_OK)
