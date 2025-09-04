from rest_framework import serializers
from decimal import Decimal
from .models import Order, OrderItem, Cart, OrderTracking, Payment
from services.serializers import ServiceSerializer, ServiceOptionSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_option = ServiceOptionSerializer(read_only=True)
    service_id = serializers.IntegerField(write_only=True)
    service_option_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'service', 'service_option', 'service_id', 'service_option_id',
                 'quantity', 'unit_price', 'total_price', 'item_description', 
                 'special_instructions', 'created_at')
        read_only_fields = ('id', 'unit_price', 'total_price', 'created_at')
    
    def create(self, validated_data):
        from services.models import Service, ServiceOption
        
        service_id = validated_data.pop('service_id')
        service_option_id = validated_data.pop('service_option_id', None)
        
        service = Service.objects.get(id=service_id)
        service_option = None
        
        if service_option_id:
            service_option = ServiceOption.objects.get(id=service_option_id)
            validated_data['unit_price'] = service_option.price
        else:
            validated_data['unit_price'] = service.price
        
        validated_data['service'] = service
        validated_data['service_option'] = service_option
        validated_data['total_price'] = validated_data['unit_price'] * validated_data['quantity']
        
        return super().create(validated_data)


class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = ('id', 'status', 'description', 'location', 'created_at')
        read_only_fields = ('id', 'created_at')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'payment_method', 'amount', 'status', 'transaction_id', 
                 'payment_gateway_response', 'created_at')
        read_only_fields = ('id', 'created_at')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    tracking = OrderTrackingSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'user_email', 'user_name', 'status', 
                 'payment_status', 'payment_method', 'pickup_address', 'delivery_address',
                 'subtotal', 'tax_amount', 'delivery_charge', 'total_amount',
                 'pickup_date', 'delivery_date', 'special_instructions', 'notes',
                 'items', 'tracking', 'payments', 'created_at', 'updated_at')
        read_only_fields = ('id', 'order_number', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        # Calculate totals
        items_data = self.context.get('items_data', [])
        subtotal = Decimal('0.00')
        
        for item_data in items_data:
            if 'service_option_id' in item_data and item_data['service_option_id']:
                from services.models import ServiceOption
                service_option = ServiceOption.objects.get(id=item_data['service_option_id'])
                item_total = service_option.price * item_data['quantity']
            else:
                from services.models import Service
                service = Service.objects.get(id=item_data['service_id'])
                item_total = service.price * item_data['quantity']
            
            subtotal += item_total
        
        # Calculate tax and delivery charge
        tax_amount = subtotal * Decimal('0.18')  # 18% GST
        delivery_charge = Decimal('50.00')  # Fixed delivery charge
        total_amount = subtotal + tax_amount + delivery_charge
        
        validated_data['subtotal'] = subtotal
        validated_data['tax_amount'] = tax_amount
        validated_data['delivery_charge'] = delivery_charge
        validated_data['total_amount'] = total_amount
        
        order = super().create(validated_data)
        
        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        # Create initial tracking entry
        OrderTracking.objects.create(
            order=order,
            status='pending',
            description='Order placed successfully'
        )
        
        return order


class CartSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_option = ServiceOptionSerializer(read_only=True)
    service_id = serializers.IntegerField(write_only=True)
    service_option_id = serializers.IntegerField(write_only=True, required=False)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ('id', 'service', 'service_option', 'service_id', 'service_option_id',
                 'quantity', 'total_price', 'created_at', 'updated_at')
        read_only_fields = ('id', 'total_price', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Update quantity
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


class CartSummarySerializer(serializers.Serializer):
    """Serializer for cart summary"""
    total_items = serializers.IntegerField()
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    items = CartSerializer(many=True)