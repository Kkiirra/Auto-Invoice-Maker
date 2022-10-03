from django.urls import path
from .views import orders_view, delete_order, order_edit, order_add, change_status, get_product


app_name = 'orders'

urlpatterns = [
    path('orders/', orders_view, name='orders_list'),
    path('delete_order/', delete_order, name='delete_order'),
    path('orders/<uuid:ord_uid>/', order_edit, name='order_edit'),
    path('orders/add/', order_add, name='order_add'),
    path('orders/change_status/', change_status, name='change_status'),
    path('orders/get_product/', get_product, name='get_product')
]
