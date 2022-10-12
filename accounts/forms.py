from django.forms import ModelForm
from .models import Account


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['account_id', 'account_description', 'bank', 'currency', 'company']


    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     print(self.cleaned_data)
    #     if Account.objects.filter(account_id=cleaned_data['account_id'], user_account=self.user_account):
    #         self.add_error('account_id', 'Account with this Name already exists')
    #
    #     return cleaned_data
