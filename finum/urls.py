from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customuser.views import password_email_request
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('user/password_reset/', password_email_request, name='password_reset'),
    path('user/', include('django.contrib.auth.urls')),
    path('', include('customuser.urls', namespace='customuser')),
    path('', include('company.urls', namespace='company')),
    path('', include('accounts.urls', namespace='accounts')),
    path('', include('transactions.urls', namespace='transactions')),
    path('', include('orders.urls', namespace='orders')),
    path('', include('contractors.urls', namespace='contractors')),
    path('', include('subscription.urls', namespace='subscription')),
    path('', include('dashboard.urls', namespace='dashboard')),
    path('', include('products.urls', namespace='products')),
    path('', include('invoice.urls', namespace='invoice')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
