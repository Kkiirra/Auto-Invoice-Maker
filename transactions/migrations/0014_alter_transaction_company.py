# Generated by Django 4.0 on 2022-10-02 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_company_company_name'),
        ('transactions', '0013_alter_transaction_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
    ]
