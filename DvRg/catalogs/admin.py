from django.contrib import admin
from .models import *


class ProductsAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)


admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductsGroup)
admin.site.register(Images)
admin.site.register(TypesOfProducts)
admin.site.register(Characteristics)
admin.site.register(Organization)
admin.site.register(Counterparty)
admin.site.register(Agreement)
admin.site.register(Contract)
