# Generated by Django 4.0 on 2022-09-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0008_bank_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank_account',
            name='data',
            field=models.JSONField(blank=True, db_index=True, null=True),
        ),
    ]