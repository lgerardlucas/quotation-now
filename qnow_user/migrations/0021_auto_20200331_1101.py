# Generated by Django 2.2.2 on 2020-03-31 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnow_user', '0020_auto_20200330_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='information',
            field=models.TextField(blank=True, max_length=200, verbose_name='Conquistando o Cliente'),
        ),
    ]
