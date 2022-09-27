from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.models import Account
import uuid
from customuser.models import User_Account
from contractors.models import Contractor


class Transaction_type(models.Model):
    transaction_type = models.CharField(max_length=255)


    def __str__(self):
        return self.transaction_type

    class Meta:
        verbose_name = 'Transaction Type'
        verbose_name_plural = 'Transactions Types'


class Transaction(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(max_length=28, blank=True, null=True)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    account = ForeignKey(Account, related_name='accounts', on_delete=models.CASCADE)
    contractor = ForeignKey(Contractor, on_delete=models.CASCADE)
    sum_of_transactions = models.DecimalField(decimal_places=2, max_digits=30)
    transaction_type = models.CharField(max_length=255)

    transaction_date = models.DateTimeField(
        verbose_name=_("transaction date"), default=timezone.now,
    )
    creation_date = models.DateTimeField(
        verbose_name=_("creation date"), default=timezone.now,
    )

    def __str__(self):
        return self.transaction_type

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
