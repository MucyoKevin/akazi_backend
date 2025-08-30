from django.contrib import admin
from .models import Booking, BookingAvailability

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'provider', 'service', 'scheduled_date', 'status', 'total_amount']
    list_filter = ['status', 'scheduled_date', 'created_at']
    search_fields = ['customer__username', 'provider__user__username', 'service__name']

@admin.register(BookingAvailability)
class BookingAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['provider', 'date', 'is_available']
    list_filter = ['is_available', 'date']
    search_fields = ['provider__user__username']
