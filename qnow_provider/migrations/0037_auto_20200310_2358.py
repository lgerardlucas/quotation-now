# Generated by Django 2.2.2 on 2020-03-11 02:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_provider', '0036_auto_20200310_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationprice',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 3, 20, 23, 58, 0, 456609), verbose_name='Validade da Cotação'),
        ),
    ]
