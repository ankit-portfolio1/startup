from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import ContactMessage, FAQ, SiteConfiguration, Banner, Notification
from .serializers import (
    ContactMessageSerializer, FAQSerializer, SiteConfigurationSerializer,
    BannerSerializer, NotificationSerializer
)


class ContactMessageViewSet(viewsets.ModelViewSet):
    """ViewSet for contact messages"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save()


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for FAQs"""
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['question', 'answer', 'category']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', 'created_at']
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all FAQ categories"""
        categories = FAQ.objects.filter(is_active=True).values_list('category', flat=True).distinct()
        return Response(list(categories))


class SiteConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for site configuration"""
    queryset = SiteConfiguration.objects.filter(is_active=True)
    serializer_class = SiteConfigurationSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['key', 'value', 'description']
    ordering_fields = ['key', 'created_at']
    ordering = ['key']
    
    @action(detail=False, methods=['get'])
    def by_key(self, request):
        """Get configuration value by key"""
        key = request.query_params.get('key')
        if not key:
            return Response(
                {'error': 'Key parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            config = SiteConfiguration.objects.get(key=key, is_active=True)
            return Response({'key': config.key, 'value': config.value})
        except SiteConfiguration.DoesNotExist:
            return Response(
                {'error': 'Configuration not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for banners"""
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for notifications"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'is_read', 'is_active']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        # Get user-specific notifications and general notifications
        return Notification.objects.filter(
            models.Q(user=user) | models.Q(user__isnull=True),
            is_active=True
        )
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})