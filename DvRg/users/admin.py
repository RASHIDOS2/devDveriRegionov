from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'full_name', 'status']

    fieldsets = UserAdmin.fieldsets + (
        ('Реквезиты 1С', {'fields': ('full_name', 'status', )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Реквезиты 1С', {'fields': ('full_name', 'status', )}),
    )

    search_fields = ('username', 'username')
    ordering = ('full_name', 'username')
    list_filter = ('status', )


admin.site.register(CustomUser, CustomUserAdmin)
