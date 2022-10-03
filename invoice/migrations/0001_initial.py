# Generated by Django 4.0 on 2022-09-29 16:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0009_alter_order_order_name'),
        ('customuser', '0006_alter_user_account_default_currency_and_more'),
        ('contractors', '0002_alter_contractor_contractor_name'),
        ('company', '0004_alter_company_company_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invoice_name', models.CharField(max_length=255, unique=True)),
                ('currency', models.CharField(max_length=255)),
                ('invoice_sum', models.DecimalField(decimal_places=2, max_digits=30)),
                ('invoice_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Invoice date')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation date')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contractors.contractor')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.order')),
                ('user_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customuser.user_account')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
    ]
