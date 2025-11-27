from django.contrib import admin
from .models import UserProfile, CarPlate


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for User Profiles."""
    list_display = ('profile_id', 'full_name', 'national_id', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('profile_id', 'full_name', 'national_id', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('profile_id', 'full_name', 'national_id', 'profile_picture')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CarPlate)
class CarPlateAdmin(admin.ModelAdmin):
    """Admin interface for Car Plates."""
    list_display = ('plate_number', 'profile', 'car_icon', 'is_primary', 'is_active', 'created_at')
    list_filter = ('is_primary', 'is_active', 'created_at')
    search_fields = ('plate_number', 'plate_letters', 'car_name', 'profile__full_name')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Plate Information', {
            'fields': ('profile', 'plate_number', 'plate_letters')
        }),
        ('Car Details', {
            'fields': ('car_icon', 'car_name', 'car_color')
        }),
        ('Status', {
            'fields': ('is_primary', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

