# Generated by Django 4.0 on 2022-09-01 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_contractor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_sum',
            field=models.DecimalField(decimal_places=2, max_digits=30),
        ),
    ]
