from django.contrib import admin
from .models import ServiceCategory, Service, ServiceOption, ServiceImage, ServiceReview


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'emoji', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


class ServiceOptionInline(admin.TabularInline):
    model = ServiceOption
    extra = 0


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 0


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'estimated_time', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    ordering = ('category', 'name')
    inlines = [ServiceOptionInline, ServiceImageInline]


@admin.register(ServiceOption)
class ServiceOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'price', 'is_active', 'created_at')
    list_filter = ('service__category', 'is_active', 'created_at')
    search_fields = ('name', 'service__name')
    ordering = ('service', 'name')


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ('service', 'alt_text', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('service__name', 'alt_text')
    ordering = ('-is_primary', 'created_at')


@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('user__email', 'service__name', 'comment')
    ordering = ('-created_at',)