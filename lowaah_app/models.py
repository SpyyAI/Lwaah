from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class UserProfile(models.Model):
    """
    User profile for storing personal information.
    Designed for deaf/mute users to save data once and reuse.
    """
    # Unique identifier (can be email, phone, or auto-generated)
    profile_id = models.CharField(max_length=50, unique=True, primary_key=True)
    
    # Personal Information
    full_name = models.CharField(max_length=200, help_text="Full name in Arabic/English")
    national_id = models.CharField(
        max_length=10, 
        validators=[RegexValidator(r'^\d{10}$', 'Must be 10 digits')],
        help_text="National ID (10 digits)"
    )
    
    # Profile Picture (for visual identification)
    profile_picture = models.ImageField(
        upload_to='profiles/', 
        null=True, 
        blank=True,
        help_text="Profile picture for visual identification"
    )
    
    # Contact Information (optional)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Active status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.full_name} ({self.profile_id})"


class CarPlate(models.Model):
    """
    Car license plate information linked to user profile.
    Users can have multiple cars.
    """
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='car_plates')
    
    # Plate Information
    plate_number = models.CharField(
        max_length=20,
        help_text="License plate number (e.g., ABC 1234)"
    )
    plate_letters = models.CharField(
        max_length=10,
        help_text="Plate letters in Arabic"
    )
    
    # Car Details (for visual identification)
    car_icon = models.CharField(
        max_length=10,
        default='🚗',
        help_text="Emoji icon for car type"
    )
    car_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Friendly name (e.g., 'My Red Car')"
    )
    car_color = models.CharField(
        max_length=50,
        blank=True,
        help_text="Car color for visual identification"
    )
    
    # Status
    is_primary = models.BooleanField(default=False, help_text="Primary car for quick selection")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', '-created_at']
        verbose_name = 'Car Plate'
        verbose_name_plural = 'Car Plates'
    
    def __str__(self):
        return f"{self.plate_number} - {self.profile.full_name}"
    
    def save(self, *args, **kwargs):
        # If this is set as primary, unset other primary plates for this profile
        if self.is_primary:
            CarPlate.objects.filter(profile=self.profile, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

