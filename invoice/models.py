import uuid

from django.db import models
from django.db.models import ForeignKey
from django.db.models import Sum

from accounts.models import Account
from company.models import Company
from contractors.models import Contractor
from customuser.models import User_Account
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from orders.models import Order
from products.models import Product


class Invoice(models.Model):

    draft = 'Draft'
    sent = 'Sent'
    paid = 'Paid'
    paid_part = 'Partially Paid'
    canceled = 'Canceled'

    invoice_stats = (
        (draft, 'Draft'),
        (sent, 'Sent'),
        (paid, 'Paid'),
        (paid_part, 'Partially Paid'),
        (canceled, 'Canceled'),
    )


    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE)

    invoice_name = models.CharField(max_length=255)
    company = ForeignKey(Company, on_delete=models.CASCADE)
    account = ForeignKey(Account, on_delete=models.CASCADE)
    invoice_status = models.CharField(max_length=255, choices=invoice_stats)
    contractor = ForeignKey(Contractor, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255)
    invoice_sum = models.DecimalField(decimal_places=2, max_digits=30)

    order = ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)

    invoice_date = models.DateTimeField(
        verbose_name=_("Invoice date"), default=timezone.now,
    )

    creation_date = models.DateTimeField(
        verbose_name=_("Creation date"), default=timezone.now,
    )

    def __str__(self):
        return f'# {self.invoice_name} ({self.invoice_sum} {self.currency})'

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        unique_together = 'invoice_name', 'user_account'


    def save(self, *args, **kwargs):
        transactions_sum = self.transactions.all().aggregate(Sum('sum_of_transactions')).get('sum_of_transactions__sum', None)
        if transactions_sum is not None:
            if self.invoice_sum <= transactions_sum:
                self.invoice_status = Invoice.paid
            elif self.invoice_sum > transactions_sum and transactions_sum is not None:
                self.invoice_status = Invoice.paid_part
            else:
                self.invoice_status = Invoice.draft
        else:
            self.invoice_status = Invoice.draft
        super(Invoice, self).save(*args, **kwargs)


class InvoiceItem(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_inv')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items_inv')
    price = models.DecimalField(decimal_places=2, max_digits=30, blank=True, default=0)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'
