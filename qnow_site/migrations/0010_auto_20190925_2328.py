# Generated by Django 2.2.2 on 2019-09-26 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_site', '0009_auto_20190925_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='return_send',
            field=models.BooleanField(default=False, verbose_name='E-mail respondido?'),
        ),
    ]
