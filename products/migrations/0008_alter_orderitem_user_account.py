# Generated by Django 4.0 on 2022-09-19 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0006_alter_user_account_default_currency_and_more'),
        ('products', '0007_orderitem_user_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='user_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customuser.user_account'),
        ),
    ]
