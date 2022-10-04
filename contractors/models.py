import uuid
from customuser.models import User_Account
from django.db import models


class Contractor(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    contractor_name = models.CharField(max_length=255)

    def __str__(self):
        return self.contractor_name

    class Meta:
        verbose_name = 'Contractor'
        verbose_name_plural = 'Contractors'
        unique_together = 'contractor_name', 'user_account'
