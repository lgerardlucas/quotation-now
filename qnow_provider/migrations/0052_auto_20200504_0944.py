# Generated by Django 2.2.2 on 2020-05-04 12:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_provider', '0051_auto_20200331_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationprice',
            name='cancel_comments',
            field=models.TextField(blank=True, verbose_name='Comentário Sobre o Cancelamento do Preço'),
        ),
        migrations.AddField(
            model_name='quotationprice',
            name='cancel_quotation',
            field=models.BooleanField(default=False, verbose_name='Cancelar Preço(S/N)'),
        ),
        migrations.AlterField(
            model_name='quotationprice',
            name='date_create',
            field=models.DateField(default=datetime.date.today, verbose_name='Data do Lançamento'),
        ),
        migrations.AlterField(
            model_name='quotationprice',
            name='date_validate',
            field=models.DateField(default=datetime.datetime(2020, 5, 14, 9, 44, 38, 400925), verbose_name='Validade da Cotação'),
        ),
    ]
