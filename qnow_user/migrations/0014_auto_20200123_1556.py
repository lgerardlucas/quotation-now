# Generated by Django 2.2.2 on 2020-01-23 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_user', '0013_auto_20200123_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='approved',
            field=models.BooleanField(blank=True, default=False, verbose_name='Mov/Autorizada'),
        ),
    ]
