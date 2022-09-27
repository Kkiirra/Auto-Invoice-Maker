import uuid

from django.db import models
from customuser.models import User_Account


class Bank_Account(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE, related_name='bank_account')
    name = models.CharField(max_length=255, default=None)
    data = models.JSONField(db_index=True, blank=True, null=True)


    def __str__(self):
        return self.name
