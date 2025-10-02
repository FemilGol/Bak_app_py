from django.contrib import admin
from .models import Product, CartItem, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'id')
    search_fields = ('name', 'description')
    list_filter = ('price',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price_calculated')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('total_price_calculated',) 


class OrderItemInline(admin.TabularInline): 
    model = OrderItem
    extra = 0 
    readonly_fields = ('product', 'quantity', 'price_at_purchase', 'total_price') 
    fields = ('product', 'quantity', 'price_at_purchase', 'total_price') 


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'payment_method', 'order_date', 'is_completed')
    list_filter = ('payment_method', 'is_completed', 'order_date')
    search_fields = ('user__username', 'payment_method', 'upi_id')
    readonly_fields = ('user', 'total_amount', 'payment_method', 'upi_id', 'order_date') 
    inlines = [OrderItemInline] #
    fieldsets = (
        (None, {
            'fields': ('user', 'total_amount', 'payment_method', 'upi_id', 'order_date', 'is_completed')
        }),
    )
