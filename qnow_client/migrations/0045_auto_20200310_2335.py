# Generated by Django 2.2.2 on 2020-03-11 02:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0044_auto_20200310_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 4, 9, 23, 35, 3, 430801), verbose_name='Validade da Cotação'),
        ),
    ]
