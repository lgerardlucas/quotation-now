# Generated by Django 2.2.2 on 2020-03-11 02:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_provider', '0021_auto_20200310_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationprice',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 3, 20, 23, 18, 36, 968481), verbose_name='Validade da Cotação'),
        ),
    ]