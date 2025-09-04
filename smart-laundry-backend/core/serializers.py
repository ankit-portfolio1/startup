from rest_framework import serializers
from .models import ContactMessage, FAQ, SiteConfiguration, Banner, Notification


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ('id', 'name', 'email', 'phone', 'subject', 'message', 'status', 'created_at')
        read_only_fields = ('id', 'status', 'created_at')
    
    def create(self, validated_data):
        return ContactMessage.objects.create(**validated_data)


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer', 'category', 'is_active', 'order', 'created_at')
        read_only_fields = ('id', 'created_at')


class SiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = ('id', 'key', 'value', 'description', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'subtitle', 'image', 'link_url', 'is_active', 'order', 'created_at')
        read_only_fields = ('id', 'created_at')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'title', 'message', 'notification_type', 'is_read', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')