# Generated by Django 2.2.2 on 2020-03-25 14:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0072_auto_20200323_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 4, 9, 11, 37, 53, 504993), verbose_name='Validade(Data)'),
        ),
    ]
