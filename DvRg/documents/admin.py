from django.contrib import admin
from .models import Orders, OrderDetails, ExchangeNode


# Register your models here.
class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails


class OrdersAdmin(admin.ModelAdmin):
    search_fields = ['date', 'number', 'partner__username', 'partner__email']

    inlines = [
        OrderDetailsInline
    ]


admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderDetails)
admin.site.register(ExchangeNode)