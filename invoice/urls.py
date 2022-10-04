from django.urls import path
from .views import invoice, invoice_add, delete_invoice, invoice_edit, invoice_byOrder, change_status


app_name = 'invoice'

urlpatterns = [
    path('invoice/', invoice, name='invoice'),
    path('invoice/add/', invoice_add, name='invoice_add'),
    path('invoice_delete/', delete_invoice, name='invoice_delete'),
    path('invoice/<uuid:inv_uid>/', invoice_edit, name='invoice_edit'),
    path('invoice/by-order/<uuid:ord_uid>/', invoice_byOrder, name='invoice_byOrder'),
    path('change_status/', change_status, name='change_status')
]
