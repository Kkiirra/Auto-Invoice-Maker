from django.urls import path
from .views import products, add_product, delete_product, product_edit, delete_item

app_name = 'products'

urlpatterns = [
    path('products/', products, name='products'),
    path('add_product/', add_product, name='add_product'),
    path('delete_product/', delete_product, name='delete_product'),
    path('product/<uuid:prod_uid>/', product_edit, name='product_edit'),
    path('products/delete_item/', delete_item, name='delete_item'),
]
