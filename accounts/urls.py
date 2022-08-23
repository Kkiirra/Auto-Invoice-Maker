from django.urls import path
from .views import accounts, delete_account, add_accounts, delete_this_account, company_add_account, account_edit


app_name = 'accounts'

urlpatterns = [
    path('profile/accounts/', accounts, name='accounts'),
    path('add_account/<uuid:com_uid>/', add_accounts, name='add_account'),
    path('company_add_account/<uuid:com_uid>/', company_add_account, name='company_add_account'),
    path('delete_this_account/<uuid:com_uid>/<uuid:ac_uid>/', delete_this_account, name='delete_this_account'),
    path('delete_account/', delete_account, name='delete_account'),
    path('profile/accounts/<uuid:ac_uid>/', account_edit, name='account_edit')
]
