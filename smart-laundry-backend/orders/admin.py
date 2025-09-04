from django.contrib import admin
from .models import Order, OrderItem, Cart, OrderTracking, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)


class OrderTrackingInline(admin.TabularInline):
    model = OrderTracking
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'user__email', 'user__phone')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [OrderItemInline, OrderTrackingInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Payment', {
            'fields': ('payment_status', 'payment_method')
        }),
        ('Address', {
            'fields': ('pickup_address', 'delivery_address')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'tax_amount', 'delivery_charge', 'total_amount')
        }),
        ('Schedule', {
            'fields': ('pickup_date', 'delivery_date')
        }),
        ('Additional Info', {
            'fields': ('special_instructions', 'notes')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'service', 'service_option', 'quantity', 'unit_price', 'total_price')
    list_filter = ('service__category', 'created_at')
    search_fields = ('order__order_number', 'service__name', 'item_description')
    ordering = ('-created_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'service_option', 'quantity', 'created_at')
    list_filter = ('service__category', 'created_at')
    search_fields = ('user__email', 'service__name')
    ordering = ('-created_at',)


@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'description', 'location', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__order_number', 'description', 'location')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'status', 'transaction_id', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('order__order_number', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)