from django.urls import path
from .views import transactions_view, add_transaction, delete_transaction, transaction_edit, get_invoice_val, \
    get_transaction_company, delete_invoice, add_invoice, load_transactions

app_name = 'transactions'

urlpatterns = [
    path('transactions/', transactions_view, name="transactions_list"),
    path('add/transaction/', add_transaction, name='add_transaction'),
    path('delete/transaction/', delete_transaction, name='delete_transaction'),
    path('transactions/<uuid:tr_uid>/', transaction_edit, name='transaction_edit'),
    path('get_invoice_val/', get_invoice_val, name='get_invoice_val'),
    path('get_transaction_company/', get_transaction_company, name='get_transaction_company'),
    path('delete_invoice/', delete_invoice, name='delete_invoice'),
    path('add_invoice/', add_invoice, name='add_invoice'),
    path('load_transactions/', load_transactions, name='load_transactions')
]
