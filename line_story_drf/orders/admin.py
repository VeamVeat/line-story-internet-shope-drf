from django.contrib import admin
from orders.models import Order, CartItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity', 'final_price', 'products', 'address', 'is_active')

    list_filter = ('final_price',)

    search_fields = ('final_price',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'product_id', 'quantity')

    search_fields = ('product',)

