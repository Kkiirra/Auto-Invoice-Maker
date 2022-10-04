# Generated by Django 4.0 on 2022-10-02 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0008_invoice_status_invoice_invoice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=30),
            preserve_default=False,
        ),
    ]