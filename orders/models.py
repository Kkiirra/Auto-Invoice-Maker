from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone
from company.models import Company
from customuser.models import User_Account
from contractors.models import Contractor
from django.utils.translation import gettext_lazy as _
import uuid


class Order_status(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status


    class Meta:
        verbose_name = 'Order status'
        verbose_name_plural = 'Order stats'


class Order(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_name = models.CharField(max_length=255, unique=True)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    company = ForeignKey(Company, on_delete=models.CASCADE)
    contractor = ForeignKey(Contractor, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255)
    order_sum = models.DecimalField(decimal_places=2, max_digits=30)
    order_status = ForeignKey(Order_status, on_delete=models.CASCADE, blank=True, null=True)

    order_date = models.DateTimeField(
        verbose_name=_("order date"), default=timezone.now,
    )

    creation_date = models.DateTimeField(
        verbose_name=_("creation date"), default=timezone.now,
    )

    def __str__(self):
        return self.order_name

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

