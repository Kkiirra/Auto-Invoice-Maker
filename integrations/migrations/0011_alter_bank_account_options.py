# Generated by Django 4.0 on 2022-10-09 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0010_remove_bank_account_id_bank_account_uid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bank_account',
            options={'verbose_name': 'Bank Account', 'verbose_name_plural': 'Bank Accounts'},
        ),
    ]
