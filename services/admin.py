from django.contrib import admin
from .models import ServiceCategory, Service, Review, ServicePackage

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'base_price', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'category__name']

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'price', 'duration_display', 'is_popular', 'is_active']
    list_filter = ['service', 'is_popular', 'is_active']
    search_fields = ['name', 'service__name']
    ordering = ['service', 'price']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'provider', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['customer__username', 'provider__user__username']
