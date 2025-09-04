from rest_framework import serializers
from .models import ServiceCategory, Service, ServiceOption, ServiceImage, ServiceReview


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ('id', 'image', 'alt_text', 'is_primary')


class ServiceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOption
        fields = ('id', 'name', 'emoji', 'price', 'is_active')


class ServiceReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = ServiceReview
        fields = ('id', 'user_name', 'user_email', 'rating', 'comment', 'created_at')
        read_only_fields = ('id', 'user_name', 'user_email', 'created_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ServiceSerializer(serializers.ModelSerializer):
    options = ServiceOptionSerializer(many=True, read_only=True)
    images = ServiceImageSerializer(many=True, read_only=True)
    reviews = ServiceReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ('id', 'name', 'emoji', 'description', 'price', 'estimated_time', 
                 'is_active', 'options', 'images', 'reviews', 'average_rating', 
                 'review_count', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(review.rating for review in reviews) / reviews.count(), 1)
        return 0
    
    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()


class ServiceCategorySerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    service_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceCategory
        fields = ('id', 'name', 'emoji', 'description', 'is_active', 
                 'services', 'service_count', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def get_service_count(self, obj):
        return obj.services.filter(is_active=True).count()


class ServiceDetailSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    options = ServiceOptionSerializer(many=True, read_only=True)
    images = ServiceImageSerializer(many=True, read_only=True)
    reviews = ServiceReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ('id', 'category', 'name', 'emoji', 'description', 'price', 
                 'estimated_time', 'is_active', 'options', 'images', 'reviews', 
                 'average_rating', 'review_count', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(review.rating for review in reviews) / reviews.count(), 1)
        return 0
    
    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()