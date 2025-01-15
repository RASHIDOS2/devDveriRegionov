from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'full_name']

    fieldsets = UserAdmin.fieldsets + (
        ('Реквизиты 1С', {'fields': ('full_name', )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Реквизиты 1С', {'fields': ('full_name', )}),
    )

    search_fields = ('full_name', 'username',)
    ordering = ('full_name', 'username',)


admin.site.register(CustomUser, CustomUserAdmin)
