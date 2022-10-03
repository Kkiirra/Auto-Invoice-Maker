import uuid

from django.db import models
from django.db.models import ForeignKey

from accounts.models import Account
from company.models import Company
from contractors.models import Contractor
from customuser.models import User_Account
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from orders.models import Order
from products.models import Product


class Invoice_status(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Invoice status'
        verbose_name_plural = 'Invoice stats'


class Invoice(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE)

    invoice_name = models.CharField(max_length=255)
    company = ForeignKey(Company, on_delete=models.CASCADE)
    account = ForeignKey(Account, on_delete=models.CASCADE)
    invoice_status = ForeignKey(Invoice_status, on_delete=models.CASCADE)
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
        return f'Invoice # {self.invoice_name} ({self.invoice_sum} {self.currency})'

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        unique_together = 'invoice_name', 'user_account'


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


