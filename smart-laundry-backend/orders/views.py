from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from decimal import Decimal
from .models import Order, OrderItem, Cart, OrderTracking, Payment
from .serializers import (
    OrderSerializer, OrderItemSerializer, CartSerializer, 
    OrderTrackingSerializer, PaymentSerializer, CartSummarySerializer
)
from services.models import Service, ServiceOption


class CartViewSet(viewsets.ModelViewSet):
    """ViewSet for cart operations"""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get cart summary with totals"""
        cart_items = self.get_queryset()
        
        total_items = sum(item.quantity for item in cart_items)
        subtotal = sum(item.total_price for item in cart_items)
        tax_amount = subtotal * Decimal('0.18')  # 18% GST
        delivery_charge = Decimal('50.00')  # Fixed delivery charge
        total_amount = subtotal + tax_amount + delivery_charge
        
        summary_data = {
            'total_items': total_items,
            'subtotal': subtotal,
            'tax_amount': tax_amount,
            'delivery_charge': delivery_charge,
            'total_amount': total_amount,
            'items': CartSerializer(cart_items, many=True, context={'request': request}).data
        }
        
        serializer = CartSummarySerializer(summary_data)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        """Update quantity of a cart item"""
        cart_item = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        if quantity <= 0:
            cart_item.delete()
            return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = CartSerializer(cart_item, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Clear all items from cart"""
        self.get_queryset().delete()
        return Response({'message': 'Cart cleared successfully'}, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for orders"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'payment_method']
    search_fields = ['order_number', 'user__email']
    ordering_fields = ['created_at', 'total_amount', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def tracking(self, request, pk=None):
        """Get order tracking information"""
        order = self.get_object()
        tracking = order.tracking.all()
        serializer = OrderTrackingSerializer(tracking, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update order status (admin only)"""
        if request.user.role != 'admin':
            return Response(
                {'error': 'Only admins can update order status'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        order = self.get_object()
        new_status = request.data.get('status')
        description = request.data.get('description', f'Status updated to {new_status}')
        location = request.data.get('location', '')
        
        if new_status not in [choice[0] for choice in Order.STATUS_CHOICES]:
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = new_status
        order.save()
        
        # Create tracking entry
        OrderTracking.objects.create(
            order=order,
            status=new_status,
            description=description,
            location=location
        )
        
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        
        if order.status in ['delivered', 'cancelled']:
            return Response(
                {'error': 'Cannot cancel this order'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        # Create tracking entry
        OrderTracking.objects.create(
            order=order,
            status='cancelled',
            description='Order cancelled by customer'
        )
        
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for order items"""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['order', 'service', 'service_option']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=user)


class OrderTrackingViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for order tracking"""
    queryset = OrderTracking.objects.all()
    serializer_class = OrderTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['order', 'status']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return OrderTracking.objects.all()
        return OrderTracking.objects.filter(order__user=user)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for payments"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['order', 'payment_method', 'status']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Payment.objects.all()
        return Payment.objects.filter(order__user=user)