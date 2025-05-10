from django.contrib import admin
from django.utils.decorators import method_decorator
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

# Custom User Manager for the Admin Panel
class UserAdmin(BaseUserAdmin):
    """
    Custom admin class to manage the User model.
    """
    # Fields to display in the list view
    list_display = ('email', 'first_name', 'last_name', 'phone', 'country', 'is_verified', 'is_admin', 'is_staff','is_customer', 'date_joined')
    
    # Fields for searching
    search_fields = ('email','is_customer', 'first_name', 'last_name', 'phone')
    
    # Filter options
    list_filter = ('is_admin', 'is_staff', 'is_verified', 'country')
    
    # Order by date_joined to display the newest users first
    ordering = ('-date_joined',)
    
    # Define fieldsets for the form to manage user creation and editing
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'phone', 'country', 'password')}),
        (_('Permissions'), {'fields': ('is_admin', 'is_staff', 'is_verified', 'is_customer')}),
        (_('Profile Picture'), {'fields': ('picture',)}),
    )
    
    # Add the 'add' form for new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'country', 'password1', 'password2', 'is_superuser', 'is_admin', 'is_staff', 'is_verified'),
        }),
    )
    
    # Add custom behavior for saving the user
    def save_model(self, request, obj, form, change):
        # Call the base save method
        super().save_model(request, obj, form, change)
    
    @method_decorator(admin.action(description=_("Bulk verify selected users")))
    def bulk_verify(self, request, queryset):
        """
        Custom admin action to mark multiple users as verified.
        """
        updated_count = queryset.update(is_verified=True)
        self.message_user(request, f'{updated_count} users have been marked as verified.')

# Register the custom User model with the UserAdmin class
admin.site.register(User, UserAdmin)
