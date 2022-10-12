from django.forms import ModelForm
from .models import Invoice, InvoiceItem
from django import forms


class InvoiceForm(ModelForm):
    invoice_date = forms.DateField(input_formats=['%d.%m.%Y'])

    class Meta:
        model = Invoice
        fields = [
            'invoice_name', 'company', 'account', 'invoice_status', 'currency', 'invoice_sum', 'order'
        ]
