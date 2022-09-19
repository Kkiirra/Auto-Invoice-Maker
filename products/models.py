from django.db import models
from customuser.models import User_Account
import uuid
# from invoice.models import Invoice
from orders.models import Order


class Product(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(decimal_places=2, max_digits=30)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'



class OrderItem(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_account = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product} + {self.quantity} + {self.order}'

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'


# class InvoiceItem(models.Model):
#     uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#
#     def __str__(self):
#         return self.uid
#
#     class Meta:
#         verbose_name = 'Order Item'
#         verbose_name_plural = 'Order Items'