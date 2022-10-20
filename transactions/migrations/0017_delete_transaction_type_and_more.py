# Generated by Django 4.0 on 2022-10-17 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0016_remove_transaction_invoice_transaction_invoice'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transaction_type',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('exp', 'Expenses'), ('inc', 'Income')], max_length=255),
        ),
    ]