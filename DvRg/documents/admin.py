from django.contrib import admin
from .models import Orders, OrdersDetail, ExchangeNode


class OrdersDetailInline(admin.TabularInline):
    model = OrdersDetail


class OrdersAdmin(admin.ModelAdmin):
    search_fields = ('date', 'number', 'partner__username', 'partner__email',)

    inlines = [
        OrdersDetailInline,
    ]


admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrdersDetail)
admin.site.register(ExchangeNode)
