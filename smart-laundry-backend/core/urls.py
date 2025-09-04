from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'contact', views.ContactMessageViewSet)
router.register(r'faqs', views.FAQViewSet)
router.register(r'config', views.SiteConfigurationViewSet)
router.register(r'banners', views.BannerViewSet)
router.register(r'notifications', views.NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]