# Generated by Django 2.2.2 on 2020-03-11 02:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_provider', '0026_auto_20200310_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationprice',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 3, 20, 23, 22, 11, 285956), verbose_name='Validade da Cotação'),
        ),
    ]
