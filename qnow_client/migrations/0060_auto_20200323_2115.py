# Generated by Django 2.2.2 on 2020-03-24 00:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0059_auto_20200323_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 4, 7, 21, 15, 52, 950766), verbose_name='Validade(Data)'),
        ),
    ]
