# Generated by Django 2.2.2 on 2019-11-01 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_provider', '0011_auto_20191101_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationprice',
            name='quotation_value',
            field=models.FloatField(default=0.0, verbose_name='Valor da Cotação'),
        ),
    ]
