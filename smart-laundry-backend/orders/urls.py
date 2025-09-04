from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'items', views.OrderItemViewSet)
router.register(r'cart', views.CartViewSet)
router.register(r'tracking', views.OrderTrackingViewSet)
router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]