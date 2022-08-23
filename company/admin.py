from django.contrib import admin
from .models import Company, Currency, Bank
from accounts.models import Account


class AccountAdmin(admin.StackedInline):
    model = Account
    max_num = 2


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [AccountAdmin]
    list_display = ['company_name', 'uid']

    class Meta:
        model = Company


admin.site.register(Account)
admin.site.register(Currency)
admin.site.register(Bank)
