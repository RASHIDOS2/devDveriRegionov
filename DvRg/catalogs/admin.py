from django.contrib import admin

# Register your models here.
from .models import *


class ProductsAdmin(admin.ModelAdmin):
    search_fields = ['full_name', ]


admin.site.register(Products)
admin.site.register(ProductGroup)
admin.site.register(Images)
admin.site.register(TypesOfProducts)
admin.site.register(Characteristics)
admin.site.register(Organizations)
admin.site.register(CounterParty)
admin.site.register(Agreement)
admin.site.register(Contract)