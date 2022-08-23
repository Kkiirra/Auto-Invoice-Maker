from django.urls import path
from .views import subscription_view

app_name = 'subscription'

urlpatterns = [
    path('profile/subscription/', subscription_view, name='subscription'),
]
