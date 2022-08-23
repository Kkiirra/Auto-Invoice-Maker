from django.urls import path
from .views import orders_view, delete_order, add_order, order_edit


app_name = 'orders'

urlpatterns = [
    path('orders/', orders_view, name='orders_list'),
    path('delete_order/', delete_order, name='delete_order'),
    path('add_transaction/', add_order, name='add_order'),
    path('orders/<uuid:ord_uid>/', order_edit, name='order_edit')
]
