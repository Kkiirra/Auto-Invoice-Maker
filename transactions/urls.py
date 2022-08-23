from django.urls import path
from .views import transactions_view, add_transaction, delete_transaction, transaction_edit

app_name = 'transactions'

urlpatterns = [
    path('transactions/', transactions_view, name="transactions_list"),
    path('add/transaction/', add_transaction, name='add_transaction'),
    path('delete/transaction/', delete_transaction, name='delete_transaction'),
    path('transactions/<uuid:tr_uid>/', transaction_edit, name='transaction_edit'),
]
