# Generated by Django 2.2.2 on 2020-03-11 03:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0051_auto_20200310_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 4, 10, 0, 0, 18, 252663), verbose_name='Validade(Data)'),
        ),
    ]
