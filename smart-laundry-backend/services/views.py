from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import ServiceCategory, Service, ServiceOption, ServiceImage, ServiceReview
from .serializers import (
    ServiceCategorySerializer, ServiceSerializer, ServiceDetailSerializer,
    ServiceOptionSerializer, ServiceImageSerializer, ServiceReviewSerializer
)


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for service categories"""
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        """Get all services for a specific category"""
        category = self.get_object()
        services = category.services.filter(is_active=True)
        serializer = ServiceSerializer(services, many=True, context={'request': request})
        return Response(serializer.data)


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for services"""
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'category__name']
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['category', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDetailSerializer
        return ServiceSerializer
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get reviews for a specific service"""
        service = self.get_object()
        reviews = service.reviews.filter(is_approved=True)
        serializer = ServiceReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, pk=None):
        """Add a review for a service"""
        service = self.get_object()
        serializer = ServiceReviewSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Check if user already reviewed this service
            if ServiceReview.objects.filter(service=service, user=request.user).exists():
                return Response(
                    {'error': 'You have already reviewed this service'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(service=service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for service options"""
    queryset = ServiceOption.objects.filter(is_active=True)
    serializer_class = ServiceOptionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['service', 'service__category']
    search_fields = ['name', 'service__name']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['service', 'name']


class ServiceReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for service reviews"""
    queryset = ServiceReview.objects.filter(is_approved=True)
    serializer_class = ServiceReviewSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['service', 'rating', 'user']
    search_fields = ['comment', 'service__name', 'user__email']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']