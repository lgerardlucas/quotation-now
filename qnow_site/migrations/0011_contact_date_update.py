# Generated by Django 2.2.2 on 2019-09-26 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_site', '0010_auto_20190925_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='date_update',
            field=models.DateField(auto_now=True, verbose_name='Última ação'),
        ),
    ]
