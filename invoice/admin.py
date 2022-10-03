from django.contrib import admin
from .models import Invoice, InvoiceItem, Invoice_status

admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Invoice_status)

# Register your models here.
