# Generated by Django 2.2.2 on 2020-03-31 14:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0076_auto_20200330_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 4, 15, 11, 1, 47, 991337), verbose_name='Validade(Data)'),
        ),
    ]