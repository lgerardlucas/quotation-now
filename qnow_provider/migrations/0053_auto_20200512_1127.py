# Generated by Django 2.2.2 on 2020-05-12 14:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_provider', '0052_auto_20200504_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationprice',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 5, 22, 11, 27, 4, 119976), verbose_name='Validade da Cotação'),
        ),
    ]