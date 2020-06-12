# Generated by Django 2.2.2 on 2020-05-12 14:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0078_auto_20200504_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='view_environment_quotation_home',
            field=models.BooleanField(default=False, verbose_name='Mostrar Foto do Ambiente na Home'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='view_project_quotation_home',
            field=models.BooleanField(default=False, verbose_name='Mostrar Foto do Projeto na Home'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 5, 27, 11, 27, 2, 189115), verbose_name='Validade(Data)'),
        ),
    ]