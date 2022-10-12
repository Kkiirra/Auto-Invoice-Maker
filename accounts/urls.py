from django.urls import path
from .views import accounts, delete_account, account_edit


app_name = 'accounts'

urlpatterns = [
    path('profile/accounts/', accounts, name='accounts'),
    path('delete_account/', delete_account, name='delete_account'),
    path('profile/accounts/<uuid:ac_uid>/', account_edit, name='account_edit')
]
