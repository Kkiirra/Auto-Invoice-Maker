# Generated by Django 4.0 on 2022-09-24 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customuser', '0006_alter_user_account_default_currency_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank_Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(db_index=True)),
                ('user_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customuser.user_account')),
            ],
        ),
    ]
