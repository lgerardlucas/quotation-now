# Generated by Django 2.2.2 on 2019-08-15 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0004_auto_20190813_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pendente'), (1, 'Em Análise'), (2, 'Liberado'), (3, 'Orçado'), (4, 'Finalizado'), (5, 'Cancelado'), (6, 'Destativodo')], default=0),
        ),
    ]
