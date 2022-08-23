from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from customuser.models import User_Account
import uuid


class Currency(models.Model):

    currency = models.CharField(max_length=255)

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class Bank(models.Model):

    bank_name = models.CharField(max_length=255)

    def __str__(self):
        return self.bank_name

    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'


class Company(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    user = ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_joined = models.DateTimeField(
        verbose_name=_("date joined"), default=timezone.now,
    )

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
