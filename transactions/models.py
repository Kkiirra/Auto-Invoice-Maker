from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.models import Account
from company.models import Company
from customuser.models import User_Account
from contractors.models import Contractor
from invoice.models import Invoice
import uuid


class Transaction(models.Model):

    transaction_types = (
        ('exp', 'Expenses'),
        ('inc', 'Income'),
    )

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(max_length=28, blank=True, null=True)
    transaction_type = models.CharField(max_length=255, choices=transaction_types)
    sum_of_transactions = models.DecimalField(decimal_places=2, max_digits=30)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    company = ForeignKey(Company, on_delete=models.CASCADE)
    account = ForeignKey(Account, related_name='accounts', on_delete=models.CASCADE)
    contractor = ForeignKey(Contractor, on_delete=models.CASCADE)
    invoice = ForeignKey(Invoice, blank=True, null=True, related_name='transactions', on_delete=models.SET_NULL)

    transaction_date = models.DateTimeField(
        verbose_name=_("transaction date"), default=timezone.now,
    )
    creation_date = models.DateTimeField(
        verbose_name=_("creation date"), default=timezone.now,
    )


    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        unique_together = 'transaction_id', 'user_account'

    def __str__(self):
        return self.transaction_type
