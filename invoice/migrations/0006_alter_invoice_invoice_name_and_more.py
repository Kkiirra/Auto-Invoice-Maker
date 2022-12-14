# Generated by Django 4.0 on 2022-10-02 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0006_alter_user_account_default_currency_and_more'),
        ('invoice', '0005_alter_invoiceitem_invoice_alter_invoiceitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together={('invoice_name', 'user_account')},
        ),
    ]
