from django.forms import ModelForm

from company.models import Company
from .models import Account


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['account_id', 'account_description', 'bank', 'currency', 'company']


    def __init__(self, user, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)

        self.fields['company'].queryset = Company.objects.filter(user_account=user)
