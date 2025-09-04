from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.ServiceCategoryViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'options', views.ServiceOptionViewSet)
router.register(r'reviews', views.ServiceReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]