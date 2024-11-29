# asher_admin/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.html import mark_safe

@admin.display(description='Profile Picture')
def picture_preview(self, obj):
    return mark_safe(f'<img src="{obj.picture.url}" width="50" height="50" style="object-fit: cover;">')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'phone', 'country', 'active', 'is_admin', 'is_staff', 'is_customer', 'date_joined','last_login')
    list_filter = ('email', 'first_name', 'last_name', 'is_admin', 'is_staff', 'is_customer', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'country', 'picture', 'status')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_customer')}),
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'country', 'password1', 'password2', 'is_admin', 'is_staff', 'is_customer')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)
