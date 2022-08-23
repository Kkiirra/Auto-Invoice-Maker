from django.urls import path
from .views import contractors_list, delete_contractor, contractor_edit
app_name = 'contractors'


urlpatterns = [
    path('contractors/', contractors_list, name='contractors'),
    path('delete_contractor/', delete_contractor, name='delete_contractor'),
    path('contractors/<uuid:contr_uid>/', contractor_edit, name='contractor_edit'),
]
