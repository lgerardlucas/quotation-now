# Generated by Django 2.2.2 on 2020-03-28 01:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_provider', '0048_auto_20200327_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationprice',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 4, 6, 22, 14, 11, 478964), verbose_name='Validade da Cotação'),
        ),
    ]