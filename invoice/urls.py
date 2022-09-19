from django.urls import path
from .views import invoice


app_name = 'invoice'

urlpatterns = [
    path('invoice/', invoice, name='invoice')
]
