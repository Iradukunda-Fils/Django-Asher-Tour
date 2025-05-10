from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from .db_package import Category, TourPackage, Destination, Itinerary, PackageMedia, Review, PackageOffer




#Django admin Query Optimizer

class OptimizedAdmin(admin.ModelAdmin):
    """
    Abstract admin class that optimizes querysets by using select_related and prefetch_related.
    Extend this class in specific admin classes to reuse optimized queries.
    """
    related_select_fields = []  # ForeignKey and OneToOne relationships
    related_prefetch_fields = []  # ManyToMany or reverse ForeignKey relationships

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if hasattr(self, 'related_select_fields') and self.related_select_fields:
            queryset = queryset.select_related(*self.related_select_fields)
        if hasattr(self, 'related_prefetch_fields') and self.related_prefetch_fields:
            queryset = queryset.prefetch_related(*self.related_prefetch_fields)
        return queryset





#DJANGO BUILD IN ADMIN RESISTRATION OF MODELS

@admin.register(Category)
class CategoryAdmin(OptimizedAdmin):
    list_display = ('slug', 'name', 'description', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
 
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

@admin.register(TourPackage)
class TourPackageAdmin(OptimizedAdmin):
    list_display = ('slug', 'title', 'category', 'price', 'is_active', 'is_published', 'deadline', 'created_at')
    list_filter = ('category', 'is_active', 'is_published', 'deadline', 'created_at')
    search_fields = ('title', 'category__name', 'created_by__email')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_editable = ('is_active', 'is_published')


@admin.register(Destination)
class DestinationAdmin(OptimizedAdmin):
    list_display = ('name', 'tour_package', 'location', 'is_popular')
    list_filter = ('is_popular', 'created_at')
    search_fields = ('name', 'location', 'tour_package__title')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(Itinerary)
class ItineraryAdmin(OptimizedAdmin):
    list_display = ('tour_package', 'day_number', 'title', 'created_at')
    list_filter = ('tour_package', 'created_at')
    search_fields = ('title', 'tour_package__title')
    ordering = ('day_number',)
    date_hierarchy = 'created_at'
    related_select_fields = ['tour_package']

    class Meta:
        verbose_name = "Itinerary"
        verbose_name_plural = "Itineraries"


@admin.register(PackageMedia)
class PackageMediaAdmin(OptimizedAdmin):
    list_display = ('tour_package', 'created_at', 'updated_at')
    search_fields = ('tour_package__title',)
    ordering = ('-created_at',)
    related_select_fields = ['tour_package']



@admin.register(Review)
class ReviewAdmin(OptimizedAdmin):
    list_display = ('tour_package', 'customer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('tour_package__title', 'customer__email', 'comment')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    related_select_fields = ['tour_package']



@admin.register(PackageOffer)
class PackageOfferAdmin(OptimizedAdmin):
    """
    Custom admin configuration for the PackageOffer model.
    """
    list_display = ('title', 'tour_package', 'discount_percentage', 'is_active', 'start_date', 'end_date', 'created_at')
    search_fields = ('title', 'tour_package__title')  # Enables search by offer title and associated tour package title
    list_filter = ('is_active', 'start_date', 'end_date')  # Filters for quick view on active status and date range
    ordering = ('-created_at',)  # Orders by the latest created offers
    related_select_fields = ['tour_package']

    def discount_percentage(self, obj):
        """
        Fetch the calculated discount percentage as a column in the admin.
        """
        return f"{obj.discount_percentage}%"

    discount_percentage.short_description = "Discount Percentage"  # Column header in admin
    
    
#CUSTOM ADMIN SITE REGISTRATION FOR PACKAGE MANAGEMENT

class PackageAdminSite(AdminSite):
    """
    A custom AdminSite with personalized configurations.
    """
    site_header = _("Tour Management System Admin")
    site_title = _("Tour Management Admin Portal")
    index_title = _("Welcome to the Tour Management Admin")

    def each_context(self, request):
        """
        Custom context for the admin dashboard.
        """
        context = super().each_context(request)
        context['custom_message'] = _("Manage your tours, packages, and reviews effectively!")
        return context
    
# Create an instance of the custom admin site
package_admin_site = PackageAdminSite(name='custom_admin_site')


# Manually register models with the custom admin site (without decorators)
package_admin_site.register(Category, CategoryAdmin)
package_admin_site.register(TourPackage, TourPackageAdmin)
package_admin_site.register(Destination, DestinationAdmin)
package_admin_site.register(Itinerary, ItineraryAdmin)
package_admin_site.register(PackageMedia, PackageMediaAdmin)
package_admin_site.register(Review, ReviewAdmin)
package_admin_site.register(PackageOffer, PackageOfferAdmin)