from django.urls import path
from .views import integrations_view, integrations_response, integrate_account, add_invoices


app_name = 'integrations'

urlpatterns = [
    path('integrations/', integrations_view, name='integrations'),
    path('integration-response/', integrations_response, name='integrations_response'),
    path('integrate-account/', integrate_account, name='integrate_account'),
    path('add_invoices', add_invoices, name='add_invoices'),
]
