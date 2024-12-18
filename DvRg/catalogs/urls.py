from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'api/v1/products', ProductViewSet, basename='products')
router.register(r'api/v1/products_group', ProductsGroupViewSet, basename='products_group')
router.register(r'api/v1/types_of_products', TypesOfProductsViewSet, basename='types_of_products')
router.register(r'api/v1/images', ImageViewSet, basename='images')
router.register(r'api/v1/characteristics', CharacteristicsViewSet, basename='characteristics')
router.register(r'api/v1/organization', OrganizationViewSet, basename='organization')
router.register(r'api/v1/counterparty', CounterPartyViewSet, basename='counterparty')
router.register(r'api/v1/agreement', AgreementViewSet, basename='agreement')
router.register(r'api/v1/contract', ContractViewSet, basename='contract')


urlpatterns = [
    path('', include(router.urls)),

]