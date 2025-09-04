from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ServiceCategory(models.Model):
    """Service categories like Steam Pressing, Dry Cleaning, etc."""
    
    name = models.CharField(max_length=100, unique=True)
    emoji = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_categories'
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Service(models.Model):
    """Individual services within a category"""
    
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estimated_time = models.DurationField(help_text="Estimated time to complete this service")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['category', 'name']
        unique_together = ['category', 'name']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"


class ServiceOption(models.Model):
    """Service options with different prices (e.g., Shirt, T-Shirt, Kurta)"""
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_options'
        verbose_name = 'Service Option'
        verbose_name_plural = 'Service Options'
        ordering = ['service', 'name']
        unique_together = ['service', 'name']
    
    def __str__(self):
        return f"{self.service.name} - {self.name}"


class ServiceImage(models.Model):
    """Images for services"""
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='services/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'service_images'
        verbose_name = 'Service Image'
        verbose_name_plural = 'Service Images'
        ordering = ['-is_primary', 'created_at']
    
    def __str__(self):
        return f"{self.service.name} - Image"


class ServiceReview(models.Model):
    """Customer reviews for services"""
    
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='service_reviews')
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_reviews'
        verbose_name = 'Service Review'
        verbose_name_plural = 'Service Reviews'
        ordering = ['-created_at']
        unique_together = ['service', 'user']
    
    def __str__(self):
        return f"{self.user.email} - {self.service.name} - {self.rating} stars"