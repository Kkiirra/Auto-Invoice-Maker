from django.urls import path
from django.views.generic import RedirectView

from .views import companies_list, delete_company, company_edit


app_name = 'company'

urlpatterns = [
    path('profile/companies/', companies_list, name='companies'),
    path('profile/companies/<uuid:com_uid>/', company_edit, name='this_company'),
    path('delete_company/', delete_company, name='delete_company'),
    path('', RedirectView.as_view(url='/dashboard/', permanent=True)),
]
