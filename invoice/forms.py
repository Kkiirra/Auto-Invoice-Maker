from django.forms import ModelForm

from accounts.models import Account
from company.models import Company
from orders.models import Order
from .models import Invoice
from django import forms


class InvoiceForm(ModelForm):
    invoice_date = forms.DateField(input_formats=['%d.%m.%Y'])

    class Meta:
        model = Invoice
        fields = [
            'invoice_name', 'company', 'account', 'invoice_status', 'currency', 'invoice_sum', 'order', 'invoice_date'
        ]


    def __init__(self, user, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)

        self.fields['company'].queryset = Company.objects.filter(user_account=user)
        self.fields['order'].queryset = Order.objects.filter(user_account=user)
        self.fields['account'].queryset = Account.objects.filter(user_account=user)
