# Generated by Django 2.2.2 on 2020-03-24 00:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0058_auto_20200323_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 4, 7, 21, 15, 12, 986978), verbose_name='Validade(Data)'),
        ),
    ]