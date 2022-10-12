from django.urls import path
from .views import signup, signin, signout, settings, \
    password_reset_request, activate_link, email_send_success, \
    email_invalid, bad_request, deactivate_user

app_name = 'customuser'

urlpatterns = [
    path('profile/settings/', settings, name='settings'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('password_reset_request/', password_reset_request, name='password_reset_request'),
    path('activate/<uidb64>/<token>/', activate_link,
            name='activate'),
    path('activate-email-link/done/', email_send_success, name='email_send_success'),
    path('email-invalid-link/', email_invalid, name='email_invalid'),
    path('bad_request/', bad_request, name='bad_request'),
    path('deactivate/', deactivate_user, name='deactivate'),
]
