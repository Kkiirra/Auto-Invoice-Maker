from django.db import models
from django.utils import timezone
from company.models import Company
from django.utils.translation import gettext_lazy as _
from customuser.models import User_Account
import uuid


class Account(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.CharField(max_length=255)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='accounts', on_delete=models.CASCADE)
    account_description = models.TextField(blank=True, null=True)
    bank = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)

    date_joined = models.DateTimeField(
        verbose_name=_("date joined"), default=timezone.now,
    )

    def __str__(self):
        return f'{self.currency} - {self.account_id} - {self.bank}'

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
