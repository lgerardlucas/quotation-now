# Generated by Django 2.2.2 on 2019-08-27 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0018_auto_20190824_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationstage',
            name='explication',
            field=models.CharField(default='Aguardando texto...', max_length=200),
        ),
    ]
