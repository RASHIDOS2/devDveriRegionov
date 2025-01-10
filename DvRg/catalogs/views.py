from rest_framework import viewsets, permissions, status

from .serializers import *
from .models import *
from .mixins import MyModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView


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


class Node(object):
    def __init__(self, node):
        self.id = node.id
        self.parent = node.parent
        self.title = node.title
        self.children = []


def add_nodes(product_groups):
    tree_nodes = {}
    for i in (1, 2):
        for group in product_groups:
            node = Node(group)
            tree_nodes[node.id] = node
            if node.parent is not None:
                if node.parent.id in tree_nodes.keys():
                    if node not in tree_nodes[node.parent.id].children :
                        tree_nodes[node.parent.id].children.append(node)
    return tree_nodes


class ProductsGroupTree(APIView):
    def get(self, request):
        tree_nodes = add_nodes(ProductGroup.objects.all())
        root_nodes = [node for id, node in tree_nodes.items() if (node.parent is None)]

        result = []
        for node in root_nodes:
            group_sr = ProductsGroupTreeSerializer(node)
            result.append(group_sr.data)

        return Response({'results': result, 'errors': ''}, status=status.HTTP_200_OK)


