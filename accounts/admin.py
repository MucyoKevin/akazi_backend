from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CustomerProfile, ServiceProvider, OTPVerification

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'phone_number', 'is_phone_verified', 'location')}),
    )
    list_display = ['username', 'phone_number', 'user_type', 'is_phone_verified', 'date_joined']
    list_filter = ['user_type', 'is_phone_verified']

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_bookings', 'rating']
    search_fields = ['user__username', 'user__phone_number']

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['user', 'hourly_rate', 'is_available', 'rating', 'is_verified']
    list_filter = ['is_available', 'is_verified']
    search_fields = ['user__username', 'user__phone_number']

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'is_verified', 'created_at', 'expires_at']
    list_filter = ['is_verified']

admin.site.register(User, CustomUserAdmin)
