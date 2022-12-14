# Generated by Django 4.0 on 2022-10-16 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0015_alter_invoice_invoice_status'),
        ('transactions', '0015_alter_transaction_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='invoice',
        ),
        migrations.AddField(
            model_name='transaction',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='invoice.invoice'),
        ),
    ]
