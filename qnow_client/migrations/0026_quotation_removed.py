# Generated by Django 2.2.2 on 2019-09-11 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_client', '0025_auto_20190830_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='removed',
            field=models.BooleanField(default=False),
        ),
    ]