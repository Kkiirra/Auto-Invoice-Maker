# Generated by Django 4.0 on 2022-10-02 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_company_company_name'),
        ('transactions', '0010_alter_transaction_invoice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
    ]
