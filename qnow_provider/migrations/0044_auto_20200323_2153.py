# Generated by Django 2.2.2 on 2020-03-24 00:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_provider', '0043_auto_20200322_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationprice',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 4, 2, 21, 53, 51, 610942), verbose_name='Validade da Cotação'),
        ),
    ]