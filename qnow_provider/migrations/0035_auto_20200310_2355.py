# Generated by Django 2.2.2 on 2020-03-11 02:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_provider', '0034_auto_20200310_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationprice',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 3, 20, 23, 55, 54, 365936), verbose_name='Validade da Cotação'),
        ),
    ]
