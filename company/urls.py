from django.urls import path
from django.views.generic import RedirectView

from .views import companies_list, delete_company, this_company, start_company


app_name = 'company'

urlpatterns = [
    path('profile/companies/', companies_list, name='companies'),
    path('profile/companies/<uuid:com_uid>/', this_company, name='this_company'),
    path('delete_company/', delete_company, name='delete_company'),
    path('', RedirectView.as_view(url='/dashboard/', permanent=True)),
    path('start_company/', start_company, name='start_company'),
]
