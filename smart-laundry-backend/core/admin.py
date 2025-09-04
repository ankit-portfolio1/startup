from django.contrib import admin
from .models import ContactMessage, FAQ, SiteConfiguration, Banner, Notification


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_active', 'order', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('question', 'answer', 'category')
    ordering = ('order', 'created_at')


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('key', 'value', 'description')
    ordering = ('key',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    ordering = ('order', '-created_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'is_active', 'created_at')
    list_filter = ('notification_type', 'is_read', 'is_active', 'created_at')
    search_fields = ('title', 'message', 'user__email')
    ordering = ('-created_at',)