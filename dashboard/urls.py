from django.urls import path
from .views import dashboard, date_dashboard

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/<str:date>/', date_dashboard, name='dashboard_date'),
]
