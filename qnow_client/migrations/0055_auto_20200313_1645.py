# Generated by Django 2.2.2 on 2020-03-13 19:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0054_auto_20200313_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 4, 12, 16, 45, 21, 457310), verbose_name='Validade(Data)'),
        ),
    ]
