# Generated by Django 4.0 on 2022-09-29 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0006_alter_user_account_default_currency_and_more'),
        ('invoice', '0003_invoiceitem_user_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='user_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customuser.user_account'),
        ),
    ]
