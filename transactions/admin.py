from django.contrib import admin
from .models import Transaction, Contractor, Transaction_type

admin.site.register(Transaction)
admin.site.register(Contractor)
admin.site.register(Transaction_type)
