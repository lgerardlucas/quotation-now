# Generated by Django 2.2.2 on 2020-03-13 19:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0053_auto_20200311_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 4, 12, 16, 42, 59, 902702), verbose_name='Validade(Data)'),
        ),
    ]