from django.contrib import admin
from .models import Order, Order_status
from products.models import OrderItem

admin.site.register(Order)
admin.site.register(Order_status)
admin.site.register(OrderItem)

