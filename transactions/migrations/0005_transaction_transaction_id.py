# Generated by Django 4.0 on 2022-09-22 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_transaction_sum_of_transactions'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=28, null=True),
        ),
    ]
