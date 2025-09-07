from django.contrib import admin
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (
            'User Info', {
                'fields': ('email', 'phone_number', 'first_name', 'last_name', 'password')
            }
        ),
        (
            'Permissions', {
                'fields': ('is_active', 'is_admin')
            }
        )
    )

    add_fieldsets = (
        (
            'User Info', {
                'fields': ('email', 'phone_number', 'first_name', 'last_name', 'password1', 'password2')
            }
        ),
        (
            'Permissions', {
                'fields': ('is_active', 'is_admin')
            }
        )
    )

    search_fields = ('email', 'phone_number')
    ordering = ('first_name',)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
